"""Navigate directly to the Worker settings with custom domains."""
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
        if not page:
            page = ctx.new_page()
        page.bring_to_front()

        # try accept cookies first
        for label in ["Accept All Cookies", "Accept all", "Accept"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible(timeout=1000):
                    btn.first.click()
                    print(f"  accepted cookies: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(1500)

        # go direct to worker settings
        target = "https://dash.cloudflare.com/b1c393c0ca48e9577d6d2ab7f4fa78c9/workers/services/view/ai-consulting-website/production/settings"
        page.goto(target, wait_until="domcontentloaded")
        page.wait_for_timeout(6000)
        print("URL:", page.url)
        for h in page.locator("h1, h2, h3").all()[:10]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass
        # Look for "Domains & Routes" section
        print("--- sections / buttons with 'domain' or 'route' ---")
        for b in page.locator("button:visible, a:visible").all()[:40]:
            try:
                t = b.inner_text().strip()[:80]
                if t and ("domain" in t.lower() or "route" in t.lower() or "Add" in t):
                    print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
