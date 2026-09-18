# Induction checkpoint — 2026-09-18, edge-critical spanning cores

JSP-000058 and general induction lemmas A and B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: transferring a five-vertex deletion
witness from a simpler graph while respecting independently optimized cuts.

## Genuine progress — PROVED

[INDUCTION_CRITICAL_CORE.md](INDUCTION_CRITICAL_CORE.md) proves:

- Every graph G has a spanning edge-critical core C with d(C)=d(G).
  All original vertices, including isolates, remain.
- For every X, gamma_G(X)=gamma_C(X)-[d(G-X)-d(C-X)]<=gamma_C(X).
  The same five-set transfers from C to G. No transfer of the same cut,
  or separate bound on q and e, is asserted.
- A is equivalent to A_crit on triangle-free edge-critical graphs with
  d>=2k. B is equivalent to B_crit on nonbalanced such graphs with
  d>=2k-1. Smaller-d cases are automatic. B's exception is safe because
  B_k has no proper triangle-free spanning supergraph.
- Every edge of a critical graph is monochromatic in some optimal cut
  and lies on an odd cycle. Bridges and degree-one vertices are absent;
  isolates remain possible.
- A complete C5 blow-up with positive part sizes is edge-critical exactly
  when balanced. The proof accounts for cuts that split parts by random
  part rounding, rather than assuming all optimal cuts respect parts.

This is a reduction of the domain of the unproved induction lemmas. It
neither proves those lemmas nor assumes that a core is simultaneously
maximal, connected, or a complete blow-up.

## Other classifications

**FALSIFIED:** the same increment-transfer inequality for arbitrary spanning
subgraphs without d(C)=d(G). C5 plus five isolates versus a path plus five
isolates gives increments 1 and 0 for the specified common five-set.
This counterexample does not refute A, B, or JSP-000058.

**COMPUTATIONALLY VERIFIED:** all 25 saved balanced-extension JSON artifacts
were read, with complete=true and max_gap=0 throughout. They certify the
homogeneous family, not arbitrary mixed patterns or uniqueness at equality.
The t>=26 symbolic argument allows arbitrary patterns; the two scopes do
not alone establish the all-t arbitrary theorem. Subsequent proofs cover
t>=3, while mixed t=2 remains **CONJECTURAL**. This cycle's reduction uses
none of these balanced-extension claims as a premise. No enumeration was
repeated, and the t=5 empty witness was left unchanged.

**COMPUTATIONALLY VERIFIED:** bounded inference tests verify core extraction
and the exact increment identity on every five-set of five fixed 10-vertex
examples, the critical-edge/optimal-cut equivalence on all 388 labeled
triangle-free five-vertex graphs, and the critical-edge criterion on all
126 positive ordered C5 size vectors of sum 10. Independent full cuts
allow split parts. Additional checks cover the transfer counterexample
and maximality of B_1 and B_2. These do not certify A_crit/B_crit generally.

## Exact next claim and clean stopping point

**CONJECTURAL A_crit:** every triangle-free edge-critical C on 5k vertices
with d(C)>=2k has a five-set X and remainder coloring c satisfying
q(c)+e_X(c)<=2k-1. The B_crit variant excludes B_k, starts at d>=2k-1,
and requires <=2k-2. These address the same selection bottleneck.

Criticality gives edgewise optimal-cut witnesses whose monochromatic sets
cover all edges. The missing argument must coordinate these witnesses to
choose five vertices and control remainder reoptimization. Simply covering
edges with different optimal cuts does not do this. The earlier mixed t=2
subcase remains open but was not the target of this cycle.

Validation: `.venv/bin/python -m pytest -q tests/test_induction_critical_core.py
 tests/test_balanced_patterns.py tests/test_structural_analysis.py` —
**18 passed**, 26.60 seconds. Process inspection before this test job found
no existing computation. No long-running research job or random search was
launched. No potential complete solution appeared, so no POTENTIAL_PROOF.md
was warranted. State and research notes record the new reduction; existing
result artifacts and unrelated overnight log changes were left untouched.

Final `git diff --check` passed. Final process inspection found no running
compute job. This is a clean research checkpoint.
