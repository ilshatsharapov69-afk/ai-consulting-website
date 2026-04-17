"""Click 'Новый проект' on Clarity, fill form, extract Project ID."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def get_page(ctx):
    for p in ctx.pages:
        if "clarity" in p.url:
            return p
    return None


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page: print("no page"); return
        page.bring_to_front()

        # Click New Project
        try:
            btn = page.locator("button:has-text('Новый проект'), a:has-text('Новый проект')").first
            btn.click(timeout=5000)
            print("  clicked Новый проект")
        except Exception as e:
            print(f"  click err: {str(e)[:80]}")

        page.wait_for_timeout(4000)
        print("URL:", page.url)
        print("--- inputs ---")
        for inp in page.locator("input:visible, textarea:visible").all()[:10]:
            try:
                t = inp.get_attribute("type") or ""
                n = inp.get_attribute("name") or inp.get_attribute("aria-label") or inp.get_attribute("placeholder") or ""
                v = inp.input_value()
                print(f"  type={t} n={n[:40]!r} v={v[:40]!r}")
            except Exception:
                pass
        print("--- buttons ---")
        for b in page.locator("button:visible").all()[:10]:
            try:
                t = b.inner_text().strip()[:60]
                if t: print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
