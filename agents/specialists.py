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


def _parse_specialist_response(raw: str, agent_name: str) -> AgentResponse:
    """Try to parse JSON from the specialist's response, with fallback."""
    # Try to find JSON in the response
    for match in re.finditer(r'\{[\s\S]*\}', raw):
        try:
            data = json.loads(match.group())
            # Concept explainer / exam coach
            answer = data.get("answer", "")
            # Exam coach might have "question" or "feedback" instead
            if not answer:
                answer = data.get("question", "")
            if not answer:
                answer = data.get("feedback", "")
            # Practice generator has "questions" list
            if not answer and "questions" in data:
                questions = data["questions"]
                formatted = []
                for q in questions:
                    formatted.append(
                        f"**Q ({q.get('difficulty', '?')}):** {q.get('question', '')}\n"
                        f"**A:** {q.get('answer', '')}\n"
                        f"*{q.get('explanation', '')}*"
                    )
                answer = "\n\n---\n\n".join(formatted)

            return AgentResponse(
                answer=answer or raw,
                sources=data.get("sources", []),
                confidence=float(data.get("confidence", 0.5)),
                agent_name=agent_name,
                raw_response=raw,
            )
        except (json.JSONDecodeError, ValueError, TypeError):
            continue

    # Fallback: return raw text as the answer
    return AgentResponse(
        answer=raw,
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
