# Induction checkpoint — 2026-09-19, three-boundary selection

JSP-000058 and general induction lemmas A/B remain **CONJECTURAL**.
Exactly one bottleneck was addressed: five-set q+e selection in residual
critical cores, through balanced pieces with three retained attachments.
See [INDUCTION_THREE_BOUNDARY_SELECTION.md](INDUCTION_THREE_BOUNDARY_SELECTION.md).

## PROVED

For at most three prescribed roots in B_s, every constrained boundary
profile is F_s(a)=s^2+delta(S,a), with delta in {0,2} independent of s.
A complete root-orbit table constructs upper bounds. Constrained rounding
and explicit nonnegative quadratic coefficient tables prove lower bounds
for the two exceptional color patterns, at every admissible s.

If every part has a private vertex, deleting a private transversal from
such a piece has gamma=2s-1. Both glued optimization problems have the same
boundary penalty, which cancels. Nested optimal colorings give q=0 and
e=2s-1. A proper piece has s<=k-1, so its five-set satisfies B and A.
Equal-d spanning-core transfer carries that upper bound to the original
graph. No bound on the attached graph is assumed.

## FALSIFIED

Three-root flatness: three zero-colored roots in consecutive parts force
cost s^2+2. A subdivided claw attached to these roots of B_2 gives d=5,
rather than the additive value 4. Its private transversal still costs 3.
Thus constant profile differences suffice even when flatness fails.
This does not refute A/B.

## COMPUTATIONALLY VERIFIED

Bounded checks cover all 20 normalized placement/color rows, each with
32 quadratic cut templates; independent full cuts for every triple in
B_1 and B_2; and a triangle-free glued graph with a nested q=0 witness.
Existing two-boundary regression tests are included. These checks validate
the algebra and gluing inference; they are not general A/B enumeration.
Validation: `.venv/bin/python -m pytest -q tests/test_induction_three_boundary_selection.py tests/test_induction_two_boundary_selection.py`
— **7 passed in 68.99 seconds**. `git diff --check` passed. The test job
finished; no compute job remains. This is a clean research checkpoint.

## CONJECTURAL / remaining bottleneck

Select five vertices with q+e<=2k-1 (A), or <=2k-2 away from B_k (B), on
nonautomatic critical cores lacking automatic, path-capacity, pendant,
or feasible three-boundary balanced-piece witnesses. Arbitrary leaf blocks
and higher-degree cores remain unresolved. No reduction to balanced pieces
or to 4-connected cores is claimed. Four-root profiles are not addressed.

## Coverage and stopping point

All t=1,...,25 artifacts were read: complete=true and max_gap=0 throughout.
Their homogeneous scope does not combine with the arbitrary t>=26 symbolic
argument to prove the arbitrary all-t theorem. Subsequent symbolic notes
reach t>=3, leaving mixed t=2 unresolved. No balanced-remainder extension
result was used as a premise. The t=5 empty witness does not classify equality.
No enumeration was repeated; no random search or long research job was run.
Process inspection before computation found no existing compute job.
No potential complete solution appeared. Unrelated overnight logs were left
untouched. Earlier pendant and two-boundary results remain in their notes.
