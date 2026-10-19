"""Lab 5: automate login, create a task, mark it complete, log out.

Fill in pages/task_page.py first (it has TODO markers), then write the
four test functions below.

Run with:
    pytest test_ui.py -v --html=report.html --self-contained-html

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"
"""
from pages.login_page import LoginPage
from pages.task_page import NewTaskPage, TaskListPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from uuid import uuid4

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"


def test_login_with_valid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)
    task_page = NewTaskPage(driver, base_url)
    task_page.open()
    assert driver.find_element(*task_page.TITLE_INPUT).is_displayed()


def test_login_with_invalid_credentials(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login("demo", "wrong-password")
    error = login_page.wait_for_error()
    assert "Invalid username or password" in error.text


def test_create_task(driver, base_url):
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    task_page = NewTaskPage(driver, base_url)
    task_page.open()
    task_page.create_task(
        title="Prepare slides",
        priority="2",
        due_date="2026-12-01",
        hours="3",
    )
    assert task_page.wait_for_success().is_displayed()


def test_mark_task_complete_and_logout(driver, base_url):
    task_title = f"Prepare slides {uuid4().hex}"
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    new_task_page = NewTaskPage(driver, base_url)
    new_task_page.open()
    new_task_page.create_task(
        title=task_title,
        priority="2",
        due_date="2026-12-01",
        hours="3",
    )
    new_task_page.wait_for_success()

    task_list_page = TaskListPage(driver, base_url)
    task_list_page.open()
    complete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            f'//*[@id="task-table"]//tr[td[normalize-space(.)="{task_title}"]]'
            '//button[@data-task-id]',
        ))
    )
    task_id = complete_button.get_attribute("data-task-id")
    task_list_page.mark_complete(task_id)
    assert task_list_page.wait_until_completed(task_id)

    driver.find_element(By.ID, "logout-link").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(LoginPage.USERNAME_INPUT)
    )
