"""
HaMoach — Streamlit Study Assistant UI
=======================================
Chat interface with agent badges and retrieval sidebar.
"""

import streamlit as st
from pathlib import Path

from core.config import (
    AGENT_NAMES,
    CONFIDENCE_THRESHOLD,
    DOCS_FOLDER,
    GUARD_ENABLED,
    STREAMLIT_TITLE,
    STREAMLIT_SUBTITLE,
)
from core.config import SUPPORTED_EXTENSIONS
from core.embeddings import ingest_documents
from agents.specialists import run_pipeline, AgentResponse

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="HaMoach", page_icon="🧠", layout="wide")

# ---------------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_sources" not in st.session_state:
    st.session_state.last_sources = []
if "last_agent" not in st.session_state:
    st.session_state.last_agent = ""
if "docs_ingested" not in st.session_state:
    st.session_state.docs_ingested = False

# ---------------------------------------------------------------------------
# Sidebar — sources + ingestion
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("📚 Document Manager")

    # Ingest button
    docs_path = Path(DOCS_FOLDER)
    doc_count = 0
    if docs_path.exists():
        for ext in SUPPORTED_EXTENSIONS:
            doc_count += len(list(docs_path.glob(f"*{ext}")))

    st.caption(f"Found **{doc_count}** document(s) in `{DOCS_FOLDER}`")

    if st.button("🔄 Ingest Documents", use_container_width=True):
        with st.spinner("Embedding documents..."):
            try:
                stats = ingest_documents(docs_path=DOCS_FOLDER, reset_collection=True)
                st.session_state.docs_ingested = True
                st.success(
                    f"Ingested **{stats['documents']}** docs → "
                    f"**{stats['chunks']}** chunks"
                )
            except Exception as e:
                st.error(f"Ingestion failed: {e}")

    if st.session_state.docs_ingested:
        st.caption("✅ Documents loaded into ChromaDB")

    # File uploader for adding new docs
    st.divider()
    st.subheader("Upload New Documents")
    uploaded = st.file_uploader(
        "Add documents",
        type=["md", "txt", "pdf"],
        accept_multiple_files=True,
    )
    if uploaded:
        docs_path.mkdir(parents=True, exist_ok=True)
        for f in uploaded:
            target = docs_path / f.name
            target.write_bytes(f.getvalue())
            st.caption(f"Saved: {f.name}")
        st.info("Click 'Ingest Documents' to embed the new files.")

    # Retrieved chunks display
    st.divider()
    st.subheader("🔍 Last Retrieved Chunks")

    if st.session_state.last_sources:
        for i, src in enumerate(st.session_state.last_sources, 1):
            score = src.get("relevance_score", src.get("score", 0))
            doc = src.get("document", src.get("source", "?"))
            chunk_id = src.get("chunk_id", src.get("chunk_index", "?"))
            st.markdown(
                f"**{i}.** `{doc}` chunk {chunk_id} — "
                f"score: `{score:.2f}`"
            )
    else:
        st.caption("No retrieval yet — ask a question!")

    if st.session_state.last_agent:
        st.divider()
        if st.session_state.last_agent == "guard":
            st.caption("Last agent: 🛡️ Guard (blocked)")
        else:
            agent_display = AGENT_NAMES.get(
                st.session_state.last_agent, st.session_state.last_agent
            )
            st.caption(f"Last agent: {agent_display}")

    st.divider()
    st.caption(f"🛡️ Guard: {'Enabled' if GUARD_ENABLED else 'Disabled'}")

# ---------------------------------------------------------------------------
# Main chat area
# ---------------------------------------------------------------------------
st.title(STREAMLIT_TITLE)
st.caption(STREAMLIT_SUBTITLE)

# Replay conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("agent"):
            agent_display = AGENT_NAMES.get(msg["agent"], msg["agent"])
            confidence = msg.get("confidence", 0)
            st.caption(f"{agent_display} · confidence: {confidence:.0%}")

# Chat input
if user_input := st.chat_input("Ask about your course materials..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run pipeline
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result: AgentResponse = run_pipeline(user_input)

                st.markdown(result.answer)

                agent_display = AGENT_NAMES.get(result.agent_name, result.agent_name)
                confidence = result.confidence

                if confidence < CONFIDENCE_THRESHOLD:
                    st.warning("⚠️ Low confidence — answer may be incomplete.")

                st.caption(f"{agent_display} · confidence: {confidence:.0%}")

                # Update sidebar state
                st.session_state.last_sources = result.sources
                st.session_state.last_agent = result.agent_name

                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result.answer,
                    "agent": result.agent_name,
                    "confidence": confidence,
                })

            except Exception as e:
                error_msg = f"Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                })
