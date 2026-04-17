"""Enable Email Routing and add routing rule."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = None
        for p in ctx.pages:
            if "email/routing" in p.url:
                page = p; break
        if not page: print("no page"); return
        page.bring_to_front()

        # Inspect full page text
        body = page.locator("body").inner_text()
        # Find the main content area (excluding sidebar)
        print("--- body lines containing 'enable', 'get started', 'routing', 'destination' ---")
        for line in body.split("\n"):
            s = line.strip()
            if s and any(k in s.lower() for k in ["enable", "get started", "forward", "destination", "address", "rule", "setup", "configure"]):
                if len(s) < 120:
                    print(f"  {s!r}")

        print("\n--- main clickable elements ---")
        # Look for buttons outside the sidebar
        for b in page.locator("main button:visible, [role='main'] button:visible, .content button:visible").all()[:15]:
            try:
                t = b.inner_text().strip()[:80]
                if t: print(f"  {t!r}")
            except Exception:
                pass


if __name__ == "__main__":
    main()
