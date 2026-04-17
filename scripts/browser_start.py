"""
Launch real Chrome (not Chromium) via patchright with stealth.
Navigates to Google sign-in first so user logs in once; SSO propagates to other sites.
"""
import asyncio
from patchright.async_api import async_playwright


async def main():
    pw = await async_playwright().start()
    user_data = "d:/ai-consulting-website/.browser-profile"
    ctx = await pw.chromium.launch_persistent_context(
        user_data_dir=user_data,
        channel="chrome",
        headless=False,
        no_viewport=True,
        args=["--remote-debugging-port=9333"],
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()
    await page.goto("https://accounts.google.com/")
    print("[browser] Real Chrome launched (patchright stealth). CDP port 9333.")
    print("[browser] Navigated to Google sign-in. Waiting indefinitely.")
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        await ctx.close()


if __name__ == "__main__":
    asyncio.run(main())
