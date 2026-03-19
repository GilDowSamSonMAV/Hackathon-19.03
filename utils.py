# =============================================================================
# CONTEXT INJECTION TEMPLATE (used at runtime by all specialist agents)
# =============================================================================

def build_agent_prompt(system_prompt: str, user_query: str, retrieved_chunks: list[dict]) -> list[dict]:
    """
    Build the full message array for an Ollama API call.
    
    retrieved_chunks format:
    [
        {
            "document": "intro_to_oop.md",
            "chunk_id": "chunk_004",
            "text": "Polymorphism allows objects of different classes...",
            "score": 0.87
        }
    ]
    """
    # Format chunks as XML context block
    context_parts = []
    for i, chunk in enumerate(retrieved_chunks):
        context_parts.append(
            f'<chunk id="{chunk["chunk_id"]}" document="{chunk["document"]}" score="{chunk["score"]:.2f}">\n'
            f'{chunk["text"]}\n'
            f'</chunk>'
        )
    context_block = "\n".join(context_parts)
    
    user_message = (
        f"<context>\n{context_block}\n</context>\n\n"
        f"<question>\n{user_query}\n</question>\n\n"
        f"Respond in valid JSON only. No text outside the JSON."
    )
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
