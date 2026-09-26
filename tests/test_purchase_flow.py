import pytest

from config import config
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from utils.data_reader import get_test_data
from utils import screenshot_utils, report_utils


def log_and_capture(driver, step_name, message=""):
    screenshot_utils.capture(driver, step_name)
    report_utils.log_step(step_name, status="PASS", message=message)


TEST_DATA_ROWS = get_test_data()


@pytest.mark.parametrize("row", TEST_DATA_ROWS, ids=lambda r: r.get("TestCaseID", "TC"))
def test_ecommerce_purchase_flow(driver, row):
    email = row["Email"]
    password = row["Password"]
    product_name = row["ProductName"]
    updated_quantity = str(row.get("UpdatedQuantity") or config.DEFAULT_QUANTITY_UPDATE)

    login_page = LoginPage(driver)
    search_page = SearchPage(driver)
    cart_page = CartPage(driver)

    log_and_capture(driver, "browser_launched", f"Navigating to {config.BASE_URL}")

    # open login page and handle any popups
    login_page.open_login_page()
    login_page.handle_alert_if_present()
    log_and_capture(driver, "login_page_opened", "Opened login page")

    login_page.login(email, password)
    login_page.handle_alert_if_present()

    login_success = login_page.is_login_successful()
    log_and_capture(driver, "after_login", f"Login {'succeeded' if login_success else 'failed'} for {email}")

    if not login_success:
        error_msg = login_page.get_login_error() or "Login verification failed"
        report_utils.log_step("login", status="FAIL", message=error_msg)
        pytest.fail(f"Login failed for '{email}': {error_msg}")

    # search and open the product
    search_page.search_product(product_name)
    log_and_capture(driver, "product_searched", f"Searched for: {product_name}")

    search_page.open_first_result()
    product_title = search_page.get_product_title()
    log_and_capture(driver, "product_page_opened", f"Opened product: {product_title}")

    assert product_name.lower() in product_title.lower(), \
        f"Expected product '{product_name}' but got '{product_title}'"

    # add to cart
    search_page.add_to_cart()
    search_page.handle_alert_if_present()
    added = search_page.wait_for_add_to_cart_confirmation()
    log_and_capture(driver, "added_to_cart", f"Add to cart confirmation: {added}")
    assert added, f"Product '{product_name}' was not added to cart"

    # go to cart and update quantity
    cart_page.go_to_cart()
    cart_page.handle_alert_if_present()
    log_and_capture(driver, "cart_page_opened", "Navigated to cart page")

    cart_page.update_quantity(updated_quantity)
    cart_page.handle_alert_if_present()
    log_and_capture(driver, "quantity_updated", f"Quantity updated to {updated_quantity}")

    # verify cart contents
    row_count = cart_page.get_cart_row_count()
    product_names_in_cart = cart_page.get_product_names_in_cart()
    actual_quantity = cart_page.get_quantity_value()
    cart_total = cart_page.get_cart_total()

    log_and_capture(
        driver,
        "cart_verified",
        f"Rows: {row_count}, Products: {product_names_in_cart}, Qty: {actual_quantity}, Total: {cart_total}",
    )

    assert row_count >= 1, "Cart is empty"
    assert any(product_name.lower() in name.lower() for name in product_names_in_cart), \
        f"'{product_name}' not in cart items: {product_names_in_cart}"
    assert actual_quantity == updated_quantity, \
        f"Expected quantity '{updated_quantity}' but got '{actual_quantity}'"
    assert cart_total is not None, "Cart total could not be read"

    report_utils.log_step(
        "test_ecommerce_purchase_flow",
        status="PASS",
        message=f"Purchase flow completed for '{product_name}' (qty={updated_quantity})",
    )
