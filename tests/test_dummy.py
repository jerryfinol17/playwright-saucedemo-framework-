import pytest
from playwright.async_api import expect
from pages.base_page  import BasePage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.config import CREDENTIALS, DATA
from pages.locators import INVENTORY


async def test_base_page_init(page):
    base = BasePage(page)
    assert base.page == page
    assert base.timeout == 15000


async def test_saucedemo_title(page):
    await expect(page).to_have_title("Swag Labs")


async def test_login_work(page):
    login = LoginPage(page)
    user = CREDENTIALS["standard"]
    assert await login.is_on_base_page()
    await login.login(user["username"], user["password"])
    assert await login.is_login_ok()


async def test_inventory_dummy(page):
    login = LoginPage(page)
    user = CREDENTIALS["standard"]

    assert await login.is_on_base_page()
    await login.login(user["username"], user["password"])
    assert await login.is_login_ok()

    inventory = InventoryPage(page)
    assert await inventory.is_on_inventory_page()
    assert await inventory.get_title_text() == "Products"
    assert await inventory.get_cart_badge_count() == 0

    await inventory.add_item_to_cart("Sauce Labs Backpack")
    assert await inventory.get_cart_badge_count() == 1


async def test_cart_dummy(page):
    login = LoginPage(page)
    user = CREDENTIALS["standard"]

    await login.login(user["username"], user["password"])

    inventory = InventoryPage(page)
    await inventory.add_item_to_cart("Sauce Labs Backpack")
    await inventory.add_item_to_cart("Sauce Labs Bike Light")

    await inventory.click_element(INVENTORY["SHOPPING_CART_LINK"])

    cart = CartPage(page)
    assert await cart.is_on_cart_page()
    assert await cart.get_title_text() == "Your Cart"
    assert await cart.get_cart_badge_count() == 2

    names = await cart.get_cart_item_names()
    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Bike Light" in names

    assert await cart.get_item_quantity("Sauce Labs Backpack") == 1

    await cart.remove_item_from_cart("Sauce Labs Bike Light")
    assert await cart.get_cart_badge_count() == 1


async def test_add_item_badge_updates(logged_in_page):
    await logged_in_page.add_item_to_cart("Sauce Labs Backpack")
    assert await logged_in_page.get_cart_badge_count() == 1


async def test_checkout_work(page):
    login = LoginPage(page)
    user = CREDENTIALS["standard"]
    data = DATA["valid_checkout"]

    await login.login(user["username"], user["password"])

    inventory = InventoryPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)

    await inventory.add_item_to_cart("Sauce Labs Bike Light")
    await inventory.add_item_to_cart("Sauce Labs Backpack")
    await inventory.click_element(INVENTORY["SHOPPING_CART_LINK"])

    assert await cart.is_on_cart_page()

    await cart.proceed_to_checkout()

    assert await checkout.is_on_checkout_page()

    await checkout.fill_personal_info(data["first_name"], data["last_name"], data["zip_code"])
    await checkout.continue_to_overview()
    await checkout.finish_purchase()

    assert await checkout.is_complete_page() is True


async def test_sorting_name(logged_in_page):
    inventory = logged_in_page
    await inventory.select_sort_option("za")
    names = await inventory.get_name_list()
    expected = sorted(names, reverse=True)
    assert names == expected


async def test_sorting_price(logged_in_page):
    inventory = logged_in_page
    await inventory.select_sort_option("lohi")
    prices = await inventory.get_price_list()
    expected = sorted(prices)
    assert prices == expected