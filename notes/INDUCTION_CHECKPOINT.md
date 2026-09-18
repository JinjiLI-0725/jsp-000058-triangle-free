# Induction checkpoint — 2026-09-18, 2-connected threshold obstruction

JSP-000058 and induction lemmas A/B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: whether 2-connectedness permits a
universal constant slack window to certify a specified five-set at an
A/B threshold. See
[INDUCTION_TWO_CONNECTED_SLACK.md](INDUCTION_TWO_CONNECTED_SLACK.md).

## PROVED

The symbolic family F_(a,h), a>=1 and h>=3, is triangle-free,
2-connected and edge-critical. It joins J_a and B_h at two vertices of
the independent deleted boundary and replaces one retained edge by a
nine-edge path. For its specified five-set X,

    k=2a+h+2, d=3a+h^2, gamma=3a+3h, L=2a+3h,
    minimum slack of a coloring attaining gamma = a.

All two-vertex boundary compatibility, critical-edge witnesses and
subdivision effects are proved explicitly. With h=a+3, gamma=T_B+1;
with h=a+4, gamma=T_A+1. Both specializations have d>=2k, and the first
threshold-violating coloring has slack exactly a.

## FALSIFIED

Every proposed universal constant slack cutoff for deciding a specified
five-set's A or B threshold, even on 2-connected nonautomatic critical
cores. Choose a larger than the cutoff. Unlike earlier examples, these
are false positives at the actual thresholds, not merely incorrect exact
increments that still satisfy the threshold.

This does NOT refute A/B: five consecutive internal vertices of the long
path give a different set with increment at most one. It also does not
refute the proved graph-dependent cutoff U_X-T-1.

## COMPUTATIONALLY VERIFIED

Exact boundary tables check the symbolic formulas and threshold failures
for a=1,2,3, with h=a+3 and a+4. They enumerate every Q coloring and every
B_h part-count pattern, retaining shared vertex colors. Independent graph
checks verify triangle-freeness and connectivity after every single-vertex
deletion; a path truth table checks the subdivision inference. Existing
amplification and full-cut regressions also pass.

Validation: `.venv/bin/python -m pytest -q
 tests/test_induction_two_connected_slack.py
 tests/test_induction_slack_amplification.py tests/test_induction_cut_slack.py`
— **6 passed**, 72.70 seconds. These bounded construction checks are not
an exhaustive A/B verification. Process inspection before launch found
no visible existing compute job. Only one test job ran; it finished.
No broad random search or balanced-extension enumeration ran.

## CONJECTURAL / exact remaining claim

A_window/B_window still require choosing five vertices X on each
nonautomatic critical core so that all cuts through its graph-dependent
slack window U_X-T-1 satisfy r_X<=T+s, where T=2k-1 for A and T=2k-2
for nonbalanced B. These remain equivalent to A/B. The new obstruction
shows that even threshold-only control cannot use a universal constant
window for an arbitrary X; the selection of X must do real work.
No reduction of A/B to 2-connected graphs is claimed.

## Coverage and clean stopping point

All t=1,...,25 artifacts were read: complete=true and max_gap=0 throughout.
They certify homogeneous extensions. Together with the arbitrary t>=26
symbolic proof they do not establish an all-t arbitrary extension theorem.
Subsequent symbolic notes reach t>=3; mixed t=2 remains unresolved. No
balanced-extension result was used as a premise or recomputed.

Notes and state were updated; `git diff --check` passed. Unrelated existing
overnight log changes were left untouched. No potential complete proof
appeared. This is a clean research checkpoint, not a claim that the entire
working tree is clean.
