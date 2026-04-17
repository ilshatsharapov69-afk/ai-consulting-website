"""Navigate the attached browser to Web3Forms app (user clicks Sign in with Google)."""
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.bring_to_front()
        page.goto("https://app.web3forms.com/login", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        print("URL:", page.url)
        print("TITLE:", page.title())


if __name__ == "__main__":
    main()
