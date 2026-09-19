# Rejected lemmas and unsafe research shortcuts

## R9: critical-path deletion losses add

**FALSIFIED (2026-09-18).** Two terminals joined by two length-two and two
length-three internally disjoint paths give a triangle-free edge-critical
graph with d=2. Each individual path-interior deletion has loss one, but
deleting interiors of one path of each parity has total loss one, while
deleting interiors of two even paths has loss two. Exact signed-path
reoptimization, not summation of single-path losses, gives the increment.
See [INDUCTION_THREAD_SELECTION.md](INDUCTION_THREAD_SELECTION.md).
This does not refute A/B; two isolates pad the example to order ten.

## R8: a constant slack window decides A/B thresholds on 2-connected cores

**FALSIFIED (2026-09-18).** The family F_(a,h) in
[INDUCTION_TWO_CONNECTED_SLACK.md](INDUCTION_TWO_CONNECTED_SLACK.md)
is triangle-free, 2-connected, edge-critical, and nonautomatic. For
h=a+3 at B's threshold, or h=a+4 at A's threshold, its specified five-set
has gamma=T+1, and the minimum slack of any threshold-violating cut is a.
Taking a larger than any proposed constant produces a false positive.
This strengthens R7 from incorrect exact evaluation below the threshold
to incorrect threshold decisions, and removes the articulation vertex.
It does not refute A/B: another five-set in the same graph has increment
at most one. Graph-dependent slack windows remain valid.

## R7: connectedness repairs optimal-cut or constant-slack sufficiency

**FALSIFIED (2026-09-18).** The symbolic connected, bridgeless critical
family K_a in [INDUCTION_CONNECTED_SLACK.md](INDUCTION_CONNECTED_SLACK.md)
has a five-set with gamma=3a+1, optimal-cut maximum 2a+1, and minimum
maximizing slack a, for every a>=1. All members lie in the nonautomatic
A/B domain. This strengthens the earlier disconnected examples and the
[slack amplification result](INDUCTION_SLACK_AMPLIFICATION.md).
It does not refute A/B or a claim about specially selected five-sets;
these graphs have a cut vertex, so 2-connected restrictions are untested.

## R6: optimal full-graph cuts determine every critical-core deletion increment

**FALSIFIED (2026-09-18).** On G_s=Petersen disjoint-union B_s, s>=3,
choose X={0,1,3,8} in the Petersen labeling of
[INDUCTION_CUT_SLACK.md](INDUCTION_CUT_SLACK.md), together with one B_s
vertex. Then gamma(X)=s+3, while every optimal full-graph cut has at most
s+2 monochromatic edges incident with X. These graphs are edge-critical,
triangle-free, of order 5(s+2), and have d=s^2+3>=2(s+2), so the failure
occurs in the nonautomatic domain of both A_crit and B_crit. A cut with
slack one attains the exact increment. This refutes Candidate O, not A/B
or the possibility of choosing a different five-set with compatible cuts.

## R5: arbitrary spanning-subgraph reduction transfers deletion increments

**FALSIFIED (2026-09-18).** Let G=C5 plus five isolates and let C remove
one cycle edge. Delete X consisting of one cycle vertex and four isolates.
Then gamma_G(X)=1 while gamma_C(X)=0. Thus gamma_G<=gamma_C cannot be
inferred merely from C being spanning. The additional condition d(C)=d(G)
DOES make that inequality valid for every X, as proved in
[INDUCTION_CRITICAL_CORE.md](INDUCTION_CRITICAL_CORE.md). This is not a
counterexample to A or B.

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

## R10: balanced-piece boundary flatness extends to three roots

**FALSIFIED (2026-09-19).** Three prescribed zero-colored roots in consecutive
parts of B_s force constrained cost s^2+2. The exact proof and a triangle-free
gluing example with nonadditive deletion distance are in
[INDUCTION_THREE_BOUNDARY_SELECTION.md](INDUCTION_THREE_BOUNDARY_SELECTION.md).
Nevertheless the penalty is independent of s for every boundary of size at
most three. Private-transversal increments therefore remain exactly 2s-1.
This rejects flatness, not A/B or the three-boundary selection rule.

## R11: four-root pieces retain constant profile differences

**FALSIFIED (2026-09-19).** Two opposite-colored root pairs in nonadjacent
parts of B_s have constrained cost s^2+2s, hence size increment 2s+1.
Attaching M=2s+1 disjoint length-three paths between each pair forces this
row to minimize the glued cost, yielding an actual private-transversal
increment 2s+1 for s>=3. The graph is triangle-free and may be padded with
isolates to order 5k. This refutes the exact 2s-1 piece rule, not A/B.
[INDUCTION_FOUR_BOUNDARY_SELECTION.md](INDUCTION_FOUR_BOUNDARY_SELECTION.md)
proves the weaker universal 2s+1 bound and its selection consequences.

## R12: every five-root profile is a single quadratic in the piece size

**FALSIFIED (2026-09-19).** Five retained roots in parts 00113, colored
00001, have constrained cost t^2+min(2t,8) for every integer t>=2.
This has a genuine change of polynomial at t=4. The exact all-size
certificate is in [INDUCTION_FIVE_BOUNDARY_SELECTION.md](INDUCTION_FIVE_BOUNDARY_SELECTION.md).
The penalty's consecutive increments are still between zero and two,
which is sufficient for the private-transversal bound. The five-outside-
vertex budget also removes the B gap. This refutes a profile shortcut,
not A/B or the earlier four-root classification.
