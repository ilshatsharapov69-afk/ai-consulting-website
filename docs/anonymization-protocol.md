---
title: Anonymization Protocol — Case Study Publication
date: 2026-04-22
session: C4.3
status: protocol
tags: [privacy, case-study, anonymization]
---

# Anonymization Protocol

Rules for converting audit findings into a publishable case study without exposing client data. Applies regardless of which consent option the client picks ([A/B/C/D in consent template](./case-study-consent-template.md)); the stricter the option, the more of these rules apply cumulatively.

**Goal:** the case study tells the truth about what the audit found. It does not expose information the client would not want public. Both things can be true.

---

## 1. Revenue

**Always use buckets, never exact.**

| Exact figure | Published as |
|---|---|
| $127,000 | "under $500K" |
| $687,000 | "$500K–$1M" |
| $2,340,000 | "$2M–$3M" *(1M wide buckets above $1M)* |
| $8,900,000 | "$7M–$10M" |
| $12,400,000 | "$10M+" *(out of our ICP — rare) |

Reason: exact revenue + industry + region + revenue is often enough to identify a small business even with no name.

## 2. Dates

**Month/quarter, never specific day.**

| Exact | Published as |
|---|---|
| 2026-04-17 | "April 2026" or "Q2 2026" |
| "the week of March 3" | "early March" |
| "exactly 90 days after delivery" | "about 90 days after delivery" |

Reason: specific dates tied to specific industries can identify a client via news events, weather records, or calendar overlap.

## 3. Business name

- **Option A** (named): use exactly as client writes it. Don't abbreviate, don't capitalize differently.
- **Option B** (named business, no owner): same.
- **Option C** (anonymized): replace with a regional + industry descriptor:
  - `"a Midwest HVAC service business"`
  - `"a West Coast independent restaurant"`
  - `"a Southeast professional services firm"`
- **Option D** (fully anonymous): industry-type only, no region:
  - `"a professional services business"`
  - `"a multi-location retail operation"`

Never invent a fake business name — it implies specificity we didn't earn.

## 4. Owner / employee names

- **Option A**: first name + last initial OK ("Jennifer T." or "Jennifer"). Full name only if client explicitly confirms.
- **Option B, C, D**: no first names. Refer as "the owner" or "the client."

Never use a nickname not in the consent form.

## 5. Customer names — ALWAYS REDACT

Regardless of consent option: no customer names, no customer company names, no account identifiers, no deal sizes attributed to specific customers. If a finding is "Customer X is overdue $40,000," publish it as "one customer is overdue $40,000" or "a top-20 customer is overdue roughly $40K."

## 6. Named software / platforms — OK to name

You CAN name these (they're universal, not identifying):

- **Accounting:** QuickBooks, QuickBooks Online, Xero, Wave, FreshBooks
- **CRM:** HubSpot, Salesforce, Pipedrive, Zoho, Copper, Mindbody, Clio, Jobber, ServiceTitan
- **POS / payments:** Stripe, Square, Toast, Shopify, PayPal
- **Calendar / scheduling:** Google Calendar, Calendly, Acuity
- **Marketing / analytics:** Google Analytics, Meta Ads, Google Ads, Mailchimp

Reason: naming tools makes the case study legible. These platforms run millions of businesses; the mention doesn't identify one.

## 7. Tenant IDs, API keys, URLs — ALWAYS REDACT

If a finding requires referencing a system state, describe the state, not the identifier:

- NOT: "account ID `HUB_3481929`"
- YES: "the primary HubSpot portal"

- NOT: `https://clientname.shopify.com/admin/...`
- YES: "the client's Shopify admin view"

- NOT: API key fragment
- YES: never — just don't include.

## 8. Screenshots

**Default: don't use screenshots.** If a screenshot is the only way to convey a pattern, follow this protocol:

- Blur all personally identifiable data: customer names, amounts (unless specifically part of the finding), dates, email addresses
- Replace real data with placeholder if needed (but clearly mark the screenshot `[ILLUSTRATIVE]`)
- Prefer line-chart or table reproduction in Markdown over screenshots — easier to anonymize

## 9. Industry / region descriptors

If combining industry + region could identify the business (e.g., "the only kosher bakery in Portland"), loosen one:

- Specific industry, broad region: "a specialty bakery in the Pacific Northwest"
- Broad industry, specific region: "a food-service business in Portland"
- In extreme cases: drop both specifics

Rule of thumb: if a journalist with Google could find the client from the descriptors, the descriptors are too tight.

## 10. Quotes

- Only quote what the client approved in the consent review (see [consent template](./case-study-consent-template.md) section 6)
- Remove verbal tics and false starts unless they carry meaning ("um," "like," "you know")
- Don't "clean up" meaning — quotes stay true to intent
- If a quote contains identifying detail ("I've been running Setpoint Plumbing since 1998"), replace the identifying detail with a bracketed descriptor: "I've been running [my business] for over 25 years"

## 11. Follow-up data verification

If the case study includes 30/60/90-day outcome data:

- Prefer numbers the client provides, not ones you infer
- If client won't share exact follow-up numbers, publish the case study without them (see "what didn't get published" note)
- Never extrapolate ("they probably saved...") — it's either data or it isn't

## 12. Final review checklist — before publishing

Run through this list. One "no" = don't publish yet.

- [ ] Client signed or email-approved the consent form
- [ ] Chosen consent option (A/B/C/D) applied consistently throughout
- [ ] Revenue expressed as bucket, not exact
- [ ] Dates expressed as month/quarter, not day
- [ ] Customer names: 0 instances in the draft
- [ ] Tenant IDs / URLs / API keys: 0 instances
- [ ] Screenshots either absent or fully blurred + marked
- [ ] Industry + region combination not uniquely identifying
- [ ] Client reviewed the final draft at least 5 business days ago
- [ ] Client approved in writing (email reply is fine)
- [ ] Withdrawal clause communicated ("you can ask me to unpublish any time")
- [ ] Follow-up data: sourced from client directly, not inferred

---

## Concrete before/after example

**Raw audit finding (internal):**
> "Sunshine Kitchen & Bath Remodeling of Tampa, FL (owner: Michael R., 2.4M annual revenue) had 47 draft-status invoices totaling $181,400, dating from Jan 3 through March 28, 2026. Top overdue: Johnson Family Renovation, $24,100. Full list attached."

**Published version, Option C:**
> "A remodeling contractor in the Southeast ($2M–$3M revenue band) had 47 invoices sitting in draft status — totaling roughly $180K — with the oldest stretching back about three months. The top single unbilled invoice was in the low-$20K range on a residential project that had already been completed and closed out. Total: about $181K in completed work that hadn't been invoiced to the customer."

What survived: the finding (unbilled revenue, 47 invoices, ~$180K, oldest ~3 months). What dropped: business name, city, owner name, exact revenue, customer name, exact dollar amounts, exact dates. The case study still proves the pattern. The client stays private.

---

## Links

- Consent template: [case-study-consent-template.md](./case-study-consent-template.md)
- Case study blog template: [_template-case-study.md](../src/content/blog/_template-case-study.md)
- Audit methodology (pillar): [/blog/small-business-data-audit-guide/](../src/content/blog/small-business-data-audit-guide.md)
