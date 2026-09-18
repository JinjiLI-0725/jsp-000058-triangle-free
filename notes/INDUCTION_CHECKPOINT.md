# Induction checkpoint — 2026-09-18, t=6 bounded repair

JSP-000058 and general induction lemmas A and B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: the strict arbitrary mixed-neighborhood
extension of B_6, within the balanced-remainder transition of A/B_inherit.

## Genuine progress — PROVED

Every triangle-free five-vertex extension of B_6 has d<=49, with equality
exactly for B_7. Together with the earlier t>=7 proof, the arbitrary strict
balanced-extension theorem now holds for **all t>=6**.
Full proof and inference audit: [BALANCED_EXTENSION_T6.md](BALANCED_EXTENSION_T6.md).

The five-cut average handles W-D<=4. In the remaining cases D>=6L and
s=D-6L<=W-6L-5. Only K_(1,4), C4 with a pendant vertex, and K_(2,3)
can occur internally. The exact surplus identity bounds the boundary edges
that must be removed before a compatible retyping. At most one edge is
needed for the star, zero for the five-edge shape, and two for K_(2,3).
The containing blow-up has two adjacent parts of size six, hence d=36.
Restoring the removed edges costs at most their number, proving strictness.

The new repair step handles the case missed by zero-surplus reasoning:
a K_(2,3) pattern containing both centers loses only one unit from maximum
cardinality but contributes two boundary edges. Both are explicitly paid for.

## Exact scope and classifications

- **COMPUTATIONALLY VERIFIED:** all saved t=1,...,25 certificates are
  complete with max_gap=0, covering homogeneous neighborhoods only. All were
  read; no enumeration was repeated. A maximizing witness alone does not
  classify equality, and t=5 has the previously documented missing witness.
- **FALSIFIED (previous cycle):** homogeneous spanning-supergraph coverage
  of arbitrary mixed neighborhoods. No such reduction is used.
- **PROVED:** arbitrary balanced extensions at t>=6, including strictness.
- **COMPUTATIONALLY VERIFIED:** arbitrary t=1 and equality classification
  from the separately saved exhaustive n=10 result.
- **CONJECTURAL:** arbitrary mixed t=2,...,5, general A, general B, and
  JSP-000058. No new candidate was falsified this cycle.

The original t<=25 homogeneous certification and t>=26 arbitrary symbolic
argument were checked before use: their different coverage leaves a mixed
finite gap. The newer symbolic proofs reduce that gap, not the enumeration.

## Induction consequence and exact obstruction

For k>=7, every X with G-X=B_(k-1) satisfies A and, for nonbalanced G, B.
By B_inherit, A plus equality uniqueness through k=6 would imply uniqueness
at all orders. Neither A nor that finite equality base is established.
For arbitrary remainders the exact obstruction remains finding X,c with
q_H(c)+e_X(c)<=2k-1 (or <=2k-2 for B). The proof uses actual cuts and
explicit repair costs, not an incorrect reversal of a restriction bound.

## Validation and clean stopping point

Passed: `.venv/bin/python -m pytest -q tests/test_balanced_patterns.py
 tests/test_structural_analysis.py` — **10 tests**, 10.70 seconds.
The new regression checks 1,875 normalized type maps for the three exceptional
shapes. A small loss-budget dynamic program bounds all permitted mixed and
nonmaximal individual patterns, without enumerating full extensions. This
is **COMPUTATIONALLY VERIFIED** checking of proof ingredients; the theorem
is symbolic and independent of it. `git diff --check` passed.

Process inspection before testing found no other compute job. No long-running
research computation or broad random search was launched. Completed result
artifacts and pre-existing overnight log changes were left untouched.

Next action on the same bottleneck: prove the strict mixed extension theorem
for t=2,...,5. At t=5 the condition is W-D>=5 with D>=5L; the t=6 shape
classification must not be assumed exhaustive. No potential complete solution
appeared. This is a clean checkpoint.
