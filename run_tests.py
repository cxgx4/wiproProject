import sys
import pytest

from config import config

if __name__ == "__main__":
    exit_code = pytest.main(["-v", "tests/test_purchase_flow.py"])
    print(f"\nScreenshots saved to: {config.SCREENSHOTS_DIR}")
    print(f"HTML report saved to: {config.HTML_REPORT_DIR}")
    sys.exit(exit_code)
