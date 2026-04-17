"""Fill Clarity project form, save, extract Project ID."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "clarity" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Fill name
        name_inp = page.locator("input[placeholder*='Contoso']").first
        if name_inp.count() > 0:
            name_inp.click()
            name_inp.fill("AI Consulting Website")
            print("  name filled")

        # Fill URL
        url_inp = page.locator("input[placeholder*='www.contoso']").first
        if url_inp.count() > 0:
            url_inp.click()
            url_inp.fill("ai-consulting-website.sherlock753cc.workers.dev")
            print("  URL filled")

        # Make sure Website (not Mobile app) is selected
        try:
            web_btn = page.locator("button:has-text('Веб-сайт')").first
            if web_btn.count() > 0 and web_btn.is_visible():
                web_btn.click()
                print("  clicked Веб-сайт")
        except Exception:
            pass

        page.wait_for_timeout(800)

        # Click Создать / Save / Добавить
        clicked = False
        for label in ["Добавить новый проект", "Создать", "Add new project", "Create project", "Сохранить", "Save", "Добавить"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    clicked = True
                    break
            except Exception:
                pass
        if not clicked:
            # look at all visible buttons
            print("  NO button clicked; visible buttons:")
            for b in page.locator("button:visible").all()[:15]:
                try:
                    t = b.inner_text().strip()[:60]
                    if t: print(f"    {t!r}")
                except Exception:
                    pass

        page.wait_for_timeout(6000)
        print("\nURL after:", page.url)
        # Search for Clarity project ID pattern (10-char lowercase-alphanumeric)
        body = page.locator("body").inner_text()
        # Look for URL pattern clarity.microsoft.com/projects/{ID}
        m = re.search(r"/projects/([a-z0-9]{10,12})(?:/|$|\b)", page.url)
        if m:
            print(f">>> CLARITY_PROJECT_ID={m.group(1)}")
        else:
            m2 = re.search(r'["\s/](["\']?[a-z0-9]{10})["\s/]', body)
            if m2:
                print(f"  body match: {m2.group(1)}")
            print("  URL path:", page.url.split("/")[-1][:50])
            print("--- body last 500 ---")
            print(body[-500:])


if __name__ == "__main__":
    main()
