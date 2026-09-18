import json
from math import comb
from pathlib import Path
import random

import pytest

from triangle_free import Graph, c5_blowup, exact_max_cut, random_triangle_free
from triangle_free.heuristic import andrasfai, blowup, compositions, fill_maximal, mutate, run, structured_bases
from triangle_free.research import independent_max_cut, triangle_free_triples
from test_research import nauty_tools


def test_positive_compositions():
    for parts in range(1, 16):
        vectors = list(compositions(15, parts))
        assert len(vectors) == comb(14, parts - 1)
        assert len(set(vectors)) == len(vectors)
        assert all(len(w) == parts and sum(w) == 15 and min(w) >= 1 for w in vectors)
    assert list(compositions(2, 3)) == []


def weighted_cut(base, weights):
    return max(sum(weights[u] * weights[v] for u, v in base.edges
                   if bool(mask & (1 << u)) != bool(mask & (1 << v)))
               for mask in range(1 << base.n))


def test_blowups_against_weighted_base_cut():
    assert blowup(c5_blowup(1), (3, 3, 3, 3, 3)) == c5_blowup(3)
    rng = random.Random(5803)
    for name, base in structured_bases():
        assert triangle_free_triples(base), name
        weights = [1] * base.n
        for _ in range(15 - base.n):
            weights[rng.randrange(base.n)] += 1
        graph = blowup(base, weights)
        assert graph.n == 15
        assert triangle_free_triples(graph)
        assert independent_max_cut(graph)[0] == weighted_cut(base, weights)
    with pytest.raises(ValueError):
        blowup(c5_blowup(1), (0, 1, 1, 1, 1))


def test_andrasfai_definition():
    for index in range(1, 6):
        graph = andrasfai(index)
        assert graph.n == 3 * index - 1
        assert triangle_free_triples(graph)
        assert all(mask.bit_count() == index for mask in graph.adjacency_masks())
    with pytest.raises(ValueError):
        andrasfai(0)


@pytest.mark.parametrize('operator', ['delete_refill', 'rewire_vertex', 'force_nonedge'])
def test_mutations_reproducible_triangle_free_and_maximal(operator):
    for seed in range(20):
        graph = c5_blowup(3) if seed % 2 else random_triangle_free(15, random.Random(seed))
        output = mutate(graph, random.Random(seed), operator)
        assert output == mutate(graph, random.Random(seed), operator)
        assert output.n == 15
        assert triangle_free_triples(output)
        adjacency = output.adjacency_masks()
        for u in range(15):
            for v in range(u + 1, 15):
                if (u, v) not in output.edges:
                    assert adjacency[u] & adjacency[v]


def test_completion_and_mutation_errors():
    graph = c5_blowup(3)
    assert fill_maximal(graph, random.Random(0)) == graph
    with pytest.raises(ValueError):
        mutate(graph, random.Random(0), 'unknown')
    with pytest.raises(ValueError):
        mutate(Graph(3, ((0, 1), (0, 2), (1, 2))), random.Random(0), 'delete_refill')


def test_heuristic_reproducibility_and_no_exhaustive_claim(tmp_path):
    _, labelg = nauty_tools()
    params = dict(seeds=(7, 8), samples=8, steps=251, checkpoint_every=20, include_structured=False)
    first = run(tmp_path / 'first', labelg, **params)
    second = run(tmp_path / 'second', labelg, **params)
    assert first == second
    assert first['best_d'] == 9
    assert first['exhaustive'] is False
    assert first['evaluations'] == 523  # benchmark + two (8 random + start + 251 steps + restart)
    assert first['best_witnesses'][0]['is_C5_blowup']
    checkpoint = json.loads((tmp_path / 'first' / 'checkpoint.json').read_text())
    assert checkpoint['status'] == 'complete'
    assert checkpoint['exhaustive'] is False
    with pytest.raises(ValueError, match='fresh output'):
        run(tmp_path / 'first', labelg, **params)
