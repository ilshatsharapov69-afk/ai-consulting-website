"""Inspect Cal.com profile page structure."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "cal.com" in p.url and "profile" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()
        page.wait_for_timeout(1000)

        print("--- visible labels ---")
        for lab in page.locator("label:visible").all()[:15]:
            try:
                t = lab.inner_text().strip()[:80]
                if t: print(f"  {t!r}")
            except Exception:
                pass

        print("\n--- all inputs ---")
        for inp in page.locator("input").all()[:20]:
            try:
                n = inp.get_attribute("name") or ""
                t = inp.get_attribute("type") or ""
                v = inp.input_value() if t not in ("checkbox", "radio", "hidden") else ""
                vis = inp.is_visible()
                if t in ("hidden",): continue
                print(f"  name={n!r} type={t!r} visible={vis} value={v[:40]!r}")
            except Exception:
                pass

        print("\n--- text containing ilshat-sharapov ---")
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            s = line.strip()
            if "ilshat-sharapov" in s.lower() and len(s) < 200:
                print(f"  {s!r}")


if __name__ == "__main__":
    main()
