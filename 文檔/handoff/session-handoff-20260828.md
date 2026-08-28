# Session Handoff — 2026-08-28

## Session 08:07

### 一、本 session 主題

架構討論「這包 bridge 到底保證什麼」（8/27 接力棒指定主題）：使用者分四輪給出 Product Promise → 依賴鏈上修 → 十條護欄 → v0 綁定表，AI 逐項查證後收斂成正式技術方向文件、過審、commit。零 schema 改動（照方向文件護欄，PoC 前不動 schema.yaml）。

### 二、完成事項

- **Bridge Guarantee 定案**：Product Promise 合併版（語意留初版閘門式、語感借改版）＋三條 mechanism-independent 保證（Contract Preservation / Verifiable Completion / Explicit Degradation）。
- **TDD 位置定案**：不進承諾本身，活在 Contract Verification 層（「目前版本對程式變更要求的驗證機制，證據 RED/GREEN」）——硬約束沒削弱、換了住址。
- **依賴鏈上修一層**：真根不是 Evidence Contract、是 Bridge Guarantee；四條卡住工作全部重新掛載。
- **v0 綁定表逐 skill 查證**：全部存在；`/to-tickets` 讀全文（107 行）確認四性質屬實＋撈到三個適配事實（`disable-model-invocation`、模板無 Contracts 欄、自帶第二套清單載體＝SSOT 待定）。
- **探索層定案**：不綁定、不建 router；預設 brainstorming → grilling、explore 為前置；harness 只規定出口條件（進 Task Decomposition 前要有被接受的 spec）。
- **正式文件落地**：`docs/superpowers/specs/2026-08-27-bridge-guarantee-architecture-direction.md`（定位＝技術方向與設計邊界、非 implementation spec；含七項未決顯式清單）。
- **審查**：Codex 額度耗盡 → 照 4.3.1 降級矩陣記 `[REVIEWER_FALLBACK]`、派 `contract-neutral-reviewer` 兩輪：第一輪 ✅ Mergeable（2 sub-threshold 當場修）、第二輪複驗零新缺陷 ✅ Mergeable；`review-state note doc_review pass` 已記。
- **Commit**：`b1abd82`（使用者親口核可；照 repo 慣例英文 conventional commits、無 AI 署名）。
- **登記**：`task-20260828-concept-poc`（概念 PoC，掛下一代改造底下）。

### 三、未完事項 / 接力棒

- [#接力] **下一步＝概念 PoC**（方向文件 §7）：證明最小鏈 `Requirement/Scenario → Task → Verification Method → Verification Result → Gate PASS/BLOCK`。PoC 前不動 schema.yaml、不建新 artifact。PoC 自己作為一個 change 走 brainstorm → spec → 核可。
- [#接力] **七項未決在文件 §6**，其中要使用者拍板的：#1 G1 要不要雙向（不偷加；AI 建議納入）、#2 CLAUDE.md 階段界線重表述（v0 已把 Orca 定為唯一 runtime）。
- [#接力] `fix-tdd-transitive-claim` **仍暫停**；文件 §6#7 明寫其第一題定案（丙）應保住，推翻要明說。
- [#不重議] 探索層不建 router 機制、`verify.md` 不重構、Evidence 不當主系統——均已定案寫進文件。
- [#環境] Codex 額度 8/27 22:30 已恢復；本 session 備援鏈（contract-neutral-reviewer via general-purpose agent）實測可用。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] **「修完外送、不自查」這次照做了**：文件兩處 sub-threshold 修正後，交第二個獨立審查者專門盯「修 A 造 B」，複驗確認零新缺陷——8/27 學習候選（修改動作本身是缺陷產生源）的直接應用。
- [#反] **Codex 額度三天內第二次在審查中途耗盡**。這次 fallback 鏈走通（照 4.3.1 降級矩陣派 `contract-neutral-reviewer`、記 `[REVIEWER_FALLBACK]`、驗 sentinel），沒把審查掛起來等。attribute: 全域 CLAUDE.md 複審紀律「複審開跑前先定 fallback 鏈」。propose action: 無需新規——本次即為該條的正常執行，記錄以供下次直接照走。

**【當日洞見】**

- [#洞見] **表面瓶頸與真瓶頸差一層**：AI 診斷「四條卡在證據契約」，使用者上修「證據契約自己卡在 Bridge Guarantee」。錯誤的形狀是把中間層當根——中間層看起來像根，因為所有下游確實都指向它。
- [#洞見] **探索層綁單一 skill 是對自家原則的自違反**——「規定證據不規定步驟」的 repo，自己的綁定表把保證範圍上游的探索層釘死成一個 skill，與 plan 放寬要刪的句子同型。
- [#洞見] **`/to-tickets` 三個適配事實全部只有讀全文才撈得到**——「讀了名字沒讀實際說什麼」的正面對照組：這次先讀完才進綁定表。
- [#決策] **v0 把 Orca 定為唯一 runtime＝階段界線正式跨過**；CLAUDE.md 兩階段表在方向落地時要重表述（文件 §6#2）。

**【學習候選】**

> Gate 第 3 次手動試跑（累計 3 / 目標 5，見 `驗收節點.md` 2026-09-10 節點）。同樣標註：我知道閘門在驗什麼，成績受污染。

- **Case**：AI 診斷四條工作的共同卡點是 Evidence Contract；使用者把診斷再上修一層到 Bridge Guarantee，四條工作隨即自然重新掛載。
- **Candidate Pattern**：多條工作卡在同一個中間層時，SHALL 先問「這個中間層自己是從哪裡推導出來的」——共同卡點常常還有上游。邊界：卡點若是外部依賴（額度、他人）不適用。
- **Evidence**：1 次，標 **Hypothesis**。
- **Minimum Sufficient Intervention**：不新增規則——「動工前三問」已含背景層提問；缺的是把「發現共同卡點」當成再上溯一層的觸發訊號。無 enforcement 掛點 ⇒ 依規則停在 Observe。
- **Promotion**：History only（傾向），由使用者決定。

### 五、檔案異動

| 異動 | 內容 |
|---|---|
| `b1abd82` | `docs/superpowers/specs/2026-08-27-bridge-guarantee-architecture-direction.md` 新增（246 行） |
| 未進版控 | `2026-08-27-brainstorm-產品承諾.md`（討論工作紀錄，repo 根，照 8/25、8/26 慣例不 commit） |
| （本次收工） | `workflow-harness/work-map.jsonl`（+1 筆 `task-20260828-concept-poc`）、本 handoff |

錨來源：本 session 開工 commit（fb9be44、開工於 2026-08-27T18:10:06）——列 fb9be44..HEAD

### 六、下一步建議

1. **拍板未決 #1（G1 要不要雙向）**——一句話能定，定了 PoC 的 verify 對照就知道要不要看反方向。
2. **概念 PoC 立 change**：走 brainstorm → spec → 核可（照探索層定案，brainstorming 起手、要打就 grilling）。
3. **CLAUDE.md 階段界線與兩階段表重表述**——可與 PoC change 一起或先行小 change。
4. **`fix-tdd-transitive-claim` 依新方向決定**：恢復（照丙案只刪假宣稱）或併入 PoC 後續。


## Session 12:03

### 一、本 session 主題

G1 雙向拍板落文件（方向文件未決 #1 收案）＋概念 PoC 從 brainstorming 到 spec 定稿＋Step 0 Tool Capability Preflight 實測完成。

### 二、完成事項

- **G1 雙向定案落文件並 commit（`6eb855c`）**：G1 拆 G1a No Silent Loss（blocking）/ G1b No Silent Expansion（detect + require disposition）、邊界＝禁止 silent contract deviation 非逐字比對；連動 §1.1 Product Promise 升級（「未經確認地擴張功能範圍」，使用者定措辭）、§1.4、§4.3、§4.4、§6#1 收為已拍板。審查兩輪（Codex → 額度中斷 → fallback 複驗）全 ✅。
- **概念 PoC spec 定稿**：`docs/superpowers/specs/2026-08-28-concept-poc-traceability-gate-design.md`（十節）。brainstorming 逐題與使用者拍板：hypothesis（結構化 Verification Record、不宣稱消除自我宣稱）、兩條線（Req→Task coverage / Req→Result）、Structural Traceability vs Semantic Correctness 對照、兩階段分開判讀（Core / Integration）、六案例必做（REQ-E evidence 空、REQ-F CONFLICT 由審查者用 REQ-D 論證抓出補入）、三欄 provisional Result（contract+status+evidence）、Step 0 preflight 章、粒度邊界（Requirement-level）、「不新增正式 artifact type」精準措辭。審查六輪（fallback carrier）全 ✅ Mergeable。
- **Step 0 Preflight 實測完成**：`docs/superpowers/poc/2026-08-28-traceability-gate/step0-capability-inventory.md`。三個關鍵發現：①手造 change 只要 `proposal.md` 就能被 `openspec show --json` 讀出 Requirement/Scenario（審查者的 latent tension 實測不成立）②change 層 JSON 不含 Requirement 標題名（Contracts key 實作時定）③最小新增面積＝Task reference + Result interface + Gate。與 spec 假設無矛盾。
- **登記結算**：`task-20260828-concept-poc` 標 DOING。

### 三、未完事項 / 接力棒

- [#接力] **PoC spec＋Step 0 inventory 兩檔未 commit**（使用者喊收工在先）：擬 message `docs(superpowers): add concept PoC spec and step-0 capability inventory`，下 session 開工先收。
- [#接力] **Phase 1 動工**：手造六案例 fixture＋Python 標準庫 validator（落點 `docs/superpowers/poc/2026-08-28-traceability-gate/`）。Step 0 已確認 fixture 可直接吃 CLI JSON（需 `proposal.md`）；Contracts key 三選一（位置序號/text/自抽標題行）實作時定。
- [#接力] Phase 1 Core PASS 後才進 Phase 2（specimen＝CLAUDE.md 階段界線重表述、屆時開真 opsx change、routing exception 已明記於 spec §6）。
- [#環境] Codex 額度本 session 兩度探測失敗（回報 13:01 恢復）；fallback agent（general-purpose）連跑六輪審查、同 thread 複用可行。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] **Codex 額度中斷第三次，fallback 鏈已成慣例動作**：兩次探測失敗都直接記 `[REVIEWER_FALLBACK]`、派 general-purpose 代審、驗 sentinel，零停等；同一 fallback agent 連跑六輪（含三次「修 A 造 B」複驗）、同 thread 複用省 context。
- [#正] **「修完外送、不自查」連續第二個 session 照做**：每輪 sub-threshold 修正都交回審查者盯新缺陷，六輪全 ✅。

**【當日洞見】**

- [#洞見] **審查者的「可能不行」用五分鐘實驗定案，別讓它掛成未決**：審查者兩度標記「CLI JSON 可能只認 CLI 建的 change」為 latent tension；Step 0 在 scratchpad 手造 change 實測，發現只要 `proposal.md` 在場就能讀——猜想不成立。「能碰就碰」的正例：實驗成本遠低於讓疑慮掛在文件裡的成本。
- [#洞見] **自己定的論證會被審查者拿回來打自己**：REQ-D「每條判斷路徑都要有案例打到」的論證，被審查者原樣用來抓出 evidence 空、CONFLICT 兩條沒被案例覆蓋的 Gate 路徑（REQ-E/F 因此補進 spec）——論證寫得好的副作用是它變成可執行的檢查器。
- [#決策] G1 採雙向（G1a/G1b、silent contract deviation 為界、G1a blocking / G1b detect+disposition）；PoC 兩階段分開判讀、六案例必做、Contracts 標註與 Result 載體全 provisional；Requirement-level 粒度、Scenario-level 明列未證明。

**【學習候選】**

> Gate 第 4 次手動試跑（累計 4 / 目標 5，見 `驗收節點.md` 2026-09-10 節點）。本次產出：**沒有**（兩條當日洞見各 1 例、無 enforcement 掛點，照規則停在 Observe、不硬升規則）。

### 五、檔案異動

| 異動 | 內容 |
|---|---|
| `6eb855c` | `docs/superpowers/specs/2026-08-27-bridge-guarantee-architecture-direction.md` G1 雙向定案（+17/−7） |
| 未 commit | `docs/superpowers/specs/2026-08-28-concept-poc-traceability-gate-design.md`（新）、`docs/superpowers/poc/2026-08-28-traceability-gate/step0-capability-inventory.md`（新）、`workflow-harness/work-map.jsonl`（concept-poc → DOING）、本 handoff |
| 未進版控 | `2026-08-27-brainstorm-產品承諾.md`（沿慣例不 commit） |

錨來源：本 session 開工 commit（e811b5c、開工於 2026-08-28T08:11:45）——列 e811b5c..HEAD

### 六、下一步建議

1. **先收 commit**：PoC spec＋Step 0 inventory（＋本 handoff、work-map），一次 commit。
2. **Phase 1 動工**：六案例 fixture＋validator，Core PASS ⇔ 六案例判定全對；失敗停在 Phase 1 回頭改設計。
3. Phase 1 過後進 Phase 2 smoke（CLAUDE.md 階段界線重表述 specimen——它同時是方向文件 §6 未決 #2 的實作）。


## Session 17:39

### 一、本 session 主題

概念 PoC 全程執行收案（Phase 1 fixture＋validator → Phase 2 真 artifact smoke → 結論 concept supported）＋CLAUDE.md 階段界線重表述落地（方向文件 §6 未決 #2 收案，使用者拍板甲案）。

### 二、完成事項

- **Phase 1 Core Mechanism: PASS（6/6）**：六案例 fixture（真 OpenSpec 形狀）＋標準庫 gate_check.py；expected 表先於 Gate 邏輯落檔；首跑全綠後以 10 個變異測試證明非假綠（每條 BLOCK 路徑破壞後如預期轉紅）。
- **審查抓到兩個真缺陷並補死**：P1 孤兒／同層 `- Contracts:` 標註可偽造 coverage（兩輪才修對——改為縮排嚴格深於 checkbox 的機械判定）；P2 results 欄位無型別驗證（`evidence: null` 會 crash）。code review 3 輪 ✅、precommit fallback（schema validate＋smoke）✅、doc review 4 輪 ✅。
- **Phase 2 Integration: PASS**：`openspec new change claude-md-phase-boundary --schema superpowers-bridge` 建真 change、CLI validate 通過；happy path 四步全成立（CLI JSON 讀 Requirement → tasks.md Contracts 標註建 reference → Inspection 型 Result 掛回 → Gate PASS）。
- **真工作交付**：CLAUDE.md「分兩階段」改為事件閘門（使用者定版：「方向可以先決定 ≠ 現在就可以實作」；兩個 YES/NO——PoC 通過？正式設計核可？）；殘留「階段一」指涉一併清除；方向文件 §6#2 比照 #1 標記已拍板。
- **PoC 總報告落檔**：`docs/superpowers/poc/2026-08-28-traceability-gate/poc-report.md`——結論 concept supported；最小載體＝Contracts 標註＋三欄 result 檔＋小型標準庫 Gate；三條架構訊號供正式設計。
- **驗收節點收案**：學習候選閘門 5 次樣本到齊、依節點判準 ✅ 達標、規矩保留（詳見 result 欄；5 次全為開卷、成績受污染已註記）。
- **Commit 六筆**：`b822599`（Phase 1）、`7a426fa`（smart-commit 腳本補裝進 .claude/scripts/）、`f213e5d`（CLAUDE.md＋specimen change）、`b7441e7`（PoC 報告）、`0a0a8f8`（§6#2 標記）＋本次收工 commit。
- **登記結算**：`task-20260828-concept-poc` 標 DONE（證據：poc-report.md 記載雙 PASS 實跑輸出）。

### 三、未完事項 / 接力棒

- [#接力] **方向文件 §6 剩餘未決 #3～#7 要先拍板再往下做**（使用者本 session 明示優先）：#3 降級模式表（對應既有 record「apply 階段改規定交件證據」）、#4 「不保證」清單窮舉、#5 `/to-tickets` SSOT、#6 Gate 綁哪個 state transition（護欄 9：先調查 OpenSpec lifecycle）、#7 `fix-tdd-transitive-claim` 銜接（對應 record「修正 TDD 保證的錯誤宣稱」，仍 DOING）。多數已有對應 record 在追、不需新開。
- [#接力] specimen change `claude-md-phase-boundary` 尚未 archive（未登記為 record、使用者裁示不開 leftover）；要走時記得 Windows 目錄鎖三步 SOP（cp → diff 驗 IDENTICAL → 委派使用者 rm）。
- [#不重議] PoC 收案結論與宣稱邊界都在 poc-report.md——不宣稱消除自我宣稱、不宣稱語意正確性、Scenario-level 未證明；正式資料模型（stable ID / freshness）是後續設計題、不因 PoC「夠用」而預先否決。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] **第一次全綠先破壞再相信**：Phase 1 六案例首跑即 6/6，未直接宣稱 PASS——先做 5 個變異驗證每條 BLOCK 路徑會轉紅才收；其後兩輪 review 的修復各配上打到該漏洞的新變異（最終 10 個、全如預期）。
- [#正] **「修完外送、不自查」連續第三個 session 照做**：code 3 輪＋doc 4 輪，每輪修正交回審查者複驗零新缺陷才收；Codex 額度今日全程正常、未動用 fallback 鏈。

**【當日洞見】**

- [#洞見] **連約 180 行的 Gate 都有兩個「結構檢查被繞過」的洞**（孤兒與同層 Contracts 標註都能偽造 coverage），靠兩輪獨立審查才補死。給正式設計的訊號：附屬語法要一開始就定義成機械可判（已寫進 poc-report 架構訊號節）。
- [#洞見] **單一資料來源不夠、交叉核對才攔得住**：標題抽取數 vs CLI JSON requirement 數的比對，實際攔下 CLI 對破損標題行的寬鬆解析（變異 M5）。
- [#決策] **PoC 收案：concept supported**（Core＋Integration 雙 PASS）。
- [#決策] **CLAUDE.md 動工門檻改事件閘門**（使用者定版：方向可以先決定 ≠ 現在就可以實作）；§6 未決 #2 收案、剩 #3～#7 五項且使用者明示要先拍板。
- [#決策] **學習候選閘門驗收達標、規矩保留**（沒有×2、候選 11、改既有 4:新增 0、Hypothesis 7；5 次全開卷、污染已註記）。

**【學習候選】**

> Gate 第 5 次手動試跑（累計 5 / 目標 5——樣本到齊，本 session 已依節點判準收驗收）。本次產出：**沒有**——「事件門檻取代時間階段」是既有原則（ship 判準是事件不是時間軸）的應用、非新 pattern，照規則不硬升。

### 五、檔案異動

| 異動 | 內容 |
|---|---|
| `b822599` | Phase 1：fixture 五檔＋`gate_check.py`＋`expected-phase1.json`＋`phase1-core-results.md`（+368） |
| `7a426fa` | `.claude/scripts/` 補裝 smart-commit 三支腳本 |
| `f213e5d` | `CLAUDE.md` 事件閘門重表述＋`openspec/changes/claude-md-phase-boundary/`（五檔） |
| `b7441e7` | `poc-report.md`（+51） |
| `0a0a8f8` | 方向文件 §6#2 標記已拍板 |
| 本次收工 | `驗收節點.md`（打勾＋result）、`workflow-harness/work-map.jsonl`（concept-poc → DONE）、本 handoff |

錨來源：本 session 開工 commit（7f80084、開工於 2026-08-28T12:05:42）——列 7f80084..HEAD

### 六、下一步建議

1. **拍板方向文件 §6 剩餘未決（#3～#7）**——使用者明示要先決再做。建議起手 #6（Gate 綁哪個 state transition：護欄 9 要求先調查 OpenSpec lifecycle 三態，是 PoC 之後最自然的下一塊）或 #7（恢復 `fix-tdd-transitive-claim`，record 仍 DOING、就是現算下一步）。
2. #3 降級模式表可與既有 record「apply 階段改規定交件證據」併行處理（同一題的兩面）。
3. specimen change 的 archive 等正式設計動工前順手收（三步 SOP）。


## Session 18:13

### 一、本 session 主題

方向文件 §6 未決 #3~#7 全數拍板落檔（OpenSpec lifecycle 前置調查 → 五題決策包 → 使用者裁決 → 寫進方向文件與 CLAUDE.md → doc review gate 過）。

### 二、完成事項

- **#6 前置調查（讀 CLI 1.3.1 原始碼）**：OpenSpec 無 Change Complete 狀態——`all_done` 是 checkbox 全勾的導出值（提示文字 CLI 寫死、schema 蓋不掉）；archive 是收檔非驗收（incomplete tasks 僅警告可繞、無 post_apply hook）；archive 進度檢查寫死讀 `tasks.md`（`utils/task-progress.js`，不理會 `apply.tracks`）。
- **五題全數拍板**（使用者裁決）：#6 甲——Gate 自身定義 Change Complete（tasks 全勾 → Gate PASS＝Complete → 才可 archive；archive 前置檢查為第二道保險）；#5 甲——`tasks.md` 是 SSOT、ticket 檔是 Worker 工作包；#3 甲——降級表與「apply 改規定交件證據」在正式設計同章收斂、不回寫歷史語意；#4 照排程（非新決策）；#7 甲但**corrective-fix exception**——恢復 `fix-tdd-transitive-claim`，只准刪／修已證偽宣稱，schema 動工總門檻（PoC AND 正式設計核可）不變。
- **G3 定版濃縮寫進 §1.2**：Orca 是 capability provider 非 hard dependency；每項 guarantee 分 required / degradable（required 缺失 → BLOCK）；required 宣告位置歸 Completion Contract。
- **CLAUDE.md 事件閘門收緊**：兩事件全 YES 才動 schema（明記否決逐列解讀）＋corrective-fix 窄例外＋PoC 已過（YES, 2026-08-28）。
- **doc review gate 過**：Codex 額度用盡 → fallback 鏈（`[REVIEWER_FALLBACK]` → general-purpose 代審 → sentinel 機械驗證）；首輪 ✅ Mergeable 零 🔴；🟡＋⚪ 各一當場修、交回複驗零新缺陷；`doc_review pass` 已記。一條 ⚪（PoC 報告連結化）照規則 deferred。

### 三、未完事項 / 接力棒

- [#接力] **本批改動 commit**（本 session 收工 commit 收）。
- [#接力] **下個 session：恢復 `fix-tdd-transitive-claim`**（corrective-fix exception 身分、record `task-20260826-fix-false-tdd-claim` 仍 DOING）：change 目錄現只有 brainstorm.md，走 opsx continue 生 proposal / spec / tasks 再動手；變更面清單已凍結（brainstorm §四、全 repo 約 10 處）；老實話措辭已在 brainstorm §三 Q3 打磨好。動 schema.yaml 要同步 `openspec/schemas/` 副本。
- [#接力] 正式設計（§6#3~#6 定案為輸入）在修錯之後；specimen change `claude-md-phase-boundary` 的 archive 等正式設計動工前順手收（Windows 目錄鎖三步 SOP）。
- [#環境] Codex 額度 18:00 前用盡（回報 19:10 恢復）；fallback agent（general-purpose）跑首審＋複驗共兩輪、同 agent 複用可行。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] **Codex 額度中斷第 4 次，fallback 鏈零停等**：探測失敗即記 `[REVIEWER_FALLBACK]`、派 general-purpose 代審、sentinel 機械驗證通過才收；「修完外送、不自查」連續第四個 session 照做（🟡＋⚪ 當場修後交回複驗、零新缺陷）。
- [#正] **端選擇不端結論有生效**：五題決策包走完整格式（已查證事實＋選項優劣＋建議＋我沒查的），#7 被使用者當場糾正——決策點被看見，把關才發生。

**【當日洞見】**

- [#洞見] **為了想修的事重新解釋門禁＝偷拆大門**：agent 提「PoC 過了就能動 schema.yaml」的逐列解讀被使用者否決；正解是總門檻不動、另開範圍封閉的修錯例外。規則的例外要顯式新增，不能靠重新詮釋既有條文生出來。
- [#洞見] **OpenSpec 三態實查**：archive 寫死讀 tasks.md、all_done 提示文字 CLI 寫死、無 post_apply hook——「Task 全勾 ≠ Change Complete」從實作層被證實，反向支持 Completion Gate 方向。
- [#決策] **§6 五題全收**：#6 Gate 自定義 Complete、#5 tasks.md SSOT、#3 併正式設計且不回寫歷史語意、#4 照排程、#7 corrective-fix exception。

**【學習候選】**

- **Case**：agent 把閘門表讀成逐列對應、提議 schema.yaml 已解鎖；使用者否決，改開 corrective-fix 窄例外。
- **Candidate Pattern**：被 gate 擋住又確有正當需求時，正確動作是「提案新增範圍封閉的顯式例外」，不是「重新解釋 gate 條文讓需求剛好通過」。邊界：適用於自己不是 gate owner 的情形。
- **Evidence**：1 例（2026-08-28）。**Hypothesis**。
- **Minimum Sufficient Intervention**：已改既有環境——CLAUDE.md 閘門段把「否決逐列解讀」與例外條文寫死，下次 agent 讀到的就是收緊版。不新增規則（無需另找掛點）。
- **Promotion**：History only（環境已修，等 sibling case）。

### 五、檔案異動

| 異動 | 內容 |
|---|---|
| 未 commit（本次收工 commit 收） | `CLAUDE.md`（事件閘門收緊＋修錯例外）、`docs/superpowers/specs/2026-08-27-bridge-guarantee-architecture-direction.md`（§1.2 G3 濃縮、§6 rows 3-7 收案、§7 更新）、本 handoff |
| 未進版控 | `2026-08-27-brainstorm-產品承諾.md`（沿慣例不 commit） |

錨來源：本 session 開工 commit（4848914、開工於 2026-08-28T17:43:24）——列 4848914..HEAD

### 六、下一步建議

1. **恢復 `fix-tdd-transitive-claim`**（corrective-fix exception）：opsx continue 生 proposal / spec / tasks → 刪假宣稱＋補老實話（約 10 處、清單已凍結）→ 完整審查鏈。
2. 修錯收案後進**正式設計**（§6 定案為輸入：Gate 定義 Complete、tasks.md SSOT、G3 required/degradable 分級表、「不保證」窮舉 checklist）。
3. Codex 19:10 後恢復，下個 session 主審應可回 Codex（fallback 是 per-change sticky，新 change 重新探測）。
