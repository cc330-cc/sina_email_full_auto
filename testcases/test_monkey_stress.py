import pytest
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
import allure

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@allure.feature("Monkey 随机压力测试")
class TestMonkeyStress:

    @allure.story("页面随机操作 60 秒")
    def test_sina_monkey_stress(self):
        # 1. 打开浏览器
        driver = webdriver.Chrome()
        driver.get("https://mail.sina.com.cn/")
        driver.implicitly_wait(3)  # 隐式等待

        start_time = time.time()
        timeout = 60
        action = ActionChains(driver)

        # 统计变量
        total_ops = 0
        stats = {"click": 0, "input": 0, "hover": 0, "scroll": 0, "errors": 0}
        error_screenshots = []

        try:
            while time.time() - start_time < timeout:
                try:
                    # 随机操作类型
                    op = random.choice(["click", "input", "hover", "scroll"])
                    # 收集当前可交互元素（扩大选择范围）
                    elements = driver.find_elements(By.XPATH,
                        "//*[@onclick or @href or @type='submit' or @role='button' or @class='loginBtn']")
                    if not elements:
                        time.sleep(0.5)
                        continue

                    target = random.choice(elements)
                    with allure.step(f"执行随机操作: {op}"):
                        if op == "click":
                            target.click()
                            stats["click"] += 1
                            logger.info(f"点击元素: {target.tag_name}")
                        elif op == "input":
                            if target.tag_name in ["input", "textarea"]:
                                text = random.choice(["test", "123", "hello", "monkey"])
                                target.send_keys(text)
                                stats["input"] += 1
                                logger.info(f"输入文本: {text}")
                        elif op == "hover":
                            action.move_to_element(target).perform()
                            stats["hover"] += 1
                            logger.info(f"悬停元素: {target.tag_name}")
                        elif op == "scroll":
                            driver.execute_script("window.scrollBy(0, 100);")
                            stats["scroll"] += 1
                            logger.info("滚动页面")
                        total_ops += 1
                        time.sleep(random.uniform(0.2, 0.8))

                except Exception as e:
                    logger.error(f"随机操作异常: {e}")
                    stats["errors"] += 1
                    # 截图并嵌入报告
                    screenshot = driver.get_screenshot_as_png()
                    allure.attach(
                        screenshot,
                        name=f"异常截图_{int(time.time())}",
                        attachment_type=allure.attachment_type.PNG
                    )
                    # 继续执行
                    continue

        finally:
            # 无论如何，最后附加统计信息
            allure.attach(
                f"总操作数: {total_ops}\n"
                f"点击次数: {stats['click']}\n"
                f"输入次数: {stats['input']}\n"
                f"悬停次数: {stats['hover']}\n"
                f"滚动次数: {stats['scroll']}\n"
                f"错误次数: {stats['errors']}",
                name="操作统计",
                attachment_type=allure.attachment_type.TEXT
            )
            # 关闭浏览器
            driver.quit()
            logger.info("Monkey 测试执行完毕")