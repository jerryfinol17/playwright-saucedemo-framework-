from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


def test_e2e_cart(logged_in_page):
	inventory = logged_in_page
	items_to_add= ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt (Red)"]
	prices = inventory.get_price_list()
	for item in items_to_add:
		inventory.add_item_to_cart(item)
	assert inventory.get_cart_badge_count() == 6
	inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
	cart = CartPage(inventory.page)
	assert cart.is_on_cart_page() is True
	assert cart.get_title_text() == "Your Cart"
	assert cart.get_cart_badge_count() == 6
	assert cart.get_cart_item_names() == items_to_add
	assert cart.get_cart_item_prices() == prices
	for item in items_to_add:
		assert cart.get_item_quantity(item) == 1
	for item in items_to_add:
		cart.remove_item_from_cart(item)
	assert cart.is_cart_empty() is True
	cart.click_element(CartPage.BURGER_MENU_BUTTON)
	cart.click_element(CartPage.ALL_ITEMS_LINK)
	assert inventory.is_on_inventory_page() is True

