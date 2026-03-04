import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.config import CREDENTIALS
import time

POSITIVE_USERS = [
    ("standard", True),
    ("problem", False),
    ("visual", False),
    ("error", False),
    ("performance", True),
]

@pytest.mark.parametrize("user_key, should_measure_time", POSITIVE_USERS)
def test_login_positive(page: Page, user_key: str, should_measure_time: bool) -> None:
    creds = CREDENTIALS[user_key]
    login = LoginPage(page)

    start_time = time.perf_counter() if should_measure_time else None

    login.login(creds["username"], creds["password"])

    expect(page.locator(LoginPage.INVENTORY_TITLE)).to_be_visible(timeout=20000)

    assert login.is_login_ok() is True

    if should_measure_time:
        duration = time.perf_counter() - start_time
        print(f"{user_key} login + load took: {duration:.2f} seconds")
        assert duration > 1.0, f"{user_key} too fast for glitch: {duration:.2f}s"
        assert duration < 12.0, f"{user_key} too slow: {duration:.2f}s"

    if user_key in ["standard", "visual", "performance"]:
        page.screenshot(
            path=f"screenshots/login_{user_key}_success.png",
            full_page=True
        )

NEGATIVE_USERS = [
("locked", ["Sorry", "locked"]),
    ("blank_user", ["Username", "required"]),
    ("blank_password", ["Password", "required"]),
    ("invalid_user", ["Username", "do not match"]),
    ("invalid_password", ["password", "do not match"]),
    ("all_blank", ["Username", "required"])
]

@pytest.mark.parametrize("user_key, expected_keywords", NEGATIVE_USERS)
def test_login_negative(page: Page, user_key: str, expected_keywords: list[str]) -> None:
    creds = CREDENTIALS[user_key]
    login = LoginPage(page)
    login.login(creds["username"], creds["password"])
    assert login.is_error_visible() is True
    error_msg = login.get_error_message_or_empty()
    error_lower = error_msg.lower()
    for keyword in expected_keywords:
        assert keyword.lower() in error_lower, \
        f"Expected '{keyword}' to be in, but got:  '{error_lower}'"


def test_logout(page: Page) -> None:
    creds = CREDENTIALS["standard"]
    login = LoginPage(page)

    login.login(creds["username"], creds["password"])
    assert login.is_login_ok() is True

    login.click_element(LoginPage.BURGER_MENU_BUTTON)
    login.click_element(LoginPage.LOGOUT_BUTTON)

    assert login.is_on_base_page() is True