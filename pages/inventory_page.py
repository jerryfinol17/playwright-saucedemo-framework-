from playwright.sync_api import Page
from pages.base_page import BasePage

class InventoryPage(BasePage):
	PRIMARY_HEADER = '[data-test="primary-header"]'
	SHOPPING_CART_LINK = '[data-test="shopping-cart-link"]'
	SHOPPING_CART_BADGE = '.shopping_cart_badge'
	BURGER_MENU_BUTTON = '#react-burger-menu-btn'
	TITLE = '[data-test="title"]'
	SORT_DROPDOWN = '[data-test="product_sort_container"]'
	PRODUCT_ITEM = '.inventory_item'
	PRODUCT_NAME = '.inventory_item_name'
	PRODUCT_PRICE = '.inventory_item_price'

	def __init__(self, page: Page):
		super().__init__(page)

	def is_on_inventory_page(self) -> bool:
		return 'inventory.html' in self.page.url

	def primary_header_is_visible(self) -> bool:
		return self.is_visible(self.PRIMARY_HEADER)

	def get_title_text(self) -> str:
		return self.get_text(self.TITLE).strip()

	def get_cart_badge_count(self) -> int:
		if not self.is_visible(self.SHOPPING_CART_BADGE):
			return 0
		count_text = self.get_text(self.SHOPPING_CART_BADGE).strip()
		return int(count_text) if count_text.isdigit() else 0

	def get_product_name(self, product_name: str) -> str:

		items = self.page.locator(self.PRODUCT_ITEM).all()
		for item in items:
			name = item.locator(self.PRODUCT_NAME).inner_text().strip()
			if name == product_name:
				return name
		return ""

	def get_product_price(self, product_name: str) -> str:
		items = self.page.locator(self.PRODUCT_ITEM).all()
		for item in items:
			name = item.locator(self.PRODUCT_NAME).inner_text().strip()
			if name == product_name:
				return item.locator(self.PRODUCT_PRICE).inner_text().strip()
		return ""

	def add_item_to_cart(self, item_name: str) -> None:
		items = self.page.locator(self.PRODUCT_ITEM).all()
		for item in items:
			name = item.locator(self.PRODUCT_NAME).inner_text().strip()
			if name == item_name:
				add_button = item.locator('[data-test^="add-to-cart-"]')
				self.click_element(add_button)
				return
		raise ValueError(f"Producto '{item_name}' no encontrado en el inventario")

	def remove_item_from_cart(self, item_name: str) -> None:
		items = self.page.locator(self.PRODUCT_ITEM).all()
		for item in items:
			name = item.locator(self.PRODUCT_NAME).inner_text().strip()
			if name == item_name:
				remove_button = item.locator('[data-test^="remove-"]')
				self.click_element(remove_button)
				return
		raise ValueError(f"Producto '{item_name}' no encontrado para remover")



