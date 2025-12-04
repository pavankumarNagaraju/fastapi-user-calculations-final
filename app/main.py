# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import users, calculations

# ✅ Create all tables whenever the app module is imported.
# This ensures the DB is ready as soon as tests import app.main.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI User Calculations - Module 14",
    version="0.1.0",
)

# ✅ Serve static files (register.html, login.html, etc.)
# The Playwright E2E tests visit /static/register.html and /static/login.html
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ User register/login at /users/...
app.include_router(users.router)

# ✅ Calculations BREAD at /calculations/...
app.include_router(calculations.router)


@app.get("/")
def read_root():
    return {"message": "FastAPI User Calculations - Module 14"}
