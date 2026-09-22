# Completion and remaining business uncertainty

## Deliverable completion: 12 / 12 = 100%

This measures the checklist below under the requested descriptive fallback. It does not mean a future-churn model, an intervention, or a causal explanation has been delivered.

| Completed deliverable | Evidence |
|---|---|
| Source, licence, collection-period and label audit, including unknowns | [Source audit](source_and_dictionary.md) |
| Row-grain, identifier, missingness, duplicate and value validation; source preserved | [Cleaning log](cleaning_log.json) |
| Six executable DuckDB SQL analyses | [SQL directory](../sql/) |
| Label distribution, engagement comparisons and supported segments | [Findings](business_findings.md) |
| Six actual charts, visually inspected, with underlying tables | [Figure index](tables/figure_index.csv) |
| Prediction feasibility assessment and required-data proposal | [Feasibility](model_feasibility.md) |
| Three evidence-linked recommendations, targets and success metrics | [Recommendations](business_findings.md) |
| Proposed institution-level controlled experiment | [Experiment](business_findings.md) |
| Executed notebook with charts and zero error outputs | [Notebook execution](notebook_execution.json) |
| README, pinned direct dependencies and exact run instructions | [README](../README.md) |
| Independent SQL/Pandas agreement and validation checks | [Verification](verification.json) |
| Three resume bullets restricted to verified work | [Resume bullets](resume_bullets.md) |

## Business-question coverage: 2 / 4 = 50%

This is an explicit, equally weighted question-count measure chosen for this case study, not an industry score or a percentage of the company's churn problem solved.

1. Describe the supplied churn labels: **answered**, with observation-window limitations.
2. Identify engagement associations and groups worth investigating: **answered descriptively**, without causal or risk-ranking claims.
3. Validate prediction of future churn: **unresolved**; label lineage, feature timing and dated snapshots are insufficient.
4. Demonstrate that an intervention improves retention: **unresolved**; no experiment has been implemented.

**Measured churn reduction or revenue improvement: unknown, not measured.**

## Final quality assurance

- 130 independent SQL/Pandas comparisons passed.
- All eight notebook code cells executed with zero error outputs.
- All six PNGs were visually inspected for readable titles, units, denominators, footnotes and clipping. Chart 5 explicitly discloses log1p spacing and whisker calculation.
- Original CSV checksum and equality of raw/processed values passed; no source rows or values changed.
- Four invalid-input cases were rejected; distinct institutions with matching profiles remained valid.
- No unsupported model, cohort chart, raw-event analysis or measured campaign outcome is included.

The packaged release records these checks. Re-execute the analysis and notebook after any code/data changes; the manual visual review is specific to the delivered charts.
