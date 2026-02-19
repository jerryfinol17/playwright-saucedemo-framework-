from playwright.sync_api import expect

from pages import config
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.config import CREDENTIALS

def test_base_page_init(page):
    base = BasePage(page)
    assert base.page == page
    assert base.timeout == 15000
    print("URL inicial:", base.get_current_url())

def test_saucedemo_title(page):
    expect(page).to_have_title("Swag Labs")

def test_login_work(page):
    login = LoginPage(page)
    user = CREDENTIALS["standard"]
    login.login(user["username"], user["password"])
    assert login.is_login_sucessful()

