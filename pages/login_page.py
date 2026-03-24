from playwright.async_api import Page
from pages.base_page import BasePage
from pages.locators import LOGIN


class LoginPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ====================== Main Action ======================
    async def login(self, username: str, password: str) -> None:
        await self.fill_input(LOGIN["USERNAME_INPUT"], username)
        await self.fill_input(LOGIN["PASSWORD_INPUT"], password)
        await self.click_element(LOGIN["LOGIN_BUTTON"], force=True)

    # ====================== Error Handling ======================
    async def get_error_message_or_empty(self) -> str:
        if await self.is_visible(LOGIN["ERROR"]):
            return (await self.get_text(LOGIN["ERROR"])).strip()
        return ""

    async def is_error_visible(self) -> bool:
        return await self.is_visible(LOGIN["ERROR"])

    # ====================== Login Status ======================
    async def is_login_ok(self) -> bool:
        try:
            await self.assert_current_url_contains('inventory.html')
            return True
        except AssertionError:
            return False

    async def is_on_base_page(self) -> bool:
        return await self.is_visible(LOGIN["SWAG_LABS_LOGO"])

    async def is_inventory_title_visible(self) -> bool:
        return await self.is_visible(LOGIN["INVENTORY_TITLE"])

    # ====================== Utility Methods ======================
    async def clear_login_fields(self) -> None:
        await self.page.locator(LOGIN["USERNAME_INPUT"]).clear()
        await self.page.locator(LOGIN["PASSWORD_INPUT"]).clear()

    # ====================== Logout ======================
    async def logout(self) -> None:
        await self.click_element(LOGIN["BURGER_MENU_BUTTON"])
        await self.click_element(LOGIN["LOGOUT_BUTTON"])