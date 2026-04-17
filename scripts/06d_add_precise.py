"""Click the Add button specifically in Domains & Routes section."""
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

        # Close any open menu first
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        # Find the Domains & Routes section card and click Add within it
        section = page.locator("section:has(h2:text('Domains & Routes')), div:has(> h2:text('Domains & Routes')), div:has(h3:text('Domains & Routes'))").first
        if section.count() > 0:
            print("  found Domains & Routes section")
            # Click Add inside it
            try:
                add_btn = section.locator("button:has-text('Add')").first
                add_btn.scroll_into_view_if_needed()
                add_btn.click(timeout=5000)
                print("  clicked Add in Domains & Routes section")
                page.wait_for_timeout(2500)
            except Exception as e:
                print(f"  click failed: {str(e)[:80]}")
        else:
            print("  section not found, trying via Section heading")
            # Alt: find heading, go to parent container, find Add
            h = page.locator("h2:has-text('Domains & Routes'), h3:has-text('Domains & Routes')").first
            if h.count() > 0:
                h.scroll_into_view_if_needed()
                # try nearby button
                try:
                    # get parent container
                    parent = h.locator("xpath=ancestor::*[button][1]")
                    if parent.count() > 0:
                        add = parent.locator("button:has-text('Add')").first
                        add.click()
                        print("  clicked via ancestor Add")
                        page.wait_for_timeout(2500)
                except Exception as e:
                    print(f"  ancestor approach failed: {str(e)[:80]}")

        # Now look for menu items
        print("\n--- menu/button items after click ---")
        for sel in ["[role='menuitem']:visible", "[role='option']:visible", "button:visible"]:
            try:
                items = page.locator(sel).all()
                for item in items[:20]:
                    try:
                        t = item.inner_text().strip()[:60]
                        if t and any(k in t for k in ["Custom Domain", "Domain", "Route", "Subdomain", "workers.dev"]):
                            print(f"  [{sel[:20]}] {t!r}")
                    except Exception:
                        pass
            except Exception:
                pass


if __name__ == "__main__":
    main()
