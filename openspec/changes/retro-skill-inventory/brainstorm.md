# Brainstorm — retro-skill-inventory（2026-10-01）

> Raw capture：決策日誌。分類：**bounded**（修改 repo 內既有的模板與 schema instruction 文字；流程本身已存在、可讀）。
> 已呼叫 `superpowers:brainstorming`（6.4.1）；依 schema `brainstorm` instruction 的輸出重導，寫入本檔、不寫 `docs/superpowers/specs/`。
> 探索、未決問題與裁定均在 2026-10-01 同一場對話完成。使用者先前已拍板的事項視為 frozen input，本場只補真正未決處。

## 背景

- 來源：`requirement-scenario-identity` retrospective §6 ③（`openspec/changes/archive/2026-10-01-requirement-scenario-identity/retrospective.md`），2026-10-01 使用者裁定另開修正工作；work-map `task-20261001-retro-template-writing-plans`。
- 起始症狀：`superpowers-bridge/templates/retrospective.md` §4 表格列 `superpowers:writing-plans`，但 `schema.yaml` plan instruction（第 357–361 行）明寫「No skill invocation is required」、只容許私下當拆解輔助；bridge README 第 301 行也標 **Not invoked**。照表填的人可能把它記成「跳過」，製造錯誤的紀錄。Identity retrospective §4 該列只能填 N/A 並引 schema 原文自證。

## 探索發現（2026-10-01，讀檔，未改 repo）

| 查什麼 | 結果 |
|---|---|
| 模板 §4 表格 | 7 列：brainstorming、writing-plans、using-git-worktrees、subagent-driven-development、test-driven-development（條件性標示）、requesting-code-review（structural via SDD）、finishing-a-development-branch |
| `schema.yaml` retrospective §4 instruction（第 1514 行） | 「list each skill in this schema's **apply phase**」 |
| apply 階段實際要求的 skill（`schema.yaml` 第 1618–1630 行 PRECHECK） | using-git-worktrees、subagent-driven-development、finishing-a-development-branch；TDD「not separately invoked by this schema」 |
| `brainstorming` | 由 `brainstorm` artifact 要求呼叫並 PRECHECK（第 34–40 行），不屬 apply 階段 |
| README 第 310 行 | schema 真正要求並 PRECHECK 的是四個（brainstorming + apply 三個）；`writing-plans` 只是可選私下輔助；`test-driven-development`／`requesting-code-review` 從不由 schema 本身 invoke |
| 主 spec `tdd-claim-accuracy` REQ-4 | 已管 retrospective 模板的 skill-compliance 表——但管的是「不誘導全 ✓ 的假宣稱」，不管表裡該列哪些項目 |

**發現：** 模板（列 brainstorming）與 schema instruction（限 apply 階段）對「§4 該列哪些 skill」的定義本身互相矛盾；`writing-plans` 誤列只是這個定義不一致的其中一個表現。

**看到但不屬本次範圍：** `finishing-a-development-branch` 在 archive 之後才執行，而 retrospective 寫於 archive 之前，該列天生只能填「尚未」（Identity 即如此）。這是時序／lifecycle 問題，已在 bridge README 設計觸點 #6 記載，與模板定義不一致是不同類問題。

## 決策鏈

### Q1 修多寬？（2026-10-01 使用者裁定：乙）

- 甲：只刪 `writing-plans` 一列——修症狀，已知的定義矛盾留著。
- **乙：刪 `writing-plans`，同時把 schema §4 instruction 的定義改成與模板一致。** ← 選定
- 丙：乙 + 處理 finishing 時序——**明確排除**，屬另一類問題，避免 scope creep。

使用者理由：第二項發現證明 `writing-plans` 誤列是同一個定義不一致的表現；只做甲是明知 owner 定義仍互相矛盾。

### Q2 TDD 與 code-review 兩列留不留？（2026-10-01 使用者裁定：甲，保留）

使用者初版 claim 為「只列 schema 實際要求呼叫的 skill，不列僅可私下輔助者」。照字面套用，`test-driven-development` 與 `requesting-code-review` 也非 schema 直接 invoke，會一併被刪；但它們記錄的是 TDD／code review 紀律有無落實，schema 第 1540 行起的「§4 跳過規則」也直接點名這兩列，TDD 更是本 repo 的硬約束。

- **甲：保留兩列，定義改兩層。** ← 選定
- 乙：照字面刪除——需連帶改 schema 跳過規則，且 retrospective 失去記錄 TDD 落實的位置。

使用者修正後的 claim：

> Retrospective §4 應記錄兩類項目：
> 1. superpowers-bridge workflow 明確要求呼叫的 Superpowers skills；
> 2. schema 明確要求落實、並需要在 retrospective 留下執行情況的 Superpowers disciplines（紀律／機制），即使它們不是由 schema 直接 invoke。

分類結果：

| Skill | 類別 |
|---|---|
| `brainstorming` | 第一類（直接要求呼叫） |
| `using-git-worktrees` | 第一類 |
| `subagent-driven-development` | 第一類 |
| `finishing-a-development-branch` | 第一類（時序問題本次不處理） |
| `test-driven-development` | 第二類（annotation-driven；schema 要求 TDD applicability 與 RED/GREEN 證據） |
| `requesting-code-review` | 第二類（structural via SDD；review 紀律是 apply 設計的一部分） |
| `writing-plans` | **兩類都不是**——不要求呼叫，也不是 schema 要 retrospective 追蹤的紀律 → 刪除 |

使用者定位：retrospective 不是「函式呼叫紀錄表」，而是記「這個 bridge 承諾採用的 Superpowers 工作方法，這次有沒有實際落實」。邊界：只修 §4 inventory 的定義與 `writing-plans` 誤列；不擴張 TDD、code-review 兩列現有的行為或驗證規則。

### Q3 兩類定義的規範放在哪份 spec？（2026-10-01 使用者裁定：`tdd-claim-accuracy` 新增 REQ-5）

- **在現有 `tdd-claim-accuracy` 新增 REQ-5。** ← 選定
- 另開新 capability——名稱較貼切，但同一張表的契約會拆成兩份 spec。

使用者理由：REQ-4 已在管 §4 這張表的宣稱方式；再開 capability 會讓「不能亂宣稱全部有做」與「表裡該列哪些項目」分屬兩個 owner，違背單一事實單一 owner。capability 名稱對 REQ-5 不完全貼切，但為名稱而拆的成本大於收益；未來 retrospective inventory 長出更多與 TDD 無關的契約時，再以證據考慮重組。

### Q4 要不要先暫停、先做 OpenSpec 1.14.0 相容性 spike？（2026-10-01 使用者裁定：不暫停，照原順序）

本 change 改的是 instruction 文字與模板表格，OpenSpec CLI 只搬運兩者、不解讀內容；「§4 該列什麼」是 bridge 自己的定義問題，1.14.0 推翻不了。1.14.0 唯一可能碰到的是驗證手段（`openspec instructions retrospective` 的輸出），影響「怎麼驗」不影響「改什麼」。與表格內容真正相關的是 Superpowers 版本（README 釘 `v5.1.0`、最新 `v6.4.2`）；本機 6.4.1 下表中 6 個 skill 均存在，`brainstorming` 已實際執行——但這不等於 v5.1.0 → v6.4.x 相容性已驗完，留給 issue #2 spike（OpenSpec 與 Superpowers 一起看、各驗自己的 dependency surface）。

## 核可的短設計（2026-10-01 使用者回覆「可以」）

**要改的地方**

1. `superpowers-bridge/templates/retrospective.md` §4：刪 `superpowers:writing-plans` 列；表格下方說明補一句兩類定義。TDD、code-review 兩列的標示與 `### Deliberately Skipped Skills` 規則原樣不動。
2. `superpowers-bridge/schema.yaml` retrospective §4 instruction（第 1514 行）：「list each skill in this schema's apply phase」改為兩類定義。第 1540 行起的「§4 跳過規則」不動。
3. bridge README（en／zh-TW）：只做一致性核對、不預設修改。預先核對（en 版，以 `rg -n "writing-plans|compliance"` 全檔掃），預期都不用改——第 301–310 行是「schema 點名哪些 skill」表，與 §4 定義是兩回事且已標 writing-plans 不呼叫；第 413 行只泛稱「Skill compliance」；第 497、531、563、570–574、594 行是 v2 移除 writing-plans 依賴的遷移說明與上游漂移紀錄，皆與「不呼叫」一致。（更正：對話中曾誤寫「第 571 行談 v2 遷移」，實際行號如上。）
4. 主 spec `tdd-claim-accuracy`：新增 REQ-5，規範 §4 inventory 的兩類定義。

**驗證（不新增任何檢查機制）**

- 每個 task 標 `TDD: n/a`，理由：本次只改文字與模板、沒有可執行行為。
- `openspec schema validate superpowers-bridge` 與 `openspec validate` 通過。
- 讀檔確認：§4 表剩 6 列、無 `writing-plans`；schema instruction 與模板的定義一致。
- 重同步 dogfood 副本後跑 `openspec instructions retrospective`，確認實際送給 agent 的是新 instruction。
- 依規定跑 Codex 文件審查。

**版本：** 不動 `VERSION`。既有規則下 `VERSION` 與 tag 在發版時才動，本 change 不負責發版；`v3.0.0` tag 本身尚未打，這次修正會隨下一次發版一起出去。

**明確排除：** finishing 時序（只記 observation）、TDD／code review 重新設計、新增 lint／CI／enforcement、版本發佈。

## 觀察（作為「小修正的程序成本」案例素材，不在本 change 處理）

- brainstorming 6.4.1 的 bounded 路徑原本只在對話中給短設計、不寫檔，schema 卻要求寫入 `brainstorm.md`——是工作地圖「修 brainstorming 三路徑漂移」的一個實例。本次照 schema 寫檔。
- 即使是 bounded 小修正，brainstorming 的「先寫回理解、只問真正未決處」仍抓到一個實質問題（Q2：初版 claim 判準會誤刪 TDD／code-review 紀錄），未把已決事項拿回重談。

## 補記（2026-10-02，specs 撰寫後）

### Q5 REQ-5 條文要不要明列 6 個 skill 名稱？（2026-10-02 使用者裁定：明列，並修正 owner 分工）

起因：specs 初稿明列了 6 個名稱，與 design D3「schema 只寫判準、不重複列名稱」看似有張力，端給使用者決定。

使用者裁定：保留 6 個名稱，並修正概念——既然 REQ-5 是正式 spec owner，normative owner 是 `tdd-claim-accuracy` REQ-5，不是 schema instruction。分工為三層：

> **Spec：定義規則，並明列目前六個應收錄項目。**
> **schema：把判準轉成交給 Agent 的 instruction。**
> **template：呈現這六列實際表格。**

這是「契約 → 實作 → 產物模板」三層，不是互相競爭的多份真相；spec 只講抽象兩類反而難以直接判斷模板是否合約。REQ-5 同時寫：兩類判準、目前符合判準的六項、`writing-plans` 為明確反例。日後 inventory 真正變動時，先改 spec，再連動 schema／template。
