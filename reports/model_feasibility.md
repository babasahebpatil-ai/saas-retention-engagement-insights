# Prediction feasibility decision

**Decision: do not train a future-churn model from this snapshot.**

The source README reports temporal feature aggregation before May 1, 2026, and future-inactivity labels. This is useful supporting context, but the actual inactivity rule, target window, required follow-up, per-account cutoff and engagement-score formula are absent from the released CSV and documentation. The accompanying notebook consumes the label; it does not reconstruct these facts.

Consequently we cannot rule out definitional leakage, uneven follow-up or retrospective label reconstruction. An institution-level random holdout would avoid repeated IDs but would not demonstrate generalisation to a later calendar period. Cohort retention cannot be calculated without first-active/signup dates and time-stamped outcomes.

## Baseline arithmetic, not a model result
An always-churn rule labels all 1,083 institutions as churned. It would match 1,017 supplied labels (93.91% apparent accuracy), while detecting zero of the 66 active-labelled institutions. This full-snapshot arithmetic is not a held-out evaluation. Churn-positive average precision would also have a high prevalence baseline; a future evaluation must report both classes and minority-active behaviour.

## Required evidence before ML
1. Document a feature cutoff and a full future follow-up window per institution.
2. Define qualifying events and the inactivity threshold; distinguish inactivity from contract cancellation.
3. Supply event lineage and the engagement-score formula; exclude score until available.
4. Establish that features are available at prediction time and are not part of the outcome rule.
5. Obtain multiple dated snapshots, account age, eligibility and verified renewal/activity outcomes.

With those inputs, compare a majority/recency baseline, logistic regression and a constrained tree model. Keep institution IDs out of features; exclude constants; fit preprocessing only on training data. Use earlier periods for training and later periods for validation/testing, with organisation grouping to prevent leakage. Report precision, recall and F1 for both classes, ROC-AUC, PR-AUC/average precision with the exact definition, class prevalence and sample counts. Explain the validated model with SHAP; explanations are associations, not intervention effects.

## Replacement / extension proposal
The preferred replacement for prediction is a versioned **AIO Class institution-month panel** containing institution_id, snapshot_date, signup_date, account_eligibility, event counts from fixed lookback windows, last_qualifying_activity_at, and an independently calculated next-30-day inactivity outcome after complete follow-up. Contract renewal/cancellation data are needed for paid churn. This specification is proposed; the data is not publicly supplied and has not been fabricated.

If company data cannot be obtained, a public **synthetic** multi-table SaaS dataset is a separate practice option: https://www.misata.studio/datasets . Its dated fields and label construction still require inspection before predictive use. Do not combine synthetic accounts with this real-source snapshot or claim synthetic findings describe AIO Class. No replacement dataset was used here because the requested descriptive fallback is supportable.

No model binaries, model comparison chart, test scores or SHAP plot are produced. The complete descriptive evidence remains available.
