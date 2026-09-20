# Existential core-penalty-one audit: counterexample

The fixed-X assertion

    min_t (t + F_X(t)) = min(F_X(0), 1 + F_X(1))

is **false** in the requested n=15 corpus. No local-descent lemma is used.
This does not refute the possibility that each graph has some other suitable
five-set satisfying the assertion, and does not refute Candidate A.

The audit followed the requested order, with five-sets in lexicographic order:

1. Known d=8 A-tight witness, graph6 `NEL_FF_DgAeOATbBPp?`: all 3003 passed.
2. B3, the balanced C5 blow-up with parts of size 3: all 3003 passed.
3. Non-balanced class 1: first failure at five-set 282 (one-based).

It stopped at this failure. Classes 2--22 and the remaining five-sets of class 1
were not audited. Total five-sets checked: 6288.

## Exact counterexample to the fixed-X identity

Graph6: `N????KEWOprqxa}W^K?`.

Vertex labels are zero-based, as decoded directly from this graph6 string.

    X = {0, 1, 10, 13, 14}
    H = G-X
    d(G) = 7
    d(H) = 1
    q(X) = 6

| t | F_X(t) | t+F_X(t) |
|---:|---:|---:|
| 0 | 7 | 7 |
| 1 | 6 | 7 |
| 2 | 4 | 6 |
| 3 | 3 | 6 |
| 4 | 2 | 6 |
| 5 | 2 | 7 |
| 6 | 3 | 9 |
| 7 | 3 | 10 |
| 8 | 3 | 11 |
| 9 | 4 | 13 |
| 10 | 3 | 13 |
| 11 | 6 | 17 |
| 12 | 7 | 19 |
| 13 | 4 | 17 |

These are all feasible penalties. The minimizing penalties are exactly
`{2, 3, 4}`. Consequently the unrestricted minimum is 6 and the t<=1 minimum
is 7. The eight earlier slack-4 examples still satisfy their reported equality;
this is a different five-set in one of the same graph classes.

## Method and artifacts

`scripts/audit_existential_core_band.cpp` enumerates all 16384 full-graph cuts
modulo global reversal once per graph. For each five-set it counts core and
incident monochromatic edges for every full cut. Grouping the incident costs by
core monochromatic count yields the entire F profile, including its low-band
minimum. Global reversal preserves all relevant counts, even when vertex 0
belongs to X, so this enumeration covers every core/extension possibility.

At the first failure, `scripts/audit_existential_core_band.py` independently
enumerates all 512 core cuts modulo reversal and all 32 assignments on X using
direct Python edge counts. It recomputes d(G) and d(H) with the reference solver
and verifies every F entry, all minimizing penalties, and the strict inequality.
This reference check completed successfully.

The result, input hashes, complete cut witnesses for each F entry, and progress
are saved under `results/existential_core_band_n15/`. `result.json` is complete
for the requested stop-on-first-failure audit. There is no unfinished job from
this audit and no further corpus search is needed to answer this question.

To reproduce later, use a fresh output directory:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python \
  scripts/audit_existential_core_band.py \
  --output results/existential_core_band_n15_recheck
```

No broad random search was run. PID 3132683 and
`results/candidate_A_n20_large` were not modified.
