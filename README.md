# E-Commerce Selenium Automation — Capstone Assignment 1

End-to-end automation for the OpenCart demo site (`https://tutorialsninja.com/demo/`) using Selenium + Python. Covers login, product search, cart operations and verification.

## What it covers

- Login and session handling
- Product search and add to cart
- Cart quantity update and verification
- Screenshots at each step
- Test data from Excel or JSON
- HTML report generated after the run

## Project structure

```
EcommerceAutomation/
├── config/
│   └── config.py
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── search_page.py
│   └── cart_page.py
├── utils/
│   ├── driver_factory.py
│   ├── data_reader.py
│   ├── screenshot_utils.py
│   └── report_utils.py
├── testdata/
│   ├── test_data.xlsx
│   └── test_data.json
├── tests/
│   ├── conftest.py
│   └── test_purchase_flow.py
├── reports/
├── pytest.ini
├── requirements.txt
└── run_tests.py
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate       # mac/linux: source venv/bin/activate
pip install -r requirements.txt
```

Chrome needs to be installed. ChromeDriver is handled automatically by webdriver-manager.

## ⚠️ Register a demo account first

The demo site has no pre-existing accounts. Register one at `https://tutorialsninja.com/demo/index.php?route=account/register` and add the credentials to `testdata/test_data.xlsx` (Email/Password columns) or `test_data.json`.

## Running

```bash
pytest -v tests/test_purchase_flow.py

# or
python run_tests.py
```

You can change browser/headless/data source via env vars:
- `AUT_BROWSER` — chrome (default), firefox, edge
- `AUT_HEADLESS` — true (default) or false
- `AUT_DATA_SOURCE` — excel (default) or json

## Output

Screenshots go to `reports/screenshots/` and a HTML report is generated at `reports/html_report/execution_report.html` after each run. Open it in any browser.

## Notes

- POM is used so locators are kept separate from test logic
- Explicit waits used throughout, avoids flaky sleeps where possible
- alert handling is called after steps that might trigger a popup — its a no-op if nothing shows up
