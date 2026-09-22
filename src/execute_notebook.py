"""Execute the walkthrough using this interpreter, without global kernel installation."""
from pathlib import Path
import hashlib
import json
import os
import sys
import tempfile
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT=Path(__file__).resolve().parents[1]

def main():
    path=ROOT/'notebooks/01_saas_analysis.ipynb'
    nb=nbformat.read(path,as_version=4)
    with tempfile.TemporaryDirectory(prefix='saas-notebook-') as td:
        temp=Path(td)
        kernel=temp/'kernels'/'saas-local';kernel.mkdir(parents=True)
        spec={'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}','--HistoryManager.hist_file=:memory:'],'display_name':'SaaS local environment','language':'python'}
        (kernel/'kernel.json').write_text(json.dumps(spec),encoding='utf-8')
        env=os.environ.copy()
        for var,folder in [('IPYTHONDIR','ipython'),('JUPYTER_RUNTIME_DIR','runtime'),('JUPYTER_CONFIG_DIR','config'),('MPLCONFIGDIR','matplotlib')]:
            (temp/folder).mkdir()
            env[var]=str(temp/folder)
        km=KernelManager(kernel_name='saas-local',kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(temp/'kernels')]),connection_file=str(temp/'runtime'/'kernel.json'))
        client=NotebookClient(nb,km=km,timeout=180,resources={'metadata':{'path':str(ROOT)}},allow_errors=False)
        try:
            client.execute(env=env)
        finally:
            if km.has_kernel:
                km.shutdown_kernel(now=True)
            if client.kc:
                client.kc.stop_channels()
    nbformat.write(nb,path)
    codes=[c for c in nb.cells if c.cell_type=='code']
    errors=[o for c in codes for o in c.get('outputs',[]) if o.output_type=='error']
    assert not errors and all(c.execution_count is not None for c in codes)
    result={'status':'PASS','code_cells_executed':len(codes),'error_outputs':len(errors),'notebook_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'python':sys.version.split()[0]}
    (ROOT/'reports/notebook_execution.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
