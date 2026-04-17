"""Click Get started on Email Routing."""
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

        try:
            btn = page.locator("main button:has-text('Get started')").first
            btn.click(timeout=3000)
            print("  clicked Get started")
        except Exception as e:
            print(f"  err: {str(e)[:80]}")
        page.wait_for_timeout(5000)

        print("URL:", page.url)
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass
        print("--- inputs ---")
        for inp in page.locator("input:visible").all()[:10]:
            try:
                t = inp.get_attribute("type") or ""
                ph = inp.get_attribute("placeholder") or ""
                n = inp.get_attribute("name") or inp.get_attribute("aria-label") or ""
                if t in ("hidden",): continue
                print(f"  type={t} n={n[:40]!r} ph={ph[:40]!r}")
            except Exception:
                pass
        print("--- buttons ---")
        for b in page.locator("main button:visible").all()[:15]:
            try:
                t = b.inner_text().strip()[:60]
                if t: print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
