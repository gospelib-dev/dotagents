# Nutrition targets and the brief for the meal planner

The trainer sets **targets**; the meal planner turns them into meals. Never send menus, recipes or shopping lists. Health numbers (weight, labs) are private: put computed targets in the brief, not raw measurements, and never in shared documents.

## 1. Energy
**Preferred tool:** NIH Body Weight Planner (Hall dynamic model; accounts for metabolic adaptation, gives a calorie level to reach a goal by a date and to maintain after). https://www.niddk.nih.gov/research-funding/at-niddk/labs-branches/laboratory-biological-modeling/integrative-physiology-section/research/body-weight-planner?dkrd=prspf0115
- The old "3,500 kcal = 1 lb" / "500 kcal/day = 1 lb/week" rule overestimates actual weight loss; do not use it for forecasts. https://newsinhealth.nih.gov/2016/01/online-weight-management-gets-personal ; https://pmc.ncbi.nlm.nih.gov/articles/PMC4035446

**Fallback:** Mifflin-St Jeor resting energy × activity factor (`fitness-nutrition` skill: `scripts/body_calc.py tdee`).
- Men: 10×kg + 6.25×cm − 5×age + 5; women: same −161 (Mifflin 1990, AJCN 51:241, doi 10.1093/ajcn/51.2.241; equation as reproduced https://pmc.ncbi.nlm.nih.gov/articles/PMC11948829 and https://europepmc.org/article/MED/42229949).
- Most accurate common equation, but only ~70–82% of people fall within ±10% of measured; errors up to ~20%. Treat as a starting range and correct from the 2–4-week weight trend. Frankenfield 2005 https://pubmed.ncbi.nlm.nih.gov/15883556
- Always give a **range** (e.g. ±100–150 kcal) not a single number.

**Deficit size (ISSN diets & body composition, Aragon 2017):** fat loss is driven by a sustained deficit; the higher the starting body fat, the more aggressively the deficit can be imposed; leaner people keep more lean mass with slower loss (0.7%/wk body weight outperformed 1.4%/wk in leaner athletes). Diet type (low-fat to low-carb) matters less than adherence; intermittent restriction shows no advantage over daily restriction. https://pmc.ncbi.nlm.nih.gov/articles/PMC5470183
- **My rule:** default rate ≈0.5–1% of body weight per week for people with weight to lose, slower (≤0.5%) as they get leaner; never very-low-calorie plans without a physician (screening file).

## 2. Protein
| Source | Recommendation |
|---|---|
| RDA | 0.8 g/kg/day (healthy adults) https://extension.okstate.edu/fact-sheets/the-new-dietary-guidelines-for-americans-2025-2030 |
| DGA 2025–2030 | 1.2–1.6 g/kg/day, protein at every meal https://cdn.realfood.gov/DGA.pdf |
| ISSN (Jäger 2017) | 1.4–2.0 g/kg/day for most exercising people; 20–40 g (≈0.25 g/kg) high-quality protein per dose, spread every 3–4 h https://pubmed.ncbi.nlm.nih.gov/28642676/ ; https://link.springer.com/article/10.1186/s12970-017-0177-8 |
| ISSN (Aragon 2017) | 2.3–3.1 g/kg fat-free mass may be needed for lean, resistance-trained people in a deficit |

**Disagreement / my rule:** DGA's range is for the general population; ISSN's is for exercising people. For a beginner doing resistance training, especially in a deficit, I target **1.4–1.6 g/kg/day** (the overlap of both), 25–40 g per meal; up to 2.0 g/kg if they train hard and want to preserve muscle while losing fat. In people with obesity, base it on a reasonable goal/adjusted weight rather than full current weight [coaching practice; flag to clinician/RD for kidney disease].

## 3. Fiber
- 14 g per 1,000 kcal (DRI-based goal), e.g. ~28 g at 2,000 kcal, 34 g at 2,400; >90% of women and 97% of men fall short. DGA 2020–2025 https://www.dietaryguidelines.gov/sites/default/files/2020-12/Dietary_Guidelines_for_Americans_2020-2025.pdf
- DGA 2025–2030 says prioritise fiber-rich whole grains (2–4 servings/day), vegetables 3 and fruit 2 servings at 2,000 kcal, high-fiber foods for gut health, but gives no gram target. https://cdn.realfood.gov/DGA.pdf
- **My rule:** use 14 g/1,000 kcal (the only quantified target) with the 2025 food-group servings.

## 4. Limits
| Item | DGA 2025–2030 (current) | DGA 2020–2025 (previous) |
|---|---|---|
| Added sugars | No amount recommended; ≤10 g per meal; avoid sugar-sweetened beverages | <10% of calories |
| Saturated fat | ≤10% of calories | <10% of calories |
| Sodium | <2,300 mg/day (14+); highly active people may need more to offset sweat | <2,300 mg/day |
| Highly processed foods | Avoid salty/sweet packaged snacks; limit refined carbs | (not a named category) |
Sources: https://cdn.realfood.gov/DGA.pdf ; https://cacfp.org/2026/01/08/2025-2030-dietary-guidelines-for-americans-released ; DGA 2020 (above). Commentary on the change and its internal tensions (e.g. saturated-fat messaging): https://nutritionsource.hsph.harvard.edu/2026/01/09/dietary-guidelines-for-americans-2025-2030

**My rule:** follow the current DGA 2025–2030 limits in briefs (official current guidance), and keep saturated fat ≤10% since both editions agree.

## 5. Hydration
Water and unsweetened drinks first (DGA 2025–2030).

## 6. The Nutrition targets brief (template — send exactly this shape)
```
NUTRITION TARGETS BRIEF — for the meal planner
For: <person>   From: trainer   Date: <date>   Review by: <date + 4 wk>
Goal: <e.g. gradual fat loss while building strength / maintenance / gain>
1. Daily energy: <low>–<high> kcal (method: <Body Weight Planner | Mifflin x factor>; adjust ±100–150 after 2–4 wk of weight trend)
2. Protein: <g>–<g> g/day (<1.4–1.6> g/kg), <25–40> g at each meal incl. any snack-meal
3. Fiber: ≥<g> g/day (14 g per 1,000 kcal)
4. Limits: added sugar ≤10 g/meal, no sugary drinks; sat fat ≤10% kcal (<g> g); sodium <2,300 mg
5. Timing/constraints: <meal pattern realities, e.g. early shift with no time to cook → needs make-ahead or grab-and-go options; training times; late-evening eating; allergies; budget; family-meal compatibility>
6. Favour: <protein foods the person eats, beans/lentils, whole grains, vegetables, fruit, plain dairy, water>
7. Limit: <highly processed snacks, sweetened drinks, fried foods>
8. Why: <one or two lines linking targets to the goal and training>
9. Not my call: menus, recipes, shopping list (meal planner); medical diets (clinician/RD)
```
Keep it under ~200 words. If a target conflicts with a medical diet, the clinician's instruction wins and the brief says so.
