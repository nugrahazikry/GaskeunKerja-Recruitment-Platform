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
