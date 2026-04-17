"""Full Email Routing setup in one go."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from patchright.sync_api import sync_playwright


def get_page(ctx):
    for p in ctx.pages:
        if "email/routing" in p.url:
            return p
    return None


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://localhost:9333")
        ctx = browser.contexts[0]
        page = get_page(ctx)
        if not page: print("no page"); return
        page.bring_to_front()

        # Click Get started in main content
        try:
            btn = page.locator("main button:has-text('Get started')").first
            btn.click(timeout=3000)
            print("[1] clicked Get started")
        except Exception as e:
            print(f"  get-started err: {str(e)[:80]}")

        page.wait_for_timeout(3500)

        # Fill customAddress
        try:
            ca = page.locator("input[name='customAddress']").first
            ca.click()
            ca.fill("hello")
            print("[2] filled customAddress=hello")
        except Exception as e:
            print(f"  ca err: {str(e)[:80]}")

        page.wait_for_timeout(800)

        # Click the Action dropdown — find by label's parent container
        # Use JS to find and click it
        clicked_action = page.evaluate("""() => {
          const labels = [...document.querySelectorAll('label, span, div')].filter(
            el => el.textContent.trim() === 'Action' && el.children.length < 2
          );
          for (const lbl of labels) {
            const container = lbl.closest('div[class], fieldset, section');
            if (!container) continue;
            // look for button or combobox in container
            const ctrl = container.querySelector('button[aria-haspopup], button[role="combobox"], select, [role="combobox"], [role="button"][aria-expanded]');
            if (ctrl) {
              ctrl.scrollIntoView({block: 'center'});
              ctrl.click();
              return 'clicked: ' + ctrl.tagName + '|' + (ctrl.getAttribute('role') || '') + '|' + (ctrl.getAttribute('aria-haspopup') || '');
            }
            // fallback: any clickable that's NOT the label itself and NOT an input
            const clickables = container.querySelectorAll('button, [tabindex]');
            for (const c of clickables) {
              if (c === lbl || c.tagName === 'INPUT') continue;
              const txt = (c.innerText || '').trim();
              if (txt.includes('Create') || txt.includes('Exit') || txt.includes('Skip')) continue;
              c.scrollIntoView({block: 'center'});
              c.click();
              return 'fallback-clicked: ' + c.tagName + ' txt=' + txt.slice(0, 30);
            }
          }
          return 'no Action widget found';
        }""")
        print(f"[3] action-click: {clicked_action}")
        page.wait_for_timeout(2000)

        # Pick "Send to an email" option — any visible option
        picked = page.evaluate("""() => {
          const sels = ['[role="option"]', '[role="menuitem"]', 'li'];
          for (const s of sels) {
            const els = document.querySelectorAll(s);
            for (const e of els) {
              if (!e.offsetParent) continue;  // not visible
              const t = (e.innerText || '').trim();
              if (t.toLowerCase().includes('send to') && t.toLowerCase().includes('email')) {
                e.click();
                return 'picked: ' + t.slice(0, 40);
              }
            }
          }
          return 'no option found';
        }""")
        print(f"[4] pick-option: {picked}")
        page.wait_for_timeout(2000)

        # Fill destination input — last visible text input not named customAddress
        filled = page.evaluate("""() => {
          const inputs = [...document.querySelectorAll('input')].filter(i => {
            const t = i.type || '';
            if (t === 'hidden' || t === 'checkbox' || t === 'radio' || t === 'submit' || t === 'button') return false;
            if (!i.offsetParent) return false;  // not visible
            if (i.name === 'customAddress') return false;
            return true;
          });
          if (!inputs.length) return 'no destination input';
          const inp = inputs[inputs.length - 1];
          inp.focus();
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          setter.call(inp, 'sherlock753cc@gmail.com');
          inp.dispatchEvent(new Event('input', {bubbles: true}));
          inp.dispatchEvent(new Event('change', {bubbles: true}));
          return 'filled destination input';
        }""")
        print(f"[5] fill-dest: {filled}")
        page.wait_for_timeout(1500)

        # Verify values
        print("\n--- values check ---")
        for inp in page.locator("input:visible").all()[:6]:
            try:
                n = inp.get_attribute("name") or ""
                t = inp.get_attribute("type") or ""
                v = inp.input_value() if t not in ("hidden","checkbox","radio") else ""
                if t in ("hidden","checkbox","radio"): continue
                print(f"  {n!r} [{t}]={v[:30]!r}")
            except Exception:
                pass

        # Click Create and continue
        try:
            btn = page.locator("button:has-text('Create and continue')").first
            btn.click(timeout=5000)
            print("\n[6] clicked Create and continue")
        except Exception as e:
            print(f"  submit err: {str(e)[:80]}")

        page.wait_for_timeout(6000)
        print("\n--- after submit ---")
        print("URL:", page.url)
        body = page.locator("body").inner_text()
        for line in body.split("\n"):
            s = line.strip()
            if any(k in s.lower() for k in ["verification", "verify", "confirm", "email sent"]) and len(s) < 200:
                print(f"  {s!r}")


if __name__ == "__main__":
    main()
