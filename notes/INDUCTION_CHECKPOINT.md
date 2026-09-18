# Induction checkpoint — 2026-09-18, exact path-based selection

JSP-000058 and general induction lemmas A/B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: selecting five vertices in a critical
core with a rigorous bound on the reoptimized increment, restricted in this
cycle to degree-two path interiors, cycle components, and isolates.
See [INDUCTION_THREAD_SELECTION.md](INDUCTION_THREAD_SELECTION.md).

## PROVED

Compress maximal degree-two paths to signed parity constraints K, retaining
loops and parallel constraints. If o counts odd cycle components, then

    d(C)=D(K)+o.

For a deletion X confined to path interiors, cycle components and isolates,
let S be the hit paths and j the number of hit odd cycle components. Then

    gamma_C(X)=D(K)-D(K-S)+j.

Any nonempty interior deletion on one path of an edge-critical core has
increment exactly one, regardless of the number or spacing of deleted
vertices. Deleting interiors from two paths with the same endpoints and
opposite length parity also has loss exactly one, without criticality.
The two paths must both be hit; total interior capacity at least five
then suffices to select five vertices. A general capacity criterion gives
explicit five-set witnesses with loss at most the maximum selected
constraint cost plus j. The proof constructs an optimal remainder cut
with q=0, allowing proper recoloring of surviving path fragments.

A/B reduce further to critical cores with no such capacity witness.
This does not resolve higher-degree selection. For k>=4 the OLD sequential
degree bound already excludes cores with five vertices of degree at most
three; the present work does not claim this observation as a new theorem
or remove the remaining low-degree vertices from the original order.

The nine-edge path in the previous F_(a,h) obstruction supplies five-sets
of increment exactly one. Thus those arbitrary-set threshold failures
still do not refute existential A/B.

## FALSIFIED

Additivity of losses from distinct critical paths. Two terminals joined
by two length-two and two length-three paths give d=2 and are edge-critical.
Hitting one path of each parity loses one in total, although each alone
loses one. Hitting two even paths loses two. The exact signed optimization
cannot be replaced by adding individual critical-edge losses.

## COMPUTATIONALLY VERIFIED

Independent full cut enumeration checks the signed formulas on every
interior/cycle/isolate deletion subset of five fixed decompositions,
1536 subsets in total. Fixtures include parallel paths of both parities,
rooted odd/even loops, odd/even cycle components, and subdivided K4.
Every original edge deletion is compared with the compressed prediction.
Separate tests check five separated interior deletions on a critical
length-ten path, opposite-parity five-set witnesses, and prescribed
monochromatic edge positions. Existing core-transfer regressions pass.

Validation: `.venv/bin/python -m pytest -q
 tests/test_induction_thread_selection.py tests/test_induction_critical_core.py`
— **8 passed**, 17.90 seconds. An initial expected subset-count assertion
was corrected from 1920 to 1536; mathematical assertions had passed.
These are bounded inference checks, not exhaustive general A/B evidence.

## CONJECTURAL / remaining claim

Select five vertices with q+e<=2k-1 (A), or <=2k-2 in the nonbalanced case
(B), on nonautomatic edge-critical cores without a path-capacity witness.
For k>=4 these cores have at most four vertices of degree at most three;
selection involving higher-degree vertices remains the substantive gap.
No minimum-degree-four reduction, 2-connected reduction, or general
optimal-cut sufficiency is claimed. No potential complete proof appeared.

## Coverage and clean stopping point

All t=1,...,25 saved artifacts were read: complete=true and max_gap=0.
Their homogeneous-neighborhood scope and the arbitrary t>=26 symbolic
proof do not alone establish an arbitrary all-t theorem. Subsequent
symbolic notes reach t>=3; mixed t=2 remains unresolved. The present
proof uses no balanced-extension result as a premise. No enumeration
was repeated and no random search was run.

Process inspection before each test launch found no existing compute job;
the two test jobs ran sequentially and finished. Notes and state were
updated; `git diff --check` passed. Unrelated overnight logs were left
untouched. This is a clean research checkpoint, not a claim that the
entire working tree is clean.
