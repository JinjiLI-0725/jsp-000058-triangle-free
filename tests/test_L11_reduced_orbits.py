import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_L11_reduced_orbits import (  # noqa: E402
    SHAPES, TYPE_INDEX, TYPES, assignment_gains, endpoint_profiles,
)


RESULT = Path("results/hard_regime_L_n15/L11_reduced_orbits.json")


def test_reduced_state_counts_and_exact_minima():
    result = json.loads(RESULT.read_text())
    expected = {
        "zero": (178464, 18320, 29),
        "one": (3442706, 175386, 27),
        "path": (11730131, 665015, 23),
        "matching": (51250771, 673334, 17),
    }
    assert result["status"] == "finite_certificate_minimum_at_least_7"
    assert result["global_min_total_gain"] == 17
    for name, (raw, orbits, minimum) in expected.items():
        row = result["shapes"][name]
        assert row["reduced_states_before_symmetry"] == raw
        assert row["reduced_states_after_symmetry"] == orbits
        assert row["exact_min_total_gain"] == minimum


def test_saved_minimizers_recompute_exactly():
    result = json.loads(RESULT.read_text())
    for name, row in result["shapes"].items():
        witness = row["witness"]
        endpoint = tuple(TYPE_INDEX[sum(1 << i for i in neighbourhood)]
                         for neighbourhood in witness["endpoint_neighbourhoods"])
        profiles, _ = endpoint_profiles(SHAPES[name], endpoint)
        multiplicities = tuple(witness["isolated_multiplicities"])
        gains = assignment_gains(profiles, multiplicities)
        assert list(gains) == witness["assignment_gains"]
        assert sum(gains) == witness["total_gain"] == row["exact_min_total_gain"]
        assert sum(multiplicities) == 10 - len(endpoint)
        boundary = (sum(TYPES[t].bit_count() for t in endpoint) +
                    sum(multiplicities[t] * TYPES[t].bit_count()
                        for t in range(len(TYPES))))
        assert boundary == witness["total_boundary"]
        assert boundary >= 9


def test_matching_branch_used_multiplicity_pruning():
    matching = json.loads(RESULT.read_text())["shapes"]["matching"]
    assert matching["distinct_endpoint_profiles"] == 3267
    assert matching["matching_vectors_examined"] == 6350
    assert matching["matching_vectors_pruned_by_monotone_bound"] == 26122429
