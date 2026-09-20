# Uniform core-penalty cutoff audit: T=2,3,4 all fail

The completed fixed-corpus audit found **no surviving cutoff in {2,3,4}**.
Each cutoff was tested from the start of the prescribed corpus and stopped
immediately at its first counterexample. No random search or proof attempt was
performed. The protected n=20 process and results directory were not modified.

Order: the known d=8 A-tight witness (`NEL_FF_DgAeOATbBPp?`), B3, then the 22
representatives in `results/induction_B_tight_nonbalanced_reps.g6`, in file order.
Five-sets are tested in lexicographic order with zero-based vertex labels.
Both the d=8 witness and B3 pass all 3003 five-sets at every tested cutoff.

| Cutoff | First failing class | Five-set index in that graph (1-based) | Completed graphs | Total five-sets checked |
|---:|---:|---:|---:|---:|
| 2 | non-balanced 1 | 819 | 2 | 6825 |
| 3 | non-balanced 5 | 1821 | 6 | 19839 |
| 4 | non-balanced 10 | 1233 | 11 | 34266 |

Later five-sets/classes were not evaluated for that cutoff after its failure.

## First counterexamples

For each counterexample, d(G)=7, d(H)=0, q=d(G)-d(H)=7, and the minimum of
t+F_X(t) over 0<=t<=T is 8. The unrestricted minimum is 7.

| T | graph6 | X | All minimizing t |
|---:|---|---|---|
| 2 | `N????KEWOprqxa}W^K?` | {0,5,6,13,14} | {3,4,5} |
| 3 | `N@GU_?NxOq[DHosGzG?` | {2,3,6,11,13} | {4,5} |
| 4 | `NDz?pL_SCDCbFA_[bK_` | {1,3,4,6,9} | {6} |

The complete F profiles follow. Infinity denotes an unattained core penalty.
Every penalty above the table's range is also unattained.

| t | F for T=2 counterexample | F for T=3 counterexample | F for T=4 counterexample |
|---:|---:|---:|---:|
| 0 | 11 | 9 | 8 |
| 1 | 7 | infinity | infinity |
| 2 | 9 | 6 | infinity |
| 3 | 4 | 5 | 6 |
| 4 | 3 | 3 | 7 |
| 5 | 2 | 2 | 5 |
| 6 | 4 | 2 | 1 |
| 7 | 3 | 3 | 3 |
| 8 | 2 | 2 | 2 |
| 9 | 6 | 3 | 3 |
| 10 | 3 | 3 | 3 |
| 11 | 4 | 3 | 5 |
| 12 | 6 | 3 | 3 |
| 13 | 2 | 4 | 6 |
| 14 | infinity | infinity | 4 |
| 15 | infinity | 4 | 7 |
| 16 | infinity | infinity | infinity |
| 17 | infinity | infinity | infinity |
| 18 | infinity | infinity | 5 |

The last example also directly excludes T=5 for this fixed pair: the only
minimizing penalty is 6. No T=5 or T=6 corpus audit was launched, and no claim
that T=6 survives the corpus is made. These examples refute fixed-X cutoff
identities; they do not refute Candidate A or selection of another X.

## Exact validation and preserved artifacts

For each graph, the C++ audit enumerates all 16384 full cuts modulo reversal.
For each X, it groups incident monochromatic cost by core monochromatic count,
obtaining every feasible F(t), d(H), q, and all minimizing penalties. It checks
that min_t(t+F(t)) equals independently enumerated d(G) minus d(H).

Every first counterexample is separately verified in Python using all 512 core
cuts modulo reversal, each with all 32 assignments on X. Direct edge counting
reproduced every F entry. The reference deletion-distance solver reproduced
d(G) and d(H). All three independent verifications passed.

Sources: `scripts/audit_uniform_core_cutoff.cpp` and
`scripts/audit_uniform_core_cutoff.py`. The Python driver reuses the independent
reference routine from `scripts/audit_existential_core_band.py`.

Results: `results/uniform_core_cutoff_n15/summary.json`, per-cutoff
`T2_result.json`, `T3_result.json`, `T4_result.json`, and progress JSONL files.
The manifest records corpus order and source/input hashes. Counterexample
records contain a full-cut bitmask attaining every F entry; bit v is vertex v's
side. No audit job remains unfinished.

Reproduction, using a fresh output directory:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -u \
  scripts/audit_uniform_core_cutoff.py \
  --output results/uniform_core_cutoff_n15_recheck
```
