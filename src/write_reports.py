"""Generate evidence-linked narrative reports from computed results."""
import base64
import html
import json
from pathlib import Path

SOURCE='https://zenodo.org/records/21759158'
TITLE='SaaS Retention & Engagement Insights'

def create_reports(root, df, audit, metrics, tables, checks, review_count):
    def save(name,text):
        (root/name).write_text(text.strip()+'\n',encoding='utf-8')
    n=len(df); churn=int(metrics['churn_labelled']);active=int(metrics['active_labelled']);share=metrics['churn_label_share_pct']
    student=tables['03_student_segments'].set_index('student_band')
    zero=student.loc['0'];large=student.loc['51+']
    gap=zero.churn_label_share_pct-large.churn_label_share_pct
    material=tables['05_material_segments'].set_index('segment')
    yes=material.loc['Materials recorded'];no=material.loc['No materials recorded']
    reviews=tables['06_review_groups'].set_index('review_group').institutions
    source_text=f'''# Source, licence and data dictionary

Dataset: [{TITLE} candidate]({SOURCE}); DOI: https://doi.org/10.5281/zenodo.21759158.

Original title: User Engagement-Based Institutional Churn Analysis in Educational SaaS: An End-to-End Business Analytics and Lakehouse Approach.

Authors: Timotius Simanjuntak, Miftahul Hafizh, Hepriyanti Siahaan and Teguh Prasandy (2026), Binus University. The publisher describes this as anonymised institutional data derived from AIO Class (CV Smart Edutek Solusi), not synthetic data. That provenance is the authors' claim; we did not independently audit the company database.

- **Licence:** CC BY 4.0, verified in the saved Zenodo API metadata, `metadata.license.id`.
- **Publication/version:** 2026-08-02, v1. This date is not the collection period.
- **Source observation cutoff:** README says observations end before 2026-05-01. The start date is undisclosed.
- **Target:** 0 = active; 1 = churn based on future inactivity according to the source. Inactivity threshold, qualifying events, outcome dates and full-follow-up eligibility are not disclosed.
- **Grain:** one row per unique anonymised educational institution; {n:,} rows and nine columns. No subscription revenue, raw events, timestamps, tenure, plan tier or cohort keys are supplied.
- **Original bytes:** preserved at `data/raw/institutions.csv`, renamed only. MD5 `{audit['source_md5']}`; SHA-256 `{audit['source_sha256']}`. MD5 matches the publisher's file checksum.
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
'''
    save('reports/source_and_dictionary.md',source_text)

    finding_text=f'''# Business findings

## Decision brief
The immediate priority is to validate the account population and activity measurements before launching retention targeting. This snapshot supports descriptive diagnosis; it cannot independently validate future churn predictions or prove a retention intervention works.

## Measured findings
1. **{churn:,}/{n:,} institutions ({share:.2f}%) are churn-labelled; {active} are active-labelled.** This is the supplied snapshot label share. The observation window ends before 2026-05-01 according to the source; its start and the future outcome window are not disclosed. It is not a monthly or annual business churn rate. Evidence: [SQL/Python headline](tables/01_headline.csv), [label chart](../images/02_churn_labels.png).
2. **Zero registered students: {int(zero.churn_labelled):,}/{int(zero.institutions):,} ({zero.churn_label_share_pct:.2f}%) churn-labelled.** For 51+ registered students, the corresponding value is {int(large.churn_labelled)}/{int(large.institutions)} ({large.churn_label_share_pct:.2f}%). Difference: {gap:.2f} percentage points. This is an association, potentially influenced by account eligibility, institutional size, tenure and the label definition. Evidence: [student bands](tables/03_student_segments.csv), [chart](../images/04_student_segments.png).
3. **Materials recorded: {int(yes.churn_labelled)}/{int(yes.institutions)} ({yes.churn_label_share_pct:.2f}%) churn-labelled**, versus {int(no.churn_labelled)}/{int(no.institutions):,} ({no.churn_label_share_pct:.2f}%) with no materials recorded. Smaller sample size and unmeasured confounding prevent a causal claim about publishing materials. Evidence: [material segments](tables/05_material_segments.csv).
4. **Attendance and assessment counts are zero for every institution.** All seven supplied indicators are zero for {audit['all_seven_indicators_zero']} institutions. {int(reviews.iloc[0])} institutions have a positive engagement score although all six count fields are zero; {int(reviews.iloc[1])} have materials recorded but a zero score. These are questions about score semantics, not proven errors. Evidence: [quality profile](tables/data_quality.csv), [review groups](tables/06_review_groups.csv).
5. **{int(reviews['Active label; no teacher or no class recorded'])}/{active} active-labelled institutions lack a recorded teacher or class.** {int(reviews['Active label; no materials recorded'])}/{active} have no materials recorded. Confirm present status and whether the relevant features apply before proposing contact. Evidence: [review groups](tables/06_review_groups.csv), [institution review list](tables/institution_review_list.csv).

## Three recommended actions
| Action | Evidence and target | Owner | Success measurement |
|---|---|---|---|
| Validate the account denominator and event capture | Review the {int(zero.institutions)} zero-student institutions; audit the two constant activity fields and {int(reviews.iloc[0])+int(reviews.iloc[1])} score/count review cases | Data analyst + data engineer + customer operations | Proportion with verified account status; documented event completeness; reconciled label denominator |
| Pilot guided setup for confirmed eligible active accounts | {int(reviews['Active label; no teacher or no class recorded'])} active-labelled institutions have no teacher or no class recorded; this is a retrospective review group | Customer success + product onboarding | Verified setup completion within 14 days; qualifying product activity within 30 days; support burden |
| Test material-workflow assistance | {int(reviews['Active label; no materials recorded'])} active-labelled institutions have zero materials; compare against the descriptive material association | Product education + customer success | First qualifying material action; 30-day qualifying activity; incremental effect versus control |

Review groups overlap; {review_count} unique institutions match at least one documented review condition. They are not a validated churn-risk ranking. No company contact, campaign or experiment has been executed.

## Proposed experiment
First obtain current snapshots, verified account eligibility and a written activity definition. Randomise at institution level between standard support and one clearly defined guided-onboarding intervention. Stratify on baseline institution size and setup status; do not randomise individual teachers within an institution.

Primary outcome: institution has a pre-specified qualifying product event in days 31-60 after assignment, measuring continued activity after onboarding. Report treatment minus control in percentage points, with an interval and intention-to-treat denominator. Secondary outcomes: 14-day setup completion and first material action within 30 days; guardrails: support burden, complaints and opt-outs. This measures activity retention, not paid renewal. Paid retention needs actual subscription renewal records.

The {active} active-labelled accounts are a historical snapshot, not a sufficient recruitment or power calculation. Set the minimum meaningful effect and calculate sample size using fresh baseline data; if too small, run a feasibility pilot and report uncertainty rather than success. Avoid peeking and multiple unplanned tests.

## Proof and limits
- {checks} independent SQL/Pandas comparisons pass, including headline counts, segments and engagement summaries: [reconciliation](tables/reconciliation_checks.csv).
- Missing cells: 0; duplicate full rows: 0; duplicate IDs: 0; removed rows: 0. Matching profiles across different institutions are preserved.
- Labels, demographics, tenure and selection criteria are incomplete; the sample is not claimed to represent all SaaS companies.
- [Prediction feasibility](model_feasibility.md) explains why there are no model scores or SHAP images.
- **Business-question coverage: 2 of 4 questions answered (50%)**: describe supplied labels and engagement patterns. Future prediction and actual intervention effectiveness remain unresolved. This is an explicit question-count measure, not a percentage of churn prevented.
'''
    save('reports/business_findings.md',finding_text)
    save('reports/model_feasibility.md',f'''# Prediction feasibility decision

**Decision: do not train a future-churn model from this snapshot.**

The source README reports temporal feature aggregation before May 1, 2026, and future-inactivity labels. This is useful supporting context, but the actual inactivity rule, target window, required follow-up, per-account cutoff and engagement-score formula are absent from the released CSV and documentation. The accompanying notebook consumes the label; it does not reconstruct these facts.

Consequently we cannot rule out definitional leakage, uneven follow-up or retrospective label reconstruction. An institution-level random holdout would avoid repeated IDs but would not demonstrate generalisation to a later calendar period. Cohort retention cannot be calculated without first-active/signup dates and time-stamped outcomes.

## Baseline arithmetic, not a model result
An always-churn rule labels all {n:,} institutions as churned. It would match {churn:,} supplied labels ({share:.2f}% apparent accuracy), while detecting zero of the {active} active-labelled institutions. This full-snapshot arithmetic is not a held-out evaluation. Churn-positive average precision would also have a high prevalence baseline; a future evaluation must report both classes and minority-active behaviour.

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
''')
    save('models/README.md','''# No model fitted

See [prediction feasibility](../reports/model_feasibility.md). This directory intentionally contains no model binary. A score would not establish future-churn validity with the available temporal and label evidence.
''')
    save('reports/metric_definitions.md','''# Metric definitions

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
''')
    save('reports/resume_bullets.md',f'''# Verified portfolio bullets

Project: SaaS Retention & Engagement Insights

- Analysed {n:,} anonymised educational SaaS institutions using Python and six DuckDB SQL queries, comparing source-defined churn labels with engagement and institutional-size segments.
- Produced six evidence charts and reconciled {checks} SQL/Pandas calculations; identified two constant activity fields and preserved distinct institutions with matching profiles during data-quality validation.
- Found {int(zero.churn_labelled)}/{int(zero.institutions)} zero-student institutions were churn-labelled; documented prediction limitations and proposed targeted account validation, onboarding support and a controlled retention experiment.

Do not claim a deployed model, reduced churn, increased revenue, raw-event ETL or measured campaign impact. The data publisher defines the label as future inactivity; its complete rule is not disclosed.
''')
    readme=f'''# {TITLE}

**A completed descriptive case study using a real-source institutional SaaS snapshot.** Prediction was assessed and withheld because the released data does not allow independent verification of the temporal target definition.

## Business question
How do engagement and institutional-size patterns differ across source churn labels, and what should customer operations investigate before retention outreach?

## Results
- **{n:,} institutions; {churn:,} churn-labelled ({share:.2f}%) and {active} active-labelled.** This is a snapshot label share, not a monthly churn rate.
- **{int(zero.churn_labelled)}/{int(zero.institutions)} zero-student institutions** are churn-labelled, versus **{int(large.churn_labelled)}/{int(large.institutions)}** institutions with 51+ students. Association does not prove causation.
- Two activity columns are entirely zero. No missing cells or duplicate institution IDs were found. Zero values and identical profiles were retained.
- **{checks} SQL/Pandas reconciliations** support the published results. No claimed model accuracy or business uplift.

## Start here
- [Business findings and recommendations](reports/business_findings.md)
- [Visual evidence report](reports/evidence_report.html) - self-contained HTML; open locally in a browser
- [Executed analysis notebook](notebooks/01_saas_analysis.ipynb)
- [Source, licence and dictionary](reports/source_and_dictionary.md)
- [Prediction feasibility and next-data specification](reports/model_feasibility.md)
- [Verified resume bullets](reports/resume_bullets.md)
- [Completion and business-question coverage](reports/completion_report.md)

## Evidence
![Recorded zero values by metric](images/01_data_quality.png)
![Active and churn-labelled institutions](images/02_churn_labels.png)
![Engagement comparison](images/03_engagement_comparison.png)
![Churn-label share by registered-student band](images/04_student_segments.png)

Every chart has a CSV source listed in [figure_index.csv](reports/tables/figure_index.csv). All six images are in `images/`.

## Run from a clean checkout
Requires Python 3.12. Internet is needed only for package installation and an optional source re-download. The pinned original CSV is included under CC BY 4.0.

```powershell
python -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.\\.venv\\Scripts\\python.exe src/download_data.py
.\\.venv\\Scripts\\python.exe src/analyze.py
.\\.venv\\Scripts\\python.exe src/verify.py
.\\.venv\\Scripts\\python.exe src/execute_notebook.py
```

On macOS/Linux replace `.\\.venv\\Scripts\\python.exe` with `.venv/bin/python`.
To inspect interactively: `.\\.venv\\Scripts\\python.exe -m jupyterlab notebooks/01_saas_analysis.ipynb`.

`analyze.py` runs all six SQL scripts against the raw CSV, independently computes matching Pandas results, exports tables/charts and regenerates narrative reports. `verify.py` also tests that invalid labels, negative counts, missing values and duplicate IDs are rejected. `execute_notebook.py` executes and saves all notebook cells with the same Python environment.

The pipeline fails rather than silently accepting an unreviewed source checksum or schema. `requirements.txt` pins direct dependencies; `reports/environment.json` records the tested Python/package versions. It is not a full operating-system lockfile.

## Folder structure
```text
data/          original, processed and small sample CSVs
sql/           six independent business-analysis queries
notebooks/     executed analysis with visible outputs
src/           download, analysis, chart, report and validation scripts
images/        six actual PNG charts
reports/       findings, metrics, tables, provenance and verification
models/        explanation of why no model is fitted
```

## Scope and limits
SQL: aggregation, CASE, CTEs, lateral row expansion and window-based contribution percentages. No artificial multi-table joins are introduced: the source is one institution-level table. Python/Pandas: validation, descriptive analysis, review flags and reconciliation. Matplotlib/Seaborn: evidence charts. Jupyter: an executed walkthrough.

No cohort retention, revenue, A/B-test result, monthly churn rate, future risk score or model explanation is invented. Snapshot dates and label lineage are insufficient for these claims. The report proposes an experiment but does not execute it. Power BI and GenAI are not used.

## Attribution
Simanjuntak, T., Hafizh, M., Siahaan, H., & Prasandy, T. (2026). *User Engagement-Based Institutional Churn Analysis in Educational SaaS: An End-to-End Business Analytics and Lakehouse Approach*. Zenodo. https://doi.org/10.5281/zenodo.21759158 . Data: CC BY 4.0. Source publication date: 2026-08-02; reported observation cutoff: before 2026-05-01; exact start/outcome dates unavailable. Code in this project is independently written; the author's model implementation is not reused.
'''
    save('README.md',readme)

    # A portable report with embedded evidence images; no remote assets or scripts.
    cards=''.join(f'<div class="card"><strong>{v}</strong><span>{html.escape(k)}</span></div>' for k,v in [('Institutions',f'{n:,}'),('Churn-labelled',f'{share:.1f}%'),('Active-labelled',str(active)),('SQL/Pandas checks',str(checks))])
    images=[]
    for p in sorted((root/'images').glob('*.png')):
        encoded=base64.b64encode(p.read_bytes()).decode('ascii')
        images.append(f'<figure><img src="data:image/png;base64,{encoded}" alt="{html.escape(p.stem)}"><figcaption>{html.escape(p.name)} - numerical sources in reports/tables/figure_index.csv</figcaption></figure>')
    segment_html=tables['03_student_segments'][['student_band','institutions','churn_labelled','active_labelled','churn_label_share_pct']].to_html(index=False,float_format=lambda x:f'{x:.2f}')
    report=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE}</title>
<style>body{{margin:0;background:#f2f5f7;color:#19354d;font:16px/1.6 system-ui,sans-serif}}main{{max-width:1120px;margin:auto;padding:42px 24px}}h1{{font-size:36px;line-height:1.2;max-width:850px}}h2{{margin-top:34px}}.eyebrow{{text-transform:uppercase;letter-spacing:2px;color:#087e8b;font-size:12px}}.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}.card,figure,.panel{{background:white;padding:20px;border-radius:10px;border:1px solid #dce4e8}}.card strong{{display:block;font-size:32px}}.card span,figcaption{{font-size:13px;color:#667582}}figure{{margin:20px 0}}img{{max-width:100%;height:auto}}.note{{border-left:4px solid #cd622d;padding:12px 18px;background:#fff5ee}}table{{border-collapse:collapse;width:100%;font-size:14px}}td,th{{padding:10px;text-align:left;border-bottom:1px solid #dce4e8}}a{{color:#087e8b}}@media(max-width:700px){{.cards{{grid-template-columns:repeat(2,1fr)}}h1{{font-size:28px}}.table-wrap{{overflow:auto}}}}@media print{{body{{background:white}}figure{{break-inside:avoid}}main{{padding:10px}}}}</style></head><body><main>
<div class="eyebrow">Portfolio case study / Educational SaaS</div><h1>{TITLE}</h1>
<p>Diagnose engagement differences and account-quality questions before choosing a retention intervention.</p>
<div class="cards">{cards}</div>
<p class="note"><b>Interpretation:</b> {share:.2f}% is the source's snapshot label share, not a monthly cancellation rate. Observation ends before May 1, 2026 according to the source; start and outcome dates are undisclosed. No predictive model or measured business uplift is claimed.</p>
<h2>What the evidence says</h2><div class="panel"><ol>
<li>{int(zero.churn_labelled)}/{int(zero.institutions)} zero-student institutions are churn-labelled ({zero.churn_label_share_pct:.2f}%), versus {int(large.churn_labelled)}/{int(large.institutions)} with 51+ students ({large.churn_label_share_pct:.2f}%). This association does not establish cause.</li>
<li>{audit['all_seven_indicators_zero']} institutions have zero values across all seven indicators. Two entire activity fields contain only zeros.</li>
<li>{int(reviews['Active label; no teacher or no class recorded'])} active-labelled institutions have no teacher or no class recorded. Validate their current status and applicable workflow before outreach.</li></ol></div>
<h2>Student-size segments</h2><div class="panel table-wrap">{segment_html}</div>
<h2>Visual evidence</h2>{''.join(images)}
<h2>Recommended next actions</h2><div class="panel"><ol><li><b>Validate population and tracking.</b> Resolve zero-student eligibility, constant activity fields and engagement-score semantics.</li><li><b>Pilot guided setup.</b> After fresh eligibility checks, test support for accounts lacking teachers/classes.</li><li><b>Test material-workflow assistance.</b> Use an institution-randomised experiment and measure 30-day qualifying activity, plus support burden.</li></ol><p>Groups overlap. Current account status and event lineage must be verified. No customer has been contacted.</p></div>
<h2>How much of the business problem is answered?</h2><div class="panel"><p><b>2 of 4 explicit business questions (50%):</b> supplied label distribution and engagement associations are answered. Reliable future prediction and measured retention improvement remain unresolved. This percentage is question coverage, not reduction in churn.</p><p>The requested conditional deliverable checklist is recorded separately in completion_report.md after verification.</p></div>
<h2>Source and reproducibility</h2><p>Simanjuntak, Hafizh, Siahaan &amp; Prasandy (2026), <a href="{SOURCE}">Zenodo 21759158</a>. Licence: CC BY 4.0. Published August 2, 2026. Original data bytes are included with their checksum; the source claims real anonymised AIO Class institutions. Independent source-database validation is unavailable.</p><p>Run instructions: ../README.md. Detailed findings: business_findings.md. Metric definitions: metric_definitions.md. Reconciliation evidence: tables/reconciliation_checks.csv. Model decision: model_feasibility.md.</p>
</main></body></html>'''
    save('reports/evidence_report.html',report)
