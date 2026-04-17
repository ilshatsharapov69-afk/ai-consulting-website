"""Click 'Continue with Google' on Cal.com signup."""
from patchright.sync_api import sync_playwright


def get_page(ctx):
    for p in ctx.pages:
        if "cal.com" in p.url:
            return p
    return None


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page:
            print("no cal.com page"); return
        page.bring_to_front()

        # Click the first button (Google is top)
        buttons = page.locator("button").all()
        for b in buttons[:5]:
            try:
                t = b.inner_text().strip()
                if "Google" in t or "google" in t:
                    b.click()
                    print(f"clicked: {t[:60]!r}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(5000)
        print("URL after:", page.url)
        # wait for onboarding redirect
        for i in range(15):
            page.wait_for_timeout(2000)
            url = page.url
            print(f"[{i*2}s] {url[:100]}")
            if "getting-started" in url or "onboarding" in url or "/event-types" in url or "/bookings" in url or "/settings" in url:
                break


if __name__ == "__main__":
    main()
