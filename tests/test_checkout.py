import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.config import  DATA
from tests.conftest import logged_in_page


def test_checkout_happy_path(logged_in_page):
    inventory = logged_in_page
    items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    items_prices = inventory.get_inventory_items_with_prices()

    for item in items_to_add:
        inventory.add_item_to_cart(item)

    inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
    cart = CartPage(inventory.page)
    cart.is_on_cart_page()
    assert cart.get_cart_badge_count() == len(items_to_add)
    cart.proceed_to_checkout()
    checkout = CheckoutPage(inventory.page)
    assert checkout.is_on_checkout_page() is True
    data = DATA['valid_checkout']
    checkout.fill_personal_info(data['first_name'], data['last_name'],data['zip_code'])
    checkout.continue_to_overview()
    names = checkout.get_overview_item_names()
    assert set(names) == set(items_to_add)
    subtotal = checkout.get_subtotal()
    expected_subtotal = sum(items_prices[item] for item in items_to_add)
    assert abs(subtotal - expected_subtotal) < 0.01
    tax = checkout.get_tax()
    expected_tax = round(expected_subtotal * 0.08, 2)
    assert abs(tax - expected_tax) < 0.001
    total = checkout.get_total()
    expected_total = (expected_subtotal + expected_tax)
    assert abs(total - expected_total) < 0.01
    checkout.finish_purchase()
    assert checkout.is_complete_page() is True
    checkout.back_to_products()
    assert inventory.is_on_inventory_page() is True


@pytest.mark.parametrize("first, last, zip_code, expected_error_msg", [
    ("",      "Pérez",   "1414",   "Error: First Name is required"),
    ("Juan",  "",        "1414",   "Error: Last Name is required"),
    ("Juan",  "Pérez",   "",       "Error: Postal Code is required"),
    ("","","", "Error: First Name is required"),
])
def test_checkout_step_one_required_fields(logged_in_page, first, last, zip_code, expected_error_msg):
    inventory = logged_in_page

    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.click_element(InventoryPage.SHOPPING_CART_LINK)

    cart = CartPage(inventory.page)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(inventory.page)

    checkout.fill_personal_info(first, last, zip_code)
    checkout.continue_to_overview()

    assert checkout.is_error_visible()
    assert checkout.get_error_message() == expected_error_msg


def test_checkout_cancel_from_step_one(logged_in_page):
    inventory = logged_in_page
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
    cart = CartPage(inventory.page)
    cart.proceed_to_checkout()
    checkout = CheckoutPage(inventory.page)
    checkout.is_on_checkout_page()
    assert checkout.is_on_checkout_page() is True
    checkout.cancel_from_step_one()
    assert cart.is_on_cart_page() is True
    assert cart.get_cart_badge_count() == 1

def test_checkout_cancel_from_step_two(logged_in_page):
    inventory = logged_in_page
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
    cart = CartPage(inventory.page)
    cart.proceed_to_checkout()
    checkout = CheckoutPage(inventory.page)
    checkout.is_on_checkout_page()
    assert checkout.is_on_checkout_page() is True
    data = DATA['random_checkout']()
    checkout.fill_personal_info(data['first_name'], data['last_name'], data['zip_code'])
    checkout.continue_to_overview()
    checkout.get_subtotal()
    assert checkout.get_subtotal() is not None
    checkout.cancel_from_overview()
    inventory.is_on_inventory_page()
    assert "inventory.html" in inventory.page.url
    assert inventory.get_cart_badge_count() == 1

def test_checkout_without_items_on_cart(logged_in_page):
    inventory = logged_in_page
    inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
    cart = CartPage(inventory.page)
    cart.is_on_cart_page()
    assert cart.is_on_cart_page() is True
    cart.proceed_to_checkout()
    data = DATA['random_checkout']()
    checkout = CheckoutPage(inventory.page)
    checkout.fill_personal_info(data['first_name'], data['last_name'], data['zip_code'])
    checkout.continue_to_overview()
    checkout.get_total()
    assert checkout.get_subtotal() == 0.00
    checkout.finish_purchase()
    checkout.is_complete_page()
    assert checkout.is_complete_page() is False

    """This tests should fail because in a regular shopping web you can't make the checkout\\
     without items in the shopping cart, but this page let you make the checkout."""

def test_items_on_overview_are_correct(logged_in_page):
    inventory = logged_in_page
    items_to_add = ['Sauce Labs Backpack', 'Sauce Labs Onesie', 'Sauce Labs Fleece Jacket', 'Sauce Labs Bolt T-Shirt']
    for item in items_to_add:
        inventory.add_item_to_cart(item)

    inventory_prices= inventory.get_inventory_items_with_prices()
    inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
    cart_badge_count = inventory.get_cart_badge_count()
    cart = CartPage(inventory.page)
    cart.is_on_cart_page()
    assert cart.is_on_cart_page() is True
    cart.proceed_to_checkout()
    data = DATA['random_checkout']()
    checkout = CheckoutPage(inventory.page)
    checkout.fill_personal_info(data['first_name'], data['last_name'], data['zip_code'])
    checkout.continue_to_overview()
    checkout_count = checkout.get_overview_item_count()
    assert cart_badge_count == checkout_count
    checkout.get_overview_item_names()
    assert checkout.get_overview_item_names() == items_to_add
    checkout.get_overview_item_count()
    assert checkout.get_overview_item_count() == len(items_to_add)
    overview_prices = checkout.get_overview_items_with_prices()
    for name in items_to_add:
        assert name in overview_prices, f"Item '{name}' no aparece en overview"
        assert name in inventory_prices, f"Item '{name}' no encontrado en inventory (bug?)"
        assert abs(overview_prices[name] - inventory_prices[name]) < 0.001, \
            f"Precio de '{name}' no coincide: inventory ${inventory_prices[name]} vs overview ${overview_prices[name]}"
    expected_subtotal = sum(inventory_prices[name] for name in items_to_add)
    actual_subtotal = checkout.get_subtotal()
    assert abs(actual_subtotal - expected_subtotal) < 0.01
    tax = checkout.get_tax()
    expected_tax = round(expected_subtotal * 0.08, 2)
    assert abs(tax - expected_tax) < 0.001
    total = checkout.get_total()
    expected_total = (expected_subtotal + expected_tax)
    assert abs(total - expected_total) < 0.01
    checkout.finish_purchase()
    checkout.is_complete_page()
    assert checkout.is_complete_page() is True
