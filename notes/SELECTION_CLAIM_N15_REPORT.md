# Exact n=15 audit of the structural selection claim

> INVALIDATED: the original auditor admitted arbitrary bipartite induced
> subgraphs instead of complete bipartite ones, and selected cross-X maxima
> by raw numerators with varying denominators. Its flip witnesses also mixed
> local and global labels. The historical results below are not valid evidence
> for the selection conjecture. A fresh corrected audit is required.
>
> Superseded by [the corrected audit](SELECTION_CLAIM_N15_CORRECTED_REPORT.md),
> using new sources and fresh output in `results/selection_exact_corrected_v2`.

The claim audited was

    Phi_X >= d(G[X]) + e(X,G-X)/2 - (2k-1)

for at least one five-set X, where Phi_X is the assignment-averaged maximum
gain over independent sets, complete bipartite sets, and their complements,
with the maximum taken over optimal core colorings. Margins are

    M(X)=Phi_X-(d(G[X])+e(X,G-X)/2-(2k-1)).

All 24 fixed graphs were audited: one d=8 A-tight witness, B3, and 22
non-balanced d=7 canonical representatives. Each has exactly 3003 five-sets,
for 72,072 five-set instances total. Every result was passed by the exact C++
enumerator; B3 has sharp maximum margin 0. No graph had a negative maximum.

The maximum-margin records are below. A listed X is zero-based. `dH` and `q`
are included as a check on the selected witness; `core_side1` and
`maximizing_flip_sets` are the corresponding optimal core coloring and the
maximizing allowed flip sets, represented in the ten-vertex H order used by the
enumerator. Multiple flip sets can maximize the assignment-wise gain; the
listed vector contains one for each optimal X assignment.

| graph | graph6 | max M(X) | maximizing X | dH | q |
|---|---|---:|---|---:|---:|
| d8 A-tight | `NEL_FF_DgAeOATbBPp?` | 0 | {0,1,2,6,8} | 3 | 5 |
| B3 | `NFz_ww[?wF?[wFwF[B_` | 0 | {0,3,6,10,14} | 4 | 5 |
| nonbalanced 1 | `N????KEWOprqxa}W^K?` | 1 | {0,5,8,11,13} | 3 | 4 |
| nonbalanced 2 | `N?CNnRGLM?_YHIs@d@_` | 0.8 | {0,2,6,8,12} | 3 | 4 |
| nonbalanced 3 | `N?HsWJXw?qaQBCwPcDo` | 1 | {1,3,5,9,10} | 3 | 4 |
| nonbalanced 4 | `N?]aGe`TN_@RaS?ieOO` | 0.8 | {0,2,4,5,12} | 3 | 4 |
| nonbalanced 5 | `N@GU_?NxOq[DHosGzG?` | 1 | {4,6,9,12,13} | 3 | 4 |
| nonbalanced 6 | `NAo?jIBCHS`Ywcl@Da?` | 1 | {4,5,6,10,14} | 3 | 4 |
| nonbalanced 7 | `NAq?jIBCHS`Ywck@Da?` | 1 | {0,3,8,9,13} | 3 | 4 |
| nonbalanced 8 | `NB?^UG`GOKRFEE@kWcO` | 1 | {0,4,10,12,13} | 3 | 4 |
| nonbalanced 9 | `NCjaoxo_yoSHGE@hwGO` | 0.8 | {0,2,8,9,11} | 3 | 4 |
| nonbalanced 10 | `NDz?pL_SCDCbFA_[bK_` | 0.5 | {0,1,2,6,10} | 3 | 4 |
| nonbalanced 11 | `NGaue?XMT_@xPEGgj?G` | 0.5 | {0,5,8,9,13} | 3 | 4 |
| nonbalanced 12 | `NIo[a?fAdIsioKIo?_W` | 0.8 | {0,1,2,10,12} | 3 | 4 |
| nonbalanced 13 | `NOJB_w[B_KCIL?uBWDo` | 1 | {0,2,4,8,14} | 3 | 4 |
| nonbalanced 14 | `NPBWM@AEr?rDIoq_ADW` | 1 | {0,1,7,8,11} | 3 | 4 |
| nonbalanced 15 | `NUCJCKpaaHooX??LlGG` | 0.8 | {0,2,3,4,14} | 3 | 4 |
| nonbalanced 16 | `NUM?[OoPZIKW_iKcAR?` | 1 | {0,2,5,9,13} | 3 | 4 |
| nonbalanced 17 | `NWdPWEDQP`eGQH`D?PW` | 1 | {0,1,2,4,9} | 3 | 4 |
| nonbalanced 18 | `NXa@QwUVE@C_s`?vHC_` | 0.6 | {0,1,2,4,14} | 3 | 4 |
| nonbalanced 19 | `NYp?XeCd@d@`O\oPQOO` | 0.6 | {0,1,2,5,9} | 3 | 4 |
| nonbalanced 20 | `N[LPGUDOP`eGQHbD?PW` | 0.75 | {0,1,3,7,12} | 3 | 4 |
| nonbalanced 21 | `NqHCXeDORCBFKcQGeaG` | 0.8 | {0,1,2,3,12} | 3 | 4 |
| nonbalanced 22 | `NqHKGuDWRCBFK_QGe_G` | 0.6 | {2,5,6,10,14} | 3 | 4 |

The minimum positive margin among the non-balanced classes is 0.5. The two
zero-margin graphs are exactly the d=8 witness and B3; B3's maximizing X is a
transversal, as required by the equality model.

## Exactness and scope

The enumerator checks every 15-vertex cut modulo global reversal, every optimal
core coloring, every optimal assignment on X, and every allowed flip set. The
allowed family is independent subsets, complete bipartite induced subsets, and
their complements. Margins are calculated as exact rational numbers; the report
displays decimals only for readability. The C++ source and Python driver are
`scripts/audit_selection_claim_n15.cpp` and
`scripts/audit_selection_claim_n15.py`.

Hashes:

    audit_selection_claim_n15.cpp
    d01816a28b192da8b5899938091207466e8ca343d08fd2b325b47b50d561b98e
    audit_selection_claim_n15.py
    e96f91afb6857369c70a86c58176fc81b32f8e9ed9407f5fc1f4e2794dc3b461
    corpus.txt (d8, B3, classes 1--22)
    c4663652263d12d37a03cf60b3a91e6fbb1a1ff978b2ae1516f328107cd2a5ed
    corpus_7_22.txt (independent continuation)
    d008565dce8e06bd082ae343728793b902b1ebb8e4aa3990ea3a8502602b8f0f
    induction_B_tight_nonbalanced_reps.g6
    72fc041ac54664a95930ab8820721d30c4c4c1c750b074b7ca46c2e80c6680ad

The audit tests only this fixed corpus. It does not prove the selection claim
for all triangle-free graphs, and it does not prove Candidate A.
