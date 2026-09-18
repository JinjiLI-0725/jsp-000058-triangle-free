# Induction checkpoint — 2026-09-18, t=7 equality-case refinement

JSP-000058 and general induction lemmas A and B remain **CONJECTURAL**.
Single bottleneck this cycle: arbitrary mixed-neighborhood extensions of a
balanced remainder, including the strict transition needed by B_inherit.

## Genuine progress

**PROVED:** every triangle-free five-vertex extension of B_t, for t>=7,
satisfies d(G)<=(t+1)^2, with equality exactly for B_(t+1).
The new t=7 proof and inference audit are in
[BALANCED_EXTENSION_T7.md](BALANCED_EXTENSION_T7.md); t>=8 follows from
[BALANCED_EXTENSION_COVER_BOUND.md](BALANCED_EXTENSION_COVER_BOUND.md).

The exact surplus identity is
D-7L=sum_(j,a in A_j) [alpha(F[S_j])-|N_X(a)|]. The five-cut average
proves strictness unless W-D>=5. At t=7 the only possibilities are:

- K_(1,4), L=1, W=12, D=7;
- K_(1,4), L=2, W=20, D=14 or 15;
- K_(2,3), L=1, W=12, D=7.

In each case maximum-cardinality independent patterns force a star center
to have no neighbors in a shared allowed part (or no H neighbors at all).
Retyping that center makes every X-edge compatible. Repeated leaf types
force containment in an unbalanced C5 blow-up, proving strictness.

## Exact scope and classifications

- **COMPUTATIONALLY VERIFIED:** all saved t=1,...,25 runs are complete,
  have max_gap=0, and cover homogeneous neighborhoods. All artifacts were
  read; no extension enumeration was repeated.
- **FALSIFIED (previous cycle):** homogeneous spanning-supergraph coverage
  of arbitrary mixed neighborhoods. No such reduction is used here.
- **PROVED:** arbitrary extensions at t>=7, including strictness.
- **COMPUTATIONALLY VERIFIED:** arbitrary t=1 and its equality
  classification from the separately saved exhaustive n=10 result.
- **CONJECTURAL:** mixed t=2,...,6, general A, general B, and JSP-000058.

The t<=25 certificates and original t>=26 proof do not establish the all-t
arbitrary theorem: their finite coverage differs. The new symbolic proofs
close part, but not all, of that gap. Finite max_gap=0 does not itself
classify equality.

For k>=8, any X with G-X=B_(k-1) satisfies A, and B if G is nonbalanced.
A plus equality uniqueness through k=7 would imply uniqueness at every
order by B_inherit. Neither that finite base nor A is proved here. For
arbitrary remainders the exact min_c(q_H(c)+e_X(c)) obstruction remains.

## Next action and clean stopping point

Prove the mixed-pattern inequality M for 2<=t<=6, with strictness for
nonbalanced graphs. At t=6 analyze W-D>=5 with D>=6L; do not assume the
three t=7 cases still exhaust it. No potential complete solution appeared.

No long-running research computation was launched. Process inspection found
no existing compute job before the bounded check. Existing overnight logs
were left untouched. No broad random search or t=1,...,25 rerun occurred.

## Validation

Passed: `.venv/bin/python -m pytest -q tests/test_balanced_patterns.py
tests/test_structural_analysis.py` — **9 tests**, 7.60 seconds.
The new regression checks 1,250 type maps for only the two exceptional
internal graphs. It derives W from actual cuts and independently checks
compatible unbalanced containment for the union of all patterns allowed by
the surplus budget. It does not enumerate full extensions. The symbolic
proof does not rely on that finite test. `git diff --check` passed.
