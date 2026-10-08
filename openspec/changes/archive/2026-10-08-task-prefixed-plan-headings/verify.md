# Verification Report

> 此檔案由 `openspec-verify-change` skill 在 apply 完成後產生，用以確認實作
> 與 specs / design / tasks 的一致性。失敗的檢查須返回對應 artifact 修正後
> 再重跑 verify。

**Change**: `task-prefixed-plan-headings`
**Verified at**: `2026-10-08 11:42`
**Verifier**: independent verify agent (Claude Opus 5.5 subagent; did not implement this change). Ran the schema's verify instruction (v4, rendered by the CLI from the installed copy `openspec/schemas/superpowers-bridge/`) after invoking the `openspec-verify-change` skill. The skill's three-dimension scorecard is at the end of this file. Every check below was run against the files directly; results taken from the execution ledger rather than re-run are marked **(ledger)**.

**PRECHECK — implementation evidence** (both positive; run 2026-10-08):

| Command | Result |
|---|---|
| `git log --oneline $(git merge-base HEAD origin/main)..HEAD \| wc -l` (merge-base = `origin/main` = `e139fc1`) | **4** (`238ecbe`, `1efb729`, `737aa56`, `0b11be5`) |
| `grep -c '^- \[x\]' openspec/changes/task-prefixed-plan-headings/tasks.md` | **18** |

---

## 1. Structural Validation (`openspec validate --all --json`)

- [x] 全數 items `"valid": true`

**結果**（local OpenSpec CLI **1.3.1**, run in the worktree root）：

```text
items 6, passed 6, failed 0
  spec  contract-identity       valid (8 INFO: requirement text > 500 chars)
  spec  plan-contract           valid (1 INFO, same)
  spec  repo-guidance           valid
  change task-prefixed-plan-headings valid (no issues)
  spec  tdd-claim-accuracy      valid (1 INFO, same)
  spec  tdd-evidence-contract   valid (2 INFO, same)
```

若有失敗項目，列出 id + issues：

| Item | Type | Issues |
|---|---|---|
| — | — | 無（INFO only） |

Note: the Compatibility v4 row lists OpenSpec `1.14.0`; nothing in this change was validated on 1.14.0. Every CLI result in this file (checks 1, 3, 13, and task 4.1's `schema validate` / `schemas`) is from **1.3.1**.

---

## 2. Task Completion (`tasks.md`)

- [x] 所有 task 的 checkbox 皆為 `- [x]` 或 `- [~]`
      （`- [~]` 是 check 7 定義的 DEFERRED TASK,不是未完成任務;
       它是否已被妥善交代由 check 7 判,不在本項失敗。仍有 `- [ ]` 才需填下表。）

18 task lines, 18 `- [x]`, 0 `- [~]`, 0 `- [ ]`.

**未完成任務**（若有）：

| Task | 未完成原因 | 是否阻塞 archive |
|---|---|---|
| — | — | — |

Outside tasks.md by design (D6, release-versioning REQ-1): creating, pushing and remotely confirming the annotated tag `v4.0.0`. It happens **after archive** on the release commit and gates the work-map record `task-20261002-task-brief-heading-compat`, which stays DOING until `refs/tags/v4.0.0^{}` on the remote equals the recorded release commit. It is **not done** and is not claimed here; `git tag -l` returns nothing today.

---

## 3. Delta Spec Sync State

| Capability | Sync 狀態 | 備註 |
|---|---|---|
| `plan-contract` | ✗ Needs sync | Main spec holds REQ-1–REQ-3 only; the delta ADDs REQ-4 (10 scenarios) |
| `release-versioning` | ✗ Needs sync | New capability: `openspec/specs/release-versioning/` does not exist; the delta ADDs REQ-1–REQ-4 |

Neither is synced, so check 13 below reads both main specs as the pre-archive baseline (no "required pre-sync state unavailable" case).

---

## 4. Design / Specs Coherence Spot Check

| 抽樣項 | design 描述 | specs 對應 | 差距 |
|---|---|---|---|
| Entry rule | D2: column-0 `##` + whitespace; `Task` (exact case) + whitespace + number, or number alone; number `\d+(\.\d+)*` followed by whitespace/EOL; key = number | plan-contract REQ-4 conditions 1–4 + key paragraph; S1, S2, S3, S6, S7 | None in meaning. Schema wording says "the text after that WHOLE run" (Ruling R7) where REQ-4 says "the text after that whitespace" — a clarification, same meaning |
| Fence rule | D4: only column-0 backtick lines toggle; `~~~` / indented do not | REQ-4 fence paragraph; S4, S5, S8 | None |
| Scope of check 12 change | D5: stages, non-short-circuiting, messages, tasks side unchanged; asymmetry with check 13 stated in both | REQ-4 paragraph 4; S10 | None. The D5 overclaim ("align with SDD's task extraction") was narrowed in the final fix wave to fences only (uncommitted design.md edit) |
| Release / rollback | D6: tag from 4.0.0 on the release commit, peeled-SHA confirmation, no back-tagging, `pending` date, rollback = parent SHA of first `version: 4` commit | release-versioning REQ-1–REQ-4 | None |
| Verification method | D7: fixtures table (7 rows) + blind agent runs + upstream `task-brief` dogfood | REQ-4-S3/S4/S6/S7 | See warnings |

**漂移警告**（非阻塞）：

- REQ-4-S6 names seven near-miss forms; fixtures exist for five (`f18`–`f22`). `## Tasks 1.1` and `## Task1.1` have none (Ruling R3, scope: they are not in the D7 table). REQ-4-S5 (tilde / indented fences), S8 (unclosed fence), S9 (mixed forms + trailing section) and S10 (check-13 counting) have no fixture or blind run; the ledger records only that the group-2 reviewer hand-ran S1–S10 against the text **(ledger)**.
- design Migration Plan step 4 says "push 後確認 `validate-schemas.yml` 綠". That workflow triggers only on push/PR to `main` or `workflow_dispatch` (`.github/workflows/validate-schemas.yml` `on:`), so the branch push did **not** run it — `gh run list --branch feat/task-prefixed-plan-headings` shows only run `37723513752` (Weekly upstream version check). **CI schema validation is not green on this branch; it has not run.**
- D8 did not list the root `README.md` / `README.zh-TW.md` bridges table; it was updated anyway (Ruling R9). Retrospective item.

---

## 5. Implementation Signal

- [ ] Worktree 內無未 staged 的檔案 — **not met.** `git status --porcelain` lists 8 modified, uncommitted files: `CLAUDE.md`, `docs/roadmap.md`, `docs/roadmap.zh-TW.md`, `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md`, `openspec/changes/task-prefixed-plan-headings/design.md`, `.../tasks.md`, `superpowers-bridge/README.md`, `superpowers-bridge/README.zh-TW.md` (final-review fix wave, task 3.8 SHA substitution, tasks.md ticks and RED/GREEN records), plus this `verify.md` (new).
- [ ] 所有相關 commit 已推送 — **partly.** `origin/feat/task-prefixed-plan-headings` = `0b11be5` = `HEAD`; the working-tree edits above are neither committed nor pushed.

**Commit 範圍**：`e139fc1..0b11be5` (the four commits above; `737aa56` is the base the apply started from). `superpowers-bridge/schema.yaml`, `templates/` and `VERSION` are unchanged between `0b11be5` and the working tree (`git diff --stat 0b11be5 --` on them is empty), so the committed schema is the schema verified below.

Also found: the installed copy `openspec/schemas/superpowers-bridge/` is **no longer identical** to the source bundle. `diff -r` shows `schema.yaml` and every template identical, but `README.md` and `README.zh-TW.md` differ at lines 530, 537, 661 (fix-wave edits made after task 4.1's sync). Task 4.1's "recursive diff is empty" held when it ran **(ledger)** but does not hold now. It does not affect any verify verdict (the instruction comes from `schema.yaml`, which is identical), but the copy should be re-synced before archive per repo `CLAUDE.md`.

---

## 6. Front-Door Routing Leak Detector（warning,非阻塞）

設計產出不應落在 `docs/superpowers/specs/`(brainstorm artifact 的
output redirection 會把它導到 `openspec/changes/<name>/brainstorm.md`)。

偵測:

```bash
ls docs/superpowers/specs/*.md 2>/dev/null
```

- [x] 無檔案,或存在的檔案是 schema 安裝前的合法存留

**洩漏清單**（若有）：

| 檔案 | 內容是否已 captured 進 change | 建議動作 |
|---|---|---|
| `2026-05-02-openspec-schemas-monorepo-design.md` | N/A — repo-level design, not this change | Keep |
| `2026-08-27-bridge-guarantee-architecture-direction.md` | N/A — repo direction doc cited by root `CLAUDE.md` | Keep |
| `2026-08-28-concept-poc-traceability-gate-design.md` | N/A | Keep |
| `2026-09-01-bridge-guarantee-formal-design.md` | N/A — cited by root `CLAUDE.md` as the approved formal design | Keep |
| `2026-09-23-formal-design-revision-map.md` | N/A | Keep |

WARNING recorded as the instruction requires: "Front-door routing leak — design output found at docs/superpowers/specs/…". All five files predate this change (last touched 2026-05-02 … 2026-09-29 per `git log`; this change opened 2026-10-07) and none is this change's design output, so nothing here needs moving.

> 不會擋住 archive。新的 schema-installed cycle 產生的洩漏,應搬進
> `openspec/changes/<name>/brainstorm.md` 或 `design.md` 後刪原檔。

---

## 7. Deferred Dogfood vs Automated-Test Equivalence

tasks.md has **no** line whose first non-space characters are `- [~]` (`grep -c '^\s*- \[~\]'` → 0). This section is empty, which is a PASS.

| Deferred task (tasks.md) | Equivalent automated test | Coverage assessment | 真正 gap? |
|---|---|---|---|
| — | — | — | — |

---

## 8. TDD Evidence Contract — Deterministic Checks 8–12

Reports the verify instruction's deterministic checks 8–12. Checks 8–11 are
per task; check 12 is per change. Any BLOCK here means the change is not
verified for archive.

Check titles, copied from the schema's check list — do not paraphrase:

8. **TDD annotation present and well-formed** (deterministic)
9. **RED and GREEN records present, required fields present and non-empty, and every `subject:` value well-formed** (deterministic)
10. **Outcome markers** (deterministic)
11. **Records pair by `subject:` value — unique on each side, then one RED and one GREEN per subject** (deterministic, two stages)
12. **tasks.md task numbers and plan.md entry keys correspond 1:1 — no duplicate on either side, then equal sets** (deterministic, two stages)

How they were run: a line-by-line reading of tasks.md / plan.md applying the instruction's rules (task-line, belongs-to, blank-transparency, field, cardinality, `::` scan, outcome token, two-stage pairing, and check 12's v4 FENCE / ENTRY / KEY rules), cross-checked with a small script over the same rules. Inputs: tasks.md and plan.md as they are in the working tree at 2026-10-08 11:42 (plan.md is byte-identical to `737aa56`, sha256 `b93b594d…2e837`).

**Per-task results** (one row per task line in `tasks.md`):

| Task | Annotation (8) | Records, fields + subject grammar (9) | Outcome markers (10) | Subject pairing (11) | Review judgement (R1–R4) |
|---|---|---|---|---|---|
| 1.1 | ✓ `TDD: n/a — test material for 2.2…` | N/A | N/A | N/A | ✓ R3 holds (fixtures are the test input, validated by 2.2's runs); R4 no records |
| 1.2 | ✓ `TDD: n/a — test material for 2.5…` | N/A | N/A | N/A | ✓ R3 holds (breaking-change / regression / positive-control fixtures cannot be RED); R4 no records |
| 1.3 | ✓ `TDD: n/a — prose/doc-only…` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 2.1 | ✓ `TDD: n/a — author-facing prose…` | N/A | N/A | N/A | ✓ R3 holds (Plan Contract verdicts are carried by check 12, tested in 2.2); R4 no records |
| 2.2 | ✓ `TDD: applicable` | ✓ 3 RED + 3 GREEN; every RED has `subject`/`outcome`/`failure`, every GREEN `subject`/`outcome`, none empty, no repeated key; every subject has exactly one `::` with both sides non-empty | ✓ RED `FAIL` ×3, GREEN `PASS` ×3 | ✓ stage 1: no repeat on either side; stage 2: `{f14…::PASS, f15…::PASS, f16…::BLOCK}` equal both ways | ✓ R1: each `failure:` is a wrong verdict under the v3 wording (behavioural, not a harness error); R2: each subject names the fixture that isolates the rule the task changes (fence exclusion, Task form, Task/legacy same key) |
| 2.3 | ✓ `TDD: n/a — rationale prose only…` | N/A | N/A | N/A | ✓ R3 (confirmed: check 13's diff `737aa56..HEAD` is one line extended with the rationale, nothing else); R4 no records |
| 2.4 | ✓ `TDD: n/a — configuration…` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 2.5 | ✓ `TDD: n/a — breaking-change and regression verification…` | N/A | N/A | N/A | ✓ R3 holds (v3 is either already right or not wrong by its own wording for these fixtures); R4 no records |
| 3.1 | ✓ `TDD: n/a — template prose…` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 3.2 | ✓ `TDD: n/a — configuration` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 3.3 | ✓ `TDD: n/a — prose/doc-only…` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 3.4 | ✓ `TDD: n/a — prose/doc-only…` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 3.5 | ✓ `TDD: n/a — configuration…` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 3.6 | ✓ `TDD: n/a — prose/doc-only…` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 3.7 | ✓ `TDD: n/a — prose/doc-only…` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 3.8 | ✓ `TDD: n/a — documentation of a ref…` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 4.1 | ✓ `TDD: n/a — structural validation…` | N/A | N/A | N/A | ✓ R3; R4 no records |
| 4.2 | ✓ `TDD: n/a — integration acceptance test…` | N/A | N/A | N/A | ✓ R3; R4 no records |

Legend: ✓ pass · ⛔ BLOCK (checks 8–11) · N/A (task annotated `n/a`, records not owed).
Checks 9–11 examine **every** record a task carries, however many subjects it has —
a defect in the second RED is reported exactly like one in the first. Check 11 runs
two stages and stage one does **not** short-circuit: record both the duplicate-subject
findings (naming the repeated value and the side it repeats on) and the two-direction
set comparison (a subject with a RED and no GREEN, and one with a GREEN and no RED),
even when both hold.
A review-judgement violation (R1 error-output RED, R2 subject does not test the claimed
behaviour, R3 `n/a` reason does not hold, R4 an `n/a` task carrying RED/GREEN records)
is a **blocking finding of the review**, not of a check — record it in the same row and
list it below.

**Check 12, stage one — duplicate keys per side** (each side examined independently;
a repeated key BLOCKs on its own, whatever the other side holds):

| Side | Repeated keys (name each) | Verdict |
|---|---|---|
| `tasks.md` task numbers | — (18 task lines, every one numbered) | ✓ |
| `plan.md` entry keys | — | ✓ |

**Check 12, stage two — set equality in both directions** (both differences must be empty):

| `tasks.md` task numbers | `plan.md` entry keys | Only in tasks (no entry) | Only in plan (no task) | Verdict |
|---|---|---|---|---|
| `{1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 4.1, 4.2}` | `{1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 4.1, 4.2}` | — | — | ✓ |

Check 12 was applied **as the v4 text is written** (the copy installed under `openspec/schemas/` is v4; its `schema.yaml` is identical to the source). plan.md contains no backtick fence line; its 18 `##` lines are all canonical `## Task <n> — …` at column 0 and each yields its number as key (canonical form; `Task` not part of the key). There are no other `##` lines in plan.md. Under the **v3** wording this same plan would collect no keys and BLOCK — plan.md's header says so deliberately; this report applies v4 as instructed.

> Stage one does **not** short-circuit — stage two is evaluated and recorded whatever
> stage one found, and the two messages stay distinct because the repairs differ
> (renumber one of two duplicates; add or remove a key for a missing/extra one).
> Also BLOCK: a task line carrying no task number, no collectable entry key, or no
> plan.md at all — record the last as "plan.md absent — no entry keys to compare",
> never as a set difference.

**Blocking findings** (deterministic checks and review judgements):

- 無

**Evidence behind task 2.2's records, and what kind of evidence it is.** It is **instruction-layer behavioural verification, agent-executed blind runs** — never an automated test run. The runner was a fresh subagent that read check 12's text and fixture copies and reported keys and a verdict; the controller compared those with the frozen expectations in the fixtures README. What this verifier confirmed itself vs took from records:

| Item | Confirmed by this verifier | Source |
|---|---|---|
| v3 check-12 text sha256 `4d1ac91b…cec91e` = extract of `737aa56:superpowers-bridge/schema.yaml` | ✓ recomputed (96 lines) and equal to `scratch/blind/red-v3/check12.txt` | extraction rule in fixtures README § 2026-10-08 盲測紀錄 |
| v4 check-12 text sha256 `79d796db…e9d046` = extract of the current / `0b11be5` `schema.yaml` | ✓ recomputed from the working tree (138 lines; schema.yaml unchanged since `0b11be5`) and equal to `scratch/blind/green-v4-r1/check12.txt` | same |
| Delivered case copies = fixtures (f14 plan `57e479e2`, f15 `bfcd7dc2`, f16 `eef33eb0`; tasks `eb19adae` / `5945d5c2`) | ✓ sha256 of fixtures vs `red-v3` and `green-v4-r1` case dirs, and key files | — |
| The runners' reported keys and verdicts | ✗ not re-run; runner transcripts not available | **(ledger)** + fixtures README tables |
| Independent non-blind cross-check: v4 rule applied by this verifier to f5, f8, f9, f14–f23 | ✓ keys match every v4 row in the README (f14/f15/f23 `{1.1,1.2}` PASS; f16 `1.1` twice; f17 `{1.1,3}`; f18–f22 none; f5 `{1,2,9}` vs `{1,2,3}`; f8 tasks `1.1` twice; f9 plan `2.3` twice) | not blind — this verifier knew the expectations |

Limits of that evidence, stated as the ledger and README record them:
- **Protocol deviation**: the re-run note asks for one fixture per delivery; each run gave one runner several case dirs (3, 6, 3, 10). The runner could see sibling cases from the same run.
- **Weaker discriminators**: v4 check 12 names the near-miss forms literally (` ## 1.1`, `##1.1`, `## task 1.1`, `1.1a`), so for `f18`–`f22` a runner may have matched an example rather than applied the general rule. `f14`–`f16` and `f23` do not have this weakness.
- **No fixtures** for REQ-4-S6's `## Tasks 1.1` and `## Task1.1` (Ruling R3).
- **`subject:` paths are relative** to the fixtures README directory `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/` (e.g. `fixtures/f14-fenced-heading-not-entry` resolves there; all three directories exist).
- The two earlier v4 runs (`green-v4`, `v4-25`, sha `2c4735b0…`) are superseded; their wording was never committed. The runs of record are `green-v4-r1` and `v4-25-r1` (10/10 match) **(ledger)**.

> **Claim boundary — copy as written, claim no more.** These checks are
> deterministic in *what they decide* and agent-executed (instruction-mediated)
> in *how they run*: their execution is the verify agent following the schema
> instruction. This schema requires them to run before archive and to block on
> failure, but this is **not** a Harness-level, mechanically enforced, non-bypassable
> archive-time gate — if the verify agent skips one, no mechanism in this schema
> intercepts the omission, and review of this file is the only backstop. Checks 9–11
> decide **structure, format and cardinality only** — never evidence truth. The checks
> verify the **presence and structure** of the annotations and records; they do not
> establish that the evidence is authentic (the evidence is agent-submitted), do
> not prove a test-first development history, and do not assess semantic quality.

> **Freshness.** Every result above describing `tasks.md` or `plan.md` describes it
> as it was when that check ran. If either file is modified afterwards, the results
> computed from it are **STALE** and those checks must be re-run before archive.
> The affected set derives from each check's **inputs**: an edit to `tasks.md` reaches
> **§2, §7 and §8's checks 8–11 and 12**; an edit to `plan.md` reaches **check 12 only**.
> Scope is deliberately those two files — staleness for the checks reading `specs/`,
> `design.md`, commit state or `docs/` is not addressed here and must not be claimed
> to be — except check 13, which states its own staleness rule (13.F) over the main
> specs and the change's delta files (§9). This is agent-executed like the checks
> themselves: **nothing in this schema detects a stale result.**

---

## 9. Identity Integrity — Check 13

Reports the verify instruction's check 13 (Requirement / Scenario heading identity). A BLOCK
here means the change is not verified for archive.

Check title, copied from the schema — do not paraphrase:

13. **Identity integrity** (deterministic in what it decides, agent-executed like checks 8-12; BLOCKs are of two kinds)

**Verdict**:

- [x] ✓ PASS — preview 成功，13.C／13.D 沒有任何 finding，13.E 每一項比對都完成且一致
- [ ] ⛔ BLOCK — 至少一項 finding（見下方兩表）

**Archive preview (13.B)**: copied the repository's whole `openspec/` into a fresh directory in the session scratch (outside the working tree) and ran `openspec archive task-prefixed-plan-headings -y` there (CLI 1.3.1, no other flags). Output: `plan-contract: update` (+1 added), `release-versioning: create` (+4 added), `Totals: + 5, ~ 0, - 0, → 0`, `Change 'task-prefixed-plan-headings' archived as '2026-10-08-task-prefixed-plan-headings'`. Exit 0; `changes/task-prefixed-plan-headings/` gone; `changes/archive/2026-10-08-task-prefixed-plan-headings/` present → **preview succeeded**. The repository's own `openspec/` was not modified (`git status` unchanged).

**13.C** (all six candidate main specs: `contract-identity`, `plan-contract`, `release-versioning`, `repo-guidance`, `tdd-claim-accuracy`, `tdd-evidence-contract`): every requirement and scenario heading matches the grammar, every scenario's `<REQ-ID>` equals its block's ID, no repeated requirement ID per file, no repeated scenario ID per block. No finding.

**13.D** (current state; neither capability synced per §3): `plan-contract` ADDED `REQ-4` — largest current numeric ID is `REQ-3`, so 4 > 3 ✓; it is not an ID the main spec already holds ✓; its scenarios `S1`–`S10` are under a new requirement (empty current set, no leading zeros) ✓. `release-versioning` is a new capability (empty current sets): `REQ-1`–`REQ-4`, scenarios `REQ-n-S1…` ✓. No MODIFIED, REMOVED or RENAMED entries; no new heading lacks a legal ID. No finding.

**13.E** (stdout only, stderr discarded):

| Comparison | Text | CLI | Result |
|---|---|---|---|
| candidate `contract-identity` requirementCount / scenarios per position | 8 / `[5,4,6,6,2,4,3,5]` | 8 / same | agree |
| candidate `plan-contract` | 4 / `[7,2,2,10]` | 4 / same | agree |
| candidate `release-versioning` | 4 / `[3,1,2,2]` | 4 / same | agree |
| candidate `repo-guidance` | 1 / `[2]` | 1 / same | agree |
| candidate `tdd-claim-accuracy` | 5 / `[3,2,3,1,4]` | 5 / same | agree |
| candidate `tdd-evidence-contract` | 3 / `[2,12,4]` | 3 / same | agree |
| change `plan-contract` ADDED entries / scenarios | 1 / `[10]` | 1 / `[10]` | agree |
| change `plan-contract` MODIFIED / REMOVED / RENAMED | 0 / 0 / 0 | 0 / 0 / 0 | agree |
| change `release-versioning` ADDED entries / scenarios | 4 / `[3,1,2,2]` | 4 / same | agree |
| change `release-versioning` MODIFIED / REMOVED / RENAMED | 0 / 0 / 0 | 0 / 0 / 0 | agree |

Check 13 的 BLOCK 分兩種、彼此不吸收：同一個 count mismatch 可能同時產生
VIOLATION 與 UNDETERMINABLE 兩種 finding，兩張表都要分別列出，**不得**
合併寫成一句「ID verification failed」。

**VIOLATION findings**（check 完整跑完某條規則後發現違反 REQ-1～REQ-4，
或一個可靠配對的 13.E 比對結果不一致）：

| 依據（13.C / 13.D / 13.E） | 檔案 / heading / 位置 | 說明（雙方數值或內容） |
|---|---|---|
| 無 | — | — |

**UNDETERMINABLE findings**（check 無法可靠跑完——preview 失敗、CLI 輸出
缺資料或形狀不符、配對不可靠；未跑完本身不是違規，也不得記成違規）：

| 依據（13.B / 13.E） | 對象 | 說明 |
|---|---|---|
| 無 | — | — |

Staleness (13.F): this result describes the main specs and the change's delta files as of 2026-10-08 11:42. Any later edit to either requires re-running check 13.

**宣稱邊界摘要**（僅摘要，不重述規範文字；完整定義見
openspec-schemas repository 的 `openspec/specs/contract-identity/spec.md` 的 REQ-8，
<https://github.com/azuma520/openspec-schemas/blob/main/openspec/specs/contract-identity/spec.md>
——該 spec **不隨** `superpowers-bridge/` bundle 內含，單獨複製 bundle 的專案裡沒有這個檔）：check 13 是一組
決定論、機器可判的規則，由 verify agent 依 instruction 執行；它不是
harness 層強制、不可繞過的 archive-time gate——verify agent 沒跑它時，本
schema 沒有機制攔截這個疏漏。它只確立 candidate state 與本 change 在
13.C 到 13.E 範圍內的結論，**不**確立「退役的 ID 不會被重新配用」、「一個
scenario ID 不會透過 MODIFIED 全文替換或 archive 悄悄消失」、「同一個 ID
底下的語意沒有被弱化」，或「capability 改名後 ID 存活」。

---

## 10. Task-level evidence spot-checks (carried here because the ledger is git-excluded and will be deleted)

| Task | What this verifier checked itself | Result |
|---|---|---|
| 2.4 / 3.2 | `schema.yaml` line 2 `version: 4`; `VERSION` bytes `4.0.0\n` | ✓ |
| 3.1 | `templates/plan.md` entry headings | ✓ `## Task 1.1 —`, `## Task 1.2 —`, `## Task 2.1 —`; no legacy example heading |
| 3.3 / REQ-2 | bridge README: no "tagged" / "tag `vN`" / `v3.0.0` / "created at release" text; current-release sentence is rule-form | ✓ |
| 3.3–3.4 / REQ-3 | Compatibility rows en and zh-TW | ✓ identical; v4 row `` | v4 | `1.14.0` | `v5.1.0` | pending | ``; below-table note says "not a compatibility guarantee" |
| 3.5 local | ran the step's `grep -E '^\| v4 \| `'` + `awk -F'`'` against the working-tree README | ✓ `1.14.0` / `v5.1.0` |
| 3.5 remote | `gh run view 37723513752`: `workflow_dispatch`, branch `feat/task-prefixed-plan-headings`, head `0b11be5`, completed / success; log line `Pinned in README: OpenSpec=1.14.0, Superpowers=v5.1.0` | ✓ (side effect per ledger: the run opens/updates the drift issue, as weekly) |
| 3.8 / REQ-4 | `git log -S 'version: 4' -- superpowers-bridge/schema.yaml` → only `0b11be5`; its parent is `737aa56ecfd3f2fc9c5562fbdd82e8d005ca14a2`; `git show 737aa56…:superpowers-bridge/schema.yaml` line 2 `version: 3`; that SHA appears twice in each bridge README; `V3_ROLLBACK_SHA_PLACEHOLDER` has 0 occurrences in tracked md/yaml | ✓ (I read the tree with `git show`; the one-time checkout REQ-4 asks for is recorded in the ledger: throwaway `git worktree add --detach` → `version: 3`, `VERSION` 3.0.0 **(ledger)**). The SHA stays valid only if the branch is merged without squash/rebase |
| 4.1 | `openspec schema validate superpowers-bridge` → valid, `openspec schemas` lists it, CLI 1.3.1 | **(ledger)**; see §5 — the installed copy's two READMEs have drifted since |
| 4.2 | ran Superpowers **6.4.1** `skills/subagent-driven-development/scripts/task-brief` (path `C:/Users/user/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/…`) on this plan.md for entries 2.2 (non-final) and 4.2 (final) | ✓ 2.2: 7 lines, identical line for line to the plan entry (heading through the blank line before the next `##`); 4.2: 5 lines, identical — plan.md has no trailing non-entry text, so the "final entry swallows trailing text" limitation is **not exercised** by this plan. Ledger run (entries 1.1–1.3, 4.2 at `737aa56`) agrees **(ledger)** |

**Deferred items and their rulings** (from the ledger; status as of this verify):

| Item | Ruling / status |
|---|---|
| Check 12's asymmetry rationale says what upstream `task-brief` honours without "as of Superpowers v6.4.1" | **R15 — deferred.** Editing check 12 would change the `79d796db` text the GREEN and 2.5 runs are bound to. Reads as a timeless claim about upstream |
| REQ-4-S6 `## Tasks 1.1` / `## Task1.1` have no fixtures | R3 — deferred (scope) |
| Multi-case blind deliveries vs "one fixture" protocol; `subject:` paths relative | R14 — recorded here, not edited |
| f16 plan title "(second heading)" hints the duplicate | Not changed (RED already bound to its sha); harmless, the key is what is tested |
| Fixtures README intro (~line 32) still says "schema v2 … checks 8–12" only; design-note bullet mixing f16 note with classification; re-review nits (step 3 wording implicit, item-1 location phrasing) | Deferred minors (group 1); not re-checked here |
| "such a token alone" readable as whole-line; stage one / tasks instruction say "key leading … entry heading"; "backtick fenced code block" may evoke CommonMark; check 12 names near-miss forms literally | Deferred minors (group 2) |
| README ~580 "since v2" vs ~656 "since v1 row" phrasing | Deferred minor (group 3), both true |
| Roadmap "v4 — Released" heading before the tag exists | R8 — kept; D6 completion still gates the work-map record |
| v3-supp note merges the f18/f19 ambiguity notes | Out of scope (final re-review) — left |
| Resolved, for the record: design D5 overclaim (fixed, final fix item 8); version-check drift-issue "Last verified" text (R10, fixed); CLAUDE.md CI bullet (final fix item 4); README exception-2 "only as missing keys" overclaim and CLAUDE.md recovery step (R16, fixed) | Fixed in working tree, uncommitted |
| `/codex-review-doc` for the edited docs | **Not yet run** at the time of writing |

---

## openspec-verify-change scorecard

| Dimension | Status |
|---|---|
| Completeness | 18/18 tasks; 2 capabilities, 5 requirements (plan-contract REQ-4; release-versioning REQ-1–4) |
| Correctness | 5/5 requirements have implementation evidence (schema.yaml Plan Contract + check 12 + check 13 sentence; READMEs, VERSION, version-check.yml, CLAUDE.md, roadmap). REQ-1 (tag) is post-archive by design. Scenario coverage gaps listed in §4 (S5, S8, S9, S10; two S6 forms) |
| Coherence | Followed; warnings in §4 |

CRITICAL: none. WARNINGS: §4 (CI validate not run on branch; scenario/fixture gaps), §5 (uncommitted edits; installed copy README drift), §6 (pre-existing files), doc review pending.

---

## Overall Decision

- [ ] ✅ PASS — 可進入 finishing-a-development-branch 與 archive
- [x] ⚠️ PASS WITH WARNINGS — 可進入後續步驟但需注意：checks 1–13 have no BLOCK, but check 5 is **not met** (8 modified files uncommitted, plus this file), the installed schema copy's two READMEs differ from the source, `validate-schemas.yml` has not run on this branch, and `/codex-review-doc` has not run on the edited docs. Evidence for 2.2 / 2.5 is agent-executed instruction-layer behaviour, with the limits listed in §8.
- [ ] ❌ FAIL — 返回失敗的 artifact 修正後重跑 verify

**下一步**：

1. Run `/codex-review-doc` on the edited docs (and this file). If it leads to any edit of `tasks.md` or `plan.md`, re-run §2, §7, §8 per Freshness; any edit to the delta specs or main specs re-runs §9.
2. Re-sync `openspec/schemas/superpowers-bridge/` from `superpowers-bridge/` (`diff -r` must be empty).
3. Commit the working-tree edits (needs the user's per-use authorisation), push, and either dispatch `validate-schemas.yml` on the branch or let the PR to `main` run it; record the result.
4. Retrospective, then archive (Windows: copy + `diff -r` + user deletes the source dir).
5. After archive, the release commit, annotated tag `v4.0.0`, push with authorisation, and confirm `refs/tags/v4.0.0^{}` on the remote equals the release commit before closing the work-map record (D6) — not part of this change's tasks.
