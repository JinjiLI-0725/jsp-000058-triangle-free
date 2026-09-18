# Balanced extensions for t>=4 by occupied types

Date: 2026-09-18. Single bottleneck: strict arbitrary mixed-neighborhood
balanced extensions, the balanced-remainder transition in induction A/B.
The selected t=5 case admits a proof that also covers t=4.

**PROVED:** if t>=4 and a triangle-free graph G consists of an induced
B_t and five additional vertices, then d(G)<=(t+1)^2, with equality
if and only if G=B_(t+1). This proof is symbolic and independent of any
extension enumeration. General A, B, and JSP-000058 remain **CONJECTURAL**.

## Coverage checked before use

All 25 completed t1.json,...,t25.json artifacts were read. Each has
complete=true and max_gap=0, with 242,500 configurations and 1,245,367
maximal homogeneous neighborhood choices. These certify the homogeneous
family only (**COMPUTATIONALLY VERIFIED**). The t=5 empty witness remains
the documented resume-metadata issue, and a maximizing witness would not
classify equality in any case. No saved enumeration was repeated or altered.

The t>=26 symbolic argument allows mixed neighborhoods: incompatible
endpoints have disjoint neighborhoods in a shared part, giving D>=t;
then W<=30 gives W-D<=4. Thus it combines with the finite certificates
only to cover different families in the two ranges, not all arbitrary
extensions. The claimed homogeneous spanning-supergraph reduction remains
**FALSIFIED**. The later t>=6 symbolic proof was valid; the proof here
supersedes its threshold. The separate exhaustive n=10 corpus covers t=1,
including equality, **COMPUTATIONALLY VERIFIED**.

## Setup

Let H=B_t have parts A_j, let X be the five added vertices, and put
F=G[X], m=e(F). Indices are modulo five. Choose a type f(x) for each x
such that N_H(x) is contained in A_(f(x)-1) union A_(f(x)+1).
This is possible because that neighborhood is independent in H: it meets
at most two nonconsecutive parts. Empty and single-part supports also fit.
Let n_j=|f^(-1)(j)|, so sum n_j=5. No homogeneity within H parts is assumed.

For each cycle edge e, let c^e be the part coloring whose only
monochromatic cycle edge is e. Color each x by c^e_(f(x)). These are
actual cuts of G. Their restriction to H is optimal, with cost t^2.

We use an auxiliary complete blow-up K with part sizes t+n_j. All H and
X-H edges of G occur in K; F edges need not. In the type cut c^e, the
monochromatic H and boundary edges of G are therefore at most the full
monochromatic cost of K, namely (t+n_i)(t+n_(i+1)) if e=i(i+1).
Consequently the following inequality is always valid:

    b_G(c^e extended by f)
      <= (t+n_i)(t+n_(i+1)) + b_F(c^e composed with f).       (1)

This can overcount compatible F edges already in K, which only weakens
an upper bound. It does NOT assert G is a spanning subgraph of K.

## A five-vertex cut bound

**PROVED:** every triangle-free F on five vertices has at most six edges,
and every nonconstant coloring a of its five vertices has b_F(a)<=4.

For the edge bound, triangle-freeness gives deg(u)+deg(v)<=5 for each
edge uv. Summing and applying Cauchy--Schwarz gives
4m^2/5<=sum deg(v)^2<=5m, hence m<=6.
For the coloring assertion, its two nonempty sides have sizes 1 and 4,
or 2 and 3. The same degree-sum argument on four vertices bounds the
number of edges within the size-four side by four. A triangle-free
three-vertex graph has at most two edges, and a two-vertex graph has at
most one. Thus b_F<=4 in the first case and b_F<=3 in the second.
This proves the assertion without graph enumeration.

## Noninjective type maps

Suppose fewer than five types are occupied.

If two adjacent types are empty, choose that edge for e. Equation (1)
and m<=6 give

    d(G)<=t^2+6<=t^2+2t  for t>=4.                         (2)

If no adjacent types are empty, there are either one or two empty types.
(An independent set in a pentagon has size at most two.) There is an edge
e from an empty type to a type occupied exactly once:

- With one empty type, the four positive counts sum to five, so three
  counts are one; both neighbors of the empty type cannot have count two.
- With two nonadjacent empty types, the three positive counts sum to five,
  so at least one is one. Each occupied type neighbors an empty type.

For this choice e the product in (1) is t(t+1). Moreover the coloring
on X is nonconstant. With four occupied types, they cannot all lie on
one side of a pentagon coloring, whose side sizes are two and three.
With three occupied types and nonadjacent empty types, two occupied
types are adjacent. Their edge differs from e, because e touches an
empty type. That occupied edge crosses c^e, so both X colors occur.
The five-vertex cut bound now yields

    d(G)<=t(t+1)+4<=t^2+2t  for t>=4.                     (3)

Thus EVERY noninjective valid type map proves the strict result. These
bounds allow all mixed and nonmaximal boundary neighborhoods; no deficit
budget, compatible retyping, or boundary-edge repair is required.

## Injective type maps

The remaining case has n_j=1 for each j. Set

    S_j={x:f(x)=j-1 or j+1},
    L=sum_j tau(F[S_j]), D=10t-e(X,H).

Each S_j has two vertices. Hence tau(F[S_j])=e(F[S_j]), and L is exactly
the number of F edges with distinct nonconsecutive types. Each such edge
lies in just one S_j. Independent neighborhoods at the individual H
vertices give D>=tL, as in the earlier cover proof.

Let W count how many of the five type cuts make F edges monochromatic,
summed over those edges. Consecutive endpoint types contribute one and
nonconsecutive types contribute three, so W=m+2L. Each boundary edge is
monochromatic in exactly one of the five cuts. Their average total cost is

    t^2 + (10t-D+W)/5 = t^2+2t+(W-D)/5.

If L>=1 and t>=4, then

    W-D <= m-(t-2)L <= 6-2 = 4.

The cut costs are integers, so one is at most t^2+2t. This is strict
relative to (t+1)^2.

If L=0, every F edge joins consecutive types. In this branch G actually
IS a spanning subgraph of B_(t+1), with parts A_j union f^(-1)(j).
Thus d(G)<=(t+1)^2. If it is proper, select a missing edge uv and the
balanced cut whose sole monochromatic part pair contains uv. That cut
has cost at most (t+1)^2-1 in G. Equality therefore forces G=B_(t+1).
Conversely the balanced blow-up has d=(t+1)^2. This completes the proof.

## Inference audit and attempted falsification

- The auxiliary K need not contain incompatible internal edges; (1)
  explicitly pays for ALL monochromatic F edges. Its role is only to
  bound H and boundary costs. This avoids the earlier false coverage step.
- The nonconstant-coloring hypothesis is essential: K_(2,3) colored
  constantly has six monochromatic edges. The proof verifies that
  hypothesis exactly in the t(t+1) branch, not in the t^2 branch.
- The empty-singleton edge is established by integer occupancy counts,
  and the proof separately checks nonconstancy with one or two empty types.
- D>=tL is obtained vertex by vertex; different independent patterns in
  the same H part cause no loss of validity. No maximum-cardinality or
  maximal-pattern assumption is made.
- The average is an upper-bound construction using five actual cuts;
  its restriction has q_H=0. No inequality from restriction of an optimal
  G cut is reversed. Allowing q_H>0 can only improve the true optimum.
- Equality follows from excluding every incompatible/noninjective branch
  strictly and then treating every proper balanced subgraph, not from
  a finite maximizing witness.
- At t=3, (3) gives 16 rather than the needed strict bound 15. That is
  a limitation of this estimate, not a counterexample to the theorem.
  The injective estimate as written also needs refinement at t=3.

A preliminary targeted loss-budget check at t=5 tested compatible-retyping
bounds for the 14 internal graph shapes and their normalized type maps.
It found six K_(2,3) maps where that sufficient bound was 37, above 35;
this did not falsify the graph bound. Noticing that internal incompatible
edges can instead be explicitly charged led to (1). The exploratory check
finished before testing; no random search or full extension enumeration
was run. The proof above does not depend on the exploratory calculation.

## Consequence and clean remaining bottleneck

**PROVED:** for k>=5, every five-set X with G-X=B_(k-1) satisfies A;
if G is nonbalanced, it satisfies B. In fact our strict branches exhibit
an optimal remainder cut with extension cost at most 2k-2.
By B_inherit, A plus equality uniqueness through k=4 would imply equality
uniqueness at all orders. Neither general A nor that finite base is proved.

**CONJECTURAL:** the arbitrary mixed extension theorem with strictness
for t=2,3; general A and B; JSP-000058. The general obstruction remains
selecting X,c with q_H(c)+e_X(c)<=2k-1 (or <=2k-2 for B).
No new candidate lemma was falsified, and no potential complete solution
appeared. Next work on this same bottleneck should address t=3, where
(3) misses strictness by one, without repeating homogeneous enumeration.

## Validation

The new regression separately checks the occupied-type cut construction
on all 625 normalized maps and the nonconstant-cut bound on all 388 labeled
triangle-free five-vertex graphs. It also checks the injective overlap
identity independently on their subsets and all 24 normalized bijections.
These are **COMPUTATIONALLY VERIFIED** proof-ingredient checks, not
extension enumeration. The theorem itself is **PROVED** symbolically.
Test outcomes are recorded in INDUCTION_CHECKPOINT.md and current_state.json.
