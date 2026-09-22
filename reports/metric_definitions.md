# Metric definitions

- **Institutions:** count of rows after verifying unique institution_id. One organisation per row.
- **Churn-labelled share:** count(churn_label = 1) / all eligible rows in the released snapshot. It is not a monthly churn rate; actual source eligibility is undocumented.
- **Within-segment churn share:** count(label = 1 AND segment) / count(segment). Show the denominator.
- **Contribution to churn labels:** count(label = 1 AND segment) / all label = 1 rows; distinct from within-segment risk.
- **Positive recorded-value share:** count(metric > 0) / institutions in that label group. A positive registered-student count is not evidence of recent activity.
- **Student bands:** 0, 1-10, 11-50, 51+ registered students. Descriptive operational bins, not fitted prediction cutoffs.
- **Materials segments:** material_count = 0 versus > 0. Event semantics follow source documentation.
- **Review flags:** source-definition or retrospective account-validation questions, not model probabilities. Flags can overlap.
- **Engagement score:** opaque source composite; no percentage unit or 0-100 bound is assumed.
- **Completion:** task checklist completion is separate from business-question coverage and measured intervention impact.

Observation: source README reports aggregation before 2026-05-01. Observation start and future outcome window are not supplied. No date is inferred from the filename.
