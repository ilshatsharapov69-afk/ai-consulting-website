"""Walk through Cal.com onboarding. Fill username, pick free tier, grab event URL."""
from patchright.sync_api import sync_playwright


def get_calcom_page(ctx):
    for p in ctx.pages:
        if "cal.com" in p.url:
            return p
    return None


def click_continue(page):
    for label_variants in [
        ["Continue", "Продолжить", "Next", "Далее"],
    ]:
        for label in label_variants:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click()
                    print(f"  clicked: {label}")
                    return True
            except Exception:
                pass
    return False


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_calcom_page(ctx)
        if not page:
            print("no page"); return
        page.bring_to_front()

        for step in range(15):
            page.wait_for_timeout(1800)
            url = page.url
            print(f"[step {step}] url={url[:100]}")

            # if on event-types / settings / booking page, we're done with onboarding
            if any(k in url for k in ["/event-types", "/bookings", "/settings", "/apps/installed"]):
                print("  reached dashboard")
                break

            # Fill visible inputs (username, name) if empty
            inputs = page.locator("input:visible").all()
            for inp in inputs[:5]:
                try:
                    t = inp.get_attribute("type") or ""
                    n = inp.get_attribute("name") or ""
                    if t in ("checkbox", "radio", "submit"):
                        continue
                    current = inp.input_value()
                    if not current and n:
                        if "username" in n.lower():
                            inp.fill("ilshatai")
                            print(f"  filled username=ilshatai")
                        elif "name" in n.lower() and "user" not in n.lower():
                            inp.fill("Ilshat")
                            print(f"  filled name=Ilshat")
                except Exception:
                    pass

            # Click Continue
            if not click_continue(page):
                # try clicking "Finish" or similar end-buttons
                for label in ["Finish", "Done", "Get Started", "Skip"]:
                    try:
                        btn = page.get_by_role("button", name=label, exact=False)
                        if btn.count() > 0 and btn.first.is_visible():
                            btn.first.click()
                            print(f"  clicked end: {label}")
                            break
                    except Exception:
                        pass

        # Now on dashboard. Find event types.
        page.wait_for_timeout(2000)
        page.goto("https://app.cal.com/event-types", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        print("\n--- event-types page ---")
        print("URL:", page.url)
        # list all links that look like event URLs
        print("--- event links ---")
        for a in page.locator("a").all():
            try:
                href = a.get_attribute("href") or ""
                txt = a.inner_text().strip()[:40]
                if href.startswith("/") and "/event-types/" not in href:
                    pass
                if "ilshatai" in href or txt.count("min") or "20" in txt:
                    print(f"  {txt!r} -> {href[:80]}")
            except Exception:
                pass

        # Better: look for username in page data
        body = page.locator("body").inner_text()
        print("\n--- body 600 chars ---")
        print(body[:600])


if __name__ == "__main__":
    main()
