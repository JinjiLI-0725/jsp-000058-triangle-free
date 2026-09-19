# Induction checkpoint — 2026-09-19, four-boundary selection

JSP-000058 and general induction lemmas A/B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: private-transversal q+e selection
for balanced pieces with four retained attachment vertices. See
[INDUCTION_FOUR_BOUNDARY_SELECTION.md](INDUCTION_FOUR_BOUNDARY_SELECTION.md).

## PROVED

Every four-root constrained profile of B_s is s^2 plus 0, 2, 4, or 2s,
with a fixed polynomial for each boundary placement/coloring. An explicit
47-row table and nonnegative quadratic coefficients certify every s in
its admissible range. This includes the lower bounds, not just witnesses.

If every part has a private vertex, deleting a private transversal gives
2s-1<=gamma<=2s+1. A remainder-optimal coloring supplies q=0 and an
extension of cost at most 2s+1. Thus every proper piece supplies A;
s<=k-2 supplies B. A minimizing remainder boundary row of slope zero
also supplies B for s=k-1. Equal-d core transfer preserves these bounds.

## FALSIFIED

Universal size-independent penalties and exact increment 2s-1 beyond
three roots. Root parts 0022 with colors 0101 have cost s^2+2s.
Attaching M=2s+1 internally disjoint paths of length three between each
root pair forces that profile to control both glued minima, giving actual
gamma=2s+1. This triangle-free construction does not refute A/B.

## COMPUTATIONALLY VERIFIED

All 47 normalized boundary rows and all 32 quadratic templates per row;
independent orbit coverage; full cuts of every four-root set in B_1/B_2;
independent feasible-part-count/path-cut checks of the glued obstruction
at s=3,4,5. Earlier three-boundary regressions are included.

Validation: `.venv/bin/python -m pytest -q tests/test_induction_four_boundary_selection.py tests/test_induction_three_boundary_selection.py`
— **6 passed in 21.61 seconds**. This checks the proof and fixed examples,
not arbitrary-order A/B enumeration. The test job has finished.

## CONJECTURAL / next mathematical gap

General five-set selection on residual nonautomatic critical cores remains
open. Within this four-boundary certificate, B is still unresolved by the
bound when s=k-1 and all optimal remainder boundary rows have slope two.
No claim is made that this obstruction can occur with only five outside
vertices, or that every residual core has a balanced piece. Arbitrary leaf
blocks and higher-degree cores remain unresolved.

## Coverage and clean stopping point

All completed t=1,...,25 JSON artifacts were read in full: complete=true,
max_gap=0. They certify homogeneous neighborhoods. They do not combine
with the arbitrary t>=26 symbolic theorem to prove all mixed cases;
later symbolic results reach t>=3 and leave mixed t=2 open. No balanced-
remainder result was used as a premise. The t=5 empty witness does not
classify equality. No enumeration was repeated and no random search run.
Process checks preceded computation; jobs were sequential. No potential
complete solution appeared. Unrelated overnight logs were left untouched.

`git diff --check` passed. Final process inspection found no running compute
job. Notes and state are synchronized at this clean research checkpoint.
