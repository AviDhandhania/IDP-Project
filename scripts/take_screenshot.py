import asyncio
from playwright.async_api import async_playwright

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to dashboard...")
        await page.goto("http://localhost:8081/")
        # wait for any animations or data to load
        await page.wait_for_timeout(2000)
        
        # Take full page screenshot
        await page.screenshot(path="assets/dashboard.png", full_page=True)
        print("Dashboard screenshot saved to assets/dashboard.png")

        # Let's try to simulate a scan and take another screenshot
        # If there's a scan button, we can click it
        try:
            scan_button = await page.query_selector('button:has-text("Scan")')
            if scan_button:
                print("Clicking scan button...")
                await scan_button.click()
                await page.wait_for_timeout(3000)
                await page.screenshot(path="assets/dashboard_results.png", full_page=True)
                print("Results screenshot saved to assets/dashboard_results.png")
            else:
                # wait to see if it just auto-loads
                await page.wait_for_timeout(2000)
                await page.screenshot(path="assets/dashboard_results.png", full_page=True)
        except Exception as e:
            print("Could not click scan button:", e)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture())
