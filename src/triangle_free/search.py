"""Reproducible baseline: exhaustive k=1, seeded greedy samples for k=2."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import platform
import random
import sys

from .core import Graph, c5_blowup, exact_max_cut, is_triangle_free, random_triangle_free


def all_labeled_graphs(n):
    pairs = tuple(combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        yield Graph(n, tuple(edge for i, edge in enumerate(pairs) if mask & (1 << i)))


def search(k: int, *, seed: int = 58, samples: int = 2000) -> dict:
    if k not in (1, 2):
        raise ValueError("baseline supports only k=1 and k=2")
    if type(samples) is not int or samples < 0:
        raise ValueError("samples must be a nonnegative integer")
    rng = random.Random(seed)
    probabilities = (0.25, 0.5, 0.75, 1.0)
    if k == 1:
        candidates = (("exhaustive", graph) for graph in all_labeled_graphs(5))
    else:
        def sampled():
            yield "balanced_C5_blowup", c5_blowup(k)
            for index in range(samples):
                p = probabilities[index % len(probabilities)]
                yield f"random_greedy_p={p}", random_triangle_free(5 * k, rng, edge_probability=p)
        candidates = sampled()
    considered = examined = 0
    unique = set()
    histogram = Counter()
    best = -1
    witnesses = []
    violations = []
    for index, (source, graph) in enumerate(candidates):
        considered += 1
        if not is_triangle_free(graph):
            if k == 2:
                raise RuntimeError("triangle-free generator produced a triangle")
            continue
        examined += 1
        unique.add(graph.edges)
        cut = exact_max_cut(graph)
        d = len(graph.edges) - cut.value
        histogram[d] += 1
        record = {"candidate_index": index, "source": source, "n": graph.n,
                  "edges": [list(edge) for edge in graph.edges], "m": len(graph.edges),
                  "max_cut": cut.value, "cut_side": list(cut.side), "d": d,
                  "cuts_examined": cut.cuts_examined}
        if d > k * k:
            violations.append(record)
        if d > best:
            best, witnesses = d, [record]
        elif d == best and len(witnesses) < 10 and not any(w["edges"] == record["edges"] for w in witnesses):
            witnesses.append(record)
    return {"schema_version": 1, "k": k, "n": 5 * k, "target_bound": k * k,
            "strategy": "exhaustive_labeled" if k == 1 else "C5_blowup_plus_random_greedy",
            "seed": seed, "random_samples": 0 if k == 1 else samples,
            "edge_probability_schedule": [] if k == 1 else list(probabilities),
            "candidates_considered": considered, "triangle_free_evaluations": examined,
            "unique_labeled_graphs_evaluated": len(unique),
            "d_histogram": {str(d): histogram[d] for d in sorted(histogram)},
            "best_d": best, "best_witnesses": witnesses, "bound_violations": violations,
            "scope": "Computational evidence only; random sampling is not exhaustive or uniform. No general proof.",
            "python_version": platform.python_version()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, choices=(1, 2), nargs="+", default=[1, 2])
    parser.add_argument("--seed", type=int, default=58)
    parser.add_argument("--samples", type=int, default=2000)
    parser.add_argument("--output", type=Path, default=Path("results/baseline"))
    args = parser.parse_args()
    if args.samples < 0:
        parser.error("--samples must be nonnegative")
    args.output.mkdir(parents=True, exist_ok=True)
    violation = False
    for k in args.k:
        result = search(k, seed=args.seed, samples=args.samples)
        path = args.output / f"k{k}_seed{args.seed}.json"
        path.write_text(json.dumps(result, indent=2) + "\n")
        print(f"k={k}: best d={result['best_d']}, evaluations={result['triangle_free_evaluations']}, saved {path}")
        violation |= bool(result["bound_violations"])
    return 1 if violation else 0


if __name__ == "__main__":
    sys.exit(main())
