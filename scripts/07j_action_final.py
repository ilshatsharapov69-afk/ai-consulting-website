"""Try click on Action field via JS / by label association."""
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

        # press Escape to close any stray menu
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        # Use JS to find the Action label's paired control
        result = page.evaluate("""() => {
          const labels = [...document.querySelectorAll('label')];
          const action_lbl = labels.find(l => l.textContent.trim() === 'Action');
          if (!action_lbl) return 'no Action label';
          // look for aria-labelledby references
          const id = action_lbl.getAttribute('for') || action_lbl.id;
          const parent = action_lbl.closest('div, fieldset, section');
          if (!parent) return 'no parent';
          // find the first interactive element AFTER label in parent
          const candidates = parent.querySelectorAll('button, [role="combobox"], [role="button"], select, [tabindex]:not([tabindex="-1"])');
          const list = [];
          for (const c of candidates) {
            list.push({
              tag: c.tagName,
              role: c.getAttribute('role') || '',
              text: (c.innerText || c.textContent || '').trim().slice(0, 50),
              aria: c.getAttribute('aria-label') || ''
            });
          }
          return JSON.stringify(list.slice(0, 8));
        }""")
        print(result)

        # Click via JS as well
        clicked = page.evaluate("""() => {
          const labels = [...document.querySelectorAll('label')];
          const action_lbl = labels.find(l => l.textContent.trim() === 'Action');
          if (!action_lbl) return 'no label';
          const parent = action_lbl.closest('div, fieldset, section');
          if (!parent) return 'no parent';
          // click first combobox or button that's not 'Create and continue'
          const candidates = parent.querySelectorAll('button, [role="combobox"], [role="button"]');
          for (const c of candidates) {
            const txt = (c.innerText || '').trim();
            if (!txt.includes('Create') && !txt.includes('Exit') && !txt.includes('Skip')) {
              c.click();
              return 'clicked: ' + txt.slice(0, 30) + ' | ' + c.tagName;
            }
          }
          return 'no target found';
        }""")
        print("js-click:", clicked)

        page.wait_for_timeout(1500)

        # Look for menu options
        print("\n--- options after JS click ---")
        for sel in ["[role='option']:visible", "li[role='option']", "[role='menuitem']"]:
            els = page.locator(sel).all()
            for e in els[:6]:
                try:
                    t = e.inner_text().strip()[:80]
                    if t: print(f"  [{sel[:30]}] {t!r}")
                except Exception:
                    pass

        # pick "Send to an email"
        for sel in ["[role='option']:has-text('Send to an email')", "li:has-text('Send to an email')"]:
            try:
                el = page.locator(sel).first
                if el.is_visible(timeout=1500):
                    el.click()
                    print(f"  picked: Send to an email")
                    break
            except Exception:
                pass


if __name__ == "__main__":
    main()
