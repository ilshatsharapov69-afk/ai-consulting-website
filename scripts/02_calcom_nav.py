"""Navigate to Cal.com signup — user clicks Sign in with Google."""
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.bring_to_front()
        page.goto("https://cal.com/signup", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        print("URL:", page.url)
        print("TITLE:", page.title())
        print("--- buttons ---")
        for b in page.locator("button, a[role='button']").all()[:10]:
            try:
                t = b.inner_text().strip()[:60]
                if t:
                    print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
