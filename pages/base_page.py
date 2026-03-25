from playwright.async_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from typing import Optional


class BasePage:
	def __init__(self, page: Page):
		self.page = page
		self.timeout = 15000

	# ====================== Helper privado ======================
	def get_locator(self, locator: str | Locator) -> Locator:
		if isinstance(locator, str):
			return self.page.locator(locator)
		return locator

	# ====================== Actions ======================
	async def fill_input(
			self,
			locator: str | Locator,
			value: str,
			clear_first: bool = True
	) -> None:
		loc = self.get_locator(locator)

		if clear_first:
			await loc.clear()

		await loc.fill(value)

	async def click_element(
			self,
			locator: str | Locator,
			**kwargs
	) -> None:

		loc = self.get_locator(locator)
		await loc.click(**kwargs)

	async def wait_for_visible(
			self,
			locator: str | Locator,
			timeout: Optional[int] = None
	) -> Locator:
		loc = self.get_locator(locator)
		await loc.wait_for(
			state="visible",
			timeout=timeout or self.timeout
		)
		return loc

	async def get_text(self, locator: str | Locator) -> str:
		loc = self.get_locator(locator)
		return await loc.inner_text()

	async def get_current_url(self) -> str:
		return self.page.url

	# ====================== Assertions ======================
	async def assert_current_url_contains(
			self,
			expected_substring: str,
			message: Optional[str] = None
	) -> None:
		current_url = await self.get_current_url()
		current = current_url.strip()

		assert expected_substring in current, (
			f"URL assertion failed.\n"
			f"Expected substring : '{expected_substring}'\n"
			f"Actual URL         : '{current}'\n"
			f"{f'Additional info   : {message}' if message else ''}"
		)

	async def is_visible(self, locator: str | Locator) -> bool:
		loc = self.get_locator(locator)
		return await loc.is_visible()