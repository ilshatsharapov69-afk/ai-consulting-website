"""Verify schedule saved + check timezone + peek public booking page."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        # 1. Check schedule page for saved state + timezone
        page = None
        for p in ctx.pages:
            if "availability/1444194" in p.url:
                page = p; break
        if not page:
            page = ctx.new_page()
            page.goto("https://app.cal.com/availability/1444194", wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
        page.bring_to_front()

        # Look for timezone section
        print("--- timezone dropdown value ---")
        # cal.com shows timezone as a select with text like "Asia/Manila"
        tz_el = page.locator("input[name='Timezone Select']").first
        if tz_el.count() > 0:
            print(f"  timezone input value: {tz_el.input_value()!r}")

        # look for text containing "Asia" or "Europe" or "GMT" nearby
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            line = line.strip()
            if any(k in line for k in ["Asia/", "Europe/", "America/", "UTC", "GMT"]) and len(line) < 60:
                print(f"  line: {line!r}")

        # 2. Open public booking page for audit event
        page2 = ctx.new_page()
        page2.goto("https://cal.com/ilshat-sharapov-uk7uld/audit", wait_until="domcontentloaded")
        page2.wait_for_timeout(4000)
        print("\n--- public booking page ---")
        print("URL:", page2.url)
        print("TITLE:", page2.title()[:80])

        # Count visible time slots (buttons with AM/PM)
        slot_count = 0
        slot_examples = []
        for b in page2.locator("button:visible").all():
            try:
                t = b.inner_text().strip()
                if ":" in t and ("AM" in t or "PM" in t) and len(t) < 12:
                    slot_count += 1
                    if len(slot_examples) < 8:
                        slot_examples.append(t)
            except Exception:
                pass
        print(f"  visible time slots: {slot_count}")
        print(f"  examples: {slot_examples}")


if __name__ == "__main__":
    main()
