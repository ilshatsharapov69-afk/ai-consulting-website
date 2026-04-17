"""Verify custom domain status on Cloudflare."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "cloudflare.com" in p.url and "settings" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        page.reload(wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        body = page.locator("body").inner_text()
        # find lines around setpointaudit
        for line in body.split("\n"):
            s = line.strip()
            if s and ("setpointaudit" in s.lower() or "Active" in s or "Pending" in s or "certificate" in s.lower()):
                if len(s) < 150:
                    print(f"  {s!r}")


if __name__ == "__main__":
    main()
