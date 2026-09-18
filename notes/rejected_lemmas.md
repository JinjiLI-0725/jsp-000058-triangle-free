# Rejected lemmas and unsafe research shortcuts

## R4: every balanced-remainder extension has a homogeneous supergraph

**FALSIFIED (2026-09-18).** Let H=B_2, add five vertices whose sole internal
edge is xy, and attach x and y to distinct vertices a,b in the same H part.
The graph is triangle-free. Any common X-neighborhood for a,b that contains
both original neighborhoods contains x,y and creates a triangle with xy.
Thus the claimed fixed-part homogeneous spanning-supergraph reduction fails.
The completed t=1,...,25 enumerations remain valid for their homogeneous
family. This is not a falsification of the bound, A, B, or a possible separate
numerical domination theorem. Full proof and corrected representation:
[BALANCED_EXTENSION_AUDIT.md](BALANCED_EXTENSION_AUDIT.md).

## Earlier rejections

The following are concrete counterexamples to overly strong structural guesses,
not counterexamples to JSP-000058. Every example has 15 vertices and was checked
for triangles and evaluated with both exact MaxCut implementations.
Full canonical graphs, edge lists, cut witnesses, and structural data are in
`results/structural_checks.json`.

## R1: more edges implies larger d among triangle-free graphs of fixed order

Rejected. K7,8 has 56 edges, MaxCut 56, and d=0. The balanced C5 blow-up with
weights (3,3,3,3,3) has 45 edges, MaxCut 36, and d=9. Thus edge count alone is
not a valid objective for this search.

This does not contradict monotonicity under edge inclusion: if an edge is
added on the same vertex set, MaxCut increases by either zero or one, so d
cannot decrease. The counterexample compares graphs with different edge sets.

## R2: every maximal triangle-free graph is extremal for d

Rejected by the same pair. Both K7,8 and the balanced C5 blow-up are maximal
triangle-free (every missing edge closes a triangle), but their d values are
0 and 9. Maximal completion is a useful search operation, not an extremality
certificate. Greedy maximal generation can still miss important graphs.

## R3: d>=8 on 15 vertices forces a C5 blow-up

Rejected. Delete one edge from the balanced (3,3,3,3,3) C5 blow-up. The resulting
graph is triangle-free, has 44 edges, MaxCut 36, and d=8. Its false-twin quotient
has seven vertices, so it is not a positive-weight C5 blow-up. Deleting edges
can preserve proximity to the target while destroying the exact module
structure. This example does not reject a quantitative edit-distance stability
statement.

## Methodological rejection: heuristic coverage is exhaustive coverage

The k=3 search samples and mutates graphs and enumerates specific blow-up
families. Neither repeated discovery of d=9 nor failure to find d>9 implies
exhaustive coverage of all triangle-free 15-vertex graphs. Only the separate
k=2 canonical-generation run is exhaustive at its specified order.
