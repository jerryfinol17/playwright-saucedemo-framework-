from playwright.async_api import Page
from pages.base_page import BasePage
from pages.locators import CHECKOUT
from typing import List, Dict


class CheckoutPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # ====================== General ======================
    async def get_title_text(self) -> str:
        return (await self.get_text(CHECKOUT["TITLE"])).strip()

    async def is_on_checkout_page(self) -> bool:
        try:
            await self.assert_current_url_contains('checkout-step-one.html')
            return True
        except AssertionError:
            return False

    # ====================== Step One ======================
    async def fill_personal_info(self, first: str, last: str, zip_code: str) -> None:
        await self.wait_for_visible(CHECKOUT["FIRST_NAME"])
        await self.page.locator(CHECKOUT["FIRST_NAME"]).fill(first)
        await self.page.locator(CHECKOUT["LAST_NAME"]).fill(last)
        await self.page.locator(CHECKOUT["ZIP_CODE"]).fill(zip_code)

    async def continue_to_overview(self) -> None:
        await self.click_element(CHECKOUT["CONTINUE_BTN"])

    async def get_error_message(self) -> str:
        if await self.is_visible(CHECKOUT["ERROR_MSG"]):
            return (await self.get_text(CHECKOUT["ERROR_MSG"])).strip()
        return ""

    async def is_error_visible(self) -> bool:
        return await self.is_visible(CHECKOUT["ERROR_MSG"])

    # ====================== Step Two (Overview) ======================
    async def get_subtotal_text(self) -> str:
        return await self.get_text(CHECKOUT["SUBTOTAL_LABEL"])

    async def get_subtotal(self) -> float:
        text = await self.get_text(CHECKOUT["SUBTOTAL_LABEL"])
        return float(text.split("$")[-1].strip()) if "$" in text else 0.0

    async def get_tax(self) -> float:
        text = await self.get_text(CHECKOUT["TAX_LABEL"])
        return float(text.split("$")[-1].strip()) if "$" in text else 0.0

    async def get_total(self) -> float:
        text = await self.get_text(CHECKOUT["TOTAL_LABEL"])
        return float(text.split("$")[-1].strip()) if "$" in text else 0.0

    async def get_overview_item_names(self) -> List[str]:
        names: List[str] = []
        items = await self.page.locator(CHECKOUT["CART_ITEM"]).all()

        for item in items:
            name_locator = item.locator(CHECKOUT["PRODUCT_NAME"])
            if await name_locator.is_visible():
                name = (await name_locator.inner_text()).strip()
                names.append(name)
        return names

    async def get_overview_items_with_prices(self) -> Dict[str, float]:
        items: Dict[str, float] = {}
        item_locators = await self.page.locator(CHECKOUT["CART_ITEM"]).all()

        for item_locator in item_locators:
            name = (await item_locator.locator(CHECKOUT["PRODUCT_NAME"]).inner_text()).strip()
            price_str = (await item_locator.locator(CHECKOUT["PRODUCT_PRICE"]).inner_text()).strip()
            price = float(price_str.replace("$", "").strip())
            items[name] = price
        return items

    async def get_overview_item_count(self) -> int:
        items = await self.page.locator(CHECKOUT["CART_ITEM"]).all()
        return len(items)

    # ====================== Step Three (Complete) ======================
    async def is_complete_page(self) -> bool:
        header_text = await self.get_text(CHECKOUT["COMPLETE_HEADER"])
        return "Thank you for your order!" in header_text

    async def get_complete_text(self) -> str:
        return (await self.get_text(CHECKOUT["COMPLETE_TEXT"])).strip()

    async def finish_purchase(self) -> None:
        await self.click_element(CHECKOUT["FINISH_BUTTON"])

    async def back_to_products(self) -> None:
        await self.click_element(CHECKOUT["BACK_HOME_BTN"])

    # ====================== Cancel actions ======================
    async def cancel_from_step_one(self) -> None:
        await self.click_element(CHECKOUT["CANCEL_BTN"])

    async def cancel_from_overview(self) -> None:
        await self.click_element(CHECKOUT["CANCEL_BUTTON"])