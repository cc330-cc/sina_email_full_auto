import pytest
import asyncio
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_async_playwright():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://mail.sina.com.cn/")
        await page.locator("input[name='freename']").fill("user")
        # ... 异步操作
        await page.screenshot(path="screenshot/async_example.png")
        await browser.close()