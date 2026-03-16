from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_schema import TokenOut, UserCreate, UserOut
from app.services.auth_service import login_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    user = register_user(db=db, email=payload.email, password=payload.password)
    return UserOut(id=user.id, email=user.email, created_at=user.created_at)


@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> TokenOut:
    token = login_user(db=db, email=form.username, password=form.password)
    return TokenOut(access_token=token)

