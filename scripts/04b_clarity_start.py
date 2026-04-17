"""Click Get Started on Clarity, pick sign-in provider."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def get_page(ctx):
    for p in ctx.pages:
        if "clarity.microsoft" in p.url or "login.microsoftonline" in p.url or "login.live" in p.url:
            return p
    return None


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page: print("no page"); return
        page.bring_to_front()

        for label in ["Начало работы", "Get started", "Регистрация", "Sign up"]:
            try:
                btn = page.get_by_role("button", name=label, exact=True)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=3000)
                    print(f"  clicked: {label}")
                    break
                # try link too
                a = page.get_by_role("link", name=label, exact=True)
                if a.count() > 0 and a.first.is_visible():
                    a.first.click(timeout=3000)
                    print(f"  clicked link: {label}")
                    break
            except Exception:
                pass

        page.wait_for_timeout(5000)
        print("\nURL:", page.url)
        for h in page.locator("h1, h2, h3").all()[:5]:
            try:
                t = h.inner_text().strip()[:80]
                if t: print(f"  h: {t!r}")
            except Exception:
                pass
        print("--- buttons ---")
        for b in page.locator("button:visible, a:visible").all()[:15]:
            try:
                t = b.inner_text().strip()[:60]
                if t and len(t) < 80: print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
