---
name: reconciled-spending-reports
description: Use when reporting household spending, income or balances to the exact cent.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Reconciled household spending reports

## Purpose
Produce exact, calm household money reports from read-only financial data. A short answer that
reconciles beats a broad dashboard that does not answer the question. The method: freeze the scope,
enumerate accounts, collect every transaction rail, reconcile before summing, verify with integer
arithmetic, classify conservatively, and report one total with a breakdown that adds up.

## When to use
- Month-to-date or period spending totals; category breakdowns.
- Cash-outflow summaries, income totals, balance reports, net cash flow.
- Reconciliation across connected bank and card accounts, provider-managed sub-accounts and
  transfers.
- Any household-facing number that must be backed by an auditable calculation.
- Not for moving money, changing automations, or investment advice.

## Method
1. **Freeze the scope before reading data.** Write down the included people/entities, account
   classes, date range, timezone, and the measure: spending, cash outflow, income, balance, or net
   cash flow. Use the agreed scope literally; keep business, trust, investment or child accounts
   out of a household total unless the requester includes them. Record an exact cutoff timestamp;
   "today" without a timezone is not reproducible.
2. **Enumerate accounts first.** Fetch the complete active account list and follow pagination.
   Separate connected external accounts from provider-managed sub-accounts (envelopes, pods,
   buckets) and income sources; separate depository, liability, investment, loan and business
   accounts before choosing what is in scope.
3. **Collect every rail that can affect the measure.** External account activity, the provider's
   own card purchases, and transfers between accounts are often separate sources; query all of them
   for the same window. Use the largest page size and follow pagination to the end; a first page is
   not a total. Use settled entries for posted-spend totals unless pending activity is requested.
4. **Reconcile before summing.** Count purchases and paid bills once. Exclude internal routing,
   savings moves and credit-card payments from "spending" (they move or settle money; they do not
   create a purchase); include them only for cash outflow. Deduplicate mirrored activity across
   rails by account relationship, amount, merchant and nearby timestamps, never on amount alone.
   Keep refunds as negative spending.
5. **Verify with deterministic arithmetic.** Money as integer cents until formatting; dedupe by
   transaction ID within each source; assert category totals plus "Other" equal the total exactly.
   Record transaction count, sources checked, pagination completion and exclusions in working notes.
6. **Classify conservatively.** Prefer provider categories; otherwise a few plain categories
   inferred from merchants. Put uncertain small items in "Other"; disclose ambiguity that could
   change a top category.
7. **Report for the household.** Lead with one total and the exact period/cutoff; give three to
   five largest categories then "Other" so the breakdown reconciles; add one short method note
   (settled vs pending, main exclusions). Neutral tone; never moralize about past spending.

Source matrix, query order, mirror rules and a verification snippet:
`references/multi-rail-reconciliation.md`.

## Pitfalls
- Querying only the obvious "spending" account and missing cards funded from other buckets.
- Treating a cached monthly profile or snapshot as the month-to-date ledger.
- Counting both a card purchase and the card payment in "spending".
- Deduplicating on amount alone (legitimate same-value purchases exist).
- Rounding category percentages and subtracting them instead of computing "Other" in cents.
- Exposing raw transactions when only a total was asked for.

## Verification
- The account set matches the agreed scope; every rail and page was checked.
- Payments and mirrored transactions are not double-counted.
- Integer-cent category totals reconcile exactly to the reported total.
- The report states its cutoff and pending-data treatment and is short enough to relay unchanged.

## Household specifics
This skill is the method only. The agent's own local skill supplies the data provider, its exact
query names and account types, which accounts and people are in the household scope, and any
known mirroring between the household's accounts.

## References
- `references/multi-rail-reconciliation.md`
