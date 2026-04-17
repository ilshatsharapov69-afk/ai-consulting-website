"""Find and set Action field near label 'Action'."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "email/routing" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Click on Action field (usually adjacent element)
        action_label = page.locator("label:has-text('Action')").first
        action_label.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        # Find the clickable element right after Action label
        # Use xpath to get following sibling or nearby field
        try:
            # The field might be a button next to the label or inside same container
            container = action_label.locator("xpath=..")
            clickable = container.locator("button, [role='button'], [role='combobox'], div[tabindex]").first
            if clickable.count() > 0:
                clickable.click()
                print("  clicked Action dropdown")
                page.wait_for_timeout(1500)
        except Exception as e:
            print(f"  err: {str(e)[:80]}")

        # Look for options (menu items)
        print("--- menu options ---")
        for sel in ["[role='menuitem']:visible", "[role='option']:visible", "li:visible"]:
            opts = page.locator(sel).all()
            for o in opts[:8]:
                try:
                    t = o.inner_text().strip()[:80]
                    if t and len(t) < 120:
                        print(f"  [{sel[:25]}] {t!r}")
                except Exception:
                    pass

        # Click "Send to an email" option
        for label in ["Send to an email", "Send to email", "Forward to email"]:
            try:
                el = page.locator(f"[role='option']:has-text('{label}'), [role='menuitem']:has-text('{label}'), li:has-text('{label}')").first
                if el.is_visible(timeout=1500):
                    el.click()
                    print(f"  picked: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(1500)

        # Now check state
        print("\n--- inputs state ---")
        for inp in page.locator("input:visible").all()[:5]:
            try:
                t = inp.get_attribute("type") or ""
                n = inp.get_attribute("name") or ""
                if t in ("hidden", "checkbox", "radio"): continue
                print(f"  n={n!r} t={t!r} v={inp.input_value()!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
