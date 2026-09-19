# Five-boundary selection, including the outside budget

Date: 2026-09-19. **Single bottleneck:** private-transversal q+e selection
for a balanced piece with five retained attachment vertices. This extends
the four-boundary certificate. General A/B and JSP-000058 remain
**CONJECTURAL**; no reduction of arbitrary critical cores to these pieces
is claimed.

## Constrained profiles — PROVED

Prescribe colors on five distinct roots of B_t. Record their parts p_i and
colors a_i, for i=0,...,4. Let r_j count roots in part j, z_j count its
zero-colored roots, and m=max_j r_j. For integers t>=m, write F_t(a) for
the minimum monochromatic edge count extending these colors.

Root permutation, dihedral symmetry of the part cycle, and global color
reversal leave 111 orbits. Their exact profiles are:

| Penalty F_t(a)-t^2 | Number of orbits |
| --- | ---: |
| 0 | 66 |
| 2 | 18 |
| 4 | 11 |
| 6 | 2 |
| 2t | 12 |
| 2t+2 | 1 |
| min(2t,8) | 1 |

The 2t+2 row is p=01234, a=00000. The piecewise row is
p=00113, a=00001, with m=2. Root digits can repeat but roots are distinct.
In particular every penalty is nondecreasing and has consecutive integer
increments between zero and two.

Here is a finite algebraic certificate for the classification, including
the whole unbounded size range. The explicit 111 orbit representatives,
intervals, and attaining bit strings are in
[profiles.json](../results/induction_five_boundary/profiles.json).
This is an exact certificate, not fitted values at sampled sizes.

Holding all other colors fixed, the cost is linear in the number of
unprescribed zero vertices in a part. Round each such count to an endpoint
without increasing the cost. Thus F_t is the minimum of the 32 templates
with zero counts x_j=z_j+b_j(t-r_j), b_j in {0,1}. Put v_j=z_j-b_j*r_j.
The template polynomial is C_b(t)=A_b*t^2+L_b*t+H_b, where

    A_b = sum_j [b_j*b_(j+1)+(1-b_j)*(1-b_(j+1))],
    L_b = sum_j [(2*b_j-1)*v_(j+1)+(2*b_(j+1)-1)*v_j],
    H_b = 2*sum_j v_j*v_(j+1).

For a proposed region t>=l with penalty lambda*t+delta, set

    alpha = A_b-1,
    beta  = (2*l+1)*alpha + L_b-lambda,
    eta   = l*l*alpha + l*(L_b-lambda) + H_b-delta.

Every certificate row on an unbounded region has alpha,beta,eta>=0 for
EVERY b. For t=l+u its cost minus the claimed profile is exactly

    alpha*u*(u-1) + beta*u + eta >= 0

for every integer u>=0. The supplied witness has polynomial coefficients
(1,lambda,delta), giving equality. Integer rather than real u matters:
the all-zero transversal row can have alpha>0 and beta=eta=0.
Its lower bound must not be justified by nonnegative ordinary monomial
coefficients, which need not hold.

For 00113/00001, the first region is the three integers t=2,3,4,
with witness b=01010 and profile t^2+2t. Direct substitution of all 32
polynomials at these three integers gives the lower bound. On t>=4,
b=00101 attains t^2+8 and the preceding nonnegative-coefficient certificate
applies. Both formulas agree at 4. This proves the finite first region
and the infinite second region without extrapolation. The regression
checks orbit coverage and every integer certificate coefficient.

## Private-transversal bound with arbitrary outside order — PROVED

Let G have order 5k and an induced piece P=B_s. Assume all edges from P
to outside P meet a retained root set S of size at most five, and every
part has a vertex outside S. Delete one such private vertex per part,
forming X. For exactly five roots s>=m+1; fewer roots use the earlier
profiles. Assign all P edges to P and all other edges to R, retaining S
as the shared boundary. R has no root-root edges. Its optimized cost
with root colors a is R(a), independent of s. Consequently

    d(G)   = s^2     + min_a [f_a(s)+R(a)],
    d(G-X) = (s-1)^2 + min_a [f_a(s-1)+R(a)],

where f_a(t)=F_t(a)-t^2. The profile classification proves

    2s-1 <= gamma_G(X) <= 2s+1.

The upper bound has an explicit q=0 certificate: take an optimal
remainder assignment and an attaining template at t=s-1 with slope at
most two. At the kink t=4 choose the constant template. Extend by giving
the deleted vertex of each part the template color. The added cost is
2s-1+lambda<=2s+1, without changing the remainder's optimal cost.

Thus every proper such piece supplies A, and s<=k-2 supplies B with
gamma<=2k-3. It remains to account for s=k-1, when outside P has five
vertices. This is part of the same five-boundary selection claim.

## Five outside vertices remove the B gap — PROVED

Let O contain N<=5 outside vertices. Fix any coloring of O and a root
coloring a. Flipping root i while leaving O fixed changes the R-cost by

    D_i = opposite-colored O-neighbors - same-colored O-neighbors.

Flipping a set J changes R by sum_(i in J) D_i, since R has no root-root
edges. Each outside vertex has an independent neighborhood in the roots.
This constraint holds even when O has internal edges; those edges retain
exactly the same cost under our flips.

The following table covers all 14 nonconstant profile orbits. Positions
are numbered 0,...,4 in the displayed root order. An action J is a set of
positions to flip. Its resulting profile has a constant penalty delta.
Repeated actions count with multiplicity in the average. The column c
bounds the sum of the actions' R-cost changes contributed by ONE outside
vertex, for either color and every independent root neighborhood. The
column U=floor((5c+sum delta)/number of actions) bounds the cheapest
action's total extra cost above t^2+R(a).

| Parts | Colors | m | Actions J : delta | c | U | Minimum original penalty |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| 00022 | 00101 | 3 | 2:0, 3:0, 4:0 | 2 | 3 | 6 |
| 00023 | 00100 | 3 | 2:0, 3:0, 4:0 | 1 | 1 | 6 |
| 00023 | 00111 | 3 | 2:2, 3:0, 4:0 | 2 | 4 | 6 |
| 00113 | 00001 | 2 | 0:4, 1:4, 2:4, 3:4, 4:0, 4:0 | 2 | 4 | 4 |
| 00123 | 00011 | 2 | 2:2, 3:4, 4:0 | 1 | 3 | 4 |
| 00133 | 00001 | 2 | 2:0, 3:4, 4:0 | 2 | 4 | 4 |
| 00134 | 00011 | 2 | 2:0, 3:0, 4:4 | 1 | 3 | 4 |
| 00122 | 01001 | 2 | 0:0, 1:2, 3:0, 4:2 | 2 | 3 | 4 |
| 00123 | 01000 | 2 | 0:2, 1:2, 3:0, 4:2 | 2 | 4 | 4 |
| 00124 | 01001 | 2 | 1:2, 2:2, 3:0, 4:2 | 1 | 2 | 4 |
| 00123 | 01011 | 2 | 0:0, 3:2, 4:0 | 1 | 2 | 4 |
| 00133 | 01001 | 2 | 0:0, 3:2, 4:0 | 2 | 4 | 4 |
| 01234 | 00000 | 1 | 0:2, 1:2, 2:2, 3:2, 4:2 | 2 | 4 | 4 |
| 01234 | 00011 | 1 | 3:2, 1:0, {0,4}:0 | 1 | 2 | 2 |

All rows have U no larger than the original penalty at any admissible t.
Thus every nonconstant row is dominated or tied by a constant-profile
row, keeping the outside coloring fixed. The penultimate row uses that
an independent set of C5 has size at most two. In the last row the
aggregate flipped positions are 0,1,3,4, each once. Same-colored positions
0,1 are adjacent, as are 3,4, so one outside vertex contributes at most
one; the penalties sum to two, yielding floor((5+2)/3)=2.
In the piecewise row the multiplicities are (1,1,1,1,2). The two roots
in part 0 are adjacent to both roots in part 1. Positive contributions
from these four zero roots total at most two; the last root, colored one,
has weight two. For either outside color the contribution is at most
two. The penalty sum is 16, yielding floor((10+16)/6)=4.
The other rows follow directly from the same independent-neighborhood
check; the tests check every allowed neighborhood and both outside colors.

It follows that, for all t>=m, the optimized glued profile is

    d(G_t) = t^2 + K,
    K = min_(a with constant profile) [delta_a+R(a)],

with K independent of t. Here G_t retains the same roots, outside graph,
and attachments, changing only the number of private vertices per part.
An attaining constant-profile template gives nested optimal colorings.
At s=k-1 this proves gamma_G(X)=2s-1=2k-3, with q=0 and e=2s-1.

Combining both size regimes, **every proper balanced piece with at most
five attachment roots and a private transversal supplies B (and A),
with gamma<=2k-3**. The s=1 case necessarily has no roots and is an
isolated C5, with increment one. Equal-d spanning-core transfer preserves
the upper bound for the original graph, but need not preserve its q=0
coloring. The spanning piece B_k has the familiar A increment 2k-1.

## Falsification and scope

**FALSIFIED:** every five-root profile is one fixed quadratic polynomial
throughout its admissible size range. The 00113/00001 row has penalty
2t at t=2,3,4 and penalty 8 at every t>=4. This refutes that profile
shortcut, not A/B. The earlier unrestricted-outside four-root obstruction
still disproves universal exact increment 2s-1 without an outside budget.

**COMPUTATIONALLY VERIFIED:** tests independently enumerate full cuts
for every five-root set and coloring in B_1 and B_2; check the complete
111-orbit algebraic certificate; check the flip table against every
independent neighborhood; and optimize fixed glued examples by all
feasible part counts and outside colors, including nested optima.
The all-size claims follow from the displayed certificate and inequalities,
not from the small full-cut tests. A bounded aggregate-vector check of the
last row covered 6,895 vectors from five outside vertices; the final proof
uses the simpler three-action inequality instead of this enumeration.

**CONJECTURAL:** general five-set q+e selection on residual nonautomatic
critical cores, general A/B, and JSP-000058. Larger boundaries and graphs
without balanced pieces are outside this theorem. Mixed t=2 balanced
extensions remain open. No potential complete solution appeared.

All t=1,...,25 artifacts were read in full and have complete=true and
max_gap=0. They certify homogeneous neighborhoods. The arbitrary t>=26
symbolic theorem does not combine with them to cover all mixed cases;
the subsequent symbolic proofs reach t>=3. No balanced-remainder theorem
is used as a premise here. The t=5 empty witness does not classify equality.
No completed enumeration or random search was run. Process inspection
preceded computation; bounded jobs ran sequentially.

Validation: `.venv/bin/python -m pytest -q
 tests/test_induction_five_boundary_selection.py
 tests/test_induction_four_boundary_budget.py
 tests/test_induction_four_boundary_selection.py` — **9 passed in 41.69 seconds**.
`git diff --check` passed. No compute job remains running.
