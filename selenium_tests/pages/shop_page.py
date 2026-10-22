from selenium.webdriver.common.by import By
from .base_page import BasePage

class ShopPage(BasePage):
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    ADD_TO_CART_BUTTONS = (By.XPATH, "//button[contains(@class, 'btn_primary')]")
    REMOVE_FROM_CART_BUTTON = (By.XPATH, "//*[@class='btn btn_secondary btn_small cart_button']")
    REMOVE_FROM_CART_BUTTONS = (By.XPATH, "//*[@class='btn btn_secondary btn_small btn_inventory ']")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    ITEM_TITLE = (By.CSS_SELECTOR, ".inventory_item_name")
    LOGO_TITLE = (By.XPATH, "//*[@class='app_logo']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    ZIP_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")

    SUCCESS_MESSAGE = (By.CLASS_NAME, "complete-text")
    BACK_TO_PRODUCTS_LINK = (By.XPATH, "//*[@class='btn btn_secondary back btn_medium']")

    def add_item_to_cart(self, index=0):
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        buttons[index].click()

    def remove_item_from_cart(self, index=0):
        # Используем find_elements, чтобы получить список кнопок
        buttons = self.find_elements(self.REMOVE_FROM_CART_BUTTON)
        if index < len(buttons):
            buttons[index].click()
        else:
            raise IndexError(f"Нет кнопки удаления с индексом {index}, всего кнопок: {len(buttons)}")

    def open_cart(self):
        self.click(self.CART_ICON)

    def get_cart_count(self):
        if self.is_element_present(self.CART_BADGE):
            badge = self.find_element(self.CART_BADGE)
            return int(badge.text) if badge.text else 0
        return 0

    def open_checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def fill_checkout_form(self, first_name, last_name, zip_code):
        self.find_element(self.FIRST_NAME_INPUT).send_keys(first_name)
        self.find_element(self.LAST_NAME_INPUT).send_keys(last_name)
        self.find_element(self.ZIP_CODE_INPUT).send_keys(zip_code)

    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)

    def click_finish(self):
        self.click(self.FINISH_BUTTON)

    def is_success_message_present(self):
        return self.is_element_present(self.SUCCESS_MESSAGE)

    def get_success_message_text(self):
        return self.get_text(self.SUCCESS_MESSAGE)

    def go_back_to_products(self):
        self.click(self.BACK_TO_PRODUCTS_LINK)

    def clear_cart(self):
        while True:
            buttons = self.find_elements_no_wait(self.REMOVE_FROM_CART_BUTTON)
            if not buttons:
                break
            buttons[0].click()
            #self.wait_until_element_absent(self.REMOVE_FROM_CART_BUTTON)