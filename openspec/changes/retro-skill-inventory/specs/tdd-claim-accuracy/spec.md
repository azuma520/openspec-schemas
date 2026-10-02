## ADDED Requirements

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
