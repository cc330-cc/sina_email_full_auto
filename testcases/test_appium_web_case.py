import pytest
pytestmark = pytest.mark.skip(reason="Appium 环境未配置")


import pytest
from appium import webdriver as appium_webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from pages.sina_email_page import LoginPageSelenium
import allure

@allure.feature("Appium Web 模式")
class TestAppiumWeb:

    @allure.story("移动端浏览器登录测试")
    def test_appium_web_login(self):
        chrome_options = ChromeOptions()
        # 可添加移动端仿真参数（可选）
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        caps = {
            "platformName": "Android",
            "browserName": "Chrome",
            "deviceName": "emulator-5554",
        }
        # 将 options 和 capabilities 合并
        driver = appium_webdriver.Remote(
            command_executor="http://127.0.0.1:4723/wd/hub",
            options=chrome_options,
            desired_capabilities=caps  # 部分版本仍支持
        )
        driver.get("https://mail.sina.com.cn/")
        login_page = LoginPageSelenium(driver)
        main_page = login_page.login("cc2535404199@sina.com", "Cc046353")
        assert "cc2535404199@sina.com" in main_page.get_username()
        driver.quit()