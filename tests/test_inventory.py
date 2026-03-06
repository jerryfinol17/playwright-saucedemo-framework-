import pytest
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.config import CREDENTIALS
from pages.login_page import LoginPage


def test_add_one_product(logged_in_page) -> None:
    inventory = logged_in_page
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.get_cart_badge_count()
    assert inventory.get_cart_badge_count() == 1
    assert inventory.is_remove_button_visible("Sauce Labs Backpack") is True

def test_add_multiple_product(logged_in_page) -> None:
    inventory = logged_in_page
    items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Onesie"]
    for item in items_to_add:
        inventory.add_item_is_visible(item)
        inventory.add_item_to_cart(item)
        inventory.is_remove_button_visible(item)
    assert inventory.get_cart_badge_count() == 3


def test_add_two_product(logged_in_page) -> None:
    inventory = logged_in_page
    items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    for item in items_to_add:
        inventory.add_item_to_cart(item)
    assert inventory.get_cart_badge_count() == 2
    for item in items_to_add:
        assert inventory.is_remove_button_visible(item)
    inventory.remove_item_from_cart("Sauce Labs Bike Light")
    assert inventory.get_cart_badge_count() == 1
    assert inventory.add_item_is_visible("Sauce Labs Bike Light") is True

def test_remove_all_product(logged_in_page) -> None:
    inventory = logged_in_page
    items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt (Red)"]
    for item in items_to_add:
        inventory.add_item_to_cart(item)
    assert inventory.get_cart_badge_count() == 6
    for item in items_to_add:
        inventory.remove_item_from_cart(item)
    assert inventory.get_cart_badge_count() == 0

def test_consistency_across_pages(logged_in_page) -> None:
    inventory = logged_in_page
    item_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    for item in item_to_add:
        inventory.add_item_to_cart(item)
    assert inventory.get_cart_badge_count() == 3
    inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
    cart = CartPage(inventory.page)
    cart.get_cart_item_names()
    assert cart.get_cart_item_names() == item_to_add
    cart.continue_shopping()
    for item in item_to_add:
        inventory.remove_item_from_cart(item)
    assert inventory.get_cart_badge_count() == 0
    inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
    cart.get_cart_item_names()
    assert cart.get_cart_item_names() != item_to_add
    print(cart.get_cart_item_names())


def test_description(logged_in_page) -> None:
    inventory = logged_in_page
    inventory.get_product_description("Sauce Labs Backpack")
    assert "Sly Pack" in inventory.get_product_description("Sauce Labs Backpack")


@pytest.mark.parametrize("name, brief_description", [("Sauce Labs Backpack"," Sly Pack")
    ,("Sauce Labs Bike Light", "AAA battery included"),
    ("Sauce Labs Bolt T-Shirt", "American Apparel"),
    ("Sauce Labs Fleece Jacket", "quarter-zip fleece jacket"),
    ("Sauce Labs Onesie", " two-needle hemmed"),
    ("Test.allTheThings() T-Shirt (Red)","Super-soft and comfy")])
def test_description_in_all_products(logged_in_page, name, brief_description) -> None:
    inventory = logged_in_page
    assert brief_description in inventory.get_product_description(name)

def test_az_sorting(logged_in_page) -> None:
    inventory = logged_in_page
    inventory.select_sort_option("az")
    name = inventory.get_name_list()
    expected = sorted(name)
    assert name == expected, f'A to Z fail: {name} != {expected}'

def test_za_sorting(logged_in_page):
    inventory = logged_in_page
    inventory.select_sort_option("za")
    names = inventory.get_name_list()
    expected = sorted(names, reverse=True)
    assert names == expected, f'Z to A Fallo: {names} != {expected}'

def test_lohi_sorting(logged_in_page):
    inventory = logged_in_page
    inventory.select_sort_option("lohi")
    prices = inventory.get_price_list()
    expected = sorted(prices)
    assert prices == expected, f'Lohi to A Fallo: {prices} != {expected}'

def test_hilo_sorting(logged_in_page):
    inventory = logged_in_page
    inventory.select_sort_option("hilo")
    prices = inventory.get_price_list()
    expected = sorted(prices, reverse=True)
    assert prices == expected, f'Hilo to A Fallo: {prices} != {expected}'

def test_sorting_preserves_item_prices(logged_in_page):
    inventory = logged_in_page
    initial_data = inventory.get_inventory_items_with_prices()

    for options_value in ["az", "za", "lohi", "hilo"]:
        inventory.select_sort_option(options_value)
        current_data = inventory.get_inventory_items_with_prices()

        assert set(current_data.keys()) == set(initial_data.keys()),\
        f'Sorting {options_value} lost items'

        for name, initial_price in initial_data.items():
            assert current_data[name] == initial_price, \
            f'Sorting {options_value} lost the price of {name}'


def test_sorting_preserves_cart_states_and_add_remove_btn(logged_in_page):
    inventory = logged_in_page
    assert inventory.get_cart_badge_count() == 0
    inventory.add_item_to_cart("Sauce Labs Bike Light")
    assert inventory.get_cart_badge_count() == 1
    names = inventory.get_name_list()
    inventory.select_sort_option("za")
    assert inventory.is_remove_button_visible("Sauce Labs Bike Light") == True
    expected = sorted(names)
    assert names == expected, f'Z to A Fallo: {names} != {expected}'
    assert inventory.get_cart_badge_count() == 1
    assert inventory.is_remove_button_visible("Sauce Labs Bike Light") == True

@pytest.mark.xfail(reason="The UI does not restart the status on remove btn")
def test_reset_btn(logged_in_page):
    inventory = logged_in_page
    assert inventory.is_on_inventory_page() == True
    inventory.add_item_to_cart("Sauce Labs Bike Light")
    assert inventory.get_cart_badge_count() == 1
    assert inventory.is_remove_button_visible("Sauce Labs Bike Light") == True
    inventory.click_element(InventoryPage.BURGER_MENU_BUTTON)
    inventory.click_element(InventoryPage.RESET_APP_LINK)
    assert inventory.get_cart_badge_count() == 0
    assert inventory.is_on_inventory_page() == True
    try:
        assert inventory.is_remove_button_visible("Sauce Labs Bike Light") == False
        print("Unexpected error, remove btn should not appear")
    except AssertionError:
        print("Expected error, remove_btn should not appear")
        assert inventory.is_remove_button_visible("Sauce Labs Bike Light") == True
    """Actually this test have a bug on it, it supposes to change the status on the remove button\\
    and the badge count of the cart, restarting the status at the initial status, but it does not happen\\
    just change the status on the cart badge but the status on the remove buttons never change"""

def test_reset_app_full_happy_path(logged_in_page):
    inventory = logged_in_page
    assert inventory.get_cart_badge_count() == 0
    items_to_add= ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    for item in items_to_add:
        inventory.add_item_to_cart(item)
    assert inventory.get_cart_badge_count() == 3
    inventory.click_element(InventoryPage.BURGER_MENU_BUTTON)
    inventory.click_element(InventoryPage.RESET_APP_LINK)
    inventory.click_element(InventoryPage.CROSS_BURGER_BUTTON)
    assert inventory.get_cart_badge_count() == 0, f'Reset does not change status on cart badge'
    inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
    cart = CartPage(inventory.page)
    assert cart.is_on_cart_page() == True
    assert cart.is_cart_empty() == True
    assert cart.get_cart_item_names() == []
    cart.continue_shopping()
    assert inventory.is_on_inventory_page() == True
    for item in items_to_add:
        assert inventory.is_remove_button_visible(item)  == False,f'Reset does not change the status on  remove btn for {item}'
    """When you go to cart page after click reset app, to check if the cart is already empty\\
    then when you go to the inventory page the UI update the status on the remove/add button."""


def assert_sorting_preserves_items(inventory, initial_data, sort_option):
    inventory.select_sort_option(sort_option)
    current_data = inventory.get_inventory_items_with_prices()
    assert set(current_data.keys()) == set(initial_data.keys()), \
        f"Sorting '{sort_option}' lost items"
    for name, initial_price in initial_data.items():
        assert current_data[name] == initial_price, \
            f"Sorting '{sort_option}' changed/lost price of '{name}'"
        #HELPER

def test_sorting_with_multiple_items_and_removals(logged_in_page):
    inventory = logged_in_page
    initial_data = inventory.get_inventory_items_with_prices()
    items_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket"
    ]
    sort_options = ["az", "za", "lohi", "hilo"]
    for opt in sort_options:
        assert_sorting_preserves_items(inventory, initial_data, opt)

    for item in items_to_add:
        inventory.add_item_to_cart(item)
        assert inventory.is_remove_button_visible(item) is True
    assert inventory.get_cart_badge_count() == 4

    for opt in sort_options:
        assert_sorting_preserves_items(inventory, initial_data, opt)

    for item in items_to_add:
        assert inventory.is_remove_button_visible(item) is True, \
            f"Remove button disappeared for '{item}' after sorting"
    for item in items_to_add:
        inventory.remove_item_from_cart(item)
        assert inventory.add_item_is_visible(item) is True
    for opt in sort_options:
        assert_sorting_preserves_items(inventory, initial_data, opt)

def test_about_btn_work(logged_in_page):
    inventory = logged_in_page
    assert inventory.about_btn_work() is True

@pytest.mark.xfail(reason="Expected bugs in problem_user: limited add, no remove from inventory")
def test_add_remove_with_problem_user(page):
    login = LoginPage(page)
    creds = CREDENTIALS['problem']
    login.login(creds['username'], creds['password'])
    inventory = InventoryPage(page)
    assert inventory.is_on_inventory_page() == True
    all_items = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)"
    ]
    addable_items = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Onesie"]
    non_addable_items = [item for item in all_items if item not in addable_items]
    for item in all_items:
        try:
            inventory.add_item_to_cart(item)
            assert inventory.is_remove_button_visible(item) is True, f"Failed to switch to Remove for '{item}'"
            print(f"Successfully added '{item}' to cart (expected for addable ones)")
        except AssertionError:
            print(f"Failed to add '{item}' to cart (expected for non-addable ones)")
            assert item in non_addable_items, f"Unexpected fail adding '{item}'"

    assert inventory.get_cart_badge_count() == 3
    for item in addable_items:
        try:
            inventory.remove_item_from_cart(item)
            assert inventory.add_item_is_visible(item) is True, f"Failed to switch to Remove for '{item}'"
            print(f"Unexpectedly removed '{item}' should fail!")
        except AssertionError:
            print(f"Failed to remove '{item}' (expected bug: remove doesn't work from inventory)")
            assert inventory.is_remove_button_visible(item) is True, f"Button should still be Remove for '{item}' after failed remove"
    assert inventory.get_cart_badge_count() == 3
    inventory.click_element(InventoryPage.SHOPPING_CART_LINK)
    cart = CartPage(page)
    assert cart.get_cart_item_names() == addable_items


@pytest.mark.xfail(reason="Expected bugs in visual_user: sorting always breaks the data for prices")
def test_sorting_in_visual_user(page):
    login = LoginPage(page)
    creds = CREDENTIALS['visual']
    login.login(creds['username'], creds['password'])
    inventory = InventoryPage(page)
    assert inventory.is_on_inventory_page() is True
    initial_data = inventory.get_inventory_items_with_prices()
    initial_prices_list = inventory.get_price_list()
    sort_options = ["az", "za", "lohi", "hilo"]
    for opt in sort_options:
        print(f"\n=== Testing sort: {opt.upper()} ===")
        inventory.select_sort_option(opt)
        current_data = inventory.get_inventory_items_with_prices()
        current_prices_list = inventory.get_price_list()
        initial_keys = set(initial_data.keys())
        current_keys = set(current_data.keys())
        if initial_keys != current_keys:
            missing = initial_keys - current_keys
            extra = current_keys - initial_keys
            if missing:
                print(f"  → Items LOST after sort: {missing}")
            if extra:
                print(f"  → Extra items appeared: {extra}")
        changes_found = False
        print("  Cambios detectados en precios:")
        for name in initial_keys:
            initial_price = initial_data.get(name, "N/A")
            current_price = current_data.get(name, "N/A")
            if initial_price != current_price:
                changes_found = True
                print(f"    - {name}: {initial_price} → {current_price}  (has changed!)")

        if not changes_found:
            print("    (Ningún precio cambió en este sort – inesperado si es bug)")
        if opt in ["lohi", "hilo"]:
            expected_sorted_prices = sorted(initial_prices_list) if opt == "lohi" else sorted(initial_prices_list,
                                                                                              reverse=True)
            if current_prices_list == expected_sorted_prices:
                print("  → Precios se ordenaron correctamente (NO esperado en visual_user)")
            else:
                print("  → Precios NO se ordenaron correctamente (expected bug)")
                print(f"     Lista actual:   {current_prices_list}")
                print(f"     Lista esperada: {expected_sorted_prices}")
    print("\nTest finalizado. En visual_user se esperan cambios/rupturas en precios con cada sort.")