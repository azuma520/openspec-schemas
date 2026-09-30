<!--
Delta spec template for a change.

此模板示範 4 種 delta section，按實際需要取用：
- ADDED / MODIFIED / REMOVED / RENAMED
檔名與位置：openspec/changes/<change-name>/specs/<capability>/spec.md
（`<capability>` 對齊 openspec/specs/<capability>/ 目錄名）

格式硬規則（OpenSpec 會 validate）：
- Requirement 句子 MUST 含 `SHALL` 或 `MUST`
- 每個 Requirement MUST 至少有一個 `#### Scenario:`
- Scenario MUST 用 level-4 (`####`)，level-3 或 bullet 會 silent fail

身份規則（本模板只示範，完整定義與配置演算法見 `specs` instruction，
不在此重述）：
- 每個 Requirement / Scenario 標題都帶一個穩定 ID——ID 是身份，
  description 不是：`### Requirement: REQ-<n> <description>` /
  `#### Scenario: REQ-<n>-S<m> <description>`
- 既有非數字 ID（例如 `REQ-PB`）維持合法；數字形式只約束新配的 ID，
  且新配的號碼須大於歷史最大值（配置規則見 `specs` instruction）
- MODIFIED / REMOVED 的 heading MUST 與 main spec 中的 heading 完全相同
  ——含 ID
- RENAMED 的 FROM／TO 必須帶**同一個** ID（description 可以變；換 ID
  是換身份，不算 rename）
-->

## ADDED Requirements

<!-- 新增行為。列出本 change 要加到 capability 的新 Requirement。 -->

### Requirement: REQ-1 <!-- requirement description -->
<!-- requirement text — 須含 SHALL 或 MUST -->

#### Scenario: REQ-1-S1 <!-- scenario description -->
- **WHEN** <!-- condition -->
- **THEN** <!-- expected outcome -->

---

## MODIFIED Requirements

<!--
修改既有 Requirement。**MUST 使用與 openspec/specs/<capability>/spec.md
完全相同的 normalized header，含 ID**（trim 後 case-sensitive 比對），
否則 archive 時的 delta apply 會因找不到對應 requirement 而失敗。ID 不變
——修改內文不影響身份。

**MUST 貼出修改後的完整內容**（不是只寫 diff），因為 OpenSpec archive
是用全文替換的方式 apply MODIFIED。
-->

### Requirement: REQ-1 <!-- 與既有 spec 中相同的 header，含 ID -->
<!-- 修改後的完整 requirement text — 含 SHALL 或 MUST -->

#### Scenario: REQ-1-S1 <!-- scenario description（可新增、可修改；新增的 scenario 編號須大於同一 Requirement 目前最大編號） -->
- **WHEN** <!-- condition -->
- **THEN** <!-- expected outcome -->

---

## REMOVED Requirements

<!--
刪除既有 Requirement。MUST 包含 Reason 與 Migration 說明，讓 reviewer
理解為何廢除以及既有引用方該怎麼遷移。
-->

### Requirement: REQ-1 <!-- 要刪除的 header，與既有 spec 完全相同，含 ID -->

**Reason**: <!-- 為何廢除 -->

**Migration**: <!-- 既有呼叫方/依賴方應如何調整 -->

---

## RENAMED Requirements

<!--
重新命名 Requirement header。格式固定：FROM / TO 用 code-fence header。
FROM 與 TO MUST 帶同一個 ID——重新命名只能換 description，換 ID 是換
身份、不算 rename。唯一例外：FROM 沒有 ID（既有未編號的 requirement），
此時 TO 的 ID 是依配置規則新配的 ID（見 `specs` instruction）。

若名稱變更 + 內容變更，**同時**在 RENAMED 列出名字變更，並在 MODIFIED
用**新的** header 再寫一份完整內容。

archive 時 apply 順序：RENAMED → REMOVED → MODIFIED → ADDED
-->

- FROM: `### Requirement: REQ-1 <Old Description>`
- TO: `### Requirement: REQ-1 <New Description>`
