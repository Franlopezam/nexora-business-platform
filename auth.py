from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models.user import User
from ..schemas.auth import LoginRequest, TokenResponse, UserCreate, UserOut
from ..security.auth import authenticate, create_token, hash_password, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate(db, data.email, data.password)
    if not user:
        raise HTTPException(401, "Invalid email or password")

    access = create_token(user.id, "access", timedelta(minutes=settings.access_token_minutes))
    refresh = create_token(user.id, "refresh", timedelta(days=settings.refresh_token_days))
    return {"access_token": access, "refresh_token": refresh}


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.post("/users", response_model=UserOut)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    if current.role != "admin":
        raise HTTPException(403, "Admin role required")
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(409, "Email already exists")

    user = User(
        name=data.name,
        email=data.email.lower(),
        password_hash=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
