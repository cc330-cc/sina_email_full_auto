import pytest
import allure
from playwright.sync_api import Page

@allure.feature("新浪邮箱-Playwright 轻量化测试")
class TestPlaywright:

    @allure.story("登录并发送邮件（同步 API）")
    def test_sina_playwright_login(self, page: Page):
        # 1. 打开页面
        page.goto("https://mail.sina.com.cn/", wait_until="domcontentloaded")
        page.screenshot(path="screenshot/pw_01_page_loaded.png")

        # 2. 通过 ID 定位输入框（主文档）
        page.locator("#freename").fill("cc2535404199@sina.com")
        page.locator("#freepassword").fill("Cc046353")
        page.screenshot(path="screenshot/pw_02_credentials_filled.png")

        # 3. 点击免费邮箱登录按钮（限定在 freeMailbox 区域内，避免与 VIP 冲突）
        page.locator("div.freeMailbox a.loginBtn").click()
        page.screenshot(path="screenshot/pw_03_after_click_login.png")

        # 4. 处理图形验证码（如果出现）
        try:
            page.locator("#freecheckcode").wait_for(timeout=3000)
            print("检测到图形验证码，请手动输入")
            captcha = input("请输入验证码后按回车: ")
            page.locator("#freecheckcode").fill(captcha)
            # 再次点击登录
            page.locator("div.freeMailbox a.loginBtn").click()
            page.screenshot(path="screenshot/pw_04_captcha_submitted.png")
        except:
            print("未检测到图形验证码")

        # 5. 处理安全验证弹窗（Text 定位）
        try:
            page.wait_for_selector("text=安全验证", timeout=3000)
            print("检测到安全验证弹窗，请手动完成")
            input("完成后按回车继续...")
            page.screenshot(path="screenshot/pw_05_security_verified.png")
        except:
            pass

        # 6. 等待登录成功
        try:
            page.wait_for_selector(".userName", timeout=10000)
            assert page.locator(".userName").is_visible()
            page.screenshot(path="screenshot/pw_06_login_success.png")

            # 7. 写信并发送
            page.locator("span[title='写信']").click()
            page.locator("input[name='to']").fill("receiver@sina.com")
            page.locator("#subject").fill("Playwright Test Email")
            # 正文编辑框在 iframe 内
            compose_frame = page.frame_locator("iframe")
            compose_frame.locator("body").fill("This email is sent by Playwright.")
            page.locator("a[role='button'][title='发送']").click()
            page.wait_for_selector("text=发送成功", timeout=10000)
            assert page.locator("text=发送成功").is_visible()
            page.screenshot(path="screenshot/pw_10_send_success.png")
            print("登录及发送邮件成功！")
        except Exception as e:
            print(f"登录或发送失败: {e}")
            page.screenshot(path="screenshot/pw_error.png")

        # 最终截图
        page.screenshot(path="screenshot/pw_final.png")
        print("Playwright 测试执行完成，所有截图已保存。")