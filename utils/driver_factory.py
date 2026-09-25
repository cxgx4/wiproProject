from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from config import config


def get_driver(browser=None, headless=None):
    browser = (browser or config.BROWSER).lower()
    headless = config.HEADLESS if headless is None else headless

    # only chrome for now, TODO: add firefox support if needed
    if browser != "chrome":
        raise ValueError(f"Unsupported browser: {browser}. Only chrome is supported currently.")

    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(config.IMPLICIT_WAIT)
    if not headless:
        driver.maximize_window()

    return driver
