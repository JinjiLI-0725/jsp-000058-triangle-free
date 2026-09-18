# Balanced extensions at t=7: equality in the cover bound

Date: 2026-09-18. **PROVED:** every triangle-free five-vertex extension of
B_7 has d(G)<=64, with equality exactly for B_8. Together with the previous
[cover proof](BALANCED_EXTENSION_COVER_BOUND.md), this establishes the
arbitrary balanced-remainder theorem for all t>=7.

The single bottleneck addressed is the mixed balanced-remainder extension
needed by A and the strict balanced transition in B_inherit. This is a
partial theorem; general A, B, and JSP-000058 remain **CONJECTURAL**.

## Coverage checked first

All 25 saved t artifacts were read: complete=true and max_gap=0 throughout.
Their **COMPUTATIONALLY VERIFIED** coverage is homogeneous neighborhoods,
not arbitrary mixed neighborhoods. The t>=26 symbolic proof independently
allows mixed neighborhoods, but cannot fill the finite mixed gap. The later
t>=8 cover proof also allows mixed neighborhoods. The claimed homogeneous
spanning-supergraph reduction is **FALSIFIED**, as proved in the
[audit](BALANCED_EXTENSION_AUDIT.md). Neither enumeration was repeated here.
The separate exhaustive n=10 corpus covers arbitrary t=1 and its equality
classification. These facts leave precisely t=2,...,6 unresolved after the
proof below; max_gap=0 alone does not certify finite equality uniqueness.

## Notation and inequalities

Use F=G[X], m=e(F), a valid type map f, S_j, D, L and W from the cover
proof. In particular

    L=sum_j tau(F[S_j]),  D=70-e(X,H)>=7L,
    W=m+2 sum_j e(F[S_j]).

The average of the five type-colored extensions of optimal H cuts is
14+(W-D)/5. Hence W-D<=4 gives d(G)<=49+14=63, the desired strict bound.
If L=0, all F edges join consecutive types, and the existing C5 blow-up
argument gives d(G)<=64 with equality only for B_8. It remains to consider
L>=1 and W-D>=5. In particular W-7L>=5.

For a vertex a in A_j, its neighborhood I_a in X is an independent subset
of S_j. Writing alpha_j=alpha(F[S_j]), we have the exact identity

    D-7L = sum_j sum_(a in A_j) (alpha_j-|I_a|).             (1)

Every summand is a nonnegative integer. Thus a small total surplus forces
individual neighborhoods to have near-maximum cardinality. This identity
uses each actual vertex separately and is valid for mixed neighborhoods.

## Exhausting the exceptional internal graphs

If m<=5 and Delta(F)<=3, then W<=m+6L, so W-7L<=m-L<=4.
If Delta(F)=4, triangle-freeness forces F=K_(1,4).
The only remaining possibility is m=6, and then F=K_(2,3): its maximum
degree is at most 3 and its average degree is 12/5, so take a degree-three
vertex. Its three neighbors are independent. The fifth vertex cannot be
adjacent to the first (degree four would force m=4); to obtain six edges
it must be adjacent to all three neighbors.

Thus only the star and K_(2,3) can violate the average criterion. We handle
both symbolically, without an extension enumeration.

### F=K_(1,4)

Let z be the center. An S_j induces edges only if it contains z; there are
two such parts. Each nonempty induced edge set is a star with cover number
one. Hence L is 1 or 2.

If L=1, sum_j e(F[S_j])<=4 and W<=12. The inequalities W-D>=5 and
D>=7 force W=12, D=7. All four edges therefore occur in the same S_j,
and no edge occurs in any other S. If f(z)=j-1, every leaf has type j+1:
a leaf must have one of types j-1,j+1 to lie in S_j, and type j-1 would
make its edge occur also in S_(j-2), contradicting L=1. Reflection covers
the other orientation. The unique maximum independent set of F[S_j] is
the four leaves. By (1), D-7L=0, so z has no neighbor in A_j. Its remaining
H neighbors lie in A_(j-2). Change f(z) to j+2 (modulo five): its allowed
parts are A_(j+1),A_(j-2), so this is valid and is consecutive to every
leaf type j+1. All F edges are now compatible.

If L=2, W=4+2 sum_j e(F[S_j])<=20 and W is even. Since W>=7L+5=19,
we must have W=20 and D<=15. Each star edge occurs in both parts allowed
for z, so every leaf has the same type as z. Each of those two induced
stars has a unique maximum independent set of size four. Any independent
pattern containing z has size one, losing three relative to that maximum.
But (1) has total D-14<=1. Therefore z has no H neighbors in either part,
hence none at all. Retype z to a type consecutive to the common leaf type.
Again every F edge is compatible.

### F=K_(2,3)

Since W<=6+6L, the inequality W-7L>=5 forces L=1. Exactly one S_j
has edges, with cover number one, so those edges form a star with at most
three edges. Since W>=12, it has exactly three edges, W=12 and D=7.
It consists of one degree-three center z and its three neighbors. The
other center w is outside S_j: otherwise the induced K_(2,3) would have
cover number two. As in the preceding star case, if f(z)=j-1 then all
three leaves have type j+1; no edge can have equal endpoint types, since
that would contribute to two different S sets. Every w-leaf edge is
compatible, since all incompatible edges must occur in S_j.

The unique maximum independent set of F[S_j]=K_(1,3) is its three leaves.
By (1), z has no neighbor in A_j. Retyping z to j+2 is valid and makes
its three edges compatible; it does not change the already compatible
edges incident with w. Reflection again covers the other orientation.

## Finishing and equality

In every exceptional case the new valid type map makes G a spanning
subgraph of a complete C5 blow-up with part sizes 7+|f^(-1)(i)|. At least
three of the added vertices share a type (four in the star cases), so
these sizes cannot all equal eight. The exact blow-up formula and AM--GM
therefore give d(G)<64, hence d(G)<=63 by integrality. This proves strictness
also in the cases where the original five-cut average was insufficient.
The L=0 branch has equality only for B_8, and B_8 attains 64.

## Attempts to falsify the proof

- L counts cover numbers, not merely the number of nonempty S_j. The latter
  description is used only for induced stars, where it is justified.
- The L=2 star case cannot be discarded: it has W=20, not 12. Allowing
  D=15 is essential. The loss of three when a pattern contains its center
  rules out that neighborhood even with this one unit of surplus.
- Minimum-deficit equality means maximum *cardinality* patterns at each
  vertex. The argument uses uniqueness only for K_(1,3) and K_(1,4),
  where it is proved directly by independence of the leaves.
- Retyping does not change G or add boundary edges. Each proposed new
  type contains the entire actual remaining neighborhood of the center.
- The final blow-up is unbalanced because repeated leaf types persist.
  Merely establishing containment in some blow-up would not prove strictness.
- All five initial cuts have q_H=0. The argument uses their costs as upper
  bounds, never as an identity for the true optimum. The exceptional cases
  use actual cuts supplied by the containing blow-up. Thus reoptimization
  in min_c(q_H(c)+e_X(c)) causes no direction-of-inequality error.

## Induction consequence and next checkpoint

**PROVED:** for k>=8, any five-set leaving B_(k-1) satisfies A; for
nonbalanced G it satisfies B. Consequently A plus equality uniqueness
through k=7 would imply equality uniqueness at all orders by B_inherit.
That finite base is not established; general A still requires a choice
of X and c controlling q_H(c)+e_X(c).

**CONJECTURAL:** the same mixed balanced-extension theorem, including
strictness, for t=2,...,6. Continue on this one bottleneck. At t=6 the
exceptional condition is W-D>=5 with D>=6L; the present t=7 classification
must not be assumed to exhaust it. No complete solution has appeared.

## Validation

The targeted regression enumerates only normalized type maps for the two
exceptional internal graphs (1,250 maps, no extension-neighborhood search).
It independently derives W from the five cycle cuts, computes independent
patterns and covers, and verifies that every pattern allowed by the surplus
budget admits the claimed compatible containment with repeated types. This
is **COMPUTATIONALLY VERIFIED** checking of proof ingredients; the theorem
above is **PROVED** symbolically and does not depend on the enumeration.
Process inspection before the check found no other compute job. No long-running
research computation was launched. Existing logs were left untouched.

Passed: `.venv/bin/python -m pytest -q tests/test_balanced_patterns.py
 tests/test_structural_analysis.py` — **9 tests**, 7.60 seconds.
`git diff --check` passed.
