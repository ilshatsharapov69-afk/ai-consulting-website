"""Select Web platform, fill fields, find Create button."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "analytics.google.com" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # 1) Click Web platform
        try:
            web = page.get_by_role("button", name="Веб", exact=True)
            if web.count() > 0:
                web.first.click()
                print("  clicked Веб")
        except Exception as e:
            print(f"  Веб click: {str(e)[:60]}")

        page.wait_for_timeout(3500)

        # 2) Inspect dialog/form
        print("\n--- after platform click ---")
        for h in page.locator("h1, h2, h3, [role='heading']:visible").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass
        print("  all visible inputs:")
        for inp in page.locator("input:visible").all()[:10]:
            try:
                t = inp.get_attribute("type") or ""
                n = inp.get_attribute("name") or inp.get_attribute("aria-label") or inp.get_attribute("placeholder") or ""
                v = inp.input_value() if t not in ("checkbox", "radio", "hidden") else ""
                print(f"    type={t} n={n[:40]!r} v={v[:40]!r}")
            except Exception:
                pass
        print("  all visible buttons:")
        for b in page.locator("button:visible").all()[:15]:
            try:
                t = b.inner_text().strip()[:50]
                if t: print(f"    {t!r}")
            except Exception:
                pass

        # 3) Fill URL and name
        url_input = page.locator("input[aria-label*='URL' i], input[placeholder*='URL' i], input[name*='URL']").first
        if url_input.count() > 0 and url_input.is_visible():
            url_input.click()
            url_input.fill("ai-consulting-website.sherlock753cc.workers.dev")
            print("  URL filled")
        page.wait_for_timeout(500)

        # Find stream name input
        stream_input = page.locator("input[aria-label*='поток' i], input[aria-label*='stream' i], input[placeholder*='поток' i]").first
        if stream_input.count() > 0 and stream_input.is_visible():
            stream_input.click()
            stream_input.fill("Main")
            print("  name filled")
        else:
            # fallback: second text input
            inputs = page.locator("input[type='text']:visible, input:not([type]):visible").all()
            for inp in inputs:
                try:
                    n = inp.get_attribute("name") or inp.get_attribute("aria-label") or ""
                    if "URL" in n: continue
                    val = inp.input_value()
                    if not val:
                        inp.click()
                        inp.fill("Main")
                        print("  fallback name filled")
                        break
                except Exception:
                    pass

        page.wait_for_timeout(1000)

        # Click Create
        for label in ["Создать поток", "Create stream", "Создать и продолжить", "Create", "Создать"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(6000)
        body = page.locator("body").inner_text()
        m = re.search(r"\bG-[A-Z0-9]{8,12}\b", body)
        if m:
            print(f"\n>>> GA4_MEASUREMENT_ID={m.group(0)}")
            return
        print("\n--- no ID yet; last 800 chars ---")
        print(body[-800:])


if __name__ == "__main__":
    main()
