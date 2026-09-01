# Session Handoff — 2026-09-01

## Session 09:00

### 一、本 session 主題

開工 stub(沿 2026-08-31 使用者拍板前例:今日 handoff 不存在時先建檔讓 Stop hook 安靜):本 session 實際主題為 bridge guarantee 正式設計 brainstorming,正式區塊待收工 `/end-session` append。

### 二、完成事項

- 開工三步驟:跑 /work-status、讀 8/31 handoff 三個 session 區塊、逐條交代接力棒 3 條並提優先建議。
- 週一 backlog 週檢:8/31 Session 15:38 已執行(0 候選、無事可清),本 session 不重跑。
- 接力棒 #2 收掉:查證 fork Actions 已啟用(workflows state=active、使用者截圖確認無 enable 橫幅),之後 push 會自動觸發 CI。
- 正式設計 brainstorming 進行中(六題釐清已拍板,分段呈現進行中)。

### 三、未完事項 / 接力棒

- [#接力] 正式設計分段核可未完成;收工時走 `/end-session` append 正式區塊,本 stub 不取代收工流程。

### 四、洞見 / 反省

**【紀律接力】**

- (待收工補;實際工作進行中)

**【當日洞見】**

- (待收工補)

### 五、檔案異動

- 本檔(新建 stub)。

### 六、下一步建議

- 續完成正式設計分段核可 → 落檔 `docs/superpowers/specs/` → 自審 + doc 審查義務 → 使用者審。


## Session 10:46

### 一、本 session 主題

bridge guarantee 正式設計——六題釐清逐題拍板 → 九段分段核可 → 落檔 + 自審 → doc 審查(Codex 斷供第 7 次,fallback ✅ Mergeable)→ 事件閘門第二 YES。

### 二、完成事項

- 接力棒 #2 收掉:查證 fork Actions 已啟用(workflows state=active、使用者截圖確認無 enable 橫幅);「過去 push 無 CI」最合理解釋為停用期事件被丟棄,下次 push 為最終實測。
- 正式設計 brainstorming(architectural 路徑):六題釐清全數拍板——A′ 範圍(吸收 TDD 證據契約 + apply 交件證據的設計責任)/ stable ID(heading 載體、fail-closed)/ C′ 粒度(Task→Requirement、Verification→Scenario)/ freshness 兩層(digest 基線 + Diff 優化層)/ G1b 責任三角(Diff→Reviewer→Gate)/ 兩層宣告 + Effective Completion Contract(core invariants 不可 override)。
- 九段設計分段核可(含使用者四項修訂:Gate PASS 自身 freshness、I7 不依賴 Orca、不保證清單擴 G1a 語意漏失、spike 治理模型)。
- 落檔 `docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`(~240 行,含 I1–I7、assurance v1 預設表、S1–S6 spike 清單、拍板紀錄附錄);自審修 2 處(4.1 編號、「必要 Scenario」v1 預設)。
- doc 審查:Codex 額度斷(第 7 次)→ fallback contract-neutral-reviewer(首用)→ ✅ Mergeable 零 🔴、6 🟡 + 3 ⚪ 全 deferred;sentinel 驗證通過、note doc_review pass。
- 使用者核可設計 = **事件閘門第二個 YES**(2026-09-01)。
- 結算:`task-20260831-formal-design` / `task-20260826-tdd-evidence-contract` / `task-20260827-apply-degradation-boundary` 標 DONE(證據:設計文件 + 本 session 核可 + doc review PASS;後兩條為 A′ absorbed 處置);新開 `task-20260901-guarantee-spikes`(標 NEXT)與 `task-20260901-reqpb-exception-delta`。

### 三、未完事項 / 接力棒

- [#接力] **capability spikes(S1–S6)+ 選型**(record 已標 NEXT):依設計 §9 治理——spike 取事實 → 選型比較 → 使用者拍板 implement/simplify/defer/reject;S2(acceptance provenance)與 S6(reviewer provenance)最關鍵。
- [#接力] **REQ-PB 例外補小 delta**(record `task-20260901-reqpb-exception-delta`)。
- [#接力] **9 筆 deferred findings** 下次動設計文件時順手收(優先:G3 attribution 措辭、I6「blocking」未定義)。
- [#不重議] 事件閘門雙 YES 已成立,但 schema 實作仍逐塊走 opsx change + 設計 §9 spike 治理,不因解鎖而直接動 schema.yaml。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] **Codex 額度中斷第 7 次、fallback 鏈續走且首次啟用 contract-neutral-reviewer**:`[REVIEWER_FALLBACK]` → 代審 → `validate-family-sentinel.js doc` 驗證 → ✅ Mergeable 收案、`note doc_review pass`;9 筆 sub-threshold 依規則記錄放行、不開修正輪。

**【當日洞見】**

- [#決策] **事件閘門第二個 YES 成立**(正式設計核可,2026-09-01):schema 實作解鎖,但依設計 §9 治理——先 spike 取事實、再選型、再由使用者拍板 implement/simplify/defer/reject,不自動視為必做。
- [#洞見] **fork Actions 之謎收案**:workflows state=active、頁面無 enable 橫幅——「過去 35 筆 push 無 CI」最合理解釋是停用期間 push 事件被丟棄、事後啟用不補跑;下次 push 是最終實測。
- [#洞見] **審查攔下 provenance 漂移**:設計把本輪新增的「required→degradable 經重新核可」出口寫成「G3 已定」——把擴充寫成引用,會讓後人以為舊決策本來就含這個口子。已 defer 待下次動該文件時修。

**【學習候選】**

- **Case**:設計文件引用方向文件 G3 時,把本輪才拍板的例外出口寫成「G3 已定」,被外部審查標出(🟡)。
- **Candidate Pattern**:設計文件重述舊決策時,「引用」與「本輪擴充」必須分開措辭;凡寫「X 已定」前,回原文確認 X 真的含這句。邊界:僅適用有上游決策文件的設計寫作;全新決策不適用。
- **Evidence**:1 例(2026-09-01)。**Hypothesis**。與全域「修正絕對句要再過例外檢查」同族(措辭動作本身製造新宣稱)但載體不同。
- **Minimum Sufficient Intervention**:先觀察,不新增規範(寫不出可靠掛點;外部審查本次已攔住,現有補償層有效)。
- **Promotion**:History only。

### 五、檔案異動

| 異動 | 內容 |
|---|---|
| 新增 | `docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`(正式設計,~240 行) |
| 修改 | `workflow-harness/work-map.jsonl`(3 標 DONE、2 新增、1 標 NEXT) |
| 新增+append | 本 handoff(開工 stub + 本區塊) |
| 未進版控 | `2026-08-27-brainstorm-產品承諾.md`(沿慣例) |

錨來源:本 session 開工 commit(aa7182d、開工於 2026-08-31T16:00:18)——列 aa7182d..HEAD(本 session 無新 commit,異動全在 working tree,收工 commit 收入)

### 六、下一步建議

1. **capability spikes(S1–S6)+ 選型**(record 已標 NEXT):S2 acceptance provenance 與 S6 reviewer provenance 最關鍵——它們決定 assurance 模型能不能被 Gate 真的判定。
2. **REQ-PB 例外補小 delta**(獨立小 change,record 已開)。
3. **push 後看 Actions 是否自動觸發**(fork Actions 之謎的最終實測)。


## Session 14:55

### 一、本 session 主題

bridge guarantee capability spikes S1–S6:取事實 → 選型比較 → 使用者六項拍板 → 報告落檔 + doc 審查兩輪(4 🔴 修畢)✅ Mergeable → 獨立 commit 收案(bd71f3a)。

### 二、完成事項

- 開工三步驟:跑 /work-status、讀 9/1 handoff 兩個 session 區塊、接力棒 3 條逐條交代、提優先建議 3 條。
- S1–S6 spikes 全數完成(全部本機實測、非文件推測):S1 Scenario 標題/body 兩載體都過 validate、CLI JSON 只吐 rawText;S2 OpenSpec 無 approve 機制、Orca gate 身分自報;S3 schema.yaml 自訂區塊過 validate、schemas --json 四鍵不含自訂欄位;S4 模板零 TDD 欄位、顯式標註是唯一機械載體;S5 change 目錄自造 JSON 可行;S6 orca worker-list 實測拿到 runtime 核發的 dispatchId/terminalHandle 等全部欄位。
- 使用者六項拍板:S1-A / S2-A′(保證「有顯式 record」、不保證「不可偽造」)/ S3-A / S4-A(annotation 是 semantic assertion、受 artifact review)/ S5-A′(gate-pass.json 是稽核紀錄不是通行證、archive 機械確認 current Gate PASS)/ S6-A(dispatchId+terminalHandle 相異即獨立)。
- doc 審查:Codex 額度恢復(第 7 次中斷後首次正常代審)。首輪 4 🔴 全有效——schemas --json 欄位宣稱錯、S2 與正式設計 §2.3 矛盾、CONFLICT 更正載體漏答、S6 拍板早於欄位事實;逐筆修正(含當場唯讀實測 worker-list 補欄位)後二輪 ✅ Mergeable、2 筆 🟡/⚪ deferred。
- 收案:spike 報告 + record DONE 獨立 commit bd71f3a;task-20260901-guarantee-spikes 標 DONE 附證據。
- 結算決策(使用者拍板):REQ-PB delta 降級 deferred spec cleanup 併 claudemd-governance-rewrite 批(spec 無 runtime 消費者、例外唯一適用案已 archive 且雙 YES 後例外失效);loosen-plan 標 NEXT(Formal Design/Spike 結論第一個落地與 dogfood);新登記 task-20260901-design-223-convergence(TODO、掛主線)。

### 三、未完事項 / 接力棒

- [#接力] **plan 放寬(record 已標 NEXT)**:規定契約取代規定步驟,作為 Formal Design + spike 拍板的第一個實際落地與 dogfood;TDD 硬約束以「證據要求」形式保留(S4 拍板的顯式標註 + §4.3 RED/GREEN 證據契約)。
- [#接力] **正式設計 §2.3 措辭收斂**(task-20260901-design-223-convergence、TODO):收斂為 S2 弱保證版,可與 9 筆 deferred findings 同批收(另加本輪 2 筆:實測憑據可重現性、中英排版)。
- [#接力] brainstorming 三路徑漂移留作下一個獨立小修;REQ-PB delta deferred 併 governance-rewrite 批、不插主線。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] Codex 額度恢復(第 7 次中斷後首次正常代審):spike 報告首輪 4 筆 🔴 全部有效、修正後二輪 ✅ Mergeable——外部審查再次攔下自查沒抓到的事實錯誤與設計矛盾。

**【當日洞見】**

- [#決策] Capability spikes S1–S6 完成 + 六項選型拍板,核心邊界為使用者定調的「**有紀錄 ≠ 能證明紀錄來源**」(S2 acceptance、S5 Gate PASS 同族)——v1 保證「有顯式 record」,不保證「系統層不可偽造」,正式文件不得宣稱超過能力。
- [#反省] **截斷輸出釀事實錯誤**:查 `schemas --json` 只看 head 截斷的前 800 字元就寫成「只吐 name/description」,審查抓出實有四鍵。結論(自訂欄位不暴露)沒錯、宣稱錯——「窮舉查完才宣告」的既有病,這次載體是自己加的輸出截斷。
- [#洞見] **審查逼出當場實測,成本比預期低**:S6 原把欄位驗證留到實作前,審查依 §9.1「先取事實再選型」打回;當場唯讀實測 worker-list --json 十分鐘拿到全部欄位。「先拍板、之後再驗」省的時間其實很少。

**【學習候選】**

- **Case**:用 head 截斷 JSON 輸出後,對「輸出裡有哪些欄位」做了全稱宣告,被外部審查證偽。
- **Candidate Pattern**:對機器輸出做「有/沒有某欄位」的宣稱前,必須 parse 完整輸出取 keys,不得以截斷片段推斷。邊界:僅適用「宣稱輸出結構」的場景;截斷用於省 context 讀內文不受限。
- **Evidence**:1 例(2026-09-01)。**Hypothesis**。與全域「窮舉查完才宣告沒有」同族、新載體(自加截斷)。
- **Minimum Sufficient Intervention**:先觀察不新增規範(寫不出可靠掛點;外部審查本次已攔住)。
- **Promotion**:History only。

### 五、檔案異動

| 異動 | 內容 |
|---|---|
| commit bd71f3a | `docs/superpowers/poc/2026-09-01-capability-spikes/spike-report.md`(新增)+ `workflow-harness/work-map.jsonl`(spikes record DONE) |
| working tree | `workflow-harness/work-map.jsonl`(loosen-plan 標 NEXT、design-223-convergence 新增、REQ-PB 加註 deferred)+ 本 handoff append |
| 未進版控 | `2026-08-27-brainstorm-產品承諾.md`(沿慣例) |

錨來源:本 session 開工 commit(8636440、開工於 2026-09-01T11:02:51)——列 8636440..HEAD

### 六、下一步建議

1. **plan 放寬**(record 已標 NEXT):走 opsx change,依 spike 拍板落地——「規定證據不規定步驟」主軸的正體。
2. **§2.3 措辭收斂 + deferred findings 批**(task-20260901-design-223-convergence):動設計文件時一批收 11 筆。
3. **push 後看 Actions 是否自動觸發**(fork Actions 之謎最終實測;本 session 已有 commit 待 push)。


## Session 15:28

### 一、本 session 主題

push 5 筆 commit 上 main(/push-ci 完整流程)+ fork Actions 之謎破案(fork 專屬啟用按鈕未按,已啟用並 dispatch 驗證綠)。

### 二、完成事項

- 開工三步驟:跑 /work-status、讀 9/1 handoff 三個 session 區塊、接力棒 3 條逐條交代、提優先建議 3 條。
- doc gate 清完:上 session 收工 append 的 handoff 區塊經 Codex 代審(implementation-sync profile)✅ Mergeable、零 🔴、1 🟡 deferred(terminalHandle 欄位名,handoff append-only 不回改)、note doc_review pass。
- push:走 /push-ci 完整流程(Phase 0 preflight → 保護分支預核准 → 計畫核准 → SHA/目的地 digest 綁定執行),dca5c5d..1b3606a 5 筆 commit 上 origin/main。
- fork Actions 之謎破案:push 後 CI 仍未觸發,查出唯一 run 的 event 是 workflow_dispatch(手動)、證偽「已啟用」假說;使用者開網頁找到 fork 專屬橫幅「Workflows aren't being run on this forked repository」並按下啟用;手動 dispatch Validate schemas 驗證 1b3606a → success(15s)。
- 向使用者白話解說 CI 機制、fork 停用規則、本次解決的問題。

### 三、未完事項 / 接力棒

- [#接力] **plan 放寬**(record 已標 NEXT):下個 session 主題(使用者已指定)。
- [#接力] push 自動觸發尚未實測(啟用後還沒有新 push);下次 push 自然驗證,不必特地推。
- [#接力] Weekly upstream version check 在 fork 上仍 Disabled(排程類要單獨啟用),要不要開由使用者決定。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] push 走 /push-ci 完整流程(保護分支預核准 + 計畫核准 + SHA/目的地 digest 綁定),doc gate 先清再推。
- [#反省] 本 session 多步驟工作(push 流程 + CI 追查)未建 TaskCreate 管制——違反 Guardrail A4,下不為例。

**【當日洞見】**

- [#決策] **fork Actions 之謎真因確定並解決**:GitHub 對「fork 時帶 workflow 檔」的 repo 預設停用 Actions,啟用開關只存在於網頁 Actions 頁橫幅,**API 層(state=active、enabled=true)完全讀不到這一層**——前兩個 session 據 API 判「已啟用」皆為誤判。使用者按下按鈕後已啟用;手動 dispatch 驗證 1b3606a ✅ success(15s)。
- [#洞見] 破案關鍵是 gh run list 的 **event 欄位**:唯一一筆 run 是 workflow_dispatch 不是 push,直接證偽「push 曾觸發過」——查「有沒有跑」不夠,要查「被什麼觸發」。
- [#洞見] 排程類 workflow(Weekly upstream version check)在 fork 上要**另外單獨啟用**,主開關不連動,目前仍 Disabled(待使用者決定)。

**【學習候選】**

- **Case**:連續三個 session 用 API(gh api workflows、actions/permissions)判定 fork Actions「已啟用」,實際的 fork 專屬開關只在網頁 UI 有,API 讀不到,誤判兩輪。
- **Candidate Pattern**:宣告某平台功能「已啟用/已設定」前,若存在「UI 專屬狀態層」(API 讀不到的開關),必須以**該功能的實際行為**(這裡:push 是否真的產生 run)驗證,不得以 API 設定值代替行為證據。邊界:僅適用「設定宣稱」場景;API 與行為一致的平台不受限。
- **Evidence**:1 案(跨 3 session、同一誤判重複 2 次)。與全域「證據先於斷言」「能碰就碰」同族,新載體(API/UI 狀態分層)。**Hypothesis**。
- **Minimum Sufficient Intervention**:先觀察不新增規範(掛點寫不出——沒有機制能列舉「哪些平台有 UI 專屬層」;本次由使用者開網頁攔住,行為驗證這步已因「下次 push 自然實測」內建)。
- **Promotion**:History only。

### 五、檔案異動

- 本 session 無新 commit(工作為推送既有 commit + GitHub 側啟用操作);本 handoff append 為唯一本地檔案改動。
- 遠端:origin/main dca5c5d → 1b3606a(5 筆 commit 上線);GitHub Actions 已啟用;Validate schemas run #2(workflow_dispatch、1b3606a、success)。
- 未進版控:2026-08-27-brainstorm-產品承諾.md(沿慣例)。

錨來源:本 session 開工 commit(1b3606a、開工於 2026-09-01T14:57:21)——列 1b3606a..HEAD(無新 commit)

### 六、下一步建議

1. **plan 放寬**(record 已標 NEXT、使用者已指定為下個 session 主題):走 opsx change,依 Formal Design + spike 拍板落地「規定證據不規定步驟」;TDD 以證據要求形式保留。
2. 下次 push 順看 Actions 是否自動觸發(啟用後的最終實測)。
3. Weekly upstream version check 仍 Disabled,要啟用去 Actions 頁點該 workflow enable(一鍵,由使用者決定)。
