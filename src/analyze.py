"""Independent descriptive analysis. No author modelling code is reused."""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import sys
import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COUNTS = ['attendance_count', 'material_count', 'assessment_count', 'teacher_count', 'student_count', 'class_count']
METRICS = COUNTS + ['engagement_score']
COLUMNS = ['institution_id'] + METRICS + ['churn_label']
EXPECTED_MD5 = '5e9482aa466382c3121394245d9b8bf1'

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')

def validate(df):
    if list(df.columns) != COLUMNS:
        raise ValueError('Unexpected schema. Review the new source before proceeding.')
    if df.empty or df.isna().any().any():
        raise ValueError('Empty data or missing values; no automatic imputation is authorised.')
    if not all(pd.api.types.is_numeric_dtype(df[c]) for c in COLUMNS):
        raise ValueError('Every source column must parse as numeric.')
    if not np.isfinite(df.to_numpy(dtype=float)).all():
        raise ValueError('Non-finite numeric values found.')
    if df.institution_id.duplicated().any() or df.institution_id.le(0).any():
        raise ValueError('Institution identifiers must be positive and unique.')
    if not set(df.churn_label.unique()).issubset({0, 1}):
        raise ValueError('Churn labels must be 0 or 1.')
    if df[METRICS].lt(0).any().any():
        raise ValueError('Negative counts or scores require source review.')
    integer_cols = ['institution_id'] + COUNTS + ['churn_label']
    if not df[integer_cols].mod(1).eq(0).all().all():
        raise ValueError('Identifiers, counts and labels must be integers.')

def flags(df):
    all_zero = df[COUNTS].eq(0).all(axis=1)
    return {
      'Positive score; all six counts zero': df.engagement_score.gt(0) & all_zero,
      'Materials recorded; score zero': df.material_count.gt(0) & df.engagement_score.eq(0),
      'Active label; no students recorded': df.churn_label.eq(0) & df.student_count.eq(0),
      'Active label; no teacher or no class recorded': df.churn_label.eq(0) & (df.teacher_count.eq(0) | df.class_count.eq(0)),
      'Active label; no materials recorded': df.churn_label.eq(0) & df.material_count.eq(0),
    }

def main(root=ROOT):
    root = Path(root)
    for p in ['data/processed', 'data/samples', 'reports/tables', 'images']:
        (root/p).mkdir(parents=True, exist_ok=True)
    raw = root/'data/raw/institutions.csv'
    source_bytes = raw.read_bytes()
    md5 = hashlib.md5(source_bytes).hexdigest()
    if md5 != EXPECTED_MD5:
        raise ValueError('Raw file checksum differs from the inspected Zenodo version.')
    df = pd.read_csv(raw)
    validate(df)
    df.to_csv(root/'data/processed/institutions_clean.csv', index=False)
    # Non-ID duplicates represent distinct institutions and are intentionally preserved.
    df.groupby('churn_label', group_keys=False).head(5).to_csv(root/'data/samples/institutions_sample.csv', index=False)

    quality = pd.DataFrame([{
        'column': c, 'dtype': str(df[c].dtype), 'rows': len(df),
        'missing_count': int(df[c].isna().sum()), 'zero_count': int(df[c].eq(0).sum()),
        'zero_share_pct': float(df[c].eq(0).mean()*100), 'distinct_values': int(df[c].nunique()),
        'minimum': float(df[c].min()), 'maximum': float(df[c].max()),
        'constant': bool(df[c].nunique()==1)
    } for c in df])
    quality.to_csv(root/'reports/tables/data_quality.csv', index=False)

    feature_only_duplicates = int(df[METRICS].duplicated().sum())
    identical_profiles_and_label = int(df.drop(columns='institution_id').duplicated().sum())
    audit = {
      'input_rows': len(df), 'output_rows': len(df), 'input_columns': len(df.columns),
      'output_columns': len(df.columns), 'missing_cells': int(df.isna().sum().sum()),
      'duplicate_full_rows': int(df.duplicated().sum()), 'duplicate_institution_ids': int(df.institution_id.duplicated().sum()),
      'extra_identical_feature_rows': feature_only_duplicates,
      'extra_identical_features_and_label_rows': identical_profiles_and_label,
      'all_six_counts_zero': int(df[COUNTS].eq(0).all(axis=1).sum()),
      'all_seven_indicators_zero': int(df[METRICS].eq(0).all(axis=1).sum()),
      'constant_features': [c for c in METRICS if df[c].nunique()==1],
      'source_md5': md5, 'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
      'rows_removed': 0, 'cells_imputed': 0, 'values_changed': 0,
      'decision': 'Preserve every source value. Valid unique institutions can share identical zero-heavy profiles.',
      'publication_date': '2026-08-02',
      'observation_window_end': 'Before 2026-05-01, reported by source README; not independently reconstructable.',
      'observation_window_start': 'Not supplied', 'outcome_window': 'Not supplied',
      'label_rule': 'Future inactivity, according to source; exact threshold and SQL not supplied.',
      'engagement_score_formula': 'Not supplied',
    }
    write_json(root/'reports/cleaning_log.json', audit)
    cleaning = pd.DataFrame([
        {'step':'Parse and validate nine numeric columns', 'rows_before':len(df),'rows_after':len(df),'rows_removed':0,'cells_changed':0},
        {'step':'Check unique institution grain; preserve matching profiles', 'rows_before':len(df),'rows_after':len(df),'rows_removed':0,'cells_changed':0},
        {'step':'Flag zero-heavy and opaque score fields; do not overwrite', 'rows_before':len(df),'rows_after':len(df),'rows_removed':0,'cells_changed':0},
        {'step':'Write clean typed CSV; verify unchanged values', 'rows_before':len(df),'rows_after':len(df),'rows_removed':0,'cells_changed':0},
    ])
    cleaning.to_csv(root/'reports/tables/cleaning_steps.csv', index=False)

    # SQL loads raw source separately rather than consuming Pandas summaries.
    con = duckdb.connect(':memory:')
    con.execute('CREATE TABLE institutions AS SELECT * FROM read_csv(?, header=true)', [str(raw)])
    sql_tables = {}
    for script in sorted((root/'sql').glob('*.sql')):
        table = con.execute(script.read_text(encoding='utf-8')).df()
        table.to_csv(root/'reports/tables'/f'{script.stem}.csv', index=False, float_format='%.10g')
        sql_tables[script.stem] = table
    con.close()

    headline_py = {
      'institutions': len(df), 'unique_institutions': int(df.institution_id.nunique()),
      'churn_labelled': int(df.churn_label.sum()), 'active_labelled': int(df.churn_label.eq(0).sum()),
      'churn_label_share_pct': float(df.churn_label.mean()*100),
      'recorded_students': int(df.student_count.sum()), 'recorded_teachers': int(df.teacher_count.sum()),
      'recorded_classes': int(df.class_count.sum()), 'recorded_materials': int(df.material_count.sum()),
    }
    checks = []
    def compare(name, a, b):
        passed = bool(np.isclose(float(a), float(b), rtol=1e-10, atol=1e-8))
        checks.append({'check':name, 'pandas_value':float(a), 'duckdb_value':float(b), 'passed':passed})
        if not passed: raise AssertionError(f'{name}: Pandas {a} != DuckDB {b}')
    for key, value in headline_py.items():
        compare('headline.'+key, value, sql_tables['01_headline'].iloc[0][key])

    bands = pd.cut(df.student_count, [-1,0,10,50,float('inf')], labels=['0','1-10','11-50','51+'])
    for row in sql_tables['03_student_segments'].to_dict('records'):
        g = df[bands.eq(row['student_band'])]
        compare('student_band.'+row['student_band']+'.count', len(g), row['institutions'])
        compare('student_band.'+row['student_band']+'.churn', g.churn_label.sum(), row['churn_labelled'])
        compare('student_band.'+row['student_band']+'.share', g.churn_label.mean()*100, row['churn_label_share_pct'])
    for row in sql_tables['02_label_distribution'].to_dict('records'):
        compare('label.'+str(row['churn_label']), df.churn_label.eq(row['churn_label']).sum(), row['institutions'])
    for row in sql_tables['04_engagement_summary'].to_dict('records'):
        s = df.loc[df.churn_label.eq(row['churn_label']), row['metric']]
        for key, val in {'total':s.sum(),'mean':s.mean(),'median':s.median(),'p25':s.quantile(.25),'p75':s.quantile(.75),'positive_count':s.gt(0).sum(),'positive_share_pct':s.gt(0).mean()*100}.items():
            compare(f"engagement.{row['churn_label']}.{row['metric']}.{key}", val, row[key])
    for row in sql_tables['05_material_segments'].to_dict('records'):
        mask = df.material_count.gt(0) if row['segment']=='Materials recorded' else df.material_count.eq(0)
        compare('material.'+row['segment']+'.count', mask.sum(), row['institutions'])
        compare('material.'+row['segment']+'.churn', df.loc[mask,'churn_label'].sum(), row['churn_labelled'])
    review_flags = flags(df)
    for row in sql_tables['06_review_groups'].to_dict('records'):
        compare('review.'+row['review_group'], review_flags[row['review_group']].sum(), row['institutions'])
    pd.DataFrame(checks).to_csv(root/'reports/tables/reconciliation_checks.csv', index=False)
    pd.testing.assert_frame_equal(df, pd.read_csv(root/'data/processed/institutions_clean.csv'))
    assert hashlib.md5(raw.read_bytes()).hexdigest()==md5

    reviewed = df.copy()
    for i,(name,mask) in enumerate(review_flags.items(),1):
        reviewed[f'review_flag_{i}'] = mask
    mask = pd.Series(False,index=df.index)
    for f in review_flags.values():mask |= f
    reviewed['review_reasons'] = ['; '.join(name for name,m in review_flags.items() if m.loc[i]) for i in df.index]
    reviewed.loc[mask].to_csv(root/'reports/tables/institution_review_list.csv', index=False)

    decision = {
      'status':'NOT_TRAINED', 'decision':'Descriptive analysis only; future-churn validity cannot be independently established.',
      'source_claim':'README says observation ends before 2026-05-01 and labels reflect future inactivity.',
      'missing_evidence':['Exact inactivity threshold and qualifying events','Label observation start/end and full follow-up','Per-institution feature cutoff/eligibility/tenure','Engagement score formula and timestamp lineage'],
      'excluded_from_any_future_model':['institution_id','churn_label','attendance_count (constant)','assessment_count (constant)','engagement_score until formula/lineage is verified'],
      'time_split_possible':False, 'cohort_analysis_possible':False,
      'reference_only_always_churn_accuracy_pct':headline_py['churn_label_share_pct'],
      'reference_only_always_churn_active_recall_pct':0,
      'reference_note':'Arithmetic prevalence baseline across the full snapshot, not a trained or held-out model.',
      'model_comparison':'Not produced', 'shap':'Not produced', 'measured_retention_improvement':None,
    }
    write_json(root/'reports/model_feasibility.json',decision)
    write_json(root/'reports/metrics.json',headline_py)
    write_json(root/'reports/environment.json',{'python':sys.version.split()[0], 'packages':{p:importlib.metadata.version(p) for p in ['pandas','numpy','duckdb','matplotlib','seaborn','nbformat','nbclient','ipykernel']}})

    from charts import create_charts
    create_charts(root, df, quality, sql_tables)
    from write_reports import create_reports
    create_reports(root, df, audit, headline_py, sql_tables, len(checks), len(reviewed.loc[mask]))
    print(f'Analysed {len(df):,} institutions; churn-labelled share {headline_py["churn_label_share_pct"]:.2f}%.')
    print(f'{len(checks)} independent SQL/Pandas comparisons passed. Modelling status: NOT_TRAINED.')
    return headline_py

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args()
    main(args.root)
