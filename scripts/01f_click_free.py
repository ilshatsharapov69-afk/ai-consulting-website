"""Click 'Continue with Free' using multiple strategies."""
from patchright.sync_api import sync_playwright
import re


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
            print("no page"); return

        # inspect all clickable elements with "Free" text
        print("=== elements containing 'Free' ===")
        els = page.locator("*:has-text('Continue with Free')").all()
        for i, e in enumerate(els[:10]):
            try:
                tag = e.evaluate("el => el.tagName")
                text = (e.inner_text() or "")[:40].replace("\n", " ")
                print(f"  [{i}] <{tag}> {text!r}")
            except Exception as ex:
                print(f"  [{i}] err {ex}")

        # try clicking the innermost one (last in DOM tree usually)
        print("\n=== trying clicks ===")
        strategies = [
            lambda: page.get_by_text("Continue with Free", exact=True).click(),
            lambda: page.locator("button:has-text('Continue with Free')").first.click(),
            lambda: page.locator("a:has-text('Continue with Free')").first.click(),
            lambda: page.locator("[class*='plan']:has-text('Free') button").first.click(),
            lambda: page.locator("text=Continue with Free").click(),
        ]
        for i, s in enumerate(strategies):
            try:
                s()
                print(f"  strategy {i} clicked")
                page.wait_for_timeout(3000)
                print(f"  after url: {page.url[:100]}")
                if "onboarding/welcome" not in page.url:
                    break
            except Exception as e:
                print(f"  strategy {i} failed: {str(e)[:100]}")

        page.wait_for_timeout(2000)
        print(f"\n=== final URL: {page.url[:100]} ===")
        body = page.locator("body").inner_text()
        match = re.search(r"\b([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\b", body)
        if match:
            print(f">>> WEB3FORMS_KEY={match.group(1)}")
        else:
            print("still no key. body[:400]:")
            print(body[:400])


if __name__ == "__main__":
    main()
