"""Click 'Войти' (Sign in) on Clarity."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "clarity" in p.url or "microsoft" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Click Войти using .locator with text matching
        try:
            el = page.locator("a:has-text('Войти'), button:has-text('Войти')").first
            el.click(timeout=5000)
            print("  clicked Войти")
        except Exception as e:
            print(f"  click err: {str(e)[:80]}")

        page.wait_for_timeout(6000)
        print("\nURL:", page.url)
        for h in page.locator("h1, h2").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass
        # providers
        print("--- visible providers ---")
        for b in page.locator("button:visible, a:visible").all()[:15]:
            try:
                t = b.inner_text().strip()[:80]
                if any(p in t for p in ["Microsoft", "Google", "Facebook", "Корпорати", "microsoft", "google"]):
                    print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
