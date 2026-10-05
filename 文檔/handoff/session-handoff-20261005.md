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

## Session 10:18

### 一、本 session 主題

開工三步驟後，依使用者「分析任務依賴與性質、派 agent 併行、再討論」：5 個唯讀 agent 平行調查（紅旗三條、task-brief、brainstorming 漂移、FOCUS 槽、VS 下一件 A／B 備料）→ 逐題裁定；backlog 週檢；Verification Strategy 第二步 B（第一個一般程式對照案例）；盤點表補 F-VS11；兩個 commit 一起 push；收工前保存 A 的最小證據包、定下一個 session 做 A。

### 二、完成事項

- **5 個唯讀調查 agent**（報告已隨暫存區清理；結論在本區塊與工作地圖）：每份主 session 都回原檔抽查 2–3 處出處，全部對得上。
  - 紅旗三條：「executing-plans 不派獨立 reviewer」在 repo 現行規範 9 處＋**主 spec `tdd-claim-accuracy` REQ-3**（三條待辦都沒提到；只改其他處會反違主 spec）；「須隨 apply schema change、不可先行」不是正式設計要求（work-map 自加）；spike 報告 B-i 搜遍 handoff **未裁定過**。
  - task-brief：只認 `#+ Task <數字>`、無參數；實測 `## 1.1 —` exit 3、`## Task 1.1 —` 可用；只改 README 擋不住（apply 執行者讀 schema.yaml）。上游另有兩個錯：傳 1 抓到 1.1/1.2/1.10、最後一個 task 後的段落被吞。
  - brainstorming：三路徑仍在，真正衝突是**結束步驟與寫檔指令**；「產出稀薄」查無實例。
  - FOCUS：契約允許但「事先固定清單」算不算使用者提供是灰區；§5.4 題 2 接近被禁的「指定攻擊目標」。
- **使用者裁定**：VS 下一步走 B（A 不獨立開、C 保留）；相容性 change 未來只裝「修 executing-plans 理由（不重評 fallback）＋task-brief 寫進 apply 說明 workaround」，brainstorming 不塞；task-brief 上游問題要回報；REQ-PB、FOCUS **取消**（已改，`ed47186`）；brainstorming 改描述、CLAUDE.md 紅旗撤依賴 → **乙：暫不動**（登記工具只能改狀態，改描述需取消重登、會換代號；新說法見三）。
- **backlog 週檢 W41**（`ed47186`）：刪安裝帶入的 4 條範本示範（L80–83，與 workflow-harness `templates/backlog.md:80-82` 逐字相同）；「裝 smart-commit 腳本」標 done（兩支腳本 `7a426fa` 08-28 即在 main；`--execute` 行為本次未重跑）；shadow 帳一併 commit。第一次刪除被護欄擋下（讀檔把 CRLF 轉 LF、snapshot 對不上），照原文重送才成功。
- **workflow-harness bug 已交給該 repo 的 session**（使用者直接貼過去）：shadow 四輪時間盒在本 repo 永遠走不完——W37／W38／W39／W41 全為 `incomplete_coverage`，因 6 條 open 待辦皆無粗體標題、0 條可掃。本 repo 不修。
- **VS 第二步 B**（`7083983`）：`docs/superpowers/research/2026-10-05-verification-comparison-case-resurface.md`＋索引——12 條 claim 主鏈表、層表／finding 表、§3 框架適配、§4 驗證器材出錯 11 筆（A 樣本）、§5 單案例假說 H1–H5（不升格）、§6 裁定（盤點表分類暫不改，等第二個程式案例）。盤點表補 **F-VS11**（修正時寫反 drift issue 觸發條件；原文從 Codex rollout 找回，對照 `version-check.yml` 的 `if:` 逐字比過）。Codex 文件審 r1 ⛔ 1 🔴（把盤點表「重新發現」定義講窄）＋4 🟡 事實錯 → 修 → r2 ✅。
- **push**：8 commit 推上 `origin/main`（`7268814..7083983`，fast-forward）；CI Validate schemas ✅。
- **A 的最小證據包**：`docs/superpowers/research/evidence/2026-10-05-resurface-verifier-pack/`（`mutants.py`、`mut-vp{,2,3}.{json,err}` 逐 byte 複製、`cmp` 相同＋`PROVENANCE.md`）；對照文件加一句指過去。Codex 文件審見本次收工 commit 前的結論。
- work-map：新增 `task-20261005-vs-step2-a-verifier-reliability`（**NEXT**，掛 VS 研究下）、`task-20261005-superpowers-task-brief-upstream-report`（TODO，掛 task-brief 下）。

### 三、未完事項 / 接力棒

- [#接力] **下一個 session 只開一條研究線：VS 第二步 A**（`task-20261005-vs-step2-a-verifier-reliability`，description 有完整研究問題、兩組證據、範圍與停止條件）。不做 backlog 整理或相容性雜務。
- [#接力] 今晚 10-05 22:00 台北 fork 每週排程：開工時已過 22:00 才查（issue #2 只多一則留言、無新 issue），未到不阻塞主線。
- [#不重議] verify-sync lifecycle 留在 VS 研究底下、**不當下一步**（規則會建議自動標 NEXT，依使用者裁定不標）。
- [#不重議] 乙案：以下兩條工作地圖描述已過時、等真的啟動再取消重登——
  - `task-20260826-fix-brainstorming-drift` 實際問題：三條路徑（spike／bounded／architectural）的**結束步驟與寫檔指令互相衝突**（bounded 直接寫程式、architectural 交給 writing-plans），不是「產出太少」。
  - `task-20260901-claudemd-governance-rewrite`：撤掉「不可先行、須隨 apply schema change」依賴（非正式設計要求）。
- [#接力] 相容性 change 未來開時：B-i 已裁定「只修理由文字、不重評 fallback」；**REQ-3 主 spec 要一起改**；task-brief 走 apply 說明 workaround、不改標題格式（避免 schema major）。
- [#接力] 先不碰：盤點表 §0／O6「原始報告都消失」——Codex rollout 其實多仍在 `~/.codex/sessions/`，說法可能要改成「repo 內沒有、repo 外可能還在但無保存保證」。
- [#接力] 照舊：`v3.0.0` tag 未打；本機空目錄 `.claude/worktrees/requirement-scenario-identity` 待重開機後刪；公開 review-fix-propagation、workflow-harness 三條這輪未動。

### 四、洞見 / 反省

**【紀律接力】**

- **「轉述出處的定義／條件」又錯，今天 +1**：B 對照文件 r1 🔴 把盤點表「重新發現」的定義講窄（原文「同一缺陷先前已被記錄（含被 defer）」）。和昨天「把 version-check 觸發條件寫反」同一族，差別是這次轉述的是**另一份研究文件的定義**、不是程式條件式。做法照舊、範圍擴大：**轉述任何出處（程式、規格、自己 repo 的其他研究文件）的條件或定義，寫完拿出處原文逐字比一次。**
- **派 agent 備料後，主 session 回原檔抽查關鍵出處**：今天 6 份 agent 報告各抽 2–3 處全部對得上；抽查真正派上用場的是補 agent 沒查的範圍（例：B-i 有沒有被裁定過，是主 session 搜遍 handoff 才確認）。

**【當日洞見】**

- **盤點表 §0／O6 的前提可能不成立**：Codex 原始對話仍在 `~/.codex/sessions/`（F-VS11 就是從那裡找回原文）。先不碰（使用者裁定）。
- **B 案例最重要的反例**：起點備忘「TDD 內建判別力」在一般程式案例不成立——Task 1 的 RED 是「屬性不存在」，判別力來自另做的反向對照與變異測試。單案例、不升格。
- **週檢四輪時間盒在本 repo 永遠走不完**：表面有 timebox、實際不可能滿足、畫面沒有明顯警示；已交 workflow-harness。
- **寫入護欄有效**：CRLF→LF 讓 snapshot 對不上，triage execute 整批 `not_executed`，零誤刪。
- 封裝候選檢查：backlog 無 open `[SOP 候選]`；「轉述出錯」已有載體（紀律接力），屬範圍擴充、不新開條目。

**【學習候選】**

- **Case**：轉述盤點表的定義時講窄被 Codex 擋下；前一天修正時把 CI 觸發條件寫反也被擋下——兩次都是轉述出處時沒有逐字對照。
- **Candidate Pattern**：轉述「X 的定義／觸發條件」時，以出處原文為準逐字比對；出處不限程式碼。適用：任何重述他處規則、定義、條件的句子；不適用：純意見或摘要性描述。
- **Evidence**：Hypothesis——「修正時又寫錯」族已 5 例，其中 2 例是轉述出處。
- **Minimum Sufficient Intervention**：不新增規則；把紀律接力那條的適用範圍從「程式條件式」擴大為「任何出處的定義或條件」。
- **Promotion**：Refine Existing Strategy（紀律接力那條）。

### 五、檔案異動

錨來源：本 session 開工 commit（61b1f10、開工於 2026-10-05T08:13:32）——列 61b1f10..HEAD

- `ed47186`：`backlog.md`、`backlog-crosscheck-shadow.json`、`workflow-harness/work-map.jsonl`（REQ-PB、FOCUS 取消）
- `7083983`：`docs/superpowers/research/2026-10-02-verification-evidence-inventory.md`、`docs/superpowers/research/2026-10-05-verification-comparison-case-resurface.md`（新）、`docs/superpowers/research/README.md`
- 本次收工：`docs/superpowers/research/evidence/2026-10-05-resurface-verifier-pack/`（新，8 檔）、對照文件加一句、`workflow-harness/work-map.jsonl`（兩條新待辦、A 標 NEXT）、本 handoff

### 六、下一步建議

1. 開工先讀本 handoff（今天很多刻意 deferred 的項目），不靠記憶續做。
2. 開工時已過今晚 22:00 → 先查 fork 排程（issue #2 只多一則留言、無新 issue），完成即收；未到不阻塞主線。
3. 做 VS 第二步 A（`task-20261005-vs-step2-a-verifier-reliability`）：先做兩組證據的 failure-mode inventory、守停止條件（跨組重複 < 3 類即停並回報），結尾只回答「A 的結果是否足以讓 C 升成下一題」；不做 C。


## Session 14:09

### 一、本 session 主題

照接力棒只開一條研究線：Verification Strategy 第二步 A（驗證工具本身會怎麼失效）。兩組內部證據做 failure-mode inventory → 使用者三項裁定 → 寫研究文件 → Codex 文件審三輪（中途額度用完、排程後接續同一對話）→ commit → A 結案、C 改題登記。

### 二、完成事項

- **A 的 failure-mode inventory**（`4a45721`）：`docs/superpowers/research/2026-10-05-verification-step2-a-verifier-failure-modes.md`＋索引一列。第一組＝盤點表 O2 5 筆（回 ledger、Identity／RS retrospective、Identity `verify.md` 核對原文）；第二組＝對照文件 A1–A11（證據包 `mut-vp*.json` 確認 id 12 活口）。按**壞法**分 7 類；跨組 3 類：① 只驗比 claim 更窄的代替品（2 對 3，相對穩）、② 執行環境偏差（1 對 1，弱）、③ 輸出格式表達不出需要的區分（1 對 1，弱）；④ 自我檢查不完整為 conditional。F-ID6 換成按後果分類仍是 3 類。**未觸發停止條件**，只代表 A 不必中止、不是一般化結論。
- **使用者裁定（2026-10-05）**：分類定位為 working taxonomy；本輪不讀 OPA（留給 C 的 targeted source）；A 足以讓 C 升題，但 C 改為「Completion Gate 的信任鏈」，分 (a) 執行／強制、(b) 判定可靠兩子問題；改題理由只引用跨組的 ①②③，⑥ 反向對照假紅、coverage 缺口標單組／附條件。核心句：programmatic enforcement 是提升可靠性的手段，但不是 verifier correctness 的充分條件。
- **Codex 文件審**（thread `01a10a30…`，三次回覆）：r1 第一次跑到一半額度用完（exit 1、無報告）→ 使用者選乙等恢復、改為**接續同一對話**而非開新對話 → 13:17 排程接續 → ⛔ 1 🔴（selftest 15／16 兩版混寫，`blind-kit/v2/FROZEN.md` Fix round 1／Fix round 2）→ 修 → r2 ✅ → 同類實例也在**盤點表 L-ID5** 修（使用者選甲）→ r3 ✅。review-state 已記 pass。
- **工作地圖**：`task-20261005-vs-step2-a-verifier-reliability` → DONE；新登記 `task-20261005-vs-completion-gate-trust-chain`（NEXT，掛 VS 研究下，描述含 (a)(b) 與立題依據邊界）。
- 封裝候選檢查：backlog 無 open `[SOP 候選]`，無命中。

### 三、未完事項 / 接力棒

- 研究 commit 原為 `b01918b`，訊息漏了主旨後空行；使用者授權後 amend 為 `4a45721`（只改訊息、內容不變、未 push）。
- [#接力] 本 session 的 scratchpad 審查暫存（`a-review/`：prompt／log／report／exit 檔與腳本）**未清**——AI 的 `rm` 被擋，需使用者手動刪。
- [#接力] 下一題 C（`task-20261005-vs-completion-gate-trust-chain`）**開新 session 再做**；起點證據：A 文件 §3（自我檢查的觸發方式皆非程式強制）、§6（(a)(b) 子問題）、起點備忘 §4。OPA 只讀 policy testing／coverage／negative cases 三項。
- [#接力] 今晚 10-05 22:00 台北 fork 每週排程：本 session 結束時未到，下個 session 若已過 22:00 先查（issue #2 上次只多一則留言）。
- [#不重議] A 的分類**不回寫盤點表 taxonomy**（只修了 L-ID5 一格事實錯誤）；④ 與 coverage 缺口屬「條件代表性」題，不算 verifier failure mode。
- [#接力] 照舊：`v3.0.0` tag 未打；本機空目錄 `.claude/worktrees/requirement-scenario-identity` 待重開機後刪；早上 handoff 列的乙案兩條過時描述、盤點表 §0／O6 說法維持不碰。

### 四、洞見 / 反省

**【紀律接力】**

- **「轉述出處」又錯，今天 +1，而且是轉述數字**：selftest「16 項」是修正後的數，我把它和修正前「沒涵蓋重複案例」寫在同一句，被 Codex 擋下；盤點表 L-ID5 早就是同一種混寫，我照抄了一次。做法擴充：**轉述計數時，連同「這個數是哪一版的」一起比對**，不只比字面。
- **沒有來源的理由不要拿來支撐建議**：今天兩次——「接續舊對話不划算」（使用者追問後收回，實際算不出哪邊省）、「有效的自我檢查幾乎都是作者自己選擇去跑的」（寫文件前回查才發現觸發方式有四種）。兩者都是用來推一個選項的理由句，比事實句更容易漏檢。

**【當日洞見】**

- **A 最重要的產出是「程式化不是充分條件」**：出錯的驗證工具很多本身就是程式（`grade.py`、verify 腳本、測試套），所以 C 不能只問「怎麼把 Gate 改成程式」。
- **兩個案例都是「第一道自我檢查不完整，由另一種產生方式不同的檢查補上」**（selftest 漏重複案例 → Codex 審；手工反向對照漏 id 12 → 變異測試）。單案例層級，未升格。
- **Codex 額度中斷可接續同一對話**：`codex exec … resume <id>` 在額度恢復後可用，接續後的報告 session id 與原對話一致（本次三輪皆核對）。
- **`git commit -F -` 的訊息若主旨後沒空行，整段變主旨**：今天實際發生。

**【學習候選】**

- **Case**：本 session 兩次把「沒查過的理由」講成事實來推選項（接續成本、自我檢查觸發方式），一次被使用者追問收回、一次自己回查更正。
- **Candidate Pattern**：給選項附「為什麼」時，理由句和事實句一樣要有來源；算不出來就說算不出來。適用：任何「建議 X，因為 Y」的 Y；不適用：明確標成推論的句子。
- **Evidence**：Hypothesis——本 session 2 例；與全域「證據先於斷言」同族，差別是落在理由而非結論。
- **Minimum Sufficient Intervention**：不新增規則；全域「證據先於斷言」已涵蓋，只是在「端選項」時執行不到位。先記在紀律接力觀察。
- **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（0cd728e、開工於 2026-10-05T11:18:46）——列 0cd728e..HEAD

- `4a45721`：`docs/superpowers/research/2026-10-05-verification-step2-a-verifier-failure-modes.md`（新）、`docs/superpowers/research/README.md`、`docs/superpowers/research/2026-10-02-verification-evidence-inventory.md`（L-ID5 一格）、`workflow-harness/work-map.jsonl`
- 本次收工：本 handoff

### 六、下一步建議

1. 確認 scratchpad 的 `a-review/` 已手動清掉。
2. 若已過 10-05 22:00：先查 fork 每週排程，完成即收。
3. 開 C（`task-20261005-vs-completion-gate-trust-chain`）：先用 A 文件 §3、§6 與起點備忘 §4 定 (a)(b) 兩子問題的內部證據，再決定 OPA 三項要不要讀；不把 A 的單組／附條件發現當結論。
