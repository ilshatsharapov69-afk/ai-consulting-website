"""Wait longer for Turnstile to resolve, then print page state."""
from patchright.sync_api import sync_playwright
import time


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        # find the active web3forms page
        target = None
        for p in ctx.pages:
            if "web3forms" in p.url:
                target = p
                break
        if not target:
            print("no web3forms page")
            return

        for i in range(12):
            time.sleep(2)
            url = target.url
            title = target.title()
            print(f"[{i*2}s] url={url[:80]} title={title[:60]}")
            if "login" in url and "moment" not in title.lower() and "одну" not in title.lower():
                # past challenge
                print("--- DOM ready, looking for Google button ---")
                buttons = target.locator("button, a[role='button']").all()
                for b in buttons[:15]:
                    try:
                        txt = b.inner_text().strip()[:50]
                        if txt:
                            print(f"  btn: {txt!r}")
                    except Exception:
                        pass
                break


if __name__ == "__main__":
    main()
