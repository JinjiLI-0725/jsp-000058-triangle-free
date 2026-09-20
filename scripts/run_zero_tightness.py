"""Run the bounded saved-corpus implication audit with a durable progress log."""
import json,subprocess,hashlib,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/zero_margin_tightness'
def main():
 binary=Path('/tmp/audit_zero_tightness')
 test=subprocess.run(['.venv/bin/python','tests/test_zero_tightness_audit.py',str(binary)],cwd=ROOT,capture_output=True,text=True,check=True)
 (OUT/'tests.txt').write_text(test.stdout);print(test.stdout,flush=True)
 log=OUT/'audit.jsonl';assert not log.exists()
 rows=[];start=time.monotonic()
 with (OUT/'corpus.txt').open()as inp,log.open('w')as output:
  process=subprocess.Popen([str(binary)],stdin=inp,stdout=subprocess.PIPE,text=True)
  for line in process.stdout:
   row=json.loads(line);rows.append(row);output.write(line);output.flush()
   if len(rows)%100==0 or row['status']!='positive_certificate':print('checked',len(rows),'last',row,'elapsed',round(time.monotonic()-start,1),flush=True)
  assert process.wait()==0
 inventory=json.loads((OUT/'inventory.json').read_text());failed=next((r for r in rows if r['status']=='counterexample'),None)
 assert len(rows)==len(inventory['records'])or failed is not None
 from collections import Counter
 summary=dict(completed=len(rows),inventory_classes=len(inventory['records']),labeled_graphs=inventory['labeled_graphs'],status_counts=dict(Counter(r['status']for r in rows)),dG_histogram=dict(sorted(Counter(r['dG']for r in rows).items())),first_counterexample=failed,zero_graphs=[r for r in rows if r['status']in ('zero_and_tight','counterexample')],elapsed_seconds=time.monotonic()-start)
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
 files=[ROOT/'scripts/audit_zero_tightness.cpp',ROOT/'scripts/audit_selection_exact.cpp',ROOT/'scripts/inventory_tightness_n15.py',Path(__file__),ROOT/'tests/test_zero_tightness_audit.py',binary]+sorted(OUT.iterdir())
 (OUT/'manifest.json').write_text(json.dumps({str(f):hashlib.sha256(f.read_bytes()).hexdigest()for f in files if f.is_file()},indent=2)+'\n')
if __name__=='__main__':main()
