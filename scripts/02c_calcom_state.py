"""Check Cal.com state and handle onboarding."""
from patchright.sync_api import sync_playwright


def get_calcom_page(ctx):
    for p in ctx.pages:
        if "cal.com" in p.url:
            return p
    return None


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_calcom_page(ctx)
        if not page:
            print("no cal.com page — list all pages:")
            for p in ctx.pages:
                print(" -", p.url[:80])
            return
        page.bring_to_front()
        print("URL:", page.url)
        print("TITLE:", page.title())
        print("--- inputs ---")
        for inp in page.locator("input").all()[:10]:
            try:
                t = inp.get_attribute("type") or ""
                n = inp.get_attribute("name") or ""
                ph = inp.get_attribute("placeholder") or ""
                v = inp.input_value() if t not in ("checkbox", "radio", "hidden") else ""
                visible = inp.is_visible()
                if visible:
                    print(f"  type={t} name={n} placeholder={ph!r} value={v!r}")
            except Exception:
                pass
        print("--- buttons ---")
        for b in page.locator("button").all()[:15]:
            try:
                t = b.inner_text().strip()[:50]
                if t and b.is_visible():
                    print(f"  {t!r}")
            except Exception:
                pass
        print("--- body text 500 chars ---")
        print(page.locator("body").inner_text()[:500])


if __name__ == "__main__":
    main()
