from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import users, calculations, profile

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI User Calculations - Module 14")

# Serve static HTML files (register, login, profile, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"message": "FastAPI User Calculations - Module 14"}


# Existing routers
app.include_router(users.router)
app.include_router(calculations.router)

# New profile router
app.include_router(profile.router)
