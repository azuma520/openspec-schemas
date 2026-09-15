# Known-defect list sealed BEFORE Codex formal branch review (not sent to reviewer)
sealed_at: 2026-09-10T06:26Z (local 14:26)
snapshot: worktree HEAD b07d571 + frozen working tree (see 文檔/handoff/attachments/20260910-pilot2/pilot2-snapshot.md)

Known, unfixed, in-scope at dispatch time:
1. superpowers-bridge/schema.yaml:1180 — 84-char line among ~65-char neighbours (fallback r2 Nit)
2. superpowers-bridge/schema.yaml:532 — check 7 says `grep -c` on absent tasks.md returns 0; actually prints nothing, exit 2; STOP still holds (fallback r2 Nit)
3. check 10 — no fixture for the absent-`outcome:` case (fallback r2 Missing Items)
4. schema.yaml:175 / :567 — author instruction fixed indent vs check accepting any depth (Codex 0909 补审 Important; judged deliberate; fallback r1/r2 did not report)
5. fixtures f8–f13 never blind-run (disclosed in README; fallback r2 Missing Items)

Purpose: after review, mark each as HIT / MISS. Measures miss on known defects only, not recall.
