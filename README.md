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
