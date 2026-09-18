# Five-set selection through a two-vertex boundary

Date: 2026-09-18. The single bottleneck is five-set q+e selection in
residual critical cores. This cycle proves a selection rule for a balanced
piece with two retained attachment vertices. General A/B remain CONJECTURAL.

## Flat boundary profiles — PROVED

For a graph P and boundary S, write F_P(a) for the minimum number of
monochromatic edges over colorings extending a:S->{0,1}. For P=B_s and
any S of at most two vertices,

    F_P(a)=s^2 for every a.                              (1)

The lower bound is d(B_s)=s^2. For two roots in different parts, consider
the five part colorings with one monochromatic cycle edge. On a path of
length l=1 or 2 between the root parts, their color relation changes
according as that sole monochromatic edge lies on or off the path.
Both choices exist. Global reversal supplies the prescribed absolute
colors. For roots in the same part with the same color, a part coloring
suffices. If they have opposite colors, color the other four parts
alternately along their path. The two neighboring parts then have opposite
colors. Every vertex in the root part contributes exactly s monochromatic
edges, regardless of its own color, and there are none elsewhere. This
also shows that an arbitrary coloring of one entire part is extendible
at cost s^2. Zero or one root is immediate. No cut-rounding assumption
is made for the opposite-color, same-part case.

For an edge-disjoint union G=P union R with V(P) intersect V(R)=S,

    d(G)=min_a [F_P(a)+F_R(a)].                           (2)

This is exact by restricting and combining colorings. In particular (1)
implies d(G)=s^2+d(R), regardless of the boundary preferences of R.
If the two roots are adjacent, assign their shared edge only to P;
R is allowed to omit it. Double-counting that edge would invalidate (2).

## A private transversal — PROVED

Suppose G is triangle-free on 5k vertices, P is an induced B_s, and all
edges from P to outside P have their P endpoint in a set S of at most
two retained vertices. Suppose s>=2 and every part has a vertex outside
S. This holds for s>=3, and for s=2 unless both roots occupy the same
part. Choose a transversal X disjoint from S. Then P-X=B_(s-1), still
containing S, so both boundary profiles are constant. Applying (2) twice,

    gamma_G(X)=s^2-(s-1)^2=2s-1.                         (3)

If P is proper, 5s<5k implies s<=k-1, and (3) is at most 2k-3.
Thus this X satisfies B and A. For P=G=B_k it satisfies A, as expected.
The result does not require criticality or any bound for R. Applied to an
equal-d spanning critical core, its witness transfers to the original
G by the proved core-transfer inequality.

The q+e obstruction is resolved explicitly for this X. Take an optimal
coloring of R and its boundary assignment a. The proof of (1) constructs
nested optimal colorings on B_(s-1) and B_s agreeing on retained vertices:
use the same part coloring for distinct root parts or equal root colors;
for opposite roots in one part, use the alternating four-part path and
arbitrary colors in the remaining part at both sizes. Hence a full coloring
has cost s^2+d(R), and its restriction has cost (s-1)^2+d(R). The latter
is optimal: q=0, and extension cost e=2s-1 (a cheaper extension would
contradict the full optimum).

This goes beyond pendant blocks. Identify two nonadjacent vertices in
different parts of two B_s copies and add two isolated vertices. For
s>=2 this has order 10s, k=2s, d=2s^2>=2k. Its nonisolated part is
2-connected: each copy stays connected after any one vertex deletion,
and at least one shared vertex survives. Every edge is critical: an
optimal coloring making it monochromatic in its own copy can be matched
by an optimum in the other using (1). Every nonisolated vertex has degree
at least 2s, yet a private transversal has increment 2s-1. The only
vertices of degree at most three are the two isolates. Thus the new rule
covers nonautomatic, higher-degree critical cores beyond pendant cases.

## Limits and falsification safeguards

CONJECTURAL: selection on residual cores with no automatic, path, pendant,
or feasible two-boundary balanced-piece witness. There is no general
reduction to such balanced pieces, or to 3-connected cores. The s=2 case
with both attachment vertices in one part is excluded by feasibility,
not declared a counterexample. Arbitrary deletions need not preserve (1).

FALSIFIED: extending flat profiles to arbitrary boundary size. Take all
vertices as boundary and prescribe color zero everywhere: the constrained
cost is 5s^2 rather than s^2. No maximal valid boundary size is claimed.
The earlier two-path C5 example already falsifies
unconditional two-boundary additivity for arbitrary pieces.

COMPUTATIONALLY VERIFIED results are recorded after the tests below.
The symbolic proof, not these finite tests, establishes (1)--(3).

## Balanced-extension coverage audit

All saved t=1,...,25 artifacts were read and have complete=true and
max_gap=0. They cover homogeneous remainder-part neighborhoods; the
arbitrary t>=26 argument therefore does not combine with them into an
arbitrary all-t theorem. Later symbolic results reach t>=3, with mixed
t=2 still unresolved. The t=5 empty witness does not classify equality.
No balanced-extension theorem is used above; no enumeration was repeated.
