# fix-v2-blocking-defects — Plan Contract

> **For agentic workers:** Use superpowers:subagent-driven-development
> to implement this plan task-by-task. Each entry states what "done"
> means for one task, not how to get there — two executors may satisfy
> the same entry by different paths and both conform.

**Goal:** Close the five P1 correctness defects the 2026-09-07 post-archive independent review found in schema v2's deterministic checks and their coupled documents, so that the verify checks assert exactly what their names claim (check 12 truly 1:1; checks 9–11 deterministic per subject; check 7 reading the carrier that exists) and the canonical spec and repo guidance give one answer where they gave two.

**Pointers:** [`specs/plan-contract/spec.md`](./specs/plan-contract/spec.md), [`specs/tdd-evidence-contract/spec.md`](./specs/tdd-evidence-contract/spec.md), [`specs/tdd-claim-accuracy/spec.md`](./specs/tdd-claim-accuracy/spec.md); [`design.md`](./design.md) for decisions D1–D6, the non-goals, the risk mitigations and the landing order. [`brainstorm.md`](./brainstorm.md) §已查證依據 holds the line-level verification of each defect.

**Global constraints (verbatim from the specs; every entry below is bound by them):**

- "The correspondence between tasks.md task numbers and plan.md entry keys SHALL be one-to-one, and the deterministic verify check SHALL establish it in two stages: first that neither side contains a duplicate key, then that the two key sets are equal in both directions."
- "A duplicate on either side SHALL be reported as a blocking finding naming the repeated key, distinctly from a missing or extra key, because the two are different defects with different repairs."
- "plan.md SHALL NOT carry task-level state markers (deferral and the like); tasks.md is their carrier. Any deterministic check concerning task state SHALL therefore read tasks.md, and a check that searches plan.md for task rows is non-conforming"
- "Records SHALL pair by their `subject:` value, and each subject appearing under a task SHALL have exactly one RED record and exactly one GREEN record. Subject values SHALL be unique within each side of a task — at most one RED record and at most one GREEN record per subject"
- "Ordinal pairing (the n-th RED with the n-th GREEN) SHALL NOT be used, because inserting one record silently re-pairs every record after it."
- "A `subject:` value SHALL, after trimming, match `<test-file>::<test-name>`: exactly one `::` separator, with a non-empty remainder on each side after trimming. The check SHALL NOT constrain path syntax, file extension, or test-name characters beyond that"
- "The deterministic checks SHALL verify structure, format and cardinality only, and bridge-owned surfaces SHALL NOT claim they verify evidence truth."
- "A surface MUST NOT cite `writing-plans`' micro-step task format as the description of where TDD comes from: under the evidence contract the carrier is the tasks.md annotation plus its RED/GREEN evidence"
- "Surfaces SHALL NOT describe plan.md task content as the carrier of that requirement — under the Plan Contract plan.md holds contract entries and no task list."

Binding non-goals carried from design.md (not spec text, but every entry is bounded by them): no P2 is pulled in; no archived loosen-plan artifact is rewritten; no deferred-task-to-plan-entry rule is added; schema major stays `2` and the bundle stays `2.0.0` while D5's precondition holds.

---

## 1.1 — Fixtures for duplicate keys on either side (f8, f9)

- **Delivers:** Two new self-contained fixture directories in the mutation-fixture set, each breaking exactly one thing: f8 has a repeated task number in tasks.md against a single matching plan entry; f9 has a repeated entry key in plan.md against a single matching task. Everything else in each pair conforms to the current v2 contract, so no check other than the two-stage check 12 has grounds to block.
- **Acceptance:** Each directory contains a tasks.md and a plan.md and nothing that a v2 check other than check 12 would flag (every task annotated, every applicable task fully evidenced, every outcome marker well-formed). In f8 exactly one task number appears exactly twice and the two key sets are otherwise equal; in f9 exactly one `##` entry key appears exactly twice and the sets are otherwise equal. Under the pre-edit check 12 wording, both fixtures reach a PASS verdict (sets equal) — that is the property 2.1 needs them to have.
- **Blocked by:** none
- **Interfaces:** Produces fixture directories `f8-duplicate-task-number/` and `f9-duplicate-plan-key/` consumed by 2.1 (as RED/GREEN subjects) and by 1.4 (as README rows).

## 1.2 — Fixtures for subject grammar, duplicate subject, and the multi-subject positive control (f10, f11, f12)

- **Delivers:** Three fixture directories: f10 carries a RED whose `subject:` has no `::`; f11 carries two RED records with identical subjects and one GREEN under the same task; f12 carries one applicable task with two distinct, fully paired subjects and is a positive control that must not block under the new wording.
- **Acceptance:** f10's only non-conformance is the malformed subject (the GREEN carries the same malformed value so check 11 in its current form has nothing to say). f11's only non-conformance is the duplicated RED subject. f12 has zero non-conformances under the new contract, and under the pre-edit check 11 wording ("the RED record's subject … the GREEN record's subject", singular) its verdict is indeterminate or wrong — a reader following the old text cannot decide which RED pairs with which GREEN. Each directory is a self-contained tasks.md + plan.md pair with all other checks satisfied.
- **Blocked by:** none
- **Interfaces:** Produces `f10-subject-without-separator/`, `f11-duplicate-subject-one-side/`, `f12-two-subjects-paired/` consumed by 2.2 and 1.4.

## 1.3 — Fixture with a deferred task where v2 actually keeps it (f13)

- **Delivers:** One fixture directory whose tasks.md contains a task marked `[~]` and whose plan.md is a conforming v2 Plan Contract with no task rows at all.
- **Acceptance:** tasks.md has exactly one `[~]` task, annotated and (if applicable) evidenced like the rest; plan.md has a header plus one `##` entry per task and no checkbox lines. Under the pre-edit check 7 wording ("If plan.md has any tasks marked `[~]`") the check reports no deferred tasks — the fixture demonstrates the check cannot fire on any v2 plan.
- **Blocked by:** none
- **Interfaces:** Produces `f13-deferred-task-in-tasks/` consumed by 2.3 and 1.4.

## 1.4 — Fixtures README covers f8–f13

- **Delivers:** The fixtures README describes the six new fixtures on the same terms as f1–f7, marks f12 as a positive control alongside f7, records that f8–f13 target the post-`fix-v2-blocking-defects` wording and were not part of the 2026-09-03 blind run, and tells a re-runner to shuffle all thirteen.
- **Acceptance:** The "破壞的東西 / 應得判定" table has one row per directory under `fixtures/` and no row without a directory (both directions, checked by listing). Each new row states the expected verdict, and f12's row says "不 BLOCK". The blind-run section states plainly that f8–f13 have no blind verdict yet. No existing row's content is altered.
- **Blocked by:** 1.1, 1.2, 1.3
- **Interfaces:** Consumes the six fixture directory names and their expected verdicts from 1.1, 1.2 and 1.3 (each of those entries names this task as a consumer). Produces nothing another task in this change consumes; the README rows serve future re-runners.

## 2.1 — check 12 asserts the 1:1 its name claims (D1)

- **Delivers:** check 12 in `schema.yaml` detects a duplicate key on either side before comparing sets, reports each repeated key by name with a message distinct from the missing/extra-key message, and then performs the unchanged bidirectional set comparison. The check's title matches what it now asserts.
- **Acceptance:** Reading the new check text against f8 yields BLOCK naming `1.1` as repeated in tasks.md; against f9 yields BLOCK naming `2.3` as repeated in plan.md; against f7 (unique keys, equal sets) yields no finding from this check; against f5 the existing set-difference message is unchanged. The pre-existing branches (non-numeric first token, absent plan.md, no collectable entry key) are still present in the same order, and duplicate detection sits after them and before the set comparison. The word "1:1" no longer appears anywhere in the check that the check's own logic does not deliver. tasks.md 2.1 carries RED/GREEN records for at least the f8 and f9 subjects, each RED obtained against the pre-edit wording and each `failure:` stating expected vs actual verdict.
- **Blocked by:** 1.1
- **Interfaces:** Consumes fixtures from 1.1. Produces the check-12 wording that 3.1 (templates/verify.md) and 3.2 (READMEs) must mirror.

## 2.2 — checks 9–11 decide evidence per subject with a grammar (D2, D3)

- **Delivers:** checks 9, 10 and 11 in `schema.yaml` read RED/GREEN records grouped by `subject:` value within a task. A subject must match the `::` grammar (exactly one separator, non-empty trimmed sides, nothing else constrained); subject values are unique per side within a task; each subject has exactly one RED and one GREEN; check 11 pairs by subject rather than assuming one pair per task. The text states that these checks decide structure, format and cardinality only and never evidence truth. Check 9's title covers the grammar it now asserts.
- **Acceptance:** Reading the new text against f10 yields BLOCK naming the malformed subject; against f11 yields BLOCK naming the duplicated subject; against f12 yields no finding from checks 9–11; against f2, f3, f4 the verdicts recorded in the fixtures README are unchanged (missing GREEN, PASS-on-RED, unpaired subject still block). The identifier `tests/api_test.go::TestRejectsEmptyEmail/subcase-2` is accepted by the grammar as written (the spec's conforming-identifier scenario). No sentence in checks 9–11 presumes a single RED or a single GREEN per task. tasks.md 2.2 carries RED/GREEN records for at least f10, f11 and f12, with f12's records showing the expected verdict "no BLOCK" and the RED being the pre-edit indeterminacy.
- **Blocked by:** 1.2
- **Interfaces:** Consumes fixtures from 1.2. Produces the checks 9–11 wording mirrored by 2.4 (tasks instruction), 3.1 and 3.2.

## 2.3 — check 7 reads tasks.md (D4)

- **Delivers:** check 7's carrier is tasks.md in every place `schema.yaml` names it — the opening condition, the "plan + test files" aside, the blocking condition, and the FRESHNESS map's input-derived affected sets. The enumeration into verify §7, the equivalent-automated-test identification and the retrospective-Misses routing are unchanged.
- **Acceptance:** Reading the new text against f13 yields "one deferred task found" and proceeds to the equivalence step; the pre-edit text against the same fixture yields "no deferred tasks". Against f7 (no `[~]` anywhere) the new text yields "no deferred tasks" and §7 may be blank — the no-deferral control. Within check 7's body and the freshness block, `grep -n 'plan.md'` returns only the freshness sentences that describe check 12's inputs (which legitimately read both files); no sentence says check 7 reads plan.md, and the freshness map states that an edit to tasks.md reaches checks 2, 7, 8–12 and an edit to plan.md reaches check 12. Outside those carrier references, a diff of check 7 shows no clause altered. No new rule about linking deferred tasks to plan entries appears (design D4 non-goal). tasks.md 2.3 carries a RED/GREEN pair for the f13 subject only — f7 already reads correctly under the pre-edit wording, so it has no RED to give and serves as an acceptance control, not evidence.
- **Blocked by:** 1.3
- **Interfaces:** Consumes the fixture from 1.3 and the existing f7. Produces the check-7 carrier wording and the freshness affected-set wording mirrored by 3.1 (templates/verify.md §7 and freshness footnote) and 3.2 (READMEs' check-7 sentence).

## 2.4 — The tasks instruction agrees with the checks it feeds

- **Delivers:** The `tasks` artifact instruction's evidence segment and normative SHAPE block in `schema.yaml` describe multi-subject evidence, per-subject pairing, one RED and one GREEN per subject, and the `::` grammar at the point where `test-file::test-name` is introduced — so an agent writing tasks.md from the instruction produces exactly what checks 9–11 accept.
- **Acceptance:** A grep of `schema.yaml` for the three residual single-pair phrasings named in tasks.md 2.4 returns zero hits outside the SHAPE example, and the SHAPE example itself is either unchanged (a single-subject task is still conforming) or extended to show two subjects — either way it conforms to the new checks. The instruction states the grammar in the same terms as check 9 (one `::`, non-empty sides, nothing further). `openspec schema validate superpowers-bridge` passes.
- **Blocked by:** 2.2
- **Interfaces:** Consumes the checks 9–11 wording from 2.2; both must state the same grammar and cardinality.

## 3.1 — Templates mirror the schema

- **Delivers:** `templates/tasks.md`'s shape comment and `templates/verify.md`'s deterministic-checks section say what `schema.yaml` now says for checks 7, 9–12.
- **Acceptance:** Every check number and title in `templates/verify.md` matches the schema's check list one for one (no renamed check keeps its old title in the template). The tasks template's comment does not presume one subject per task and mentions the `::` grammar. Both templates render through `openspec instructions <artifact> --change fix-v2-blocking-defects` without error.
- **Blocked by:** 2.1, 2.2, 2.3, 2.4
- **Interfaces:** Consumes the check wording from 2.1–2.3 and the instruction wording from 2.4. Produces the two template files that 5.1 copies into the dogfood tree.

## 3.2 — Both bridge READMEs describe the corrected checks (D6)

- **Delivers:** `superpowers-bridge/README.md` and `README.zh-TW.md` describe check 12 as two-stage 1:1, checks 9–11 as per-subject with grammar, uniqueness and cardinality, check 7 as reading tasks.md, the RED outcome as a single uppercase token other than PASS, and the checker-truth boundary — in both languages, in the same commit.
- **Acceptance:** Each statement about checks 7–12 in either README can be matched to a sentence in `schema.yaml` saying the same thing; the phrase "anything else" no longer describes the RED outcome in either language. The Compatibility table's `v2` row is byte-identical before and after (first cell `v2`, OpenSpec and Superpowers versions each in a single backtick span, then the date cell), so `version-check.yml`'s `grep -E '^\| v2 \| \`'` still matches and its `awk -F'\`'` still reads fields 2 and 4. The two language versions cover the same set of points (a bilingual reader finds no claim in one that is absent from the other).
- **Blocked by:** 2.1, 2.2, 2.3
- **Interfaces:** Consumes the check wording from 2.1–2.3. Produces the two README files that 5.1 copies into the dogfood tree (they live under `superpowers-bridge/`, so a copy taken before this task lands carries the stale check descriptions).

## 4.1 — The canonical tdd-claim-accuracy spec names one carrier

- **Delivers:** `openspec/specs/tdd-claim-accuracy/spec.md` states everywhere that a TDD requirement reaches an executor through the tasks.md annotation and RED/GREEN evidence, and nowhere that it travels through plan.md task content or `writing-plans`' micro-step format.
- **Acceptance:** A grep for the two stale phrasings — written with the markdown backticks around `writing-plans` exactly as the file has them — returns zero hits; a full read of the file finds no third statement of a plan.md carrier. The file still validates (`openspec validate --all`). The delta spec under this change is untouched, since `openspec archive` is what merges it.
- **Blocked by:** none

## 4.2 — CLAUDE.md coupling table and version narrative match the repo

- **Delivers:** The cross-file coupling row for the Compatibility table names the `v2` row that `version-check.yml` actually greps; the "兩個版本號" section and any schema-major sentence read `2` / `2.0.0`; the loosen-plan pointer resolves to the archived path.
- **Acceptance:** The grep pattern quoted in the coupling row is the one found on `version-check.yml`'s corresponding line. Every path named in the edited sentences exists (checked by listing). A diff of `CLAUDE.md` shows changes only in those sentences — no red-flag list edit, no governance-language rewrite (that is a separate registered task).
- **Blocked by:** none

## 5.1 — The dogfood copy is the fixed checker

- **Delivers:** `openspec/schemas/superpowers-bridge/` is a fresh copy of `superpowers-bridge/`, and the CLI validates and lists it.
- **Acceptance:** `diff -r superpowers-bridge openspec/schemas/superpowers-bridge` is empty; `openspec schema validate superpowers-bridge` and `openspec schemas` both succeed; `openspec instructions verify --change fix-v2-blocking-defects` renders the retitled checks from 2.1 and 2.2 (a stale copy renders the old titles, which is how this step's omission shows).
- **Blocked by:** 2.1, 2.2, 2.3, 2.4, 3.1, 3.2
- **Interfaces:** Consumes the final `superpowers-bridge/` tree — schema from 2.1–2.4, templates from 3.1, READMEs from 3.2 — and produces the checker that this change's own verify artifact runs under.

## 5.2 — Archived record gets its pointer, nothing more

- **Delivers:** One appended entry in the archived loosen-plan `errata.md` saying that a post-archive independent review found five blocking correctness defects and that `fix-v2-blocking-defects` carries the fixes.
- **Acceptance:** `git diff` for the archived change directory shows additions only, confined to `errata.md`; no other file under `openspec/changes/archive/2026-09-04-loosen-plan/` changes. The entry names this change and is dated.
- **Blocked by:** none

## 5.3 — D5's precondition re-verified before verify is written

- **Delivers:** A recorded check, taken immediately before this change's verify artifact is drafted, that v2 is still unreleased.
- **Acceptance:** `git tag -l` output is empty and `git log origin/main..HEAD` still contains the v2 commits (i.e. they are not on `origin/main`). The command outputs are recorded where verify can cite them. If either condition fails, this task's outcome is "stop — D5 must be re-opened", and no verify artifact is written until the user rules.
- **Blocked by:** 5.1

---

## Self-review

1. Entry keys `{1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 5.3}` — fifteen, matching tasks.md's fifteen task numbers in both directions.
2. Every acceptance criterion names an observable (a verdict on a named fixture, a grep count, a diff scope, a command's success, a table's row/directory correspondence) rather than a quality word.
3. Interfaces are stated where a task consumes or produces something another task depends on (fixtures → README rows and checks → templates/READMEs → dogfood copy) and each side names the other: 1.1–1.3 ↔ 1.4 and 2.1–2.3; 2.1–2.3 ↔ 2.4, 3.1, 3.2; 3.1, 3.2 ↔ 5.1. 4.1, 4.2, 5.2 and 5.3 have no cross-task coupling and omit the block — 5.3's `Blocked by: 5.1` is ordering only (run the precondition check last), not an interface.
