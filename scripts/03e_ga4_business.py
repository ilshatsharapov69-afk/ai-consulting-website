"""Fill GA4 business details: industry + size."""
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

        # First check where we are
        page.wait_for_timeout(1500)

        # Print labels around radios to understand
        print("--- radio labels ---")
        labels_text = []
        for label in page.locator("mat-radio-button, label").all()[:20]:
            try:
                t = label.inner_text().strip()[:100]
                if t and len(t) < 150:
                    labels_text.append(t)
                    print(f"  {t!r}")
            except Exception:
                pass

        # Click the first radio in the group (pick "Small business" or first option)
        radios = page.locator("input[type='radio']:visible").all()
        if radios:
            radios[0].check(force=True)
            page.wait_for_timeout(500)
            print(f"  checked first radio (of {len(radios)})")

        # Now handle the dropdown "Выберите нужный вариант"
        try:
            btn = page.get_by_role("combobox", name="Выберите", exact=False)
            if btn.count() > 0:
                btn.first.click()
                page.wait_for_timeout(1500)
                # pick first option
                options = page.locator("mat-option:visible").all()
                if options:
                    options[0].click()
                    print("  picked first dropdown option")
                    page.wait_for_timeout(500)
        except Exception as e:
            print(f"  combobox: {str(e)[:80]}")

        # alternative approach for dropdown
        try:
            btn = page.locator("button:has-text('Выберите')").first
            if btn.is_visible(timeout=1000):
                btn.click()
                page.wait_for_timeout(1500)
                opts = page.locator("mat-option:visible").all()
                if opts:
                    opts[0].click()
                    print("  picked first option (fallback)")
        except Exception:
            pass

        page.wait_for_timeout(800)

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

        # Next step — objectives
        print("\n--- step (objectives?) ---")
        print("URL:", page.url)
        # checkboxes or radios
        for h in page.locator("h1, h2, h3").all()[:4]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass
        print("  checkboxes:")
        for cb in page.locator("input[type='checkbox']:visible").all()[:10]:
            try:
                label = cb.evaluate("el => el.closest('label, mat-checkbox, mat-card')?.innerText?.trim()")
                print(f"    checked={cb.is_checked()} label={(label or '')[:60]!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
