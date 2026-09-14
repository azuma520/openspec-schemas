## MODIFIED Requirements

### Requirement: No unconditional TDD guarantee

Bridge-owned normative surfaces MUST NOT state or imply — the surfaces being
`superpowers-bridge/schema.yaml`, `superpowers-bridge/README.md`,
`superpowers-bridge/README.zh-TW.md`, `superpowers-bridge/templates/*.md`, the top-level
`README.md` / `README.zh-TW.md` bridges table, and the `CLAUDE.md` red-flag list — that TDD executes
automatically or unconditionally downstream — including the forms "internally enforces",
"every task follows RED-GREEN-REFACTOR", "you do NOT need to invoke", and the compressed
pseudo-identifier `TDD-via-subagents`. Statements reporting a **conditional** or
already-falsified status (e.g. rows marked ❌ False / ⚠️, and the factual description that
applicability is declared per task in tasks.md and carries no guarantee for tasks annotated
`TDD: n/a`) are conforming. A surface MUST NOT cite `writing-plans`' micro-step task format as
the description of where TDD comes from: under the evidence contract the carrier is the
tasks.md annotation plus its RED/GREEN evidence, and `writing-plans` is not a normative
dependency of any artifact. Record-class files (handoffs, discussion material,
`openspec/changes/**/archive`) are exempt as append-only records.

#### Scenario: Falsified guarantee segments are corrected

- **WHEN** each segment of the frozen Affected Surface (brainstorm §4.1, 35 segments / 21
  logical positions) is read after the change
- **THEN** no segment claims unconditional or automatic TDD; each formerly false segment
  either is deleted or states the conditional truth

#### Scenario: Replacement wording passes the guarantee test

- **WHEN** any sentence added or reworded by this change is checked for absolute claims
  (positive "always happens" or mirror-image "never happens")
- **THEN** every claim about TDD execution is conditional on the task list, and the
  negative claim is scoped as "no layer **guarantees** to add it", not "no layer will"

#### Scenario: writing-plans is no longer cited as the carrier

- **WHEN** a bridge-owned normative surface is read for how a task acquires its TDD requirement
- **THEN** it names the tasks.md annotation and the RED/GREEN evidence contract, and no
  surface presents `writing-plans`' micro-step task format as that answer

### Requirement: executing-plans exclusion rationale rests on review structure

The rationale SHALL rest on verified structural facts everywhere the bridge explains why
`superpowers:executing-plans` is not supported as an apply fallback — it dispatches no
independent reviewer, and upstream itself directs users to subagent-driven-development when
subagents exist — and SHALL NOT use TDD transitivity as a differentiator. TDD is not a
differentiator between the two executors because it does not travel through either of them:
applicability is declared per task in tasks.md and evidenced by the RED/GREEN records the
tdd-evidence-contract capability defines, so the requirement reaches an executor through the
task list it is given, whichever executor that is. Surfaces SHALL NOT describe plan.md task
content as the carrier of that requirement — under the Plan Contract plan.md holds contract
entries and no task list.

#### Scenario: Old TDD-based comparison is gone

- **WHEN** the fallback rationale segments (schema.yaml, both bridge READMEs, CLAUDE.md
  red-flag list) are read after the change
- **THEN** none argues "it does not bring TDD while we do"; each states the
  review-structure rationale, with the code-review comparison scoped honestly (structural
  dispatch, not one-reviewer-per-task)

#### Scenario: Carrier named consistently across the spec

- **WHEN** this capability's own requirements are read together
- **THEN** every statement of where a TDD requirement reaches an executor names the tasks.md
  annotation and evidence contract, and none names plan.md task content, so the spec presents
  a single answer rather than two conflicting ones
