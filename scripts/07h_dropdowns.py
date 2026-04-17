"""Find and set Action dropdown, then destination."""
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

        # Look for select / combobox dropdowns
        print("--- dropdowns/comboboxes/selects ---")
        for sel in ["select:visible", "button[role='combobox']:visible", "div[role='combobox']:visible", "[role='listbox']"]:
            els = page.locator(sel).all()
            for e in els[:5]:
                try:
                    t = e.inner_text().strip()[:80]
                    aria = e.get_attribute("aria-label") or ""
                    name = e.get_attribute("name") or ""
                    print(f"  [{sel[:20]}] aria={aria[:30]!r} name={name[:20]!r} text={t[:40]!r}")
                except Exception:
                    pass

        # Also look for any element with aria-haspopup
        print("\n--- aria-haspopup elements ---")
        for e in page.locator("[aria-haspopup='listbox'], [aria-haspopup='true']").all()[:10]:
            try:
                t = e.inner_text().strip()[:80]
                if t: print(f"  {t!r}")
            except Exception:
                pass

        # Look for any labeled field
        print("\n--- labels near Required errors ---")
        for lab in page.locator("label:visible").all()[:10]:
            try:
                t = lab.inner_text().strip()[:100]
                if t: print(f"  label: {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
