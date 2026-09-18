# Induction checkpoint — 2026-09-18, occupied-type cuts

JSP-000058 and general induction lemmas A and B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: the strict arbitrary mixed-neighborhood
balanced-extension theorem, selecting t=5 from the previous t=2,...,5 gap.
The resulting symbolic argument also covers t=4.

## Genuine progress — PROVED

Every triangle-free five-vertex extension of B_t for **t>=4** has
 d(G)<=(t+1)^2, with equality exactly for B_(t+1).
Full proof and inference audit:
[BALANCED_EXTENSION_TYPE_OCCUPANCY.md](BALANCED_EXTENSION_TYPE_OCCUPANCY.md).

For a noninjective valid type map, either two adjacent types are empty,
giving d<=t^2+6, or an empty-singleton type edge supplies a nonconstant
coloring of X and gives d<=t(t+1)+4. Both are at most t^2+2t for t>=4.
The internal bound follows because a nonconstant cut of a triangle-free
five-vertex graph leaves at most four monochromatic edges. The auxiliary
blow-up contains all H and boundary edges; incompatible internal edges
are explicitly paid for. No false containment inference is used.

For an injective type map, every S_j has size two, so W=m+2L and D>=tL.
When L>=1, W-D<=4 yields a strict bound. When L=0, the graph is a spanning
subgraph of B_(t+1), and every proper such subgraph is strictly below equality.
All constructed remainder cuts are optimal, so q_H=0; cut reoptimization
can only improve these valid upper bounds.

## Classifications and coverage

- **PROVED:** arbitrary strict balanced extensions for every t>=4,
  superseding the previous t>=6 threshold.
- **COMPUTATIONALLY VERIFIED:** all saved homogeneous t=1,...,25 artifacts
  are complete with max_gap=0. All were read; no enumeration was repeated.
  Their witness metadata does not classify equality; t=5 retains its
  previously documented empty-witness issue.
- **COMPUTATIONALLY VERIFIED:** arbitrary t=1 and equality from the separate
  exhaustive n=10 corpus; new bounded checks of the proof ingredients.
- **FALSIFIED (previous cycle):** homogeneous spanning-supergraph coverage
  of mixed neighborhoods. No new candidate lemma was falsified this cycle.
- **CONJECTURAL:** arbitrary strict mixed t=2,3; general A/B; JSP-000058.

Before use, the t<=25 homogeneous certification and t>=26 arbitrary
symbolic argument were checked. Their different scopes leave a finite
mixed gap; the new symbolic proof reduces that gap to t=2,3.

## Induction consequence and exact remaining obstruction

For k>=5, every X with G-X=B_(k-1) satisfies A and, for nonbalanced G, B.
By B_inherit, A plus equality uniqueness through k=4 would imply uniqueness
at all orders. General A and that finite equality base are not established.
For arbitrary remainders, finding X,c with q_H(c)+e_X(c)<=2k-1 (or <=2k-2
for B) remains unresolved. This partial theorem does not select X there.

The next step on the same bottleneck is t=3: the noninjective estimate
 t(t+1)+4=16 misses strictness d<=15 by one. The injective average as written
also needs refinement. Do not assume either bound is sharp or repeat the
completed homogeneous enumeration. No potential complete solution appeared.

## Validation and clean stopping point

Passed: `.venv/bin/python -m pytest -q tests/test_balanced_patterns.py
 tests/test_structural_analysis.py` — **12 tests**, 13.91 seconds.
The new regressions check the occupancy construction on 625 normalized maps,
the nonconstant-cut bound on all 388 labeled triangle-free five-vertex
graphs, and the injective overlap identity with all 24 normalized bijections.
These test proof ingredients, not extension families.
`git diff --check` passed.

A short preliminary t=5 repair diagnostic examined only internal shapes and
type maps with a loss-budget DP. Six failures of that particular sufficient
bound motivated the simpler symbolic proof; they were not graph
counterexamples. That process finished before the tests. Process inspections
found no pre-existing compute job, and no long-running research computation
or random search was launched. Saved result artifacts and pre-existing
log changes were left untouched. This is a clean checkpoint.
