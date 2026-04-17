"""Change Cal.com username to 'ilshatai'."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "cal.com" in p.url and "profile" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        uname = page.locator("input[name='username']").first
        uname.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        uname.click()
        page.wait_for_timeout(200)
        uname.press("Control+A")
        page.wait_for_timeout(100)
        uname.press("Delete")
        page.wait_for_timeout(200)
        uname.type("ilshatai", delay=60)
        print("  typed ilshatai")
        page.wait_for_timeout(2500)

        # check availability text
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            s = line.strip()
            if any(k in s.lower() for k in ["available", "taken", "already", "not available"]) and len(s) < 120:
                print(f"  availability: {s!r}")

        # Click Update
        for label in ["Update", "Save"]:
            try:
                btn = page.get_by_role("button", name=label, exact=True)
                cnt = btn.count()
                if cnt > 0:
                    for i in range(cnt):
                        b = btn.nth(i)
                        if b.is_visible():
                            b.scroll_into_view_if_needed()
                            b.click(timeout=3000)
                            print(f"  clicked {label} (index {i})")
                            break
                    break
            except Exception as e:
                print(f"  {label} err: {str(e)[:60]}")

        page.wait_for_timeout(4000)

        # check for confirmation modal
        print("\n--- after click ---")
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            s = line.strip()
            if any(k in s.lower() for k in ["confirm", "sure", "want to change", "verification", "check email"]) and len(s) < 200:
                print(f"  {s!r}")

        # If confirm dialog — click confirm
        for label in ["Confirm", "Yes", "Change", "I'm sure"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible(timeout=1500):
                    btn.first.click(timeout=3000)
                    print(f"  confirmed: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(4000)

        # Verify
        uname2 = page.locator("input[name='username']").first
        print(f"\n  final username value: {uname2.input_value()!r}")

        # Verify public URL
        page2 = ctx.new_page()
        page2.goto("https://cal.com/ilshatai/audit", wait_until="domcontentloaded")
        page2.wait_for_timeout(3000)
        print(f"\n  /ilshatai/audit page title: {page2.title()[:80]!r}")


if __name__ == "__main__":
    main()
