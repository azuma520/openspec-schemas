# task-prefixed-plan-headings — Plan Contract

> **For agentic workers:** Use superpowers:subagent-driven-development
> to implement this plan task-by-task. Each entry states what "done"
> means for one task, not how to get there — two executors may satisfy
> the same entry by different paths and both conform.

> **Heading form, deliberately ahead of the installed schema.** Every entry below is written `## Task <n> — …`, the canonical form this change introduces (design D7 point 3), so that upstream `task-brief` can extract entries during apply (task 4.2). The schema copy installed under `openspec/schemas/` is still v3, whose Plan Contract says an entry heading begins with the number; this plan departs from that wording on purpose. Its 1:1 check is meaningful only under the v4 check 12, available once task 4.1 re-syncs the copy, and verify runs after that. Do not "fix" these headings back to `## <n> —`. This plan has no non-entry `##` section, so no upstream extraction range runs into one.

**Goal:** Make plan entries written as `## Task <n> — …` recognisable both by verify's check 12 and by upstream Superpowers `task-brief`, keep `## <n> — …` valid with no scheduled removal, and release the result as schema major 4 / bundle `4.0.0` with version claims that point only at things that exist.

**Pointers:** [`specs/plan-contract/spec.md`](./specs/plan-contract/spec.md) (REQ-4), [`specs/release-versioning/spec.md`](./specs/release-versioning/spec.md) (REQ-1–REQ-4); [`design.md`](./design.md) for decisions D1–D8, the fixture table (D7), the coupled-file list (D8), the risks and the migration plan. The v4.0.0 tag is a post-archive close-out on the work-map record (D6), not an entry here.

**Global constraints (verbatim from the specs; every entry below is bound by them):**

- "The entry KEY SHALL be the entry number only: `Task` identifies the canonical form and is not part of the key, so `## Task 1.1 …` and `## 1.1 …` carry the same key `1.1`, and a plan holding both carries a repeated key that REQ-1's first stage blocks."
- "Both forms SHALL remain accepted with no scheduled removal of the legacy form; the canonical form is the recommended form for new or edited plans, and mixing the two forms in one plan is legal."
- "Tilde fences (`~~~`) and indented fences SHALL NOT delimit a block for this purpose. An unclosed block SHALL NOT produce a separate finding; entries after its opening line are simply not collected, and REQ-1's second stage reports the resulting missing keys."
- "REQ-1's two stages, their non-short-circuiting and their messages SHALL stay as they are; tasks.md task-number collection, including its treatment of code blocks, SHALL stay as it is; and the contract-identity check SHALL keep counting heading-shaped lines inside code blocks"
- "The guidance SHALL claim only that canonical entries are recognisable by that extractor, never that its extracted range is correct, and SHALL NOT state that the extractor accepts only the canonical form."
- "Releases before `4.0.0` are out of scope: they carry no tags, and none SHALL be created for them retroactively"
- "Until such a run exists the cell SHALL hold `pending` as plain text, and a run against versions other than those listed in the row SHALL NOT be grounds to fill it."
- "Rollback instructions written by this change or any later change SHALL reference only a tag or commit that exists in the repository."

Binding non-goals carried from design.md: upstream Superpowers and the OpenSpec CLI are not modified; check 13's decisions do not change; tasks.md parsing does not change; the Compatibility Superpowers baseline value stays `v5.1.0`; no `v3.0.0` tag is created; the v1 → v2 and v2 → v3 rollback texts are not rewritten; the adopters fragment is not touched.

---

## Task 1.1 — RED→GREEN fixtures for check 12

- **Delivers:** Three new self-contained fixture directories after `f13` — fence exclusion, Task-form recognition, Task/legacy same key — each with a tasks.md and plan.md that differ from a conforming pair in exactly one way.
- **Acceptance:** Each directory matches its D7 table row (contents, tasks set); a reader who did not write them can name the single defect in each; no fixture also exercises a second rule (D7: "one fixture, one defect").
- **Blocked by:** none
- **Interfaces:** Produces the fixture directory names that task 1.3 tabulates and task 2.2 uses as the left side of its `subject:` values.

## Task 1.2 — Breaking-change, regression and positive-control fixtures

- **Delivers:** The non-RED fixtures: `## Task 3` reread as an entry; `##1.1` / ` ## 1.1` no longer an entry; the near-miss forms (one fixture or one per form, chosen and recorded here); the combined Task-plus-fence positive control.
- **Acceptance:** The column-0 / whitespace fixture is separate from the near-miss fixture; each fixture's v3 and v4 verdicts can be derived by hand from the respective wording and match the D7 table; the split decision for near-miss forms is stated in task 1.3's README rows.
- **Blocked by:** none
- **Interfaces:** Produces the fixtures task 2.5 runs and task 1.3 tabulates.

## Task 1.3 — Fixtures README rows and blind re-run note

- **Delivers:** The fixtures README gains one row per new fixture with v3 and v4 expected verdicts and its kind (RED→GREEN, breaking change, regression, positive control), and its re-run note says single fixtures are delivered without the README.
- **Acceptance:** Every new fixture directory has exactly one row and every new row has a directory; the expected verdicts agree with design D7; the re-run note names the README as material the executing agent must not see.
- **Blocked by:** 1.1, 1.2
- **Interfaces:** Holds the frozen expectations that tasks 2.2 and 2.5 compare against.

## Task 2.1 — Plan Contract states the v4 entry rule

- **Delivers:** The `plan` instruction's Plan Contract defines entries positively per REQ-4, restates why the key leads (only the fixed word `Task` may precede it), states the fence semantics, and carries the three `task-brief` guidance sentences plus the canonical-form recommendation.
- **Acceptance:** Every condition in REQ-4's first paragraph appears in the Plan Contract; the old negative wording "does not begin with a number is not an entry" is gone; the guidance claims recognition only and contains no "upstream accepts only" phrasing; a reader comparing it with task 2.2's check 12 text finds no rule stated in one and contradicted in the other.
- **Blocked by:** none
- **Interfaces:** Must agree with task 2.2 — check 12 says it "introduces nothing of its own" beyond what the Plan Contract requires, so the two texts define the same set of entries.

## Task 2.2 — Check 12 collects keys by the v4 rule

- **Delivers:** Check 12's ENTRY KEY collection implements REQ-4: canonical and legacy forms, column-0 `##` plus whitespace, the line-by-line backtick toggle, no unclosed-fence finding, tasks side stated as unchanged; stages, non-short-circuiting and messages untouched.
- **Acceptance:** RED/GREEN records in tasks.md for each of the three task-1.1 fixtures meet the four boundaries in the tasks.md header, with RED captured against the pre-edit wording before the edit; the diff outside the ENTRY KEY collection paragraph and the added rationale is empty; the frozen expectation in the fixtures README equals each GREEN verdict.
- **Blocked by:** 1.1, 1.3
- **Interfaces:** Consumes the task-1.1 fixtures and task-1.3 expectations; its wording is the v4 reading that task 2.5 runs and that verify uses after task 4.1.

## Task 2.3 — Asymmetry rationale in checks 12 and 13

- **Delivers:** Both checks state why check 12 skips backtick-fenced headings and check 13 deliberately counts them.
- **Acceptance:** Each check carries the rationale; check 13's diff is that addition and nothing else; the two statements do not contradict each other or REQ-4.
- **Blocked by:** 2.2

## Task 2.4 — Schema major 4

- **Delivers:** `superpowers-bridge/schema.yaml` declares `version: 4`.
- **Acceptance:** The file reads `version: 4` and `openspec schema validate` passes in task 4.1.
- **Blocked by:** none
- **Interfaces:** The commit that first lands this line is the commit whose parent task 3.8 records.

## Task 2.5 — v4 verdicts for the non-RED and existing check-12 fixtures

- **Delivers:** Recorded blind-protocol runs of the task-1.2 fixtures and of `f5`, `f8`, `f9` against the v4 wording, each with intermediate values and actual verdict beside the frozen expectation.
- **Acceptance:** Every actual verdict equals the README's v4 expectation; the combined positive control yields keys exactly `1.1, 1.2`; any mismatch is recorded and returns work to task 2.2 rather than being explained away.
- **Blocked by:** 1.2, 1.3, 2.2
- **Interfaces:** Consumes task 2.2's wording and the task-1.2 / task-1.3 material.

## Task 3.1 — Plan template uses the canonical form

- **Delivers:** `templates/plan.md` shows `## Task 1.1 —`, `## Task 1.2 —`, `## Task 2.1 —`, and its comment explains the fixed `Task` prefix is accepted and is not part of the key.
- **Acceptance:** No example heading keeps the legacy form; the comment does not contradict REQ-4 or task 2.1's Plan Contract; the example key set still matches `templates/tasks.md`.
- **Blocked by:** 2.1

## Task 3.2 — Bundle version 4.0.0

- **Delivers:** `superpowers-bridge/VERSION` reads `4.0.0`.
- **Acceptance:** The file content is exactly `4.0.0` and agrees with every README and CLAUDE.md mention of the current bundle.
- **Blocked by:** none

## Task 3.3 — Bridge README (en) reflects v4

- **Delivers:** Every README location named in design D8, updated: v3 → v4 migration with its three exceptions and rationale, Known breaking changes, Versioning table and current-release sentence in rule form, Compatibility v4 row and its below-table note, S11 and its follow-up paragraphs.
- **Acceptance:** No sentence claims a tag exists (REQ-2); the v4 row's date cell is `pending` and its Superpowers cell is a single backtick-wrapped `v5.1.0` with the explanation below the table (REQ-3); the migration text names all three exceptions and states the repo was scanned; a doc review finds no contradiction with design D6/D8.
- **Blocked by:** 2.4, 3.2
- **Interfaces:** Produces the Compatibility v4 row that task 3.5 reads and the rollback placeholder location task 3.8 fills; task 3.4 mirrors it.

## Task 3.4 — Bridge README (zh-TW) mirrors 3.3

- **Delivers:** The zh-TW README carries the same v4 changes as task 3.3.
- **Acceptance:** Section by section, every change in task 3.3 has a counterpart with the same facts (versions, dates, exceptions, rule wording); the Compatibility table rows are identical.
- **Blocked by:** 3.3

## Task 3.5 — Weekly version check reads the v4 row

- **Delivers:** `version-check.yml`'s `Read pinned versions` step selects the `v4` row.
- **Acceptance:** Running that step's selection commands locally against the edited README prints the v4 row's OpenSpec and Superpowers versions; after push, a `workflow_dispatch` run reads the same two values.
- **Blocked by:** 3.3
- **Interfaces:** Consumes the README row shape produced by task 3.3.

## Task 3.6 — Repo CLAUDE.md reflects v4 and the release rule

- **Delivers:** The CLAUDE.md places design D8 names: structure-tree note, two-version-numbers table (release commit definition, practised from 4.0.0), cross-file coupling row corrected to "a kept old row is read silently".
- **Acceptance:** No remaining text in those places says schema major 3 or bundle `3.x.y` is current; the coupling row no longer claims CI fails when a new row is added above a kept old one; a doc review finds no contradiction with design D6.
- **Blocked by:** 2.4, 3.2

## Task 3.7 — Roadmap v4 section

- **Delivers:** `docs/roadmap.md` and `docs/roadmap.zh-TW.md` each gain a v4 "Released" section in the style of the v2 and v3 sections.
- **Acceptance:** Both name schema major 4, bundle `4.0.0`, the Task form and the code-block behaviour change, and agree with each other.
- **Blocked by:** none

## Task 3.8 — v3 → v4 rollback points at a real commit

- **Delivers:** Both READMEs name the full SHA of the parent of the first commit setting `version: 4` as the v3 → v4 rollback.
- **Acceptance:** Checking that SHA out yields `superpowers-bridge/schema.yaml` with `version: 3`; the SHA is identical in both READMEs; no placeholder text remains anywhere in the repo for it.
- **Blocked by:** 2.4, 3.3, 3.4
- **Interfaces:** Consumes the commit produced when task 2.4's edit is first committed (needs a user-authorised commit mid-apply).

## Task 4.1 — Installed copy re-synced and structurally valid

- **Delivers:** `openspec/schemas/superpowers-bridge/` equals the source bundle, and the bundle passes structural validation.
- **Acceptance:** A recursive diff between source and copy is empty; `openspec schema validate superpowers-bridge` and `openspec schemas` succeed in a throwaway project and their output is recorded.
- **Blocked by:** 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.8

## Task 4.2 — Upstream task-brief extracts this plan's entries

- **Delivers:** A recorded run of the loaded upstream `task-brief` on this plan.md, with the Superpowers version and script path.
- **Acceptance:** For at least one non-final entry, the extracted brief is line-for-line identical to that entry in this file (a return code of 0 alone does not count); the final entry's result is recorded, including any trailing text it swallows, as a known upstream limitation.
- **Blocked by:** none
