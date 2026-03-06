from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.config import DATA
import pytest

@pytest.mark.e2e
def test_e2e_happy_path(logged_in_page):
	inventory = logged_in_page
	items_prices= inventory.get_inventory_items_with_prices()
	items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt (Red)"]
	items_to_remove = ["Test.allTheThings() T-Shirt (Red)", "Sauce Labs Onesie"]
	final_item = [item for item in items_to_add if item not in items_to_remove]
	data = DATA["random_checkout"]()
	assert inventory.is_on_inventory_page() is True
	for item in items_to_add:
		inventory.add_item_to_cart(item)
	assert inventory.get_cart_badge_count() == 6
	inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
	cart = CartPage(inventory.page)
	assert cart.is_on_cart_page() is True
	assert cart.get_cart_badge_count() == 6
	for item in items_to_remove:
		cart.remove_item_from_cart(item)
	assert cart.get_cart_badge_count() == 4
	assert cart.get_cart_item_names() == final_item
	prices = cart.get_cart_item_prices()
	print(f'prices = {prices}')
	cart.proceed_to_checkout()
	checkout = CheckoutPage(inventory.page)
	assert checkout.is_on_checkout_page()is True
	checkout.fill_personal_info(data['first_name'], data['last_name'], data['zip_code'])
	checkout.continue_to_overview()
	names = checkout.get_overview_item_names()
	assert set(names) == set(final_item)
	subtotal = checkout.get_subtotal()
	expected_subtotal = sum(items_prices[item] for item in final_item)
	assert abs(subtotal - expected_subtotal) < 0.01
	tax = checkout.get_tax()
	expected_tax = round(expected_subtotal * 0.08, 2)
	assert abs(tax - expected_tax) < 0.001
	total = checkout.get_total()
	expected_total = (expected_subtotal + expected_tax)
	assert abs(total - expected_total) < 0.01
	print(f'total = {total}')
	checkout.finish_purchase()
	assert checkout.is_complete_page() is True
	checkout.back_to_products()
	assert inventory.is_on_inventory_page() is True
	login = LoginPage(inventory.page)
	login.click_element(LoginPage.BURGER_MENU_BUTTON)
	login.click_element(LoginPage.LOGOUT_BUTTON)
	assert login.is_on_base_page() is True
	print("Video path:", inventory.page.video.path() if inventory.page.video else "No video")