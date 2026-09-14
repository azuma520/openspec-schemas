# Report — tasks 4.1 + 4.2

Worktree: `C:/Users/user/orca/openspec-schemas/.claude/worktrees/loosen-plan`

## Files changed (by me)

- `openspec/specs/tdd-claim-accuracy/spec.md` (4.1)
- `CLAUDE.md` (4.2)
- `openspec/changes/fix-v2-blocking-defects/tasks.md` (ticks + control results for 4.1, 4.2)

`git diff --name-only` also lists `superpowers-bridge/README.md`, `README.zh-TW.md`,
`templates/tasks.md`, `templates/verify.md` — group 3's pre-existing uncommitted edits, left alone.
No `git add` / `commit` / `push` was run.

---

## 4.1 — canonical tdd-claim-accuracy spec names one carrier

### Grep, before the edit (backtick-inclusive, exactly as the file writes it)

```
$ grep -n '`writing-plans`' openspec/specs/tdd-claim-accuracy/spec.md
22:`writing-plans`' task format contains TDD micro-steps) are conforming. Record-class files
42:The apply instruction in `schema.yaml` SHALL state where TDD actually comes from ... and SHALL NOT retain the superseded statements that the schema "neither enforces nor verifies TDD" or that TDD arrives via `writing-plans`' micro-step task content.
exit=0

$ grep -n 'plan\.md' openspec/specs/tdd-claim-accuracy/spec.md
60:requires TDD, both executors receive that requirement through plan.md task content;

$ grep -n 'micro-step' openspec/specs/tdd-claim-accuracy/spec.md
22: (same line as above)
42: (same line as above)
52:- **THEN** none states that the schema "neither enforces nor verifies TDD" or that TDD arrives via writing-plans micro-steps; each describes the annotation + evidence carrier at its actual capability
```

Four hits, two of them defects. **:42 and :52 are conforming and were left**: they name the stale
wording only in order to forbid it (`SHALL NOT retain the superseded statements …` /
`**THEN** none states …`). Deleting those would delete the prohibition. The bare-word grep for
`writing-plans` returned the same lines plus :52 — on this file it did not lose a hit, but the
backtick form is the one the acceptance names and the one reported here.

### Clause 1 — Requirement "No unconditional TDD guarantee" (was :20-24)

Before:

> already-falsified status (e.g. rows marked ❌ False / ⚠️, and the factual description that
> `writing-plans`' task format contains TDD micro-steps) are conforming. Record-class files
> (handoffs, discussion material, `openspec/changes/**/archive`) are exempt as append-only
> records.

After:

> already-falsified status (e.g. rows marked ❌ False / ⚠️, and the factual description that
> applicability is declared per task in tasks.md and carries no guarantee for tasks annotated
> `TDD: n/a`) are conforming. A surface MUST NOT cite `writing-plans`' micro-step task format as
> the description of where TDD comes from: under the evidence contract the carrier is the
> tasks.md annotation plus its RED/GREEN evidence, and `writing-plans` is not a normative
> dependency of any artifact. Record-class files (handoffs, discussion material,
> `openspec/changes/**/archive`) are exempt as append-only records.

The old text carved out an *exemption* permitting a surface to describe `writing-plans`' task format
as where TDD comes from — the exact thing this change's global constraint forbids.

### Clause 2 — Requirement "executing-plans exclusion rationale rests on review structure" (was :56-61)

Before:

> subagents exist — and SHALL NOT use TDD transitivity as a differentiator (when a task
> requires TDD, both executors receive that requirement through plan.md task content;
> neither path guarantees it otherwise).

After:

> subagents exist — and SHALL NOT use TDD transitivity as a differentiator. TDD is not a
> differentiator between the two executors because it does not travel through either of them:
> applicability is declared per task in tasks.md and evidenced by the RED/GREEN records the
> tdd-evidence-contract capability defines, so the requirement reaches an executor through the
> task list it is given, whichever executor that is. Surfaces SHALL NOT describe plan.md task
> content as the carrier of that requirement — under the Plan Contract plan.md holds contract
> entries and no task list.

Both replacements are the delta spec's own wording, character for character, so the archive merge is
idempotent rather than conflicting.

### Grep, after the edit

```
$ grep -n "\`writing-plans\`' task format contains TDD micro-steps\|through plan.md task content" \
    openspec/specs/tdd-claim-accuracy/spec.md
grep-exit=1        # zero hits, no output
```

### What the full read found beyond the two cited ranges

All 87 lines read. No third statement of a plan.md / `writing-plans` carrier. The only other
mentions are the two prohibitions at :42 and :52, which state the carrier correctly ("each describes
the annotation + evidence carrier at its actual capability"). The Purpose section, the
retrospective-template requirement and every scenario name no carrier at all.

**Not copied, deliberately:** the delta spec adds two NEW scenarios ("writing-plans is no longer
cited as the carrier"; "Carrier named consistently across the spec"). Those are additions, not stale
clauses, and `openspec archive` merges them. Authoring them here would be double-applying in the
other direction.

### Delta spec untouched

```
$ git diff --name-only -- openspec/changes/fix-v2-blocking-defects/specs/ | wc -l
0
$ git status --porcelain openspec/changes/fix-v2-blocking-defects/specs/
(no output)
```

### Validation

```
$ openspec validate --all
- Validating...
✓ change/fix-v2-blocking-defects
✓ spec/plan-contract
✓ spec/repo-guidance
✓ spec/tdd-claim-accuracy
✓ spec/tdd-evidence-contract
Totals: 5 passed, 0 failed (5 items)
EXIT=0
```

Re-run after the tasks.md annotation landed: identical output, exit 0.

---

## 4.2 — CLAUDE.md coupling table and version narrative

### Correction 1 — cross-file coupling row

The workflow and the README, read directly:

```
.github/workflows/version-check.yml:44   line=$(grep -E '^\| v2 \| `' superpowers-bridge/README.md | head -1)
.github/workflows/version-check.yml:50   pinned_openspec=$(echo "$line" | awk -F'`' '{print $2}')
.github/workflows/version-check.yml:51   pinned_superpowers=$(echo "$line" | awk -F'`' '{print $4}')

superpowers-bridge/README.md:520   | v2 | `1.3.1` | `v5.1.0` | 2026-09-01 |
superpowers-bridge/README.md:521   | v1 | `1.3.1` | `v5.1.0` | 2026-05-11 |
```

Row before:

> **CI 直接 fail**。它用 ``grep -E '^\| v1 \| `'`` 抓那一行,再用 ``awk -F'`'`` 取第 2、4 個 backtick 欄位 —— 表格必須維持「第一欄 `v1`、OpenSpec 版本與 Superpowers 版本各自包在單一 backtick 裡」的形狀

Row after:

> **CI 直接 fail**。它用 ``grep -E '^\| v2 \| `'`` 抓那一行(取第一筆),再用 ``awk -F'`'`` 取第 2、4 個 backtick 欄位 —— 表格必須維持「第一欄 `v2`、OpenSpec 版本與 Superpowers 版本各自包在單一 backtick 裡」的形狀

The added 「取第一筆」 records the `head -1`, which became load-bearing once the table kept a `v1`
row below the `v2` row. Re-running the workflow's own commands against the README yields `1.3.1`
and `v5.1.0`.

### Correction 2 — schema major / bundle version

| Line | Before | After |
|---|---|---|
| 32 (structure tree) | `bundle SemVer(1.0.1),與 schema.yaml 的 version: 1 是兩回事` | `bundle SemVer(2.0.0),與 schema.yaml 的 version: 2 是兩回事` |
| 187 (coupling table) | `schema major 需從 1 bump` | `schema major 需從 2 bump` |
| 196 | `schema.yaml: version: 1` | `schema.yaml: version: 2` |
| 197 | git tag `v1.x.y` … `1.x.y` 都屬 schema major 1 | git tag `v2.x.y` … `2.x.y` 都屬 schema major 2 |
| 199 | `Compatibility 表的列鍵用的是 **schema major(v1)**,不是 bundle 版本` | `… **schema major(v2)**,不是 bundle 版本` |

Ground truth: `superpowers-bridge/VERSION` = `2.0.0`; `superpowers-bridge/schema.yaml:2` = `version: 2`.

Line 199's **point survives intact**: the sentence still says the row key is the schema major and
not the bundle version, and still warns that touching that first column breaks the CI grep. Only the
example moved from `v1` to `v2`, which now agrees with correction 1's `^\| v2 \|`.

Two judgment calls, stated rather than buried:

- **Line 187 was included.** It sits in the coupling table rather than the 「兩個版本號別搞混」
  section, but it is a schema-major sentence that still asserts the current major is 1 — the same
  defect, same class as :196. The brief's wording is "the schema-major sentences say `version: 2` /
  `2.0.0` where they still say 1".
- **Lines 87 (`這個 repo 正在從 v1 往下一代改`), 210 (`本 schema 在 v1 已具體應對`) and 233
  (`roadmap(v1.x backlog …)`) were left alone.** 210 and 233 are historically true. 87 sits inside
  the governance/direction section the brief fences off.

### Correction 3 — loosen-plan pointer

Before:

> 第一個落地的 schema change 是 `loosen-plan`(`openspec/changes/loosen-plan/`,Plan Contract + TDD 證據契約,schema major → 2)。

After:

> 第一個落地的 schema change 是 `loosen-plan`(已 archive,見 `openspec/changes/archive/2026-09-04-loosen-plan/`,Plan Contract + TDD 證據契約,schema major → 2)。

```
$ ls -d openspec/changes/archive/2026-09-04-loosen-plan
openspec/changes/archive/2026-09-04-loosen-plan/
$ ls -d openspec/changes/loosen-plan
ls: cannot access 'openspec/changes/loosen-plan': No such file or directory
```

### Every path named in the edited sentences

```
OK   openspec/changes/archive/2026-09-04-loosen-plan
OK   superpowers-bridge/README.md
OK   .github/workflows/version-check.yml
OK   superpowers-bridge/VERSION            (contents: 2.0.0)
OK   superpowers-bridge/schema.yaml        (line 2: version: 2)
OK   superpowers-bridge/templates
OK   docs/roadmap.md
OK   .github/workflows/validate-schemas.yml
OK   superpowers-bridge/templates/adopters/CLAUDE.md.fragment.md
```

(The last four are named by neighbouring cells of the coupling-table rows I touched; checked so the
edited row does not sit beside a dead path.)

### Containment

```
$ git diff --ignore-cr-at-eol --stat CLAUDE.md
 CLAUDE.md | 14 +++++++-------
 1 file changed, 7 insertions(+), 7 deletions(-)
```

Seven changed lines — :32, :107, :185, :187, :196, :197, :199 — and each is one of the three
corrections. Nothing else changed: the red-flag list (:224) is untouched and no governance language
was rewritten. Locale kept: 繁體中文 with Taiwanese usage, no 簡體字, no 大陸用語, no English drift.

---

## Self-review findings

- The bare-word grep trap did not bite on this file (both forms surfaced the :22 hit), but the
  backtick-inclusive form is what was run and reported.
- I initially framed 4.1 as "edit the two cited line ranges". Reading the whole file showed :42 and
  :52 also match those greps and must **not** be edited — a grep-driven sweep would have deleted two
  prohibitions. Caught by reading, not by grepping.
- `openspec validate --all` could genuinely have failed: it parses the requirement/scenario
  structure, and clause 1 rewrote a requirement body.
- `ls -d openspec/changes/loosen-plan` could genuinely have succeeded (it would have, had the change
  still been active); it returned "No such file or directory", which is the fact the repoint rests on.

## Concerns

1. **`schema major 需從 2 bump` (:187) hard-codes today's major**, so it goes stale at the next bump
   exactly as `1` did. A version-agnostic 「schema major 需 bump」 would not, but that is a wording
   change beyond correcting a stale number, so I made the minimal correction and flag it here.
2. **`superpowers-bridge/README.zh-TW.md`'s Compatibility table was not checked** — outside my scope
   fence, and group 3's file. The coupling row I edited describes only the en README, which is what
   the workflow actually greps.
3. **Line 87 (`這個 repo 正在從 v1 往下一代改`) still reads as if v2 had not landed.** Left per the
   governance fence; noting it so the separate registered governance task can pick it up.

---

## Fix round 1 (Minor) — the 4.1 control record named only two of three greps

**Finding.** `openspec/changes/fix-v2-blocking-defects/tasks.md:133` named two greps, then classified
"the other two hits, :42 and :52". `:52` came from neither named grep — it came from a third search
(`micro-step`) the record never mentioned. The record therefore under-described its own method: a
reader re-running only the named greps would reproduce three hits, not the four classified.

**Fix — one clause, nothing else.**

Before:

> before the edit, `grep -n '`writing-plans`' openspec/specs/tdd-claim-accuracy/spec.md` returned lines 22 and 42 and `grep -n 'plan\.md'` returned line 60. Two of those are the stale carrier claims — …

After:

> before the edit, `grep -n '`writing-plans`' openspec/specs/tdd-claim-accuracy/spec.md` returned lines 22 and 42, `grep -n 'plan\.md'` returned line 60, and `grep -n 'micro-step'` returned lines 22, 42 and 52. Two of those four hits are the stale carrier claims — …

The classification itself was not re-run and not restructured.

**Check that the fix worked** — the three greps as now named, re-run verbatim against the pre-edit
file (`git show HEAD:` piped to grep; no temp file), reproduce exactly the four hits classified:

```
$ git show HEAD:openspec/specs/tdd-claim-accuracy/spec.md | grep -n '`writing-plans`'
22:`writing-plans`' task format contains TDD micro-steps) are conforming. …
42:The apply instruction in `schema.yaml` SHALL state where TDD actually comes from …

$ git show HEAD:openspec/specs/tdd-claim-accuracy/spec.md | grep -n 'plan\.md'
60:requires TDD, both executors receive that requirement through plan.md task content;

$ git show HEAD:openspec/specs/tdd-claim-accuracy/spec.md | grep -n 'micro-step'
22: (as above)
42: (as above)
52:- **THEN** none states that the schema "neither enforces nor verifies TDD" …

union of line numbers → 22 42 52 60
```

Four hits, matching the four the record classifies (:22 and :60 stale and fixed; :42 and :52
conforming prohibitions, left).

**Not fixed, per the round's instruction** (both ruled correctly out of scope): `CLAUDE.md:187`'s
`需從 2 bump` hard-coding today's major (carried to close-out as a follow-up for the user), and
`CLAUDE.md:87` 「這個 repo 正在從 v1 往下一代改」 (belongs to the registered governance-language task).

Files changed this round: `openspec/changes/fix-v2-blocking-defects/tasks.md` only.
No commit; scope fence unchanged. `openspec validate --all` re-run after the edit: 5 passed, 0 failed, exit 0.
