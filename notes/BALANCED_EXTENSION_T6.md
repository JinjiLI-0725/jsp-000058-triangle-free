# Balanced extensions at t=6: bounded edge repair

Date: 2026-09-18. Single bottleneck: the strict arbitrary mixed-neighborhood
extension of B_6, needed for the balanced transition in induction A/B.

**PROVED:** every triangle-free graph G obtained by adding five vertices to
an induced B_6 satisfies d(G)<=49, with equality exactly for B_7.
Together with [the t>=7 theorem](BALANCED_EXTENSION_T7.md), the strict
arbitrary balanced-extension theorem now holds for every t>=6.
General A, B, and JSP-000058 remain **CONJECTURAL**.

## Coverage verified first

All completed results/balanced_extension/t1.json through t25.json were read.
Each has complete=true and max_gap=0. This is **COMPUTATIONALLY VERIFIED**
coverage of homogeneous neighborhoods, not arbitrary mixed neighborhoods.
The t>=26 symbolic argument independently handles mixed neighborhoods;
therefore those two ranges alone do not prove an all-t arbitrary theorem.
The homogeneous spanning-supergraph claim is **FALSIFIED**, as recorded in
[BALANCED_EXTENSION_AUDIT.md](BALANCED_EXTENSION_AUDIT.md). The separately
saved exhaustive n=10 corpus covers arbitrary t=1 and equality there.
No completed enumeration was repeated. The t=5 missing witness is the
previously documented resume-metadata issue, not a new certificate of equality.

## Setup and a repair inequality

Use H=B_6, X=V(G)\V(H), F=G[X], m=e(F), a valid type map f, and
S_j={x:f(x)=j-1 or j+1}, with indices modulo five. Write

    alpha_j=alpha(F[S_j]), L=sum_j tau(F[S_j]),
    D=60-e(X,H), E=sum_j e(F[S_j]), W=m+2E.

The earlier cover proof gives D>=6L, and the five type-colored extensions
of optimal H cuts have average extra cost 12+(W-D)/5. Thus W-D<=4
already gives d(G)<=48. If L=0, all internal edges have consecutive types,
and containment in a C5 blow-up gives d(G)<=49 with equality only for B_7.
It suffices to treat L>=1 and W-D>=5. Let

    s=D-6L=sum_j sum_(v in A_j) (alpha_j-|N_X(v)|).

Each summand is a nonnegative integer, and s<=W-6L-5.
All arguments below concern actual individual patterns N_X(v), not their
completion or a common neighborhood for a whole part.

**PROVED repair inequality.** If deleting r boundary edges gives a graph
contained in a C5 blow-up K on the same vertices, then

    d(G)<=d(K)+r.

Indeed use an optimal cut of K; at most r restored edges are monochromatic.
No assumption about an optimal cut of G or of H is needed.

## Exhaustion of the possible internal graphs

If m<=4 and Delta(F)<=3, then E<=3L, so W-6L<=m<=4: no exception.
If Delta(F)=4, triangle-freeness makes F=K_(1,4).
For m=5 or 6, Delta(F)<=3. If Delta(F)<=2, E<=2L and
W-6L<=m-2L<=4. Otherwise choose a degree-three vertex z. Its three
neighbors are independent; the fifth vertex w cannot meet z, since that
would give degree four. All other edges run from w to those neighbors.
For m=5 it meets exactly two of them; for m=6 it meets all three.
Thus the only remaining shapes are C4 with a pendant vertex and K_(2,3).
This classification uses no enumeration.

## Four-leaf star

Let z be its center. Only the two S_j containing z can have edges;
each such induced star has cover number one. Thus L is 1 or 2.

If L=1, write r for the number of edges in that sole induced star.
Then W=4+2r and s<=2r-7. Since r<=4 and s>=0, r=4 and s<=1.
All leaves have a common type a, distinct and nonconsecutive to f(z):
otherwise an equal-type edge would occur in both parts allowed for z.
In the shared part an independent pattern containing z has size one,
losing three from the maximum four. Hence z has no neighbor there.
If f(z)=a+2, retype z to a-1; its remaining allowed part A_(a+3)
is still allowed. Reflect for f(z)=a-2. All edges are now compatible,
and only two adjacent added types are occupied. A pair of adjacent parts
receives no added vertex, so the containing blow-up has d=36.

If L=2, write r_1,r_2<=4 for the two induced star sizes. Then
s<=2(r_1+r_2)-13, forcing their sum to be 7 or 8.

- Sum 7: the sizes are 4 and 3, and s<=1. Three leaves share z's
  type a; the fourth has type a+2 or a-2. Patterns containing z lose
  at least two in either part, so z has no H neighbors at all. Retype
  z to a+1 or a-1 respectively. Only three consecutive added types
  occur; two adjacent untouched parts again give d<=36.
- Sum 8: all four leaves share z's type a, and s<=3. In either
  allowed part each pattern containing z loses three. Consequently
  z has at most one H neighbor in total. Delete that boundary edge
  if present and retype z to a+1. The containing blow-up has d=36;
  the repair inequality gives d(G)<=37.

All star exceptions therefore satisfy the required strict bound.

## The two shapes of maximum degree three

Here m is 5 or 6, and E<=3L. As E is integral, E<=3L-1 would imply
W-6L<=m-2<=4. Hence every exception has E=3L and s<=m-5.
Each individual inequality e(F[S_j])<=3 tau(F[S_j]) must be equality.

For m=5, the only nonempty induced subgraph with this equality is the
three-leaf star centered at z. To see this, tau>=2 would require at
least six edges; tau=1 requires three edges covered by a degree-three
vertex, and z is the unique such vertex. The vertex w is absent from
that S_j, since it meets two leaves. For m=6, F=K_(2,3); its nonempty
induced subgraphs are K_(r,q), r<=2, q<=3. The equality
rq=3 min(r,q) forces q=3 and r=1 or 2. Thus in both shapes every
S_j with edges contains all three leaves and one or both centers.
(In the m=5 shape only z can be such a center.)

The three leaves must have a common type a. Indeed take any S_j with
edges. Leaf types belong to {j-1,j+1}. If both types occur, a center
in S_j has the same type as some leaf. Their edge also occurs in the
other allowed part for that type. That other S set omits the leaves
of the opposite type, contradicting the just-proved equality shape.

Every incompatible center consequently has type a or a+/-2. Delete its
boundary edges in parts shared with the leaves' allowed parts. These
are precisely its boundary edges in the S_j that have edges. In any
such part, a pattern containing h>=1 centers has no leaves. For K_(2,3),
it has size h<=2 and loss 3-h, so h<=2(3-h). For m=5, a pattern
containing z has size one and loss two. Summing over actual vertices
shows that the total number R of deleted edges satisfies

    R<=2s<=2(m-5)<=2.

Now retype each incompatible center: type a goes to a+1 (its H
neighborhood is empty after deletion); type a+2 goes to a-1 (its
remaining neighbors lie in A_(a+3)); type a-2 goes to a+1 by reflection.
Centers whose type was already a+/-1 retain it. In the m=5 shape, w's
two edges were necessarily compatible already, since no edged S_j can
contain w. Thus w already has type a+/-1 and also retains it.

All internal edges now join consecutive types, and all remaining boundary
edges respect these types. The three leaves have type a, and the other
two vertices have types a-1 or a+1. Parts a+2 and a+3 are adjacent and
still have size six. The containing C5 blow-up has d=36, so

    d(G)<=36+R<=38<49.

This resolves every exception. The L=0 branch alone can give equality,
where the earlier blow-up argument forces G=B_7. Conversely d(B_7)=49.

## Inference audit and limits

- At t=6 the m=5 shape and K_(2,3) with larger L really must be allowed;
  the t=7 exception list was not reused as an exhaustive list.
- A unit of surplus need not forbid center neighborhoods: in K_(2,3),
  the pattern consisting of both centers has loss one and two edges.
  The repair inequality charges both edges. Similarly the star with all
  equal types allows one center edge when s=3.
- The repair is only a comparison, not a claim that the original graph
  embeds into a blow-up without deleting edges. All patterns, including
  nonmaximal and different patterns in a part, obey the surplus identity.
- The two adjacent size-six parts establish the explicit bound 36 for
  the containing blow-up. We do not spend an unproved global slack or
  claim that an arbitrary unbalanced blow-up tolerates two restored edges.
- Both the five initial cuts and the repaired blow-up cuts are actual
  cuts on the original vertex set, with restored edges explicitly paid for.
  This respects gamma=min_c(q_H(c)+e_X(c)); no lower bound on gamma is
  misused as an upper bound.

**PROVED induction consequence:** for k>=7, any X leaving B_(k-1)
satisfies A, and satisfies B if G is nonbalanced. By B_inherit, A plus
equality uniqueness through k=6 would imply uniqueness at all orders.
That finite base is not established. For general remainders, selecting
X,c with q_H(c)+e_X(c)<=2k-1 (or 2k-2) remains **CONJECTURAL**.
The unresolved arbitrary mixed balanced-extension range is t=2,...,5.
No potential complete solution appeared.

## Validation

A bounded regression checks normalized type maps for exactly the three
exceptional internal shapes. It computes W from actual five-cycle cuts,
then uses a loss-budget dynamic program over individual patterns to bound
the worst number of edges removed by a compatible retyping. This checks
all mixed patterns permitted by the surplus budget without enumerating
full extensions. The theorem above is symbolic, independent of that check.
Test results are recorded in INDUCTION_CHECKPOINT.md and current_state.json.
