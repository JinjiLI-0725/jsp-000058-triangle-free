#!/usr/bin/env bash

set -u

cd ~/jsp-000058-triangle-free

LOG_DIR="logs/overnight"
mkdir -p "$LOG_DIR"

while true; do
    TS=$(date +"%Y-%m-%d_%H-%M-%S")
    LOG="$LOG_DIR/run_$TS.log"

    echo "===== Starting research cycle at $(date) =====" | tee -a "$LOG"

    codex exec --sandbox workspace-write "
You are continuing mathematical research on JSP-000058.

Before doing anything, read:
- PROBLEM.md
- notes/INDUCTION_CHECKPOINT.md
- notes/INDUCTION_ROUTE.md
- notes/structural_analysis.md
- notes/candidate_lemmas.md
- notes/rejected_lemmas.md
- notes/BALANCED_REMAINDER_THEOREM.md if it exists
- state/current_state.json if it exists
- relevant results/ files

Current verified milestone:
- exhaustive k=1 verification complete;
- exhaustive k=2 verification complete;
- heuristic k=3 found equality d(G)=9;
- exact balanced-extension verification for t=1,...,25 has max_gap=0;
- the t>=26 balanced-remainder case was previously argued symbolically and must be rechecked carefully.

Your job in THIS cycle:
1. Identify the single most valuable unresolved mathematical step.
2. Work only on that step.
3. Prefer proof or falsification over broad random searching.
4. Use targeted computation only if it directly tests a specific claim.
5. Clearly separate:
   - PROVED
   - COMPUTATIONALLY VERIFIED
   - CONJECTURAL
   - FALSIFIED
6. Never claim JSP-000058 is solved unless a complete rigorous proof exists.
7. Update the appropriate notes files with any real progress.
8. Update state/current_state.json.
9. Run relevant tests before finishing.
10. End at a clean checkpoint.

If you find a potential full proof:
- create notes/POTENTIAL_PROOF.md;
- immediately try to break every step;
- do not announce success merely because the argument looks plausible.

Do not start an unbounded computation that requires Codex itself to remain alive.
Long numerical work should be launched as a persistent script with checkpointing.
" 2>&1 | tee -a "$LOG"

    CODEX_RC=${PIPESTATUS[0]}

    echo "Codex exit code: $CODEX_RC" | tee -a "$LOG"

    git add .

    if ! git diff --cached --quiet; then
        git commit -m "Automated research checkpoint $TS" | tee -a "$LOG"
        git push origin main | tee -a "$LOG"
    else
        echo "No repository changes this cycle." | tee -a "$LOG"
    fi

    echo "===== Cycle finished at $(date) =====" | tee -a "$LOG"

    # Wait 5 minutes before starting the next reasoning cycle.
    sleep 300
done
