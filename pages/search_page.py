from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    PRODUCT_RESULT_LINKS = (By.CSS_SELECTOR, ".product-thumb h4 a")
    PRODUCT_TITLE = (By.CSS_SELECTOR, "#content h1")
    ADD_TO_CART_BUTTON = (By.ID, "button-cart")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "div.alert-success")

    def search_product(self, product_name: str):
        self.type(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)

    def open_first_result(self):
        results = self.find_all(self.PRODUCT_RESULT_LINKS)
        if not results:
            raise AssertionError("No search results found for the given product.")
        self.click(results[0])

    def get_product_title(self):
        return self.get_text(self.PRODUCT_TITLE)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def wait_for_add_to_cart_confirmation(self, timeout=10):
        return self.is_visible(self.SUCCESS_ALERT, timeout=timeout)
