# Corrected fixed n=15 selection audit

The previous selection-audit pass is invalid evidence. This report uses a fresh run of a corrected auditor; it does not reuse previous pass records.

The audited family is exactly independent induced subgraphs, complete bipartite induced subgraphs with two nonempty sides, and complements in H. Complements are explicitly permitted in section B of `notes/COORDINATED_FLIP_SELECTION.md`. General bipartite induced subgraphs are not included unless their complements qualify.

For every X, the auditor computes U = min over optimal core colorings c of the average over all optimal assignments a on X of min over allowed S of [b_G(c^S union a)-d(H)]. Thus M=5-U, exactly the margin in the selection note. Core reversal is quotiented in the audit; assignments include both orientations. The allowed family is closed under complementation.

Margins use integer numerator/denominator pairs. The C++ maximum uses cross-multiplication, and the reporting driver uses Python Fraction. All vertex labels below are zero-based; witness files translate local core masks to original labels.

Completed: **24 graphs, 72072 five-sets**; exactly 3,003 distinct five-sets per completed graph. The fixed input has 24 distinct labeled graphs: the d=8 witness, B3, and 22 supplied non-balanced d=7 canonical representatives. Canonical completeness outside the supplied file is not claimed.

| Graph | Max M | First maximizing X | Smallest positive M | Closest negative M | Pass |
|---|---:|---|---:|---:|---|
| d8_A_tight | 0 | [0, 1, 2, 6, 8] | none | -1/4 | yes |
| B3 | 0 | [0, 3, 6, 9, 12] | none | -2 | yes |
| nonbalanced_1 | 1 | [0, 1, 2, 12, 13] | 1/2 | -1/5 | yes |
| nonbalanced_2 | 1 | [0, 1, 2, 5, 6] | 1/4 | -1/5 | yes |
| nonbalanced_3 | 1 | [0, 1, 2, 3, 9] | 1/5 | -1/5 | yes |
| nonbalanced_4 | 1 | [0, 1, 2, 4, 8] | 1/8 | -1/8 | yes |
| nonbalanced_5 | 1 | [0, 1, 4, 6, 9] | 1/5 | -1/4 | yes |
| nonbalanced_6 | 1 | [0, 1, 3, 4, 8] | 1/8 | -1/5 | yes |
| nonbalanced_7 | 1 | [0, 1, 3, 4, 8] | 1/8 | -1/5 | yes |
| nonbalanced_8 | 1 | [0, 1, 2, 3, 6] | 1/4 | -1/8 | yes |
| nonbalanced_9 | 1 | [0, 1, 2, 3, 8] | 1/5 | -1/5 | yes |
| nonbalanced_10 | 1 | [0, 1, 2, 3, 5] | 2/5 | -1/4 | yes |
| nonbalanced_11 | 1 | [0, 1, 2, 5, 14] | 1/4 | -1/2 | yes |
| nonbalanced_12 | 1 | [0, 1, 2, 3, 4] | 1/2 | -1/5 | yes |
| nonbalanced_13 | 1 | [0, 1, 2, 4, 5] | 2/5 | -1/8 | yes |
| nonbalanced_14 | 1 | [0, 1, 2, 5, 7] | 1/4 | -1/5 | yes |
| nonbalanced_15 | 1 | [0, 1, 2, 3, 4] | 1/5 | -1/5 | yes |
| nonbalanced_16 | 1 | [0, 1, 2, 3, 5] | 1/4 | -1/8 | yes |
| nonbalanced_17 | 1 | [0, 1, 2, 3, 10] | 1/5 | -1/8 | yes |
| nonbalanced_18 | 1 | [0, 1, 2, 4, 5] | 1/5 | -1/4 | yes |
| nonbalanced_19 | 1 | [0, 1, 2, 4, 13] | 1/4 | -1/5 | yes |
| nonbalanced_20 | 1 | [0, 1, 2, 4, 9] | 1/4 | -1/4 | yes |
| nonbalanced_21 | 1 | [0, 1, 2, 3, 4] | 1/8 | -1/8 | yes |
| nonbalanced_22 | 1 | [0, 1, 2, 4, 9] | 1/5 | -1/8 | yes |

B3: all 243 transversals have margin exactly 0.

First counterexample: none in the completed fixed corpus.

Regression tests reject P4, 2K2, an edge plus an isolated vertex, and a triangle as primitive shapes; accept independent sets and K(2,3); and distinguish an invalid shape with an allowed complement from a set with neither side allowed. A separate partition-enumeration predicate agrees for all 32 subsets of all 1,024 labeled five-vertex graphs (32,768 checks). Rational tests cover positive, negative, and tied fractions with unequal denominators, including 2/2 > 8/10.

Independent verification uses NetworkX connected bipartiteness plus the complete edge-count condition, and enumerates full-graph coloring costs directly in original labels. For each graph it checks a maximum-margin witness, the smallest positive and closest negative witnesses when present, and a minimum-margin witness, including both orientations of every optimal core coloring. It records every maximizing allowed flip for each optimal X assignment at the chosen base coloring. This is independent witness verification, not a second independent exhaustive audit of every X.

Artifacts: `all_X.tsv` contains every margin and selected base coloring; `summary.json` contains graph6 strings, all maximizing X, exact extrema, and input/source hashes; `independent_witnesses.json` contains original-label colorings and all assignment-wise maximizing flip sets for the selected extrema. `manifest.json` hashes all sources, tests, relevant notes, binaries, and output files, including this report.

Reproduce in a fresh output directory (the driver refuses existing directories):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python scripts/audit_selection_exact.py --output results/selection_exact_reproduction
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/verify_selection_exact.py results/selection_exact_reproduction
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/report_selection_exact.py results/selection_exact_reproduction --report notes/SELECTION_AUDIT_REPRODUCTION.md
```

Scope: this is an exhaustive audit of the specified fixed corpus only. It proves neither the universal structural selection conjecture nor Candidate A. No random search or further proof attempt was made. The protected PID 3132683 and results/candidate_A_n20_large were not modified.
