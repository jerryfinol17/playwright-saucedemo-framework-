from playwright.async_api import Page
from pages.base_page import BasePage
from pages.locators import CART
from typing import List


class CartPage(BasePage):

	def __init__(self, page: Page):
		super().__init__(page)

	# ====================== Checks ======================
	async def is_on_cart_page(self) -> bool:
		try:
			await self.assert_current_url_contains('cart.html')
			return True
		except AssertionError:
			return False

	# ====================== Getters ======================
	async def get_title_text(self) -> str:
		return (await self.get_text(CART['TITLE'])).strip()

	async def get_cart_badge_count(self) -> int:
		if not await self.is_visible(CART['SHOPPING_CART_BADGE']):
			return 0

		count_text = (await self.get_text(CART['SHOPPING_CART_BADGE'])).strip()
		return int(count_text) if count_text.isdigit() else 0

	async def get_cart_item_names(self) -> List[str]:
		names: List[str] = []
		items = await  self.page.locator(CART['CART_ITEM']).all()

		for item in items:
			name = (await item.locator(CART['PRODUCT_NAME']).inner_text()).strip()
			names.append(name)

		return names

	async def get_cart_item_prices(self) -> List[float]:
		elements = await self.page.locator(CART['PRODUCT_PRICE']).all()
		prices: List[float] = []

		for el in elements:
			price_text = (await el.inner_text()).replace("$", "").strip()
			prices.append(float(price_text))

		return prices

	async def get_item_quantity(self, item_name: str) -> int:
		items = await  self.page.locator(CART['CART_ITEM']).all()

		for item in items:
			name = (await item.locator(CART['PRODUCT_NAME']).inner_text()).strip()
			if name == item_name:
				quantity_text = (await item.locator(CART['CART_QUANTITY']).inner_text()).strip()
				return int(quantity_text) if quantity_text.isdigit() else 0
		return 0

	async def is_cart_empty(self) -> bool:
		return await self.get_cart_badge_count() == 0

	# ====================== Actions ======================
	async def remove_item_from_cart(self, item_name: str) -> None:
		items = await  self.page.locator(CART['CART_ITEM']).all()
		for item in items:
			name = (await item.locator(CART['PRODUCT_NAME']).inner_text()).strip()
			if name == item_name:
				remove_button = item.locator(CART['REMOVE_BTN'])
				await self.click_element(remove_button)
				return
		raise ValueError(f"Producto '{item_name}' no encontrado para remover")

	async def proceed_to_checkout(self) -> None:
		await self.click_element(CART['CHECKOUT_BTN'])

	async def continue_shopping(self) -> None:
		await self.click_element(CART['CONTINUE_SHOPPING_BTN'])

	async def reset_app(self) -> None:
		await self.click_element(CART['BURGER_MENU_BUTTON'])
		await self.click_element(CART['ALL_ITEMS_LINK'])



