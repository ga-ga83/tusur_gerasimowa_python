import pytest
import allure
from allure import severity, severity_level
from selenium.webdriver.common.by import By

from selenium_tests.pages.login_page import LoginPage

# Данные для тестов
VALID_CREDENTIALS = {"username": "standard_user", "password": "secret_sauce"}
INVALID_USERNAME = "wrong_user"
INVALID_PASSWORD = "wrong_password"
EXPECTED_ERROR_MSG = "Epic sadface: Username and password do not match any user in this service"
EXPECTED_ERROR_MSG_EMPTY = "Epic sadface: Username is required"


@allure.feature("Авторизация пользователя")
@allure.severity(severity_level.BLOCKER)
class TestLogin:

    @allure.title("Успешная авторизация с корректными учётными данными")
    @allure.description(
        "Проверяется успешный вход пользователя со стандартными учётными данными. "
        "После входа проверяется URL страницы инвентаря и наличие логотипа приложения."
    )
    @allure.story("Успешный вход в систему")
    def test_successful_login(self, driver):
        @allure.step("Ввести логин и пароль, нажать кнопку входа")
        def perform_login():
            login_page = LoginPage(driver)
            login_page.enter_username(VALID_CREDENTIALS["username"])
            login_page.enter_password(VALID_CREDENTIALS["password"])
            login_page.click_login()

        perform_login()

        assert "https://www.saucedemo.com/inventory.html" in driver.current_url
        assert LoginPage(driver).is_element_present((By.CLASS_NAME, "app_logo"))

    @allure.title("Неуспешная авторизация при неверных учётных данных")
    @allure.description(
        "Проверяется поведение системы при попытке входа с некорректными логином и паролем. "
        "Ожидается сообщение об ошибке, указывающее на несоответствие учётных данных."
    )
    @allure.story("Обработка неверных учётных данных")
    @allure.severity(severity_level.CRITICAL)
    def test_unsuccessful_login_wrong_credentials(self, driver):
        @allure.step("Ввести неверные логин и пароль, нажать кнопку входа")
        def attempt_login_with_wrong_creds():
            login_page = LoginPage(driver)
            login_page.enter_username(INVALID_USERNAME)
            login_page.enter_password(INVALID_PASSWORD)
            login_page.click_login()

        attempt_login_with_wrong_creds()

        error_mgs = LoginPage(driver).get_error_message()
        assert error_mgs == EXPECTED_ERROR_MSG, (
            f"Expected error '{EXPECTED_ERROR_MSG}', got '{error_mgs}'"
        )

    @allure.title("Проверка обработки пустых полей при входе")
    @allure.description(
        "Проверяется реакция системы на попытку входа без ввода логина и пароля. "
        "Ожидается сообщение о том, что поле имени пользователя обязательно для заполнения."
    )
    @allure.story("Валидация обязательных полей")
    @allure.severity(severity_level.CRITICAL)
    def test_unsuccessful_login_empty_fields(self, driver):
        @allure.step("Нажать кнопку входа без заполнения полей")
        def attempt_login_without_credentials():
            login_page = LoginPage(driver)
            login_page.click_login()

        attempt_login_without_credentials()

        error_mgs = LoginPage(driver).get_error_message()
        assert error_mgs == EXPECTED_ERROR_MSG_EMPTY, (
            f"Expected error '{EXPECTED_ERROR_MSG_EMPTY}', got '{error_mgs}'"
        )
