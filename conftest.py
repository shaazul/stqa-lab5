"""Shared pytest setup. Takes a screenshot after every test step and
attaches it to the pytest-html report, whether the step passed or failed.
"""
import os
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = os.environ.get("PYTODO_URL", "http://127.0.0.1:5000")
RESET_TOKEN = os.environ.get("PYTODO_RESET_TOKEN", "lab5reset")


@pytest.fixture(scope="session", autouse=True)
def reset_app_state_before_run():
    """Clears all tasks on the server before the test suite starts, so a
    newly created task is always id=1. Without this, running the suite
    more than once makes task IDs climb (2, 3, 4...), since the task list
    lives on the server, not in the browser. Silently does nothing if the
    reset endpoint is unreachable, so this never blocks the run.
    """
    try:
        requests.post(f"{BASE_URL}/admin/reset", params={"token": RESET_TOKEN}, timeout=10)
    except requests.RequestException:
        pass


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    driver = item.funcargs.get("driver")
    if driver is None:
        return
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    file_name = f"{screenshots_dir}/{item.name}.png"
    driver.save_screenshot(file_name)
    if hasattr(report, "extra"):
        pass
    extra = getattr(report, "extra", [])
    try:
        from pytest_html import extras
        extra.append(extras.image(file_name))
        report.extra = extra
    except ImportError:
        pass
