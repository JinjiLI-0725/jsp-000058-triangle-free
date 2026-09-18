# Structural analysis of the C5 equality example

Date: 2026-09-18. Throughout, graphs are finite, simple and undirected,
and `d(G) = |E(G)| - MaxCut(G)`. Indices of parts are taken modulo five.
The original question is whether every triangle-free graph on `5k` vertices
satisfies `d(G) <= k²`. No general proof or global equality classification is
claimed here. Sections 1–6 are proofs; section 7 contains unproved proposed
lemmas; section 8 reports finite computations separately.

## 1. Exact blow-up formula (proved)

Let `B(a)` have independent parts `A_0,...,A_4` of nonnegative integer sizes
`a_0,...,a_4`, with all edges between consecutive parts and no other edges.
Allowing zero parts is useful for boundary cases. Then

\[
 |E(B(a))|=\sum_i a_i a_{i+1},\qquad
 d(B(a))=\min_i a_i a_{i+1},\qquad
 \operatorname{MaxCut}(B(a))=\sum_i a_i a_{i+1}-\min_i a_i a_{i+1}.
\]

**Part-rounding proof.** More generally consider a blow-up of any simple base
graph. Fix a cut and all vertices outside one part. Every vertex in that part
has the same number `p` of neighbors on the left and `q` on the right. If `x`
of the `a` vertices are on the left, their contribution is `xq+(a-x)p`.
This linear expression has a maximum at `x=0` or `x=a`. Start from a maximum
cut and round each part once. Its value cannot decrease and cannot exceed the
global maximum. Already rounded parts remain intact when later parts move.
Thus a maximum cut exists that keeps every part intact. This asserts existence,
not that every maximum cut keeps parts intact.

For C5 such cuts are two-colorings of the base cycle. The number of crossing
cycle edges is even, so at least one edge is monochromatic. Their total
monochromatic weight is at least the smallest `a_i a_{i+1}`. Conversely, for
each chosen cycle edge there is a coloring making that edge the only
monochromatic edge: alternate colors along the remaining four-edge path.
This proves the formula, including zero weights. In particular, if a part is
empty the graph is bipartite and the formula gives zero.

## 2. Maximization with fixed order (proved)

Suppose `sum a_i=5k`, with integer `k>=1`, and put `t=min_i a_i a_{i+1}`.
If any part is zero, `t=0<k²`. Otherwise

\[
 t^5\leq\prod_i(a_i a_{i+1})
       =\left(\prod_i a_i\right)^2
       \leq\left(\frac{\sum_i a_i}{5}\right)^{10}=k^{10}.
\]

The last step is arithmetic–geometric mean. Hence `t<=k²`. If `t=k²`, both
inequalities are equalities, and equality in arithmetic–geometric mean forces
`a_0=...=a_4=k`. Conversely these sizes give `t=k²`.
Thus the balanced vector is the **unique maximizer**, even if nonnegative
real part sizes are allowed. For integer sizes every other vector has
`d<=k²-1`; this does not classify equality among graphs outside this family.

## 3. Why the balanced example has d=k² (proved)

The formula already proves the assertion. There is also a useful independent
counting certificate. There are `k^5` transversal five-cycles, obtained by
choosing one vertex in each part. Every set of edges whose deletion makes the
graph bipartite must meet every such odd cycle. Each edge belongs to exactly
`k^3` transversal cycles. If `F` is a bipartizing deletion set, double counting
cycle–edge incidences gives `|F| k^3 >= k^5`, hence `|F|>=k²`.
Deleting all `k²` edges between one consecutive pair of parts leaves a blow-up
of a path and therefore a bipartite graph. Both bounds agree. In particular
the graph has `5k²` edges and maximum cut `4k²`.

## 4. Exact responses to perturbations (proved)

### 4.1 Moving a vertex between parts

Move a vertex from part `p` to distinct part `q`, where `a_p>=1`, retaining
the blow-up construction. Set `delta_i=1_{i=q}-1_{i=p}` and `w_i=a_i a_{i+1}`.
The complete exact update is

\[
 d'=\min_i\{w_i+a_i\delta_{i+1}+a_{i+1}\delta_i+
                         \delta_i\delta_{i+1}\}.
\]

Only edges of the base cycle incident with `p` or `q` need updating.
This also covers adjacent source and destination, where the quadratic term
is `-1`. There is no universal sign for the change: the reverse of a
balancing move reverses its effect, and moving between two zero-product
configurations can leave `d=0`. At the balanced vector, **every** move gives

\[
 d'=k(k-1),\qquad d'-d=-k.
\]

Indeed a neighbor of `p` other than `q` remains of size `k`, giving product
`k(k-1)`; all other products are at least this. For `k=1` the source empties.
Thus a single part transfer costs `k` in the objective, whereas a single
edge deletion costs only one. These are different perturbation scales.

### 4.2 Deleting an edge

For any graph let `b_G(S)` count edges monochromatic in cut `S`. If `e` is
deleted, then `b_{G-e}(S)=b_G(S)-1_{e monochromatic in S}`. Consequently

\[
 d(G)-1\leq d(G-e)\leq d(G),
\]

and `d(G-e)=d(G)-1` **if and only if** some optimal cut of `G` leaves `e`
monochromatic. For necessity, a cut attaining `d(G)-1` after deletion must
have had cost exactly `d(G)` and contained `e` among its monochromatic edges.
The converse follows by using that cut after deletion.

In the balanced blow-up every edge can be monochromatic in an optimal cut:
choose its part pair as the sole monochromatic cycle edge. Hence deleting
any one edge gives `d=k²-1`. In an arbitrary blow-up this conclusion holds
whenever the edge is in a minimum-product pair; the general optimal-cut
criterion above is the exact characterization without extra assumptions.

More generally, edge inclusion makes `d` nondecreasing. Every proper spanning
subgraph of the balanced blow-up has `d<=k²-1`, by comparison with a graph
missing just one of its edges. Thus searching its edge-deleted subgraphs
cannot produce a different equality graph, for any `k`.

### 4.3 Changing one vertex's whole neighborhood

Here all edges not incident with a fixed vertex `v` stay unchanged. Put
`H=G-v` and let `N` be the proposed new neighborhood in `H`. Exactly

\[
 d(H+v_N)=\min_{S\subseteq V(H)}
 \bigl[b_H(S)+\min\{|N\cap S|,|N\setminus S|\}\bigr].                 \tag{1}
\]

For a fixed cut of `H`, put `v` on the better side; then minimize over the
cuts of `H`. The extension is triangle-free precisely when `H` is
triangle-free and `N` is independent in `H`. Formula (1) is valid for
arbitrary graphs and describes the exact change by subtracting its values
for the old and new neighborhoods. In particular

\[
 d(H)\leq d(H+v_N)\leq d(H)+\lfloor |N|/2\rfloor,
 \quad |d(H+v_N)-d(H+v_M)|\leq |N\mathbin\triangle M|.
\]

There is a sharper complete description when the starting graph is balanced.
Label the old part of `v` as `A_0`; the remaining part sizes in `H` are
`(k-1,k,k,k,k)`. Write `N_0=A_4 union A_1` for its old neighborhood.
For every independent `N` in `H`,

\[
 d(H+v_N)=
 \begin{cases}
 k^2-k+\min\{|N\cap A_4|,|N\cap A_1|\},&N\subseteq N_0,\\
 k^2-k,&N\not\subseteq N_0.
 \end{cases}                                                       \tag{2}
\]

**Proof for `k>=2`.** Since all remaining parts are nonempty, an independent
neighborhood meets at most two parts, whose indices are nonadjacent in C5.
Such a set is contained in the two neighboring parts of some cycle index
`j`. If `N` is not contained in `N_0`, necessarily `j!=0`. The extension is
a spanning subgraph of the blow-up obtained by moving `v` from part 0 to
part `j`; that graph has `d=k²-k` by 4.1. Its induced subgraph `H` also has
`d=k²-k`, so monotonicity proves the second line.

For the first line put `x=|N cap A_4|`, `y=|N cap A_1|` and assume
`x<=y` by reflection. A cut of `H` whose sole monochromatic part pair is
incident with part 0 has cost `k(k-1)` and puts `A_4,A_1` on opposite sides.
Putting `v` on the better side gives the upper bound `k(k-1)+x`.
If `x=0`, the matching lower bound follows from the induced subgraph `H`.
For `x>0`, use the following fractional odd-cycle packing:

* Give each transversal cycle entirely in `H` weight `1/k³`, for total
  weight `(k-1)k`. Each edge incident with `A_0` receives total weight 1;
  each edge in the other three consecutive part pairs receives `(k-1)/k`.
* Give each transversal cycle through `v` weight `1/(y k²)`. There are
  `xy k²` such cycles, so their total weight is `x`. An edge from `v` to
  `A_4` receives weight 1 and an edge from `v` to `A_1` receives `x/y<=1`.
  An edge in `A_4`–`A_3` receives at most `1/k`, one in `A_1`–`A_2` at
  most `x/(yk)<=1/k`, and one in `A_2`–`A_3` receives `x/k²<=1/k`.

Thus the combined packing loads every edge by at most 1. Every bipartizing
deletion set meets every packed odd cycle, and its cardinality is at least
the sum of the cycle weights, namely `(k-1)k+x`. This proves the first line
without assuming that the modified graph has a part-respecting optimal cut.

For `k=1`, the graph has five vertices; its only possible odd cycle has
length five. Starting with the remaining four-vertex path, it occurs exactly
when both old neighbors are retained, giving (2) directly.

In particular equality `d=k²` forces the original neighborhood `N=N_0`.
Even without the first line of (2), this last claim follows immediately:
if `N` is a proper subset of `N_0`, 4.2 applies; otherwise the part-transfer
upper bound gives `d<=k²-k`.

## 5. Quantitative stability inside the blow-up family (proved)

Let `r=k²-d(B(a))` and suppose `0<=r<k²`. Set `epsilon=r/k²` and
`x_i=a_i/k`. Then `sum x_i=5`, `0<x_i<=5`, and

\[
 \prod_i x_i\geq(1-\epsilon)^{5/2}.
\]

For `0<x<=5`, Taylor's theorem and `(log x)''=-1/x²<=-1/25` give
`log x <= x-1-(x-1)²/50`. Summing and taking logarithms of the product bound
proves

\[
 \sum_i(a_i-k)^2\leq -125k^2\log(1-r/k^2).
\]

If `r<=k²/2`, this is at most `250r`, since `-log(1-u)<=2u` for `0<=u<=1/2`.
Thus small deficit forces the five part sizes close to balance. One can
balance the parts by moving `T=(1/2)sum_i |a_i-k|` vertices. Only pairs
incident with moved vertices can change adjacency, so on the same vertex set
the edge symmetric difference from some balanced blow-up is at most

\[
 5kT\leq (5k/2)\sqrt{1250r}\qquad(0\leq r\leq k^2/2).
\]

The constant is deliberately loose. This is a rigorous stability statement
**within the blow-up family**, not a statement about arbitrary triangle-free
graphs. A general stability theorem must first control the distance to this
family; arithmetic–geometric mean supplies no such reduction.

## 6. What equality searches can and cannot establish

The preceding proofs exclude every proper spanning subgraph, every unbalanced
C5 blow-up, and every nontrivial triangle-free one-vertex neighborhood change
of the balanced example as a new equality graph, for all `k`. A graph requiring
simultaneous changes at two or more vertices is not covered by these arguments.
For example, two disjoint balanced blow-ups of scales `p,q>0` have
`d=p²+q²<(p+q)²`, since deletion distance adds over components; this also
rules out that particular way of constructing another equality example.

## 7. Proposed structural lemmas (unproved)

New general reduction: [INDUCTION_CRITICAL_CORE.md](INDUCTION_CRITICAL_CORE.md)
proves that each of A and B is equivalent to its restriction to edge-critical
spanning graphs (with small-d cases automatic). This preserves vertex count,
including isolates, and transfers the same five-set using d(C)=d(G).
The selection lemma on that smaller class remains conjectural.

Current partial progress: [BALANCED_EXTENSION_T3.md](BALANCED_EXTENSION_T3.md)
proves that for k>=4, any five-set leaving B_(k-1) satisfies A, and also
B when G is nonbalanced. This does not select a suitable set in an arbitrary
graph. The general q+e obstruction remains as stated in INDUCTION_ROUTE.md.

These are precise induction targets. Their computational tests are reported
in section 8; passing those tests is not a proof. Neither is used to assume
the conjecture in the computations.

**A — five-vertex reduction.** For every triangle-free graph `G` on `5k`
vertices, `k>=2`, there exists a five-vertex set `X` such that

\[
 d(G)-d(G-X)\leq 2k-1.
\]

Together with the elementary `n=5` base case, A implies the original
conjecture by induction: `(k-1)²+(2k-1)=k²`. The base case follows since
a nonbipartite triangle-free graph on five vertices must contain a spanning
C5, whose every additional edge would form a triangle. On the balanced
blow-up, taking one vertex from every part attains the proposed increment
exactly. The main obstacle is choosing `X` and controlling optimal cuts of
the remainder, rather than just counting edges incident with `X`.

**B — strict reduction away from the balanced example.** Under the same
hypotheses, if `G` is not isomorphic to the balanced C5 blow-up, there exists
a five-vertex set `X` such that

\[
 d(G)-d(G-X)\leq 2k-2.
\]

B plus the already proved balanced calculation implies A, the conjectured
bound, and global uniqueness at equality, all by induction. Specifically,
every nonbalanced graph would have `d<=(k-1)²+2k-2=k²-1`.
It is substantially stronger than the original bound: that bound by itself
does not guarantee a remainder retaining enough deletion distance.
Neither A nor B alone quantifies edit distance of near-extremizers; B only
distinguishes exact equality from positive integer deficit. A robust version
controlling the edits incurred in successive reductions would be needed for
global stability.

## 8. Computational observations and reproducibility

The new targeted experiment is implemented in
`src/triangle_free/structural_analysis.py`, with machine-readable output in
`results/structural_analysis.json`. Run from the repository root:

```sh
PYTHONPATH=src .venv/bin/python -m triangle_free.structural_analysis
```

It enumerates every independent neighborhood of one distinguished vertex
after its removal from the balanced blow-up for `k=1,2,3`. Symmetry makes
the choice of the distinguished vertex immaterial. It minimizes (1) over
every cut, cross-checks a representative of every attained objective value
with the Gray-code solver, and checks every equality-or-better graph with
both existing full-graph exact solvers. This is exhaustive for the specified
one-vertex modification family, not for all graphs of these orders.

It also attempts to falsify **each of A and B** on the full saved `n=10`
corpus and every distinct labeled graph in the completed bounded `n=15`
request log, supplemented by the balanced example with one edge deleted.
When `d(G)` is already below the proposed increment, nonnegativity of
`d(G-X)` makes the check automatic. Otherwise the code enumerates remaining
vertex subsets, computes their exact deletion distances, and stops when a
witness is found. A reported failure requires exhausting all subsets, so
failure and success both have a finite exact criterion. The `n=15` input
values are reused from the completed experiment; input hashes are pinned.

### New one-vertex experiment

| k | Independent neighborhoods tested | Exact d histogram | Non-C5 equality graphs |
|---|---:|---|---:|
| 1 | 8 | `{0:7, 1:1}` | 0 |
| 2 | 47 | `{2:38, 3:8, 4:1}` | 0 |
| 3 | 221 | `{6:172, 7:33, 8:15, 9:1}` | 0 |

Every equality case retained the original neighborhood. These computations
agree with (2), whose proof applies to all `k`. They are exhaustive over
neighborhood subsets of the fixed remainder, with no maximal-completion step.
In particular the `k=3` experiment includes 15 labeled one-vertex changes
with `d=8`; it does not claim they represent 15 isomorphism classes.

### Falsification attempts for the proposed lemmas

| Input corpus | Graphs | A automatic | B automatic | Remainders evaluated jointly | A failures | B failures |
|---|---:|---:|---:|---:|---:|---:|
| All n=10 triangle-free isomorphism classes | 12,172 | 12,171 | 12,146 | 1,630 | 0 | 0 |
| Saved n=15 distinct labeled graphs, plus one edge-deleted example | 8,237 | 5,112 | 3,207 | 40,425 | 0 | 0 |

For the balanced graph, the joint test uses A's threshold because B's
nonbalanced hypothesis does not apply. The two tests share remainder
computations; the last count is not doubled. None of these tests uses the
conjectured bound for a remainder: its value is computed by exact cuts.
The n=15 corpus has 8,236 distinct labeled inputs from the previous bounded
run and the one additional graph. There is no new broad random search.

A and B survived their specified falsification attempts and are worth
investigating as induction targets. Evidence for A at n=10 is particularly
weak as a structural test: all but the balanced example pass automatically.
B requires nontrivial tests on 26 of those graphs (including the balanced
exception tested with A's bound). Survival of either test does not establish
it for larger orders or for unexamined n=15 graphs.

### Search for equality outside the family

The new exhaustive local neighborhood search found no non-C5 equality graph.
The earlier bounded search found only the balanced equality class at `k=3`;
the exhaustive `k=2` corpus had only that equality class as well. These older
observations are documented in `notes/observations.md`. Combined with section
6, this rules out several concrete construction mechanisms, but leaves the
general existence question open. In particular, the local rigidity theorem
cannot exclude distant equality graphs or coordinated changes at several
vertices. Near equality does not force an exact blow-up: deleting one edge
from the balanced k=3 example gives `d=8` and seven false-twin classes, as
verified in `results/structural_checks.json`.

### Validation

`tests/test_structural_analysis.py` compares the blow-up formula with full
cut enumeration on balanced, boundary, and seeded unbalanced vectors, checks
all k=2 single-edge deletions and representatives of every part-transfer
type, and exercises the neighborhood and reduction experiment helpers.
The result JSON pins the script and input hashes and saves the full equality
witnesses, including their cut values and structural classifications.
The complete repository test suite passed: **62 tests**, with no skips.
`git diff --check` passed, and the saved script/input hashes were rechecked.
