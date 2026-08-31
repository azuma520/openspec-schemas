# tdd-claim-accuracy

## Purpose

Keep every bridge-owned statement about TDD execution honest: TDD is task-list-conditional,
never guaranteed by the schema or any downstream layer. Established by change
`fix-tdd-transitive-claim` (2026-08-31), which removed the falsified "upstream automatically
enforces TDD" claims.

## Requirements

### Requirement: No unconditional TDD guarantee

Bridge-owned normative surfaces MUST NOT state or imply — the surfaces being
`superpowers-bridge/schema.yaml`, `superpowers-bridge/README.md`,
`superpowers-bridge/README.zh-TW.md`, `superpowers-bridge/templates/*.md`, the top-level
`README.md` / `README.zh-TW.md` bridges table, and the `CLAUDE.md` red-flag list — that TDD executes
automatically or unconditionally downstream — including the forms "internally enforces",
"every task follows RED-GREEN-REFACTOR", "you do NOT need to invoke", and the compressed
pseudo-identifier `TDD-via-subagents`. Statements reporting a **conditional** or
already-falsified status (e.g. rows marked ❌ False / ⚠️, and the factual description that
`writing-plans`' task format contains TDD micro-steps) are conforming. Record-class files
(handoffs, discussion material, `openspec/changes/**/archive`) are exempt as append-only
records.

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

### Requirement: Honest statement of the TDD carrier

The apply instruction in `schema.yaml` SHALL state where TDD actually comes from: TDD
execution depends on whether the task list requires it; `superpowers:writing-plans`'
standard task format contains TDD micro-steps but per-task inclusion depends on that
skill's judgment of task type; the schema itself neither enforces nor verifies TDD; and if
the task list lacks a TDD requirement, no layer of this schema guarantees to add it.

#### Scenario: Agent reading the apply instruction learns the condition

- **WHEN** an agent reads the apply instruction's TDD passage after the change
- **THEN** it is told TDD is task-list-conditional and unverified by the schema, and it is
  not told that any skill will enforce TDD on its behalf

### Requirement: executing-plans exclusion rationale rests on review structure

The rationale SHALL rest on verified structural facts everywhere the bridge explains why
`superpowers:executing-plans` is not supported as an apply fallback — it dispatches no
independent reviewer, and upstream itself directs users to subagent-driven-development when
subagents exist — and SHALL NOT use TDD transitivity as a differentiator (when a task
requires TDD, both executors receive that requirement through plan.md task content;
neither path guarantees it otherwise).

#### Scenario: Old TDD-based comparison is gone

- **WHEN** the fallback rationale segments (schema.yaml, both bridge READMEs, CLAUDE.md
  red-flag list) are read after the change
- **THEN** none argues "it does not bring TDD while we do"; each states the
  review-structure rationale, with the code-review comparison scoped honestly (structural
  dispatch, not one-reviewer-per-task)

### Requirement: Retrospective template does not induce unverifiable attestation

`superpowers-bridge/templates/retrospective.md` SHALL keep the skill-compliance table but
MUST NOT pressure the agent toward a default all-✓ attestation: no "default expectation:
all ✓", no "blank section (all green) is the expected state", and no prohibition on honest
reasons (such as "不需要") for a ✗.

#### Scenario: Compliance table filled honestly

- **WHEN** an agent fills the retrospective skill-compliance section for a cycle where a
  skill was legitimately not used
- **THEN** the template's instructions permit recording ✗ with an honest reason, and no
  instruction tells the agent that all-✓ is the expected default
