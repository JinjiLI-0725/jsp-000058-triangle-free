# Extension budgets localize the A/B slack obstruction

Date: 2026-09-18. **Single bottleneck:** how many full-cut slack layers
must be controlled to certify a selected five-set at the A/B threshold?
The result is a **PROVED threshold-dependent reduction**. It improves the
previous incident-edge cutoff, but does not select a five-set and does not
prove A, B, or JSP-000058.

## Uniform extension budget — PROVED

Fix any graph G and vertex set X, and put H=G-X. Write h=e(G[X]),
z=e(X,H), and let U be an integer such that EVERY coloring of H extends
to G with at most U monochromatic edges incident with X. An explicit
choice, requiring no knowledge of d(H), is

    U_X = min(floor((h+z)/2), d(G[X])+floor(z/2)).          (1)

For the first bound, color X independently and uniformly at random. The
expected incident cost is (h+z)/2 for every fixed remainder coloring;
some extension has cost at most its floor. For the second, take a coloring
attaining d(G[X]) and its reversal. The internal cost stays d(G[X]);
the two boundary costs sum to z. Choose the better orientation. Taking
the smaller bound is legitimate separately for every remainder coloring.
For a triangle-free five-set d(G[X]) is 1 precisely when G[X]=C5 and
is 0 otherwise. Thus (1) is a local, directly computable budget.

The word EVERY is essential: a mere upper bound on gamma is not the
uniform extension property used below.

## Localization theorem — PROVED

Use the established notation s(c)=b_G(c)-d(G), r_X(c) for monochromatic
edges incident with X (internal edges counted once), and

    gamma=d(G)-d(H)=max_c(r_X(c)-s(c)).

Choose an optimal coloring of H and extend it with incident cost e<=U.
The resulting full coloring c has

    r_X(c)-s(c)=gamma,       0<=s(c)=e-gamma<=U-gamma.      (2)

This is an existence statement about a maximizing coloring, not an
upper bound on the slack of EVERY maximizing coloring. In particular,
gamma<=U. If L=max_{s(c)=0} r_X(c), then L<=gamma, so

    gamma = max_{0<=s(c)<=U-L} (r_X(c)-s(c)).             (3)

This replaces the older cutoff based on h+z by the usually much smaller
uniform extension budget. It does not bound U-L by a universal constant.

For every integer threshold T>=0 there is the sharper decision rule

    gamma<=T
      iff r_X(c)<=T+s(c) for all c with 0<=s(c)<=U-T-1.   (4)

An upper limit below zero means that the quantified set is empty. If
gamma<=T the inequality holds for every cut by the full-cut identity.
Conversely, if gamma>T then integrality gives gamma>=T+1; the coloring
in (2) violates the inequality and has s(c)<=U-T-1. This proves (4),
including its endpoints and the automatic case U<=T.

An equivalent way to audit the key inference is to hold any remainder
coloring fixed and recolor X optimally. Its score r-s=d(G)-b_H remains
unchanged, while its new slack is at most U-(r-s). Every violation
therefore has a representative inside the stated slack window. We are
not claiming that cuts outside the window individually satisfy the bound.

## Consequence for the one unresolved selection claim

**CONJECTURAL A_window/B_window:** on each nonautomatic edge-critical
triangle-free core C of order 5k, select a five-set X such that every cut
with 0<=s(c)<=U_X-T-1 satisfies r_X(c)<=T+s(c), with T=2k-1 for A and
T=2k-2 for B (excluding B_k in the latter).

**PROVED reduction:** these claims are respectively equivalent to
A_crit/B_crit by (4), and hence to A/B by the existing core-transfer
theorem. This is a smaller cut family to control, not a logically weaker
conjecture or a new proof of the vertex-selection assertion. The q+e
obstruction is respected because (2) explicitly optimizes the remainder
and pays the full extension cost.

A useful narrow-band corollary is: if U_X<=T+1 and L<=T, this X already
meets the threshold. Only slack zero can witness failure in this band.
More generally U_X<=T+j+1 requires only slack 0,...,j. In particular,
any failed X passing all optimal-cut checks must have U_X>=T+2.
These conditions are sufficient; no existence of a set in any fixed
band is asserted. The balanced transversal has U_X=5k-4 and gamma=2k-1,
so even this familiar set need not have U_X close to the target.

## Falsification audit and finite validation

The prior **FALSIFIED** constant-cutoff and optimal-cut-only shortcuts
remain false. The amplified connected examples have growing budgets;
(2) does not contradict their growing minimum maximizing slack. No new
candidate was falsified this cycle.

The proof uses no triangle-freeness except to simplify d(G[X]), no
criticality except for the domain reduction, and no balanced-remainder
theorem. It never infers an upper bound on gamma from an incident count
of one optimal full cut. The -1 in (4) uses integer costs and an integer
threshold; it must not be discarded when describing the exact window.

**COMPUTATIONALLY VERIFIED:** the regression independently enumerates
full cuts and solves induced remainders on every five-set of Petersen,
B_2, C5 plus five isolates, and K_(5,5). It checks both implications of
(4) for every integer T from 0 through U+1, checks (2)/(3), and checks
the uniform extension property for every remainder coloring. These
include critical, noncritical, bipartite, disconnected, and balanced
examples. A separate Petersen four-set regression retains the known
slack-one obstruction, preventing an accidental optimal-cut-only test.
These bounded tests are not a search for A/B counterexamples.

All 25 completed balanced-extension artifacts were read; each records
complete=true and max_gap=0. They certify homogeneous neighborhoods.
Together with the original arbitrary t>=26 proof they do not establish
the all-t arbitrary extension theorem. Later symbolic notes cover t>=3;
mixed t=2 remains unresolved. No enumeration was repeated or used here.

No potential complete proof appeared. The next unresolved claim is
exactly A_window/B_window above: selecting X that controls its budgeted
slack window. Validation and checkpoint details are in
INDUCTION_CHECKPOINT.md.
