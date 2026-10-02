# Retrospective skill inventory — Plan Contract

> **For agentic workers:** Use superpowers:subagent-driven-development
> to implement this plan task-by-task. Each entry states what "done"
> means for one task, not how to get there — two executors may satisfy
> the same entry by different paths and both conform.

**Goal:** Make the retrospective §4 skill inventory follow one definition: the template lists exactly the six items `tdd-claim-accuracy` REQ-5 names (no `writing-plans`), and the schema's retrospective instruction states the same two-class criterion instead of "apply phase".

**Pointers:** `specs/tdd-claim-accuracy/spec.md` (REQ-5 and scenarios REQ-5-S1..S4); `design.md` (D1–D6, especially D3 on what the schema and the template each carry).

**Global constraints (verbatim from the specs; every entry below is bound by them):**

- The retrospective skill-compliance section (§4) SHALL inventory exactly two classes of items: (1) Superpowers skills the superpowers-bridge workflow explicitly requires invoking — `brainstorming` (required by the `brainstorm` artifact) and the skills required by apply pre-flight (`using-git-worktrees`, `subagent-driven-development`, `finishing-a-development-branch`); and (2) Superpowers disciplines the schema requires to be carried out and whose execution the retrospective must record, even though the schema does not invoke them directly — `test-driven-development` (carried by the tasks.md TDD annotations and RED/GREEN evidence) and `requesting-code-review` (structural via subagent-driven-development).
- A skill the schema names only as an optional aid, and that carries none of the class (2) disciplines, MUST NOT be listed on the grounds that it may be useful; `superpowers:writing-plans` is such a skill.
- This requirement is the normative owner of the criterion and of the six-item inventory above. The retrospective instruction in `superpowers-bridge/schema.yaml` SHALL state the two-class criterion to the agent, and `superpowers-bridge/templates/retrospective.md` SHALL present exactly the six rows above. Both the schema instruction and the template MUST NOT state a second, different definition of what §4 lists. When the inventory changes, this requirement changes first and the schema and template follow it.
- This requirement governs which rows the inventory contains. It does not change how a row is filled: the conditional and structural labels on the TDD and code-review rows, the skipped-skill rules, and REQ-4's prohibition on default all-✓ attestation stay as they are. A row may still be filled as not yet done when its skill runs after the retrospective is written (for example `finishing-a-development-branch`, which runs after archive).

---

## 1.1 — Template §4 presents the six REQ-5 rows

- **Delivers:** A retrospective generated from the template carries a §4 table whose rows are exactly the six REQ-5 items, and a note stating the two-class definition.
- **Acceptance:**
  - The §4 table in `superpowers-bridge/templates/retrospective.md` has exactly six skill rows, naming `brainstorming`, `using-git-worktrees`, `subagent-driven-development`, `test-driven-development`, `requesting-code-review` and `finishing-a-development-branch`; no row names `writing-plans` (REQ-5-S1, S2, S3).
  - The TDD and code-review row labels, the existing note on conditional/structural rows, and the `### Deliberately Skipped Skills` subsection are unchanged from the pre-change template (a diff of the file touches no line of them).
  - The §4 text states the two classes (required invocations; required disciplines not invoked by the schema) and contains no wording that describes §4 as the apply phase only or by any other definition (REQ-5-S4).
  - No other section of the template changes.
- **Blocked by:** none
- **Interfaces:** shares the two-class criterion with 1.2 — the template note and the schema instruction must describe the same two classes and the same exclusion of optional aids; 1.2 is the other end. Produces the edited template that 2.2 checks the CLI delivers.

## 1.2 — Schema §4 instruction states the two-class criterion

- **Delivers:** An agent writing a retrospective is told by the schema which items §4 inventories, by the same two-class criterion the template presents.
- **Acceptance:**
  - The retrospective instruction's §4 item in `superpowers-bridge/schema.yaml` no longer says "this schema's apply phase"; it states class (1) as the skills the workflow requires invoking (identifiable by where the schema requires them: the `brainstorm` artifact and apply pre-flight), class (2) as the TDD and code-review disciplines, and that skills named only as optional aids (e.g. `writing-plans`) are not listed (REQ-5-S4).
  - The "Skipped-skill rules for §4" text and every other part of the schema are unchanged (a diff of the file touches only the §4 item).
  - `openspec schema validate superpowers-bridge` passes on a copy of the edited bundle.
- **Blocked by:** none
- **Interfaces:** shares the two-class criterion with 1.1 (the other end); produces the instruction text that 2.2 checks the CLI delivers.

## 2.1 — README consistency recorded

- **Delivers:** A recorded finding on whether the bridge README (en and zh-TW) says anything about what retrospective §4 lists that conflicts with REQ-5.
- **Acceptance:**
  - Both `superpowers-bridge/README.md` and `superpowers-bridge/README.zh-TW.md` were searched in full for statements about the retrospective skill-compliance section and about `writing-plans`; each hit is listed with its location and a conflict / no-conflict verdict against REQ-5.
  - If no hit conflicts, neither README is modified. If one conflicts, the conflict is reported to the user before any README edit is made.
  - The finding is recorded where the verify artifact can cite it.
- **Blocked by:** none

## 2.2 — CLI delivers the new §4 text

- **Delivers:** The dogfood copy the OpenSpec CLI reads in this repo matches the edited bridge, and the retrospective instructions it hands an agent carry the new §4 criterion.
- **Acceptance:**
  - `openspec/schemas/superpowers-bridge/` is identical to `superpowers-bridge/` (`diff -r` reports no difference).
  - `openspec schema validate superpowers-bridge` passes and `openspec validate retro-skill-inventory --strict` reports the change valid.
  - The output of `openspec instructions retrospective --change retro-skill-inventory` contains the new §4 criterion text from 1.2 and does not contain "this schema's apply phase"; its template section shows the six-row table from 1.1 with no `writing-plans` row.
- **Blocked by:** 1.1, 1.2
- **Interfaces:** consumes the edited template from 1.1 and the edited instruction text from 1.2.
