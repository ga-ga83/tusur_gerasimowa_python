"""Базовый класс с общими методами"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.find_element(locator).click()

    def get_text(self, locator):
        return self.find_element(locator).text

    def get_attribute(self, locator, attr):
        return self.find_element(locator).get_attribute(attr)

    def is_element_present(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

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

    def find_elements_no_wait(self, locator, short_timeout=1):
        """
        Возвращает список элементов. Если не найдены за short_timeout секунд — пустой список.
        Не выбрасывает TimeoutException.
        """
        # Создаём временный wait с нужным коротким таймаутом
        temp_wait = type(self.wait)(self.driver, short_timeout)
        try:
            return temp_wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

