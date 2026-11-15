# Legal and tax basics: US sole proprietor or single-member LLC

Not legal or tax advice. Use these official facts to frame questions; send decisions to a CPA/enrolled agent or attorney. Recheck figures each tax year.

Sources:
- [SBA] SBA, Launch your business (structure, registration, EIN, bank account): https://www.sba.gov/business-guide/launch-your-business/choose-business-structure
- [SE] IRS, Self-employment tax: https://www.irs.gov/businesses/small-businesses-self-employed/self-employment-tax-social-security-and-medicare-taxes
- [EST] IRS, Estimated taxes: https://www.irs.gov/businesses/small-businesses-self-employed/estimated-taxes
- [ESTI] IRS, Individuals — Estimated tax (FAQ): https://www.irs.gov/faqs/estimated-tax/individuals
- [SBA2] SBA, Launch your business (licenses, permits, registration, DBA): https://www.sba.gov/counseling/launch-your-business/
- [SMLLC] IRS, Single member LLCs: https://www.irs.gov/businesses/small-businesses-self-employed/single-member-limited-liability-companies
- [EIN] IRS, Get an EIN: https://www.irs.gov/businesses/small-businesses-self-employed/get-an-employer-identification-number
- [HO] IRS, Simplified option for home office deduction: https://www.irs.gov/businesses/small-businesses-self-employed/simplified-option-for-home-office-deduction
- [1099K] IRS, Understanding your Form 1099-K: https://www.irs.gov/businesses/understanding-your-form-1099-k
- [HOB] IRS Tax Tip 2022-57, hobby vs business (marked archival by IRS): https://www.irs.gov/newsroom/heres-how-to-tell-the-difference-between-a-hobby-and-a-business-for-tax-purposes
- [BOI] FinCEN, Beneficial Ownership Information: https://www.fincen.gov/boi
- [STAX] Stripe, Introduction to SaaS taxability in the US: https://stripe.com/guides/introduction-to-saas-taxability-in-the-us
- [SCORE] SCORE, How mentoring works: https://www.score.org/how-mentoring-works/

## Structure [SBA][SMLLC]
| | Sole proprietorship | Single-member LLC (default tax treatment) |
|---|---|---|
| Setup | Entity form is automatic when you do business without registering another type; state/local registration, tax IDs, DBA, zoning, licenses and permits may still apply [SBA][SBA2] | Formed under state statute; state filing and fees vary [SBA][SMLLC] |
| Liability | Unlimited personal liability; assets not separate [SBA] | Owners generally not personally liable [SBA] |
| Federal income tax | Schedule C on Form 1040 [SMLLC] | Disregarded entity: reported on owner's 1040 (Schedule C for a business) unless it elects corporate treatment on Form 8832 [SMLLC] |
| Self-employment tax | Yes [SBA] | Yes, same as a sole proprietor [SMLLC][SBA] |
| SBA's fit guidance | Low-risk businesses; owners testing an idea before forming something formal [SBA] | Medium/higher-risk businesses; owners with significant personal assets to protect [SBA] |
SBA: converting later is possible but may have restrictions and tax consequences; consult counselors, attorneys and accountants [SBA]. Doing business under your legal name may need no registration; a trade name (DBA) is registered with state/local government [SBA].

## IDs and banking
- EIN is free from the IRS online and issued immediately if approved; "You never have to pay a fee for an EIN." The online session expires after 15 minutes of inactivity [EIN].
- A single-member disregarded LLC with no employees and no excise tax liability does not need an EIN for federal tax purposes; it uses the owner's TIN; but "most new single-member LLCs" will need one for employment/excise purposes or other reasons [SMLLC]. Banks commonly ask for one; SBA says you can open a business bank account once you have your EIN [SBA].
- SBA: open a business bank account as soon as you start accepting or spending money as the business; it keeps business and personal funds separate [SBA].
- FinCEN BOI (updated Aug 11, 2026): U.S. companies are exempt from BOI reporting [BOI]. Ignore services that charge to file BOI for a U.S. company.

## Federal tax facts [SE][EST][HO][1099K]
| Item | Figure | Source |
|---|---|---|
| Self-employment tax rate | 15.3% (12.4% Social Security + 2.9% Medicare), via Schedule SE | [SE] |
| Social Security wage base 2026 | First $184,500 of combined wages and net earnings | [SE] |
| Additional Medicare tax | 0.9% above $250,000 MFJ / $200,000 single | [SE] |
| Deduction | Employer-equivalent half of SE tax is deductible in figuring AGI | [SE] |
| Estimated tax trigger | Generally required only if BOTH: (a) you expect to owe at least $1,000 after withholding and refundable credits, AND (b) withholding and refundable credits will be less than the smaller of 90% of current-year tax or 100% of prior-year tax (110% if prior-year AGI was over $150,000, $75,000 MFS). Special rules apply (e.g. farmers/fishermen, no prior-year liability). Work it through Form 1040-ES / Publication 505; penalties can apply for underpaying or paying late | [EST][ESTI] |
| Home office (simplified) | $5 per square foot, maximum 300 square feet; requires regular and exclusive use and principal place of business | [HO] |
| Form 1099-K | Platforms report when payments exceed $20,000 in more than 200 transactions; may send for less. All business income must be reported regardless | [1099K] |
SE tax filing threshold ($400 net earnings) is commonly cited; not verified on a page fetched for this skill; confirm on the Schedule SE instructions.

## Hobby vs business [HOB]
IRS factors include: businesslike manner with complete books; time and effort showing intent to profit; dependence on the income; changing methods to improve profitability; losses normal for the startup phase. "No one factor is more important than another." The page is marked archival; confirm current rules with a professional. Practical step: keep books from the first dollar.

## Sales tax [STAX]
Stripe reports 25 states tax SaaS and 7 more tax it if customers must download software; rules differ by state. Before collecting meaningful revenue across states, ask a tax professional about registration duties.

## Free help
- SCORE mentoring is free for any aspiring or established owner of a U.S.-based business, "for the life of your business"; matching is online by ZIP code and messages can be sent through the site [SCORE].
- SBA lists resource partners (SBDCs, Women's Business Centers, VBOCs) with free to low-cost counseling [SBA].

## First-revenue checklist (to hand to the owner; each item is theirs to decide)
1. Keep a simple ledger from the first payment (date, customer, amount, fees, expenses, receipts).
2. Separate account for business money (SBA recommendation).
3. Set aside a share of net profit for SE and income tax; ask a CPA/EA for the percentage and whether quarterly estimates apply.
4. Payment processor in the owner's name/EIN; no paid EIN or BOI services.
5. Before an LLC: is there real liability exposure or significant assets? If yes, attorney/CPA consult.
