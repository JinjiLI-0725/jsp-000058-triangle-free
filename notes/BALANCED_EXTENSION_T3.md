# Strict arbitrary balanced extensions at t=3

Date: 2026-09-18. **PROVED:** every triangle-free graph consisting of an
induced B_3 and five other vertices has d<=16, with equality exactly for B_4.
Together with the occupied-type proof, the strict theorem holds for all t>=3.
This cycle addresses exactly the t=3 balanced-remainder bottleneck in A/B.
General A, B, and JSP-000058 remain **CONJECTURAL**.

## Coverage prerequisite

All completed t1.json,...,t25.json were read: complete=true, max_gap=0,
242500 configurations and 1245367 maximal homogeneous choices each.
These are **COMPUTATIONALLY VERIFIED** homogeneous results only. The original
t>=26 symbolic proof allows arbitrary mixed neighborhoods, but these two
ranges do not establish an all-t arbitrary theorem. The homogeneous
spanning-supergraph reduction is **FALSIFIED**, as recorded in the audit.
The t=5 empty witness and lack of equality classification in these artifacts
remain unchanged. No enumeration was repeated. The t>=4 occupied-type proof
is the starting point here; t=1 and its equality case have separate exhaustive
n=10 certification. Only arbitrary mixed t=2 remains after this proof.

## Setup and two-cut inequality

Use H=B_3, X={0,1,2,3,4}, F=G[X], and a valid type map f as in
BALANCED_EXTENSION_TYPE_OCCUPANCY.md. Write n_j=|f^(-1)(j)| and
S_j={v:f(v)=j-1 or j+1}, with type indices modulo five.
Every individual vertex of H part A_j has an independent F-neighborhood
I subset S_j. Its pattern need not agree with any other vertex's pattern.

For two part colorings c,c' of H, each with exactly one monochromatic
cycle edge, and arbitrary X colorings a,a', define

    M_j = max_{I subset S_j, I independent in F}
          sum_{v in I} ([a_v=c_j]+[a'_v=c'_j]).

The sum of the costs of these two actual cuts is at most

    18 + b_F(a)+b_F(a') + 3 sum_j M_j.                    (1)

Each H cut costs 9. Apply the displayed maximum separately to each of the
three actual vertices of A_j and sum. This proves (1) for arbitrary mixed
and nonmaximal patterns. A right side <=31 supplies a cut of integer cost
<=15. One may safely enlarge the pattern family by imposing independence
only in a subgraph of F, and independently upper-bound the internal costs.
One may NOT complete F and then assume the original patterns are independent
in the completion. The proof below expressly avoids that inference.

## Injective maps

The previous proof gives W=m+2L and D>=3L, where m=e(F) and L counts edges
with distinct nonconsecutive types. The five type cuts have average cost
15+(W-D)/5, so W-D<=4 suffices for d<=15.
If L>=1 and m<=5, then W-D<=m-L<=4.
If m=6, F is K_(2,3): a nonbipartite triangle-free five-vertex graph is
exactly C5 and has five edges, while a bipartite five-vertex graph with six
edges must be complete with side sizes two and three. At most four edges
of K_(2,3) lie on the type pentagon, since all five would be an odd cycle.
Consequently L>=2 and again m-L<=4.
If L=0, G is a spanning subgraph of B_4. Every proper such subgraph has
an explicit cut of cost <=15, by making a missing edge's part pair the
sole monochromatic pair. Equality therefore occurs only for B_4.

## Noninjective maps: the occupancy reduction

Adjacent empty types give a cut of cost <=9+6=15. Otherwise there are
one or two empty types. For an empty-singleton type edge, the old proof
gives H-plus-boundary cost <=12. If its X cut splits 2+3, its internal
cost is <=1+2=3, proving d<=15.

The following complete occupancy check is elementary, with rotations and
reflections allowed. With one empty type, rotate it to 0: the other counts
are three ones and one two. Choosing an appropriate incident edge always
splits X as 2+3. Explicitly, when the double type is 1,2,3,4, choose the
sole monochromatic edge 40,01,01,01 respectively.

With two nonadjacent empty types, rotate/reflect them to 0,2. Write the
positive counts (n_1,n_3,n_4). Their six possibilities are:

| Counts | A 2+3 empty-singleton cut, or exceptional form |
| --- | --- |
| (1,1,3) | edge 01 |
| (1,2,2) | edge 01 |
| (1,3,1) | edge 12 |
| (2,1,2) | E1 |
| (2,2,1) | reflection of E1 |
| (3,1,1) | E2 |

Thus only E1=(0,2,0,1,2) and E2=(0,3,0,1,1) require attention.
A 1+4 cut has four internal monochromatic edges only if the four-vertex
side induces C4: triangle-freeness bounds it by four, and a triangle-free
four-vertex graph with four edges is C4. (A nonbipartite such graph would
need at least five vertices; a bipartite one has at most 2*2 edges.)

## E1: two pairs and a singleton

Label f=(1,1,3,4,4). The edge 23 type cut isolates vertex 2 of X.
Unless F-2 is C4 it already gives <=15. Let Q=F-2=C4. The neighbors
of vertex 2 in Q are independent, hence contained in one of its two
opposite pairs. This is a constraint on internal edges only.

Up to permutations within the two repeated types, the bipartition of Q
is either aligned, {0,1}|{3,4}, or crossed, {0,3}|{1,4}.
The table gives two cuts. Strings list colors in index order 0,...,4.
The M vector is computed using only independence in Q, with vertex 2
unrestricted; thus it bounds every actual neighborhood in F.
The column B bounds b_F(a)+b_F(a') for either choice of the opposite pair
to which vertex 2 can attach, including all subsets of that pair.

| Q bipartition | c | a | c' | a' | (M_0,...,M_4) | B | RHS (1) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 / 34 | 00101 | 00011 | 01010 | 11100 | (2,0,0,0,0) | 4 | 28 |
| 03 / 14 | 00101 | 01011 | 00101 | 10011 | (1,0,1,0,0) | 5 | 29 |

These small certificates can be checked directly. In the aligned row,
only part 0 contributes boundary cost: each of its four allowed Q vertices
has combined weight one, and alpha(Q)=2. Internal Q edges cross both cuts;
attachments to {0,1} cost four in total, and to {3,4} cost zero.
In the crossed row, part 0 assigns weight one to vertices 0 and 1 only,
which are adjacent in Q. Part 2 does the same; all other weights are zero.
The combined Q cost is three. Each possible attachment edge costs one,
so the at-most-two attachments add at most two. Both rows prove d<=15.
No completion of F is used to restrict a boundary pattern.

## E2: a triple and two singletons

Label f=(1,1,1,3,4). The empty-singleton cuts at edges 23 and 40 isolate
vertices 3 and 4 respectively. If either leaves at most three internal
edges, d<=15. Otherwise both F-3 and F-4 are C4.

The graph on {0,1,2} is then P3, since deleting a vertex from C4 leaves P3.
Both vertices 3 and 4 attach to exactly its two endpoints. They cannot
be adjacent because they have common neighbors. Thus F is K_(2,3).
Permute the three type-1 vertices so its size-two side is {0,1}, giving
edges from {0,1} to {2,3,4}.

Use c=00101, a=01001 and c'=01001, a'=11101. The two internal costs
are 3 and 4. In part 0, S_0={0,1,2,4}; the only positively weighted
vertices are 0 and 2, each of weight one, and they are adjacent.
In part 2, S_2={0,1,2,3}; vertices 1 and 3 each have weight one, and they are adjacent.
All other parts have zero weights. Hence M=(1,0,1,0,0), and (1) is
18+3+4+3*2=31. One cut therefore has cost <=15.
This finishes every noninjective case and the theorem.

## Inference audit and classification

**PROVED:** strict arbitrary balanced-extension theorem for t>=3, with
equality exactly B_(t+1). Noninjective t=3 maps are strictly below equality;
injective compatible maps use the explicit missing-edge argument.
All cuts used restrict to optimal H cuts, so q_H=0. We upper-bound q+e
with actual extensions and do not reverse the restriction inequality.

The most dangerous inference was completing a C4-plus-vertex graph to
K_(2,3) while keeping old boundary patterns. That would be invalid.
The E1 certificates instead maximize over the larger Q-independent family
and bound internal attachments separately. This repairs the inference
before it enters the proof. The E2 K_(2,3) description is forced equality
of F itself, so its independent-pattern constraint is legitimate.

**COMPUTATIONALLY VERIFIED:** regressions independently check the occupancy
classification, the injective inequality, and each certificate on every
allowed independent pattern and internal attachment. Exploratory bounded
checks of the two exceptional maps and pairs of cuts motivated the displayed
certificates; the proof above does not rely on extension enumeration.

**FALSIFIED:** no new lemma this cycle; the earlier homogeneous-supergraph
claim remains falsified. **CONJECTURAL:** mixed t=2 strict extension,
general A/B, and JSP-000058.

## Induction consequence and next checkpoint

For k>=4, every X with G-X=B_(k-1) satisfies A and, for nonbalanced G, B.
By B_inherit, A plus equality uniqueness through k=3 would imply uniqueness
at every order. Neither general A nor the full k=3 equality classification
is proved. The general obstruction is still selecting X,c with
q_H(c)+e_X(c)<=2k-1, or <=2k-2 for B.

The next precise claim on this bottleneck is the strict arbitrary mixed
extension at t=2. Do not infer it from homogeneous t=2 certification.
No potential complete solution of JSP-000058 appeared. Test results and
clean stopping status are recorded in INDUCTION_CHECKPOINT.md.
