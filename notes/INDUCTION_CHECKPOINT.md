# Induction checkpoint — 2026-09-18, pendant five-set selection

JSP-000058 and general induction lemmas A/B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: selecting five vertices while
controlling q+e in critical cores, this cycle through pieces attached at
one retained vertex. See [INDUCTION_PENDANT_SELECTION.md](INDUCTION_PENDANT_SELECTION.md).

## PROVED

Using the existing one-vertex gluing identity, deletion increments localize
exactly to pendant interiors and add across disjoint such interiors.
For a balanced block B_s, s>=2, avoiding any one prescribed root, the
minimum increment for deleting j=0,...,5 vertices is respectively

    0, s, s, 2s-1, 2s-1, 2s-1.

For C5 the private capacity is four, each nonempty deletion costing one.
A proper pendant B_s with s>=2 supplies a five-set at cost
2s-1<=2k-3, hence satisfying B. The construction has a remainder-optimal
coloring with q=0. This handles vertices of arbitrarily large degree.

A/B hold for critical cores whose nontrivial blocks are balanced C5
blow-ups or odd cycles, with B's usual balanced exception. The proof
uses a large leaf block, two C5 leaf blocks, or a single-block component.
It never discards vertex counts or assumes a conjectural bound on an
arbitrary block. The equal-d spanning-core transfer gives the same
five-set upper bound in the original graph.

## FALSIFIED

Unconditional extension of additive gluing to two shared boundary vertices:
a length-two path and a length-three path are each bipartite, but their
union along both endpoints is C5. This is an inference safeguard, not a
counterexample to A/B. Single-root gluing was already proved in earlier
notes; the new progress is the rooted profile and five-set selection.

## COMPUTATIONALLY VERIFIED

Full cut enumeration checks 398 root-avoiding subsets of B_1/B_2, every
local increment for B_2 glued to C5 or K2,3 (764 cases), simultaneous
private deletions in two C5 pieces, and a B_3 transversal. A nonautomatic
order-20 example (two B_2 blocks sharing a root plus one isolate) has
only one vertex of degree at most three, d=8, gamma=3, and an explicitly
checked q=0, e=3 coloring.

Validation ran sequentially:

- `.venv/bin/python -m pytest -q tests/test_induction_pendant_selection.py tests/test_induction_critical_core.py`
  — 7 passed, 22.42 seconds.
- After adding the high-degree/q=0 check:
  `.venv/bin/python -m pytest -q tests/test_induction_pendant_selection.py`
  — 4 passed, 11.61 seconds.

Together these cover eight distinct tests; the three initial new tests
were rerun with the added fourth test. These are bounded inference checks,
not exhaustive general A/B evidence. `git diff --check` passed.

## CONJECTURAL / remaining bottleneck

Select five vertices with q+e<=2k-1 (A), or <=2k-2 in the nonbalanced case
(B), on residual nonautomatic critical cores lacking the automatic,
path-capacity, and pendant witnesses. Arbitrary leaf blocks and
2-connected higher-degree cores remain unresolved. No general reduction
to 2-connected cores or minimum degree four is claimed.

## Coverage and stopping point

All t=1,...,25 saved artifacts were read: complete=true and max_gap=0.
Their homogeneous scope and the arbitrary t>=26 symbolic proof do not
alone establish the arbitrary all-t result; subsequent symbolic notes
reach t>=3, leaving mixed t=2 unresolved. No balanced-extension theorem
was used as a premise. The t=5 empty witness does not classify equality.
No enumeration was repeated and no random search was run.

Process inspection before each test launch found no existing compute job.
Both test jobs finished. Notes and state were updated. Unrelated overnight
logs were left untouched. No potential complete solution appeared.
This is a clean research checkpoint, not an entirely clean working tree.
