## ADDED Requirements

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
