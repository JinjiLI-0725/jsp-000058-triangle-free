> **Latest progress (2026-09-18, threshold slack localization):**
> [INDUCTION_THRESHOLD_SLACK.md](INDUCTION_THRESHOLD_SLACK.md) proves that
> a uniform extension budget U_X gives an exact threshold test using only
> cuts with slack at most U_X-T-1. Here
> U_X=min(floor((h+z)/2), d(G[X])+floor(z/2)). This improves the earlier
> incident-edge cutoff; it does not give a constant cutoff or select X.
> A_window/B_window remain **CONJECTURAL**, equivalent to A/B on critical
> cores. No balanced-extension enumeration was repeated.

> **Latest progress (2026-09-18, connected slack obstruction):**
> [INDUCTION_CONNECTED_SLACK.md](INDUCTION_CONNECTED_SLACK.md) proves that
> even connected, bridgeless, nonautomatic edge-critical cores can require
> arbitrarily large slack to attain a specified five-deletion increment.
> The one-vertex union of J_a, B_(2a+3), and C13 has gamma=3a+1,
> optimal-cut maximum 2a+1, and minimum maximizing slack a.
> **FALSIFIED:** connected versions of optimal-cut sufficiency and universal
> constant slack truncation. A/B remain **CONJECTURAL**; these sets satisfy B.

> **Latest progress (2026-09-18, full-cut slack):**
> [INDUCTION_CUT_SLACK.md](INDUCTION_CUT_SLACK.md) proves the exact identity
> gamma(X)=max_c(r_X(c)-s(c)). **FALSIFIED:** restricting this maximum to
> optimal full-graph cuts, even on nonautomatic edge-critical cores.
> The symbolic family Petersen disjoint-union B_s (s>=3) has a specified
> five-set with gamma=s+3 but optimal-cut maximum s+2. A slack-one cut
> accounts for the gap. A/B remain **CONJECTURAL**; positive-slack cuts
> must be controlled as part of the same five-set selection bottleneck.

# Candidate lemmas and research directions

Current single bottleneck (2026-09-18): **CONJECTURAL A_crit/B_crit**, the
five-vertex q+e selection claim restricted to edge-critical spanning cores.
The reduction to this class is **PROVED** in
[INDUCTION_CRITICAL_CORE.md](INDUCTION_CRITICAL_CORE.md): preserving d while
removing edges can only increase every five-deletion increment. Thus any
witness in the core transfers to the original graph. The proof also handles
B's balanced exception, and proves that a positive complete C5 blow-up is
edge-critical exactly when balanced.

The next step is to coordinate the optimal cuts witnessing criticality
of individual edges into one five-set and one remainder coloring. The
union of their monochromatic edge sets covers all edges, but this does not
yet control q+e after deletion. A_crit requires only d>=2k; B_crit requires
d>=2k-1 and excludes B_k. Smaller d is automatic. Neither restricted lemma
is proved or computationally certified at arbitrary order.

The previous balanced-remainder target is still **CONJECTURAL M for t=2**,
including strictness for nonbalanced arbitrary mixed extensions. The
[BALANCED_EXTENSION_T3.md](BALANCED_EXTENSION_T3.md) proof handles t>=3.
Completed homogeneous t=1,...,25 enumeration does not settle mixed t=2.
This cycle did not advance or repeat that computation.

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
