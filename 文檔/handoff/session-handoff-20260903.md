# Session Handoff — 2026-09-03

## Session 08:02

### 一、本 session 主題

loosen-plan apply 執行（2026-09-02 開工、跨午夜）：照 schema 自己的 apply 指令走完整流程 —— push 對齊 → worktree + branch → subagent-driven-development 逐 task 派工 → 每 task 獨立審查 → 群組邊界 commit。25 步完成 12 步，在批次 B 審查中撞到 subagent 額度上限而中斷。

### 二、完成事項

- 開工三步驟 + 接力棒 3 條逐條交代；push `main` 3 個 commit 對齊 origin，**Actions 自動觸發實測成功**（run 33598507429，`push` 事件，14 秒綠）—— 拖三個 session 的接力棒兌現。
- 使用者裁定走 **(a) worktree + branch + PR**，理由：正在修改的就是 workflow 本身，而 apply step 1/6 在本 repo 從未 dogfood 過。前置條件：先確認 3 個 commit 該進 main 再 push 對齊。
- `EnterWorktree` 建 `worktree-loosen-plan`（base `5aa19bf` == origin/main）。
- **群 1-5 完成 10/10**（schema.yaml 全部 + VERSION），commit `932a044`：plan 指令 → Plan Contract、tasks 指令 → TDD 標註文法 + RED/GREEN 證據契約、apply 指令 TDD 段落改寫、verify 指令新增 5 條確定性檢查 + 4 條審查判斷 + 強制力邊界、top-level description 移除 writing-plans、`version: 1→2` / VERSION `2.0.0`。
- **群 6-9 完成 2/11**（6.1 + 6.2 模板，已審已清）；批次 B（7.1+7.2+7.4，bridge README +83/−40、29 章節）已實作但**審查未完成**。
- 6 次派工、6 次完整審查、3 次 fix round、1 次盲測、28 條裁定（R0–R29）。
- 盲測（R21）：無 context 的 agent 拿中性改名 + 打亂的六個 fixture，**6/6 全中、零歧義**，並找出一個作者測不出的洞 → 補為第四條審查判斷 R4。
- Checkpoint 1 由使用者跑 `/smart-commit --execute` 完成。

### 三、未完事項 / 接力棒

- [#接力] **批次 B 未通過審查就留在工作目錄**：`superpowers-bridge/README.md` +83/−40。reviewer 開始讀 diff 後即因 `session limit` 掛掉、零產出。機械面我已自驗（dogfood IDENTICAL、四個過期詞 0 命中、v2 相容性列 CI 抽取可用、8 個 `writing-plans` 殘留逐一確認為提及而非要求），**內容判斷缺第二雙眼睛** —— 特別是三處超出指派範圍的改動、以及 v2 列該標 `v5.1.0` 還是 `v6.3.0`。**下次開工第一件事是重派這個審查。**
- [#接力] **tasks.md 的 checkbox 一個都沒勾**，`openspec list` 顯示 `0/25`。apply 指令明寫要隨任務完成更新，我全程沒做；verify 會拿這份 tasks.md 跑 check 8-12。
- [#接力] 剩 13 步：7.3（zh-TW 鏡像，須照批次 B 報告的「章節清單、依檔案順序」走）、8.1-8.4、9.1、群 10 四步（含 10.4 fresh-context smoke test —— **Q4-A 的第一個真樣本**）。
- [#接力] verify.md → retrospective.md → archive → PR；archive 在 Windows 必撞目錄鎖，走 `cp -r` + `diff -r` + 委派使用者 `rm -rf`。
- [#接力] **Codex independent review 未補**（跨 session 債，第三個 session）：補審前不 archive。
- [#接力] **執行報告草稿**在 `.superpowers/sdd/plan/REPORT-draft.md`（七節，已寫到群 1-5）—— 使用者要求「做完之後整理成文檔報告統一討論」，尚未補完。⚠️ 該檔在 SDD 工作區內，**最終審查後會被刪除**，補完前需先搬出。
- [#待確認] **D1：task 4.2 指錯檔案，三處過期宣稱無人涵蓋。** `templates/verify.md` 全檔零個 TDD 字樣（§4 是 Design/Specs Coherence），4.2 描述的文字實際在 `templates/retrospective.md:59`（`N/A — plan-step TDD only`）、`:63-64`、`schema.yaml:664`。**10.2 的掃描抓不到**（不含四句精確過期句、不含五個邊界詞彙）。`tdd-claim-accuracy` Scenario 2 禁止**任何** bridge-owned 規範面再說 TDD 經由 writing-plans micro-steps 抵達 —— 留著等於本 change 違反自己正在落地的規格。選項 (a) 補進本 change / (b) 延到後續 change；我建議 (a)，暫按使用者「執行中不擴 scope」原則照 (b) 處理。
- [#不重議] R0–R29 全部已裁定並記錄在 `.superpowers/sdd/plan/progress.md`；後續派工遇同題引用照辦。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **我在這次執行中製造了六個「形式完整、實質空洞」的產物**，全部不報錯、全部輸出一個有說服力的錯東西：① `review-pkg.sh` 扁平快照誤報整檔 DELETED、② 統計 `grep -c '^+[^+]'` 漏算空行報 `+61 -18`（實為 `+70 -22`）、③ fixture 目錄名 `f1-missing-annotation` 把答案印在路徑上（盲測會 6/6 全中而什麼都沒證明）、④ `review-pkg.sh` 的 "Untracked additions" 印的是 repo-wide status 而非該 task 新增、⑤ 用 `/tmp` 當 Python↔bash 中介、⑥ 快照式複審裡「pre-existing」相對於快照、而 guardrail 相對於 HEAD，兩個基準在第二輪就分岔。**attribute:** 全域 CLAUDE.md「證據先於斷言」+「先讀『實際驗到什麼』再讀『名字說驗什麼』」。**propose action:** 這六個裡只有第 ⑤ 個在產出任何結果前就被擋下 —— 因為只有它有 enforcement 掛點（hook 檢查 `/tmp` 字面）。其餘五個都是事後才被發現，其中兩個是 reviewer 發現的。這正是全域規則「寫不出掛點的規範要降級為 Observe」那句話的正面實證，建議寫進報告而非新增規則。
- [#反] **preflight 掃描漏了真的耦合缺陷，而且是用形式上成立的方式漏的。** 我列了 `2.1 ↔ 3.1/4.1/6.2` 的介面 pair row 並標 Clean，因為「誰生產誰消費」方向對；但從沒問「**是什麼讓三個消費者跟生產者保持一致**」—— 答案是沒有任何機械手段，所以 R11/R12/R15 只能一個消費者補一條地事後發明。同一隻病第二次：3.2 的邊界碰撞我只找到一個實例就當成全部，第二個實例在實作階段才冒出來（R17）。**共通點：我檢查了「邊界存在嗎」，沒檢查「邊界裡面裝了什麼」。**
- [#債] **Codex independent review 連三個 session 未補**；本 change 的 schema 契約屬高風險，全套只過 fallback 審 + 本 session 的 subagent 審。
- [#債] **未審查的工作跨 session 留在工作目錄**（批次 B）—— 這正是 repo 一路在防的「未清閘門」，這次發生在我自己身上。

**【當日洞見】**

- [#決策] worktree dogfood 三個環境發現，使用者裁定**定性為開發環境問題、不泛化為產品層**：E1 worktree 下 opsx **靜默切換 schema 並宣告 `isComplete: true`**（`openspec/schemas/` 被 gitignore → 新 worktree 沒有 bundle → CLI fallback 到 `spec-driven`、artifact 8→4、exit 0、無警告）；E2 `.claude/worktrees/` 未 gitignore 而原生 `EnterWorktree` 路徑無 ignore precheck（手動路徑有）；E3 **正面** —— harness 機械阻止 isolated session 對主 checkout 操作 git，也拒絕無法靜態驗證的複合指令。E1 的連帶後果：**10.1「重建 dogfood 副本」在 worktree 下是開工前置條件，不是收尾驗證** —— execution environment 改變後 task dependency 也跟著改變。
- [#決策] **commit 粒度 R8**（使用者裁）：review 維持 task-level、commit 改 group-level；**「有 commit」不得當成「review 已完成」的證據**。SDD 正常流程依賴 implementer task-level commit，而 repo governance 全域禁止（Anchor #4）—— 但 retrospective **不得**寫成「Agent 本來就不該 commit」，要寫成值得後續正式評估 Anchor #4 的事實基礎：worktree 可能不只是檔案隔離，而是**安全授予 worker 局部權限的 execution boundary**。
- [#取捨] **架構 learning**：重用 skill ≠ 繼承 skill 的權限假設。**skill 定義 procedure，repo / harness 定義 execution permission。** 具體實證：SDD 的 `task-brief` 腳本寫死 `## Task N` 標題慣例，對 Plan Contract 的 `## 1.1 —` 直接失效 —— schema 指定 SDD 當執行器，而 SDD 的輔助腳本綁在這個 change 正要移除的輸出格式上。
- [#決策] **Q4/D3 觀察，六次派工零卡住、零 scope expansion。** 三個正面樣本：1.1 自創「PRECHECK 行號前後比對」當邊界證據（brief 沒說怎麼證）；3.1 fix round **分辨「定義形式」與「指涉對象」**（這個區分不在 brief 也不在 finding 裡）並標記讓 controller 裁而非自作主張；4.1 fix round 2 **未經要求自行加 F7 正向對照**並驗證它在修正前會被假 BLOCK。反向細節：1.1 自選的證據方法比 reviewer 用的弱一級（行號位移 vs 單一 hunk 對 HEAD）—— 自主性給出正確結果 + 夠用但非最佳的證明，較強的由審查層補上，正是 D3 預測的分工。**注意：本 change 的 plan.md 是 v1 下手寫的，10.4 才是 Q4-A 的第一個樣本。**
- [#洞見] **check 12 找到的第一個缺陷，是它所要檢查的東西本身的缺陷。** 現行 v1 模板 `## Task 1: <name>` 在 check 12 下收集到零個 key → 照 v1 模板寫的 plan 會被 v2 的檢查擋下。這是真實 migration 問題不是理論風險，而且**盲測抓不到、作者也抓不到** —— 盲測只看得到作者想得到要造的 case。順序也值得記：tasks 文法在 2.1 審查抓到三個 Important 後被釘死，plan 文法有一模一樣的缺陷卻拖到 4.1 才浮現，因為**在 check 12 存在之前沒有任何東西檢查 plan 的形狀**。
- [#洞見] **規定證據不夠，證據本身也要能被驗證不是自我循環。** 這次唯一真正打破自我循環的是 R21 盲測（作者測自己的檢查不是證據），而它之所以有效，是因為在派工前最後一刻拿掉了 fixture 目錄名裡的答案。
- [#偏離] **check 9 的散文與確定性文字不一致（良性）**：散文說「紀錄在任務完成時才寫」，check 9 本身沒有這個豁免。實務無害（verify 在 apply 之後跑），但實作者把它寫成「check 9 對草稿狀態不適用」是**字面錯誤**，不得當定論記下。R29 記的不是要改 check 9，是**不要把它記錯**。
- [#建議] **subagent 回報經 teammate message 截斷 7 次**（承 9/2 記錄的 3 次，累計 10 次）。每次都要再發一則訊息索取尾段，而被吃掉的永遠是結尾的 verdict 行。可行緩解：派工時強制「verdict 放在 Spec Compliance 之後、不放結尾」+ 硬性行數上限，本 session 後半已改用此法、有效。

### 五、檔案異動

本 session 一個 commit（`932a044`）+ 三個未 commit 檔案：

| 異動 | 內容 |
|---|---|
| commit `932a044` | `superpowers-bridge/schema.yaml`（583→約 850 行）、`templates/verify.md`（+43，新 §8）、`VERSION`（1.0.1→2.0.0） |
| 未 commit | `superpowers-bridge/README.md`（批次 B，+83/−40，**未過審**） |
| 未 commit | `superpowers-bridge/templates/plan.md`、`templates/tasks.md`（批次 A，已過審） |
| 未進版控 | `.superpowers/sdd/plan/`（ledger `progress.md`、25 份 brief、各 task 報告、7 個 fixture、`REPORT-draft.md`）—— 已用 `.git/info/exclude` 本機排除，不進 PR |

錨來源：本 session 於 `5aa19bf` 起始（worktree base），列 `5aa19bf..HEAD`

### 六、下一步建議

1. **重派批次 B 的審查**（唯一開著的閘門）—— 順便測 subagent 額度是否恢復。四個判斷題已寫好：三處超出地圖的改動是否必要 / v2 列標 `v5.1.0` 還是 `v6.3.0` / 8 個 `writing-plans` 殘留逐一判定 / migration guide 對照設計四步，外加「章節清單對照 diff 是否完整」（漏列的章節會**安靜地**不被 7.3 鏡像）。
2. **裁定 D1**（4.2 指錯檔案、三處過期宣稱無人涵蓋）—— 這條會決定本 change 是否留下「違反自己正在落地的規格」的狀態。
3. **補勾 tasks.md 的 checkbox**，讓 `openspec list` 與 verify 讀到真實進度。
4. 續跑 7.3 / 8.x / 9.1 / 群 10 → checkpoint 2 commit → verify → retrospective → archive → PR。
5. **報告草稿先搬出 SDD 工作區**（該區在最終審查後會被刪除），再補完群 6-9 與群 10 的內容。

---

## Session 17:18

### 一、本 session 主題

完成 loosen-plan 的 verify / retrospective / 執行報告三份收尾產出，並以**三輪獨立 doc review + 一輪 targeted review** 過閘；過程中由報告的獨立查證**反向找出 change 本身違反自己新增的 check 12**，補上 plan 群 11 條目後重跑並雙向舉證。

### 二、完成事項

- **verify.md（653 → 707 行）+ retrospective.md（237 → 299 行）落地**，`openspec list` ✓ Complete 27/27，`openspec validate` 通過。verify.md 含五條確定性檢查對本 change 自跑（8/12 實質判定、9/10/11 空跑且為 design.md 事先預測）、盲測 6/6 + 正向對照、兩次 10.4 plan 生成樣本（run 1 因儀器缺陷作廢，裁定寫在 run 2 存在之前）、Codex **等效保證替代**裁定（僅限本 change、明文非先例）。
- **執行報告落地並進版控**：`docs/superpowers/retrospectives/2026-09-03-loosen-plan-execution.md`（242 行）。它是 SDD ledger 的可讀化萃取 —— ledger 隨 branch 收尾刪除，這份留下。含十一個「形式完整、實質空洞」產物全表、apply step 1/6 首次執行的環境證據、Anchor #4 事實基礎（只記錄不裁定）、以及**可信度分佈表**（哪些可從 repo 獨立查證、哪些只有 ledger 佐證）。
- **doc gate 走完並記錄 PASS**：round 1（1 🔴）→ round 2（3 🔴）→ round 3（0 🔴，`✅ Mergeable`）→ targeted review of the 10 yellow fixes（1 🔴，已修）。四份報告皆過 `validate-family-sentinel.js`。Codex 不可用，走 `[REVIEWER_FALLBACK] plane=doc_review from=codex to=contract-neutral-reviewer reason=quota | 2026-09-03T07:19:05Z`（sticky 本 change）。
- **修掉 check 12 在 27 tasks 下會 BLOCK 的缺陷**：群 11 補開 tasks 到 27 時沒補 plan 條目 → 27 task numbers vs 25 entry keys。補上 `## 11.1` / `## 11.2`，重跑並**雙向舉證**：現樹 PASS；`git show HEAD:` 的修正前 fixture BLOCK 且點名 `['11.1','11.2']`，正向對照在該 fixture 上正確翻成 False。
- **四個 checkpoint commit**：`31d012c`（v1 殘留 + fail-open PRECHECK 修正）、`84df208`（verify + retrospective）、`79e6c21`（doc gate 修正 + 群 11 plan 條目）、`8e73373`（執行報告）。每個 commit 前跑 `verify-last` 確認無 AI attribution trailer，`文檔/handoff/` 全程排除在 branch 外。

### 三、未完事項 / 接力棒

- **`task-20260903-loosen-plan-close`（工作地圖新建，狀態 `NEXT`）** —— loosen-plan 收尾四件事：
  1. `openspec archive` —— **Windows 目錄鎖 3/3 穩定複現**，`cp -r` 進 `archive/` → `diff -r` 驗 IDENTICAL → **`rm -rf` 委派使用者跑**（agent 的 `rm` 會被 deny）。別先試 `mv` 撞牆。
  2. 刪 `.superpowers/` SDD 工作區（報告已搬進版控，安全）。
  3. `superpowers:finishing-a-development-branch` → push + PR（**apply step 6，本 repo 史上首次**）。
  4. push 後補驗 **task 9.1 的 live Actions run** —— `verify.md` §10 記為 owed verification、不是略過。
- **待使用者裁定**：`verify.md` carried-forward #6 —— schema 沒有任何一層擁有「檢查新鮮度」。要不要在 v2.x 處理，以及能否在不動用 claim boundary 明文否認的 Harness 層機制下表述。
- **`驗收節點.md` 的 2026-09-10 條目已被勾為 `[x]`**，但其驗收條件是「累積 5 次【學習候選】產出」，今天的報告產出 3 條。是否提前勾掉，交使用者判斷（本 session 未動它）。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **修正本身有可測量的出錯率，而這次量到了。** doc gate 三輪：修 3 個 🔴 → 製造 2 個新 🟡；修 10 個 🟡 → 製造 1 個新 🔴。三次都是同一形狀：**改了 A、忘了十幾行外的 B**（最後那個 🔴 是把 §0 的 commit 範圍釘死成四個 commit、卻留下十二行外的 commit chain 區塊仍寫「兩個落地、一個 pending」）。**attribute:** `rules/auto-loop.md` 的 Anchor「Fixing ≠ Verifying」。**propose action:** 這不是告誡而是數據 —— 它是那條 Anchor 為什麼不可降級的實證，也是「修完不重審」這條捷徑走不得的理由。已寫進 retrospective §2 的 📌 一條。
- [#反] **一個誠實通過的檢查，不會因為被檢查的對象改變而自己失效 —— 也不會有人通知你。** check 12 在 25 tasks 時真的通過了；群 11 把 tasks 加到 27、沒補 plan 條目，於是**有一個 commit 的期間這個 change 違反自己新增的檢查**。所有閘門（checks 8–12、群 11 審查、whole-branch review、兩次 checkpoint）**都在 reopen 之前跑完了，沒有一個會再跑**。缺的是**新鮮度**不是正確性。**attribute:** harness 自己用 tree digest 綁定審查結論解決了同一問題（`review-state.js`），schema 沒有。**propose action:** 已列 `verify.md` carried-forward #6 交使用者裁；**它與本 change 修掉的 D3（fail-open PRECHECK）是同一隻病的兩個層級 —— 沒看到失敗訊號，被當成可以放行**。
- [#反] **要一份紀錄接受獨立查證，會連帶查到被紀錄的那件事的缺陷。** 上面那個 check 12 的 🔴 不是報告的問題、是 change 的問題 —— 它在 verify、在 whole-branch review、在兩次 checkpoint 都沒被抓到，卻在 reviewer「查證報告裡引的一個 task 數字」時撞出來。**propose action:** 審查紀錄的成本買到的不只是紀錄的正確性；把收尾紀錄送外部審，值得當常規而非額外。

**【當日洞見】**

- **正向對照解決不了新鮮度。** 「讀完全部沒找到」與「什麼都沒讀所以沒找到」輸出逐位元組相同 —— 這靠正向對照分得開。但「當時算對、之後對象變了」分不開，那需要「輸入變了就作廢先前結論」的綁定。今天把這個 pattern 的邊界推廣了一格（報告學習候選 #1 已納入）。
- **便宜的機械對帳，價值不在它多常抓到東西，在它不需要你當時夠警覺。** 今天四次：staged 檔案集合雙向差集、check 12 集合比對、class-(b) 39 條/8 面逐檔重算、ledger `defect #N` 編號逐一列舉。**其中兩次推翻了我自己「看起來合理」的數字**（bundle「零個 v1」實為規範面 0 / README 各 15 行；ledger「9 條編號」實為 6 條）。
- **查不到來源時，標記比猜一個接近的數字誠實。** 派工次數兩處打架、ledger 用散文記所以數不出來 → 寫「**不是證據支持的**」而非挑一個順眼的填。這是使用者今天定的線（A′ 裁定：「若沒有可靠來源，不要猜另一個數字，改成刪除精確宣稱或明確標記無法可靠重建」）。
- **舊數字會在自己被更正的那句話裡復發。** verify.md 有一段專門記錄「我先前數錯了、已更正」—— 而那句更正本身寫的 902 也是錯的（實際 916，且 916 從 `31d012c` 起就成立、比該檔被寫出來還早）。**一段宣稱已查證自己數字的話，不是它已查證的證據。**

### 五、檔案異動

錨來源：共用 per-cwd 時間戳 N=3h（起點 2026-09-03T14:58:43）——可能非本 session（快照屬另一專案根）

```
8e73373 docs(retro): land the loosen-plan execution record
A	docs/superpowers/retrospectives/2026-09-03-loosen-plan-execution.md

79e6c21 docs(loosen-plan): close the doc gate; plan gains the group-11 entries
M	openspec/changes/loosen-plan/plan.md
M	openspec/changes/loosen-plan/retrospective.md
M	openspec/changes/loosen-plan/verify.md

84df208 docs(loosen-plan): land verify and retrospective, tasks 27/27
A	openspec/changes/loosen-plan/retrospective.md
M	openspec/changes/loosen-plan/tasks.md
A	openspec/changes/loosen-plan/verify.md

31d012c fix(schema): close v1 residue and the fail-open retrospective PRECHECK
M	superpowers-bridge/README.md
M	superpowers-bridge/README.zh-TW.md
M	superpowers-bridge/schema.yaml
M	superpowers-bridge/templates/retrospective.md
M	superpowers-bridge/templates/verify.md
```

本次收工另有 `workflow-harness/work-map.jsonl`（新增 `task-20260903-loosen-plan-close` 並標 `NEXT`）與本 handoff，隨收工 commit 一併入庫。

**無專案資料夾**（`artifact_paths children --key projects_dir` 回空）→ 專案 Changelog 這步 skip。

### 六、下一步建議

1. **`openspec archive`** —— `cp -r` + `diff -r` 驗 IDENTICAL，然後**請使用者跑 `rm -rf openspec/changes/loosen-plan`**（agent 的 `rm` 會被 deny）。CLAUDE.md 已載明別先試 `mv`。
2. **刪 `.superpowers/` SDD 工作區** —— SDD 的 Finish 步驟要求；報告已搬進版控故安全。
3. **`finishing-a-development-branch` → push + PR** —— apply step 6，本 repo 首次真正 dogfood。push 前確認 `文檔/handoff/` 仍在 branch 外（handoff 屬 main）。
4. **push 後補驗 task 9.1 的 live Actions run**，回填 verify.md §10 的 owed verification。
5. **裁定 carried-forward #6**（schema 的檢查新鮮度缺口）—— 這條會決定 v2 是否帶著一個已知的結構性缺口出貨，以及要不要開新 change。
