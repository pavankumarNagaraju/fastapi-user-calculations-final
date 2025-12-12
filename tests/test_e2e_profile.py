import pytest
from playwright.sync_api import Page, expect
from passlib.context import CryptContext

from app.database import SessionLocal, Base, engine
from app import models

BASE_URL = "http://localhost:8000"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def ensure_e2e_user(
    email: str = "e2e_profile@example.com",
    password: str = "oldpassword",
    full_name: str = "E2E Profile User",
):
    Base.metadata.create_all(bind=engine)
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
    finally:
        db.close()


@pytest.mark.e2e
def test_profile_e2e_flow(page: Page):
    # Prepare a known user directly in the DB
    ensure_e2e_user()

    # Open the profile page
    page.goto(f"{BASE_URL}/static/profile.html")

    # Load current profile
    page.fill("#profile-email", "e2e_profile@example.com")
    page.fill("#profile-current-password", "oldpassword")
    page.click("#load-profile")

    expect(page.locator("#profile-message")).to_contain_text("Profile loaded")
    expect(page.locator("#profile-full-name")).to_have_value("E2E Profile User")

    # Update profile details
    page.fill("#profile-full-name", "Updated E2E User")
    page.fill("#profile-new-email", "new-e2e-profile@example.com")
    page.click("#save-profile")

    expect(page.locator("#profile-message")).to_contain_text("Profile updated")

    # Change password
    page.fill("#password-email", "new-e2e-profile@example.com")
    page.fill("#password-current", "oldpassword")
    page.fill("#password-new", "super-secret123")
    page.click("#change-password")

    expect(page.locator("#password-message")).to_contain_text("Password updated")
