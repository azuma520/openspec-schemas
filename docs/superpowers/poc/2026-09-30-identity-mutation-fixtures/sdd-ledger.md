# SDD ledger — plan: openspec/changes/requirement-scenario-identity/plan.md

Spec: openspec/changes/requirement-scenario-identity/specs/contract-identity/spec.md (+ 4 補號 delta specs). Worktree branch: worktree-requirement-scenario-identity (base 42c3d24).

## Rulings

- Ruling: implementers do NOT git commit; review packages are working-tree diffs / whole new files — repo Anchor Register #4 forbids AI git add/commit outside /smart-commit --execute or explicit user authorization — cost if wrong: review diffs mix tasks; mitigated by per-task file scopes (commit batching happens via /smart-commit with user approval).
- Ruling: Task 1.1 was executed inline by the controller (deviation from SDD, disclosed to user 2026-09-30); remedied by an independent fixture review (strict-reviewer, 2 rounds, ✅ Ready) per user decision 3A — cost if wrong: author bias in fixtures not caught by a spec-compliance reviewer of SDD shape.
- Ruling (user, 2026-09-30): "one thing broken" = one author-introduced mutation source; collateral rule hits allowed and listed in 1.2 — recorded in plan.md §1.1.
- Ruling (user, 2026-09-30): blind scoring = final verdict + exact set of BLOCK categories; reasons not scored — plan.md §1.1.
- Ruling (user, 2026-09-30): check 13 text counting is literal line-start match, code blocks not recognised — plan.md §3.1.
- Ruling (user, 2026-09-30): archive success = exit 0 AND change moved into archive/ — plan.md §3.1, §5.2.
- Ruling: the fixture reviewer (strict-reviewer, name fixture-reviewer) has seen expected answers and MUST NOT serve as a blind executor in 2.1/3.1.

## Pre-flight scan

| Pair / task | Produces → consumes | Finding |
|---|---|---|
| 1.1 → 1.2 | fixture dirs + mutation descriptions → expected-answer / coverage tables | consistent; README must carry collateral hits (reviewer F6: v15 S4+S3) and category sets |
| 1.1 → 1.3 | fixtures → shuffled copies | 1.3 must exclude author-run.md and README from copies (both outside fixtures/) |
| 1.2 → 2.1 / 3.1 | expected answers + result table → filled columns | scoring model now in plan §1.1 |
| 1.3 → 2.1 / 3.1 | frozen prompt/procedure → same text both runs | only rule source differs |
| 2.1 → 3.1 | subject list + RED content | 3.1 blocked by 2.1 (schema.yaml untouched until then) |
| 3.1 / 3.2 | both edit schema.yaml (verify vs specs instruction, version line) | serial; no conflict in sections |
| 3.1 → 4.1 / 4.2 | check 13 text → templates/README | titles must match verbatim |
| 4.2 ↔ 4.3 | Compatibility row shape ↔ version-check.yml grep | mutual; run grep/awk after both |
| 5.1 → 5.2 | synced schema → archive preview | 5.2 success criterion updated |
| 1.2 self | README tables vs fixture dirs | row per dir, both directions |
| 3.1 self | TDD applicable; RED/GREEN in own task | GREEN obtained inside 3.1 (plan r3 fix) |
| other tasks self | n/a annotations | no self-contradiction found |

## Progress

Task 1.1: complete (uncommitted; fixture review ✅ Ready r2; Codex doc review of plan 1.1/5.2 edits ✅ Mergeable r2, thread 01a0f026-1881-7893-aadf-2187145e9118)
Task 1.2: review r0 — spec ✅, 1 Important (§2 REQ-1-S4 row wrongly lists v07 as collateral) → fix round 1 sent to impl-1-2
Task 1.2: minor (deferred): README §2 REQ-1-S5 row says REQ-PB 未被改動 for all p*, but p04 MODIFIES REQ-PB with unchanged text — wording 內容未變 would be exact
Task 1.2: minor (deferred): typo in task-1.2-report.md (implementer report, not a deliverable)
Task 1.2: fix round 1/5 (1 addressed, 0 open — REQ-1-S4 collateral cell; uncommitted)
Task 1.2: complete (uncommitted, review clean after fix round 1)
Ruling: 1.3 kit layout — frozen prompt/procedure/hashes in repo blind-kit/ (evidence), shuffled copies + mapping outside repo in scratchpad/blind/ — cost if wrong: scratchpad is not cleaned automatically; must be cleaned after 5.3
Ruling: rule source handed to executors = whole schema.yaml (RED: git show 42c3d24), same file name both runs — verify instruction references tasks instruction grammar — cost if wrong: executors see other artifacts' instructions (harmless noise)
Ruling: GREEN A/B get two physically separate byte-identical copies with identical names — plan says 同一份副本; physical separation prevents cross-contamination if one writes — cost if wrong: none on content
Ruling: blind executors' do-not-read-repo boundary is instruction-only; recorded as a limitation for 5.3
[REVIEWER_FALLBACK] plane=doc_review from=codex to=contract-neutral-reviewer reason=quota | 2026-09-30T03:10:00Z (user chose model=fable; sticky for this change)
doc_review fb1 (contract-neutral-reviewer, model fable): ✅ Mergeable, SENTINEL_VALID; 4 🟡/⚪ deferred
Ruling: doc 🟡 'model record location' (tasks.md header says 寫入結果表, README §3 says tasks.md 2.1/3.1) — resolve at 2.1 by recording the model in BOTH places; no doc edit now (sub-threshold) — cost if wrong: one redundant field
Ruling: doc 🟡 'plan §3.1 counting limitation names only the fence direction' — carry the reverse direction (case/spacing variants CLI counts, literal match does not; author-run fact 3) into the 3.1 brief — cost if wrong: check 13 text documents half the limitation
Task 1.2: minor (deferred): README p04 row over-states 'RENAMES 每個 requirement' (only token-auth's two) — same class as the REQ-PB 未被改動 minor
Task 1.3: complete (uncommitted, review clean — review-1-3 Approved; RED kit at scratchpad/blind/red/, mapping seed 20260930; frozen hashes in blind-kit/FROZEN.md)
Task 1.3: minor (deferred): acceptance wording could carve out pre-existing rule-file text from the leak dictionary (3 'expected' hits in schema.yaml judged non-leaks)
Note: blind-kit/*.md are new .md files — doc gate re-opened; batch with the next doc review
Ruling (user, 2026-09-30): blind executors = sonnet for RED and both GREEN — measures rule clarity, not reasoning power; pilot setting only, not a routing rule; if sonnet fails broadly, a fresh fable may run as a diagnostic that never overrides the sonnet results
Task 2.1: RED blind run dispatched 2026-09-30 — executor blind-red, model=sonnet (explicit), fresh context, wrapper = blind-dispatch-wrapper.txt with KIT=scratchpad/blind/red/kit, REPORT=scratchpad/blind/red/report-red.md
Task 2.1: complete (uncommitted, review clean — RED all 22 PASS {}; 17 subjects u01,v01–v16; 5 conformance-only p01–p05; premise holds; evidence in blind-runs/red/)
Ruling: 3.1 rule text — archive-preview failure → 無法判定, but change-level parts that need no candidate state still run and report (a change can carry both kinds) — REQ-7 distinguishes kinds and forbids degrading either — cost if wrong: extra violations reported alongside 無法判定 on broken changes
Ruling: 3.1 rule text — a MODIFIED/RENAMED entry unresolvable to a main requirement is an archive-preview matter (無法判定 via REQ-5), not an ID violation — REQ-5-S2/REQ-7-S1 name it undeterminable — cost if wrong: u01-type cases under-reported as violations
Task 3.1: part A dispatched (implementer, model fable, unnamed); BASE schema.yaml = 42c3d24 clean
Task 3.1: review r0 (opus) — Needs fixes: I1 REQ-4 no-ID new heading unreported when preview fails; I2 kind-set ambiguity after count mismatch for RENAMED/REMOVED; I3 synced-state conflict (spec-level, to user) → fix round 1 (I1, I2) sent to part-A implementer
Task 3.1: minor (deferred): M1 FRESHNESS scope bullet contradicts 13.F staleness rule — carve out check 13 (also in 4.1 template)
Task 3.1: minor (deferred): M2 check 13 sits under CHECKS 8-12 header — add own header
Task 3.1: minor (deferred): M3 13.D should read headings 'as 13.A counts them' (fenced heading in current max)
Task 3.1: minor (deferred): M4 RENAMED FROM has ID, TO has none — state the violation wording
Task 3.1: minor (deferred): M5 grammar wording: 'one or more spaces' looser than spec; description must contain a non-whitespace char
Task 3.1: minor (deferred): M6 placeholder names mixed; deltas[].spec = capability dir name unstated; archive dir name check hard-codes date
Task 3.1: fix round 1/5 (2 addressed, 0 open — I1 no-ID new heading violation in 13.D.3; I2 per-case undeterminable set in 13.E). GREEN held until the user decides I3 (a later check-13 edit would force a GREEN rerun).
Ruling (user, 2026-09-30) I3 = A, per capability: a capability that check 3 records as ✓ Already synced → check 13 reports 無法判定 (required pre-sync state unavailable) for every identity judgement that depends on the pre-sync baseline, and must not treat same IDs in the post-sync main spec as a collision; unsynced capabilities are checked normally; fail-closed BLOCK; 'verify before sync' is recovery guidance only, NOT a new workflow-ordering contract. Controller note: the archive preview is whole-change, so a synced capability also makes the candidate state unavailable for the others — their candidate-state parts are 無法判定 under the existing preview-failure rule, their current-state parts run normally.
Follow-up (not this change): lifecycle research — verification depends on a pre-sync state that a legal workflow step (sync) consumes; options: formal verify/sync ordering, preserving/rebuilding the pre-sync baseline, or a post-sync verifiable representation.
Task 3.1: minor (deferred): check 13's synced-capability branch inherits check 3's precision — check 3's '✓ Already synced' has no mechanical test (not touched per ruling)
Task 3.1: fix round 2/5 (I3 addressed per re-review). Controller probe (re-reviewer's out-of-scope note): MODIFIED-already-applied → preview SUCCEEDS; RENAMED-already-applied → aborts (exit 0) → I4 opened: text falsely asserts any applied delta aborts the preview → fix round 3 sent
Task 3.1: fix round 3/5 (I4 addressed). Part A rule text frozen for GREEN.
Task 3.1: GREEN run 1 dispatched — two fresh sonnet executors (A, B), same wrapper, kits scratchpad/blind/green/kit-A|kit-B (tree hash 1229064a… both), seed 73115, rule file sha256 7e9fbca1…
Task 3.1: GREEN run 1 result — A 22/22 match; B 21/22 (v13 reported {違規} only; its reasoning named the unreliable-pairing UNDETERMINABLE but the category/FINAL lines omitted it). A/B disagree on v13 → no vote; v13 not GREEN; failure type: 操作對應不清 (reasoning → reported kind list). B also wrote simplified Chinese and check 5 as '無法判定' instead of '不適用於 fixture' (prompt nonconformance, unscored). 16 subjects consistent+expected in run 1. Evidence: blind-runs/green-r1/ (hashes recorded).
Ruling: per plan 3.1 procedure — clarify check 13 rule text (prompt is frozen and cannot change), then rerun BOTH executors on a fresh shuffle; no rerun without a rule change (that would be retry-until-green) — cost if wrong: two more blind runs (~20 min each)
Task 3.1: fix round 4/5 → fresh implementer (fable) per SDD rounds 4-5
Task 3.1: fix round 4 done (13.E dependent unpaired comparisons are own findings; 13.F kind set over ALL findings) → scoped re-review
Task 3.1: fix round 4/5 re-review: all addressed. GREEN run 2 dispatched — fresh sonnet A/B, kits scratchpad/blind/green-r2/kit-A|B (tree bbc7a7d0… both), seed 90421, rule file sha256 f2eea915…; leak grep: 1 hit 'the primary' in generic 13.F text (judged non-leak); r1/r2 shuffle coincide at case-01=v07 (chance; fresh executors)
Task 3.1: GREEN run 2 result — A 22/22; B 21/22: v06 check-13 line = BLOCK 違規 (correct) but FINAL line = PASS {} (self-contradicting aggregation; prompt-level, not rule text). v13 now correct for both. B again mixed scripts (違规). Evidence: blind-runs/green-r2/. Per plan 3.1: a subject without consistent+expected verdict → stop and report to user.
Ruling (user, 2026-09-30) B = instrument repair: GREEN r1/r2 kept as round-1/2 data labelled 'reporting instrument defect found' — not official GREEN evidence; check 13 rules frozen (no edits); prompt v2 changes ONLY the output contract (FINAL the single authoritative result field, fixed enum categories, no judgement hints); re-freeze + reviewer; then ONE full rerun: RED 1 + GREEN 2; if the same class of output instability recurs → stop, no prompt v3, record as pilot finding. Taxonomy for 5.3: rule-interpretation failure / execution instability / reporting-grading instability.
Task 2.1: reopened (unchecked) — RED must be rerun under prompt v2; round-1 RED record kept as instrument-v1 data
Pending user: official RED = v2 rerun (post-edit, method-identical) vs round-1 RED (pre-edit) — controller recommends v2 + note
Ruling (user, 2026-09-30) RED provenance = hybrid: round-1 RED (prompt v1, pre-edit) stays the official chronological RED; prompt-v2 + old rules run = 'RED replay / baseline replication' — does NOT replace RED, verifies prompt v2 did not change baseline verdicts and gives GREEN a same-instrument control; GREEN = prompt v2 + new rules. If replay ≠ original RED → STOP (prompt v2 was not a pure instrument repair).
Controller execution details (agreed): replay runs first, GREEN A/B dispatched only after replay matches; 'match' = scoring model over all 22 fixtures; tasks.md 3.1 RED records = original RED only (contract: one RED per subject; replay recorded in README only); invocation fields name prompt v1 (RED) / v2 (GREEN).
Task 2.1: re-checked — its official RED stands (round-1 record in README is the chronological RED); replay belongs to 3.1's instrument repair
Instrument v2: review r0 Needs fixes — Important: 4-token per-check set has no non-blocking 'no verdict' slot (old-rule check 7 absent-tasks case; check 5 worktree basis read as outside NOT_APPLICABLE by r1-B) → could flip RED. Root cause: controller's brief. Fix round 1 sent: add NO_VERDICT token; NOT_APPLICABLE covers git state (history or working tree). Minor: stray __pycache__ in v2.
Instrument v2: re-review all addressed; frozen. RED replay dispatched — fresh sonnet, prompt/procedure v2, rule schema-red.yaml (546e2726…), kit scratchpad/blind/v2-replay/kit (tree 01b4373b…), seed 58213. GREEN held until replay matches original RED over all 22.
Replay result: 22/22 FINAL: PASS, NONCONFORMING=0 — identical to original RED (all PASS {}); prompt v2 did not change baseline verdicts. Executor briefly wrote a helper file inside the kit then removed it (instruction-only boundary; observation for 5.3).
GREEN v2 dispatched (the one instrument-repair run) — fresh sonnet A/B, prompt/procedure v2, rule schema.yaml f2eea915…, kits scratchpad/blind/v2-green/kit-A|B (tree edb295dd… both), seed 31907; graded by frozen blind-kit/v2/grade.py
GREEN v2 result: A 22/22, B 22/22, NONCONFORMING 0, A/B FINAL lines identical per case → all 17 subjects consistent+expected (GREEN). Evidence: blind-runs/v2-replay/, blind-runs/v2-green/.
Task 3.1: complete (uncommitted; part A 4 fix rounds + instrument v2 repair; part C review clean; 17 RED/GREEN pairs; checks 8–12 pass by script)
Task 3.2: complete (uncommitted; fix round 1: non-empty description; verify span sha256 6bcf8f71… identical to official GREEN rule file)
Task 4.1: complete (uncommitted; review clean)
Ruling: 4.1 minor — template quotes check-13 title without the schema's trailing colon; accepted as the existing convention for checks 8–12 in the same template (plan says 逐字相同) — cost if wrong: a future reviewer flags a false mismatch
Task 4.2+4.3: review r0 (opus) Needs fixes — I-1 no ID heading grammar + no spec link; I-2 v3 Superpowers v6.4.1 contradicts badge + README :576 policy (baseline stays v5.1.0 until brainstorming drift fix) + :588 exceptions → USER DECISION (controller recommends v5.1.0 + honest record); I-3 breaking criterion wording differs across README :117/:485/:596 and CLAUDE.md; I-4 verification record says 'checks 3.1/3.2/4.1'; I-5 zh 註記語法 → 標題語法. Minors: migration step 2 'the same way' (scenarios get IDs via MODIFIED); REQ-PB example internal; 13.G capability-rename non-guarantee omitted; root README descriptions. Fix round 1 (I-1, I-3, I-4, I-5 + minors 1–3) → implementer; I-2 held.
Task 4.2+4.3: fix round 1/5 (I-1, I-3, I-4, I-5, minors a–c addressed per scoped re-review); I-2 still open awaiting user decision; 4.2/4.3 not ticked.
Task 4.2: minor (deferred): relative spec link resolves only when the README is read inside this repo, not in an adopter's copied openspec/schemas/
Ruling (user, 2026-09-30) I-2 = B: v3 Compatibility Superpowers baseline stays v5.1.0; README policy 'baseline not raised until the brainstorming drift fix lands' unchanged (badge unchanged); verification record states honestly that this change's apply and related flow ran on the installed Superpowers v6.4.1 (only the paths actually exercised). Distinguish compatibility baseline vs observed working environment. Plan 4.2's 'fill actually verified versions' reconciled: baseline column = declared baseline; observed version goes in the record. Relative-link minor stays deferred (README repo-native vs portable question).
User authorized: commit after B lands and 4.2/4.3 pass review — one WIP checkpoint commit via /smart-commit before 5.1.
Task 4.2+4.3: fix round 2/5 (I-2 addressed per user ruling B); complete (uncommitted).
Task 4.2: minor (deferred): README :588 says fixtures ran 'under the row's version:' — fixtures carry no schema copy; phrase like :551 ('under CLI 1.3.1')
WIP checkpoint commits (execution fallback: /smart-commit scripts blocked by worktree isolation; user chose manual git add/commit with equivalent checks, 2026-09-30): 1de8e10 test(poc) 234 files; 3780ab3 feat(schema) 7 files (version-check.yml moved here per CLAUDE.md coupling rule); 05fd2f8 docs 8 files. Checks: git var identity azuma520 <kyoe33@gmail.com> from ~/.gitconfig; no commit-msg hook installed (manual guard-regex scan of each message: clean); no sensitive/stray files; post-commit: tree clean, no AI trailers in last 3. 4 raw reports LF-normalized on commit (no committed doc records their hashes). Not pushed.
Worktree friction #7: isolation refuses any 'bash <script>' → /smart-commit (inspect/execute scripts) cannot run; forced a downgrade to manual equivalent checks.
Ruling (user, 2026-09-30) 5.2 = A: 'completed with approved deviation' — literal criterion (line-identical except headings) not met: repo-guidance shows 3 blank-line-only differences after archive; non-blank content identical except ID headings; archive transition, IDs, counts all as expected; D7 content-unchanged claim holds; plan text NOT amended. Root cause wording: 'produced by the archive process, blank lines only' (fact); 'suspected OpenSpec re-formatting' = observation only. Delta trailing blank line ruled out by controller probe (as-is vs no-trailing-blank: identical drift).
Pattern for 5.3: exit 0 ≠ archive success; line/byte equality ≠ the semantic contract — acceptance oracles must map to the claim.
Task 5.1: complete (review clean)
Task 5.2: complete with approved deviation (review clean; independently reproduced; evidence migration-acceptance.md)
Task 5.2: minor (deferred): why the other three capabilities show no blank-line drift is unexplained — backlog candidate if adopters hit it
Task 5.2: minor (deferred): pre-archive snapshot taken from worktree state, not a pinned ref
Task 5.3: review Approved; controller found: §5 cites the gitignored ledger by line number (brief said not to) → ruling: persist the append-only ledger into the repo as docs/.../sdd-ledger.md (final copy at finish; earlier line numbers stay valid) and repoint §5 citations to it
Task 5.3: fix round 1 (8 §5 citations repointed to ./sdd-ledger.md, 11 line refs script-verified); controller one-line fix of the same class in §3b (line 162) per the one-line on-the-spot exception
Session close 2026-09-30: 12/12 tasks complete, all task reviews clean. User ruling: stop here; commit 5.x checkpoint (authorized for this one commit only; no push/merge/archive); worktree kept (no teardown); handoff written on main. Next: SDD final whole-branch review → doc gate (sticky fallback Fable) + code gate (schema.yaml) → verify → retrospective → archive (user runs rm).
