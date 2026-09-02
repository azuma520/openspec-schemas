# plan-contract

## ADDED Requirements

### Requirement: Plan is a per-task execution contract

`superpowers-bridge` plan.md SHALL consist of a header (goal; pointers to the change's specs/ and design.md; global constraints copied verbatim from the specs) and exactly one contract entry per tasks.md task, keyed by the tasks.md task number. Each entry SHALL state: what it delivers (end-to-end behaviour, not a layer-by-layer implementation list); acceptance criteria that are concrete and verifiable; and its blocking dependencies (or an explicit "none"). Interfaces (consumed/produced names and shapes) SHALL be stated for tasks that couple with other tasks and MAY be omitted for tasks with no cross-task coupling.

#### Scenario: Conforming plan entry

- **WHEN** a plan.md entry for a coupled task states delivered behaviour, verifiable acceptance criteria, blocking dependencies, and its cross-task interfaces
- **THEN** the entry conforms to the Plan Contract

#### Scenario: Entry-count cross-check

- **WHEN** verify runs on a change whose plan.md entry count does not match the tasks.md task count
- **THEN** the mismatch is reported as a blocking finding

#### Scenario: Uncoupled task omits interfaces

- **WHEN** a task has no consumer or producer relationship with any other task and its plan entry omits the interfaces block
- **THEN** the entry still conforms (interfaces are conditionally required, not unconditional)

### Requirement: No step prescription

The plan artifact instruction SHALL NOT require micro-step decomposition, exact file paths, code snippets, commit points, or any fixed execution sequence. A decision-rich snippet (state machine, schema, type shape) MAY be included where it encodes a decision more precisely than prose. Vague acceptance language that cannot be verified (e.g. "works correctly", "handles errors appropriately") is non-conforming.

#### Scenario: Two implementations both conform

- **WHEN** two executors implement the same plan entry by different paths and both satisfy its acceptance criteria
- **THEN** neither is non-conforming for having deviated from any step sequence, because no step sequence is prescribed

#### Scenario: Vague acceptance criterion rejected

- **WHEN** a plan entry's acceptance criterion is "feature works correctly" with no verifiable condition
- **THEN** plan self-review or artifact review flags the entry as non-conforming

### Requirement: Producer is agent direct generation

The schema SHALL NOT require invoking any skill to produce plan.md; the agent generates it directly from tasks.md, design.md, and the change's specs. `superpowers:writing-plans` SHALL NOT be a normative dependency of the plan artifact and SHALL NOT have a plan-artifact PRECHECK, but its use as an optional decomposition aid is not prohibited; its micro-step output does not define plan.md's normative format.

#### Scenario: Plan produced without any skill

- **WHEN** an agent produces plan.md directly from the change artifacts on a platform without the Superpowers writing-plans skill
- **THEN** the plan artifact completes without a PRECHECK failure

#### Scenario: Optional aid does not change the format

- **WHEN** an executor uses writing-plans as a private decomposition aid and then writes plan.md
- **THEN** plan.md must still conform to the Plan Contract shape, not the micro-step format
