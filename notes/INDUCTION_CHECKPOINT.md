# Induction checkpoint — 2026-09-18

Progress is saved in `INDUCTION_ROUTE.md`. A and B remain conjectural.

## Proved so far

- Exact induction implications of both lemmas and the five-vertex base case.
- Exact excess-plus-extension identity for a fixed five-vertex deletion.
- Sparse-boundary and sequential-degree sufficient conditions.
- From first principles: minimum degree at least 2k forces a triangle-free
  graph on 5k vertices to be bipartite or the balanced C5 blow-up.
- From first principles plus the existing blow-up formula: a triangle-free
  extension of B_t by five vertices, t>=26, obeys the conjectured bound,
  strictly unless the resulting graph is B_(t+1).
- Exact deficit formula for a fixed internal five-vertex graph F and type map:
  `D_min=t(10-Σ_j α(F[S_j]))`, proved by independent per-part assignments.

## Conjectural and missing

A: find X and a coloring c of H=G-X with
`b_H(c)-d(H)+e_X(c)<=2k-1` in the general unresolved case.

B: exclude a nonbalanced graph with all five-deletion increments at least
2k-1; equivalently obtain the same expression <=2k-2 for some X,c.
The balanced-remainder special case above does not settle this.

The balanced-remainder extension claim for t=1,...,25 is also unresolved.
The exact maximal-extension enumerator was written and started, but stopped
before completion; no partial output is being presented as certification.

Updated finite status: the optimized exact enumerator completed t=1,2,3,4.
Each checked 242,500 normalized configurations and 1,245,367 maximal
neighborhood configurations, with maximum gap d-(t+1)^2 equal to 0. Results
are saved under `results/balanced_extension/t1.json` through `t4.json`.
The same run for each remaining t is about two minutes, leaving an estimated
38--45 minutes for t=5,...,25. No claim is made for those t values.

## Finite verification status

**COMPUTATIONALLY VERIFIED:** all 388 triangle-free labeled graphs on five
new vertices, all 625 normalized type maps, and the exact deficit reduction
were specified; the 388×625 diagnostic reproduced the finite L/W maxima
recorded in `INDUCTION_ROUTE.md`.

**COMPUTATIONALLY ATTEMPTED, NOT CERTIFIED:** varying every maximal
independent neighborhood choice and exact ten-bit cuts for every t<=25 did
not finish in this window. Therefore no t in 1,...,25 is marked proved or
falsified, and no explicit counterexample was found.

The stronger current statement is: t=1,2,3,4 are **COMPUTATIONALLY
VERIFIED**; t=5,...,25 remain **UNRESOLVED**.

## Single best next action after reset

Sharpen the five-new-vertex argument (equation (4) in the route note) to
cover t=1,...,25 by replacing the unfinished Cartesian-product run with a
symbolic branch-and-bound over the five part supports. First certify whether
the five base cuts already suffice; if not, add the finitely many cut types
that differ inside a remainder part. Use the saved scripts as the exact
starting point, and preserve proof versus computation labels.

This checkpoint will be finalized with the targeted literature findings,
symbolic counterexamples to stronger rules, and bounded experiment results.

## Update — completed finite balanced-extension verification

The previous finite-status section is superseded by the following result.

COMPUTATIONALLY VERIFIED:

For every t = 1,...,25, the optimized exact checker completed the full
enumeration.

For each t:
- 242,500 normalized configurations were checked;
- 1,245,367 maximal neighborhood configurations were evaluated;
- maximum gap d-(t+1)^2 was 0;
- no counterexample was found.

Final result files are stored at:

results/balanced_extension/t1.json
...
results/balanced_extension/t25.json

Therefore the finite t<=25 balanced-remainder gap is closed computationally.

The next priority is NOT to repeat this enumeration.

The remaining research task is to combine:
1. the exhaustive t<=25 verification;
2. the symbolic t>=26 argument;

and then determine whether the resulting balanced-remainder theorem can
advance induction lemmas A or B toward the full JSP-000058 conjecture.
