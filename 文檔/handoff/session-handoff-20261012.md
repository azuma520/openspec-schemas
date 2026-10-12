<!--
workflow-harness — Handoff template
對應 inventory：A5 六欄 schema、A6 append-only、A7 檔名 schema
檔名：文檔/handoff/session-handoff-{DATE:YYYYMMDD}.md
規則：append-only — 同日多 session append 多個「## Session HH:MM」區塊；前段不可改
-->

# Session Handoff — 2026-10-12

## Session 08:05

### 一、本 session 主題

開工於 2026-10-08 17:21（跨日延續、10-12 收工）。push 10/08 的 4 個 commit；開始 CLAUDE.md 紅旗治理改寫：裁定範圍、建 opsx change `executor-governance-wording`、完成並審過 brainstorm。

### 二、完成事項

- **push**（使用者授權）：`d2a350c..b40e059` 推上 `origin/main`（fast-forward；repo 未裝 pre-push hook）；`v4.0.0` tag 先前已在遠端。
- 釐清「紅旗改寫」**未做**：10/05 的 `fix-executing-plans-rationale`（`9ef62c2`）只修理由，禁令本身未改（CLAUDE.md 第 258 行仍是舊寫法）。
- 讀依據：正式設計 §5（第 195–222 行）、CLAUDE.md 紅旗、README 中英 executing-plans 各段、`schema.yaml` 第 8–12 行與約 1795 行、10/06 複盤 §6 第 1 條（目標是 **schema apply instruction**）、living spec `tdd-claim-accuracy` REQ-3/4/5。
- **裁定**（使用者，記在 brainstorm.md Q1–Q7）：選 A（只改治理說明、不改 Step 0 STOP、不新增 fallback）；三種情境分開（無能力 → STOP／有 SDD → 正式路徑／有 SDD 但經裁定刻意略過 → 例外偏離、記 retrospective、不得稱等同 SDD）；本 change 不跑 SDD（具名例外，只限本次）；MODIFIED REQ-3（理由與版本證據分離、CLAUDE.md 紅旗移出逐處陳述事實的範圍）＋ MODIFIED REQ-4（略過 SDD 的揭露方式）；版本號依 Versioning 判準於 proposal 決定。
- **建 change**：`openspec new change executor-governance-wording --schema superpowers-bridge`；`openspec/changes/executor-governance-wording/brainstorm.md` 完成。
- **Codex 文件審**（Orca 分頁、`codex exec -p review`，thread `01a11b02-24c0-71d2-901d-6335dec9127a`，已回覆 1 次）：✅ Mergeable，🔴🟡⚪ 皆 0；`doc_review pass` 已記；暫存目錄已清（使用者執行 rm）。
- 清掉 10/08 留下的 `docrevreadme/` 暫存目錄（README 審查 ✅ Mergeable、thread `01a11ac8…`，結論已在 10/08 17:15 handoff）。
- 工作地圖：`task-20260901-claudemd-governance-rewrite` → DOING。

### 三、未完事項 / 接力棒

- [#接力] 本機 `main` 領先 origin（`213a6fb` 與本收工 commit）；未授權 push。
- [#接力] 下一步：寫 `proposal`（含依 README Versioning 段判定版本號；Q5：寫成「既有三題如何回答」、不新增欄位，避免舊 retrospective 變不合法）→ `design` → `specs`（MODIFIED REQ-3、REQ-4）→ `tasks`（全 `TDD: n/a` 附理由）→ `plan`。
- [#接力] 驗證時須確認三個語意未變：無 subagent 仍 STOP；有 SDD 走正式路徑；略過 SDD 的紀錄不被解讀為已滿足必要保障（併入文件審與 verify，不新增機械檢查）。
- [#接力] 已登記 `task-20261012-non-sdd-execution-support`（掛 superpowers-bridge 下一代改造）：「是否支援無 SDD 的能力等價或合法降級執行」**留待後續依 §9 研究**。
- [#接力] 10/08 遺留仍在：空目錄 `.claude/worktrees/task-prefixed-plan-headings/` 待 `! rmdir`；上一個 session 的 `e6eab2eb-…/` 下 `docrev6x/`、`mkprompt2.py`、`profile6x.json` 未清（使用者只授權清 `docrevreadme/`）。
- [#不重議] 範圍 A 與三個邊界；三種情境的定位；本 change 不跑 SDD 的具名例外（不升格為支援模式）；§5 能力導向原則不重議；揭露方式併入既有 REQ-4、不新增 requirement。

### 四、洞見 / 反省

**【紀律接力】**

- **宣告「沒有」前沒窮舉**（沿用；本 session 0 次）：搜 executing-plans 時同時掃了 README／schema／specs／adopters／CLAUDE.md，才撞到 REQ-3 把 CLAUDE.md 紅旗列入範圍——若只掃工作地圖點名的 README 兩段就會漏。
- **說過頭的句子**（沿用；本 session 0 次被抓）。使用者貼的文字把一句話歸給我，我當場更正「那不是我說的原話」並指出出處。
- **附和裁定時驗事實前提**（沿用；本 session 每次都驗）：REQ-4 適用範圍只到模板、REQ-5 末段不構成禁令、verify 不讀 SDD 產物、retrospective 既有三題——都在回覆前查過原文。

**【當日洞見】**

- **工作地圖的範圍描述會漏掉同類位置**：工作地圖只點名 README 兩段，實際同類混寫還在 `schema.yaml` 兩處、README 另兩處，且被 living spec REQ-3 鎖住。改「理由」類文字前先搜 `openspec/specs/` 有沒有規格規定它的位置與形式。
- **「沒有能力」與「有能力但選擇不用」是兩種情境**：複盤 §6 ① 的案例是後者，Step 0 STOP 只管前者；使用者據此定出三層（執行方式／能力／最低保障）。
- 使用者裁定以「貼上的整段裁定＋你同意嗎」形式連續出現 5 次，都照 memory `feedback_pasted_rulings_are_user_replies` 當使用者回覆處理、先驗事實再回。

【學習候選】

- **Case**：工作地圖寫的修改範圍（README 兩段）小於實際同類位置，且有 living spec 規定那段文字的寫法。
- **Candidate Pattern**：改「理由／說明」類規範文字前，除了全 repo 搜同義句，也搜 `openspec/specs/` 是否有 requirement 規定該段的位置或形式；有就把 spec delta 列入範圍。適用於有 living spec 的 repo；純文件 repo 不適用。
- **Evidence**：本次 1 例（REQ-3）；10/06 複盤 §5 也記過「錯誤說法是正式規格強制的」——同一份 spec，第 2 例。**Hypothesis**（兩例同一 spec）。
- **Minimum Sufficient Intervention**：不新增規則；本 change 的 tasks 會自然包含 spec delta。觀察。
- **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（b40e059、開工於 2026-10-08T17:21:04）——列 b40e059..HEAD

- `213a6fb`：`openspec/changes/executor-governance-wording/`（`.openspec.yaml`、`brainstorm.md`）
- 本收工 commit：`workflow-harness/work-map.jsonl`（governance-rewrite → DOING；新增 `task-20261012-non-sdd-execution-support`）、本交接檔——收工 commit 走 `/smart-commit --execute`（使用者授權）。

### 六、下一步建議

1. 繼續 `executor-governance-wording`：寫 proposal（含版本號判定）。
2. 之後 design → specs（MODIFIED REQ-3、REQ-4）→ tasks → plan。
3. 清 10/08 遺留暫存（空 worktree 目錄、`docrev6x/` 等，需使用者執行 rm）。

## Session 17:27

### 一、本 session 主題

開工於 2026-10-12 08:18（接續 08:05 session）。`executor-governance-wording` 從 proposal 一路做到 archive，**發布 bundle v5.0.0**（schema major 5）。verify 後依使用者裁定補 REQ-6，並用四維度判準把 7 份封存 retrospective 的 §6 升級候選清了一次帳。

### 二、完成事項

- **實作**（`2551ea0`）：
  - `schema.yaml`：description 與 apply 改成能力語言；apply 三種情境分開；Step 0 不再指向不存在的 manual fallback；retrospective 略過 SDD 的寫法。
  - 模板。
  - bridge README 中英：重新查證紀錄新增「executing-plans review structure」段、v5 版本處。
  - 版本連動：`VERSION` 5.0.0、`version-check.yml` 列鍵 v5、頂層 README、roadmap、CLAUDE.md 紅旗。
- **verify 兩輪**（皆 ⚠️ PASS WITH WARNINGS、無 BLOCK）：
  - Round 1：備援 agent（Opus 5.5）。
  - 實作者附記：W5 用分得出對錯的變異測試，證明 version-check 讀 v5 列；同時更正我先前「原樣取出」的不實描述。
  - Round 2：Fable 獨立驗證。
- **W6 補規格**（使用者裁定甲）：`tdd-claim-accuracy` ADDED REQ-6，S1–S4 保護三種情境與 Step 0 STOP；proposal／design／tasks／plan 同步。
- **retrospective** 寫完，§6 每條逐一取得使用者裁定（A–G）。SDD 略過記為第三例（8/31、10/06），並列 §6 F。
- **§6 候選盤點**：35 條中已做到 10、沒做 12。沒做的全部來自沒有逐條裁定的 retrospective。盤點表保存為 archive 內的 `retro-s6-audit.md`。
- **四維度判準存檔**：`docs/superpowers/research/2026-10-12-improvement-decision-four-dimensions.md`（備查、非規範）。
- **memory**：`feedback_claim_first_discriminating_oracle` 補第 3 點——說「讀到 X／原樣／相同」前要 diff 或分得出對錯的實跑。
- **CLAUDE.md**：跨檔耦合表新增「升 schema major」列；dogfood 同步條件放寬到 bridge 任何檔；兩處 archive 舊路徑。
- **backlog**：新增 5 條 `[優化建議]`（2.3、3.5、7.1、§6 B、§6 E）與 1 條 `[構想]`（發版前審查留下的 a–f 舊文件問題）。第 80 行補 `[mature: 2026-10-12]`，是我早上手改 case-count 時漏的，改經 writer `repair` 補上。
- **發版**（使用者授權）：
  - `58b907e`：archive，spec 合入；`openspec validate --all` 6/6。
  - `c49a2d9`：release commit。
  - annotated tag `v5.0.0`，遠端 `^{}` = `c49a2d9`。
  - `e8515cc`：roadmap v5 標 Released。
  - 全部已 push。
  - `workflow_dispatch` run 38229715270 success（讀到 1.14.0／v5.1.0；v4、v5 兩列值相同，故此次實跑本身分不出列鍵，列鍵正確性靠本機變異測試）。
- **審查**：全程 Codex 無額度，fallback 載體為 Fable（Fable 撞用量上限的一輪改由預設模型）。發版前三批全檔審 ✅ Mergeable；歸檔後兩份 spec 文審 ✅；`.openspec.yaml` 搬移碼審 ✅ Ready；precommit 仍為 `⚠️ NO CHECKS RUN`（非通過）。
- 封裝候選檢查：本 session 唯一相關的 `[SOP 候選]` 是第 80 行 precommit 缺口，今早已記為 case 5，同日不重複 bump。

### 三、未完事項 / 接力棒

- [#接力] **Codex 額度恢復後補審 v5.0.0**：發版前所有審查都由 fallback 擔任（全域規則 2026-09-01：高風險項外部審恢復後必須補審）。範圍：`c49a2d9` 的 bridge 實作與版本連動。出處：archive retrospective §6 C。
- [#接力] 依 retrospective §6 A：之後寫每份 retrospective 時，§6 每條當場取得使用者裁定。
- [#接力] backlog 新增各條（2.3／3.5／7.1／B／E／a–f）等累積或下一個 change；f 與 `release-versioning` Purpose TBD、`tdd-claim-accuracy` REQ-3 標題（宜用 RENAMED）留給下一個碰該 spec 的 change。
- [#接力] 暫存待清（需使用者 rm）：本 session scratchpad、08:05 交接第 33 行的 10/08 遺留。
- [#不重議] W6 補 REQ-6（不新增 fallback／執行器／檢查／欄位）；N2 標題偏窄這次不改；1.3、3.6 算「已做到（遲到）」；四維度只作判讀輔助、不當規格。

### 四、洞見 / 反省

**【紀律接力】**

- **說過頭的句子**（沿用；**本 session 被抓 4 次**）：
  - 「實跑讀到 v5 列」（兩列值相同，證明不了）。
  - 「原樣取出」（只比了第一行）。
  - retrospective 把 7.5 寫成「再犯」、把 3.7 寫成「先觀察」。
  - 「v4.0.0 只靠 fallback 發版」。
  - 四次都是驗證者或審查者抓到，不是我說出口前自己查。共同形狀：**摘要或轉述別人的結果時，沒回原始資料逐字核對**。memory 已補「讀到／原樣／相同」那半；「摘要盤點結果」這半還沒有掛點。
- **宣告「沒有」前沒窮舉**（沿用；本 session 0 次）。
- **附和裁定時驗事實前提**（沿用；本 session 每次都驗）：W6 寫 REQ-6 前讀完 Step 0 所有分支，找到 CLI 工具只 WARNING 的例外，寫進 S4。

**【當日洞見】**

- **retrospective 的價值卡在「執行」那一段，不是「找方案」那一段**：有逐條裁定的 3 份幾乎全部落地，沒有裁定的 3 份漏了 12 條；schema 寫的「未勾選候選帶到下一輪」從沒發生過。最小改法是寫完當場逐條裁定，不是新增追蹤機制（用四維度判讀後的結論）。
- **獨立驗證真正有價值的是「抓到原本方法證明不了的事」**：W5（測試分不出對錯）與 W6（核心行為沒有規格）都是驗證者抓到、所有文件審都沒抓到（使用者也這樣評價）。
- **append 式 verify.md 與 retrospective PRECHECK 的「恰好一個勾選框」不合**（Round 2 N3）：這次兩輪結論相同所以沒事。

【學習候選】

- **Case**：本 session 四次說過頭，都在「轉述／摘要」既有結果時發生，都由他人抓到。
- **Candidate Pattern**：轉述或摘要一份結果（測試輸出、盤點表、別人的報告）之前，回到原始資料逐句核對要寫的那句。適用於寫進 tracked 檔或回報給使用者的摘要句；口頭推理過程不適用。
- **Evidence**：本 session 4 例。全域 CLAUDE.md「證據先於斷言」已涵蓋「有沒有來源」，但這 4 例都**有**來源、只是轉述時走樣——是另一個形狀。**Hypothesis**。
- **Minimum Sufficient Intervention**：不新增規則（寫不出 enforcement 掛點 → 依規則降級為 Observe）；在既有 memory `feedback_claim_first_discriminating_oracle` 第 3 點的 Why 已記本次兩例，再累積。
- **Promotion**：Case Memory（已併入既有 memory），待使用者決定是否升級。

### 五、檔案異動

錨來源：本 session 開工 commit（80fd84b、開工於 2026-10-12T08:18:16）——列 80fd84b..HEAD

- `2551ea0`：`superpowers-bridge/`（schema.yaml、VERSION、README 中英、templates/retrospective.md）、`.github/workflows/version-check.yml`、`CLAUDE.md`、頂層 README 中英、`docs/roadmap*.md`、change 產出物。
- `ba68235`：`backlog.md`、`backlog-crosscheck-shadow.json`（週檢）。
- `58b907e`：change 搬進 `openspec/changes/archive/2026-10-12-executor-governance-wording/`（新增 verify.md、retrospective.md、retro-s6-audit.md）；`openspec/specs/{release-versioning,tdd-claim-accuracy}/spec.md`；`superpowers-bridge/README.zh-TW.md`。
- `c49a2d9`：`CLAUDE.md`、`backlog.md`、`docs/superpowers/research/`（四維度文件＋索引）。
- `e8515cc`：`docs/roadmap*.md`、`backlog.md`。
- 本收工 commit：本交接檔、`workflow-harness/work-map.jsonl`。

### 六、下一步建議

1. Codex 額度恢復後補審 v5.0.0（見接力棒第一條）。
2. 從工作地圖挑下一件：`task-20261012-non-sdd-execution-support`（§9 研究）或 `task-20261007-superpowers-6x-rebaseline`。
3. 有空時一次修 backlog 那條 a–e 舊文件小問題。
