"""Fill GA4 web stream URL + name, create, extract Measurement ID."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def get_page(ctx):
    for p in ctx.pages:
        if "analytics.google.com" in p.url:
            return p
    return None


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page: print("no page"); return
        page.bring_to_front()

        # Fill URL
        url_input = page.locator("input[name='URL веб-сайта'], input[aria-label*='URL' i]").first
        if url_input.count() > 0:
            url_input.click()
            url_input.fill("ai-consulting-website.sherlock753cc.workers.dev")
            print("  filled URL")

        # Fill stream name — second input
        all_inputs = page.locator("input[type='text']:visible, input:not([type]):visible").all()
        filled_second = False
        for inp in all_inputs:
            try:
                n = inp.get_attribute("name") or ""
                if "URL" in n:
                    continue
                # this is the stream name
                inp.click()
                inp.fill("Main")
                print("  filled stream name: Main")
                filled_second = True
                break
            except Exception:
                pass

        page.wait_for_timeout(800)

        # Click Create Stream
        for label in ["Создать поток", "Create stream", "Создать"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(6000)
        print("\nURL:", page.url)

        # A modal should show stream details with Measurement ID G-XXXXXXXX
        body = page.locator("body").inner_text()
        m = re.search(r"\bG-[A-Z0-9]{8,12}\b", body)
        if m:
            print(f"\n>>> GA4_MEASUREMENT_ID={m.group(0)}")
            return

        # if not in modal, navigate to data streams
        print("  no ID in body; looking for streams page")
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass

        # try closing any overlay and navigate
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        page.wait_for_timeout(1500)

        # Check page text to see what's there
        body = page.locator("body").inner_text()
        # last 1500 chars often contain the measurement ID
        print("\n--- body last 1500 chars ---")
        print(body[-1500:])


if __name__ == "__main__":
    main()
