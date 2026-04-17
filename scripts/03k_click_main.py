"""Force click on Main stream by coordinates."""
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

        # find the Main text and click it
        try:
            el = page.get_by_text("Main", exact=True).first
            if el.count() > 0:
                el.click()
                print("  clicked Main text")
        except Exception as e:
            print(f"  Main click: {str(e)[:60]}")

        page.wait_for_timeout(4000)
        body = page.locator("body").inner_text()
        m = re.search(r"\bG-[A-Z0-9]{8,12}\b", body)
        if m:
            print(f"\n>>> GA4_MEASUREMENT_ID={m.group(0)}")
            return

        # try clicking Next button to progress
        for label in ["Далее", "Next"]:
            try:
                btn = page.get_by_role("button", name=label, exact=True)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    page.wait_for_timeout(4000)
                    break
            except Exception:
                pass

        body = page.locator("body").inner_text()
        m = re.search(r"\bG-[A-Z0-9]{8,12}\b", body)
        if m:
            print(f"\n>>> GA4_MEASUREMENT_ID={m.group(0)}")
            return

        # try navigating to admin page
        page.goto("https://analytics.google.com/analytics/web/#/a/admin/streams/list", wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
        print("  admin URL:", page.url)
        body = page.locator("body").inner_text()
        m = re.search(r"\bG-[A-Z0-9]{8,12}\b", body)
        if m:
            print(f"\n>>> GA4_MEASUREMENT_ID={m.group(0)}")
            return

        # last resort: look at all pages admin URLs
        print("\n--- URL:", page.url)
        print(body[-1500:])


if __name__ == "__main__":
    main()
