"""Snapshot existing explicit n=15 graphs; no graph generation/search."""
import ast,hashlib,json,re,subprocess
from collections import defaultdict,Counter
from pathlib import Path
from triangle_free.research import graph6,from_graph6
from triangle_free.core import is_triangle_free
from triangle_free.balanced_patterns import extension_graph
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/zero_margin_tightness'

def main():
 OUT.mkdir(exist_ok=False)
 graphs=defaultdict(set);hashes={};rejected=set();mixed=0
 def add(s,path):
  if not isinstance(s,str)or len(s)!=19 or s[0]!='N' or any(not 63<=ord(c)<=126 for c in s):return
  if s in graphs:graphs[s].add(path);return
  try:
   G=from_graph6(s)
   if G.n!=15 or graph6(G)!=s or not is_triangle_free(G):rejected.add(s);return
  except Exception:rejected.add(s);return
  graphs[s].add(path)
 def walk(obj,path):
  nonlocal mixed
  if isinstance(obj,str):add(obj,path)
  elif isinstance(obj,list):
   for v in obj:walk(v,path)
  elif isinstance(obj,dict):
   if 'patterns'in obj and 'edges'in obj:
    try:
     pats=obj['patterns'];eds=obj['edges']
     if len(pats)==5 and all(len(p)==2 for p in pats):
      G=extension_graph(tuple(map(tuple,eds)),tuple(map(tuple,pats)))
      if G.n==15:add(graph6(G),path);mixed+=1
    except (TypeError,ValueError,KeyError):pass
   for value in obj.values():walk(value,path)
 paths=[]
 for root in ('results','notes','scripts','tests','src','experiments','state','logs'):
  for f in (ROOT/root).rglob('*'):
   if not f.is_file()or f.suffix not in ('.json','.jsonl','.g6','.tsv','.txt','.md','.py','.log'):continue
   rel=str(f.relative_to(ROOT))
   if rel.startswith(('results/candidate_A_n20_large','results/zero_margin_tightness','results/selection_claim_n15','results/selection_exact_corrected/')):continue
   paths.append(f)
 for f in sorted(paths):
  rel=str(f.relative_to(ROOT));raw=f.read_bytes();hashes[rel]=hashlib.sha256(raw).hexdigest()
  try:text=raw.decode()
  except UnicodeDecodeError:continue
  if f.suffix=='.json':
   try:walk(json.loads(text),rel)
   except json.JSONDecodeError:pass
  elif f.suffix=='.jsonl':
   for line in text.splitlines():
    try:walk(json.loads(line),rel)
    except json.JSONDecodeError:pass
  else:
   for line in text.splitlines():
    add(line.strip(),rel);add(line.split('\t')[0],rel)
   # Graph6 literals in notes, logs and source; these are identity inputs only.
   for match in re.finditer(r'N[?-~]{18}',text):add(match.group(),rel)
 labels=sorted(graphs)
 canon=subprocess.run(['/usr/bin/nauty-labelg','-q'],input='\n'.join(labels)+'\n',text=True,capture_output=True,check=True).stdout.splitlines()
 assert len(canon)==len(labels)
 classes=defaultdict(list)
 for g,c in zip(labels,canon):classes[c].append(g)
 records=[dict(id=i,graph6=c,labeled_graphs=gs,sources=sorted(set().union(*(graphs[g]for g in gs))))for i,(c,gs)in enumerate(sorted(classes.items()))]
 (OUT/'inventory.json').write_text(json.dumps(dict(scope='Snapshot of explicit graph6 encodings and saved mixed-extension records; triangle-freeness checked; numerical d values will be recomputed',files_read=len(paths),labeled_graphs=len(labels),isomorphism_classes=len(records),mixed_records_seen=mixed,rejected_candidate_strings=len(rejected),input_hashes=hashes,records=records),indent=2)+'\n')
 with (OUT/'corpus.txt').open('w')as out:
  for r in records:
   G=from_graph6(r['graph6']);out.write(f"{r['id']} {r['graph6']} 15 {len(G.edges)} -1\n"+''.join(f'{u} {v}\n'for u,v in G.edges))
 print(json.dumps(dict(files=len(paths),labeled=len(labels),classes=len(records),mixed_records=mixed,rejected=len(rejected))),flush=True)
if __name__=='__main__':main()
