import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from playwright.sync_api import sync_playwright
import logging

logger = logging.getLogger(__name__)

class EngineSwitch:
    CHROME_DRIVER_PATH = "F:/Python/chromedriver.exe"  # 改为您的实际路径

    @staticmethod
    def get_driver(engine=None):
        # 忽略 engine，只支持 selenium
        service = Service(EngineSwitch.CHROME_DRIVER_PATH)
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        return driver  # 请修改为您的实际路径

    @staticmethod
    def get_driver(engine=None):
        engine = engine or os.getenv("ENGINE", "selenium")
        if engine == "selenium":
            service = Service(EngineSwitch.CHROME_DRIVER_PATH)
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            # 可选无头模式
            # options.add_argument("--headless")
            driver = webdriver.Chrome(service=service, options=options)
            driver.maximize_window()
            return driver
        elif engine == "playwright":
            # 返回 playwright 对象、浏览器和页面，由调用方管理
            pw = sync_playwright().start()
            browser = pw.chromium.launch(headless=False)
            page = browser.new_page()
            return {"playwright": pw, "browser": browser, "page": page}
        else:
            raise ValueError("不支持的引擎，请选择 selenium 或 playwright")