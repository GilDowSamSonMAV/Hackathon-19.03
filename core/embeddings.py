"""
HaMoach - Document ingestion for ChromaDB.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import chromadb
import google.generativeai as genai

from core.config import (
    CHROMA_PERSIST_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DOCS_FOLDER,
    GEMINI_API_KEY,
    GEMINI_EMBED_MODEL,
    MIN_CHUNK_SIZE,
    SANITIZE_ON_INGEST,
)

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
from core.sanitizer import sanitize_document

DEFAULT_COLLECTION_NAME = "course_docs"
EmbeddingFunction = Callable[[str], list[float]]


@dataclass(frozen=True)
class ChunkRecord:
    chunk_id: str
    text: str
    source: str
    chunk_index: int


def get_chroma_client(path: str = CHROMA_PERSIST_DIR) -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=path)


def get_collection(
    client: chromadb.PersistentClient | None = None,
    name: str = DEFAULT_COLLECTION_NAME,
):
    client = client or get_chroma_client()
    return client.get_or_create_collection(
        name=name,
        metadata={"hf:space": "cosine"},
    )


def read_markdown_documents(docs_path: str | Path = DOCS_FOLDER) -> list[Path]:
    return sorted(Path(docs_path).glob("*.md"))


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
    min_chunk_size: int = MIN_CHUNK_SIZE,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0:
        raise ValueError("overlap cannot be negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()
        if len(chunk) >= min_chunk_size:
            chunks.append(chunk)

        if end >= text_length:
            break
        start = end - overlap

    return chunks


def embed_text(text: str, prefix: str) -> list[float]:
    """
    Get embeddings using Gemini.
    Prefix is used for context (e.g. 'search_document: ' or 'search_query: ').
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    # Gemini text-embedding-004 handles task_type. 
    # For RAG, we typically use RETRIEVAL_DOCUMENT for indexing and RETRIEVAL_QUERY for search.
    task_type = "RETRIEVAL_DOCUMENT" if "document" in prefix else "RETRIEVAL_QUERY"
    
    response = genai.embed_content(
        model=GEMINI_EMBED_MODEL,
        content=text,
        task_type=task_type,
        title="Course Document" if task_type == "RETRIEVAL_DOCUMENT" else None
    )
    
    return response["embedding"]


def build_chunk_records(docs_path: str | Path = DOCS_FOLDER) -> list[ChunkRecord]:
    records: list[ChunkRecord] = []

    for doc_path in read_markdown_documents(docs_path):
        content = doc_path.read_text(encoding="utf-8")
        if SANITIZE_ON_INGEST:
            content, _ = sanitize_document(doc_path.name, content)

        for chunk_index, chunk in enumerate(chunk_text(content)):
            records.append(
                ChunkRecord(
                    chunk_id=f"{doc_path.stem}:{chunk_index}",
                    text=chunk,
                    source=doc_path.name,
                    chunk_index=chunk_index,
                )
            )

    return records


def ingest_documents(
    docs_path: str | Path = DOCS_FOLDER,
    client: chromadb.PersistentClient | None = None,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    embedding_fn: EmbeddingFunction | None = None,
    reset_collection: bool = False,
) -> dict[str, int]:
    client = client or get_chroma_client()

    if reset_collection:
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

    collection = get_collection(client=client, name=collection_name)
    records = build_chunk_records(docs_path)
    embed = embedding_fn or (lambda text: embed_text(text, prefix="search_document: "))

    if not records:
        return {"documents": 0, "chunks": 0}

    collection.upsert(
        ids=[record.chunk_id for record in records],
        documents=[record.text for record in records],
        embeddings=[embed(record.text) for record in records],
        metadatas=[
            {
                "source": record.source,
                "chunk_index": record.chunk_index,
            }
            for record in records
        ],
    )

    return {
        "documents": len({record.source for record in records}),
        "chunks": len(records),
    }
