# FastAPI User Calculations - Module 14

A small FastAPI app that supports **user registration/login** and **BREAD** operations for calculations.
This project is designed for the IS601 Module 14 requirements with:
- REST APIs for users & calculations
- Basic JWT-style login response (as expected by tests)
- Simple static UI pages for E2E Playwright checks
- Pytest markers and GitHub Actions CI
- Docker build/push workflow

## Repositories

- **GitHub:** https://github.com/pavankumarNagaraju/fastapi-user-calculations-m14
- **Docker Hub:** https://hub.docker.com/repository/docker/pavankumarnagarju/

## Features

### Users
- Register a new user
- Login with existing credentials
- Password hashing

Endpoints:
- `POST /users/register`
- `POST /users/login`

### Calculations (BREAD)
Create, Read (single & list), Edit, Delete calculations.

Endpoints:
- `POST /calculations/`
- `GET /calculations/`
- `GET /calculations/{id}`
- `PUT /calculations/{id}`
- `DELETE /calculations/{id}`

Supported operations:
- `add`
- `sub`
- `mul`
- `div`

## Tech Stack

- FastAPI
- SQLAlchemy + SQLite
- Pydantic
- Passlib (bcrypt)
- Pytest
- Playwright (E2E)

## Project Structure (high-level)

```
app/
  main.py
  database.py
  models.py
  schemas.py
  security.py
  dependencies.py
  routers/
    __init__.py
    users.py
    calculations.py
  static/
    register.html
    login.html
tests/
pytest.ini
.github/workflows/
Dockerfile
```

## Local Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Run the app:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Running Tests

Non-E2E tests:

```bash
python -m pytest -m "not e2e"
```

E2E tests:

```bash
python -m pytest -m "e2e"
```

## E2E UI Pages

These pages are used by Playwright tests. Open in browser:

- `http://127.0.0.1:8000/static/register.html`
- `http://127.0.0.1:8000/static/login.html`

They rely on `data-testid` attributes that match the tests.

## BREAD Screenshots Guide (for submission)

Use Swagger (`/docs`) or curl to capture screenshots.

1) **Register**
- `POST /users/register`
```json
{
  "email": "screenshots_user@example.com",
  "full_name": "Screenshots User",
  "password": "secret123"
}
```

2) **Login**
- `POST /users/login`
```json
{
  "email": "screenshots_user@example.com",
  "password": "secret123"
}
```

3) **Create Calculation**
- `POST /calculations/`
```json
{
  "operation": "add",
  "operand1": 6,
  "operand2": 4
}
```

4) **Read All**
- `GET /calculations/`

5) **Read One**
- `GET /calculations/{id}`

6) **Edit**
- `PUT /calculations/{id}`
```json
{
  "operation": "mul",
  "operand1": 6,
  "operand2": 4
}
```

7) **Delete**
- `DELETE /calculations/{id}`

Tip: If you see `Unsupported operation 'string'`, update the payload to one of:
`add`, `sub`, `mul`, `div`.

## Docker

Build locally:

```bash
docker build -t fastapi-user-calculations-m14 .
docker run -p 8000:8000 fastapi-user-calculations-m14
```

If your Docker Hub image name is set to the repo name, you can pull like:

```bash
docker pull pavankumarnagarju/fastapi-user-calculations-m14:latest
```

## CI/CD Notes

GitHub Actions should run:
- Unit/integration tests on push/PR
- E2E tests when configured
- Docker build & push on main (if enabled)

Ensure these secrets exist in your GitHub repository settings:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## Known Warnings

You may see warnings related to:
- Pydantic V2 config migration
- `datetime.utcnow()` deprecation
- SQLAlchemy legacy `.query().get()`

These do not fail the tests and are acceptable unless your course requires cleanup.
