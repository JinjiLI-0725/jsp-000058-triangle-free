# Induction checkpoint — 2026-09-18, threshold slack localization

JSP-000058 and induction lemmas A/B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: how many full-cut slack layers must
be controlled to certify a selected five-set at the A/B threshold?
See [INDUCTION_THRESHOLD_SLACK.md](INDUCTION_THRESHOLD_SLACK.md).

## PROVED

For h=e(G[X]) and z=e(X,G-X), the local integer budget
U_X=min(floor((h+z)/2), d(G[X])+floor(z/2)) bounds the extension cost
of EVERY remainder coloring. There is a full coloring attaining gamma
with slack at most U_X-gamma. Consequently, for every integer T>=0,

    gamma(X)<=T iff r_X(c)<=T+s(c) for all 0<=s(c)<=U_X-T-1.

The empty window is automatic. If L is the optimal-full-cut incident
maximum, exact evaluation also needs only slack at most U_X-L.
In particular, U_X<=T+1 and L<=T suffice. This improves the previous
incident-edge cutoff without claiming a universal constant cutoff.

## COMPUTATIONALLY VERIFIED

Tests independently check the uniform extension budget for every remainder
coloring, the maximizing-witness slack bound, and both directions of the
threshold test for all integer T=0,...,U_X+1 on every five-set of four
fixed order-10 graphs: Petersen, B_2, C5 plus five isolates, and K_(5,5).
The known Petersen four-set slack-one obstruction is retained. Existing
full-cut identity and critical Petersen/B_3 certificates also pass.

Validation: `.venv/bin/python -m pytest -q
 tests/test_induction_threshold_slack.py tests/test_induction_cut_slack.py`
— **5 passed**, 82.99 seconds. These are bounded inference checks, not
an exhaustive A/B verification. Process inspection before launch found
no visible existing compute job. Only this test job was launched; it has
finished. No random search or balanced-extension enumeration ran.

## CONJECTURAL / exact next claim

A_window/B_window: on each nonautomatic critical core, select five vertices
X passing its threshold test through slack U_X-T-1, with T=2k-1 for A
or 2k-2 for nonbalanced B. These are equivalent to A/B by the proved
localization and core-transfer results. The selection claim is unresolved;
no fixed-width window is guaranteed, even for balanced transversals.

## FALSIFIED / retained limits

The earlier optimal-cut-only and universal constant-slack shortcuts remain
falsified, including on connected bridgeless critical cores. No new
candidate was falsified this cycle. The new cutoff varies with X and G.

All t=1,...,25 artifacts were read and have complete=true, max_gap=0.
Their homogeneous certification and the original arbitrary t>=26 proof
do not establish an all-t arbitrary extension theorem. Later symbolic
proofs cover t>=3; mixed t=2 remains unresolved. No extension theorem
was used in this cycle. No potential complete proof appeared.

Notes and state were updated; `git diff --check` passed. Unrelated
existing overnight log changes were left untouched. This is a clean
research checkpoint, not a claim that the working tree is otherwise clean.
