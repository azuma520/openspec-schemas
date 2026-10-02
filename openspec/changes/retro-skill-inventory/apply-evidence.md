# Apply Evidence — retro-skill-inventory (tasks 2.1, 2.2)

## 2.1 — README consistency check

**Scope:** `superpowers-bridge/README.md` and `superpowers-bridge/README.zh-TW.md`, searched in full for any statement about what retrospective §4 ("Skill / workflow compliance") lists, and about `writing-plans`.

**Search commands used (re-runnable):**

```bash
# English README
grep -n "writing-plans" superpowers-bridge/README.md
grep -n "retrospective|§4|Skill compliance|compliance|skill inventory" -E superpowers-bridge/README.md

# zh-TW README
grep -n "writing-plans|撰寫計畫|寫計畫" -E superpowers-bridge/README.zh-TW.md
grep -n "retrospective|回顧|技能|合規|§4|遵循" -E superpowers-bridge/README.zh-TW.md
```

Also read in full: the "Seven Superpowers touchpoints" table (README.md lines 296–312 / README.zh-TW.md equivalent), the "Apply phase walkthrough → 4. Retrospective" section (README.md lines 411–413 / README.zh-TW.md lines 411–413), and every `writing-plans` hit's surrounding paragraph in both files (migration sections, re-verification log, versioning rationale).

**Hits found and verdicts:**

| # | File | Location | Quoted text (paraphrase of key clause) | Verdict |
|---|------|----------|------------------------------------------|---------|
| 1 | README.md | line 413 (also README.zh-TW.md line 413 — same sentence, which keeps the English phrase "Skill compliance", so the recorded zh-TW grep pattern does not match it; found by the full read noted above, not by grep) | "§0 Evidence ... plus 6 analysis sections (Wins / Misses / Plan deviations / **Skill compliance** / Surprises / Promote candidates)" | No conflict — names the section title only, does not enumerate which skills/rows §4 contains. Does not state a second definition of what §4 lists. |
| 2 | README.md | lines 296–312, "Seven Superpowers touchpoints" table | Row 2: `superpowers:writing-plans` → "Not invoked ... the instruction names the skill only as an optional private decomposition aid"; row 5 `test-driven-development` → "Conditional"; row 6 `requesting-code-review` → "Structural"; closing note: "Naming is not requiring... writing-plans is named only as an optional private aid, and test-driven-development / requesting-code-review are never invoked by the schema itself." | No conflict — this table describes schema.yaml invocation sites generally (not the retrospective §4 inventory specifically), and its characterization of `writing-plans` as "optional aid, not invoked" is consistent with REQ-5's rule that such a skill MUST NOT be listed in §4. |
| 3 | README.zh-TW.md | lines 296–312 (zh-TW equivalent of #2) | Same content in Traditional Chinese, including `writing-plans` 列為「可選的私下拆解輔助」| No conflict — same reasoning as #2. |
| 4 | README.md | lines 524–531, "Migrating v1 → v2", item 4 | "`superpowers:writing-plans` — no longer a required dependency; remove it from your install expectations. It stays usable as a private decomposition aid." | No conflict — about install/dependency expectations, not about the retrospective §4 inventory. |
| 5 | README.zh-TW.md | lines 524–531 (zh-TW equivalent of #4) | Same content in Traditional Chinese. | No conflict — same reasoning as #4. |
| 6 | README.md | lines 492–499, "Why v1 → v2 is a schema-major bump", item 2 | Discusses removal of the `plan` artifact's skill PRECHECK because `writing-plans` is no longer a dependency. | No conflict — about the `plan` artifact's PRECHECK, unrelated to §4's inventory. |
| 7 | README.zh-TW.md | lines 492–499 (zh-TW equivalent of #6) | Same content in Traditional Chinese. | No conflict — same reasoning as #6. |
| 8 | README.md | lines 559–568, "Re-verification log" (2026-08-26, Superpowers v6.3.0) | Lists the "8 skills this schema names" including `writing-plans`, and notes "as of v2 `writing-plans` is named only as an optional decomposition aid." | No conflict — this is a drift-tracking log about which skills the *schema* names anywhere (not specifically the retrospective §4 inventory), and it is consistent with `writing-plans` being excluded from §4. |
| 9 | README.zh-TW.md | lines 559–568 (zh-TW equivalent of #8) | Same content in Traditional Chinese. | No conflict — same reasoning as #8. |

**Remaining hits, not individually tabled above:** re-running the four recorded commands gives `writing-plans`: 9 lines in each file, `retrospective|...`: 20 lines in each file (re-verified 2026-10-02). The table above addresses lines 301, 310, 413, 497, 531, 563 in README.md and the equivalent lines in README.zh-TW.md (except README.zh-TW.md has no hit at line 413 under its own pattern — its nearest `writing-plans`/TDD-discipline passage sits at line 397, a false-positive substring match of `合規` inside `符合規定`, "conforms to the format rule", unrelated to §4). The remaining lines in both files are not statements about §4's contents: README.md 570/572/574/594 and README.zh-TW.md 570/572/574/594 continue the same "re-verification log" paragraph as rows 8/9 (559–568) — more TDD-provenance history for how `writing-plans` used to carry TDD before schema v2, not a claim about what §4 lists; and lines 10, 115, 166, 202, 214, 215, 249, 286, 293, 333, 348, 409, 411, 464, 469, 473, 475, 507 (both files, same numbering except zh-TW's 397 in place of README.md's 413) are lifecycle/DAG diagrams and artifact-order tables (202, 214, 215, 249, 286, 473, 475, 507), timing/CLI-usage mentions of when the retrospective artifact runs (293, 333, 348, 409), general intro prose about the bridge or the artifact (10, 115, 166, 411), or descriptions of the file-existence PRECHECK mechanism for the `retrospective` artifact (464, 469) — none enumerates or redefines what the §4 table lists.

**Conclusion:** No hit in either README conflicts with REQ-5. Neither README was modified (per acceptance criterion — "If no hit conflicts, neither README is modified").

---

## 2.2 — CLI delivery check

### Step 1: Dogfood sync

Command:
```bash
cp -R superpowers-bridge/. openspec/schemas/superpowers-bridge/
diff -r superpowers-bridge openspec/schemas/superpowers-bridge
```

Output: no output (diff reports no difference) → `DIFF_EMPTY_OK` confirmed by follow-on echo.

### Step 2: Schema and change validation

Command:
```bash
openspec schema validate superpowers-bridge
```
Output:
```
Note: Schema commands are experimental and may change.
✓ Schema 'superpowers-bridge' is valid
```
Exit code: 0.

Command:
```bash
openspec validate retro-skill-inventory --strict
```
Output:
```
Change 'retro-skill-inventory' is valid
```
Exit code: 0.

### Step 3: Retrospective instructions content check

**Re-run 2026-10-02, after the final-review fix to the §4 exclusion sentence (see "Final-review fix round" in `.superpowers/sdd/plan/batchB-report.md`).** Command (output captured to a scratchpad file, then inspected via grep — avoiding `/tmp` per repo convention):
```bash
openspec instructions retrospective --change retro-skill-inventory > <scratchpad>/instr_output2.txt
```
Exit code: 0. Output: 338 lines.

**Absence check — "this schema's apply phase":**
```bash
grep -c "this schema's apply phase" <scratchpad>/instr_output2.txt
```
Result: `0` — the old phrase is absent.

**New §4 criterion text — present (excerpt, lines 98–110 of the captured output):**
```
   §4) **Skill / workflow compliance** — inventory exactly
       two classes of items, and mark whether each was
       actually used: (1) Superpowers skills this schema
       explicitly requires invoking — identifiable by where
       the schema requires them (the `brainstorm` artifact,
       and apply pre-flight); and (2) Superpowers
       disciplines this schema requires to be carried out
       and whose execution the retrospective must record,
       even though the schema does not invoke them
       directly — the TDD and code-review disciplines. A
       skill named only as an optional aid and carrying
       neither discipline (e.g. `writing-plans`) is not
       listed merely because it may be useful.
```
This matches the revised two-class criterion text (final-review fix, schema.yaml:1524–1526): the exclusion now names the condition — "carrying neither discipline" — instead of leaving it implicit, and "is not listed merely because it may be useful" replaces the ambiguous "is not listed on the grounds that it may be useful".

**`writing-plans` occurrence count and context:**
```bash
grep -n "writing-plans" <scratchpad>/instr_output2.txt
```
Result: 2 lines — 109 and 272. Line 109 is inside the revised criterion-text sentence above, naming `writing-plans` only as the example of an excluded optional-aid skill (not as a table row). Line 272 is the zh-TW note under the template's §4 table, stating the same exclusion in Traditional Chinese (unchanged by this fix round). Neither occurrence is a `writing-plans` row in the six-row table.

**New-sentence presence check:**
```bash
grep -n "merely because it may be useful" <scratchpad>/instr_output2.txt
```
Result: line 110 — present.

**Six-row table — present, no `writing-plans` row (excerpt, template section around lines 255–264 of the captured output):**
```
## 4. Skill / workflow compliance

| Skill                                            | Used |
|--------------------------------------------------|------|
| superpowers:brainstorming                        |      |
| superpowers:using-git-worktrees                  |      |
| superpowers:subagent-driven-development          |      |
| superpowers:test-driven-development (✓ only if the skill was explicitly invoked; write `N/A — annotation-driven` when TDD discipline came from the `TDD:` annotations in `tasks.md` and their RED/GREEN evidence instead) |      |
| (structural via SDD) superpowers:requesting-code-review |      |
| superpowers:finishing-a-development-branch       |      |
```
Row count: 6 (brainstorming, using-git-worktrees, subagent-driven-development, test-driven-development, requesting-code-review, finishing-a-development-branch). No `superpowers:writing-plans` row. Matches the six rows specified by REQ-5 and task 1.1's edit.

**Conclusion:** All three 2.2 acceptance bullets re-confirmed after the final-review fix — dogfood copy (`cp -R superpowers-bridge/. openspec/schemas/superpowers-bridge/` then `diff -r`, output empty) is identical to the source bundle, both `openspec schema validate superpowers-bridge` and `openspec validate retro-skill-inventory --strict` pass with exit code 0, and the CLI-delivered retrospective instructions carry the revised §4 exclusion sentence, omit "this schema's apply phase", and show the six-row table (1.1) with no `writing-plans` row.
