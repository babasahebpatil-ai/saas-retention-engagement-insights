# Correction change log

- Independently recalculated the six published descriptive analysis tables from the included raw CSV; no genuine numerical corrections were required.
- Verified raw checksum, row/ID integrity and raw-versus-processed value equality.
- Added `independent_review_2026-09-21.md` and linked it from the README.
- Preserved the project's descriptive scope: no monthly churn rate, cohort retention, revenue metrics, predictive model or completed experiment was invented.
- The complete DuckDB pipeline was not re-executed in the correction environment because `duckdb` was unavailable and package installation could not reach the package index; the project's existing recorded PASS results were preserved without being misrepresented as a fresh run.

## Final naming update
- Standardized the portfolio title to **SaaS Retention & Engagement Insights** across README, notebook/report metadata, generated HTML, and report text.
- No source records, descriptive calculations, or validation results were changed in this naming pass.
