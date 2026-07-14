from pathlib import Path

# ==========================================
# Project Paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ROOT = PROJECT_ROOT.parent

NOTES_FILE = PROJECT_ROOT / "notes.json"

PROMPTS_DIR = PROJECT_ROOT / "prompts"

# ==========================================
# LLM
# ==========================================

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3.5:2b"

TEMPERATURE = 0

# ==========================================
# Repository Scanner
# ==========================================

SUPPORTED_FILE_EXTENSIONS = {
    ".py",
    ".ipynb",
    ".md",
    ".txt",
}

# ==========================================
# Logging
# ==========================================

LOG_LEVEL = "INFO"