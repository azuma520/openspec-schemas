# Verification Report

> 此檔案由 `openspec-verify-change` skill 在 apply 完成後產生，用以確認實作
> 與 specs / design / tasks 的一致性。失敗的檢查須返回對應 artifact 修正後
> 再重跑 verify。

**Change**: `fix-executing-plans-rationale`
**Verified at**: `2026-10-06 15:47`
**Verifier**: 獨立 verify subagent（Claude Opus 5.5；未參與實作），依 `openspec instructions verify` 的 check 1–13 與 `openspec-verify-change` skill 執行

**PRECHECK — implementation evidence**（兩項皆 > 0，繼續）：

```text
$ git log --oneline $(git merge-base HEAD origin/main 2>/dev/null || git merge-base HEAD origin/master 2>/dev/null)..HEAD | wc -l
19
$ grep -c '^- \[x\]' openspec/changes/fix-executing-plans-rationale/tasks.md
7
```

（19 是 `origin/main`（`0cd728e`）到 HEAD 的全部本地 commit；屬於本 change 的實作 commit 只有 HEAD `9ef62c2`，見 §5。）

---

## 1. Structural Validation (`openspec validate --all --json`)

- [x] 全數 items `"valid": true`

**結果**：

```text
$ openspec validate --all --json 2>/dev/null   # exit 0
totals: {'items': 6, 'passed': 6, 'failed': 0}
byType: {'change': {'items': 1, 'passed': 1, 'failed': 0}, 'spec': {'items': 5, 'passed': 5, 'failed': 0}}
contract-identity               spec   valid=True  (8 INFO: "Requirement text is very long")
fix-executing-plans-rationale   change valid=True  (0 issues)
plan-contract                   spec   valid=True  (1 INFO)
repo-guidance                   spec   valid=True  (0 issues)
tdd-claim-accuracy              spec   valid=True  (1 INFO)
tdd-evidence-contract           spec   valid=True  (2 INFO)
```

所有 issue 都是 `INFO` 等級（requirement 文字超過 500 字的建議），沒有 ERROR / WARNING。

另依 plan 3.2 跑 bundle 結構驗證：

```text
$ diff -rq superpowers-bridge openspec/schemas/superpowers-bridge   # 無輸出，exit 0
$ openspec schema validate superpowers-bridge
✓ Schema 'superpowers-bridge' is valid                               # exit 0
$ openspec schemas | grep -n superpowers-bridge
7:  superpowers-bridge (project)
```

| Item | Type | Issues |
|---|---|---|
| — | — | — |

---

## 2. Task Completion (`tasks.md`)

- [x] 所有 task 的 checkbox 皆為 `- [x]` 或 `- [~]`
      （7 個 task 行全為 `- [x]`；無 `- [ ]`、無 `- [~]`）

**未完成任務**（若有）：

| Task | 未完成原因 | 是否阻塞 archive |
|---|---|---|
| — | — | — |

逐項對照 plan.md 的 Acceptance（獨立查核，非照抄 tasks 的勾選）：

| Task | Acceptance 查核 | 結果 |
|---|---|---|
| 1.1 | `schema.yaml:8-12` 不再含「dispatches no independent reviewer」；改為「no reviewer per task, and without subagents its one final review is done by the author」；不引用上游建議；schema validate 通過 | ✓ |
| 1.2 | `schema.yaml:1708-1718`：每句可對到 REQ-3 或 executing-plans 6.4.1 原文（`SKILL.md:8-10`、`:253-258`）；「upstream itself directs users…」已刪；TDD 句改為經 tasks.md 標註與證據契約承載；`spec-driven` 指引保留 | ✓ |
| 2.1 | README.md 三段（:312、:462、:660）已改；`git show HEAD` 的 hunk 只在 :309、:451、:459、:657，查核紀錄列 :563–564、:605 未動 | ✓ |
| 2.2 | README.zh-TW.md 同三段與英文版逐段同論點（含 §4 的「每個 task、或每批同類小 task」）；查核紀錄列未動 | ✓ |
| 2.3 | 兩份 README §2 不再含「schema doesn't change」/「本 schema 不用改」（`rg` 0 命中）；PRECHECK 只限定於「必要」skill，並明示只點名的 skill（如 `test-driven-development`）不會被擋 | ✓ |
| 3.1 | `CLAUDE.md:252` 仍以 ❌ 開頭、仍禁止加 fallback；含指向正式設計 §5 與 `task-20260901-claudemd-governance-rewrite` 的預告句；舊說法只以「8/31 寫的…當時成立、v6.4.1 起不成立」的明示失效引用出現 | ✓ |
| 3.2 | 同步、validate 見 §1；殘留搜尋見下 | ✓ |

**3.2 殘留搜尋**（排除 `openspec/changes/archive/`；每筆命中標類別）：

```bash
for p in 'dispatches no independent reviewer' 'dispatches no' \
  'directs users to `subagent-driven-development`' 'directs users to subagent-driven-development' \
  '不派任何獨立審查者' '上游自己' 'self-checks' 'whenever subagents are available' \
  'does not travel through either'; do rg -n -F "$p" -g '!openspec/changes/archive/**' .; done
```

| 命中位置 | 類別 |
|---|---|
| `openspec/specs/tdd-claim-accuracy/spec.md:64-67` | 歸檔時由本 change delta 取代的 living spec（archive preview 已確認取代，見 §9） |
| `superpowers-bridge/README.md:605-606`（S13 / S14 列） | README 查核紀錄列 |
| `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/…`、`2026-09-03-loosen-plan-sdd-reports/…` | 歷史報告 |
| `docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/**/schema-*.yaml`、`poc/2026-10-02-issue2-compat-spike/raw/…` | 實驗快照 |
| `文檔/handoff/session-handoff-20260827.md`、`session-handoff-20261006.md` | handoff |
| `openspec/changes/fix-executing-plans-rationale/{proposal,design,brainstorm,plan,tasks}.md`、`specs/…/spec.md` | 本 change 描述舊說法的文件 |
| `CLAUDE.md:252`（「不派任何獨立審查者」） | 新文字中明示「v6.4.1 起不成立」的引用 |

沒有落在四類以外的命中。

---

## 3. Delta Spec Sync State

| Capability | Sync 狀態 | 備註 |
|---|---|---|
| `tdd-claim-accuracy` | ✗ Needs sync | main spec `openspec/specs/tdd-claim-accuracy/spec.md:61-87` 仍是舊 REQ-3（「it dispatches no independent reviewer, and upstream itself directs users to subagent-driven-development」，只有 S1、S2）；delta 為 MODIFIED REQ-3（含新增 S3）。尚未 archive，屬正常狀態，由 `openspec archive` 合入 |

---

## 4. Design / Specs Coherence Spot Check

| 抽樣項 | design 描述 | specs 對應 | 差距 |
|---|---|---|---|
| D1 規格先行 | REQ-3 為唯一理由 owner，表面跟規格 | delta 改寫 REQ-3；S1/S3 點名 schema.yaml、兩份 README、CLAUDE.md 紅旗 | 無 |
| D2 理由只寫審查結構 | (a) 無每任務審查、最後審一次；(b) 無 subagent 時作者自審；apply 依賴執行中審查（可合批） | REQ-3 第一段逐點對應；S1 寫明「may batch small same-shape tasks — not one-reviewer-per-task」；SHALL NOT 依上游建議 | 無 |
| D3 TDD 段保留結論改推理 | 經 tasks.md 標註＋證據契約送達，刪「不經過任何一個執行者」 | REQ-3 第二段；S2 | 無 |
| D4 預告句只放 CLAUDE.md | — | spec 不規範預告句（屬維護者面），與 design 一致；實作也只在 CLAUDE.md:252 加 | 無 |

**上游事實查核**（本 verifier 直接讀安裝檔，非轉述）：

```text
$ md5sum .../claude-plugins-official/superpowers/{6.3.0,6.4.1}/skills/executing-plans/SKILL.md \
         .../superpowers-marketplace/superpowers/{6.4.1,6.4.2}/skills/executing-plans/SKILL.md
c4230e0d014235b8741efc9ad75177a3  6.3.0 (64 行)
b0376b13b41e77a8bd1cece870dec5ea  6.4.1 official (373 行)
b0376b13b41e77a8bd1cece870dec5ea  6.4.1 marketplace
b0376b13b41e77a8bd1cece870dec5ea  6.4.2 marketplace
```

| 宣稱 | 上游原文 | 判定 |
|---|---|---|
| 沒有每個任務的審查，最後審整條分支一次 | 6.4.1 `executing-plans/SKILL.md:8-10`「no implementer subagent per task, no reviewer per task. One fresh-context review of the whole branch at the end.」 | ✓ |
| 有 subagent 時最後派獨立審查者 | `:240-251`「With a subagent tool: dispatch the reviewer…」 | ✓ |
| 無 subagent 時作者自審 | `:253-258`「Without a subagent tool: … perform that review yourself … a self-review by the author is weaker…」 | ✓ |
| 「在同一個 context 做完所有 task」（README §4） | `:8`「Execute the plan yourself, task by task, in this session」 | ✓ |
| executing-plans 無條件載入 TDD（design D3） | `:149`「REQUIRED SUB-SKILL: load superpowers:test-driven-development now」 | ✓ |
| SDD 端 TDD 為條件式（design D3） | 6.4.1 `subagent-driven-development/implementer-prompt.md:36`「following TDD if task says to」 | ✓ |
| SDD 可合批同類小任務（design D2、schema.yaml:1701-1705） | 6.4.1 `subagent-driven-development/SKILL.md:222-229`「Batch small same-shape work…」 | ✓ |
| 上游把兩條路當使用者挑選（舊說法②失效） | 6.4.1 `writing-plans/SKILL.md:177-182`（Subagent-driven / Native 二選一並推薦其一）；`executing-plans/SKILL.md:3`、`:60-61` | ✓ |
| 6.4.1 與 6.4.2 一致 | 上方 md5 相同 | ✓ |
| v6.3.0 沒有最後審查、且說有 subagent 就改用 SDD | 6.3.0 `SKILL.md:14`；全文 64 行無任何 reviewer 派發 | ✓ |
| CLAUDE.md:252「查過的舊版（v5.1.0、v6.3.0）連最後那次都沒有」 | v6.3.0 已親查成立；**v5.1.0 本機未安裝，本 verifier 未親查**，此半句的來源是 spike 報告 `docs/superpowers/poc/2026-10-02-issue2-compat-spike/report.md:178` 的 `grep -c` 計數 | 【未親查】部分 |

**漂移警告**（非阻塞）：

- brainstorm.md:87（Q3）寫「bridge 的 apply 依賴『每個任務都有獨立審查』」，比 spec / design 的定稿（「每個任務，或每批同類小任務」）嚴。brainstorm 是原始紀錄，下游 artifact 與實作都已採較精確的說法，不影響實作；記錄供 retrospective 參考。

---

## 5. Implementation Signal

- [x] Worktree 內無未 staged 的檔案（`git status --porcelain | wc -l` → `0`）
- [ ] 所有相關 commit 已推送 —— **未推送**：`git rev-list --count origin/main..HEAD` → `19`。推送屬使用者決定，不阻塞 verify

**Commit 範圍**：`a136720..9ef62c2`（單一實作 commit `9ef62c2 fix(bridge): correct executing-plans exclusion rationale for Superpowers v6.4.1`，11 files, +413 / −15；實作檔為 `CLAUDE.md`、`superpowers-bridge/{README.md,README.zh-TW.md,schema.yaml}`，其餘為本 change 的 artifacts）

---

## 6. Front-Door Routing Leak Detector（warning,非阻塞）

設計產出不應落在 `docs/superpowers/specs/`(brainstorm artifact 的
output redirection 會把它導到 `openspec/changes/<name>/brainstorm.md`)。

偵測:

```bash
$ ls docs/superpowers/specs/*.md 2>/dev/null
docs/superpowers/specs/2026-05-02-openspec-schemas-monorepo-design.md
docs/superpowers/specs/2026-08-27-bridge-guarantee-architecture-direction.md
docs/superpowers/specs/2026-08-28-concept-poc-traceability-gate-design.md
docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md
docs/superpowers/specs/2026-09-23-formal-design-revision-map.md
```

- [x] 無檔案,或存在的檔案是 schema 安裝前的合法存留

**WARNING（按 check 6 規定記錄）**：Front-door routing leak detector 命中 5 個檔案。判讀：這 5 份都是本 repo 維護者的設計文件（repo `CLAUDE.md`「結構約定」明列 `docs/superpowers/specs/` 為維護者 design spec 存放處），最近一次異動是 `6e6b2fb`（2026-09-29），**本 change 的 commit 沒有新增或修改任何一份**（`git show --stat HEAD` 未列出該目錄）。屬合法的非 schema 用途，非本 change 造成的洩漏。

**洩漏清單**（若有）：

| 檔案 | 內容是否已 captured 進 change | 建議動作 |
|---|---|---|
| 上列 5 份 | 不適用——非本 change 產出，是 repo 的維護者設計文件 | 不動 |

> 不會擋住 archive。新的 schema-installed cycle 產生的洩漏,應搬進
> `openspec/changes/<name>/brainstorm.md` 或 `design.md` 後刪原檔。

---

## 7. Deferred Dogfood vs Automated-Test Equivalence

tasks.md 存在，且沒有任何以 `- [~]` 開頭的任務行（見 §8 的判定腳本輸出 `deferred []`）。本節空白即 PASS。

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

判定方式：以 Python 依 instruction 的 TASK LINE / BELONGS TO / 空行透明規則逐行解析 tasks.md 與 plan.md（`##` 恰好一層、token 兩側定界）。輸出：

```text
('x', '1.1', 1, ['- TDD: n/a — prose-only：YAML 註解文字，無可單元測試的行為；正確性由 REQ-3 逐句對照與外部審查判定'], [])
('x', '1.2', 1, ['- TDD: n/a — prose-only：instruction 文字，schema validate 不讀 prompt 內容；正確性由 REQ-3 逐句對照與外部審查判定'], [])
('x', '2.1', 1, ['- TDD: n/a — prose-only：說明文件'], [])
('x', '2.2', 1, ['- TDD: n/a — prose-only：說明文件翻譯'], [])
('x', '2.3', 1, ['- TDD: n/a — prose-only：說明文件'], [])
('x', '3.1', 1, ['- TDD: n/a — prose-only：維護者守則'], [])
('x', '3.2', 1, ['- TDD: n/a — configuration / 查驗：同步與結構驗證，無新行為'], [])
tasks ['1.1', '1.2', '2.1', '2.2', '2.3', '3.1', '3.2']
plan ['1.1', '1.2', '2.1', '2.2', '2.3', '3.1', '3.2']
dup tasks [] dup plan []
only tasks set() only plan set()
unchecked [] deferred []
```

（欄位：checkbox、task number、符合 check 8 形式的標註行數、標註內容、RED/GREEN 紀錄行。）

**Per-task results** (one row per `- [ ]` / `- [x]` / `- [~]` task line in `tasks.md`):

| Task | Annotation (8) | Records, fields + subject grammar (9) | Outcome markers (10) | Subject pairing (11) | Review judgement (R1–R4) |
|---|---|---|---|---|---|
| 1.1 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 理由成立（被改的是 YAML `description:` 純文字值；見下方 suggestion）；R4 無紀錄 |
| 1.2 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立（instruction prompt 文字，validate 不讀）；R4 無紀錄 |
| 2.1 | ✓ `TDD: n/a — prose-only：說明文件` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 2.2 | ✓ `TDD: n/a — prose-only：說明文件翻譯` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 2.3 | ✓ `TDD: n/a — prose-only：說明文件` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 3.1 | ✓ `TDD: n/a — prose-only：維護者守則` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 3.2 | ✓ `TDD: n/a — configuration / 查驗…` | N/A | N/A | N/A | ✓ R3 成立（同步＋結構驗證，無新行為）；R4 無紀錄 |

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
| `tasks.md` task numbers | — | ✓ |
| `plan.md` entry keys | — | ✓ |

**Check 12, stage two — set equality in both directions** (both differences must be empty):

| `tasks.md` task numbers | `plan.md` entry keys | Only in tasks (no entry) | Only in plan (no task) | Verdict |
|---|---|---|---|---|
| `{1.1, 1.2, 2.1, 2.2, 2.3, 3.1, 3.2}` | `{1.1, 1.2, 2.1, 2.2, 2.3, 3.1, 3.2}` | — | — | ✓ |

> Stage one does **not** short-circuit — stage two is evaluated and recorded whatever
> stage one found, and the two messages stay distinct because the repairs differ
> (renumber one of two duplicates; add or remove a key for a missing/extra one).
> Also BLOCK: a task line carrying no task number, no collectable entry key, or no
> plan.md at all — record the last as "plan.md absent — no entry keys to compare",
> never as a set difference.

**Blocking findings** (deterministic checks and review judgements):

- 無

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

**13.B Archive preview**（`<tmp>` = scratchpad 下的 `verify/preview/`，在 repo working tree 之外；複製整個 `openspec/` 後執行）：

```text
$ cd <tmp> && openspec archive fix-executing-plans-rationale -y      # exit=0
Task status: ✓ Complete
Specs to update:
  tdd-claim-accuracy: update
Applying changes to openspec/specs/tdd-claim-accuracy/spec.md:
  ~ 1 modified
Totals: + 0, ~ 1, - 0, → 0
Specs updated successfully.
Change 'fix-executing-plans-rationale' archived as '2026-10-06-fix-executing-plans-rationale'.
$ ls <tmp>/openspec/changes/                 → archive/   （change 目錄已不存在）
$ ls <tmp>/openspec/changes/archive | grep fix-executing → 2026-10-06-fix-executing-plans-rationale/
```

三條件（exit 0、change 目錄消失、archive 目錄存在）全部成立 → preview SUCCEEDED。repo 自身 `openspec/` 未被修改（之後 `git status --porcelain` 為空）。check 3 記錄為 ✗ Needs sync，非 synced，故無 13.B SYNCED CAPABILITY 情形。

**13.C Candidate state**：對 `<tmp>/openspec/specs/*/spec.md` 五個 capability 逐行以 13.A 規則讀 heading（字面比對、不辨識 fenced code）：無不合文法的 requirement / scenario heading、無 scenario ID 與所屬 requirement 不符、無重複 requirement ID、無同一 requirement 下重複 scenario ID。candidate 的 `tdd-claim-accuracy` REQ-3 下為 `REQ-3-S1`、`REQ-3-S2`、`REQ-3-S3`。

**13.D Current state**：唯一 delta 為 `tdd-claim-accuracy` 的 MODIFIED `REQ-3`。
- 13.D.1：依 (b) 以 ID `REQ-3` 解析到 main spec `REQ-3`（同一 contract）。無 ADDED、無 RENAMED。
- 13.D.2：無 RENAMED pair，不適用。
- 13.D.3：新 scenario 為 `REQ-3-S3`（main spec 的 REQ-3 只有 S1、S2，目前最大 2）；`3 > 2` ✓。`S1`、`S2` 為既有 ID。無新 requirement ID。

**13.E Cross-check against the CLI**（只讀 stdout，`2>/dev/null`）：

```text
# change-level half（repo root）
$ openspec show fix-executing-plans-rationale --json --deltas-only 2>/dev/null   # exit=0
deltas: [ {spec: tdd-claim-accuracy, operation: MODIFIED, requirement.scenarios: 3} ]
text count: MODIFIED requirement headings = 1, scenarios under it = 3     → 一致

# candidate-state half（<tmp>，preview 之後；每個 capability `openspec show <cap> --type spec --json`，全部 exit=0）
contract-identity      text reqs 8 cli 8 | scen text [5,4,6,6,2,4,3,5] cli [5,4,6,6,2,4,3,5] | match True
plan-contract          text reqs 3 cli 3 | scen text [7,2,2]           cli [7,2,2]           | match True
repo-guidance          text reqs 1 cli 1 | scen text [2]               cli [2]               | match True
tdd-claim-accuracy     text reqs 5 cli 5 | scen text [3,2,3,1,4]       cli [3,2,3,1,4]       | match True
tdd-evidence-contract  text reqs 3 cli 3 | scen text [2,12,4]          cli [2,12,4]          | match True
```

**VIOLATION findings**：

| 依據（13.C / 13.D / 13.E） | 檔案 / heading / 位置 | 說明（雙方數值或內容） |
|---|---|---|
| 無 | — | — |

**UNDETERMINABLE findings**：

| 依據（13.B / 13.E） | 對象 | 說明 |
|---|---|---|
| 無 | — | — |

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

本結果描述 2026-10-06 15:47 時的 main specs 與 delta file；之後若任一被編輯，結果即過期，須重跑 check 13（13.F）。

---

## Skill 三維度摘要（`openspec-verify-change`）

| Dimension | Status |
|---|---|
| Completeness | 7/7 tasks；1 requirement（MODIFIED REQ-3，3 scenarios） |
| Correctness | REQ-3 在 5 個表面皆有實作（`schema.yaml:8-12`、`:1708-1718`；`README.md:312`、`:462`、`:660`；`README.zh-TW.md` 同行；`CLAUDE.md:252`）；S1/S2/S3 逐表面閱讀符合 |
| Coherence | design D1–D6 皆被遵循（D6：查核紀錄列 :563-564、:605 未動） |

**CRITICAL**：無。

**WARNING**：
- §6 Front-door routing leak detector 命中 5 份既有維護者設計文件（非本 change 產出，不需動作）。
- §5 commit 尚未推送（`origin/main..HEAD` = 19）。

**SUGGESTION**（非阻塞，皆不需在本 change 修）：
- `tasks.md:3`、`plan.md:21-24` 把 `schema.yaml:8-12` 稱為「檔頭 Requirements 註解」，實際上是 YAML `description:` 的折疊字串值（`schema.yaml:3` `description: >`），不是註解。不影響實作正確性，但「註解」一詞會讓讀者以為 CLI 不讀它（CLI 其實會讀 description）。可在 retrospective 記一筆。
- `README.md:608` / `README.zh-TW.md:608`（2026-10-02 查核紀錄段）仍寫「Two follow-ups are registered: rewrite the rationale for refusing `executing-plans`…」。這是帶日期的歷史紀錄、本 change 依 D6 不改是對的；但讀者看不到「這條後續已由本 change 完成」。可考慮之後在查核紀錄新增一列（append，不改舊列）註明 S13/S14 理由已於本 change 修正。
- `README.md:312`、`:462` 的 SKILL.md 連結指向 `obra/superpowers` 的 `main`，但文字寫「Superpowers v6.4.1–v6.4.2」；上游 `main` 之後若再改，連結內容會與版本註記脫鉤。可改指向 tag（如 `blob/v6.4.2/…`）。
- `CLAUDE.md:252` 的「v5.1.0 連最後那次都沒有」本 verifier 未親查（本機無 v5.1.0），依據為 spike 報告 `report.md:178` 的計數；v6.3.0 那半已親查成立。

---

## Overall Decision

- [ ] ✅ PASS — 可進入 finishing-a-development-branch 與 archive
- [x] ⚠️ PASS WITH WARNINGS — 可進入後續步驟但需注意：check 1–5、7–13 全部通過、無 blocking finding；警告僅為 §6 leak detector 命中 5 份既有維護者設計文件（非本 change 造成）與 §5 commit 尚未推送；另有 4 條 suggestion（見上）
- [ ] ❌ FAIL — 返回失敗的 artifact 修正後重跑 verify

**下一步**：

產出 `retrospective` artifact（須依 design D5 在「Deliberately Skipped Skills」誠實記錄未走 worktree / SDD 的偏離，並可順帶記錄上方 suggestion 與 §4 的 brainstorm 措辭漂移）；之後由使用者決定推送與 `openspec archive`。若 archive 前再編輯 tasks.md / plan.md 或 spec 檔，依 §8 Freshness 與 13.F 重跑對應檢查。
