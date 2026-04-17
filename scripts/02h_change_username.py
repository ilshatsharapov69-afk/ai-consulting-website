"""Change Cal.com username in profile settings."""
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
        page = get_page(ctx)
        if not page:
            page = ctx.new_page()
        page.bring_to_front()

        page.goto("https://app.cal.com/settings/my-account/profile", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        print("URL:", page.url)

        # find username input
        for selector in ["input[name='username']", "input[placeholder*='username' i]"]:
            try:
                el = page.locator(selector).first
                if el.count() > 0 and el.is_visible(timeout=1000):
                    print(f"found via: {selector}")
                    print("  current value:", el.input_value())
                    el.click()
                    el.press("Control+A")
                    el.press("Delete")
                    el.type("ilshatai", delay=50)
                    page.wait_for_timeout(1500)
                    break
            except Exception as e:
                print(f"  {selector}: {str(e)[:80]}")

        # Save / Update
        page.wait_for_timeout(500)
        for label in ["Update", "Save", "Обновить", "Сохранить"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    page.wait_for_timeout(3000)
                    break
            except Exception:
                pass

        # there might be a confirmation dialog
        for label in ["Yes", "Confirm", "Да", "Подтвердить", "Continue", "Продолжить"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=2000)
                    print(f"  confirmed: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(3000)
        # re-read username
        try:
            el = page.locator("input[name='username']").first
            print("  final value:", el.input_value())
        except Exception:
            pass


if __name__ == "__main__":
    main()
