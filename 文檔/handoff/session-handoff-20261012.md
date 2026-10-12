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
