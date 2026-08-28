# superpowers-bridge 下一代：技術方向與設計邊界（v0）

> 2026-08-27 架構討論定案。**這是技術方向與設計邊界文件，不是 implementation spec**——方向看起來完整不等於一次全做。任何依本文件動工的 change，仍走各自的 brainstorm → spec → 核可流程。
>
> 討論原始紀錄：repo 根 `2026-08-27-brainstorm-產品承諾.md`（未進版控）。前情：`fix-tdd-transitive-claim` change 暫停、四條工作共同卡點的上溯，見 `文檔/handoff/session-handoff-20260827.md` Session 18:06。

---

## 1. Bridge Guarantee：這包 bridge 到底保證什麼

所有下游設計（Completion Contract、Verification、Evidence、Gate）都從這裡推導，**不是反過來**。

### 1.1 Product Promise（核心句）

> 讓 AI Agent 從已確認的規格一路完成實作與驗收，確保重要需求不會在過程中被遺漏或悄悄弱化，也不會在未經確認的情況下擴張功能範圍；未完成必要驗證的工作，不得被宣稱為完成。

（「擴張功能範圍」一詞是刻意選的：對應 G1b 禁止的「未經確認的契約擴張」，而非禁止任何額外的 code change——正常重構、命名、抽 helper 不在此列；2026-08-28 與雙向 G1 同步升級。）

這個 bridge 不保證「你用了哪些 Skills」；它保證的是：**規格承諾不會在 Agent workflow 裡被悄悄弄丟、也不會未經確認地擴張，而且沒有足夠驗證就不能被當成真正完成。**

措辭紀律（討論中確立、寫進承諾時不可丟）：

- 「**弱化**」必須明寫——假保證的實際形態多半不是需求消失，而是宣稱被悄悄改強或改弱；
- 完成條件用**閘門式**（「未完成必要驗證不得宣稱完成」），不用性質式（「有足夠的驗證依據」）——後者量不出違反。

### 1.2 三條核心保證（mechanism-independent）

| # | 保證 | 內容 |
|---|---|---|
| G1 | **Contract Preservation**（雙向，2026-08-28 拍板） | 已接受的契約在 decomposition、implementation、verification、completion 過程中，不得被靜默遺漏、弱化，也不得被靜默擴張。拆兩個子條款：<br>**G1a — No Silent Loss**：已接受的 Requirement / Scenario 不得被遺漏或弱化。<br>**G1b — No Silent Expansion**：不得未經接受就新增 contract-level behavior。 |
| G2 | **Verifiable Completion** | 任何 Complete 宣稱都必須能追溯到其承接的 contract，且必要 verification 已實際執行並取得可接受結果 |
| G3 | **Explicit Degradation** | 能力不足時可以降級執行機制，但不得把降低後的 assurance 偽裝成完整保證；缺失的 guarantee 必須顯式化 |

**G1b 的邊界（定案時一併劃定，落條文時不可丟）**：禁止的是 **silent contract deviation**，不是「任何 Spec 沒逐字寫到的 code change」。內部重構、命名、抽共用函式、補型別、改善內部 error handling 不屬於 contract expansion——使用者得到的系統能力沒有增加；**新增或改變可觀察行為、介面、資料語意或重要副作用**才是。兩個子條款共享同一原則：**實作可以自由選路徑，但不能自行改變契約邊界**（即 "Model owns path; harness owns boundaries" 在契約層的直接應用）。

**G1 的 Gate 語意（兩邊不對稱，刻意的）**：

- **G1a 直接 blocking**——Requirement 沒人承接、Scenario 沒驗、Requirement 被弱化，顯然不能宣稱完成。
- **G1b 第一版做 detect + require disposition**：偵測到疑似新增契約行為 D 時，不要求機器自行判斷語意（「這個 helper 算不算 scope creep」機器判不可靠），而是要求明確處置——證明它只是 implementation detail、或回 Spec 把 D 正式加入 Change 並取得接受、或移除 D。**未處置前 Gate BLOCK**。Harness 不需要理解業務語意，它只需確保：被判定為 contract-level expansion 的東西，不能無聲留下。

保證用途對照：G1 對應 `/to-tickets` 適配與 plan 放寬；G2 對應 Completion Contract / Acceptance Gate；G3 對應降級邊界那條工作，並直接回答「沒有 subagent 是不是禁止執行」——答案是：可以降級執行，但缺失的保證要明講。

**G3 定版濃縮（2026-08-28 拍板，配套 §6#3）**：

> 沒有 Orca 時，工作流可以退回較簡單的執行模式；失去哪些 Orca 能力就明確標示哪些保證不可用。若失去的是該 Change 的必要保證，則不得降級，必須 BLOCK。

三個支撐點（使用者 2026-08-28 定調）：

- **Orca 是 execution capability provider，不是 hard dependency**——完整模式＝Core Harness Guarantee＋Orca Capability；降級模式＝Core Harness Guarantee。traceability、驗證、Gate 不因無 Orca 消失；消失的是 Orca 附加能力（多 Worker 並行、隔離、dispatch、implementer/reviewer 分離）。分層上 Orca 位於 Contract/Governance 與 Verification/Completion 之間——中層可缺，上下兩層不隨之消失。
- **每項 guarantee 分 required / degradable**：degradable 缺失 → 降級＋顯式標示（例：`Review: PASS` / `Independent Review: unavailable` / `Reason: Orca runtime unavailable`）；required 缺失 → BLOCK，不得降級。
- **「哪些 guarantee 對哪類 Change 是 required」需要一個宣告位置**——由 Completion Contract 在正式設計定義該欄位，不留成默契。

**TDD 的位置（定案）**：TDD 不寫進保證本身——它是實現手段，活在 Contract Verification 層，身分是「目前版本對程式變更要求的驗證機制，證據為 RED/GREEN 輸出」。「TDD 不可丟」這條硬約束沒有被削弱，只是換了住址：想丟 TDD 必須顯式修改驗證契約，而那是看得見的改動。

### 1.3 依賴鏈

```
Bridge Guarantee        「這套 bridge 對使用者保證什麼？」
        ↓
Completion Contract     「什麼條件才有資格宣稱完成？」
        ↓
Contract Verification   「哪些承諾要怎麼被實際驗證？」
        ↓
Verification Result / Evidence  「用什麼結果與證據支撐 PASS？」
        ↓
Acceptance Gate         「機械判斷是否可以 Complete」
```

### 1.4 五個定界問題（防過度工程的第一道）

設計任何一層之前，先有這五題的答案就夠；不要先設計 20 種 evidence type、10 個 state：

1. 哪些事情是 bridge **必須保證**的？→ G1–G3（G1 已定案為雙向：G1a No Silent Loss + G1b No Silent Expansion，見 §1.2）
2. 哪些只是**目前版本選擇的實現機制**（可替換）？→ SDD artifact DAG、TDD（RED/GREEN）、subagent 獨立審查、PRECHECK、verify 逐需求對照、Evidence Matrix 三軸
3. 哪些事情 bridge **明確不保證**？→ 規格本身的品質與正確性（「已接受的規格」是輸入前提）；prompt 文字層的正確性（CI 驗不到）；agent 產出品質上限（bridge 保證流程性質，不保證聰明程度）。⚠️ 此清單落成正式條文時需再窮舉一輪。
4. degraded mode 時哪些 guarantee 下降？→ 已確認一例：無獨立審查者時，G2 的「驗證有執行」仍成立但**獨立性喪失**（residual risk 有 2026-08-27 實測數據：語意類缺陷自查命中 0%、外部命中 100%）；其餘情形待降級邊界工作逐一盤。
5. 宣稱 Complete 最少要證明哪些 guarantee 已成立？→ 每條被接受的 Requirement 有對應驗證結果（G2）＋對照表無缺漏（G1a）＋疑似 contract expansion 均已處置（G1b）＋若有降級已顯式記錄（G3）。此即 Evidence Matrix 三軸的一般化。

---

## 2. 十條設計護欄（防膨脹）

1. **先驗證責任邊界，再實作**——OpenSpec、Matt `/to-tickets`、Orca、Superpowers、sd0x 各承擔自己最擅長的責任；不為整合而複製既有能力。
2. **成熟機制優先，最小適配**——`/to-tickets`、sd0x 的 state / freshness / terminal invariant、OpenSpec verify 都先確認能否直接利用；只有真缺口才新增。
3. **不要把 Evidence 當主系統**——Evidence 只是支撐 Verification Result 的材料；核心鏈是 `Requirement/Scenario → Verification → Result → Completion Gate`。
4. **Contract Verification 不得退化成「又跑一次測試」**——它逐項回答「原契約是否被充分驗證」；測試只是 Verification Method 之一。
5. **Acceptance Gate 不得變成 Agent prompt**——Gate 的價值是機械判定 blocking conditions；Agent 產生判斷，Harness 負責判斷結果齊不齊、PASS 與否、還 fresh 嗎。
6. **Task traceability 夠用就好**——只需「每個重要 Contract 找得到承接 Task、每個 Task 完成後找得到 Verification Result」；先不發明龐大 Evidence Matrix schema。
7. **PASS 必須有 freshness**——驗證後 implementation 又變更時，要研究哪些 Verification Result 應失效；「曾經 PASS」不得永遠視為 PASS。
8. **`verify.md` 暫不重構**——它是 Change-level verification report／裁判紀錄；先建好 Contract Verification、Completion Contract、Gate state，再決定怎麼吸收新結果。
9. **Task `[x]`、Change Complete、Archive 是三個不同狀態**——不預設 Gate 綁哪一個；先調查現行 OpenSpec lifecycle，再決定哪個 state transition 需要 hard gate。
10. **先做概念 PoC，不做 Harness v2**——先證明最小鏈 `Requirement/Scenario → Task → Verification Method → Verification Result → Gate PASS/BLOCK` 跑得通，再擴充 review、freshness、parallel execution。

**新增機制的准入問題**（提出大 schema／多 artifact／多 state 前必答）：

> 這個新增機制，是在補「目前沒有辦法證明 Complete」的真缺口，還是只是把既有資訊再記一次？後者原則上先不要做。

**主軸句**：

> 這次設計的目標不是打造更多流程，而是讓「Complete」變成一個可以被證明的狀態。模型仍然擁有解題路徑；Harness 只接管那些不能靠模型自我宣稱的完成邊界。

---

## 3. v0 架構：整體鏈與 Skill 綁定

### 3.1 整體鏈

```
OpenSpec（定義 Change / Capability / Requirement / Scenario / Design）
  ↓ Task Decomposition（把承諾切成可執行 Task）
  ↓ Orca（Coordinator / Worker / serial / parallel runtime）
  ↓ Implementation（TDD / Debug / Review / Fresh Verification）
  ↓ Contract Verification（逐條驗 Requirement / Scenario 是否真的成立）
  ↓ Harness State（記住 PASS / FAIL / OWED，以及 PASS 是否仍有效）
  ↓ Completion Contract（定義怎樣才叫 Complete）
  ↓ Acceptance Gate（機械判斷現在能不能宣稱完成）
  ↓ OpenSpec Verify（Change-level 總體驗證）
  ↓ verify.md（裁判紀錄）
  ↓ Finish / Archive
```

### 3.2 綁定表

| Workflow Node | 初步方案 | 狀態 |
|---|---|---|
| 問題探索 | **探索層自由**；預設 `superpowers:brainstorming` → `grilling`，`openspec-explore` 為前置選項（見 §5） | ✅ 定案 |
| Change / Spec 建立 | OpenSpec propose / artifact workflow | ✅ 直接用 |
| Task Decomposition | Matt Pocock `/to-tickets` | 🟡 做 OpenSpec 適配（見 §4.1） |
| Execution Runtime | Orca `orchestration` | ✅ 本階段唯一正式 runtime；execution strategy 在 Orca 裡決定 |
| Implementation | superpowers `test-driven-development` | ✅ 直接用 |
| Debugging | superpowers `systematic-debugging` | ✅ 直接用 |
| Worker 完成前驗證 | superpowers `verification-before-completion` | ✅ 直接用 |
| Code Review | Superpowers review 紀律 + Orca dispatch | 🟡 改 dispatch |
| Contract Verification | 薄層自建 Skill + 既有驗證 Skills | 🆕 真正需要補（見 §4.2） |
| 測試鏈 | sd0x `/verify` 類機制 | 🟡 可重用 |
| Test coverage review | sd0x `/test-review` / `/check-coverage` | 🟡 可重用 |
| Completion State | sd0x state / freshness 概念 | 🟡 強參考 |
| Acceptance Gate | sd0x Gate pattern + Harness command | 🆕 少量新增（見 §4.4） |
| Change Verify | `openspec-verify-change` | ✅ 保留強化 |
| Verification Report | 現有 `verify.md` | ✅ 保留，之後優化 |
| Finish | superpowers `finishing-a-development-branch` | ✅ |
| Archive | `openspec-archive-change` | ✅ |

表內全部 skill 已於 2026-08-27 逐一確認實際存在（session 可見或磁碟上）。

### 3.3 角色分工（架構哲學濃縮）

> **OpenSpec** 管「承諾什麼」。**Matt `/to-tickets`** 管「怎麼把承諾切成可執行工作」。**Orca** 管「誰來執行、怎麼編排」。**Superpowers / sd0x Skills** 管「怎麼把工程活動做好」。**Contract Verification** 管「承諾真的成立了嗎」。**Harness** 管「必要驗證沒有發生，就不能 Complete」。**OpenSpec Verify + `verify.md`** 管最後的 Change 級裁判與紀錄。

配套定位：

- **Superpowers 降回工程 Skill Library**——不再讓整套 SDD workflow 控制 runtime；Worker 內用 TDD / systematic-debugging / verification-before-completion，review 紀律由 Superpowers 提供、dispatch 由 Orca 負責。
- **Orca 是本階段唯一正式 execution runtime**——Coordinator 不在 runtime 外自由選（SDD？Orca？另一套？），而是在 Orca 裡決定 serial / parallel 等 execution strategy。

---

## 4. 缺口盤點：輕量適配三處＋真正新增四項

**輕量適配**（既有機制加薄補丁）：① `/to-tickets` → OpenSpec Contract-aware（§4.1）② Code Review → Orca dispatch ③ sd0x state → 增加 Contract Verification state。

**真正新增**（目前僅此四項）：① Contract Verification 薄層（§4.2）② `Requirement/Scenario ↔ Task ↔ Verification Result` 最小 traceability ③ Completion Contract（§4.3）④ Acceptance Gate（§4.4，以 sd0x 為基底非重造）。

### 4.1 `/to-tickets` 的 OpenSpec 適配（不自建 Task Decomposition）

`/to-tickets`（mattpocock-skills）作為母體。已讀全文確認它具備：tracer-bullet 垂直切片、每張 ticket 自足可驗（demoable / verifiable on its own）、blocked-by 依賴邊、fresh-context（一張 ticket 一個乾淨 context window，做完清 context 再拿下一張）、內建「切完先給使用者審 granularity 與 blocking edges」的核可閘。

**要補的只有 OpenSpec Contract awareness**：Task 標明承接哪條 Requirement / Scenario——

```
Task
├─ Deliverable
├─ Contracts（Requirement A / Scenario A1 …）
├─ Blocked by
└─ Boundary
```

讀全文另撈到三個影響適配的事實（光看描述看不到）：

1. frontmatter `disable-model-invocation: true`——只能使用者以 slash 觸發；且依賴 `/setup-matt-pocock-skills` 先配好 tracker 與 triage label。適配時要決定這個限制留不留。
2. ticket template（local 與 issue 兩版）**沒有 Contracts 欄位**——適配補丁正是加這欄。
3. 它有自己的清單載體（`.scratch/<slug>/issues/` 或真 tracker），結尾綁 `/implement` 逐張執行——與 OpenSpec `tasks.md` 是兩套清單，**適配時必須決定誰是唯一事實來源**（雙存放＝同步漂移風險，與 schema 安裝副本同步是同型問題）。

### 4.2 Contract Verification 薄層

目前唯一找不到成熟 skill 可完全取代的核心。它是控制層，不重造測試框架：

```
讀 Contract
  ↓ 決定這條要執行哪個 Verification Method
  ↓ 呼叫既有能力執行：
      Test            → sd0x /verify
      Coverage 判斷    → /test-review、/check-coverage
      Review / 檢視    → Reviewer Skill
      Smoke / E2E     → 對應工具
  ↓ 收斂成正式 Verification Result：PASS / FAIL / BLOCKED（必要時附 Evidence）
```

**Evidence 的定位**（縮小）：Evidence ≠ completion mechanism；Evidence ＝ 支撐 Verification Result 的材料。automated test 的 command result 本身就足夠；inspection 需要 reviewer 結論；manual demonstration 需要操作結果；analysis 需要分析輸出。

### 4.3 Completion Contract（Done 的定義）

回答「什麼條件成立，Task / Change 才能叫 Complete」。初步條件集（**欄位不現在定死**，先確立「Complete 是一組條件，不是 Agent 的一句宣稱」）：

- 所有 blocking Contract 都有 Verification
- 所有 blocking Verification = PASS
- 疑似 contract expansion 均已處置（G1b：證明為 implementation detail / 回補 Spec 取得接受 / 移除）
- required Review = PASS
- 必要 Evidence 存在
- verification freshness 有效
- 沒有 unresolved blocker

### 4.4 Acceptance Gate（以 sd0x 為基底，不從零造）

不是寫一個 acceptance-gate skill 叫 Agent「請自行檢查」，而是借 sd0x 的成熟機制：`/precommit` 的 gate pattern、`review-state` 的 durable state、tree digest 的 verification freshness、terminal completion invariant——再加我們自己的 **Requirement / Scenario verification state**。注意：sd0x 這套在它自己家裡是**提醒層**（hook-lightweighting 後刻意 nothing blocks，verdict 在行為層）；「機械擋下」是我們要在它的 state / digest 基礎上**新加**的部分，不是它現成就有的行為：

```
REQ-A/B/C = PASS？ required Review = PASS？ Evidence required → present？
Result still fresh？ blocker = 0？ 疑似 contract expansion 均已處置？（G1b）
  → 全 YES = Complete；否則 BLOCK
```

分工原則：**Contract Verification 可由 Skill / Agent 執行；Acceptance Gate 盡量讓 Harness 機械判斷。**

**sd0x 明確保留的五原則**：① Model owns path ② Harness owns boundaries ③ Durable state（不相信模型記得自己欠什麼）④ Verification freshness（implementation 改了，舊 PASS 不一定還有效）⑤ Terminal completion invariant（Complete 是一組必須成立的終態條件）。

最小 traceability（真正新增第②項）也在這裡落地：`Requirement/Scenario ↔ Task ↔ Verification Result`，夠用就好（護欄 6）。

---

## 5. 探索層定案：預設 brainstorming + grilling

探索層在 bridge 保證的**上游**（三條保證從「已接受的規格」起算），屬「模型與使用者擁有的路徑」——所以**不綁定單一 skill、不建 router 機制**。

三個候選的實際角色（已逐檔讀畢）：

| | 本質 | 方向 | 終點 |
|---|---|---|---|
| `openspec-explore` | 「a stance, not a workflow」：開放思考夥伴、無核可閘、OpenSpec-aware | 發散 | 無 |
| `superpowers:brainstorming` | 流程：分類 → 一次一問 → 方案 → 分段設計 → spec，硬核可閘 | 收斂 | 被核可的 spec |
| `grilling`（mattpocock） | 對抗式訪談：拷問使用者既有計畫，事實自查、決定逐條問 | 壓力測試 | 共識確認 |

**定案**：

- **預設鏈 = brainstorming（收斂成設計）→ grilling（拷問一輪）→ 核可、進 spec**。grilling 段是預設非強制——bounded 級小改動由 brainstorming 的短設計＋核可即可。
- `openspec-explore` 留作「還不確定要不要動工、純想事情」的前置選項。
- **harness 只規定出口條件**：進 Task Decomposition 前必須存在被使用者接受的 spec（有 Requirement / Scenario 可承接）。用哪條路走到那裡，不管——「規定證據，不規定步驟」在探索層的直接應用。

---

## 6. 未決事項（顯式清單，落地前逐一拍板）

| # | 未決 | 說明 |
|---|---|---|
| 1 | ~~G1 要不要雙向~~ **已拍板（2026-08-28）** | 採雙向，拆 G1a / G1b，邊界定義為「禁止 silent contract deviation」而非禁止所有未逐字寫在 Spec 的 implementation change；G1a blocking、G1b detect + require disposition。全文見 §1.2。決策依據之一：2026-08-27 三輪審查中「修 A 順手造 B」實際發生 8 次 |
| 2 | ~~階段界線重表述~~ **已拍板（2026-08-28）** | 採甲案：`CLAUDE.md` 兩階段表改為**事件閘門**（概念 PoC 通過？正式設計核可？兩個 YES/NO），Orca 確定為未來正式 execution runtime、方向以本文件為準；更新的是「禁止動 `schema.yaml` 的理由」，不是提前允許 Orca 實作。已落地：commit `f213e5d`（change `claude-md-phase-boundary`——同時是 traceability-gate PoC 的 Phase 2 specimen，Gate PASS） |
| 3 | ~~降級模式表~~ **已拍板（2026-08-28）** | 與 record「apply 階段改規定交件證據」**在正式設計同一章收斂**（Completion / Evidence＋Degraded Mode＋Independent Review degradation），**不回寫歷史語意**——舊 record 當時沒包含完整 G3 就是沒有，不得事後說成「本來就是同一件事」。G3 定版濃縮與 required / degradable 分級見 §1.2；「審查獨立性」將為表中第一個明名項目（已有 2026-08-27 實測數據：語意類缺陷自查命中 0%、外部命中 100%） |
| 4 | **「不保證」清單窮舉 → 已排程（2026-08-28 確認非新決策）** | §1.4 第 3 題自帶時機（「落成正式條文時再窮舉一輪」），列為正式設計 checklist 項即可，現在不掃 |
| 5 | ~~`/to-tickets` 適配的唯一事實來源~~ **已拍板（2026-08-28）** | **`tasks.md` 是 SSOT**；ticket 檔是 Worker 工作包、非權威紀錄。依據（讀 CLI 1.3.1 實作）：CLI 機械消費 `tasks.md` 兩處——`instructions apply` 的 `all_done` 判定＋archive 的進度警告（後者路徑寫死在 `utils/task-progress.js`、不理會 schema `apply.tracks` 設定）；ticket 檔無任何機械消費者。PoC 已證 Contracts 標註於 `tasks.md` 可跑 Gate。反向（ticket 為權威）＝雙載體必然同步＝「兩份真相」漂移風險 |
| 6 | ~~Gate 綁哪個 state transition~~ **已拍板（2026-08-28）** | **Gate 自身定義 Change Complete**（甲案）。調查結論（讀 CLI 1.3.1 實作）：OpenSpec **沒有** Change Complete 狀態——`all_done` 是「checkbox 全勾」的導出值（其提示文字 CLI 寫死、schema 蓋不掉）、archive 是收檔不是驗收（incomplete tasks 僅警告可繞、無 post_apply hook）。定案順序：tasks 全 `[x]` → 跑 Acceptance Gate → **Gate PASS＝Complete** → 才可 archive；archive 前置檢查「Gate PASS 紀錄存在」為第二道保險、不是 Completion 本體。Task `[x]` 層級的機械攔截留給 Orca runtime（worker 交件時）。分工句：**OpenSpec 管「工作清單做完了沒」；Harness 管「這個 Change 有沒有資格被稱為完成」** |
| 7 | ~~`fix-tdd-transitive-claim` 如何銜接~~ **已拍板（2026-08-28）** | **恢復執行，定性為 corrective-fix exception**：只允許刪除／修正已被證偽的既有宣稱，不得藉此加入 Completion Gate、Contract Verification、Orca 或任何新正式設計。schema 動工總門檻**不變**（PoC 通過 **AND** 正式設計核可，才正式動 schema）——「PoC 過了就能動 schema.yaml」的逐列解讀已被否決；例外條文寫入 `CLAUDE.md` 事件閘門段。原丙案（只刪假宣稱＋收窄理由）與本方向相容、保住 |

---

## 7. 下一步（依護欄 10）

~~先做**概念 PoC**~~ **已完成（2026-08-28）**：最小鏈 `Requirement/Scenario → Task → Verification Method → Verification Result → Gate PASS/BLOCK` 已證明跑得通（Core 6/6＋Integration 雙 PASS，結論 concept supported，見 `docs/superpowers/poc/2026-08-28-traceability-gate/poc-report.md`）。

現在的下一步（2026-08-28 §6 全數拍板後）：

1. **corrective-fix exception 先行**：恢復 `fix-tdd-transitive-claim`（§6#7），只刪／修已證偽宣稱。
2. **正式設計**：§6#3～#6 的定案為輸入（Gate 定義 Complete、tasks.md SSOT、G3 required/degradable 分級表、「不保證」清單窮舉為 checklist 項）；核可後才開始正式 schema 實作。
