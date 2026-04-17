"""Check full Email Routing status + destination verification + MX records."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()

        # 1. Overview page
        page.goto("https://dash.cloudflare.com/b1c393c0ca48e9577d6d2ab7f4fa78c9/setpointaudit.com/email/routing/overview",
                  wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
        print("=" * 40)
        print("OVERVIEW:")
        print("URL:", page.url)
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            s = line.strip()
            if any(k in s for k in ["Email Routing", "enabled", "Enabled", "disabled", "Active", "Pending", "pending", "verified", "not verified", "verification", "Required", "Missing", "Success"]):
                if 5 < len(s) < 150:
                    print(f"  {s!r}")

        # 2. Routes page
        page.goto("https://dash.cloudflare.com/b1c393c0ca48e9577d6d2ab7f4fa78c9/setpointaudit.com/email/routing/routes",
                  wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        print("\n" + "=" * 40)
        print("ROUTES:")
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            s = line.strip()
            if any(k in s.lower() for k in ["hello", "setpointaudit", "destination", "verified", "@gmail"]):
                if 3 < len(s) < 200:
                    print(f"  {s!r}")

        # 3. Destination addresses page (might be separate)
        page.goto("https://dash.cloudflare.com/b1c393c0ca48e9577d6d2ab7f4fa78c9/setpointaudit.com/email/routing/destination-addresses",
                  wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        print("\n" + "=" * 40)
        print("DESTINATION ADDRESSES:")
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            s = line.strip()
            if "@" in s and 5 < len(s) < 150:
                print(f"  {s!r}")
            elif any(k in s.lower() for k in ["verified", "not verified", "pending", "verification"]) and len(s) < 150:
                print(f"  {s!r}")

        # 4. DNS records for setpointaudit
        page.goto("https://dash.cloudflare.com/b1c393c0ca48e9577d6d2ab7f4fa78c9/setpointaudit.com/dns/records",
                  wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
        print("\n" + "=" * 40)
        print("DNS RECORDS:")
        body = page.locator("body").inner_text()
        # print only MX and mail-related TXT
        for line in body.split("\n"):
            s = line.strip()
            if s.startswith("MX") or "route" in s.lower() and "mx" in s.lower() or "v=spf" in s.lower() or "domainkey" in s.lower():
                if len(s) < 200:
                    print(f"  {s!r}")


if __name__ == "__main__":
    main()
