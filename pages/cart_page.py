from playwright.sync_api import Page
from pages.base_page import BasePage

class CartPage(BasePage):
	TITLE = '[data-test=title]'
	CONTINUE_SHOPPING_BTN = '[data-test=continue-shopping]'
	CHECKOUT_BTN = '[data-test=checkout]'
	CART_ITEM = '[data-test="inventory-item"]'
	BURGER_MENU_BUTTON = '#react-burger-menu-btn'
	ALL_ITEMS_LINK = '[data-test=inventory-sidebar-link]'
	SHOPPING_CART_BADGE = '.shopping_cart_badge'
	PRODUCT_NAME = '.inventory_item_name'
	PRODUCT_PRICE = '.inventory_item_price'
	CART_QUANTITY = '[data-test="item-quantity"]'
	REMOVE_BTN = '[data-test^="remove-"]'

	def __init__(self, page: Page):
		super().__init__(page)

	def is_on_cart_page(self) -> bool:
		return 'cart.html' in self.page.url

	def get_title_text(self) -> str:
		return self.get_text(self.TITLE).strip()

	def get_cart_badge_count(self) -> int:
		if not self.is_visible(self.SHOPPING_CART_BADGE):
			return 0
		count_text = self.get_text(self.SHOPPING_CART_BADGE).strip()
		return int(count_text) if count_text.isdigit() else 0


	def get_cart_item_names(self) -> list[str]:
		names = []
		for item in self.page.locator(self.CART_ITEM).all():
			name = item.locator(self.PRODUCT_NAME).inner_text().strip()
			names.append(name)
		return names

	def get_cart_item_prices(self) -> list[str]:
		prices = []
		for item in self.page.locator(self.CART_ITEM).all():
			price = item.locator(self.PRODUCT_PRICE).inner_text().strip()
			prices.append(price)
		return prices

	def get_item_quantity(self, item_name: str) -> int:
		items = self.page.locator(self.CART_ITEM).all()
		for item in items:
			name = item.locator(self.PRODUCT_NAME).inner_text().strip()
			if name == item_name:
				quantity_text = item.locator(self.CART_QUANTITY).inner_text().strip()
				return int(quantity_text) if quantity_text.isdigit() else 0
		return 0

	def is_cart_empty(self) -> bool:
		return self.get_cart_badge_count() == 0


	def remove_item_from_cart(self, item_name: str) -> None:
		items = self.page.locator(self.CART_ITEM).all()
		for item in items:
			name = item.locator(self.PRODUCT_NAME).inner_text().strip()
			if name == item_name:
				remove_button = item.locator('[data-test^="remove-"]')
				self.click_element(remove_button)
				return
		raise ValueError(f"Producto '{item_name}' no encontrado para remover")

	def proceed_to_checkout(self) -> None:
		self.click_element(self.CHECKOUT_BTN)

	def continue_shopping(self) -> None:
		self.click_element(self.CONTINUE_SHOPPING_BTN)



