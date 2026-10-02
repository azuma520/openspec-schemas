## Context

retrospective artifact 的 §4「Skill / workflow compliance」由兩個 owner 共同決定：`superpowers-bridge/schema.yaml` 的 retrospective instruction（第 1514 行，告訴 agent 這張表該列什麼）與 `superpowers-bridge/templates/retrospective.md`（實際的表格）。兩者目前不一致：

- schema 寫「list each skill in this schema's **apply phase**」——apply 階段要求的 skill 只有 using-git-worktrees、subagent-driven-development、finishing-a-development-branch（apply step 0 PRECHECK，第 1618–1630 行）。
- 模板列 7 列，多了屬於 brainstorm 階段的 `brainstorming`（`brainstorm` artifact 要求呼叫並 PRECHECK，第 34–40 行），以及 schema 根本不要求呼叫的 `writing-plans`（plan instruction 第 357–361 行：「No skill invocation is required」，只容許私下當拆解輔助）。另兩列 TDD、code-review 有條件性／結構性標示，schema 第 1540 行起的「§4 跳過規則」直接點名這兩列。

主 spec `tdd-claim-accuracy` REQ-4 已管這張表的「不誘導全 ✓ 假宣稱」，但沒有規範表裡該有哪些項目。

約束：TDD 是本 repo 硬約束，TDD 落實紀錄不可因本次修正而消失；本 change 是 bounded 文字修正，不新增 enforcement；使用者已裁定的範圍見 brainstorm Q1–Q4。

## Goals / Non-Goals

**Goals:**

- schema instruction 與模板對 §4 inventory 只有一個、一致的定義（兩類項目）。
- 模板 §4 刪除 `writing-plans`，剩 6 列。
- 主 spec 有一條需求（`tdd-claim-accuracy` REQ-5）作為該定義的 owner。

**Non-Goals:**

- 不改 TDD、code-review 兩列的標示，也不改「§4 跳過規則」與 `### Deliberately Skipped Skills` 子節。
- 不處理 `finishing-a-development-branch` 在 archive 後才執行的時序問題（README 設計觸點 #6 範圍，只記 observation）。
- 不新增 lint、CI、verify check 或任何 enforcement。
- 不動 `VERSION`、不發版、不打 tag。
- 不修改 bridge README（核對結果無衝突）。
- 不重設 skill provenance 規則、不改其他 artifact 或 `requires:`／PRECHECK。

## Decisions

### D1：修正範圍——修定義，不只修症狀

- **選擇**：刪 `writing-plans` 列，同時把 schema §4 instruction 的定義改成與模板一致（brainstorm Q1 乙）。
- **理由**：`writing-plans` 誤列只是「schema 與模板定義不一致」的一個表現；只刪該列，`brainstorming` 列與 schema 文字的矛盾仍在，下次照表填的人還會碰到。
- **已考慮 alternative**：只刪一列（修症狀、矛盾保留）；連同 finishing 時序一起處理（另一類問題，scope creep）。

### D2：inventory 採兩類定義

- **選擇**：§4 記錄 ① workflow 明確要求呼叫的 Superpowers skill，與 ② schema 要求落實、需在 retrospective 留下執行情況的 Superpowers 紀律（即使非 schema 直接 invoke）。僅被 schema 點名為可選私下輔助的 skill 不列。
  - ①：brainstorming、using-git-worktrees、subagent-driven-development、finishing-a-development-branch
  - ②：test-driven-development（annotation-driven）、requesting-code-review（structural via SDD）
  - 排除：writing-plans
- **理由**：retrospective §4 記的是「bridge 承諾採用的工作方法這次有沒有落實」，不是函式呼叫紀錄（brainstorm Q2）。單一判準「schema 有沒有直接呼叫」會誤刪 TDD、code-review 兩列，失去 TDD 落實紀錄。
- **已考慮 alternative**：只列直接呼叫的 skill（會刪 TDD／code-review 兩列並連帶改跳過規則）；只列 apply 階段（即現行 schema 文字，與模板矛盾）。

### D3：schema 與模板各寫到什麼程度

- **選擇**（三層分工，brainstorm Q5）：
  - spec（REQ-5）是 normative owner：寫判準、明列目前符合判準的 6 項、以 `writing-plans` 為反例。inventory 日後變動時先改 spec，再連動 schema 與模板。
  - schema instruction 寫**判準**：兩類的定義，第一類以「schema 在哪裡要求呼叫」指認（`brainstorm` artifact 與 apply pre-flight），第二類明列 TDD 與 code review 兩項紀律，並明說僅作可選輔助的 skill（例：`writing-plans`）不列入。
  - 模板寫**清單**：6 列表格；表格下方既有說明補一句兩類定義，不另寫一套定義。
- **理由**：契約 → 實作 → 產物模板三層，不是互相競爭的多份真相；spec 明列 6 項才能直接判斷模板是否合約。schema 是把判準交給 agent 的實作層，模板是判準套用後的結果。第二類是本次裁定的封閉集，明列比抽象描述更不易被誤讀；點名 `writing-plans` 為排除例，防止日後被當成「漏列」加回去。
- **已考慮 alternative**：schema 也逐一列出 6 個 skill 名（與 PRECHECK 清單重複，多一處要同步）；模板不加說明（讀模板的人看不出為何沒有 writing-plans）。

### D4：規範的 owner——`tdd-claim-accuracy` 新增 REQ-5

- **選擇**：在既有 capability 新增 `REQ-5`，不另開 capability（brainstorm Q3）。
- **理由**：REQ-4 已管同一張表；分到兩份 spec 會讓同一張表的契約有兩個 owner。capability 名稱對 REQ-5 不完全貼切，為名稱拆分的成本大於收益。
- **已考慮 alternative**：新 capability（名稱貼切，但契約分散）；修改 REQ-4 併入（REQ-4 談假宣稱壓力，混入 inventory 定義會讓一條需求管兩件事）。

### D5：驗證沿用既定最小集合

- **選擇**：每個 task `TDD: n/a`（只改文字與模板，無可執行行為）；以 `openspec schema validate`、`openspec validate`、讀檔核對（表 6 列、無 writing-plans、schema 與模板定義一致）、重同步 dogfood 副本後 `openspec instructions retrospective` 確認送出的是新文字、Codex 文件審查為證據。
- **理由**：使用者裁定不新增 apparatus；這組足以對準本次 claim（定義一致、誤列已除、新文字實際送達 agent）。
- **已考慮 alternative**：新增自動比對模板列與 schema 判準的檢查（使用者明確排除）。

### D6：版本不動

- **選擇**：不改 `VERSION`，schema major 維持 3。
- **理由**：無原本合法 artifact 變不合法、無 artifact／`requires:`／PRECHECK 變動，不構成 major；`VERSION` 與 tag 依既有規則在發版時才動，本 change 不負責發版（`v3.0.0` tag 尚未打，本修正隨下次發版出去）。

## Risks / Trade-offs

- [Risk] 沒有 enforcement，日後有人改 schema 判準或模板表格時可能再度不一致 → Mitigation：REQ-5 讓定義有 spec owner，review 時有條文可對照；enforcement 是使用者明確排除的範圍，不在本次補。
- [Risk] 採用者手上已寫好的 retrospective 仍有 `writing-plans` 列 → Mitigation：非破壞性，舊檔仍可讀；README 既有說明已載明重跑 `/opsx:continue → retrospective` 時套用新模板。
- [Trade-off] REQ-5 放在名稱以 TDD 為主的 capability → 接受理由：單一 owner 優先於命名，未來證據足夠再重組。
- [Trade-off] finishing 列仍只能填「尚未」→ 接受理由：時序問題屬設計觸點 #6，刻意不混入本 change。

## Migration Plan

N/A — 本 change 不涉及部署變更。採用者端無遷移步驟：新模板只影響之後產生的 retrospective。本 repo 實作後需重同步 dogfood 副本（`openspec/schemas/superpowers-bridge/`，gitignore）。Rollback：revert 本 change 的 commit。

## Open Questions

（無。範圍、定義、owner、驗證與版本均已於 brainstorm Q1–Q5 裁定。）
