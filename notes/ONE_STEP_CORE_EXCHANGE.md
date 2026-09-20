# One-step core exchange: exact reduction and current status

> Superseded research direction: the proposed universal per-cut one-vertex
> descent condition is false and is not being pursued. The weaker fixed-X
> existential t<=1 optimality assertion also has an exact counterexample;
> see [EXISTENTIAL_CORE_BAND_N15.md](EXISTENTIAL_CORE_BAND_N15.md). The
> conditional implication below does not establish either hypothesis.

Fix (Xsubseteq V(G)), (|X|=5), and (H=G-X). For a two-colouring (c) of
(H), write

\[
t(c)=b_H(c)-d(H),\qquad e_X(c)=\min_{a:X\to\{0,1\}} b_G(c\cup a)-b_H(c).
\]

The exact deletion identity is

\[
\gamma_G(X)=d(G)-d(H)=\min_c\{t(c)+e_X(c)\}.
\tag{1}
\]

The strongest simple one-step exchange statement is the following.

**Exchange condition (E_X).** Every colouring (c) of (H) with (t(c)\ge2)
has a vertex (v\in H) such that, after flipping (v),

\[
t(c^v)<t(c),qquad t(c^v)+e_X(c^v)\le t(c)+e_X(c).
\tag{2}
\]

If (E_X) holds, repeatedly apply (2). The nonnegative integer (t) strictly
decreases and the objective in (1) never increases, so some minimizer of (1)
has (t\le1). Thus

\[
E_X\Longrightarrow
\gamma_G(X)=\min_{t(c)\le1}(t(c)+e_X(c)).
\tag{3}
\]

This is exactly the desired “it is enough to inspect (t\le1)” reduction.

There is a directly checkable sufficient local form. Let (m_H(v,c)) and
(x_H(v,c)) be the numbers of monochromatic and bichromatic (H)-edges at
(v), and let (b_X(v)) be the number of (vX)-edges. Flipping (v) changes

\[
t(c^v)-t(c)=x_H(v,c)-m_H(v,c).
\]

For any fixed assignment on (X), the extension cost changes by at most
(b_X(v)), hence (e_X(c^v)\le e_X(c)+b_X(v)). Consequently it is enough to
find, at every (t\ge2) colouring, a vertex satisfying

\[
m_H(v,c)-x_H(v,c)\ge b_X(v)>0.
\tag{4}
\]

Then (t) drops by at least (b_X(v)), while (e) rises by at most (b_X(v)),
so (t+e) does not increase. A weaker exact audit can verify (2) directly,
without requiring the crude boundary-degree bound (4).

For the eight previously identified slack-4 sets, the audit is in
`results/one_step_core_exchange_n15.json`. It checks every core colouring with
(t\ge2), all one-vertex flips, and exact extension costs. This finite result
supports the reduction for those eight selected pairs if every entry reports
`all_have_good_exchange=true`; it does not establish (E_X) for arbitrary
triangle-free graphs or select a suitable (X).

If a suitable (X) satisfying (E_X) also has one explicitly checked
(t\le1) colouring with (t+e_X(c)\le2k-1), then (1)--(3) prove Candidate A
for that graph. To prove Candidate A universally, one still needs a theorem
that every relevant graph admits such an (X), plus the low-band bound. The
eight examples have (q=6), (F(1)=5), and therefore (1+F(1)=6), but this
numerical pattern is evidence only. Triangle-freeness alone does not imply
(4): a vertex can have many boundary neighbours and no profitable core flip.

The exchange condition is therefore a precise, finite next target rather than
a completed proof of Candidate A.
