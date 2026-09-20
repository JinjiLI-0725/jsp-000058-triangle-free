from itertools import product
from pathlib import Path

from triangle_free.research import from_graph6
from triangle_free.core import deletion_distance

graph6s = [
    x.strip()
    for x in Path(
        "results/induction_B_tight_nonbalanced_reps.g6"
    ).read_text().splitlines()
    if x.strip()
]

# The 8 sets already proved to have minimum witnessing slack 4.
TARGETS = {
    1: [
        (1,5,6,13,14),
        (2,5,6,13,14),
        (3,5,6,13,14),
        (4,5,6,13,14),
    ],
    2: [
        (0,1,9,11,12),
    ],
    4: [
        (2,8,9,10,12),
    ],
    21: [
        (1,2,3,6,12),
        (1,2,6,9,12),
    ],
}


def mono_count(edges, side):
    return sum(side[u] == side[v] for u, v in edges)


for gi, Xs in TARGETS.items():
    g6 = graph6s[gi - 1]
    G = from_graph6(g6)

    dG = deletion_distance(G)
    all_vertices = set(range(G.n))

    print()
    print("=" * 70)
    print("GRAPH", gi)
    print("graph6 =", g6)
    print("d(G) =", dG)
    print("=" * 70)

    for X_tuple in Xs:
        X = set(X_tuple)
        Hverts = sorted(all_vertices - X)

        Hset = set(Hverts)

        Hedges = [
            (u, v)
            for u, v in G.edges
            if u in Hset and v in Hset
        ]

        touch_edges = [
            (u, v)
            for u, v in G.edges
            if u in X or v in X
        ]

        # --------------------------------------------------
        # Enumerate all core cuts.
        # Fix the first H vertex to side 0.
        # --------------------------------------------------
        core_records = []

        fixed = Hverts[0]
        free_H = Hverts[1:]

        for bits in range(1 << len(free_H)):
            core_side = {fixed: 0}

            for j, v in enumerate(free_H):
                core_side[v] = (bits >> j) & 1

            mono_H = sum(
                core_side[u] == core_side[v]
                for u, v in Hedges
            )

            # ----------------------------------------------
            # Given this core coloring, optimize the 5 new
            # vertices over all 32 assignments.
            # ----------------------------------------------
            best_a = None
            best_assignments = []

            for xbits in range(1 << len(X_tuple)):
                side = dict(core_side)

                for j, v in enumerate(X_tuple):
                    side[v] = (xbits >> j) & 1

                a = sum(
                    side[u] == side[v]
                    for u, v in touch_edges
                )

                if best_a is None or a < best_a:
                    best_a = a
                    best_assignments = [xbits]
                elif a == best_a:
                    best_assignments.append(xbits)

            core_records.append(
                (mono_H, best_a, len(best_assignments))
            )

        dH = min(r[0] for r in core_records)
        q = dG - dH

        # F[t] = minimum extension cost among core cuts
        # whose core penalty is t.
        F = {}
        cut_count = {}
        arg_count = {}

        for mono_H, a, num_assignments in core_records:
            t = mono_H - dH

            cut_count[t] = cut_count.get(t, 0) + 1

            if t not in F or a < F[t]:
                F[t] = a
                arg_count[t] = 1
            elif a == F[t]:
                arg_count[t] += 1

        optimum = min(t + a for t, a in F.items())

        print()
        print("-" * 70)
        print("X =", X_tuple)
        print("d(H) =", dH)
        print("q = d(G)-d(H) =", q)
        print()
        print(" t | F(t) | t+F(t) | #core cuts | #cuts attaining F(t)")
        print("---+------+--------+------------+----------------------")

        for t in sorted(F):
            print(
                f"{t:2d} | "
                f"{F[t]:4d} | "
                f"{t + F[t]:6d} | "
                f"{cut_count[t]:10d} | "
                f"{arg_count[t]:20d}"
            )

        print()
        print("min_t [t + F(t)] =", optimum)

        # For these slack-4 cases:
        # minimum global slack among cuts whose H restriction
        # is optimal equals F(0)-q.
        print("F(0) =", F[0])
        print("F(0)-q =", F[0] - q)

        assert optimum == q, (gi, X_tuple, optimum, q)
        assert F[0] - q == 4, (
            gi, X_tuple, F[0], q
        )

        print("IDENTITY CHECK = PASSED")

print()
print("=" * 70)
print("ALL 8 EXTREMAL SETS ANALYZED")
print("=" * 70)
