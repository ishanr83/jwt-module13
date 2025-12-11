"""
Playwright E2E tests for JWT authentication.
"""
import pytest
from playwright.sync_api import Page, expect
import random
import string


def generate_random_email():
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@example.com"


def generate_random_username():
    return ''.join(random.choices(string.ascii_lowercase, k=8))


class TestRegistrationPositive:
    def test_register_with_valid_data(self, page: Page, base_url: str):
        page.goto(f"{base_url}/register")
        email = generate_random_email()
        username = generate_random_username()
        page.fill("#username", username)
        page.fill("#email", email)
        page.fill("#password", "SecurePass123")
        page.fill("#confirm-password", "SecurePass123")
        page.click("#submit-btn")
        success_message = page.locator("#success-message")
        expect(success_message).to_be_visible(timeout=10000)
        expect(success_message).to_contain_text("Registration successful")


class TestRegistrationNegative:
    def test_register_with_short_password(self, page: Page, base_url: str):
        page.goto(f"{base_url}/register")
        page.fill("#username", "testuser")
        page.fill("#email", "test@example.com")
        page.fill("#password", "short")
        page.fill("#confirm-password", "short")
        page.click("#submit-btn")
        password_error = page.locator("#password-error")
        expect(password_error).to_be_visible()
        expect(password_error).to_contain_text("at least 8 characters")

    def test_register_with_invalid_email(self, page: Page, base_url: str):
        page.goto(f"{base_url}/register")
        page.fill("#username", "testuser")
        page.fill("#email", "invalidemail")
        page.fill("#password", "SecurePass123")
        page.fill("#confirm-password", "SecurePass123")
        page.click("#submit-btn")
        email_error = page.locator("#email-error")
        expect(email_error).to_be_visible()
        expect(email_error).to_contain_text("valid email")


class TestLoginPositive:
    def test_login_with_valid_credentials(self, page: Page, base_url: str):
        page.goto(f"{base_url}/register")
        email = generate_random_email()
        username = generate_random_username()
        page.fill("#username", username)
        page.fill("#email", email)
        page.fill("#password", "SecurePass123")
        page.fill("#confirm-password", "SecurePass123")
        page.click("#submit-btn")
        expect(page.locator("#success-message")).to_be_visible(timeout=10000)
        page.evaluate("localStorage.clear()")
        page.goto(f"{base_url}/login")
        page.fill("#email", email)
        page.fill("#password", "SecurePass123")
        page.click("#submit-btn")
        success_message = page.locator("#success-message")
        expect(success_message).to_be_visible(timeout=10000)
        expect(success_message).to_contain_text("Login successful")


class TestLoginNegative:
    def test_login_with_wrong_password(self, page: Page, base_url: str):
        page.goto(f"{base_url}/register")
        email = generate_random_email()
        username = generate_random_username()
        page.fill("#username", username)
        page.fill("#email", email)
        page.fill("#password", "SecurePass123")
        page.fill("#confirm-password", "SecurePass123")
        page.click("#submit-btn")
        expect(page.locator("#success-message")).to_be_visible(timeout=10000)
        page.evaluate("localStorage.clear()")
        page.goto(f"{base_url}/login")
        page.fill("#email", email)
        page.fill("#password", "WrongPassword123")
        page.click("#submit-btn")
        server_error = page.locator("#server-error")
        expect(server_error).to_be_visible(timeout=10000)
        expect(server_error).to_contain_text("Invalid credentials")

    def test_login_with_unregistered_email(self, page: Page, base_url: str):
        page.goto(f"{base_url}/login")
        page.fill("#email", "nonexistent@example.com")
        page.fill("#password", "SomePassword123")
        page.click("#submit-btn")
        server_error = page.locator("#server-error")
        expect(server_error).to_be_visible(timeout=10000)
        expect(server_error).to_contain_text("Invalid credentials")
