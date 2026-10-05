# Session Handoff — 2026-10-05

## Session 08:07

### 一、本 session 主題

接 2026-10-02 17:46 區塊（session 開工於 10-02 17:55，跨日到 10-05 收工）：Verification Strategy 第二步——審並 commit 起點備忘、完成內部證據盤點表；另派 agent 做產品承諾 SSOT 語意比對，依結果讓 brainstorm 退出版控。

### 二、完成事項

- **第二步起點備忘＋研究索引**：Codex 文件審 2 輪（thread `01a0fc12-…`；r1 ✅ 1 🟡「66 個 finding」應為「分類單位」→ 修；r2 ✅ 0 意見）→ 授權 commit `3cc1ad2`。
- **產品承諾 SSOT 比對**（背景 general-purpose agent，唯讀）：三個承諾拆 15 個語意要素，方向文件／正式設計全部承接；未承接的只有未拍板暫定想法、推理理由、審查過程紀錄。使用者裁定：**brainstorm 退役**（只退出版控、檔案仍在本機）、**方向文件也算正式來源**（G1–G3 定義只在方向文件 §1.2，正式設計 0 次提到 G2）、承諾措辭比正式設計 §8 強→**先不改**、「審查結論是不是完成條件」→**轉研究輸入**。結論寫進備忘 §8。
  - `.gitignore` 一行：Codex 程式碼審 ✅（thread `01a0fc18-…`）；precommit runner `⚠️ NO CHECKS RUN`（repo 無 lint／測試），改跑 schema validate ✓＋`git check-ignore` 確認 → 授權 commit `65c2ee4`。
  - work-map：`task-20261002-product-promise-ssot-check` → DONE。
- **內部證據盤點表** `docs/superpowers/research/2026-10-02-verification-evidence-inventory.md`＋索引一列 → 授權 commit `5337c8d`。
  - 內容：§0 六個來源的完整性（**每個來源都缺部分原始審查報告**，RS 的 SDD ledger 隨 worktree 整份消失）；層表（claim／oracle、執行者與強制機制、成本 proxy、快照、已知漏抓）＋ finding 表（首次／重新、前一層是否已漏、沒抓到的後果〔推論〕）；§3 觀察 O1–O8（後層額外偵測、讓證據失真的 finding 多落在驗證器材、原標嚴重度與後果不一致、成本資料大多未知）。
  - 審查經過：Codex 首派撞額度上限（exit 1）→ `[REVIEWER_FALLBACK] plane=doc_review from=codex to=contract-neutral-reviewer reason=quota`，使用者指定 fable → ✅（SENTINEL_VALID）3 🟡＋2 ⚪ 已修 → 使用者裁定 A：cron 於 10-02 21:52 補跑 Codex 首次派發（thread `01a0fce3-…`）→ ⛔ 3 🔴（F-ID10a 誤標首次、F-VS7 誤標重新發現、version-check 能力低估；fallback 都沒抓到）→ 修 → r2 ⛔ 1 🔴（**修正時把 drift issue 觸發條件寫反**）→ 修 → r3 ✅。
- work-map：`task-20261002-vs-step2-evidence-inventory` TODO → DOING（開工時）；本次收工標 DONE（見五·五結算）。

### 三、未完事項 / 接力棒

- [#接力] **盤點表待補一筆**：Codex r2 的「修審查意見時把觸發條件寫反」是本文件自己審查過程的資料點，使用者裁定 A：先記在本 handoff，**下次修改盤點表時補進 L-VS2e／F 表**（補了要重審）。
- [#接力] **第二步之後的下一步未定**：研究題底下只剩 `verify-sync lifecycle`（TODO），依既有裁定**不標為研究的下一步**；備忘 §7 的研究題（Claim↔Oracle 對齊、RED 等價物、條件代表性、Assurance 分層、驗到哪停、證據保存、依成本訂政策、對照組）與 §7a 外部來源（OPA 有限度讀、Anthropic eval）要由使用者挑下一件。
- [#接力] **今天 10-05（一）22:00 台北**：fork 每週 version-check 排程會跑，確認 issue #2 只多一則留言、沒有新開 issue。
- [#接力] 本機 main 領先 origin 5 commit（`7268814`、`57ea8eb`、`3cc1ad2`、`65c2ee4`、`5337c8d`）＋本次收工 commit，未 push。
- scratchpad 審查暫存已由使用者清空（AI 刪除被權限擋）。
- [#不重議] 產品承諾：brainstorm 已退役；方向文件是正式來源、不可刪；承諾措辭與「審查結論是否為完成條件」不另開追蹤（見備忘 §8）。
- [#接力] 照舊：`v3.0.0` tag 未打；`backlog-crosscheck-shadow.json` 未 commit；本機空目錄 `.claude/worktrees/requirement-scenario-identity` 待重開機後刪。

### 四、洞見 / 反省

**【紀律接力】**

- **修審查意見時自己又寫錯，今天再 +1**（盤點表 r2：補 version-check 能力時把「驗證失敗才開 issue」寫成「任一成立就開」）。10-02 已有 3 例（P2 衝突兩端、P4 摘要、retrospective 相對指標）。既有載體是 review-fix-propagation skill 與全域「修正絕對句時寫出的替代句要再過一次例外檢查」；這次的錯是**改寫一段描述時沒回頭對照原始碼的條件式**。修完後把新句子拿去和出處（這次是 `version-check.yml` 的 `if:`）逐字比一次。
- **fallback 與 Codex 各抓到不同東西，不要只靠一層**：盤點表 fallback 漏了 3 個 🔴，全在「首次／重新」與「前一層已漏」兩欄——正是盤點表要回答的增量欄位。研究類文件仍以 Codex 為 Gate（與第一步 §5d 先例一致）。

**【當日洞見】**

- **盤點表自己就是 P6 的實例**：要盤點的審查紀錄，原始報告大多已隨 scratchpad／worktree 消失，只剩摘要；本 session 的審查報告也照清理規則刪了，只剩盤點表的轉述。
- **讓證據失真的 finding 多落在驗證器材**（評分器、回報格式、verify 腳本、PRECHECK），由多種不同層抓到——可能是第二步最值得往下追的觀察。
- **原標嚴重度不能當增量價值的代理**：RS 的排除句漏限定條件標 Minor、ID 兩條先判 Minor 被 defer，後果都比標記重。
- 封裝候選檢查：backlog 無 open `[SOP 候選]`；「修正時又寫錯」已有載體，屬載體執行不夠力，只記於此、不新開條目。

**【學習候選】**

- **Case**：修審查意見時改寫一段描述，把原始碼的條件式（OR 的其中一支是「失敗」）寫反，下一輪審查才抓到。
- **Candidate Pattern**：改寫「某程式何時觸發」這類描述時，以原始碼的條件式為準逐字對照，而不是憑記憶改寫。
- **Evidence**：Hypothesis——本次 1 例；與既有「修正又寫錯」累積 4 例同族，但其中只有這例是條件式。
- **Minimum Sufficient Intervention**：不新增規則；下次修審查意見跑 review-fix-propagation 時，對「描述程式行為」的句子多一步回原始碼對照。
- **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（4bfb2e1、開工於 2026-10-02T17:55:47）——列 4bfb2e1..HEAD

- `3cc1ad2`：`docs/superpowers/research/2026-10-02-verification-strategy-step2-starting-memo.md`（新）、`docs/superpowers/research/README.md`
- `65c2ee4`：`.gitignore`（忽略 `2026-08-27-brainstorm-產品承諾.md`）
- `5337c8d`：`docs/superpowers/research/2026-10-02-verification-evidence-inventory.md`（新）、`docs/superpowers/research/README.md`
- 本次收工：`文檔/handoff/session-handoff-20261005.md`（本檔）、`workflow-harness/work-map.jsonl`（product-promise DONE、盤點表 DOING→DONE）

### 六、下一步建議

1. 挑 Verification Strategy 的下一件：建議從盤點表 §3 O2「驗證器材本身要被驗」接 P3 Claim↔Oracle 對齊（備忘 §7 第一題），或先做 §7 的對照組（找 workflow-harness 一個一般程式案例重拆）——由使用者選。
2. 今晚 22:00 後看 fork 排程：issue #2 只多一則留言。
3. 決定要不要 push（本機領先 6 commit）；補盤點表那一筆時記得要重審。
