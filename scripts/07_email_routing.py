"""Enable Cloudflare Email Routing for setpointaudit.com."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()
        # Go to the domain's email routing page
        page.goto("https://dash.cloudflare.com/b1c393c0ca48e9577d6d2ab7f4fa78c9/setpointaudit.com/email/routing", wait_until="domcontentloaded")
        page.wait_for_timeout(6000)
        print("URL:", page.url)
        for h in page.locator("h1, h2, h3").all()[:10]:
            try:
                t = h.inner_text().strip()[:100]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass
        print("--- buttons ---")
        for b in page.locator("button:visible").all()[:20]:
            try:
                t = b.inner_text().strip()[:80]
                if t and len(t) < 100: print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
