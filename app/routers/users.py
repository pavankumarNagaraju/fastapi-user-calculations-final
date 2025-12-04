# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import get_password_hash, verify_password, create_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead)
def register_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    Test expects:
    - POST /users/register
    - JSON body with: email, full_name, password
    - Status code 201 on success
    """
    existing = (
        db.query(models.User)
        .filter(models.User.email == user_in.email)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = models.User(
        email=user_in.email,
        full_name=getattr(user_in, "full_name", None),
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login_user(
    user_in: schemas.UserCreate,  # reuse UserCreate: email + password (+ full_name ignored)
    db: Session = Depends(get_db),
):
    """
    Login and return a JWT access token.

    Test does:
    - POST /users/login with email + password
    - Expects 200 and JSON with `message == "Login successful"`
    """
    user = (
        db.query(models.User)
        .filter(models.User.email == user_in.email)
        .first()
    )
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token({"sub": str(user.id)})
    return {
        "message": "Login successful",
        "user_id": user.id,          # ✅ what the test asserts
        "access_token": access_token,
        "token_type": "bearer",
    }

