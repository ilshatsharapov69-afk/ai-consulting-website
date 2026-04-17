"""Final check + change slug to 'audit' for cleaner URL."""
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

        # Print current state
        for name in ["title", "slug", "length"]:
            try:
                el = page.locator(f"input[name='{name}']").first
                if el.count():
                    print(f"  {name} = {el.input_value()!r}")
            except Exception:
                pass

        # change slug to 'audit'
        slug = page.locator("input[name='slug']").first
        if slug.count():
            slug.click()
            slug.press("Control+A")
            slug.press("Delete")
            slug.type("audit", delay=30)
            print("  slug -> 'audit'")

        page.wait_for_timeout(500)

        # Save
        for label in ["Save", "Сохранить"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  saved")
                    break
            except Exception:
                pass

        page.wait_for_timeout(4000)

        # Verify
        page.goto("https://cal.com/ilshat-sharapov-uk7uld/audit", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        print("\n--- verify public URL ---")
        print("  URL:", page.url)
        print("  TITLE:", page.title()[:80])
        for h in page.locator("h1, h2").all()[:3]:
            try:
                t = h.inner_text().strip()[:60]
                if t:
                    print("  h:", t)
            except Exception:
                pass


if __name__ == "__main__":
    main()
