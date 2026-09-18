# Fixed slack windows fail at the A/B thresholds on 2-connected cores

Date: 2026-09-18. **Single bottleneck:** can 2-connectedness justify a
universal constant slack window for certifying a specified five-set at
an A/B threshold? **FALSIFIED**, by the symbolic family below. Unlike the
earlier obstructions, these examples actually give false positives at
those thresholds, rather than merely an incorrect exact increment below
the threshold. This does not falsify the existence statements A or B.

## Construction and compatibility — PROVED

Use Q, Y={0,1,3,8}, and J_a from
[INDUCTION_SLACK_AMPLIFICATION.md](INDUCTION_SLACK_AMPLIFICATION.md).
Thus Q is Petersen with edges 01 and 38 replaced by three-edge paths;
J_a consists of a copies of Q sharing exactly the independent set Y.
For every a>=1 the established properties are

    |J_a|=10a+4, d(J_a)=3a, d(J_a-Y)=0,
    max_{c optimal} r_Y(c)=2a,
    min{b_J_a(c): c proper on J_a-Y}=4a.                 (1)

Also J_a has an optimal coloring with vertices 0 and 1 equal: take a
Petersen optimal cut with monochromatic triple {01,38,79}, extend the
replacement paths optimally, and copy it to all copies. No compatibility
of independently selected Q colorings is assumed in (1).

Take B_h, h>=3, and identify two distinct vertices of its part A_0 with
vertices 0 and 1 of J_a. Choose a third vertex z of A_0. Otherwise the
vertex sets are disjoint. Finally replace the edge 79 in the FIRST Q
copy by a path of length nine with eight fresh internal vertices.
Call the graph F_(a,h), and put X=Y union {z}.

For any prescribed colors of the two identified vertices, B_h has an
optimal coloring of cost h^2 with those colors. Indeed color A_1 and A_4
oppositely, alternate along A_1,A_2,A_3,A_4, and color A_0 arbitrarily.
The three pairs not touching A_0 contribute zero; every A_0 vertex
contributes exactly h. This is also why the cost-four Q coloring, whose
0 and 1 have opposite colors, is compatible with a B_h optimum.

Replacing an edge by an odd path preserves minimum cost for fixed colors
of all old vertices: the path minimum is 1 for equal endpoints and 0
otherwise. Its sole monochromatic edge in the first case can be placed
anywhere. Hence subdivision preserves d and edge-criticality here. The
subdivided edge 79 is entirely outside X. It therefore also preserves
remainder minimum cost, the optimal incident maximum, and minimum full
cost subject to an optimal remainder. For this last assertion, restriction
to old vertices cannot increase either cost; conversely an optimal path
extension attains both old costs simultaneously. A remainder-optimal
coloring must minimize its path, since its endpoints are retained.

## Structural claims — PROVED

F_(a,h) is simple and triangle-free. The identified pair 0,1 is independent
in both pieces. Any triangle meeting both pieces would need either an edge
between their private vertices or an edge between 0 and 1; neither exists.
The long subdivision creates no triangles.

It is 2-connected. Petersen stays connected on removal of any vertex:
if an outer vertex is removed, the inner five-cycle is intact and every
remaining outer vertex attaches to it by a spoke; the inner-vertex case
is symmetric. Odd subdivision preserves 2-connectedness (as does any
subdivision of an edge in a 2-connected graph). Thus Q is 2-connected.
Gluing 2-connected graphs along at least two vertices preserves this
property: after any one vertex is removed each piece stays connected,
and at least one common vertex remains. Apply this first to the Q copies
sharing Y and then to B_h sharing {0,1}. B_h is 2-connected since after
any vertex deletion its five nonempty parts still form a cycle blow-up.
The final subdivision also preserves 2-connectedness.

The graph is edge-critical. For an edge in J_a, take its established
optimal monochromatic witness and extend its 0,1 colors to an optimal
B_h coloring using the flexibility just proved. For an edge of B_h,
use a part-respecting optimum with its pair monochromatic: this gives
0 and 1 equal, compatible after global reversal with the equal-terminal
optimum of J_a above. These witnesses have total cost 3a+h^2, which
is a lower bound from the two edge-disjoint pieces. Subdivision transfers
the witness for 79 to any chosen edge of its replacement path. Every edge
is therefore monochromatic in an optimal full cut, proving criticality.

In particular, no assertion about arbitrary two-vertex gluing is used:
the explicit boundary flexibility is essential. F_(a,h) is not B_k:
it has subdivision vertices of degree two, whereas B_k is 2k-regular.

## Exact cut quantities — PROVED

The order and full optimum are

    |F_(a,h)|=10a+4+5h-2+8=5k,   k=2a+h+2,
    d(F_(a,h))=3a+h^2.                                  (2)

Deleting X separates the remaining Q pieces from B_h. The Q remainders,
including the odd subdivision of the retained edge 79, are bipartite.
The remaining blow-up has sizes (h-3,h,h,h,h), and hence d=h(h-3),
including h=3. Consequently

    gamma(X)=3a+3h.                                     (3)

Every full optimum minimizes both original pieces. Its incident count
from J_a is at most 2a. The three X vertices in A_0 are independent;
each has degree 2h inside B_h, and in any B_h optimum each has at most h
monochromatic edges, or flipping it would improve the cut. Thus L<=2a+3h.
Choose an optimum of J_a attaining 2a, and the flexible A_0 coloring
above: every A_0 vertex has exactly h monochromatic incident edges,
regardless of the prescribed colors. Optimal subdivision preserves this.
Therefore

    L(X):=max_{c optimal} r_X(c)=2a+3h.                  (4)

A coloring attaining gamma in the full-cut identity must be optimal on
the remainder. It is proper on every Q remainder, so its J_a cost is at
least 4a. Its B_h cost is at least h^2. Conversely, copy the cost-four
Q coloring, extend B_h by the flexible A_0 construction, and extend the
subdivided edge optimally. The remainder cost is h(h-3), since every
retained A_0 vertex contributes h and all other pairs cross. Therefore

    min{s(c): r_X(c)-s(c)=gamma(X)}=a.                  (5)

This proof pays for remainder reoptimization explicitly: it uses the
identity r_X-s=d(F)-b_(F-X), not an upper bound inferred from an optimal
full cut's incident count.

## False positives exactly at the induction thresholds — FALSIFIED

The rejected claim is: **there exists a universal integer C>=0 such
that on every nonautomatic 2-connected triangle-free edge-critical graph
of order 5k, a specified five-set passes A (respectively B) whenever
r_X(c)<=T+s(c) for all full cuts of slack at most C.**

For B, choose h=a+3. Then

    k=3a+5, d=a^2+9a+9, T_B=2k-2=6a+8,
    gamma=6a+9=T_B+1, L=5a+9<=T_B.

For A, choose h=a+4. Then

    k=3a+6, d=a^2+11a+16, T_A=2k-1=6a+11,
    gamma=6a+12=T_A+1, L=5a+12<=T_A.

Both families have d>=2k for every a>=1, so both are in the nonautomatic
critical-core domain. In each case the scores r_X-s are integers and at
most gamma=T+1. A violation of the threshold must therefore attain gamma
exactly. By (5) its minimum possible slack is a. For ANY proposed C,
choose a>C: every cut through slack C passes, but gamma>T. This proves
the claimed false positive, separately for the A and B thresholds.

The graph-dependent window U_X-T-1 in
[INDUCTION_THRESHOLD_SLACK.md](INDUCTION_THRESHOLD_SLACK.md) remains valid.
This result falsifies replacing that window by a universal constant,
even for 2-connected cores and even just for deciding the threshold.

## Limits and validation

**CONJECTURAL:** A, B, and JSP-000058 remain unresolved. The exhibited X
fails the indicated threshold; an existential lemma can choose another X.
Indeed five consecutive internal vertices of the new nine-edge path give
an increment at most one: for any fixed coloring of the remainder, the
deleted five-vertex path can be colored with at most one monochromatic
edge in the six-edge connection between its retained endpoints. This also explicitly supplies A/B witnesses
in these graphs. No potential complete proof appeared.

**COMPUTATIONALLY VERIFIED:** a bounded regression enumerates every Q
coloring, retains all sixteen Y color patterns, and joins exact cost tables
only at equal shared colors. The B_h table enumerates counts in its parts
and all colors of its three distinguished vertices, which is exact even
for cuts splitting parts. It checks (2)--(5) and the threshold false
positives for a=1,2,3 and h=a+3,a+4. Independent graph checks test triangle-
freeness and connectivity after each one-vertex deletion. A path truth
table checks both endpoint parities and all monochromatic-edge positions.
These are tests of one specified construction, not a random graph search
or exhaustive A/B certification. Test outcomes are in the checkpoint.

All t=1,...,25 artifacts were read and have complete=true, max_gap=0.
They cover homogeneous neighborhoods. The original arbitrary t>=26
argument therefore does not combine with them into an all-t arbitrary
extension theorem; subsequent notes reach t>=3, leaving mixed t=2 open.
No balanced-extension result is a premise here and none was recomputed.
