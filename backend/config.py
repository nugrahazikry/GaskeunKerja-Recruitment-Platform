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

STORAGE_DIR = str(REPO_ROOT / os.environ.get("STORAGE_DIR", "./storage").lstrip("./"))
CACHE_DIR = str(Path(STORAGE_DIR) / "llm_cache")
