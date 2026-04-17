"""Inspect full modal/dialog state after clicking Add."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "cloudflare.com" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Check if dialog/modal/drawer opened
        print("URL:", page.url)
        print("--- dialog/modal headings ---")
        for sel in ["[role='dialog'] h1, [role='dialog'] h2, [role='dialog'] h3",
                    "[aria-modal='true'] h1, [aria-modal='true'] h2, [aria-modal='true'] h3",
                    ".modal h1, .modal h2, .modal h3",
                    "h1, h2, h3"]:
            els = page.locator(sel).all()
            for e in els[:10]:
                try:
                    t = e.inner_text().strip()[:80]
                    if t and len(t) < 120:
                        print(f"  [{sel[:30]}] {t!r}")
                except Exception:
                    pass
            if els: break
        # All inputs
        print("\n--- all visible inputs ---")
        for inp in page.locator("input:visible").all()[:15]:
            try:
                t = inp.get_attribute("type") or ""
                ph = inp.get_attribute("placeholder") or ""
                n = inp.get_attribute("name") or inp.get_attribute("aria-label") or ""
                v = inp.input_value() if t not in ("checkbox", "radio", "hidden") else ""
                if t in ("hidden",): continue
                print(f"  type={t} n={n[:40]!r} ph={ph[:40]!r} v={v[:40]!r}")
            except Exception:
                pass

        # Look for full buttons
        print("\n--- visible buttons (all) ---")
        for b in page.locator("button:visible").all()[:25]:
            try:
                t = b.inner_text().strip()[:60]
                if t: print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
