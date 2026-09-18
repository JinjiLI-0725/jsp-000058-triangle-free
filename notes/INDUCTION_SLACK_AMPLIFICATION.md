# No constant slack cutoff for critical-core deletion increments

Date: 2026-09-18. **Single bottleneck:** can the full-cut formulation of
A/B be reduced to a fixed number of slack layers on nonautomatic
edge-critical cores? A natural exact truncation claim is **FALSIFIED**.
The counterexample and its unbounded slack requirement are **PROVED**
below. General A, B, and JSP-000058 remain **CONJECTURAL**.

## The precise rejected claim

Use the notation of [INDUCTION_CUT_SLACK.md](INDUCTION_CUT_SLACK.md):
`s(c)=b_G(c)-d(G)` and `r_X(c)` counts monochromatic edges touching X.
The proved identity is `gamma_G(X)=max_c(r_X(c)-s(c))`.

**Candidate S:** there is an absolute integer C>=0 such that, on every
nonautomatic triangle-free edge-critical graph of order 5k and every
five-set X, this maximum is attained by a coloring with s(c)<=C.

The earlier Petersen example rejects C=0. The construction here rejects
every fixed C, even with |X| fixed at five. It does not reject truncation
for a specially selected X, or a cutoff depending on the graph or k.

## A shared-boundary gadget — PROVED

Let P be the Petersen graph with exactly the labeling in the preceding
note, and put Y={0,1,3,8}. Replace each of edges 01 and 38 by a path of
length three, using four distinct new internal vertices. Call the resulting
14-vertex graph Q. In Q, Y is independent. Subdivision preserves
triangle-freeness here: new vertices have degree two and the new paths
cannot create a shorter cycle.

For fixed colors of an odd path's endpoints, its minimum monochromatic
cost is one if the endpoints agree and zero otherwise. The minimum is
attainable with the sole monochromatic edge at any prescribed position
when the endpoints agree. Consequently every coloring of Q has cost at
least that of its restriction to the original vertices evaluated on P,
and every coloring of P has an extension attaining the same cost.
Thus d(Q)=d(P)=3.

Every optimal coloring of Q restricts to an optimal coloring of P and
minimizes the cost of both replacement paths. The five monochromatic
triples of P were proved exhaustively, without computation, in the
preceding note. Each has exactly two edges touching Y. Replacing an
internal Y-edge by an odd path cannot increase its incident contribution
in an optimal extension: the path has only one monochromatic edge, which
can touch Y or lie in the middle. Thus r_Y<=2 on every optimal Q cut.
Equality is attained, for example by extending a P optimal cut whose
monochromatic triple contains neither 01 nor 38.

Q-Y is bipartite: P-Y is a tree, and each replacement path leaves just
one disjoint edge. Therefore gamma_Q(Y)=3. A Q coloring whose restriction
to Q-Y is proper cannot have cost three: such an optimal cut would have
r_Y=3, contrary to r_Y<=2. Its cost is therefore at least four.
The P coloring with side {0,3,4,6,7} has four monochromatic edges,
all touching Y, and has both 01 and 38 crossing. Extend the replacement
paths properly. This gives cost four and a proper coloring of Q-Y.

Q is edge-critical. For an unchanged edge, take a P optimal cut leaving
that edge monochromatic and extend both paths optimally. For an edge
on a replacement path, take a P optimal cut leaving the replaced edge
monochromatic and put the path's unique monochromatic edge at the
prescribed position. Every Q edge is therefore monochromatic in some
optimal Q cut, which is the proved critical-edge criterion.

## Amplification with only four shared deleted vertices — PROVED

For an integer a>=1, take a copies of Q, identifying the four vertices
of Y across all copies, and making no other identifications. Call the
result J_a. Because Y is independent, edge sets of copies are disjoint;
the result is a simple graph of order 10a+4. It is connected and
triangle-free. Indeed a triangle contained in one copy is impossible;
a triangle using different copies would require an edge within Y or
an edge between private vertices of different copies, neither of which
exists.

Every full coloring costs at least three in each copy. Copying a single
optimal Q coloring to all copies attains 3a with consistent Y colors.
Hence d(J_a)=3a. A full optimal coloring has cost exactly three in
every copy, so its incident count is at most 2a, with equality attained
by copying an appropriate Q coloring. J_a-Y is bipartite, giving

    gamma_(J_a)(Y)=3a,       L_(J_a)(Y)=2a.

Criticality also survives the identification. For any selected edge,
choose its optimal monochromatic-edge witness in its Q copy. Give every
other copy the same Q coloring (including the same boundary colors).
The resulting full coloring has cost 3a and witnesses criticality of
the selected edge. This explicitly checks the shared-boundary constraint;
additivity for arbitrary independently chosen cuts is NOT assumed.

To attain gamma=3a in the full-cut identity, a coloring must be proper
on J_a-Y, since its score is exactly `3a-b_(J_a-Y)`. Each copy then costs
at least four, so b>=4a and slack>=a. Conversely, copying the cost-four
Q coloring gives a full coloring of cost 4a, proper on the remainder.
Thus **the minimum slack among maximizing colorings is exactly a**.

## Five deletions and the nonautomatic A/B domain — PROVED

Let h=2a+3, and take G_a to be the disjoint union of J_a, one isolated
vertex z, and B_h. Set X=Y union {z}. Then

    |V(G_a)|=10a+5+5h=5k,       k=4a+4,
    d(G_a)=3a+h^2=4a^2+15a+9 >= 2k,
    d(G_a-X)=h^2,               gamma_(G_a)(X)=3a,
    L_(G_a)(X)=2a.

The graph is triangle-free and edge-critical (including its isolated
vertex, as allowed in the core reduction), and is not B_k. Thus it lies
in the nonautomatic domain of both A_crit and B_crit.

A maximizing cut must be optimal on G_a-X. Its J_a-Y restriction must
be proper and its B_h restriction optimal: the component minima are
zero and h^2, and excesses are nonnegative. Its full slack is consequently
at least a. The copied cost-four coloring and an optimal B_h coloring
attain slack a. For every fixed C, choosing a>C therefore gives

    max_{c: s(c)<=C}(r_X(c)-s(c)) < gamma_(G_a)(X).

This is a symbolic infinite family, not an extrapolation from finite
enumeration. Notice that 3a<=2k-2=8a+6: these particular X satisfy B.
We have not produced an A/B counterexample, or a false positive at their
specific thresholds. Nor have we ruled out a theorem selecting an X with
compatible optimal cuts. The result rules out the universal exact
bounded-slack shortcut, including cutoffs depending only on |X|=5.

## Validation and checkpoint

**COMPUTATIONALLY VERIFIED:** `tests/test_induction_slack_amplification.py`
enumerates all 16384 labeled Q colorings. It independently checks d=3,
triangle-freeness, critical-edge coverage, the optimal incident maximum
two, and minimum cost four subject to a proper remainder. An exact
dynamic program, keeping all 16 Y color patterns separate, combines
the resulting (cost, incident-count) tables for a=1,2,3,5. It verifies
the formulas and minimum maximizing slack a for these four sizes.
These finite checks supplement the all-a proof; they do not certify A/B.

All completed t=1,...,25 extension artifacts were read; all have
complete=true and max_gap=0. They certify homogeneous patterns. The
original arbitrary t>=26 symbolic theorem therefore does not combine
with them into an all-t arbitrary theorem. Later symbolic notes reach
t>=3; mixed t=2 remains unresolved. No balanced-remainder result is
used as a premise here, and no extension enumeration was repeated.

**CONJECTURAL / remaining single target:** select X on a nonautomatic
critical core so that every coloring obeys r_X(c)<=T+s(c), where T is
2k-1 for A or 2k-2 for nonbalanced B. Controlling finitely many universal
slack layers cannot supply an exact formula for arbitrary X. Further
progress must exploit selection of X, a graph-dependent slack bound,
or another bound on remainder cuts. No potential complete proof appeared.
