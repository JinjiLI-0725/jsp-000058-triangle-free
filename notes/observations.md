# Baseline observations — 2026-09-18

## Scope and assumptions

We consider finite simple undirected graphs on exactly 5k labeled vertices,
including isolated vertices. Loops, repeated undirected edges, and invalid
vertex labels are rejected. All computations use integers. Triangle-freeness
is checked by common neighbors across each edge. Exact MaxCut enumerates all
partitions up to complementation; d is the edge count minus that optimum.
A saved maximizing cut alone does not certify optimality: that conclusion
comes from the exhaustive calculation.

Computational evidence is not proof. No full solution is claimed.

## Reproducible experiment

Python 3.10.12, seed 58, unchanged baseline source:

```bash
PYTHONPATH=src .venv/bin/python -m triangle_free.search --k 1 2 --seed 58 --samples 2000 --output results/baseline
.venv/bin/python -m pytest -q
```

| k | Method | Triangle-free evaluations | Unique labeled graphs | Best d | Target k² |
|---|---|---:|---:|---:|---:|
| 1 | All 1,024 labeled five-vertex graphs, filtered | 388 | 388 | 1 | 1 |
| 2 | Balanced C5 blow-up plus 2,000 random greedy samples | 2,001 | 1,991 | 4 | 4 |

For k=1, the d histogram is {0: 376, 1: 12}. The 12 nonbipartite graphs
are labeled C5 graphs. This is an exhaustive computational check for this size.
For k=2, the histogram (including repeated evaluations and the benchmark) is
{0: 526, 1: 797, 2: 613, 3: 52, 4: 13}. No evaluated graph exceeded k².
The balanced C5 blow-up has 10 vertices, 20 edges, exact MaxCut 16, and d=4.
Full edge lists and cut witnesses are in `results/baseline/k1_seed58.json`
and `results/baseline/k2_seed58.json`.

## Validation and bug checks

Empty graphs and paths have d=0. Tested even cycles C4, C6, C8, C10 have d=0.
C5 has 5 edges, MaxCut 4, and d=1; C7 and C9 also have d=1.
Two disjoint C5 graphs plus isolates have d=2. Independent full partition
and triangle-triple enumeration check every graph through five vertices,
including graphs containing triangles. Additional random ten-vertex graphs
check Gray-code updates and relabeling invariance. Tests also check cut
witnesses, random generator reproducibility and maximality at probability 1,
input validation, the CLI, and saved witnesses.

## Limitations and next experiments

The random generator shuffles potential edges and accepts proposed edges only
when no triangle is formed. Proposal probabilities cycle through 0.25, 0.5,
0.75, 1.0. This distribution is not uniform; dense greedy generation may favor
bipartite graphs. Counts are labeled, not isomorphism counts. The best-witness
list is capped at 10, so it is not a classification of extremizers. The C5
benchmark is deliberately included, so attaining d=4 alone does not show that
random sampling reliably finds it. The k=2 search is not exhaustive and does
not exclude a counterexample. The exact solver is exponential and guarded at
24 vertices by default.

Next: independent cross-checks with a second exact solver, broader seeded
sampling, and systematic enumeration or triangle-preserving local search at
k=2. Any apparent violation must be independently verified before drawing a
mathematical conclusion.
