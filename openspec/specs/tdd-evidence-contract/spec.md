# tdd-evidence-contract

## Purpose

Carry TDD through evidence rather than through prescribed steps: tasks.md declares per-task
applicability, applicable tasks record RED/GREEN evidence, and verify runs deterministic
checks on the presence and structure of both before archive. The contract also fixes the
boundary of what those checks may be claimed to prove. Established by change `loosen-plan`
(2026-09-04), which loosened plan.md and moved the TDD carrier here so no state exists where
TDD has no carrier.

## Requirements

### Requirement: tasks.md is the SSOT for TDD applicability

Every task in tasks.md SHALL carry a TDD applicability annotation, indented under the task checkbox: `TDD: applicable` or `TDD: n/a — <reason>`. tasks.md is the single source of truth for applicability; plan.md entries MAY echo but SHALL NOT redefine it. The annotation is a semantic assertion subject to artifact review; the deterministic verify checks verify only its presence and format.

#### Scenario: Missing annotation blocks before archive

- **WHEN** verify runs on a change whose tasks.md contains a task with no TDD annotation
- **THEN** verify reports the missing annotation as a blocking finding (fail-closed at verify), so the change is not verified for archive until annotated

#### Scenario: n/a reason is review-judged, not machine-judged

- **WHEN** a task is annotated `TDD: n/a — documentation only`
- **THEN** the deterministic check passes on presence and format, and whether the reason holds is judged by artifact review

### Requirement: Applicable tasks require RED and GREEN evidence

Every task annotated `TDD: applicable` SHALL, as part of its completion claim, record RED evidence (subject; non-pass outcome that is a behavioural failure; failure output excerpt sufficient to show the target behaviour was not yet satisfied) and GREEN evidence (the same subject; pass outcome). A SyntaxError, import error, missing dependency, or test-harness error is not a valid RED outcome. The RED and GREEN subject SHALL be identical; the v1 subject carrier is `test-file::test-name`. An invocation record (the command run) is supporting evidence, recommended but not required. **Evidence carrier (v1)**: the RED and GREEN records SHALL be written in tasks.md, indented under the task's checkbox beside its `TDD:` annotation; plan.md SHALL NOT hold a second copy. tasks.md is the first carrier, not an architecture invariant — a later Result/Evidence store MAY replace it without changing the evidence semantics above. Missing or structurally invalid required evidence is fail-closed at verify.

#### Scenario: Evidence lives under the task

- **WHEN** an applicable task's RED/GREEN records are indented under that task's checkbox in tasks.md
- **THEN** verify finds and checks them there without consulting any other artifact for evidence

#### Scenario: Valid RED then GREEN

- **WHEN** an applicable task's evidence shows subject `test/foo.test.js::rejects empty email` failing with an assertion message ("expected 'Email required', got undefined") and the same subject later passing
- **THEN** the evidence satisfies the contract's required fields

#### Scenario: Error output is not RED

- **WHEN** an applicable task's RED evidence shows a SyntaxError or missing-import error instead of a behavioural assertion failure
- **THEN** the evidence does not satisfy the contract; this is a review judgement (the deterministic checks see only a non-pass marker), and the reviewer reports it as a blocking finding

#### Scenario: Subject mismatch invalidates the pair

- **WHEN** RED evidence cites one test and GREEN evidence cites a different test
- **THEN** the pair fails the deterministic subject-equality check and verify reports a blocking finding

### Requirement: Claim boundaries of the evidence contract

Bridge-owned surfaces stating what this contract guarantees SHALL claim no more than: RED evidence supports that the subject was executed and failed correctly because the target behaviour was not yet satisfied, supporting the RED-to-GREEN transition. They SHALL NOT claim the evidence proves a test-first development history, proves evidence authenticity (v1 evidence is agent-submitted; authenticity assurance rests on the review layer and degrades with it), or that the deterministic checks assess semantic quality. They SHALL distinguish a *deterministic (machine-evaluable) check* from a *mechanically enforced gate*: v1 requires verify to run the deterministic checks before archive and to block on failure, and that enforcement is instruction-mediated — the verify agent following the schema instruction — so surfaces SHALL NOT claim a Harness-level mechanically enforced, non-bypassable archive-time gate. Generation-time self-review is earlier feedback, not the required control. A recorded check result describes the checked artifacts as they were when the check ran: if `tasks.md` or `plan.md` is modified after a result is recorded, every result computed from the modified file SHALL be treated as STALE and those checks SHALL be re-run before archive. The affected set SHALL be derived from each check's inputs rather than from which checks a given change introduced. That freshness requirement is agent-executed on the same terms as the checks — no digest of the checked state is computed or compared — so surfaces SHALL NOT describe freshness as mechanically guaranteed.

#### Scenario: No over-claim in normative surfaces

- **WHEN** any bridge-owned normative surface describes the TDD evidence contract
- **THEN** it does not state or imply that the evidence proves test-first history, cannot be fabricated, or is enforced by a non-bypassable Harness gate

#### Scenario: Required control located at verify

- **WHEN** an agent skips plan-stage self-review but verify runs its deterministic checks before archive
- **THEN** the v1 claim (verify blocks on failed deterministic checks before archive) still holds as stated

#### Scenario: Verify agent skips a check

- **WHEN** the verify agent does not execute one of the numbered deterministic checks
- **THEN** no v1 mechanism intercepts the omission — this is the stated boundary of instruction-mediated enforcement, and review of verify.md is the only backstop

#### Scenario: Checked artifact changes after the result is recorded

- **WHEN** a deterministic check has been recorded as passing and `tasks.md` or `plan.md` is then modified before archive
- **THEN** the recorded result is stale and the affected checks are re-run before archive, and no surface describes that staleness as being detected mechanically — nothing in the schema compares the checked state against the state the result was computed over
