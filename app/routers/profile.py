from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/profile", tags=["profile"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class ProfileCredentials(BaseModel):
    email: EmailStr
    password: str


class ProfileRead(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        orm_mode = True


class ProfileUpdate(BaseModel):
    email: EmailStr
    current_password: str
    new_email: Optional[EmailStr] = None
    new_full_name: Optional[str] = None


class PasswordChange(BaseModel):
    email: EmailStr
    current_password: str
    new_password: str = Field(min_length=8)


@router.post("/me", response_model=ProfileRead)
def read_profile(
    credentials: ProfileCredentials, db: Session = Depends(get_db)
):
    """
    Verify email + password and return basic profile details.
    """
    user = (
        db.query(models.User)
        .filter(models.User.email == credentials.email)
        .first()
    )
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password for profile access",
        )

    return ProfileRead(email=user.email, full_name=getattr(user, "full_name", None))


@router.post("/update", response_model=ProfileRead)
def update_profile(update: ProfileUpdate, db: Session = Depends(get_db)):
    """
    Update full_name and/or email after verifying current password.
    """
    user = (
        db.query(models.User)
        .filter(models.User.email == update.email)
        .first()
    )
    if not user or not verify_password(update.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password for profile update",
        )

    # Email change
    if update.new_email and update.new_email != user.email:
        existing = (
            db.query(models.User)
            .filter(models.User.email == update.new_email)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with that new email already exists",
            )
        user.email = update.new_email

    # Name change
    if update.new_full_name is not None:
        user.full_name = update.new_full_name

    db.add(user)
    db.commit()
    db.refresh(user)

    return ProfileRead(email=user.email, full_name=getattr(user, "full_name", None))


@router.post("/change-password")
def change_password(
    payload: PasswordChange, db: Session = Depends(get_db)
):
    """
    Change password after verifying current password.
    """
    user = (
        db.query(models.User)
        .filter(models.User.email == payload.email)
        .first()
    )
    if not user or not verify_password(payload.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password for password change",
        )

    user.hashed_password = pwd_context.hash(payload.new_password)
    db.add(user)
    db.commit()

    return {"message": "Password updated successfully"}
