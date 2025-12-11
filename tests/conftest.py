"""
Pytest configuration and fixtures for Playwright E2E tests.
"""
import pytest
import os


@pytest.fixture(scope="session")
def base_url():
    """Get the base URL for tests."""
    return os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="function")
def page(browser):
    """Create a new page for each test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
