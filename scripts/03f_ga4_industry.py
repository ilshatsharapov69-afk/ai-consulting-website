"""Pick Industry for GA4 + continue."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "analytics.google.com" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # search input is open, type to filter
        search = page.locator("input[type='search']").first
        if search.is_visible():
            search.click()
            search.type("Бизнес", delay=50)
            page.wait_for_timeout(1500)

        # pick first matching option
        for sel in ["mat-option:visible", "li[role='option']:visible", "button:visible"]:
            try:
                opts = page.locator(sel).all()
                if opts:
                    for o in opts[:5]:
                        t = o.inner_text().strip()[:60]
                        print(f"  opt: {t!r}")
                    # click first with "Бизнес" or "промышлен"
                    for o in opts:
                        t = o.inner_text().strip()
                        if "Бизнес" in t or "промышлен" in t.lower():
                            o.click()
                            print(f"  clicked: {t[:40]}")
                            break
                    else:
                        opts[0].click()
                        print(f"  fallback clicked first: {opts[0].inner_text().strip()[:40]}")
                    break
            except Exception as e:
                print(f"  {sel}: {str(e)[:60]}")

        page.wait_for_timeout(1200)

        # Click Next
        for label in ["Далее", "Next"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(4000)
        print("\nAfter URL:", page.url)
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
