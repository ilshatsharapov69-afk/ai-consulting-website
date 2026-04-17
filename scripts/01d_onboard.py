"""Click through Web3Forms onboarding, then extract first Access Key."""
from patchright.sync_api import sync_playwright
import re, time


def get_page(ctx):
    for p in ctx.pages:
        if "web3forms" in p.url:
            return p
    return None


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page:
            print("no page")
            return

        for step in range(8):
            page.wait_for_timeout(1500)
            url = page.url
            title = page.title()
            print(f"[step {step}] url={url[:80]}")

            # try click Continue / Skip / Finish / Get started
            clicked = False
            for label in ["Continue", "Skip", "Get Started", "Finish", "Done", "Next"]:
                try:
                    btn = page.get_by_role("button", name=label, exact=False)
                    if btn.count() > 0 and btn.first.is_visible():
                        btn.first.click()
                        print(f"  clicked: {label}")
                        clicked = True
                        break
                except Exception:
                    pass

            if not clicked:
                # check if we're on dashboard with API key
                body = page.locator("body").inner_text()
                match = re.search(r"\b([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\b", body)
                if match:
                    print(f"\n>>> WEB3FORMS_KEY={match.group(1)}")
                    return
                print("  no button; URL is stable")
                break

        # final key search
        page.wait_for_timeout(2000)
        body = page.locator("body").inner_text()
        match = re.search(r"\b([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\b", body)
        if match:
            print(f"\n>>> WEB3FORMS_KEY={match.group(1)}")
        else:
            print("\n--- no key; dumping visible text (500 chars) ---")
            print(body[:500])


if __name__ == "__main__":
    main()
