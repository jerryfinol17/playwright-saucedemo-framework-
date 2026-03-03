import pytest
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


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





