# Four-boundary selection with a five-vertex outside budget

Date: 2026-09-19. Exactly one bottleneck addressed: the unresolved
s=k-1 private-transversal case of the four-boundary B certificate.
General A/B and JSP-000058 remain **CONJECTURAL**.

## Boundary recoloring lemma — PROVED

Let P=B_t have four distinct retained roots S. Let O be at most five
outside vertices, and suppose all P--O edges meet S. Assume the resulting
graph is triangle-free. Assign all edges of P to P and all other edges
to R; thus R has no edges between roots. Write R(a) for the minimum
monochromatic R-edge count with prescribed root colors a.

The classification in
[INDUCTION_FOUR_BOUNDARY_SELECTION.md](INDUCTION_FOUR_BOUNDARY_SELECTION.md)
gives F_t(a)=t^2+lambda_a*t+delta_a. Up to root permutation, cycle symmetry,
and color reversal, exactly three rows have lambda=2 (and delta=0).
Every one-root flip in these rows has lambda=0. Their constant penalties,
listed in root order, are:

| Root parts | Root colors | Minimum admissible t | Penalties after flips 1,2,3,4 | c |
|---|---|---:|---|---:|
| 0022 | 0101 | 2 | 0,0,0,0 | 2 |
| 0023 | 0100 | 2 | 2,0,0,0 | 2 |
| 0123 | 0011 | 1 | 0,2,2,0 | 1 |

Here is a direct argument controlling R; it assumes neither optimal
colorings of the full graph nor independence of the outside vertices.
Fix an R-optimal coloring y extending a. If only root i is flipped while
y on O is kept fixed, the R-cost changes by the integer

    D_i = number of opposite-colored outside neighbors of root i
          - number of same-colored outside neighbors of root i.

For every outside vertex v, its contribution to sum_i D_i is at most c
from the table. Indeed its neighbors in S form an independent set:

* For 0022/0101, there are only two roots of either color, so at most two
  positive contributions, even without using independence.
* For 0023/0100, the three zero roots include the adjacent roots in parts
  2 and 3. An independent subset contains at most two zeros or one one.
* For 0123/0011, the roots induce a four-vertex path; each same-color pair
  is adjacent. An independent subset contains at most one root of either
  color, so there is at most one positive contribution.

Negative contributions only decrease these bounds. Therefore, with
N=|O|<=5 and delta_i the flip penalties, at least one i satisfies

    D_i+delta_i <= floor((c*N + sum_j delta_j)/4).

For the three rows this upper bound is at most 2, 3, 2, respectively.
These bounds are at most 2t throughout their admissible ranges (t>=2,
t>=2, t>=1). If a^(i) denotes that flipped root coloring, keeping y on O
is a feasible coloring of R, and hence

    delta_i + R(a^(i)) <= delta_i+R(a)+D_i <= 2t+R(a).

Thus every size-dependent row is dominated, or tied, by a slope-zero row.
Consequently the exact identity is

    d(P union R) = t^2 + K,
    K = min_{a:lambda_a=0} [delta_a+R(a)],

for every admissible t with the same root placement and outside graph.
K is independent of t. Ties are allowed: the statement is existence of a
slope-zero optimum, not exclusion of all slope-two optima. For fewer than
four roots, the earlier three-boundary theorem already gives the same
size-independence, without any bound on N.

## Private transversal and B — PROVED

Let G have order 5k and an induced proper piece P=B_s. Suppose every edge
from P to its complement meets a retained set S of at most four roots,
and every part of P has a vertex outside S. Choose any private transversal
X, one nonroot vertex from each part. Assume s>=2; the empty-boundary
isolated B_1 case is handled below.

If s=k-1, there are exactly five vertices outside P. With
m=max_i |S intersection A_i|, feasibility gives s-1>=m. Apply the lemma
at t=s and t=s-1, with the identical R. It yields

    d(G)=s^2+K,  d(G-X)=(s-1)^2+K,
    gamma_G(X)=2s-1=2k-3.

This is also an explicit certificate for the exact q+e obstruction.
Choose a slope-zero boundary assignment attaining K and the corresponding
part-rounding template from the four-boundary table, at size s-1, together
with an optimal R-coloring. This is an optimal coloring of G-X, so q=0.
Give each deleted private vertex the template color of its part. The same
template at size s has cost s^2+delta, so the added cost is exactly 2s-1.
It is an optimal extension, since the exact difference is already 2s-1.
Thus e_X=2s-1 and q+e=2k-3, with no uncharged recoloring of the remainder.

If s<=k-2, the previous unrestricted four-boundary bound already supplies
an optimal remainder coloring with e_X<=2s+1<=2k-3 and q=0. Therefore
**every proper balanced piece with at most four attachment roots and a
private transversal supplies B, with the stronger bound gamma<=2k-3**.
If s=1, existence of a private vertex in each singleton part forces S
empty; the piece is an isolated C5. Delete it, giving gamma=1<=2k-3.
The bound also supplies A. For P=G=B_k, the usual transversal supplies A
with gamma=2k-1; B excludes that graph.

Equal-d spanning-core transfer preserves the increment bound and the
five-set, as proved in INDUCTION_CRITICAL_CORE.md. A q=0 coloring in the
original supergraph is not asserted by that transfer. No reduction of
arbitrary residual cores to balanced pieces has been proved.

## Inference audit and scope

**PROVED:** the outside-budget recoloring lemma, size-independent optimized
penalty for N<=5, exact private increment 2s-1 at s=k-1, and the resulting
four-boundary B selection theorem. The full constrained profile can still
depend on size; only its minimum after gluing has become size-independent.

**COMPUTATIONALLY VERIFIED:** see the checkpoint for test results. The new
tests check the one-vertex budgets for every independent root neighborhood
and both outside colors, all reachable aggregate flip costs for N<=5,
and fixed glued examples by independent feasible-part-count minimization.
The earlier all-size polynomial and orbit certificates are rerun as
regressions. These checks audit the proof, not arbitrary-order A/B.

**FALSIFIED (previous result, still valid):** universal exact increment
2s-1 with unrestricted outside order. The earlier path attachment has
4(2s+1)>5 outside vertices, so it does not contradict this theorem.
No new counterexample to A/B is claimed.

**CONJECTURAL:** five-set selection on residual nonautomatic critical cores
without any established selection certificate. This cycle removes the
s=k-1 qualification from the four-boundary certificate; it does not settle
arbitrary blocks, five-root attachments, or mixed balanced extensions t=2.
No potential complete solution appeared.

## Balanced-extension coverage

All completed t=1,...,25 JSON files were read in full; all report
complete=true and max_gap=0. They enumerate homogeneous neighborhoods.
The arbitrary symbolic t>=26 theorem therefore combines with them only
for that finite homogeneous family and all extensions in the symbolic
range; it does not prove the all-t arbitrary statement. The audited
spanning-supergraph reduction is false. Later symbolic proofs reach t>=3,
leaving mixed t=2 open. The empty t=5 witness does not classify equality.
No balanced-remainder extension theorem is used as a premise here.
No completed enumeration was repeated and no random search was run.
