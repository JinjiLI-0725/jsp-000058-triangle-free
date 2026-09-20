# Zero selection margin: exact structure and limits

## Outcome and scope

Zero maximum selection margin does **not** force a C5 blow-up, or even a
graph admitting a homomorphism to C5. The corrected d=8 witness is an explicit
counterexample to both statements. Its zero-margin five-sets also need not
induce C5. A common exact feature of the two audited zero-maximum graphs is
instead tight deletion together with coverage of optimal five-set colorings
by global optimal colorings. Allowed coordinated flips realize that coverage.

The evidence comes exclusively from
`SELECTION_CLAIM_N15_CORRECTED_REPORT.md` and
`results/selection_exact_corrected_v2`, whose manifest hashes were verified
before analysis. The invalid earlier audit is not used. This analysis examines
all zero maximizers in the two specified graphs, and checks a restriction
criterion on all 3,003 five-sets of each. It does not sample new graphs.

Definitions are those of the coordinated-flip selection note. Put B=2k-1,
H=G-X, q=d(G)-d(H), and let A_X be **all** optimal colorings of G[X], including
reversals. R(H) consists exactly of independent induced subsets, complete
bipartite induced subsets with two nonempty sides, and their complements.
For an optimal core coloring c, define

    C_c(a) = min_{S in R(H)} [b_G(c^S union a)-d(H)],
    U_X = min_{c optimal H} average_{a in A_X} C_c(a),
    M(X) = B-U_X.

In the n=15 analysis B=5. Distinguish a local zero M(X)=0 from a graph whose
**maximum** over X is zero: a graph with positive maximum can still have
local zero sets.

## 1. Complete finite characterization

| Feature | B3 | d=8 A-tight witness |
|---|---:|---:|
| graph6 | `NFz_ww[?wF?[wFwF[B_` | `NEL_FF_DgAeOATbBPp?` |
| Edges | 45 | 36 |
| Global optimal colorings, including reversals | 70 | 54 |
| Zero-margin maximizing five-sets | 243 | 301 |
| Minimum q over all five-sets | 5 | 5 |
| Five-sets with q=5 | 243 | 321 |
| Automorphism orbits of zero sets | 1 | 86 |
| Isomorphism types of G[X] at zero sets | 1 | 12 |
| Isomorphism types of H at zero sets | 1 | 16 |
| d(H) at zero sets | 4 | 3 |
| All optimal base core colorings attain Phi_X | 243 sets | 271 sets |
| Some base serves every assignment using penalty-zero flips | 243 sets | 283 sets |

The d=8 automorphism group has order 4. Its zero sets split into 65 orbits
of size 4, 20 of size 2, and one of size 1. `summary.json` lists every orbit
and every core isomorphism class, with all its member X. This is a labeled
enumeration, not a proposed universal forbidden-subgraph classification.

For **each of these two fixed graphs**, the following equivalence was checked
on all 3,003 five-sets:

    M(X)=0
      iff q(X)=5 and the restriction map from optimal colorings of G
          covers every optimal coloring of G[X].                         (F)

This supplies a second characterization of all 544 zero sets, independent
of their naming or automorphism representatives. The audit enumerates all
32,768 global colorings to obtain the optimal colorings, then computes their
restrictions directly. The reverse implication in (F) is a **finite result**;
surjectivity alone does not supply allowed flips from one common base in a
general graph. Section 4 gives the precise general statement that is proved.

### B3

The five open-neighborhood classes are

    {0,1,2}, {3,4,5}, {6,7,8}, {9,10,11}, {12,13,14}.

The 243 zero sets are **exactly** the transversals of these classes. Each
G[X]=C5, H=B2, d(G[X])=1, z=e(X,H)=20, Phi_X=6, and U_X=5.
Every core vertex has two neighbors in X. The five boundary-neighborhood
classes coincide with the five core twin classes and each has size 2.
Consecutive core classes are completely joined; other pairs have no edges.

Each core has 30 optimal colorings including reversal, not just the ten
part-constant ones. Ten are part-constant; the other twenty split one neutral
two-vertex part. Every one of the thirty is a maximizing base for Phi_X.
For every optimal X assignment, **all** allowed maximizing flips in the
audited records have core penalty zero. The files retain all such flips,
including ones involving partial parts; they are not restricted to unions
of whole twin classes. Section 5 proves the transversal characterization
for balanced B_k generally.

### The d=8 witness

Its degree histogram is 4:5, 5:8, 6:2. All fifteen open neighborhoods are
distinct, so it has no nontrivial independent twin class. In particular it
cannot be a complete C5 blow-up with fifteen vertices.

Its zero sets have the following induced graphs:

| G[X] | Count |
|---|---:|
| P4 plus an isolated vertex | 70 |
| C4 with a pendant vertex | 48 |
| P5 | 48 |
| Subdivided claw (one edge of K1,3 subdivided) | 34 |
| K1,3 plus an isolated vertex | 28 |
| P3 plus two isolated vertices | 20 |
| P3 plus K2 | 15 |
| Two disjoint edges plus an isolated vertex | 12 |
| K2,3 | 10 |
| C4 plus an isolated vertex | 8 |
| K1,4 | 4 |
| C5 | 4 |

Thus 297 zero sets have d(G[X])=0 and only four have d(G[X])=1.
Every zero core has d(H)=3; the number of optimal core colorings ranges from
6 to 40, including reversals. The full histogram and every coloring are saved.

Boundary edge counts z=12,13,14,15,16,17,18,19 occur respectively
10,8,42,54,79,70,30,8 times. At zero margin Phi_X=d(G[X])+z/2-5,
ranging from 1 to 9/2. There are 6--10 boundary-neighborhood classes,
with sizes at most 3. In ten zero sets all ten core vertices even have
distinct neighborhoods in X. For neighborhoods **inside H**, 187 zero cores
have ten singleton classes, 92 have one pair and eight singletons, and 22
have two pairs and six singletons. This differs fundamentally from B2's
five pairs. Exact boundary matrices and classes for every X are saved.

All maximizing bases serve every optimal X assignment at total cost 5.
But 18 zero sets have no base that can do this using only penalty-zero flips.
For example take

    X = {0,1,2,6,8},  H = {3,4,5,7,9,10,11,12,13,14},
    c^{-1}(1) = {4,5,7,9,11},   a^{-1}(1) = {0,1,2},
    S = {4,5,7,11,12,13,14}.

Here G[X]=K1,3 plus an isolated vertex. S is allowed because its complement
{3,9,10} induces K1,2. Flipping S raises core cost from 3 to 4, while the
extension cost falls from 8 to 4: extension saving 4, core penalty 1,
net gain 3, total extension-plus-penalty 5. For this base and assignment S
is the unique maximizing allowed flip. Across all bases, this X has no
penalty-zero simultaneous cover. General allowed optimal flips in the d=8
records can have penalties up to 4. Thus even zero selection margin does
not restore a universal zero-penalty exchange principle.

## 2. A short obstruction to any C5-blow-up interpretation

The d=8 witness has no graph homomorphism to C5. Here is a direct certificate,
in addition to the tested exact CSP checker.

The vertices (0,13,11,6,14), in that order, form a C5. Any homomorphism of
this cycle to C5 must be an automorphism: a five-step closed walk on C5 has
steps +/-1, whose sum is a multiple of 5; with five steps it must be +/-5,
so all steps have the same sign. Relabel the target so these vertices map
to 0,1,2,3,4 in order.

Vertex 3 is adjacent to vertices 0 and 11, so its image must be 1, the
unique common neighbor of target vertices 0 and 2. Vertex 5 is adjacent
to vertices 13 and 14, so its image must be 0, the unique common neighbor
of target vertices 1 and 4. But vertex 1 is adjacent to both 3 and 5.
Target vertices 1 and 0 have no common neighbor. Contradiction.

All edges in this eight-vertex certificate are saved and checked. Since
every subgraph of a C5 blow-up has a homomorphism to C5, the witness is not
even such a subgraph. Consequently neither its four C5 zero sets nor its
other 297 zero sets can be transversals of a C5 template for the whole G.
Calling this witness 'C5-blowup-like' would need a genuinely weaker,
explicit definition; homomorphic containment is already too strong.

## 3. Counterexamples to stronger statements

* **max_X M(X)=0 implies G is C5-homomorphic:** false by the d=8 witness
  and the certificate above. Literal C5 blow-up is therefore also false.
* **M(X)=0 implies G[X]=C5:** false for X={0,1,2,6,8} in that witness.
* **Zero margin permits a common penalty-zero cover:** false for the same X;
  the audit finds eighteen such zero sets in this witness.
* **q(X)=5 implies M(X)=0:** false for X={0,1,4,10,12} in the same witness.
  Here q=5 but M=-3/8. There are sixteen optimal assignments on X; fourteen
  have optimized cost 5 and two have cost 8 at every maximizing base.
  The two assignments, local masks 14 and 17 in sorted X order, do not
  extend to any global optimal coloring. The average is 43/8, not 5.
  In total twenty q=5 sets have negative margin: fourteen with -1/2,
  four with -3/8, and two with -1/4.
* **Local zero margin implies q(X)=5:** false in the corrected corpus's
  first non-balanced graph, graph6 `N????KEWOprqxa}W^K?`, for
  X={1,2,3,5,10}. Here d(G)=7, d(H)=3, q=4, but M=0. This graph's maximum
  margin is 1, so it does not refute a statement conditional on *global*
  maximum zero. The example was recomputed with the exact allowed family.

## 4. General tight-cover lemma — proved, without geometric conclusions

**Lemma.** Suppose q(X)=B. Then M(X)=0 if and only if there is one optimal
core coloring c such that **every** a in A_X has a global optimal extension
of the form c^S union a with S in R(H).

**Proof.** Every full coloring has at least d(G) monochromatic edges, so
C_c(a)>=d(G)-d(H)=B for every c,a. If M(X)=0, choose a minimizing base c:
the average of its C_c(a) is B, and all weights are strictly positive.
Every term therefore equals B. Choose a minimizing S for each a; its full
coloring is global optimal. Conversely such a cover gives U_X<=B, while
the same pointwise lower bound gives U_X>=B. Thus U_X=B and M(X)=0.

In fact every maximizing base has this covering property when q=B and M=0.
For any such base, an allowed S maximizes gain for a **exactly when**
c^S union a is global optimal. This characterizes all the maximizing flips
in terms of optimal-cut incidence, without imposing a penalty cutoff.

This is the precise common certificate present at every zero set in the two
graphs. It is necessary and sufficient within the tight-deletion class;
it is not a five-part neighborhood theorem. There is no claim of a uniquely
'weakest' geometric feature. Removing common-base reachability by R(H)
gives ordinary restriction surjectivity, a necessary condition when q=B in
general and, by the additional finite audit, sufficient when q=5 in these
two graphs.

For arbitrary q define the nonnegative excess

    gamma_X = min_c average_a [C_c(a)-q].

Then the exact identity is M(X)=B-q(X)-gamma_X. This explains why local
zero need not imply tight deletion, and identifies exactly where a converse
based only on q can fail. No triangle-free structure theorem is hidden in
this identity or the tight-cover lemma.

## 5. Geometric statements that are actually proved

### Balanced blow-up rigidity of the selected set

For every k>=2, in G=B_k,

    M(X)=0  iff X is a transversal of the five parts.                   (B)

Moreover every nontransversal has M(X)<=-1.

For a blow-up with part sizes a_i, d=min_i a_i a_{i+1}. To see this, round
each part to a constant color without increasing monochromatic edge count:
with other parts fixed, the objective is linear in the number of vertices
of that part on either side. Among part-constant colorings of the weighted
odd cycle, at least one edge is monochromatic and the cheapest single edge
can be made the only monochromatic edge. This also covers zero-size parts.

Let r_i=|X intersect V_i|. The formula gives

    q(X)=max_i [k(r_i+r_{i+1})-r_i r_{i+1}],  sum_i r_i=5.

If X is not transversal some adjacent sum s is at least 3. Otherwise the
five sums, whose total is 10, all equal 2; the odd-cycle equations force
every r_i=1. Since 3<=s<=5, the displayed loss is at least

    ks-floor(s^2/4) >= 2k.

The three cases are 3k-2, 4k-4, and 5k-6; all are at least 2k for k>=2.
Thus U_X>=q(X)>=2k and M(X)<=-1 for a nontransversal.

For a transversal, H=B_(k-1) and q=2k-1. Put t=k-1 and choose part colors
(0,0,1,0,1) on H. The ten optimal C5 assignments on X are obtained from
these part colors by flipping part index sets

    empty, {1}, {1,2}, {0,4}, {0}, and their complements.

These are independent parts, complete bipartite adjacent-part pairs, or
complements, hence allowed. Matching each target assignment on the core
keeps its cost t^2 and has extension cost 2t+1. The tight-cover lemma gives
M=0. This proves (B) for the whole balanced family, not merely B3.

A checkable density corollary slightly broadens the starting hypothesis.
Suppose a graph on 5k vertices has a surjective homomorphism to C5 and
minimum degree at least 2k. If the five nonempty fibers have sizes a_i,
then a_{i-1}+a_{i+1}>=2k for each i. Summing gives equality, since the sum
of these five bounds is 2(5k). All five equations are therefore equalities;
the odd-cycle linear system forces a_i=k. Every vertex can have neighbors
only in the two adjacent fibers, of total size 2k, so the degree bound
forces all permitted edges. Thus G=B_k, and (B) applies. Under these explicit
hypotheses, zero margin really does force X to be a transversal. The d=8
witness satisfies neither the homomorphism nor the degree hypothesis.

### Conditional reconstruction from boundary neighborhoods

Suppose G is maximal triangle-free, X induces C5=(x_0,...,x_4), and every
vertex of H has exactly two neighbors in X. Then G is a complete C5 blow-up
and X is a transversal. This condition does **not** follow from zero margin.

Indeed each such pair is independent on the cycle, hence uniquely
{x_{i-1},x_{i+1}} for some i. Place that vertex in V_i with x_i. Within a
part, or between nonconsecutive parts, the two vertices share an X neighbor,
so cannot be adjacent by triangle-freeness. G is thus a subgraph of the
C5 blow-up on these parts. Adding any missing edge between consecutive
parts still cannot create a triangle, so maximality forces all such edges.

This lemma explains how boundary data *could* force a transversal template;
it does not use zero margin, and should not be presented as a deduction of
the boundary hypotheses from zero. Without maximality, deleting a core-core
edge of B3 while leaving a transversal untouched preserves the two-neighbor
boundary condition but destroys completeness. The d=8 witness is itself
maximal triangle-free, yet its zero C5 sets do not meet the boundary condition.

## 6. What remains open in this route

The proposed implication from zero maximum to C5-blow-up geometry is
**refuted**, rather than merely unproved. A remaining precise question that
would extend the common tight-cover interpretation beyond these examples is:

> For triangle-free G on 5k vertices, does max_X M(X)=0 force
> min_{|X|=5}[d(G)-d(G-X)]=2k-1?

This implication is **unproved here**. Its conclusion would make every
zero-margin maximizing X tight (since q(X)<=U_X=B), so the proved tight-cover
lemma would apply to every such X. It would still not imply a C5 template.
The local zero/slack counterexample shows why the global-maximum hypothesis
cannot simply be dropped. Deriving a geometric classification of all graphs
with that tight-cover property remains a separate problem; the d=8 obstruction
must be included in, rather than excluded by, any valid proposed classification.

## 7. Separation from the exchange lemma and reproducibility

The previously proved identity

    b_G(c^S union a)-d(H) = E_c(a)-g_c(a,S),
    g_c(a,S)=sum_{v in S}(w_a(v)-sigma_c(v))+2e(H[S])-4m_c(S)

remains the deterministic coordinated-flip exchange lemma. Nothing here
changes its allowed family or attempts a new local descent theorem. The new
arguments are the tight-cover equivalence, balanced-family rigidity, and
conditional boundary reconstruction above. The first is an equality argument;
the latter two use explicitly stated structural hypotheses.

Artifacts in `results/zero_margin_structure`:

* `d8_A_tight.jsonl`, `B3.jsonl`: every zero X, induced and boundary edges,
  neighborhood classes, every optimal core coloring modulo reversal, and
  **all** assignment-wise maximizing allowed flips for every recorded base.
  Masks use the stored sorted H or X order. Reversing a base and complementing
  each flip recovers the other base orientation with the same target coloring.
  A base attains Phi_X precisely when `sum_cost == best_sum`.
* `summary.json`: all zero sets partitioned into automorphism orbits, induced
  X types and core isomorphism classes, with exact histograms.
* `restriction_audit.json`: the additional all-6,006-set verification of (F).
* `d8_A_tight_tight_negative.json`: all twenty tight-deletion failures of the
  converse. `local_zero_with_slack.json`: the separate local-zero example.
* `comparisons.json`: aggregate flip information and the explicit C5-homomorphism
  obstruction. Counts of flip occurrences are across bases and assignments,
  not counts of distinct subsets of the graph.
* Hash manifests identify the corrected inputs, analysis scripts and outputs;
  `final_manifest.json` additionally covers this note, tests and all artifacts.

Reproduce from the repository root, with the output directory absent:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tests/test_zero_margin_structure.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/analyze_zero_margin.py --output results/zero_margin_structure
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/audit_zero_restrictions.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/summarize_zero_margin.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/validate_zero_margin_artifacts.py
```

Tests cover literal blow-up recognition, removal of a template edge,
C5 homomorphism against brute force on all labeled four-vertex graphs,
a triangle-free non-C5-homomorphic graph, induced flip shapes, neighborhood
classes, and positive/negative restriction-cover examples from the corrected
d=8 witness. No broad random search was run. PID 3132683 and
`results/candidate_A_n20_large` were not modified. No universal selection
theorem, proof of Candidate A, or novelty claim is made.
