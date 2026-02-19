from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
	USERNAME_INPUT = '[data-test="username"]'
	PASSWORD_INPUT = '[data-test="password"]'
	LOGIN_BUTTON = '[data-test="login-button"]'
	ERROR = '[data-test="error"]'
	INVENTORY_TITLE = '.title'
	SWAG_LABS_LOGO = '.login_logo'

	def __init__(self, page : Page) -> None:
		super().__init__(page)

	def login(self, username: str, password: str) -> None:
		self.fill_input(self.USERNAME_INPUT, username)
		self.fill_input(self.PASSWORD_INPUT, password)
		self.click_element(self.LOGIN_BUTTON, force= True)

	def get_error_message_or_empty(self) -> str:
		if self.is_visible(self.ERROR):
			return self.get_text(self.ERROR).strip()
		return ""

	def is_error_visible(self) -> bool:
		return self.is_visible(self.ERROR)

	def is_login_ok(self) -> bool:
		return "inventory.html" in self.page.url

	def clear_login_fields(self) -> None:
		self.page.locator(self.USERNAME_INPUT).clear()
		self.page.locator(self.PASSWORD_INPUT).clear()

	def is_on_login_page(self) -> bool:
		return self.is_visible(self.SWAG_LABS_LOGO)





