import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from config import config


class CartPage(BasePage):
    CART_ROWS = (
        By.XPATH,
        "//div[@id='content']//form//table//tbody/tr[.//input[contains(@name, 'quantity')]]"
    )
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name^='quantity']")
    UPDATE_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-original-title='Update'], button[title='Update']"
    )

    def go_to_cart(self):
        self.open(config.BASE_URL + "index.php?route=checkout/cart")

    def get_cart_row_count(self):
        try:
            return len(self.find_all(self.CART_ROWS))
        except Exception:
            return 0

    def get_product_names_in_cart(self):
        rows = self.find_all(self.CART_ROWS)
        names = []
        for row in rows:
            links = row.find_elements(By.CSS_SELECTOR, "td a")
            for link in links:
                txt = link.text.strip()
                if txt:
                    names.append(txt.split("\n")[0].strip())
                    break
        return names

    def update_quantity(self, new_quantity: str, row_index: int = 0):
        rows = self.find_all(self.CART_ROWS)
        if not rows:
            raise AssertionError("No quantity input fields found in the cart.")

        target_row = rows[row_index]
        qty_input = target_row.find_element(By.CSS_SELECTOR, "input[name^='quantity']")
        qty_input.clear()
        qty_input.send_keys(new_quantity)

        try:
            update_btn = target_row.find_element(*self.UPDATE_BUTTON)
            update_btn.click()
        except Exception:
            qty_input.send_keys(Keys.ENTER)

        time.sleep(2)

    def get_quantity_value(self, row_index: int = 0):
        rows = self.find_all(self.CART_ROWS)
        if rows and row_index < len(rows):
            qty_input = rows[row_index].find_element(By.CSS_SELECTOR, "input[name^='quantity']")
            return qty_input.get_attribute("value")
        return None

    def get_cart_total(self):
        # grab the total from the order summary at the bottom of the cart table
        loc = (By.XPATH, "//table[contains(@class, 'table')]//tr[td[contains(., 'Total:')]]/td[last()]")
        try:
            text = self.get_text(loc)
            if text and any(c.isdigit() for c in text):
                return text
        except Exception:
            pass
        return None