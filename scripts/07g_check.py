"""Check state - maybe error showing; try Tab + Enter flow."""
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

        # Show any error/alert text
        print("--- alerts / errors ---")
        for sel in ["[role='alert']", ".error", "[class*='error']:visible", "[class*='warning']:visible"]:
            for e in page.locator(sel).all()[:5]:
                try:
                    t = e.inner_text().strip()[:100]
                    if t and "cookie" not in t.lower(): print(f"  [{sel}] {t!r}")
                except Exception:
                    pass

        # Find destination input, click, and press Tab to blur — might trigger validation
        inp = None
        for i in page.locator("input:visible").all():
            try:
                if (i.get_attribute("name") or "") != "customAddress":
                    t = i.get_attribute("type") or ""
                    if t not in ("hidden","checkbox","radio","submit","button"):
                        inp = i
                        break
            except Exception:
                pass

        if inp:
            inp.click()
            page.wait_for_timeout(300)
            inp.press("End")
            print("  focused destination input")
            # tab out
            inp.press("Tab")
            page.wait_for_timeout(1000)
            print("  tabbed out")

        # check again for errors
        print("\n--- body text for validation signals ---")
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            s = line.strip()
            if any(k in s.lower() for k in ["required", "invalid", "verify", "verification", "confirm"]) and len(s) < 200:
                print(f"  {s!r}")

        # Click submit again
        try:
            btn = page.locator("button:has-text('Create and continue')").first
            btn.click()
            print("\n  clicked Create and continue")
        except Exception as e:
            print(f"  err: {str(e)[:80]}")
        page.wait_for_timeout(6000)

        print("\n--- final state ---")
        print("URL:", page.url)
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
