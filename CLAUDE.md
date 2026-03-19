# CLAUDE.md — HaMoach (Hackathon Sprint)

## Project

Multi-agent RAG study assistant. 4-hour sprint build. Local inference only (Ollama).

## Stack

- Python 3.11+
- Ollama (qwen2.5:14b for LLM, nomic-embed-text for embeddings)
- ChromaDB for vector storage
- Streamlit for UI
- No LangChain, no CrewAI, no LangGraph — raw Python agent loop

## Architecture

```
User Input → [Guard Agent] → [Router Agent] → [Specialist Agent]
                                                    ↓
                                            [Retrieval Tool] → ChromaDB
                                                    ↓
                                            [Citation Formatter] → Response
```

### Agents
- **Guard**: Classifies input as SAFE/BLOCKED before routing
- **Router**: Classifies into "concept" | "practice" | "exam"
- **Concept Explainer**: Retrieves + explains concepts simply
- **Practice Generator**: Creates questions + answers from material
- **Exam Coach**: Interactive Q&A, evaluates student responses

### Key Files
```
hamoach/
├── app.py                  # Streamlit entry point
├── core/
│   ├── embeddings.py       # Chunk + embed + store in ChromaDB
│   ├── retrieval.py        # Query ChromaDB, return top-k with scores
│   └── agent_loop.py       # The core observe→think→act→return loop
├── agents/
│   ├── router.py           # Classify input → dispatch to specialist
│   ├── specialists.py      # 3 specialist agents
│   └── guard.py            # Input safety classifier
├── prompts/                # System prompts (pre-written, load at runtime)
│   ├── router.txt
│   ├── concept_explainer.txt
│   ├── practice_generator.txt
│   ├── exam_coach.txt
│   └── guard.txt
├── docs/                   # Course material (test data)
└── tests/
    └── test_scenarios.py
```

## Rules

1. **All inference through Ollama Python SDK**: `import ollama` → `ollama.chat()` / `ollama.embeddings()`
2. **ChromaDB with cosine similarity**: `collection = client.create_collection("docs", metadata={"hf:space": "cosine"})`
3. **nomic-embed-text requires prefix**: `"search_document: "` for docs, `"search_query: "` for queries
4. **Set context window**: `options={"num_ctx": 8192}` on every `ollama.chat()` call
5. **Chunk size**: 500 chars, 50 char overlap
6. **Top-k**: 5 chunks per retrieval
7. **Confidence threshold**: 0.7 cosine similarity. Below = "I don't have enough info"
8. **Streamlit session_state**: All agent memory and conversation history goes in `st.session_state`
9. **No external API calls**: Everything runs on local Ollama. Zero network dependency.
10. **System prompts loaded from /prompts/**: Don't hardcode prompts in Python files

## Task Phases

### Phase 1 (0:30-1:30): RAG Pipeline
- [ ] `core/embeddings.py`: Read all files from docs/, chunk, embed via Ollama, store in ChromaDB
- [ ] `core/retrieval.py`: Query → embed → cosine search → return top-5 chunks with metadata + scores
- [ ] Verify: embed a doc, query it, get relevant chunks back

### Phase 2 (1:30-2:30): Multi-Agent System  
- [ ] `core/agent_loop.py`: Generic agent runner (system_prompt + user_input + tools → response)
- [ ] `agents/router.py`: Router agent that classifies and dispatches
- [ ] `agents/specialists.py`: 3 specialists, each uses retrieval as a tool
- [ ] Verify: ask "What is polymorphism?" → routes to Concept Explainer → retrieves from intro_to_oop.md

### Phase 3 (2:30-3:15): Integration + UI
- [ ] `app.py`: Streamlit chat with agent badges, sidebar showing retrieved chunks
- [ ] Run all 10 test scenarios end-to-end
- [ ] Fix any routing or retrieval failures

### Phase 4 (3:15-3:45): TWIST — Guard Agent
- [ ] `agents/guard.py`: Classify messages as SAFE/BLOCKED
- [ ] Wire guard before router in the pipeline
- [ ] Test: jailbreak, data exfil, role hijack, indirect injection in docs
- [ ] `core/embeddings.py`: Add sanitization during doc ingestion

## Testing

Run test scenarios:
```bash
python -m pytest tests/test_scenarios.py -v
```

Run the app:
```bash
python -m streamlit run app.py
```
