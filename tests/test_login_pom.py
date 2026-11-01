import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page):
    lp = LoginPage(page)
    lp.open()
    return lp


# TC-LOGIN-001
def test_successful_login(login_page: LoginPage, page: Page):
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url(f"{LoginPage.URL}/#/inventory")
    expect(login_page.products_title).to_have_text("Products")


# TC-LOGIN-003
def test_empty_username(login_page: LoginPage):
    login_page.login("", "secret_sauce")
    expect(login_page.error_message).to_contain_text("Username is required")


# TC-LOGIN-004
def test_empty_password(login_page: LoginPage):
    login_page.login("standard_user", "")
    expect(login_page.error_message).to_contain_text("Password is required")


# TC-LOGIN-005
def test_locked_out_user(login_page: LoginPage):
    login_page.login("locked_out_user", "secret_sauce")
    expect(login_page.error_message).to_contain_text("locked out")


# TC-LOGIN-002, 008, 009, 011
@pytest.mark.parametrize("username, password", [
    ("standard_user", "wrong_pass"),
    ("STANDARD_USER", "secret_sauce"),
    ("standard_user", "SECRET_SAUCE"),
    ("unknown_user", "secret_sauce"),
])
def test_invalid_credentials(login_page: LoginPage, username, password):
    login_page.login(username, password)
    expect(login_page.error_message).to_contain_text("Username and password do not match")
