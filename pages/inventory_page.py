from playwright.sync_api import Page
from pages.base_page import BasePage

class InventoryPage(BasePage):
	PRIMARY_HEADER = '[data-test="primary-header"]'
	SHOPPING_CART_LINK = '[data-test="shopping-cart-link"]'
	SHOPPING_CART_BADGE = '.shopping_cart_badge'
	BURGER_MENU_BUTTON = '#react-burger-menu-btn'
	ABOUT_LINK = '[data-test="about-sidebar-link"]'
	RESET_APP_LINK = '[data-test="reset-sidebar-link"]'
	TITLE = '[data-test="title"]'
	SORT_DROPDOWN = '[data-test="product_sort_container"]'
	PRODUCT_ITEM = '.inventory_item'
	PRODUCT_NAME = '.inventory_item_name'
	PRODUCT_PRICE = '.inventory_item_price'
	PRODUCT_DESCRIPTION = '[data-test="inventory-item-desc"]'

	def __init__(self, page: Page):
		super().__init__(page)

	def is_on_inventory_page(self) -> bool:
		return 'inventory.html' in self.page.url

	def about_btn_work(self) -> bool:
		self.click_element(InventoryPage.BURGER_MENU_BUTTON)
		self.click_element(InventoryPage.ABOUT_LINK)
		return 'saucelabs.com' in self.page.url

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
	def get_product_description(self, product_name: str) -> str:

		items = self.page.locator(self.PRODUCT_ITEM).all()
		for item in items:
			name = item.locator(self.PRODUCT_NAME).inner_text().strip()
			if name == product_name:
				return item.locator(self.PRODUCT_DESCRIPTION).inner_text().strip()
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

	def get_inventory_items_with_prices(self) -> dict[str, float]:
		items = {}
		for item_locator in self.page.locator(self.PRODUCT_ITEM).all():
			name = item_locator.locator(self.PRODUCT_NAME).inner_text().strip()
			price_str = item_locator.locator(self.PRODUCT_PRICE).inner_text().strip()
			price = float(price_str.replace("$", "").strip())
			items[name] = price
		return items


	def is_remove_button_visible(self, item_name: str) -> bool:
		items = self.page.locator(self.PRODUCT_ITEM).all()
		for item in items:
			name = item.locator(self.PRODUCT_NAME).inner_text().strip()
			if name == item_name:
				remove_button = item.locator('[data-test^="remove-"]')
				return self.is_visible(remove_button)
		return False
	def add_item_is_visible(self, item_name: str) -> bool:
		items = self.page.locator(self.PRODUCT_ITEM).all()
		for item in items:
			name = item.locator(self.PRODUCT_NAME).inner_text().strip()
			if name == item_name:
				add_button = item.locator('[data-test^="add-to-cart-"]')
				return self.is_visible(add_button)
		return False
	def select_sort_option(self, value: str) -> None:
		self.page.locator(".product_sort_container").select_option(value)

	def get_name_list(self) -> list[str]:
		elements = self.page.locator(self.PRODUCT_NAME).all()
		return [el.inner_text().strip() for el in elements]

	def get_price_list(self) -> list[float]:
		elements = self.page.locator(self.PRODUCT_PRICE).all()
		return [float(el.inner_text().replace("$", "").strip()) for el in elements]

