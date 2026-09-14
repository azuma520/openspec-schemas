# Retrospective: fix-v2-blocking-defects

> Written: 2026-09-08 (after verify recorded ⚠️ PASS WITH WARNINGS)
> Commit range: `6c4605e..e38e817`
> Worktree: `.claude/worktrees/loosen-plan` (branch `worktree-loosen-plan`) — not merged, not pushed, not archived

> **Scope note on the range.** `6c4605e..HEAD` covers the *implementation*. This change's own
> artifacts (brainstorm, proposal, design, specs, plan, tasks skeleton) landed before `6c4605e`
> in an earlier session and are context here, not part of the measured diff.

---

## 0. Evidence

- **Commit range**: `6c4605e..e38e817` (4 commits)
- **Diff size**: **+1099 / −149 across 24 files** (`git diff --ignore-cr-at-eol --stat 6c4605e..HEAD`).
  The `--ignore-cr-at-eol` flag is load-bearing: the repo pins LF, the working copy is CRLF, and
  without it every line of every touched file reports as changed. Largest single file:
  `superpowers-bridge/schema.yaml` at +392/−79.
- **Tasks done**: **15/15** (`grep -cE '^\s*- \[x\]' tasks.md` → 15; `- [ ]` → 0; `- [~]` → 0)
- **Active hours**: ~9h of a ~24h wall-clock span. First artifact `.superpowers/sdd/plan/task-1.1-brief.md`（git-ignored 工作區，teardown 後不可複驗）
  at 2026-09-07 16:17; last at 2026-09-08 16:04. The ledger has one overnight gap (task 2.1 review
  17:04 → task 2.2 review 07:57), so the span crosses a date boundary but the work does not fill it.
- **Subagent dispatches**: **42 named agent seats** (implementers, reviewers, re-reviewers, the four
  fallback code-gate seats, the verify agent). Actual dispatch count is higher — several seats were
  *resumed* for fix rounds rather than replaced. Plus 5 external Codex dispatches on the doc plane
  (batch 0 first pass + 2 replies, batch 1 first pass, and the aborted code-plane dispatch).
- **New external dependencies**: none. This repo has no `package.json`, no source, no test framework.
- **Bugs encountered post-merge**: n/a — never merged, never pushed (`git ls-remote origin main`
  = `5aa19bf`, 24 commits behind HEAD, verified in task 5.3).
- **OpenSpec validate state at archive**: **not-run — archive not reached** (user ruling, §2 below).
  Current state: `openspec validate --all` → `Totals: 5 passed, 0 failed (5 items)`.
- **Test coverage signal**: no test framework exists. The equivalent is the mutation-fixture set:
  **13 fixtures, 13/13 verdicts re-derived independently** by the round-4 code reviewer against the
  new check text (`docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/code-rereview-fallback-3.md` § Regression, byte-identical copy of the SDD workspace report), plus
  `openspec schema validate superpowers-bridge` → `✓`.

Commit chain (時序):

```
6c4605e (base — artifacts from the prior session)
22c15cf docs(poc): add mutation fixtures f8-f13 for the five v2 checker defects
cffe99a fix(schema): make the v2 verify checks assert what their names claim
787b14c docs(bridge): bring every coupled surface in line with the corrected checks
e38e817 fix(schema): close the code-plane review findings and land the verify artifact
```

No archive commit exists. That is the change's current terminal state, by ruling.

---

## 1. Wins

- [evidence: `cffe99a`, `superpowers-bridge/schema.yaml` checks 7 and 9–12] **All five P1 defects
  are closed, and the closure was derived independently rather than inherited.** The round-4 code
  reviewer re-implemented the checks itself and re-derived all thirteen fixture verdicts
  (`code-rereview-fallback-3.md` § Regression), and the verify agent walked checks 8–12 from the
  raw `tasks.md` / `plan.md` text without consulting any review report (`verify.md` header note).
  Two derivations, same result.

- [evidence: `verify.md` §8, `code-rereview-fallback-3.md` § Self-application] **The change passes
  its own corrected checks.** Fifteen task numbers unique, fifteen plan entry keys unique, sets
  equal both directions; three applicable tasks, six subjects, twelve records, every subject
  conforming to the `::` grammar it introduced. Dogfooding worked as the design intended: had the
  new rules rejected the change that wrote them, that would itself have been the signal.

- [evidence: ledger 2026-09-07/08, `.superpowers/sdd/plan/progress.md:53`（git-ignored 工作區，teardown 後不可複驗）] **Fixtures first was
  the right inversion.** The plan ordered fixtures before checker edits so every RED could be
  obtained against pre-edit wording (`22c15cf` is the cited baseline in all six RED records in
  `tasks.md`, lines 61, 70, 81, 90, 99 and 110 — and the final reviewer re-ran every citation and
  confirmed each resolves). A RED written after the edit is a retro-written claim — precisely the defect class
  this change exists to close — and the ordering made that structurally impossible rather than
  merely discouraged.

- [evidence: ledger `progress.md:92`, `:160`] **Checking the tree beat believing the message,
  twice.** Two implementers hit usage limits mid-task and reported less than they had done. Task
  2.2's implementer died right after writing its report; the controller verified file mtimes
  (`task-2.2-red-walk.md` at 17:04 preceded the 17:09 schema edits, so the RED genuinely precedes
  the edit) and re-dispatched nothing. In the final fix wave, an agent's last message read
  "I'll start by reading…" while the tree already carried four of six completed fixes. Both times
  the recovery was reading the working tree instead of the transcript.

- [evidence: ledger `progress.md:109`] **A reviewer overturned a controller ruling on its premise,
  and the correction was recorded rather than absorbed.** The ruling that an absent `tasks.md`
  "is already blocked by checks 2 and 8–12" was false — those checks are universally quantified
  over task lines and pass *vacuously* when there are none. Only check 12 and the verify PRECHECK
  actually block. The conclusion survived; the premise did not, and it had already been written
  into shipped text. The re-reviewer then falsified the *replacement* premise the same way it had
  falsified the original.

- [evidence: `templates/verify.md`, `superpowers-bridge/README.md` + `.zh-TW.md`, `787b14c`]
  **The coupled-surface table in `CLAUDE.md` did its job** — templates and both language READMEs
  moved in the same commit as the checks they describe, and the `version-check.yml` grep contract
  survived: re-running the workflow's own `grep -E '^\| v2 \| \`'` + `awk -F'\`'` still yields
  `1.3.1` / `v5.1.0` (`tasks.md` task 3.2 control record).

## 2. Misses

- 🔴 [blocking | evidence: ledger `progress.md:185-187`, `verify.md` § Overall Decision warning 1]
  **The code-plane external review never happened.** Codex's quota was exhausted mid-dispatch
  (`[REVIEWER_FALLBACK] plane=code_review from=codex to=contract-neutral-reviewer reason=quota |
  2026-09-08T04:50:00Z`). A contract-aware fallback carried the gate over four rounds to
  `✅ Ready`. Per the global degradation clause that is **provisional assurance, not a closed
  external review** — and the user ruled that `archive` waits for it, on the reasoning that
  `archive` asserts "this delta may merge into the canonical spec" and that assertion must not
  rest on a fallback verdict. This is the one blocking miss, and it is open as of writing.

- 🔴 [blocking-class, caught before it shipped | evidence: ledger `progress.md:191-192`,
  `code-rereview-fallback-3.md` § Fifth recurrence] **"An instruction changed, its coupled
  template did not" recurred five times inside one change, and not once was it caught by the
  implementer who caused it.** Different reviewer each time. The instructive part is which repair
  worked: fixing the named instance failed three times in a row; a two-surface sweep closed it.
  The fourth recurrence then exposed a defect in the sweep itself — it scanned instruction →
  template only, so a rule that never entered the instruction was invisible **by construction**.
  Rebuilt as a 25-rule × 3-surface matrix (instruction / check text / template) scanned in both
  directions, it produced findings the one-way sweep could not have. The fifth recurrence was
  found by that matrix and ruled Minor.

- 🟡 [painful | evidence: ledger `progress.md:109`] **The controller ruled once on a premise it
  had not verified, and shipped it.** See §1 — the win is that a reviewer caught it; the miss is
  that "I ruled on a premise I did not verify" is the same defect class the change exists to
  close, committed by the person policing it.

- 🟡 [painful | evidence: ledger `progress.md:179`] **Two implementers ran in parallel on one
  file, against the SDD rule the controller had kept all run.** A stale idle notification was
  read as "the message was not received", so a second implementer was dispatched onto a task the
  first still had in its inbox. No conflicting write landed; the second was stopped and asked to
  report any edit plus its independent derivation. Same root as the two wins above — a stale
  message read as ground truth — but in the opposite direction: there, the message under-reported
  work that existed; here, it under-reported a message that had been delivered.

- 🟡 [painful | evidence: ledger `progress.md:128`, this file's §0] **A diff-size claim was wrong
  by an order of magnitude and was used in a review package.** "verify.md grew +406 lines" was a
  CRLF artifact; the real figure was ~+44 net. Every diffstat quoted in the run before that point
  was inflated the same way. The fix is mechanical — `--ignore-cr-at-eol` whenever the *size* of a
  diff is part of a judgement — and it is now stated in §0 so the next reader does not re-derive it.

- 🟡 [painful | evidence: ledger `progress.md:151`] **The prescribed `rm -rf` for the dogfood
  re-sync was denied by the permission system, twice.** The implementer did not spell a different
  delete to get past it (correct), and instead proved the end state equivalent. Accepted — but the
  equivalence held **only because this change deleted no file from the bundle**. A future change
  that removes one would leave it behind; `cp -R` without `rm -rf` is not interchangeable in general.

- 📌 [nit | evidence: `verify.md` §8 task 5.2 row] **A control record went stale inside the run.**
  Task 5.2's control asserted "22 added" for the errata append; a later correction to the same file
  made it 33. Found by verify, repaired by restating the *invariant* (removals stay 0) plus the
  command and base commit to re-derive it, rather than a count the next append invalidates again.

## 3. Plan deviations

| Plan task | What changed | Why |
|-----------|--------------|-----|
| 2.1 | Scope grew by one sentence: `schema.yaml:285`, the `plan` artifact instruction's definition of "1:1" as set identity, was folded in although no task owned it | The task's own edit created the contradiction — after 2.1 landed, that sentence would have told authors 1:1 means set identity while the checker blocks duplicates. Not one of the six enumerated P2s, so the "no P2 pulled in" non-goal is not engaged (ledger `progress.md:82`) |
| 2.2 | The R2 review-judgement amendment was folded into 2.2's fix round instead of being routed to 2.4 | The reviewer established that 2.4's residual-wording grep list does not match R2's phrasing — routing it to 2.4 meant nothing would catch it. The earlier routing decision had been made without that fact (ledger `progress.md:98`) |
| 2.2 / code-plane fix round (`e38e817`) | R1 review judgement widened: a RED recording `INDETERMINATE` for a rule executed by reading counts as a behavioural failure | Needed by f12's positive-control RED (`tasks.md` 2.2). Landed in the code-plane fix commit without a proposal / delta-spec declaration; declared post-hoc on 2026-09-10 after branch review r2 (fallback) flagged it as undeclared scope. `INDETERMINATE` stays RED-side only: never PASS, never a substitute for GREEN |
| 2.3 | The absent-`tasks.md` branch's stated justification was rewritten mid-task | The original premise was false (see §2). The fix names check 12 and the verify PRECHECK explicitly rather than gesturing at "the checks that read tasks.md" |
| 3.1 | `superpowers-bridge/templates/plan.md` was edited although task 3.1's text names only `templates/tasks.md` and `templates/verify.md` | The two-stage entry-key wording had to reach the plan-side author surface. Direction is consistent with D1/D6; recorded in `verify.md` §4 as "a coupled surface the task text did not name", non-blocking |
| 4.1+4.2 | Batched into one implementer dispatch rather than one each | Small, prose-only, single-file each, no shared file and no dependency — the SDD batching rule's exact case (ledger `progress.md:137`) |
| 5.1 | `rm -rf` replaced by in-place `cp -R` after two permission denials | See §2. End state proven equivalent by inventory comparison + `diff -r` + per-file md5 |
| — (not a task) | Scope deliberately **not** expanded at close-out: D2 and nine sibling gaps from the matrix left as follow-up | User ruling, §5 below |

## 4. Skill / workflow compliance

| Skill                                            | Used |
|--------------------------------------------------|------|
| superpowers:brainstorming                        | ✓ (prior session; `brainstorm.md`, 133 lines, §已查證依據 holds the line-level verification of each defect) |
| superpowers:writing-plans                        | ✓ (prior session; `plan.md`, 15 entries, Plan Contract shape) |
| superpowers:using-git-worktrees                  | ✓ (`.claude/worktrees/loosen-plan`, branch `worktree-loosen-plan`) |
| superpowers:subagent-driven-development          | ✓ (42 named seats; fresh implementer per task or batch, independent reviewer after each, fix loop, scoped re-review per round) |
| superpowers:test-driven-development (✓ only if the skill was explicitly invoked; write `N/A — annotation-driven` when TDD discipline came from the `TDD:` annotations in `tasks.md` and their RED/GREEN evidence instead) | **N/A — annotation-driven.** 3 tasks `TDD: applicable` (2.1, 2.2, 2.3) carrying 6 subjects / 12 records; 12 tasks `TDD: n/a`, each with the verification that replaces a test named in the reason |
| (structural via SDD) superpowers:requesting-code-review | ✓ (11 internal review seats + 4 re-review seats before the gates; then the external doc gate and the fallback code gate) |
| superpowers:finishing-a-development-branch       | ✗ — not reached |

### Deliberately Skipped Skills

- **`superpowers:finishing-a-development-branch`**
  - **What was skipped**: the whole skill, and with it `openspec archive`, the delta-spec sync,
    the push and the PR.
  - **Why this cycle**: the concrete trigger is
    `[REVIEWER_FALLBACK] plane=code_review from=codex to=contract-neutral-reviewer reason=quota |
    2026-09-08T04:50:00Z` — Codex's quota was exhausted mid-dispatch on the code plane, so the
    code gate closed on a fallback verdict (`code-rereview-fallback-3.md` → `✅ Ready`). The user
    then ruled (`progress.md:200-202`) that `archive` is not folder tidying — it asserts the delta
    may merge into the canonical spec — and that assertion must not rest on a fallback verdict.
    `verify` and `retrospective` are by contract pre-archive artifacts and are best written while
    the context is hot, so they proceed; everything downstream of them stops.
  - **How to prevent recurrence**: `scope-judgment rule` — this is not a skip to prevent, it is
    the degradation clause working as designed. The rule to keep is the one the user articulated:
    *a fallback verdict is sufficient to keep working and insufficient to declare completion, and
    the boundary between the two is the `archive` action, not the end of the session.* The debt
    ("Codex re-review of the code plane, findings fixed inside the still-active change") goes in
    the handoff and the change stays open until it clears.

## 5. Surprises

- **Eleven internal review seats all passed two defects that one external seat found.** The doc-plane
  Codex review (`gpt-5.6-sol`) found a self-contradiction *inside* `CLAUDE.md` — the structure tree
  at `:24` said 「本 repo 無 openspec/,不跑自己的 bridge 流程」 while the dogfooding section said the
  opposite, and `openspec/changes/fix-v2-blocking-defects/` demonstrably existed — and an answer-key
  row in the fixtures README that could not score the fixture it documented (both BLOCK verdicts were
  the same under old and new wording, so the binary question was undiscriminating). Both are now
  repaired (`CLAUDE.md:24`, `e38e817`). **Which layer caught what is the most reusable fact this
  change produced**: internal Claude seats caught per-task correctness reliably and cross-document
  contradiction not once in eleven tries; the external seat caught the contradiction on its first
  pass and the answer-key defect on its third round, after two attempts at the same row had failed.
- **The external reviewer also produced a false positive, and withdrew it itself.** It reported three
  named discussion files as absent from the repo root. They exist — untracked, and a git worktree
  does not receive untracked files, which is exactly where the reviewer was running. Dismissed on a
  directory listing rather than on judgement (`[DISMISS_VERDICT] CLAUDE.md:111`), and on round 2 the
  reviewer verified the files itself (confirming the 43k-line claim at 43,656 lines) and withdrew
  the finding. A half-clause about clones and worktrees was added anyway, at `CLAUDE.md:111` — this
  session was the case that proved it was needed.
- **The first `openspec schema validate` of the edited schema ran at task 5.1, not before.** Every
  earlier task could only run a YAML parse, and each said so. The whole of groups 2–4 was authored
  against a validator that had not yet been able to fail for the reason it claims to test.
- **"Deterministic" was three claims short.** The fallback code reviewer, reading the checks as an
  algorithm rather than as prose, found three inputs on which two conforming executors reach opposite
  verdicts: a record carrying two `subject:` lines (`code-review-fallback.md` I1), a `### 1.1` sub-heading
  under check 12's `##` collection (M1), and `- [x]1.1 Foo` with no whitespace after the `]` (M2).
  All three were latent in text whose *name* said deterministic — the same defect shape the change
  exists to close, one level down. All three are now closed.
- **The mutation fixtures survived the grammar they did not anticipate.** The biggest risk in the
  change was that the new `::` subject grammar would retroactively break f1–f7. It did not:
  twelve of thirteen fixtures still isolate exactly one defect under the new checks, re-derived by
  the reviewer's own implementation (`final-review.md`, `code-rereview-fallback-3.md`).

### Deferred, with evidence — carried out of this change

| Item | Evidence | Why deferred |
|---|---|---|
| **D2** — check 8 blocks on more than one `- TDD:` line while neither author surface states it | `code-rereview-fallback-3.md` § D2 characterisation: instruction `schema.yaml:175-181` says "exactly one of these two **forms**" (a form choice, not a cardinality); `templates/tasks.md:20` is silent; check 8 at `:576`, `:586-587` blocks on "more than one" | User ruling `progress.md:203`: real, but not caused by the five P1s and not a precondition of fixing them. The matrix found **nine gaps of the same family**, so it is a topic — "do all author-facing surfaces completely reflect the actual gate rules" — not two sentences. Pulling D2 in invites D3 next round |
| **The nine matrix gaps** (D1 separators, D4 blank-line transparency, row 15 `n/a`-by-design, the fifth recurrence at `templates/tasks.md:49-50`, and the rest) | `code-rereview-fallback-3.md` § Matrix audit, five rows audited cell by cell | Same family as D2, same ruling. Standing boundary for the rest of the change: no further scope expansion unless a gap is shown to affect the correctness of the five P1 fixes themselves |
| **Three latent ambiguities verify recorded rather than silently resolved** | `verify.md` §3 note, §5 note, §8 note 1 | (1) check 3 lists three outcomes but never says whether ✗ blocks — ruled non-blocking; (2) check 5 says "confirm all code changes are committed" but never says whether uncommitted files are FAIL or warning — ruled warning; (3) checks 8–12 define TASK LINE and `#` heading by first-non-space characters with **no exclusion for HTML comments or fenced code blocks** — this change's own `tasks.md` opens with a 40-line HTML comment, confirmed line by line to contain no `- [` or `#`-leading line, so it did not fire. A `tasks.md` with `- [ ] 1.1 …` inside a comment or a fence **would** be miscounted |
| **Four rules that now block with no fixture behind them** | `code-rereview-fallback-3.md` § Deferred observation; 2026-09-10 Codex branch review r1 (plan-key delimiter) | `###` in a plan, whitespace-after-`]`, and repeated-field-key were verified **by reading only**; the plan-key delimiter rule added to check 12 on 2026-09-10 (a `##` heading's leading number must be followed by whitespace or end of line — `## 1x` keys nothing) joins them. Four rules the corrected checker blocks on with no mutation fixture exercising them; a fixture for each is part of the same follow-up |
| **Candidate f14** — a fixture carrying both a duplicate *and* a set difference | ledger `progress.md:88` | The only input that distinguishes short-circuit from no-short-circuit in check 12. Not added: this change's own check 12 demands equal key sets, so adding one fixture means adding a task *and* a matching plan entry — a structural edit to the change's artifacts mid-implementation |
| **The outstanding external code review** | `verify.md` § Overall Decision warning 1 | See §2 and §4. The change does not archive until it clears |
| **`CLAUDE.md:187`'s `需從 2 bump`** | ledger `progress.md:142` | Hard-codes today's schema major and goes stale at the next bump. Left minimal-and-flagged; a version-independent rewording would have been a fourth unauthorised correction failing task 4.2's containment acceptance |

## 6. Promote candidates → long-term learning

- [ ] 🔴 **When a rule changes on one surface, sweep every surface that states any rule of that
      family — in both directions — never just the surface named in the finding.**
      → **Promote to memory** (type: feedback)
  > **Why**: "an instruction changed, its coupled template did not" recurred **five times inside a
  > single change** (ledger `progress.md:191-192`, `code-rereview-fallback-3.md` § Fifth recurrence),
  > each time caught by a different reviewer and never by the implementer who caused it. Fixing the
  > named instance failed three times running. A one-way sweep (instruction → template) then missed
  > a rule that never entered the instruction — invisible **by construction**, not by oversight.
  > The repair that finally worked was a rule × surface matrix scanned both ways.
  > **How to apply**: on any change that edits normative prose replicated across surfaces
  > (`schema.yaml` instruction / check text / `templates/*`, or spec / README / adopter fragment):
  > before declaring the fix round done, enumerate the rules and the surfaces as a grid and check
  > every cell, including the cells where a surface says *nothing*. A blank cell and an unexamined
  > cell look identical unless you mark them.

- [ ] 🔴 **A fallback review verdict is sufficient to keep working and insufficient to declare
      completion; the boundary is the irreversible action, not the end of the session.**
      → **Promote to memory** (type: feedback)
  > **Why**: the user's ruling on 2026-09-08 (`progress.md:200-202`) sharpened the controller's own
  > proposal: `archive` is not folder tidying, it asserts "this change is complete and its delta may
  > merge into the canonical spec", and that assertion must not rest on a fallback verdict. `verify`
  > and `retrospective` are pre-archive by contract and are best written hot, so they are unaffected.
  > **How to apply**: whenever `[REVIEWER_FALLBACK]` is recorded on a gate — identify the change's
  > irreversible action (archive / merge / publish / release), do everything *before* it while the
  > context is hot, stop there, and put the external-review debt in the handoff.

- [ ] 🔴 **Check the working tree before believing an agent's last message — in both directions.**
      → **Promote to memory** (type: feedback)
  > **Why**: three incidents in one change, from one root cause. Twice an agent hit a usage limit and
  > reported less than it had done (`progress.md:92`, `:160`) — inspecting the tree recovered two
  > complete pieces of work. Once the error ran the other way: a **stale idle notification** was read
  > as "message not received", a second implementer was dispatched onto the same file, and two
  > implementers ran in parallel against the SDD rule (`progress.md:179`). No conflicting write landed.
  > **How to apply**: before re-dispatching, resuming, or concluding an agent failed — read the tree
  > (`git status`, file mtimes, the actual diffs), then the inbox state. Never the notification text.

- [ ] 🟡 **Before ruling on a premise, verify the premise — a vacuously-true check is not a check.**
      → **Promote to memory** (type: feedback)
  > **Why**: the controller ruled that an absent `tasks.md` "is already blocked by checks 2 and 8–12".
  > Those checks are universally quantified over task lines and pass **vacuously** when there are
  > none; only check 12 and the verify PRECHECK block. A reviewer proved it and the premise had
  > already been written into shipped text (`progress.md:109`). The conclusion survived, which is
  > exactly why the error was invisible.
  > **How to apply**: when a ruling rests on "X is already covered elsewhere", open the elsewhere and
  > check it fires on the actual input. Universally-quantified rules over an empty set are the
  > canonical trap: they report success and assert nothing.

- [ ] 🟡 **Use `--ignore-cr-at-eol` on every diff whose *size* is part of a judgement.**
      → **Promote to project CLAUDE.md** (`CLAUDE.md`, 「沒有 build / test / lint」 or a Windows-notes section)
  > **Why**: this repo pins LF while Windows working copies are CRLF, so a bare `git diff --stat`
  > reports every line of a touched file as changed. A review package in this very change claimed a
  > file "grew by 406 lines"; the real figure was ~44 (`progress.md:128`). The claim was wrong by an
  > order of magnitude and no layer flagged it — the number simply looked alarming and was believed.
  > **How to apply**: any diffstat that enters a review package, a retrospective, a handoff or a
  > containment acceptance. Not needed when the diff is being *read* rather than *measured*.

- [ ] 🟡 **An answer key must record the discriminating result, not the intent.**
      → **Promote to project CLAUDE.md** (fixtures README convention, `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md`)
  > **Why**: the fixtures README's verdict table was written against each fixture's *intent* rather
  > than re-derived under the checks in force, so f2's row went stale (final review, Important #4)
  > and f13's row recorded "no BLOCK" — an answer identical under both old and new wording, so the
  > binary question could not score the fixture at all (doc gate batch 0, round 2). The row now
  > records the discriminating fact: current check 7 reads tasks.md and finds 1 deferred task; old
  > check 7 read plan.md and found 0; neither blocks.
  > **How to apply**: whenever a fixture's expected verdict is recorded, ask what a *correct* run
  > and an *incorrect* run would each produce. If they produce the same token, the row is not an
  > answer key — widen what the row asks for.

- [ ] 📌 **`cp -R` without `rm -rf` reaches the same state only when nothing was deleted from the source.**
      → **One-off** (recorded; already stated in `tasks.md` task 5.1's control record)
  > **Why**: the dogfood re-sync's prescribed `rm -rf` was denied twice by the permission system.
  > The implementer proved equivalence instead of spelling a different delete — correct behaviour —
  > but the equivalence rested on this change removing no file from the bundle (`progress.md:151`).
  > **How to apply**: it does not generalise into a rule, it generalises into a *check*: before
  > substituting an in-place copy for a delete-then-copy, list what exists in the destination and
  > not in the source. Non-empty ⇒ the two are not interchangeable.
