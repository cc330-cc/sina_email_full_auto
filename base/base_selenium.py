from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import os
import time

logger = logging.getLogger(__name__)

class BaseSeleniumPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"定位元素超时: {locator}")
            self.take_screenshot("find_error")
            raise

    def click(self, locator):
        self.find_element(locator).click()
        logger.info(f"点击元素: {locator}")

    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"输入文本: {text} 到 {locator}")

    def get_text(self, locator):
        return self.find_element(locator).text

    def wait_until_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_until_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def switch_to_frame(self, frame_ref):
        self.driver.switch_to.frame(frame_ref)

    def switch_to_new_window(self, timeout=10):
        original_handles = self.driver.window_handles
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > len(original_handles)
        )
        new_handles = self.driver.window_handles
        for handle in new_handles:
            if handle not in original_handles:
                self.driver.switch_to.window(handle)
                logger.info(f"切换到新窗口: {handle}")
                return handle
        raise Exception("未发现新窗口")

    def take_screenshot(self, name="screenshot"):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join("screenshot", f"{name}_{timestamp}.png")
        self.driver.save_screenshot(path)
        logger.info(f"截图保存至: {path}")
        return path

    def quit(self):
        self.driver.quit()