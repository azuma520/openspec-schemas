# fix-tdd-transitive-claim Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **In this repo** the maintainer executes inline (docs-only change, single session) — the review gates below are the required evidence either way.

**Goal:** Delete every claim that upstream automatically enforces TDD, replace it with the honest conditional statement, and correct the `executing-plans` rationale — nothing else.

**Architecture:** Text-only edits over the frozen Affected Surface (brainstorm §4.1: 35 segments / 21 logical positions). No artifact graph change, schema major stays 1. Every new sentence must pass the D2 test (spec `tdd-claim-accuracy`): claims conditional, negatives scoped to "no layer **guarantees**".

**Tech Stack:** OpenSpec CLI 1.3.1 (validate + smoke), git, review chain (`/codex-review-fast` code plane, `/codex-review-doc` doc plane, fallback per auto-loop rules).

**Spec:** `openspec/changes/fix-tdd-transitive-claim/specs/tdd-claim-accuracy/spec.md` (+ `design.md` D1–D7)

## Global Constraints

- Corrective-fix exception scope: ONLY delete/correct falsified claims — no gate, no evidence mechanism, no new capability (CLAUDE.md event gate).
- Identify segments by meaning; 2026-08-27 line numbers are for relocation only. Do not re-run discovery scans (design D7).
- en / zh-TW README edits land symmetrically, same commit per file pair.
- Record-class files (handoffs, discussion material, archives) untouched.
- `git add/commit` only via `/smart-commit --execute` with user approval (repo git rules); commit points below mean "checkpoint: propose a commit".
- After any `superpowers-bridge/` edit lands: re-sync dogfood copy before running opsx commands.

---

### Task 1: schema.yaml — false guarantee body + fallback rationale + header

**Files:**
- Modify: `superpowers-bridge/schema.yaml` (5 segments: description :8-12 and :19-20; plan instruction :186 untouched — true claim; PRECHECK :474-475; apply step 2 :507-518; fallback :521-526)

**Interfaces:**
- Consumes: frozen wording from design D2/D3.
- Produces: the honest-statement block later tasks' README wording must stay consistent with.

- [x] **Step 1: Replace the apply-step-2 transitive-activation block** (currently "IMPORTANT — transitive skill activation: … internally enforces … every task follows RED-GREEN-REFACTOR … Implementation code written before a failing test is deleted. … requesting-code-review — after each task …"). New text:

```
       IMPORTANT — how TDD and code review actually arrive:

       Whether TDD is executed depends on whether the task list
       requires it. superpowers:writing-plans' standard task format
       contains TDD micro-steps (failing test → verify fail →
       minimal implementation → verify pass), but whether each task
       carries them depends on that skill's judgment of the task
       type (upstream prescribes no tests for prose-only work).
       This schema itself neither enforces nor verifies TDD; if a
       task lacks a TDD requirement, no layer of this schema
       guarantees to add one.

       Code review is structural: subagent-driven-development
       dispatches reviewer subagents during execution and a final
       review before apply concludes (it may batch several small
       same-shape tasks into one reviewed diff — not strictly one
       reviewer per task).
```

- [x] **Step 2: Replace the fallback-rationale block** (currently "Per its SKILL.md, executing-plans does not transitively activate TDD or code-review — defeating the rigor…"). New text:

```
       This schema does NOT support `superpowers:executing-plans`
       as a fallback for non-subagent platforms. Per its SKILL.md,
       executing-plans dispatches no independent reviewer — a
       single agent executes the plan and self-checks — and
       upstream itself directs users to subagent-driven-development
       whenever subagents are available. (TDD is not the
       differentiator: when a task requires it, both executors
       receive that requirement through plan.md task content;
       neither path guarantees it otherwise.) If your platform
       lacks subagent support, use
       the built-in `spec-driven` schema instead of this one.
```

- [x] **Step 3: Fix the header description.** :10-11 "because the alternative executor (executing-plans) loses TDD and code-review transitive activation, defeating Superpowers' value." → "because the alternative executor (executing-plans) dispatches no independent reviewer, losing the review rigor Superpowers brings." :19-20 "(brings TDD and code-review transitively)" → "(structural code-review dispatch; TDD arrives via plan.md task content when tasks require it)".

- [x] **Step 4: Fix the PRECHECK annotation.** :474-475 "(transitively: superpowers:test-driven-development, superpowers:requesting-code-review)" → "(which dispatches superpowers:requesting-code-review; TDD discipline arrives via plan.md task content — superpowers:test-driven-development is not separately invoked by this schema, though an implementer may self-trigger it)" (final wording after doc-review round 2). The two skill names remain in the annotation as documentation; the PRECHECK bullets independently verify only the three top-level apply skills, as before this change.

- [x] **Step 5: Verify the falsified phrases are gone from schema.yaml**

Run: `grep -n -i "internally enforces\|do NOT need to invoke\|every task[[:space:]]*$\|loses TDD" superpowers-bridge/schema.yaml`
Expected: 0 matches (RED-GREEN may remain only inside the honest conditional sentence if used; target: no unconditional claim).

- [x] **Step 6: Re-sync dogfood copy + validate**

Run: `rm -rf openspec/schemas/superpowers-bridge && cp -R superpowers-bridge openspec/schemas/`
Then the CLAUDE.md /tmp procedure: `openspec schema validate superpowers-bridge` + `openspec schemas` in a clean test project.
Expected: validate passes; `superpowers-bridge` listed.

- [ ] **Step 7: Checkpoint — propose commit** `fix(schema): replace false TDD-enforcement claim with honest conditional statement`

---

### Task 2: Bridge READMEs (en + zh-TW, symmetric)

**Files:**
- Modify: `superpowers-bridge/README.md` — 14 segments: body :213, :247, :282, :304, :305, :328, :368, :381, :383, :443, :445; fallback :310, :449, :553
- Modify: `superpowers-bridge/README.zh-TW.md` — the 14 mirror segments (same content positions)

**Interfaces:**
- Consumes: Task 1's honest-statement wording (README claims must not exceed it).
- Produces: none downstream.

- [x] **Step 1: Correct the 11 body segments in README.md.** Per segment (locate by content):
  - :213 table row "(with TDD + code-review transitive)" → "(structural code review; TDD via plan micro-steps when tasks require it)"
  - :247 mermaid label "↳ TDD + code-review (transitive)" → "↳ structural code review; TDD per task content"
  - :282 "(+ TDD + code-review transitive)" → "(+ structural code review; TDD when tasks require it)"
  - :304 skills-table row 5 "(activated inside #4) | **Transitive**" → "(TDD discipline arrives via plan.md task content; the schema does not invoke this skill — an implementer may self-trigger it) | **Conditional**" (final wording after doc-review rounds 1-2)
  - :305 row 6 "(activated inside #4) | **Transitive**" → "(dispatched by #4; batching possible) | **Structural**"
  - :328 comment "(with TDD + code-review)" → "(structural code review; TDD per task content)"
  - :368 "(transitive: `test-driven-development`, `requesting-code-review`)" → "(dispatches `requesting-code-review`; TDD discipline arrives via plan.md task content — `test-driven-development` is neither prechecked nor schema-invoked, though an implementer may self-trigger it)" (final wording after doc-review round 2)
  - :381 "Each subagent transitively activates:" → "Each subagent works from its task's content:"
  - :383 TDD bullet "write failing test → … gets deleted" → "**TDD discipline** (via plan content): the task's micro-steps carry RED→GREEN when `writing-plans` judged the task to need tests; the schema does not invoke `superpowers:test-driven-development` itself, and the executor does not enforce it — an implementer may self-trigger the skill" (final wording after doc-review rounds 1-2)
  - :443 heading "### 3. Transitive dependencies made explicit" → "### 3. How TDD and code review actually arrive — made explicit"
  - :445 body → "TDD and code-review used to be described as hidden transitive activations. Our schema's apply step 2 instruction now states the conditional truth explicitly — TDD depends on plan.md task content; code review is structurally dispatched — so a reader sees what is and is not guaranteed during apply at a glance."
- [x] **Step 2: Correct the 3 fallback segments in README.md** (:310, :449, :553) to the D3 rationale — no independent reviewer + upstream's own direction to SDD; explicitly retire the TDD comparison. Keep each segment's surrounding structure (blockquote / design-touch prose / lifecycle bullet); keep the SKILL.md link, re-purposed as evidence for "no reviewer dispatch and no TDD/code-review mention".
- [x] **Step 3: Mirror all 14 segments in README.zh-TW.md**, translating the same corrections (「傳遞」/「自動」guarantee phrasing goes; conditional phrasing arrives), segment-by-segment symmetric.
- [x] **Step 4: Verify symmetry and residue**

Run: `grep -n -i "transitiv\|傳遞" superpowers-bridge/README.md superpowers-bridge/README.zh-TW.md`
Expected: remaining hits are only in honest/record rows (:498-506 drift table en; zh mirror) — none states an active guarantee. Then eyeball-count corrected segments: 14 per file.

- [ ] **Step 5: Checkpoint — propose commit** `docs(bridge): correct TDD claims and executing-plans rationale in both READMEs`

---

### Task 3: retrospective template + CLAUDE.md red flag + top-level READMEs + VERSION

**Files:**
- Modify: `superpowers-bridge/templates/retrospective.md` (semantic block §4, ~:55-84)
- Modify: `superpowers-bridge/schema.yaml` (retrospective-instruction "Skipped-skill rules for §4" block — the schema-side twin, found in review round 1; see Step 0)
- Modify: `CLAUDE.md` (red-flag bullet, currently :217)
- Modify: `README.md` + `README.zh-TW.md` (bridges table, line 11)
- Modify: `superpowers-bridge/VERSION` (1.0.0 → 1.0.1)

- [x] **Step 0 (added in review round 1): Defuse the schema-side twin.** `schema.yaml`'s
      retrospective instruction carried the same inducement ("Default expectation: §4 has
      every row marked ✓" + the vague-reasons ban) — rewritten to the truthful framing,
      matching the template. This is the 6th schema segment in the proposal's Impact.
- [x] **Step 1: Defuse retrospective.md §4.** Keep the table; change the two `(transitive)` row labels — final wording after doc-review round 2: for TDD, "✓ only if the skill was explicitly invoked; write `N/A — plan-step TDD only` when TDD discipline came from plan steps alone"; for code-review, `(structural via SDD)`. Replace the "Default expectation: 全部 ✓ … 跳過屬於異常情境" note with: "如實勾選。TDD 與 code-review 兩列依上方標註本就是條件性/結構性的——沒被要求就不算跳過。任一項確實被跳過時,在下方 subsection 記錄原因。" Replace ":69-70" escape-hatch framing ("整節空白(全綠)是預期狀態") with "本節記錄實際發生了什麼;空白代表沒有刻意跳過,不是達標證明。" In the three-questions block, delete the ban on honest reasons — "不可寫『不需要』…" becomes "理由要具體(寫實際 trigger:commit / log / 觀察到的行為);『不需要』需要說明為什麼不需要". Keep the §6 promote-candidates linkage note.
- [x] **Step 2: Reword CLAUDE.md red-flag bullet** (:217) to: "❌ 在 apply instruction 加 `superpowers:executing-plans` 當 fallback(它不派任何獨立審查者——單 agent 自跑自查,上游在有 subagent 時也明示改用 subagent-driven-development;TDD 兩邊都靠任務單內容、不是差異點。缺 subagent 就叫使用者改用內建 `spec-driven`)"
- [x] **Step 3: Fix top-level bridges table** (both languages, line 11): `brainstorming, writing-plans, TDD-via-subagents, code review, finishing` → `brainstorming, writing-plans (TDD micro-steps), subagent execution with structural code review, finishing`; zh-TW mirror: `brainstorming、writing-plans(TDD 微步驟)、subagent 執行與結構性 code review、finishing`.
- [x] **Step 4: Bump VERSION** to `1.0.1`. Do not touch the Compatibility table `v1` row key (CI grep depends on its shape).
- [x] **Step 5: Verify residue repo-wide (non-record surfaces)**

Run: `grep -rn -i "TDD-via-subagents\|internally enforces\|do NOT need to invoke" README.md README.zh-TW.md CLAUDE.md superpowers-bridge/ docs/roadmap.md docs/roadmap.zh-TW.md`
Expected: 0 matches.

- [x] **Step 6: Re-sync dogfood copy again** (retrospective.md changed): `rm -rf openspec/schemas/superpowers-bridge && cp -R superpowers-bridge openspec/schemas/` and re-run validate + smoke.
- [ ] **Step 7: Checkpoint — propose commit** `docs: correct remaining TDD false-premise surfaces (template, red flags, top README) + bump bundle to 1.0.1`

---

### Task 4: Sweep + review chain (the change's evidence)

**Files:**
- Test: no test framework — evidence is the review chain + validation commands above.

- [x] **Step 1: Spec sweep.** Re-read every edited segment against the four requirements in `specs/tdd-claim-accuracy/spec.md`. For each absolute claim kept or added, hunt one counter-example before keeping it (global rule). Record the sweep result in the conversation.
- [ ] **Step 2: Code plane review.** Dispatch `/codex-review-fast` (probe Codex; on failure record `[REVIEWER_FALLBACK]` and use the fallback carrier). Fix blocking findings, return for re-verification. On ✅ Ready: run precommit-equivalent (validate + smoke already green) and note verdicts: `node .claude/scripts/review-state.js note code_review pass` / `note precommit pass`.
- [ ] **Step 3: Doc plane review.** One `/codex-review-doc` dispatch over all edited `.md`. Fix and return until ✅ Mergeable; `note doc_review pass`.
- [ ] **Step 4: Update tasks.md checkboxes** for groups 1–4 as they complete.
- [ ] **Step 5: Checkpoint — propose final commit** (any review fixes + tasks.md) and hand to verify artifact.

## Self-Review (done at plan time)

- Spec coverage: Req 1 → Tasks 1–3 + residue greps; Req 2 → Task 1 Step 1; Req 3 → Task 1 Steps 2–3, Task 2 Step 2, Task 3 Step 2; Req 4 → Task 3 Step 1. No gaps.
- Placeholder scan: all steps carry exact wording or exact commands; per-segment README table gives content-addressed instructions.
- Consistency: honest-statement wording identical between Task 1 Step 1 and the README conditional phrasings; "no layer guarantees" scoping used everywhere a negative appears.
