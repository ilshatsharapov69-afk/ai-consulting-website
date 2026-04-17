"""Edit Cal.com 30min event: change duration to 20, rename."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def get_page(ctx):
    for p in ctx.pages:
        if "cal.com" in p.url:
            return p
    return None


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx) or ctx.new_page()
        page.bring_to_front()

        page.goto("https://app.cal.com/event-types/5394243?tabName=setup", wait_until="domcontentloaded")
        page.wait_for_timeout(3500)
        print("URL:", page.url)

        # Inspect: look for a "Duration" / "Length" input
        print("--- visible number inputs ---")
        for inp in page.locator("input[type='number']:visible").all()[:10]:
            try:
                val = inp.input_value()
                name = inp.get_attribute("name") or ""
                print(f"  name={name} value={val}")
            except Exception:
                pass

        # Strategy: find input with value=30 (the duration)
        duration_input = None
        for inp in page.locator("input:visible").all():
            try:
                val = inp.input_value()
                name = (inp.get_attribute("name") or "").lower()
                t = inp.get_attribute("type") or ""
                if val == "30" and t in ("number", "text", ""):
                    duration_input = inp
                    print(f"  found duration input: name={name}")
                    break
            except Exception:
                pass

        if duration_input:
            duration_input.click()
            duration_input.press("Control+A")
            duration_input.type("20", delay=80)
            print("  duration set to 20")

        # also rename title
        title_input = None
        for inp in page.locator("input[type='text']:visible").all():
            try:
                val = inp.input_value()
                if "30" in val or "минут" in val or "Min" in val or "Meeting" in val or "min" in val.lower():
                    title_input = inp
                    break
            except Exception:
                pass
        if title_input:
            title_input.click()
            title_input.press("Control+A")
            title_input.type("AI Audit Call — Money Leaks Review", delay=30)
            print("  title updated")

        page.wait_for_timeout(1000)

        # Click Save
        for label in ["Save", "Сохранить", "Update"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(4000)
        print("URL after save:", page.url)

        # Check: re-read the duration
        for inp in page.locator("input:visible").all():
            try:
                val = inp.input_value()
                name = (inp.get_attribute("name") or "").lower()
                if val in ("20", "30") and not name:
                    print(f"  current duration: {val}")
                    break
            except Exception:
                pass


if __name__ == "__main__":
    main()
