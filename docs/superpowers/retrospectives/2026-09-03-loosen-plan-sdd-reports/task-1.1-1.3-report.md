# Report — tasks 1.1, 1.2, 1.3 (batch)

## What was created

Six self-contained fixture directories added under
`docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/`,
each with `tasks.md` + `plan.md`, matching the file layout and tone of
existing `f1`–`f7` (bare `## N — <title>` plan headings, no
Delivers/Acceptance/Blocked-by prose — that fuller Plan Contract shape is
enforced by review judgement, not by any deterministic check 8-12, and
f1–f7 already establish this minimal style as the accepted convention for
this fixture set).

- `f8-duplicate-task-number/` — tasks.md has two task lines both numbered
  `1.1` (one applicable with RED/GREEN, one `n/a — prose/doc-only`);
  plan.md has one entry `## 1.1`.
- `f9-duplicate-plan-key/` — tasks.md has one task `2.3` (applicable,
  RED/GREEN matching); plan.md has two entries both keyed `## 2.3`.
- `f10-subject-without-separator/` — one applicable task; RED and GREEN
  both carry `subject: rejects empty email` (no `::`).
- `f11-duplicate-subject-one-side/` — one applicable task; two RED
  records with identical `subject:` values, one GREEN.
- `f12-two-subjects-paired/` — one applicable task; two distinct
  subjects (`rejects empty email`, `rejects empty password`), each with
  its own RED and GREEN, correctly paired by subject. Positive control.
- `f13-deferred-task-in-tasks/` — tasks.md has exactly one task marked
  `[~]`, annotated `TDD: n/a — manual smoke test, deferred this cycle`;
  plan.md has one entry heading and no checkbox/task lines (as every v2
  plan has, since plan.md never carries task rows).

## Pre-edit verdict walks (evidence for later RED records)

All walks below are against the **current, pre-edit** `schema.yaml` text
(`superpowers-bridge/schema.yaml`, verify artifact instruction, checks
7-12, lines ~399-552). Checks not mentioned for a fixture were walked and
found non-applicable or non-blocking with no bearing on the isolated
defect.

### f8-duplicate-task-number

- **Check 12** (`schema.yaml` check 12, current text): "Collect the TASK
  NUMBER of every task line... Collect the ENTRY KEY of every plan.md
  contract entry... Compare the two SETS in both directions... Equal
  counts do not pass this check." Collecting task numbers from tasks.md
  gives the multiset `{1.1, 1.1}`; as a **set** (the check's own word)
  this collapses to `{1.1}`. Entry keys from plan.md: `{1.1}`. The two
  sets compare equal in both directions → no difference reported →
  **PASS, no BLOCK**.
- **Expected (post-fix) verdict:** BLOCK, naming `1.1` as a duplicate
  task number — the two-stage check's stage 1 (no duplicate on either
  side) is what check 12 currently has no text for.
- **Verdict: PASS (wrong)** — the pre-edit set-comparison silently
  discards the duplicate; this is the defect 2.1 fixes.
- Other checks walked: 8 (both tasks carry a valid `TDD:` annotation,
  em-dash separator on the `n/a`) — no block. 9 (task 1.1-first is
  applicable with one RED + one GREEN, both fully fielded; task
  1.1-second is `n/a`, owes no records) — no block. 10 (RED `outcome:
  FAIL`, GREEN `outcome: PASS`, both conforming tokens) — no block. 11
  (RED subject == GREEN subject, identical string) — no block. 7 (no
  `[~]` markers anywhere) — no block.

### f9-duplicate-plan-key

- **Check 12**: task numbers from tasks.md: `{2.3}`. Entry keys from
  plan.md: multiset `{2.3, 2.3}` → as a set, `{2.3}`. Sets equal in both
  directions → **PASS, no BLOCK**.
- **Expected (post-fix) verdict:** BLOCK, naming `2.3` as a duplicate
  entry key on the plan side.
- **Verdict: PASS (wrong)** — same mechanism as f8, mirrored onto the
  plan.md side.
- Other checks walked: 8, 9, 10, 11 all conforming for the single task
  `2.3` (applicable, one RED, one GREEN, matching subjects, valid
  markers) — no block. 7 — no `[~]` markers — no block.

### f10-subject-without-separator

- **Check 11** (current text): "within one task, the RED record's
  `subject:` value and the GREEN record's `subject:` value must be
  identical character for character after leading and trailing
  whitespace is trimmed. Any difference → BLOCK." RED's `subject:` is
  `rejects empty email`; GREEN's `subject:` is the same literal string
  `rejects empty email`. They are identical → **no BLOCK** — check 11
  has nothing to say about the missing `::` because it only ever
  compares RED-to-GREEN, never validates either value's shape.
- **Check 9** (record presence + required fields): both RED and GREEN
  are present with all required fields non-empty after trimming
  (`subject:`, `outcome:`, `failure:` on RED; `subject:`, `outcome:` on
  GREEN) — the check has no format constraint on `subject:`'s content,
  only presence/non-emptiness → **no BLOCK**.
- **Verdict: PASS (wrong)** — no existing check validates the
  `<test-file>::<test-name>` shape of `subject:`; this fixture's only
  defect (missing `::`) is invisible to every current check. This is
  the gap the new subject-grammar check (bound by 2.2) closes.
- Other checks walked: 8, 10, 12 all conforming — no block.

### f11-duplicate-subject-one-side

- **Check 9**: "the lines belonging to it must include one `- RED:`
  line and one `- GREEN:` line" — read as presence (the failure clause
  that follows lists only "a missing record, a missing required field,
  or a required field whose value is empty" as BLOCK triggers — nothing
  about a duplicate). The task includes at least one RED line and one
  GREEN line, and every individual RED/GREEN record present has all its
  required fields non-empty → **no BLOCK**.
- **Check 11**: "the RED record's subject... the GREEN record's
  subject" (singular). Both RED records here carry the identical
  subject `test/auth.test.js::rejects empty email`, which is also the
  GREEN record's subject — so whichever RED record a reader/executor
  picks as "the RED record," its subject equals the GREEN subject →
  **no BLOCK**. The literal check happens to pass cleanly here only
  because the duplicate is a duplicate of an already-matching value.
- **Verdict: PASS (wrong)** — the duplicate RED subject (a violation of
  the new "Subject values SHALL be unique within a task" rule) passes
  through undetected because no current check counts records per
  subject.
- Other checks walked: 8, 10 (both REDs have valid non-`PASS` uppercase
  tokens, `FAIL` and `ERROR`; GREEN is `PASS`) — no block. 12 —
  conforming — no block.

### f12-two-subjects-paired (positive control)

- **Check 9**: presence-based reading again — the task includes RED
  line(s) and GREEN line(s) (two of each), each individual record has
  all required fields non-empty → **no BLOCK** under the presence
  reading.
- **Check 10**: all four records carry valid outcome tokens (`FAIL`,
  `PASS`, `FAIL`, `PASS` in order) — **no BLOCK**.
- **Check 11**: the check's text names "the RED record" and "the GREEN
  record" in the singular, but this task has two RED records (`...email`,
  `...password`) and two GREEN records (`...email`, `...password`) that
  are NOT identical to each other. The check gives no rule for which RED
  pairs with which GREEN when more than one of each exists. A literal
  executor could: (a) take the first RED and first GREEN encountered in
  document order — here that is the email pair, which matches, reading
  as PASS; (b) take the last of each — the password pair, which also
  matches, reading as PASS; or (c) cross-pair first RED against last
  GREEN (`...email` vs `...password`) — a mismatch, reading as BLOCK.
  All three are defensible readings of the same sentence, and (c) is
  exactly the failure mode "ordinal pairing" is banned for under the new
  contract (inserting or reordering one record silently changes which
  pair (a) or (b) picks).
- **Verdict: INDETERMINATE under the pre-edit text** — not a clean PASS:
  the check's wording does not define behavior for more than one RED/GREEN
  per task, so its outcome depends on implementation-specific pairing
  order rather than on the fixture's content. This is the property 1.2's
  brief calls for ("a reader following the old text cannot decide which
  RED pairs with which GREEN").
- **Expected (post-fix) verdict:** PASS / no BLOCK — under subject-scoped
  pairing (new check 9-11), each subject (`...email`, `...password`) has
  exactly one RED and exactly one GREEN, correctly paired by subject
  value, so f12 must not block. This is the positive control the design's
  "good input must not be rejected" risk requires.
- Other checks walked: 8, 12 conforming — no block.

### f13-deferred-task-in-tasks

- **Check 7** (current text): "If plan.md has any tasks marked `[~]`
  deferred..., enumerate each in verify.md §7... Blocks only if §7 is
  empty AND plan.md has `[~]` rows." plan.md in this fixture (as in every
  v2 plan, which never carries checkbox/task lines at all — the Plan
  Contract's entries are `##` headings, not `- [ ]` lines) contains zero
  `[~]` markers. Searching plan.md for `[~]` finds nothing, so the check
  reports "no deferred tasks" and does not block — **even though
  tasks.md's single task IS marked `[~]`**.
- **Verdict: PASS (wrong)** — the fixture demonstrates check 7 can never
  fire against any conforming v2 plan.md, because it reads the wrong
  carrier (plan.md) for a state marker that v2's Plan Contract requires
  to live in tasks.md instead. The real deferred task and its
  gap-analysis obligation are silently skipped.
- Other checks walked: 8 (the one task carries a valid `TDD: n/a —
  manual smoke test, deferred this cycle` annotation) — no block. 9-11
  do not apply (task is `n/a`, owes no RED/GREEN records, and carries
  none). 12 (task number `1` == plan entry key `1`) — no block.

## Files changed

New files only, under the shared fixtures directory (no existing file
touched):

```
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f8-duplicate-task-number/tasks.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f8-duplicate-task-number/plan.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f9-duplicate-plan-key/tasks.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f9-duplicate-plan-key/plan.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f10-subject-without-separator/tasks.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f10-subject-without-separator/plan.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f11-duplicate-subject-one-side/tasks.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f11-duplicate-subject-one-side/plan.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f12-two-subjects-paired/tasks.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f12-two-subjects-paired/plan.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f13-deferred-task-in-tasks/tasks.md
docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f13-deferred-task-in-tasks/plan.md
```

The fixtures README (`.../fixtures/README.md`) was deliberately NOT
touched — that is task 1.4, dispatched separately.

## Self-review findings

- **Completeness:** all six directories present, each with both
  `tasks.md` and `plan.md`. Every acceptance bullet in each brief
  checked against the authored content (task numbers/keys as specified
  — `1.1`/`1.1` for f8, `2.3`/`2.3` for f9; malformed subject with no
  `::` for f10; duplicate RED subject for f11; two paired subjects for
  f12; one `[~]` task with a task-row-free plan.md for f13).
- **Isolation:** each negative fixture (f8, f9, f10, f11, f13) was
  walked against all 12 checks by hand (walk detail above); each has
  exactly one property that reaches a wrong/indeterminate verdict under
  the pre-edit wording, and no other check fires. f12 was walked against
  all 12 checks and found to have zero non-conformances under the
  *targeted new* wording; under the *current* wording its check-11
  outcome is indeterminate rather than a clean pass, which is expected
  and is the property 2.2's positive-control risk mitigation needs (a
  clean pre-edit PASS would not have exercised the ambiguity the fix
  removes).
- **Consistency:** all six follow the f1–f7 shape — `## 1. Fixture
  group` heading, checkbox task lines, two-space nested TDD/RED/GREEN
  blocks, bare `## N — <title>` plan.md entries, realistic (non-`foo`)
  content reusing the auth/email domain already established by f1–f7 so
  the new fixtures read as part of the same set rather than a different
  style.
- **Discipline:** no file outside the six new directories was created,
  edited, or deleted. `git status` (informational, not run as a commit
  action) would show only these twelve new files.

## Concerns

- **f11 and f9's cardinality vs. check 9's wording is a genuine reading
  call, flagged for the controller/2.x implementers:** check 9's phrase
  "must include one `- RED:` line and one `- GREEN:` line" is
  ambiguous between "at least one" and "exactly one." I read it as
  presence-only (supported by the check's own BLOCK-condition list,
  which only names *missing* records/fields, never *extra* ones), which
  is what makes f9's plan-key duplicate and f11's RED-subject duplicate
  possible to author as isolated, single-defect fixtures at all — if
  check 9 already blocked on a second RED line under a stricter reading,
  f11 would not isolate the subject-uniqueness gap (it would trip check
  9 for an unrelated reason). This reading is what 2.1/2.2 will need to
  confirm or correct when they design the exact new wording; I did not
  guess at what the *new* text should say, only walked the *current*
  text faithfully.
- **f12's pre-edit verdict is reported as "indeterminate," not a
  specific PASS or BLOCK** — the brief's own language anticipates this
  ("indeterminate or wrong"), and I judged that an honest walk of check
  11's singular wording against two RED/two GREEN records cannot be
  collapsed to one deterministic answer without picking an
  implementation detail the check's text does not specify. 2.2's RED
  record for f12 should state which of the plausible pre-edit readings
  was actually exercised (first-first, last-last, or the mismatched
  cross-pair) when it captures this fixture's RED — that record has to
  be obtained by actually running the fixture (per the tasks.md header's
  boundary 1), which this task did not do since 1.x is fixture-authoring
  only, not check-execution.

## Fix report — round 1 (2026-09-07)

**Finding (Important):** `f11-duplicate-subject-one-side/tasks.md:11-12`
(original) — the second RED's `outcome: ERROR` / `failure: TypeError:
cannot read property 'value' of undefined` is the same shape as
`f6-syntaxerror-red`, a candidate R1 (review judgement) violation. A
reviewer could raise R1 alongside the duplicate-subject finding, and
f11 would then fail to isolate which rule fired — breaking the one
property its brief pins on it ("f11's only non-conformance is the
duplicated RED subject").

**What changed:** the second RED's `outcome:`/`failure:` pair, in
`docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f11-duplicate-subject-one-side/tasks.md`.
Before:

```
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: ERROR
    - failure: TypeError: cannot read property 'value' of undefined
```

After (matches the first RED's register — an assertion mismatch, not a
harness error — while staying distinguishable from the first record so
the duplicate isn't also an exact-line copy):

```
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined (second run, after refactor)
```

Nothing else in the fixture was touched; no other fixture was touched.

**Re-walk (amended f11 only)**, against the current `schema.yaml`
verify instruction (checks 8-12, lines ~399-552, and review judgement
R1, lines ~563-568 — same text cited in the original walk above):

- **Check 8**: the single task carries one `TDD: applicable` line in
  the required form → no BLOCK.
- **Check 9** (presence-based reading, per the original walk's
  reasoning: the BLOCK conditions the check's text lists are "a
  missing record, a missing required field, or a required field whose
  value is empty" — nothing about a duplicate): the task includes RED
  line(s) and one GREEN line; both RED records have non-empty
  `subject:`/`outcome:`/`failure:`; GREEN has non-empty
  `subject:`/`outcome:` → no BLOCK.
- **Check 10**: both REDs now carry `outcome: FAIL` (a valid
  non-`PASS` uppercase token); GREEN carries `outcome: PASS` → no
  BLOCK.
- **Check 11**: "the RED record's subject... the GREEN record's
  subject" (singular) — both RED subjects are still identical to each
  other and to the GREEN subject
  (`test/auth.test.js::rejects empty email`), so whichever RED is read
  as "the RED record," its subject equals the GREEN subject → no
  BLOCK.
- **Check 12**: task number `{1}` equals plan entry key `{1}`, no
  duplicate on either side → no BLOCK.
- **R1** (review judgement — is each RED's `failure:` excerpt a
  BEHAVIOURAL failure rather than a SyntaxError/import/harness error?):
  the first RED's excerpt is `expected 'Email required', got undefined`
  — an assertion mismatch. The amended second RED's excerpt is
  `expected 'Email required', got undefined (second run, after
  refactor)` — same assertion-mismatch shape, no harness-error language
  (no `TypeError`, `SyntaxError`, import/dependency wording). Both
  records read as behavioural failures → **no R1 violation**.

**Result:** amended f11 now carries exactly one finding under the
current contract — the duplicated RED `subject:` value, invisible to
every deterministic check (9-11) as walked above and in the original
report, and requiring the new per-subject cardinality rule (bound by
2.2) to catch. The R1 ambiguity the reviewer flagged is closed.
