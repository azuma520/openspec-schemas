# Bridge Guarantee Capability Spikes(S1–S6)報告與選型拍板

> 2026-09-01 執行。依[正式設計](../../specs/2026-09-01-bridge-guarantee-formal-design.md)§9 治理模型:bounded spike 取事實 → 選型比較(2–3 案)→ 使用者拍板。
> 全部事實來自本機實測(openspec 1.3.1、orca CLI、Python 3.13),非文件推測;實測基底為 PoC fixture 的 scratchpad 副本。
> **本輪總結論(使用者定調)**:「有紀錄」跟「能證明紀錄來源」不是同一件事——S2 / S5 的拍板即為此邊界的落點,正式文件不得宣稱超過實際能力。

## S1:Scenario identity / coverage extraction

**事實**:

- change 層 `openspec show <id> --json --deltas-only` 的 scenario 只含 `rawText`(WHEN/THEN 內文),**標題名不吐**(與 PoC step0 發現 #3 的 Requirement 標題同型)。
- 實測兩種載體都通過 `openspec validate --json`:①Scenario 標題帶 sub-ID(`#### Scenario: REQ-A-S1 happy path`);②body 首行帶 ID(`- **ID** REQ-A-S1`,會直接出現在 CLI JSON `rawText`)。

**選項**:A. 標題載體(與 Requirement ID 同構;需文本抽取+與 CLI JSON scenario 計數交叉核對——PoC 在 Requirement 層已用同招)/ B. body 載體(CLI 直接抽得到;污染 WHEN/THEN、兩層兩套規則)。

**拍板:A — implement**。一致性比省 parser 成本值錢;PoC 已證此路能走。

## S2:Completion Contract overrides + acceptance provenance

**事實**:

- proposal 正文區段不在 CLI JSON(change 層 `show --json` 只吐 deltas)⇒「Completion Contract Overrides」固定區段須文本抽取(固定 heading,同標題抽取一招)。
- OpenSpec CLI 指令全集**無任何 approve/accept 機制**。
- Orca 有 decision gate(`gate-create` / `gate-resolve` / `gate-list`),紀錄機械可讀,但 `--from <handle>` 為**自報身分**——CLI 層無法證明 resolve 者是使用者本人。

**選項**:A. 使用者親手跑指令在 change 目錄寫 acceptance record / B. Orca decision gate(身分自報;Orca 成依賴)/ C. 維持對話核可(self-claim,設計已否決)。

**拍板:A′ — simplify + implement**(使用者修正 A 的宣稱強度):

- v1 使用「使用者明確操作產生的 acceptance record」作為 change-local degradation 的接受紀錄——**但不得宣稱「檔案存在」能機械證明不可偽造的 human provenance**:Agent 同樣具寫檔能力,Gate 最後看到的只是一個檔案。
- v1 保證:**有顯式 acceptance record**。v1 不保證:**這筆紀錄在系統層不可由 Agent 偽造**。
- 強 human provenance 留待未來有可信 runtime/UI actor metadata 時強化;B 保留為 optional enhancement。不為追求完美身分證明造 authentication system,也不過度宣稱 A 解決了 provenance。

**對正式設計 §2.3 必答題的正面回答**:S2 必答題原文為「required→degradable override 如何取得**可被 Gate 判定的** user-acceptance evidence(否則接受又成 self-claim)」。spike 的事實答案是:**現有 runtime(OpenSpec CLI、Orca CLI)無法提供可被 Gate 機械判定的 human provenance**——任何 v1 載體最終都是 Agent 也寫得出的檔案或自報 handle。因此 A′ 不是「已達成必答題的強版」,而是**收斂保證**:Gate 判定的對象從「使用者本人接受」縮為「顯式 acceptance record 存在且格式有效」,真偽 assurance 依賴 review 層(與正式設計 §8#5 Evidence 真偽同一宣稱邊界)。**配套修訂責任**:正式設計 §2.3 該句所隱含的強保證需隨本拍板同步收斂措辭,由後續 change 修訂設計文件(見「後續」),本報告不直接改設計文件。

**未查證**:Orca UI 上由人按的 gate resolve 是否有不同署名(需開 app 實測;若有,B 的身分弱點可能不成立)。

## S3:Assurance defaults 的 schema carrier

**事實**:schema.yaml 加自訂頂層區塊與 artifact 層自訂欄位,`openspec schema validate` **照樣通過**、`openspec schemas` 照常列出。實測加入的區塊:

```yaml
completion_contract:
  assurance_defaults:
    independent_review: degradable
    tdd_evidence: required
```

`schemas --json` 對該 schema 輸出的欄位為 `name` / `description` / `artifacts` / `source` 四鍵(2026-09-01 實測,openspec 1.3.1),**自訂 `completion_contract` 欄位不在其中** ⇒ 自訂欄位不經 CLI 暴露,Gate 直接讀 schema.yaml 檔案。

**選項**:A. schema.yaml 自訂區塊(單一來源、與 schema 同進退;依賴 validate 寬容——upstream 改嚴時每週 version-check CI 用最新版驗會提前發現)/ B. bridge 目錄另放 `completion-contract.yaml`(不碰 schema.yaml;兩個來源要同步)。

**拍板:A — implement**。assurance defaults 本來就是 schema policy,放一起乾淨;upstream 風險由既有 CI 承接,可接受。

## S4:TDD applicability 機械判準

**事實**:tasks.md 與 plan.md 模板現況**零 TDD 欄位**;task 與其觸及檔案無事前對應(「看副檔名推斷」路不存在)。

**選項**:A. 顯式標註(仿 `Contracts:`,如 `- TDD: applicable` / `- TDD: n/a — 純文件`;未標=BLOCK,fail-closed)/ B. 預設全 applicable、僅 n/a 要標(文件型 change 反而更囉嗦)/ C. 語意推斷(self-claim,設計已否決,列出僅為完整)。

**拍板:A — implement**,並在正式設計明講分工:

> TDD applicability annotation 是 **semantic assertion(語意判斷)**,必須受 artifact review;Gate 只機械驗它**存在與格式有效**。

與 G1b 責任三角同構(機器管完整性、Reviewer 管語意正確性),故不是回到 self-claim。

## S5:記錄載體(Result / 降級 / CONFLICT / Gate PASS)

**事實**:PoC 已證 change 目錄放自造 JSON(`verification-results.json`)CLI 完全不干涉(validate/show 只認 proposal.md);archive 搬整個目錄,紀錄自然隨 change 留史。

**選項**:A. change 目錄內約定名 JSON(`verification-results.json` 擴欄位 method/digest/timestamp/scenario 指認 + `degradation-records.json` + `gate-pass.json`)/ B. repo 外 state(仿 sd0x `~/.cache`;不隨 change 歸檔、archive 後查無憑據)。

**拍板:A′ — implement**(使用者補安全邊界):

- change-local JSON 為 Result / degradation / Gate 紀錄的正式**留史載體**(audit records)——歸檔、diff、追歷史照做。
- **但 `gate-pass.json` 不得成為 archive 的 authority**:Agent 也寫得出 `"status": "PASS"`。archive 必須**機械確認 current Gate PASS / freshness**(呼叫 Gate 或驗當下 state,條件真的全部成立才放行),不能只因可寫入檔案聲稱 PASS 就放行。此界線與正式設計 §7「Gate PASS 自身 freshness」「archive 第二道保險是 current valid Gate PASS exists,不是 PASS record exists」一致——本拍板將其落到載體層:**檔案是稽核紀錄,不是通行證**。

**CONFLICT 更正的載體與語意**(§9.2 S5 明列項,補齊):

- 每筆 Verification Result 帶 stable `id`(檔內唯一即可,不建 registry)。
- 更正紀錄與 Result 同檔(`verification-results.json`,append-only):`{ "type": "invalidation", "target": "<result-id>", "reason": "<必填>", "timestamp": "<ISO8601>" }`。缺 `reason` 或 `target` dangling → 格式無效,Gate fail-closed。
- **Gate 讀法**:被有效 invalidation 指到的 Result 不再參與 CONFLICT 判定與 Complete 支撐;原 Result 與 invalidation 都不刪除(留稽核歷史)。這是正式設計 §6「有紀錄地標 invalid 附 reason」的載體落點。
- invalidation 本身同樣是 Agent 寫得出的檔案——真偽依賴 review 層,與上條 Gate PASS 同一宣稱邊界,不另立防偽機制。

## S6:Independent Review 的最小 provenance

**事實**:

- Orca **supervised worker**(`orchestration worker-start`)由 Orca 親自開終端機並綁 dispatch 紀錄;`worker-show` 說明文明載「A Dispatch created by orchestration dispatch is shown as unsupervised and reports the exact adopted terminal when its identity is still provable」——runtime **已有「可證明的執行者身分」概念**,supervised 與 unsupervised 有別。
- **實際欄位實測**(2026-09-01,`orca orchestration worker-list --json` 讀本機既有 worker 紀錄):每筆 supervised dispatch 帶 runtime 自發的 `dispatchId` / `taskId` / `runId` / `agentTerminalHandle` / `workerState` / `dispatchStatus`,及 `resource.worktreeId` / `originDispatchId` / `ownerDispatchId` / `ownershipState`。這些 ID 由 Orca 核發、非 agent 自填。
- **獨立性判定規則(機械可判)**:review dispatch 與 implementation dispatch 為**兩筆 dispatch 紀錄,`dispatchId` 與 `agentTerminalHandle` 相異**(可加驗 `resource.worktreeId` 相異)即為不同執行 context——證據為 Orca 核發的紀錄本身,非 self-claim。
- 自由填的 `--from <handle>` 為自報;Claude Code subagent 執行後**無任何留存的機械紀錄**(只在對話)。

**選項**:A. 採認 Orca supervised dispatch 紀錄為獨立性證據;無 Orca 或非 supervised ⇒ 依 G3 降級(self-review + degradation record)/ B. 自建最小 adapter(executor 指紋由 agent 自寫——又是 self-claim,白做)。

**拍板:A — implement**。與既有架構完全對齊:有 Orca → assurance 強一點;沒 Orca → Core Harness 繼續運作、independence 降級;該 change 明寫 Independent Review = required 且無可信 provenance → BLOCK。Orca 仍非 hard dependency。

**實作前最後確認(不影響選型)**:欄位形狀已於本輪以既有紀錄實測(上表);實作該能力前僅需確認欄位在屆時 Orca 版本仍穩定,並對「同 session 先後扮演兩角」的邊界個案(同 terminal 兩次 dispatch)定 Gate 讀法。

## 拍板總表(2026-09-01)

| Spike | 拍板 | 關鍵限定 |
|---|---|---|
| S1 | A — implement | 標題載體+文本抽取+CLI 交叉核對 |
| S2 | A′ — simplify + implement | 保證「有顯式 record」,不保證「不可偽造」;B 留 optional |
| S3 | A — implement | Gate 直讀 schema.yaml;upstream 風險由 version-check CI 承接 |
| S4 | A — implement | annotation 是 semantic assertion,受 artifact review;Gate 只驗存在+格式 |
| S5 | A′ — implement | JSON 是稽核紀錄不是通行證;archive 機械確認 current Gate PASS |
| S6 | A — implement | 欄位已實測(dispatchId/terminalHandle 相異即獨立);無可信 provenance 依 G3 降級 |

## 後續

- 實作逐塊走各自的 OpenSpec change 流程(事件閘門雙 YES 已成立,但不因此直接動 schema.yaml)。
- **正式設計 §2.3 措辭收斂**(隨 S2 拍板產生的修訂責任):該節 acceptance provenance 的隱含強保證,需收斂為本報告 S2 的弱保證版(保證「有顯式 record」、不保證「不可偽造」),由後續修訂設計文件的 change 處理,可與既有 9 筆 deferred findings 同批收。
- 本報告餘下的「未查證」(S2 Orca UI 署名)掛在對應實作 change 的前置確認,不另開 spike。
