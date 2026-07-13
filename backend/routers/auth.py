from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from services import auth

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    users = repo.hr_users.list(db, email=body.email)
    if not users or not auth.verify_password(body.password, users[0].password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user = users[0]
    token = auth.create_hr_jwt(hr_user_id=user.id, company_id=user.company_id)
    return LoginResponse(access_token=token)


def get_current_hr(authorization: str = Header(...)) -> dict:
    """Dependency: guards HR-only routes. Expects 'Authorization: Bearer <token>'."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.removeprefix("Bearer ")
    try:
        return auth.verify_hr_jwt(token)
    except auth.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e


def get_candidate_by_token(token: str, db: Session = Depends(get_db)):
    """Dependency: resolves a candidate's own unguessable token to their row, scoped to
    exactly that candidate's session — never returns another candidate's data. Rejects
    expired or unknown tokens with 401 (a shared 'link tidak valid' state at the API level,
    per Area 1 T3's frontend guard)."""
    candidates = repo.candidates.list(db, token=token)
    if not candidates:
        raise HTTPException(status_code=401, detail="Invalid or unknown token")

    candidate = candidates[0]
    if not auth.is_candidate_token_valid(candidate.token_expires_at):
        raise HTTPException(status_code=401, detail="Token has expired")

    return candidate
