"""Go to Clarity install/setup page to get confirmed tracking ID."""
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

        # Clarity settings/setup tab
        page.goto("https://clarity.microsoft.com/projects/view/wcya539i1f/settings/setup", wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        print("URL:", page.url)

        # Try the install tab
        for tab_label in ["Установить", "Install", "Настройка", "Setup", "Track"]:
            try:
                el = page.locator(f"button:has-text('{tab_label}'), a:has-text('{tab_label}')").first
                if el.is_visible(timeout=1000):
                    el.click()
                    print(f"  clicked tab: {tab_label}")
                    page.wait_for_timeout(2000)
                    break
            except Exception:
                pass

        # Get full HTML and look for the actual project ID
        html = page.content()
        matches = list(set(re.findall(r'clarity\.ms/tag/([a-z0-9]{6,15})', html)))
        print("  all tag IDs in HTML:", matches)
        # the PROJECT's real tracking id
        # try matching "projectId": "XXX"
        pm = re.search(r'projectId["\']?\s*[:=]\s*["\']([a-z0-9]+)', html)
        if pm:
            print(f"  projectId from JS: {pm.group(1)}")
        tm = re.search(r'"tag"\s*[:,]?\s*["\']([a-z0-9]+)', html)
        if tm:
            print(f"  tag from JS: {tm.group(1)}")
        # Look for patterns like "T,"xxxx");
        tm2 = re.search(r'"script",\s*"([a-z0-9]+)"', html)
        if tm2:
            print(f"  script id: {tm2.group(1)}")

        # Also inspect body
        body = page.locator("body").inner_text()
        # print a chunk around "clarity"
        idx = body.find("clarity.ms")
        if idx >= 0:
            print("\n--- body around clarity.ms ---")
            print(body[max(0, idx-200):idx+400])


if __name__ == "__main__":
    main()
