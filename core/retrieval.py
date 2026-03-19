"""
HaMoach - ChromaDB retrieval helpers.
"""

from __future__ import annotations

from typing import Callable

import chromadb

from core.config import TOP_K
from core.embeddings import (
    DEFAULT_COLLECTION_NAME,
    embed_text,
    get_chroma_client,
    get_collection,
)

EmbeddingFunction = Callable[[str], list[float]]


def cosine_similarity_from_distance(distance: float) -> float:
    similarity = 1.0 - float(distance)
    return max(0.0, min(1.0, similarity))


def retrieve_chunks(
    query: str,
    client: chromadb.PersistentClient | None = None,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    top_k: int = TOP_K,
    embedding_fn: EmbeddingFunction | None = None,
) -> list[dict]:
    if not query.strip():
        return []

    client = client or get_chroma_client()
    collection = get_collection(client=client, name=collection_name)
    embed = embedding_fn or (lambda text: embed_text(text, prefix="search_query: "))

    results = collection.query(
        query_embeddings=[embed(query)],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved: list[dict] = []
    for document, metadata, distance in zip(documents, metadatas, distances):
        retrieved.append(
            {
                "text": document,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "score": cosine_similarity_from_distance(distance),
            }
        )

    return retrieved
