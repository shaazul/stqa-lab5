"""Page Object for the login page.

A Page Object is one class per page. It holds the locators (where things
are on the page) and the actions (what you can do on the page). Tests call
these methods instead of calling Selenium directly. If the page changes,
only this file changes, not every test that uses the page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.ID, "login-error")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url + "/login")
        # 30 seconds: Render's free tier can take a while to wake up
        # if the app has been idle.
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def wait_for_error(self):
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )
