> **Latest progress (2026-09-18, connected slack obstruction):**
> [INDUCTION_CONNECTED_SLACK.md](INDUCTION_CONNECTED_SLACK.md) proves that
> even connected, bridgeless, nonautomatic edge-critical cores can require
> arbitrarily large slack to attain a specified five-deletion increment.
> The one-vertex union of J_a, B_(2a+3), and C13 has gamma=3a+1,
> optimal-cut maximum 2a+1, and minimum maximizing slack a.
> **FALSIFIED:** connected versions of optimal-cut sufficiency and universal
> constant slack truncation. A/B remain **CONJECTURAL**; these sets satisfy B.

> **Latest progress (2026-09-18, full-cut slack):**
> [INDUCTION_CUT_SLACK.md](INDUCTION_CUT_SLACK.md) proves the exact identity
> gamma(X)=max_c(r_X(c)-s(c)). **FALSIFIED:** restricting this maximum to
> optimal full-graph cuts, even on nonautomatic edge-critical cores.
> The symbolic family Petersen disjoint-union B_s (s>=3) has a specified
> five-set with gamma=s+3 but optimal-cut maximum s+2. A slack-one cut
> accounts for the gap. A/B remain **CONJECTURAL**; positive-slack cuts
> must be controlled as part of the same five-set selection bottleneck.

> **Latest progress (2026-09-18, critical-core reduction):**
> [INDUCTION_CRITICAL_CORE.md](INDUCTION_CRITICAL_CORE.md) proves that A and B
> can each be restricted to spanning edge-critical graphs. If C is a
> spanning subgraph with d(C)=d(G), then gamma_G(X)<=gamma_C(X) for every X.
> B's balanced exception transfers because B_k is maximal triangle-free.
> The remaining single target is q+e selection on nonautomatic critical
> cores. General A/B remain conjectural; mixed t=2 is still unresolved.
> No balanced-extension enumeration was repeated.

> **Latest progress (2026-09-18, t=3 two-cut certificates):**
> [BALANCED_EXTENSION_T3.md](BALANCED_EXTENSION_T3.md) proves the strict
> arbitrary balanced-extension theorem for **t>=3**. Only mixed t=2 remains.
> For B_inherit, A plus equality uniqueness through k=3 now suffices;
> neither assumption is established. General A/B and the q+e obstruction
> remain open. Earlier thresholds below are historical.

> **Latest progress (2026-09-18, occupied-type proof):**
> [BALANCED_EXTENSION_TYPE_OCCUPANCY.md](BALANCED_EXTENSION_TYPE_OCCUPANCY.md)
> proves the strict arbitrary balanced-extension theorem for **t>=4**.
> Only mixed t=2,3 remain unresolved. For B_inherit, A plus equality
> uniqueness through k=4 now suffices; neither assumption is established.
> General A/B and the exact q+e obstruction remain open. Earlier thresholds
> below are historical; all homogeneous t=1,...,25 runs are complete.

> **Latest progress (2026-09-18, t=6 repair):**
> [BALANCED_EXTENSION_T6.md](BALANCED_EXTENSION_T6.md) proves the strict
> arbitrary balanced-extension theorem for **t>=6**. Mixed t=2,...,5
> remain unresolved. For B_inherit, A plus equality uniqueness through
> k=6 now suffices. General A/B and the exact q+e obstruction remain open.
> Earlier thresholds and incomplete-run reports below are historical;
> all homogeneous t=1,...,25 certificates are complete with max_gap=0.

> **Latest progress (2026-09-18):**
> [BALANCED_EXTENSION_T7.md](BALANCED_EXTENSION_T7.md) proves the arbitrary
> strict balanced-extension theorem for **t>=7**. The mixed range still
> unresolved is t=2,...,6. For B_inherit, A plus equality uniqueness through
> k=7 now suffices. General A/B and the q+e obstruction remain open.
> Earlier thresholds below are historical.

# The two induction routes for JSP-000058

> **New symbolic progress (2026-09-18):**
> [BALANCED_EXTENSION_COVER_BOUND.md](BALANCED_EXTENSION_COVER_BOUND.md) proves
> the strict arbitrary balanced-remainder theorem for **t>=8**, superseding
> the t>=26 threshold below. Only mixed t=2,...,7 remain unresolved in this
> special case. General A/B and their q+e obstruction remain open.

> **Current coverage correction (2026-09-18):** read
> [BALANCED_EXTENSION_AUDIT.md](BALANCED_EXTENSION_AUDIT.md). All saved
> t=1,...,25 runs are complete with max_gap=0; historical incomplete-run
> statements below are superseded. However, those runs enumerate homogeneous
> neighborhoods within remainder parts. The claimed spanning-supergraph
> reduction for arbitrary mixed neighborhoods is **FALSIFIED**. The symbolic
> t>=26 theorem remains valid; the all-t extension theorem does not yet follow.
> The corrected exact mixed-pattern formula and the single current bottleneck
> are in the audit. General A and B remain conjectural.

Date: 2026-09-18. Scope: only A and B from `structural_analysis.md`,
Section 7. Neither general lemma has been proved or refuted here.
Computational evidence is not proof. Statements marked **Proved** have
arguments below or explicitly identified earlier proofs; reductions are
conditional, and experiments are recorded separately.

## Precise targets and induction

All graphs are finite, simple, undirected; isolated vertices count. Write
`d(G)=min_c b_G(c)=|E(G)|-MaxCut(G)`, where a coloring `c:V(G)->{0,1}` has
`b_G(c)` monochromatic edges. Let `B_k` be the complete C5 blow-up with five
independent parts of size k. Write `G-X=G[V(G)\X]`.

**Conjecture A.** For every integer k>=2 and every triangle-free graph G
with |V(G)|=5k, there exists X subset V(G), |X|=5, such that

`d(G)-d(G-X) <= 2k-1`.

**Conjecture B.** For every integer k>=2 and every triangle-free graph G
with |V(G)|=5k and G not isomorphic to B_k, there exists X subset V(G),
|X|=5, such that

`d(G)-d(G-X) <= 2k-2`.

The set X need not be independent, a cycle, or a module. Both statements
compare independently optimized cuts; neither prescribes a cut of G-X.

**Proved conditional implication for A.** At k=1, a nonbipartite
triangle-free graph contains an odd cycle, necessarily a spanning C5. Every
chord makes a triangle, so its d is 1; all other graphs have d=0. Assume
the desired bound for every triangle-free graph of order 5(k-1). Apply A:
`d(G)<=d(G-X)+2k-1<=(k-1)^2+2k-1=k^2`. The induced remainder is
triangle-free and has the required order. This is ordinary induction.

**Proved conditional implication for B.** The same base case also gives
uniqueness at equality. At each subsequent order, the known calculation
`d(B_k)=k^2` treats the exception. Every other graph satisfies
`d(G)<=(k-1)^2+2k-2=k^2-1`. Thus B gives JSP-000058 and uniqueness of
equality, without needing uniqueness in the induction hypothesis. It also
implies A: in B_k delete a transversal, leaving B_(k-1), with increment
exactly 2k-1. B is a substantially stronger target than JSP-000058 alone.

## Exact cut identity and the first obstruction

**Proved.** Fix X, put H=G-X. For each coloring c of H define

`e_X(c)=min_{a:X->{0,1}} [ b_{G[X]}(a) + number of monochromatic X-H edges ]`,

and `q_H(c)=b_H(c)-d(H)>=0`. Partitioning all colorings of G by their
restriction to H gives the exact identity

`gamma_G(X):=d(G)-d(H)=min_c [q_H(c)+e_X(c)].`                 (1)

Consequently A asks for some X and c with `q_H(c)+e_X(c)<=2k-1`;
B asks for `<=2k-2` under its additional hypothesis. One must account for
the cost q of changing the remainder's optimum as well as extension cost.
Restricting to optimal c gives only an upper bound on gamma, not equality.

**First genuinely missing step for A.** Select five vertices and a remainder
coloring for which the sum in (1) is at most 2k-1. Triangle-freeness alone
has not yet supplied the needed simultaneous control of q and e. The
elementary estimates below do not reach this threshold in the unresolved
case.

**First genuinely missing step for B.** Even granting A, show that a
nonbalanced graph has a choice with sum at most 2k-2: equivalently, exclude
a nonbalanced graph for which every five-vertex deletion has gamma>=2k-1.
Local rigidity under changing one vertex does not address five coordinated
changes or cut reoptimization. A special balanced-remainder case is proved
below; it is not the general missing step.

**Direction of inequality matters.** If c is optimal on G and its
monochromatic edges incident with X number r, restriction gives
`d(H)<=d(G)-r`, hence `gamma_G(X)>=r`. Bounding r from above does not prove
A. Likewise `E[min_c b_H(c)]<=min_c E[b_H(c)]`; sampling remainders does
not supply the required lower bound on their d.

## Elementary partial proofs

**Proved extension estimates.** Let h=e(G[X]) and z=e(X,H). Randomly color
X independently, keeping an optimal cut of H fixed. Also try an optimal
cut of G[X] and its global reversal. These give, respectively,

`gamma_G(X)<=floor((z+h)/2)`,
`gamma_G(X)<=d(G[X])+floor(z/2)`.                            (2)

Here d(G[X])<=1 by the five-vertex base case. Either estimate proves A or
B whenever its right side meets the relevant threshold. In particular,
`z+h<=4k-1` suffices for A, and `z+h<=4k-3` for B. These are sufficient
conditions, not assertions that such X always exists.

Deleting vertices v_1,...,v_5 in order, and writing G_i=G-{v_1,...,v_i},
the single-vertex extension bound telescopes to

`gamma_G(X)<=sum_{i=1}^5 floor(deg_{G_(i-1)}(v_i)/2)`.       (3)

For instance, five vertices of original degree at most r suffice when
`5 floor(r/2)` meets the threshold. Another proved automatic case is
`d(G)<=2k-1` for A, or `d(G)<=2k-2` for B, since d(H)>=0.

**Proved minimum-degree boundary.** A triangle-free graph on 5k vertices
with minimum degree at least 2k is either bipartite or B_k. Here is a
first-principles proof, including the equality case. In a nonbipartite G
take a shortest odd cycle C of length l>=5. It is chordless. An outside
vertex has at most two neighbors on C: otherwise their cyclic gaps are
at least two, one gap is odd, and that odd gap is at most l-4, producing
a shorter odd cycle through the outside vertex. Therefore
`sum_{v in C} deg(v)<=2l+2(5k-l)=10k`. Minimum degree 2k forces l=5
and equality throughout. Every outside vertex has exactly two neighbors
on C. They are nonconsecutive. Assign it to type i when these are the
neighbors of cycle vertex i, and assign cycle vertex i to type i itself.
Vertices of the same or nonconsecutive types share a cycle neighbor, so
may not be adjacent. All five types are nonempty. If their sizes are a_i,
minimum degree implies `a_(i-1)+a_(i+1)>=2k` for every i. Summing forces
equality in all five inequalities; solving them gives a_i=k. Every vertex
must have all 2k allowed neighbors, proving G=B_k.

Thus A and B hold in this boundary regime. Any still unresolved graph for
either lemma may be assumed nonbipartite and to have minimum degree at most
2k-1. This alone is inadequate: the five costs in (3) can have scale 5k,
whereas the target has scale 2k.

## A strict balanced-remainder extension theorem

**Proved here.** Let t>=26 be an integer. If a triangle-free graph G on
5(t+1) vertices contains an induced B_t, then

`d(G)<=(t+1)^2`, with equality if and only if G is B_(t+1).

In particular, for k>=27, if G-X=B_(k-1), this particular X satisfies A;
if G is nonbalanced it satisfies B.

**Proof.** Put H=B_t, with parts A_i, and X=V(G)\V(H), |X|=5.
The H-neighborhood of each x in X is independent. Its support meets at
most two nonconsecutive parts, so choose a type f(x) with
`N_H(x) subset A_(f(x)-1) union A_(f(x)+1)`. This also covers empty
and single-part neighborhoods. Put `D_x=2t-|N_H(x)|` and `D=sum D_x`.

Use each of the five part-respecting optimal colorings of H, indexed by
its sole monochromatic cycle edge. Extend by giving x the color of its
type f(x). Each X-H edge is monochromatic in one of the five colorings.
An edge xy inside X is monochromatic in one, three, or five colorings
according as its types are consecutive, distinct nonconsecutive, or equal.
Let W be the sum of these weights over E(G[X]). The average additional
cost of these five extensions is exactly

`(10t-D+W)/5=2t+(W-D)/5`.                                 (4)

There are at most six edges in the triangle-free five-vertex graph G[X],
so W<=30. For completeness, for every edge uv in a triangle-free graph of
order 5, deg(u)+deg(v)<=5. Summing and applying Cauchy--Schwarz gives
`4m^2/5<=sum deg(v)^2<=5m`, hence m<=6.

If some X-edge has nonconsecutive or equal types, its endpoints have
disjoint neighborhoods in at least one common allowed H-part of size t.
Their combined deficits are at least t (at least 2t for equal types).
Thus D>=t>=26 and W-D<=4. One extension has additional cost strictly
less than 2t+1, hence at most 2t by integrality. This proves the strict bound.

Otherwise all X-edges join consecutive types. G is then a spanning
subgraph of a C5 blow-up with part sizes `t+|f^(-1)(i)|`, totaling 5(t+1).
The proved blow-up formula and AM--GM in `structural_analysis.md` give
`d<= (t+1)^2`, strictly unless these sizes all equal t+1 and the spanning
subgraph is complete. Indeed every proper spanning subgraph of B_(t+1)
has d<=(t+1)^2-1, by deleting one edge and using monotonicity. Equality
therefore forces G=B_(t+1), which attains it. This completes the proof.

The constant 26 is deliberately coarse. No claim for t=1,...,25 follows
from this argument. Its five explicitly chosen remainder cuts avoid the
general cut-selection problem only because the remainder is known exactly.

## Weaker versions that still suffice

### Direct terminal cases, proved from first principles

Let n=5k and m=|E(G)|. A random cut gives `d(G)<=floor(m/2)`, so the
desired bound holds if m<=2k^2+1, strictly if m<=2k^2-1.

For each v, the cut `(N(v),V\N(v))` has size
`sum_{u in N(v)} deg(u)`, because N(v) is independent. Averaging over v
and using Cauchy--Schwarz proves

`MaxCut(G)>=sum_v deg(v)^2/n>=4m^2/n^2`,
`d(G)<=m-4m^2/n^2`.                                      (5)

The right side decreases for m>=n^2/8 and equals k^2 at m=5k^2.
Thus m>=5k^2 is another terminal case, strictly when m>5k^2. If
m=5k^2 and d(G)=k^2, equality in the degree-square inequality forces
regular degree 2k. The minimum-degree proof above forces G=B_k (the
bipartite alternative cannot have d=k^2). Hence equality is classified
throughout this dense terminal range. This does not prove A or B there:
a bound on d(G) alone is not a lower bound on d(G-X).

### A restricted to maximal graphs in the unresolved density interval

**Sufficient conjectural weakening A_M.** Require A only for maximal
triangle-free graphs G of order 5k with

`2k^2+1 < |E(G)| < 5k^2`.

They are connected: vertices in distinct components could be joined
without making a triangle. Their minimum degree is at most 2k-1.

**Proved reduction.** Complete any G, by adding edges, to a maximal
triangle-free M on the same vertices. Monotonicity gives d(G)<=d(M).
The terminal cases handle M outside the interval. Inside, apply A_M and
the order-5(k-1) induction hypothesis to M-X. Therefore A_M suffices for
JSP-000058. This argument does not infer A for a subgraph from A for M:
the increments themselves are not known to be monotone under adding edges.

### B restricted to maximal graphs, and a weaker strictness rule

**Sufficient conjectural weakening B_M.** Require B only for maximal
triangle-free graphs G of order 5k with

`2k^2 <= |E(G)| < 5k^2`.

**Proved reduction.** Complete G to M as above. Sparse M has a strict
bound; dense M has a strict bound unless M=B_k. In the latter case a
proper spanning subgraph G has d(G)<=k^2-1 by the previously proved
single-edge deletion argument. In the remaining interval B_M and induction
give d(M)<=k^2-1. Thus B_M implies the full bound and equality uniqueness.
These terminal cases explain the slightly different lower endpoints for
A_M and B_M.

**Sufficient conjectural weakening B_inherit.** For each nonbalanced
triangle-free G of order 5k, require a five-set X such that

- `gamma_G(X)<=2k-1`, and
- if G-X is B_(k-1), then `gamma_G(X)<=2k-2`.

This is weaker than B: it allows increment 2k-1 when the remainder is
nonbalanced. Induct simultaneously on the bound and equality uniqueness.
For a nonbalanced remainder use `d(G-X)<=(k-1)^2-1`; for a balanced
remainder use the second clause. Either way d(G)<=k^2-1. Treat G=B_k
directly, as before. This proves the conditional implication exactly.

The balanced-remainder theorem supplies the second clause automatically
for k>=27. Consequently **A plus equality uniqueness through k=26 would
imply equality uniqueness at all orders**. The required finite base is
not established here; the saved exhaustive evidence reaches only k=2.
This is a reduction of B's intended consequence, not a proof of B.

### Variable block sizes and the deficit trap

**Another sufficient weakening of A.** For each k>=2 and triangle-free
G of order 5k, allow some integer 1<=r<k and some X of size 5r satisfying
`d(G)-d(G-X)<=2kr-r^2`. Strong induction then gives
`d(G)<=(k-r)^2+2kr-r^2=k^2`. A is the special case r=1. The analogous
strict threshold `2kr-r^2-1` for nonbalanced G implies the strict result,
with B_k handled directly. No general block-selection theorem is proved.

It is tempting to spend the remainder's slack
`s=(k-1)^2-d(G-X)`. But the condition
`gamma_G(X)<=2k-1+s` is algebraically identical to d(G)<=k^2, for every
X. The strict version is identical to d(G)<=k^2-1. Without an independent
estimate or construction, these are restatements, not progress.

## Targeted literature checks

The searches addressed three specific possible bridges: minimum degree
to a suitable deletion set; comparison with a pentagon blow-up; and cut
extension bounds retaining the sharp increment. No broad new graph search
was launched. Links below are primary research sources; implications for
the present route are our deductions, not claims made by their authors.

1. **Minimum-degree bridge.** Reiher's
   [Quickly proving the Andrásfai–Erdős–Sós theorem](https://arxiv.org/abs/1212.2521)
   describes the classical minimum-degree theorem and its extremal graphs.
   In the triangle-free case the strict threshold is 2n/5. The elementary
   proof above independently includes the needed equality boundary.
   It resolves the high-minimum-degree case but cannot turn a vertex of
   degree approximately 2k into five vertices with total extension cost
   approximately 2k. This is the precise obstruction to using it for A;
   its balanced exception matches B but does not prove B below the threshold.

2. **Blow-up comparison bridge.** Erdős, Győri and Simonovits,
   [How many edges should be deleted to make a triangle-free graph bipartite?](https://korandi.org/docs/misc/erdos_gyori_simonovits.pdf),
   Theorem 2, compare graphs in the range m>=n^2/5 with a C5 blow-up of
   the same order having at least as many edges and at least as large d.
   Their Theorem 4 is a stability statement under an additional closeness
   hypothesis. The comparison graph need not be an induced subgraph of G.
   Thus it does not produce the remainder in A or B. Even a small quadratic
   edit error would not automatically yield B's one-edge saving. The dense
   terminal bound needed for our weaker routes already follows from (5).

3. **Extension and intermediate-density bridge.** Balogh, Clemen and
   Lidický, [Max Cuts in Triangle-free Graphs](https://arxiv.org/html/2103.14179),
   Theorem 1.2, prove, for sufficiently large n, d<=n^2/23.5 generally
   and d<=n^2/25 in density ranges m/binom(n,2)<=0.2486 or >=0.3197.
   Their Section 2.2, Lemma 1, bounds extension after minimum-degree
   removal by `3(n^2-m^2+n-m)/32`, where m there is the remaining order.
   Section 2.1 constructs cuts from small rooted configurations.
   **Our deduction:** setting the remaining order to n-5 makes that
   extension bound `15n/16-15/8`, much larger than `2n/5-1`.
   It does not supply A's increment or B's strictness. The density results
   can instead terminate an induction on graphs meeting their hypotheses;
   they do not compare two independently optimized induced subgraphs.
   Care is needed with finite orders: under a uniform t-fold blow-up,
   density tends to `2|E(G)|/n^2`, not `|E(G)|/binom(n,2)`.
   For example the large-order theorem transfers to every finite G with
   `2|E(G)|/n^2 < 0.2486` or `>=0.3197`, by taking t large and using
   `d(G[t])=t^2 d(G)`. The strict low-density inequality avoids an endpoint
   issue. These are bound-only terminal cases, not equality classifications.

No checked result supplies the missing lower bound on the deletion distance
of some (5k-5)-vertex induced subgraph. This is a statement about the checked
sources, not a claim that an exhaustive literature review has been done.

## Symbolic attempts to refute A and B

### Balanced graphs: sharpness and failure of arbitrary deletion

**Proved.** For B_k, a transversal has gamma=2k-1, so A's constant cannot
be reduced for all graphs. No five-deletion has a smaller increment:
every remainder is a C5 blow-up of order 5(k-1), hence has d<=(k-1)^2.
For k>=5, deleting all five vertices from one part instead gives
`d(G-X)=k(k-5)` and gamma=5k. Thus “every X works” is false even on
the equality family. This does not refute the existential A.

### Nonbalanced blow-ups: transversal rules fail

The exact formula `d(B(a))=min_i a_i a_(i+1)` makes these symbolic,
all-parameter calculations independent of any MaxCut computation.

**Refuted strengthening of B.** For every integer k>=5 take cyclic sizes
`a=(1,2k-1,3,k-2,2k-1)`. Their sum is 5k and d=2k-1. Every transversal
empties the singleton part, leaving a bipartite graph. Its increment is
2k-1, exceeding B's 2k-2. But deleting five vertices from the second
part leaves d=2k-6, for increment 5<=2k-2. Hence this is a counterexample
to the transversal prescription, not to B.

**Refuted strengthening of A.** For every integer s>=1 take sizes
`a=(15s,150s,45s,50s,150s)`, so k=82s and d=2250s^2. A transversal
leaves d=2250s^2-165s+1. Its increment 165s-1 exceeds A's 164s-1.
Instead delete three vertices from the second part and two from the fifth.
The remainder has d=2250s^2-45s, so the increment 45s satisfies even B.
Thus restricting X to a C5 is invalid for both targets: a five-cycle in
a C5 blow-up is necessarily transversal. In particular A cannot be proved
just by selecting a particularly favorable induced pentagon.

### Perturbed equality and disconnected constructions

**Proved non-counterexamples.** For B_k with one edge removed, d=k^2-1.
Choose a transversal containing one endpoint of that missing edge. The
remainder is B_(k-1), so gamma=2k-2: B is sharp on this infinite
nonbalanced family. Indeed no remainder has d>(k-1)^2, because it is a
spanning subgraph of a C5 blow-up of that order.

For `G=B_p disjoint-union B_q`, p,q>=1 and k=p+q, deletion distance is
additive. Delete a transversal in B_p. The increment is 2p-1 (also valid
for p=1, with an empty remainder component), which is <=2k-2. This
natural disconnected construction cannot refute B.

**Exact symbolic counterexample to ignoring q in (1).** Let H be the
tree consisting of an edge uw with four leaves at u and four at w.
Add x adjacent to all eight leaves and add four isolated vertices to
form a triangle-free G on 15 vertices. Let X contain x and the four
isolates. H is connected bipartite, so its optimal cut is unique up to
reversal and splits x's neighbors four-four. Thus
`min_{c optimal on H} e_X(c)=4`. But d(G)=1: every odd cycle uses uw,
deleting uw gives a bipartite graph, and a five-cycle shows d>=1.
Consequently gamma=1. A nonoptimal cut of H with q=1 permits e_X=0.
The optimal-remainder-only expression is not the exact increment.
This example is not a counterexample to A or B, which hold automatically
because d(G)=1.

No symbolic counterexample to A or B itself was obtained. Their stronger
prescriptions failing is useful information, not a refutation of the targets.

## Computational evidence (separate from the proofs)

### Previously saved evidence, not rerun

`results/structural_analysis.json` and `structural_analysis.md`, Section 8,
record zero A/B failures on all 12,172 triangle-free isomorphism classes
of order 10 and on 8,237 specified labeled order-15 inputs. The latter
corpus is not exhaustive. The balanced graph was tested using A's threshold
because B excludes it. At order 10 all but the balanced graph pass A
automatically. These data are evidence only and do not certify a larger base
range for the equality induction described above.

### New bounded test: the specific transversal claim

Enumerated all positive integer C5 weight vectors of sum 5k, for 2<=k<=8.
Only the fixed transversal deletion was tested, by the proved product
formula. Failure counts below are **not failures of A or B**.

| k | Ordered vectors | A-threshold failures | B-threshold failures (excluding balanced) |
|---|---:|---:|---:|
| 2 | 126 | 0 | 0 |
| 3 | 1,001 | 0 | 0 |
| 4 | 3,876 | 0 | 0 |
| 5 | 10,626 | 0 | 5 |
| 6 | 23,751 | 0 | 10 |
| 7 | 46,376 | 0 | 15 |
| 8 | 82,251 | 0 | 50 |

The first B-threshold failure was (1,9,3,3,9), yielding the symbolic
family above. The symbolic A-threshold failure at k=82 is outside this
bounded experiment; its algebra, not an extrapolation, verifies it.

Reproduce from the repository root (standard library only):

```sh
python3 - <<'PY'
from itertools import combinations
for k in range(2,9):
    count = fa = fb = 0
    for bars in combinations(range(1,5*k),4):
        a = tuple(y-x for x,y in zip((0,)+bars,bars+(5*k,)))
        d = min(a[i]*a[(i+1)%5] for i in range(5))
        h = min((a[i]-1)*(a[(i+1)%5]-1) for i in range(5))
        count += 1
        fa += d-h > 2*k-1
        fb += a != (k,)*5 and d-h > 2*k-2
    print(k,count,fa,fb)
PY
```

### New bounded test: sharpening the balanced-remainder argument

For a triangle-free graph F on the five new vertices and a type map f,
let `S_j={x: f(x)=j-1 or j+1}` and

`L=10-sum_{j=0}^4 alpha(F[S_j])`.

**Proved inequality.** Each vertex of H-part A_j has an independent
neighborhood in F[S_j], so at most alpha(F[S_j]) new neighbors. Summing
over the five parts shows `D>=tL`. This strengthens D>=t in the proof.

**Experiment only.** Enumerating all 388 labeled triangle-free F and
625 type maps with f(0)=0 (rotation removes the other five equivalent
choices), restricted to maps having an incompatible edge, gave:

| L | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| Largest W observed | 12 | 20 | 24 | 30 | 21 | 25 |

No other L occurred. This suggests that the same proof works for t>=8
if these finite maxima are independently certified or proved by cases.
The formally stated first-principles theorem above retains t>=26.
For L=1, W=12 is realized by a four-leaf star whose center has type 0
and leaves type 2. The averaging estimate alone therefore cannot force
`W-tL<=4` when t<=7; improving constants alone is insufficient there.
An extension may still have a better cut than this average.

Reproduction of the complete bounded experiment:

```sh
python3 - <<'PY'
from itertools import combinations, product
pairs = list(combinations(range(5),2))
maxima = {}; graphs = 0
for mask in range(1024):
    E = [e for i,e in enumerate(pairs) if mask>>i&1]
    if any(all(e in E for e in ((a,b),(a,c),(b,c)))
           for a,b,c in combinations(range(5),3)):
        continue
    graphs += 1
    independent = [s for s in range(32)
                   if all(not(s>>u&1 and s>>v&1) for u,v in E)]
    alpha = [max(s.bit_count() for s in independent if s & ~T == 0)
             for T in range(32)]
    for tail in product(range(5),repeat=4):
        f = (0,)+tail
        if not any((f[u]-f[v])%5 not in (1,4) for u,v in E):
            continue
        W = sum(5 if f[u]==f[v] else
                1 if (f[u]-f[v])%5 in (1,4) else 3 for u,v in E)
        S = [sum(1<<v for v in range(5) if (f[v]-j)%5 in (1,4))
             for j in range(5)]
        L = 10-sum(alpha[s] for s in S)
        assert L > 0
        maxima[L] = max(maxima.get(L,0),W)
print(graphs, dict(sorted(maxima.items())))
PY
```

## Exact next task and stopping point

The best next action is a bounded attack on the **balanced-remainder
extension claim for t=1,...,25**, especially t<=7 where the average bound
fails. Keep F on five new vertices and encode each vertex of each H-part
by its independent neighborhood in F. Counts of these finitely many
patterns are nonnegative integers summing to t in each part. Test whether
one of the five optimal cuts of H, extended by any of the 32 colorings of
X, always attains the strict bound for nonbalanced G. If this restricted
cut claim fails, retain the exact pattern counts as a symbolic obstruction
and allow nonoptimal H cuts using (1). Do not infer failure of B merely
from failure of these candidate cuts.

This is useful because it targets the remaining strict transition in
B_inherit; it does not claim to resolve A. No large new computation has
been started. The two general missing steps remain those explicitly
identified following (1).

## Bounded balanced-remainder verification status (2026-09-18)

**COMPUTATIONALLY VERIFIED (reduction, not the final inequality).** The
finite check is implemented in
`scripts/check_balanced_extension.py` and the optimized companion
`scripts/check_balanced_extension.cpp`. It enumerates all 388 labeled
triangle-free graphs F on X={0,...,4}, all 625 type maps with f(0)=0
(rotation normalization), and all inclusion-maximal independent choices
I_j in each allowed type support S_j. For a fixed choice, the exact forced
deficit is

`D=t Σ_j(2-|I_j|)=10t-t Σ_j|I_j|`.

This corrected formula is for homogeneous patterns I_j, each repeated t
times. The previous displayed formula omitted their multiplicity t.

An internal edge xy forces x and y to have disjoint neighborhoods in every
common remainder part. Therefore the exact minimum possible deficit over
all neighborhood subsets with the given (F,f) is

`D_min=t(10-Σ_j α(F[S_j]))`,

where S_j={x:f(x)=j−1 or j+1} and α is independence number. This identity
is proved by assigning each of the t vertices in A_j to an independent set
of F[S_j], independently for each j. The earlier 388×625 diagnostic
computed this quantity and the internal-edge monochromatic weights; its
largest W values by L=10−Σα were
`L=1:12, 2:20, 3:24, 4:30, 5:21, 6:25`.

**COMPUTATIONALLY ATTEMPTED, NOT CERTIFIED.** The exact maximal-extension
run was started for every t=1,...,25. It was stopped before completion
because the Cartesian product of maximal independent-set choices and ten-bit
cut evaluations was too large for this session. No output was accepted as
evidence, and no t-specific pass/fail conclusion was drawn. In particular,
there is currently no explicit counterexample configuration for any t, and
there is no exhaustive finite proof for t<=25.

**CONJECTURAL.** The desired balanced-remainder statement remains:
for every 1<=t<=25, every triangle-free extension G of B_t by five
vertices satisfies d(G)<= (t+1)^2, with equality only for B_(t+1).
The t>=26 theorem earlier in this file is proved. Consequently the combined
all-t theorem has not been established: only the range t>=26 is proved.

### Optimized exact runs (2026-09-18)

**COMPUTATIONALLY VERIFIED.** The optimized C++ enumerator
`scripts/check_balanced_extension.cpp` keeps the same exhaustive search
space. For each cut it precomputes a cost polynomial `c0+c1*t+c2*t^2`,
uses 512 cuts modulo complementation, and checkpoints after every 1000
configurations. Per-t artifacts are in `results/balanced_extension/t1.json`
through `t4.json`; resumable partial state uses the corresponding
`tN.checkpoint.json` files. Each completed run examined all 388 triangle-free
F, all 625 normalized type maps, and 1,245,367 maximal-neighborhood choices.

| t | configurations | maximal choices | max d-(t+1)^2 | result |
|---|---:|---:|---:|---|
| 1 | 242,500 | 1,245,367 | 0 | holds |
| 2 | 242,500 | 1,245,367 | 0 | holds |
| 3 | 242,500 | 1,245,367 | 0 | holds |
| 4 | 242,500 | 1,245,367 | 0 | holds |

The witness saved in each file attains equality and is a balanced C5 blow-up
extension; it is a maximizing witness, not a counterexample. No t-specific
counterexample was found for t<=4. The remaining t=5,...,25 runs have the
same exact search size and measured runtime about two minutes per t on this
environment (approximately 38--45 minutes total). They were not started in
this window, so t<=25 is not fully computationally verified.
