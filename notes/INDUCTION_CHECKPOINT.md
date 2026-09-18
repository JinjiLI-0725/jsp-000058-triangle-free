# Induction checkpoint — 2026-09-18, t=3 two-cut certificates

JSP-000058 and general induction lemmas A and B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: the strict arbitrary mixed-neighborhood
balanced-extension theorem at t=3.

## Genuine progress — PROVED

Every triangle-free five-vertex extension of B_t for **t>=3** has
 d(G)<=(t+1)^2, with equality exactly for B_(t+1).
New proof and inference audit: [BALANCED_EXTENSION_T3.md](BALANCED_EXTENSION_T3.md).
The earlier occupied-type proof handles t>=4; the new argument closes t=3.

For injective maps the average refines to W-D<=m-L<=4 whenever L>=1:
six internal edges force K_(2,3), which has at least two incompatible edges.
For noninjective maps, adjacent empty types or a 2+3 split prove strictness
immediately. The remaining occupancies, up to dihedral symmetry, are
(0,2,0,1,2) and (0,3,0,1,1). A failed elementary cut forces an internal C4;
three explicit pairs of cuts have total costs at most 28,29,31. Thus one
cut costs at most 15. Their boundary bounds hold vertex by vertex and allow
arbitrary mixed patterns. Every remainder cut is optimal, so q_H=0.

The inference audit specifically avoids completing F to K_(2,3) and then
restricting old boundary patterns by the added edges. In the first exception,
only the forced C4 constrains those patterns; internal attachments are paid
for separately. In the second exception, F itself is forced to be K_(2,3).
The compatible injective branch classifies equality by a missing-edge cut.

## Classifications and coverage

- **PROVED:** strict arbitrary balanced extensions for all t>=3.
- **COMPUTATIONALLY VERIFIED:** all saved homogeneous t=1,...,25 artifacts
  were read and are complete with max_gap=0. No enumeration was repeated.
  Their witness metadata does not classify equality; the documented empty
  t=5 witness remains unchanged.
- **COMPUTATIONALLY VERIFIED:** arbitrary t=1 and equality from the separate
  exhaustive n=10 corpus; new bounded checks of the proof ingredients.
- **FALSIFIED:** the earlier homogeneous spanning-supergraph coverage claim.
  No new lemma was falsified this cycle.
- **CONJECTURAL:** strict arbitrary mixed t=2; general A/B; JSP-000058.

Before using balanced-remainder results, the different scopes of the t<=25
homogeneous certification and t>=26 arbitrary symbolic proof were verified.
They do not by themselves establish the arbitrary all-t theorem. The newer
symbolic arguments now leave only t=2 of that mixed gap.

## Induction consequence and exact remaining obstruction

For k>=4, every X with G-X=B_(k-1) satisfies A and, for nonbalanced G, B.
By B_inherit, A plus equality uniqueness through k=3 would imply uniqueness
at all orders. Neither general A nor that finite equality base is established.
For arbitrary remainders, finding X,c with q_H(c)+e_X(c)<=2k-1 (or <=2k-2
for B) remains unresolved. This theorem does not select X there.

The next precise claim on the same bottleneck is strict arbitrary extension
of B_2 by five vertices. Do not replace mixed patterns by a homogeneous
supergraph or use max_gap=0 to infer uniqueness. No potential complete
solution of JSP-000058 appeared.

## Validation and clean stopping point

The targeted regressions check occupancy reduction on 625 normalized maps,
the injective inequality and forced E2 shape on all 388 labeled triangle-free
five-vertex graphs, and the three pair certificates on every permitted
independent pattern and internal attachment. Mixtures follow by summing
these per-vertex bounds. These are ingredient tests, not extension enumeration.

A first run passed the certificate test but found a normalization mismatch
in a test assertion: maps normalized by f(0)=0 cannot have n_0=0. The assertion
was corrected to compare with the occupied-type-0 subset of the orbit; no
mathematical statement or certificate changed. Final test results follow.

Exploratory finite checks used only two exceptional type maps, five-vertex
internal graphs, and pairs of cuts to find the certificates. Every job
finished before the next compute job; process inspections found no existing
compute job. No broad random search or balanced-extension rerun was launched.
Saved result artifacts and pre-existing log changes were left untouched.

Final validation: `.venv/bin/python -m pytest -q tests/test_balanced_patterns.py
 tests/test_structural_analysis.py` — **14 passed**, 13.39 seconds.
`git diff --check` passed. No research compute job remains running.
This is a clean checkpoint; state/current_state.json records the new threshold.
