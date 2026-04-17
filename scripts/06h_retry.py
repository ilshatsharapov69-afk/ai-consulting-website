"""Retry: fill hostname input with setpointaudit.com and submit."""
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

        # Fill hostname directly
        inp = page.locator("input[name='hostname']").first
        if inp.count() > 0 and inp.is_visible():
            inp.click()
            inp.fill("setpointaudit.com")
            print("  filled hostname=setpointaudit.com")
        else:
            print("  hostname input not found/visible — re-opening dialog")
            # Re-open dialog
            try:
                section = page.locator("section:has(h2:has-text('Domains & Routes')), div:has(> h2:has-text('Domains & Routes'))").first
                add_btn = section.locator("button:has-text('Add')").first
                add_btn.click()
                page.wait_for_timeout(2000)
                page.locator("button:has-text('Custom domain')").first.click()
                page.wait_for_timeout(2000)
                inp = page.locator("input[name='hostname']").first
                inp.click()
                inp.fill("setpointaudit.com")
                print("  filled hostname after reopen")
            except Exception as e:
                print(f"  reopen err: {str(e)[:80]}")
                return

        page.wait_for_timeout(1500)

        # Find submit button
        print("\n--- all visible buttons with text ---")
        for b in page.locator("button:visible").all():
            try:
                t = b.inner_text().strip()
                if t and len(t) < 40 and any(k in t.lower() for k in ["add", "save", "submit", "connect", "domain"]):
                    print(f"  {t!r}")
            except Exception:
                pass

        # Click buttons with typical submit labels
        for label in ["Add Custom Domain", "Add domain", "Add Domain", "Connect", "Save"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                count = btn.count()
                if count > 0:
                    # click the last one (dialog submit is usually at bottom)
                    btn.nth(count - 1).click(timeout=3000)
                    print(f"  clicked (last): {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(6000)
        print("\n--- after submit ---")
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            if "setpointaudit" in line.lower() and len(line) < 120:
                print(f"  line: {line.strip()!r}")


if __name__ == "__main__":
    main()
