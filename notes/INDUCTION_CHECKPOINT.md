# Induction checkpoint — 2026-09-19, five-boundary selection

JSP-000058 and general induction lemmas A/B remain **CONJECTURAL**.
Exactly one bottleneck was addressed and resolved: private-transversal
A/B selection for balanced pieces with five retained attachment roots.
See [INDUCTION_FIVE_BOUNDARY_SELECTION.md](INDUCTION_FIVE_BOUNDARY_SELECTION.md).

## PROVED

All 111 five-root color orbits have exact constrained profiles t^2 plus
one of 0, 2, 4, 6, 2t, 2t+2, min(2t,8). The explicit certificate is
[profiles.json](../results/induction_five_boundary/profiles.json).
Endpoint rounding and nonnegative coefficients in the integer basis
u(u-1), u, 1 prove the profiles for all admissible sizes. The piecewise
row has a separately checked finite region and an infinite region.

The penalty increments lie between zero and two. Thus a private
transversal has 2s-1<=gamma<=2s+1, with a q=0 upper-bound extension.
This supplies A for every proper piece, and B when s<=k-2.

With at most five outside vertices, all 14 nonconstant profile orbits
are dominated by constant rows. Two exceptional rows require weighted
single-root flips or a two-root flip. The optimized glued profile is
therefore t^2+K with K independent of t. At s=k-1 the private transversal
has exact gamma=2s-1 and q=0, resolving the remaining B case.

Consequently every proper balanced piece with at most five retained
attachment roots and a private transversal supplies B (and A), with
gamma<=2k-3. Equal-d spanning-core transfer preserves the bound, without
asserting that the same q=0 coloring transfers to the original graph.

## COMPUTATIONALLY VERIFIED

Tests check every orbit and polynomial coefficient; independently enumerate
full cuts for every five-root set and coloring in B_1 and B_2; check all
recoloring actions against every independent root neighborhood and outside
color; and minimize fixed glued examples over all feasible part counts
and outside colors, including nested optimal remainder/extension checks.
The existing four-boundary regressions also pass.

Validation:
`.venv/bin/python -m pytest -q tests/test_induction_five_boundary_selection.py tests/test_induction_four_boundary_budget.py tests/test_induction_four_boundary_selection.py`
— **9 passed in 41.69 seconds**. The test job has finished. These are
checks of the symbolic proof and fixed examples, not arbitrary-order A/B
certification. The bounded exploratory computations were confined to the
same boundary-profile and recoloring claim.

## FALSIFIED

The shortcut that every five-root profile is one quadratic polynomial
throughout its admissible range is false. Roots in parts 00113 colored
00001 have penalty min(2t,8). This does not refute A/B or the earlier
four-root classification. The earlier unrestricted-outside counterexample
to exact increment 2s-1 also remains valid.

## CONJECTURAL / next mathematical gap

General five-set q+e selection remains open for residual nonautomatic
critical cores without existing selection certificates. No reduction of
arbitrary cores to balanced pieces is known. Larger attachment boundaries
and graphs without such pieces remain outside this theorem. Mixed balanced
extensions at t=2 remain open. No potential complete solution appeared.

## Coverage and clean stopping point

All completed t=1,...,25 JSON artifacts were read in full: complete=true,
max_gap=0. Their homogeneous scope does not combine with the arbitrary
t>=26 symbolic theorem to prove all mixed cases. Later symbolic results
reach t>=3 and leave mixed t=2 open. No balanced-remainder theorem was
used as a premise. The t=5 empty witness does not classify equality.
No completed enumeration was repeated and no random search was run.
Process inspection preceded computation; bounded jobs ran sequentially.
Unrelated overnight logs were left untouched.

`git diff --check` passed. Final process inspection found no running compute
job. Notes and state are synchronized at this clean research checkpoint.
