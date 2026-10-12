# Retrospective: executor-governance-wording

> Written: 2026-10-12 (after verify passed: Round 1 and Round 2 both ⚠️ PASS WITH WARNINGS, no BLOCK)
> Commit range: `b40e059..ba68235` (+ uncommitted W5/W6 fixes in the working tree at write time)
> Worktree: none — main checkout (brainstorm Q4 ruling; see §4)

---

## 0. Evidence

- **Commit range**: `b40e059..ba68235` (4 commits; the only implementation commit is `2551ea0`, see verify.md PRECHECK table)
- **Diff size**: committed `b40e059..ba68235` — +1068 / −55 lines across 23 files. Uncommitted after verify Round 1 (REQ-6, artifact sync, zh-TW link): `proposal.md`, `design.md`, `tasks.md`, `plan.md`, the `tdd-claim-accuracy` delta spec and `superpowers-bridge/README.zh-TW.md`, plus the untracked `verify.md` and this file. Line counts are omitted because later edits kept moving them.
- **Tasks done**: 20/20 (`grep -cE '^\s*- \[x\]' tasks.md` → 20)
- **Active hours**: about one working day on 2026-10-12, from the first commit `213a6fb` at 08:16 to this retrospective at about 15:40 (not measured precisely)
- **Subagent dispatches**: no implementer dispatches, because SDD was not run (§4). Review and verification dispatches: at least 10.
  - Earlier part of the session: doc reviews of proposal / design / specs, tasks / plan, task 1.5 and the full implementation, plus a code review of `version-check.yml` — all by the fallback reviewer on model Fable. Then the Fable verify agent, which stopped on a usage limit, and the fallback verify agent on the default model.
  - After compaction: three doc reviews (Fable), the Round 2 verify (Fable), and an audit of earlier §6 candidates.
  - The exact count for the earlier part was not tallied; the session transcript holds it.
- **New external dependencies**: none
- **Bugs encountered post-merge**: none so far (not merged / pushed at write time)
- **OpenSpec validate state at archive**: pass at write time (`openspec validate --all --json` 7/7, verify Round 2 總表 check 1); archive not yet run
- **Test coverage signal**: n/a — prose and config only. The executable evidence is the weekly version-check step, run locally from a verbatim extraction against a marked copy of the README (verify.md, implementer appendix and Round 2 W5 judgement). The precommit runner reports `⚠️ NO CHECKS RUN`, which is not a pass (backlog line 80, case 5).

Commit chain (時序):

```
b40e059 chore(handoff): record the 2026-10-08 17:15 session (base)
213a6fb docs(openspec): open executor-governance-wording change with its brainstorm
80fd84b chore(handoff): record the 2026-10-12 session; register non-SDD execution research
2551ea0 feat(superpowers-bridge)!: state executor governance as capability; schema major 5
ba68235 chore(backlog): record weekly triage round and precommit gap case 5
(uncommitted) REQ-6 + artifact sync + zh-TW link + verify.md + this retrospective
```

---

## 1. Wins

- [evidence: verify.md §6.4 Round 1; implementer appendix W5; Round 2 W5] **The independent verifier caught a claim with no discriminating power.** I had said several times that "the run read the v5 row". The Round 1 verifier swapped the row key and showed the output did not change. The later mutation test — distinct values in the v5 row of a scratch copy, step extracted verbatim — tells right from wrong. Round 2 reproduced it and added two more mutations: a `v6` key exits 1, and swapping the row order still reads v5.
- [evidence: verify.md §4 drift warning 1; spec delta REQ-6] **Verify found a gap between spec and implementation that every doc review had missed.** The change's core behaviour — the three apply situations and the Step 0 STOP — existed in `schema.yaml` with no requirement behind it. REQ-6 now holds it, and Round 2 mapped every clause to a `schema.yaml` passage.
- [evidence: tasks 1.5; `git log -S` on `75274b6` / `045ab98`] **A dangling sentence was traced to its exact history before being fixed.** The Step 0 sentence pointed at a manual fallback that had been removed. Its history was established from git, not guessed; an earlier draft that said "dangling since 75274b6" was corrected after review.
- [evidence: design D8; `release-versioning` delta REQ-3-S2] **The residue search found a stale spec scenario.** The living spec still said the weekly check reads "the v4 row". The fix was worded as "the row of the released schema major", per the user's ruling, and does not claim automatic detection.
- [evidence: verify.md Round 1 header; Round 2 independence statement] **Every verifier stated its own limits.** Round 1 said it came from the same session and the same model family. Round 2 said it was cross-model but dispatched from the same session.

## 2. Misses

- 🟡 [painful | evidence: verify.md implementer appendix, "更正" paragraph] **I over-claimed verification twice in a row.** First I said the run read the v5 row, though both rows held equal values. Then I said the mutation script was a verbatim extraction, but it had replaced the three `GITHUB_OUTPUT` lines with an `echo`. Both were caught by verifiers or by re-reading, not by me before speaking. This is the same pattern as memory `feedback_claim_first_discriminating_oracle`, which already existed.
- 🟡 [painful | evidence: verify.md §4 drift warning 1] **Normative instruction text was written without a requirement.** Design D3 and task 1.5 changed agent-facing behaviour text, but the spec artifact only modified REQ-3 and REQ-4. None of the doc reviews before verify flagged the missing axis; verify did.
- 🟡 [painful | evidence: brainstorm Q4; §0 dispatch list] **The planned substitute review was not the one used.** Q4 named "independent Codex document review" as part of the substitute for SDD. Codex was unavailable through apply, so every gate was carried by the fallback reviewer on Fable. This is disclosed here and in §4, and a Codex re-review is owed (§6 C).
- 📌 [nit | evidence: verify.md Round 2 N2; `schema.yaml` apply situations, first item] **The first situation's label is narrower than its rule.** "No subagent capability" names one cause, but the item defers to Step 0, which stops on *any* missing required skill. REQ-6 is worded at the correct scope. The user ruled not to change the label in this change (N2 option 乙).
- 📌 [nit | evidence: Round 2 doc review nits] Two counting measures in verify.md were left unstated: headings exclude fenced code, and Round 1 counted unique link targets while Round 2 counted occurrences. One cited line range ran past the end of the file. All are recorded as `[NIT_DEFERRED]`.

## 3. Plan deviations

| Plan task | What changed | Why |
|-----------|--------------|-----|
| 1.5 | Added during apply | Step 0 pointed at a removed manual fallback. User ruling 甲, 2026-10-12. |
| specs (`release-versioning`) | A MODIFIED REQ-3-S2 delta was added during apply | The residue search (6.2) found "reads the v4 row". User ruling 甲. |
| specs (`tdd-claim-accuracy`) | ADDED REQ-6, after verify Round 1 | Verify warning W6: no spec axis for the three situations and Step 0. User ruling 甲. |
| 6.3 | Acceptance extended to map REQ-6 S1–S4 to `schema.yaml` | Follows from REQ-6. The mapping is in the verify.md appendix and is confirmed in Round 2. |
| 6.4 | A discriminating mutation test was added after verify | The original run could not tell the v4 row from the v5 row (W5). |
| Verify | Done in two rounds: Round 1 by the fallback agent on the default model, Round 2 by Fable | The first Fable verify agent hit a usage limit. The user ruled W3: Fable re-reviews after W6 is fixed. |

## 4. Skill / workflow compliance

| Skill                                            | Used |
|--------------------------------------------------|------|
| superpowers:brainstorming                        | ✓ (`brainstorm.md`, Superpowers v6.4.1) |
| superpowers:using-git-worktrees                  | ✗ (見下) |
| superpowers:subagent-driven-development          | ✗ (見下) |
| superpowers:test-driven-development              | N/A — annotation-driven (all 20 tasks `TDD: n/a`, reasons judged in verify R3) |
| (structural via SDD) superpowers:requesting-code-review | ✗ — not obtained structurally, because SDD was not run; substitute: post-hoc external reviews (見下) |
| superpowers:finishing-a-development-branch       | ✗ (見下) |

### Deliberately Skipped Skills

- **`superpowers:subagent-driven-development`**, together with `using-git-worktrees` and `finishing-a-development-branch`, which only make sense on the SDD path
  - **What was skipped**: SDD as a whole, so the change did **not** get independent review during execution — no review after each task or batch while the work was being done. The implementation was written in the main session and committed as one commit, `2551ea0`. No worktree was created, and no branch was finished, because the work happened on `main`.
  - **Why this cycle**:
    - **The ruling**: the user ruled in brainstorm Q4 (`brainstorm.md` Q4): "不跑，只限本次，作為具名、經核可的流程例外". Its stated grounds were: the change is governance and instruction wording, it adds no executor, and worktrees interfere with the dogfood `opsx` commands, the same cause as on 10/06.
    - **How the work was actually done**: in the main session, by the implementer.
    - **The substitute checks, all after the fact**:
      - Doc reviews of every artifact and of the full implementation, plus a code review of `version-check.yml`. All were by the fallback reviewer on model Fable. Codex, which the ruling named, was unavailable.
      - Verify Round 1, by a fallback agent from the same session and the same model family.
      - Verify Round 2, by Fable, cross-model.
      - Mutation tests of the version-check step.

    These checks review the output after it was produced. They are not review during execution, and they are not equivalent to SDD.
  - **How to prevent recurrence**: `one-off — schema boundary case`.
    - The ruling covers this change only, and an earlier ruling never authorises a later skip. Any future skip needs its own explicit ruling.
    - **How the deviation was disclosed**:
      - in `plan.md`'s Execution header;
      - in verify.md, in the Round 1 "執行方式的偏離" section and in warning 1, which Round 2 confirmed is still open;
      - in this section.
    - **Where the evidence is**: `brainstorm.md` Q4, verify.md, and the review verdicts in the session transcript.
    - **Prior cases.** This is the **third** full skip of SDD:
      - `openspec/changes/archive/2026-08-31-fix-tdd-transitive-claim/retrospective.md` §4;
      - `openspec/changes/archive/2026-10-06-fix-executing-plans-rationale/retrospective.md` §4.

      There is also one **partial** case, in `openspec/changes/archive/2026-10-01-requirement-scenario-identity/retrospective.md` §4: Task 1.1 was executed inline. All three full skips were wording-only changes, so the pattern is raised as §6 candidate F.

    This record discloses a deviation. It does not make the missing assurance present, and it does not make this path a supported execution mode.

## 5. Surprises

- **Retrospective learnings mostly did not land unless the user ruled on each one.** I audited the 35 §6 candidates in the 7 archived retrospectives, using the four-dimension frame recorded in `docs/superpowers/research/2026-10-12-improvement-decision-four-dimensions.md`. The audit table is kept in this change directory as `retro-s6-audit.md` (copied unchanged from the session scratchpad). **Numbering used below and in `backlog.md`** ("盤點編號 m.n"): m is the retrospective's position among the 7 archived retrospectives in archive-date order (1 = `2026-08-31-fix-tdd-transitive-claim`, 2 = `2026-09-04-loosen-plan`, 3 = `2026-09-14-fix-v2-blocking-defects`, 4 = `2026-10-01-requirement-scenario-identity`, 5 = `2026-10-02-retro-skill-inventory`, 6 = `2026-10-06-fix-executing-plans-rationale`, 7 = `2026-10-08-task-prefixed-plan-headings`; `2026-08-31-claude-md-phase-boundary` has no retrospective and is skipped); n is the item's position in that retrospective's §6 checklist.

  | Result | Count |
  |---|---|
  | Done (incl. 2 late: 1.3, 3.6) | 10 |
  | Registered as work items | 2 |
  | Decided against | 11 |
  | Not done | 12 |

  Counting rule: an item whose lesson landed later by another route, after a recurrence, counts as done (late); the user ruled this for 1.3 and 3.6. The audit's own table uses the stricter rule (Done 8 / Not done 14) and is kept as written.

  All 12 not-done items come from the three retrospectives where the user did **not** rule on each item: loosen-plan 4/6, fix-v2 4/7, task-prefixed 4/5. Retrospectives 4–6, which have per-item rulings, have no not-done item. Retrospective 1 (fix-tdd-transitive-claim) has no ruling record either; its one not-done item under the strict rule, 1.3, landed late.

  Two items had been parked as "observe first" with a trigger, and the trigger later fired without anyone coming back to them: 1.2 and 2.4. One-off item 3.7 also recurred (10/08). One not-done item affected **this change** without recurring: 7.5, adding the top-level README Status column to the coupling table. The table still lacked it, so the Status column in `2551ea0` was updated only because design D8 remembered it. The item that did **recur** in this change is 7.1: `plan.md` again writes "recorded" without naming the tracked file, though this time nothing was lost.
- **The schema says something that never happens.** The retrospective instruction says unchecked candidates "carry into the next cycle's retro for re-evaluation". Facts found:
  - No archived retrospective did this.
  - The template phrases it as optional ("可 grep").
  - Archived retrospectives are not edited, so their checkboxes never change: `2026-10-06` §6 item 3 became CLAUDE.md:66 and is still unticked.
- **An appended verify.md and the retrospective PRECHECK do not fit together** (verify Round 2 N3). The PRECHECK requires exactly one checked `Overall Decision` box. To keep Round 1 intact, Round 2 recorded its decision as bold text rather than a second box, so the machine check still reads Round 1's box. The two decisions agree here. If a later round disagreed with an earlier one, the check would read a stale verdict. The schema assumes verify.md is overwritten on each run; this change appended instead. No action now: one instance, and the user's ruling W3 asked that Round 1 be kept.
- **The fallback-review lesson recurred before release.** On 09-14, candidate 3.2 said a fallback verdict is enough to keep working but not enough to declare done. The 10/08 v4.0.0 release still went out with every external doc gate carried by the fallback reviewer (it did have SDD's internal reviews and an independent verify). This change is about to do the same: Codex was briefly available on 2026-10-12, then out of quota again.

## 6. Promote candidates → long-term learning

> Per candidate A: every item below gets an explicit user ruling at write time (`裁定：…`). An item without one is not finished.

- [ ] 🔴 **A. Rule on every §6 candidate while writing the retrospective; an unruled candidate is effectively lost.** → **Promote to** this retrospective's own practice now. Whether to write it into the schema's retrospective instruction is decided separately (see B).
  > **Why**: all 12 not-done candidates came from the three retrospectives without per-item rulings (§5 audit; 13 of 14 under the audit's stricter rule).
  > **How to apply**: at the end of every retrospective §6, before archive.
  > **裁定**：使用者 2026-10-12 同意（自本 retrospective 起照做）
- [ ] 🟡 **B. The schema's "unchecked candidates carry into the next retro" describes something that never happens.** → **Promote to** schema — rewrite the sentence or remove it. A separate change, not this one.
  > **Why**: §5. If a mechanism is described but never run, readers believe the learnings are tracked.
  > **How to apply**: if rewritten as a requirement, name its enforcement hook — who notices when it is not done — or downgrade it to Observe (global CLAUDE.md, 學習候選 rule 4).
  > **裁定**：使用者 2026-10-12 同意 AI 建議：記入 backlog，另開 change 處理，本 change 不動 schema
- [ ] 🔴 **C. A fallback review verdict is enough to keep working, not enough to release.** → **Promote to memory** (type: feedback; this is earlier candidate 3.2, still not done). Also, for this release: a **Codex re-review of the v5.0.0 implementation is owed once Codex quota returns**, recorded in the handoff baton.
  > **Why**: it recurred — v4.0.0 on 10/08, and v5.0.0 now.
  > **How to apply**: before tagging any release whose gates were all carried by fallback reviewers.
  > **裁定**：使用者 2026-10-12：Codex 無額度，發版前審查改派 Fable；依全域規則（2026-09-01）外部審恢復後補審
- [ ] 🟡 **D. Before calling something "verbatim", "identical" or "it read X", prove it with a diff against the source or a discriminating run.** → **Promote to memory** — refine the existing `feedback_claim_first_discriminating_oracle`.
  > **Why**: two over-claims in this change (§2), both caught by others.
  > **How to apply**: whenever a sentence is about to assert what a test or extraction proved.
  > **裁定**：使用者 2026-10-12 同意：補進既有 memory `feedback_claim_first_discriminating_oracle`
- [ ] 🟡 **E. Every design decision that changes agent-facing instruction text needs a requirement in the specs artifact.** → **Promote to** schema (the `specs` instruction), or keep as Observe.
  > **Why**: W6 — the core behaviour of this change had no spec axis until verify.
  > **How to apply**: when writing specs, map each design decision to a REQ or state why none is needed.
  > **裁定**：使用者 2026-10-12 同意 AI 建議：先 Observe，記入 backlog `[優化建議]`（目前 1 例）
- [ ] 📌 **F. Wording-only changes have now skipped SDD three times (8/31, 10/06, this change).** → **Promote to** the existing work item `task-20261012-non-sdd-execution-support` (registered in `80fd84b`) as evidence. No new item.
  > **Why**: REQ-4 requires a pattern of prior cases to be raised here. Each ruling covers only its own change.
  > **How to apply**: when that work item is picked up.
  > **裁定**：使用者 2026-10-12 同意：作為證據併入 `task-20261012-non-sdd-execution-support`
- [ ] 📌 **G. The first apply situation's label is narrower than its rule (verify Round 2 N2).** → **One-off** — not changed here; REQ-6 holds the correct scope.
  > **裁定**：使用者 2026-10-12 選乙（本 change 不改，記入 retrospective）

### 既往候選盤點的處置（使用者 2026-10-12 同意 AI 建議）

| 處置 | 項目 |
|---|---|
| 直接修，在本 change 之外單獨提交 docs commit | 7.5：CLAUDE.md 跨檔耦合表加入頂層 README 狀態欄。7.3：重新同步副本的說法改為「`superpowers-bridge/` 任何檔案」 |
| 記入 backlog `[優化建議]` | 2.3：重用 SDD 不等於繼承它的 commit 權限假設。3.5：CRLF 讓 diff 大小失真。7.1：plan 寫「recorded」要寫明記在哪個檔 |
| 寫明理由後結案：只發生一次、沒搜到再發生、原因仍屬推測 | 2.2、2.5、3.3、3.4、7.2 |
| 不重提 | 2.1：使用者 09-14 決定不開 backlog |
| 算「已做到（遲到）」，是再發生之後才從別的路徑補上 | 1.3：`feedback_smart_commit_tmpdir_windows`。3.6：`feedback_claim_first_discriminating_oracle` |
| 併入 C | 3.2 |
