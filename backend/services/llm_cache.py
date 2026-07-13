import hashlib
import json
from pathlib import Path
from typing import Any

from config import CACHE_DIR

_cache_dir = Path(CACHE_DIR)
_cache_dir.mkdir(parents=True, exist_ok=True)


def make_key(model: str, messages: list[dict], temperature: float) -> str:
    payload = json.dumps({"model": model, "messages": messages, "temperature": temperature}, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def get(key: str) -> dict[str, Any] | None:
    path = _cache_dir / f"{key}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def set(key: str, value: dict[str, Any]) -> None:
    path = _cache_dir / f"{key}.json"
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
