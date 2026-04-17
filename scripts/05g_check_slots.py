"""Click on a future date on the booking page and verify slots render."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()
        page.goto("https://cal.com/ilshat-sharapov-uk7uld/audit", wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        # Click on a non-disabled day (tomorrow or so)
        # Cal.com uses button[data-testid='day'] elements
        for sel in ["button[data-testid='day']:not([disabled])", "button[aria-label*='available']:not([disabled])", "button.cursor-pointer:not([disabled])"]:
            try:
                days = page.locator(sel).all()
                print(f"  selector {sel!r}: {len(days)} matches")
                for d in days[:3]:
                    try:
                        al = d.get_attribute("aria-label") or ""
                        txt = d.inner_text().strip()
                        print(f"    day: aria={al[:40]!r} txt={txt!r}")
                    except Exception:
                        pass
                # click a future day (3rd available)
                if len(days) > 2:
                    days[2].click()
                    print(f"  clicked day index 2")
                    page.wait_for_timeout(2500)
                    break
            except Exception as e:
                print(f"  {sel}: err {str(e)[:50]}")

        # Now look for time slots
        print("\n--- slot buttons ---")
        slots = page.locator("button[data-testid='time'], button.time-slot, [role='listitem'] button").all()
        print(f"  found {len(slots)} potential slots")
        for s in slots[:10]:
            try:
                t = s.inner_text().strip()
                if t: print(f"    {t!r}")
            except Exception:
                pass

        # Fallback: any visible buttons with time format
        print("\n--- any time-like buttons ---")
        count = 0
        for b in page.locator("button:visible").all():
            try:
                t = b.inner_text().strip()
                if ("AM" in t or "PM" in t or ":" in t) and len(t) < 12 and any(c.isdigit() for c in t):
                    count += 1
                    if count <= 10:
                        print(f"    {t!r}")
            except Exception:
                pass
        print(f"  total: {count}")

        # Also read the timezone shown at the bottom of the booking page
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            if "Manila" in line or "UTC" in line or "GMT" in line or "America/" in line or "Asia/" in line or "Europe/" in line:
                if len(line.strip()) < 60:
                    print(f"  tz hint: {line.strip()!r}")


if __name__ == "__main__":
    main()
