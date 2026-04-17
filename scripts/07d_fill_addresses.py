"""Fill email routing wizard: custom address + destination."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "email/routing" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Fill custom address
        ca = page.locator("input[name='customAddress']").first
        ca.click()
        ca.fill("hello")
        print("  filled customAddress: hello")

        # Fill destination — find second input
        inputs = page.locator("input[type='text']:visible, input[type='email']:visible").all()
        for inp in inputs:
            try:
                n = inp.get_attribute("name") or ""
                if n == "customAddress":
                    continue
                inp.click()
                inp.fill("sherlock753cc@gmail.com")
                print("  filled destination: sherlock753cc@gmail.com")
                break
            except Exception:
                pass

        page.wait_for_timeout(1000)

        # Click Create and continue
        try:
            btn = page.get_by_role("button", name="Create and continue", exact=True)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click(timeout=3000)
                print("  clicked Create and continue")
        except Exception as e:
            print(f"  err: {str(e)[:80]}")

        page.wait_for_timeout(5000)
        print("\nURL:", page.url)
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t and "Cookie" not in t: print(f"  h: {t!r}")
            except Exception:
                pass
        print("--- buttons ---")
        for b in page.locator("main button:visible").all()[:10]:
            try:
                t = b.inner_text().strip()[:60]
                if t: print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
