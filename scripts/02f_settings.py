"""Set Cal.com username to 'ilshatai' (match YouTube handle), proceed."""
from patchright.sync_api import sync_playwright


def get_page(ctx):
    for p in ctx.pages:
        if "cal.com" in p.url:
            return p
    return None


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page:
            print("no page"); return
        page.bring_to_front()

        # Fill username
        uname_input = page.locator("input[name='username']").first
        uname_input.click()
        uname_input.fill("")
        uname_input.fill("ilshatai")
        page.wait_for_timeout(800)
        print("username set to 'ilshatai'")

        # check for availability warnings
        # (skip — we'll just proceed)

        # Click Next/Continue — likely second-to-last visible button
        page.wait_for_timeout(500)
        # Try "Далее" (Next) first, then Continue
        for label in ["Далее", "Next", "Continue", "Продолжить"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass

        # Walk through any remaining onboarding steps
        for step in range(10):
            page.wait_for_timeout(2000)
            url = page.url
            print(f"[step {step}] {url[:90]}")

            if "/onboarding" not in url:
                print("  exited onboarding")
                break

            # fill any empty visible text inputs (defensively)
            for inp in page.locator("input:visible").all()[:5]:
                try:
                    t = inp.get_attribute("type") or ""
                    if t in ("checkbox", "radio", "submit", "hidden"):
                        continue
                    val = inp.input_value()
                    n = inp.get_attribute("name") or ""
                    # leave username alone, skip filled
                    if val or "username" in n.lower():
                        continue
                    # fill name if empty
                    if "name" in n.lower():
                        inp.fill("Ilshat")
                except Exception:
                    pass

            # click Next / Continue / Skip / Finish
            advanced = False
            for label in ["Далее", "Next", "Continue", "Продолжить", "Finish", "Готово", "Skip", "Пропустить"]:
                try:
                    btn = page.get_by_role("button", name=label, exact=False)
                    if btn.count() > 0 and btn.first.is_visible():
                        btn.first.click(timeout=2000)
                        print(f"  clicked: {label}")
                        advanced = True
                        break
                except Exception:
                    pass
            if not advanced:
                print("  no advance button found")

        print("\n--- final URL:", page.url)
        print("--- first h1/h2 ---")
        for h in page.locator("h1, h2").all()[:5]:
            try:
                print(" ", h.inner_text().strip()[:80])
            except Exception:
                pass


if __name__ == "__main__":
    main()
