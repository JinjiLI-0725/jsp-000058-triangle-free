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

## Conjectural and missing

A: find X and a coloring c of H=G-X with
`b_H(c)-d(H)+e_X(c)<=2k-1` in the general unresolved case.

B: exclude a nonbalanced graph with all five-deletion increments at least
2k-1; equivalently obtain the same expression <=2k-2 for some X,c.
The balanced-remainder special case above does not settle this.

## Single best next action after reset

Sharpen the five-new-vertex argument (equation (4) in the route note) to
cover t=1,...,25: enumerate only triangle-free graphs on the five new
vertices and their five type assignments, then derive exact bounds on
neighborhood deficits forced by incompatible edges. This is a bounded
test of the missing balanced-remainder claim, not a broad graph search.

This checkpoint will be finalized with the targeted literature findings,
symbolic counterexamples to stronger rules, and bounded experiment results.
