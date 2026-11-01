from playwright.sync_api import Page


class LoginPage:
    URL = "http://localhost:8000"

    def __init__(self, page: Page):
        self.page = page
        # selectorها فقط اینجا تعریف می‌شن
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")
        self.products_title = page.locator(".title")

    def open(self):
        self.page.goto(self.URL, wait_until="domcontentloaded")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
