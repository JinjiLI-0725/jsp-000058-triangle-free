"""Corrected fixed-corpus audit. No search; fresh output directories only."""
import json, subprocess, argparse, hashlib
from pathlib import Path
from fractions import Fraction
from triangle_free.core import c5_blowup, is_triangle_free
from triangle_free.research import graph6, from_graph6
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 out=args.output.resolve();protected=ROOT/'results/candidate_A_n20_large'
 if out==protected or protected in out.parents:raise ValueError('protected output')
 out.mkdir(parents=True,exist_ok=False)
 reps=ROOT/'results/induction_B_tight_nonbalanced_reps.g6'
 lines=reps.read_text().splitlines();assert len(lines)==22 and len(set(lines))==22
 corpus=[('d8_A_tight','NEL_FF_DgAeOATbBPp?',8),('B3',graph6(c5_blowup(3)),9)]+[(f'nonbalanced_{i}',g,7)for i,g in enumerate(lines,1)]
 chunks=[]
 for name,g,d in corpus:
  G=from_graph6(g);assert G.n==15 and is_triangle_free(G)
  chunks.append(f'{name} {g} 15 {len(G.edges)} {d}\n'+''.join(f'{u} {v}\n'for u,v in G.edges))
 (out/'corpus.txt').write_text(''.join(chunks));(out/'corpus.json').write_text(json.dumps(corpus,indent=2)+'\n')
 source=Path(__file__).with_suffix('.cpp');binary=out/'audit'
 subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(binary)],check=True)
 test_source=ROOT/'tests/test_selection_exact.cpp';test_binary=out/'test_audit'
 subprocess.run(['g++','-O2','-std=c++17',str(test_source),'-o',str(test_binary)],check=True)
 test=subprocess.run([str(test_binary)],check=True,capture_output=True,text=True)
 (out/'tests.txt').write_text(test.stdout);print(test.stdout,flush=True)
 with (out/'corpus.txt').open()as inp,(out/'all_X.tsv').open('w')as log:
  subprocess.run([str(binary)],stdin=inp,stdout=log,check=True)
 rows={}
 for line in (out/'all_X.tsv').read_text().splitlines():
  name,x,num,den,dg,dh,dx,z,c,nr=line.split('\t');margin=Fraction(int(num),int(den))
  row=dict(X=list(map(int,x.split(','))),margin=str(margin),dG=int(dg),dH=int(dh),dX=int(dx),z=int(z),core_mask_local=int(c),allowed_count=int(nr))
  rows.setdefault(name,[]).append(row)
 summary=[]
 for name,g,d in corpus:
  if name not in rows:break
  rs=rows[name];assert len(rs)==3003 and len({tuple(r['X'])for r in rs})==3003
  vals=[Fraction(r['margin'])for r in rs];mx=max(vals)
  def pick(v):return next((r for r in rs if Fraction(r['margin'])==v),None)
  pos=[v for v in vals if v>0];neg=[v for v in vals if v<0]
  record=dict(name=name,graph6=g,count=len(rs),max_margin=str(mx),maximizer=pick(mx),maximizing_X=[r['X']for r in rs if Fraction(r['margin'])==mx],smallest_positive=pick(min(pos))if pos else None,closest_negative=pick(max(neg))if neg else None,minimum=pick(min(vals)),passes=mx>=0)
  if name=='B3':
   trans=[r for r in rs if len({x//3 for x in r['X']})==5];assert len(trans)==243 and all(Fraction(r['margin'])==0 for r in trans);record['zero_margin_transversals']=243
  summary.append(record)
 assert len(summary)==24 or (summary and not summary[-1]['passes'])
 hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()for f in [source,Path(__file__),test_source,ROOT/'notes/COORDINATED_FLIP_SELECTION.md',reps,out/'corpus.txt',out/'corpus.json',out/'all_X.tsv',out/'tests.txt']}
 (out/'summary.json').write_text(json.dumps(dict(scope='Fixed corpus only; corrected complete-bipartite flip family; exact rational margins',graphs_completed=len(summary),five_sets=sum(r['count']for r in summary),rows=summary,sha256=hashes),indent=2)+'\n')
 print(json.dumps([(r['name'],r['max_margin'],r['maximizer']['X'])for r in summary]))
if __name__=='__main__':main()
