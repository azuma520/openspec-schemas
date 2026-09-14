## MODIFIED Requirements

### Requirement: Applicable tasks require RED and GREEN evidence

Every task annotated `TDD: applicable` SHALL, as part of its completion claim, record RED evidence (subject; non-pass outcome that is a behavioural failure; failure output excerpt sufficient to show the target behaviour was not yet satisfied) and GREEN evidence (the same subject; pass outcome). A SyntaxError, import error, missing dependency, or test-harness error is not a valid RED outcome. An invocation record (the command run) is supporting evidence, recommended but not required. **Evidence carrier (v1)**: the RED and GREEN records SHALL be written in tasks.md, indented under the task's checkbox beside its `TDD:` annotation; plan.md SHALL NOT hold a second copy. tasks.md is the first carrier, not an architecture invariant — a later Result/Evidence store MAY replace it without changing the evidence semantics above. Missing or structurally invalid required evidence is fail-closed at verify.

**The pairing unit is the subject, not the task.** A task MAY carry evidence for more than one subject. Records SHALL pair by their `subject:` value, and each subject appearing under a task SHALL have exactly one RED record and exactly one GREEN record. Subject values SHALL be unique within each side of a task — at most one RED record and at most one GREEN record per subject: two records claiming the same subject on the same side make the pairing indeterminate, which is the property these checks exist to guarantee. Ordinal pairing (the n-th RED with the n-th GREEN) SHALL NOT be used, because inserting one record silently re-pairs every record after it.

**Subject grammar.** A `subject:` value SHALL, after trimming, match `<test-file>::<test-name>`: exactly one `::` separator, with a non-empty remainder on each side after trimming. The check SHALL NOT constrain path syntax, file extension, or test-name characters beyond that — test identifiers differ across ecosystems, and rejecting a legal identifier would manufacture a false non-conformance.

**Record field form.** Within one record, each field key SHALL appear at most once, whether the field is required (`subject:`, `outcome:`, `failure:`) or supporting (`invocation:`); a record carrying the same key on more than one line is structurally invalid and fail-closed at verify, naming the repeated key. A field is one line: its value runs to the end of that line. A following line is read by its own form, not by the author's intent — a line written `- <key>: <value>` is a field of that key, never a continuation of the line above it — so a wrapped value that begins with a field key is the repeated-key case, and a wrapped value that does not is simply not read.

**Completion evidence is one RED and one GREEN per subject, not an execution history.** Where a subject was run more than once, the records submitted as completion evidence SHALL be the single RED and the single GREEN that make the claim; additional runs SHALL NOT be recorded as further RED or GREEN records under that subject.

**Boundary of what these checks decide.** The deterministic checks SHALL verify structure, format and cardinality only, and bridge-owned surfaces SHALL NOT claim they verify evidence truth. Whether the evidence is credible, whether it genuinely reflects test-first development, and whether a RED excerpt is a behavioural failure rather than a harness error remain review judgements. Where the subject under test is a rule executed by reading rather than by code (these checks themselves, when a change edits them), a RED recording `INDETERMINATE` because the rule as written could not decide the case SHALL be judged a behavioural failure (the target property, decidability, unsatisfied), not a harness error. `INDETERMINATE` is a RED-side outcome only: it SHALL NOT be accepted as a GREEN outcome and SHALL NOT by itself satisfy any completion claim.

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

- **WHEN** a RED record's subject has no GREEN record carrying the identical subject value
- **THEN** the deterministic check reports that subject as unpaired and verify reports a blocking finding

#### Scenario: Two subjects under one task both pass

- **WHEN** an applicable task records subjects `test/a.test.js::rejects empty email` and `test/a.test.js::rejects malformed email`, each with exactly one RED and one GREEN
- **THEN** the deterministic checks pass, because the pairing unit is the subject and both subjects are completely paired

#### Scenario: Duplicate subject on one side blocks

- **WHEN** an applicable task carries two RED records whose subject values are identical
- **THEN** verify reports a blocking finding naming the duplicated subject, because the RED-to-GREEN pairing for that subject is indeterminate

#### Scenario: Repeated field key in one record blocks

- **WHEN** a RED record carries two `- failure:` lines, or a GREEN record carries `- subject:` twice
- **THEN** the deterministic check reports the record as structurally invalid, naming the repeated key, and verify reports a blocking finding

#### Scenario: Wrapped value is not a field

- **WHEN** a `failure:` value continues onto a second indented line that does not itself read `- <key>: <value>`
- **THEN** the continuation line is not read as part of the value and is not a field; the record is checked on its one-line fields alone

#### Scenario: Subject not matching the grammar blocks

- **WHEN** a record's `subject:` value is `rejects empty email` with no `::`, or `a::b::c` with two separators, or `::rejects empty email` with an empty left side
- **THEN** the deterministic check reports the malformed subject as a blocking finding

#### Scenario: Unconventional but conforming identifier passes

- **WHEN** a record's `subject:` value is `tests/api_test.go::TestRejectsEmptyEmail/subcase-2`
- **THEN** the grammar check passes, because exactly one `::` separates two non-empty sides and no further path or name syntax is constrained

#### Scenario: Repeated runs are not extra records

- **WHEN** a subject was executed several times before passing and the task records one RED and one GREEN for it
- **THEN** the evidence conforms; the omitted intermediate runs are not required, and recording them as additional RED records under the same subject would instead block as duplicates

#### Scenario: Structurally valid but untrue evidence is not caught by the checks

- **WHEN** a task's records are well-formed, uniquely subjected and completely paired, but the cited test does not exist
- **THEN** the deterministic checks pass and report nothing, and no bridge-owned surface describes that pass as evidence of truth — detecting it is a review judgement
