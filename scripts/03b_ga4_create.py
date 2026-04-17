"""Click Create Account on GA4, start provisioning."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def get_page(ctx):
    for p in ctx.pages:
        if "analytics.google.com" in p.url:
            return p
    return None


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page: print("no page"); return
        page.bring_to_front()

        # Click "Создать аккаунт" (Create Account)
        for label in ["Создать аккаунт", "Create account", "Get started"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(4000)
        print("URL:", page.url)
        print("--- visible inputs ---")
        for inp in page.locator("input:visible").all()[:10]:
            try:
                t = inp.get_attribute("type") or ""
                n = inp.get_attribute("name") or inp.get_attribute("aria-label") or ""
                v = inp.input_value() if t not in ("checkbox", "radio") else ""
                print(f"  type={t} name/label={n!r} value={v[:40]!r}")
            except Exception:
                pass
        print("--- h1/h2/h3 ---")
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t:
                    print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
