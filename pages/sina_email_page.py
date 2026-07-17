from base.base_selenium import BaseSeleniumPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

logger = logging.getLogger(__name__)

class LoginPageSelenium(BaseSeleniumPage):
    # ---------- 定位器（涵盖多种定位方式） ----------
    # 1. ID
    USERNAME_INPUT = (By.ID, "freename")
    PASSWORD_INPUT = (By.ID, "freepassword")
    CAPTCHA_INPUT = (By.ID, "freecheckcode")
    # 2. CSS
    LOGIN_BTN_CSS = (By.CSS_SELECTOR, "a.loginBtn")
    # 3. XPath
    LOGIN_BTN_XPATH = (By.XPATH, "//a[contains(@class,'loginBtn')]")
    # 4. LINK_TEXT（注册链接）
    REGISTER_LINK = (By.LINK_TEXT, "注册")
    # 5. PARTIAL_LINK_TEXT（忘记密码链接，演示第八种）
    FORGET_PWD = (By.PARTIAL_LINK_TEXT, "忘记密码")
    # 6. 其他（在 MainPageSelenium 中有 CLASS_NAME，在 ComposePageSelenium 中有 NAME、TAG_NAME）

    VERIFY_POPUP = (By.XPATH, "//div[contains(text(),'安全验证') or contains(text(),'请完成安全验证')]")

    def login(self, username, password):
        # 1. 页面加载
        self.wait_for_page_loaded()
        self.take_screenshot("01_page_loaded")

        # 2. 演示注册窗口切换（使用 LINK_TEXT）
        self._demo_register_window_switch()

        # 3. 切换到登录 iframe
        self._switch_to_login_iframe()

        # 4. 填写账号密码
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.take_screenshot("02_credentials_filled")

        # 5. 演示 PARTIAL_LINK_TEXT 定位（忘记密码链接）
        self._demo_partial_link_text()

        # 6. 点击登录
        login_btn = self._find_login_button()
        self.driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", login_btn)
        logger.info("点击登录按钮")
        self.take_screenshot("03_after_click_login")

        # 7. 等待验证出现并截图（第四张）
        time.sleep(3)
        self.driver.switch_to.default_content()
        self.take_screenshot("04_verify_appeared")
        logger.info("已截取验证出现时的页面")

        # 8. 检测图形验证码
        try:
            self._switch_to_login_iframe()
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.CAPTCHA_INPUT)
            )
            logger.info("检测到图形验证码，请手动输入")
            captcha = input("请输入页面上的图形验证码（输入后按回车继续）: ")
            self.send_keys(self.CAPTCHA_INPUT, captcha)
            login_btn = self._find_login_button()
            self.driver.execute_script("arguments[0].click();", login_btn)
        except TimeoutException:
            logger.info("未检测到图形验证码")

        # 9. 检测安全验证弹窗
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.VERIFY_POPUP)
            )
            logger.info("检测到安全验证弹窗，请手动完成")
            input("请完成页面上的安全验证，完成后按回车继续...")
        except TimeoutException:
            pass

        input("登录演示结束，按回车退出...")
        return MainPageSelenium(self.driver)

    def _demo_partial_link_text(self):
        """演示 PARTIAL_LINK_TEXT 定位（忘记密码）"""
        try:
            # 由于登录表单在 iframe 内，需要确保在正确的 iframe 内查找
            # 我们已经切到 iframe，所以直接查找
            element = self.driver.find_element(*self.FORGET_PWD)
            # 高亮或滚动到元素（可选），并截图
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            self.take_screenshot("06_forget_password_partial_link")
            logger.info("成功定位 '忘记密码' 链接（PARTIAL_LINK_TEXT）")
        except Exception as e:
            logger.warning(f"演示 PARTIAL_LINK_TEXT 失败: {e}")

    def _demo_register_window_switch(self):
        """演示注册窗口切换（LINK_TEXT 定位）"""
        try:
            # 注册链接在主文档，切回主文档
            self.driver.switch_to.default_content()
            reg_link = self.driver.find_element(*self.REGISTER_LINK)
            reg_link.click()
            logger.info("点击注册链接")

            original_handle = self.driver.current_window_handle
            self.switch_to_new_window(timeout=10)
            self.take_screenshot("05_register_window")
            logger.info("切换到注册窗口并截图")

            self.close_current_window_and_switch_back(original_handle)
            logger.info("切回登录窗口")
            self.wait_for_page_loaded()
            # 切回后需要重新进入 iframe，因为后续操作需要
            self._switch_to_login_iframe()
        except Exception as e:
            logger.warning(f"注册窗口切换演示失败: {e}")

    # ---------- 辅助方法 ----------
    def _switch_to_login_iframe(self):
        try:
            self.driver.find_element(*self.USERNAME_INPUT)
            logger.info("登录表单不在 iframe 内")
            return
        except NoSuchElementException:
            pass
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            try:
                self.driver.find_element(*self.USERNAME_INPUT)
                logger.info(f"切换到登录 iframe: {iframe.get_attribute('src')}")
                return
            except NoSuchElementException:
                self.driver.switch_to.default_content()
        raise Exception("未找到登录 iframe")

    def _find_login_button(self):
        locators = [self.LOGIN_BTN_CSS, self.LOGIN_BTN_XPATH]
        for locator in locators:
            try:
                btn = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(locator)
                )
                return btn
            except TimeoutException:
                continue
        raise Exception("找不到登录按钮")

    def wait_for_page_loaded(self, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )


class MainPageSelenium(BaseSeleniumPage):
    # 演示 CLASS_NAME 定位
    USERNAME_LABEL = (By.CLASS_NAME, "userName")
    WRITE_MAIL_BTN = (By.CSS_SELECTOR, "span[title='写信']")

    def get_username(self):
        return self.get_text(self.USERNAME_LABEL)


class ComposePageSelenium(BaseSeleniumPage):
    # 演示 NAME 和 TAG_NAME 定位
    RECEIVER_INPUT = (By.NAME, "to")
    SUBJECT_INPUT = (By.ID, "subject")
    BODY_FRAME = (By.TAG_NAME, "iframe")
    BODY_BODY = (By.XPATH, "//body[@contenteditable='true']")
    SEND_BTN = (By.CSS_SELECTOR, "a[role='button'][title='发送']")
    SEND_SUCCESS_MSG = (By.XPATH, "//div[contains(text(),'发送成功')]")

    def send_mail(self, to, subject, body):
        self.send_keys(self.RECEIVER_INPUT, to)
        self.send_keys(self.SUBJECT_INPUT, subject)
        self.switch_to_frame(self.BODY_FRAME)
        self.send_keys(self.BODY_BODY, body)
        self.driver.switch_to.default_content()
        self.click(self.SEND_BTN)
        self.wait_until_visible(self.SEND_SUCCESS_MSG, timeout=15)
        return self.get_text(self.SEND_SUCCESS_MSG)
    
# 在 pages/sina_email_page.py 末尾添加以下内容

from base.base_playwright import BasePlaywrightPage

class LoginPagePlaywright(BasePlaywrightPage):
    """Playwright 版登录页，演示多种定位"""
    def login(self, username, password):
        # 1. 使用 CSS 定位（选择器）
        self.page.locator("input[name='freename']").fill(username)
        # 2. 使用 Placeholder 定位（假设存在）
        # self.fill(password, placeholder="请输入密码")
        # 但实际新浪邮箱密码框没有 placeholder，用 CSS
        self.page.locator("input[name='freepassword']").fill(password)

        # 3. 使用 Role 定位（按钮）
        # 登录按钮是 <a class="loginBtn">，不支持 role，我们用 CSS
        self.click(selector="a.loginBtn")

        # 4. 检测验证码（演示 Text 定位，如果出现“安全验证”字样）
        try:
            self.page.wait_for_selector("text=安全验证", timeout=3000)
            # 出现安全验证，提示用户
            print("检测到安全验证，请手动完成...")
            input("完成后按回车继续...")
        except:
            pass

        # 5. 断言登录成功：使用 Text 定位用户名
        self.assert_visible(text="cc2535404199")  # 假设用户名显示
        # 截图
        self.take_screenshot("playwright_login_success")
        return MainPagePlaywright(self.page)

class MainPagePlaywright(BasePlaywrightPage):
    def click_write_mail(self):
        self.click(selector="span[title='写信']")
        return ComposePagePlaywright(self.page)

class ComposePagePlaywright(BasePlaywrightPage):
    def send_mail(self, to, subject, body):
        # 使用 CSS 和 XPath 混合
        self.fill(to, selector="input[name='to']")
        self.fill(subject, selector="#subject")
        # 切换到 iframe（Playwright 使用 frame_locator）
        frame = self.page.frame_locator("iframe")
        frame.locator("body").fill(body)
        self.click(selector="a[role='button'][title='发送']")
        # 断言发送成功
        self.assert_visible(text="发送成功")
        self.take_screenshot("playwright_send_success")
        return "发送成功"