from playwright.sync_api import expect
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
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
    assert login.is_on_login_page()
    login.login(user["username"], user["password"])
    assert login.is_login_ok()


def test_inventory_dummy(page):
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    assert inventory.is_on_inventory_page()
    assert inventory.get_title_text() == "Products"
    assert inventory.get_cart_badge_count() == 0

    inventory.add_item_to_cart("Sauce Labs Backpack")
    assert inventory.get_cart_badge_count() == 1
