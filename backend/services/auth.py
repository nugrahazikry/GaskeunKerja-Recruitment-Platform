import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from config import CANDIDATE_TOKEN_TTL_HOURS, JWT_EXPIRE_MINUTES, JWT_SECRET

JWT_ALGORITHM = "HS256"


class InvalidTokenError(Exception):
    """Raised for an expired/malformed/missing JWT or candidate token."""


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))


def create_hr_jwt(hr_user_id: int, company_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(hr_user_id),
        "company_id": company_id,
        "role": "hr",
        "iat": now,
        "exp": now + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_hr_jwt(token: str) -> dict:
    """Returns the decoded payload (hr_user_id, company_id) or raises InvalidTokenError."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as e:
        raise InvalidTokenError(str(e)) from e

    if payload.get("role") != "hr":
        raise InvalidTokenError("Not an HR token")
    return payload


def generate_candidate_token() -> tuple[str, datetime]:
    """Returns (unguessable token, expires_at) for a new candidate session link."""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=CANDIDATE_TOKEN_TTL_HOURS)
    return token, expires_at


def is_candidate_token_valid(token_expires_at: datetime, now: datetime | None = None) -> bool:
    now = now or datetime.now(timezone.utc)
    return now < token_expires_at
