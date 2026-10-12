# executor-governance-wording — Plan Contract

> **Execution for this change:** by the brainstorm Q4 ruling, this change's apply runs in the main
> session **without** `superpowers:subagent-driven-development` — a named, user-approved exception
> for this change only, not a supported execution mode. Independent review comes from external
> document review, diff checks and a full bridge verify; the retrospective records the deviation
> and the assurance not obtained under the rules this change writes (REQ-4). Each entry states
> what "done" means for one task, not how to get there.

**Goal:** Rewrite the bridge's executor governance from a tool ban into capability and assurance
language, move executing-plans' version facts into the Re-verification log, give a deliberately
skipped SDD a defined place (exception, disclosed in the retrospective), and release the result
as schema major 5 / bundle `5.0.0`.

**Pointers:** `specs/tdd-claim-accuracy/spec.md` (MODIFIED REQ-3, REQ-4); `specs/release-versioning/spec.md` (MODIFIED REQ-3, scenario S2 only); `design.md` (D1–D8;
D6 lists every README location and its disposition, D8 every version-coupled location).

**Global constraints (verbatim from the specs; every entry below is bound by them):**

- The exclusion rationale SHALL rest on the capability the bridge's apply requires, on every bridge-owned surface that explains why `superpowers:executing-plans` is not supported as an apply fallback: independent review during execution (after each task, or after each batch of small same-shape tasks, rather than only at the end).
- Each of them SHALL also state the current limitation: this version's apply requires subagent-driven-development, and when the required capability is missing apply stops at Step 0 instead of switching to executing-plans.
- The design surfaces above SHALL refer to the log for these facts rather than restate version-specific mechanism, so that an upstream change is recorded by adding to the log, not by rewriting the rationale. The CLAUDE.md red-flag list SHALL likewise refer to the log and is not required to restate those facts.
- Moving the facts to the log does not license an unsupported rationale: a surface that says executing-plans lacks the required capability SHALL say so only as the log's verified facts support. Dated entries already in the log stay as they are.
- No surface, the log included, SHALL rest the exclusion on what upstream recommends choosing between executors, and none SHALL state that executing-plans dispatches no independent reviewer at all — with a subagent tool it dispatches one for the final review.
- The rationale SHALL NOT use TDD as a differentiator between the two executors.
- Surfaces SHALL NOT describe plan.md task content as the carrier of that requirement — under the Plan Contract plan.md holds contract entries and no task list.
- Both surfaces SHALL name that option with the same text, `one-off — schema boundary case`; the template SHALL NOT qualify it as "no prevention possible", because the answer still states how unauthorised deviation, undisclosed gaps and untrue conformance claims are prevented.
- Neither surface SHALL present such a record as satisfying an assurance that was not obtained, as equivalent to subagent-driven-development, as conformance with the bridge's execution contract, or as making the path actually taken a supported execution mode.
- A ruling SHALL cover only the change it was made for. Neither surface SHALL treat an earlier ruling as precedent that authorises a later skip. When a similar skip has occurred in earlier cycles, the record SHALL state how many and where, and the pattern SHALL be raised as a §6 Promote candidate under the existing rule for skills skipped across multiple cycles.

---

## Task 1.1 — schema.yaml `description` states capability and limitation

- **Delivers:** the `description` value tells a reader why a subagent-capable platform is required in terms of the capability apply needs, states the current limitation, and points to the bridge README's Re-verification log for executing-plans' behaviour.
- **Acceptance:** the value names independent review during execution as the required capability; states that apply requires subagent-driven-development and that without it the user should use `spec-driven`; contains no per-version description of how executing-plans reviews (no "no reviewer per task", no "final review … by the author"); names the Re-verification log; `openspec schemas` still lists the schema.
- **Blocked by:** none
- **Interfaces:** names the log section produced by 3.2.

## Task 1.2 — apply instruction: capability rationale and three situations

- **Delivers:** apply step 2's fallback paragraph rests the exclusion on the required capability and the log, and is followed by the three situations of design D3.
- **Acceptance:** (a) the fallback paragraph meets the same capability / limitation / no-version-mechanism conditions as 1.1 and keeps the reasoning that TDD is not the differentiator because applicability and evidence are carried by the tasks.md annotations and the evidence contract; (b) the three situations are present: no subagent capability → Step 0 STOP (unchanged); SDD available → step 2 contract (unchanged); SDD available but deliberately not used under an explicit user ruling → an exception, not a supported mode, not to be called equivalent to SDD, stop if a required assurance cannot be provided, record per the skipped-skill rules; (c) Step 0's required-skill list and its STOP behaviour are unchanged; the only edit inside Step 0 is the one 1.5 makes.
- **Blocked by:** none
- **Interfaces:** the third situation points to the skipped-skill rules written in 1.3; names the log section produced by 3.2; the first situation agrees with Step 0 as corrected by 1.5.

## Task 1.3 — retrospective skipped-skill rules for a sanctioned SDD skip

- **Delivers:** the retrospective instruction tells the agent how the existing three questions are answered when `subagent-driven-development` is skipped under an explicit user ruling.
- **Acceptance:** the rules state each item of REQ-4's three-question guidance, the ruling-covers-this-change-only rule, the conditional prior-cases rule with the §6 Promote candidate, and the prohibition on presenting the record as an obtained assurance, SDD-equivalent, contract conformance or a supported mode; no new field, option or question is added; the option is named `one-off — schema boundary case`.
- **Blocked by:** none
- **Interfaces:** the same guidance appears in the template (2.1); the two must not state different rules. Referenced by 1.2's third situation.

## Task 1.4 — schema major 5

- **Delivers:** `schema.yaml` declares `version: 5`.
- **Acceptance:** line 2 reads `version: 5`; `openspec schema validate superpowers-bridge` passes and `openspec schemas` lists the schema after the dogfood copy is re-synced.
- **Blocked by:** none
- **Interfaces:** must agree with `VERSION` (4.1), the README version surfaces (3.3, 3.4), CLAUDE.md (5.2) and roadmap (4.4).

## Task 1.5 — Step 0 no longer points at a nonexistent manual fallback

- **Delivers:** apply Step 0 tells the user and agent what actually exists when a required skill is missing: STOP, then the user installs the skills or explicitly chooses the built-in `spec-driven` schema for this change.
- **Acceptance:** the sentence "explicitly opt into the manual fallback path described at the end of this instruction" is gone; Step 0 states that this schema has no internal manual fallback for apply, that switching to `spec-driven` is the user's explicit choice of a different workflow, and that the agent does not switch schemas or execution paths on its own; the required-skill list and the "If any required skill is missing, STOP and inform the user" sentence are unchanged.
- **Blocked by:** none
- **Interfaces:** agrees with 1.2's first situation (no subagent capability → Step 0 STOP) and with the README apply-phase fallback entry changed in 3.1.

## Task 2.1 — retrospective template guidance and option text

- **Delivers:** the template's `### Deliberately Skipped Skills` guidance carries the same sanctioned-SDD-skip answers as 1.3, and the `one-off` option's text matches the schema.
- **Acceptance:** the option reads exactly `one-off — schema boundary case` (no ", no prevention possible"); the guidance covers the same points as 1.3 without contradicting it; the option list keeps its five options; REQ-4's original prohibitions (no default all-✓, honest ✗ reasons allowed) still hold.
- **Blocked by:** none
- **Interfaces:** mirrors 1.3.

## Task 3.1 — English README rationale surfaces

- **Delivers:** every rationale location design D6 marks for change in `superpowers-bridge/README.md` states capability and limitation and refers to the Re-verification log; the apply section also places a deliberate SDD skip as an exception recorded in the retrospective.
- **Acceptance:** each D6 row marked for change is changed as D6 says and each row marked "不改" is byte-identical; none of those locations describes executing-plans' review mechanism per version; each link to the log points at the exact anchor of the heading produced by 3.2 and resolves.
- **Blocked by:** 3.2 (link target)
- **Interfaces:** links to the log section from 3.2; translated by 3.4; the apply-phase fallback entry agrees with Step 0 as corrected by 1.5.

## Task 3.2 — Re-verification log entry for executing-plans

- **Delivers:** one new documentation-only entry at the end of the Re-verification log holding executing-plans' review-structure facts and the versions and sources they were verified against.
- **Acceptance:** the entry opens with its own Markdown heading one level below `### Re-verification log` (the existing dated entries are bold paragraphs with no heading, so a bold paragraph alone does not satisfy this); the heading text contains no date or version, so its anchor stays stable when later entries are added; the entry states that executing-plans has no reviewer per task, reviews the whole branch once at the end, uses a fresh reviewer when a subagent tool exists and is author-performed without one, and loads `test-driven-development`; it cites the v6.4.1 `SKILL.md` at a fixed tag and the 2026-10-02 spike's v6.4.2 comparison; it states it does not move the baseline and that the design text refers to it; every existing dated entry and follow-up paragraph is byte-identical; no sentence says executing-plans dispatches no independent reviewer at all.
- **Blocked by:** none
- **Interfaces:** its heading is the link target for 3.1, 3.4 and 5.1, which link to that exact anchor; 1.1 and 1.2 name it in text.

## Task 3.3 — English README schema-major-5 surfaces

- **Delivers:** `superpowers-bridge/README.md` presents schema major 5 and bundle `5.0.0` consistently, with the reasons for the bump and the migration from v4.
- **Acceptance:** every README location in design D8's table is updated; "Why v4 → v5" names only the previously-valid-becomes-invalid criterion, states that the others do not apply, and records that keeping v4 because no check would block was rejected; "Migrating v4 → v5" limits the impact to retrospectives recording a sanctioned SDD skip written after the upgrade, says archived retrospectives are not rewritten, and gives rollback to tag `v4.0.0`; the Compatibility table has a v5 row above the v4 row whose first cell is `v5`, whose OpenSpec and Superpowers cells are `1.14.0` and `v5.1.0` each in a single pair of backticks, and whose date cell is plain `pending`, with an explanation below the table that it is an unrevalidated historical declaration; no sentence states that tag `v5.0.0` exists.
- **Blocked by:** none
- **Interfaces:** the v5 row's shape is read by 4.2; translated by 3.4; the version values must agree with 1.4, 4.1 and 5.2.

## Task 3.4 — Traditional Chinese README

- **Delivers:** `superpowers-bridge/README.zh-TW.md` carries the same changes as 3.1–3.3.
- **Acceptance:** every section changed in the English README has a changed counterpart with the same meaning, including a heading for the new log entry at the same level, whose anchor is the link target named in 3.2; the zh-TW Compatibility v5 row is identical in its backtick cells to the English one; no section changed in only one language.
- **Blocked by:** 3.1, 3.2, 3.3
- **Interfaces:** consumes 3.1–3.3; its zh-TW log heading is the link target named in 3.2; the version values must agree with 1.4 and 4.1.

## Task 4.1 — bundle version 5.0.0

- **Delivers:** `superpowers-bridge/VERSION` reads `5.0.0`.
- **Acceptance:** the file content is `5.0.0`.
- **Blocked by:** none
- **Interfaces:** must agree with 1.4, 3.3, 3.4.

## Task 4.2 — weekly version check reads the v5 row

- **Delivers:** `.github/workflows/version-check.yml`'s `Read pinned versions` step reads the v5 row.
- **Acceptance:** the grep key is `v5`; running that step's grep/awk locally against the edited README prints `1.14.0` and `v5.1.0`; after push, a `workflow_dispatch` run completes the step (recorded after push, outside this change's tasks).
- **Blocked by:** 3.3
- **Interfaces:** consumes the v5 row produced by 3.3; the grep key it uses is the one CLAUDE.md describes in 5.2.

## Task 4.3 — top-level README status

- **Delivers:** the bridges table in the top-level `README.md` and `README.zh-TW.md` shows `v5` in the Status column.
- **Acceptance:** line 11 of each file ends with `| v5 |`; nothing else in either file changes.
- **Blocked by:** none

## Task 4.4 — roadmap v5 section

- **Delivers:** `docs/roadmap.md` and `docs/roadmap.zh-TW.md` gain a v5 section describing this change, without a release label.
- **Acceptance:** each file has a v5 section placed after v4, consistent with the existing sections' content style, whose heading does not say "Released" / "已釋出"; the two files describe the same change.
- **Blocked by:** none
- **Interfaces:** the schema major it names must agree with 1.4.

## Task 5.1 — CLAUDE.md red flag

- **Delivers:** the executing-plans entry under 修 schema 時的紅旗 becomes a capability-and-assurance prohibition per design D5.
- **Acceptance:** the entry forbids adding to apply an execution path that lacks the required capability (independent review during execution) and is not legally degraded per formal design §5, forbids treating a degradation or deviation record as a satisfied assurance, states that this version supports SDD only, and refers to the bridge README's Re-verification log; it contains no version history (v5.1.0, v6.3.0, v6.4.1, 8/31), no "⚠️ 之後要改寫" sentence and no work-map task id; it does not use an upstream recommendation or TDD as the reason.
- **Blocked by:** 3.2 (link target)
- **Interfaces:** refers to the log section from 3.2.

## Task 5.2 — CLAUDE.md version descriptions

- **Delivers:** the CLAUDE.md places design D8 names describe schema major 5 and bundle `5.0.0`.
- **Acceptance:** the structure tree's `VERSION` note, the cross-file coupling row's grep key, the two-version-numbers table (`version: 5`, "需從目前的 5 bump") and the Compatibility row-key sentence all name v5 / 5.0.0; the v3 → v4 rollback SHA paragraph is unchanged.
- **Blocked by:** none
- **Interfaces:** must agree with 1.4, 3.3, 4.1, 4.2.

## Task 6.1 — structural validation

- **Delivers:** the edited bundle validates and loads.
- **Acceptance:** after re-syncing the dogfood copy, `openspec schema validate superpowers-bridge` passes, `openspec schemas` lists `superpowers-bridge`, and `openspec validate executor-governance-wording` reports the change valid; outputs are recorded in verify.
- **Blocked by:** 1.1, 1.2, 1.3, 1.4, 1.5, 2.1

## Task 6.2 — residue search

- **Delivers:** a recorded search showing the superseded statements and stale v4 references are gone from current documents.
- **Acceptance:** for each pattern searched (the REQ-3 superseded claims; `v4`, `version: 4`, `4.x.y`, `4.0.0`), every hit outside record locations (archive, handoff, poc, retrospectives, research) is listed with a keep/changed judgement and reason; no unjudged hit remains.
- **Blocked by:** 1.1–5.2

## Task 6.3 — three semantics unchanged

- **Delivers:** a recorded check, with locations cited, that the change did not alter the three behaviours.
- **Acceptance:** cites where it still holds that (1) without subagent capability apply stops at Step 0; (2) with SDD apply follows step 2's contract; (3) a deliberate-skip record is stated not to satisfy a required assurance — each with file and section.
- **Blocked by:** 1.2, 1.3, 1.5, 2.1

## Task 6.4 — weekly version check matches the released schema major

- **Delivers:** a recorded check that the weekly version check reads the row of the schema major this change releases, as the modified `release-versioning` REQ-3-S2 requires.
- **Acceptance:** records that `superpowers-bridge/schema.yaml` declares `version: 5`, that the `Read pinned versions` step in `.github/workflows/version-check.yml` targets the `v5` row, and that the Compatibility table has a `v5` row; runs that step's commands as extracted verbatim from the workflow file against the README and records the output `1.14.0` and `v5.1.0`; the record does not claim the check selects the newest row on its own.
- **Blocked by:** 1.4, 3.3, 4.2
- **Interfaces:** checks the outputs of 1.4 (schema major), 3.3 (v5 row) and 4.2 (row key) together.
