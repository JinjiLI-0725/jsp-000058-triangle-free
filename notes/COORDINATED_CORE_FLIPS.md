# Coordinated core flips: exact structure and exchange lemma

This analysis concerns only the four saved first counterexamples to cutoffs
T=1,2,3,4. No further cutoff audit or random search was run. Vertex labels below
are the original zero-based graph6 labels.

## Findings

The minimum numbers of core vertices that must change side to reach an optimal
full-graph coloring are **1, 3, 3, and 5**, respectively. The minimum is over
every optimal core cut, every globally optimal core restriction, and both
orientations of each cut. The three bipartite cores are connected, so each has
exactly one bipartition up to global reversal. The last example reaches the
trivial maximum of five flips for a ten-vertex core modulo reversal. Thus even
a four-vertex flip bound fails on these fixed pairs (G,X).

Use c(v)=1 for vertices in A and c(v)=0 for those in B.

| Counterexample | graph6 | X | A | B |
|---|---|---|---|---|
| T=2 | `N????KEWOprqxa}W^K?` | {0,5,6,13,14} | {3,4,8,9,12} | {1,2,7,10,11} |
| T=3 | `N@GU_?NxOq[DHosGzG?` | {2,3,6,11,13} | {8,9,10,12,14} | {0,1,4,5,7} |
| T=4 | `NDz?pL_SCDCbFA_[bK_` | {1,3,4,6,9} | {2,5,10,13,14} | {0,7,8,11,12} |

For T=1, graph6 is `N????KEWOprqxa}W^K?`, X={0,1,10,13,14}, and d(H)=1.
H is not bipartite. Its two optimal core cuts, up to reversal, are:

* A={3,4,5,6,9}, B={2,7,8,11,12}, with monochromatic edge (2,12)
  and optimized extension cost 9.
* A={7,8,11,12}, B={2,3,4,5,6,9}, with monochromatic edge (2,9)
  and optimized extension cost 7. We use this second cut below.

### Smallest flip witnesses

In each row S is flipped relative to the displayed base cut. The new side A'
determines the entire minimizing core coloring; the other side is H minus A'.

| Case | S | H[S] | A' | t | Extension before -> after | Net improvement in t+extension |
|---|---|---|---|---:|---|---:|
| T=1 | {8} | singleton | {7,11,12} | 2 | 7 -> 4 | 1 |
| T=2 | {1,2,12} | path 1--12--2 | {1,2,3,4,8,9} | 3 | 11 -> 4 | 4 |
| T=3 | {0,1,14} | path 0--14--1 | {0,1,8,9,10,12} | 4 | 9 -> 3 | 2 |
| T=4 | {0,5,10,11,12} | K_(3,2), parts {0,11,12}, {5,10} | {0,2,11,12,13,14} | 6 | 8 -> 1 | 1 |

Full optimal colorings are obtained by taking the following side-1 subsets of
X, respectively: {10,13,14}, {0,5,6}, {3}, {1,6}. All other X vertices have
color 0. The total q=t+extension is 6 in the first row and 7 in the others.

The core boundaries of the displayed flip sets are:

* T=1: (5,8), (6,8); neither is monochromatic in the base coloring.
* T=2: (1,9), (2,9), (10,12).
* T=3: (0,9), (1,9), (4,14), (7,14).
* T=4: (0,13), (2,11), (5,7), (8,10), (11,14), (12,13).

For the bipartite cores these boundary sizes are precisely the core penalties.
For T=1 the same happens for this particular S because its boundary avoids the
base cut's one monochromatic edge.

For completeness, the minimum flip sizes at *each* globally minimizing penalty
are:

| Case | Minimizing penalty t : minimum number of flips |
|---|---|
| T=1 | 2:1, 3:3, 4:3 |
| T=2 | 3:3, 4:4, 5:5 |
| T=3 | 4:3, 5:4 |
| T=4 | 6:5 |

The T=1 minimum of three flips at t=3 uses the other optimal core cut, whose
extension cost is 9. Starting specifically from an F(0)-attaining base requires
four flips at that penalty. The machine-readable records retain this distinction.

### The strongest obstruction: a dense five-vertex flip

In the T=4 example there are exactly six minimum-cardinality flip sets relative
to the displayed bipartition:

    {0,5,10,11,12}, {0,5,10,12,13}, {0,8,10,12,13},
    {2,5,7,11,14},  {2,7,8,11,14},  {2,7,8,13,14}.

Every one induces K_(3,2). They come in complementary pairs. Every minimizing
core coloring has distance five from the bipartition, and no set of at most
four flips lowers the optimized total cost below F(0)=8.

For S={0,5,10,11,12} and X-side-1={1,6}, the boundary savings at its vertices
are w=(2,1,1,1,2), while their core degrees are (3,4,4,4,3). Each singleton
flip is unfavorable for this fixed X assignment. The sum of singleton losses
is 11. Flipping them together keeps the six internal core edges bichromatic,
giving a rebate of 2 per internal edge: 12-11=1 net improvement.

All seven S--X edges change from monochromatic to bichromatic. Extension cost
drops from 8 to 1; the remaining extension edge lies in G[X], which is a C5.
Six core boundary edges become monochromatic. This is a coordinated dense
subgraph effect, rather than a small core-penalty effect.

## Proven coordinated-flip identity

Fix any optimal core coloring c of H, so b_H(c)=d(H), and fix a coloring a of X.
Let E_c(a) be its extension cost, including internal edges of X. Define

    w_a(v) = (# v--X edges monochromatic under c,a)
             - (# v--X edges bichromatic under c,a).

For S subset V(H), let delta_H(S) be its core edge boundary, and put

    D_c(S) = (# bichromatic edges in delta_H(S) under c)
             - (# monochromatic edges in delta_H(S) under c).

Then, exactly,

    b_G(c^S union a) - d(H) = E_c(a) + D_c(S) - sum_(v in S) w_a(v).       (1)

Only edges crossing a flip boundary change status. Each initially bichromatic
core boundary edge costs one; each initially monochromatic one saves one.
Flipping v saves w_a(v) on its X edges. Internal X edges do not change. This
proves (1), including the nonbipartite case. Optimality of c gives D_c(S)>=0.
Every core coloring is c^S for some S, so minimizing (1) over a and S is exact:

    q(X) = min_a [ E_c(a) - max_S { w_a(S) - D_c(S) } ].                 (2)

No monotone single-vertex descent or small-penalty hypothesis is used.

## Bipartite-core coordinated exchange lemma

When H is bipartite and c is a proper coloring, D_c(S)=|delta_H(S)|. Hence

    gain_a(S) = w_a(S) - |delta_H(S)|
              = 2 e(H[S]) - sum_(v in S) (deg_H(v)-w_a(v)).              (3)

**Certificate lemma.** For any assignment a and subset S, if

    2 e(H[S]) >= sum_(v in S)(deg_H(v)-w_a(v)) + E_c(a)-B,              (4)

then q(X)<=B. This follows by substituting (3) into (1). Taking B=2k-1
gives a sufficient certificate for this selected X at the Candidate-A bound.
It is not an assertion that such X,a,S always exist.

Formula (4) is the structural replacement for a penalty cutoff: internal edges
of the recolored set offset its vertex costs. For a path, tree, or complete
bipartite induced subgraph, one can substitute its exact internal edge count.
It directly accounts for coordinated flips that are individually unfavorable.

**Component structure.** Fix a. Gain is additive over the connected components
of H[S], since there are no edges between these components. Thus any improving
S contains a connected component with positive gain. Moreover, choose a
minimum-cardinality maximizer of gain. Every nonempty component C then has
strictly positive gain: removing a negative-gain component improves the
objective, and removing a zero-gain one preserves it with fewer vertices.
For every vertex of such a maximizer, removal also gives

    w_a(v) - deg_H(v) + 2 deg_(H[S])(v) > 0.                           (5)

These are necessary structural conditions for a smallest optimum, not an
upper bound on its size. A single profitable component need not achieve the
full gain required by the threshold in (4); several may be required.

**Dependence on the size of S.** Reusing an optimal X assignment after a flip
in either direction gives

    |e_X(c^S)-e_X(c)| <= e(S,X) <= 5|S|.                               (6)

Therefore if c attains F(0) and c^S is globally minimizing with penalty t,

    5|S| >= t + F(0) - q.                                             (7)

This is only a necessary lower bound on support size. The example requiring
five flips shows why no universal small upper bound should be inferred from
these four examples. The trivial support bound is |S|<=floor(|H|/2), by
reversing the entire target coloring, including its X assignment.

### Assignment changes must be charged

For the T=3 path witness, the target X assignment {3} has extension cost 10
before the core flip, whereas F(0)=9. Its boundary rewards are (3,3,1), so it
saves 7 extension edges while paying 4 core edges. The full accounting is

    9 + 1 (change X assignment) + 4 (core boundary) - 7 (boundary saving) = 7.

The optimized extension saving is 6, not 7. For the T=2 and T=4 displayed
witnesses, the target assignment already attains F(0), so this extra charge
is zero. Formula (1) always uses E_c(a), never F(0) unless a attains F(0).

## Exact algorithmic consequence for bipartite cores

For each of the 32 assignments a on X, expression (1) is a nonnegative
minimum-cut energy. Give every H edge unit cut cost. For vertex v use unary
costs u_v(0) and u_v(1), the incident X cost before and after flipping v.
With source side meaning unflipped and sink side meaning flipped, add arcs

    source -> v of capacity u_v(1),
    v -> sink of capacity u_v(0),
    u -> v and v -> u of capacity 1 for each H edge uv.

A source/sink cut then costs sum_v u_v(flip_v)+|delta_H(S)|. Adding b_X(a)
gives the full monochromatic count. Thus 32 minimum cuts recover the exact
q and optimal coordinated flip sets for any bipartite H, with no cutoff on
penalty or support. This is an optimization reduction for a given X, not a
selection theorem or a proof of Candidate A. Signed core edges obstruct this
direct nonnegative-capacity reduction for the T=1 nonbipartite core.

## Validation and saved artifacts

`scripts/analyze_coordinated_core_flips.py` analyzed only the four saved pairs.
It enumerated all 512 core cuts modulo reversal and all 32 X assignments,
reproduced every previously saved F(t), enumerated every optimal base cut and
globally minimizing core cut, and checked distances in both orientations.
All bipartitions, nearest supports at each minimizing penalty, exact extension
savings, and vertex boundary rewards are in `results/coordinated_core_flips_n15/`.

The signed identity (1) was checked on all 1024 core flip subsets for each
displayed witness assignment. For each bipartite example, all 32 minimum-cut
values were independently compared against direct enumeration; all agree.
The input/source hashes are in the manifest. The computation is complete.

**Remaining mathematical target:** select X together with a core coloring and
a coordinated flip set meeting a threshold certificate such as (4). The data
suggest paths and dense bipartite pieces as useful supports, but neither
their universal sufficiency nor an upper bound on required support size has
been proved. The fixed-X cutoff obstructions remain intact.
