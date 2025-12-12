# FastAPI User Calculations – Final Project

A small FastAPI app that supports user registration/login, BREAD operations for calculations, and a **final-project feature for managing user profiles and passwords**.

This project builds on the IS601 Module 14 work and extends it with:

- REST APIs for users & calculations  
- Profile + password change feature touching all layers (DB, schemas, routes, UI, tests)  
- Static UI pages for Playwright E2E checks  
- Pytest markers and GitHub Actions CI  
- Docker build/push workflow

---

## Repositories

- GitHub: https://github.com/pavankumarNagaraju/fastapi-user-calculations-final  
- Docker Hub: https://hub.docker.com/repository/docker/pavankumarnagarju/

Typical image name used in CI:  
`pavankumarnagarju/fastapi-user-calculations-final:latest`

---

## Features

### 1. Users

- Register a new user  
- Login with existing credentials  
- Passwords are stored **hashed** using Passlib (bcrypt).  
- Login returns a simple JWT-style access token response used by the tests.

Endpoints:

- `POST /users/register`
- `POST /users/login`

---

### 2. Calculations (BREAD)

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

Each calculation stores the operands, operation, result, and a timestamp.

---

### 3. Final Project Feature – Profile & Password Management

The final assignment adds a **Profile & Password** feature that lets a user:

- Load their basic profile details (email + full name)  
- Update their email and/or full name  
- Change their password securely (old password → new password)

All profile actions:

- Verify the **current password** against the stored bcrypt hash  
- Use SQLAlchemy to read/update the existing `User` row  
- Are covered by both **integration tests** and **Playwright E2E tests**

#### Backend Routes (`/profile`)

All profile routes live in `app/routers/profile.py` under the `/profile` prefix.

1. **Read profile**

   - `POST /profile/me`  
   - Request body:

     ```json
     {
       "email": "user@example.com",
       "password": "current-password"
     }
     ```

   - Response (example):

     ```json
     {
       "email": "user@example.com",
       "full_name": "Existing Name"
     }
     ```

2. **Update profile**

   - `POST /profile/update`  
   - Request body:

     ```json
     {
       "email": "user@example.com",
       "current_password": "current-password",
       "new_email": "new-email@example.com",
       "new_full_name": "New Name"
     }
     ```

   - Either `new_email`, `new_full_name`, or both can be provided.  
   - Email changes check for duplicates and return `400` if the new email already exists.

3. **Change password**

   - `POST /profile/change-password`  
   - Request body:

     ```json
     {
       "email": "user@example.com",
       "current_password": "current-password",
       "new_password": "super-secure-password"
     }
     ```

   - `new_password` has a minimum length validation.  
   - On success, returns:

     ```json
     { "message": "Password updated successfully" }
     ```

---

### 4. Front-End Pages (Static HTML)

Static pages under `static/` are used by Playwright for E2E tests:

- `http://127.0.0.1:8000/static/register.html`
- `http://127.0.0.1:8000/static/login.html`
- `http://127.0.0.1:8000/static/profile.html`  ← **new final-project UI**

The **Profile** page allows a user to:

- Load their profile (email, full name) using email + current password  
- Update name/email  
- Change their password  

All key elements use stable IDs and/or `data-testid` attributes so the Playwright tests can locate them reliably.

---

## Tech Stack

- FastAPI  
- SQLAlchemy + SQLite  
- Pydantic  
- Passlib (bcrypt)  
- Pytest  
- Playwright (E2E)  
- Docker  
- GitHub Actions (CI/CD)

---

## Project Structure (high-level)

```text
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
    profile.py      # ← final project feature
static/
  register.html
  login.html
  profile.html      # ← final project UI
tests/
  test_users_integration.py
  test_calculations_integration.py
  test_profile_integration.py   # ← new integration test
  test_e2e_auth.py
  test_e2e_profile.py           # ← new E2E test
pytest.ini
.github/workflows/
Dockerfile
docker-compose.yml
requirements.txt
reflection.md
```

---

## Local Setup

```bash
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Running the App

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

---

## Running Tests

### All tests (unit + integration + E2E)

```bash
python -m pytest
```

> Note: E2E tests expect the FastAPI app to be running at `http://localhost:8000`.

Typical workflow in two terminals:

1. **Terminal 1 – Start the app**

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Terminal 2 – Run tests**

   ```bash
   python -m pytest -m "not e2e"   # unit + integration only
   python -m pytest -m "e2e"       # Playwright E2E tests
   ```

---

## BREAD & Profile Usage Guide (for screenshots / grading)

1. **Register**

   - `POST /users/register`

     ```json
     {
       "email": "screenshots_user@example.com",
       "full_name": "Screenshots User",
       "password": "secret123"
     }
     ```

2. **Login**

   - `POST /users/login`

     ```json
     {
       "email": "screenshots_user@example.com",
       "password": "secret123"
     }
     ```

3. **Create Calculation**

   - `POST /calculations/`

     ```json
     {
       "operation": "add",
       "operand1": 6,
       "operand2": 4
     }
     ```

4. **Read All**

   - `GET /calculations/`

5. **Read One**

   - `GET /calculations/{id}`

6. **Edit**

   - `PUT /calculations/{id}`

     ```json
     {
       "operation": "mul",
       "operand1": 6,
       "operand2": 4
     }
     ```

7. **Delete**

   - `DELETE /calculations/{id}`

8. **Profile + Password Feature (Final Project)**

   - `POST /profile/me` – confirm email + password and view profile  
   - `POST /profile/update` – change email and/or full name  
   - `POST /profile/change-password` – rotate password

---

## Docker

Build locally:

```bash
docker build -t fastapi-user-calculations-final .
docker run -p 8000:8000 fastapi-user-calculations-final
```

Pull from Docker Hub (after CI push):

```bash
docker pull pavankumarnagarju/fastapi-user-calculations-final:latest
docker run -p 8000:8000 pavankumarnagarju/fastapi-user-calculations-final:latest
```

---

## CI/CD Notes

GitHub Actions is configured to:

- Install dependencies  
- Run unit + integration tests  
- Run Playwright E2E tests  
- Build and push a Docker image to Docker Hub on `main` (when secrets are configured)

Required repository secrets:

- `DOCKERHUB_USERNAME`  
- `DOCKERHUB_TOKEN`

---

## Known Warnings

You may see warnings related to:

- Pydantic V2 config migration (`Config` vs `ConfigDict`)  
- `datetime.utcnow()` deprecation  
- SQLAlchemy legacy `.query().get()` API

These warnings **do not** cause tests to fail and are acceptable for this course unless stricter requirements are specified.
