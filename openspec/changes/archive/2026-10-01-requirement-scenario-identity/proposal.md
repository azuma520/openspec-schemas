## Why

Requirement 與 Scenario 目前只有標題文字，沒有穩定、可被機器引用的身分：標題一改，所有指向它的引用就無聲斷掉；同一 capability 裡兩條需求用同一個編號，OpenSpec CLI 也照樣驗證通過、照樣合併（2026-09-29 實測）。正式設計 §3.1 把 stable ID 定為整條需求追蹤鏈的地基——後續的 `Contracts:`、驗收台帳、Gate 都要先能指認「這是哪一條需求、哪一個情境」才建立得起來。依主線排序（2026-09-29 裁定），身分層是第一塊。

## What Changes

**Requirement / Scenario 標題**
- From: `### Requirement: <name>`、`#### Scenario: <name>`，無 ID
- To: `### Requirement: <REQ-ID> <description>`、`#### Scenario: <REQ-ID>-S<m> <description>`；新 ID 依固定規則配置，改名不換 ID
- Reason: 讓每條契約有不隨措辭改變的身分，供後續引用
- Impact: **破壞性**——原本合法的無 ID spec 在本版後過不了 verify

**verify 新增 check 13（identity integrity）**
- 以「若現在歸檔本 change 會得到的主 spec」（在暫存複本實跑 `openspec archive` 預演）為驗收對象，並以歸檔前的主 spec 與 delta spec 為判斷基準，檢查缺 ID、同一 capability 內同一 ID 指向不同契約、Scenario ID 不屬於所在 Requirement、RENAMED 換 ID、新 ID 不符配置規則，並與 CLI JSON 的數量交叉核對；任一成立即 BLOCK
- Impact: 破壞性（同上）

**schema major 2 → 3**
- Reason: 依 bridge README「Why v1 → v2 is a schema-major bump」的既有定義，原本合法的 artifact 變不合法即為 breaking。v3 描述的是相容性邊界，不是 roadmap 階段；後續 change 是否再跳版，依其本身是否再破壞相容性各自判斷
- Impact: 附 v2 → v3 遷移指南；CI 解析的 Compatibility 表新增 v3 列

**本 repo 既有 spec 一次補完 ID**
- 3 個 capability 的 10 條 Requirement、37 個 Scenario 補號；`repo-guidance` 的 `REQ-PB` 保留原名（正式設計 §3.1 grandfathered），其兩個 Scenario 補為 `REQ-PB-S1`、`REQ-PB-S2`。不留「部分 spec 不用 ID」的例外

## Out of Scope

留給後續 change：

- `tasks.md` 的 `Contracts:` 承接標註
- `verification-results.json` 驗收台帳
- 可執行、不可繞過的 Gate
- 需要歷史或歸檔前後比較的身分檢查：退休 ID 不得重新指派、MODIFIED／archive 過程不得無聲弄丟 Scenario ID、Scenario 退休紀錄格式

## Assurance Boundary

本 change 只新增由 verify agent 執行、判準固定的 identity check；不宣稱已提供不可繞過的 executable Gate。完整的保證範圍與不保證事項以 `contract-identity` spec 為準（normative owner）。

## Capabilities

### New Capabilities

- `contract-identity`: Requirement / Scenario stable ID 的語法、新 ID 配置規則、改名保 ID，以及 verify check 13 的判定內容與宣稱邊界

### Modified Capabilities

以下四個 capability 的需求**標題（身分）變更、行為不變**，正文一字不改，每一個都需要 delta spec 檔。前三個的 Requirement 走 RENAMED 補 ID、Scenario 標題隨 MODIFIED 全文更新；`repo-guidance` 的 `REQ-PB` 不改名，只以 MODIFIED 補 Scenario ID：

- `plan-contract`: 補 Requirement 與 Scenario ID
- `tdd-claim-accuracy`: 補 Requirement 與 Scenario ID
- `tdd-evidence-contract`: 補 Requirement 與 Scenario ID
- `repo-guidance`: `REQ-PB` 保留；兩個 Scenario 補 ID

## Impact

- `superpowers-bridge/schema.yaml`：`specs` instruction、`verify` check 13、`version: 3`
- `superpowers-bridge/templates/spec.md`、`templates/verify.md`
- `superpowers-bridge/README.md` ＋ `.zh-TW.md`（格式、檢查清單、Versioning、遷移指南、Compatibility、Known breaking changes）、`VERSION`
- `.github/workflows/version-check.yml`（解析 Compatibility 表的列鍵）
- repo `CLAUDE.md`（版本號與跨檔耦合表中寫死的 `v2`）
- `docs/roadmap.md` ＋ `.zh-TW.md`
- `openspec/specs/` 四個 capability（補號）
- 採用者：升級到 v3 須依遷移指南為既有 spec 補 ID
