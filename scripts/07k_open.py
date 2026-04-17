"""Just open Email Routing page for setpointaudit.com."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()
        page.goto("https://dash.cloudflare.com/b1c393c0ca48e9577d6d2ab7f4fa78c9/setpointaudit.com/email/routing/overview", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        print("URL:", page.url)
        print("Page is open in browser. User can now click Get started.")


if __name__ == "__main__":
    main()
