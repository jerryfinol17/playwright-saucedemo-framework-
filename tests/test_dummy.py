from playwright.sync_api import expect
from pages.base_page import BasePage

def test_base_page_init(page):
    base = BasePage(page)
    assert base.page == page
    assert base.timeout == 15000
    print("URL inicial:", base.get_current_url())

def test_saucedemo_title(page):
    expect(page).to_have_title("Swag Labs")