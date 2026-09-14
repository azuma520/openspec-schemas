# plan-contract

## Purpose

Define what a `superpowers-bridge` plan.md is: a per-task execution contract that specifies
*what must be true* rather than *which steps to take*. Two competent executors may reach the
same acceptance criteria by different paths without either being non-conforming. Established
by change `loosen-plan` (2026-09-04), which replaced the micro-step plan format.
## Requirements
### Requirement: Plan is a per-task execution contract

`superpowers-bridge` plan.md SHALL consist of a header (goal; pointers to the change's specs/ and design.md; global constraints copied verbatim from the specs) and exactly one contract entry per tasks.md task, keyed by the tasks.md task number. Each entry SHALL state: what it delivers (end-to-end behaviour, not a layer-by-layer implementation list); acceptance criteria that are concrete and verifiable; and its blocking dependencies (or an explicit "none"). Interfaces (consumed/produced names and shapes) SHALL be stated for tasks that couple with other tasks and MAY be omitted for tasks with no cross-task coupling.

The correspondence between tasks.md task numbers and plan.md entry keys SHALL be one-to-one, and the deterministic verify check SHALL establish it in two stages: first that neither side contains a duplicate key, then that the two key sets are equal in both directions. Set equality alone is insufficient — a duplicate collapses in a set, so two tasks numbered `1.1` against one plan entry keyed `1.1` would compare equal while one task holds no contract entry of its own. A duplicate on either side SHALL be reported as a blocking finding naming the repeated key, distinctly from a missing or extra key, because the two are different defects with different repairs.

plan.md SHALL NOT carry task-level state markers (deferral and the like); tasks.md is their carrier. Any deterministic check concerning task state SHALL therefore read tasks.md, and a check that searches plan.md for task rows is non-conforming — under this contract plan.md holds contract entries, never a task list, so such a check can never fire.

#### Scenario: Conforming plan entry

- **WHEN** a plan.md entry for a coupled task states delivered behaviour, verifiable acceptance criteria, blocking dependencies, and its cross-task interfaces
- **THEN** the entry conforms to the Plan Contract

#### Scenario: Task ID set cross-check

- **WHEN** verify runs on a change where the set of tasks.md task numbers and the set of plan.md entry keys differ in either direction (a task with no plan entry, or a plan entry keyed to no task — including the equal-count case such as tasks `{1,2,3}` vs plan `{1,2,9}`)
- **THEN** each missing or extra key is reported as a blocking finding

#### Scenario: Duplicate task number blocks

- **WHEN** tasks.md contains two task lines both numbered `1.1` and plan.md contains exactly one entry keyed `1.1`
- **THEN** verify reports a blocking finding naming the repeated task number `1.1`, and does not pass the change on the grounds that the two key sets are equal

#### Scenario: Duplicate plan entry key blocks

- **WHEN** plan.md contains two `##` contract entries whose keys are both `2.3`
- **THEN** verify reports a blocking finding naming the repeated entry key `2.3`, on the same terms as a duplicate on the tasks side

#### Scenario: Unique keys and equal sets pass

- **WHEN** every tasks.md task number occurs once, every plan.md entry key occurs once, and the two sets are equal
- **THEN** the one-to-one check passes

#### Scenario: Deferral marker is read from tasks.md

- **WHEN** a task is marked deferred in tasks.md and verify runs the deferred-versus-automated-test equivalence check
- **THEN** the check finds the deferred task by reading tasks.md, and does not report "no deferred tasks" on the basis that plan.md contains no task rows

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

