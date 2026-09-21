# Reduced finite enumeration for the abstract L11 exchange shapes

## Result and exact scope

Let (X=C_5), and let (F) be a ten-vertex core consisting of one of

1. no edges;
2. one edge;
3. a two-edge path; or
4. two disjoint edges,

together with enough isolated vertices to make ten vertices. Give every edge
of (F) its proper bipartite colouring. For each (v\in V(F)), let
(T(v)=N_X(v)) be an independent subset of (C_5), require
(T(u)\cap T(v)=\varnothing) on every (uv\in E(F)), and assume

\[
z=\sum_v |T(v)|\ge 9.
\]

The reduced exact enumeration proves

| core shape | reduced states before symmetry | D5/core-shape orbits | exact minimum ten-assignment gain |
|---|---:|---:|---:|
| zero edges | 178,464 | 18,320 | 29 |
| one edge | 3,442,706 | 175,386 | 27 |
| two-edge path | 11,730,131 | 665,015 | 23 |
| two-edge matching | 51,250,771 | 673,334 | 17 |

Thus every abstract state has total gain at least (17), and in particular
at least (7). There is no counterexample with gain at most (6).

This is a finite certificate for a core that is exactly the displayed forest
plus isolated vertices. It does **not** by itself cover a ten-vertex core
having additional properly coloured edges while only its monochromatic-edge
set has one of these shapes. Such edges change both \(\sigma_c\) and which
sets are independent or complete bipartite. This boundary is essential.

## The eleven neighbourhood types

Triangle-freeness leaves exactly the eleven independent subsets of (C_5):
the empty set, five singletons, and five diagonals. Index them as

```text
empty; 0,1,2,3,4; 02,13,24,03,14.
```

For an isolated core vertex of colour zero, put

\[
w_a(T)=\sum_{i\in T}\bigl(1_{a_i=0}-1_{a_i=1}\bigr).
\]

Across the ten optimal (C_5) assignments,

\[
\sum_a (w_a(T))_+=
\begin{cases}
0,&T=\varnothing,\\
5,&|T|=1,\\
6,&|T|=2.
\end{cases}
\]

Consequently the orientation of an isolated neighbourhood does not affect
the total gain in the zero-edge, one-edge, or path shapes. Only its size does.
Orientations still matter for the state count and the D5 quotient.

Endpoint types retain their full (w_a)-vectors. On one edge the two types
must be disjoint. On the path, (T_0\cap T_1=T_1\cap T_2=\varnothing); no
condition is imposed between the leaves. On the matching the two endpoint
pairs are independently disjoint. These are exactly the endpoint data that
can affect the gain.

## Direct multiplicity formula

Let (mu_T) be the number of isolated vertices of type (T). If the shape
has (s) endpoints, then

\[
\sum_T\mu_T=10-s.
\]

For an endpoint set (S\subseteq V(F)), define

\[
b_a(S)=\sum_{v\in S}(w_a(T(v))-\deg_F(v))+2e_F(S).
\]

The degree is \(\sigma_c(v)\) because the forest is properly coloured, and
there are no monochromatic core edges. Define

\[
\begin{aligned}
A_a&=\max\{b_a(S):S\text{ or }V(F)\setminus S\text{ is independent}\},\\
B_a&=\max\{b_a(S):F[S]\text{ is an edge-containing complete bipartite graph}\},\\
C_a&=\max\{b_a(V(F)\setminus S):F[S]\text{ is an edge-containing complete bipartite graph}\},\\
P_a(\mu)&=\sum_T\mu_T(w_a(T))_+,\qquad
W_a(\mu)=\sum_T\mu_Tw_a(T).
\end{aligned}
\]

Then the total ten-assignment gain is exactly

\[
G(T_0,\ldots,T_{s-1};\mu)
=\sum_a\max\{A_a+P_a(\mu),\ B_a,\ C_a+W_a(\mu)\}. \tag{1}
\]

The three terms correspond respectively to an independent set or its
complement with arbitrary isolated vertices, a complete-bipartite support
with no isolated vertices, and the complement of such a support, which
contains every isolated vertex.

For the zero-edge, one-edge, and path shapes, every endpoint subset or its
complement is independent whenever the subset is not already usable as a
biclique. Hence the last two terms in (1) are dominated and

\[
G=\sum_a A_a+5\sum_{|T|=1}\mu_T+6\sum_{|T|=2}\mu_T. \tag{2}
\]

Only the matching is non-additive. Its exceptional endpoint masks are the
two masks selecting exactly one whole matching edge. If the two edges have
assignment weights ((x_0,x_1)) and ((x_2,x_3)), the endpoint quantities
used by (1) reduce to

\[
\begin{aligned}
A_a={}&\max\left\{
 \sum_{uv\in E(F)}\max(0,x_u-1,x_v-1),
 \sum_{uv\in E(F)}\max(x_u-1,x_v-1,x_u+x_v)
 \right\},\\
B_a=C_a={}&\max(x_0+x_1,x_2+x_3).
\end{aligned}
\]

This is the only branch for which the DP retains the ten-entry vectors
(P_a(\mu)) and (W_a(\mu)).

## Multiplicity bounds and monotonic pruning

Write (k=10-s), (z_{\rm ep}=\sum_{i<s}|T_i|), and

\[
m_1=\sum_{|T|=1}\mu_T,\qquad
m_2=\sum_{|T|=2}\mu_T.
\]

Every feasible state satisfies

\[
0\le\mu_T\le k,qquad
\sum_T\mu_T=k,qquad
m_1+2m_2\ge 9-z_{\rm ep}.
\]

In particular, with (R=\max(0,9-z_{\rm ep})),

\[
\mu_\varnothing\le k-\lceil R/2\rceil,
\]

and the endpoint tuple is impossible if (z_{\rm ep}+2k<9). These bounds
come only from ten core vertices, (z\ge9), and the independent-subset bound
(|T|\le2); the edge-disjointness conditions above are imposed separately.

The independent-support term gives the monotone lower bound

\[
G\ge \sum_a A_a+5m_1+6m_2. \tag{3}
\]

Adding another isolated singleton or diagonal type increases the right side
by (5) or (6). The matching vectors are sorted by this bound. Once (3)
reaches the current incumbent, every larger multiplicity suffix is pruned.
Only 6,350 matching endpoint/profile combinations required exact evaluation;
26,122,429 larger branches were discarded by this certified monotonicity.

## Symmetry and finite certificate

No isolated vertex is labelled. A state is an endpoint tuple together with
the eleven-entry multiplicity vector (mu). The pre-symmetry counts in the
table are counts of these states satisfying (z\ge9). Orbit counts are
computed by Burnside's lemma for

\[
D_5\times\operatorname{Aut}(F).
\]

For each group element, a small generating-function DP counts multiplicity
vectors fixed by its permutation of the eleven types, while endpoint tuples
are checked only against edge disjointness and the same group element.

The exact minimizing witnesses, their ten assignment gains, all state/orbit
counts, and the matching pruning totals are saved in
`results/hard_regime_L_n15/L11_reduced_orbits.json`. Reproduce with

```sh
python3 scripts/check_L11_reduced_orbits.py
python3 -m pytest -q tests/test_L11_reduced_orbits.py
```

The checker performs no graph search and never enumerates labelled isolated
vertices.

## Certificate lemma

**Lemma.** Under the hypotheses in the first paragraph, for every assignment
of independent (C_5)-neighbourhoods with total boundary at least nine,

\[
\sum_{a\in A_X}\max_{S\in\mathcal R(F)}g_c(a,S)\ge17.
\]

**Proof.** Triangle-freeness reduces every neighbourhood to one of the eleven
types and imposes disjointness on edge endpoints. Formula (1) evaluates the
allowed independent, complete-bipartite, and complementary supports exactly.
Equations (2) and (3) reduce the first three shapes to endpoint tuples and the
two cardinality multiplicities, and reduce the matching to the stated
ten-entry profile DP. Burnside counting is not needed for the inequality but
certifies that the state quotient is exhaustive. The exact minima are the
four values in the first table, whose least is (17). ∎
