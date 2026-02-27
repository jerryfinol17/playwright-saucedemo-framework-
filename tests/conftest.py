import pytest
from playwright.sync_api import sync_playwright, Browser, Page, expect
from pages.config import BASE_URL, CREDENTIALS
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

BROWSERS_AND_DEVICES = [
    {"name": "chromium", "browser_type": "chromium", "channel": None, "device_name": None},
    {"name": "msedge",   "browser_type": "chromium", "channel": "msedge", "device_name": None},
    {"name": "webkit",   "browser_type": "webkit",   "channel": None,     "device_name": None},
    {"name": "iphone13", "browser_type": "chromium", "channel": None,     "device_name": "iPhone 13"},
    {"name": "pixel5",   "browser_type": "chromium", "channel": None,     "device_name": "Pixel 5"},
]

@pytest.fixture(scope="function", params=BROWSERS_AND_DEVICES, ids=lambda x: x["name"])
def page(request) -> Page:
    config = request.param
    browser_type = config["browser_type"]
    channel = config.get("channel")
    device_name = config["device_name"]
    pw = sync_playwright().start()
    try:
        if browser_type == "chromium":
            browser: Browser = pw.chromium.launch(
                headless=True,
                slow_mo=300,
                channel=channel
            )
        elif browser_type == "webkit":
            browser: Browser = pw.webkit.launch(headless=True, slow_mo=300)
        else:
            raise ValueError(f"Browser no soportado: {browser_type}")
        context_kwargs = {}
        if device_name:
            device = pw.devices[device_name]
            context_kwargs.update(device)

        context = browser.new_context(**context_kwargs)
        page: Page = context.new_page()

        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded")

        yield page

    finally:
        if 'page' in locals():
            page.close()
        if 'context' in locals():
            context.close()
        if 'browser' in locals():
            browser.close()
        pw.stop()


@pytest.fixture(scope="function")
def logged_in_page(page):

    creds = CREDENTIALS['standard']
    username = creds["username"]
    password = creds["password"]

    login_page = LoginPage(page)
    login_page.is_on_base_page()
    login_page.login(username, password)

    inventory_page = InventoryPage(page)
    assert inventory_page.get_title_text() == "Products"

    yield inventory_page