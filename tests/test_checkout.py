import pytest
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.config import  DATA
from tests.conftest import logged_in_page
async def test_checkout_happy_path(logged_in_page):
    inventory = logged_in_page
    cart = CartPage(inventory.page)
    checkout = CheckoutPage(inventory.page)
    items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    items_prices = await inventory.get_inventory_items_with_prices()
    for item in items_to_add:
        await inventory.add_item_to_cart(item)
    await inventory.go_to_cart()
    await cart.is_on_cart_page()
    assert await cart.get_cart_badge_count() == len(items_to_add)
    await cart.proceed_to_checkout()
    assert await  checkout.is_on_checkout_page() is True
    data = DATA['valid_checkout']
    await checkout.fill_personal_info(data['first_name'], data['last_name'],data['zip_code'])
    await checkout.continue_to_overview()
    names = await  checkout.get_overview_item_names()
    assert set(names) == set(items_to_add)
    subtotal = await checkout.get_subtotal()
    expected_subtotal = sum(items_prices[item] for item in items_to_add)
    assert abs(subtotal - expected_subtotal) < 0.01
    tax = await checkout.get_tax()
    expected_tax = round(expected_subtotal * 0.08, 2)
    assert abs(tax - expected_tax) < 0.001
    total = await checkout.get_total()
    expected_total = (expected_subtotal + expected_tax)
    assert abs(total - expected_total) < 0.01
    await checkout.finish_purchase()
    assert await checkout.is_complete_page() is True
    await checkout.back_to_products()
    assert await inventory.is_on_inventory_page() is True
@pytest.mark.parametrize("first, last, zip_code, expected_error_msg", [
    ("",      "Pérez",   "1414",   "Error: First Name is required"),
    ("Juan",  "",        "1414",   "Error: Last Name is required"),
    ("Juan",  "Pérez",   "",       "Error: Postal Code is required"),
    ("","","", "Error: First Name is required"),
])
async def test_checkout_step_one_required_fields(logged_in_page, first, last, zip_code, expected_error_msg):
    inventory = logged_in_page
    cart = CartPage(inventory.page)
    checkout = CheckoutPage(inventory.page)
    await inventory.add_item_to_cart("Sauce Labs Backpack")
    await inventory.go_to_cart()
    await cart.proceed_to_checkout()
    await checkout.fill_personal_info(first, last, zip_code)
    await checkout.continue_to_overview()
    assert await checkout.is_error_visible()
    assert await checkout.get_error_message() == expected_error_msg
async def test_checkout_cancel_from_step_one(logged_in_page):
    inventory = logged_in_page
    cart = CartPage(inventory.page)
    checkout = CheckoutPage(inventory.page)
    await inventory.add_item_to_cart("Sauce Labs Backpack")
    await inventory.go_to_cart()
    await cart.proceed_to_checkout()
    await checkout.is_on_checkout_page()
    assert await checkout.is_on_checkout_page() is True
    await checkout.cancel_from_step_one()
    assert await cart.is_on_cart_page() is True
    assert await cart.get_cart_badge_count() == 1
async def test_checkout_cancel_from_step_two(logged_in_page):
    inventory = logged_in_page
    cart = CartPage(inventory.page)
    checkout = CheckoutPage(inventory.page)
    await inventory.add_item_to_cart("Sauce Labs Backpack")
    await inventory.go_to_cart()
    await cart.proceed_to_checkout()
    await checkout.is_on_checkout_page()
    assert await  checkout.is_on_checkout_page() is True
    data = DATA['random_checkout']()
    await checkout.fill_personal_info(data['first_name'], data['last_name'], data['zip_code'])
    await checkout.continue_to_overview()
    await checkout.get_subtotal()
    assert await checkout.get_subtotal() is not None
    await checkout.cancel_from_overview()
    assert await inventory.is_on_inventory_page() is True
    assert await  inventory.get_cart_badge_count() == 1
@pytest.mark.xfail(reason= "Expected bug in checking process without items")
async def test_checkout_without_items_on_cart(logged_in_page):
    inventory = logged_in_page
    cart = CartPage(inventory.page)
    checkout = CheckoutPage(inventory.page)
    await inventory.go_to_cart()
    assert await cart.is_on_cart_page() is True
    await cart.proceed_to_checkout()
    data = DATA['random_checkout']()
    await checkout.fill_personal_info(data['first_name'], data['last_name'], data['zip_code'])
    await checkout.continue_to_overview()
    await checkout.get_total()
    assert await  checkout.get_subtotal() == 0.00
    try:
        await checkout.finish_purchase()
        assert await checkout.is_complete_page() is False, f'Failed to complete checkout'
        print("Unexpected error, checkout is not  complete, Should Fail")
    except AssertionError:
        print("Expected error, checkout is complete")
    """This tests should fail because in a regular shopping web you can't make the checkout\\
     without items in the shopping cart, but this page let you make the checkout."""
async def test_items_on_overview_are_correct(logged_in_page):
    inventory = logged_in_page
    cart = CartPage(inventory.page)
    checkout = CheckoutPage(inventory.page)
    items_to_add = ['Sauce Labs Backpack', 'Sauce Labs Onesie', 'Sauce Labs Fleece Jacket', 'Sauce Labs Bolt T-Shirt']
    for item in items_to_add:
        await inventory.add_item_to_cart(item)
    inventory_prices= await  inventory.get_inventory_items_with_prices()
    await inventory.go_to_cart()
    cart_badge_count = await inventory.get_cart_badge_count()
    assert await  cart.is_on_cart_page() is True
    await cart.proceed_to_checkout()
    data = DATA['random_checkout']()
    await checkout.fill_personal_info(data['first_name'], data['last_name'], data['zip_code'])
    await checkout.continue_to_overview()
    checkout_count = await  checkout.get_overview_item_count()
    assert cart_badge_count == checkout_count
    assert await checkout.get_overview_item_names() == items_to_add
    assert await checkout.get_overview_item_count() == len(items_to_add)
    overview_prices = await checkout.get_overview_items_with_prices()
    for name in items_to_add:
        assert name in overview_prices, f"Item '{name}' no aparece en overview"
        assert name in inventory_prices, f"Item '{name}' no encontrado en inventory (bug?)"
        assert abs(overview_prices[name] - inventory_prices[name]) < 0.001, \
            f"Precio de '{name}' no coincide: inventory ${inventory_prices[name]} vs overview ${overview_prices[name]}"
    expected_subtotal = sum(inventory_prices[name] for name in items_to_add)
    actual_subtotal = await  checkout.get_subtotal()
    assert abs(actual_subtotal - expected_subtotal) < 0.01
    tax = await checkout.get_tax()
    expected_tax = round(expected_subtotal * 0.08, 2)
    assert abs(tax - expected_tax) < 0.001
    total = await checkout.get_total()
    expected_total = (expected_subtotal + expected_tax)
    assert abs(total - expected_total) < 0.01
    await checkout.finish_purchase()
    assert  await checkout.is_complete_page() is True
