from playwright.sync_api import Page, expect
import logging
import os
import time

logger = logging.getLogger(__name__)

class BasePlaywrightPage:
    """Playwright 通用基类（同步 API）"""
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 10000  # 毫秒

    # ---------- 多种定位方式 ----------
    def click(self, selector=None, text=None, role=None, placeholder=None, label=None):
        """支持 CSS/XPath/Text/Role/Placeholder/Label 定位"""
        if selector:
            loc = self.page.locator(selector)
        elif text:
            loc = self.page.get_by_text(text)
        elif role:
            loc = self.page.get_by_role(role)
        elif placeholder:
            loc = self.page.get_by_placeholder(placeholder)
        elif label:
            loc = self.page.get_by_label(label)
        else:
            raise ValueError("至少提供一种定位方式")
        loc.click()
        logger.info(f"点击元素: {selector or text or role or placeholder or label}")

    def fill(self, value, selector=None, placeholder=None, label=None):
        if selector:
            loc = self.page.locator(selector)
        elif placeholder:
            loc = self.page.get_by_placeholder(placeholder)
        elif label:
            loc = self.page.get_by_label(label)
        else:
            raise ValueError("请提供 selector/placeholder/label")
        loc.fill(value)
        logger.info(f"填入: {value}")

    def get_text(self, selector=None, text=None):
        if selector:
            return self.page.locator(selector).text_content()
        elif text:
            return self.page.get_by_text(text).text_content()
        raise ValueError("请提供 selector 或 text")

    # ---------- 断言封装 ----------
    def assert_visible(self, selector=None, text=None, role=None):
        if selector:
            expect(self.page.locator(selector)).to_be_visible()
        elif text:
            expect(self.page.get_by_text(text)).to_be_visible()
        elif role:
            expect(self.page.get_by_role(role)).to_be_visible()
        logger.info(f"断言可见: {selector or text or role}")

    def assert_contains_text(self, selector, expected_text):
        expect(self.page.locator(selector)).to_contain_text(expected_text)

    # ---------- 截图 ----------
    def take_screenshot(self, name="playwright_screenshot"):
        os.makedirs("screenshot", exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join("screenshot", f"{name}_{timestamp}.png")
        self.page.screenshot(path=path)
        logger.info(f"截图保存至: {path}")
        return path

    # ---------- 窗口/标签页 ----------
    def switch_to_new_tab(self):
        new_page = self.page.context.new_page()
        self.page = new_page
        return new_page

    # ---------- 等待 ----------
    def wait_for_selector(self, selector, timeout=10000):
        self.page.wait_for_selector(selector, timeout=timeout)