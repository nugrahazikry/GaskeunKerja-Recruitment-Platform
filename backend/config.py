import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


LLM_BASE_URL = _require("LLM_BASE_URL")
LLM_API_KEY = _require("LLM_API_KEY")
LLM_MODEL_FLASH = _require("LLM_MODEL_FLASH")
LLM_MODEL_PRO = _require("LLM_MODEL_PRO")
LLM_TEMPERATURE_SCORING = float(os.environ.get("LLM_TEMPERATURE_SCORING", "0"))

EMBEDDING_PROVIDER = os.environ.get("EMBEDDING_PROVIDER", "sumopod")
EMBEDDING_MODEL = _require("EMBEDDING_MODEL")
EMBEDDING_DIMENSIONS = int(os.environ.get("EMBEDDING_DIMENSIONS", "1536"))

STT_PROVIDER = os.environ.get("STT_PROVIDER", "groq")
STT_LANGUAGE = os.environ.get("STT_LANGUAGE", "id")
STT_BASE_URL = os.environ.get("STT_BASE_URL")
STT_API_KEY = os.environ.get("STT_API_KEY")
STT_MODEL = os.environ.get("STT_MODEL")
STT_LOCAL_MODEL = os.environ.get("STT_LOCAL_MODEL", "small")
STT_LOCAL_DEVICE = os.environ.get("STT_LOCAL_DEVICE", "cuda")
STT_LOCAL_COMPUTE_TYPE = os.environ.get("STT_LOCAL_COMPUTE_TYPE", "float16")

VISION_PROVIDER = os.environ.get("VISION_PROVIDER", "groq")
VISION_MODEL = os.environ.get("VISION_MODEL")

STORAGE_DIR = str(REPO_ROOT / os.environ.get("STORAGE_DIR", "./storage").lstrip("./"))
CACHE_DIR = str(Path(STORAGE_DIR) / "llm_cache")

TELEGRAM_ENABLED = os.environ.get("TELEGRAM_ENABLED", "true").lower() == "true"
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_USERNAME = os.environ.get("TELEGRAM_BOT_USERNAME")

# Round-3 Task 19: Gmail SMTP replaces Telegram as the candidate notification channel. Telegram
# code stays intact (see TELEGRAM_ENABLED above) as a flag-guarded fallback — flip EMAIL_ENABLED
# off and TELEGRAM_ENABLED on to roll back with no code change.
EMAIL_ENABLED = os.environ.get("EMAIL_ENABLED", "false").lower() == "true"
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")  # Gmail App Password, not the account password
SMTP_FROM = os.environ.get("SMTP_FROM", SMTP_USERNAME)

DATABASE_URL = _require("DATABASE_URL")

QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.environ.get("QDRANT_PORT", "6333"))
QDRANT_URL = os.environ.get("QDRANT_URL", f"http://{QDRANT_HOST}:{QDRANT_PORT}")

JWT_SECRET = _require("JWT_SECRET")
JWT_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", "120"))
CANDIDATE_TOKEN_TTL_HOURS = int(os.environ.get("CANDIDATE_TOKEN_TTL_HOURS", "72"))
