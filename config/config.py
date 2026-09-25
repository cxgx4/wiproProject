import os

BASE_URL = "https://tutorialsninja.com/demo/"

BROWSER = os.getenv("AUT_BROWSER", "chrome")
HEADLESS = os.getenv("AUT_HEADLESS", "true").lower() == "true"
IMPLICIT_WAIT = 5
EXPLICIT_WAIT = 15

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTDATA_DIR = os.path.join(ROOT_DIR, "testdata")
REPORTS_DIR = os.path.join(ROOT_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
HTML_REPORT_DIR = os.path.join(REPORTS_DIR, "html_report")

EXCEL_TESTDATA_FILE = os.path.join(TESTDATA_DIR, "test_data.xlsx")
JSON_TESTDATA_FILE = os.path.join(TESTDATA_DIR, "test_data.json")
TESTDATA_SOURCE = os.getenv("AUT_DATA_SOURCE", "excel")

DEFAULT_QUANTITY_UPDATE = "3"
