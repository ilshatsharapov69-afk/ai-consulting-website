"""Dismiss cookie banner, reopen domain dialog, click Custom Domain option."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "cloudflare.com" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Cookie banner dismiss — look for Accept buttons
        print("--- cookie banner buttons ---")
        for b in page.locator("button:visible").all()[:30]:
            try:
                t = b.inner_text().strip()[:60]
                if any(k in t.lower() for k in ["accept all", "accept", "confirm", "save settings", "reject all"]):
                    print(f"  {t!r}")
            except Exception:
                pass

        for label in ["Accept All Cookies", "Accept All", "Confirm My Choices", "Accept", "Reject All"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible(timeout=800):
                    btn.first.click(timeout=3000)
                    print(f"  dismissed cookies via: {label}")
                    break
            except Exception:
                pass
        page.wait_for_timeout(2000)

        # Press Escape to close any menu/modal
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        # Reload page
        page.reload(wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
        print("\n  page reloaded")
        print("URL:", page.url)

        # Find Domains & Routes section
        heading = page.locator("h2:has-text('Domains & Routes')").first
        heading.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        # Click Add nearby (first in that section)
        section = page.locator("section:has(h2:has-text('Domains & Routes')), div:has(> h2:has-text('Domains & Routes'))").first
        add_btn = section.locator("button:has-text('Add')").first
        add_btn.click()
        print("  clicked Add")
        page.wait_for_timeout(2500)

        # Look for dialog content with Custom Domain option
        print("\n--- all visible buttons in dialog area ---")
        for b in page.locator("[role='dialog'] button, [role='menu'] button, button[role='menuitem']").all()[:15]:
            try:
                t = b.inner_text().strip()[:80]
                if t: print(f"  {t!r}")
            except Exception:
                pass
        print("\n--- any element containing Custom Domain ---")
        for e in page.locator(":visible:text-matches('Custom Domain', 'i')").all()[:5]:
            try:
                tag = e.evaluate("el => el.tagName")
                t = e.inner_text().strip()[:60]
                print(f"  <{tag}> {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
