# Module 13 Reflection Document

## Project Overview
Implemented JWT-based authentication system with FastAPI backend, HTML/CSS/JS frontend, Playwright E2E tests, and CI/CD pipeline.

## Key Experiences

### JWT Authentication Implementation
- Implemented secure user registration with password hashing using bcrypt
- Created login endpoint that validates credentials and returns JWT tokens
- Used Pydantic schemas for input validation (email format, password length)

### Frontend Development
- Built responsive registration and login pages with modern CSS
- Implemented client-side validation with real-time visual feedback
- Stored JWT tokens in localStorage for session management

### Playwright E2E Testing
- Wrote positive tests for successful registration and login flows
- Wrote negative tests for invalid inputs (short password, wrong credentials)
- Learned to use Playwright locators and assertions

### CI/CD Pipeline
- Configured GitHub Actions to run unit tests and E2E tests automatically
- Set up PostgreSQL service container for testing
- Automated Docker image build and push to Docker Hub

## Challenges Faced

### Challenge 1: Dependency Conflicts
- pytest-asyncio required pytest<8, but requirements specified pytest==8.0.0
- Solution: Downgraded pytest to 7.4.4 for compatibility

### Challenge 2: Database Configuration
- Had to handle different database URLs for SQLite (local) vs PostgreSQL (CI/CD)
- Solution: Used environment variables and conditional connection arguments

### Challenge 3: Playwright Test Timing
- E2E tests initially failed due to timing issues with async operations
- Solution: Added proper waits and timeouts for UI elements

## Learning Outcomes Achieved
- CLO3: Created Python applications with automated testing
- CLO4: Set up GitHub Actions for CI/CD
- CLO9: Containerized application using Docker
- CLO10: Created and tested REST APIs
- CLO11: Integrated with SQL databases
- CLO12: Used Pydantic for JSON validation
- CLO13: Implemented secure authentication with hashing and JWT

## Conclusion
This module provided hands-on experience with full-stack authentication implementation, automated testing, and DevOps practices.
