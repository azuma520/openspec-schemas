# 補號遷移驗收紀錄（tasks 5.1／5.2）

> 這份是 plan.md §§ 5.1、5.2 的驗收實測紀錄：5.1 同步 dogfood schema 副本、跑三項 CLI 驗收；5.2 在暫存複本對本 change 實跑 `openspec archive`，驗證補號遷移（design D7）後主 spec 的狀態轉換、ID 合法性、標題對照、逐行內容一致性與 CLI 交叉核對。所有指令皆在暫存目錄或本 worktree 跑，未動 repo 內任何 spec／schema，未 `git add`／`commit`。

- 日期：2026-09-30
- OpenSpec CLI：`1.3.1`
- 環境：Windows 11，Git Bash；worktree 根目錄執行 5.1；5.2 的暫存複本在 repo 外的 scratchpad（`archive-rehearsal-1790755689/`）。

## 5.1 — dogfood 副本同步

同步前，`superpowers-bridge/` 與 `openspec/schemas/superpowers-bridge/` 有版本號差異（README 的 v2/v3、check 12/13 等文字未同步）；因副本 gitignored 且 `rm` 被拒、bundle 沒有刪除任何檔案，改用 overlay copy：

```bash
$ cp -R superpowers-bridge/. openspec/schemas/superpowers-bridge/
$ diff -r superpowers-bridge openspec/schemas/superpowers-bridge
(無輸出，exit 0)
```

三項 CLI 驗收：

```bash
$ openspec schema validate superpowers-bridge
Note: Schema commands are experimental and may change.
✓ Schema 'superpowers-bridge' is valid
exit=0

$ openspec schemas
Available schemas:
  spec-driven
    ...
  superpowers-bridge (project)
    ...
exit=0

$ openspec instructions verify --change requirement-scenario-identity | grep -n "13\."
476:13. **Identity integrity** (deterministic in what it decides,
```

三項全過：`diff -r` 空、`schema validate` 通過、`schemas` 列出 `superpowers-bridge (project)`、render 出的 verify instructions 含 check 13 標題。

## 5.2 — 補號遷移驗收

### 暫存複本與歸檔實跑

```bash
TMPCOPY=.../scratchpad/archive-rehearsal-1790755689/
$ cp -R <worktree>/openspec  $TMPCOPY/openspec   # 含已同步的 schemas/superpowers-bridge/

$ cd $TMPCOPY && openspec archive requirement-scenario-identity -y
Proposal warnings in proposal.md (non-blocking):
  ⚠ Consider splitting changes with more than 10 deltas
Task status: 9/12 tasks
Warning: 3 incomplete task(s) found. Continuing due to --yes flag.

Specs to update:
  contract-identity: create
  plan-contract: update
  repo-guidance: update
  tdd-claim-accuracy: update
  tdd-evidence-contract: update
Applying changes to openspec/specs/contract-identity/spec.md:
  + 8 added
Applying changes to openspec/specs/plan-contract/spec.md:
  ~ 3 modified
  → 3 renamed
Applying changes to openspec/specs/repo-guidance/spec.md:
  ~ 1 modified
Applying changes to openspec/specs/tdd-claim-accuracy/spec.md:
  ~ 4 modified
  → 4 renamed
Applying changes to openspec/specs/tdd-evidence-contract/spec.md:
  ~ 3 modified
  → 3 renamed
Totals: + 8, ~ 11, - 0, → 10
Specs updated successfully.
Change 'requirement-scenario-identity' archived as '2026-09-30-requirement-scenario-identity'.
EXIT=0
```

### 狀態轉換證明（不只看結束碼）

`author-run.md` 已實測「結束碼 0 不代表歸檔真的發生」（`u01-modified-no-match` 印 `Aborted. No files were changed.` 但結束碼仍 0）。本次歸檔印出 `Specs updated successfully.` 與具體 `+/~/→` 統計，且：

```bash
$ ls $TMPCOPY/openspec/changes/requirement-scenario-identity
No such file or directory                              ← change 路徑已不存在

$ ls $TMPCOPY/openspec/changes/archive | grep requirement-scenario-identity
2026-09-30-requirement-scenario-identity/               ← 已歸檔
```

狀態轉換確認發生，非假成功。

### ID 合法性 + 數量

逐 capability（腳本比對 `REQ-[A-Z0-9]+` 語法、描述非空、capability 內唯一、scenario 前綴對應到自己的 requirement、`m` 為無前導零正整數）：

| capability | requirements | scenarios | 違規數 |
|---|---|---|---|
| contract-identity | 8 | 35 | 0 |
| plan-contract | 3 | 11 | 0 |
| repo-guidance | 1 | 2 | 0 |
| tdd-claim-accuracy | 4 | 8 | 0 |
| tdd-evidence-contract | 3 | 18 | 0 |

- `plan-contract` + `tdd-claim-accuracy` + `tdd-evidence-contract`：10 requirement／37 scenario，符合預期。
- `repo-guidance`：`REQ-PB` + `REQ-PB-S1`／`REQ-PB-S2`，符合預期。
- `contract-identity`：`REQ-1`–`REQ-8`，符合預期。

0 違規。

### 標題 before → after 對照（四個既有 capability，摘要）

比對方法：逐一取歸檔前快照與歸檔後主 spec 的 `### Requirement:` / `#### Scenario:` 標題，依出現順序配對，確認描述文字（ID 之外的部分）保持不變、只是前面補上了 ID：

| capability | requirement 對照 | scenario 對照 |
|---|---|---|
| plan-contract | 3/3 對照成功，描述文字一致 | 11/11 對照成功，描述文字一致 |
| repo-guidance | 1/1（`event-gated schema work boundary` → `REQ-PB event-gated schema work boundary`） | 2/2（`REQ-PB-S1`／`S2`） |
| tdd-claim-accuracy | 4/4 對照成功，描述文字一致 | 8/8 對照成功，描述文字一致 |
| tdd-evidence-contract | 3/3 對照成功，描述文字一致 | 18/18 對照成功，描述文字一致 |

完整逐條 before→after 清單見本次量測的暫存腳本輸出（未落地為 repo 檔案，已記錄於 task-5.1-5.2-report.md）；標題文字本身未發現被竄改或遺漏。

### 逐行內容一致性（除標題行外）

去除兩側 `### Requirement:` / `#### Scenario:` 行後逐行 diff：

| capability | 結果 |
|---|---|
| plan-contract | 完全一致 |
| tdd-claim-accuracy | 完全一致 |
| tdd-evidence-contract | 完全一致 |
| repo-guidance | **有差異**（見下） |

`repo-guidance` 的差異：

```diff
--- repo-guidance-pre
+++ repo-guidance-post
@@ -5,9 +5,7 @@
 Keep CLAUDE.md's schema-work boundary stated as an answerable event gate rather than a time
 phase. Established by change `claude-md-phase-boundary` (2026-08-28, Phase 2 specimen of the
 traceability-gate concept PoC).
-
 ## Requirements
-
 CLAUDE.md SHALL state the schema-work boundary as an event gate: Orca is
 ...
@@ -21,3 +19,4 @@
 
 - **WHEN** the restated section lands
 - **THEN** modifying schema.yaml or adding a formal artifact type is still forbidden until both gate events are YES
+
```

即歸檔前 `## Requirements` 標題後、以及 `### Requirement:` 前各有一行空白行，歸檔後這兩行空白行消失；同時檔案結尾多了一行空白行。3 處差異都是純空白行，沒有任何字元內容變化。

### 補測：標題與空白行都排除後的 diff（本次追加）

為了直接對到 design D7 保護的內容主張（「內容不變」），另外把上面的比對再排除空白行（兩側都先濾掉 `### Requirement:` / `#### Scenario:` 行，也濾掉純空白行）再 diff：

```bash
$ python check_blank_insensitive.py
repo-guidance blank+heading-insensitive diff identical: True
(diff output empty — no differences beyond heading lines and blank lines)
```

**結果為空**：`repo-guidance` 在排除標題行與空白行後，逐行內容 100% 一致。另外，控制端已測過移除 delta 檔（`openspec/changes/.../specs/repo-guidance/spec.md`）結尾的多餘空白行不影響此空白行位移（drift 不變），排除了 delta 檔尾端換行是根因的可能。

### CLI 交叉核對

`openspec show <cap> --type spec --json` 的 `requirementCount` 與逐 requirement `scenarios.length`，對照文字逐行數：

| capability | requirementCount (CLI) | 各 requirement 的 scenario 數（CLI） | 各 requirement 的 scenario 數（文字數） |
|---|---|---|---|
| contract-identity | 8 | 5,4,6,6,2,4,3,5 | 5,4,6,6,2,4,3,5 |
| plan-contract | 3 | 7,2,2 | 7,2,2 |
| repo-guidance | 1 | 2 | 2 |
| tdd-claim-accuracy | 4 | 3,2,2,1 | 3,2,2,1 |
| tdd-evidence-contract | 3 | 2,12,4 | 2,12,4 |

全部一致，CLI 交叉核對通過。

## 判定

**Approved deviation（2026-09-30 使用者核可）**：plan 5.2 原定「除 ID 標題外逐行一致」未字面達成；`repo-guidance` 經 `openspec archive` 後有 3 行純空白差異。實測確認非空白內容除 ID 標題外完全一致，歸檔狀態轉換、ID、Requirement／Scenario 數量皆符合預期。故 design D7 所要求的「內容不變」成立；原逐行比對判準受到歸檔過程中的空白行變動影響。5.2 以偏離方式完成，plan 原文保留不改。

根因（僅陳述已證實的事實）：這個差異由 `openspec archive` 的歸檔過程產生，只涉及空白行，不涉及任何非空白內容。

## 觀察（未查證，供後續參考）

- 懷疑是 OpenSpec 對 `repo-guidance` 這類單一 requirement、整段被 `MODIFIED` 取代的 capability 做了重新序列化（re-serialization），把原本標題前後的空白行位移掉了。
- 為什麼 `plan-contract`／`tdd-claim-accuracy`／`tdd-evidence-contract` 這三個多 requirement 的 capability 沒有出現同樣的空白行位移，目前未查證——可能是合併邊界不落在檔案開頭／結尾而被掩蓋，也可能是別的原因。此項標記【未查證】，不作為結論依據。
