"""Just open schedule page for user to edit."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "availability/1444194" in p.url:
                page = p; break
        if not page:
            page = ctx.new_page()
            page.goto("https://app.cal.com/availability/1444194", wait_until="domcontentloaded")
        page.bring_to_front()
        print("Page opened.")
        print("URL:", page.url)


if __name__ == "__main__":
    main()
