# Three-boundary profiles and five-set selection

Date: 2026-09-19. Single bottleneck: five-set q+e selection on residual
critical cores. This extends the two-boundary balanced-piece certificate;
it does not reduce arbitrary cores to balanced pieces. General A/B remain
**CONJECTURAL**.

## Exact constrained profile — PROVED

Let S contain at most three specified vertices of B_s. For a prescribed
coloring a of S, let F_s(a) be the minimum monochromatic edge count among
its extensions. Then

    F_s(a) = s^2 + delta(S,a),     delta in {0,2},

where delta is independent of s whenever the specified vertices fit in
their parts. With at most two roots delta=0 by the earlier proof. For three
roots, rotations, reflections, root relabeling, and global color reversal
reduce to the following table. Root colors are ordered as the listed parts.
The string b indicates which parts' *unprescribed* vertices have color zero
(bit 1 means zero). Every row gives a coloring attaining s^2+delta.

| Root parts | Root colors | delta | b |
|---|---|---:|---|
| 000 | 000,001,010,011 | 0 | 00101 |
| 001 | 000,010 | 0 | 01010 |
| 001 | 001,011 | 0 | 00101 |
| 002 | 000,010 | 0 | 00101 |
| 002 | 001,011 | 0 | 01010 |
| 012 | 000 | 2 | 00101 |
| 012 | 001 | 0 | 01010 |
| 012 | 010 | 0 | 00101 |
| 012 | 011 | 0 | 10010 |
| 013 | 000 | 0 | 01010 |
| 013 | 001 | 2 | 00101 |
| 013 | 010 | 0 | 10010 |
| 013 | 011 | 0 | 00101 |

Here is a finite algebraic proof, including the lower bound in the two
exceptional rows. Let r_i count roots and z_i count zero-colored roots in
part i. Holding all other parts fixed, the objective is linear in the
number of zero-colored unprescribed vertices of part i. Rounding those
vertices together to one color preserves the constraints and cannot
increase cost. Repeating for all five parts proves

    F_s(a) = min_{b in {0,1}^5} C_b(s),
    x_i = z_i + b_i(s-r_i),
    C_b(s) = sum_i [x_i x_(i+1) + (s-x_i)(s-x_(i+1))].

Substitution of the displayed witnesses proves all upper bounds. The
unconstrained lower bound s^2 proves every delta=0 row. For delta=2 put
u=s-1>=0. Substituting the 32 possible b strings gives precisely the
following distinct coefficient triples (A,B,C) of
C_b(s)-s^2-2 = A u^2+B u+C:

    parts 012, colors 000:
    (0,0,0), (0,2,0), (0,4,2), (2,0,0), (2,2,0),
    (2,2,2), (2,4,0), (2,4,2), (2,6,2), (4,2,0), (4,8,2).

    parts 013, colors 001:
    (0,0,0), (0,2,0), (2,2,0), (2,4,0), (4,4,0), (4,6,0).

Every coefficient is nonnegative, proving the missing lower bounds for
all s>=1. These explicit polynomial identities are a proof over arbitrary
s, not an extrapolation from tested sizes. Three roots in one part, two
in one part with the third at distance one or two, and three distinct
parts of the two possible shapes exhaust the boundary placements.

## Private transversal theorem — PROVED

Suppose G has order 5k and contains an induced P=B_s. All edges from P to
outside P must meet a retained S subset V(P), |S|<=3. Assume every part
has a vertex outside S, and select one such vertex from each part as X.
This requires s>=2; s>=4 always guarantees feasibility.

Let R contain the outside vertices and S, and all edges of G not assigned
to P. In particular any edges within S belong only to P. With F_R(a)
the constrained cost in R, edge-disjoint gluing gives exactly

    d(G)   = s^2     + min_a [delta(S,a)+F_R(a)],
    d(G-X) = (s-1)^2 + min_a [delta(S,a)+F_R(a)].

The same roots, their same-part relations, and their colors survive in
P-X=B_(s-1), so delta is identical in these equations. Consequently

    gamma_G(X)=2s-1.

If P is proper, s<=k-1, so gamma<=2k-3 and X satisfies both A and B.
If P=G=B_k, it gives A's sharp value. No conjectural bound on R is used,
and criticality is unnecessary. Equal-d spanning-core transfer preserves
this five-set upper bound in the original graph.

The table also resolves q+e, not just the difference of minima. Choose
a minimizing a and an optimal R coloring, and use the same table witness
at sizes s and s-1. These nested colorings have optimal remainder cost,
so q=0 and e=2s-1. A cheaper extension would contradict d(G).

## Falsification safeguards

**FALSIFIED:** three-boundary flatness F_s(a)=s^2. Three roots in consecutive
parts, all colored zero, have F_s=s^2+2. Thus unconditional additivity
s^2+d(R) cannot replace the shared minimization above. Constant *difference*
of profiles, rather than flatness, is what the selection theorem needs.

For example attach a subdivided claw to three consecutive-part roots of
B_2: add a center and three private intermediates, joining each root to
the center through its own intermediate. The union is triangle-free.
The claw costs zero for equal root colors, and one for any nonconstant
root assignment. Hence d(G)=4+min(2,1)=5, while d(B_2)+d(claw)=4.
After a private transversal d(G-X)=1+min(2,1)=2, as required.
One isolate gives order 15; B's bound is four and this set costs three.
This example checks compatibility, not a new nonautomatic critical family.

**CONJECTURAL:** A/B on the remaining nonautomatic cores without automatic,
path, pendant, or feasible three-boundary balanced-piece witnesses. There
is no claimed reduction to 4-connected cores, and no assertion about four
or more roots. No potential complete proof of JSP-000058 appeared.

## Coverage and validation

All completed t=1,...,25 JSON artifacts were read: complete=true and
max_gap=0 throughout. These certify homogeneous neighborhoods. The arbitrary
t>=26 symbolic argument does not fill mixed t=2,...,25 by combining with
those artifacts; later symbolic notes reach t>=3, leaving mixed t=2 open.
No balanced-remainder extension theorem is used here. No enumeration was
repeated and no random search was run.

**COMPUTATIONALLY VERIFIED:** all 20 normalized symbolic profile rows
(32 templates each), every root triple and full cut of B_1/B_2, and the
nonflat glued example with a nested q=0 optimum. Including two-boundary
regressions, **7 tests passed in 68.99 seconds**. The command and final
process status are in the checkpoint and current state. `git diff --check`
passed. No compute job remains.
