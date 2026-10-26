import pytest
import allure
import logging
from allure import severity, severity_level
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium_tests.pages.base_page import BasePage
from selenium_tests.pages.login_page import LoginPage
from selenium_tests.pages.shop_page import ShopPage

# Настройка логгера для быстрой отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VALID_CREDENTIALS = {"username": "standard_user", "password": "secret_sauce"}


@allure.feature("Корзина и оформление заказа")
@allure.severity(severity_level.CRITICAL)
class TestCart:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        login_page = LoginPage(driver)
        base_page = BasePage(driver)

        logger.info("Выполняем вход в систему")
        login_page.enter_username(VALID_CREDENTIALS["username"])
        login_page.enter_password(VALID_CREDENTIALS["password"])
        login_page.click_login()

        # Закрываем возможные алерт-окна (если есть)
        try:
            base_page.close_password_alert_window(driver)
        except Exception:
            logger.warning("Окно-алерт не найдено или не удалось закрыть — продолжаем тест")

        self.shop_page = ShopPage(driver)
        logger.info("Страница магазина инициализирована")

    @allure.title("Успешное оформление покупки и очистка корзины")
    @allure.description(
        "Тест проверяет полный сценарий покупки: добавление товара в корзину, "
        "переход к оформлению, заполнение формы, подтверждение заказа. "
        "В конце проверяется сообщение об успехе и отсутствие товаров в корзине."
    )
    @allure.story("Оформление заказа и проверка результата")
    def test_successful_purchase(self, driver):
        wait = WebDriverWait(driver, 15)

        @allure.step("Добавить первый товар в корзину")
        def add_first_item():
            self.shop_page.add_item_to_cart(index=0)

        @allure.step("Открыть корзину и перейти к оформлению заказа")
        def open_cart_and_checkout():
            self.shop_page.open_cart()
            self.shop_page.open_checkout()

        @allure.step("Заполнить форму оформления заказа и завершить покупку")
        def complete_checkout():
            self.shop_page.fill_checkout_form("Anna", "Ivanova", "123456")
            self.shop_page.click_continue()
            self.shop_page.click_finish()

        add_first_item()
        open_cart_and_checkout()
        complete_checkout()

        # Ждём появления сообщения об успехе
        assert self.shop_page.is_success_message_present(), "Сообщение об успехе не появилось"

        expected_msg = (
            "Your order has been dispatched, and will arrive just as fast "
            "as the pony can get there!"
        )
        assert expected_msg in self.shop_page.get_success_message_text(), "Текст сообщения не совпадает"

        # В успешном заказе корзина должна быть пустой
        wait.until(lambda d: self.shop_page.get_cart_count() == 0)
        assert self.shop_page.get_cart_count() == 0, "Корзина не пуста после успешного заказа"

    @allure.title("Очистка корзины через кнопки удаления и возврат на страницу магазина")
    @allure.description(
        "Тест добавляет два товара в корзину, затем последовательно удаляет их "
        "с помощью кнопок «Remove» на странице каталога. В конце проверяется, "
        "что корзина пуста, а пользователь находится на странице магазина."
    )
    @allure.story("Очистка корзины и навигация")
    @allure.severity(severity_level.NORMAL)
    def test_clear_cart_and_return_to_shop(self, driver):
        wait = WebDriverWait(driver, 15)

        @allure.step("Добавить два товара в корзину")
        def add_two_items():
            self.shop_page.add_item_to_cart(index=0)
            self.shop_page.add_item_to_cart(index=1)

        @allure.step("Проверить, что в корзине два товара")
        def verify_cart_count():
            # Убеждаемся, что счётчик обновился
            wait.until(lambda d: self.shop_page.get_cart_count() == 2)
            assert self.shop_page.get_cart_count() == 2, "В корзине не два товара"

        @allure.step("Удалить все товары из корзины по одному")
        def remove_all_items():
            #initial_count = self.shop_page.get_cart_count()
            initial_count = self.shop_page.get_cart_badge_count()
            logger.info(f"Начинаем удаление: в корзине {initial_count} товаров")

            while self.shop_page.get_cart_count() > 0:
                # Ищем хотя бы одну кликабельную кнопку удаления
                # Это надёжнее, чем ждать весь список сразу
                remove_button = wait.until(
                    EC.element_to_be_clickable(self.shop_page.REMOVE_FROM_CART_BUTTON),
                    message="Не найдена кликабельная кнопка 'Remove' для удаления товара"
                )

                count_before = self.shop_page.get_cart_count()
                logger.info(f"Текущий счётчик перед кликом: {count_before}")

                # Делаем скриншот перед кликом для отладки, если что-то пойдёт не так
                driver.save_screenshot(f"before_remove_click_{count_before}.png")

                # Клик по кнопке
                remove_button.click()

                # Ждём, что количество товаров уменьшилось
                wait.until(
                    lambda d: self.shop_page.get_cart_count() < count_before,
                    message=f"Счётчик корзины не уменьшился: был {count_before}, остался {self.shop_page.get_cart_count()}"
                )

                logger.info(f"Товар удалён. Новый счётчик: {self.shop_page.get_cart_count()}")

        @allure.step("Убедиться, что корзина пуста и пользователь на странице магазина")
        def verify_empty_cart_and_page():
            wait.until(lambda d: self.shop_page.get_cart_count() == 0)
            assert "Swag Labs" in driver.title, f"Неверный заголовок страницы: {driver.title}"
            logger.info("Корзина пуста, тест пройден")

        add_two_items()
        verify_cart_count()
        remove_all_items()
        verify_empty_cart_and_page()
