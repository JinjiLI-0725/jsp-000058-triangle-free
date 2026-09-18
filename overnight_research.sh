#!/usr/bin/env bash

set -u

cd ~/jsp-000058-triangle-free

mkdir -p logs/overnight

while true; do
    TS=$(date +"%Y-%m-%d_%H-%M-%S")
    LOG="logs/overnight/run_${TS}.log"

    echo "===== cycle start $(date) =====" | tee -a "$LOG"

    codex exec --sandbox workspace-write "
Continue rigorous research on JSP-000058.

FIRST read:
- PROBLEM.md
- notes/INDUCTION_CHECKPOINT.md
- notes/INDUCTION_ROUTE.md
- notes/structural_analysis.md
- notes/candidate_lemmas.md
- notes/rejected_lemmas.md
- all completed results/balanced_extension/t*.json

Important current milestone:
The exact balanced-extension enumeration for ALL t=1,...,25 is complete,
and every case has max_gap=0.

Do NOT redo that computation.

For this cycle:

1. Identify exactly ONE unresolved mathematical bottleneck that is most
   likely to advance the full conjecture.

2. Prefer, in order:
   - rigorous proof;
   - falsification of a candidate lemma;
   - reduction to a weaker sufficient lemma;
   - targeted finite computation tied to one precise missing claim.

3. Do not run broad random searches merely to accumulate evidence.

4. Clearly classify findings as:
   PROVED
   COMPUTATIONALLY VERIFIED
   CONJECTURAL
   FALSIFIED

5. If using the balanced-remainder result, first verify how the t<=25
   exhaustive certification and t>=26 symbolic argument combine.

6. Focus particularly on induction lemmas A and B and the exact obstruction
   described in INDUCTION_ROUTE.md.

7. Update notes with genuine progress.

8. Update state/current_state.json if appropriate.

9. Run relevant tests.

10. Stop at a clean checkpoint.

If a potential complete solution appears:
- write notes/POTENTIAL_PROOF.md;
- attempt to falsify every inference;
- do not claim JSP-000058 solved merely because an argument looks plausible.

Never launch more than one long-running computation at once.
Before launching a compute job, check whether one already exists.
" 2>&1 | tee -a "$LOG"

    RC=${PIPESTATUS[0]}

    echo "Codex exit code: $RC" | tee -a "$LOG"

    git add .

    if ! git diff --cached --quiet; then
        git commit -m "Automated research checkpoint ${TS}" | tee -a "$LOG"
        git push origin main | tee -a "$LOG"
    else
        echo "No repository changes." | tee -a "$LOG"
    fi

    # If Codex hit a usage/rate limit, don't hammer it every 5 minutes.
    if grep -qiE "usage limit|rate limit|try again at" "$LOG"; then
        echo "Usage limit detected; sleeping 1 hour." | tee -a "$LOG"
        sleep 3600
    else
        sleep 300
    fi
done
