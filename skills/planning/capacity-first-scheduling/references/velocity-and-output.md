# Velocity detail and output template

## Velocity
- **Record per planned day:** planned task minutes (padded, mandatory + suggested) and completed
  task minutes (padded estimates of what was checked off or reported done). Store it where the
  household's data docs say; if nowhere is defined, report the numbers in your output.
- **Compute:** r = sum(completed) / sum(planned) over a rolling window of the last 10 planned
  days (minimum 5; with fewer use v = 1.0 and say "velocity: insufficient data"). Exclude days
  marked sick, travel or emergency and the household's rest days. Use the sum, not the average of
  daily ratios, so one tiny day does not swing the result.
- **Apply** (v multiplies capacity; starts at 1.0; bounds 0.4-1.0):
  - r < 0.6 -> v = v x 0.8 (the plan is badly over)
  - 0.6 <= r < 0.8 -> v = v x 0.9
  - 0.8 <= r < 0.95 -> hold
  - r >= 0.95 for 5+ consecutive planned days -> v = min(1.0, v x 1.1)
  - Change v at most once per week (at the weekly build). Daily builds use the current v.
  - Mandatory items are always placed even when v is low; v trims suggested items and box count.
- **Calibration factor:** when actual minutes are reported, track actual/estimate per task kind
  (median, 3+ samples, bounded 0.7-3) and use it for padding.
- A simpler variant used by some planners: planned load = completion rate over ~2 weeks x capacity,
  rounded down; under 60% done last week -> lighter week; over 90% -> add a little.
- Framing: velocity is information, not judgement. Unfinished work returns to the backlog and is
  re-placed on merit; never an "overdue pile", never guilt language.

## Generic output template
One line per item, "none" for empty sections. If the coordinator expects machine-readable output,
emit the same data as JSON and build the text from it so they agree.

```
Plan: <weekly|daily|replan|chat> <date range>  capacity <min>/<available min>  velocity r=<0.00> v=<0.00> (<changed from x|held|insufficient data>)
Written:
- <+|~|-> <day> <HH:MM-HH:MM> <box title> [<mandatory n / suggested n>]
Dropped/Deferred:
- <task> -> <new day|backlog> : <reason>
At risk:
- <task> due <date> : <why, what would fix it>
Needs human:
- <item> : <action the person must do | money decision | conflicting rule | missing data>
Conflicts with data docs:
- none
```
(+ created, ~ changed, - removed.) Also report hour totals per category vs target when the person
keeps targets, and one-line trade-off notes crediting each input source.

Box titles name the area or theme, not a task; tasks go in the description as mandatory and
suggested lines in the household's notation. Times in the person's preferred clock format.
