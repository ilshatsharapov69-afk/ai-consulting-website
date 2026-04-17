"""Verify the final event URL and slug."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()
        page.goto("https://app.cal.com/event-types", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        for a in page.locator("a[href*='/event-types/']").all():
            try:
                href = a.get_attribute("href") or ""
                txt = a.inner_text().strip().replace("\n", " | ")[:80]
                print(f"  {href[:70]} — {txt}")
            except Exception:
                pass

        # Also check the Cal public page renders correctly
        page2 = ctx.new_page()
        page2.goto("https://cal.com/ilshat-sharapov-uk7uld/30min", wait_until="domcontentloaded")
        page2.wait_for_timeout(3000)
        print("\n--- public booking page ---")
        print("  URL:", page2.url)
        print("  TITLE:", page2.title())
        for h in page2.locator("h1, h2").all()[:3]:
            try:
                print(" ", h.inner_text().strip()[:60])
            except Exception:
                pass
        # look for duration badge
        body = page2.locator("body").inner_text()
        for line in body.split("\n"):
            if "min" in line.lower() and len(line) < 40:
                print(" line:", line.strip())


if __name__ == "__main__":
    main()
