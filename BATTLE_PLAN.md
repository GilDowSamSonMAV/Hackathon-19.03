# HaMoach — Battle Plan

## Tool Assignments by Phase

```
PHASE       | GIL (Infra Track)           | LIOR (AI Track)
------------|-----------------------------|---------------------------
Pre-Sprint  | Claude Code: scaffold,      | Antigravity: research RAG
            | pull models, verify stack   | patterns, review prompts
            |                             |
0:00-0:30   | Claude Code: setup,         | Cursor Agent Mode: create
Setup       | verify Ollama, ChromaDB,    | test docs in /docs,
            | project structure           | verify prompts work
            |                             |
0:30-1:30   | Claude Code: embeddings.py  | Cursor Agent Mode: tune
Phase 1     | → chunk_text()              | system prompts against
RAG         | → embed_and_store()         | actual Ollama output,
            | → retrieval.py: query()     | calibrate confidence
            |                             | thresholds
            |                             |
1:30-2:30   | Claude Code: agent_loop.py  | Cursor Agent Mode: refine
Phase 2     | → run_agent() core loop     | specialist prompts based
Agents      | → router dispatch logic     | on real retrieval output,
            | → tool calling pattern      | build Practice Generator
            |                             | question format, Exam
            |                             | Coach eval rubric
            |                             |
2:30-3:15   | Claude Code: app.py         | Cursor: help with UI
Phase 3     | → Streamlit chat UI         | components, run 10 test
Integration | → sidebar chunk display     | scenarios, fix failures
            | → agent badges              |
            |                             |
3:15-3:45   | Claude Code: guard.py       | Cursor: sanitizer.py
TWIST       | → Guard Agent classifier    | → doc content sanitizer
            | → wire into pipeline        | → test injection defense
            |                             |
3:45-4:00   | Record demo, write README   | Score against rubric
Demo        |                             |
```

## Why These Tool Assignments

**Gil → Claude Code throughout:**
Claude Code is the best tool for sequential infra work because the entire
infra track is a linear pipeline: embeddings → retrieval → agent loop → UI.
Each step depends on the previous one. Claude Code's single-agent deep focus
with terminal access is perfect — you're building plumbing, not designing UI.

**Lior → Cursor Agent Mode throughout:**
Lior's AI track is iterative prompt tuning — write a prompt, test it, see the
output, tweak, repeat. Cursor Agent Mode's inline editing and visual diffs make
this loop tighter than Claude Code's terminal-based workflow. Lior also benefits
from seeing the full file tree while working across multiple prompt files.

**NOT using during the sprint:**
- Factory Droids: No CI/CD needed for a 4-hour prototype
- MiniMax: Not needed, local Ollama handles all inference
- Antigravity: Only useful for pre-sprint research, not mid-sprint coding
- Claude.ai: Gil uses Claude Code directly, not the web interface

## Pre-Generated Assets (Don't Build These During Sprint)

These are fair game to pre-build because they're boilerplate, not learning:

1. ✅ Project scaffold (folder structure, __init__.py files)
2. ✅ CLAUDE.md (context for Claude Code)
3. ✅ .cursor/rules/ (context for Cursor)
4. ✅ All 4 system prompts (router + 3 specialists)
5. ✅ Guard agent prompt (for the twist — Lior doesn't see this)
6. ✅ 5 test documents (CS course material)
7. ✅ requirements.txt
8. ✅ Pre-sprint setup script

## What MUST Be Built During Sprint (The Learning)

These are the actual learning objectives — don't pre-build:

1. 🔨 Chunking + embedding pipeline (understand tokenization, overlap, vector dimensions)
2. 🔨 ChromaDB storage + retrieval (understand similarity search, top-k, metadata filtering)
3. 🔨 Agent loop from scratch (understand observe→think→act→return without LangChain)
4. 🔨 Router logic (understand classification as agent dispatch)
5. 🔨 Tool-calling pattern (understand how agents invoke functions)
6. 🔨 Confidence scoring (understand when to say "I don't know")
7. 🔨 Guard agent (understand prompt injection defense — the twist)

## Critical Decisions Pre-Made

These decisions are already locked. Don't debate them during the sprint:

| Decision | Answer | Why |
|----------|--------|-----|
| LLM model | qwen2.5:14b | Best reasoning at 14B, fits 16GB VRAM |
| Embedding model | nomic-embed-text | 768-dim, runs alongside LLM |
| Vector store | ChromaDB (PersistentClient) | Zero config, pip install |
| Chunk size | 500 chars, 50 overlap | Standard for this doc size |
| Top-k retrieval | k=5 | Enough context without flooding |
| Confidence threshold | 0.7 cosine similarity | Below = "I don't know" |
| UI framework | Streamlit | Known from Savta, ship fast |
| Agent framework | None (raw Python) | The whole point is learning |
| Context window | 8192 tokens | Set via num_ctx in Ollama |
