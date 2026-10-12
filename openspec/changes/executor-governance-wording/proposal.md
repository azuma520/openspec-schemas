## Why

正式設計 §5 定了「執行路徑看能力、不看工具名」：任何執行方式只要具備所需能力、或依 G3 合法降級並留紀錄即可，第 222 行明指 CLAUDE.md「禁止 executing-plans 當 fallback」紅旗要改寫。紅旗至今仍是工具禁令。schema 說明、兩份 README 也把設計理由和「上游某版本做了什麼」寫在同一句，上游一改版就得重寫理由，10/06 已發生一次（10/05 裁定、10/06 落地）。另一個缺口是：有 subagent、經使用者裁定刻意不跑 SDD 的情境（8/31、10/06 兩例）目前沒有規則說怎麼揭露，容易被讀成「記了就等於符合」。living spec `tdd-claim-accuracy` REQ-3 用 SHALL 規定理由要在每處陳述 executing-plans 的結構事實，且點名 CLAUDE.md 紅旗，只改文件不改規格會違反現行規格。

## What Changes

**CLAUDE.md「修 schema 時的紅旗」executing-plans 那條**
- From: 禁止在 apply 加 `superpowers:executing-plans` 當 fallback（點名工具），句尾帶「⚠️ 之後要改寫」
- To: 禁止加入不具備 apply 所需能力（執行過程中的獨立審查）、又未依 §5 合法降級的執行方式；禁止把降級紀錄當成保障已滿足；註明本版只支援 SDD。刪除「之後要改寫」句
- Reason: §5 已定案，紅旗要管的是能力與保障，不是工具名
- Impact: 僅維護者面

**理由與版本證據分離（schema.yaml、README 中英）**
- From: 設計說明直接寫「executing-plans 沒有每個任務的審查、無 subagent 時最後由作者自審」等上游版本事實
- To: 設計說明只寫 Bridge 要求的能力、保障與目前限制（本版 apply 仍要求 SDD，缺能力時 Step 0 STOP、不自動切換到 executing-plans），並引用 Re-verification log；上游哪個版本提供或缺少哪些能力、查證來源，寫在 log。舊的帶日期紀錄列不改
- Reason: 上游改版時只需更新紀錄，不用重寫設計理由
- Impact: 只動 Bridge 自己的說明文件，不涉及採用者的 artifact；結論不變（仍不支援）

**apply 指令寫明三種情境（schema.yaml）**
- 沒有 subagent 能力 → 依現行 Step 0 STOP（不變）
- 有 SDD → 照契約執行（不變）
- 有 SDD 但經使用者明確裁定刻意略過 → 例外偏離，不是支援的執行模式，不得稱等同 SDD，記在 retrospective

**retrospective 略過規則與模板（schema.yaml、`templates/retrospective.md`）**
- From: 既有三題（What was skipped／Why this cycle／How to prevent recurrence）沒有說明經裁定略過 SDD 時怎麼答
- To: 不加欄位，只說明既有三題怎麼答：What was skipped 寫出失去的保障；Why this cycle 寫使用者裁定、實際執行方式與替代審查；How to prevent recurrence 針對未授權偏離、未揭露的缺口、不實的符合宣稱，寫明本次如何揭露、證據在哪
- Reason: 揭露偏離，不授權取消必要保障
- Impact: **破壞性**，見下方版本判定

**不變的部分**
- Step 0 STOP 行為、不新增 fallback／機械檢查／降級資料結構
- 「不接受 executing-plans 當 fallback」的結論
- REQ-3 現有三條禁令：不以上游推薦為理由、不說它完全沒有獨立審查、不以 TDD 為區分

**版本判定：schema major 4 → 5（使用者 2026-10-12 裁定）**

依 README Versioning 段逐條核對：沒有新增或刪除 artifact，沒有改 `requires:`，PRECHECK 形狀不變（Step 0 不動）。但「原本合法的 artifact 變不合法」成立，這一條單獨就足以升 major。

這裡的「不合法」是指不符合 schema 契約，不限於「會被 verify 的機械檢查擋下」。retrospective 沒有機械檢查，但它的寫法受 schema 指令與 REQ-4 約束。曾考慮以「沒有檢查會擋」為由維持 4，但被否決：那等於為了這次改動臨時縮小「破壞性變更」的定義。這和 v1→v2 一節否決「改寫政策以配合改動」的理由相同。

1. **既有規定的澄清（單獨不構成破壞性變更）：**
   - 不得把沒取得的保障寫成已取得。§5 已規定 Evidence 不能把不存在的能力變成存在，REQ-4 也已規定不得誘導不實的全 ✓。
   - What was skipped 本來就要寫「具體略過的 skill 或子步驟」，寫出因此失去的審查只是把它講明。
   - 同一個 skill 在多個 cycle 被略過時列為 §6 Promote candidate，是既有規則（schema Skipped-skill rules 末段）。
   - REQ-3 的修改只動 Bridge 自己的說明文件，不涉及採用者的 artifact。
2. **真正新增的規範性要求（構成破壞性變更）：**經使用者裁定略過 `subagent-driven-development` 時：
   - How to prevent recurrence 必須選 `one-off — schema boundary case`。模板裡這個選項原本寫成 `one-off — schema boundary case, no prevention possible`，這次刪掉「, no prevention possible」，與 `schema.yaml` 的字面一致。原因是這一題仍然要寫出如何防止未授權偏離、未揭露的缺口與不實的符合宣稱，不是「無法預防」。
   - 必須寫明裁定只對這個 change 有效。
   - 同類略過已有前例時，必須寫出前例的次數與位置（沒有前例時不要求）。
   - Why this cycle 必須引用使用者裁定與替代的審查方式。
   - 不得把紀錄寫成等效於 SDD，也不得寫成符合 Bridge 的執行契約。
3. **不再符合新契約的既有寫法：**用 `scope-judgment rule` 回答經裁定的 SDD 略過，並宣稱「外部審查多輪即等效於 SDD 的審查結構」。本 repo 的實例是 8/31 `fix-tdd-transitive-claim` 與 10/06 `fix-executing-plans-rationale` 兩份 retrospective。兩份都是封存紀錄，原樣保留、不改寫。v5 只約束往後依新契約寫的 retrospective。

**bundle 版本：** schema major 5 不能用 `4.x.y` 的 bundle 發佈，所以 `VERSION` 改為 `5.0.0`。依 `release-versioning` REQ-1，本 change archive 並完成最終驗證後，要在 release commit 上打 annotated tag `v5.0.0`。push tag 需要使用者當次授權；確認遠端 tag 剝開後指向 release commit，工作地圖紀錄才能標記完成。

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `tdd-claim-accuracy`: 改寫 REQ-3，把設計理由和版本證據分開：設計說明、schema、CLAUDE.md 寫 Bridge 要求的能力、保障與執行限制；Re-verification log 記上游各版本的事實與查證來源；CLAUDE.md 紅旗不必重述版本事實，但要引用 Re-verification log（移出不代表紅旗可以沒有依據）。現有三條禁令保留。改寫 REQ-4，把刻意略過 SDD 的揭露方式併進來，適用範圍從模板擴到 `schema.yaml` 的 retrospective 略過規則
- `release-versioning`: 改寫 REQ-3 的情境 S2：原文寫每週版本檢查讀「v4 列」，升 v5 後就不成立。改成「讀的列要和目前發布的 schema major 一致，升版時同步更新」，不寫死版本號，也不宣稱檢查會自動找出最新那一列（目前是寫死列鍵，升版時手動改）。REQ-3 正文（含 v4 列的歷史宣告）不變（使用者 2026-10-12 裁定，實作時的殘留搜尋發現）

## Impact

- `CLAUDE.md`：「修 schema 時的紅旗」executing-plans 那條
- `superpowers-bridge/schema.yaml`：檔頭 `description`、apply 指令的 fallback 段（加三種情境）、retrospective 的 Skipped-skill rules
- `superpowers-bridge/templates/retrospective.md`：`### Deliberately Skipped Skills` 的填寫說明，以及 `one-off` 選項的字面（刪除「, no prevention possible」）
- `superpowers-bridge/README.md`、`README.zh-TW.md`：Seven Superpowers touchpoints 段的 executing-plans 提示框、apply 段指向設計觸點的那句、設計觸點 #2（Schema-level vs prompt-level 的維護說明）、設計觸點 #4、Fallback strategy 的 `apply` phase 列、Re-verification log（補 executing-plans 的完整事實與查證版本；舊列不改）。實際行位由 design 逐處列出
- `openspec/specs/tdd-claim-accuracy/spec.md`：歸檔時合入 REQ-3、REQ-4 的修改
- `openspec/specs/release-versioning/spec.md`：歸檔時合入 REQ-3（情境 S2）的修改
- schema major 5 的連動（比照 v3 → v4 的 `0b11be5`，逐處清單在 design）：
  - `schema.yaml` 的 `version: 5` 與 `VERSION` 改為 `5.0.0`。
  - 兩份 bridge README：版本標示、Versioning 段新增「Why v4 → v5」與「Migrating v4 → v5」（rollback 指向已存在的 tag `v4.0.0`）、目前 bundle release、Compatibility 表新增 v5 列與其說明、版本變更紀錄。
  - `.github/workflows/version-check.yml`：讀取列的列鍵 `v4` 改為 `v5`。
  - 頂層 `README.md` 與 `README.zh-TW.md`：第 11 行 bridges 表的 Status 欄 `v4` → `v5`。
  - `docs/roadmap.md` 與 `docs/roadmap.zh-TW.md`：新增 v5 段。在遠端 tag 確認之前不標「Released」（見 design D8）。
  - `CLAUDE.md`：版本號與列鍵描述。
- 本 repo 的 dogfood 副本 `openspec/schemas/superpowers-bridge/` 要重新同步（已 gitignore，不進 commit）
- 發版：archive 後打 tag `v5.0.0`（需使用者授權 push）
- 不動：正式設計文件、adopters fragment（全 repo 搜過，不含 executing-plans）、archive 與 handoff 等紀錄類檔案（含 8/31、10/06 兩份 retrospective）
- 不處理（另案）：是否支援沒有 SDD 的能力等價或合法降級執行，由 `task-20261012-non-sdd-execution-support` 依正式設計 §9 研究
- 本 change 自己的 apply 不跑 SDD（brainstorm Q4 具名例外，只限本次），retrospective 如實記錄
