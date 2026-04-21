import os
from dotenv import load_dotenv

load_dotenv()

# ── API Key (OpenAI only) ─────────────────────────────────
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = "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"
# ── Vector DB ─────────────────────────────────────────────
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")

# ── LLM Settings ──────────────────────────────────────────
LLM_MODEL  = "gpt-4o-mini"
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 1024))

# ── Image Generation Settings ─────────────────────────────
IMAGE_MODEL   = "dall-e-3"
IMAGE_SIZE    = os.getenv("IMAGE_SIZE", "1024x1024")
IMAGE_QUALITY = os.getenv("IMAGE_QUALITY", "standard")  # "hd" costs more

# ── Embeddings ────────────────────────────────────────────
EMBEDDING_MODEL = "text-embedding-ada-002"

# ── App ───────────────────────────────────────────────────
APP_TITLE = os.getenv("APP_TITLE", "Multimodal Manufacturing Creator")

def validate_keys():
    """Check that required API key is set."""
    if not OPENAI_API_KEY:
        raise EnvironmentError(
            "Missing OPENAI_API_KEY.\n"
            "Please copy .env.example → .env and add your OpenAI API key."
        )