"""Navigate to Microsoft Clarity signup."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()
        page.goto("https://clarity.microsoft.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
        print("URL:", page.url)
        print("TITLE:", page.title())
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass
        print("--- buttons ---")
        for b in page.locator("button:visible, a:visible").all()[:15]:
            try:
                t = b.inner_text().strip()[:60]
                if t: print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
