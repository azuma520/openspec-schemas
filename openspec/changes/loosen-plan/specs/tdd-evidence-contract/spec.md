# tdd-evidence-contract

## ADDED Requirements

### Requirement: tasks.md is the SSOT for TDD applicability

Every task in tasks.md SHALL carry a TDD applicability annotation, indented under the task checkbox: `TDD: applicable` or `TDD: n/a — <reason>`. tasks.md is the single source of truth for applicability; plan.md entries MAY echo but SHALL NOT redefine it. The annotation is a semantic assertion subject to artifact review; the mechanical layer verifies only its presence and format.

#### Scenario: Missing annotation blocks before archive

- **WHEN** verify runs on a change whose tasks.md contains a task with no TDD annotation
- **THEN** the missing annotation is reported as a blocking finding (fail-closed), and the change cannot proceed to archive until annotated

#### Scenario: n/a reason is review-judged, not machine-judged

- **WHEN** a task is annotated `TDD: n/a — documentation only`
- **THEN** the mechanical check passes on presence and format, and whether the reason holds is judged by artifact review

### Requirement: Applicable tasks require RED and GREEN evidence

Every task annotated `TDD: applicable` SHALL, as part of its completion claim, attach RED evidence (subject; non-pass outcome that is a behavioural failure; failure output excerpt sufficient to show the target behaviour was not yet satisfied) and GREEN evidence (the same subject; pass outcome). A SyntaxError, import error, missing dependency, or test-harness error is not a valid RED outcome. The RED and GREEN subject SHALL be identical; the v1 subject carrier is `test-file::test-name`. An invocation record (the command run) is supporting evidence, recommended but not required. Missing or structurally invalid required evidence is fail-closed at verify.

#### Scenario: Valid RED then GREEN

- **WHEN** an applicable task's evidence shows subject `test/foo.test.js::rejects empty email` failing with an assertion message ("expected 'Email required', got undefined") and the same subject later passing
- **THEN** the evidence satisfies the contract's required fields

#### Scenario: Error output is not RED

- **WHEN** an applicable task's RED evidence shows a SyntaxError or missing-import error instead of a behavioural assertion failure
- **THEN** the evidence is structurally invalid and verify reports a blocking finding

#### Scenario: Subject mismatch invalidates the pair

- **WHEN** RED evidence cites one test and GREEN evidence cites a different test
- **THEN** the pair fails the mechanical subject-equality check and verify reports a blocking finding

### Requirement: Claim boundaries of the evidence contract

Bridge-owned surfaces stating what this contract guarantees SHALL claim no more than: RED evidence supports that the subject was executed and failed correctly because the target behaviour was not yet satisfied, supporting the RED-to-GREEN transition. They SHALL NOT claim the evidence proves a test-first development history, proves evidence authenticity (v1 evidence is agent-submitted; authenticity assurance rests on the review layer and degrades with it), or that mechanical checks assess semantic quality. The v1 mechanical guarantee is blocking before archive/acceptance via verify; generation-time self-review is earlier feedback, not the mechanical guarantee.

#### Scenario: No over-claim in normative surfaces

- **WHEN** any bridge-owned normative surface describes the TDD evidence contract
- **THEN** it does not state or imply that the evidence proves test-first history or cannot be fabricated

#### Scenario: Guarantee located at verify

- **WHEN** an agent skips plan-stage self-review but verify's mechanical checks run before archive
- **THEN** the v1 guarantee (mechanical blocking before archive) still holds as claimed
