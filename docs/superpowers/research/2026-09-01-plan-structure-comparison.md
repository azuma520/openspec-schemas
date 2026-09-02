# Plan 結構比較:writing-plans vs /to-tickets → Plan Contract

> 2026-09-01 loosen-plan change brainstorming 期間的成熟來源拆解。
> **定位:分析參考,不是規範**——正式拍板以 `openspec/changes/loosen-plan/` 的 change artifacts(brainstorm / design / specs)為準;本文件保存「為什麼這樣判」的推導過程,供未來 schema 調整或其他 bridge 重複使用。
> 方法:兩個 skill 均於 2026-09-01 全文閱讀(superpowers:writing-plans 172 行 SKILL.md、mattpocock-skills /to-tickets 107 行 SKILL.md),非憑摘要或印象。

## 0. 核心判別式(整份比較的一句話版)

> 一條資訊如果編碼的是「**怎麼做**」(步驟、命令、commit 節奏),刪;
> 編碼的是「**什麼算做完、跟誰接、名字叫什麼**」,留。

兩個 skill 不是競爭者,它們防不同的失敗:

| Skill | 防的失敗 | 補償機制 |
|---|---|---|
| superpowers:writing-plans | 執行者太笨(假設零脈絡、品味可疑) | 用微步驟把行為鎖死 |
| mattpocock /to-tickets | 計畫太快過期(假設環境會變) | 只寫不會過期的東西(行為、驗收、依賴) |

Plan Contract = 留下 writing-plans 的**協調用**資訊,把它**控制用**的機制換成 /to-tickets 的契約機制。

## 1. 比較座標系:三個 artifact 的分工

| Artifact | 職責 | 依據 |
|---|---|---|
| design.md | 為什麼這樣蓋:架構、決策、trade-offs | 現行 schema 已如此 |
| tasks.md | **SSOT** 工作清單 + 進度(CLI 機械消費 checkbox);**TDD applicability 標註的家**(2026-09-01 收斂) | SSOT:2026-08-28 拍板 |
| plan.md | 每個 task 的**執行契約**:做到什麼算做完、邊界在哪、跟誰接 | 本輪定義 |

## 2. writing-plans 逐元素判定

它解決的真問題是「執行者零脈絡也能接手」。有價值的是契約性內容,要移除的是步驟性內容:

| # | 元素 | 判定 | 理由 |
|---|---|---|---|
| 1 | Goal 一句話 | 保留 | 契約的開頭 |
| 2 | Spec 指針(executor 讀 plan 也讀 spec) | 保留 | 改指向 change 目錄的 specs/ + design.md |
| 3 | Architecture / Tech Stack 表頭 | 移除 | design.md 的職責,plan 只引用不重抄(重抄必漂移) |
| 4 | Global Constraints(全案約束逐條、原文照抄) | 保留 | 「規定契約」的原型——「必須 MIT」「validate 必須過」住在這 |
| 5 | File Structure(先鎖檔案分工) | 修改 | 單元邊界與責任歸 design.md;plan 不強制列 exact paths |
| 6 | Task Right-Sizing(最小可獨立測試單位、值得一個 reviewer gate、鄰接 task 可分開否決) | 保留 | 粒度判準不是步驟;回答「細到什麼程度才足以交給執行者」 |
| 7 | 2-5 分鐘五步 TDD 微循環 | 移除 | 步驟規範的本體;TDD 改走證據契約(見同日 TDD evidence 分析) |
| 8 | Files: exact path + 行號(必填) | 移除必填 | /to-tickets 的理由成立:stale 最快的就是這個 |
| 9 | Interfaces: Consumes / Produces(跨 task 介面;每個 worker 只看到自己的 task) | 修改後保留 | writing-plans 最有價值的一塊——多 subagent 並行時鄰接 task 靠它對名字和型別。改為「介面契約」:約定名稱與 shape,不強制完整 signature。強度=條件式必填(見 §5) |
| 10 | No Placeholders(禁 TBD /「適當處理錯誤」) | 修改 | 保留「禁模糊語」精神(驗收條件必須可驗);移除「code step 必附 code block」那半 |
| 11 | Self-Review 三檢(spec coverage / placeholder 掃描 / 介面一致性) | 保留 | 契約完整性自檢,跟步驟無關 |
| 12 | Execution Handoff(二選一含 executing-plans) | 移除 | executor 歸 schema apply 段管;executing-plans 本 schema 明文禁 |
| 13 | Commit points(每 task 一 commit) | 移除 | 「分成 N 個 commit」是根 CLAUDE.md 樣例點名要刪的 |

## 3. /to-tickets 原則移植

| # | 原則 | 判定 |
|---|---|---|
| 1 | Tracer-bullet 垂直切片:每單位端到端、獨立可 demo/可驗 | 新增 |
| 2 | 「What it delivers」:從使用者/系統行為視角寫,明文非 layer-by-layer | 新增(每條 plan 條目的第一欄) |
| 3 | Acceptance criteria checkbox | 新增(每 task 必有;**不**掛 REQ-ID 機械追溯——loosen-plan scope 限縮) |
| 4 | Blocked by 顯式依賴邊 | 新增(現行只有「按依賴排序」的隱式版) |
| 5 | 單一 fresh context window 的大小上界 | 新增(併進 Right-Sizing 判準) |
| 6 | 預設不寫 file path / code snippet;例外:encode 決策的 snippet(state machine、schema、type shape)可附 | 新增(「允許但不必填」) |
| 7 | Wide refactor 的 expand–contract 例外 | 不移植(YAGNI;需要時再加) |
| 8 | Quiz user granularity(切完先給使用者審) | 延後——producer 流程,Plan Contract 定案後另議 |

## 4. /to-tickets 作為 producer 的查證結論(2026-09-01)

**成熟參考來源、目前不直接 invoke**;不等於拍板「plan 永久不 invoke skill」。直接 invoke 走不通的四個查證事實:

1. frontmatter `disable-model-invocation: true`——只能使用者親手 slash 觸發;
2. 依賴 `/setup-matt-pocock-skills` 先配 tracker;
3. 輸出載體是 `.scratch/<slug>/issues/` ticket 檔或真 tracker,不是 change 目錄的 plan.md;且正式設計 §9.3 明列 `/to-tickets` 適配細節=獨立工作線、out of scope;
4. 綁它=給所有採用者加新 plugin 依賴(新 PRECHECK 負擔)。

**Producer 選型是 Plan Contract 定案後的獨立議題**(使用者 2026-09-01 定調:不讓 producer 反過來決定 plan 長什麼樣)。候選:writing-plans 續用 / agent direct generation / Harness-native contract-planning skill / /to-tickets 正式適配。

**裁定(2026-09-01,詳見 loosen-plan change brainstorm.md Q4)**:agent direct generation;contract-planning skill 作**有觸發條件**的升級路徑(acceptance 反覆不可驗、boundary/interface/dependency 反覆漏失、reviewer 大量重寫、producer 間品質不穩 → 開 bounded spike 比較);writing-plans 移除 normative dependency 但不禁止當 optional aid;/to-tickets 維持 design reference 不 invoke。residual risk 明寫:機械檢查只托底結構完整性,語意品質仍依賴 producer + Review。

## 5. 兩個結構決策點(brainstorming 中提出,拍板結果見 change artifacts)

- **(a) Interfaces 塊強度**:建議條件式必填(有跨 task 耦合時必填、原子獨立 task 可免)。先例:正式設計 §3.2 方向性規則——Task→Contract 不反向強制,因為「反向強制會逼人硬掰對應、製造假 traceability」;Interfaces 全必填是同一種病。
- **(b) fail-closed 執行落點**:建議雙落點——plan Self-Review(prompt 層,產出時攔、盡力而為)+ verify artifact 機械檢查(archive 前必攔)。宣稱邊界:v1 的 fail-closed 是「archive 前必被機械攔到」,不是「產出當下必被攔到」。verify 加一條編號檢查不算方向文件護欄 8 的「verify.md 重構」(現有結構原封不動),此讀法需經審查驗證。

## 6. 已知連動(實作時的跨檔耦合)

- schema description「TDD arrives via plan.md task content」換軌後不再為真,須改為證據契約說法;
- bridge README 設計觸點、adopters fragment(en + zh-TW)同步;
- plan.md / tasks.md 模板重寫(templates/plan.md 17 行空殼歸本 change,2026-08-27 未決題就此收);
- writing-plans 若自 required skills 移除,schema description 清單與 plan PRECHECK 連動(PRECHECK 隨 invoke 一起移除不屬「拿掉 PRECHECK 沒換替代品」紅旗——替代品是新契約條文本身,需在 design 明寫)。
- plan.md ↔ tasks.md 1:1 對應為手維護,防漂移便宜解:plan 條目標題=tasks.md task 編號,verify 加計數交叉核對。
