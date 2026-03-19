"""
Phase 2 tests — Agent loop, router, specialists, and full pipeline.

Uses monkeypatching to replace ollama.chat with deterministic fake responses,
so tests run without a live Ollama server.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4
import json
import re

import chromadb

from core.agent_loop import run_agent, _extract_tool_call
from core.embeddings import ingest_documents
from core.retrieval import retrieve_chunks
from agents.router import route_query, _parse_router_response, VALID_AGENTS
from agents.specialists import (
    concept_explainer,
    practice_generator,
    exam_coach,
    run_pipeline,
    AgentResponse,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fake_embedding(text: str) -> list[float]:
    """Deterministic embedding based on keyword frequency."""
    lowered = text.lower()
    counts = Counter(re.findall(r"[a-z_]+", lowered))
    return [
        float(counts.get("polymorphism", 0)),
        float(counts.get("inheritance", 0)),
        float(counts.get("encapsulation", 0)),
        float(counts.get("abstraction", 0)),
        float(counts.get("object", 0) + counts.get("objects", 0)),
        float(counts.get("class", 0) + counts.get("classes", 0)),
        float(counts.get("recursion", 0)),
        float(counts.get("sort", 0) + counts.get("sorting", 0)),
        float(counts.get("array", 0) + counts.get("arrays", 0)),
        1.0,
    ]


def _make_ollama_response(content: str) -> dict:
    return {"message": {"content": content}}


# ---------------------------------------------------------------------------
# Test: tool call extraction
# ---------------------------------------------------------------------------

def test_extract_tool_call_basic():
    text = 'I need to look this up. {"tool": "retrieve", "query": "polymorphism"}'
    result = _extract_tool_call(text)
    assert result is not None
    assert result == ("retrieve", "polymorphism")


def test_extract_tool_call_no_match():
    assert _extract_tool_call("Just a normal response with no tools.") is None


# ---------------------------------------------------------------------------
# Test: agent loop with mocked ollama
# ---------------------------------------------------------------------------

def test_agent_loop_no_tools():
    """Agent returns a direct answer when no tools are available."""
    with patch("core.agent_loop.ollama") as mock_ollama:
        mock_ollama.chat.return_value = _make_ollama_response("Polymorphism is...")
        result = run_agent("You are a tutor.", "What is polymorphism?")
        assert "Polymorphism" in result
        mock_ollama.chat.assert_called_once()


def test_agent_loop_with_tool_call():
    """Agent calls a tool, gets result, then produces final answer."""
    call_count = 0

    def fake_chat(**kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return _make_ollama_response(
                '{"tool": "retrieve", "query": "polymorphism"}'
            )
        return _make_ollama_response(
            "Based on the retrieved material, polymorphism means..."
        )

    def fake_tool(query: str) -> str:
        return "Polymorphism allows objects to take many forms."

    with patch("core.agent_loop.ollama") as mock_ollama:
        mock_ollama.chat.side_effect = fake_chat
        result = run_agent(
            "You are a tutor.",
            "What is polymorphism?",
            tools={"retrieve": fake_tool},
        )
        assert "polymorphism" in result.lower()
        assert call_count == 2


def test_agent_loop_max_rounds():
    """Agent stops after MAX_TOOL_ROUNDS even if it keeps calling tools."""

    def always_tool_call(**kwargs):
        return _make_ollama_response('{"tool": "retrieve", "query": "loop"}')

    def fake_tool(query: str) -> str:
        return "result"

    with patch("core.agent_loop.ollama") as mock_ollama:
        mock_ollama.chat.side_effect = always_tool_call
        result = run_agent(
            "system", "user", tools={"retrieve": fake_tool}
        )
        # Should have been called MAX_TOOL_ROUNDS + 1 times (initial + 3 retries)
        assert mock_ollama.chat.call_count == 4


# ---------------------------------------------------------------------------
# Test: router parsing
# ---------------------------------------------------------------------------

def test_parse_router_response_valid():
    raw = '{"agent": "concept_explainer", "confidence": 0.95, "reasoning": "Asking for definition"}'
    result = _parse_router_response(raw)
    assert result.agent == "concept_explainer"
    assert result.confidence == 0.95


def test_parse_router_response_invalid_agent():
    raw = '{"agent": "unknown_agent", "confidence": 0.9, "reasoning": "test"}'
    result = _parse_router_response(raw)
    assert result.agent == "concept_explainer"  # Falls back to default


def test_parse_router_response_garbage():
    result = _parse_router_response("I don't know what to do")
    assert result.agent == "concept_explainer"
    assert result.confidence == 0.3


def test_route_query_mocked():
    """Full route_query with mocked ollama."""
    router_json = '{"agent": "practice_generator", "confidence": 0.93, "reasoning": "Student wants practice"}'
    with patch("core.agent_loop.ollama") as mock_ollama:
        mock_ollama.chat.return_value = _make_ollama_response(router_json)
        result = route_query("Give me 3 practice questions about arrays")
        assert result.agent == "practice_generator"
        assert result.confidence == 0.93


# ---------------------------------------------------------------------------
# Test: specialists with mocked retrieval + ollama
# ---------------------------------------------------------------------------

def _setup_chroma_with_docs() -> tuple[chromadb.Client, Path]:
    """Ingest docs into an in-memory ChromaDB and return (client, docs_dir)."""
    source_docs = Path(__file__).resolve().parent.parent / "docs"
    scratch_dir = Path(__file__).resolve().parent / f"_tmp_phase2_{uuid4().hex}"
    docs_dir = scratch_dir / "docs"
    docs_dir.mkdir(parents=True)

    for doc_path in source_docs.glob("*.md"):
        (docs_dir / doc_path.name).write_text(
            doc_path.read_text(encoding="utf-8"), encoding="utf-8"
        )

    client = chromadb.Client()
    ingest_documents(
        docs_path=docs_dir,
        client=client,
        collection_name="course_docs",
        embedding_fn=fake_embedding,
        reset_collection=True,
    )
    return client, docs_dir


def test_concept_explainer_returns_answer():
    """Concept explainer produces an answer with sources."""
    client, _ = _setup_chroma_with_docs()
    chunks = retrieve_chunks(
        "What is polymorphism?",
        client=client,
        collection_name="course_docs",
        embedding_fn=fake_embedding,
    )

    specialist_response = json.dumps({
        "answer": "Polymorphism allows objects of different classes to respond to the same method call.",
        "sources": [{"document": "intro_to_oop.md", "chunk_id": 0, "relevance_score": 0.92}],
        "confidence": 0.9,
    })

    with patch("core.agent_loop.ollama") as mock_ollama:
        mock_ollama.chat.return_value = _make_ollama_response(specialist_response)
        result = concept_explainer("What is polymorphism?", chunks=chunks)

    assert isinstance(result, AgentResponse)
    assert "polymorphism" in result.answer.lower()
    assert result.confidence >= 0.5
    assert result.sources


def test_practice_generator_returns_questions():
    """Practice generator produces questions."""
    client, _ = _setup_chroma_with_docs()
    chunks = retrieve_chunks(
        "recursion practice",
        client=client,
        collection_name="course_docs",
        embedding_fn=fake_embedding,
    )

    specialist_response = json.dumps({
        "questions": [
            {
                "question": "What is the base case in recursion?",
                "difficulty": "easy",
                "answer": "The condition that stops recursive calls.",
                "explanation": "Without a base case, recursion would be infinite.",
                "source_document": "recursion.md",
            }
        ],
        "sources": [{"document": "recursion.md", "chunk_id": 0, "relevance_score": 0.85}],
        "confidence": 0.88,
    })

    with patch("core.agent_loop.ollama") as mock_ollama:
        mock_ollama.chat.return_value = _make_ollama_response(specialist_response)
        result = practice_generator("Give me practice questions on recursion", chunks=chunks)

    assert isinstance(result, AgentResponse)
    assert "base case" in result.answer.lower()


def test_exam_coach_asks_question():
    """Exam coach asks a question in asking mode."""
    client, _ = _setup_chroma_with_docs()
    chunks = retrieve_chunks(
        "sorting algorithms",
        client=client,
        collection_name="course_docs",
        embedding_fn=fake_embedding,
    )

    specialist_response = json.dumps({
        "mode": "asking",
        "question": "What is the time complexity of merge sort?",
        "difficulty": "medium",
        "hint": "Think about divide and conquer.",
        "sources": [{"document": "sorting_algorithms.md", "chunk_id": 0, "relevance_score": 0.9}],
        "confidence": 0.92,
    })

    with patch("core.agent_loop.ollama") as mock_ollama:
        mock_ollama.chat.return_value = _make_ollama_response(specialist_response)
        result = exam_coach("Quiz me on sorting", chunks=chunks)

    assert isinstance(result, AgentResponse)
    assert "merge sort" in result.answer.lower()


# ---------------------------------------------------------------------------
# Test: full pipeline (router → retrieval → specialist)
# ---------------------------------------------------------------------------

def test_full_pipeline_polymorphism():
    """
    End-to-end: 'What is polymorphism?' → routes to concept_explainer →
    retrieves from intro_to_oop.md → returns explanation.
    """
    client, _ = _setup_chroma_with_docs()

    call_count = 0

    def mock_chat(**kwargs):
        nonlocal call_count
        call_count += 1
        messages = kwargs.get("messages", [])
        system_msg = messages[0]["content"] if messages else ""

        # First call is the guard
        if "security classifier" in system_msg.lower():
            return _make_ollama_response('{"status": "SAFE"}')

        # Second call is the router
        if "query router" in system_msg.lower():
            return _make_ollama_response(json.dumps({
                "agent": "concept_explainer",
                "confidence": 0.95,
                "reasoning": "Student asks for concept definition",
            }))

        # Third call is the concept explainer
        return _make_ollama_response(json.dumps({
            "answer": "Polymorphism is one of the four pillars of OOP. It allows objects of different types to be treated through a common interface.",
            "sources": [{"document": "intro_to_oop.md", "chunk_id": 2, "relevance_score": 0.91}],
            "confidence": 0.92,
        }))

    with patch("core.agent_loop.ollama") as mock_ollama, \
         patch("core.retrieval.get_chroma_client", return_value=client), \
         patch("core.retrieval.embed_text", side_effect=lambda text, prefix: fake_embedding(text)):
        mock_ollama.chat.side_effect = mock_chat
        result = run_pipeline("What is polymorphism?")

    assert result.agent_name == "concept_explainer"
    assert "polymorphism" in result.answer.lower()
    assert result.confidence >= 0.5
    assert call_count == 3  # guard + router + specialist
