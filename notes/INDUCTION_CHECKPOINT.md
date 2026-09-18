# Induction checkpoint — 2026-09-18, full-cut slack obstruction

JSP-000058 and general induction lemmas A and B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: whether the optimal full-graph cuts
of an edge-critical core suffice to determine five-vertex deletion cost.
The answer is no. See [INDUCTION_CUT_SLACK.md](INDUCTION_CUT_SLACK.md).

## Genuine progress — PROVED

For any graph and any vertex set X,

    gamma_G(X)=max_c(r_X(c)-s(c)),

where r_X(c) counts monochromatic edges incident with X, once each, and
s(c)=b_G(c)-d(G). Equality with the maximum restricted to optimal cuts
holds exactly when some optimal full-graph cut restricts optimally to G-X.
This is an exact reformulation of the existing q+e obstruction, not a
solution of it. A slack cutoff excluding cuts that cannot beat the
optimal-cut lower bound is also proved in the note.

## Candidate O — FALSIFIED

Let G_s be Petersen disjoint-union B_s, s>=3. Delete the four Petersen
vertices {0,1,3,8} in the note's explicit labeling and one B_s vertex.
The true increment is s+3, but the maximum incident monochromatic count
over optimal cuts is s+2. A cut of slack one realizes the missing unit.
The note proves the complete optimal-cut classification of Petersen
combinatorially, and proves this infinite family is triangle-free,
edge-critical, and in the nonautomatic domain of both A_crit and B_crit.

This refutes the proposed optimal-full-cut-only equality. It does not
refute A/B: the displayed five-set satisfies B. It does not rule out a
special choice of X admitting compatible optima, or a connected-core
version of the rejected claim. No complete solution appeared.

## COMPUTATIONALLY VERIFIED

Independent enumeration of the 512 Petersen cuts checks its five optimal
monochromatic triples, criticality and the slack-one witness. On all 638
vertex sets of size at most five, the new identity, compatibility criterion
and slack cutoff agree with independently optimized Gray-code remainder
cuts. Separate B_3 cut enumeration validates the order-25 component
certificate; no full order-25 cut enumeration is needed or claimed.

All completed t=1,...,25 artifacts were read, with complete=true and
max_gap=0. The saved runs certify homogeneous patterns. Together with
the original arbitrary t>=26 theorem they do not prove the all-t arbitrary
extension theorem. Later symbolic proofs cover arbitrary t>=3; mixed t=2
remains **CONJECTURAL**. This cycle uses none of these extension results
as a premise. No extension enumeration was repeated; result files,
including the t=5 empty witness, were left unchanged.

## Exact next claim and clean stopping point

The single remaining target is to choose X on a nonautomatic critical
core such that r_X(c)<=T+s(c) for every coloring c, with T=2k-1 for A,
or T=2k-2 for nonbalanced B. Edgewise optimal-cut coverage cannot justify
ignoring positive-slack colorings. Any further argument using this family
of cuts must control those layers or prove an additional compatibility
condition. This target remains **CONJECTURAL**.

Validation: `.venv/bin/python -m pytest -q tests/test_induction_cut_slack.py
 tests/test_induction_critical_core.py tests/test_balanced_patterns.py
 tests/test_structural_analysis.py` — **21 passed**, 40.80 seconds.
Process inspection before computation found no existing compute job.
Only bounded checks of the specified missing claim and regression tests
ran; no broad random search or long-running research job was launched.
The preceding critical-core reduction is preserved in
[INDUCTION_CRITICAL_CORE.md](INDUCTION_CRITICAL_CORE.md).
Notes and state record the progress. Unrelated overnight log changes were
left untouched. Final `git diff --check` passed; final process inspection
found no running compute job. This is a clean research checkpoint.
