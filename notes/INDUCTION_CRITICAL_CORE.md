# A/B reduction to edge-critical spanning cores

Date: 2026-09-18. The single bottleneck in this cycle is **transferring a
five-vertex deletion witness from a simpler graph to the original graph**.
This addresses the general q+e selection problem, rather than the remaining
mixed t=2 balanced-extension subcase. The outcome is a **PROVED reduction**
to a restricted sufficient lemma; the restricted lemma itself is
**CONJECTURAL**. Neither A, B, nor JSP-000058 is proved here.

## 1. Exact transfer, including the direction of inequality — PROVED

Call a graph C edge-critical for d if every edge e satisfies
`d(C-e)=d(C)-1`. The edgeless graph qualifies vacuously. Isolated vertices
are retained: all cores below have exactly the original 5k vertices.

Every graph G has a spanning edge-critical subgraph C with d(C)=d(G).
Choose an inclusion-minimal spanning subgraph with the same d. Removing
one edge can reduce d by at most one, so every remaining edge reduces it
by exactly one. Equivalently, repeatedly remove any edge preserving d
until none remains. This is an existence argument, not an efficient
algorithm for finding such edges without an exact cut oracle.

For EVERY vertex set X, monotonicity under edge inclusion gives

    delta_X := d(G-X)-d(C-X) >= 0,
    gamma_G(X) = gamma_C(X)-delta_X <= gamma_C(X).          (1)

Thus the very same X transfers any upper bound on the increment. In
particular an A or B counterexample G produces a core C that is still a
counterexample for every X, with the balanced exception handled below.
The equality d(C)=d(G) is essential; arbitrary edge deletion has no such
transfer rule.

This proof respects the exact obstruction in INDUCTION_ROUTE.md. If
H_C=C-X and H_G=G-X, then

    min_c(q_H_G(c)+e_X^G(c))
      = min_c(q_H_C(c)+e_X^C(c))-delta_X.

These are separately optimized minima. We do NOT transfer the same
coloring, compare q or e separately, or assert that an optimal remainder
cut extends optimally. Once X is chosen, an optimizing coloring for G
exists and supplies the required q+e bound by the identity.

## 2. Restricted sufficient lemmas — reduction PROVED, targets CONJECTURAL

**A_crit.** For every triangle-free edge-critical C on 5k vertices, k>=2,
with d(C)>=2k, there is a five-set X with gamma_C(X)<=2k-1.

**B_crit.** For every triangle-free edge-critical C on 5k vertices, k>=2,
with C not isomorphic to B_k and d(C)>=2k-1, there is a five-set X with
gamma_C(X)<=2k-2.

A_crit implies general A: choose C as above; if d(C)<=2k-1 every X
works by d(C-X)>=0, and otherwise use A_crit and (1). Conversely A
implies A_crit by restriction. Thus A and A_crit are logically equivalent,
although A_crit quantifies over a smaller class. It is a reduction of the
domain, not a claim that the unresolved theorem has been established.

For B, a nonbalanced triangle-free G cannot have a spanning core C=B_k.
Indeed B_k is maximal triangle-free on its vertex set: vertices in the
same part share a neighbor in either adjacent nonempty part, and vertices
in distinct nonconsecutive parts share a neighbor in the intervening part.
Every missing edge therefore creates a triangle. Hence C=B_k would force
G=C. Applying B_crit to the core of a nonbalanced G, or the automatic
case d(C)<=2k-2, proves B using (1). The converse again is restriction.

Consequently A_crit suffices for JSP-000058, and B_crit suffices also for
equality uniqueness, by the existing induction proofs. This does not need
the mixed t=2 extension theorem or a new finite equality base. It also
does not prove B from A. The existing minimum-degree boundary theorem
allows unresolved cores to be restricted further to minimum degree
at most 2k-1; isolated vertices must still count toward their order.

Do not combine this reduction with the earlier maximal-graph reduction
by assuming a graph is simultaneously maximal and edge-critical. Taking
a core can destroy maximality; completing a core can destroy criticality
and the equality of d needed in (1). Nor do the dense terminal bounds
alone prove A/B for a core: they still give no lower bound on d(C-X).

## 3. Concrete structure supplied by criticality — PROVED

For any graph, an edge e lowers d when deleted if and only if some
optimal coloring leaves e monochromatic. Necessity follows by evaluating
an optimal coloring of C-e on C; sufficiency by using the monochromatic
optimal coloring after deletion. Therefore edge-criticality says that
the UNION of the monochromatic edge sets of all optimal cuts covers E(C).
It does not say one optimal cut leaves every edge monochromatic.

Every edge of an edge-critical graph lies on an odd cycle. To see this,
take an optimal coloring with monochromatic set D containing e. C-D is
bipartite. Restoring e must destroy bipartiteness, or D without e would
be a smaller bipartizing set. The odd cycle created uses e. In particular
cores have no bridges and no vertices of degree one. This does not imply
minimum degree two, because retained isolated vertices are permitted.

Within the complete C5 blow-up family with all five sizes positive,
edge-criticality holds **if and only if all five sizes are equal**.
Here is a proof that also checks cuts splitting parts. Put
`p_i=a_i*a_(i+1)` and `d=min_i p_i`. For any optimal vertex coloring,
independently color each whole part by a randomly chosen vertex of that
part. The expected monochromatic cost is the original cost d: for each
part pair this follows by multiplying its two color proportions. Every
rounded cut has cost at least d, so every rounded cut with positive
probability is optimal. If an original edge between parts i,i+1 is
monochromatic, that pair is monochromatic with positive probability in
the rounding. Such a rounded cut costs at least p_i. Hence p_i=d.
Conversely, if p_i=d, the part cut with that sole monochromatic pair is
optimal and leaves every edge in the pair monochromatic.

Thus an edge in pair i is critical exactly when p_i=d. All edges are
critical exactly when all p_i agree. Positivity and the odd cycle of
equations a_i*a_(i+1)=d force all a_i equal. If any part is empty, the
blow-up is bipartite, so it is edge-critical only when edgeless.

This excludes unbalanced complete C5 blow-ups from the nontrivial core
domain. It does NOT imply that their cores are complete blow-ups, or that
all triangle-free edge-critical graphs are balanced blow-ups. For example
C7 plus three isolates is an edge-critical triangle-free graph of order
10; its d=1 puts it in the automatic case of both restricted lemmas.

## 4. Inference falsification and scope

**FALSIFIED:** omitting d(C)=d(G) from the claimed transfer inequality.
Let G be C5 plus five isolates and let C be obtained by deleting one
cycle edge. Choose X to contain one cycle vertex and four isolates.
Then gamma_G(X)=1 and gamma_C(X)=0, so gamma_G<=gamma_C fails.
Both graphs are triangle-free and have order 10.

The reduction also cannot be assumed to preserve a balanced induced
remainder, connectedness, or maximality. For example the maximal
triangle-free blow-up with sizes (6,1,1,1,1) has d=1; retaining one
transversal C5 and deleting all other edges gives a critical spanning
core with five isolated vertices and the same d. This is a legitimate
core, and demonstrates why the original order must be retained.

**Coverage prerequisite checked:** all t1.json,...,t25.json were read and
have complete=true, max_gap=0, 242500 configurations and 1245367 maximal
homogeneous choices. Their homogeneous scope and the arbitrary t>=26
symbolic proof do not alone prove the all-t arbitrary extension claim.
The subsequent proofs reach arbitrary t>=3; mixed t=2 remains open.
The t=5 empty witness supplies no equality classification. This cycle's
core reduction uses none of those extension claims as a premise.

**COMPUTATIONALLY VERIFIED:** tests check (1) on every five-set of fixed
10-vertex examples after exact core extraction, the critical-edge/optimal-
cut equivalence on all 388 labeled triangle-free five-vertex graphs, and
the blow-up edge criterion on all 126 positive ordered size vectors of
sum 10. These are bounded inference checks, not proof of A_crit/B_crit
and not a rerun of the balanced-extension enumeration.

**CONJECTURAL / exact remaining bottleneck:** on a nonautomatic
triangle-free edge-critical core, use its family of optimal cuts to find
five vertices X and a remainder coloring c with q(c)+e_X(c)<=2k-1
(or <=2k-2 in the nonbalanced B case). Edgewise coverage by different
optimal cuts does not yet coordinate five deletions or control remainder
reoptimization. The proven reduction isolates this smaller domain but
does not resolve that selection problem. No potential complete proof
of JSP-000058 appeared.
