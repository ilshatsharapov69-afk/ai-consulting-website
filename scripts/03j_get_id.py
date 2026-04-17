"""Click into Main stream to see G-XXXXX Measurement ID."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "analytics.google.com" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Click on the Main stream row
        for locator in [
            "div[role='row']:has-text('Main')",
            "tr:has-text('Main')",
            "a:has-text('Main')",
            "button:has-text('Main')",
            "*:has-text('ai-consulting-website.sherlock753cc')",
        ]:
            try:
                el = page.locator(locator).first
                if el.is_visible(timeout=1500):
                    el.click()
                    print(f"  clicked: {locator}")
                    break
            except Exception as e:
                print(f"  {locator}: {str(e)[:60]}")

        page.wait_for_timeout(5000)

        # now search for G-XXXXX
        body = page.locator("body").inner_text()
        m = re.search(r"\bG-[A-Z0-9]{8,12}\b", body)
        if m:
            print(f"\n>>> GA4_MEASUREMENT_ID={m.group(0)}")
            return

        print("\n--- URL:", page.url)
        print("--- still no ID; last 1500 chars ---")
        print(body[-1500:])


if __name__ == "__main__":
    main()
