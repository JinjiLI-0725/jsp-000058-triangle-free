# Induction checkpoint — 2026-09-19, four-boundary outside budget

JSP-000058 and general induction lemmas A/B remain **CONJECTURAL**.
Exactly one bottleneck was addressed and resolved: the s=k-1
private-transversal B gap for balanced pieces with four retained attachment
vertices. See [INDUCTION_FOUR_BOUNDARY_BUDGET.md](INDUCTION_FOUR_BOUNDARY_BUDGET.md).

## PROVED

With at most five outside vertices, each of the three size-dependent
four-root profile rows is dominated or tied by a slope-zero row after
one root is recolored. Fixing the outside coloring, the sums of four
root-flip costs are at most 2N, 2N, N in the three cases. Including the
constant piece penalties gives an available flip of cost at most 2, 3, 2
for N<=5, respectively, never exceeding the original penalty 2t in the
admissible size ranges. This includes the smallest case t=1.

The optimized glued profile is therefore t^2+K, with K independent of t.
At s=k-1 any private transversal has exact increment 2s-1=2k-3, with
an explicit remainder-optimal q=0 coloring and extension cost e=2s-1.
Combined with the previous 2s+1 bound for s<=k-2, every proper balanced
piece with at most four attachment roots and a private transversal
supplies B (and A), with gamma<=2k-3. The isolated B_1 case is included.
Equal-d spanning-core transfer preserves the increment bound, without
asserting preservation of a q=0 coloring in the original graph.

## COMPUTATIONALLY VERIFIED

The new tests check all three slope-two orbits, their four flip profiles,
every independent root neighborhood and outside color, and all reachable
aggregate flip-cost vectors from at most five outside vertices. Fixed
glued examples are independently minimized over all feasible part counts
and outside colorings, with nested optimum/extension checks.

Earlier four- and three-boundary regressions verify the all-size
polynomial certificates, orbit coverage, small full-cut profiles, and the
unrestricted-outside counterexample.

Validation:
`.venv/bin/python -m pytest -q tests/test_induction_four_boundary_budget.py tests/test_induction_four_boundary_selection.py tests/test_induction_three_boundary_selection.py`
— **8 passed in 24.81 seconds**. The test job has finished. These are checks
of the symbolic proof and fixed examples, not arbitrary-order A/B tests.

## FALSIFIED — previous rejection remains valid

Universal exact increment 2s-1 for four roots with unrestricted outside
order is still false. The previous path attachment has 4(2s+1) outside
vertices, so it is outside the present five-vertex budget. The constrained
boundary profiles themselves remain size-dependent. Only the optimized
profile after gluing with this small outside budget is size-independent.

## CONJECTURAL / next mathematical gap

General five-set q+e selection remains open for residual nonautomatic
critical cores without existing selection certificates. The four-boundary
certificate now has no s=k-1 B gap. There is still no reduction of arbitrary
cores to balanced pieces; arbitrary blocks and larger attachment boundaries
remain outside the theorem. Mixed balanced extensions at t=2 remain open.
No potential complete solution appeared.

## Coverage and clean stopping point

All completed t=1,...,25 JSON artifacts were read in full: complete=true,
max_gap=0. They certify homogeneous neighborhoods. They do not combine
with the arbitrary t>=26 symbolic theorem to prove all mixed cases;
later symbolic results reach t>=3 and leave mixed t=2 open. No balanced-
remainder extension theorem was used as a premise. The t=5 empty witness
does not classify equality. No enumeration was repeated or random search run.
Process inspection preceded computation; only one compute job ran at a time.
Unrelated overnight logs were left untouched.

`git diff --check` passed. Final process inspection found no running compute
job. Notes and state are synchronized at this clean research checkpoint.
