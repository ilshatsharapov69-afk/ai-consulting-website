"""Verify Clarity tracking ID for NEW project."""
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

        # Navigate directly to setup/install page for the new project
        page.goto("https://clarity.microsoft.com/projects/view/wcya539i1f/gettingstarted", wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
        print("URL:", page.url)

        # look for the install snippet
        html = page.content()
        # Find all clarity.ms/tag/XXX occurrences
        matches = re.findall(r'clarity\.ms/tag/([a-z0-9]+)', html)
        print("  tag ID matches in HTML:", set(matches))

        # Also look for projectId references in the visible body
        body = page.locator("body").inner_text()
        snippet_match = re.search(r'clarity\.ms/tag/([a-z0-9]+)', body)
        if snippet_match:
            print(f"  body snippet tag: {snippet_match.group(1)}")

        # Display install code section if any
        for code_elem in page.locator("code, pre").all()[:5]:
            try:
                t = code_elem.inner_text().strip()[:300]
                if "clarity" in t:
                    print("\n--- code snippet found ---")
                    print(t)
            except Exception:
                pass

        # The URL path should have the project ID
        m = re.search(r'/projects/view/([a-z0-9]+)', page.url)
        if m:
            print(f"\n  project slug from URL: {m.group(1)}")


if __name__ == "__main__":
    main()
