"""Finish Web3Forms onboarding: click Continue with Free, skip rest, grab key."""
from patchright.sync_api import sync_playwright
import re


def get_page(ctx):
    for p in ctx.pages:
        if "web3forms" in p.url:
            return p
    return None


def try_click(page, texts):
    for label in texts:
        try:
            btn = page.get_by_role("button", name=label, exact=False)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                print(f"  clicked: {label}")
                return True
        except Exception:
            pass
        # also try generic text matching
        try:
            btn = page.locator(f"button:has-text('{label}')").first
            if btn.is_visible(timeout=500):
                btn.click()
                print(f"  clicked (text): {label}")
                return True
        except Exception:
            pass
    return False


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page:
            print("no page")
            return

        # Click Continue with Free
        page.wait_for_timeout(1000)
        try_click(page, ["Continue with Free", "Free"])
        page.wait_for_timeout(2500)
        print("after plan:", page.url)

        # Keep clicking anything that looks like progression
        for i in range(10):
            page.wait_for_timeout(1500)
            if try_click(page, ["Continue", "Skip", "Next", "Get Started", "Finish", "Done", "Create Form", "Create Your First Form"]):
                continue
            # check for key
            body = page.locator("body").inner_text()
            match = re.search(r"\b([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\b", body)
            if match:
                print(f"\n>>> WEB3FORMS_KEY={match.group(1)}")
                return
            print(f"[step {i}] url={page.url[:80]} — no button, no key yet")
            # try navigating to /forms or /access-keys explicitly
            if i == 3:
                page.goto("https://app.web3forms.com/forms", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
            elif i == 5:
                page.goto("https://app.web3forms.com/", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

        # final inspection
        print("\n--- final URL:", page.url)
        print("--- BUTTONS ---")
        for b in page.locator("button").all()[:10]:
            try:
                t = b.inner_text().strip()[:60]
                if t:
                    print(f"  btn: {t!r}")
            except Exception:
                pass
        print("--- text dump 800 chars ---")
        print(page.locator("body").inner_text()[:800])


if __name__ == "__main__":
    main()
