# Full-cut slack and a failed critical-core shortcut

Date: 2026-09-18. Exactly one bottleneck is addressed: **can the family of
optimal full-graph cuts determine five-deletion increments on critical cores?**
The answer is no, even in the nonautomatic domain of both A_crit and B_crit.
This removes a concrete proposed simplification of the q+e obstruction.
It does not refute A, B, or JSP-000058.

## Exact full-cut formulation — PROVED

For a coloring c of G, let F(c) be its monochromatic edge set, let
s(c)=|F(c)|-d(G), and let r_X(c) count edges of F(c) with at least one
endpoint in X (an internal edge is counted once). Then

    gamma_G(X) = max_c [r_X(c)-s(c)].                       (1)

Indeed b_(G-X)(c|_(G-X))=b_G(c)-r_X(c), and every coloring of G-X has
an extension. Taking the minimum of the right-hand expression before
subtracting from d(G) proves (1). No compatibility of independently
optimal cuts is assumed. This is the full-graph counterpart of the
remainder identity gamma=min(q+e) in INDUCTION_ROUTE.md.

Put L_G(X)=max_{c optimal on G} r_X(c). Equation (1) implies
L_G(X)<=gamma_G(X). Equality would require an optimal coloring of G
whose restriction is optimal on G-X: in fact this condition is equivalent
to equality, since the finite maximum defining L is attained.
Edge-criticality does not ensure this compatibility.

For a threshold T, the exact condition is

    gamma_G(X)<=T iff r_X(c)<=T+s(c) for EVERY coloring c.  (2)

Thus controlling all optimal full-graph cuts gives a necessary condition,
not a sufficient one. There is a finite slack cutoff: if M_X is the
number of all G-edges incident with X, cuts with s(c)>=M_X-L_G(X)
cannot improve on L_G(X), since r_X(c)<=M_X. This cutoff is exact but
need not be small enough to yield an efficient algorithm or a proof of A.

## Candidate O — FALSIFIED by a symbolic family

**Candidate O:** for every triangle-free edge-critical graph G of order
5k in the nonautomatic domain, and every five-set X,
`gamma_G(X)=L_G(X)`.

Label the Petersen graph P by outer vertices 0,...,4 and inner vertices
5,...,9. Its edges, with indices modulo five, are

    i--(i+1),  i--(5+i),  (5+i)--(5+(i+2)).

It is triangle-free and cubic, with 15 edges. We first prove, without
relying on numerical MaxCut output, that its optimal cuts have exactly
the following five monochromatic sets:

    {(0,1),(3,8),(7,9)}
    {(1,2),(4,9),(5,8)}
    {(1,6),(3,4),(5,7)}
    {(0,5),(2,3),(6,9)}
    {(0,4),(2,7),(6,8)}.                                 (3)

Both the outer and inner vertices induce five-cycles, so an independent
set meets each in at most two vertices. Every independent four-set is
therefore, for exactly one i,

    S_i={i, i+2, 5+(i+3), 5+(i+4)}.

To check exhaustiveness, choose its two outer vertices i,i+2. Excluding
their spoke partners leaves three inner vertices; their only independent
pair is 5+(i+3),5+(i+4). Each of the six vertices outside S_i has exactly
two neighbors in S_i, directly from the displayed edge rule. Consequently
a five-set cannot induce at most one edge: removing an endpoint of that
edge (or any vertex if there are no edges) would leave an independent
four-set, but adding the removed vertex creates two edges.

For a cut whose smaller side S has size at most five, its crossing count
is 3|S|-2e(P[S]). If |S|<=4 this is at most 12, with equality precisely
for an independent four-set. If |S|=5, the preceding observation bounds
it by 11. Thus MaxCut(P)=12, d(P)=3, and the five S_i give exactly (3).
Their triples partition E(P), so every edge is monochromatic in an
optimal cut. P is edge-critical by the previously proved edge criterion.

Now take Y={0,1,3,8}. The remainder P-Y has edge set

    {(2,7),(4,9),(5,7),(6,9),(7,9)}.

It is a tree on its six vertices, hence d(P-Y)=0 and gamma_P(Y)=3.
Every triple in (3) has exactly two edges incident with Y. Therefore
L_P(Y)=2. The coloring with side {0,3,4,6,7} has monochromatic set

    {(0,4),(1,2),(3,4),(5,8)}.

All four edges touch Y, so s=1 and r_Y-s=4-1=3. Already the first
nonoptimal slack layer invalidates the proposed equality.

To obtain exactly five deleted vertices in the nonautomatic domain, let

    G_s=P disjoint-union B_s,  s>=3,
    X=Y union {v},  where v is any vertex of B_s.

Then |V(G_s)|=5(s+2), so k=s+2. Deletion distance is additive over
components: coloring each component independently both attains and
bounds the sum of its minima. The same argument shows that every optimal
cut is optimal on each component. Both components are edge-critical,
so G_s is too. It is triangle-free and is not B_k (it is disconnected).
Its d is s^2+3>=2(s+2) for all s>=3, placing it in the nonautomatic
domain of A_crit and also B_crit.

By the proved blow-up formula, d(B_s-v)=s(s-1). Moreover, the maximum
number of monochromatic edges incident with v over optimal cuts of B_s
is exactly s: every optimal cut has at most half of v's 2s incident
edges monochromatic, or flipping v would improve it; a part cut with
its monochromatic pair incident with v's part attains s. Hence

    gamma_(G_s)(X)=s+3,       L_(G_s)(X)=s+2.              (4)

This proves the counterexample for every s>=3, including all cuts that
might split blow-up parts. Combining the displayed slack-one coloring
of P with an optimal B_s cut attaining s realizes (1) at slack one.

These X actually satisfy B: s+3<=2(s+2)-2 for s>=3. The result refutes
only Candidate O, not the existence of a good five-set. Nor does it refute
a weaker proposal that some specially chosen X has gamma=L. It does not
settle what additional hypotheses might help on connected critical cores.

## Validation and exact remaining target

**COMPUTATIONALLY VERIFIED:** tests independently enumerate all 512 cuts
of P, check (3), criticality and the slack-one witness, and compare (1)
with the Gray-code solver on every deletion of at most five vertices.
They also enumerate cuts of B_3 to check the component values used for
the 25-vertex member; they do not enumerate all cuts on 25 vertices.
These finite checks validate the symbolic proof, not A/B in general.

**CONJECTURAL:** A_crit/B_crit still require selection of a five-set X
with max_c(r_X(c)-s(c))<=2k-1 / 2k-2. Optimal-cut edge coverage alone
cannot justify discarding nonoptimal cuts. A next argument must control
the positive-slack layers as well, or supply a separately proved condition
ensuring an optimal full cut remains optimal on the remainder.

All completed t=1,...,25 JSON files were read: complete=true and
max_gap=0 throughout. Their certification is homogeneous; the original
t>=26 symbolic theorem allows arbitrary patterns, so those two results
alone leave mixed t<=25 uncovered. Later notes prove arbitrary t>=3;
mixed t=2 remains open. No balanced-remainder theorem is used here, and
no balanced-extension enumeration was repeated. No broad random search
or long-running research computation was launched. No potential complete
solution appeared.
