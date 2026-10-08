# plan-contract

## Purpose

Define what a `superpowers-bridge` plan.md is: a per-task execution contract that specifies
*what must be true* rather than *which steps to take*. Two competent executors may reach the
same acceptance criteria by different paths without either being non-conforming. Established
by change `loosen-plan` (2026-09-04), which replaced the micro-step plan format.
## Requirements
### Requirement: REQ-1 Plan is a per-task execution contract

`superpowers-bridge` plan.md SHALL consist of a header (goal; pointers to the change's specs/ and design.md; global constraints copied verbatim from the specs) and exactly one contract entry per tasks.md task, keyed by the tasks.md task number. Each entry SHALL state: what it delivers (end-to-end behaviour, not a layer-by-layer implementation list); acceptance criteria that are concrete and verifiable; and its blocking dependencies (or an explicit "none"). Interfaces (consumed/produced names and shapes) SHALL be stated for tasks that couple with other tasks and MAY be omitted for tasks with no cross-task coupling.

The correspondence between tasks.md task numbers and plan.md entry keys SHALL be one-to-one, and the deterministic verify check SHALL establish it in two stages: first that neither side contains a duplicate key, then that the two key sets are equal in both directions. Set equality alone is insufficient — a duplicate collapses in a set, so two tasks numbered `1.1` against one plan entry keyed `1.1` would compare equal while one task holds no contract entry of its own. A duplicate on either side SHALL be reported as a blocking finding naming the repeated key, distinctly from a missing or extra key, because the two are different defects with different repairs.

plan.md SHALL NOT carry task-level state markers (deferral and the like); tasks.md is their carrier. Any deterministic check concerning task state SHALL therefore read tasks.md, and a check that searches plan.md for task rows is non-conforming — under this contract plan.md holds contract entries, never a task list, so such a check can never fire.

#### Scenario: REQ-1-S1 Conforming plan entry

- **WHEN** a plan.md entry for a coupled task states delivered behaviour, verifiable acceptance criteria, blocking dependencies, and its cross-task interfaces
- **THEN** the entry conforms to the Plan Contract

#### Scenario: REQ-1-S2 Task ID set cross-check

- **WHEN** verify runs on a change where the set of tasks.md task numbers and the set of plan.md entry keys differ in either direction (a task with no plan entry, or a plan entry keyed to no task — including the equal-count case such as tasks `{1,2,3}` vs plan `{1,2,9}`)
- **THEN** each missing or extra key is reported as a blocking finding

#### Scenario: REQ-1-S3 Duplicate task number blocks

- **WHEN** tasks.md contains two task lines both numbered `1.1` and plan.md contains exactly one entry keyed `1.1`
- **THEN** verify reports a blocking finding naming the repeated task number `1.1`, and does not pass the change on the grounds that the two key sets are equal

#### Scenario: REQ-1-S4 Duplicate plan entry key blocks

- **WHEN** plan.md contains two `##` contract entries whose keys are both `2.3`
- **THEN** verify reports a blocking finding naming the repeated entry key `2.3`, on the same terms as a duplicate on the tasks side

#### Scenario: REQ-1-S5 Unique keys and equal sets pass

- **WHEN** every tasks.md task number occurs once, every plan.md entry key occurs once, and the two sets are equal
- **THEN** the one-to-one check passes

#### Scenario: REQ-1-S6 Deferral marker is read from tasks.md

- **WHEN** a task is marked deferred in tasks.md and verify runs the deferred-versus-automated-test equivalence check
- **THEN** the check finds the deferred task by reading tasks.md, and does not report "no deferred tasks" on the basis that plan.md contains no task rows

#### Scenario: REQ-1-S7 Uncoupled task omits interfaces

- **WHEN** a task has no consumer or producer relationship with any other task and its plan entry omits the interfaces block
- **THEN** the entry still conforms (interfaces are conditionally required, not unconditional)

### Requirement: REQ-2 No step prescription

The plan artifact instruction SHALL NOT require micro-step decomposition, exact file paths, code snippets, commit points, or any fixed execution sequence. A decision-rich snippet (state machine, schema, type shape) MAY be included where it encodes a decision more precisely than prose. Vague acceptance language that cannot be verified (e.g. "works correctly", "handles errors appropriately") is non-conforming.

#### Scenario: REQ-2-S1 Two implementations both conform

- **WHEN** two executors implement the same plan entry by different paths and both satisfy its acceptance criteria
- **THEN** neither is non-conforming for having deviated from any step sequence, because no step sequence is prescribed

#### Scenario: REQ-2-S2 Vague acceptance criterion rejected

- **WHEN** a plan entry's acceptance criterion is "feature works correctly" with no verifiable condition
- **THEN** plan self-review or artifact review flags the entry as non-conforming

### Requirement: REQ-3 Producer is agent direct generation

The schema SHALL NOT require invoking any skill to produce plan.md; the agent generates it directly from tasks.md, design.md, and the change's specs. `superpowers:writing-plans` SHALL NOT be a normative dependency of the plan artifact and SHALL NOT have a plan-artifact PRECHECK, but its use as an optional decomposition aid is not prohibited; its micro-step output does not define plan.md's normative format.

#### Scenario: REQ-3-S1 Plan produced without any skill

- **WHEN** an agent produces plan.md directly from the change artifacts on a platform without the Superpowers writing-plans skill
- **THEN** the plan artifact completes without a PRECHECK failure

#### Scenario: REQ-3-S2 Optional aid does not change the format

- **WHEN** an executor uses writing-plans as a private decomposition aid and then writes plan.md
- **THEN** plan.md must still conform to the Plan Contract shape, not the micro-step format

### Requirement: REQ-4 Plan entry headings are recognised by a positive rule

A line of `superpowers-bridge` plan.md SHALL be a contract entry if and only if all of the following hold:

1. it is not inside a fenced code block as defined below;
2. it begins at column 0 with exactly `##` followed by at least one space or tab (`###` and deeper remain sub-headings inside an entry);
3. the text after that whitespace is either the canonical form — the literal word `Task`, case-sensitive, then at least one space or tab, then an entry number — or the legacy form — an entry number alone;
4. the entry number matches `\d+(\.\d+)*` and is followed by whitespace or the end of the line.

Every other `##` heading SHALL be a non-entry section. The entry KEY SHALL be the entry number only: `Task` identifies the canonical form and is not part of the key, so `## Task 1.1 …` and `## 1.1 …` carry the same key `1.1`, and a plan holding both carries a repeated key that REQ-1's first stage blocks. Both forms SHALL remain accepted with no scheduled removal of the legacy form; the canonical form is the recommended form for new or edited plans, and mixing the two forms in one plan is legal.

For entry recognition only, a fenced code block SHALL be delimited by lines whose first three characters are three backticks at column 0: each such line toggles the block state, and neither the toggling line nor any line inside the block can be an entry. Tilde fences (`~~~`) and indented fences SHALL NOT delimit a block for this purpose. An unclosed block SHALL NOT produce a separate finding; entries after its opening line are simply not collected, and REQ-1's second stage reports the resulting missing keys.

This requirement changes only which plan.md lines yield entry keys. REQ-1's two stages, their non-short-circuiting and their messages SHALL stay as they are; tasks.md task-number collection, including its treatment of code blocks, SHALL stay as it is; and the contract-identity check SHALL keep counting heading-shaped lines inside code blocks, because it is a deliberately conservative line-by-line count that does not recognise Markdown structure and blocks when its count disagrees with the OpenSpec CLI's — the asymmetry with this requirement is deliberate and both checks SHALL state its reason.

The plan instruction SHALL carry the following guidance for plans handed to the upstream Superpowers `task-brief` extractor, and none of it SHALL be enforced by verify: use the canonical form for every entry; do not begin a non-entry `##` heading with `Task` followed by a number; place non-entry sections before the first entry. The guidance SHALL claim only that canonical entries are recognisable by that extractor, never that its extracted range is correct, and SHALL NOT state that the extractor accepts only the canonical form.

#### Scenario: REQ-4-S1 Canonical entry is recognised

- **WHEN** plan.md holds `## Task 1.1 — Login` and `## Task 1.2 — Logout` and tasks.md holds tasks `1.1` and `1.2`
- **THEN** the collected entry keys are `1.1` and `1.2` and the one-to-one check passes

#### Scenario: REQ-4-S2 Legacy entry is still recognised

- **WHEN** plan.md holds `## 1.1 — Login` and `## 1.2 — Logout` and tasks.md holds tasks `1.1` and `1.2`
- **THEN** the collected entry keys are `1.1` and `1.2` and the one-to-one check passes

#### Scenario: REQ-4-S3 Canonical and legacy with the same number are a duplicate

- **WHEN** plan.md holds both `## Task 1.1 — A` and `## 1.1 — B` and tasks.md holds task `1.1`
- **THEN** verify reports `1.1` as occurring more than once in plan.md and blocks

#### Scenario: REQ-4-S4 Heading inside a backtick fence is not an entry

- **WHEN** plan.md holds `## 1.1`, then a column-0 backtick fence containing `## 9.9`, then `## 1.2`, and tasks.md holds tasks `1.1` and `1.2`
- **THEN** the collected entry keys are `1.1` and `1.2` only and the one-to-one check passes

#### Scenario: REQ-4-S5 Tilde and indented fences do not hide headings

- **WHEN** plan.md holds a column-0 `##` entry heading between a `~~~` opening and closing line, or between a backtick opening and closing line that are both indented
- **THEN** that heading is collected as an entry exactly as if no fence surrounded it

#### Scenario: REQ-4-S6 Near-miss forms are not entries

- **WHEN** plan.md holds `## task 1.1`, `### Task 1.1`, `## Task 1.1a`, `## Tasks 1.1`, `## Task1.1`, `##1.1` or ` ## 1.1` (leading space), and tasks.md holds task `1.1`
- **THEN** none of those headings yields an entry key and verify reports `1.1` as a task with no entry

#### Scenario: REQ-4-S7 A non-entry beginning with Task and a number becomes an entry

- **WHEN** plan.md holds `## 1.1 — Login` and a section headed `## Task 3 notes`, and tasks.md holds only task `1.1`
- **THEN** `3` is collected as an entry key and verify reports it as an entry keyed to no task

#### Scenario: REQ-4-S8 Unclosed fence surfaces as missing keys

- **WHEN** plan.md holds `## Task 1.1`, then a backtick fence that is never closed, then `## Task 1.2`, and tasks.md holds tasks `1.1` and `1.2`
- **THEN** verify reports `1.2` as a task with no entry, and reports no separate unclosed-fence finding

#### Scenario: REQ-4-S9 Mixed forms pass without guidance enforcement

- **WHEN** plan.md mixes `## Task 1.1 — A` and `## 1.2 — B`, places a self-review section after the last entry, and tasks.md holds tasks `1.1` and `1.2`
- **THEN** the one-to-one check passes, because the extractor guidance is not enforced by verify

#### Scenario: REQ-4-S10 Contract-identity counting ignores the fence rule

- **WHEN** a delta spec holds a `### Requirement:` line inside a column-0 backtick fence
- **THEN** the contract-identity check still counts that line, and its existing block on a count disagreeing with the CLI's applies unchanged

