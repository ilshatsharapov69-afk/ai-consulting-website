"""Click Add → Custom Domain, fill setpointaudit.com."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "cloudflare.com" in p.url and "settings" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Scroll to Domains & Routes and click Add
        try:
            heading = page.locator("h2:has-text('Domains & Routes'), h3:has-text('Domains & Routes')").first
            heading.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
        except Exception:
            pass

        # Click Add button near Domains & Routes
        print("--- buttons near domains section ---")
        # Look for + Add button
        for sel in ["button:has-text('Add')", "button:has(svg):has-text('Add')"]:
            try:
                btns = page.locator(sel).all()
                for b in btns[:5]:
                    t = b.inner_text().strip()
                    print(f"  btn: {t!r}")
            except Exception:
                pass

        # Click first "Add" button (for Domains & Routes)
        try:
            add_btn = page.get_by_role("button", name="Add", exact=True)
            if add_btn.count() > 0:
                add_btn.first.click()
                print("  clicked Add")
                page.wait_for_timeout(2500)
        except Exception as e:
            print(f"  add click err: {str(e)[:80]}")

        # Menu appears with options: Custom Domain, Route, Workers.dev subdomain
        print("\n--- menu options ---")
        for b in page.locator("button:visible, a:visible, li:visible").all()[:20]:
            try:
                t = b.inner_text().strip()[:80]
                if t and ("Custom" in t or "Domain" in t or "Route" in t or "Workers.dev" in t):
                    print(f"  {t!r}")
            except Exception:
                pass

        # Click Custom Domain
        for label in ["Custom Domain", "Custom domain"]:
            try:
                el = page.locator(f"button:has-text('{label}'), a:has-text('{label}'), li:has-text('{label}')").first
                if el.is_visible(timeout=1500):
                    el.click()
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(2500)
        print("\n--- modal state ---")
        print("URL:", page.url)
        for inp in page.locator("input:visible").all()[:5]:
            try:
                t = inp.get_attribute("type") or ""
                ph = inp.get_attribute("placeholder") or ""
                if t in ("hidden",): continue
                print(f"  input type={t} ph={ph[:40]!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
