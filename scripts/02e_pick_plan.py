"""Cal.com: click 'Personal' plan card (free), then Continue."""
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
            print("no page"); return
        page.bring_to_front()

        print("URL:", page.url)

        # Look for clickable plan cards — search for text "личного" (personal)
        # and click the parent clickable element
        for strat_name, strat in [
            ("click Personal card", lambda: page.locator("text=Для личного использования").first.click()),
            ("click card by heading", lambda: page.locator("*:has-text('личного использования')").first.click()),
            ("click first radio", lambda: page.locator("input[type='radio']").first.click()),
            ("click Personal by h3", lambda: page.locator("h3:has-text('личного')").first.click()),
        ]:
            try:
                strat()
                print(f"  {strat_name}: OK")
                page.wait_for_timeout(1000)
                break
            except Exception as e:
                print(f"  {strat_name}: {str(e)[:80]}")

        # Now click Continue
        page.wait_for_timeout(1000)
        try:
            page.get_by_role("button", name="Продолжить", exact=False).click(timeout=5000)
            print("  clicked Continue (Продолжить)")
        except Exception as e:
            print(f"  Continue click failed: {str(e)[:80]}")

        page.wait_for_timeout(4000)
        print("URL after:", page.url)


if __name__ == "__main__":
    main()
