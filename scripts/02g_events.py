"""Close welcome modal, find event URLs."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
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

        # Close the modal
        page.wait_for_timeout(1500)
        for label in ["Got it", "Close", "Понятно", "Закрыть", "Let's go", "Start", "Get started"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=2000)
                    print(f"  closed modal via: {label}")
                    break
            except Exception:
                pass
        # also try Escape
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)

        # go to clean event-types page
        page.goto("https://app.cal.com/event-types", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        print("URL:", page.url)

        # find event links — they're usually /{username}/{slug}
        print("--- all non-app links ---")
        seen = set()
        for a in page.locator("a").all():
            try:
                href = a.get_attribute("href") or ""
                if href.startswith("/") and href not in seen:
                    seen.add(href)
                    txt = a.inner_text().strip()[:40]
                    # filter: look for /ilshatai/ or /username/event
                    if href.count("/") == 2 and not any(x in href for x in ["/settings", "/apps", "/event-types", "/bookings", "/availability", "/workflows", "/teams", "/insights", "/app-store", "/workspace", "/routing"]):
                        print(f"  {href!r} — {txt!r}")
            except Exception:
                pass
        print("\n--- event-type links (contains /event-types/) ---")
        for a in page.locator("a[href*='/event-types/']").all():
            try:
                href = a.get_attribute("href") or ""
                txt = a.inner_text().strip()[:60].replace("\n", " | ")
                print(f"  {href[:80]} — {txt}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
