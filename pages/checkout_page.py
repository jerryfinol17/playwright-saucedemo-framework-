from playwright.sync_api import Page
from pages.config import DATA
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    # STEP ONE
    FIRST_NAME = '[data-test="firstName"]'
    LAST_NAME = '[data-test="lastName"]'
    ZIP_CODE = '[data-test="postalCode"]'
    CANCEL_BTN = '[data-test="cancel"]'
    CONTINUE_BTN = '[data-test="continue"]'
    ERROR_MSG = '[data-test="error"]'
    #STEP TWO
    CART_ITEM = '[data-test="inventory-item"]'
    PRODUCT_NAME = '.inventory_item_name'
    PRODUCT_PRICE = '.inventory_item_price'
    CART_QUANTITY = '[data-test="item-quantity"]'
    PAYMENT_INFO_LABEL = '[data-test="payment-info-label"]'
    PAYMENT_INFO_VALUE = '[data-test="payment-info-value"]'
    SHIPPING_INFO_LABEL = '[data-test="shipping-info-label"]'
    SHIPPING_INFO_VALUE = '[data-test="shipping-info-value"]'
    TOTAL_INFO_LABEL = '[data-test="total-info-label"]'
    SUBTOTAL_LABEL = ".summary_subtotal_label"
    TAX_LABEL = ".summary_tax_label"
    TOTAL_LABEL = ".summary_total_label"
    CANCEL_BUTTON = '[data-test="cancel"]'
    FINISH_BUTTON = '[data-test="finish"]'
    # STEP THREE
    COMPLETE_HEADER = '[data-test="complete-header"]'
    COMPLETE_TEXT = '[data-test="complete-text"]'
    BACK_HOME_BTN = '[data-test="back-to-products"]'
    TITLE = '[data-test="title"]'

    def __init__(self, page: Page):
        super().__init__(page)


    #GENERAL E2E
    def get_title_text(self) -> str:
        return self.get_text(self.TITLE).strip()
    def is_on_checkout_page(self) -> bool:
        return 'checkout-step-one.html' in self.page.url

    def fill_personal_info(self, first: str, last: str, zip_code: str) -> None:
        self.wait_for_visible(self.FIRST_NAME)
        self.page.locator(self.FIRST_NAME).fill(first)
        self.page.locator(self.LAST_NAME).fill(last)
        self.page.locator(self.ZIP_CODE).fill(zip_code)

    def continue_to_overview(self):
        self.click_element(self.CONTINUE_BTN)

    def finish_purchase(self):
        self.click_element(self.FINISH_BUTTON)

    def get_subtotal_text(self) -> str:
        return self.get_text(self.SUBTOTAL_LABEL)

    def is_complete_page(self) -> bool:
        return "Thank you for your order!" in self.get_text(self.COMPLETE_HEADER)

    # ── STEP ONE ── ERROR AND NEGATIVES
    def get_error_message(self) -> str:
        if self.is_visible(self.ERROR_MSG):
            return self.get_text(self.ERROR_MSG).strip()
        return ""

    def continue_without_info(self):
        self.click_element(self.CONTINUE_BTN)

    def is_error_visible(self) -> bool:
        return self.is_visible(self.ERROR_MSG)

    # ── STEP TWO ── Overview
    def get_subtotal(self) -> float:
        text = self.get_text(self.SUBTOTAL_LABEL)
        return float(text.split("$")[-1].strip()) if "$" in text else 0.0

    def get_tax(self) -> float:
        text = self.get_text(self.TAX_LABEL)
        return float(text.split("$")[-1].strip()) if "$" in text else 0.0

    def get_total(self) -> float:
        text = self.get_text(self.TOTAL_LABEL)
        return float(text.split("$")[-1].strip()) if "$" in text else 0.0

    def get_overview_item_names(self) -> list[str]:
        items = self.page.locator(self.CART_ITEM).all()
        names = []
        for item in items:
            name_locator = item.locator(self.PRODUCT_NAME)
            if name_locator.is_visible():
                names.append(name_locator.inner_text().strip())
        return names

    def get_overview_item_count(self) -> int:
        return len(self.page.locator(self.CART_ITEM).all())

    # ── STEP THREE ── Complete
    def get_complete_text(self) -> str:
        return self.get_text(self.COMPLETE_TEXT).strip()

    def back_to_products(self):
        self.click_element(self.BACK_HOME_BTN)

    # ── Cancel  on different steps
    def cancel_from_step_one(self):
        self.click_element(self.CANCEL_BTN)

    def cancel_from_overview(self):
        self.click_element(self.CANCEL_BUTTON)
