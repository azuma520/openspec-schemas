# Step 0 — Capability Inventory（2026-08-28 實查）

> PoC spec §4 的產出。全部結論來自本機實測（openspec 1.3.1、Python 3.13.5），非文件推測。
> 實測憑據：scratchpad `pf1/` 手造 change 實驗（本節「關鍵實測發現」）。

## 關鍵實測發現

1. **手造（非 CLI 建立）的 change 目錄，CLI JSON 讀得動**——條件：目錄下有 `proposal.md`（`show` / `validate` 認 change 靠它；`list` 只看目錄）。审查者先前標記的「CLI JSON 可能只認 CLI 建的 change」疑慮**實測不成立**：Phase 1 手造 fixture 可以直接吃 CLI JSON。
2. `openspec show <change> --json --deltas-only` 輸出結構化 deltas：per-capability、operation（ADDED…）、requirement `text`、scenarios `rawText`。`-r <id>` 以 **1-based 位置序號**取單條。
3. **Gap：change 層 `show --json` 不含 Requirement 標題名**（`### Requirement: <name>` 的 `<name>` 不在輸出裡，只有 requirement text）；Scenario 名同樣不在（只有 rawText）。⇒ Contracts reference 的 key 不能直接用「CLI 吐的標題名」，可選：位置序號（`demo-cap/R1`，脆弱）、requirement text（長）、或 PoC 自己抽標題行（一行 `### Requirement:` 抓取，屬最小補充、不是重寫 parser）。**實作時定，provisional。**
4. `openspec validate <change> --json` 結構化驗證結果（valid / issues）；驗的是 spec 格式硬規則（Requirement 須含 SHALL/MUST、至少一個 `#### Scenario:`）。
5. `openspec status --change <id> --json` 給 artifact 級狀態（done / ready / blocked＋missingDeps）——是 **artifact 完成度**，不是 per-Requirement 驗證狀態（後者正是 PoC 要補的）。
6. `tasks.md` 真格式：`## N. <group>` ＋ `- [ ] N.M <task>` checkbox 清單，無任何 Contract 欄位——與方向文件 §4.1 的認知一致。

## Can reuse（已有，PoC 一律復用）

| 能力 | 來源 |
|---|---|
| Requirement / Scenario 結構化讀取 | `openspec show <change> --json --deltas-only` |
| Change 結構驗證 | `openspec validate <change> --json` |
| Artifact 完成度 | `openspec status --change <id> --json` |
| Schema / template 資訊 | `openspec schemas --json`、`openspec templates --schema <s> --json` |

## Need PoC code（現有工具真的沒有，由 PoC 補）

| 能力 | 備註 |
|---|---|
| Task 的 Contracts reference 解析 | `tasks.md` 無此欄；provisional 標註＋解析都是 PoC 的 |
| per-Contract Verification Result 解析 | 完全沒有現成載體（與方向文件認知一致） |
| Gate 邏輯 | coverage / result / evidence 非空 / CONFLICT 判定 |
| （可能）Requirement 標題名抽取 | 僅當 Contracts key 決定用標題名時需要；一行抽取，非重寫 parser（見發現 #3） |

## Do not need（明記不裝不做）

新 OpenSpec Markdown parser（CLI JSON 已供資料）、資料庫、Pydantic / graph library / JSON Schema framework、sd0x 整合（reference implementation 而已）、Orca、`/to-tickets`（未來 Task Decomposition 候選，本 PoC 不依賴）。

## Runtime

Python 3.13.5 可用；repo 慣例：讀含中文檔一律 `PYTHONUTF8=1`。

## 與 spec 假設的對照

無矛盾，免觸發「停下回報」條款。最小新增面積確認為：**Task reference ＋ Verification Result interface ＋ Gate**——不是一整個 Traceability Framework。
