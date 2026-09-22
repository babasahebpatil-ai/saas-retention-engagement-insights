"""Verify evidence, row preservation, source pinning and validation failure cases."""
import hashlib
import json
from pathlib import Path
import pandas as pd
from PIL import Image
from analyze import ROOT, EXPECTED_MD5, validate

def main(root=ROOT):
    root=Path(root)
    raw=pd.read_csv(root/'data/raw/institutions.csv')
    clean=pd.read_csv(root/'data/processed/institutions_clean.csv')
    validate(raw)
    pd.testing.assert_frame_equal(raw,clean)
    assert hashlib.md5((root/'data/raw/institutions.csv').read_bytes()).hexdigest()==EXPECTED_MD5
    checks=pd.read_csv(root/'reports/tables/reconciliation_checks.csv')
    assert checks.passed.all()
    seg=pd.read_csv(root/'reports/tables/03_student_segments.csv')
    assert seg.institutions.sum()==len(raw)
    assert seg.churn_labelled.sum()==raw.churn_label.sum()
    assert len(raw)==1083 and raw.churn_label.sum()==1017
    assert not list((root/'models').glob('*.pkl')) and not list((root/'models').glob('*.joblib'))
    assert json.loads((root/'reports/model_feasibility.json').read_text())['status']=='NOT_TRAINED'
    for image in sorted((root/'images').glob('*.png')):
        with Image.open(image) as img:
            assert img.width>=1500 and img.height>=800
            img.verify()
    assert len(list((root/'images').glob('*.png')))==6
    failure_cases={}
    duplicate=raw.copy();duplicate.loc[1,'institution_id']=duplicate.loc[0,'institution_id'];failure_cases['duplicate institution']=duplicate
    missing=raw.copy();missing.loc[0,'student_count']=float('nan');failure_cases['missing count']=missing
    invalid=raw.copy();invalid.loc[0,'churn_label']=2;failure_cases['invalid label']=invalid
    negative=raw.copy();negative.loc[0,'class_count']=-1;failure_cases['negative count']=negative
    for name,bad in failure_cases.items():
        try:validate(bad)
        except ValueError:pass
        else:raise AssertionError(f'Invalid input accepted: {name}')
    # Distinct institutions with identical measurements must remain valid.
    identical=raw.iloc[:2].copy()
    for c in identical.columns:
        if c!='institution_id':identical.loc[identical.index[1],c]=identical.loc[identical.index[0],c]
    validate(identical)
    result={'status':'PASS','sql_pandas_comparisons':len(checks),'source_checksum':'PASS','row_value_preservation':'PASS','student_segment_reconciliation':'PASS','images_readable_files':6,'validation_failure_cases':len(failure_cases),'legitimate_matching_profiles':'PASS','no_unsupported_models':'PASS'}
    (root/'reports/verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':main()
