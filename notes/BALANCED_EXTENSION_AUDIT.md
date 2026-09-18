# Balanced-extension coverage audit — 2026-09-18

> **Subsequent progress:** [BALANCED_EXTENSION_COVER_BOUND.md](BALANCED_EXTENSION_COVER_BOUND.md)
> proves the arbitrary strict extension theorem for t>=8 without enumeration.
> The unresolved mixed range stated as 2<=t<=25 below is now 2<=t<=7.
> The coverage correction and exact formula in this audit remain valid.

JSP-000058 remains open. This cycle addresses exactly one bottleneck:
**does the completed homogeneous-neighborhood enumeration cover arbitrary
five-vertex extensions of a balanced remainder?** This prerequisite must be
settled before those computations can remove the balanced-remainder case
from induction A or the strict transition in B_inherit.

## Classification and outcome

- **COMPUTATIONALLY VERIFIED:** all saved t=1,...,25 runs are complete,
  each with 242,500 configurations, 1,245,367 maximal neighborhood choices,
  and max_gap=0. The enumeration was not repeated. These artifacts certify
  the enumerated homogeneous family, not all mixed-neighborhood extensions.
- **FALSIFIED:** the claimed reduction that every extension is a spanning
  subgraph of an enumerated homogeneous extension, with its remainder parts
  fixed. The explicit counterexample below is a mathematical disproof.
- **PROVED:** arbitrary extensions have the pattern-count representation
  and exact sorted-unary cut formula below. Completing each individual
  pattern to a maximal independent pattern is a valid bound-only reduction.
- **CONJECTURAL:** every mixed-pattern extension for 2<=t<=25 satisfies
  the target bound. No counterexample to that bound, A, B, or JSP-000058
  has been obtained. The failure of a coverage argument does not falsify
  any of those statements.

## What the code actually checks

For F=G[X] and f:X->Z/5Z, let S_j={x:f(x)=j-1 or j+1}. Each x has its
H-neighborhood in A_(f(x)-1) union A_(f(x)+1), since that neighborhood is
independent in B_t. A type exists also for empty or single-part support.
Rotation permits f(0)=0 without losing any graph in the represented family.

Both saved checkers choose **one** maximal independent subset I_j of F[S_j]
per part and join every one of the t vertices of A_j to precisely I_j.
Within this family the five remainder parts really are twin classes.
Rounding each twin class to one side proves that the 512 cuts modulo
complementation compute exact d. The polynomial is c0+c1*t+c2*t^2.
Enumeration of F, f, and the five choices therefore has the advertised
scope. No loop enumerates multiple patterns or their multiplicities in a part.

The t=5 artifact has best_d=0 and an empty witness. The C++ resume loader
restores maxgap and counts but not bestd/wit, and only updates the witness
on a strictly larger gap. This explains how a completed resumed run can
lack a maximizing witness; it is not evidence that the bound failed.
The artifact's coverage fields and max_gap agree with the other runs.
No artifacts were modified, and no provenance stronger than the saved
results and source audit is claimed.

## Explicit falsification of spanning-supergraph coverage

Take H=B_2 with A_j={a_j,b_j}. Add X={x,y,z_1,z_2,z_3}, with its sole
internal edge xy. Add only the boundary edges x a_1 and y b_1. The z's
are isolated. This graph is triangle-free: H is triangle-free, x and y
have no common neighbor, and each has only one neighbor in H. Choose
f(x)=f(y)=0 (and any valid types for the isolated vertices).

The two neighborhoods in A_1 are {x} and {y}. Any common neighborhood
containing both must contain {x,y}, which is not independent in F. Making
A_1 homogeneous by adding edges therefore creates a triangle. Changing f
does not help a homogeneous supergraph on these fixed parts: the union
still contains xy. Thus the asserted spanning-supergraph domination fails.
The construction works for every t>=2 by leaving other H-to-X edges absent.

This does NOT prove that some homogeneous graph cannot dominate this graph
in the numerical objective d. Such a separate extremal theorem might exist,
but none has been proved. Monotonicity under edge addition cannot supply it
through the asserted supergraph construction. Nor does twin rounding apply
to the original mixed part, whose vertices do not have identical neighbors.

## Correct representation and exact cut identity — PROVED

For every independent I subset S_j let n_(j,I) be the number of vertices
of A_j with X-neighborhood I. Then n_(j,I) are nonnegative integers and
sum_I n_(j,I)=t for each j. These conditions, together with triangle-free F
and the support definition, are necessary and sufficient for triangle-freeness:
triangles with two X vertices are excluded by independence of I; triangles
with one X vertex are excluded by its two nonconsecutive allowed H parts;
the other triangles are already absent in H and F.

It is valid to enlarge each vertex's pattern I separately to a maximal
independent subset of F[S_j]. This preserves triangle-freeness and only
increases d. Different vertices can require different maximal patterns.
Consequently a valid exhaustive upper-bound search may use counts over
maximal patterns. It may not set one count to t and all others to zero
without an additional proof. Equality classification requires additional
care even under valid edge completion: monotonicity alone need not be strict.

Here is an exact cut formula for arbitrary counts. Fix a coloring a of X.
For each vertex v in A_j, with pattern I_v, let

    u_v(0)=|{x in I_v:a(x)=0}|,
    u_v(1)=|{x in I_v:a(x)=1}|,
    delta_v=u_v(1)-u_v(0).

Sort the t deltas in A_j increasingly as delta_(j,1),...,delta_(j,t).
If precisely s vertices of A_j receive color 1, the minimum boundary cost is

    U_j(a,s)=sum_(v in A_j) u_v(0) + sum_(r=1)^s delta_(j,r).

This follows by selecting the s cheapest increments. For fixed part counts
s_0,...,s_4, edges inside H contribute exactly

    Q_t(s)=sum_j [s_j*s_(j+1)+(t-s_j)*(t-s_(j+1))].

These costs depend only on the part counts, so minimizing boundary costs
independently inside each part loses no information. Thus, exactly,

    d(G)=min_(a in {0,1}^5) min_(s in {0,...,t}^5)
         [b_F(a)+Q_t(s)+sum_j U_j(a,s_j)].                    (M)

This accounts for nonoptimal remainder cuts as required by the q+e identity.
Indeed d(H)=t^2, Q_t(s)-t^2>=0 is precisely their excess q. The expression
in brackets minus t^2 is the full extension increment after optimization.
The minimum can be reduced to 16 X colorings modulo global complementation.
The reference implementation deliberately uses the direct finite formula;
it is not a newly launched exhaustive search.

## How the finite and symbolic ranges combine

The t>=26 proof in INDUCTION_ROUTE.md uses D>=t when an incompatible
X-edge exists. That argument allows different neighborhoods inside H parts:
adjacent X endpoints have disjoint neighborhoods in a common allowed part.
Its five explicit colorings remain legitimate even when H vertices have
different X-neighborhoods. W<=30 then gives W-D<=4 and the strict bound.
If all X-edges have consecutive types, completion to a C5 blow-up is valid
and the existing AM--GM/equality argument applies. Thus that symbolic proof
survives the present audit unchanged.

For t=1 every part has just one vertex: there is no mixed-pattern gap.
Per-vertex maximal completion is then exactly the enumerated search. Hence
the saved t=1 computation certifies the full non-strict extension bound.
The separately saved exhaustive n=10 result also classifies equality there.

For 2<=t<=25 the runs certify the homogeneous family. They do not combine
with the symbolic theorem to establish an all-t theorem for arbitrary
extensions until (M) is bounded for mixed patterns or a valid numerical
domination theorem is proved. Moreover max_gap=0 plus a single maximizing
witness does not classify all equality cases even in the enumerated family.
The finite certificates therefore cannot supply B's strictness clause.

## One precise remaining claim and induction consequences

The remaining coverage claim is:

**CONJECTURAL M:** For each 2<=t<=25, each triangle-free F on five vertices,
each normalized type map f, and every multiplicity vector over maximal
independent patterns in S_j with part sums t, the minimum in (M) is at most
(t+1)^2.

M is sufficient for the non-strict balanced-remainder case of A, using
monotonicity for the per-vertex completion. The strict analogue needs an
argument for all nonbalanced original graphs, including proper subgraphs
of any completed equality graph; it does not follow from M alone.
Even establishing both would not settle general A or B: arbitrary
remainders still require finding X,c with q_H(c)+e_X(c)<=2k-1 (or 2k-2).

The next useful step on this SAME bottleneck is a proof of M, or a precise
counterexample to a proposed numerical homogenization inequality. Repeating
the completed homogeneous enumeration would add no coverage. No broad
random search or long-running computation was launched in this cycle.

## Validation

The new targeted tests check the explicit coverage counterexample, compare
(M) with independent full-graph Gray-code cuts on fixed homogeneous and mixed
examples, and read all 25 saved artifacts without rerunning their search.
See the current checkpoint for the test outcome.
