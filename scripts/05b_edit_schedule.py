"""Open default schedule to edit."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "cal.com" in p.url and "availability" in p.url:
                page = p; break
        if not page:
            page = ctx.new_page()
            page.goto("https://app.cal.com/availability", wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
        page.bring_to_front()

        # Click the schedule row (Default)
        try:
            el = page.get_by_text("Default", exact=True).first
            if el.count() > 0:
                el.click()
                print("  clicked Default")
            else:
                # click on "Часы работы"
                el = page.locator("text=Часы работы").first
                el.click()
                print("  clicked Часы работы")
        except Exception as e:
            print(f"  err: {str(e)[:80]}")

        page.wait_for_timeout(4000)
        print("URL:", page.url)
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
