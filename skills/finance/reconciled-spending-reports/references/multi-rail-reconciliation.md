# Multi-rail spending reconciliation

Use for exact spending or cash-outflow totals when a household's money flows through more than one
data rail (for example a banking or budgeting provider that links external accounts and also issues
its own cards and moves money between sub-accounts).

## Source matrix (generic)

| Source | Include for posted spending | Main pitfall |
|---|---:|---|
| Connected external bank, wallet, credit card or loan transactions | Yes, for purchases and bills | A wallet or card entry can mirror a purchase funded through the provider's own card. |
| The provider's own debit/card transactions, per funding sub-account | Yes | Querying only the obvious "spend" bucket misses cards funded from other buckets (subscriptions, utilities). |
| Transfers between managed accounts | Only for true external bills or purchases | Internal moves and credit-card payments are not new spending. |
| Financial profile / snapshot summaries | Cross-check only | Can be monthly, cached, still processing, or over a different window; not the month-to-date ledger. |

## Query order
1. List all accounts with the largest page size; continue until there is no next page.
2. Build two explicit ID sets: included external accounts; included managed sub-accounts and income
   sources.
3. Query external transactions for the exact RFC 3339 window, completed status, outward direction
   when the API supports it.
4. Query card transactions for every included managed account (settled, separate from external
   activity).
5. Query completed outgoing transfers across included managed accounts.
6. Follow pagination on every nonempty source before calculating.

## Reconciliation rules
- "Spending" = purchases and consumed services, not movement between the household's own accounts.
- Exclude a credit-card payment when the underlying purchases are counted. For cash-outflow reports,
  include the payment but do not also count the card purchases in that total.
- Exclude transfers to savings, investments, tax buckets or other owned accounts unless the measure
  is allocation or cash movement.
- Match possible mirrors on amount, normalized merchant/description, linked accounts and nearby
  dates; never on amount alone.
- Treat provider categories as evidence, not identity.
- Keep a brief exclusion ledger ("internal transfer", "credit-card payment", "mirrored wallet entry")
  so the method note is auditable without exposing raw transactions.

## Minimal verification snippet

```python
included = {row["id"]: row for row in rows}
assert len(included) == len(rows), "duplicate transaction id"
total_cents = sum(row["signed_cents"] for row in included.values())
assert sum(category_cents.values()) == total_cents
```

If the report shows only top categories, compute "Other" as the exact cent remainder rather than
rounding each percentage and subtracting percentages.
