# tdd-claim-accuracy

## Purpose

Keep every bridge-owned statement about TDD execution honest: TDD is task-list-conditional,
never guaranteed by the schema or any downstream layer. Established by change
`fix-tdd-transitive-claim` (2026-08-31), which removed the falsified "upstream automatically
enforces TDD" claims.
## Requirements
### Requirement: REQ-1 No unconditional TDD guarantee

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

#### Scenario: REQ-1-S1 Falsified guarantee segments are corrected

- **WHEN** each segment of the frozen Affected Surface (brainstorm §4.1, 35 segments / 21
  logical positions) is read after the change
- **THEN** no segment claims unconditional or automatic TDD; each formerly false segment
  either is deleted or states the conditional truth

#### Scenario: REQ-1-S2 Replacement wording passes the guarantee test

- **WHEN** any sentence added or reworded by this change is checked for absolute claims
  (positive "always happens" or mirror-image "never happens")
- **THEN** every claim about TDD execution is conditional on the task list, and the
  negative claim is scoped as "no layer **guarantees** to add it", not "no layer will"

#### Scenario: REQ-1-S3 writing-plans is no longer cited as the carrier

- **WHEN** a bridge-owned normative surface is read for how a task acquires its TDD requirement
- **THEN** it names the tasks.md annotation and the RED/GREEN evidence contract, and no
  surface presents `writing-plans`' micro-step task format as that answer

### Requirement: REQ-2 Honest statement of the TDD carrier

The apply instruction in `schema.yaml` SHALL state where TDD actually comes from under the evidence contract: TDD applicability is declared per task in tasks.md (`TDD: applicable` / `TDD: n/a — <reason>`); applicable tasks must record RED/GREEN evidence under the task in tasks.md per the tdd-evidence-contract capability; the verify instruction requires deterministic checks of the presence and structure of annotations and evidence before archive, executed by the verify agent (instruction-mediated, not a Harness-enforced gate); and the schema does not verify evidence semantics or authenticity — those rest on the review layer and degrade with it. The instruction SHALL NOT claim TDD executes automatically or unconditionally, SHALL NOT claim the schema verifies more than presence and structure, SHALL NOT claim a non-bypassable mechanical gate, and SHALL NOT retain the superseded statements that the schema "neither enforces nor verifies TDD" or that TDD arrives via `writing-plans`' micro-step task content.

#### Scenario: REQ-2-S1 Agent reading the apply instruction learns the evidence condition

- **WHEN** an agent reads the apply instruction's TDD passage after the change
- **THEN** it is told that applicability is annotation-driven from tasks.md, that applicable tasks owe RED/GREEN evidence in tasks.md checked by verify's deterministic checks (agent-executed), and that semantic and authenticity assurance belong to review — and it is not told that any skill or layer executes or fully verifies TDD on its behalf

#### Scenario: REQ-2-S2 Superseded carrier statements are gone

- **WHEN** bridge-owned normative surfaces are read after the change
- **THEN** none states that the schema "neither enforces nor verifies TDD" or that TDD arrives via writing-plans micro-steps; each describes the annotation + evidence carrier at its actual capability

### Requirement: REQ-3 executing-plans exclusion rationale rests on review structure

The rationale SHALL rest on verified structural facts about `superpowers:executing-plans` itself
everywhere the bridge explains why it is not supported as an apply fallback: it runs without a
reviewer per task and reviews the whole branch once at the end, and on a platform without a
subagent tool — the situation a fallback would serve — that final review is performed by the
author. The bridge's apply relies on independent review during execution (after each task, or
after each batch of small same-shape tasks, rather than only at the end). The rationale SHALL NOT
rest on what upstream recommends choosing between executors, and SHALL NOT state that
executing-plans dispatches no independent reviewer at all — with a subagent tool it dispatches
one for the final review.

The rationale SHALL NOT use TDD as a differentiator between the two executors. TDD is not a
differentiator because the bridge's TDD requirement does not depend on either executor carrying
it: applicability is declared per task in tasks.md and evidenced by the RED/GREEN records the
tdd-evidence-contract capability defines, so the requirement reaches an executor through the
task list it is given, whichever executor that is. Surfaces SHALL NOT describe plan.md task
content as the carrier of that requirement — under the Plan Contract plan.md holds contract
entries and no task list.

#### Scenario: REQ-3-S1 Old TDD-based comparison is gone

- **WHEN** the fallback rationale segments (schema.yaml, both bridge READMEs, CLAUDE.md
  red-flag list) are read after the change
- **THEN** none argues "it does not bring TDD while we do"; each states the
  review-structure rationale, with the code-review comparison scoped honestly (review during
  execution, which may batch small same-shape tasks — not one-reviewer-per-task)

#### Scenario: REQ-3-S2 Carrier named consistently across the spec

- **WHEN** this capability's own requirements are read together
- **THEN** every statement of where a TDD requirement reaches an executor names the tasks.md
  annotation and evidence contract, and none names plan.md task content, so the spec presents
  a single answer rather than two conflicting ones

#### Scenario: REQ-3-S3 Superseded executing-plans claims are gone

- **WHEN** the same fallback rationale segments are read after the change
- **THEN** none states that executing-plans dispatches no independent reviewer without
  qualification, none states that upstream directs users to subagent-driven-development
  whenever subagents exist, and none rests the exclusion on any upstream recommendation;
  each states that executing-plans has no reviewer per task and that its final review is
  author-performed on a platform without a subagent tool

### Requirement: REQ-4 Retrospective template does not induce unverifiable attestation

`superpowers-bridge/templates/retrospective.md` SHALL keep the skill-compliance table but
MUST NOT pressure the agent toward a default all-✓ attestation: no "default expectation:
all ✓", no "blank section (all green) is the expected state", and no prohibition on honest
reasons (such as "不需要") for a ✗.

#### Scenario: REQ-4-S1 Compliance table filled honestly

- **WHEN** an agent fills the retrospective skill-compliance section for a cycle where a
  skill was legitimately not used
- **THEN** the template's instructions permit recording ✗ with an honest reason, and no
  instruction tells the agent that all-✓ is the expected default

### Requirement: REQ-5 Retrospective skill inventory follows one spec-owned criterion

The retrospective skill-compliance section (§4) SHALL inventory exactly two classes of
items: (1) Superpowers skills the superpowers-bridge workflow explicitly requires invoking —
`brainstorming` (required by the `brainstorm` artifact) and the skills required by apply
pre-flight (`using-git-worktrees`, `subagent-driven-development`,
`finishing-a-development-branch`); and (2) Superpowers disciplines the schema requires to be
carried out and whose execution the retrospective must record, even though the schema does
not invoke them directly — `test-driven-development` (carried by the tasks.md TDD annotations
and RED/GREEN evidence) and `requesting-code-review` (structural via
subagent-driven-development).

A skill the schema names only as an optional aid, and that carries none of the class (2)
disciplines, MUST NOT be listed on the grounds that it may be useful; `superpowers:writing-plans`
is such a skill.

This requirement is the normative owner of the criterion and of the six-item inventory above.
The retrospective instruction in `superpowers-bridge/schema.yaml` SHALL state the two-class
criterion to the agent, and `superpowers-bridge/templates/retrospective.md` SHALL present
exactly the six rows above. Both the schema instruction and the template MUST NOT state a
second, different definition of what §4 lists. When the inventory changes, this requirement changes first and the schema and template
follow it.

This requirement governs which rows the inventory contains. It does not change how a row is
filled: the conditional and structural labels on the TDD and code-review rows, the skipped-skill
rules, and REQ-4's prohibition on default all-✓ attestation stay as they are. A row may still be
filled as not yet done when its skill runs after the retrospective is written (for example
`finishing-a-development-branch`, which runs after archive).

#### Scenario: REQ-5-S1 Required invocations are inventoried

- **WHEN** an agent reads the §4 table of the retrospective template
- **THEN** it finds a row for each skill the workflow explicitly requires invoking —
  `brainstorming`, `using-git-worktrees`, `subagent-driven-development` and
  `finishing-a-development-branch` — including `brainstorming`, which belongs to the
  brainstorm phase rather than apply

#### Scenario: REQ-5-S2 Required disciplines are inventoried though not invoked by the schema

- **WHEN** an agent reads the §4 table of the retrospective template
- **THEN** it finds rows for `test-driven-development` and `requesting-code-review`, with their
  existing conditional and structural labels, so the retrospective can record whether those
  disciplines were carried out

#### Scenario: REQ-5-S3 An optional aid is not inventoried

- **WHEN** an agent reads the §4 table of the retrospective template
- **THEN** it finds no row for `superpowers:writing-plans`, because the schema names it only
  as an optional private decomposition aid and it carries no class (2) discipline

#### Scenario: REQ-5-S4 Template and schema state one definition

- **WHEN** the retrospective instruction's §4 text in `schema.yaml` and the §4 section of the
  retrospective template are read together
- **THEN** the schema states the two-class criterion, the template's rows are exactly the six
  items this requirement lists, and neither describes §4 as listing only the apply phase or by
  any other conflicting definition

