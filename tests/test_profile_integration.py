from fastapi.testclient import TestClient
from passlib.context import CryptContext

from app.main import app
from app.database import SessionLocal, Base, engine
from app import models

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def ensure_test_schema():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)


def create_or_reset_user(
    email: str = "profile@example.com",
    password: str = "oldpassword",
    full_name: str = "Original Name",
):
    ensure_test_schema()
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            user = models.User(
                email=email,
                full_name=full_name,
                hashed_password=pwd_context.hash(password),
            )
            db.add(user)
        else:
            user.full_name = full_name
            user.hashed_password = pwd_context.hash(password)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def test_profile_flow_integration():
    user = create_or_reset_user()

    # 1) Get profile
    resp = client.post(
        "/profile/me",
        json={"email": user.email, "password": "oldpassword"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == user.email
    assert data["full_name"] == "Original Name"

    # 2) Update profile
    resp = client.post(
        "/profile/update",
        json={
            "email": user.email,
            "current_password": "oldpassword",
            "new_email": "newprofile@example.com",
            "new_full_name": "New Name",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "newprofile@example.com"
    assert data["full_name"] == "New Name"

    # 3) Change password
    resp = client.post(
        "/profile/change-password",
        json={
            "email": "newprofile@example.com",
            "current_password": "oldpassword",
            "new_password": "supernewpassword",
        },
    )
    assert resp.status_code == 200
    assert "updated" in resp.json()["message"].lower()

    # 4) Old password should now fail
    resp = client.post(
        "/profile/me",
        json={"email": "newprofile@example.com", "password": "oldpassword"},
    )
    assert resp.status_code == 401

    # 5) New password should now succeed
    resp = client.post(
        "/profile/me",
        json={"email": "newprofile@example.com", "password": "supernewpassword"},
    )
    assert resp.status_code == 200
