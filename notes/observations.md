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

# Phase 2 — exhaustive k=2 and exploratory k=3

## Exhaustive k=2 (completed)

Nauty 2.9.3 `geng -t 10`, without connectivity, minimum-degree, or edge-range
restrictions, generated **12,172** isomorphism classes. `labelg -q` converted
all representatives to canonical graph6; the canonical strings were distinct.
Each graph was checked by both common-neighbor and independent vertex-triple
triangle tests. Both the baseline Gray-code MaxCut and an independent NumPy
sum over all 1,024 partitions agreed for every graph.

The d histogram over isomorphism classes is:

| d | Classes |
|---|---:|
| 0 | 5,479 |
| 1 | 5,270 |
| 2 | 1,397 |
| 3 | 25 |
| 4 | 1 |

The unique maximizing class is the balanced C5 blow-up with twin-class sizes
(2,2,2,2,2), 20 edges, MaxCut 16, and d=4. Its canonical graph6 is
``Is`b?{]]?`` (nauty 2.9.3 default dense labeling). It is connected,
4-regular, and maximal triangle-free. Full edges and a maximizing cut are saved.

The complete canonical corpus occupies 121,720 bytes. Corpus SHA-256:
`9b04c7b9837de1643eba4849d0e627a9252b1647a5db23dbceeef62bb11ea5f2`.
Checkpoints were atomically written 13 times. An additional audit generated all
**12,005,168** unrestricted 10-vertex isomorphism classes, filtered with
`pickg -T0`, canonicalized, and obtained exactly the same set of 12,172 graphs.
This tests a different generation/filtering path, but both paths use nauty;
it is not independent confirmation of nauty's isomorph-free machinery.
Small-order generation also matched NetworkX's graph atlas.

This replaces the sampled k=2 run as the strongest available finite-size
evidence; the original baseline files remain as historical experiments.
It is exhaustive computational evidence for n=10, subject to implementation
correctness, and is not a proof of the general conjecture.

Artifacts: `results/exhaustive_k2/{graphs.g6,generator.json,result.json,
checkpoint.json,extremizers.g6,generation_audit.json,toolchain.json}`.
`toolchain.json` pins the nauty source archive, compiler, and baseline commit;
`result.json` pins evaluator sources and dependency versions.
The pinned source archive is obtained from the
[authors' nauty site](https://users.cecs.anu.edu.au/~bdm/nauty/).
The unrestricted count also agrees with
[McKay's graph collection](https://users.cecs.anu.edu.au/~bdm/data/graphs.html).

## k=3 method (not exhaustive)

Started only after the exhaustive k=2 evaluation and its generation audit
completed. The fixed target is d<=9 on 15 vertices.

Structured searches enumerate all positive integer weight vectors totaling 15
for bases C5, C7, C9, C11, C13, C15, Andrasfai A3/A4/A5, Petersen, and
Mycielski(C5). Candidate graphs are checked for triangles before canonical
reduction, and each distinct canonical graph within each family receives an
exact MaxCut computation. Complete coverage of these restricted constructions
must not be confused with exhaustive coverage of 15-vertex triangle-free graphs.
Zero-weight parts are outside this family enumeration. The folded 4-cube with
one vertex deleted and K7,8 provide additional benchmarks.

Andrasfai A_i is defined explicitly here on 3i-1 vertices by connecting u<v
when v-u is 1 modulo 3; its triangle-free status is always checked. This agrees
with the Cayley-graph definition in
[S. Morteza Mirafzal, The automorphism group of the Andrasfai graph](https://arxiv.org/abs/2105.07594).
Mycielski(C5) uses NetworkX's
[Mycielski construction](https://networkx.org/documentation/stable/reference/generated/networkx.generators.mycielski.mycielskian.html).

Heuristic runs use seeds 58,59,60,61, each with 500 random samples and 2,000
local proposals. Sampling probabilities cycle through 0.35,0.6,0.85,1.0.
Local operators delete 1-6 edges, remove one vertex's neighborhood, or force a
nonedge after deleting one incident edge at each common neighbor; each is
followed by randomized maximal triangle-free completion. Simulated annealing
accepts decreases with exp(delta/temperature), with temperature decreasing from
1.2 to 0.1 every 250 proposals. Restarts use current extremizers or structured
and random seeds. Explicit benchmark insertion means finding d=9 alone says
nothing about the discovery rate of random search.

Every evaluated graph is independently triangle-tested and evaluated by exact
full-partition enumeration. Every distinct labeled graph with d>=8 and every
50th newly encountered lower-value graph is cross-checked with the Gray-code
solver. All saved near-extremizers are checked with both exact solvers again.
All evaluation requests, including repeats, are preserved in a deterministic
JSONL log. Checkpoints record progress but do not resume the heuristic search;
reproduce it from the recorded seeds in a fresh directory.

## k=3 results (completed bounded run; not exhaustive)

The structured stage considered **15,550** positive weight vectors, reduced to
**1,041** canonical family representatives. These are family-level counts;
they are not a count of all 15-vertex triangle-free isomorphism classes.

| Base | Weight vectors | Canonical family representatives | Best d |
|---|---:|---:|---:|
| C5 | 1,001 | 111 | 9 |
| C7 | 3,003 | 232 | 4 |
| C9 | 3,003 | 185 | 2 |
| C11 | 1,001 | 56 | 1 |
| C13 | 91 | 7 | 1 |
| C15 | 1 | 1 | 1 |
| Andrasfai A3 | 3,432 | 232 | 7 |
| Andrasfai A4 | 1,001 | 56 | 7 |
| Andrasfai A5 | 14 | 1 | 6 |
| Petersen | 2,002 | 35 | 7 |
| Mycielski(C5) | 1,001 | 125 | 7 |

The folded 4-cube minus a vertex has 35 edges and d=7. Each of the four random
batches reached best d=7. Each local search started at the known d=9 benchmark,
so its recorded best d=9 is not an independent discovery. Seeds are processed
in the listed order and share the accumulated best-graph pool; changing the
order can change trajectories. Each seed generated 2,508 requests: 500 random
samples, one local start, 2,000 proposals, and seven restarts.

Including structured and benchmark requests, the main experiment made
**11,076 evaluations**, with **8,236 distinct labeled graphs** after memoization.
There were **191** additional Gray-code cross-checks of distinct graphs (all
near-extremizers plus the deterministic lower-value sample). Saved canonical
witnesses were cross-checked again. The request histogram, including repeats,
is {0:19, 1:558, 2:494, 3:859, 4:1396, 5:2103, 6:3687, 7:655, 9:1305}.

No evaluated graph had d>9. The only observed equality isomorphism class was
the balanced C5 blow-up with weights (3,3,3,3,3): 45 edges, MaxCut 36, d=9,
degree sequence 6 repeated 15 times, and five false-twin classes of size 3.
Canonical graph6: ``NsaCB`o[?^`}B{^_No?``. This supports the equality pattern at
the sampled points only; the k=3 search cannot classify all equality graphs.

The main run found no d=8 graph. This is a limitation worth noticing: local
moves always end with maximal completion, and random/structured sampling is
biased. A separate targeted check **does** find d=8 by deleting one edge from
the equality graph. Its seven false-twin classes have sizes (1,1,2,2,3,3,3),
so near-equality does not force an exact C5 blow-up. It is saved separately in
`results/structural_checks.json`, together with K7,8 and the equality benchmark.
These three supplementary evaluations are not included in the main histogram.
The rejected statements and candidate directions are recorded in the other
notes files; no conjecture counterexample was found.

## Reproduction and next work

Commands are in `README.md`. Raw corpus, canonical witnesses, parameterized
results, and the complete k=3 request log are retained under `results/`.
Nauty was built locally from pinned version 2.9.3; its source archive hash is
checked by `tools/build_nauty.sh`. Runtime versions: Python 3.10.12,
NetworkX 3.4.2, NumPy 2.2.6. Canonical labels and random trajectories are tied
to these versions and the recorded source hashes.

Next: target non-C5 maximal graphs with d>=8; add operators that retain
nonmaximal states to study near-equality; seed from high-d alternative
constructions; increase independent restarts and compare operator discovery
rates. Investigate a quantitative stability statement rather than assuming
exact twin structure. A separate solver or formally checked certificate would
provide stronger assurance than agreement between enumeration implementations.

Final validation: **59 pytest tests passed, none skipped**, including nauty
integration, interrupted/resumed exhaustive evaluation, source/input mismatch
rejection, canonical-label invariance, independent solver checks, mutations,
seeded replay across restart boundaries and multiple seeds, and saved artifacts.
The saved source hashes match the current evaluators. `git diff --check` passed.
