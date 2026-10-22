import pytest
from selenium.webdriver.common.by import By
from selenium_tests.pages.login_page import LoginPage

#Данные для тестов
VALID_CREDENTIALS = {"username": "standard_user", "password": "secret_sauce"}
INVALID_USERNAME = "wrong_user"
INVALID_PASSWORD = "wrong_password"
EXPECTED_ERROR_MSG = "Epic sadface: Username and password do not match any user in this service"
EXPECTED_ERROR_MSG_EMPTY = "Epic sadface: Username is required"


class TestLogin:

    def test_successful_login(self, driver):
        """Успешная авторизация"""
        login_page = LoginPage(driver)

        login_page.enter_username(VALID_CREDENTIALS["username"])
        login_page.enter_password(VALID_CREDENTIALS["password"])
        login_page.click_login()

        assert "https://www.saucedemo.com/inventory.html" in driver.current_url
        assert login_page.is_element_present((By.CLASS_NAME, "app_logo"))

    def test_unsuccessful_login_wrong_credentials(self, driver):
        """Неуспешная авторизация"""
        login_page = LoginPage(driver)

        login_page.enter_username(INVALID_USERNAME)
        login_page.enter_password(INVALID_PASSWORD)
        login_page.click_login()

        error_mgs = login_page.get_error_message()
        assert error_mgs == EXPECTED_ERROR_MSG, f"Expected error '{EXPECTED_ERROR_MSG}', got '{error_mgs}'"

    def test_unsuccessful_login_empty_fields(self, driver):
        """Проверка на пустые поля"""
        login_page = LoginPage(driver)

        login_page.click_login()

        error_mgs = login_page.get_error_message()
        assert error_mgs == EXPECTED_ERROR_MSG_EMPTY, f"Expected error '{EXPECTED_ERROR_MSG_EMPTY}', got '{error_mgs}'"
