"""
HaMoach — Central Configuration
================================
All tunable parameters in one place. No magic numbers in code.
"""

import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# --- Model Configuration ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "models/gemini-flash-latest"          # Main reasoning model
GEMINI_EMBED_MODEL = "models/gemini-embedding-001" # Embedding model

# (Deprecated Ollama Configs)
OLLAMA_MODEL = "qwen2.5:14b"
EMBED_MODEL = "nomic-embed-text"

# --- Chunking Configuration ---
CHUNK_SIZE = 500                       # Characters per chunk
CHUNK_OVERLAP = 50                     # Overlap between adjacent chunks
MIN_CHUNK_SIZE = 100                   # Discard chunks smaller than this

# --- Retrieval Configuration ---
TOP_K = 5                              # Number of chunks to retrieve
CONFIDENCE_THRESHOLD = 0.5            # Below this → "I don't have enough info"
CHROMA_COLLECTION = "hamoach_docs"     # ChromaDB collection name
CHROMA_PERSIST_DIR = "./chroma_db"     # ChromaDB storage path

# --- Agent Configuration ---
AGENT_NAMES = {
    "concept_explainer": "🎓 Concept Explainer",
    "practice_generator": "📝 Practice Generator",
    "exam_coach": "🧪 Exam Coach",
}

ROUTER_CONFIDENCE_THRESHOLD = 0.6     # Below this → ask user to clarify

# --- Security Configuration ---
GUARD_ENABLED = True                   # Toggle guard agent on/off (flip for twist)
SANITIZE_ON_INGEST = True             # Strip injection patterns during ingestion

# --- UI Configuration ---
STREAMLIT_TITLE = "🧠 HaMoach — Study Assistant"
STREAMLIT_SUBTITLE = "Upload your course materials. Ask anything. Get answers from YOUR content."
DOCS_FOLDER = "./docs"                 # Default document folder

# --- Supported file types for ingestion ---
SUPPORTED_EXTENSIONS = [".md", ".txt", ".pdf"]
