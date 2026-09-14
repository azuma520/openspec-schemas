# Brief — task 1.1

## Plan contract entry (authoritative)

## 1.1 — Fixtures for duplicate keys on either side (f8, f9)

- **Delivers:** Two new self-contained fixture directories in the mutation-fixture set, each breaking exactly one thing: f8 has a repeated task number in tasks.md against a single matching plan entry; f9 has a repeated entry key in plan.md against a single matching task. Everything else in each pair conforms to the current v2 contract, so no check other than the two-stage check 12 has grounds to block.
- **Acceptance:** Each directory contains a tasks.md and a plan.md and nothing that a v2 check other than check 12 would flag (every task annotated, every applicable task fully evidenced, every outcome marker well-formed). In f8 exactly one task number appears exactly twice and the two key sets are otherwise equal; in f9 exactly one `##` entry key appears exactly twice and the sets are otherwise equal. Under the pre-edit check 12 wording, both fixtures reach a PASS verdict (sets equal) — that is the property 2.1 needs them to have.
- **Blocked by:** none
- **Interfaces:** Produces fixture directories `f8-duplicate-task-number/` and `f9-duplicate-plan-key/` consumed by 2.1 (as RED/GREEN subjects) and by 1.4 (as README rows).

## tasks.md line (authoritative)

- [ ] 1.1 Add `f8-duplicate-task-number` (tasks.md has two task lines numbered `1.1`, plan.md has one entry keyed `1.1`) and `f9-duplicate-plan-key` (plan.md has two `##` entries keyed `2.3`, tasks.md has one task `2.3`) under `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/`, each a self-contained tasks.md + plan.md pair with everything else conforming
  - TDD: n/a — the fixtures are the test material for 2.1, not code under test; their correctness is shown by 2.1's RED/GREEN records (wrong verdict before, right verdict after)

## Plan header + Global Constraints (bind every entry)

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
- "Records SHALL pair by their `subject:` value, and each subject appearing under a task SHALL have exactly one RED record and exactly one GREEN record. Subject values SHALL be unique within a task"
- "Ordinal pairing (the n-th RED with the n-th GREEN) SHALL NOT be used, because inserting one record silently re-pairs every record after it."
- "A `subject:` value SHALL, after trimming, match `<test-file>::<test-name>`: exactly one `::` separator, with a non-empty remainder on each side after trimming. The check SHALL NOT constrain path syntax, file extension, or test-name characters beyond that"
- "The deterministic checks SHALL verify structure, format and cardinality only, and bridge-owned surfaces SHALL NOT claim they verify evidence truth."
- "A surface MUST NOT cite `writing-plans`' micro-step task format as the description of where TDD comes from: under the evidence contract the carrier is the tasks.md annotation plus its RED/GREEN evidence"
- "Surfaces SHALL NOT describe plan.md task content as the carrier of that requirement — under the Plan Contract plan.md holds contract entries and no task list."

Binding non-goals carried from design.md (not spec text, but every entry is bounded by them): no P2 is pulled in; no archived loosen-plan artifact is rewritten; no deferred-task-to-plan-entry rule is added; schema major stays `2` and the bundle stays `2.0.0` while D5's precondition holds.

---


## tasks.md file header — TDD applicability rules for this change (binding)

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
