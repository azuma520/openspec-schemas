# 正式設計（2026-09-01）章節修訂對照表

> **定位：修訂前的對照表，不是設計文件、不是修訂本身。**正式設計[`2026-09-01-bridge-guarantee-formal-design.md`](./2026-09-01-bridge-guarantee-formal-design.md)本表製作時**未動**。
> 本表只回答「哪一節要改什麼、為什麼、依據在哪」。修訂前需裁的六題已於 2026-09-23 由使用者裁定（§4），本表已依裁定更新。
>
> **流程（使用者 2026-09-23 定）**：本表先過文件審 → 依本表一次修改正式設計 → 正式設計自己再過文件審與新一輪核可。本表審過之前不動正式設計。
>
> **輸入（全部已讀全文）**：
>
> - 2026-09-23 裁定快照：`文檔/handoff/session-handoff-20260923.md` 的「Session 16:40」區塊（下稱**快照**）。所列各條為使用者已拍板、`#不重議`。
> - Spike 報告：[`../poc/2026-09-01-capability-spikes/spike-report.md`](../poc/2026-09-01-capability-spikes/spike-report.md)（S1–S6 拍板）。
> - 9/1 正式設計文件審的 9 筆 deferred findings（fallback 代審，✅ Mergeable、零 🔴）。**原文此前只存在於該 session 的對話紀錄**（`be295c7f…jsonl`，2026-09-01T02:39Z），repo 內只有交接提到其中兩筆的名字；本表 §2 的 F1–F9 為該報告逐條轉錄，自此有 repo 內出處。
> - 研究文件：[`../research/2026-09-23-requirement-traceability-current-state.md`](../research/2026-09-23-requirement-traceability-current-state.md)。
>
> 行號一律指 9/1 版本（commit `f80fc7b`，306 行）。

---

## 1. 修訂治理（已決，照辦）

出處：快照「Formal Design 修訂治理」。

| 規則 | 對本次修訂的意思 |
|---|---|
| 修訂 9/1 本文，不開第二份 normative owner | 本表與研究文件都**不是** normative；修訂直接改 9/1 那份檔案 |
| 章節號不動；作廢節保留標題並註明 | 新增內容以**既有節內段落**或**節尾追加新小節號**（如 §3.5）承載，不重排 |
| 歷史引用回看 9/1 commit | 修訂後在文件頭註明 9/1 原版 commit `f80fc7b` |
| 修訂另行核可，不使事件閘門退回 NO | 文件頭第 7 行的狀態句要補一句（見 §2 表「文件頭」列） |
| ②～④ 全裁完後一次修改、一次文件審查 | 「②～④」是當日討論的題號，快照本身未定義；依當日對話紀錄，指證據落點（快照-Verification 模型）、freshness（快照-Freshness）、身分生命週期（快照-Identity preservation、ID lifecycle）三題，快照中皆已裁；§4 六題亦已裁 ⇒ **可以動筆**。本表其餘處一律用「快照-X」名稱 |
| §2.3 措辭收斂與 9 筆 deferred findings 同批 | 見 §2 |
| plan「Global constraints 逐字照抄」同批重新裁定 | 已裁為甲′，見 §4 Q4 |

---

## 2. 逐節對照

「來源」欄代號：**快照-X** = 快照「本日已拍板」該條；**S1–S6** = spike 拍板；**F1–F9** = 9/1 deferred findings（原文見 §2.1）。

| 節 | 改什麼 | 為什麼 | 來源 |
|---|---|---|---|
| **文件頭**（1–7 行） | 加修訂註記：修訂日期、9/1 原版 commit `f80fc7b`、「本次修訂另經核可，事件閘門維持雙 YES」，並加一行指向本對照表（本表放在 `specs/` 但不是設計文件，靠這個指標被找到） | 修訂治理要求歷史可追、閘門不退回 | 快照-修訂治理 |
| **§1 背景與約束** | ①加入**上位原則**一段：先定 Artifact 責任 → 要表達的資訊 → 語言／結構 → 出生處與 owner → 最後才決定 ID／reference／機械檢查；「結構化副本仍是副本」；已有 owner 的資訊優先引用或重算。②上位原則之下加 **plan 的適用句**（Q4 甲′）：「Plan 不得成為既有 Contract constraint 的第二個 owner。需要自包含內容時，應由 authoritative source 動態產生／擷取；否則直接引用 authoritative source。不得人工維護一份聲稱逐字同步的副本。」並**明示這是新的 normative direction**：現行 `openspec/specs/plan-contract/spec.md:12`（SHALL「global constraints copied verbatim from the specs」）、`superpowers-bridge/schema.yaml:341`、`templates/plan.md:12,14` 尚未對齊，由後續 opsx change 修正；中間狀態不得寫成「現況已符合」（A 甲）。③第 17 行 corrective-fix 附註更新現況一句：已降級為 deferred spec cleanup、併 claudemd-governance-rewrite 批（2026-09-01 結算拍板）（Q6 甲） | ①這是今天所有裁定的上位判準，§3–§6 的修訂都從它推出，應放在總原則旁（第 21 行）。②見 §4 Q4。③不是改寫歷史裁定，而是避免現行文件繼續指向一個已不存在的 next action；歷史由文件頭指回 9/1 commit | 快照-上位原則；§4 Q4、Q6、A；09-01 handoff 結算決策 |
| **§2.1** I1（35 行） | 措辭補「在 capability 範圍內唯一」與「退休 ID 不得重用」（細節放 §3.1，I1 只指過去） | I1 的「重複 ID」原本沒定義範圍 | 快照-ID lifecycle |
| **§2.1** I3（37 行） | 明確 coverage 由 **Verification Result** 建立（不是 Task → Scenario） | 快照把建立者定為 Result | 快照-Scenario coverage |
| **§2.1** I6（40 行） | **定義「Blocking Verification Result」**：以機械方式導出，例如「支撐必要驗收標的（§4.2：所有被接受的 Scenario）的 Result」；並分清 I1–I7 是「完成保障條件」、不是驗收標的。②I6 的「required Evidence 存在並符合結構要求」補明：**包含 Result 引用的 Task 內 RED/GREEN**——Result 引用 Task 時，結構檢查沿引用到 Task；對 applicable task 的 RED/GREEN 結構，同時是 §2.2 TDD Evidence（required）這項 assurance condition 的判定內容（現行實作即 checks 8–11）。配合修改第 148 行括號句「I6 的『結構有效』驗的就是這種事」 | ①F5：該詞全文未定義，而同節第 43 行禁止語意判斷口袋。甲′ 已提供分類，可以用它定義。②§4.3 把 RED/GREEN 移到 Task 後，第 148 行把它綁在 I6 的那句失去錨點，須指明哪條規則負責檢查 Task 上的 RED/GREEN（2026-09-23 map 審 🟡） | F5；快照-Verification target（甲′）；map 審 r1 |
| **§2.2** 預設表（52–59 行） | ①表的收錄標準「Gate 判得動」與 Independent Review 一列對齊：寫明 v1 Gate 對這列實際判什麼；有 S6 之後，Orca supervised dispatch 紀錄（`dispatchId`／`agentTerminalHandle` 相異）即可機械判，沒有就依 G3 降級。②**新增一列 Verification executor independence，預設 `degradable`**（Q1 甲），取代第 59 行「known assurance candidate、暫不進表」。**措辭邊界**：本次拍板的是規範責任；**不得宣稱 verify executor provenance 已被 S6 證明可機械判定**——S6 實測的只是 review／implementation 兩類 dispatch 的身分區分，verify 階段是否有同樣可靠的 carrier 未實測，實作前須先確認 | ①F3。②快照已定「Result 不由 implementer 自我驗收；無獨立 verifier 時依 G3 降級並留紀錄」，本質上就是 degradable assurance，不應留在 procedure 散文（F4 抓的縫） | F3、F4、S6、快照-Scenario coverage、§4 Q1 |
| **§2.3** 生效契約（61–79 行） | ①第 70 行「Gate 只讀這份」限縮為「Gate 的 assurance 判定只讀這份；Core invariants I1–I7 恆常適用、不經此合成」。②第 75 行「這即是 G3 已定的…」改為「本輪定案（附錄 #6）：在 G3 的 required→BLOCK 之上，新增唯一合法出口…」，讓擴充看得出是擴充。③第 77 行 acceptance provenance **收斂為弱保證版**：保證「有顯式 acceptance record 且格式有效」，**不保證**「紀錄不可由 Agent 偽造」；強 human provenance 留待可信 runtime／UI actor metadata；Orca decision gate 保留為 optional enhancement | ①F2：與第 43、235 行字面矛盾。②F1：G3 原文是無條件 BLOCK（方向文件第 45 行），重新核可的出口是 9/1 才新增的。③S2 實測：OpenSpec CLI 無 approve 機制、Orca `--from` 是自報身分 | F1、F2、S2 |
| **§3 導言**（83 行） | 三邊 join 補註：Scenario → Evidence 的對應由 Result 建立；Task 層只 join 到 Requirement（C′ 不變） | 與快照 Scenario coverage 條一致 | 快照-Scenario coverage |
| **§3.1 身分層**（85–91 行） | 此節改動最多：①**唯一範圍**＝capability 內唯一；跨 capability 以 `capability / REQ-x` 引用。②**退休 ID 永不重用**；搬移／拆分／合併一律「舊 ID 退休、新 ID 出生」，lineage 只供追溯、**不是 alias**、不繼承舊 Result。③Requirement 退休沿用 OpenSpec REMOVED 的 Reason + Migration；Scenario 退休須有 Reason、lineage／Migration 的對等資訊，且必須記在 change 內隨 archive 保存；**載體格式不在本次定**，交實作 change 在真實 OpenSpec 限制下決定（Q2 甲）。④**archive 不得任意清理**——no-reuse 靠它，不建 registry（呼應第 91 行）。⑤第 89 行 Immutability 補：標題描述改動在 OpenSpec 是 RENAMED，**RENAMED 前後 ID 必須相同**。⑥**舊 ID** `REQ-PB` grandfathered，不因格式統一改名。⑦**Identity preservation**：OpenSpec 負責 merge、Bridge 負責 stable-ID preservation；重複 ID、RENAMED 前後 ID 不同、未正式處置卻消失 → BLOCK；預演在暫存複本實跑 `openspec archive`（CLI 無 dry-run），不重寫 merge；有 delta spec 的 change 不得 `--skip-specs`；此檢查不保證同一 ID 下語意未被改弱（屬 G1a） | 9/1 版只定了「不可變、fail-closed」，沒有範圍、重用、退休、搬移。研究文件 §3 ③⑤ 指出缺口，快照-Identity preservation、ID lifecycle 逐條補齊 | 快照-Identity preservation、ID lifecycle、舊 ID；研究 §3 ③⑤；實測（快照「實測」段：11 個 RENAMED 單一 change 可行、順序保留） |
| **新增 §3.5 Decision 引用**（§3 節尾追加，不重排既有節號） | `D<n>` 為 change-local；跨 change 引用寫 `change / D<n>`；歸檔後不得重排。明寫 Decision ID 是 **navigation／design identity，不是 Contract identity**：不參與 I1–I3，`per D5` 不能取代 `Contracts: REQ-x`（Q3 乙） | 研究 §3 ①：Task 實際上最常引用的是 Decision，而 9/1 版完全沒提；放 §3.2 會被誤讀成可以替代 Contracts: | 快照-Decision ID；研究 §3 ①；§4 Q3 |
| **§3.4 Result 欄位**（104–117 行） | ①補 `id`（檔內唯一，S5 已拍板）與 invalidation 紀錄（append-only 同檔）。②`evidence` 欄：**短證據直接寫、長證據引用 repo 內已 commit 的永久檔案**；scratchpad、git-ignored ledger、未追蹤檔一律不得作證據落點；Evidence 已有 Task owner（RED/GREEN）就引用 Task，不複製；**無 Task owner 者**（如既有 regression test）由驗證活動自行產生 Evidence。③寫明 `verification-results.json` 是 append-only 驗收台帳，`verify.md` 是可覆寫的工作報告、不是證據 owner。④`contract` 欄的指認對象限縮為契約標的（Requirement／Scenario），matrix row／fixture／test case 不作正式 target | 快照-Verification 模型把證據 owner 分開；S5 已定 id 與 invalidation 載體，9/1 版還沒寫進來 | 快照-Verification 模型、Verification target；S5 |
| **§4.2 Method**（135–144 行） | ①把驗證流程寫成「驗收標的 → 方法 → Evidence → Result → Gate」。②加：Result 由 verify／review 階段產生，不由 implementer 自我驗收；無獨立 verifier 時依 G3 降級並留紀錄（對應 §2.2 新增列）。③Gate 機械查 coverage、freshness、引用存在與結構；**不判語意充分性**。④「能重算」只指**程式可重算** | 快照-Scenario coverage、Verification 模型 | 快照 |
| **§4.3 TDD 證據契約**（146–151 行） | 第 148 行原寫 RED/GREEN 放在 `method = automated-test` 的 Result；實作（`loosen-plan`，checks 8–11）已放在 **Task**。改為：RED/GREEN 由 Task 保存（RED 是不可重算的歷史事實）；Result 需要時引用該 Task，不複製一份。S4 已實作的 applicability 顯式標註順帶寫入（「annotation 是語意判斷、受 artifact review；Gate 只驗存在與格式」） | `loosen-plan` 有明確選擇 Task 作為第一個 carrier，並保留未來搬到正式 Result 的可能性（`openspec/changes/archive/2026-09-04-loosen-plan/design.md:58`：「This is the first carrier, not an architecture invariant … the carrier can move」）；2026-09-23 的新裁定進一步決定 RED/GREEN 長期仍由 Task 擁有，因此 **supersede** 了當時「未來可搬」的暫定方向。9/1 正式設計第 148 行從未跟著改，所以本次要寫回 | 快照-Verification 模型；S4；研究 §3 ②；`loosen-plan` design.md:58 |
| **§5 Degraded Mode**（167–192 行） | 第 190 行「降級表 v1 第一個明名項目——審查獨立性」之後，補**第二個明名項目：Verification executor independence**（degradable；fallback 為同一套 verification procedure 由非獨立執行者執行＋degradation record；Assurance impact 為驗證結論的獨立性下降）。沿用第 179–186 行的降級紀錄最小形態，不另立格式 | Q1 選甲的連帶修改：進 §2.2 預設表為 degradable，就要有對應的降級項目 | §4 Q1 |
| **§6 Result Lifecycle**（194–215 行） | ①**Digest domain** 由系統固定、不自我指涉：排除 Result、`verify.md`、Gate 自己的紀錄、change 外工作紀錄（如 handoff）；納入被驗內容（spec、design、tasks、實作、測試等）。不允許每筆 Result 自報依賴範圍。②v1 維持 coarse digest；diff-aware invalidation 不拉進 v1（第 209 行已如此，補理由：漏算依賴會產生假保證，兩種錯誤代價不對稱）。③操作原則：候選版本穩定後才產生 Result。④統一用詞為 **`FRESH`**（B）：§6 的 lifecycle vocabulary 本來就是 FRESH／STALE／CONFLICT；其他處的 current、current valid、fresh 改為引用 FRESH 語意。**掃描集**：第 144 行（「fresh PASS」）、第 204 行（「current」）、第 227、231 行（「current valid Gate PASS」）；修訂時再以全文搜尋 `current`／`fresh` 覆核有無遺漏 | ①快照-Freshness 補的陷阱：digest 若包含自己的紀錄，Result 一寫進去就讓自己過期。④F7 | 快照-Freshness；F7；B |
| **§7 Acceptance Gate**（217–237 行） | ①第 233 行「輸入」補 identity preservation 預演結果（§3.1 ⑦）。②第 227、231 行用詞改為 FRESH（F7、B，掃描集見 §6 列）。③S5 的界線寫進來：`gate-pass.json` 是稽核紀錄、**不是**通行證，archive 必須機械確認存在 FRESH 的 Gate PASS | S5 拍板把 §7 既有原則落到載體層；identity 檢查是新的 Gate 輸入 | S5；快照-Identity preservation；F7 |
| **§8 不保證清單**（239–252 行） | ①標題第 239 行改為「方向文件 §1.4 第 3 題」（本文無 §1.4）。②新增：**驗證材料的內部覆蓋完整性**（matrix row／fixture／test case 是否每列都有測試）不由 Gate 保證。③新增：**capability rename**（n=0，不建機制）。④**併入現行第 5 條**（C）：acceptance record 結構有效但內容可能由 Agent 偽造，與「Evidence 結構存在 ≠ Evidence 為真」是同一個 assurance boundary，不另立一條。⑤**不新增**：「同一 ID 下語意是否被改弱」已由現行第 4 條（G1a）涵蓋，只需由 §3.1 ⑦ 指回第 4 條 | ①F6。②③快照明文「補進 §8」。④S2、C | F6；快照-Verification target、暫不處理；S2 |
| **§9.2 Spike 清單**（275–284 行） | S1–S6 已執行：加一句指向 spike 報告與其拍板總表。S6 列補註：已實測的是 review／implementation 的 dispatch 身分區分；**verify executor provenance carrier 未實測**，列為 Verification executor independence 實作前的前置確認（F4、Q1 措辭邊界） | 9/1 版寫的是「待 spike」，目前已完成；F4 指出 S6 題目範圍比 executor independence 窄 | spike 報告；F4；§4 Q1 |
| **§9.3 Record 處置**（286–292 行） | ①第 288 行被吸收的 record 補 work-map id：`task-20260826-tdd-evidence-contract`、`task-20260827-apply-degradation-boundary`。②加一行：S3 會動 `schema.yaml`，實作 change 須依 CLAUDE.md「跨檔耦合」表連動。③第 290 行「Scenario v1 必做」**維持不變** | ①F8。②F9。③快照「Scenario coverage：v1 仍必做」——研究 §7 第 7 題（延後 Scenario 層）因此不成立 | F8、F9；快照-Scenario coverage |
| **附錄** | 新增「2026-09-23 修訂拍板紀錄」表，逐條對應本次修訂（仿 9/1 附錄格式） | 修訂另行核可，需要可追的紀錄 | 快照-修訂治理 |

### 2.1 9/1 deferred findings 原文轉錄（F1–F9）

來源：2026-09-01 fallback 代審報告（contract-neutral-reviewer），`[NIT_DEFERRED]` 行逐字：

| # | 位置 | 內容 | 落點 |
|---|---|---|---|
| F1 | :75 | "G3 已定" attributes the required→re-approval escape to a prior decision that states an unqualified BLOCK | §2.3 |
| F2 | :70 | "Gate 只讀這份" reads as excluding I1–I7, contradicting lines 43 and 235 under a literal reading | §2.3 |
| F3 | :52 | table criterion "Gate 判得動" vs line 59/S6 admission that independence is not yet machine-evaluable | §2.2 |
| F4 | :59 | prerequisite for verification-executor independence routed to S6, whose question covers only review-vs-implementation | §2.2、§9.2 |
| F5 | :40 | I6 "Blocking Verification Result" undefined in a subsection that bans semantic-judgment pockets | §2.1 |
| F6 | :239 | bare "§1.4" citation resolves only in the direction document; this file has no §1.4 | §8 |
| F7 | :204 | FRESH / current / current valid terminology drift across §6 and §7 | §6、§7 |
| F8 | :288 | absorbed records cited by prose name only; work-map ids would make the disposition locatable | §9.3 |
| F9 | :281 | S3 touches schema.yaml but §9.3 does not point at CLAUDE.md's 跨檔耦合 obligations | §9.3 |

9 筆全部有落點，沒有「無處可放」的。

---

## 3. 同批處理、但不在正式設計本文

| 對象 | 改什麼 | 來源 |
|---|---|---|
| 研究文件 §2「Proposal → Requirement」列與 §7 第 5 題 | 加註「2026-09-23 裁定已推翻」並指到快照（Proposal 留 capability 粒度） | 快照-Proposal；快照「三」 |
| 研究文件 §8「RENAMED 後移到末尾」推論 | 加註「2026-09-23 後續實測已推翻」並指到快照「實測」段（11 個 RENAMED 後順序保留） | 快照「實測」 |
| 研究文件 §7 第 7 題 | 加註「2026-09-23 已裁：Scenario 層 v1 仍必做」並指到快照 | 快照-Scenario coverage |
| spike 報告兩筆 deferred（:4「實測結論尚缺完整、可保存及重現的命令與輸出憑據」、:1「中英文間距與標點格式不一致」，逐字引自 2026-09-01 代審的 `[NIT_DEFERRED]` 行） | **不同批**（Q5 乙）：它們不是正式設計的 normative defect，且「補可重現憑據」可能需要重新取證；已另登記工作地圖 `task-20260923-spike-report-deferred` 追蹤，不混兩種 Artifact lifecycle。09-01 handoff「同批收共 11 筆」的說法就此作廢 | 09-01 handoff 第 118、154 行；§4 Q5 |
| 「Global constraints 逐字照抄」的四處現行載體：`openspec/specs/plan-contract/spec.md:12`（canonical spec 的 SHALL）、`superpowers-bridge/schema.yaml:341`、`templates/plan.md:12`（標題）與 `:14`（填寫指引註解） | **取消人工維護的逐字副本**；改採 reference 或 source-derived snapshot（由 authoritative source 產生／擷取），兩者擇一由後續 schema change **實測 reviewer／executor 是否需要內嵌內容**後選型（Q4 甲′）。屬 schema 改動，走 opsx change，不在本次文件修訂內動；該 change 須含對 plan-contract requirement 的 **MODIFIED delta**。在它落地前，正式設計的原則與這四處刻意不一致（見 §2 表 §1 列 ②） | 快照-修訂治理；研究 `2026-09-10-contract-drift-archaeology.md` H5；§4 Q4 |

研究文件是 records 類文件，修正方式是**加註**（D）：原判斷保留，旁邊明確標「2026-09-23 後續實測／裁定已推翻」並指到新證據。研究文件保存當時推理，正式設計才保存現在有效的規則。

---

## 4. 修訂前裁定（2026-09-23 使用者裁定）

| # | 題目 | 裁定 | 理由（使用者） | 對本表的影響 |
|---|---|---|---|---|
| Q1 | 「驗證者不是實作者」要不要列入保障強度要求 | **甲**：列入 §2.2，預設 `degradable` | 快照已定「Result 不由 implementer 自我驗收；無獨立 verifier 時走 G3 降級」，本質上就是 assurance requirement，不應留在 procedure 散文。**措辭邊界**：拍板的是規範責任，不宣稱 verify executor provenance 已被 S6 證明可機械判定——S6 只證了 review／implementation 的 dispatch 身分區分，verify 的 carrier 未實測，實作前須確認 | §2.2、§4.2、§9.2 列；**連帶**：§5 補第二個明名 degradable 項目 |
| Q2 | Scenario 退休載體格式這次定不定 | **甲**：只定責任，不定格式 | 正式設計寫清楚須有 Reason、lineage／Migration 對等資訊、存在 change 內並隨 archive 保存；格式由實作 change 在真實 OpenSpec 限制下決定，符合 spike-first 紀律 | §3.1 ③ |
| Q3 | Decision ID 放哪 | **乙**：新開 §3.5「Decision 引用」 | Decision ID 是 navigation／design identity，不是 Contract identity；塞進 §3.2 易被誤會 `per D5` 可取代 `Contracts: REQ-x` | §3.5 列 |
| Q4 | plan「Global constraints 逐字照抄」 | **甲′**：取消人工逐字副本；reference 或 source-derived snapshot，由後續 schema change 實測選型 | plan 是下游執行者的工作包，執行者未必回頭讀 spec；純 reference 可能拿掉必要執行上下文。H5 只證明「人工逐字副本會漂移」，未證明「純 reference 對 plan consumer 足夠」。正式設計寫原則：「Plan 不得成為既有 Contract constraint 的第二個 owner。需要自包含內容時，應由 authoritative source 動態產生／擷取；否則直接引用 authoritative source。不得人工維護一份聲稱逐字同步的副本。」 | §1 ②；§3 表 Global constraints 列 |
| Q5 | spike 報告兩筆 deferred 是否同批 | **乙**：分開 | 不是正式設計的 normative defect；補可重現憑據可能需重新取證；不為湊「11 筆一起清」混兩種 Artifact lifecycle | §3 表 spike 列；已登記工作地圖 `task-20260923-spike-report-deferred` |
| Q6 | §1 第 17 行附註是否更新 | **甲**：更新現況一句 | 不是改寫歷史裁定，而是避免現行文件繼續告訴讀者一個已不存在的 next action；歷史由文件頭指回 9/1 commit | §1 ③ |
| A | 正式設計寫進 Q4 原則後，與現行 plan-contract 規格暫時矛盾，如何處理 | **甲**：照寫，明示是新的 normative direction、下游尚未對齊 | Formal Design 定方向，下游規格跟上；中間狀態不能寫成「現況已符合」 | §2 表 §1 列 ②；§3 表 Global constraints 列 |
| B | freshness 狀態統一用詞 | **`FRESH`** | FRESH／STALE／CONFLICT 本來就是 §6 的 lifecycle vocabulary，避免三套近義詞 | §2 表 §6 ④、§7 ② |
| C | 「acceptance record 可被偽造」新增一條或併入 | **併入 §8 現行第 5 條** | 與「Evidence 結構存在 ≠ Evidence 為真」是同一個 assurance boundary | §2 表 §8 ④ |
| D | 研究文件更正方式 | **加註**，不改寫 | 研究文件保存當時推理，正式設計保存現在有效的規則 | §3 表研究文件三列 |

A–D 為 map 第 1 輪文件審（2026-09-23，fallback，✅ Mergeable、9 筆非阻擋建議）後的追加裁定；該 9 筆已全數修入本表。

我先前在各題列的「沒查的」仍成立，已併入 §5。

---

## 5. 我沒查的、我跳過的

- **沒有逐條重讀方向文件**。只核對了 F1 引的第 45 行 G3 原文（確為「必須 BLOCK」、無重新核可出口）；其餘方向文件內容未重讀。
- Q4 引的 H5 漂移實例（`plan.md:17`）依研究文件的研究對象判定為 `fix-v2-blocking-defects` 的 plan；H5 那一列本身沒寫 change 名，我沒回原檔核對行號。
- **§4.1、§4.4 判定為不需修改**，依據是逐節讀過、快照與 findings 都沒有指到它們。§5 原本也判為不需修改，Q1 裁甲後已加入對照（§2 表 §5 列）。
- **verify 階段是否走 supervised dispatch、S6 的欄位是否同樣可用：未實測**（Q1 措辭邊界即由此而來）。
- **各 reviewer／executor 實際會讀哪些 artifact（只讀 plan 還是也讀 spec）：未查**。這是 Q4 甲′ 留給後續 schema change 實測的事。
- 快照「實測」段說跨多個 capability 的 RENAMED **未測**；§3.1 的寫法不依賴它，但日後補 ID 的實作 change 會依賴。
- 修訂後預估改動量：**未估**。
