<!--
Task numbers are the plan.md entry keys (check 12: unique on both sides, then
equal sets). Order follows design.md §Migration Plan, with one deliberate
inversion: the mutation fixtures come FIRST, because a RED record for a
checker edit is "the fixture gets the wrong verdict under the pre-fix wording",
and that can only be captured before the wording changes.

TDD applicability, as read for this change: the checks are agent-executed
instruction prose with no unit-testable subject (same reading the archived
loosen-plan tasks.md took). What makes checker edits `applicable` here anyway
is that the mutation fixtures ARE their test: each fixture is one tasks.md +
plan.md pair with exactly one thing broken, and the check either names it or
does not. RED = the fixture's verdict under the current wording is wrong;
GREEN = the fixture's verdict under the new wording is right. The `subject:`
is `<fixture dir>::<expected verdict>`, which satisfies the `file::test`
grammar this change itself tightens. Doc-only tasks are `n/a`, with the
verification that replaces a test named in the reason.

Ruled 2026-09-07 (user): applicability does not turn on whether a
conventional test framework runs the case; it turns on whether the same
re-runnable case shows the old behaviour violating the contract before the
edit and the corrected verdict after it. The archived loosen-plan's `n/a`
for similar work is not revisited — the conditions differ (re-runnable
fixtures now exist). Three boundaries every RED/GREEN record under 2.1–2.3
must satisfy:

  1. RED is obtained by actually running the fixture against the PRE-edit
     wording. "The old version would have failed" written after the edit is
     not a RED.
  2. RED and GREEN bind the same behavioural subject — same fixture, same
     expected verdict — character for character.
  3. The `failure:` field states EXPECTED verdict vs ACTUAL verdict
     (e.g. "expected check 12 BLOCK naming 1.1; actual PASS, sets equal").
     For these fixtures BLOCK is usually the correct verdict, so a BLOCK is
     not automatically GREEN and a PASS is not automatically RED — the
     direction is per fixture and must be written out.

Name this evidence for what it is — fixture-based behavioural
verification, agent-executed — never as a unit-test-framework run.
-->

## 1. Mutation fixtures — one broken thing each, plus a positive control per new rule

- [ ] 1.1 Add `f8-duplicate-task-number` (tasks.md has two task lines numbered `1.1`, plan.md has one entry keyed `1.1`) and `f9-duplicate-plan-key` (plan.md has two `##` entries keyed `2.3`, tasks.md has one task `2.3`) under `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/`, each a self-contained tasks.md + plan.md pair with everything else conforming
  - TDD: n/a — the fixtures are the test material for 2.1, not code under test; their correctness is shown by 2.1's RED/GREEN records (wrong verdict before, right verdict after)
- [ ] 1.2 Add `f10-subject-without-separator` (a RED `subject:` is `rejects empty email`, no `::`), `f11-duplicate-subject-one-side` (one task carries two RED records with identical `subject:` values and one GREEN), and `f12-two-subjects-paired` (one applicable task carries two distinct subjects, each with exactly one RED and one GREEN — a **positive control** that must NOT block) in the same fixtures directory
  - TDD: n/a — test material for 2.2, same terms as 1.1; f12 is the positive control the design's "good input must not be rejected" risk requires
- [ ] 1.3 Add `f13-deferred-task-in-tasks` (tasks.md carries one task marked `[~]` deferred; plan.md holds only contract entries and no task rows, as every v2 plan does) in the same fixtures directory
  - TDD: n/a — test material for 2.3; the fixture's whole point is that under the current check 7 wording it is invisible
- [ ] 1.4 Extend the fixtures README: add f8–f13 rows to the "破壞的東西 / 應得判定" table (f12 flagged as positive control alongside f7), note that f8–f13 target the post-`fix-v2-blocking-defects` wording and that the earlier blind run did not cover them, and refresh the "怎麼重跑" note so a re-runner shuffles all thirteen
  - TDD: n/a — prose/doc-only; verified by reading the table against the fixture directory listing (every directory has a row, every row has a directory)

## 2. schema.yaml — the five checks, plus the tasks-instruction segment they must agree with

- [x] 2.1 Rewrite check 12 as two stages per D1: stage one detects duplicate keys on each side independently (tasks.md task numbers; plan.md entry keys) and BLOCKs naming each repeated key; stage two is the existing bidirectional set comparison, unchanged. The two failures get distinct messages ("`1.1` occurs twice in tasks.md" vs "`1.1` has no plan entry"). Keep the existing non-numeric-token and absent-plan.md branches; duplicate detection goes after them and before the set comparison (design Open Question 1). Retitle the check so its name matches what it now asserts
  - TDD: applicable
  - RED:
    - subject: f8-duplicate-task-number::check 12 BLOCKs naming `1.1` as repeated in tasks.md
    - outcome: FAIL
    - failure: expected check 12 to BLOCK naming `1.1` as repeated in tasks.md; actual PASS — the pre-edit check compares only sets, so the two task lines numbered `1.1` collapse to {1.1}, plan.md's entry keys are {1.1}, both directions are empty, no task line lacks a number and plan.md exists with a collectable key, so no BLOCK condition in the pre-edit enumeration fires
    - invocation: fixture-based behavioural verification, agent-executed — walked the pre-edit check-12 text (`git show 22c15cf:superpowers-bridge/schema.yaml`, lines 523-556 — 22c15cf is the commit that landed the fixtures and the base of this task's diff) by hand against docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f8-duplicate-task-number/{tasks.md,plan.md}
  - GREEN:
    - subject: f8-duplicate-task-number::check 12 BLOCKs naming `1.1` as repeated in tasks.md
    - outcome: PASS
    - invocation: same walk against the post-edit check-12 text — stage one keeps the task numbers as a list [1.1, 1.1], finds `1.1` carried by two task lines and reports "`1.1` occurs twice in tasks.md", which BLOCKs; the text specifies that stage one does not short-circuit, so stage two is still evaluated and on this fixture adds nothing ({1.1} equals {1.1})
  - RED:
    - subject: f9-duplicate-plan-key::check 12 BLOCKs naming `2.3` as repeated in plan.md
    - outcome: FAIL
    - failure: expected check 12 to BLOCK naming `2.3` as repeated in plan.md; actual PASS — the pre-edit check collects the two `## 2.3` headings into the set {2.3}, tasks.md's task numbers are {2.3}, both directions are empty and every other pre-edit BLOCK condition is negative
    - invocation: fixture-based behavioural verification, agent-executed — same pre-edit text (`git show 22c15cf:superpowers-bridge/schema.yaml`, lines 523-556) walked against fixtures/f9-duplicate-plan-key/{tasks.md,plan.md}
  - GREEN:
    - subject: f9-duplicate-plan-key::check 12 BLOCKs naming `2.3` as repeated in plan.md
    - outcome: PASS
    - invocation: same walk against the post-edit check-12 text — stage one examines the plan side independently, finds the entry key `2.3` leading two `##` headings and reports "`2.3` occurs twice in plan.md", which BLOCKs; the differing titles do not exempt them, and stage two is still evaluated per the no-short-circuit rule and adds nothing ({2.3} equals {2.3})
- [x] 2.2 Rewrite checks 9–11 per D2/D3: pairing unit is the `subject:` value, not the task; a `subject:` must match `<test-file>::<test-name>` — after trimming, exactly one `::` with non-empty sides, nothing further constrained; subject values unique within a task on each side; each subject has exactly one RED and exactly one GREEN; extra runs are not recorded as further records. Fold the grammar into check 9's "required fields" (a field whose value fails the grammar is not a satisfied field), rewrite check 11 as per-subject pairing, and retitle check 9 so its name covers the grammar it now asserts. Add the boundary sentence: these checks decide structure, format and cardinality only, never evidence truth
  - TDD: applicable
  - RED:
    - subject: f10-subject-without-separator::check 9 BLOCKs naming the malformed `subject:` value
    - outcome: FAIL
    - failure: expected check 9 to BLOCK naming the `subject:` value `rejects empty email` as malformed; actual PASS — the pre-edit checks 9–11 contain no sentence about `::`, a separator or any value format. Pre-edit check 9 constrains a field value only by "a required field whose value is empty after trimming → BLOCK", and `rejects empty email` is not empty; pre-edit check 11 asks only that the two values be "identical character for character", which they are, so a malformed subject passes as long as both sides carry the same malformed string
    - invocation: fixture-based behavioural verification, agent-executed — walked the pre-edit checks 9–11 text (`git show 22c15cf:superpowers-bridge/schema.yaml`, lines 483-521 — 22c15cf is the commit that landed the fixtures, and task 2.1 did not touch checks 9–11, so it is the text under test) by hand against docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f10-subject-without-separator/{tasks.md,plan.md}
  - GREEN:
    - subject: f10-subject-without-separator::check 9 BLOCKs naming the malformed `subject:` value
    - outcome: PASS
    - invocation: same walk against the post-edit checks 9–11 text — check 9's SUBJECT GRAMMAR scans the trimmed value `rejects empty email` for `::`, finds zero occurrences where exactly one is required, so the `subject:` is not a satisfied field and check 9 BLOCKs naming the value and the record it belongs to (both the RED's and the GREEN's, since every record is examined). Check 11 adds nothing here: one RED subject, one GREEN subject, no repeat on either side and the two sets are equal
  - RED:
    - subject: f11-duplicate-subject-one-side::check 11 BLOCKs naming the duplicated subject on the RED side
    - outcome: FAIL
    - failure: expected check 11 to BLOCK naming `test/auth.test.js::rejects empty email` as occurring twice among the task's RED records; actual PASS — no sentence in the pre-edit checks 9–11 mentions uniqueness or per-subject cardinality at all. Pre-edit check 9 is satisfied (a RED line and a GREEN line are present, every required field is present and non-empty), check 10 is satisfied (both REDs `FAIL`, GREEN `PASS`), and pre-edit check 11 compares "the RED record's `subject:` value" with the GREEN's — whichever of the two REDs that singular designates, the values are identical, so no difference is found. That reading of pre-edit check 9's "must include one `- RED:` line and one `- GREEN:` line" is the "at least one" one, and the sentence is genuinely ambiguous — but this RED holds under either reading: under "at least one" the pre-edit text yields PASS as recorded, and under "exactly one" it instead BLOCKs at check 9 on raw record count, which never names the duplicated subject. Either way the defect f11 exists to expose goes unreported
    - invocation: fixture-based behavioural verification, agent-executed — same pre-edit text (`git show 22c15cf:superpowers-bridge/schema.yaml`, lines 483-521) walked against fixtures/f11-duplicate-subject-one-side/{tasks.md,plan.md}
  - GREEN:
    - subject: f11-duplicate-subject-one-side::check 11 BLOCKs naming the duplicated subject on the RED side
    - outcome: PASS
    - invocation: same walk against the post-edit checks 9–11 text — check 11 collects the RED subjects as the LIST [`test/auth.test.js::rejects empty email`, `test/auth.test.js::rejects empty email`] and the GREEN subjects as a second list; stage one finds the value twice on the RED side and BLOCKs reporting it by name and by side. Stage two is still evaluated (the text states stage one does not short-circuit) and adds nothing, since the two sets are equal. Check 9 does not fire: both subjects conform to the grammar
  - RED:
    - subject: f12-two-subjects-paired::checks 9-11 report no finding (positive control)
    - outcome: INDETERMINATE
    - failure: expected checks 9–11 to report no finding on this positive control; actual INDETERMINATE — the pre-edit text cannot decide the case either way. Check 11's whole pre-edit body reads "within one task, the RED record's `subject:` value and the GREEN record's `subject:` value must be identical character for character after leading and trailing whitespace is trimmed. Any difference → BLOCK." The definite singular "the RED record" and "the GREEN record" designates nothing in a task holding two RED records and two GREEN records: pairing the first RED with the first GREEN yields no difference, pairing the first RED with the second GREEN yields a difference and therefore BLOCK, and the sentence supplies no rule for choosing. Two executors reading it can reach opposite verdicts, so the pre-edit verdict is neither PASS nor BLOCK
    - invocation: fixture-based behavioural verification, agent-executed — same pre-edit text (`git show 22c15cf:superpowers-bridge/schema.yaml`, lines 483-521) walked against fixtures/f12-two-subjects-paired/{tasks.md,plan.md}
  - GREEN:
    - subject: f12-two-subjects-paired::checks 9-11 report no finding (positive control)
    - outcome: PASS
    - invocation: same walk against the post-edit checks 9–11 text — check 9 requires AT LEAST ONE RED line and AT LEAST ONE GREEN line and states that record count is check 11's question, so the two pairs satisfy it; every required field is present and both subjects conform to the grammar. Check 10 passes on all four records. Check 11 collects RED [`test/auth.test.js::rejects empty email`, `test/auth.test.js::rejects empty password`] and the same two values on the GREEN side: stage one finds no repeat on either side, stage two finds the two sets equal in both directions. No finding from any of the three — the ambiguity is settled in terms of subjects rather than raw record counts, which is what keeps this control positive
- [x] 2.3 Change check 7's carrier from `plan.md` to `tasks.md` per D4 — every reference, not one: the opening condition, the "plan + test files" aside, the blocking condition ("§7 is empty AND plan.md has `[~]` rows"), and the FRESHNESS map, whose affected sets are derived from inputs and therefore move with it (check 7 now reads `tasks.md`; an edit to `tasks.md` reaches checks 2, 7, 8–12; an edit to `plan.md` reaches check 12 only). The enumeration, equivalence-test identification and retrospective-Misses routing stay character for character. Then grep `schema.yaml` for `plan.md` within check 7 and the freshness block to confirm no carrier reference survives
  - TDD: applicable
  - RED:
    - subject: f13-deferred-task-in-tasks::check 7 finds one deferred task and requires §7 enumeration
    - outcome: FAIL
    - failure: expected check 7 to find ONE deferred task (`- [~] 1 Verify checkout flow against staging`), enumerate it in verify.md §7 and proceed to the equivalent-automated-test step; actual "no deferred tasks", §7 may be blank, equivalence step never reached — the pre-edit opening condition reads "If plan.md has any tasks marked `[~]` deferred", and f13's plan.md is a conforming v2 plan (a header plus `## 1 — checkout flow staging smoke test`) carrying no `[~]` and, by the Plan Contract, no task rows at all, so the condition is false. The pre-edit blocking condition "§7 is empty AND plan.md has `[~]` rows" is false on its second conjunct too, so the skipped gap analysis is not even reported
    - invocation: fixture-based behavioural verification, agent-executed — walked the pre-edit check 7 text (`git show 22c15cf:superpowers-bridge/schema.yaml`, the block from `7. **Deferred dogfood` to `CHECKS 8-12`; 22c15cf is the commit that landed the fixtures, and tasks 2.1 and 2.2 left check 7 byte-identical to it, verified by diffing that block against the working tree before editing) by hand against docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f13-deferred-task-in-tasks/{tasks.md,plan.md}. The walk was written to .superpowers/sdd/plan/task-2.3-red-walk.md before the edit
  - GREEN:
    - subject: f13-deferred-task-in-tasks::check 7 finds one deferred task and requires §7 enumeration
    - outcome: PASS
    - invocation: same walk against the post-edit check 7 text — the DEFERRED TASK definition scans tasks.md for lines whose first non-space characters are `- [~]` and finds exactly one, `- [~] 1 Verify checkout flow against staging`; the opening condition now reads tasks.md, so it holds, and the check enumerates that one task in verify.md §7 and proceeds to identify the equivalent automated test. plan.md is not among this check's inputs and is not consulted.
  - Acceptance control, not a TDD record (f7 has no RED to give — it already reads correctly under the pre-edit wording): walked f7-blank-spaced-record against the post-edit check 7 text. Its tasks.md carries `- [x]` markers only, so no line matches `- [~]`; the opening condition is false, the verdict is "no deferred tasks" with §7 permitted to be blank, and the blocking condition's second conjunct stays false. Unchanged behaviour, which is what the control requires
- [x] 2.4 Bring the `tasks` artifact instruction (the EVIDENCE FOR APPLICABLE TASKS segment and the normative SHAPE block) into agreement with 2.2: a task may carry several subjects; records pair by subject; each subject has one RED and one GREEN; GREEN's subject is identical to the RED it pairs with (not "to RED's", which presumes one); state the `::` grammar where the `test-file::test-name` form is introduced. Then grep `schema.yaml` for residual single-pair wording ("a RED record and a GREEN record", "identical to RED's", "the RED record's `subject:`") and clear every hit that is not the shape example
  - TDD: n/a — instruction prose; the control is the residual-wording grep returning zero hits outside the SHAPE block, recorded in verify

## 3. Templates and bridge READMEs — coupled surfaces (D6, CLAUDE.md cross-file table)

- [ ] 3.1 Update `superpowers-bridge/templates/tasks.md` (the normative shape comment: multi-subject allowed, per-subject pairing, grammar) and `superpowers-bridge/templates/verify.md` (the §7 deferred-equivalence section and its "when may this section be blank" note now keyed to `tasks.md`; the deterministic-checks section for checks 9–12 as renamed and re-scoped in group 2; the freshness footnote's affected sets updated to match 2.3)
  - TDD: n/a — template prose; verified by diffing each template's check list against schema.yaml's (same check numbers, same titles)
- [ ] 3.2 Update the checks 8–12 explanation in `superpowers-bridge/README.md` and `README.zh-TW.md` together: check 12 two-stage 1:1; per-subject evidence with grammar, uniqueness and cardinality; check 7 reads tasks.md (the "Check 7 blocks only when `plan.md` has `[~]`" sentence in both READMEs, and the freshness design-touchpoint if it names check 7's input); the RED outcome sentence tightened from "anything else" to "a single uppercase token other than PASS" so it matches check 10; the checker-truth boundary. Same commit, both languages
  - TDD: n/a — prose/doc-only; verified by reading both READMEs' check descriptions against the schema text, and by confirming the Compatibility table row shape is untouched (version-check.yml's grep depends on it)

## 4. Canonical spec and repo guidance — the two documentation P1s

- [ ] 4.1 Fix the two stale clauses in `openspec/specs/tdd-claim-accuracy/spec.md` that still name `plan.md` task content / `writing-plans`' task format as the TDD carrier (`:20-22` spanning lines, and `:59-61`), so the spec names one carrier — the tasks.md annotation plus RED/GREEN evidence — everywhere. Do not touch the delta spec under this change; it is what `openspec archive` will merge
  - TDD: n/a — prose/doc-only; the control is a grep for both stale phrasings **including the markdown backticks around `writing-plans`** (the 2026-09-07 handoff records that the bare-word grep silently returned 0 for one of the two hits) returning zero, plus a read of the whole file for a third occurrence
- [ ] 4.2 Update `CLAUDE.md`: the cross-file coupling row for the Compatibility table now says version-check.yml greps the `v2` row; the "two version numbers" section and the schema-major sentences say `version: 2` / `2.0.0` where they still say 1; the loosen-plan pointer points at `openspec/changes/archive/2026-09-04-loosen-plan/` instead of the active path. Nothing else in the file
  - TDD: n/a — prose/doc-only; verified by reading `version-check.yml`'s grep line side by side with the updated row, and by `ls` on the archived path

## 5. Close-out — make the fixed checker the one that judges this change

- [ ] 5.1 Re-sync the dogfood copy (`rm -rf openspec/schemas/superpowers-bridge && cp -R superpowers-bridge openspec/schemas/`), then `openspec schema validate superpowers-bridge` and `openspec schemas` must both succeed; confirm `openspec instructions verify --change fix-v2-blocking-defects` renders the new check text
  - TDD: n/a — configuration / copy step; the control is the rendered instruction containing the retitled checks (a stale copy renders the old titles)
- [ ] 5.2 Append one pointer to `openspec/changes/archive/2026-09-04-loosen-plan/errata.md` (append-only): post-archive independent review found five blocking correctness defects; fixes carried by `fix-v2-blocking-defects`. No edit to any other archived artifact
  - TDD: n/a — append-only record entry; verified by `git diff` showing additions only in that file
- [ ] 5.3 Re-verify D5's precondition immediately before this change's verify artifact is written: `git tag -l` is empty and `origin/main` still lacks the v2 commits. If either has changed, stop and re-open D5 rather than proceeding on the stale premise
  - TDD: n/a — a precondition check on repository state, not behaviour; the recorded command output is the evidence
