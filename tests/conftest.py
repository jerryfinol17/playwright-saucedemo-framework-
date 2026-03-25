import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, Browser, Page
from pages.config import BASE_URL, CREDENTIALS
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

BROWSERS_AND_DEVICES = [
    {"name": "chromium", "browser_type": "chromium", "channel": None,     "device_name": None},
    {"name": "msedge",   "browser_type": "chromium", "channel": "msedge", "device_name": None},
    {"name": "webkit",   "browser_type": "webkit",   "channel": None,     "device_name": None},
    {"name": "iphone13", "browser_type": "chromium", "channel": None,     "device_name": "iPhone 13"},
    {"name": "pixel5",   "browser_type": "chromium", "channel": None,     "device_name": "Pixel 5"},
]


@pytest_asyncio.fixture(scope="function", params=BROWSERS_AND_DEVICES, ids=lambda x: x["name"])
async def page(request) -> Page:
    config = request.param
    browser_type = config["browser_type"]
    channel = config.get("channel")
    device_name = config["device_name"]
    record_video = request.node.get_closest_marker("record_video") is not None

    async with async_playwright() as pw:
        # Lanzar browser
        if browser_type == "chromium":
            browser: Browser = await pw.chromium.launch(
                headless=True,
                slow_mo=300,
                channel=channel
            )
        elif browser_type == "webkit":
            browser: Browser = await pw.webkit.launch(headless=True, slow_mo=300)
        else:
            raise ValueError(f"Browser no soportado: {browser_type}")

        # Armar kwargs del contexto
        context_kwargs = {}
        if device_name:
            device = pw.devices[device_name]
            context_kwargs.update(device)

        if record_video:
            context_kwargs["record_video_dir"] = "videos/"

        context = await browser.new_context(**context_kwargs)
        page: Page = await context.new_page()

        await page.goto(BASE_URL)
        await page.wait_for_load_state("domcontentloaded")

        yield page

        try:
            await page.close()
        except Exception:
            pass
        try:
            await context.close()
        except Exception:
            pass
        try:
            await browser.close()
        except Exception:
            pass


@pytest_asyncio.fixture(scope="function")
async def logged_in_page(page):
    creds = CREDENTIALS['standard']
    username = creds["username"]
    password = creds["password"]

    login_page = LoginPage(page)
    await login_page.is_on_base_page()
    await login_page.login(username, password)

    inventory_page = InventoryPage(page)
    assert await inventory_page.get_title_text() == "Products"

    yield inventory_page