"""Download the pinned Zenodo CSV without replacing a different existing file."""
from pathlib import Path
import hashlib
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
URL='https://zenodo.org/api/records/21759158/files/Churn%20Prediction%20Dataset-2026-08-02.csv/content'
EXPECTED='5e9482aa466382c3121394245d9b8bf1'

if __name__=='__main__':
    output=ROOT/'data/raw/institutions.csv'
    if output.exists():
        if hashlib.md5(output.read_bytes()).hexdigest()!=EXPECTED:
            raise SystemExit('Existing raw file has a different checksum; review it before replacing.')
        print('Pinned dataset is already present and verified.')
    else:
        with urllib.request.urlopen(URL,timeout=60) as response:
            data=response.read()
        if hashlib.md5(data).hexdigest()!=EXPECTED:
            raise SystemExit('Downloaded file differs from the inspected version; nothing saved.')
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_bytes(data)
        print('Downloaded and verified the original CSV.')
