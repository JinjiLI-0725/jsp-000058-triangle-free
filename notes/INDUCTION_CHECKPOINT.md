# Induction checkpoint — 2026-09-18, coverage audit

JSP-000058 and general induction lemmas A and B remain **CONJECTURAL**.
Clean stopping point: no new exhaustive enumeration was launched.

Read [BALANCED_EXTENSION_AUDIT.md](BALANCED_EXTENSION_AUDIT.md) before using
any historical balanced-extension coverage claim in INDUCTION_ROUTE.md.

## Single bottleneck selected this cycle

Does the completed homogeneous-neighborhood enumeration cover arbitrary
five-vertex extensions of B_t? The proposed spanning-supergraph reduction
is **FALSIFIED**, with an explicit triangle-free mixed-neighborhood example.
This is a coverage correction, not a counterexample to the conjectured bound.

## What is established

- **COMPUTATIONALLY VERIFIED:** ALL t=1,...,25 runs are complete and have
  max_gap=0, each with 242,500 configurations and 1,245,367 maximal choices.
  The artifacts were read, not recomputed. Their scope is homogeneous
  neighborhoods within each of the five remainder parts.
- **PROVED:** the existing t>=26 strict balanced-remainder theorem survives
  the audit and applies to arbitrary neighborhoods.
- **PROVED:** arbitrary extensions have a mixed-pattern count representation
  and exact sorted-unary cut formula (M), including nonoptimal remainder cuts.
- **PROVED:** per-vertex maximal independent-pattern completion is valid.
  Completing all vertices of a part to one common pattern need not be possible.
- t=1 has no mixed-pattern gap. For 2<=t<=25 the general balanced-remainder
  bound remains **CONJECTURAL** despite the completed homogeneous runs.
- The files recording only max_gap and one witness do not classify every
  equality case. They cannot by themselves establish B's strict transition.

## Next action

Prove the precise mixed-pattern inequality M in BALANCED_EXTENSION_AUDIT.md,
or falsify a proposed numerical homogenization lemma. Do not repeat any of
the completed t runs. General A/B still face the exact q+e obstruction in
INDUCTION_ROUTE.md; this audit does not claim to solve it.

## Validation

Passed: `.venv/bin/python -m pytest -q tests/test_balanced_patterns.py
tests/test_structural_analysis.py` — **6 tests**, 4.21 seconds.
`git diff --check` passed. No completed enumeration was repeated; no
long-running research job was started. Existing overnight logs were left
untouched.
