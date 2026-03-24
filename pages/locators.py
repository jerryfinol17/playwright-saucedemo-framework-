# ==================== LOGIN PAGE ====================
LOGIN = {
    "USERNAME_INPUT": '[data-test="username"]',
    "PASSWORD_INPUT": '[data-test="password"]',
    "LOGIN_BUTTON": '[data-test="login-button"]',
    "ERROR": '[data-test="error"]',
    "INVENTORY_TITLE": '.title',
    "SWAG_LABS_LOGO": '.login_logo',
    "BURGER_MENU_BUTTON": '#react-burger-menu-btn',
    "LOGOUT_BUTTON": '[data-test="logout-sidebar-link"]',
}
# ==================== INVENTORY PAGE ====================
INVENTORY = {
    "PRIMARY_HEADER": '[data-test="primary-header"]',
    "SHOPPING_CART_LINK": '[data-test="shopping-cart-link"]',
    "SHOPPING_CART_BADGE": '.shopping_cart_badge',
    "BURGER_MENU_BUTTON": '#react-burger-menu-btn',
    "CROSS_BURGER_BUTTON": '#react-burger-cross-btn',
    "ABOUT_LINK": '[data-test="about-sidebar-link"]',
    "RESET_APP_LINK": '[data-test="reset-sidebar-link"]',
    "TITLE": '[data-test="title"]',
    "SORT_DROPDOWN": '.product_sort_container',
    "PRODUCT_ITEM": '.inventory_item',
    "PRODUCT_NAME": '.inventory_item_name',
    "PRODUCT_PRICE": '.inventory_item_price',
    "PRODUCT_DESCRIPTION": '[data-test="inventory-item-desc"]',
}

# ========CART PAGE====================================
CART = {
	"TITLE": '[data-test=title]',
	"CONTINUE_SHOPPING_BTN": '[data-test=continue-shopping]',
	"CHECKOUT_BTN": '[data-test=checkout]',
	"CART_ITEM": '[data-test="inventory-item"]',
	"BURGER_MENU_BUTTON": '#react-burger-menu-btn',
	"ALL_ITEMS_LINK": '[data-test=inventory-sidebar-link]',
	"SHOPPING_CART_BADGE": '.shopping_cart_badge',
	"PRODUCT_NAME": '.inventory_item_name',
	"PRODUCT_PRICE": '.inventory_item_price',
	"CART_QUANTITY": '[data-test="item-quantity"]',
	"REMOVE_BTN": '[data-test^="remove-"]',
}

#=======CHECKOUT PAGE ===========================
CHECKOUT = {
    # STEP ONE
    "FIRST_NAME": '[data-test="firstName"]',
    "LAST_NAME": '[data-test="lastName"]',
    "ZIP_CODE": '[data-test="postalCode"]',
    "CANCEL_BTN": '[data-test="cancel"]',
    "CONTINUE_BTN": '[data-test="continue"]',
    "ERROR_MSG": '[data-test="error"]',

    # STEP TWO (Overview)
    "CART_ITEM": '[data-test="inventory-item"]',
    "PRODUCT_NAME": '.inventory_item_name',
    "PRODUCT_PRICE": '.inventory_item_price',
    "CART_QUANTITY": '[data-test="item-quantity"]',
    "PAYMENT_INFO_LABEL": '[data-test="payment-info-label"]',
    "PAYMENT_INFO_VALUE": '[data-test="payment-info-value"]',
    "SHIPPING_INFO_LABEL": '[data-test="shipping-info-label"]',
    "SHIPPING_INFO_VALUE": '[data-test="shipping-info-value"]',
    "TOTAL_INFO_LABEL": '[data-test="total-info-label"]',
    "SUBTOTAL_LABEL": ".summary_subtotal_label",
    "TAX_LABEL": ".summary_tax_label",
    "TOTAL_LABEL": ".summary_total_label",
    "CANCEL_BUTTON": '[data-test="cancel"]',
    "FINISH_BUTTON": '[data-test="finish"]',

    # STEP THREE (Complete)
    "COMPLETE_HEADER": '[data-test="complete-header"]',
    "COMPLETE_TEXT": '[data-test="complete-text"]',
    "BACK_HOME_BTN": '[data-test="back-to-products"]',
    "TITLE": '[data-test="title"]',
}