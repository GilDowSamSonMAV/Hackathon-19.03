from __future__ import annotations

from collections import Counter
import chromadb
from pathlib import Path
import re
from uuid import uuid4

from core.embeddings import ingest_documents
from core.retrieval import retrieve_chunks


def fake_embedding(text: str) -> list[float]:
    lowered = text.lower()
    counts = Counter(re.findall(r"[a-z_]+", lowered))
    return [
        float(counts.get("polymorphism", 0)),
    ]


def test_ingest_and_retrieve_polymorphism():
    source_docs = Path(__file__).resolve().parent.parent / "docs"
    scratch_dir = Path(__file__).resolve().parent / f"_tmp_rag_pipeline_{uuid4().hex}"
    collection_name = f"course_docs_{uuid4().hex}"
    docs_dir = scratch_dir / "docs"
    docs_dir.mkdir(parents=True)

    for doc_path in source_docs.glob("*.md"):
        (docs_dir / doc_path.name).write_text(
            doc_path.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    client = chromadb.Client()

    stats = ingest_documents(
        docs_path=docs_dir,
        client=client,
        collection_name=collection_name,
        embedding_fn=fake_embedding,
        reset_collection=True,
    )

    assert stats["documents"] == 5
    assert stats["chunks"] > 5

    results = retrieve_chunks(
        "What is polymorphism?",
        client=client,
        collection_name=collection_name,
        embedding_fn=fake_embedding,
    )

    assert results
    assert any(result["source"] == "intro_to_oop.md" for result in results)
    assert results[0]["source"] == "intro_to_oop.md"
