---
title: Entity Signals — LinkedIn + Crunchbase URL Handoff
date: 2026-04-22
session: C1.3
status: action-required
tags: [entity, config, linkedin, crunchbase]
---

# Entity Signals — Post-Creation Handoff

After you create the LinkedIn and Crunchbase profiles per the Session C copy kits:

- Personal LinkedIn copy kit: [research/2026-04-21_entity-kit/linkedin-copy.md](../../DeepReserch/research/2026-04-21_entity-kit/linkedin-copy.md)
- Crunchbase copy kit: [research/2026-04-21_entity-kit/crunchbase-copy.md](../../DeepReserch/research/2026-04-21_entity-kit/crunchbase-copy.md)

...return to the chat with the URLs and Claude will wire them into the site's `sameAs` chain.

---

## What needs updating once the profiles are live

### 1. `src/config.ts` — LinkedIn personal URL

Current state (line 20):

```ts
social: {
  linkedin: '',
  youtube: 'https://youtube.com/@Ilshatai',
},
```

Replace with the actual personal profile URL. Example:

```ts
social: {
  linkedin: 'https://www.linkedin.com/in/ilshat-sharapov/',
  youtube: 'https://youtube.com/@Ilshatai',
},
```

**One-line command for Claude to run (paste your real URL in `<URL>`):**

```
Edit src/config.ts: replace `linkedin: ''` with `linkedin: '<URL>'`
```

### 2. `src/components/JsonLd.astro` — expand `sameAs` chains

Both the **Organization** node and the **Person** node in the unified `@graph` currently emit `sameAs` arrays that include only YouTube. They need to include LinkedIn (personal + Company Page) and Crunchbase (company + founder).

Expected final shape (for reference only — Claude will edit):

```json
{
  "@type": "Organization",
  "@id": "https://setpointaudit.com/#organization",
  "sameAs": [
    "https://youtube.com/@Ilshatai",
    "https://www.linkedin.com/company/setpointaudit/",
    "https://www.crunchbase.com/organization/setpoint-audit"
  ]
},
{
  "@type": "Person",
  "@id": "https://setpointaudit.com/#person",
  "sameAs": [
    "https://youtube.com/@Ilshatai",
    "https://www.linkedin.com/in/ilshat-sharapov/",
    "https://www.crunchbase.com/person/ilshat-sharapov"
  ]
}
```

### 3. Build + commit + push

```bash
cd D:/ai-consulting-website
npm run build                    # expect 17 pages, 0 errors, ~2-3s
git add src/config.ts src/components/JsonLd.astro
git commit -m "entity: wire LinkedIn + Crunchbase into sameAs chain"
git push
```

Cloudflare Pages auto-deploys on push.

### 4. Verify live after deploy (~2 min)

```bash
curl -s https://setpointaudit.com/ | grep -oE '"sameAs":\[[^]]+\]' | head -5
```

Expect both Organization and Person `sameAs` arrays to list all three URLs.

Then paste `https://setpointaudit.com/` into [Schema.org Validator](https://validator.schema.org/) and confirm 0 errors with the expanded graph.

---

## What to paste into chat (template)

When you return with URLs, a message like this is enough:

```
LinkedIn personal: https://www.linkedin.com/in/<slug>/
LinkedIn Company: https://www.linkedin.com/company/<slug>/
Crunchbase Org:   https://www.crunchbase.com/organization/<slug>
Crunchbase You:   https://www.crunchbase.com/person/<slug>
```

Claude will do the three edits above, run the build, commit, and push. No further action needed from you.

---

## Why this matters (one paragraph)

Per 2026 Q2 entity SEO research, Google's Knowledge Graph uses `sameAs` cross-links to verify that a Person entity on the site is the same individual referenced on LinkedIn, YouTube, and Crunchbase. A broken or short `sameAs` chain keeps the entity "unconfirmed" and prevents Knowledge Panel generation. Five cross-linked nodes is the floor the Kalicube and 12AM Agency 2026 guides cite for a solo consultant to even be eligible for panel. We get there with this step.
