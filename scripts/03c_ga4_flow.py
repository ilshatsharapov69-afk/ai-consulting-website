"""GA4 provisioning: fill account name, click Next, fill property, continue to web stream."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def get_page(ctx):
    for p in ctx.pages:
        if "analytics.google.com" in p.url:
            return p
    return None


def click_any(page, labels):
    for label in labels:
        try:
            btn = page.get_by_role("button", name=label, exact=False)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click(timeout=3000)
                print(f"  clicked: {label}")
                return True
        except Exception:
            pass
    return False


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page: print("no page"); return
        page.bring_to_front()

        # Step 1: Account name
        name_inp = page.locator("input[name='name']").first
        if name_inp.is_visible():
            name_inp.click()
            name_inp.fill("AI Consulting")
            print("  filled account name")

        page.wait_for_timeout(800)
        click_any(page, ["Далее", "Next"])
        page.wait_for_timeout(3500)

        # Step 2: Property details
        print("\n--- step 2 ---")
        print("URL:", page.url)
        inputs = page.locator("input:visible").all()
        for inp in inputs[:5]:
            try:
                n = inp.get_attribute("name") or ""
                t = inp.get_attribute("type") or ""
                if t == "text" and n == "name":
                    inp.click()
                    inp.fill("AI Consulting Website")
                    print("  filled property name")
                    break
            except Exception:
                pass

        page.wait_for_timeout(800)
        click_any(page, ["Далее", "Next"])
        page.wait_for_timeout(3500)

        # Step 3: Business details (may have radios/select)
        print("\n--- step 3 ---")
        print("URL:", page.url)
        # Try to click any default/skip option
        click_any(page, ["Далее", "Next"])
        page.wait_for_timeout(3500)

        # Step 4: Business objectives
        print("\n--- step 4 ---")
        print("URL:", page.url)
        # Need to select at least one objective. Click "Генерация потенциальных клиентов" / "Lead generation"
        for label in ["Генерация потенциальных", "Lead", "Generate leads"]:
            try:
                el = page.locator(f"label:has-text('{label}')").first
                if el.count() > 0 and el.is_visible():
                    el.click()
                    print(f"  selected objective: {label}")
                    break
            except Exception:
                pass
        page.wait_for_timeout(800)
        click_any(page, ["Создать", "Create", "Далее", "Next"])
        page.wait_for_timeout(4000)

        # Step 5: ToS — checkboxes + Accept
        print("\n--- step 5 tos ---")
        print("URL:", page.url)
        # check all checkboxes
        for cb in page.locator("input[type='checkbox']:visible").all():
            try:
                if not cb.is_checked():
                    cb.check(force=True)
                    print("  checked box")
            except Exception:
                pass
        click_any(page, ["Принимаю", "Accept", "I Accept"])
        page.wait_for_timeout(5000)
        print("after accept URL:", page.url)

        # inspect what's visible now
        print("\n--- after provision ---")
        print("URL:", page.url)
        print("--- h1/h2/h3 ---")
        for h in page.locator("h1, h2, h3").all()[:8]:
            try:
                t = h.inner_text().strip()[:80]
                if t:
                    print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
