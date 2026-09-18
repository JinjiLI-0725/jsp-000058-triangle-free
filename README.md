# JSP-000058 computational baseline

Finite simple undirected graphs use vertices `0,...,n-1`; isolated vertices count.
The framework computes exact MaxCut and `d(G) = |E(G)| - MaxCut(G)` with integer
arithmetic. It does not establish the general conjecture.

From the repository root (Python >=3.10; pytest required for tests):

```bash
PYTHONPATH=src .venv/bin/python -m triangle_free.search --k 1 2 --seed 58 --samples 2000 --output results/baseline
.venv/bin/python -m pytest -q
```

Use `python` instead of `.venv/bin/python` if using another environment. The core
and search use only the standard library. Install pytest with `python -m pip
install pytest` if needed.

`src/triangle_free/core.py` provides `Graph`, `is_triangle_free`,
`exact_max_cut`, `deletion_distance`, `random_triangle_free`, and `c5_blowup`.
MaxCut enumerates all `2^(n-1)` partitions for nonempty graphs, fixing vertex 0
on one side; the empty graph has one cut. Gray-code updates change one vertex
at a time. The default limit is 24 vertices; exact computation is exponential.

The search exhausts all 1,024 labeled graphs on five vertices for k=1. For k=2,
it evaluates the balanced C5 blow-up and 2,000 random greedy graphs, cycling
proposal probabilities 0.25, 0.5, 0.75, 1.0. This sampling is biased and not
exhaustive. At probability 1 the generated graphs are maximal triangle-free.
Different labelings and repeated samples are not isomorphism classes.

JSON results contain parameters, Python version, counts, the d histogram, up to
10 distinct labeled best witnesses, and every discovered bound violation.
Every witness includes the full edge list, exact MaxCut, and a maximizing cut
side (the other side is its complement). A cut witnesses the reported cut size;
its optimality relies on exhaustive enumeration. Violations are saved and cause
a nonzero CLI exit. Output filenames are deterministic and reruns overwrite
matching files; use a separate output directory to retain other experiments.
For byte-identical reproduction use the recorded Python version and unchanged
source; Python random algorithms need not be stable across versions.

Tests use independent full cut enumeration and triple-based triangle detection
on every graph through five vertices, additional ten-vertex graphs, known
examples, relabelings, disconnected graphs, generator invariants, invalid inputs,
CLI execution, and saved result witnesses. See `notes/observations.md` for the
baseline findings and limitations.

## Phase 2: canonical exhaustive search

Phase 2 additionally uses NetworkX and NumPy from `requirements.txt`. Build the
pinned nauty 2.9.3 release locally (archive SHA-256 checked, no system install):

```bash
bash tools/build_nauty.sh /tmp/jsp58-nauty
PYTHONPATH=src .venv/bin/python -m triangle_free.exhaustive --geng /tmp/jsp58-nauty/nauty2_9_3/geng --labelg /tmp/jsp58-nauty/nauty2_9_3/labelg --output results/exhaustive_k2
PYTHONPATH=src .venv/bin/python -m triangle_free.audit --nauty-dir /tmp/jsp58-nauty/nauty2_9_3 --output results/exhaustive_k2
```

Use a new output directory to rerun generation. To resume interrupted evaluation:

```bash
PYTHONPATH=src .venv/bin/python -m triangle_free.exhaustive --resume --output results/exhaustive_k2
```

`geng -t 10` covers all isomorphism classes, including disconnected graphs;
`labelg -q` supplies canonical graph6 representations. The evaluator checks each
graph with independent triple enumeration and compares the Gray-code solver
against a NumPy implementation summing edge crossings for all 1,024 partitions.
Checkpoints are atomically replaced every 1,000 evaluations and on completion.
They include all current extremizers and bind to the corpus, source, and runtime
versions. An interrupted run loses at most the last uncheckpointed batch.
Generation finishes before evaluation and is not checkpointed; it is inexpensive
at n=10. A result is marked exhaustive only after the entire generated corpus
has been evaluated. Completeness depends on nauty's generator; the audit checks
`geng 10 | pickg -T0` against the canonical corpus by exact set equality.

`graphs.g6` preserves the entire corpus; `extremizers.g6` and `result.json`
preserve every maximizing isomorphism class, without the baseline witness cap.
`generator.json` and `generation_audit.json` preserve command lines, checksums,
counts, and tool diagnostics. Canonical graph6 is specific to nauty's version
and labeling options, not a version-independent graph identifier.

Set `NAUTY_DIR` when running pytest to enable nauty integration tests:

```bash
NAUTY_DIR=/tmp/jsp58-nauty/nauty2_9_3 .venv/bin/python -m pytest -q
```

Tool source and documentation: [nauty and Traces, McKay and Piperno](https://users.cecs.anu.edu.au/~bdm/nauty/).

## Phase 2: bounded k=3 research

After completing k=2, reproduce the exploratory k=3 run with:

```bash
PYTHONPATH=src .venv/bin/python -m triangle_free.heuristic --labelg /tmp/jsp58-nauty/nauty2_9_3/labelg --seeds 58 59 60 61 --samples 500 --steps 2000 --output results/heuristic_k3
```

This evaluates fixed-base positive-weight blow-ups, random greedy graphs, and
simulated-annealing mutations of extremizers and other seeds. It is **not an
exhaustive k=3 search**. See `notes/observations.md` for constructions, acceptance
rules, and limitations. Each candidate is checked for triangles and evaluated
with exact MaxCut; all near-extremizers (d>=8) also pass the second exact solver.
The complete request log is `evaluations.jsonl`; result JSON and graph6 files
save canonical best and near-best graphs and structural measurements. Progress
checkpoints are written every 500 requests and after each seed; heuristic
resume is not implemented, so rerun deterministically into a fresh directory.

Reproduce the explicit counterexamples to stronger structural guesses with:

```bash
PYTHONPATH=src .venv/bin/python -m triangle_free.structural_checks --labelg /tmp/jsp58-nauty/nauty2_9_3/labelg --output results/structural_checks.json
```

These are counterexamples to the guesses documented in `notes/rejected_lemmas.md`,
not to JSP-000058. The phase 2 complete suite passed 59 tests with nauty enabled.
