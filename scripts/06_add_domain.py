"""Add setpointaudit.com as custom domain to Cloudflare Workers."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()
        # Navigate to Workers settings → Domains & Routes
        page.goto("https://dash.cloudflare.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        print("URL:", page.url)
        # Find the account link / Workers & Pages link
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
