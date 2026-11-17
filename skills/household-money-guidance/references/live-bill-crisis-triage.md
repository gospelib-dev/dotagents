# Live Bill-Crisis Triage From Read-Only Account Data

## When to Use

Use this procedure when the household says bills are overdue, cash is short, automatic payments have failed, or the next month looks unaffordable. It finds what is actually unresolved without mistaking every connector error for a delinquent bill.

## 1. Freeze and enforce scope

1. Obtain written agreement on the included people/entities, account classes, data window, report contents, and actions that remain forbidden.
2. Build explicit included and excluded account sets from the live account list. Exclude business, trust, child, and investment accounts unless the agreed scope names them; an account being visible does not put it in scope.
3. Record an exact cutoff timestamp and household timezone. Use the same cutoff and window on every ledger query.

## 2. Establish cash that is actually known

1. For a multi-account request, call `getAllBalances` first and follow its live assembly instructions.
2. Call `listAccounts` with the largest page size and continue until `hasNextPage` is false.
3. Call `getAccount` concurrently for every included account, skipping a linked half when the first response already contains its live balance.
4. Classify every result before totaling:
   - managed pod, income source, or depository balance: asset;
   - credit card or loan: liability, never cash;
   - investment: outside bill-paying cash unless explicitly included;
   - linked liability and payment pod: two economic roles, not duplicates.
5. Use `availableBalanceInCents` rather than `balanceInCents` when holds exist. Keep integer cents through all calculations.
6. Report three cash figures separately when present:
   - known available cash;
   - named or earmarked bill-pod cash;
   - balances unavailable because of login, provider, permission, or stale-data errors.

Never present a complete household cash total while an included depository account is unavailable. Name the missing account, not its internal ID, and make reconnection the first physical action when it blocks the decision.

## 3. Reconcile overdue candidates from transfer history

1. Query `listTransfers` across every included managed account for an exact recent window, normally 90 days, with `executionMode=LIVE` and the largest page size. Continue until `hasNextPage` is false.
2. Use `listExternalTransactions` as supplemental evidence for activity on included connected accounts; do not substitute it for managed-account transfer history.
3. Extract external bill pulls and payments. Ignore internal routing when identifying whether a creditor was paid.
4. For each candidate bill pod, run targeted `listAccountTransfers` with `accountRole=source` and `direction=MONEY_OUT`. This compact history is the verification pass after the broad ledger query.
5. Normalize each obligation by source account, payee/description, amount, and billing cycle. Treat an initial failure and its near-date retry as one obligation, not two bills.
6. Mark an obligation **resolved** when a later completed transfer matches the failed attempt or retry. Do not list it as overdue or recommend paying it again.
7. When the account holder reports that a payment was made after the ledger cutoff or through another account, treat that firsthand confirmation as the current working status even if the connector has not posted it. Refresh same-day managed transfers, external transactions, and the funding balance; then label the payment “confirmed paid by account holder; connector not yet posted” rather than leaving it in the overdue total. This prevents sync lag from overriding newer evidence.
8. Mark an obligation **unresolved failed pull** only when neither a later matching completion nor a current account-holder confirmation exists through the cutoff. This is still not proof of creditor delinquency: it could have been paid outside the connector. Say “potentially overdue” or “unresolved in the connector” until the creditor portal confirms status.
9. Preserve ambiguous destination labels literally and describe them as labels. Never guess which creditor or account a mixed or truncated payee name represents.

## 4. Estimate upcoming bills conservatively

1. Infer recurrence only when the history shows a repeatable payee and cadence.
2. Use the most recent completed or attempted amount for the next-cycle estimate; show a range or “recent amount” when it varies materially.
3. Treat connector timestamps as posting dates, not contractual due dates. State “around” or “historically posted near” unless a current statement or account field supports an exact due date.
4. Ignore stale `nextPaymentDueDate`, minimum, statement, or balance fields as current evidence. Include their as-of date when they remain useful historical context.
5. Do not use `getFinancialProfile` bill fields when the BILLS confidence is `LOW`, and do not let a narrow `accountsCount` stand in for the scoped account set. A profile is a cross-check, not the authoritative live bill ledger.

## 5. Project income without manufacturing certainty

1. Run targeted `listAccountTransfers` on each included income source with `accountRole=destination` and `direction=MONEY_IN`.
2. Group deposits by source description before inferring cadence; one income account can receive weekly and monthly payroll streams.
3. Derive future dates from observed intervals and compute variable-pay estimates with the median in integer cents. Do not use one unusually high or low deposit as the norm.
4. Project only through the agreed horizon and label every future deposit as expected, not guaranteed.
5. Compare expected inflows with unresolved and upcoming obligations, but never recommend committing every projected dollar. Reserve housing-adjacent essentials, food, utilities, insurance, transportation, and other known living costs first.

## 6. Calculate the triage gap

1. Map each unresolved bill to its matching pod or funding account.
2. Show `unresolved amount - matching available balance = preliminary gap` for decision support.
3. If one pod funds several creditors, show the shared balance once and identify the competing claims; do not pretend each creditor independently has the full pod balance.
4. Keep inaccessible depository balances outside the gap calculation and state that the gap is preliminary.
5. Keep already completed payments in a short “do not pay twice” list.

## 7. Find written assistance before suggesting contact

For every at-risk priority bill, check the creditor’s official current site for a portal message, secure chat, direct message, online hardship application, email, or mailed form. When the visible short-term path is phone-only, say so and use the documented written application or message route instead; never turn a phone number into the household’s action item.

A written request should ask for:
- the exact amount required to become current;
- fees already assessed and whether credit reporting has occurred;
- a fee waiver, due-date change, repayment plan, short deferral, or forbearance option;
- processing time and written confirmation.

Do not promise a payment amount or date until known available cash and essential expenses support it.

## 8. Report in a calm, startable shape

Lead with one sentence that distinguishes a timing problem from a total-income problem only when the data supports that distinction. Then use this order:

1. as-of timestamp and known-cash limitation;
2. total unresolved failed pulls and a prioritized table: obligation, amount, last failed date, matching available balance, status confidence;
3. payments already completed, to prevent duplicates;
4. near-term expected deposits and upcoming recurring bills, clearly labeled as estimates;
5. one first physical action, normally reconnecting the most important missing depository account or opening the highest-priority creditor portal;
6. housing, essential utilities, income-preserving secured debt, insurance, and court/tax obligations before unsecured minimums and nonessential items;
7. exact written portal routes for anything that cannot be paid safely.

Exclude raw transaction histories, account IDs, full account numbers, and irrelevant liability totals. End by stating that no money moved and no rule or autopay changed.

## Pitfalls

- Reconcile retries before totaling failures — the initial attempt and retry are one obligation, and a successful retry removes it from the overdue list.
- Finish pagination before declaring totals — busy managed accounts can exceed several hundred transfers in a 90-day window.
- Prefer targeted account-transfer histories for the final verification pass — a broad multi-account ledger is complete but hard to audit bill by bill.
- Separate known cash from inaccessible cash — treating login-required balances as zero fabricates a shortfall.
- Use available rather than ledger balance when holds exist — held money cannot safely fund a bill.
- Keep forecast income and observed cash in separate columns — expected deposits are not current funds.
- Do not let a low-confidence or narrow financial profile override the scoped live ledger — aggregation can omit the very bills under triage.
