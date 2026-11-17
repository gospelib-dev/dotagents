
# Sequence Bill-Funding Rule Design

## When to Use

Use this procedure to design read-only proposals for Sequence rules that keep recurring payments funded. It is for rule architecture and verification, not for creating or changing rules.

## 1. Establish contractual inputs

1. Enumerate every payment in scope: payee, funding pod, contractual due date, expected amount, whether the creditor pulls funds or Sequence pushes payment, and whether the amount is fixed or variable.
2. Read current statements or creditor portals for due dates and amounts. Treat transaction timestamps only as historical posting dates; use them to propose tentative staging dates, never to claim a contractual due date.
3. For variable liabilities, prefer Sequence's supported minimum-due, statement-balance, total-due, or capped liability action when live liability data is current. Otherwise use a conservative fixed reserve and state how it must be reviewed.
4. Round reserve targets upward deliberately and show the buffer. Never hide a guessed amount inside a precise-looking target.

## 2. Audit the existing automation before designing

1. Call `listRules`, paginate fully, then call `getRule` for every rule touching an income source, transit pod, bill pod, or liability in scope.
2. Inspect recent `listRuleExecutions` for skipped, failed, partial, approval-pending, and successful behavior. A rule description is not proof that its branches actually fund the intended pod.
3. Map trigger, conditions, ordered actions, source, destination, cap, and schedule. Flag these conflicts before proposing replacements:
   - a transfer-amount threshold that excludes normal paychecks;
   - a target below the current bill;
   - a fallback branch that omits a priority bill;
   - two rules funding the same destination from different shared pods;
   - a scheduled rule that cannibalizes a pod needed by another creditor;
   - a liability-payment rule whose source reserve is smaller than its cap.
4. Preserve unrelated income, tax, tithing, or savings rules unless the requested design explicitly changes them.

## 3. Choose the built-in pattern

Prefer the smallest supported design that separates bill money from spending money:

1. **Transit:** income sources route into the existing income/transit pod.
2. **Bills Queue:** create one dedicated pod that receives the bill share of each deposit.
3. **Incoming split:** use an incoming-funds rule to split net income between Bills Queue and Spend. Derive the percentage from verified monthly bill targets divided by conservative monthly net income, then add a visible buffer.
4. **Staged funding:** use monthly scheduled rules a few days before each due-date group. Each rule performs ordered `Top Up` actions from Bills Queue to the existing bill pods.
5. **Payment:** keep creditor ACH pulls or supported liability-payment rules only after their funding pod is filled before the pull date.

Use a shared bill pod only when its staged cumulative targets are explicit. For example, if one card pod funds three creditors, top it up to the first creditor's reserve before the first due date, then to the cumulative two-creditor reserve before the second. This preserves existing ACH setup without pretending each creditor has the entire shared balance.

Dedicated per-creditor pods are safer when amounts vary independently or one creditor can drain another's reserve, but they require changing the creditor's funding account. Do not recommend that migration unless its maintenance cost is justified.

## 4. Order actions by consequence and timing

1. Housing first, then essential utilities, income-preserving secured debt, insurance or court/tax obligations, unsecured minimums, and discretionary services.
2. Within a priority class, order by the verified due date and payment processing lead time.
3. Sequence executes ordinary actions in order. Put the most important Top Up first because an insufficient source can consume the remaining balance and leave later actions unfunded.
4. Use Top Up rather than repeated fixed transfers when leftovers should roll forward. Top Up moves only the deficit to the target and may transfer all available money when the source is short.
5. Use limits on variable liability payments so one unexpectedly high balance cannot drain reserves for later bills.

## 5. Separate catch-up from steady state

A stable rule set cannot instantly repair an overdue cycle. Build two explicit phases:

1. **Catch-up phase:** route a temporarily larger share of incoming money to the highest-priority overdue bill or Bills Queue until the current cycle is funded. Give the exact disable/switch point.
2. **Steady state:** enable the sustainable incoming split and staged monthly top-ups only after the current cycle is caught up.
3. Never layer the replacement on top of the old income-distribution rule. State which old rule must be paused and which payment rules remain.
4. If changing a trigger requires recreating a rule, say so; Sequence triggers are not editable after creation.

## 6. Prove the design with deterministic arithmetic

Keep cents as integers and calculate:

- maximum monthly bill target;
- conservative monthly net income by source;
- `bill target / net income` funding ratio;
- proposed Bills Queue percentage and monthly buffer;
- cash available before each staged funding date;
- cumulative target for every shared pod;
- remaining Spend allocation after bill funding.

Use median variable income and observed cadence, not the highest paycheck. Include only expected deposits that arrive before each scheduled rule. If any stage is short, move the rule later only when the creditor's processing window allows it; otherwise reduce lower-priority payments, obtain a written arrangement, or say the design cannot guarantee every due date.

Do not say automation “ensures” funding merely because the monthly total works. Timing must work at every scheduled stage, and food, fuel, insurance, and other essential outflows must remain viable.

## 7. Transition and verification checklist

Before the human enables anything:

- contractual amounts and due dates verified;
- new rules created but not yet competing with old rules;
- old conflicting rules identified by name;
- scheduled dates respect weekends, processing lead time, and household policy;
- variable payments capped;
- one complete cycle simulated or manually calculated;
- current overdue cycle handled separately;
- first execution reviewed in Sequence;
- a recurring human review task assigned to the household task owner for variable statements and failed-rule notices.

Report the proposal in this order: rules to keep, rules to pause, new account/pod, incoming rule, scheduled rules in execution order, monthly arithmetic, catch-up transition, statement facts still needing confirmation, and the read-only/no-change statement.

## Pitfalls

- Do not equate an `EXECUTED` rule status with correct allocation — a fallback branch can execute successfully while omitting the bill that mattered.
- Do not use percentages alone for fixed due-date obligations — variable income can leave a fixed bill short even when the annual average works.
- Do not top up a shared source pod from another shared bill pod — the later rule can steal money reserved for a different creditor.
- Do not schedule all monthly funding on one date unless the reserve is already one full cycle ahead — a catch-up household may need staged funding around actual income dates.
- Do not derive exact due dates from ACH posting history — weekends, retries, and lender processing shift posting dates.
- Do not hide the setup transition — duplicate rules can move the same income twice or drain the wrong source before the replacement is ready.

## Official mechanism references

- Rules overview: https://support.getsequence.io/hc/en-us/articles/34371183108243-Rules-Overview
- Triggers: https://support.getsequence.io/hc/en-us/articles/34371275427219
- Conditions and Else branches: https://support.getsequence.io/hc/en-us/articles/34371347538963
- Ordered actions: https://support.getsequence.io/hc/en-us/articles/34372536007315
- Action types, Top Up, liability payments, and limits: https://support.getsequence.io/hc/en-us/articles/34372744192275-Action-Types
