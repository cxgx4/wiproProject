from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

from config import config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator_or_element):
        if isinstance(locator_or_element, tuple):
            el = self.find_clickable(locator_or_element)
        else:
            el = locator_or_element
        el.click()

    def type(self, locator, text, clear_first=True):
        el = self.find(locator)
        if clear_first:
            el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text.strip()

    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, fragment, timeout=None):
        timeout = timeout or config.EXPLICIT_WAIT
        WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))

    def handle_alert_if_present(self, accept=True, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept() if accept else alert.dismiss()
            return text
        except (TimeoutException, NoAlertPresentException):
            return None
