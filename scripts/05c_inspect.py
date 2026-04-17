"""Inspect schedule editor form fields."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "availability/" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Print day/time rows
        print("--- switches (checkboxes for days) ---")
        for cb in page.locator("input[type='checkbox']:visible, button[role='switch']:visible").all()[:15]:
            try:
                aria = cb.get_attribute("aria-label") or ""
                name = cb.get_attribute("name") or ""
                checked = cb.is_checked() if "checkbox" in (cb.get_attribute("type") or "") else cb.get_attribute("aria-checked")
                print(f"  aria={aria[:30]!r} name={name[:30]!r} checked={checked}")
            except Exception:
                pass

        print("\n--- time inputs (first 20) ---")
        for inp in page.locator("input:visible").all()[:20]:
            try:
                t = inp.get_attribute("type") or ""
                if t in ("checkbox", "radio", "hidden", "submit"): continue
                n = inp.get_attribute("name") or inp.get_attribute("aria-label") or ""
                v = inp.input_value()
                ph = inp.get_attribute("placeholder") or ""
                print(f"  type={t} n={n[:40]!r} v={v[:20]!r} ph={ph[:20]!r}")
            except Exception:
                pass

        print("\n--- buttons ---")
        for b in page.locator("button:visible").all()[:15]:
            try:
                t = b.inner_text().strip()[:40]
                aria = b.get_attribute("aria-label") or ""
                if t or aria: print(f"  t={t!r} aria={aria[:40]!r}")
            except Exception:
                pass

        # Timezone
        print("\n--- timezone ---")
        tz_btn = page.locator("button:has-text('Europe/London'), button:has-text('Etc/GMT')").first
        try:
            if tz_btn.is_visible(timeout=1000):
                print("  timezone button visible")
        except Exception:
            pass


if __name__ == "__main__":
    main()
