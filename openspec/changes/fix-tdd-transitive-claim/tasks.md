# Tasks — fix-tdd-transitive-claim

> Work from the frozen Affected Surface (brainstorm §4.1, 35 segments / 21 logical
> positions). Identify segments by what they say, not by 2026-08-27 line numbers. Do not
> re-run discovery scans; re-confirm each segment by reading at edit time. Every new or
> reworded sentence must pass the D2 guarantee test (spec: tdd-claim-accuracy).

## 1. schema.yaml (code-class plane)

- [x] 1.1 Replace the transitive-activation false guarantee (was :507-518) with the frozen
      honest statement (design D2); correct the adjacent fallback-rationale lines
      (was :522-525) per D3; check the header/intro claims (was :10-11, :20, :474)
- [x] 1.2 Re-sync dogfood copy (`rm -rf openspec/schemas/superpowers-bridge && cp -R
      superpowers-bridge openspec/schemas/`) and run local validation
      (`openspec schema validate superpowers-bridge` + `openspec schemas` smoke in a clean
      /tmp project per CLAUDE.md)

## 2. Bridge READMEs (en + zh-TW, edited in pairs)

- [x] 2.1 Correct the 14 false-guarantee / fallback-rationale segments in
      `superpowers-bridge/README.md` (D2 wording for guarantee claims, D3 rationale for
      the `executing-plans` paragraphs; keep already-honest rows 500/501/506 and neutral
      rows unchanged)
- [x] 2.2 Mirror the same 14 segments in `superpowers-bridge/README.zh-TW.md`, keeping en
      and zh-TW symmetric segment-by-segment

## 3. Templates and repo-level surfaces

- [x] 3.1 Defuse the inducement block in `superpowers-bridge/templates/retrospective.md`
      (semantic block around :55-84, per design D5): keep the compliance table, remove
      default-all-✓ expectation and the ban on honest ✗ reasons
- [x] 3.1a Defuse the schema-side twin (added in review round 1): the same inducement in
      `schema.yaml`'s retrospective instruction ("Skipped-skill rules for §4") rewritten
      to the truthful framing — the 6th schema segment in the proposal's Impact
- [x] 3.2 Reword `CLAUDE.md` red-flag entry (was :207) to the D3 rationale
- [x] 3.3 Replace `TDD-via-subagents` in top-level `README.md` and `README.zh-TW.md`
      bridges table (was line 11) with an honest phrase (design D4)
- [x] 3.4 Bump `superpowers-bridge/VERSION` patch (1.0.x); do not touch the Compatibility
      table's `v1` row key

## 4. Verification and review chain (no corrective-fix discount)

- [x] 4.1 Sweep pass: re-read every edited segment against spec tdd-claim-accuracy's four
      requirements; hunt one counter-example for each absolute claim before keeping it
- [x] 4.2 Code plane: `/codex-review-fast` (Codex probe first; on failure record
      `[REVIEWER_FALLBACK]` and dispatch fallback per auto-loop rules) →
      precommit-equivalent (schema validate + schemas smoke) → note review-state verdicts
- [x] 4.3 Doc plane: `/codex-review-doc` over all edited .md in one dispatch → fix and
      return for re-verification until ✅ Mergeable → note review-state verdict
