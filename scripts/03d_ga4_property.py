"""Fill GA4 property name, advance step by step carefully."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def get_page(ctx):
    for p in ctx.pages:
        if "analytics.google.com" in p.url:
            return p
    return None


def snapshot(page, tag):
    print(f"\n--- {tag} ---")
    print("URL:", page.url)
    try:
        for h in page.locator("h1, h2, h3").all()[:4]:
            t = h.inner_text().strip()[:80]
            if t: print(f"  h: {t!r}")
    except Exception:
        pass
    print("  inputs:")
    for inp in page.locator("input:visible").all()[:8]:
        try:
            t = inp.get_attribute("type") or ""
            if t in ("hidden",): continue
            n = inp.get_attribute("name") or inp.get_attribute("aria-label") or ""
            v = inp.input_value() if t not in ("checkbox", "radio") else ("checked" if inp.is_checked() else "unchecked")
            print(f"    type={t} name={n[:30]!r} val={v[:30]!r}")
        except Exception:
            pass
    print("  buttons:")
    for b in page.locator("button:visible").all()[:8]:
        try:
            t = b.inner_text().strip()[:40]
            if t: print(f"    {t!r}")
        except Exception:
            pass


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page: print("no page"); return
        page.bring_to_front()

        snapshot(page, "initial")

        # Fill property name — find first visible text input
        text_inputs = page.locator("input[type='text']:visible").all()
        if text_inputs:
            text_inputs[0].click()
            text_inputs[0].fill("AI Consulting Website")
            print("  filled property name")

        page.wait_for_timeout(1500)
        # Click Next
        for label in ["Далее", "Next"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass
        page.wait_for_timeout(4000)

        snapshot(page, "step 3 (business details)")

        # Business details — click Next
        for label in ["Далее", "Next"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass
        page.wait_for_timeout(4000)

        snapshot(page, "step 4")


if __name__ == "__main__":
    main()
