# HaMoach — Cursor Agent Prompts
# ================================
# Paste each prompt into Cursor Agent Mode at the corresponding hackathon phase.
# Each prompt is self-contained and references the files already in the project.


# =============================================================================
# PHASE 1A — Ingestion Pipeline (Gil, 0:30-1:00)
# Paste this into Cursor Agent Mode:
# =============================================================================

CURSOR_PROMPT_INGESTION = """
Build the document ingestion pipeline in core/ingestion.py for the HaMoach study assistant.

REQUIREMENTS:
1. Read all .md, .txt, and .pdf files from a given folder path
2. For each document:
   - Read content (for .md and .txt, read as UTF-8; for .pdf, extract text using PyPDF2 or pdfplumber)
   - Sanitize content using core/sanitizer.py's sanitize_document() function
   - Split into chunks of ~500 characters with 50 character overlap
   - Use a simple recursive character splitter (split on \\n\\n first, then \\n, then '. ', then ' ')
   - Discard chunks shorter than 100 characters
3. Embed each chunk using Ollama's nomic-embed-text model
4. Store in ChromaDB with metadata: {source: filename, chunk_index: int, total_chunks: int}
5. Persist ChromaDB to ./chroma_db/

USE THESE IMPORTS:
- import ollama
- import chromadb
- from core.config import (CHUNK_SIZE, CHUNK_OVERLAP, MIN_CHUNK_SIZE,
                           EMBED_MODEL, CHROMA_COLLECTION, CHROMA_PERSIST_DIR,
                           SANITIZE_ON_INGEST)
- from core.sanitizer import sanitize_document

FUNCTIONS TO IMPLEMENT:
- read_document(filepath: str) -> str
- chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]
- embed_text(text: str) -> list[float]
- ingest_folder(folder_path: str) -> dict  (returns stats: num_docs, num_chunks, etc.)
- get_or_create_collection() -> chromadb.Collection

Keep it simple — no LangChain, no abstractions. Raw Python.
The agents/prompts.py and core/config.py files already exist — read them for constants.
"""


# =============================================================================
# PHASE 1B — Retrieval Function (Gil, 1:00-1:30)
# Paste this into Cursor Agent Mode:
# =============================================================================

CURSOR_PROMPT_RETRIEVAL = """
Build the retrieval function in core/retrieval.py for the HaMoach study assistant.

This module is used as a TOOL by the specialist agents. It takes a query string,
embeds it, searches ChromaDB, and returns the top-k most relevant chunks with metadata.

REQUIREMENTS:
1. Embed the query using Ollama's nomic-embed-text model
2. Query ChromaDB for the top-k nearest chunks (k from config)
3. Return results with: chunk text, source document, chunk_index, distance score
4. Convert ChromaDB distance to a relevance score (1.0 = perfect match, 0.0 = irrelevant)
   ChromaDB uses L2 distance by default — lower distance = more relevant
   Simple conversion: relevance = max(0, 1 - distance/2)
5. If no chunks have relevance > config.CONFIDENCE_THRESHOLD, return empty results
   with a flag indicating insufficient information

USE THESE IMPORTS:
- import ollama
- import chromadb
- from core.config import (EMBED_MODEL, TOP_K, CONFIDENCE_THRESHOLD,
                           CHROMA_COLLECTION, CHROMA_PERSIST_DIR)

FUNCTIONS TO IMPLEMENT:
- retrieve(query: str, top_k: int = None) -> dict
  Returns: {
    "chunks": [{"text": str, "source": str, "chunk_index": int, "relevance": float}],
    "has_relevant_info": bool,
    "avg_relevance": float
  }
- format_chunks_for_prompt(chunks: list[dict]) -> str
  Formats retrieved chunks as XML for injection into agent prompts:
  <retrieved_context>
    <chunk source="intro_to_oop.md" index="3" relevance="0.87">
      chunk text here
    </chunk>
  </retrieved_context>

Keep it simple — no abstractions. The core/ingestion.py file handles the ChromaDB
collection creation — reuse get_or_create_collection() from there, or access
ChromaDB directly with the same collection name from config.
"""


# =============================================================================
# PHASE 2 — Agent Loop + Router + Tool Calling (Gil, 1:30-2:30)
# Paste this into Cursor Agent Mode:
# =============================================================================

CURSOR_PROMPT_AGENT_LOOP = """
Build the agent orchestration loop in agents/router.py and agents/agent_loop.py
for the HaMoach study assistant.

ARCHITECTURE:
User input → Guard (if enabled) → Router → Retrieval → Specialist → Response

REQUIREMENTS:

1. agents/guard.py — Guard Agent:
   - Takes user input string
   - Calls Ollama with GUARD_SYSTEM_PROMPT from agents/prompts.py
   - Parses JSON response: {"status": "SAFE"} or {"status": "BLOCKED", "reason": "..."}
   - Returns the parsed result
   - If parsing fails, default to SAFE (don't block legitimate queries on parse errors)

2. agents/router.py — Router Agent:
   - Takes user input string
   - Calls Ollama with ROUTER_SYSTEM_PROMPT from agents/prompts.py
   - Parses JSON response: {"agent": "...", "confidence": float, "reasoning": "..."}
   - If confidence < ROUTER_CONFIDENCE_THRESHOLD from config, return a clarification request
   - Returns agent name + confidence

3. agents/agent_loop.py — Main Orchestration:
   - full_pipeline(user_input: str, chat_history: list = None) -> dict
   - Steps:
     a. If GUARD_ENABLED: run guard. If BLOCKED → return block message immediately.
     b. Run router to classify the query.
     c. Call retrieval tool with the user's query.
     d. Format retrieved chunks into XML context string.
     e. Inject chunks into the appropriate specialist prompt (from agents/prompts.py).
     f. Call Ollama with the specialist prompt + context.
     g. Parse the specialist's JSON response.
     h. Return the full response with agent name, answer, sources, confidence.

4. Helper: call_ollama(system_prompt: str, user_message: str) -> str
   - Wraps the Ollama chat API call
   - Uses config.OLLAMA_MODEL
   - Returns the raw text response
   - Handles connection errors gracefully

USE THESE IMPORTS:
- import ollama
- import json
- from core.config import *
- from core.retrieval import retrieve, format_chunks_for_prompt
- from agents.prompts import (GUARD_SYSTEM_PROMPT, ROUTER_SYSTEM_PROMPT,
                               CONCEPT_EXPLAINER_PROMPT, PRACTICE_GENERATOR_PROMPT,
                               EXAM_COACH_PROMPT)

JSON PARSING: The 14B model sometimes wraps JSON in markdown code blocks.
Always strip ```json and ``` before parsing. If JSON parse fails, try extracting
the first {...} block with a regex.

All prompts are already written in agents/prompts.py — READ THEM FIRST.
Use {retrieved_chunks} as the placeholder in specialist prompts — replace it
with the formatted XML context string from retrieval.
"""


# =============================================================================
# PHASE 3 — Streamlit UI (Both, 2:30-3:15)
# Paste this into Cursor Agent Mode:
# =============================================================================

CURSOR_PROMPT_STREAMLIT = """
Build the Streamlit UI in app.py for the HaMoach study assistant.

DESIGN:
- Main area: Chat interface with message history
- Sidebar: Retrieved chunks display + document upload
- Each message shows which agent answered (badge/icon)

REQUIREMENTS:

1. SIDEBAR:
   - Title: "🧠 HaMoach"
   - Subtitle from config.STREAMLIT_SUBTITLE
   - File uploader: accept .md, .txt, .pdf — on upload, call ingest_folder()
   - "Ingest /docs" button to process the default docs folder
   - Show ingestion stats (num docs, num chunks)
   - After each query: show retrieved chunks with source + relevance score
   - Expandable sections for each retrieved chunk

2. MAIN CHAT:
   - Use st.chat_message with custom avatars per agent:
     "🎓" for concept_explainer, "📝" for practice_generator, "🧪" for exam_coach
     "🛡️" for guard (blocked messages), "👤" for user
   - Show confidence score as a colored badge:
     Green (≥0.8), Yellow (0.5-0.79), Red (<0.5)
   - Show source documents cited in the response
   - For blocked messages: show red warning with reason

3. STATE MANAGEMENT:
   - st.session_state.messages = [] (chat history)
   - st.session_state.ingested = False
   - st.session_state.last_chunks = [] (retrieved chunks for sidebar)

4. FLOW:
   - User types message → show in chat
   - Call full_pipeline() from agents/agent_loop.py
   - Display response with agent badge
   - Update sidebar with retrieved chunks

USE THESE IMPORTS:
- import streamlit as st
- from core.config import *
- from core.ingestion import ingest_folder
- from agents.agent_loop import full_pipeline

Keep the UI clean and functional — this is a 4-hour hackathon, not a design sprint.
Use st.expander for chunk details, st.metric for confidence, st.columns for layout.
"""
