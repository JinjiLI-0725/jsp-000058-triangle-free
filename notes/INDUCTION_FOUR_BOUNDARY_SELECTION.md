> **Latest progress (2026-09-19, four-boundary outside budget):**
> [INDUCTION_FOUR_BOUNDARY_BUDGET.md](INDUCTION_FOUR_BOUNDARY_BUDGET.md)
> **PROVES** that at most five outside vertices always permit a slope-zero
> optimal boundary row. Thus the previously unresolved s=k-1 private
> transversal has gamma=2s-1 and q=0. Combined with the earlier bound,
> every proper balanced piece with at most four attachment roots and a
> private transversal supplies B, with gamma<=2k-3. General A/B remain
> **CONJECTURAL**; no reduction of arbitrary cores to such pieces is known.

# Four-boundary selection and the first size-dependent penalty

Date: 2026-09-19. Exactly one bottleneck addressed: private-transversal
q+e selection for balanced pieces with four retained attachment vertices.
This is a subcase of A_crit/B_crit, not a reduction of arbitrary cores to
balanced pieces. General A/B and JSP-000058 remain **CONJECTURAL**.

## Constrained profile classification — PROVED

Prescribe colors a on four distinct roots S in B_s. Let F_s(a) be the
minimum monochromatic edge count extending these colors. Put r_i=|S cap A_i|
and let z_i count zero-colored roots in A_i. Set m=max r_i. For all integers
s>=m, the exact profile is one of

    s^2, s^2+2, s^2+4, s^2+2s.

Which polynomial applies depends only on root parts and colors, not s.
In the table below, F_s=s^2+lambda*s+delta. Bits b indicate zero-colored
unprescribed vertices (1 means zero). Root permutations, dihedral symmetries
of C5, and global color reversal reduce the possibilities to these 47 rows.
Repeated part digits represent distinct roots, not repeated vertices.

| Parts | Colors | m | lambda | delta | b |
|---|---|---:|---:|---:|---|
| 0000 | 0000 | 4 | 0 | 0 | 00101 |
| 0000 | 0001 | 4 | 0 | 0 | 00101 |
| 0001 | 0000 | 3 | 0 | 0 | 01010 |
| 0001 | 0001 | 3 | 0 | 0 | 00101 |
| 0002 | 0000 | 3 | 0 | 0 | 00101 |
| 0002 | 0001 | 3 | 0 | 0 | 01010 |
| 0000 | 0011 | 4 | 0 | 0 | 00101 |
| 0001 | 0010 | 3 | 0 | 0 | 01010 |
| 0001 | 0011 | 3 | 0 | 0 | 00101 |
| 0002 | 0010 | 3 | 0 | 0 | 00101 |
| 0002 | 0011 | 3 | 0 | 0 | 01010 |
| 0011 | 0000 | 2 | 0 | 0 | 01010 |
| 0011 | 0001 | 2 | 0 | 0 | 10010 |
| 0012 | 0000 | 2 | 0 | 2 | 10010 |
| 0012 | 0001 | 2 | 0 | 0 | 01010 |
| 0013 | 0000 | 2 | 0 | 0 | 01010 |
| 0013 | 0001 | 2 | 0 | 4 | 00101 |
| 0014 | 0000 | 2 | 0 | 4 | 00101 |
| 0014 | 0001 | 2 | 0 | 0 | 01010 |
| 0011 | 0011 | 2 | 0 | 0 | 00101 |
| 0012 | 0010 | 2 | 0 | 0 | 00101 |
| 0012 | 0011 | 2 | 0 | 0 | 10010 |
| 0013 | 0010 | 2 | 0 | 0 | 10010 |
| 0013 | 0011 | 2 | 0 | 0 | 00101 |
| 0014 | 0011 | 2 | 0 | 0 | 10010 |
| 0022 | 0000 | 2 | 0 | 0 | 00101 |
| 0022 | 0001 | 2 | 0 | 0 | 10010 |
| 0023 | 0000 | 2 | 0 | 0 | 10010 |
| 0023 | 0001 | 2 | 0 | 0 | 00101 |
| 0022 | 0011 | 2 | 0 | 0 | 01010 |
| 0023 | 0011 | 2 | 0 | 2 | 10110 |
| 0011 | 0101 | 2 | 0 | 2 | 00101 |
| 0012 | 0100 | 2 | 0 | 2 | 00101 |
| 0012 | 0101 | 2 | 0 | 0 | 01010 |
| 0013 | 0100 | 2 | 0 | 0 | 01010 |
| 0013 | 0101 | 2 | 0 | 2 | 00101 |
| 0014 | 0100 | 2 | 0 | 2 | 00101 |
| 0014 | 0101 | 2 | 0 | 0 | 01010 |
| 0022 | 0101 | 2 | 2 | 0 | 00101 |
| 0023 | 0100 | 2 | 2 | 0 | 00101 |
| 0023 | 0101 | 2 | 0 | 0 | 00101 |
| 0123 | 0000 | 1 | 0 | 2 | 10010 |
| 0123 | 0001 | 1 | 0 | 2 | 00101 |
| 0123 | 0010 | 1 | 0 | 0 | 01010 |
| 0123 | 0011 | 1 | 2 | 0 | 00101 |
| 0124 | 0011 | 1 | 0 | 0 | 01010 |
| 0123 | 0101 | 1 | 0 | 0 | 00101 |

Here is an algebraic certificate of both bounds for the entire table.
Constrained part rounding, as in the three-boundary proof, gives
F_s=min_b C_b(s), over all 32 bit strings. Write v_i=z_i-b_i r_i. Then

    C_b(s)=A_b s^2+L_b s+H_b,
    A_b=sum_i [b_i b_(i+1)+(1-b_i)(1-b_(i+1))],
    L_b=sum_i [(2b_i-1)v_(i+1)+(2b_(i+1)-1)v_i],
    H_b=2 sum_i v_i v_(i+1).

For each displayed b, substitution gives (A_b,L_b,H_b)=(1,lambda,delta).
For every row and every bit string, substitution also gives the three
nonnegative integers

    A_b-1,
    2m(A_b-1)+L_b-lambda,
    m^2(A_b-1)+m(L_b-lambda)+H_b-delta.

These are precisely the coefficients of C_b(m+u)-[(m+u)^2+
 lambda*(m+u)+delta]. Thus all candidate costs are at least the asserted
polynomial for u>=0, and the displayed b attains it. This is a finite
explicit polynomial certificate for all s, not an extrapolation from sizes.
The accompanying test checks all 47*32 coefficient triples using integer
arithmetic and independently checks table coverage. With fewer than four
roots the earlier three-boundary theorem applies.

## A weaker sufficient selection theorem — PROVED

Let G have order 5k and an induced P=B_s. All edges from P to outside P
meet S subset V(P), |S|<=4. Suppose each part has a private vertex outside
S. Delete a private transversal X; in particular s>=m+1 and s>=2.
Assign edges within P to P, and all remaining edges to R, retaining S
as the shared boundary. Let R(a) be its constrained cost. The same row
and same polynomial apply at s and s-1. Exactly,

    d(G)   = s^2     + min_a [lambda_a*s+delta_a+R(a)],
    d(G-X) = (s-1)^2 + min_a [lambda_a*(s-1)+delta_a+R(a)].

Every lambda_a is 0 or 2, so the difference between the two minima lies
between 0 and 2. Consequently

    2s-1 <= gamma_G(X) <= 2s+1.

There is also a q=0 certificate for the upper bound: choose a minimizing
boundary assignment at size s-1, an optimal coloring of R, and the table's
bit string. Extend by giving the five deleted vertices their parts' bit
colors. The added cost is 2s-1+lambda_a<=2s+1. Unlike the three-root case,
this extension need not be globally optimal on G; only the upper bound
is asserted. No bound on R is assumed.

If s<=k-2, then gamma<=2k-3, proving both A and B for this five-set.
If s=k-1, the bound gives 2k-1, proving A but not generally B by this
argument. If the minimizing remainder boundary row has lambda=0, the
stronger upper bound 2s-1 proves B for every proper piece.
Equal-d spanning-core transfer preserves these upper bounds for G.
For G=P=B_k the known transversal gives A exactly. Criticality is not
needed in the piece theorem. No claim of a reduction to 5-connected cores
or to graphs with such a piece is made.

## Constant profile differences beyond three roots — FALSIFIED

Take root parts 0022 with colors 0101. The profile is s^2+2s for s>=2,
so its increment is 2s+1, not 2s-1. This can affect the actual unrestricted
glued optimum, not merely a forced boundary coloring.

For any s>=3 let M=2s+1. In each of parts 0 and 2 designate a pair of
roots. Join the two roots in each pair by M internally disjoint paths of
length three, all outside P except their endpoints. Call the resulting
union G, padding by 0 to 4 isolates to make its order divisible by five.
There are 5s+4M vertices before padding. The graph is triangle-free: roots
of a pair are nonadjacent, and every new internal vertex has just its two
path neighbors. Every path of length three costs zero for opposite root
colors and one for equal root colors. Thus

    R(a)=M * (number of equal-colored designated pairs).

When both pairs have opposite colors, the 0022/0101 row gives penalty 2s.
Any other assignment has R(a)>=M>2s and a nonnegative piece penalty.
Thus d(G)=s^2+2s and d(G-X)=(s-1)^2+2(s-1), giving gamma=2s+1.
The private transversal exists because s>=3. Isolates do not affect d.
This rigorously falsifies universal exact increment 2s-1 with four roots.
It does not falsify A/B: the outside paths provide ample vertices and
this five-set itself satisfies B by s<=k-2. Edge-criticality of this
example is not asserted or required for the falsification.

## Remaining bottleneck — CONJECTURAL

The original five-set selection problem remains for residual nonautomatic
critical cores without the established certificates. Within this cycle's
four-boundary subcase, the only unresolved B regime from this bound is a
proper B_(k-1) piece whose optimal remainder assignments all have lambda=2.
The theorem reduces that subcase to controlling the competition of boundary
rows in the two displayed minima; it does not prove such a regime occurs
with only five outside vertices. No complete solution appeared.

## Coverage and verification

All t=1,...,25 artifacts were read in full: complete=true, max_gap=0.
Their homogeneous scope does not fill the mixed gap in the arbitrary
 t>=26 symbolic theorem; later symbolic results reach t>=3, leaving mixed
 t=2 unresolved. No balanced-remainder theorem is used in this proof.
No completed enumeration was repeated, no random search was run, and
process inspection preceded the bounded profile calculations. Only one
computation was active at a time.

**COMPUTATIONALLY VERIFIED:** validation outcome recorded in the checkpoint
and state. Tests check the symbolic certificate, all constrained full cuts
for four roots in B_1 and B_2, and the path-glued obstruction. These are
checks of the stated proof, not general A/B enumeration.
