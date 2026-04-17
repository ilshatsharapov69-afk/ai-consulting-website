"""Confirm username change dialog."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "cal.com" in p.url and "profile" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Inspect dialog
        print("--- dialog content ---")
        for sel in ["[role='dialog'] button:visible", "[role='alertdialog'] button:visible", ".modal button:visible"]:
            for b in page.locator(sel).all()[:10]:
                try:
                    t = b.inner_text().strip()[:60]
                    if t: print(f"  [{sel[:30]}] {t!r}")
                except Exception:
                    pass

        # Try multiple confirmation labels
        for label in ["Update username", "Confirm", "Save", "Change", "Yes", "I'm sure", "Update", "Continue"]:
            try:
                btn = page.locator(f"[role='dialog'] button:has-text('{label}'), [role='alertdialog'] button:has-text('{label}')").first
                if btn.count() > 0 and btn.is_visible(timeout=1000):
                    btn.click(timeout=3000)
                    print(f"  clicked in dialog: {label}")
                    page.wait_for_timeout(4000)
                    break
            except Exception:
                pass

        page.wait_for_timeout(5000)

        # Check for success
        print("\n--- state after confirm ---")
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass

        # Verify public URL
        page2 = ctx.new_page()
        page2.goto("https://cal.com/ilshatai/audit", wait_until="domcontentloaded")
        page2.wait_for_timeout(3000)
        print(f"\n  /ilshatai/audit title: {page2.title()[:80]!r}")
        print(f"  URL: {page2.url}")


if __name__ == "__main__":
    main()
