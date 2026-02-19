import pytest
from playwright.sync_api import sync_playwright, Browser, Page
from pages.config import BASE_URL, CREDENTIALS

BROWSERS_AND_DEVICES = [
    {"browser_type": "chromium", "device_name": None, "name": "chromium"},
    {"browser_type": "firefox",  "device_name": None, "name": "firefox"},
    {"browser_type": "webkit",   "device_name": None, "name": "webkit"},
    {"browser_type": "chromium", "device_name": "iPhone 13", "name": "iphone13"},
    {"browser_type": "chromium", "device_name": "Pixel 5",   "name": "pixel5"},
]

@pytest.fixture(scope="function", params=BROWSERS_AND_DEVICES, ids=lambda x: x["name"])
def page(request) -> Page:
    config = request.param
    browser_type = config["browser_type"]
    device_name = config["device_name"]

    p = sync_playwright().start()
    try:
        if browser_type == "chromium":
            browser: Browser = p.chromium.launch(headless=False, slow_mo=300)
        elif browser_type == "firefox":
            browser = p.firefox.launch(headless=False, slow_mo=300)
        elif browser_type == "webkit":
            browser = p.webkit.launch(headless=False, slow_mo=300)
        else:
            raise ValueError(f"Browser desconocido: {browser_type}")

        context_kwargs = {}
        if device_name:
            device = p.devices[device_name]
            context_kwargs.update(device)

        context = browser.new_context(**context_kwargs)

        page: Page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded")

        yield page
    finally:
        context.close()
        browser.close()
        p.stop()

@pytest.fixture(scope="function", params= list(CREDENTIALS.values()), ids= list(CREDENTIALS.keys()))
def test_user(request):
    return request.param