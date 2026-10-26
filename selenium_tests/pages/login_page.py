from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.saucedemo.com"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")


    def open(self):
        self.driver.get(self.URL)

    def enter_username(self, username):
        self.find_element(self.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.find_element(self.PASSWORD_INPUT).send_keys(password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    #def close_password_alert(self):
    #    wait = WebDriverWait(self.driver, 10)
    #    wait.until(EC.alert_is_present())
    #    alert = self.driver.switch_to.alert
    #    alert.accept()

    def close_password_alert_window(self, driver):
        selectors = [
            "div[role='alert']",
            "div.notification",
            "div.toast"
        ]

        for selector in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for el in elements:
                if "Смените пароль" in el.text:
                    action = ActionChains(driver)
                    action.send_keys(Keys.ESCAPE).perform()
                    return  # закрыли первый подходящий алерт и выходим

    def get_error_message(self):
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
