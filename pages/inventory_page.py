from playwright.async_api import Page
from pages.base_page import BasePage
from pages.locators import INVENTORY
from typing import List, Dict


class InventoryPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # ====================== Checks ======================
    async def is_on_inventory_page(self) -> bool:
        try:
            await self.assert_current_url_contains('inventory.html')
            return True
        except AssertionError:
            return False

    async def primary_header_is_visible(self) -> bool:
        return await self.is_visible(INVENTORY["PRIMARY_HEADER"])

    # ====================== Getters ======================
    async def get_title_text(self) -> str:
        return (await self.get_text(INVENTORY["TITLE"])).strip()

    async def get_cart_badge_count(self) -> int:
        if not await self.is_visible(INVENTORY["SHOPPING_CART_BADGE"]):
            return 0
        count_text = (await self.get_text(INVENTORY["SHOPPING_CART_BADGE"])).strip()
        return int(count_text) if count_text.isdigit() else 0

    async def get_product_name(self, product_name: str) -> str:
        items = await self.page.locator(INVENTORY["PRODUCT_ITEM"]).all()
        for item in items:
            name = (await item.locator(INVENTORY["PRODUCT_NAME"]).inner_text()).strip()
            if name == product_name:
                return name
        return ""

    async def get_product_description(self, product_name: str) -> str:
        items = await self.page.locator(INVENTORY["PRODUCT_ITEM"]).all()
        for item in items:
            name = (await item.locator(INVENTORY["PRODUCT_NAME"]).inner_text()).strip()
            if name == product_name:
                return (await item.locator(INVENTORY["PRODUCT_DESCRIPTION"]).inner_text()).strip()
        return ""

    async def get_product_price(self, product_name: str) -> str:
        items = await self.page.locator(INVENTORY["PRODUCT_ITEM"]).all()
        for item in items:
            name = (await item.locator(INVENTORY["PRODUCT_NAME"]).inner_text()).strip()
            if name == product_name:
                return (await item.locator(INVENTORY["PRODUCT_PRICE"]).inner_text()).strip()
        return ""

    async def get_inventory_items_with_prices(self) -> Dict[str, float]:
        items: Dict[str, float] = {}
        item_locators = await self.page.locator(INVENTORY["PRODUCT_ITEM"]).all()

        for item_locator in item_locators:
            name = (await item_locator.locator(INVENTORY["PRODUCT_NAME"]).inner_text()).strip()
            price_str = (await item_locator.locator(INVENTORY["PRODUCT_PRICE"]).inner_text()).strip()
            price = float(price_str.replace("$", "").strip())
            items[name] = price
        return items

    async def get_name_list(self) -> List[str]:
        elements = await self.page.locator(INVENTORY["PRODUCT_NAME"]).all()
        return [(await el.inner_text()).strip() for el in elements]

    async def get_price_list(self) -> List[float]:
        elements = await self.page.locator(INVENTORY["PRODUCT_PRICE"]).all()
        return [float((await el.inner_text()).replace("$", "").strip()) for el in elements]

    # ====================== Actions ======================
    async def add_item_to_cart(self, item_name: str) -> None:
        items = await self.page.locator(INVENTORY["PRODUCT_ITEM"]).all()
        for item in items:
            name = (await item.locator(INVENTORY["PRODUCT_NAME"]).inner_text()).strip()
            if name == item_name:
                add_button = item.locator('[data-test^="add-to-cart-"]')
                await self.click_element(add_button)
                return
        raise ValueError(f"Producto '{item_name}' no encontrado en el inventario")

    async def remove_item_from_cart(self, item_name: str) -> None:
        items = await self.page.locator(INVENTORY["PRODUCT_ITEM"]).all()
        for item in items:
            name = (await item.locator(INVENTORY["PRODUCT_NAME"]).inner_text()).strip()
            if name == item_name:
                remove_button = item.locator('[data-test^="remove-"]')
                await self.click_element(remove_button)
                return
        raise ValueError(f"Producto '{item_name}' no encontrado para remover")

    async def is_remove_button_visible(self, item_name: str) -> bool:
        items = await self.page.locator(INVENTORY["PRODUCT_ITEM"]).all()
        for item in items:
            name = (await item.locator(INVENTORY["PRODUCT_NAME"]).inner_text()).strip()
            if name == item_name:
                remove_button = item.locator('[data-test^="remove-"]')
                return await self.is_visible(remove_button)
        return False

    async def add_item_is_visible(self, item_name: str) -> bool:
        items = await self.page.locator(INVENTORY["PRODUCT_ITEM"]).all()
        for item in items:
            name = (await item.locator(INVENTORY["PRODUCT_NAME"]).inner_text()).strip()
            if name == item_name:
                add_button = item.locator('[data-test^="add-to-cart-"]')
                return await self.is_visible(add_button)
        return False

    async def select_sort_option(self, value: str) -> None:
        await self.page.locator(INVENTORY["SORT_DROPDOWN"]).select_option(value)

    async def go_to_cart(self)-> None:
        await self.click_element(INVENTORY["SHOPPING_CART_LINK"])
    # ====================== Burger Menu Actions ======================
    async def about_btn_work(self) -> bool:
        await self.click_element(INVENTORY["BURGER_MENU_BUTTON"])
        await self.click_element(INVENTORY["ABOUT_LINK"])
        return 'saucelabs.com' in self.page.url
    async def reset_app(self) -> None:
        await self.click_element(INVENTORY["BURGER_MENU_BUTTON"])
        await self.click_element(INVENTORY["RESET_APP_LINK"])
        await self.click_element(INVENTORY["CROSS_BURGER_BUTTON"])

