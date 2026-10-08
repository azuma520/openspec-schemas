<!--
Task numbers are the plan.md entry keys (check 12: unique on both sides, then
equal sets). This change's own plan.md writes every entry as `## Task <n> …`
(design D7 point 3), so the 1:1 check that verifies this file is the new v4
reading — available only after 4.1 syncs the schema copy.

Order follows design.md § Migration Plan, with the same deliberate inversion
`fix-v2-blocking-defects` used: fixtures come FIRST, because a RED record for
a checker edit is "the fixture gets the wrong verdict under the pre-edit
wording", and that can only be captured before the wording changes.

TDD applicability, as read for this change (same reading as
`fix-v2-blocking-defects`, ruled 2026-09-07): check 12 is agent-executed
instruction prose; what makes its edit `applicable` is that the mutation
fixtures are its test — the same re-runnable case shows the v3 wording
reaching the wrong verdict before the edit and the v4 wording reaching the
right one after it. The `subject:` is `<fixture dir>::<expected v4 verdict>`.
Boundaries every RED/GREEN record under 2.2 must satisfy:

  1. RED is obtained by actually running the fixture against the PRE-edit
     wording, before 2.2 edits it. "v3 would have failed" written after the
     edit is not a RED.
  2. RED and GREEN bind the same subject, character for character.
  3. `failure:` states EXPECTED vs ACTUAL verdict. BLOCK is the correct v4
     verdict for some fixtures, so neither BLOCK nor PASS is automatically
     RED or GREEN — the direction is per fixture.
  4. The executing agent sees only that fixture's plan.md / tasks.md, copied
     somewhere the fixtures README is not, and reports intermediate values
     (plan keys, tasks keys, repeats, set differences) before its verdict is
     compared with the frozen expectation (design D7 point 2).

Name this evidence for what it is — instruction-layer behavioural
verification, agent-executed — never an automated test run.

Not in this file, by design (D6): creating, pushing and remotely confirming
the `v4.0.0` tag. It happens after archive, so it is carried by the work-map
record `task-20261002-task-brief-heading-compat`, which stays DOING until the
remote peeled tag equals the release commit.
-->

## 1. Mutation fixtures — one defect each, written before any schema edit

- [x] 1.1 Add the three RED→GREEN fixtures under `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/`, numbering after `f13`: fence exclusion (plan `## 1.1`, a column-0 backtick fence holding `## 9.9`, `## 1.2`; tasks `{1.1, 1.2}`), Task-form recognition (plan `## Task 1.1`, `## Task 1.2`; tasks `{1.1, 1.2}`), and Task/legacy same key (plan `## Task 1.1` and `## 1.1`; tasks `{1.1}`). Each is a self-contained tasks.md + plan.md pair with everything else conforming
  - TDD: n/a — test material for 2.2, not code under test; its correctness is shown by 2.2's RED/GREEN records
- [x] 1.2 Add the fixtures that are not RED→GREEN: the two breaking-change fixtures (`## Task 3 notes` reread as an entry; `##1.1` / indented ` ## 1.1` no longer an entry — kept separate from the near-miss fixture because their v3 verdicts differ), the near-miss regression fixture (`## task 1.1`, `### Task 1.1`, `## Task 1.1a`; one fixture or one per form, decided here — design Open Question), and the combined positive control (Task form plus a fenced `## Task 9.9`, v4 keys exactly `1.1, 1.2`)
  - TDD: n/a — test material for 2.5; these concretise breaking changes and regressions, where v3 is either already right or not "wrong" by its own wording, so they cannot be RED
- [x] 1.3 Extend `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md`: one row per new fixture in the 破壞的東西 / 應得判定 table with its v3 and v4 expected verdicts, flag which rows are RED→GREEN, breaking-change, regression or positive control, and update the re-run note so a re-runner delivers single fixtures without this README
  - TDD: n/a — prose/doc-only; verified by reading the table against the fixtures directory listing (every new directory has a row, every new row has a directory)

## 2. schema.yaml — Plan Contract, check 12, check 13 rationale, version

- [x] 2.1 Rewrite the Plan Contract in the `plan` instruction per REQ-4: positive entry definition (column-0 `##` plus whitespace; canonical `Task <n>` or legacy `<n>`; key is the number), the restated "key must lead" rationale (D2), the semantic fence sentence (D4), and the three-sentence `task-brief` guidance plus the recommendation, claiming recognition only and never "upstream accepts only this"
  - TDD: n/a — author-facing prose; its verdicts are carried by check 12, which 2.2 tests; verified in review by reading it against REQ-4 and against the check 12 text for agreement
- [x] 2.2 Rewrite check 12's ENTRY KEY collection per REQ-4 and D5: the positive definition replaces "headings that do not begin with a number", the column-0 backtick toggle is defined line by line, the unclosed-fence case is stated as producing no separate finding, and "tasks side unchanged" is written out; both stages, non-short-circuiting and all messages stay as they are
  - TDD: applicable
  - RED:
    - subject: fixtures/f14-fenced-heading-not-entry::PASS
    - outcome: FAIL
    - failure: expected PASS, actual BLOCK — plan keys [1.1, 9.9, 1.2]; entry key 9.9 matches no task number (fenced heading collected)
    - invocation: red-v3 (agent-executed blind run, pre-edit check 12, sha256 4d1ac91b)
  - GREEN:
    - subject: fixtures/f14-fenced-heading-not-entry::PASS
    - outcome: PASS
    - invocation: green-v4-r1 (agent-executed blind run, post-edit check 12, sha256 79d796db)
  - RED:
    - subject: fixtures/f15-task-form-entry::PASS
    - outcome: FAIL
    - failure: expected PASS, actual BLOCK — plan keys [] (Task-prefixed headings yield no key); tasks 1.1, 1.2 have no entry key
    - invocation: red-v3 (agent-executed blind run, pre-edit check 12, sha256 4d1ac91b)
  - GREEN:
    - subject: fixtures/f15-task-form-entry::PASS
    - outcome: PASS
    - invocation: green-v4-r1 (agent-executed blind run, post-edit check 12, sha256 79d796db)
  - RED:
    - subject: fixtures/f16-task-and-legacy-same-key::BLOCK
    - outcome: FAIL
    - failure: expected BLOCK (1.1 occurs more than once in plan.md), actual PASS — plan keys [1.1]; `## Task 1.1` not collected, so no repeat seen
    - invocation: red-v3 (agent-executed blind run, pre-edit check 12, sha256 4d1ac91b)
  - GREEN:
    - subject: fixtures/f16-task-and-legacy-same-key::BLOCK
    - outcome: PASS
    - invocation: green-v4-r1 (agent-executed blind run, post-edit check 12, sha256 79d796db)
- [x] 2.3 Add the deliberate-asymmetry rationale to both check 12 and check 13 (check 13 counts fenced heading-shaped lines on purpose; check 12 skips them on purpose), leaving every check 13 decision unchanged
  - TDD: n/a — rationale prose only; verified by a diff showing check 13 gains the sentence and nothing else in it changes
- [x] 2.4 Set `schema.yaml` `version: 4`
  - TDD: n/a — configuration; verified by `openspec schema validate` in 4.1
- [x] 2.5 Run the 1.2 fixtures and the existing check-12 fixtures (`f5`, `f8`, `f9`) against the v4 wording under the same blind protocol, and record each actual verdict and intermediate values beside its frozen expectation
  - TDD: n/a — breaking-change and regression verification, not RED→GREEN; every actual verdict must equal the README's v4 expectation, and any mismatch reopens 2.2

## 3. Templates, version and coupled documents

- [x] 3.1 Change `templates/plan.md`: the three example headings to `## Task 1.1 —`, `## Task 1.2 —`, `## Task 2.1 —`, and its HTML comment to say a fixed `Task` prefix is accepted and is not part of the key
  - TDD: n/a — template prose; verified by grep that no example heading keeps the legacy form and that the comment matches REQ-4
- [x] 3.2 Set `superpowers-bridge/VERSION` to `4.0.0`
  - TDD: n/a — configuration
- [x] 3.3 Update `superpowers-bridge/README.md` per the D8 row: schema version, v3 → v4 migration (three exceptions) and its rationale section, Known breaking changes, Versioning table and current-release sentence as a rule (REQ-2, removing the `v3.0.0` tag claims), Compatibility v4 row with `pending` and the below-table note (REQ-3), S11 and its two follow-up paragraphs
  - TDD: n/a — prose/doc-only; verified by doc review and by 3.5's local read of the v4 row
- [x] 3.4 Mirror 3.3 in `superpowers-bridge/README.zh-TW.md`
  - TDD: n/a — prose/doc-only; verified by section-by-section comparison with 3.3
- [x] 3.5 Point `.github/workflows/version-check.yml`'s `Read pinned versions` step at the `v4` row
  - TDD: n/a — configuration; verified by running that step's grep/awk locally against the edited README and getting the v4 row's two versions, then by a `workflow_dispatch` run after push
- [x] 3.6 Update the repo `CLAUDE.md` places D8 names: the structure-tree note, the two-version-numbers table (release commit definition, practised from 4.0.0), and the cross-file coupling row whose "CI fails" claim becomes "a kept old row is read silently"
  - TDD: n/a — prose/doc-only; verified by doc review
- [x] 3.7 Add a v4 "Released" section to `docs/roadmap.md` and `docs/roadmap.zh-TW.md`
  - TDD: n/a — prose/doc-only; verified by doc review
- [x] 3.8 Once the commit setting `version: 4` exists, write the v3 → v4 rollback as the full SHA of its parent into both READMEs, and check that SHA out once to confirm `superpowers-bridge/schema.yaml` reads `version: 3` (REQ-4 of `release-versioning`)
  - TDD: n/a — documentation of a ref; verified by the checkout itself, and no placeholder may remain

## 4. Integration

- [x] 4.1 Re-sync `openspec/schemas/superpowers-bridge/` from the source bundle, then run `openspec schema validate superpowers-bridge` and `openspec schemas` in a throwaway project
  - TDD: n/a — structural validation; its output is the evidence
- [x] 4.2 During this change's apply, run the loaded upstream Superpowers `task-brief` on this change's own plan.md for at least one non-final entry, record the Superpowers version and script path, and show the extracted brief is line-for-line identical to that plan entry; record whether the final entry swallows trailing non-entry text as a known upstream limitation
  - TDD: n/a — integration acceptance test; `rc=0` is not evidence, the line comparison is
