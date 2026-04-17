"""Check Lead Generation objective + click Create. Then handle ToS + get Measurement ID."""
import sys, io, re
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

        # Check "Привлечение лидов" (Lead Generation)
        cb = page.locator("input[name='Привлечение лидов']").first
        if cb.count() > 0:
            cb.check(force=True)
            print("  checked Lead Generation")

        page.wait_for_timeout(500)

        # Click Create
        for label in ["Создать", "Create"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(5000)
        print("\nURL:", page.url)

        # ToS modal may appear. Select country, check boxes, accept.
        # first look for country select + checkboxes
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass

        # check all visible checkboxes
        for cb in page.locator("input[type='checkbox']:visible").all()[:10]:
            try:
                if not cb.is_checked():
                    cb.check(force=True)
                    print("  checked ToS box")
            except Exception:
                pass

        # Click "Принимаю" / "I Accept"
        for label in ["Принимаю", "I Accept", "Accept", "Согласен"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(6000)
        print("\nURL after accept:", page.url)

        # We might see a data collection platform picker — pick Web
        for label in ["Веб", "Web"]:
            try:
                el = page.locator(f"button:has-text('{label}'), div[role='button']:has-text('{label}')").first
                if el.is_visible(timeout=1500):
                    el.click()
                    print(f"  clicked platform: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(4000)
        print("URL:", page.url)
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass

        # Look for measurement ID
        body = page.locator("body").inner_text()
        m = re.search(r"\bG-[A-Z0-9]{8,12}\b", body)
        if m:
            print(f"\n>>> GA4_MEASUREMENT_ID={m.group(0)}")


if __name__ == "__main__":
    main()
