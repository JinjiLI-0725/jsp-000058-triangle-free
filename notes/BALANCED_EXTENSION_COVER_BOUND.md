# Mixed balanced extensions: a vertex-cover bound

Date: 2026-09-18. Single bottleneck: the mixed-neighborhood balanced-remainder
case of induction A and B. General A, B, and JSP-000058 remain **CONJECTURAL**.

## Result — PROVED

For every integer t>=8, every triangle-free graph G obtained by adding five
vertices to an induced B_t satisfies

    d(G) <= (t+1)^2,

with equality if and only if G is B_(t+1). This improves the previous
first-principles threshold t>=26 without using any enumeration.

## Proof

Write H=B_t with parts A_j, X=V(G)\V(H), F=G[X], and m=e(F). Choose
f:X->Z/5Z so that N_H(x) is contained in A_(f(x)-1) union A_(f(x)+1).
Such a type exists because an independent set in H meets at most two
nonconsecutive parts. Empty and one-part neighborhoods also admit a type.
Put S_j={x: f(x)=j-1 or j+1}. Each x belongs to exactly two S_j.

Let tau_j be the minimum vertex-cover size of F[S_j], and put

    L = sum_j tau_j = 10 - sum_j alpha(F[S_j]),
    D = 10t - e(X,H).

For each v in A_j, its X-neighborhood is independent in F[S_j], so has
size at most alpha(F[S_j]). Summing over all vertices of H proves

    D >= tL.                                                   (1)

This applies to arbitrary different neighborhoods within each A_j; no
homogenization or completion of those neighborhoods has been used.

Use the five optimal part-respecting colorings of H, each with one sole
monochromatic cycle edge, and color x by the color of part f(x). Every
X-H edge is monochromatic in exactly one of these five colorings. An edge
xy of F is monochromatic in 1, 3, or 5 of them when its types are
consecutive, distinct nonconsecutive, or equal, respectively. Denote the
sum of these multiplicities by W. Their average extension cost is

    2t + (W-D)/5.                                             (2)

The two allowed-part sets for x,y intersect in 0, 1, or 2 parts in exactly
the same three cases. Consequently the following is an exact identity:

    W = m + 2 sum_j e(F[S_j]).                                 (3)

For every induced subgraph F[S], a minimum vertex cover covers all its
edges, and each vertex covers at most Delta(F) edges. Thus

    e(F[S]) <= Delta(F) tau(F[S]).                             (4)

We now prove W<=8L+4 whenever an incompatible edge (equal or distinct
nonconsecutive types) exists. Such an edge belongs to some F[S_j], hence
L>=1. A triangle-free five-vertex graph has m<=6: for each edge uv,
deg(u)+deg(v)<=5; summing gives sum deg(v)^2<=5m, while Cauchy--Schwarz
gives sum deg(v)^2>=4m^2/5. If m<=4, Delta(F)<=4 and (3),(4) give

    W <= m+8L <= 4+8L.

If m>=5, then Delta(F)<=3. Indeed a degree-four vertex is adjacent to all
other vertices, and triangle-freeness prohibits any edge among them,
forcing m=4. Thus in this case

    W <= m+6L <= 6+6L <= 4+8L,

where the final inequality uses L>=1. This proves the asserted bound.
Combining it with (1), for t>=8 we have

    W-D <= 4+(8-t)L <= 4.

By (2), some explicitly constructed cut has integer extension cost at
most floor(2t+4/5)=2t. Therefore

    d(G) <= t^2+2t = (t+1)^2-1                               (5)

whenever an incompatible edge exists.

Otherwise every F-edge joins consecutive types. Assign X vertices to their
types. Then G is a spanning subgraph of the complete C5 blow-up with part
sizes t+|f^(-1)(i)|. The blow-up formula and AM--GM from
structural_analysis.md give d(G)<=(t+1)^2, strictly if these sizes are
unbalanced. If balanced, every proper spanning subgraph has d<=(t+1)^2-1:
choose a missing edge and the optimal balanced cut with its part pair
monochromatic. Equality therefore forces G=B_(t+1). Conversely that graph
has deletion distance (t+1)^2. This completes the proof.

## Attempts to falsify the inferences

- (1) bounds each individual H-vertex's independent neighborhood. It
  does not assume that vertices in a part share that neighborhood.
- (4) is an upper bound on edge count, not an assertion that a minimum
  cover is independent or that its incident edges are counted once.
  Double counting edges within the cover only strengthens the upper bound.
- The use of L>=1 is restricted to the incompatible-edge branch. The
  L=0 branch is handled by the blow-up argument, not by (5).
- The cuts in (2) are actual cuts of G with q_H=0. An upper bound from
  these cuts is valid even if the true optimum has q_H>0. No equality
  between optimal-remainder extension cost and gamma is assumed.
- The threshold cannot be lowered by the inequality W-tL<=4 alone.
  Take F a four-leaf star, the center of type 0 and every leaf of type 2.
  Then W=12 and L=1, so at t=7 this expression is 5. The lower bound
  D=tL is attainable by giving every H vertex a maximum independent
  neighborhood in its S_j. This is a limitation of this estimate, not
  a counterexample to the extension theorem or the possibility of better cuts.

## Exact coverage and induction consequences

**COMPUTATIONALLY VERIFIED:** all saved homogeneous t=1,...,25 artifacts
are complete with max_gap=0. They were read and were not recomputed.
As proved in BALANCED_EXTENSION_AUDIT.md, their asserted homogeneous
spanning-supergraph coverage of mixed extensions is **FALSIFIED**.
The prior t>=26 symbolic theorem was independently applicable to mixed
extensions; the proof above now replaces its threshold by 8.

Thus arbitrary balanced extensions are **PROVED** for t>=8, including
equality classification. The full t=1 case and its equality classification
are **COMPUTATIONALLY VERIFIED** by the separate exhaustive n=10 corpus.
The full mixed extension bound and strict equality assertion for 2<=t<=7
remain **CONJECTURAL**. The homogeneous t artifacts do not fill that gap.

For k>=9, any five-set X leaving B_(k-1) satisfies A, and satisfies B
when G is nonbalanced. In the B_inherit reduction, A plus equality
uniqueness through k=8 would now imply uniqueness at all orders (the
previous cutoff was k=26). That finite base is not established here.
Arbitrary remainders still face the original selection requirement
min_c(q_H(c)+e_X(c))<=2k-1, or <=2k-2 for B.

Next action on this same bottleneck: prove the mixed-pattern inequality
M for 2<=t<=7, with strictness for nonbalanced extensions. No global
solution is suggested by this partial theorem.

## Validation

The focused balanced-pattern and structural test suites passed: **8 tests**
in 7.61 seconds. New tests check the cover inequality on all induced subsets
of all 388 triangle-free five-vertex graphs, and independently construct
the five cycle cuts to verify the type-overlap identity. They also check
the star limitation at t=7. This is a bounded regression check of proof
ingredients, not a repetition of the homogeneous extension enumeration.
The theorem above is proved symbolically and does not rely on these tests.
`git diff --check` passed.
