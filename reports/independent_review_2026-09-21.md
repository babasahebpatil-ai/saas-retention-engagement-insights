# Independent review - 2026-09-21

This review recalculates the published descriptive results from the included raw CSV without changing the project's scope.

## Result

No genuine numerical corrections were required for the six published analysis tables.

- Raw file: 1,083 rows, 9 columns, 1,083 unique institution IDs, 0 missing cells, 0 duplicate IDs.
- Raw MD5: `5e9482aa466382c3121394245d9b8bf1`.
- Raw SHA-256: `dccc686ee83c109f6fb59f61c8356b41fb240be123a01dc6b8c5a600b14ec1d0`.
- `data/processed/institutions_clean.csv` is value-for-value equal to the raw CSV.
- 1,017 institutions are churn-labelled and 66 are active-labelled; snapshot churn-label share is 93.9058%. This remains a snapshot label share, not a monthly churn rate.
- Zero-student band: 732/737 churn-labelled (99.32%); 51+ student band: 16/50 (32.00%).
- Materials recorded: 23/46 churn-labelled (50.00%); no materials recorded: 994/1,037 (95.85%).
- Attendance and assessment fields are constant zero.
- 16 institutions have a positive engagement score with all six count fields zero; 5 have materials recorded with score zero; 19 active-labelled institutions have no teacher or no class recorded; 43 active-labelled institutions have no materials recorded.

All six exported report tables (`01_headline.csv` through `06_review_groups.csv`) matched independent Pandas recomputation to floating-point tolerance.

## Verification boundary

The packaged project records a prior successful DuckDB/Notebook verification run in `reports/verification.json`, `reports/notebook_execution.json`, and `reports/environment.json`. In this correction environment, the `duckdb` Python dependency was not installed and external package installation was unavailable, so the complete DuckDB pipeline was not re-executed here. The existing PASS result was not overwritten or represented as a fresh run.

The independent review therefore verifies the included source bytes and published descriptive tables, while preserving the project's own recorded pipeline results separately.

## Scope preserved

No cohort-retention metric, revenue metric, monthly churn rate, predictive model, model accuracy, or completed experiment was added. Proposed experiments remain proposals rather than achieved outcomes.
