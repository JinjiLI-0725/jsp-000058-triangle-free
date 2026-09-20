"""Regression against the completed corrected all-X audit, including loss histograms."""
import json,subprocess,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 binary=Path(sys.argv[1]);source=ROOT/'results/selection_exact_corrected_v2'
 run=subprocess.run([str(binary)],input=(source/'corpus.txt').read_text(),capture_output=True,text=True,check=True)
 rows=[json.loads(l)for l in run.stdout.splitlines()];assert len(rows)==24
 expected=json.loads((source/'summary.json').read_text())['rows']
 losses={}
 for line in (source/'all_X.tsv').read_text().splitlines():
  name,x,num,den,dg,dh,*rest=line.split('\t');losses.setdefault(name,Counter())[str(int(dg)-int(dh))]+=1
 for r,e in zip(rows,expected):
  assert r['id']==e['name'] and r['dG']==e['maximizer']['dG']
  if Fraction(e['max_margin'])==0:
   assert r['status']=='zero_and_tight' and r['five_sets_checked']==3003 and r['min_q_checked']==5
   assert r['q_histogram_checked']==losses[r['id']]
  else:
   assert r['status']=='positive_certificate'
   assert 0<Fraction(r['margin_lower_num'],r['margin_lower_den'])<=Fraction(e['max_margin'])
 print(json.dumps(dict(status='passed',fixed_graphs=24,exact_zero_loss_distributions=2,positive_certificates=22)))
if __name__=='__main__':main()
