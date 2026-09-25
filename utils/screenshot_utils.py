import os
import datetime

from config import config

captured_screenshots = []


def _timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def capture(driver, step_name):
    os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in step_name)
    filename = f"{safe_name}_{_timestamp()}.png"
    filepath = os.path.join(config.SCREENSHOTS_DIR, filename)

    try:
        driver.save_screenshot(filepath)
        captured_screenshots.append((step_name, filepath))
    except Exception as e:
        print(f"Screenshot capture failed for '{step_name}': {e}")
        return None

    return filepath


def reset():
    captured_screenshots.clear()
