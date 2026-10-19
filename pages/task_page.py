"""Page Objects for the task creation page and the task list page.

TODO: this file is incomplete. Fill in the methods marked TODO.
Use the LoginPage class in login_page.py as your pattern.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NewTaskPage:
    TITLE_INPUT = (By.ID, "title")
    PRIORITY_INPUT = (By.ID, "priority")
    DUE_DATE_INPUT = (By.ID, "due_date")
    HOURS_INPUT = (By.ID, "hours")
    CREATE_BUTTON = (By.ID, "create-button")
    SUCCESS_BANNER = (By.ID, "success-banner")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + "/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.TITLE_INPUT)
        )

    def create_task(self, title, priority, due_date, hours):
        self.driver.find_element(*self.TITLE_INPUT).send_keys(title)
        self.driver.find_element(*self.PRIORITY_INPUT).send_keys(priority)
        self.driver.find_element(*self.DUE_DATE_INPUT).send_keys(due_date)
        self.driver.find_element(*self.HOURS_INPUT).send_keys(hours)
        self.driver.find_element(*self.CREATE_BUTTON).click()

    def wait_for_success(self):
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.SUCCESS_BANNER)
        )


class TaskListPage:
    TASK_TABLE = (By.ID, "task-table")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    @staticmethod
    def complete_button(task_id):
        return (By.CSS_SELECTOR, f'button[data-task-id="{task_id}"]')

    @staticmethod
    def status_cell(task_id):
        return (By.ID, f"status-{task_id}")

    def open(self):
        self.driver.get(self.base_url + "/tasks")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.TASK_TABLE)
        )

    def mark_complete(self, task_id):
        button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.complete_button(task_id))
        )
        button.click()

    def wait_until_completed(self, task_id):
        return WebDriverWait(self.driver, 15).until(
            EC.text_to_be_present_in_element(self.status_cell(task_id), "Completed")
        )
