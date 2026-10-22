import pytest
from selenium_tests.pages.base_page import BasePage
from selenium_tests.pages.login_page import LoginPage
from selenium_tests.pages.shop_page import ShopPage
import time

VALID_CREDENTIALS = {"username": "standard_user", "password": "secret_sauce"}

class TestCart:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        login_page = LoginPage(driver)
        base_page = BasePage(driver)
        login_page.enter_username(VALID_CREDENTIALS["username"])
        login_page.enter_password(VALID_CREDENTIALS["password"])
        login_page.click_login()
        base_page.close_password_alert_window(driver)

        self.shop_page = ShopPage(driver)  # Затем инициализируем страницу

    def test_successful_purchase(self, driver):
        self.shop_page.add_item_to_cart(index=0)
        self.shop_page.open_cart()
        self.shop_page.open_checkout()
        self.shop_page.fill_checkout_form("Anna", "Ivanova", "123456")
        self.shop_page.click_continue()
        self.shop_page.click_finish()
        assert self.shop_page.is_success_message_present()
        assert "Your order has been dispatched, and will arrive just as fast as the pony can get there!" in self.shop_page.get_success_message_text()
        assert self.shop_page.get_cart_count() == 0

    def test_clear_cart_and_return_to_shop(self, driver):
        self.shop_page.add_item_to_cart(index=0)
        self.shop_page.add_item_to_cart(index=1)
        assert self.shop_page.get_cart_count() == 2

        self.shop_page.open_cart()

        while True:
            remove_buttons = self.shop_page.find_elements_no_wait(
                self.shop_page.REMOVE_FROM_CART_BUTTON
            )
            if not remove_buttons:
                break
            remove_buttons[0].click()
            # Ждём, пока кнопка исчезнет
            #self.shop_page.wait_until_element_absent(
                #self.shop_page.REMOVE_FROM_CART_BUTTON,
                #timeout=10
            #)

        assert self.shop_page.get_cart_count() == 0
        assert "Swag Labs" in driver.title