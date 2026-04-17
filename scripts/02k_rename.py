"""Rename event title to English."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()

        page.goto("https://app.cal.com/event-types/5394243?tabName=setup", wait_until="domcontentloaded")
        page.wait_for_timeout(3500)

        # Print all visible text inputs to understand structure
        print("--- visible text inputs ---")
        for i, inp in enumerate(page.locator("input:visible").all()[:15]):
            try:
                t = inp.get_attribute("type") or ""
                name = inp.get_attribute("name") or ""
                val = inp.input_value()
                ph = inp.get_attribute("placeholder") or ""
                if t in ("checkbox", "radio", "hidden"):
                    continue
                print(f"  [{i}] type={t} name={name!r} ph={ph!r} value={val[:50]!r}")
            except Exception:
                pass

        # Try name="title" specifically
        title_input = page.locator("input[name='title']").first
        if title_input.count() > 0:
            title_input.click()
            title_input.press("Control+A")
            title_input.press("Delete")
            title_input.type("AI Audit Call — Money Leaks Review", delay=20)
            print("  title typed")
            page.wait_for_timeout(800)

        # Save
        for label in ["Save", "Сохранить"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked {label}")
                    break
            except Exception:
                pass
        page.wait_for_timeout(3000)
        print("done")


if __name__ == "__main__":
    main()
