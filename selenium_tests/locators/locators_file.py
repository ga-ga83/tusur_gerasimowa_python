from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def open_login():
    #Запуск драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")

    print("\n ==== Локаторы на www.saucedemo.com ====")

    #1 по ID - поле user-name
    username = driver.find_element(By.ID, "user-name")
    username.send_keys("standard_user")
    print("по ID: поле user-name найдено")
    assert username is not None, f"поле Username найдено на странице, и заполнено"

    #2 по ID - поле password
    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")
    print("по ID: поле password найдено")
    assert password is not None, f"поле Password найдено на странице, и заполнено"

    #3 по ID - кнопка login
    login_button = driver.find_element(By.ID, "login-button")
    print(f"по ID: кнопка '{login_button.get_attribute('value')}' найдена")
    assert login_button is not None, f"кнопка Login найдена на странице"

    #4 по классу - логотип
    logo = driver.find_element(By.CLASS_NAME, "login_logo")
    print(f"по CLASS_NAME: логотип '{logo.text}'")
    assert logo.text == "Swag Labs", f"поиск логотипа на странице завершен успешно"

    #5 по CSS - блок с тестовыми данными
    credentials = driver.find_element(By.CSS_SELECTOR, "#login_credentials")
    print(f"по CSS: блок с данными для авторизации найден")
    assert credentials.is_displayed()

    #нажимаем на кнопку login
    login_button.click()
    time.sleep(2) #ожидание загрузки страницы товаров

    #6 проверка - корректности загрузки страницы товаров
    title = driver.find_element(By.CLASS_NAME, "title")
    print(f"заголовок страницы после перехода: {title.text}")
    assert title.text == "Products", f"переход на страницу продуктов завершен успешно"

    #7 проверка по xPath - header на странице
    textheader = driver.find_element(By.XPATH, "//*[@class='header_label']")
    print(f"по xPath: header страницы продуктов")
    assert textheader is not None, f"заголовок {textheader} найден на странице"

if __name__ == "__main__":
    open_login()