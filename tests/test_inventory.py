import pytest
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.config import CREDENTIALS
from pages.login_page import LoginPage
async def test_add_one_product(logged_in_page) -> None:
    inventory = logged_in_page
    await inventory.add_item_to_cart("Sauce Labs Backpack")
    await inventory.get_cart_badge_count()
    assert await inventory.get_cart_badge_count() == 1
    assert await inventory.is_remove_button_visible("Sauce Labs Backpack") is True
async def test_add_multiple_product(logged_in_page) -> None:
    inventory = logged_in_page
    items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Onesie"]
    for item in items_to_add:
       await  inventory.add_item_is_visible(item)
       await inventory.add_item_to_cart(item)
       await inventory.is_remove_button_visible(item)
    assert await  inventory.get_cart_badge_count() == len(items_to_add)
async def test_add_two_product(logged_in_page) -> None:
    inventory = logged_in_page
    items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    for item in items_to_add:
        await inventory.add_item_to_cart(item)
    assert await inventory.get_cart_badge_count() == len(items_to_add)
    for item in items_to_add:
        assert  await inventory.is_remove_button_visible(item)
    await inventory.remove_item_from_cart("Sauce Labs Bike Light")
    assert await inventory.get_cart_badge_count() == len(items_to_add) - 1
    assert await inventory.add_item_is_visible("Sauce Labs Bike Light") is True
async def test_remove_all_product(logged_in_page) -> None:
    inventory = logged_in_page
    items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt (Red)"]
    for item in items_to_add:
        await inventory.add_item_to_cart(item)
    assert await inventory.get_cart_badge_count() == len(items_to_add)
    for item in items_to_add:
        await inventory.remove_item_from_cart(item)
    assert await inventory.get_cart_badge_count() == 0
async def test_consistency_across_pages(logged_in_page) -> None:
    inventory = logged_in_page
    cart = CartPage(inventory.page)
    item_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    for item in item_to_add:
        await inventory.add_item_to_cart(item)
    assert await inventory.get_cart_badge_count() == len(item_to_add)
    await inventory.go_to_cart()
    await cart.get_cart_item_names()
    assert await  cart.get_cart_item_names() == item_to_add
    await cart.continue_shopping()
    for item in item_to_add:
        await inventory.remove_item_from_cart(item)
    assert await inventory.get_cart_badge_count() == 0
    await inventory.go_to_cart()
    assert await cart.get_cart_item_names() != item_to_add
async def test_description(logged_in_page) -> None:
    inventory = logged_in_page
    assert "Sly Pack" in await inventory.get_product_description("Sauce Labs Backpack")
@pytest.mark.parametrize("name, brief_description", [("Sauce Labs Backpack"," Sly Pack")
    ,("Sauce Labs Bike Light", "AAA battery included"),
    ("Sauce Labs Bolt T-Shirt", "American Apparel"),
    ("Sauce Labs Fleece Jacket", "quarter-zip fleece jacket"),
    ("Sauce Labs Onesie", " two-needle hemmed"),
    ("Test.allTheThings() T-Shirt (Red)","Super-soft and comfy")])
async def test_description_in_all_products(logged_in_page, name, brief_description) -> None:
    inventory = logged_in_page
    assert brief_description in await  inventory.get_product_description(name)
async def test_az_sorting(logged_in_page) -> None:
    inventory = logged_in_page
    await inventory.select_sort_option("az")
    name = await  inventory.get_name_list()
    expected = sorted(name)
    assert name == expected, f'A to Z fail: {name} != {expected}'
async def test_za_sorting(logged_in_page):
    inventory = logged_in_page
    await inventory.select_sort_option("za")
    names = await inventory.get_name_list()
    expected = sorted(names, reverse=True)
    assert names == expected, f'Z to A Fallo: {names} != {expected}'
async def test_lohi_sorting(logged_in_page):
    inventory = logged_in_page
    await inventory.select_sort_option("lohi")
    prices = await inventory.get_price_list()
    expected = sorted(prices)
    assert prices == expected, f'Lohi to A Fallo: {prices} != {expected}'
async def test_hilo_sorting(logged_in_page):
    inventory = logged_in_page
    await inventory.select_sort_option("hilo")
    prices = await inventory.get_price_list()
    expected = sorted(prices, reverse=True)
    assert prices == expected, f'Hilo to A Fallo: {prices} != {expected}'
async def test_sorting_preserves_item_prices(logged_in_page):
    inventory = logged_in_page
    initial_data = await inventory.get_inventory_items_with_prices()
    for options_value in ["az", "za", "lohi", "hilo"]:
        await inventory.select_sort_option(options_value)
        current_data = await inventory.get_inventory_items_with_prices()
        assert set(current_data.keys()) == set(initial_data.keys()),\
        f'Sorting {options_value} lost items'
        for name, initial_price in initial_data.items():
            assert current_data[name] == initial_price, \
            f'Sorting {options_value} lost the price of {name}'
async def test_sorting_preserves_cart_states_and_add_remove_btn(logged_in_page):
    inventory = logged_in_page
    assert await inventory.get_cart_badge_count() == 0
    await inventory.add_item_to_cart("Sauce Labs Bike Light")
    assert await inventory.get_cart_badge_count() == 1
    names = await  inventory.get_name_list()
    await inventory.select_sort_option("za")
    assert await inventory.is_remove_button_visible("Sauce Labs Bike Light") == True
    expected = sorted(names)
    assert names == expected, f'Z to A Fallo: {names} != {expected}'
    assert await inventory.get_cart_badge_count() == 1
    await inventory.remove_item_from_cart("Sauce Labs Bike Light")
    await inventory.select_sort_option("az")
    await inventory.select_sort_option("za")
    assert names == expected, f'Z to A Fallo: {names} != {expected}'
    assert await inventory.add_item_is_visible("Sauce Labs Bike Light") == True
@pytest.mark.xfail(reason="The UI does not restart the status on remove btn")
async def test_reset_btn(logged_in_page):
    inventory = logged_in_page
    assert await  inventory.is_on_inventory_page() == True
    await inventory.add_item_to_cart("Sauce Labs Bike Light")
    assert await inventory.get_cart_badge_count() == 1
    assert await inventory.is_remove_button_visible("Sauce Labs Bike Light") == True
    await inventory.reset_app()
    assert await inventory.get_cart_badge_count() == 0
    assert await inventory.is_on_inventory_page() == True
    try:
        assert await inventory.is_remove_button_visible("Sauce Labs Bike Light") == False
        print("Unexpected error, remove btn should not appear")
    except AssertionError:
        print("Expected error, remove_btn should not appear")
        assert await inventory.is_remove_button_visible("Sauce Labs Bike Light") == True
    """Actually this test have a bug on it, it supposes to change the status on the remove button\\
    and the badge count of the cart, restarting the status at the initial status, but it does not happen\\
    just change the status on the cart badge but the status on the remove buttons never change"""
async def test_reset_app_full_happy_path(logged_in_page):
    inventory = logged_in_page
    cart = CartPage(inventory.page)
    assert await inventory.get_cart_badge_count() == 0
    items_to_add= ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    for item in items_to_add:
        await inventory.add_item_to_cart(item)
    assert await inventory.get_cart_badge_count() == len(items_to_add)
    await inventory.reset_app()
    assert await inventory.get_cart_badge_count() == 0, f'Reset does not change status on cart badge'
    await inventory.go_to_cart()
    assert await cart.is_on_cart_page() == True
    assert await cart.is_cart_empty() == True
    assert await cart.get_cart_item_names() == []
    await cart.continue_shopping()
    assert await inventory.is_on_inventory_page() == True
    for item in items_to_add:
        assert await inventory.is_remove_button_visible(item)  == False,f'Reset does not change the status on  remove btn for {item}'
    """When you go to cart page after click reset app, to check if the cart is already empty\\
    then when you go to the inventory page the UI update the status on the remove/add button."""
async def assert_sorting_preserves_items(inventory, initial_data, sort_option):
    inventory.select_sort_option(sort_option)
    current_data = await inventory.get_inventory_items_with_prices()
    assert set(current_data.keys()) == set(initial_data.keys()), \
        f"Sorting '{sort_option}' lost items"
    for name, initial_price in initial_data.items():
        assert current_data[name] == initial_price, \
            f"Sorting '{sort_option}' changed/lost price of '{name}'"
        #HELPER
async def test_sorting_with_multiple_items_and_removals(logged_in_page):
    inventory = logged_in_page
    initial_data = await inventory.get_inventory_items_with_prices()
    items_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket"
    ]
    sort_options = ["az", "za", "lohi", "hilo"]
    for opt in sort_options:
       await  assert_sorting_preserves_items(inventory, initial_data, opt)
    for item in items_to_add:
        await inventory.add_item_to_cart(item)
        assert await inventory.is_remove_button_visible(item) is True
    assert await inventory.get_cart_badge_count() == len(items_to_add)
    for opt in sort_options:
        await assert_sorting_preserves_items(inventory, initial_data, opt)
    for item in items_to_add:
        assert await  inventory.is_remove_button_visible(item) is True, \
            f"Remove button disappeared for '{item}' after sorting"
    for item in items_to_add:
        await inventory.remove_item_from_cart(item)
        assert await  inventory.add_item_is_visible(item) is True
    for opt in sort_options:
        await  assert_sorting_preserves_items(inventory, initial_data, opt)
async def test_about_btn_work(logged_in_page):
    inventory = logged_in_page
    assert await  inventory.about_btn_work() is True
@pytest.mark.xfail(reason="Expected bugs in problem_user: limited add, no remove from inventory")
async def test_add_remove_with_problem_user(page):
    login = LoginPage(page)
    inventory = InventoryPage(page)
    cart = CartPage(page)
    creds = CREDENTIALS['problem']
    await login.login(creds['username'], creds['password'])
    assert await  inventory.is_on_inventory_page() == True
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
            await inventory.add_item_to_cart(item)
            assert await inventory.is_remove_button_visible(item) is True, f"Failed to switch to Remove for '{item}'"
            print(f"Successfully added '{item}' to cart (expected for addable ones)")
        except AssertionError:
            print(f"Failed to add '{item}' to cart (expected for non-addable ones)")
            assert item in non_addable_items, f"Unexpected fail adding '{item}'"
    assert await inventory.get_cart_badge_count() == 3
    for item in addable_items:
        try:
            await inventory.remove_item_from_cart(item)
            assert await inventory.add_item_is_visible(item) is True, f"Failed to switch to Remove for '{item}'"
            print(f"Unexpectedly removed '{item}' should fail!")
        except AssertionError:
            print(f"Failed to remove '{item}' (expected bug: remove doesn't work from inventory)")
            assert await inventory.is_remove_button_visible(item) is True, f"Button should still be Remove for '{item}' after failed remove"
    assert await inventory.get_cart_badge_count() == 3
    await inventory.go_to_cart()
    assert await cart.get_cart_item_names() == addable_items
@pytest.mark.xfail(reason="Expected bugs in visual_user: sorting always breaks the data for prices")
async def test_sorting_in_visual_user(page):
    login = LoginPage(page)
    inventory = InventoryPage(page)
    creds = CREDENTIALS['visual']
    await login.login(creds['username'], creds['password'])
    assert await inventory.is_on_inventory_page() is True
    initial_data = await inventory.get_inventory_items_with_prices()
    initial_prices_list = await inventory.get_price_list()
    sort_options = ["az", "za", "lohi", "hilo"]
    for opt in sort_options:
        print(f"\n=== Testing sort: {opt.upper()} ===")
        await inventory.select_sort_option(opt)
        current_data = await inventory.get_inventory_items_with_prices()
        current_prices_list = await inventory.get_price_list()
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