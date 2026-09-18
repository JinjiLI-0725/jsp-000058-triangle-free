> **Subsequent result:** [INDUCTION_TWO_CONNECTED_SLACK.md](INDUCTION_TWO_CONNECTED_SLACK.md)
> gives 2-connected critical examples with false positives at the actual
> A/B thresholds for every universal constant slack cutoff. The earlier
> formulas and the graph-dependent localization theorem remain valid.

# Connected critical cores still require unbounded slack

Date: 2026-09-18. **Single bottleneck:** does connectedness make optimal
full cuts, or a fixed number of slack layers, sufficient to evaluate the
five-deletion increment on nonautomatic critical cores? **FALSIFIED.**
This strengthens the existing obstruction; it does not settle selection
of a good five-set in A or B.

## One-vertex gluing lemma — PROVED

Suppose connected graphs H_i have disjoint edges and share exactly one
vertex w, with no other inter-block edges. Then d(G)=sum_i d(H_i).
Every coloring has at least that cost. Conversely, independently optimal
block colorings can each be reversed to assign w color zero, attaining
the sum. Thus every optimal full coloring is optimal in every block.
If all blocks are edge-critical, so is G: choose an optimal coloring
leaving the specified edge monochromatic in its block and align optimal
colorings of every other block at w. The critical-edge criterion applies.
Every cycle lies in one block (a simple cycle cannot revisit w), so
triangle-freeness also survives. These statements need only one shared
vertex; arbitrary multi-vertex gluing would not justify them.

If w is retained when X is deleted, the same argument applies to the
remainders, even when a remainder is disconnected. Consequently gamma
and the optimal-cut incident maximum L both add over blocks. For L,
independently maximizing optimal cuts can again be aligned at w.
Also the minimum full cost subject to being optimal on G-X adds: each
block must attain its own remainder minimum, and complementing its cut
preserves that property. This last observation controls positive slack,
not merely optimal full cuts.

## A connected symbolic family — PROVED

Use J_a and Y from [INDUCTION_SLACK_AMPLIFICATION.md](INDUCTION_SLACK_AMPLIFICATION.md),
for a>=1. The proved gadget properties are

    |J_a|=10a+4, d(J_a)=3a, d(J_a-Y)=0, L_(J_a)(Y)=2a.

J_a is connected, triangle-free and edge-critical. The minimum cost of a
coloring proper on J_a-Y is 4a. These facts follow from the explicit
subdivided Petersen gadget and its shared independent four-set, rather
than an assumption about arbitrary gluing. Choose any private vertex
w outside Y. Set h=2a+3. Glue J_a, B_h, and a chordless C13 at w,
with all remaining vertices distinct; call the result K_a. Choose any
cycle vertex z different from w, and put X=Y union {z}.

The one-vertex lemma proves connectedness, triangle-freeness and
edge-criticality. In fact there are no bridges: each block edge lies
on a cycle. Indeed a bridge is crossing in every optimal cut (otherwise
reverse one component across it), so an edge-critical graph has no bridges.
The graph has an articulation vertex and is not B_k.
The numerical identities are

    |K_a|=10a+4+(5h-1)+12=5k,     k=4a+6,
    d(K_a)=3a+h^2+1=4a^2+15a+10,
    d(K_a-X)=h^2,
    gamma_(K_a)(X)=3a+1,          L_(K_a)(X)=2a+1.

For the cycle, d(C13)=1; deleting z leaves a path; an optimal coloring
can put its sole monochromatic edge incident with z, so its L is one.
The B_h block is untouched and contributes zero to both gamma and L.
The gluing lemma now gives the displayed identities, even if removing Y
separates the J_a remainder.

Furthermore, a coloring attaining gamma must be optimal on the remainder:
its score is exactly d(K_a)-b_(K_a-X). Its cost on J_a is at least 4a,
on B_h at least h^2, and on C13 at least one. All three bounds are
simultaneously attainable by aligning at w. Therefore the **minimum
slack of a maximizing coloring is exactly a**.

Since d(K_a)-2k=4a^2+7a-2>0 for every a>=1, these connected graphs lie
in the nonautomatic domain of both A_crit and B_crit. Thus connectedness
does not repair Candidate O, and no universal constant slack cutoff
computes every five-deletion increment even on connected critical cores.
Choosing a larger than any proposed cutoff gives a symbolic counterexample.

## Limits, inference audit, and validation

**CONJECTURAL:** A and B, including five-set selection on connected cores,
remain open. The exhibited set actually satisfies B, since
3a+1<=2k-2=8a+10. This is not a false positive at the A/B thresholds.
The family has a cut vertex; it says nothing about a restriction to
2-connected cores. No reduction of A/B to 2-connected cores is claimed:
block orders need not be multiples of five, and five deletions must still
be allocated. No potential complete solution appeared.

Checks against possible proof failures: X avoids the shared vertex;
all gluing uses color reversal, which preserves both cost and incident
counts; nonnegative block excesses force each remainder individually
optimal; criticality is witnessed edge by edge with compatible colors;
order counts subtract both identifications; the strict nonautomatic
inequality holds already at a=1. No optimal-cut upper bound is substituted
for gamma.

**COMPUTATIONALLY VERIFIED:** the new regression enumerates rooted cuts
of Q, C13 and B_3 and combines their exact (cost, remainder-cost) tables.
It checks d=13, gamma=4, L=3 and minimum maximizing slack one for their
connected one-vertex union, and independently checks its graph structure.
This finite instance validates the gluing inference; its B_3 scale is
not in the nonautomatic domain. That domain for K_a is established by
the symbolic calculation above, not by this test. Existing amplification
tests check the J_a boundary constraints at a=1,2,3,5.

All completed t=1,...,25 artifacts were read: complete=true, max_gap=0.
They certify homogeneous extensions; together with the arbitrary t>=26
proof they do not cover all mixed extensions. Later symbolic proofs cover
t>=3; mixed t=2 remains unresolved. No balanced-extension result is used
here and no enumeration was repeated. No random search was run.

Validation command: `.venv/bin/python -m pytest -q
 tests/test_induction_connected_slack.py
 tests/test_induction_slack_amplification.py
 tests/test_induction_cut_slack.py tests/test_induction_critical_core.py`
— **9 passed**, 59.59 seconds. Process inspection before the bounded test
run found no existing compute job. No other computation ran concurrently.
