# JWT Authentication Module 13

A complete JWT-based authentication system with FastAPI backend, HTML/CSS/JS frontend, Playwright E2E tests, and CI/CD pipeline.

## Features

- JWT Authentication with registration and login
- Password hashing with bcrypt
- Pydantic validation for email format and password strength
- Frontend pages with client-side validation
- Playwright E2E tests (positive and negative scenarios)
- CI/CD pipeline with GitHub Actions and Docker Hub deployment

## Quick Start
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://localhost:8000

## Running Tests
```bash
# Unit tests
pytest tests/test_unit.py -v

# E2E tests
playwright install chromium
uvicorn app.main:app &
pytest tests/test_e2e.py -v
```

## Docker
```bash
docker-compose up --build
```

## API Endpoints

- POST /api/register - Register new user
- POST /api/login - Login and get JWT token
- GET /api/health - Health check

## GitHub Secrets Required

- DOCKER_USERNAME
- DOCKER_PASSWORD

## Docker Hub

Image: ishanr83/jwt-module13:latest
