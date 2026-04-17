"""Retry submit with proper click flow."""
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

        # Verify fields still filled
        ca = page.locator("input[name='customAddress']").first
        print("  customAddress value:", ca.input_value())
        # Other inputs
        for inp in page.locator("input:visible").all()[:5]:
            try:
                t = inp.get_attribute("type") or ""
                n = inp.get_attribute("name") or ""
                v = inp.input_value() if t not in ("checkbox","radio","hidden") else ""
                if t not in ("hidden","checkbox","radio"):
                    print(f"  input n={n!r} v={v!r}")
            except Exception:
                pass

        # Look for any error/validation
        print("\n--- error-like text ---")
        for e in page.locator("[role='alert'], .error, .alert, [class*='error']").all()[:5]:
            try:
                t = e.inner_text().strip()[:150]
                if t: print(f"  {t!r}")
            except Exception:
                pass

        # Try click via force
        print("\n--- click Create and continue via force ---")
        try:
            btn = page.locator("button:has-text('Create and continue')").first
            # focus first
            btn.focus()
            page.wait_for_timeout(500)
            btn.click(timeout=5000, force=True)
            print("  force-clicked")
        except Exception as e:
            print(f"  err: {str(e)[:100]}")

        page.wait_for_timeout(5000)
        # Re-check URL / heading
        print("\nURL:", page.url)
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t and "Cookie" not in t: print(f"  h: {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
