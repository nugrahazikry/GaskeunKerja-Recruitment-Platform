from pathlib import Path

from config import STORAGE_DIR

_STORAGE_ROOT = Path(STORAGE_DIR)


def cv_path(candidate_id: int) -> Path:
    """storage/cv/<candidate_id>/original.pdf — DB stores only this path, not the file itself."""
    return _STORAGE_ROOT / "cv" / str(candidate_id) / "original.pdf"


def audio_path(candidate_id: int, session: str, answer_index: int) -> Path:
    """storage/audio/<candidate_id>/<session>/answer_<n>.webm"""
    return _STORAGE_ROOT / "audio" / str(candidate_id) / session / f"answer_{answer_index}.webm"


def save_cv(candidate_id: int, file_bytes: bytes) -> str:
    path = cv_path(candidate_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(file_bytes)
    return str(path)


def save_audio(candidate_id: int, session: str, answer_index: int, file_bytes: bytes) -> str:
    path = audio_path(candidate_id, session, answer_index)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(file_bytes)
    return str(path)


def delete_audio(path: str) -> None:
    """Best-effort delete of a previously-saved answer video — missing_ok so a stale/already-gone
    path (e.g. manually cleaned up) never turns a resubmit into a 500. Also removes the per-session
    directory (storage/audio/<candidate_id>/<session>/) once it's empty, since each session dir
    holds exactly the answers from one interview attempt — otherwise every superseded resubmit
    leaves an empty dir behind forever."""
    file_path = Path(path)
    file_path.unlink(missing_ok=True)
    session_dir = file_path.parent
    if session_dir.is_dir() and not any(session_dir.iterdir()):
        session_dir.rmdir()
