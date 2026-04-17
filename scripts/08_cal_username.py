"""Change Cal.com username from ilshat-sharapov-uk7uld to ilshatai."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()
        page.goto("https://app.cal.com/settings/my-account/profile", wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        print("URL:", page.url)

        # Find username field — try scrolling through the page
        print("--- visible username-related inputs/elements ---")
        for inp in page.locator("input:visible").all()[:15]:
            try:
                n = inp.get_attribute("name") or ""
                t = inp.get_attribute("type") or ""
                v = inp.input_value() if t not in ("checkbox","radio","hidden") else ""
                if t in ("hidden", "checkbox", "radio"): continue
                if "username" in n.lower() or "ilshat" in v.lower() or "sharapov" in v.lower():
                    print(f"  FOUND: name={n!r} type={t!r} value={v[:60]!r}")
            except Exception:
                pass

        # Try to find and change username
        uname = page.locator("input[name='username']").first
        if uname.count() > 0:
            try:
                uname.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                uname.click()
                uname.press("Control+A")
                uname.press("Delete")
                uname.type("ilshatai", delay=50)
                print("  typed ilshatai")
                page.wait_for_timeout(2000)

                # Check for availability indicator
                print("\n--- body text near username ---")
                body = page.locator("body").inner_text()
                for line in body.split("\n"):
                    s = line.strip()
                    if any(k in s.lower() for k in ["available", "taken", "unavailable", "not available"]) and len(s) < 120:
                        print(f"  {s!r}")

                # Click Update
                for label in ["Update", "Save"]:
                    try:
                        btn = page.get_by_role("button", name=label, exact=True)
                        if btn.count() > 0 and btn.first.is_visible():
                            btn.first.click(timeout=3000)
                            print(f"  clicked {label}")
                            break
                    except Exception:
                        pass

                page.wait_for_timeout(4000)
                # Look for confirmation or verification prompt
                print("\n--- final state ---")
                body = page.locator("body").inner_text()
                for line in body.split("\n"):
                    s = line.strip()
                    if any(k in s.lower() for k in ["verification", "verify", "confirm", "email sent", "check your email", "success", "updated"]) and len(s) < 200:
                        print(f"  {s!r}")

                # Verify final value
                page.wait_for_timeout(2000)
                uname2 = page.locator("input[name='username']").first
                if uname2.count():
                    print(f"\n  current username input: {uname2.input_value()!r}")
            except Exception as e:
                print(f"  err: {str(e)[:150]}")


if __name__ == "__main__":
    main()
