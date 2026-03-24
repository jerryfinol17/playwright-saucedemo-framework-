from pages.cart_page import CartPage
async def test_e2e_cart(logged_in_page):
    inventory = logged_in_page
    cart = CartPage(inventory.page)
    items_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)"
    ]
    for item in items_to_add:
        await inventory.add_item_to_cart(item)
    assert await inventory.get_cart_badge_count() == len(items_to_add)
    await inventory.go_to_cart()
    assert await cart.is_on_cart_page() is True
    assert await cart.get_title_text() == "Your Cart"
    assert await cart.get_cart_badge_count() == len(items_to_add)
    names = await cart.get_cart_item_names()
    assert names == items_to_add
    prices = await inventory.get_price_list()
    assert await cart.get_cart_item_prices() == prices
    for item in items_to_add:
        assert await cart.get_item_quantity(item) == 1
    for item in items_to_add:
        await cart.remove_item_from_cart(item)
    assert await cart.is_cart_empty() is True
    await cart.reset_app()
    assert await inventory.is_on_inventory_page() is True
    assert await inventory.get_title_text() == "Products"
