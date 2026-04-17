"""Fill destination email with all inputs."""
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

        # Fill ALL visible inputs except customAddress
        for inp in page.locator("input:visible").all():
            try:
                t = inp.get_attribute("type") or ""
                n = inp.get_attribute("name") or ""
                if t in ("hidden", "checkbox", "radio", "submit", "button"):
                    continue
                if n == "customAddress":
                    continue
                # This is likely our destination input
                v = inp.input_value()
                if not v:
                    inp.scroll_into_view_if_needed()
                    inp.click()
                    page.wait_for_timeout(300)
                    inp.type("sherlock753cc@gmail.com", delay=30)
                    print(f"  typed into name={n!r} type={t!r}")
                    break
            except Exception as e:
                print(f"  input err: {str(e)[:60]}")

        page.wait_for_timeout(1500)

        # Verify
        print("\n--- inputs after fill ---")
        for inp in page.locator("input:visible").all()[:5]:
            try:
                n = inp.get_attribute("name") or ""
                t = inp.get_attribute("type") or ""
                if t in ("hidden", "checkbox", "radio"): continue
                print(f"  n={n!r} t={t!r} v={inp.input_value()!r}")
            except Exception:
                pass

        # Click Create and continue
        try:
            btn = page.locator("button:has-text('Create and continue')").first
            btn.click(timeout=5000)
            print("\n  clicked Create and continue")
        except Exception as e:
            print(f"  click err: {str(e)[:80]}")

        page.wait_for_timeout(6000)
        print("\nURL:", page.url)
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t and "Cookie" not in t: print(f"  h: {t!r}")
            except Exception:
                pass
        print("--- main buttons ---")
        for b in page.locator("main button:visible").all()[:10]:
            try:
                t = b.inner_text().strip()[:60]
                if t: print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
