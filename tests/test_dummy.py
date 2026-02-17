from playwright.sync_api import expect


def test_saucedemo_title(page):
    expect(page).to_have_title("Swag Labs")