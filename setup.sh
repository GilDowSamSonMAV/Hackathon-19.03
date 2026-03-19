#!/usr/bin/env bash
# HaMoach — Pre-Sprint Setup
# Run this BEFORE the timer starts. Takes 10-20 minutes (model download).

set -e
echo "🧠 HaMoach Pre-Sprint Setup"
echo "=========================="

# 1. Pull Ollama models
echo ""
echo "📦 Step 1: Pulling Ollama models..."
echo "   (This takes 10-20 min on first run)"
ollama pull qwen2.5:14b
ollama pull nomic-embed-text

# 2. Verify models work
echo ""
echo "🔍 Step 2: Verifying LLM..."
RESPONSE=$(ollama run qwen2.5:14b "Respond with only: READY" 2>/dev/null | head -1)
if echo "$RESPONSE" | grep -qi "READY"; then
    echo "   ✅ qwen2.5:14b is working"
else
    echo "   ⚠️  qwen2.5:14b responded but output was: $RESPONSE"
fi

echo ""
echo "🔍 Step 3: Verifying embeddings..."
python3 -c "
import ollama
result = ollama.embeddings(model='nomic-embed-text', prompt='search_document: test')
dim = len(result['embedding'])
print(f'   ✅ nomic-embed-text producing {dim}-dim vectors')
" 2>/dev/null || echo "   ❌ Embedding test failed — check Ollama"

# 3. Install Python dependencies
echo ""
echo "📦 Step 4: Installing Python dependencies..."
pip install -q chromadb streamlit ollama pdfplumber pytest 2>/dev/null
echo "   ✅ Dependencies installed"

# 4. Create project structure
echo ""
echo "📁 Step 5: Creating project structure..."
PROJECT_DIR="hamoach"
mkdir -p $PROJECT_DIR/{core,agents,prompts,docs,tests}

# Copy pre-written assets if they exist alongside this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -d "$SCRIPT_DIR/../prompts" ]; then
    cp -r "$SCRIPT_DIR/../prompts/"* "$PROJECT_DIR/prompts/" 2>/dev/null
    echo "   ✅ Prompts copied"
fi
if [ -d "$SCRIPT_DIR/../docs" ]; then
    cp -r "$SCRIPT_DIR/../docs/"* "$PROJECT_DIR/docs/" 2>/dev/null
    echo "   ✅ Test docs copied"
fi
if [ -f "$SCRIPT_DIR/../CLAUDE.md" ]; then
    cp "$SCRIPT_DIR/../CLAUDE.md" "$PROJECT_DIR/CLAUDE.md" 2>/dev/null
    echo "   ✅ CLAUDE.md copied"
fi
if [ -d "$SCRIPT_DIR/../.cursor" ]; then
    cp -r "$SCRIPT_DIR/../.cursor" "$PROJECT_DIR/.cursor" 2>/dev/null
    echo "   ✅ Cursor rules copied"
fi
if [ -f "$SCRIPT_DIR/../requirements.txt" ]; then
    cp "$SCRIPT_DIR/../requirements.txt" "$PROJECT_DIR/requirements.txt" 2>/dev/null
fi

# Create __init__.py files
touch $PROJECT_DIR/core/__init__.py
touch $PROJECT_DIR/agents/__init__.py
touch $PROJECT_DIR/tests/__init__.py

# Create placeholder files
for f in core/embeddings.py core/retrieval.py core/agent_loop.py agents/router.py agents/specialists.py agents/guard.py app.py tests/test_scenarios.py; do
    [ ! -f "$PROJECT_DIR/$f" ] && echo "# TODO: Implement" > "$PROJECT_DIR/$f"
done

echo "   ✅ Project structure ready"

# 5. Verify ChromaDB
echo ""
echo "🔍 Step 6: Verifying ChromaDB..."
python3 -c "
import chromadb
client = chromadb.Client()
col = client.create_collection('test', metadata={'hf:space': 'cosine'})
col.add(ids=['1'], embeddings=[[0.1]*768], documents=['test doc'])
result = col.query(query_embeddings=[[0.1]*768], n_results=1)
assert result['documents'][0][0] == 'test doc'
client.delete_collection('test')
print('   ✅ ChromaDB working with cosine similarity')
"

# 6. Quick Streamlit check
echo ""
echo "🔍 Step 7: Verifying Streamlit..."
python3 -c "import streamlit; print(f'   ✅ Streamlit v{streamlit.__version__} installed')"

# Summary
echo ""
echo "=========================="
echo "✅ PRE-SPRINT SETUP COMPLETE"
echo ""
echo "Project: ./$PROJECT_DIR/"
echo ""
echo "To start the app:  cd $PROJECT_DIR && python -m streamlit run app.py"
echo "To run tests:      cd $PROJECT_DIR && python -m pytest tests/ -v"
echo ""
echo "Gil: Open Claude Code in ./$PROJECT_DIR/"
echo "Lior: Open Cursor in ./$PROJECT_DIR/"
echo ""
echo "🍺 Crack beers. Start timer. Ship it."
