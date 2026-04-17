"""Inspect current web3forms page."""
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        target = None
        for p in ctx.pages:
            if "web3forms" in p.url:
                target = p
                break
        if not target:
            print("no web3forms page")
            return
        print("URL:", target.url)
        print("TITLE:", target.title())
        print("--- BUTTONS ---")
        for b in target.locator("button").all()[:15]:
            try:
                t = b.inner_text().strip()[:60]
                if t:
                    print(f"  btn: {t!r}")
            except Exception:
                pass
        print("--- LINKS ---")
        for a in target.locator("a").all()[:20]:
            try:
                t = a.inner_text().strip()[:50]
                h = a.get_attribute("href") or ""
                if t:
                    print(f"  {t!r} -> {h[:60]}")
            except Exception:
                pass
        print("--- H1/H2 ---")
        for h in target.locator("h1, h2").all()[:5]:
            try:
                print("  ", h.inner_text().strip()[:80])
            except Exception:
                pass


if __name__ == "__main__":
    main()
