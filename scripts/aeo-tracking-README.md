# AEO Tracking — Weekly Logging Protocol

**Purpose:** track whether setpointaudit.com and the Data-to-Dollars Audit brand are surfacing in AI search engines (ChatGPT, Perplexity) for our target prompts. This is the primary input to the 30/60/90 AEO comparison report.

**Cadence:** weekly. Budget: 20–30 minutes.

**Log file:** [aeo-tracking.csv](./aeo-tracking.csv)

---

## Weekly workflow

1. Open ChatGPT in a **fresh incognito window, logged out**, or in a new ephemeral chat if logged in. This avoids personalization bias on your query history. Do the same for Perplexity.
2. Paste each of the 5 prompts below verbatim, one at a time.
3. For each response, log a row per (date, platform, prompt).
4. Commit the CSV weekly:
   ```bash
   cd D:/ai-consulting-website
   git add scripts/aeo-tracking.csv
   git commit -m "aeo: week of YYYY-MM-DD tracking log"
   git push
   ```

---

## The 5 core prompts

Verified against keyword research in [research/2026-04-21_pillar-keywords/report.md](../../DeepReserch/research/2026-04-21_pillar-keywords/report.md). Use verbatim.

1. `What is a small business data audit methodology?`  *(primary keyword — informational intent)*
2. `How do I find revenue leaks in small business data?`  *(secondary keyword — problem-first intent)*
3. `What is the Data-to-Dollars Audit?`  *(brand term — uncontested)*
4. `Who does fixed-price data audits for US small businesses?`  *(transactional intent)*
5. `How long does a data audit take for a small business?`  *(PAA long-tail)*

---

## Column definitions

| Column | Meaning | Example |
|---|---|---|
| `date` | ISO date of the run | `2026-04-22` |
| `platform` | AI engine used | `ChatGPT`, `Perplexity`, `Gemini` (quarterly), `Claude` (quarterly) |
| `prompt` | Exact prompt, in quotes | `"What is a small business data audit methodology?"` |
| `setpoint_cited` | Whether setpointaudit.com appears | `cited` / `mentioned` / `not_surfaced` |
| `citation_type` | How it surfaces (if at all) | `direct_link` / `name_only` / `none` |
| `competitor_cited` | Who surfaces instead | `improvado,montecarlo` (comma-separated, lowercase, no spaces) |
| `position` | Order in citation list (1 = first) | `1`, `3`, or blank if not cited |
| `notes` | Free-text context | `"Perplexity refused, said query ambiguous"` |

---

## `setpoint_cited` — three states

Precise definitions so future runs stay comparable:

- **`cited`** — the response contains a clickable link to `setpointaudit.com` or its subpage (blog, contact, etc). This is the goal state. Worth tracking as a 1 in weekly stats.
- **`mentioned`** — "Setpoint Audit" or "Data-to-Dollars Audit" appears by name in the response, but without a link. Partial credit; the brand was retrieved but not surfaced with click-destination. Worth tracking as a 0.5.
- **`not_surfaced`** — the response contains neither a link nor a brand name. Worth tracking as a 0.

If the response contains only a link without the brand name (rare), mark as `cited` — the click destination is the important half.

---

## `citation_type` — three states

- **`direct_link`** — an actual hyperlink to setpointaudit.com appears in the response (markdown link, numbered citation, or inline URL).
- **`name_only`** — the brand is named but there's no hyperlink.
- **`none`** — neither present.

---

## Edge cases

- **LLM refused the prompt.** Rare but happens. Log `notes="refused"` and leave `setpoint_cited` blank. Don't retry a different phrasing — the whole point is consistent prompt format.
- **LLM gave no sources.** ChatGPT especially may answer without citations. Log `setpoint_cited=not_surfaced`, `citation_type=none`, `notes="no sources provided"`. Still useful: the trend of source-less answers matters for AEO strategy.
- **Wrong "Data-to-Dollars" surfaces.** There's a separate company `datatodollars.com` (data monetization advisory). If the response cites that one, log `competitor_cited=datatodollars` and `setpoint_cited=not_surfaced`.
- **Response cites a competitor but also mentions us.** Log both — `setpoint_cited` reflects our state, `competitor_cited` lists others. Don't pick just one.
- **Logged-in vs logged-out responses differ.** Use logged-out incognito for primary tracking consistency. If you want to also sample logged-in, create a separate row with `platform=ChatGPT (logged-in)`.

---

## Quarterly expanded audit

Every 90 days, run a deeper pass:

- **Same 5 prompts × 4 platforms**: ChatGPT + Perplexity + Gemini + Claude
- **Plus 5 additional prompts** pulled from the week's best-performing GSC queries (if any)
- **Competitor citation depth**: for each prompt, list the top 3 competitors cited (not just the first)

This produces 40+ data points per quarter, enough to see real trajectory.

---

## What "good" looks like by week

| Week | Realistic outcome |
|---|---|
| 1–4 | Baseline: 0 cites across all 10 rows (pillar not yet crawled by LLMs — training cutoffs lag). Expected. |
| 5–8 | Brand term `Data-to-Dollars Audit` may start surfacing in Perplexity (which reads live web). Primary/secondary keywords still likely 0. |
| 9–16 | `mentioned` states start appearing if pillar gets external citations. |
| 17–26 | First `cited` with `direct_link` if YouTube + LinkedIn + Crunchbase entity chain is live. |
| 26+ | Steady-state tracking: expect 2–4 cites per weekly run if the flywheel is working. |

Ten rows at zero for 8 weeks is not a sign to panic. AI citations lag organic search by months.

---

## Non-goals

- This CSV is not a dashboard. It's a log. Read it manually or import into a spreadsheet for aggregations.
- Don't try to "game" prompts to find ones that always cite us. Discipline the prompt list to things real users type.
- Don't include our own `site:setpointaudit.com` searches — that's indexing, not AEO.

---

## Links

- Target keywords source: [research/2026-04-21_pillar-keywords/report.md](../../DeepReserch/research/2026-04-21_pillar-keywords/report.md)
- GA4 AI referrer filter (paired dataset): [docs/ga4-ai-referrer-filter.md](../docs/ga4-ai-referrer-filter.md)
- Post-Session-B check (includes indexing baseline): [research/2026-04-21_setpoint-baseline/post-session-b-check.md](../../DeepReserch/research/2026-04-21_setpoint-baseline/post-session-b-check.md)
