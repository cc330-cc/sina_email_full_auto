from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://mail.sina.com.cn/")
time.sleep(5)  # 等待页面完全加载

print("页面标题:", driver.title)

# 1. 检查是否存在 iframe
iframes = driver.find_elements(By.TAG_NAME, "iframe")
print(f"发现 {len(iframes)} 个 iframe")
for idx, iframe in enumerate(iframes):
    print(f"iframe {idx}: src='{iframe.get_attribute('src')}'")

# 2. 打印所有 input 元素的 name 和 id
inputs = driver.find_elements(By.TAG_NAME, "input")
print("\n所有 input 元素:")
for inp in inputs:
    name = inp.get_attribute('name')
    id_attr = inp.get_attribute('id')
    placeholder = inp.get_attribute('placeholder')
    print(f"  name='{name}', id='{id_attr}', placeholder='{placeholder}'")

# 3. 打印所有 button 元素上的文字
buttons = driver.find_elements(By.TAG_NAME, "button")
print("\n所有 button 文字:")
for btn in buttons:
    print(f"  {btn.text}")

driver.quit()