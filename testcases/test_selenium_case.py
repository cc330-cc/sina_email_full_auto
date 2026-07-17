import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.sina_email_page import LoginPageSelenium
import allure

@allure.feature("新浪邮箱 Selenium 引擎")
class TestSinaMailSelenium:

    @allure.story("登录验证 + 窗口切换演示")
    def test_login_demo(self):
        service = Service("F:/Python/chromedriver.exe")  # 修改为您的实际路径
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()

        driver.get("https://mail.sina.com.cn/")
        login_page = LoginPageSelenium(driver)
        login_page.login("cc2535404199@sina.com", "Cc046353")

        driver.quit()