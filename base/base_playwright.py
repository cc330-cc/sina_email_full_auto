import pytest
import allure

@allure.feature("新浪邮箱-Playwright 轻量化测试")
class TestPlaywright:

    @allure.story("登录并发送邮件（同步 API）")
    def test_sina_playwright_login(self, page):  # pytest-playwright 提供
        # 1. 打开页面
        page.goto("https://mail.sina.com.cn/")
        page.screenshot(path="screenshot/pw_01_page_loaded.png")

        # 2. CSS 定位：输入账号密码
        page.locator("input[name='freename']").fill("cc2535404199@sina.com")
        page.locator("input[name='freepassword']").fill("Cc046353")
        page.screenshot(path="screenshot/pw_02_credentials_filled.png")

        # 3. XPath 定位登录按钮（备用，如用 CSS 亦可）
        # page.locator("//a[contains(@class,'loginBtn')]").click()
        # 这里用 CSS 直接演示
        page.locator("a.loginBtn").click()
        page.screenshot(path="screenshot/pw_03_after_click_login.png")

        # 4. 处理验证码（如果有）
        try:
            page.wait_for_selector("#freecheckcode", timeout=3000)
            print("检测到图形验证码，请查看浏览器输入验证码")
            captcha = input("请输入验证码后按回车: ")
            page.locator("#freecheckcode").fill(captcha)
            page.locator("a.loginBtn").click()
            page.screenshot(path="screenshot/pw_04_captcha_submitted.png")
        except:
            pass

        # 5. 处理安全验证弹窗（Text 定位）
        try:
            page.wait_for_selector("text=安全验证", timeout=3000)
            print("检测到安全验证弹窗，请手动完成")
            input("完成后按回车继续...")
            page.screenshot(path="screenshot/pw_05_security_verified.png")
        except:
            pass

        # 6. 等待登录成功，断言用户名可见（CSS 定位 + 断言）
        page.wait_for_selector(".userName", timeout=10000)
        assert page.locator(".userName").is_visible()
        page.screenshot(path="screenshot/pw_06_login_success.png")

        # 7. 点击写信（CSS 定位）
        page.locator("span[title='写信']").click()
        page.screenshot(path="screenshot/pw_07_compose_opened.png")

        # 8. 写信：使用 Name 和 ID 定位
        page.locator("input[name='to']").fill("receiver@sina.com")
        page.locator("#subject").fill("Playwright Test Email")
        # 正文在 iframe 内，使用 frame_locator
        frame = page.frame_locator("iframe")
        frame.locator("body").fill("This email is sent by Playwright.")
        page.screenshot(path="screenshot/pw_08_compose_filled.png")

        # 9. 发送（CSS 定位）
        page.locator("a[role='button'][title='发送']").click()
        page.screenshot(path="screenshot/pw_09_after_send_click.png")

        # 10. 断言发送成功（Text 定位）
        page.wait_for_selector("text=发送成功", timeout=10000)
        assert page.locator("text=发送成功").is_visible()
        page.screenshot(path="screenshot/pw_10_send_success.png")

        print("Playwright 测试完成，所有截图已保存。")