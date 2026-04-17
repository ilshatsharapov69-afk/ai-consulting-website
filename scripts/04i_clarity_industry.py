"""Pick industry + click Add new project."""
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

        # Click "Выберите один" dropdown
        try:
            dd = page.locator("button:has-text('Выберите один'), div[role='combobox']").first
            if dd.count() > 0:
                dd.click(timeout=5000)
                print("  opened industry dropdown")
                page.wait_for_timeout(1500)
        except Exception as e:
            print(f"  dd: {str(e)[:80]}")

        # Pick "Бизнес" or "Услуги" or first option
        picked = False
        for label in ["Бизнес", "Профессиональные услуги", "Услуги", "Business", "Professional"]:
            try:
                opt = page.locator(f"li:has-text('{label}'), [role='option']:has-text('{label}'), button:has-text('{label}')").first
                if opt.is_visible(timeout=1500):
                    opt.click()
                    print(f"  picked industry: {label}")
                    picked = True
                    break
            except Exception:
                pass
        if not picked:
            # fallback: click first option
            try:
                opts = page.locator("[role='option']:visible, li[role='option']:visible").all()
                if opts:
                    opts[0].click()
                    t = opts[0].inner_text().strip()[:40]
                    print(f"  fallback pick: {t}")
            except Exception:
                pass

        page.wait_for_timeout(1000)

        # Click Add new project
        for label in ["Добавить новый проект"]:
            try:
                btn = page.get_by_role("button", name=label, exact=False)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(7000)
        print("\nURL after:", page.url)
        # Look for project ID in URL (projects/XXXXXXXXXX)
        m = re.search(r"/projects/([a-z0-9]{10,12})", page.url)
        if m:
            print(f"\n>>> CLARITY_PROJECT_ID={m.group(1)}")
            return
        # also search body for install snippet with project ID
        body = page.locator("body").inner_text()
        # Clarity snippet: clarity.ms/tag/PROJECT_ID
        m2 = re.search(r'clarity\.ms/tag/([a-z0-9]+)', body)
        if m2:
            print(f"\n>>> CLARITY_PROJECT_ID={m2.group(1)}")
            return
        # try to get from HTML source
        html = page.content()
        m3 = re.search(r'clarity\.ms/tag/([a-z0-9]+)', html)
        if m3:
            print(f"\n>>> CLARITY_PROJECT_ID={m3.group(1)}")
            return
        m4 = re.search(r'projectId["\']?\s*[:=]\s*["\']([a-z0-9]+)', html)
        if m4:
            print(f"\n>>> CLARITY_PROJECT_ID={m4.group(1)}")
            return

        print("  no ID found")
        print("  URL:", page.url)


if __name__ == "__main__":
    main()
