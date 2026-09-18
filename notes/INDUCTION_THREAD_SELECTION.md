# Selecting five vertices through degree-two paths

Date: 2026-09-18. **Single bottleneck:** select a five-set in a critical
core while controlling the exact q+e obstruction. This cycle resolves the
subproblem in which deletion is confined to degree-two paths, cycle
components, and isolates. It gives a **PROVED** exact compression and a
restricted sufficient selection lemma. General A/B remain **CONJECTURAL**.
No balanced-extension theorem is used as a premise.

## 1. Exact compression — PROVED

Let C be a spanning edge-critical core. Vertices of degree one and bridges
are absent, as proved in INDUCTION_CRITICAL_CORE.md. Retain all vertices
of degree at least three as branch vertices. Its other nonisolated vertices
partition into:

* interiors of maximal paths between branch vertices (endpoints may coincide);
* components that are cycles.

Paths here have distinct internal vertices, all of degree two, and have
no edges other than their path edges at internal vertices. Distinct paths
have disjoint interiors and edges. A path returning to its initial branch
vertex is represented as a loop. Edges between branch vertices are paths
of length one. This decomposition follows by continuing uniquely through
each degree-two vertex; a walk either reaches a branch vertex or closes
an entire cycle component. All cycle components of a critical core are
odd: an even cycle component has d=0 and none of its edges is critical.
Keep the original isolates and all vertex counts; compression is an
identity for cut costs, not a new instance of JSP-000058.

For a path P of length l, replace it by a labeled constraint on endpoints
u,v whose cost on a branch coloring c is

    epsilon_P(c) = 1{ c(u) xor c(v) != l mod 2 }.

This applies to a loop with c(u) xor c(u)=0. The minimum number of
monochromatic path edges with fixed endpoint colors is exactly epsilon:
alternation attains zero if the parity matches, and otherwise alternation
with one repeated color attains one. The parity of the number of crossing
edges proves the corresponding lower bound. When the cost is one, its
unique monochromatic edge can be placed at ANY prescribed path edge.

Let K be this signed multigraph (parallel constraints and loops must be
retained), let

    D(K) = min_c sum_P epsilon_P(c),

and let o be the number of odd cycle components. The disjoint interiors
can be optimized independently once branch colors are fixed, so

    d(C) = D(K) + o.                                      (1)

The same identity holds without criticality for any graph admitting such
a path decomposition, with even cycle components contributing zero.
This proof does not appeal to a signed-graph theorem or to a conjectural
bound for the compressed object, which can have loops and triangles.

## 2. Deletion and criticality — PROVED

Let X contain only path interiors, vertices of cycle components, and
isolates. Let S be the set of paths whose interiors X meets, and let j be
the number of odd cycle components X meets. Deleting any nonempty subset
of a path's interior leaves path fragments, each attached to at most one
branch vertex. Every such fragment can be colored with zero monochromatic
edges for ANY branch coloring. This includes a path returning to one
branch vertex. A hit cycle component becomes a union of paths (or empty).
Therefore, regardless of how many or which interior vertices were removed,

    d(C-X) = D(K-S) + o-j,
    gamma_C(X) = D(K)-D(K-S)+j.                            (2)

In particular, removing a single original edge of P has the same effect
on d as removing ANY nonempty subset of its interior. Consequently,
criticality of C is equivalent to every constraint of K satisfying
D(K-P)=D(K)-1, with all cycle components odd. For the converse, this
identity applies to every original path edge, including paths of length
one; odd cycle edges reduce that component's d by one.

It follows that **every nonempty deletion confined to the interior of
one path in a critical core has increment exactly one**. The same holds
for any nonempty deletion inside one odd cycle component. Arbitrary
isolates may also be deleted at zero additional cost. Thus a path with
five internal vertices immediately supplies an A/B witness for all k>=2.
The earlier F_(a,h) family has eight internal vertices on its nine-edge
path, so any five of those vertices have gamma exactly one, strengthening
the earlier upper bound for five consecutive vertices. The result is
symbolic; it is not an enumeration of that family.

Criticality is needed for the word 'exactly': a path in an even cycle
has deletion increment zero. Losses from different critical paths need
not add; see Section 4.

## 3. A capacity criterion that selects X — PROVED

Assign each path a capacity equal to its number of internal vertices;
cycle components have capacity their full order. Length-one paths have
capacity zero and cannot be selected this way. Suppose we select a set S
of positive-capacity paths and a set Q of cycle components, and delete z
isolates. Exactly five vertices can be chosen, meeting precisely these
pieces and avoiding branch vertices, if and only if

    0 <= z <= min(5, number of isolates),
    |S|+|Q| <= 5-z <= sum of the selected capacities.       (3)

This is just distributing 5-z integer choices among the pieces, with at
least one and at most its capacity in each. The empty choice is permitted
when z=5. Write j for the number of odd cycles in Q and define

    U(S,Q) = max_c sum_{P in S} epsilon_P(c) + j.

Using an optimal coloring of K-S in (1) gives the rigorous bound

    gamma_C(X) <= U(S,Q) <= |S|+j.                        (4)

Thus (3) and U<=T construct a five-set satisfying the required threshold
T=2k-1 for A or T=2k-2 for nonbalanced B. This works for every distribution
of the five deletions among the selected interiors. It controls the exact
q+e obstruction: choose an optimal branch coloring of K-S, color all
surviving fragments properly, and restore each hit path at cost epsilon.
Place any required monochromatic path edge incident with X, using the
prescribed-edge property in Section 1. Its restriction colors every
surviving fragment properly. Thus surviving fragments can be recolored
without changing d(C-X), and q=0 remains valid. Bounding incident monochromatic edges of an optimal FULL
cut would have the wrong inequality and is not the argument here.

There is a useful bound better than counting paths. If selected paths
join the same two DISTINCT branch vertices, with a even lengths and b
odd lengths, their total cost is a for different endpoint colors and b
for equal endpoint colors. Their contribution to U is at most max(a,b),
not a+b. Partition S into endpoint-pair bundles and sum these bounds;
a returning loop contributes its length parity. In particular, selecting
one even and one odd path contributes identically one, independent of
all other constraints. Deleting interiors from both has gamma exactly
one, without any criticality assumption, if no other pieces are hit.
If their combined capacity is at least five, (3) yields a five-set witness.

**Restricted sufficient targets, CONJECTURAL.** Require A_crit/B_crit
only on cores for which no choice (3) has U<=T. The reduction is PROVED:
all excluded cores have the explicit witnesses above, and the equal-d
core transfer passes them to the original graph. As before, a nonbalanced
triangle-free graph cannot have spanning core B_k. This does not prove
selection in the remaining class, or justify removing branch vertices
from the original order.

For perspective, the previously known sequential degree estimate already
shows that five vertices of degree at most three give gamma<=5. Hence,
for k>=4, an unresolved core has at most four such vertices (including
isolates). This is a corollary of the OLD bound, not a new theorem claimed
here. The new exact identities and parity savings address the arrangement
of paths, including thresholds below five, and clarify why arbitrarily
long subdivisions cannot by themselves obstruct existential selection.
They give no reduction to minimum degree four: up to four low-degree
vertices may remain, and k=2,3 require separate treatment.

## 4. Inference checks and scope

**FALSIFIED:** increments add when deleting interiors from different
critical paths. Take two terminals joined by two length-two paths and
two length-three paths, all internally disjoint. This graph is simple,
triangle-free and has eight vertices. Its two branch-color costs are
both two, so d=2. Every edge is critical by the path parity witness (or
by deleting its constraint). Deleting interiors from one even and one
odd path leaves d=1, so gamma=1; each individual deletion also has gamma=1.
Deleting interiors from the two even paths instead leaves d=0 and gives
gamma=2. The exact reoptimization in (2) cannot be replaced by summing
individual losses. Padding with two isolates puts this example at order
10; it is not a counterexample to A/B.

**COMPUTATIONALLY VERIFIED:** bounded tests independently compare full
Gray-code cut enumeration of graphs and induced remainders with (1)-(2),
over every interior-deletion subset of fixed small path decompositions.
They include opposite parities, same parities, parallel paths, rooted
loops, odd/even cycle components, and a subdivision of K4. Criticality
and its equivalence are checked edge by edge in these fixtures. A separate
16-vertex critical fixture checks five separated internal deletions on
one length-ten path; another checks a five-set meeting opposite-parity
paths, whose loss is exactly one. These are inference tests, not an
exhaustive A/B certification. See tests/test_induction_thread_selection.py.

**Coverage audit:** all 25 saved t artifacts were read, with complete=true
and max_gap=0. They enumerate homogeneous remainder-part neighborhoods.
The arbitrary t>=26 symbolic proof and those files alone leave a coverage
gap. Later proofs reach arbitrary t>=3; mixed t=2 remains unresolved.
The empty t=5 maximizing witness does not certify equality classification.
No balanced-extension enumeration or broad random search was run.

**CONJECTURAL remaining bottleneck:** choose five vertices controlling
q+e on the residual nonautomatic critical cores after these explicit
path witnesses are excluded. Neither constant slack truncation nor
independent critical-edge witnesses solve that selection problem.
No potential complete solution appeared.

Validation: `.venv/bin/python -m pytest -q
 tests/test_induction_thread_selection.py tests/test_induction_critical_core.py`
— **8 passed**, 17.90 seconds. The first run passed all mathematical
assertions but exposed an incorrect expected subset count (1920 instead
of 1536); that bookkeeping assertion was corrected before the passing run.
`git diff --check` passed. Process inspection found no existing compute
job before either test launch. Test jobs ran sequentially and finished.
