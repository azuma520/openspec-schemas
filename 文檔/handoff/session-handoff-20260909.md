# Session Handoff — 2026-09-09

## Session 08:42

### 一、本 session 主題

**審查行為來源的兩輪唯讀考古 + 初步觀察記錄落檔。** 本 session 自 2026-09-08 17:59 開工、跨日。使用者指定「先不要修改任何檔案」做兩件事：①追「把 PASS/BLOCK 規則當演算法重推、構造反例」這個審查方式的來源（A–E 分類）；②回到 Codex 原始 rollout 重建 2026-09-07 外部審抓出五個 P1 的過程（H1–H4）。最後一輪由使用者解除唯讀，把觀察寫成 `docs/superpowers/research/2026-09-09-review-provenance-analysis.md`。`fix-v2-blocking-defects` 全程維持凍結，未動 worktree、未 archive、未 push。

### 二、完成事項

- 「當演算法讀」來源分類完成（A–E）：skill 層無此要求；上位規則（全域 CLAUDE.md:30、:23）＋主 Agent 派工具體化＋reviewer 自構反例共同形成。fallback 那份「as an algorithm」派工單是 09-08 04:48:59Z 先寫給 Codex、配額耗盡後原文轉派。
- 0907 Codex 外部審重建完成：rollout `~/.codex/sessions/2026/09/07/rollout-…01a079b1….jsonl`，48 次 tool call 逐一對到五個 P1 的發現鏈；69 個 reasoning 全加密無摘要。
- 0907 那份 2801 字 prompt 來歷查清：主 Agent 未呼叫任何 review skill、未讀模板，骨架來自 `codex-invocation.md` 規則，題目來自 repo CLAUDE.md 翻譯。
- 觀察記錄落檔：`docs/superpowers/research/2026-09-09-review-provenance-analysis.md` + `research/README.md` 索引加一列。
- 封裝候選檢查：backlog 無未結案 `[SOP 候選]`，本次完成事項無命中、Tier 1 A/B 皆不過，痛點僅記入四【當日洞見】。

### 三、未完事項 / 接力棒

- [#接力] **doc gate 欠債**：本 session 新增 / 修改的兩份 `.md` 未跑 `/codex-review-doc`（`[DEVIATION]` 已在對話中明示：使用者指示寫完即收工）。下個 session 開工先補這道，或在 D1–D5 複盤時一併審。
- [#接力] **Codex code plane 補審**仍是唯一擋住 archive 的事（承 0908 接力棒；額度 09-08 17:27 已恢復，本 session 未派）。流程不變：補審 → active change 內修 → archive → push → PR → CI。
- [#接力] **兩條既有紀錄待更正**（詳見 research 文件 §0、§4）：`retrospective.md` §「哪一層抓到什麼」與 0908 handoff 四【當日洞見】前兩條的「十一席當散文讀」；brainstorm.md 的「五 P1 一個形狀」若當 D1/D4 前提要先改成 Codex 的三類分組。凍結中未動，等複盤一起決定載體（errata / retrospective 補段）。
- [#接力] 0908 接力棒其餘未動項照舊：D1–D5 複盤、D5-2 錯誤前提更正形式、worktree 分支上 backlog line 88 待刪 / line 84 bump、`.gitattributes` 補 bridge 目錄。**注意 backlog.md 已在 main（86 行）與 worktree 分支（89 行）分叉**，清理時要選邊。
- [#不重議] archive 前不得宣告完成；D2 不併入本 change；凍結期間不 teardown / 不刪 `.superpowers/sdd/plan/` / 不 archive / 不 push（承 0908）。
- [#待確認] work-map 引擎警告：`workflow-harness/work-map.jsonl` 有未知欄位 `evidence`（parser_warning、已保留）。是否清掉由使用者決定。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **考古一開始我把 reviewer 的報告檔當成派工單讀。** `code-review-fallback.md` 是 reviewer 寫的報告，真正的派工單只存在 Claude transcript 的 Agent 呼叫裡；差點把「Reviewer 自述 read as an algorithm」誤判成「派工要求」。**attribute:** 全域 CLAUDE.md「先讀『實際驗到什麼』再讀『名字說驗什麼』」——檔名說 review，內容是回覆。**propose action:** 既有規則涵蓋，不新增；記為「考古時先分清誰寫的」的承重案例。
- [#觀察] **兩份已進版控的事後歸納被原始資料推翻**（「十一席當散文讀」「五 P1 一個形狀」）。共同機制：主 Agent 收工時把多來源結果壓成一句好記的話，隔天那句話就成了派工單與複盤的前提。累積數：本 session 2 例（同一根因）。距任何門檻未知——先記著，若下次複盤或派工再出現「事後一句話成為前提」的形態就升 backlog 條目。
- [#接力] Stop hook 與使用者「不得改檔」指示衝突時，本 session 選擇以使用者指示為準、兩次拒寫 handoff 直到使用者解除。這個選擇要不要固定成規則由使用者決定，目前只是案例。

**【當日洞見】**

- **Codex 的 reasoning 在 rollout 裡全加密**，能看的只有 tool call、輸出、6 段中途訊息。所以任何「Codex 為什麼想到」的判斷都是推論，只有「它先查什麼、再查什麼」是事實。fallback reviewer 的 thinking 區塊同樣是空的。
- **0907 最有效的外部審 prompt 沒經過 skill**。真正起作用的是主 Agent 把 repo CLAUDE.md（耦合表、紅旗、CI grep 形狀）翻成七條題目；P1-5 幾乎是「耦合表是否被遵守」那條的直接產物。
- **Codex 自選、prompt 沒要求的高價值動作**：先寫五步計畫、全文讀而非讀 hunk、以「遷移換掉了哪個假設」為搜尋策略、作者指令與檢查器對讀、三次自選量測（數 checkbox / 跑 validate / 比 dogfood 副本）全命中、讀到維護者的延後紀錄仍反對。
- **H3 的證據分兩半**：殘留類（P1-3 → P1-4）有單一 rg 同時涵蓋兩類用語的擴散證據；決定性檢查類（P1-1、P1-2）沒有可見擴散、反例只在報告文字裡、未執行。
- **H4 不能從單次資料判斷**：沒有同 prompt 換模型或同模型換 prompt 的對照。
- **本 change 19 個審查席位中，全部 blocking finding 來自三個 change-level 席位**；純文件 task 的 review + re-review 雙席位貢獻為零。這是「邊界該畫在有沒有可證偽證據」的觀察依據，尚未拍板。

### 五、檔案異動

錨來源：本 session 開工 commit（5aa19bf、開工於 2026-09-08T17:15:23）——列 5aa19bf..HEAD

`5aa19bf..HEAD` 為空（main 無新 commit）。working tree 改動：

- `docs/superpowers/research/2026-09-09-review-provenance-analysis.md`（新增）——兩輪考古的觀察記錄
- `docs/superpowers/research/README.md`（修改）——索引加一列
- 未追蹤且刻意排除：`文檔/handoff/session-handoff-{20260903,20260904,20260907,20260908,20260909}.md`、`2026-08-27-brainstorm-產品承諾.md`、`.claude/worktrees/`

**無專案資料夾** → 專案 Changelog skip。**驗收節點 sentinel 區段無條目** → skip。
**work-map 無需變更**：本 session 只做分析、零 record 狀態變化（`task-20260907-fix-v2-blocking-defects` 維持 DOING）。

### 六、下一步建議

1. **先補 doc gate**：對 `2026-09-09-review-provenance-analysis.md` 與 `research/README.md` 跑 `/codex-review-doc`（Codex 額度已恢復）。
2. **派 Codex code plane 補審**（承 0908，與 3 可平行）——這是 archive 的唯一前提。派工單可沿用 09-08 04:48 那份，但依本 session 觀察加一句「這次改動換掉了哪個結構性假設、列出依賴它的表面」。
3. **D1–D5 複盤**，材料多了一份：research 文件 §0 的兩條推翻與 §3 的觀察者判斷。複盤前先決定「名稱大於斷言」還當不當前提。
