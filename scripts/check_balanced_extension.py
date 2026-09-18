#!/usr/bin/env python3
"""Exhaustive finite check for HOMOGENEOUS five-vertex extensions of B_t.

WARNING: this does not enumerate mixed neighborhoods within remainder parts.
The former assertion that every extension is a spanning subgraph of one of
these homogeneous extensions is false; see notes/BALANCED_EXTENSION_AUDIT.md.
Twin-part rounding correctly computes d for the enumerated family only.
"""
from itertools import combinations, product
import json
from pathlib import Path

PAIR = list(combinations(range(5), 2))

def triangle_free(E):
    E = set(E)
    return not any({(a,b),(a,c),(b,c)} <= E for a,b,c in combinations(range(5),3))

def indep_sets(E, S):
    E = set(E)
    out=[]
    for mask in range(1<<5):
        if mask & ~S: continue
        if all(not (mask>>u&1 and mask>>v&1) for u,v in E): out.append(mask)
    return out

def maximal_sets(E, S):
    vals=indep_sets(E,S)
    return [m for m in vals if not any(m != n and m & ~n == 0 for n in vals)]

def exact_d(t, E, f, choices):
    # vertices 0..4 are X; vertices 5+j denote whole B_t part j.
    edges=[]
    for u,v in E: edges.append((u,v))
    for j,I in enumerate(choices):
        for x in range(5):
            if I>>x&1:
                edges.append((x,5+j))
    for j in range(5):
        for q in ((j+1)%5,): edges.append((5+j,5+q))
    # weighted twin-part graph: each base edge has weight t^2; X-part edge 1;
    # X-to-base edge t.
    best=10**9
    for mask in range(1<<10):
        mono=0
        for u,v in edges:
            w = t*t if u>=5 and v>=5 else t if (u>=5) != (v>=5) else 1
            if ((mask>>u)^(mask>>v))&1 == 0: mono += w
        best=min(best,mono)
    return best

def main():
    graphs=[]
    for mask in range(1<<len(PAIR)):
        E=[e for i,e in enumerate(PAIR) if mask>>i&1]
        if triangle_free(E): graphs.append(E)
    # Rotation fixes f(0)=0 without loss; all labeled F are still included.
    worst={t:None for t in range(1,26)}
    config_count=0; choice_count=0
    for E in graphs:
      for tail in product(range(5), repeat=4):
        f=(0,)+tail
        S=[]
        for j in range(5):
            S.append(sum(1<<x for x in range(5) if (f[x]-j)%5 in (1,4)))
        families=[maximal_sets(E,S[j]) for j in range(5)]
        config_count += 1
        for choices in product(*families):
            choice_count += 1
            # exact deficit forced by this neighborhood pattern
            D=sum(2*t-sum((I>>x)&1 for I in choices) for I in choices) if False else None
            for t in range(1,26):
                val=exact_d(t,E,f,choices)
                gap=val-(t+1)*(t+1)
                rec=worst[t]
                if rec is None or gap>rec['gap']:
                    deficits=[2*t-I.bit_count() for I in choices]
                    worst[t]={'gap':gap,'d':val,'edges':E,'types':f,
                              'choices':choices,'deficits':deficits}
    out={'triangle_free_graphs':len(graphs),'type_assignments':config_count,
         'maximal_neighborhood_configurations':choice_count,
         'worst_by_t':worst}
    Path('results').mkdir(exist_ok=True)
    Path('results/balanced_extension_finite.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__': main()
