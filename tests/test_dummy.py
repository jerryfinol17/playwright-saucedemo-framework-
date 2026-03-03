from playwright.sync_api import expect
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.config import CREDENTIALS, DATA

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
    assert login.is_on_base_page()
    login.login(user["username"], user["password"])
    assert login.is_login_ok()


def test_inventory_dummy(page):
    login = LoginPage(page)
    user = CREDENTIALS["standard"]
    assert login.is_on_base_page()
    login.login(user["username"], user["password"])
    assert login.is_login_ok()

    inventory = InventoryPage(page)
    assert inventory.is_on_inventory_page()
    assert inventory.get_title_text() == "Products"
    assert inventory.get_cart_badge_count() == 0

    inventory.add_item_to_cart("Sauce Labs Backpack")
    assert inventory.get_cart_badge_count() == 1

def test_cart_dummy(page):
    login = LoginPage(page)
    user = CREDENTIALS["standard"]
    login.login(user["username"], user["password"])
    inventory = InventoryPage(page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.add_item_to_cart("Sauce Labs Bike Light")
    inventory.click_element(inventory.SHOPPING_CART_LINK)
    cart = CartPage(page)
    assert cart.is_on_cart_page()
    assert cart.get_title_text() == "Your Cart"
    assert cart.get_cart_badge_count() == 2
    names = cart.get_cart_item_names()
    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Bike Light" in names
    assert cart.get_item_quantity("Sauce Labs Backpack") == 1
    cart.remove_item_from_cart("Sauce Labs Bike Light")
    assert cart.get_cart_badge_count() == 1

def test_add_item_badge_updates(logged_in_page):
    logged_in_page.add_item_to_cart("Sauce Labs Backpack")
    assert logged_in_page.get_cart_badge_count() ==(1)


def test_checkout_work(page):
    login = LoginPage(page)
    user = CREDENTIALS["standard"]
    data = DATA["valid_checkout"]
    inventory = InventoryPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)
    login.login(user["username"], user["password"])
    inventory.add_item_to_cart("Sauce Labs Bike Light")
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.click_element(inventory.SHOPPING_CART_LINK)
    assert cart.is_on_cart_page()
    names = cart.get_cart_item_names()
    assert "Sauce Labs Bike Light" in names
    assert "Sauce Labs Backpack" in names
    cart.proceed_to_checkout()
    checkout.is_on_checkout_page()
    checkout.fill_personal_info(data["first_name"], data["last_name"], data["zip_code"])
    checkout.continue_to_overview()
    checkout.get_subtotal_text()
    checkout.finish_purchase()
    checkout.is_complete_page()
    assert checkout.is_complete_page() is True

def test_sorting_name(logged_in_page):
    inventory = logged_in_page
    inventory.select_sort_option("za")
    names = inventory.get_name_list()
    expected = sorted(names, reverse=True)
    assert names == expected, f'Z to A Fallo: {names} != {expected}'

def test_sorting_price(logged_in_page):
    inventory = logged_in_page
    inventory.select_sort_option("lohi")
    prices = inventory.get_price_list()
    expected = sorted(prices)
    assert prices == expected, f'Lohi to A Fallo: {prices} != {expected}'


