"""Independent full-coloring verification of saved maximum/near-zero witnesses."""
import argparse, hashlib, json
from pathlib import Path
from fractions import Fraction
import networkx as nx
import numpy as np

def verify(g6, row):
 G=nx.from_graph6_bytes(g6.encode());X=row['X'];H=sorted(set(G)-set(X));HG=G.subgraph(H)
 def family(s):
  K=HG.subgraph([H[i]for i in range(10)if s>>i&1]);e=K.number_of_edges()
  if e==0:return True
  if not nx.is_connected(K) or not nx.is_bipartite(K):return False
  colors=nx.bipartite.color(K);p=sum(colors.values())
  return e==p*(len(K)-p)
 shapes=[family(s)for s in range(1024)]
 allowed=np.array([s for s in range(1024)if shapes[s] or shapes[s^1023]],dtype=np.int64)
 assert len(allowed)==row['allowed_count']
 hmask=np.arange(1024);amask=np.arange(32)
 # Enumerate full graph colorings directly in original vertex labels.
 hc=sum(((hmask>>i)&1)<<v for i,v in enumerate(H))
 ac=sum(((amask>>i)&1)<<v for i,v in enumerate(X))
 def mono(edges,masks):
  return sum((((masks>>u)&1)==((masks>>v)&1)).astype(np.int64)for u,v in edges) if edges else np.zeros_like(masks)
 hm=mono(list(HG.edges()),hc);xm=mono(list(G.subgraph(X).edges()),ac)
 dh=int(hm.min());dx=int(xm.min());assert (dh,dx)==(row['dH'],row['dX'])
 aa=np.flatnonzero(xm==dx);cc=np.flatnonzero(hm==dh) # BOTH core orientations
 full=ac[aa,None]|hc[None,:];cost=mono(list(G.edges()),full)-dh
 sums=[]
 for c in cc:sums.append(int(cost[:,c^allowed].min(axis=1).sum()))
 best=min(sums);margin=Fraction(5)-Fraction(best,len(aa));assert margin==Fraction(row['margin'])
 chosen=row['core_mask_local'];assert chosen in cc and sums[list(cc).index(chosen)]==best
 witnesses=[]
 for j,a in enumerate(aa):
  values=cost[j,chosen^allowed];low=int(values.min());ss=allowed[values==low]
  witnesses.append(dict(assignment_side1=[X[i]for i in range(5)if int(a)>>i&1],cost=low,maximizing_flip_sets=[[H[i]for i in range(10)if int(s)>>i&1]for s in ss]))
 return dict(**row,core_side1=[H[i]for i in range(10)if chosen>>i&1],Phi=str(Fraction(dx)+Fraction(row['z'],2)-5+margin),assignments=witnesses,optimal_core_colorings_checked=len(cc))

def main():
 p=argparse.ArgumentParser();p.add_argument('output',type=Path);args=p.parse_args();out=args.output
 target=out/'independent_witnesses.json';assert not target.exists()
 data=json.loads((out/'summary.json').read_text());records=[]
 for r in data['rows']:
  witnesses={}
  for key in ('maximizer','smallest_positive','closest_negative','minimum'):
   if r[key] is not None:witnesses[key]=verify(r['graph6'],r[key])
  records.append(dict(name=r['name'],graph6=r['graph6'],witnesses=witnesses));print('verified',r['name'],flush=True)
 target.write_text(json.dumps(dict(method='NetworkX connected bipartition plus complete edge count; direct full graph coloring costs; both core orientations',records=records),indent=2)+'\n')
 paths=[Path(__file__),out/'summary.json',target]
 (out/'verification_hashes.json').write_text(json.dumps({str(f):hashlib.sha256(f.read_bytes()).hexdigest()for f in paths},indent=2)+'\n')
if __name__=='__main__':main()
