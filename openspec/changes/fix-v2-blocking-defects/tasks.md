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

- [ ] 2.1 Rewrite check 12 as two stages per D1: stage one detects duplicate keys on each side independently (tasks.md task numbers; plan.md entry keys) and BLOCKs naming each repeated key; stage two is the existing bidirectional set comparison, unchanged. The two failures get distinct messages ("`1.1` occurs twice in tasks.md" vs "`1.1` has no plan entry"). Keep the existing non-numeric-token and absent-plan.md branches; duplicate detection goes after them and before the set comparison (design Open Question 1). Retitle the check so its name matches what it now asserts
  - TDD: applicable
- [ ] 2.2 Rewrite checks 9–11 per D2/D3: pairing unit is the `subject:` value, not the task; a `subject:` must match `<test-file>::<test-name>` — after trimming, exactly one `::` with non-empty sides, nothing further constrained; subject values unique within a task on each side; each subject has exactly one RED and exactly one GREEN; extra runs are not recorded as further records. Fold the grammar into check 9's "required fields" (a field whose value fails the grammar is not a satisfied field), rewrite check 11 as per-subject pairing, and retitle check 9 so its name covers the grammar it now asserts. Add the boundary sentence: these checks decide structure, format and cardinality only, never evidence truth
  - TDD: applicable
- [ ] 2.3 Change check 7's carrier from `plan.md` to `tasks.md` per D4 — every reference, not one: the opening condition, the "plan + test files" aside, the blocking condition ("§7 is empty AND plan.md has `[~]` rows"), and the FRESHNESS map, whose affected sets are derived from inputs and therefore move with it (check 7 now reads `tasks.md`; an edit to `tasks.md` reaches checks 2, 7, 8–12; an edit to `plan.md` reaches check 12 only). The enumeration, equivalence-test identification and retrospective-Misses routing stay character for character. Then grep `schema.yaml` for `plan.md` within check 7 and the freshness block to confirm no carrier reference survives
  - TDD: applicable
- [ ] 2.4 Bring the `tasks` artifact instruction (the EVIDENCE FOR APPLICABLE TASKS segment and the normative SHAPE block) into agreement with 2.2: a task may carry several subjects; records pair by subject; each subject has one RED and one GREEN; GREEN's subject is identical to the RED it pairs with (not "to RED's", which presumes one); state the `::` grammar where the `test-file::test-name` form is introduced. Then grep `schema.yaml` for residual single-pair wording ("a RED record and a GREEN record", "identical to RED's", "the RED record's `subject:`") and clear every hit that is not the shape example
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
