import pytest
from playwright.sync_api import sync_playwright, expect, TimeoutError, Page
import re

# Reusable login helper
def login(page: Page, email: str, password: str):
    try:
        page.goto("https://app.workflowpro.com/login", timeout=15000)
        page.fill("#email", email)
        page.fill("#password", password)
        page.click("#login-btn")

        # Optional: check for 2FA screen
        if page.locator("#otp-input").is_visible(timeout=3000):
            print("2FA screen detected. Exiting login.")
            return False

        # Wait for either redirect or dashboard element
        expect(page).to_have_url(re.compile(r".*/dashboard"), timeout=10000)
        expect(page.locator(".welcome-message")).to_be_visible(timeout=10000)
        return True
    except TimeoutError as te:
        print(f"[Login TimeoutError] Page took too long to load or element missing: {te}")
        return False
    except Exception as e:
        print(f"[Login Exception] Something went wrong during login: {e}")
        return False

@pytest.mark.parametrize("email, password", [
    ("admin@company1.com", "password123"),
])
def test_user_login(email, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            success = login(page, email, password)
            assert success, "Login failed — possibly due to 2FA or timeout"
        finally:
            browser.close()

@pytest.mark.parametrize("email, password, tenant_keyword", [
    ("user@company2.com", "password123", "Company2"),
])
def test_multi_tenant_access(email, password, tenant_keyword):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            success = login(page, email, password)
            assert success, "Login failed — possibly due to 2FA or timeout"

            expect(page.locator(".project-card").first).to_be_visible(timeout=10000)
            cards = page.locator(".project-card")
            for i in range(cards.count()):
                content = cards.nth(i).text_content()
                assert tenant_keyword in content, f"Tenant data mismatch in card {i}"
        finally:
            browser.close()
