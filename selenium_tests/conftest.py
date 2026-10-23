import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture(scope="function")
def driver():
    #Инициализация браузера
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()
        time.sleep(2)

        yield driver
    finally:
        time.sleep(5)
        driver.quit()


