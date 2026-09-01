# Bridge Guarantee 正式設計:Completion Contract 系統(v1)

> 2026-09-01 brainstorming 定案。方向文件([2026-08-27 技術方向與設計邊界](./2026-08-27-bridge-guarantee-architecture-direction.md))指定的「正式設計」,輸入為其 §6 五題定案、PoC 報告([2026-08-28 traceability-gate](../poc/2026-08-28-traceability-gate/poc-report.md),結論 concept supported)與本輪逐題釐清結論。
>
> **定位:定義完成契約系統的責任邊界與判定規則,不是 implementation spec。**schema.yaml 欄位形狀、proposal override 語法、Scenario 載體等,一律由 §9 的 bounded capability spike 在實作前確認,本文件不預設 OpenSpec / Harness / Orca 已原生支援任何特定欄位。
>
> **狀態:核可後即為事件閘門的第二個 YES**(第一個 YES = PoC 通過,2026-08-28),雙 YES 後 schema 實作解鎖;實作仍逐塊走各自的 OpenSpec change 流程。

---

## 1. 背景與約束

**既有約束(引用,不重新設計、不重新解釋)**:

- CLAUDE.md 的事件閘門與 corrective-fix exception 已存在且已履行(`fix-tdd-transitive-claim` 已 archive),本設計不得重新解釋或擴張其歷史語意。
- 方向文件十條設計護欄全數繼承;本文件特別依賴:Evidence 不當主系統(#3)、Contract Verification 不退化成「又跑一次測試」(#4)、Gate 不變成 Agent prompt(#5)、traceability 夠用就好(#6)、PASS 必須有 freshness(#7)、`verify.md` 暫不重構(#8)。
- 附註(非本設計章節):主 spec `repo-guidance` 尚未載明 corrective-fix 例外,為既有審查黃燈,後續以獨立小 delta 補字。

**設計吸收與 record 處置(A′ 原則)**:本設計吸收「TDD 證據契約」與「apply 階段交件證據」兩條 record 的**設計責任**(分別落在 §4、§5);核可後該二 record 標 absorbed/resolved by Formal Design。其中殘餘的**實作責任**(schema 實作、CLAUDE.md 治理語言改寫、spike 執行)轉成後續 OpenSpec change/tasks——**設計完成 ≠ 能力已交付**。

**總原則(主軸句的落點)**:一份設計文件定義「完成系統」;後面的 change 逐塊實作。Complete 要變成一個可以被證明的狀態;模型仍擁有解題路徑,Harness 只接管不能靠模型自我宣稱的完成邊界。

## 2. Completion Contract:Complete 的定義

**核心句**:Complete 不是 Agent 的宣稱,是一組可機械判定的終態條件。**Gate PASS = Change Complete**(方向文件 §6#6 定案);archive 前置檢查是第二道保險、不是 Completion 本體(其 freshness 要求見 §7)。

條件分兩類,治理方式不同:

### 2.1 Core Integrity Invariants(核心完整性條件)

系統成立的基本規則,**任何 change 都不可關閉、不進 override 模型**:

| # | Invariant |
|---|---|
| I1 | Requirement / Scenario 有足以支撐其追蹤層級的 stable identity;缺 ID、重複 ID、dangling reference → fail-closed 報錯 |
| I2 | 每條被接受的 Requirement 有 Task 承接 |
| I3 | 每條必要 Scenario 有 Verification coverage |
| I4 | Expansion scan 已執行且有紀錄;所有列出的疑似項已 disposition |
| I5 | STALE Result 不可使用;CONFLICT fail-closed |
| I6 | Blocking Verification Result 全為 PASS,且 required Evidence 存在並符合結構要求 |
| I7 | 所有 authoritative tasks 均已完成(`tasks.md` 全 `[x]`) |

不設「無 unresolved blocker」類萬用條款:Gate 條件就是 I1–I7 加生效契約的 assurance conditions,不留語意判斷口袋。若日後出現正式的 blocker 狀態,列成明確條件再進表。

### 2.2 Assurance Requirements(保障強度要求)

進 **required / degradable** 模型,可被 change-level override:

- **required**:該能力不可用 → BLOCK,除非回 proposal 修改本 change 的 Completion Contract 並重新核可。
- **degradable**:該能力不可用 → 可依預先定義的 fallback 繼續,但**必須留下 degradation record**(留痕是 degradation 的義務,與 default 是哪個無關)。

**v1 預設表**(只列目前確實存在、Gate 判得動的機制,不預鋪):

| Assurance | v1 預設 | 說明 |
|---|---|---|
| Independent Review(含 expansion scan 的獨立性) | **degradable** | 降級 ≠ 不做:review 照做、同一套 procedure,降的是執行者獨立性,且必留降級紀錄(§5) |
| TDD Evidence(對 applicable executable-behavior code task) | **required** | v1 verification policy,非 Bridge Guarantee 本身;證據要求見 §4.3 |

「Verification executor independence」(驗證由非實作者執行)為 **known assurance candidate**:與 Independent Review 概念相近但非同一事,v1 尚無可被 Harness 機械辨識的執行者身分能力,依「不把還沒證明能管的事寫成系統已經會管」原則暫不進表;前置事實由 Spike S6 取得(§9)。

### 2.3 Effective Completion Contract(生效契約)

```text
Schema defaults(一般政策:這類 change 平常怎麼做)
        +
Proposal 固定區段「Completion Contract Overrides」(本次明確例外)
        ↓
Effective Completion Contract(本次真正要遵守的規則)
        ↓
Gate 只讀這份
```

- 無 override 區段或無對應項目 = 吃 schema 預設,這是唯一允許的「沒寫」。
- **加嚴**(degradable → required):一般 override,直接寫。
- **放寬**(required → degradable):**change-local degradation**——必須顯式附理由,並隨 proposal 的接受流程取得使用者接受。這即是 G3 已定的「修改該 change 的 Completion Contract 並重新核可」,不另建 waiver / override 子系統。
- Global schema default 的修改只用於「改變所有未來 change 的預設政策」,不拿來處理單一 change 的現實例外;反之亦然。
- 「使用者接受」如何被 Gate 機械判定(acceptance provenance),是 Spike S2 必答題(§9)——否則 override 本身又成 self-claim。

TDD 預設 required 就是「TDD 不可丟」硬約束的機械形態:想丟它,唯一路徑是 proposal 明寫降級+理由+使用者接受,或修改 schema 預設——兩條路都看得見、都要審。

## 3. Minimal Traceability(最小追溯)

三邊 join:`Requirement/Scenario ↔ Task ↔ Verification Result`。夠用就好(護欄 6)。

### 3.1 身分層(I1 的展開)

- **架構規則**:每條可追蹤 Contract 必須有 stable ID。ID 是 identity,標題文字只是 description。
- **v1 載體**:ID 寫在 Requirement heading(例 `### Requirement: REQ-12 <description>`)。未來 OpenSpec 若提供正式 ID 欄位,換載體不換架構。
- **Immutability**:Contract 被接受後,改措辭不改 ID;改 ID 視為契約身分變更、需明確處置,不得當普通 rename(否則所有舊 reference 被無聲切斷——正是 G1a 要防的「靜默弱化」的機器版)。
- **Scenario**:requirement-scoped stable sub-ID(例 `REQ-12-S1`),供 Verification coverage 指認;載體與 extraction 由 Spike S1 確認。
- **Fail-closed**:缺 ID、重複、dangling → 直接報錯,不默默續跑。不引入 UUID / registry / 資料庫。

### 3.2 承接層(I2、I7)

- **`tasks.md` 是 authoritative task list(SSOT)**(方向文件 §6#5);ticket 檔是 Worker 工作包、非權威紀錄。
- Task 承接以 `- Contracts: REQ-12` 標註;**附屬語法必須機械可判**(PoC 架構訊號 1:縮排嚴格深於 checkbox;孤兒標註、同層 sibling 標註不算數——這兩個偽造路徑是 PoC 兩輪 review 實際抓到的)。
- **方向性規則**:Requirement→Task 必須全覆蓋(I2);Task→Contract **不強制**——允許無標註 task(鷹架、雜項),不參與 contract join,但仍受 I7 管。反向強制會逼人硬掰對應、製造假 traceability。
- **檢核維度分層**(C′ 定案):Task 層 join 到 Requirement(工作分配可以到 Requirement);Verification coverage 到 Scenario(驗收 coverage 要到 Scenario)。

### 3.3 交叉核對(常設機制)

任何「從文本抽取」的計數,Gate 都要與 CLI JSON 的計數核對(PoC 架構訊號 2:此招實際攔下 CLI 對破損標題行的寬鬆解析)。**語意是「兩種獨立方法互相抓錯」**,不是「CLI 是真理」:兩邊不一致 → 有問題 → BLOCK 查清楚,不預設哪邊對。

### 3.4 Verification Result 欄位(v1 最小集)

在 PoC 三欄(contract / status / evidence)上只加必要者:

| 欄位 | 說明 |
|---|---|
| contract | Requirement ID;**必須能指認到 Scenario**(既然 coverage 到 Scenario,Result 就要說得出自己驗哪個 Scenario;欄位形狀由 Spike S5 定) |
| status | 封閉集 `PASS / FAIL / BLOCKED`(記錄當下的事實) |
| method | §4.2 封閉集之一 |
| evidence | 依 method 的結構要求(§4.2) |
| digest | Harness 機械計算的 tree digest(freshness 依據) |
| timestamp | 記錄時間 |

**staleness / conflict 不存欄位**——是 Gate 時導出的 lifecycle state(§6),存了就會過期、又成雙載體。

## 4. Contract Verification(契約驗證層)

**定位**(護欄 4):控制層,不重造測試框架;逐條回答「這條契約被充分驗證了嗎」,測試只是 method 之一。流程:讀 Contract(含 Scenario 清單)→ 依生效契約決定 Verification Method → 呼叫既有能力執行 → 收斂成正式 Result。

### 4.1 Verification Procedure Provider

**Verification Procedure Provider**:Contract Verification 不自行定義各類工程驗證的完整 procedure。既有 Skill 已定義可靠 review/test procedure 時,優先重用該 Skill 作為 method executor;本設計只定義其必須產出的 Result/Evidence contract,以及 Gate 如何接受結果。**Skill availability(或「有呼叫 Skill」)不得被等同於 verification success**——Skill 是 procedure provider,正式 Result/Evidence 才是 Gate 的輸入。分工:

```text
Skill    → 定義怎麼 Review / Test(procedure)
Executor → 執行 Skill
Harness  → 驗 Result / Evidence 是否滿足 Contract
```

此分工同時是 §5 降級順序的依據:優先只降執行者獨立性、保留同一套 procedure。它也提供後續優化 baseline:先用現有 Skill 實測 Evidence 品質與漏檢,再迭代 Skill,不必重做 Completion Contract / Gate 架構。

### 4.2 Method v1 封閉集(四種,不預鋪)

| Method | Evidence 結構要求 |
|---|---|
| `automated-test` | 執行輸出(command result 本身即可——護欄 3) |
| `inspection` | 檢視者結論 + 檢視對象指認(PoC 已證此型可過 Gate) |
| `manual-demonstration` | 操作結果紀錄 |
| `analysis` | 分析輸出 |

Scenario coverage 責任在本層:Verification 對每條必要 Scenario 給出覆蓋;Gate 只機械核對「每個必要 Scenario 有指認它的 fresh PASS」。**「必要」的 v1 預設:所有被接受的 Scenario 均為必要**——排除任一 Scenario 屬契約變更,走 proposal 接受流程,不留機器或 Agent 的語意裁量。

### 4.3 TDD 證據契約(吸收自原 record)

- **條文**:對 applicable executable-behavior code task,v1 驗證政策要求 `method = automated-test` 且 evidence **必須含 RED 輸出與 GREEN 輸出**——RED(測試先失敗的輸出)證明測試真的會抓,GREEN 證明實作真的過。只有 GREEN 沒有 RED = evidence 結構不合格(I6 的「結構有效」驗的就是這種事)。
- **範圍**:不是所有 task 一律 TDD。改文件、純資料調整等不 applicable 的 task 不硬造 RED/GREEN;applicability 的機械判準與 N/A 處置由 Spike S4 定。applicable 而不想做 = change-local degradation,走 proposal 留痕(§2.3)。
- **誠實邊界**(與 digest 同一邏輯):RED/GREEN Evidence 存在且結構合格,**不能證明開發歷史完全真實**(先寫完功能再故意弄壞跑一次,也能製造 RED/GREEN)。Harness 保證證據被要求、被檢查;真偽 assurance 依賴 review 層,並隨其降級而降級(§8#5)。
- 這是把 TDD 從「步驟要求」翻譯成「證據要求」——「規定證據,不規定步驟」主軸落在 TDD 上的具體形態。TDD 是 v1 verification policy,不是 Bridge Guarantee 本身;修改它 = 修改驗證契約,是看得見的改動。

### 4.4 G1b:Contract Expansion Scan(I4 的執行面)

責任三角:

```text
Diff     → 幫 Reviewer 找值得看的地方(列出新增/修改的介面、行為、資料結構等 change surfaces;只提供線索,不自行判定)
Reviewer → 判斷內容是否疑似超出契約(語意偵測)
Gate     → 確保審查真的做過、問題真的處理完(機械完整性)
```

- Scan 報告**必須明確記錄**「未發現疑似項」或列出疑似項;缺 scan 區段 = 視同沒掃 → BLOCK(不以「沒寫大概就是沒有」推定)。
- 每個疑似項三選一處置:①判定為 implementation detail,附理由 ②確認為合理新契約行為,回 Spec 正式加入並取得接受 ③移除。未處置 → BLOCK。
- 正常模式由 independent reviewer 執行;無獨立 reviewer 時降級為 self-review + 顯式標示獨立性下降(§5),是否允許依生效契約的 Independent Review 分級。

## 5. Degraded Mode(降級模式)

**基線**(G3 定版):能力不足時可退回較簡單的執行模式;失去哪些能力就顯式標示哪些保證不可用;**失去的是該 change 的 required 保證 → BLOCK,不得降級**。分層:Orca 是 execution capability provider、不是 hard dependency——降級模式 = Core Harness Guarantee(traceability、驗證、Gate 都在),消失的只是 Orca 附加能力(多 Worker 並行、隔離、dispatch、implementer/reviewer 分離)。

**治理方向:execution-path agnostic, contract-governed**(吸收自「apply 階段交件證據」record)。Harness 不要求工作一定由 Orca、subagent 或某個指定 executor 完成;任何 execution path 都可採用,但它必須:

1. 實際具備 Effective Completion Contract 要求的 capability;或
2. 依 G3 合法降級;
3. 並產生對應的 Evidence / degradation record。

**Evidence 不能把不存在的 capability 變成存在**:若 Independent Review = required,則 self-review 即使產出完整 review report,也不能被當成 independent review。

**降級紀錄最小一般形態**(發生 fallback 一律留痕):

```text
<capability>: unavailable
Fallback: <實際採用的替代方式>
Reason: <為什麼不可用>
Assurance impact: <哪項 assurance 降低>
```

degradable 的語意不是「可以不做」,而是「可以使用較弱但仍有效的 fallback」。降級優先順序依 §4 分工:**能保留同一套 Skill/procedure 就不要連驗證方法一起降,優先只降執行者獨立性**。正常模式 = review skill + independent reviewer;降級 = 同一套 review skill + self-review + degradation record。

**降級表 v1 第一個明名項目——審查獨立性**(方向文件 §6#3 指定):2026-08-27 實測(該次三輪審查中,語意類缺陷自查命中 0%、外部審查命中 100%)作為「review independence 確實可能造成 assurance 差異」的 design evidence——但不得泛化成 self-review 固定 0%、external review 固定 100% 的普遍能力結論。

**配套實作責任**:CLAUDE.md 現行「禁止某 fallback executor」的治理語言(紅旗「❌ 在 apply instruction 加 executing-plans 當 fallback」),由後續 implementation change 改寫為上述 capability / evidence / degradation 語言;本設計不直接修改。

## 6. Result Lifecycle(結果生命週期)

**兩個不相混的 enum**:

- **Stored Verification Status**(記錄當下的事實):`PASS / FAIL / BLOCKED`。
- **Gate-derived Lifecycle State**(Gate 依目前 artifact state 與多筆 Result 導出,不落地):`FRESH / STALE / CONFLICT / historical(superseded)`。

**Freshness invariant(正式規則)**:

```text
result digest == current digest → 可進一步判定為 current
result digest != current digest → STALE,不得支撐 Complete,須重驗
```

- **STALE ≠ FAIL**:表示 Result 曾經成立,但已不能證明目前 artifact state;舊 Result 保留作歷史紀錄,不刪除。舊 digest 的 FAIL 被新結果接替是 supersession——系統正常運作,不是 conflict。
- **Invalidation optimization(可選層,不阻塞 v1)**:machine-evaluable 的 Diff rules 可縮小失效範圍(例:diff 只動 docs → code verification 不 stale;code/doc 分面只是第一個實例,不是架構本身),但不得改變 fail-closed 語意、**不得靠 Agent 語意宣告「這個改動無關」**(自宣告依賴範圍已否決——把 freshness 交回 self-claim)。v1 只做 coarse-grained digest。

**CONFLICT**:同一 digest + 同一 Scenario 出現互斥的 PASS/FAIL → unresolved CONFLICT → Gate BLOCK。不採「最新自動覆蓋」:同一可辨識 artifact state 下互斥,表示目前的 verification claims 無法同時成立——不預判原因(可能是 flaky、造假,也可能是外部服務、fixture、DB、時間等 digest 未涵蓋因素)。**Explicit resolution**:查清楚後將錯誤 Result 有紀錄地標 invalid 附 reason,或 artifact 真正改變後在新 state 重驗。不允許 Gate 挑對 Complete 有利的一筆,也不允許以無意義修改製造新 digest 逃避 CONFLICT。

**核心原則**:Result 記錄「當時發生了什麼」;Gate 判斷「這些紀錄現在還能不能拿來證明 Complete」。

**措辭邊界**:digest 只證明「目前 artifact state 是否仍等於驗證時的 state」,不證明 Verification 真的執行過、Evidence 為真——那是另一層 assurance(§8)。

## 7. Acceptance Gate(驗收閘門)

**定位**(護欄 5):機械判定,不是 Agent prompt。Model 產生判斷(review 結論、verification 結果),Harness 判斷「齊不齊、PASS 沒、還 fresh 嗎」。

**綁定點**(方向文件 §6#6):tasks 全 `[x]` → 跑 Gate → **Gate PASS = Change Complete** → 才可 archive。**Orca 與 I7 的分工**:Orca runtime 可提供 Task completion 的早期攔截(工作途中不讓未完成的 task 往下走),但 I7「authoritative tasks 全 `[x]`」仍由 Core Acceptance Gate 最終機械檢查——Orca 不是 hard dependency,不能變成沒有 Orca 就沒人檢查 I7。

**Gate PASS 自身的 freshness**(與 Result 同一邏輯——驗收證書只能證明它驗收時看到的那個版本):

```text
Gate 執行時:記錄評估當下的 artifact digest + Effective Completion Contract state
archive 時:檢查「current valid Gate PASS」——同一 state 才有效
state 已變 → Gate PASS stale → 重跑 Gate
```

archive 的第二道保險是「**current valid Gate PASS exists**」,不是「PASS record exists」。digest 具體算法屬實作,invariant 在此定下。

**輸入**:Effective Completion Contract、contract 集(CLI JSON + 交叉核對)、`tasks.md`、Verification Results、降級紀錄、expansion scan 紀錄。

**判定**:I1–I7 + 生效契約 assurance conditions,逐條導出 YES/NO;全 YES = PASS,否則 BLOCK。**Gate report 逐條列明每個條件的判定與依據**(PoC 報告格式已證可行)——BLOCK 時要能讀出缺哪條、缺什麼;Gate 的價值一半在擋、一半在告訴你差什麼。

**實作歸屬**:Harness 側機械程式(PoC `gate_check.py` 的正式化),借 sd0x 的 durable state / digest 模式(sd0x 在它自己家裡是提醒層;「機械擋下」是在其 state/digest 基礎上新加的行為)。具體宿主與呼叫方式屬實作。

## 8. 「不保證」清單(§1.4 第 3 題指定的窮舉輪)

這套系統**不保證**:

1. **規格本身的品質與正確性**——「已接受的規格」是輸入前提。
2. **prompt / instruction 文字層的正確性**——CI 與 Gate 都驗不到。
3. **Agent 產出品質上限**——保證流程性質,不保證聰明程度。
4. **語意判斷零漏失**——含 G1a 的 silent weakening / incorrect semantic implementation(traceability 完整、Reviewer 判 PASS,實作仍可能把需求做弱而未被看出),與 G1b 的 silent expansion(Reviewer 可能漏抓)。Harness 保證這些檢查被要求、被執行、被記錄與處置;不保證 Reviewer / Verification judgment 永遠正確。無獨立 review 時此項 assurance 進一步降低,依 G3 顯式呈現。
5. **Evidence 為真、開發歷史真實**——結構有效的 Evidence 不等於 Evidence 為真;machine-captured command output 可提供較強 provenance,但仍不證明完整語意或歷史不可偽造(RED/GREEN 可被事後製造;status/evidence 在 v1 可由 Agent 寫出——PoC 宣稱邊界)。真偽 assurance 依賴 review 層,並隨其降級而降級。
6. **digest 未涵蓋的外部狀態**——外部服務、runtime environment、fixture、DB state、時間、network 等不在 tree digest 內;digest 相同不代表完整執行環境相同。
7. **`tasks.md` 之外任何載體與事實同步**——ticket 檔等非權威紀錄。
8. **change-local degradation 決策本身的明智程度**——系統保證降級被看見、被接受;不評判該不該接受。

**窮舉紀律聲明**:此清單經 2026-09-01 設計輪窮舉;但依本 repo 既有教訓(2026-08-31:凍結清單 35 段之外仍被審查抓到第 6 段),**清單不得當窮舉證明**——後續發現的新「不保證」項補進清單即可,不視為設計失效。

## 9. 實作前置:Spike 治理與收尾

### 9.1 Spike 治理模型

對仍依賴平台能力、尚未證實具體接法的項目,本設計**不預先承諾 implementation**。流程:

```text
Formal Design:定義「我們需要建立什麼性質的保證」
      ↓
Bounded capability spike:取得事實——現有 OpenSpec / Harness / Orca / subagent runtime
  提供哪些可機械利用的能力、缺口在哪、最小 adapter 是什麼
      ↓
設計選型(2–3 案):比較 implementation cost / maintenance cost / complexity /
  assurance gain / false-positive 與 false-negative risk / platform coupling /
  fallback 與 degradation behavior
      ↓
Human decision:implement now / simplify / defer / reject
```

Spike 的目標是取得事實,不是直接設計或實作完整方案;選型階段才決定值不值得做、做到哪裡。這保留了「是否值得實作」作為一個有 evidence 的決策點,避免架構一提需求、工程端就自動當成必做功能。

### 9.2 Spike 清單

| # | Spike | 必答題 |
|---|---|---|
| S1 | Scenario identity / coverage extraction | sub-ID 的 OpenSpec 載體;CLI JSON 對 Scenario 的結構;extraction 與交叉核對怎麼做 |
| S2 | Completion Contract overrides + acceptance provenance | proposal 固定語法與機械抽取;**required→degradable override 如何取得可被 Gate 判定的 user-acceptance evidence**(否則接受又成 self-claim) |
| S3 | Assurance defaults 的 schema carrier | schema.yaml 放預設表的形狀 |
| S4 | TDD applicability | applicable 的機械判準;N/A 處置 |
| S5 | 記錄載體 | Result(含 Scenario 指認欄位)/ 降級紀錄 / CONFLICT 更正 / Gate PASS 紀錄的實際載體 |
| S6 | Independent Review 的最小 provenance | 如何以 machine-evaluable 方式識別 review execution 與 implementation execution 的獨立性——不建完整 executor identity framework,先問現有 runtime 是否已提供(如 Orca run metadata);沒有再評估最小 adapter 值不值得 |

### 9.3 Record 處置與 out of scope

**Record 處置**:「TDD 證據契約」→ absorbed(§4.3);「apply 階段交件證據」→ absorbed(§5)。殘餘實作責任(schema 實作、CLAUDE.md 治理語言改寫、spike 執行)轉後續 change。

**v1 必做 / v-next 的界線(與 I3 對齊)**:Scenario identity + Scenario-level Verification coverage 是 **v1 必做**(I3 依賴它,不可延後);v-next 延後的是**更完整的 Scenario traceability**(如 Task→Scenario 對應、更豐富的 dependency / coverage model)。

**明確 out of scope**:`verify.md` 重構(護欄 8)、Diff-aware invalidation 實作(§6 可選層)、完整 executor identity framework(S6 只做最小 provenance 事實調查)、`/to-tickets` 適配細節(獨立工作線,僅受 §3.2 SSOT 約束)。

---

## 附錄:本輪拍板紀錄(2026-09-01)

| # | 題目 | 定案 |
|---|---|---|
| 1 | 設計範圍 | A′:吸收 TDD 證據契約與 apply 交件證據的設計責任;record 依設計/實作責任分流;corrective-fix 例外只入背景 |
| 2 | Contract identity | stable ID,heading 載體,fail-closed,ID immutable,不建 registry |
| 3 | Traceability 粒度 | C′:Task join 到 Requirement;Verification coverage 到 Scenario(sub-ID);Gate 核對兩者 |
| 4 | Freshness | digest 基線 fail-closed(STALE ≠ FAIL)+ Diff-aware optimization 為可選層;自宣告依賴範圍否決 |
| 5 | G1b 偵測分工 | Diff 找標靶 → Reviewer 判語意 → Gate 驗完整性;降級沿 required/degradable,不建 waiver 系統 |
| 6 | 宣告位置 | 兩層宣告 + Effective Completion Contract;放寬 = change-local degradation(理由+接受);Core invariants 不可 override |
| 7 | 段落修訂 | I7 新增、I1 擴及 Scenario、刪萬用 blocker 句、Independent Review 預設 degradable、TDD 限 applicable、executor independence 降為 candidate、Gate PASS freshness、I7 不依賴 Orca、不保證清單擴 G1a 語意漏失、Spike 治理模型 |
