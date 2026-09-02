# Session Handoff — 2026-09-02

## Session 07:59

### 一、本 session 主題

loosen-plan change 開工(2026-09-01 晚間起、跨午夜):Q1–Q5 brainstorming 全數拍板,artifacts 4/8(brainstorm / proposal / design / specs 落檔、validate 過),research 分析文檔 ×2 落檔並建索引。

### 二、完成事項

- 開工三步驟:跑 /work-status、讀 9/1 handoff 四個 session 區塊、接力棒 3 條逐條交代、提優先建議 3 條;doctor 唯一警告為 work-map 未知 key `evidence`(前向相容保留、使用者裁示放著)。
- 前置閱讀:正式設計全文、spike 報告全文、現行 schema.yaml + plan/tasks 模板、work-map record。
- 開 change:`openspec/changes/loosen-plan/`(--schema superpowers-bridge),dogfood 副本確認同步。
- **Q1 拍板**:TDD 證據契約與 plan 放寬綁同一 change(同一治理轉換的左右兩半);scope 封閉集四項、其餘 Bridge Guarantee 能力不帶。
- **Q2 拍板**:先定 Plan Contract 再選 producer;writing-plans(172 行)與 /to-tickets(107 行)全文閱讀後做逐元素「保留/修改/移除/新增」比較;(a) Interfaces 條件式必填、(b) fail-closed 雙落點。
- **Q3 拍板**(兩輪修正收斂):TDD Evidence 最小契約——tasks.md 為 applicability SSOT;RED claim 定稿為「同一 subject 曾被執行、因目標行為尚未成立而正確失敗;支持 RED→GREEN 轉變、不支持完整 TDD history」;5 required 欄 + invocation supporting;假 state ref 移除;suite-green 留 change-level;九項明確不做清單。
- **Q4 拍板**:producer = agent direct generation;residual risk 明寫(機械檢查只托底結構完整性、語意品質靠 producer + Review);C(Harness-native skill)留觸發條件明確的升級路徑;writing-plans 移除 normative dependency 不禁止;/to-tickets 吸收不 invoke。
- **Q5 拍板**:schema major 升 2、bundle 2.0.0——主理由 backward compatibility(v1 合法 tasks.md 升級後會被新 verify 擋)、副理由 PRECHECK shape 命中 policy;`version: 2` CLI 全鏈路實測正常(validate/schemas/new/status/instructions)。
- artifacts 落檔:brainstorm.md(Q1–Q5 決策日誌)、proposal.md(經使用者三點收口修訂:fail-closed 宣稱限定、PRECHECK 理由改寫、versioning 拍板)、design.md(D1–D7)、specs ×3(plan-contract ADDED、tdd-evidence-contract ADDED、tdd-claim-accuracy MODIFIED);`openspec validate` 通過。
- research 文檔落檔 + 索引:`docs/superpowers/research/`(plan-structure-comparison + tdd-evidence-analysis + README 索引);CLAUDE.md 結構樹補 poc/ + research/、相關連結加索引行。

### 三、未完事項 / 接力棒

- [#接力] **design.md(D1–D7)+ specs ×3 待使用者核可**——上次呈現重點:SSOT 分工表(不產生第二個 SSOT 的落法)、三 capability 邊界互不侵犯。核可後進 tasks artifact(展開跨檔耦合清單:schema description / 兩 README / adopters fragments / version-check.yml grep / VERSION 2.0.0 / migration guide)。
- [#接力] **doc gate 批清**:本 session 約 10 個 .md 新增/修改未過 /codex-review-doc(見四【紀律接力】)。
- [#接力] 下次 push 順驗 GitHub Actions 是否自動觸發(沿 9/1 session 接力、fork 啟用後首次 push 為最終實測)。
- [#不重議] Q1–Q5 均已拍板、記錄於 change 的 brainstorm.md——後續 artifact 遇同題引用出處照辦,不重提。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] 動工前查已決兩次兌現:「更適合的 skill 參考」靠 grep handoff + 方向文件找回 /to-tickets 綁定表,沒憑印象猜;版本題被使用者攔下「graph 沒變 → non-breaking 推論跳太快」後,查 policy 原文 + 實測 `version: 2` 全鏈路才端決策。
- [#債] **doc gate 未清**:本 session 新增/修改約 10 個 .md(research×3、CLAUDE.md、change artifacts×6),/codex-review-doc 未跑——change artifacts 仍在使用者審閱中、收斂後一批審,**下 session 必清**。

**【當日洞見】**

- [#決策] loosen-plan Q1–Q5 全數拍板(詳 change 的 brainstorm.md):TDD 證據契約與 plan 放寬綁同一 change(同一治理轉換的左右兩半);Plan Contract 先於 producer 選型;TDD 最小證據契約(5 required + invocation supporting);producer = agent direct generation + 觸發式升級路徑;schema major → 2(主理由 backward compatibility、副理由 PRECHECK policy 命中)。
- [#洞見] writing-plans 與 /to-tickets 不是競爭者——防不同的失敗(執行者太笨 vs 計畫太快過期);Plan Contract = 留協調資訊、換控制機制。
- [#洞見] 舊 TDD 保險絲大半是想像的:規定了步驟、驗證了零(apply instruction 自己承認);新制放寬的只有路徑自由度,Harness 可驗證 assurance 是淨升級(宣稱範圍限定至此)。
- [#洞見] spec 釘措辭的反向效應:tdd-claim-accuracy 把「schema 不驗證 TDD」釘成規格——實作升級後不改 spec,規格反而強迫繼續宣稱「沒驗證」。假合規的鏡像案例(spec 比實作弱也會製造 drift)。

**【學習候選】**

沒有——版本題「先查完再分析」是既有全域「能碰就碰／證據先於斷言」的又一例,已有 always-on 載體,不硬造新規則。

### 五、檔案異動

本 session 無新 commit;改動全在 working tree(收工 commit 收入):

| 異動 | 內容 |
|---|---|
| 新增 | `openspec/changes/loosen-plan/`(brainstorm / proposal / design / specs×3) |
| 新增 | `docs/superpowers/research/`(README 索引 + plan-structure-comparison + tdd-evidence-analysis) |
| 修改 | `CLAUDE.md`(結構樹補 poc/ + research/、相關連結加 research 索引行) |
| 修改 | `workflow-harness/work-map.jsonl`(loosen-plan 標 DOING,收工結算) |
| 未進版控 | `2026-08-27-brainstorm-產品承諾.md`(沿慣例) |

錨來源:本 session 開工 commit(fa3ad02、開工於 2026-09-01T15:33:10)——列 fa3ad02..HEAD(無新 commit)

### 六、下一步建議

1. **核可 design + specs → 進 tasks artifact**:tasks 會把跨檔耦合展開成工作項(schema.yaml 各段 / 模板×2 / 兩 README + migration guide / adopters fragments / version-check.yml / VERSION);Q1–Q5 已全拍板、tasks 之後 plan artifact 將是新 Plan Contract 的第一次 dogfood。
2. **doc gate 批清**(research ×3 + CLAUDE.md + change artifacts,一個 /codex-review-doc dispatch)。
3. 下次 push 順驗 Actions 自動觸發(fork 啟用後最終實測)。


## Session 14:01

### 一、本 session 主題

loosen-plan 收斂到 apply 前:design/specs 三缺口拍板落字、tasks(25 步)+ plan(Plan Contract 首次 dogfood)產出並核可、doc gate 三輪(fallback 審)✅ Mergeable、CLAUDE.md 治理段追上 9/1 正式設計。

### 二、完成事項

- 開工三步驟:/work-status、讀 07:59 handoff 接力棒 3 條逐條交代、優先建議 3 條;使用者選「核可 design + specs」。
- design/specs 摘要端出 + 兩個缺口(evidence 載體未指定;「機械檢查」實為 instruction 文字)→ 使用者裁 (a):evidence carrier = tasks.md task checkbox 下(first carrier、非 invariant);「deterministic check ≠ mechanically enforced gate」宣稱全面收斂(proposal/design/specs 五類措辭逐句改);plan↔tasks 改 Task ID 集合雙向差集。
- tasks.md 產出(10 群 24 步 → 25 步含 8.4)、每步帶 `TDD:` 標註(全 n/a、理由不以副檔名為據);使用者三修(4.1 deterministic vs review 判斷分列、n/a 理由改寫、10.2 兩類 grep)落字,同類掃到 spec「Error output is not RED」一併改為 review 判斷。
- plan.md 產出:Plan Contract 首次實戰(header + 25 entries、global constraints 逐字抄 spec、interfaces 條件式、無步驟指令);使用者三確認落字(ID 集合證明 / 四處 diff 措辭改 outcome-boundary / claim boundary 段 + task 10.4 fresh-context smoke test)。
- doc gate:Codex 額度耗盡 → `[REVIEWER_FALLBACK] plane=doc_review from=codex to=contract-neutral-reviewer reason=quota | 2026-09-02T01:43:35Z`(本 change sticky);三輪:R1 ⛔(3🔴 閘門表過期 / 7→4 skill 數 / CLAUDE.md 漏出 sweep;4🟡 2⚪)→ 修 → R2 ✅(舊 digest,新 2🟡 當場修)→ R3 ✅ 現 digest;`[SENTINEL_VALID] contract=doc`、`doc_review pass` 已記。
- CLAUDE.md 兩處(使用者親閱核可):閘門表第二列 YES(2026-09-01)+「解鎖 ≠ 可直接改、逐 change + §9 治理」+ corrective-fix 例外標歷史已失效;紅旗 TDD 子句改「由 tasks.md 標註 + 證據契約承載、與執行器無關」(只改過期子句)。
- research ×2 行數修正(171 / 36,先 `wc -l` 驗)、:78 舊「archive 前必被機械攔到」註記已被 D5 取代;design Risks 補「證據載體未真實使用」「Q4-A 證據薄弱」兩條。
- `openspec validate loosen-plan` 通過;6/8 artifacts(verify / retrospective 待 apply 後)。

### 三、未完事項 / 接力棒

- [#接力] **下 session 開工:先 commit 本 session working tree(11 檔),再 `/opsx:apply loosen-plan`**——設計定稿與實作分兩個 commit;apply 動 `superpowers-bridge/`,是新的 code/doc 審查面。
- [#接力] **Codex independent review 未補**:全套 artifacts + CLAUDE.md 治理段只過 fallback 審;Codex 恢復後補獨立審,補審前不 archive。
- [#接力] **push 順驗 Actions**:本機 main 領先 origin/main 2 commits(fa3ad02、3a153f1)+ 本 session 未 commit;連兩個 session 未兌現。
- [#接力] 方向文件(2026-08-27)仍把 corrective-fix 例外寫成現行——record 不改,是否加一行「已失效、見 CLAUDE.md」指標由使用者定。
- [#不重議] 缺口 1/2、tasks 三修、plan 三確認、doc gate 三 🔴 處置均已拍板,出處在 change 的 design.md / plan.md 與本區塊;apply 時遇同題引用照辦。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] 端出選擇而非結論兌現三次:缺口 1/2 端出三選項、🔴3 端 (a)/(b)、fallback 審結論最前面標明「非 Codex 獨立審、結論打折」——都由使用者裁、沒自己做完只報結果。
- [#正] 一個缺陷=一類缺陷兌現兩次:「7 skills」抓到後掃出 plan 7.4 同病;spec「Error output is not RED」隨 tasks 4.1 同批改。
- [#債] **Codex independent review 未補**:loosen-plan 全套 artifacts + CLAUDE.md 治理段只過 fallback 審(contract-neutral-reviewer 三輪 ✅),schema 契約屬高風險——Codex 額度恢復後 SHALL 補獨立審,補審前不 archive。
- [#債] **fa3ad02 + 3a153f1 + 本 session commit 均未 push**:9/1 handoff 寫「5 commits pushed」但收工 commit 本身沒推;接力棒「push 順驗 Actions」連兩個 session 未兌現。

**【當日洞見】**

- [#決策] design/specs 三處收斂拍板:evidence carrier = tasks.md task checkbox 下(first carrier、非 invariant);「deterministic (machine-evaluable) check ≠ mechanically enforced gate」——v1 規則硬、執行者仍是 verify agent,不宣稱 Harness 不可繞過閘門;plan↔tasks 用 Task ID 集合雙向差集、不用 count。
- [#決策] tasks.md 核可(25 步驟,全 `TDD: n/a`、理由不以副檔名為據);plan.md 為 Plan Contract 首次 dogfood 但**不算 direct-producer 證據**——10.4 fresh-context smoke test 才是 Q4-A 第一個樣本。
- [#決策] 🟡「全 n/a、證據載體未被真實使用」→ 寫進 Risks 放行、不造假 applicable task;第一個有 executable behaviour 的下游 change 才是真 dogfood。
- [#決策] CLAUDE.md 治理段追上 9/1 正式設計:閘門表第二列 YES;「解鎖 ≠ 可直接改」;corrective-fix 例外標歷史已失效;紅旗 TDD 子句改為「由 tasks.md 標註 + 證據契約承載、與執行器無關」(只改過期子句,整條 §5 重寫留登記項)。
- [#洞見] 這輪 doc gate 抓到的三個 🔴 都不是文句問題,而是三種系統病:**過期治理狀態**(CLAUDE.md 沒跟上 handoff 記的決策)、**錯誤依賴數字**(兩張不同清單混算)、**漏掉 spec 點名的 normative surface**(sweep 範圍比 spec 窄 → 假綠)。第三種正是 10.2 兩類 grep 分法要防的。
- [#洞見] 方向文件(2026-08-27)仍把 corrective-fix 例外寫成現行條文——record 不改,但讀者從那裡進來不會知道例外已失效;要不要加一行指標由使用者定。
- [#摩擦] subagent 回報經 teammate message 三次截斷(每次 ~4k 字),Gate 行落在最後永遠被切掉;要求「≤15 行、Gate 單獨末行」才一次到齊。

**【學習候選】**

1. **Case**:9/1 handoff 記「正式設計核可 → 第二個 YES」,但 CLAUDE.md 閘門表仍寫 NO;今天由 fallback reviewer 抓到,不是任何機制。
2. **Candidate Pattern**:handoff【當日洞見】記下的 `[#決策]` 若改變了某個 **always-on 載體**(CLAUDE.md / rules)裡寫死的狀態,該載體要在同一收工同步;只記在 handoff 等於決策活在只載入一次的地方、而過期版本每個 session 都被讀。
3. **Evidence**:一例(本案)+ 全域 CLAUDE.md 既有的「backlog 不會被自動載入、寫在那裡等於沒寫」同型推論 → **Hypothesis**。
4. **Minimum Sufficient Intervention**:不新增規範。掛點寫不出來(誰會發現 CLAUDE.md 沒同步?——只有下一次 doc review 碰巧把 CLAUDE.md 納進批次),依 always-on 規則降級 **Observe**:本條先記在【當日洞見】,第二例出現再談。
5. **Promotion**:Case Memory。

### 五、檔案異動

本 session 無新 commit;改動全在 working tree(本次收工 commit 收入):

| 異動 | 內容 |
|---|---|
| 修改 | `CLAUDE.md`(事件閘門段、紅旗 TDD 子句) |
| 修改 | `openspec/changes/loosen-plan/`:proposal / design / specs×3 |
| 新增 | `openspec/changes/loosen-plan/tasks.md`、`plan.md` |
| 修改 | `docs/superpowers/research/2026-09-01-plan-structure-comparison.md`、`2026-09-01-tdd-evidence-analysis.md` |
| 未進版控 | `2026-08-27-brainstorm-產品承諾.md`(沿慣例) |

錨來源:本 session 開工 commit(3a153f1、開工於 2026-09-02T08:05:18)——列 3a153f1..HEAD(無新 commit)

### 六、下一步建議

1. **commit 本批 → `/opsx:apply loosen-plan`**:25 步依 plan blocked-by 邊執行;apply 是 subagent-driven-development 第一次吃 Plan Contract 而非 micro-step,注意執行者有沒有因為沒步驟而卡住(這本身是 Q4/D3 觀察點)。
2. **Codex 恢復後補 independent review**(artifacts + CLAUDE.md),再談 archive。
3. **push + 驗 Actions**(拖兩個 session 了)。
