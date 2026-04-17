"""Click 'Custom domain' option, fill setpointaudit.com, submit."""
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

        # Click "Custom domain" button
        try:
            btn = page.locator("button:has-text('Custom domain')").first
            btn.click(timeout=5000)
            print("  clicked Custom domain")
        except Exception as e:
            print(f"  err: {str(e)[:80]}")

        page.wait_for_timeout(3500)

        # Now there should be a domain input
        print("\n--- inputs after selecting Custom Domain ---")
        for inp in page.locator("input:visible").all()[:8]:
            try:
                t = inp.get_attribute("type") or ""
                ph = inp.get_attribute("placeholder") or ""
                n = inp.get_attribute("name") or inp.get_attribute("aria-label") or ""
                if t in ("hidden",): continue
                print(f"  type={t} n={n[:40]!r} ph={ph[:40]!r}")
            except Exception:
                pass

        # Fill domain
        inp = page.locator("input[type='text']:visible, input[placeholder*='example' i]:visible, input[name='domain' i]:visible").first
        if inp.count() > 0:
            inp.click()
            inp.fill("setpointaudit.com")
            print("  filled: setpointaudit.com")
            page.wait_for_timeout(1000)

        # Click Add Domain / Submit
        for label in ["Add Custom Domain", "Add domain", "Add", "Save"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0:
                    # find the last visible one (typically the submit in dialog)
                    for b in btn.all():
                        if b.is_visible():
                            b.click()
                            print(f"  clicked: {label}")
                            break
                    else:
                        continue
                    break
            except Exception:
                pass

        page.wait_for_timeout(6000)
        print("\n--- after submit ---")
        print("URL:", page.url)
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            if "setpointaudit" in line.lower() and len(line) < 100:
                print(f"  line: {line.strip()!r}")


if __name__ == "__main__":
    main()
