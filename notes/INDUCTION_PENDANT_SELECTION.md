# Five-set selection in pieces attached through one vertex

Date: 2026-09-18. **Single bottleneck:** selecting five vertices with a
controlled reoptimized increment in the residual critical-core domain of
A/B. This cycle handles pendant pieces, including vertices of arbitrarily
large degree. General A/B and JSP-000058 remain **CONJECTURAL**.

## Exact localization — PROVED

Suppose C=P union R, with edge sets disjoint, V(P) intersect V(R)={r},
and no further edges. The pieces need not be connected or critical.
For X subset V(P) minus {r},

    d(C)=d(P)+d(R),
    d(C-X)=d(P-X)+d(R),
    gamma_C(X)=gamma_P(X).                               (1)

Every coloring costs at least the sum of the separate minima. Conversely,
choose optimal colorings of the two pieces and globally reverse one if
needed to agree at r. This proves both equalities, including when P-X
is disconnected. This is an application of the earlier one-vertex gluing
lemma in INDUCTION_CONNECTED_SLACK.md, not a new claim of that lemma.
For disjoint pendant interiors P_i-r_i whose roots are all retained in a
common remainder R, the same argument gives

    gamma_C(union X_i)=sum_i gamma_(P_i)(X_i).             (2)

Roots may coincide. The hypotheses require that distinct interiors have
no connecting edges and meet other pieces only at their own retained root.
Thus local minimum deletion profiles can be combined by minimizing their
sum over allocations with total size five. No assumption about optimal
full-graph cuts or a bounded slack window is involved.

## Root-avoiding balanced-block profile — PROVED

Let P=B_s and fix any root r. For feasible j<=5 define

    f_s(j)=min_{X subset V(P)-{r}, |X|=j} gamma_P(X).

For s>=2 the exact answer is

    j         0    1    2      3       4       5
    f_s(j)    0    s    s    2s-1    2s-1    2s-1.        (3)

For s=1, only j=0,...,4 are feasible, with f_1(0)=0 and
f_1(j)=1 for j>0.

Proof: write x_i for the number deleted from part i. The proved blow-up
formula gives d(P-X)=min_i (s-x_i)(s-x_(i+1)). Any nonempty deletion
makes this at most s(s-1). For j=1 this is attained. For j=2 it is
attained by deleting from two nonconsecutive parts. For j>=3, if some
x_i>=2, the minimum is at most s(s-2)<(s-1)^2. Otherwise at least three
parts are hit, and two are consecutive since the independence number
of C5 is two. The minimum is then at most (s-1)^2. Deleting one vertex
from each of any j distinct parts attains (s-1)^2 for 3<=j<=5. Every
construction can avoid r because s>=2. For s=1, deleting any nonempty
proper set from C5 leaves a forest, proving the stated profile.

These witnesses also explicitly control q+e. Choose a part coloring of
P-X whose sole monochromatic pair attains its minimum product; assign
any empty parts according to that same five-part coloring. Extend it to
P by coloring restored vertices with their parts. The full cost is s^2.
Glue an optimal coloring of R by reversal at r. The restriction is
optimal on C-X, so q=0 and e=gamma_P(X). For s=1 choose a pair incident
with a deleted vertex, so its remainder product is zero. This argument
constructs an appropriate remainder optimum; it does not assert that
EVERY remainder optimum extends this well.

## A higher-degree selection consequence — PROVED

Let C be triangle-free of order 5k and contain a pendant B_s, s>=2,
whose private vertices have no outside neighbors. If it is a proper
piece then 5s<5k, hence s<=k-1. A transversal avoiding its root has

    |X|=5,   gamma_C(X)=2s-1<=2k-3.                       (4)

It therefore meets both A and the strict B threshold. The graph cannot
be B_k: the pendant piece is proper and B_k is connected without a cut
vertex. If the extra vertices are in separate components, connectedness
alone also distinguishes it. A component B_s has the same transversal
witness without a forbidden root. If C=B_k, the familiar transversal
has increment 2k-1 and meets A.

In a critical core every block is critical, by (1) applied repeatedly
along its block tree, also after deleting an edge in that block. Thus a
leaf block which is a positive complete C5 blow-up must be balanced,
by INDUCTION_CRITICAL_CORE.md. Formula (4) covers all such leaf blocks
of size at least ten. An odd-cycle leaf block of length at least seven
has at least six private vertices; deleting five costs exactly one.
Two distinct C5 leaf blocks supply four private vertices from one and
one from the other, at total loss two by (2).

Consequently **A and B hold for every critical core on 5k vertices all
of whose nontrivial blocks are balanced C5 blow-ups or odd cycles**, with
B's usual exception C=B_k. Here k>=2. To verify all cases: in any
component with multiple blocks choose a leaf block of size at least
seven if one exists, using (4) or the odd-cycle rule. Otherwise all leaf
blocks are C5 and any two supply the loss-two witness. A component with
one block is a balanced blow-up or an odd cycle: use its transversal or
any five cycle vertices. A proper balanced component has s<=k-1. If
there are no nontrivial components, the graph is edgeless. Isolates
remain counted in 5k throughout. The block tree has at least two leaves
when it has multiple blocks; bridge blocks cannot occur in a critical
core. No conjectured bound for an arbitrary block is used.

For example, glue two copies of B_s at one vertex and add one isolate.
Then n=10s, k=2s, d=2s^2, and a private transversal loses 2s-1.
For s>=2 these graphs are nonautomatic for A/B (d>=2k) and have only
one vertex of degree at most three. Their nonisolated degrees are 2s
and 4s. Thus these witnesses genuinely include the higher-degree domain
left by the last path-capacity result. The example is illustrative;
the theorem allows an arbitrary graph on the other side of a pendant
balanced piece, not just another balanced block.

## Limits and inference checks

**CONJECTURAL:** A_crit/B_crit on the remaining cores after excluding
these witnesses and the earlier automatic/path cases. The reduction to
this smaller domain is **PROVED**, using equal-d core transfer. This
is not a reduction to 2-connected cores: arbitrary leaf blocks can
still remain. An arbitrary induced B_s with outside edges at several
vertices is not covered. We do not delete an attachment root.

**FALSIFIED:** extending the one-vertex additive identity to two shared
boundary vertices without compatibility information. A length-two path
and a length-three path with the same endpoints are individually
bipartite but their union is C5, with d=1. This elementary boundary
check is not a counterexample to A/B or to (1).

**COMPUTATIONALLY VERIFIED:** see tests/test_induction_pendant_selection.py.
Independent full cut calculations check every root-avoiding deletion of
size at most five in B_1 and B_2, including all five minima for B_2.
The B_2 profiles are also checked after gluing an arbitrary fixed rooted
triangle-free piece (C5 or K2,3). A separate two-C5 gluing checks simultaneous
deletions in both pieces. A B_3 transversal checks the larger-degree
formula. Two copies of B_2 glued at one vertex, plus an isolate, check
a nonautomatic order-20 example and an explicit q=0, e=3 coloring. A finite
check records the two-boundary incompatibility above. These tests check
inferences on fixed graphs, not all A/B instances.

All completed t=1,...,25 artifacts were read: complete=true, max_gap=0.
They certify homogeneous neighborhoods. They and the arbitrary t>=26
symbolic theorem do not alone cover arbitrary mixed extensions; later
notes prove t>=3 and leave mixed t=2 unresolved. No balanced-extension
result is needed in this proof, and no enumeration was repeated.
No broad random search or potential complete solution occurred.

Validation: the new tests plus critical-core regressions passed (7 tests,
22.42 seconds); after adding the order-20/q=0 check, all four new tests
passed (11.61 seconds). Eight distinct tests passed across the two runs.
Process inspection before each launch found no existing compute job. Both
runs finished sequentially. `git diff --check` passed.
