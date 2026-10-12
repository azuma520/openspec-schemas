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

The exclusion rationale SHALL rest on the capability the bridge's apply requires, on every
bridge-owned surface that explains why `superpowers:executing-plans` is not supported as an
apply fallback: independent review during execution (after each task, or after each batch of
small same-shape tasks, rather than only at the end). These surfaces are the `description` and the apply
instruction in `superpowers-bridge/schema.yaml`, the design sections of both bridge READMEs that
give the rationale (the touchpoints notice, design touch #4 and the apply-phase entry of the
fallback strategy), and the CLAUDE.md red-flag list. Each of them SHALL also state the current
limitation: this version's apply requires subagent-driven-development, and when the required
capability is missing apply stops at Step 0 instead of switching to executing-plans.

Facts about what a particular upstream version of executing-plans does or lacks, together with
the Superpowers versions and sources against which they were verified, SHALL be recorded in the
bridge README's Re-verification log. The log SHALL state, with those versions and sources, that
executing-plans runs without a reviewer per task and reviews the whole branch once at the end,
and that on a platform without a subagent tool — the situation a fallback would serve — that
final review is performed by the author. The design surfaces above SHALL refer to the log for
these facts rather than restate version-specific mechanism, so that an upstream change is
recorded by adding to the log, not by rewriting the rationale. The CLAUDE.md red-flag list
SHALL likewise refer to the log and is not required to restate those facts. Moving the facts to the log does not license an
unsupported rationale: a surface that says executing-plans lacks the required capability SHALL
say so only as the log's verified facts support. Dated entries already in the log stay as they
are.

No surface, the log included, SHALL rest the exclusion on what upstream recommends choosing
between executors, and none SHALL state that executing-plans dispatches no independent reviewer
at all — with a subagent tool it dispatches one for the final review.

The rationale SHALL NOT use TDD as a differentiator between the two executors. TDD is not a
differentiator because the bridge's TDD requirement does not depend on either executor carrying
it: applicability is declared per task in tasks.md and evidenced by the RED/GREEN records the
tdd-evidence-contract capability defines, so the requirement reaches an executor through the
task list it is given, whichever executor that is. Surfaces SHALL NOT describe plan.md task
content as the carrier of that requirement — under the Plan Contract plan.md holds contract
entries and no task list.

#### Scenario: REQ-3-S1 Old TDD-based comparison is gone

- **WHEN** the fallback rationale surfaces (schema.yaml, both bridge READMEs, CLAUDE.md
  red-flag list) are read after the change
- **THEN** none argues "it does not bring TDD while we do"; each states the capability
  rationale, with the review comparison scoped honestly (review during execution, which may
  batch small same-shape tasks — not one-reviewer-per-task)

#### Scenario: REQ-3-S2 Carrier named consistently across the spec

- **WHEN** this capability's own requirements are read together
- **THEN** every statement of where a TDD requirement reaches an executor names the tasks.md
  annotation and evidence contract, and none names plan.md task content, so the spec presents
  a single answer rather than two conflicting ones

#### Scenario: REQ-3-S3 Superseded executing-plans claims are gone

- **WHEN** the fallback rationale surfaces and the Re-verification log are read after the
  change
- **THEN** none states that executing-plans dispatches no independent reviewer without
  qualification, none states that upstream directs users to subagent-driven-development
  whenever subagents exist, and none rests the exclusion on any upstream recommendation; the
  log states, with the versions and sources verified, that executing-plans has no reviewer per
  task and that its final review is author-performed on a platform without a subagent tool

#### Scenario: REQ-3-S4 Version facts live in the log, rationale states capability

- **WHEN** a design surface named in this requirement is read after the change
- **THEN** it states the required capability (independent review during execution) and the
  current limitation (apply requires subagent-driven-development and stops at Step 0 without
  it), refers to the Re-verification log for executing-plans' behaviour, and does not itself
  describe that behaviour per Superpowers version; a later upstream change to executing-plans
  is recordable by a new log entry without editing these surfaces

### Requirement: REQ-4 Retrospective template does not induce unverifiable attestation

`superpowers-bridge/templates/retrospective.md` SHALL keep the skill-compliance table but
MUST NOT pressure the agent toward a default all-✓ attestation: no "default expectation:
all ✓", no "blank section (all green) is the expected state", and no prohibition on honest
reasons (such as "不需要") for a ✗.

The same honesty SHALL govern the record of a deliberately skipped
`superpowers:subagent-driven-development`. When it is skipped under an explicit user ruling,
the skipped-skill rules of the retrospective instruction in `superpowers-bridge/schema.yaml`
and the `### Deliberately Skipped Skills` guidance in the template SHALL direct the record to
answer the existing three questions as follows, without adding a field or an option:

- **What was skipped** names the assurance that was not obtained — independent review during
  execution.
- **Why this cycle** cites the user ruling, how the work was actually executed, and what
  substitute review or verification was used.
- **How to prevent recurrence** uses the existing `one-off — schema boundary case` option and
  states that the ruling covers this change only, how the deviation was disclosed, and where
  the evidence is kept.

Both surfaces SHALL name that option with the same text, `one-off — schema boundary case`; the
template SHALL NOT qualify it as "no prevention possible", because the answer still states how
unauthorised deviation, undisclosed gaps and untrue conformance claims are prevented.

Neither surface SHALL present such a record as satisfying an assurance that was not obtained,
as equivalent to subagent-driven-development, as conformance with the bridge's execution
contract, or as making the path actually taken a supported execution mode.

A ruling SHALL cover only the change it was made for. Neither surface SHALL treat an earlier
ruling as precedent that authorises a later skip. When a similar skip has occurred in earlier
cycles, the record SHALL state how many and where, and the pattern SHALL be raised as a §6
Promote candidate under the existing rule for skills skipped across multiple cycles.

#### Scenario: REQ-4-S1 Compliance table filled honestly

- **WHEN** an agent fills the retrospective skill-compliance section for a cycle where a
  skill was legitimately not used
- **THEN** the template's instructions permit recording ✗ with an honest reason, and no
  instruction tells the agent that all-✓ is the expected default

#### Scenario: REQ-4-S2 Sanctioned SDD skip discloses the lost assurance

- **WHEN** a retrospective records that subagent-driven-development was skipped under an
  explicit user ruling
- **THEN** the schema rules and the template direct the record to name independent review
  during execution as not obtained, cite the ruling and the substitute review, and answer the
  prevention question with the existing `one-off — schema boundary case` option; nothing in
  either tells the agent that the record makes the skip equivalent to subagent-driven-development
  or the bridge's execution contract satisfied

#### Scenario: REQ-4-S3 Recurring skips are not hidden behind one-off

- **WHEN** a retrospective records a sanctioned subagent-driven-development skip and similar
  skips are on record from earlier cycles
- **THEN** the schema rules and the template direct the record to state that the ruling covers
  this change only, to give the number and location of the earlier cases, and to raise the
  pattern as a §6 Promote candidate; neither presents the earlier rulings as authorising this
  or any later skip

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

### Requirement: REQ-6 Apply keeps its three execution situations apart

The apply instruction in `superpowers-bridge/schema.yaml` SHALL keep three situations apart and
SHALL NOT merge any two of them:

- **Required skill missing.** When any skill that Step 0 lists as required for apply is missing,
  apply SHALL STOP at Step 0 and inform the user. The instruction SHALL state that the bridge
  has no internal manual fallback for apply and SHALL NOT point to one. It SHALL name the
  user's options — install the required skills, or explicitly choose to continue the change
  under the built-in `spec-driven` schema, a different workflow rather than a degraded path of
  this one — and SHALL forbid the agent from switching schemas or execution paths on its own
  initiative.
- **subagent-driven-development available.** Apply SHALL execute per its step-2 contract through
  subagent-driven-development.
- **subagent-driven-development available but deliberately not used under an explicit user
  ruling.** The instruction SHALL describe this as an exception to the schema's process, not a
  supported execution mode. It SHALL state that only the user's explicit ruling for this change
  makes the exception, that the agent SHALL NOT decide it on its own initiative, and that a
  ruling made for an earlier change does not carry over. It SHALL NOT describe the path taken as
  equivalent to subagent-driven-development or as satisfying the independent review it
  provides. When the change requires an assurance the substitute cannot provide, it SHALL direct
  the agent to STOP and report. The deviation is recorded per REQ-4.

This requirement states the existing execution contract explicitly. It adds no fallback, no
executor, no mechanical check and no recorded field, and the third situation is not an
execution path the agent may select. Its STOP rule covers the required-skill check only: the
CLI-tool check that Step 0 also performs surfaces a missing tool as a warning, not a STOP, and
this requirement does not change that.

#### Scenario: REQ-6-S1 Missing required skill stops without a fallback

- **WHEN** a required apply skill is missing at Step 0
- **THEN** the instruction tells the agent to STOP and inform the user, states that the bridge
  has no internal manual fallback, does not refer to any fallback section, names installing
  the skills or explicitly choosing `spec-driven` as the user's options, and forbids the agent
  from switching schemas or execution paths itself

#### Scenario: REQ-6-S2 Deliberate skip is a user-ruled exception, not a mode

- **WHEN** the apply instruction is read for the case where subagent-driven-development is
  available but not used
- **THEN** it calls the case an exception rather than a supported execution mode, requires an
  explicit user ruling for this change, says an earlier ruling does not carry over, forbids the
  agent from choosing it, and does not present the path taken as equivalent to
  subagent-driven-development

#### Scenario: REQ-6-S3 Missing assurance stops rather than being recorded away

- **WHEN** a deliberate skip is under way and the change requires an assurance the substitute
  cannot provide
- **THEN** the instruction directs the agent to STOP and report, and does not let a record of
  the deviation stand in for the missing assurance

#### Scenario: REQ-6-S4 CLI-tool warning is unchanged

- **WHEN** Step 0 finds a project CLI tool missing but every required skill present
- **THEN** the instruction surfaces the missing tool as a warning and does not STOP on that
  ground

