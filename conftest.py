import pytest

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "executable_path": "/snap/bin/chromium",
    }

@pytest.fixture(autouse=True)
def fast_page(page):
    page.set_default_navigation_timeout(60000)
    page.set_default_timeout(15000)
    yield
