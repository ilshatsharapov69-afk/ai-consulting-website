"""Check if destination email is verified."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()

        # Routes page in detail
        page.goto("https://dash.cloudflare.com/b1c393c0ca48e9577d6d2ab7f4fa78c9/setpointaudit.com/email/routing/routes",
                  wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        # Full body dump filtered
        print("URL:", page.url)
        body = page.locator("body").inner_text()
        # show all non-navigation lines
        in_main = False
        for line in body.split("\n"):
            s = line.strip()
            if "Email Routing" in s and "summary" in s.lower():
                in_main = True
            if in_main and s and len(s) < 150:
                # skip clear navigation items
                if s in ("Overview", "Routes", "Destination addresses", "Settings", "Analytics & logs", "DNS", "Email", "SSL/TLS", "Security", "Speed", "Caching", "Rules", "Traffic"):
                    continue
                print(f"  {s!r}")

        # Destination addresses tab
        print("\n=== Destinations ===")
        try:
            tab = page.locator("a:has-text('Destination addresses'), button:has-text('Destination addresses')").first
            if tab.is_visible(timeout=1500):
                tab.click()
                page.wait_for_timeout(3500)
                body = page.locator("body").inner_text()
                for line in body.split("\n"):
                    s = line.strip()
                    if ("@" in s or any(k in s.lower() for k in ["verified", "unverified", "pending", "not verified", "delivered"])) and len(s) < 200:
                        print(f"  {s!r}")
        except Exception as e:
            print(f"  err: {str(e)[:80]}")


if __name__ == "__main__":
    main()
