## Why

Superpowers v6.0.0 起，subagent-driven-development 用 `scripts/task-brief` 從 plan 抽出單一任務的簡報，它只認 `Task <數字>` 形式的標題。bridge Plan Contract 規定的條目標題 `## 1.1 — …` 交給它會 exit 3，所以照 bridge 寫的 plan 無法直接交給上游的主要執行器（Compatibility S11；2026-10-02 dogfood 實際撞到，以等效抽取繞過）。

本 change 讓 bridge 的 plan 能被上游辨識，同時保留既有的編號條目寫法：既有 plan 一般不需遷移，例外見下方三項 breaking。改條目寫法會重新解讀 v3 合法的 `## Task 3 備註` 這類標題，必須升 schema major，連帶把版本宣告整理成誠實的狀態：bundle release 要打 tag 的規則寫在 repo `CLAUDE.md` 與 README，但 repo 至今沒有任何 tag；Compatibility 的驗證日期與退回說明也指向不存在的事物。

## What Changes

**Plan 條目標題的寫法**
- From: 條目是「文字以編號開頭」的 `##` 標題（`## 1.1 — …`）；其他 `##` 是非條目。
- To: 條目由正面規則定義——canonical `## Task <編號> …`（新寫法、建議使用）或 legacy `## <編號> …`（無期限繼續接受）；`Task` 大小寫精確，編號文法不變；鍵值是編號，兩種寫法同編號即為重複。附三句 guidance 加一句寫法建議（都不進 validation），說明要交給上游 `task-brief` 時怎麼寫才不會抽錯範圍。
- Reason: 上游可辨識；Bridge 接受的 `Task` 語法是上游可辨識語言的安全子集（只保證辨識、不保證抽取範圍）。
- Impact: **breaking**——v3 下以 `## Task <數字>` 開頭的非條目標題，v4 會讀成條目。

**程式碼區塊內的標題**
- From: 條文未提程式碼區塊，照字面讀會收 ``` 內的 `##` 標題。
- To: 行首未縮排的 ``` 區塊內的標題形狀文字不構成條目（不認 `~~~`、縮排 fence，與上游一致）。check 13 刻意維持不跳過，兩處都寫理由。
- Reason: 程式碼範例不該改變 plan 的任務結構；若 Bridge 收、上游不收，又是一個新的辨識差異。
- Impact: **breaking**——靠區塊內標題通過（或被擋）的 plan，判定會改變。

**條目標題必須是行首 H2**
- From: 條文說編號「從 `##` 之後第一個非空白字元開始」，沒要求 `##` 後有空白、也沒限定 `##` 在行首；照字面讀，`##1.1` 與縮排的 ` ## 1.1` 都會被收成條目。
- To: 條目標題必須從行首開始，且 `##` 後至少一個空白（space 或 tab）；兩種寫法同一條規則。
- Reason: `##1.1` 在 Markdown 不是標題；縮排 1–3 格的 ` ## 1.1` 在 CommonMark 仍是 H2，但上游 `task-brief` 只認行首的 `#`，所以「行首」是比 Markdown 更嚴、與上游一致的辨識規則。若只替 legacy 寫法保留寬鬆讀法，同一份 plan 會有兩套辨識規則。
- Impact: **breaking**——v3 照字面可能收到的 `##1.1`、` ## 1.1`，v4 不再是條目。本 repo 已掃描全部 45 個 `plan.md`，無此情況（掃描早於本 change 加入的變異 fixtures；f18、f19 刻意含這兩種寫法）。

**check 12**
- From: 只收以編號開頭的 `##` 標題。
- To: 依上述條目定義收鍵值、跳過 ``` 區塊；兩階段比對、不提前結束、訊息格式不變；tasks 側不改。

**版本與發布**
- schema major 3 → 4；bundle `VERSION` → `4.0.0`；`version-check.yml` 改讀 v4 列；`templates/plan.md` 範例改 Task 寫法。
- Compatibility 新增 v4 列：Superpowers 欄沿用 `v5.1.0` 並在表下註明為未重驗的歷史宣告；驗證日期填 `pending`，等真正對該列版本跑完整流程才填。
- v3 → v4 的退回指向 commit SHA（第一個 `version: 4` commit 的 parent），不引用不存在的 tag。
- 落實既有的 release tag 規則：自 bundle 4.0.0 起，每個 release 以同版本 tag `vX.Y.Z` 標記，tag 打在最終 release commit 上；README 改成規則式陳述，修掉「`v3.0.0` tag 已建立」的錯誤陳述。`v4.0.0` 的打 tag 與遠端確認屬 archive 後的 close-out，不在 tasks.md。
- bridge README（en + zh-TW）遷移說明、Known breaking changes、roadmap（en + zh-TW）v4 段、repo `CLAUDE.md` 版本相關段落連動更新。

## Capabilities

### New Capabilities
- `release-versioning`: bundle release 的版本宣告要對應可驗證的事實——release 以同版本 Git tag 標記（自 4.0.0 起）與 release commit 的定義；Compatibility 驗證日期只在對該列版本跑完完整流程後填入；退回說明只指向實際存在的 tag 或 commit。

### Modified Capabilities
- `plan-contract`: 新增條目標題辨識的需求——canonical／legacy 兩種寫法、正面的條目定義（行首 `##` 接空白）、跳過行首 ``` 區塊、兩種寫法同編號為重複；REQ-1 的 1:1 對應規則本身不變。

## Impact

- `superpowers-bridge/schema.yaml`：`version`、`plan` instruction 的 Plan Contract、`verify` instruction 的 check 12（check 13 加一句不對稱理由，判定不變）。
- `superpowers-bridge/VERSION`、`templates/plan.md`、`README.md`、`README.zh-TW.md`。
- `.github/workflows/version-check.yml`（不改不會 fail：v3 列仍在，每週檢查會默默讀 v3 列而非 v4 列，所以改完要手動觸發確認讀到 v4 列）。
- repo `CLAUDE.md`、`docs/roadmap.md`、`docs/roadmap.zh-TW.md`。
- `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/` 新增測試資料。
- 採用者：既有 plan 一般不需遷移；例外為以 `## Task <數字>` 開頭的非條目標題、行首 ``` 區塊內的 `##` 標題、`##` 後無空白或 `##` 前有縮排的標題。目前沒有外部採用者。
- 不影響：上游 Superpowers、OpenSpec CLI、adopters fragment、tasks.md 的解析、check 13 的判定。
