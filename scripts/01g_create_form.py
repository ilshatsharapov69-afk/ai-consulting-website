"""Fill Create Form onboarding step, extract API key from resulting dashboard."""
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
        print("URL:", page.url)

        # Fill the two inputs
        inputs = page.locator("input[type='text'], input:not([type])").all()
        print(f"found {len(inputs)} text inputs")
        if len(inputs) >= 2:
            inputs[0].fill("Contact Form")
            print("  form name filled")
            inputs[1].fill("ai-consulting-website.sherlock753cc.workers.dev")
            print("  domain filled")
        elif len(inputs) == 1:
            inputs[0].fill("Contact Form")
            print("  only 1 input, filled")

        page.wait_for_timeout(500)

        # Click Create Form
        clicked = False
        for strat in [
            lambda: page.get_by_role("button", name="Create Form").click(timeout=5000),
            lambda: page.locator("button:has-text('Create Form')").first.click(timeout=5000),
            lambda: page.locator("text=Create Form").click(timeout=5000),
        ]:
            try:
                strat()
                clicked = True
                print("  clicked Create Form")
                break
            except Exception as e:
                print(f"  strat failed: {str(e)[:80]}")

        if not clicked:
            print("\n--- couldn't click Create Form. Inspecting buttons ---")
            for b in page.locator("button").all()[:10]:
                try:
                    print("  btn:", b.inner_text().strip()[:50])
                except Exception:
                    pass
            return

        # Wait for redirect to dashboard
        page.wait_for_timeout(4000)
        print("after create, URL:", page.url)

        # Search for access key
        for attempt in range(6):
            body = page.locator("body").inner_text()
            match = re.search(r"\b([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\b", body)
            if match:
                print(f"\n>>> WEB3FORMS_KEY={match.group(1)}")
                return
            # maybe need to click into the form to see key
            page.wait_for_timeout(2000)
            # try going to /forms
            if attempt == 2:
                page.goto("https://app.web3forms.com/forms", wait_until="domcontentloaded")
                page.wait_for_timeout(2500)
                # click first form row
                try:
                    first = page.locator("a[href*='/forms/'], tr").first
                    first.click(timeout=2000)
                    page.wait_for_timeout(2500)
                except Exception:
                    pass

        print("\n--- final URL:", page.url)
        print("--- body text 800 chars ---")
        print(page.locator("body").inner_text()[:800])


if __name__ == "__main__":
    main()
