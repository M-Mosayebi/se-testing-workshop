import pytest
from playwright.sync_api import Page, expect

URL = "http://localhost:8000"


# TC-LOGIN-001: ورود موفق
def test_successful_login(page: Page):
    page.goto(URL, wait_until="domcontentloaded")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url(f"{URL}/#/inventory")
    expect(page.locator(".title")).to_have_text("Products")


# TC-LOGIN-003: نام کاربری خالی
def test_empty_username(page: Page):
    page.goto(URL, wait_until="domcontentloaded")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page.locator("[data-test='error']")).to_contain_text("Username is required")


# TC-LOGIN-004: رمز عبور خالی
def test_empty_password(page: Page):
    page.goto(URL, wait_until="domcontentloaded")
    page.fill("#user-name", "standard_user")
    page.click("#login-button")

    expect(page.locator("[data-test='error']")).to_contain_text("Password is required")


# TC-LOGIN-005: کاربر قفل‌شده
def test_locked_out_user(page: Page):
    page.goto(URL, wait_until="domcontentloaded")
    page.fill("#user-name", "locked_out_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page.locator("[data-test='error']")).to_contain_text("locked out")


# TC-LOGIN-002, 008, 009, 011: اطلاعات اشتباه (یک تست با چند داده)
@pytest.mark.parametrize("username, password", [
    ("standard_user", "wrong_pass"),     # TC-002
    ("STANDARD_USER", "secret_sauce"),   # TC-008
    ("standard_user", "SECRET_SAUCE"),   # TC-009
    ("unknown_user", "secret_sauce"),    # TC-011
])
def test_invalid_credentials(page: Page, username, password):
    page.goto(URL, wait_until="domcontentloaded")
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")

    expect(page.locator("[data-test='error']")).to_contain_text(
        "Username and password do not match"
    )
    expect(page).to_have_url(f"{URL}/")


