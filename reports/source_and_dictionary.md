# Source, licence and data dictionary

Dataset: [SaaS Retention & Engagement Insights candidate](https://zenodo.org/records/21759158); DOI: https://doi.org/10.5281/zenodo.21759158.

Original title: User Engagement-Based Institutional Churn Analysis in Educational SaaS: An End-to-End Business Analytics and Lakehouse Approach.

Authors: Timotius Simanjuntak, Miftahul Hafizh, Hepriyanti Siahaan and Teguh Prasandy (2026), Binus University. The publisher describes this as anonymised institutional data derived from AIO Class (CV Smart Edutek Solusi), not synthetic data. That provenance is the authors' claim; we did not independently audit the company database.

- **Licence:** CC BY 4.0, verified in the saved Zenodo API metadata, `metadata.license.id`.
- **Publication/version:** 2026-08-02, v1. This date is not the collection period.
- **Source observation cutoff:** README says observations end before 2026-05-01. The start date is undisclosed.
- **Target:** 0 = active; 1 = churn based on future inactivity according to the source. Inactivity threshold, qualifying events, outcome dates and full-follow-up eligibility are not disclosed.
- **Grain:** one row per unique anonymised educational institution; 1,083 rows and nine columns. No subscription revenue, raw events, timestamps, tenure, plan tier or cohort keys are supplied.
- **Original bytes:** preserved at `data/raw/institutions.csv`, renamed only. MD5 `5e9482aa466382c3121394245d9b8bf1`; SHA-256 `dccc686ee83c109f6fb59f61c8356b41fb240be123a01dc6b8c5a600b14ec1d0`. MD5 matches the publisher's file checksum.
- **Transformation:** parse numeric columns and export a typed CSV; no values changed and no records removed. Analysis tables and charts are our derivatives.
- **Supporting source files:** `reports/source/zenodo_record.json` and `reports/source/original_readme.md`. The author's notebook was inspected only to check available target/feature provenance; its modelling implementation and reported model scores are not used or redistributed here.

| Column | Source meaning | Analytical caution |
|---|---|---|
| institution_id | Anonymised organisation identifier | Identifier only; never a model feature |
| attendance_count | Attendance tracking events in observation window | Every value is zero; unusable for comparisons |
| material_count | Learning materials published or accessed | Exact event interpretation needs source confirmation |
| assessment_count | Assessments created | Every value is zero; unusable for comparisons |
| teacher_count | Active teachers/staff | Definition of active and cutoff lineage unavailable |
| student_count | Registered students | Institutional size, not proof of current usage |
| class_count | Active classes | Time definition of active unavailable |
| engagement_score | Normalised composite learning-intensity score | Formula unavailable; do not interpret as percentage or known 0-100 scale |
| churn_label | Author-defined future-inactivity label | Does not establish subscription cancellation or monthly churn |

**Reuse attribution:** retain this source notice and cite the authors/DOI. Licence: https://creativecommons.org/licenses/by/4.0/ . Source data remains under its original licence; our code is independently written.
