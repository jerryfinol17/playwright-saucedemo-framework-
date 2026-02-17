from playwright.sync_api import Page, Locator, expect, TimeoutError as PlaywrightTimeoutError
from typing import Optional

class BasePage(Page):
	def __init__(self,page: Page):
		super().__init__(page)
		self.page = page
		self.timeout = 15000

	def fill_input(self, locator: str | Locator, value: str, clear_first: bool = True)  -> None:
		loc= self.get_locator(locator)
		if clear_first:
			loc.clear()
			loc.fill(value)

	def click_element(self, locator: str | Locator, value: str, force: bool = False) -> None:
		self.get_locator(locator).click(force=force)

	def click_and_wait_navigation(self, locator: str | Locator, value: str, timeout:Optional[int] = None) -> None:
		with self.expect_navigation(timeout=timeout or self.timeout):
			self.click_element(locator)


	def wait_for_visible(self, locator: str | Locator, timeout:Optional[int] = None) -> Locator:
		loc = self.get_locator(locator)
		loc.wait_for(state = "visible", timeout = timeout or self.timeout)
		return loc

	def wait_for_hidden(self, locator: str | Locator, timeout:Optional[int] = None) -> None:
		self.get_locator(locator).wait_for(state = "hidden", timeout = timeout or self.timeout)

	def get_text(self, locator: str | Locator) -> str:
		return self.get_locator(locator).inner_text()
	def get_current_url(self) -> str:
		return self.page.url
	def assert_current_url_contains(self, expected_substring: str, message: Optional[str] = None) -> None:
		current = self.get_current_url()
		assert current == expected_substring, f"{current} != {expected_substring}"

	def assert_text_equals(self, locator: str | Locator, expected_text: str) -> None:
		expect(self.get_text(locator)).to_have_text(expected_text)

	def get_locator(self, locator: str| Locator) -> Locator:
		if isinstance(locator, str):
			return self.page.locator(locator)
		return locator