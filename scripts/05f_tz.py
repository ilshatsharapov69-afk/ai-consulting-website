"""Change schedule timezone to Asia/Manila."""
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
            page.wait_for_timeout(3000)
        page.bring_to_front()

        # Click on timezone (currently Europe/London)
        tz = page.locator("text=Europe/London").first
        if tz.count() > 0:
            tz.click()
            print("  clicked Europe/London")
            page.wait_for_timeout(1500)

            # Type Manila in the filter
            # The search input should be visible now
            search = page.locator("input[role='combobox']:visible, input[name='Timezone Select']").first
            if search.count() > 0:
                search.click()
                search.press("Control+A")
                search.type("Manila", delay=60)
                print("  typed 'Manila'")
                page.wait_for_timeout(1500)

                # click first option
                for sel in ["[role='option']:visible", "div[id^='react-select'][id*='option']:visible", ".select-option:visible"]:
                    try:
                        opts = page.locator(sel).all()
                        if opts:
                            opts[0].click()
                            print(f"  picked: {opts[0].inner_text().strip()[:40]}")
                            break
                    except Exception:
                        pass

        page.wait_for_timeout(1500)

        # Save
        try:
            btn = page.get_by_role("button", name="Save", exact=False)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click(timeout=3000)
                print("  clicked Save")
        except Exception as e:
            print(f"  save err: {str(e)[:60]}")

        page.wait_for_timeout(3000)
        # re-check
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            line = line.strip()
            if any(k in line for k in ["Asia/", "Europe/", "America/", "UTC", "GMT", "Manila"]) and len(line) < 60:
                print(f"  TZ line: {line!r}")


if __name__ == "__main__":
    main()
