# Business findings

## Decision brief
The immediate priority is to validate the account population and activity measurements before launching retention targeting. This snapshot supports descriptive diagnosis; it cannot independently validate future churn predictions or prove a retention intervention works.

## Measured findings
1. **1,017/1,083 institutions (93.91%) are churn-labelled; 66 are active-labelled.** This is the supplied snapshot label share. The observation window ends before 2026-05-01 according to the source; its start and the future outcome window are not disclosed. It is not a monthly or annual business churn rate. Evidence: [SQL/Python headline](tables/01_headline.csv), [label chart](../images/02_churn_labels.png).
2. **Zero registered students: 732/737 (99.32%) churn-labelled.** For 51+ registered students, the corresponding value is 16/50 (32.00%). Difference: 67.32 percentage points. This is an association, potentially influenced by account eligibility, institutional size, tenure and the label definition. Evidence: [student bands](tables/03_student_segments.csv), [chart](../images/04_student_segments.png).
3. **Materials recorded: 23/46 (50.00%) churn-labelled**, versus 994/1,037 (95.85%) with no materials recorded. Smaller sample size and unmeasured confounding prevent a causal claim about publishing materials. Evidence: [material segments](tables/05_material_segments.csv).
4. **Attendance and assessment counts are zero for every institution.** All seven supplied indicators are zero for 486 institutions. 16 institutions have a positive engagement score although all six count fields are zero; 5 have materials recorded but a zero score. These are questions about score semantics, not proven errors. Evidence: [quality profile](tables/data_quality.csv), [review groups](tables/06_review_groups.csv).
5. **19/66 active-labelled institutions lack a recorded teacher or class.** 43/66 have no materials recorded. Confirm present status and whether the relevant features apply before proposing contact. Evidence: [review groups](tables/06_review_groups.csv), [institution review list](tables/institution_review_list.csv).

## Three recommended actions
| Action | Evidence and target | Owner | Success measurement |
|---|---|---|---|
| Validate the account denominator and event capture | Review the 737 zero-student institutions; audit the two constant activity fields and 21 score/count review cases | Data analyst + data engineer + customer operations | Proportion with verified account status; documented event completeness; reconciled label denominator |
| Pilot guided setup for confirmed eligible active accounts | 19 active-labelled institutions have no teacher or no class recorded; this is a retrospective review group | Customer success + product onboarding | Verified setup completion within 14 days; qualifying product activity within 30 days; support burden |
| Test material-workflow assistance | 43 active-labelled institutions have zero materials; compare against the descriptive material association | Product education + customer success | First qualifying material action; 30-day qualifying activity; incremental effect versus control |

Review groups overlap; 69 unique institutions match at least one documented review condition. They are not a validated churn-risk ranking. No company contact, campaign or experiment has been executed.

## Proposed experiment
First obtain current snapshots, verified account eligibility and a written activity definition. Randomise at institution level between standard support and one clearly defined guided-onboarding intervention. Stratify on baseline institution size and setup status; do not randomise individual teachers within an institution.

Primary outcome: institution has a pre-specified qualifying product event in days 31-60 after assignment, measuring continued activity after onboarding. Report treatment minus control in percentage points, with an interval and intention-to-treat denominator. Secondary outcomes: 14-day setup completion and first material action within 30 days; guardrails: support burden, complaints and opt-outs. This measures activity retention, not paid renewal. Paid retention needs actual subscription renewal records.

The 66 active-labelled accounts are a historical snapshot, not a sufficient recruitment or power calculation. Set the minimum meaningful effect and calculate sample size using fresh baseline data; if too small, run a feasibility pilot and report uncertainty rather than success. Avoid peeking and multiple unplanned tests.

## Proof and limits
- 130 independent SQL/Pandas comparisons pass, including headline counts, segments and engagement summaries: [reconciliation](tables/reconciliation_checks.csv).
- Missing cells: 0; duplicate full rows: 0; duplicate IDs: 0; removed rows: 0. Matching profiles across different institutions are preserved.
- Labels, demographics, tenure and selection criteria are incomplete; the sample is not claimed to represent all SaaS companies.
- [Prediction feasibility](model_feasibility.md) explains why there are no model scores or SHAP images.
- **Business-question coverage: 2 of 4 questions answered (50%)**: describe supplied labels and engagement patterns. Future prediction and actual intervention effectiveness remain unresolved. This is an explicit question-count measure, not a percentage of churn prevented.
