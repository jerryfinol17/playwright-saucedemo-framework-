from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.config import DATA
import pytest

@pytest.mark.e2e
@pytest.mark.record_video
async def test_e2e_happy_path(logged_in_page):
	inventory = logged_in_page
	cart = CartPage(inventory.page)
	checkout = CheckoutPage(inventory.page)
	login = LoginPage(inventory.page)
	items_prices= await inventory.get_inventory_items_with_prices()
	items_to_add = ["Sauce Labs Backpack",
	                "Sauce Labs Bike Light",
	                "Sauce Labs Bolt T-Shirt",
	                "Sauce Labs Fleece Jacket",
	                "Sauce Labs Onesie",
	                "Test.allTheThings() T-Shirt (Red)"]
	items_to_remove = ["Test.allTheThings() T-Shirt (Red)",
	                   "Sauce Labs Onesie"]
	final_item = [item for item in items_to_add if item not in items_to_remove]
	data = DATA["random_checkout"]()
	assert await inventory.is_on_inventory_page() is True
	for item in items_to_add:
		await inventory.add_item_to_cart(item)
	assert await inventory.get_cart_badge_count() == len(items_to_add)
	await inventory.go_to_cart()
	assert await cart.is_on_cart_page() is True
	assert await cart.get_cart_badge_count() == len(items_to_add)
	for item in items_to_remove:
		await cart.remove_item_from_cart(item)
	assert await  cart.get_cart_badge_count() == len(final_item)
	assert await cart.get_cart_item_names() == final_item
	prices = await cart.get_cart_item_prices()
	print(f'prices = {prices}')
	await cart.proceed_to_checkout()
	assert await checkout.is_on_checkout_page()is True
	await checkout.fill_personal_info(data['first_name'], data['last_name'], data['zip_code'])
	await checkout.continue_to_overview()
	names = await  checkout.get_overview_item_names()
	assert set(names) == set(final_item)
	subtotal = await checkout.get_subtotal()
	expected_subtotal = sum(items_prices[item] for item in final_item)
	assert abs(subtotal - expected_subtotal) < 0.01
	tax = await checkout.get_tax()
	expected_tax = round(expected_subtotal * 0.08, 2)
	assert abs(tax - expected_tax) < 0.001
	total = await checkout.get_total()
	expected_total = (expected_subtotal + expected_tax)
	assert abs(total - expected_total) < 0.01
	print(f'total = {total}')
	await checkout.finish_purchase()
	assert await checkout.is_complete_page() is True
	await checkout.back_to_products()
	assert await inventory.is_on_inventory_page() is True
	await login.logout()
	assert await login.is_on_base_page() is True
	print("Video path:", inventory.page.video.path() if inventory.page.video else "No video")