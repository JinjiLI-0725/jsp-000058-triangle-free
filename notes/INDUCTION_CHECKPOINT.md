# Induction checkpoint — 2026-09-18, symbolic vertex-cover progress

JSP-000058 and general induction lemmas A and B remain **CONJECTURAL**.
Single bottleneck this cycle: arbitrary mixed-neighborhood extensions of a
balanced remainder, including the strict transition needed by B_inherit.

## Genuine progress

**PROVED:** every triangle-free five-vertex extension of B_t, for t>=8,
satisfies d(G)<=(t+1)^2, with equality exactly for B_(t+1).
Read [BALANCED_EXTENSION_COVER_BOUND.md](BALANCED_EXTENSION_COVER_BOUND.md)
for the full first-principles proof and attempts to falsify its inferences.
This improves the previous symbolic t>=26 theorem without enumeration.

The new identity is W=m+2 sum_j e(F[S_j]). A minimum vertex cover gives
 e(F[S_j])<=Delta(F) tau(F[S_j]). For m<=4 use Delta<=4; for 5<=m<=6
triangle-freeness forces Delta<=3. With L=sum_j tau(F[S_j])>=1 this gives
W<=8L+4. The arbitrary-neighborhood deficit satisfies D>=tL, so one of
five explicit cuts has extension cost at most 2t for t>=8. The compatible
type case is handled by the existing blow-up formula and strictness proof.

## Exact scope and classifications

- **COMPUTATIONALLY VERIFIED:** all saved t=1,...,25 runs are complete,
  have max_gap=0, and cover homogeneous neighborhoods. All artifacts were
  read; no enumeration was repeated.
- **FALSIFIED (previous cycle):** homogeneous spanning-supergraph coverage
  of arbitrary mixed neighborhoods. The new proof does not use it.
- **PROVED:** arbitrary extensions at t>=8, including strictness.
- **COMPUTATIONALLY VERIFIED:** the arbitrary t=1 case and equality
  classification, from the separately saved exhaustive n=10 result.
- **CONJECTURAL:** mixed t=2,...,7, general A, general B, and JSP-000058.

For k>=9, any X with G-X=B_(k-1) satisfies A, and B if G is nonbalanced.
A plus equality uniqueness through k=8 would imply uniqueness at every
order. Neither that finite base nor A is proved here. For arbitrary
remainders the exact min_c(q_H(c)+e_X(c)) obstruction remains unchanged.

## Next action and clean stopping point

Prove the mixed-pattern inequality M for 2<=t<=7, with strictness for
nonbalanced graphs. The four-leaf star with types (0,2,2,2,2) has W=12,
L=1, so W-tL<=4 fails at t=7; extending the same average estimate alone
cannot close the gap. This does not falsify the actual extension bound.

No long-running research computation was launched. The process check showed
no existing compute job. Existing overnight logs were left untouched.

## Validation

Passed: `.venv/bin/python -m pytest -q tests/test_balanced_patterns.py
tests/test_structural_analysis.py` — **8 tests**, 7.61 seconds.
New checks independently verify type-overlap multiplicities from actual
five-cycle cuts, the cover inequality on every induced subset of all 388
triangle-free five-vertex graphs, and the t=7 limitation. Existing tests
check mixed cut identities, saved artifacts, and structural formulas.
`git diff --check` passed.
