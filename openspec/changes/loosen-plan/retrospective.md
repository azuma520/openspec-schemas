# Retrospective: loosen-plan

> Written: 2026-09-03 (after verify passed with warnings)
> Commit range: `5aa19bf..84df208` — four commits (pinned to literal SHAs; `HEAD` re-evaluates on
> every read and would make this line false as soon as another commit lands)
> Worktree: `.claude/worktrees/loosen-plan` on branch `worktree-loosen-plan`

---

## 0. Evidence

- **Commit range**: `5aa19bf..84df208` — 4 commits (`932a044`, `a4c761c`, `31d012c`, `84df208`)
- **Diff size**: `git diff --shortstat 5aa19bf..84df208` → **18 files changed, +1614 / −184**.
  An earlier figure here read "15 files changed, +688 / −170"; the file count matched the then-current
  two-commit range but **the ± figures reproduce against no range at all** (`5aa19bf..a4c761c` gives
  15/+682/−166), so they are replaced by a pinned range with its command rather than by a
  closer-looking guess. Recorded because this is the same defect class §2 collects — a stat that was
  plausible and unrecomputable, sitting in a section headed *Evidence*
- **Tasks done**: **27/27** — reopened from 25/25 at verification (see §3) and closed again after review
- **Active hours**: ~8 across two calendar days (2026-09-02 into 2026-09-03), one session
- **Subagent dispatches**: **~31, and this figure is NOT evidence-backed** — approximately 10
  implementers, 11–13 task reviewers / re-reviewers, 2 blind evaluators, 2 plan producers, 2 plan
  scorers, 1 whole-branch reviewer, plus 1 review that died on a capacity limit.
  **The disagreement is between this bullet's own breakdown and §4**: §4 states 9 implementer
  dispatches and 11 task reviews / re-reviews, which agrees with `verify.md` §15's 11 — it is this
  bullet's "~10 / 11–13" that neither matches. **Nothing in the repository settles it.** The SDD ledger
  records dispatches in prose rather than in a countable form — a mechanical pass over it finds only
  three agent identifiers — so every one of these figures is a reconstruction from the session, not a
  derived count. Recorded as a discrepancy rather than reconciled to a plausible number, per this
  change's own standard: a count with no source is not made true by picking the one that looks right.
  What the workspace does hold is the review **artifacts** — 17 `review-*.diff` packages plus
  `branch-review.txt` and `task11-review.txt` — and their existence is a stronger fact than any of
  these counts, while still not establishing which of them is right.
- **New external dependencies**: none
- **Bugs encountered post-merge**: n/a — not merged
- **OpenSpec validate state**: `openspec validate loosen-plan` → valid
- **Test coverage signal**: n/a — this repo has no build/test/lint. The standing verification is
  `openspec schema validate` + instruction render + targeted greps, and for this change additionally a
  seven-fixture mutation exercise run by a blind third party

Commit chain:

```
5aa19bf  (base) docs(loosen-plan): artifacts 6/8
932a044  feat(schema): plan becomes a contract, TDD becomes evidence (v1 -> v2)
a4c761c  docs(bridge): carry the v2 contract into templates, docs and CI
31d012c  fix(schema): close v1 residue and the fail-open retrospective PRECHECK
84df208  (head) docs(loosen-plan): land verify and retrospective, tasks 27/27
```

---

## 1. Wins

- [evidence: blind run, 6 fixtures + 1 control] **The five deterministic checks were proven by someone who
  could not have known the answers.** An agent with no context, given only the rendered verify instruction
  and six fixtures under neutral shuffled names, mapped all six correctly and reported zero ambiguities.
  The fixture directories were originally named `f1-missing-annotation`, `f3-pass-marker-on-red` … — **the
  answers were in the paths**, and a run against them would have scored 6/6 while proving nothing. Caught
  at the last moment before dispatch.
- [evidence: fixture f7] **A positive control was added unprompted by the implementer**, after the
  blank-line rule changed: a conforming record with blank lines that must *not* block, verified to have
  been a false BLOCK under the previous reading. Six fixtures proved the checks catch violations; f7 is the
  only one that proved they pass conforming work.
- [evidence: `schema.yaml` verify block, HEAD vs tree] **Guardrail 8 was established against the right
  baseline** — 108 of 108 pre-existing lines preserved, opcodes `['equal','insert']` only — and confirmed
  independently by a reviewer reading the hunk header rather than trusting the author's own difflib run.
- [evidence: `README.md:306`, `README.zh-TW.md:306`] **A pre-existing error was caught because reviews were
  pointed at `schema.yaml`, not at the other language version.** Both locales said `finishing-a-development-branch`
  hangs off apply step 4; it is step 6. The translation had faithfully mirrored a v1 error, so the two
  versions **agreed with each other and were both wrong**. A consistency check between locales passes this
  every time.
- [evidence: final whole-branch review] **The whole-branch pass found a contradiction inside one file that
  no per-task review could have seen**: the plan instruction defines an entry as a `##` heading while
  check 12 collected any `#` heading — and the check's own sentence claimed it "introduces nothing of its
  own". Each side had been reviewed with a different task.
- [evidence: group 11, `tasks.md`] **The completion count was reopened rather than defended.** At 25/25 with
  verify written, two holes were known: three normative surfaces still carrying a v1 TDD claim, and a
  fail-open PRECHECK. Ticking through would have meant "all tasks complete" while both stood. The owner
  reopened to 25/27 on the ground that these are **task-coverage holes, not scope expansion** — the specs
  already required those surfaces to be true, the breakdown simply missed them. Closed at 27/27 after fix
  and review. **A completion count that cannot go backwards is a count that stops meaning anything.**
- [evidence: `schema.yaml` retrospective PRECHECK, four exercises] **A guard was broken on purpose before
  being believed.** The amended PRECHECK was run against a real verdict, a verdict-less file and an
  ambiguous two-verdict file; and the **old** command was run against the verdict-less fixture, where it
  returns exit 0. The hole was demonstrated, not described — and the demonstration is what distinguishes
  "we changed the check" from "the check now catches it".

---

## 2. Misses

- 🔴 [blocking | evidence: ledger defects, plus two found at the doc gate] **Eleven controller-made
  defects, and ten of them produced a plausible-looking wrong result rather than an error.** A flat
  snapshot that reported a whole file as DELETED; a stat that silently dropped blank lines (`+61 −18` for
  a `+70 −22` change); fixture directory names carrying the answers; a package section printing repo-wide
  status as if it were the task's; a snapshot review package leaving two live baselines, which made two
  reviewers report false positives; a CRLF→LF rewrite that git hid by normalising; a fidelity fix that
  weakened a blinding; a substring probe that missed a wrapped sentence; a check result that stayed on the
  record after its subject changed; and a line count reported as an occurrence count. **None of those ten
  errored.** The eleventh — a `/tmp` path meaning different directories to Git Bash and Windows Python —
  is the only one caught before it produced anything, and the only one with an enforcement hook. The last
  two were found by the independent doc-gate review, after this section first said "nine".
- 🔴 [blocking | evidence: class-(b) sweep, first version] **A silent zero was trusted as evidence.** An ad hoc grep
  returned nothing for two surfaces and was recorded as "0 hits"; the real counts were 1 and 4. The
  conclusion survived — all five missed hits were negations or out of scope — but **the evidence behind it
  had not**. It prompted a re-verification of my own class-(a) sweep through a different code path, with a
  positive control, because the two failure modes are byte-identical in output.
- 🟡 [painful | evidence: 10.4 run 1, discarded] **The first Q4-A sample measured a condition no adopter is in.** I
  withheld `templates/plan.md`, which the CLI ships inside the same artifact block, and built a fixture
  whose "uncoupled" task consumed a shape and a set of names from its siblings. Two of the four scores were
  therefore uninterpretable. Discarded and re-run on a corrected instrument — **and the discard was
  recorded before the second run existed**, which is the only thing that makes the boundedness claim
  checkable rather than convenient.
- 🟡 [painful | evidence: fix round scoping, R32] **I twice took a review's enumeration as the scope instead of sweeping
  the class.** The `v1` wording fix was scoped to three named phrases and left a fourth instance; the class
  sweep found it one round later. The repo's own rule says one defect means one class.
- 🔴 [blocking | evidence: `verify.md` Overall Decision, first version] **My own verification report
  summarised itself too favourably** — "No CRITICAL. No WARNING." while its §11.3 recorded a defect in
  shipped contract text. A reader of the decision alone would have taken away less than the file
  established. **And the correction was itself wrong**: the paragraph recording it stated a `schema.yaml`
  line count of 902 against an actual 916 — inside the very sentence asserting the counts had been
  checked. Caught at the doc gate, two rounds later.
- 📌 [nit | evidence: doc gate rounds 1–3] **My fixes have a measurable defect rate.** Repairing three
  blocking findings in round 2 introduced two new ones in round 3 — both in the sentence written to record
  a discrepancy honestly. This is the argument for re-reviewing a fix rather than trusting it, stated as a
  measurement rather than as caution.

---

## 3. Plan deviations

- **Task 4.2's premise was false from the start.** It said to update `templates/verify.md` "§4 TDD rows";
  that file contained no TDD text at all (`git show 5aa19bf:… | grep -i tdd` → 0 hits) and its §4 is a
  design-coherence section. A new §8 was added instead. The task text is left unedited as the historical
  record; the wording it describes lives in `templates/retrospective.md` and the retrospective instruction,
  which **no task in this change covers** — an open scope decision for the owner.
- **Task 10.1's literal command could not be run.** `rm -rf` is denied to agents in this environment, so
  the dogfood re-sync used overwrite-copy plus `diff -r`. Equivalent here only because this change deletes
  no file from the bundle, which was verified rather than assumed. A reviewer later pointed out the check
  was stronger than claimed: `diff -r` reports destination extras as `Only in …`, so the empty diff proved
  tree identity on its own.
- **Two rulings widened a check rather than tightening it, on an explicit asymmetry argument** (R10
  separators, R26 blank lines): a stricter reading would false-BLOCK conforming artifacts, while the looser
  reading can never accept *missing* evidence. Both are recorded with that reasoning rather than as taste.
- **Commit granularity was changed by owner ruling (R8).** SDD's normal flow has each implementer commit
  per task; this repo's governance forbids agent commits outside three enumerated workflows. Reviews stayed
  task-level, commits became group-level, and **a commit is explicitly not evidence that a review
  happened** — the ledger, the per-task diffs and the review reports carry that.

---

## 4. Skill / workflow compliance

| Skill | Used |
|---|---|
| superpowers:brainstorming | ✓ (prior session — Q1–Q5 rulings in `brainstorm.md`) |
| superpowers:writing-plans | ✗ — **by design**: this change removes it as a dependency; `plan.md` was written directly to the Plan Contract |
| superpowers:using-git-worktrees | ✓ — native `EnterWorktree`, per the skill's own preference for a platform tool |
| superpowers:subagent-driven-development | ✓ — 9 implementer dispatches, one fresh agent per batch |
| superpowers:test-driven-development | **N/A — every task in this change is honestly `TDD: n/a`** (YAML, Markdown and a CI workflow; no unit-testable subject). Not "plan-step TDD only": under v2 applicability is declared per task in `tasks.md`, and this change's tasks declare it does not apply |
| (structural via SDD) superpowers:requesting-code-review | ✓ — 11 task reviews / re-reviews plus one whole-branch review |
| superpowers:finishing-a-development-branch | pending — the PR is the last step |

> The `test-driven-development` row is filled at v2's semantics deliberately. When this section was
> first written the template still offered `N/A — plan-step TDD only` — the superseded v1 claim this
> change removes — so using it would have contradicted the change in its own retrospective. **Task 11.1
> then rewrote that row**: the shipped template now offers `N/A — annotation-driven`
> (`superpowers-bridge/templates/retrospective.md:59`), and `plan-step TDD` returns 0 hits across all
> bridge-owned surfaces (§12, §14.1). This sentence is kept in corrected form rather than deleted,
> because the gap between the two states is what task 11.1 existed to close.

### Deliberately Skipped Skills

- **`superpowers:writing-plans`** — not a skip in the escape-hatch sense: this change **removes** it as a
  normative dependency and removes its PRECHECK, on the argument (design D7) that the check's *subject* is
  gone. The whole-branch review ruled that argument sound. It remains permitted as a private aid.

---

## 5. Surprises

- **The check found its first defect in the thing it checks.** Written to compare tasks.md task numbers
  against plan.md entry keys, check 12's first real catch was that the shipped v1 `templates/plan.md`
  (`## Task 1: …`) yields **zero** entry keys — so a plan written from the old template would be blocked by
  the new check. A real migration problem, invisible until the check existed.
- **The producer-side and reviewer-side blindness are the same property.** A plan entry that is the
  *upstream* end of a coupling has nothing to consume when it is written, so a consumer-first Interfaces
  field cannot see the edge from there; and a reviewer reading one entry is never forced to build the
  coupling graph that would reveal the omission. Two independent agents reached the two halves separately.
- **A guard I specified was wrong three times in one sentence.** The "naming is not requiring" blockquote —
  added precisely to stop *named* skills being read as *required* — miscounted the PRECHECKed skills,
  misplaced `executing-plans`, and mis-described `writing-plans`.
- **The retrospective's own PRECHECK is fail-open.** It runs `! grep -q '^- \[x\] ❌ FAIL' verify.md`. A
  verify.md that omits the template's three decision checkboxes passes it **because the thing it looks for
  is absent** — which is exactly what my first draft did. Fixed in this change's own artifact by adding the
  checkboxes; the PRECHECK's shape is untouched and is recorded below.

---

## 6. Promote candidates → long-term learning

- [ ] 🔴 **A zero from a reader that read nothing is byte-identical to a zero from a reader that read
      everything** → **Promote to CLAUDE.md** (strengthen the existing "0 hits ≠ absence" rule)
  > **Why**: two live instances this session — a silently-failing grep trusted as evidence (class-(b)
  > sweep reported 0 hits for two files that actually had 1 and 4), and my own substring probe returning
  > "not found" for a sentence the file wraps.
  > **How to apply**: every "expect 0" check ships with a positive control that proves the reader read,
  > plus an explicit report of what it could not open.

- [ ] 🔴 **Bilingual agreement is not evidence of correctness** → **Promote to CLAUDE.md**
  > **Why**: `apply step 4` was wrong in the English README and **faithfully mirrored** into zh-TW; both
  > locales agreed and both were wrong. A review comparing translation against source is blind to this.
  > **How to apply**: when checking a translated normative surface, check it against the **authoritative
  > source** (the schema, the CLI, the code), never against its counterpart locale.

- [ ] 🟡 **Reusing a skill does not inherit its permission assumptions** → **Promote to schema**
      (a line in the bridge README's integration section)
  > **Why**: SDD's normal flow depends on implementer task-level commits; this repo forbids agent commits
  > outright (Anchor Register #4). The schema names SDD as its executor and says nothing about the gap.
  > **How to apply**: a skill defines *procedure*; the repo and harness define *execution permission* —
  > check the second before adopting the first. This is also the fact base for the separate governance
  > question of whether an isolated worktree should permit worker-local commits.

- [ ] 📌 **A per-entry field cannot surface an edge invisible from that entry** → **Promote to one-off**
      (hold as a D3 trigger observation at N=1; do not act yet)
  > **Why**: the Plan Contract's Interfaces field is worded consumer-first, so an entry written before its
  > consumers exist has nothing to consume — and per-entry review does not force building the coupling graph.
  > **How to apply**: if the omission recurs, the fix is a graph-level check or a differently-scoped field,
  > not a stricter reviewer.

- [ ] 🟡 **State a discard before you see the replacement** → **Promote to memory** (type: feedback)
  > **Why**: run 1 of the Q4-A sample was discarded for instrument defects; said afterwards, "discarded for
  > defects rather than for its result" would have been unfalsifiable.
  > **How to apply**: whenever a measurement is re-run, record what the first run produced and why it is
  > being discarded **before** the second run exists.

- [ ] 🔴 **A check that passed truthfully does not stay true when its subject changes** → **Promote to schema**
  > **Why**: checks 8–12 ran and passed at 25 tasks; the group-11 reopen took `tasks.md` to 27 without
  > adding plan entries, and for one commit this change violated its own check 12. Every gate had already
  > run; none re-ran. Found by an independent review of the execution record, not by any gate.
  > **How to apply**: a recorded check result needs a binding to what it was computed over — freshness, not
  > correctness, is the property that was missing. See `verify.md` carried-forward #6 for the open question
  > of whether this can be stated without a Harness-level mechanism the claim boundary disclaims.

---

## 7. Assurance decision — the Codex independent-review debt

A prior session left: *"Codex independent review 未補 … 只過 fallback 審 … schema 契約屬高風險——Codex
額度恢復後 SHALL 補獨立審，補審前不 archive。"* The owner ruled it dispositioned for this change.

**Classified from the original wording rather than from convenience.** The SHALL's object is 「補**獨立
審**」 — supply *independent review*; the stated deficiency is 「只過 **fallback** 審」; Codex appears as
the timing condition (「額度恢復後」), the vehicle designated at the time. `rules/auto-loop.md` § Review
Dispatch already treats reviewer identity as substitutable, with the gate being what must hold. So this
is an **equivalent-assurance substitution**, not a Codex-specific waiver: what the debt asked for was
independent review beyond one fallback pass, and this change received 11 independent reviews, a blind
mutation exercise, a blind plan sample with an independent scorer, a whole-branch review, and six fix
rounds that caught defects which would otherwise have shipped.

Recorded as directed: *Original Codex-specific review debt is explicitly dispositioned for this change
using the completed multi-layer independent review chain. This is an explicit assurance decision, not a
silent skip, and does not establish a general precedent for future changes.*

**Scope: `loosen-plan` only.** It retires no debt on any other change and amends no rule.

---

## Open items handed to the owner

The two items this section carried in its first draft — the three superseded v1 surfaces and the
fail-open PRECHECK — were **reopened as tasks 11.1 and 11.2, fixed, reviewed and closed**. They are not
deferrals and are recorded in `verify.md` §14.

What remains, all recorded rather than resolved:

1. **Task 9.1's live CI run** — needs a real Actions run after push; the only acceptance criterion in this
   change not closed by evidence in `verify.md`.
2. **The evidence carrier is installed but not exercised end-to-end** — every task here is honestly
   `TDD: n/a`, so three of the five deterministic checks are vacuous. The first downstream change with
   executable behaviour is the real dogfood.
3. **The v1 → v2 migration guide has never been walked** — stated and reviewed, not exercised.
4. **`tasks.md` task 4.2's false premise stays on the record** — it names a `templates/verify.md` §4 that
   never had TDD rows. The delivered §8 is right; the task text is left as the historical record of what
   was planned.
5. **Class-(a) detection is exact-phrase.** Extended from four phrases to nine by task 11.1, and each of
   the three real survivors was checked against its *pre-fix* text to confirm it would have been caught —
   but a differently-worded fourth instance would still slip. Narrowed, not closed; the hand-reviewed
   class-(b) sweep is the net it would most likely fall into.
6. **Nothing in the shipped schema owns check *freshness*, and this change proved it on itself.** The
   group-11 reopen changed `tasks.md` after checks 8–12 had run, and no gate re-ran the set comparison:
   for the span of one commit this change violated its own check 12 (27 task numbers, 25 plan entry
   keys). It was found by an independent review of the **execution record**, not by any gate — every gate
   had already run. Now re-run and evidenced in both directions (`verify.md` §8.1a: current tree PASS,
   pre-fix fixture BLOCK naming `{11.1, 11.2}`). **The residue handed over is the schema-level question**:
   `verify` says the checks must run before archive, but not that a later edit to `tasks.md` or `plan.md`
   invalidates a recorded result — and whether that can be stated without the Harness-level mechanism the
   claim boundary explicitly disclaims is the owner's call, not a verification fix.
