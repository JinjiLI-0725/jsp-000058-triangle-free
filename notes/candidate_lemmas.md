# Candidate lemmas and research directions

Current single target (2026-09-18): **CONJECTURAL M for t=2,3**, with
strictness for nonbalanced extensions, in the mixed-pattern representation of
[BALANCED_EXTENSION_AUDIT.md](BALANCED_EXTENSION_AUDIT.md).
The [occupied-type proof](BALANCED_EXTENSION_TYPE_OCCUPANCY.md) establishes
the strict arbitrary extension theorem for every t>=4, superseding the
previous t>=6 threshold. It uses an auxiliary blow-up only for H and boundary
costs, and explicitly charges internal monochromatic edges. No homogeneous
spanning-supergraph reduction is assumed. The completed homogeneous
t=1,...,25 enumeration does not settle M in the remaining mixed range.

This advances only the balanced-remainder transition of A/B_inherit.
General A, B, and the q+e selection obstruction remain conjectural. The
next precise obstacle is the t=3 noninjective estimate t(t+1)+4=16, which
misses the required strict bound 15 by one. Historical broad-search
suggestions below are not the current next action.

Computational evidence is not proof. These statements are not used to prune
the exhaustive k=2 search or certify the k=3 conjecture.

Update: [structural_analysis.md](structural_analysis.md) proves the blow-up
reduction and exact C5 formula below, proves local equality rigidity, and
records tested five-vertex reduction candidates. The earlier evidence and
research directions below are retained for context.

## C1: rigidity of equality at multiples of five

Candidate: if a triangle-free graph on 5k vertices has d=k², it is the balanced
C5 blow-up with five independent parts of size k.

Evidence: the exhaustive k=1 run has only labeled copies of C5 at equality.
The exhaustive k=2 run has exactly one equality isomorphism class, the balanced
C5 blow-up with weights (2,2,2,2,2). Neither observation establishes the
statement for k>=3. The structured and heuristic k=3 run tests this pattern
but cannot rule out other equality graphs. See observations for the final run
counts and canonical witnesses.

Next falsification test: target 15-vertex graphs with d>=9 and a false-twin
quotient different from C5; seed searches from the saved non-C5 near-extremizers.
The current implementation never assumes this rigidity when evaluating graphs.

## C2: class-respecting cuts as a reduction for blow-ups

Proposed useful reduction: for a blow-up of a fixed simple graph H with positive
integer part sizes w_i, there exists a maximum cut placing each part wholly on
one side. Consequently, d equals the minimum over two-colorings of H of the
sum of w_i*w_j over monochromatic base edges ij.

Reason to investigate: with all other parts fixed, the cut size is linear in
the number of vertices placed on one side in a given independent part. Moving
that entire part to a favorable endpoint cannot lower the cut. Repeating over
parts suggests the reduction. This is a separate elementary argument, not a
consequence of the numerical data and not a solution of JSP-000058. Automated
checks compare weighted base enumeration with full 15-vertex enumeration on
representative weight vectors for every structured family.

For odd cycle bases, the resulting weighted-cycle formula is expected to be
`d = min_i w_i*w_(i+1)`: every two-coloring leaves an odd number of cycle edges
monochromatic, and each individual cycle edge can be the sole monochromatic
edge. This formula is now proved in `structural_analysis.md`, including zero weights.
The positive-weight structured search evaluates full graphs directly;
it does not rely on this formula for its reported MaxCut values.

## C3: quantitative stability rather than exact near-equality structure

A useful future statement might bound the number of edits to a balanced C5
blow-up in terms of the deficit k²-d. No numerical constant or general bound
has been justified. Exact C5-blow-up structure at deficit one is already false
(see rejected lemma R3). Distances to the family, rather than twin-class
identity alone, should be measured before proposing a precise stability claim.
