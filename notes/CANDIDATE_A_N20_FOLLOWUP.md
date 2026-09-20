# Candidate A, n=20: isolated follow-up tools

The existing `scripts/search_candidate_A_n20.py` and its shared library are
unchanged. Nothing here attaches to, signals, restarts, or changes PID 3132683.
The tools refuse output inside `results/candidate_A_n20_large`, including paths
that resolve there through symlinks. Use a separate fresh directory for outputs.

## Review of the existing pipeline

`d(G)=|E(G)|-MaxCut(G)` is computed exactly. At n=20 the driver uses the existing
C++ Gray-code cut enumerator; its 15-vertex cores use the NumPy full-partition
oracle. The sampled M15 is a lower bound on M15, so `d-sampled_M15` is an **upper**
bound on Delta5. An estimated gap of 7 certifies Delta5 <= 7, not equality.
Records marked `d_too_small` have `estimated_gap=d` and no sampled M15; extraction
must include these when their logged estimate is 7.

Screens 2 and 3 repeat earlier subsets, and the failure check starts over again.
The failure check can exit on a single core with d(H)>=d(G)-7; such a check does
not determine exact M15. Only exhaustion of all 15504 deletions justifies the
existing A_FAILURE output. `full_verifications` counts attempts, including early
refutations. The cache is by labeled edge set, not isomorphism class. Histograms
count requests, including duplicates. The pool and current state influence later
search, and replay must restore random draws, not merely reload the best graphs.
The existing log is flushed only every 100 requests and has no resume support.

## Future searches: checkpoint and resume

```bash
PYTHONPATH=src .venv/bin/python scripts/search_candidate_A_n20_resumable.py \
  --output results/candidate_A_n20_resumable --seeds 801 --samples 250 --steps 2000
# Repeat exactly the same arguments, adding --resume:
PYTHONPATH=src .venv/bin/python scripts/search_candidate_A_n20_resumable.py \
  --output results/candidate_A_n20_resumable --seeds 801 --samples 250 --steps 2000 --resume
```

This new driver wraps the unchanged original search. Every completed evaluation
is flushed and fsynced; an atomic checkpoint describes committed progress. The
journal itself is authoritative if interruption occurs between journal and
checkpoint writes. Resume replays deterministic graph generation and acceptance
decisions, restores cache/counters/pool/RNG trajectory, and skips completed cut
calculations. It rejects different arguments, Python versions, or dependency
hashes. It discards only an unterminated final journal line and fails on interior
corruption or trajectory disagreement. A directory lock rejects concurrent use.

Replay takes time linear in prior search steps. An interrupted evaluation is
recomputed. This does not retrofit resume into the active legacy job, nor import
an arbitrary legacy log. Run this driver only for a future separate search.

## Post-run analysis

```bash
bash scripts/postrun_candidate_A_n20.sh
# If interrupted:
bash scripts/postrun_candidate_A_n20.sh \
  results/candidate_A_n20_large results/candidate_A_n20_postrun --resume
# To analyze the smoke corpus separately:
bash scripts/postrun_candidate_A_n20.sh \
  results/candidate_A_n20_smoke results/candidate_A_n20_smoke_postrun
```

The wrapper runs one process at lowered CPU priority. Input is read only; a
snapshot of complete JSONL records is written to the separate output directory.
For a growing input, this is only the prefix visible at snapshot time. Resume
uses that immutable snapshot; use a new output directory to analyze a later one.
The tool requires the existing `scripts/libmaxcut_fast.so` and nauty's `labelg`
(default `/usr/bin/nauty-labelg` when installed; `--labelg` accepts another path).

Extraction retains all distinct labeled graphs with estimated gap >=7 and all
sources/request indices; `estimated_gap7.g6` contains exactly the gap-7 subset.
Including estimates above 7 ensures that potential failures are also audited.
Nauty canonicalizes every selected graph, and NetworkX checks each input/output
pair for isomorphism. One representative per class is verified over **all 15504
five-vertex deletions with no early exit**. Exact invariance under the checked
isomorphisms transfers the result to every listed member. All deletion witnesses
and vertex labels in verification/structure outputs refer to the canonical graph.

The compiled cut oracle is used for all cores, with a bounded cache reusing exact
values for identical labeled cores. Every deletion is still enumerated and counted.
Each graph's full cut is checked
against the Python reference implementation, and the first core is checked
against the independent NumPy full-partition implementation. Checkpoints save the
next deletion position, M15, histogram and maximizing-set statistics every 256
cores. Resume requires matching snapshot and toolchain hashes. Completed classes
are reused from their checkpoints.

Outputs:

- `manifest.json`, `input_snapshot.jsonl`: scope, input hash, toolchain hashes.
- `extracted.json`, `estimated_gap7.g6`: full extraction and provenance.
- `verify_<sha256>.json`: resumable exhaustive deletion computations.
- `verified.json`: exact d, M15, Delta5 and all labeled members per class.
- `tight_classes.json`: exact Delta5=7 classes and structural measurements.
- `exact_failures.json`: only classes with Delta5>=8 after all 15504 checks.
- `summary.json`: concise counts and explicit heuristic-coverage limitation.

Tight-class analysis records degree sequence, components, vertex connectivity,
independence number, maximal triangle-freeness, false-twin classes and quotient,
C5 blow-up/B4 recognition, and a maximum-cut witness. Exhaustive verification
also records the full core-distance histogram, one maximizing deletion, number
of maximizing deletions, their vertex incidence and induced-edge distribution.
These describe tight classes found in this corpus; they are not a classification
of every possible tight triangle-free graph on 20 vertices.

No negative heuristic search result proves Candidate A. A counterexample claim
requires a triangle-free graph and exact Delta5>=8 from all 15504 deletions.
