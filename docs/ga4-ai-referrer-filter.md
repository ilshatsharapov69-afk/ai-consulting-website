---
title: GA4 AI Referrer Filter — Segment Setup
date: 2026-04-22
session: C3.3
status: action-required
tags: [ga4, analytics, aeo]
---

# GA4 AI Referrer Filter — Segment Setup

**Purpose:** measure how much of setpointaudit.com traffic arrives from AI engines (ChatGPT, Perplexity, Gemini, Claude, Copilot, You.com). GA4 by default lumps these into "Referral" or sometimes "Direct" — a dedicated segment surfaces the true number.

**Time to set up: 5 minutes, one-time.**

---

## 1. The regex

Use this exact regex across all AI traffic setups. It's conservative — matches only primary referrer domains, avoids false positives.

```
chatgpt\.com|perplexity\.ai|gemini\.google\.com|claude\.ai|copilot\.microsoft\.com|you\.com|search\.brave\.com
```

**Note on Brave Search:** Brave's "Leo" AI summaries can surface on a real-web search page. Including `search.brave.com` is defensible; if you prefer strict AI-only, remove it.

**Not included:** `bing.com` (difficult to separate Bing-Chat-origin traffic from plain Bing search). If Bing Chat adoption increases, add it later with a separate segment named "Bing AI".

---

## 2. Create the GA4 segment — step-by-step

1. Open [https://analytics.google.com/](https://analytics.google.com/)
2. Select the `setpointaudit.com` property (should be the GA4 property created in session 3/4)
3. Left sidebar → **Explore** → click **+ Blank** to start a new exploration
4. In the Exploration workspace, left panel:
   - **VARIABLES** pane → **Segments** → click the **+** icon
5. In the segment builder:
   - Choose segment type: **Session segment**
   - Name: `AI traffic`
   - Add condition:
     - Dimension: `Session source` (or `Session source / medium` if you want finer granularity)
     - Match type: **matches regex**
     - Value: paste the regex from section 1
   - Click **Save**

6. The segment is now available in all explorations.

---

## 3. Test it immediately (confirm regex fires)

Still in the exploration:

1. Drag `AI traffic` segment from Variables → into Settings → **Segment comparisons**
2. Also drag the default `All users` segment in for comparison
3. In the Tab settings, choose Visualization: **Table**
4. Drag dimensions: `Event name`, `Page path + query string`
5. Drag metrics: `Sessions`, `Engaged sessions`, `Conversions` (include the `book_discovery_call` event if configured)
6. Set the date range to **Last 30 days**

Expect the `AI traffic` column to be very low (possibly 0) for weeks 1–8 after Session B deploy — same logic as AEO tracking: AI citations lag indexing by months.

If the `AI traffic` column shows rows = 0 for all 30 days even after 30+ days post-deploy, check:
- Regex is exact (no extra spaces, proper escaped dots)
- Session source dimension (not Page referrer)
- Date range covers the period AFTER pillar publish (2026-04-21 onwards)

---

## 4. Recommended exploration to save

Build this exploration and save it as `AI Traffic — 30 day roll-up`:

| Config | Value |
|---|---|
| Technique | Free form |
| Segments | `All users`, `AI traffic` (comparison) |
| Dimensions | `Session source`, `Landing page + query string`, `Country` |
| Metrics | `Sessions`, `Engaged sessions`, `Session conversion rate`, `Engagement rate`, `Total revenue` *(if set up)* |
| Filter | Session source matches the regex |
| Date | Last 30 days — rolling |

Then export to PDF or screenshot monthly for the 30/60/90-day comparison tracking.

---

## 5. Secondary — look-like AI referrers via UTMs

If AI engines start attributing traffic via UTM parameters (Perplexity has been experimenting with this), you can catch those too. Add to the same segment as an OR condition:

- Dimension: `Session medium`
- Match type: **matches regex**
- Value: `ai|llm|assistant`

Most AI traffic today is `referral` medium, not a purpose-built medium, so this is a low-priority add.

---

## 6. What to do with the numbers

**Monthly check:**
- Sessions from AI traffic vs total sessions
- Most-cited landing pages (which pages are AI engines sending traffic to?)
- Engagement rate on AI traffic vs organic — AI traffic tends to have higher engagement because the user already has intent
- Conversion rate on AI traffic (do they book calls at all?) — this is the most important metric long-term

**If AI traffic hits 5% of sessions in any month within the first 6 months**, that's strong early evidence the entity + pillar + YouTube flywheel is working. Flag it in the next session log.

**If AI traffic is 0% at month 6**, escalate: either AI engines haven't indexed the pillar, or the entity sameAs chain is missing a node. Check C0 indexing report for pillar crawl status first.

---

## 7. Related

- AEO prompt tracking: [scripts/aeo-tracking-README.md](../scripts/aeo-tracking-README.md)
- GSC queries >7 words (proxy for AI-style queries) — check manually in Search Console monthly
- Baseline metrics (pre-AI traffic): [research/2026-04-21_setpoint-baseline/baseline.md](../../DeepReserch/research/2026-04-21_setpoint-baseline/baseline.md)
