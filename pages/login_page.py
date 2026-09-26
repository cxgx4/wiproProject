from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config import config


class LoginPage(BasePage):
    MY_ACCOUNT_MENU = (By.CSS_SELECTOR, "a[title='My Account']")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    LOGIN_ERROR_ALERT = (By.CSS_SELECTOR, "div.alert-danger")

    def open_login_page(self):
        self.open(config.BASE_URL)
        try:
            self.click(self.MY_ACCOUNT_MENU)
            self.click(self.LOGIN_LINK)
        except Exception:
            self.open(config.BASE_URL + "index.php?route=account/login")

    def login(self, email, password):
        self.type(self.EMAIL_INPUT, email)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_login_successful(self):
        try:
            self.wait_for_url_contains("account/account", timeout=5)
            return True
        except Exception:
            return self.is_visible(
                (By.XPATH, "//h2[contains(text(), 'My Account')] | //a[contains(@href, 'route=account/logout')] | //aside//a[contains(text(), 'Logout')]"),
                timeout=3,
            )

    def get_login_error(self):
        if self.is_visible(self.LOGIN_ERROR_ALERT, timeout=3):
            return self.get_text(self.LOGIN_ERROR_ALERT)
        return None
