"""
HaMoach — Specialist Agents
=============================
Three specialists, each using retrieval as a tool:
  - Concept Explainer: explains CS concepts from course materials
  - Practice Generator: creates practice questions from materials
  - Exam Coach: interactive oral exam simulation
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from agents.prompts import (
    CONCEPT_EXPLAINER_PROMPT,
    EXAM_COACH_PROMPT,
    PRACTICE_GENERATOR_PROMPT,
)
from core.agent_loop import run_agent
from core.config import CONFIDENCE_THRESHOLD, TOP_K
from core.retrieval import retrieve_chunks


@dataclass
class AgentResponse:
    answer: str
    sources: list[dict] = field(default_factory=list)
    confidence: float = 0.0
    agent_name: str = ""
    raw_response: str = ""


def _format_chunks_for_prompt(chunks: list[dict]) -> str:
    """Format retrieved chunks into text for injection into the prompt."""
    if not chunks:
        return "(No relevant course material found.)"

    parts: list[str] = []
    for i, chunk in enumerate(chunks, 1):
        score = chunk.get("score", 0.0)
        source = chunk.get("source", "unknown")
        text = chunk.get("text", "")
        parts.append(
            f"[Chunk {i}] (source: {source}, relevance: {score:.2f})\n{text}"
        )
    return "\n\n".join(parts)


def _find_json_objects(text: str) -> list[tuple[int, int, dict]]:
    """Find valid JSON objects in text by scanning for balanced braces.

    Returns a list of (start_index, end_index, parsed_dict) tuples.
    Uses a brace-counting approach instead of greedy regex to avoid
    matching from the first '{' to the last '}' across the entire response.
    """
    results = []
    i = 0
    while i < len(text):
        if text[i] == '{':
            depth = 0
            in_string = False
            escape_next = False
            for j in range(i, len(text)):
                ch = text[j]
                if escape_next:
                    escape_next = False
                    continue
                if ch == '\\' and in_string:
                    escape_next = True
                    continue
                if ch == '"' and not escape_next:
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        candidate = text[i:j + 1]
                        try:
                            data = json.loads(candidate)
                            if isinstance(data, dict):
                                results.append((i, j + 1, data))
                        except (json.JSONDecodeError, ValueError):
                            pass
                        break
        i += 1
    return results


def _strip_json_blocks(text: str) -> str:
    """Remove all JSON object blocks from text and clean up whitespace."""
    json_objects = _find_json_objects(text)
    if not json_objects:
        return text
    # Remove JSON blocks from end to start to preserve indices
    result = text
    for start, end, _ in reversed(json_objects):
        result = result[:start] + result[end:]
    # Clean up leftover whitespace / blank lines
    result = re.sub(r'\n{3,}', '\n\n', result).strip()
    return result


def _extract_answer_from_json(data: dict) -> str:
    """Extract the human-readable answer from a parsed JSON response."""
    # Direct answer fields (concept explainer, general)
    for key in ("answer", "question", "feedback"):
        val = data.get(key)
        if val and isinstance(val, str) and val.strip():
            return val.strip()

    # Practice generator: "questions" list
    if "questions" in data and isinstance(data["questions"], list):
        questions = data["questions"]
        formatted = []
        for i, q in enumerate(questions, 1):
            if not isinstance(q, dict):
                continue
            formatted.append(
                f"**Q{i} ({q.get('difficulty', '?')}):** {q.get('question', '')}\n"
                f"**Answer:** {q.get('answer', '')}\n"
                f"*{q.get('explanation', '')}*"
            )
        if formatted:
            return "\n\n---\n\n".join(formatted)

    # Exam coach evaluation with next_question
    parts = []
    if data.get("score"):
        parts.append(f"**Score:** {data['score']}/5")
    if data.get("feedback"):
        parts.append(f"**Feedback:** {data['feedback']}")
    if data.get("ideal_answer"):
        parts.append(f"**Ideal answer:** {data['ideal_answer']}")
    if data.get("next_question"):
        parts.append(f"\n{data['next_question']}")
    if parts:
        return "\n\n".join(parts)

    return ""


def _parse_specialist_response(raw: str, agent_name: str) -> AgentResponse:
    """Parse the specialist's response, stripping any leaked JSON.

    Strategy:
    1. Look for JSON objects in the response.
    2. If found, extract the answer field from JSON and also capture
       any natural-language text that appears BEFORE the JSON block.
    3. Prefer pre-JSON natural text (the LLM often writes a good answer
       then appends JSON). Fall back to the extracted JSON field.
    4. Always strip raw JSON from the final answer string.
    """
    json_objects = _find_json_objects(raw)

    if json_objects:
        # Use the first valid JSON object for metadata
        start, end, data = json_objects[0]

        # Text before the first JSON block (often the natural-language answer)
        pre_json_text = raw[:start].strip()
        # Text after the last JSON block
        post_json_text = raw[json_objects[-1][1]:].strip()

        # Extract answer from JSON fields
        json_answer = _extract_answer_from_json(data)

        # Decide which text to use as the answer:
        # - If there's substantial pre-JSON text, prefer it (the LLM wrote
        #   a natural response then appended JSON for structure)
        # - Otherwise use the extracted JSON answer
        if pre_json_text and len(pre_json_text) > 20:
            answer = pre_json_text
            # Append any post-JSON text too
            if post_json_text:
                answer += "\n\n" + post_json_text
        elif json_answer:
            answer = json_answer
        else:
            # Last resort: strip JSON from raw and use whatever remains
            answer = _strip_json_blocks(raw)

        # Final safety: strip any remaining JSON blocks from the answer
        answer = _strip_json_blocks(answer)

        return AgentResponse(
            answer=answer or raw,
            sources=data.get("sources", []),
            confidence=float(data.get("confidence", 0.5)),
            agent_name=agent_name,
            raw_response=raw,
        )

    # No JSON found — return raw text (now expected, since prompts ask
    # for natural language)
    return AgentResponse(
        answer=raw.strip(),
        sources=[],
        confidence=0.5,
        agent_name=agent_name,
        raw_response=raw,
    )


def _run_specialist(
    prompt_template: str,
    agent_name: str,
    user_input: str,
    chunks: list[dict] | None = None,
) -> AgentResponse:
    """
    Core specialist runner: retrieve chunks, inject into prompt, call LLM.

    Args:
        prompt_template: System prompt with {retrieved_chunks} placeholder.
        agent_name: Human-readable name for the agent.
        user_input: The student's question.
        chunks: Pre-retrieved chunks (if None, retrieves automatically).
    """
    if chunks is None:
        chunks = retrieve_chunks(user_input, top_k=TOP_K)

    formatted_chunks = _format_chunks_for_prompt(chunks)
    system_prompt = prompt_template.replace("{retrieved_chunks}", formatted_chunks)

    raw_response = run_agent(
        system_prompt=system_prompt,
        user_input=user_input,
    )

    result = _parse_specialist_response(raw_response, agent_name)

    # Attach retrieval sources if the LLM didn't include them
    if not result.sources and chunks:
        result.sources = [
            {
                "document": c["source"],
                "chunk_id": c["chunk_index"],
                "relevance_score": c["score"],
            }
            for c in chunks
        ]

    # Low-confidence guard
    if result.confidence < CONFIDENCE_THRESHOLD and not any(
        "don't have enough" in result.answer.lower()
        for _ in [1]
    ):
        result.answer += (
            "\n\n⚠️ *Low confidence — the course materials may not "
            "fully cover this topic.*"
        )

    return result


def concept_explainer(user_input: str, chunks: list[dict] | None = None) -> AgentResponse:
    """Explain a concept using retrieved course materials."""
    return _run_specialist(
        prompt_template=CONCEPT_EXPLAINER_PROMPT,
        agent_name="concept_explainer",
        user_input=user_input,
        chunks=chunks,
    )


def practice_generator(user_input: str, chunks: list[dict] | None = None) -> AgentResponse:
    """Generate practice questions from course materials."""
    return _run_specialist(
        prompt_template=PRACTICE_GENERATOR_PROMPT,
        agent_name="practice_generator",
        user_input=user_input,
        chunks=chunks,
    )


def exam_coach(user_input: str, chunks: list[dict] | None = None) -> AgentResponse:
    """Run an interactive exam coaching session."""
    return _run_specialist(
        prompt_template=EXAM_COACH_PROMPT,
        agent_name="exam_coach",
        user_input=user_input,
        chunks=chunks,
    )


# --- Full Pipeline: route → retrieve → specialist → response ---

SPECIALIST_MAP = {
    "concept_explainer": concept_explainer,
    "practice_generator": practice_generator,
    "exam_coach": exam_coach,
}


def run_pipeline(user_input: str) -> AgentResponse:
    """
    Full pipeline: guard → route → retrieve → specialist.

    Returns:
        AgentResponse with the specialist's answer, sources, and confidence.
        If blocked by guard, returns an AgentResponse with the block reason.
    """
    from agents.guard import check_input
    from agents.router import route_query

    # Layer 2: Guard agent
    guard_result = check_input(user_input)
    if guard_result.status == "BLOCKED":
        return AgentResponse(
            answer=f"🚫 **Message blocked**: {guard_result.reason}\n\n"
                   f"Please ask a study-related question about your course materials.",
            sources=[],
            confidence=1.0,
            agent_name="guard",
        )

    route = route_query(user_input)
    specialist_fn = SPECIALIST_MAP.get(route.agent, concept_explainer)

    # Retrieve once, pass to specialist (avoid double retrieval)
    chunks = retrieve_chunks(user_input, top_k=TOP_K)

    result = specialist_fn(user_input, chunks=chunks)
    result.agent_name = route.agent
    return result
