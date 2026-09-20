# Coordinated flips: deterministic certificate and missing selection inequality

Starting point: `COORDINATED_CORE_FLIPS.md`. Let G be triangle-free on n=5k
vertices, k>=2, and put B=2k-1. This note proves a sufficient condition on a
five-set X and a conditional averaging/selection lemma. It does **not** prove
that the sufficient condition always holds. The single remaining structural
selection inequality is isolated at the end.

## A. Deterministic exchange inequality — proved

Fix X, H=G-X, an optimal core coloring c, and an assignment a on X. Write

    b = d(G[X]),     z = e(X,H),
    E_c(a) = b_(G[X])(a) + monochromatic X--H edges under (c,a),
    w_a(v) = monochromatic v--X edges - bichromatic v--X edges,
    sigma_c(v) = bichromatic H-edges at v - monochromatic H-edges at v.

Optimality of c gives sigma_c(v)>=0. Let m_c(S) count monochromatic edges of
H[S] under c, and define

    D_c(S) = bichromatic edges of delta_H(S) - monochromatic edges of delta_H(S),
    g_c(a,S) = w_a(S)-D_c(S).

Counting internal edges twice gives the exact formulas

    D_c(S) = sum_(v in S) sigma_c(v) - 2e(H[S]) + 4m_c(S),

    g_c(a,S) = sum_(v in S)(w_a(v)-sigma_c(v))
               + 2e(H[S]) - 4m_c(S),                                    (1)

    b_G(c^S union a)-d(H) = E_c(a)-g_c(a,S).                              (2)

Thus the following is a deterministic sufficient certificate for this X:

    g_c(a,S) >= E_c(a)-B.                                                (3)

It implies q(X)<=B. Formula (1), including the term -4m_c(S), applies to
arbitrary cores. One must not replace sigma by degree or discard this term
merely because H[S] is bipartite. Those simplifications are valid when c is
proper on all of H, as in the three d(H)=0 examples.

### Concrete triangle-free controls

These are all unconditional:

1. A triangle-free graph on five vertices is bipartite unless it is exactly
   C5. Therefore b is 0 or 1, with b=1 exactly for G[X]=C5.

2. N_H(x) is independent for every x in X. On a subset of N_H(x), (1) is
   additive. In particular, for each assignment a,

       max_S g_c(a,S) >= max_(x in X)
           sum_(v in N_H(x)) (w_a(v)-sigma_c(v))_+.                       (4)

   The maximizing subset inside this neighborhood consists precisely of the
   vertices with positive summands. This allows a coordinated independent-set
   flip without assuming any local descent property.

3. If uv is an H-edge, N_X(u) and N_X(v) are disjoint, so

       deg_X(u)+deg_X(v)<=5.

   More generally, if H[S]=K_(p,q) with sides P,Q, the sets N_X(P) and N_X(Q)
   are disjoint. Every X vertex attaches to at most one side. Consequently

       e(S,X) <= 5 max(p,q),      w_a(S) <= e(S,X).                       (5)

   For such a flip, the internal contribution in (1) is exactly
   2pq-4m_c(S). This is the structural gain missed by separate vertex flips.

4. Triangle-freeness also gives e(H[S])<=floor(|S|^2/4). Its direction is
   important: this is an UPPER bound on a beneficial term in (1), not a
   lower bound ensuring an exchange. For completeness, neighborhoods of
   adjacent vertices in H[S] are disjoint, giving deg(u)+deg(v)<=|S|.
   Summing over edges and applying Cauchy--Schwarz yields the stated bound.

The controls (4)--(5) connect the rewards to actual independent neighborhoods
and bicliques. They do not force enough positive reward to meet (3).

## B. Averaging assignments after selecting a flip — proved

Let A_X be the set of all optimal colorings of G[X], and let mu_X be uniform
on A_X, including both orientations. It has at most 32 elements. Every vertex
is marginally colored 0 or 1 with probability 1/2; vertex colors need not be
independent. For every fixed optimal c,

    E_(a~mu_X) E_c(a) = b + z/2,     E_(a~mu_X) w_a(v)=0.                (6)

Define the explicit structural flip family R(H) to contain:

* every independent subset of H;
* every S inducing a complete bipartite graph with two nonempty sides;
* the complements in H of all these sets.

It includes the empty set and all of H. No size or core-penalty cutoff is
imposed. The path and K_(3,2) supports found in the counterexamples belong
to this family, as do the part flips needed for balanced blow-ups.

For fixed c define

    Psi_(X,c)(a) = max_(S in R(H)) g_c(a,S),
    Phi_X = max_(c optimal on H) E_(a~mu_X) Psi_(X,c)(a),
    U_X = b + z/2 - Phi_X.                                              (7)

The maximum in Phi_X chooses ONE base coloring before averaging a. The flip
set is then allowed to depend on a. All these maxima are finite and attained.

**Assignment-averaging lemma.** For every X,

    q(X) <= floor(U_X).                                                 (8)

Indeed, choose a c attaining Phi_X and, for every a, a maximizing S(a).
The average of the integer costs E_c(a)-g_c(a,S(a)) is exactly U_X.
At least one of these explicit colorings has cost at most floor(U_X).
Equation (2) proves (8).

Hence the following is a sufficient condition ON X:

    Phi_X >= b+z/2-(2k-1).                                              (9)

The slightly weaker strict inequality U_X<2k also suffices by integrality.
Condition (9) is convenient for a sharp real-valued bound and is attained at
equality for balanced transversals, as proved below.

For a simpler certificate, replace Phi_X in (9) by

    L_X = max_(c optimal on H) E_(a~mu_X)
          max_(x in X) sum_(v in N_H(x))(w_a(v)-sigma_c(v))_+.

Equation (4) gives 0<=L_X<=Phi_X. Thus (9) with L_X is a proved sufficient
condition involving only independent neighborhoods, degree imbalances, and
the at most 32 explicitly specified assignments on X. It may be weaker than
the biclique certificate.

### Why an independent random flip does not help

If S is chosen independently of a, (6) gives

    E_a g_c(a,S) = -D_c(S) <= 0,                                       (10)

because c is an optimal core coloring. The same holds for a random S chosen
independently of a. The favorable term in (7) is an expected MAXIMUM after a
is known. Replacing it by the maximum of expected gains loses the mechanism.

## C. Averaging/selection over five-sets — proved conditional lemma

For any probability distribution pi on five-sets, if

    E_(X~pi) [b_X+z_X/2-Phi_X] < 2k,                                  (11)

then some X, assignment a, and allowed flip S satisfy Candidate A. Average
the explicit integer-cost coloring constructions above over X and a; some
cost is less than 2k and therefore at most 2k-1.

There is a noncircular sufficient graph condition using uniform X and only
Phi_X>=0. If m=e(G) and N_5 counts induced C5 vertex sets, then

    E_X b_X = N_5 / binom(n,5),
    E_X (z_X/2) = 5(n-5)m / [n(n-1)].

The first identity uses triangle-freeness; the second counts the probability
that exactly one endpoint of a fixed edge lies in X. Thus

    N_5/binom(n,5) + 5(n-5)m/[n(n-1)] < 2k                              (12)

GUARANTEES some X works, even with S empty. This proves a selection lemma
for this density/cycle-count regime. Keeping E_X Phi_X improves its left
side, but uniform averaging cannot handle all graphs, even with unrestricted
flips and optimal assignments.

### Uniform X fails already for B3

The blow-up formula from `structural_analysis.md` gives, when X deletes r_i
vertices from part i of B3,

    q(X) = max_i [3(r_i+r_(i+1))-r_i r_(i+1)],     sum r_i=5.

Exactly 3^5=243 of its 3003 five-sets are transversals, and these have q=5.
If X is not a transversal, some adjacent sum s=r_i+r_(i+1) is at least 3:
otherwise all five sums are exactly 2, forcing every r_i=1. For s=3,4,5,

    3s-floor(s^2/4) >= 7.

Thus every nontransversal has q>=7, and

    E_X q(X) >= (243*5 + 2760*7)/3003 = 6845/1001 > 6.                  (13)

Since U_X>=q(X), even the exact optimum cannot make (11) work with uniform
X on B3. This is a genuine obstruction to that averaging scheme, not a loose
estimate of its gains. A successful general selection argument must favor
suitable five-sets rather than average them uniformly.

A finite arithmetic check using the blow-up formula and multiplicities
product_i binom(3,r_i) gives the exact B3 histogram
q=5:243, q=7:2025, q=8:405, q=9:330, and average 7200/1001.
This is an enumeration of part-size counts for the fixed benchmark, not a
new graph search; the weaker symbolic bound (13) already proves the obstruction.

## D. Balanced calibration: the structural bound is sharp

Take G=B_k and let X be a transversal, so H=B_(k-1) and G[X]=C5.
Set t=k-1. Choose a part-respecting optimal core coloring whose five part
colors are (0,0,1,0,1). Up to reversal, the five optimal C5 colorings are
obtained by flipping the part index sets

    empty, {1}, {1,2}, {0,4}, {0}.

Include their complements for the other orientation. On H these supports are
empty, independent parts, complete bipartite pairs of adjacent parts, or
their complements. Hence they all belong to R(H). Every target core cut
remains optimal, so D_c(S)=0. Matching the core part colors to a gives
extension cost 2t+1 for each optimal assignment a on X.

The exact blow-up formula gives q(X)=k^2-(k-1)^2=2t+1, so no allowed gain can
improve these costs. Since b=1 and z=10t, equations (6)--(7) give

    Phi_X = (1+5t)-(1+2t) = 3t,
    U_X = 2t+1 = 2k-1.                                                 (14)

Thus (9) is sharp on balanced transversals, with the whole required gain
accounted for by explicit independent-set/biclique exchanges. This verifies
the constants and explains why the flip family is not limited to independent
neighborhoods or to small vertex supports.

Nor can another five-set improve the Candidate-A constant on B_k. A
nontransversal has an adjacent deletion sum s>=3, giving
q(X)>=ks-floor(s^2/4)>=2k-1 for k>=2 and 3<=s<=5; transversals attain 2k-1.
Thus min_X U_X=2k-1 on B_k as well.

## E. The single unproved inequality

The general argument would close if one could prove this structural selection
statement for every triangle-free G on 5k vertices in the remaining regime:

    There exists X, |X|=5, such that

      Phi_X >= d(G[X]) + e(X,G-X)/2 - (2k-1),                          (SEL)

with Phi_X exactly as defined in (7): optimal assignments on the five-set,
one optimally chosen base core coloring, and independent-set/biclique flips
or their complements. Equivalently, min_X U_X<=2k-1.

Everything from (SEL) to Candidate A is proved above. Equation (14) shows
that its right-hand constant cannot be reduced in general. The exceptional
automatic cases q<=d(G)<=2k-1 need no exchange selection theorem.

**What is missing:** the triangle-free incidence constraints (4)--(5) have
not supplied a lower bound on the assignment-adaptive gain Phi_X for a
suitably chosen X. They give useful independent supports, exclusions between
boundary neighborhoods, and upper bounds on densities/rewards; these do not
force the required positive gain. Uniform X cannot supply it by (13).

(SEL) is a stronger SUFFICIENT conjectural selection inequality, not a claim
of equivalence to Candidate A. Restricting assignments to A_X, restricting
flip shapes, and averaging their optimized costs may lose useful colorings.
It has not been proved or universally audited, and its failure would not
refute Candidate A. No universal selection theorem or complete proof of A
is claimed. No new graph search was launched.
