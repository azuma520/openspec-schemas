# Roadmap

[English](./roadmap.md) · [繁體中文](./roadmap.zh-TW.md)

This repository is actively maintained as a side project. The roadmap below sketches what's planned but isn't a contract — items can shift based on what real usage surfaces.

## v1 — Released

- [x] **`superpowers-bridge`** — bridges OpenSpec ↔ obra/superpowers + native `retrospective` artifact

## v2 — Released

- [x] **Plan Contract + TDD evidence contract** — replaced the step-prescribing `plan` artifact with a per-task execution contract (what "done" means, not how to get there); TDD applicability (`TDD: applicable` / `TDD: n/a — <reason>`) and RED/GREEN records now travel with `tasks.md`, checked by verify for presence and structure only, not enforced as a non-bypassable gate (schema major 2, bundle 2.0.0)

## v3 — Released

- [x] **Contract identity (Requirement / Scenario stable IDs)** — every Requirement and Scenario heading now carries a stable, machine-referenceable ID (`### Requirement: <REQ-ID> <description>` / `#### Scenario: <REQ-ID>-S<m> <description>`) that survives a rewording; new-ID allocation follows a fixed rule. Verify's new check 13 deterministically judges the change's post-archive candidate state for missing/duplicate/misplaced IDs, cross-checked against the OpenSpec CLI's JSON (schema major 3, bundle 3.0.0). This is the identity layer only — a `Contracts:` annotation on tasks, a verification-results ledger, and an executable (non-bypassable) gate stay out of scope for later changes.

## v4 — Released

- [x] **Task-prefixed plan entry headings** — a `plan.md` entry may now be written in the canonical form `## Task <number> — <title>`, which Superpowers' `task-brief` extractor recognises; the legacy form `## <number> — <title>` stays accepted, with no scheduled removal, and `Task` is not part of the key (schema major 4, bundle 4.0.0). Entries are defined by a positive rule, and verify's check 12 no longer collects `##` heading-shaped lines inside a column-0 backtick fenced code block. Two other behaviour changes come with the rule: a non-entry column-0 `##` heading of the form `Task <number>` (the word `Task`, one or more spaces or tabs, then a number matching `\d+(\.\d+)*` followed by whitespace or the end of the line) becomes an entry, and `##1.1` or an indented ` ## 1.1` is no longer one. Canonical entries become recognisable by `task-brief`; this does not make the range it extracts for an entry correct.

## v1.x — In follow-up backlog

These items are tracked in `~/.claude/plans/pr-quizzical-oasis.md` (the implementation plan):

- [ ] **`workflow-retrospective` skill packaging** — currently the retrospective procedure is embedded in the schema instruction (Decision 3). If real users need to invoke `/workflow-retrospective` interactively (outside the schema flow), repackage as a Claude Code plugin
- [ ] **End-to-end CI integration test** — current CI only runs `openspec schema validate`. A round-trip test (`/opsx:new` through `/opsx:archive`) would catch regressions but requires Superpowers in CI
- [ ] **Verify artifact 5 polish points** — listed in v1.1 backlog A (templates clarity, design optional handling, worktree origin, pass criteria, TDD note)

## Awaiting OpenSpec core

These cannot be solved in a community schema:

- [ ] **`requires_skills:` schema field** — would replace the prompt PRECHECKs with engine-validated declarations
- [ ] **`post_apply` phase** — would let `verify` and `retrospective` be true post-apply hooks instead of artifacts with timing-mismatch (analogous to spec-kit's `after_implement`)

## Future bridge candidates

When real demand surfaces:

- [ ] **`obra-bridge`** — broader integration with other obra/* tools (if the user community grows)
- [ ] **Domain-specific schemas** — e.g., a `data-pipeline` schema variant with stronger schema-validation artifacts

Want to suggest a bridge? Open an issue at <https://github.com/azuma520/openspec-schemas/issues>.
