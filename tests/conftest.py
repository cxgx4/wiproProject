import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import get_driver
from utils import screenshot_utils, report_utils


@pytest.fixture(scope="function")
def driver():
    drv = get_driver()
    yield drv
    drv.quit()


@pytest.fixture(scope="session", autouse=True)
def _reset_logs():
    screenshot_utils.reset()
    report_utils.reset()
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            screenshot_utils.capture(drv, f"FAILURE_{item.name}")
        report_utils.log_step(item.name, status="FAIL", message=str(call.excinfo.value) if call.excinfo else "")


def pytest_sessionfinish(session, exitstatus):
    report_path = report_utils.generate_html_report(screenshot_utils.captured_screenshots)
    print(f"\nExecution report generated at: {report_path}")
