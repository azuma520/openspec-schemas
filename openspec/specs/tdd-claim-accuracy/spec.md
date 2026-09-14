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

### Requirement: Honest statement of the TDD carrier

The apply instruction in `schema.yaml` SHALL state where TDD actually comes from under the evidence contract: TDD applicability is declared per task in tasks.md (`TDD: applicable` / `TDD: n/a — <reason>`); applicable tasks must record RED/GREEN evidence under the task in tasks.md per the tdd-evidence-contract capability; the verify instruction requires deterministic checks of the presence and structure of annotations and evidence before archive, executed by the verify agent (instruction-mediated, not a Harness-enforced gate); and the schema does not verify evidence semantics or authenticity — those rest on the review layer and degrade with it. The instruction SHALL NOT claim TDD executes automatically or unconditionally, SHALL NOT claim the schema verifies more than presence and structure, SHALL NOT claim a non-bypassable mechanical gate, and SHALL NOT retain the superseded statements that the schema "neither enforces nor verifies TDD" or that TDD arrives via `writing-plans`' micro-step task content.

#### Scenario: Agent reading the apply instruction learns the evidence condition

- **WHEN** an agent reads the apply instruction's TDD passage after the change
- **THEN** it is told that applicability is annotation-driven from tasks.md, that applicable tasks owe RED/GREEN evidence in tasks.md checked by verify's deterministic checks (agent-executed), and that semantic and authenticity assurance belong to review — and it is not told that any skill or layer executes or fully verifies TDD on its behalf

#### Scenario: Superseded carrier statements are gone

- **WHEN** bridge-owned normative surfaces are read after the change
- **THEN** none states that the schema "neither enforces nor verifies TDD" or that TDD arrives via writing-plans micro-steps; each describes the annotation + evidence carrier at its actual capability

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

