# Brainstorm — loosen-plan(2026-09-01 起)

> Raw capture:brainstorming 對話的決策日誌。分類:**architectural**(動 schema 行為契約、採用者依賴的介面)。
> 背景輸入:[正式設計](../../../docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md)(事件閘門雙 YES 已成立)、[spike 報告](../../../docs/superpowers/poc/2026-09-01-capability-spikes/spike-report.md)(S4 TDD 標註拍板)、work-map record `task-20260826-loosen-plan`(「把 plan.md 從 2-5 分鐘微步驟改成目標/邊界/介面/驗收契約。依賴 TDD 證據契約先成立,否則放寬等於拆保險絲」)。
> 深度分析已落獨立參考文檔(見 [research 索引](../../../docs/superpowers/research/README.md)),本檔記決策鏈與拍板結果。

## 主軸

> 模型擁有路徑,harness 擁有證據和不可逾越的邊界。
> 判準:如果兩個優秀的 agent 可以用不同做法、最後都符合規格,那計畫就不該提前替它們選一個。

## Q1:TDD 證據契約要不要包在本 change?

**拍板:A — 包在一起,scope 嚴格限縮**(使用者,2026-09-01)。

理由(使用者原話要旨):兩者是**同一個治理轉換的左右兩半**,不只是碰到同一個檔案——plan 用 micro-step 綁住行為、TDD 主要靠這種步驟規範存在;改成 TDD annotation + RED/GREEN Evidence 後,品質控制從「規定怎麼做」轉成「規定要證明什麼」。拆兩個 change 會出現 TDD 無落點空窗(先 loosen)或同段 instruction 改兩次(先 TDD)。A = 一次完整換軌:舊保險絲拆掉的同時,新保險絲裝上。

**Scope 封閉集(只包這四項)**:plan 放寬 + `TDD: applicable / n/a` 標註 + applicable task 的 RED/GREEN evidence requirement + 缺標註或缺必要 evidence 時 fail-closed。**明確不帶**:Scenario traceability、full Gate lifecycle、reviewer provenance、Diff freshness。

## Q2(重拆):先定 Plan Contract,producer 選型延後

原 Q2 問「還要不要 invoke writing-plans」,使用者往前拆一層:**先定義 Plan Contract(plan 負責什麼、包含什麼、不包含什麼),producer(誰產生 plan)是定案後的選型——不讓 producer 反過來決定 plan 長什麼樣。**

### Q2a:/to-tickets 查證(2026-09-01,全文閱讀)

**結論:成熟參考來源、目前不直接 invoke;不等於拍板 plan 永久不 invoke skill。** 其 ticket 契約形狀(end-to-end 行為、acceptance criteria、blocked-by、明文避免 file path/code snippet)與我們要的高度同構;但 `disable-model-invocation: true`、依賴 setup、輸出載體不合、會增採用者依賴——四個事實擋掉直接 invoke。細節:research/2026-09-01-plan-structure-comparison.md §4。

### Q2b:Plan Contract 結構比較(逐元素「保留/修改/移除/新增」)

writing-plans 13 元素 + /to-tickets 8 原則的完整判定表:research/2026-09-01-plan-structure-comparison.md §2–3。核心判別式:**編碼「怎麼做」的刪(微步驟、exact path 必填、commit points、execution handoff);編碼「什麼算做完、跟誰接」的留(Goal、Global Constraints、Task Right-Sizing、Interfaces、Self-Review)+ 移植 /to-tickets 契約機制(垂直切片、行為視角、acceptance criteria、顯式依賴邊、context window 上界、預設不寫易 stale 細節)。**

比較座標系(artifact 分工):design.md = 為什麼這樣蓋;tasks.md = SSOT 清單 + 進度 + **TDD 標註的家**;plan.md = 每 task 的執行契約。

**兩個結構決策點(使用者 2026-09-01「整體收斂接受」)**:

- **(a) Interfaces 條件式必填**:有跨 task 耦合時必填、原子獨立 task 可免。先例:正式設計 §3.2「反向強制會逼人硬掰對應」。
- **(b) fail-closed 雙落點**:plan Self-Review(prompt 層,產出時攔、盡力而為)+ verify artifact 機械檢查(archive 前必攔)。宣稱邊界:v1 fail-closed 是「archive 前必被機械攔到」,不是「產出當下必被攔到」。verify 加編號檢查不算護欄 8 的「verify.md 重構」(此讀法留給審查驗證)。

## Q3:TDD Evidence 契約(從成熟 skill 反推,不從欄位開始設計)

方法論(使用者定調):先回答「想證明什麼」,再談欄位;能機械判斷的不交給模型猜。完整分析(程序拆解、三類分類、有效性判準、機械/review 分工):research/2026-09-01-tdd-evidence-analysis.md。

**拍板結果(2026-09-01,經使用者兩輪修正收斂)**:

1. **TDD procedure 由成熟 Skill 負責**(主要參考 superpowers:test-driven-development),不搬進 Harness。
2. **Verify RED / Verify GREEN 是唯二 Evidence 化節點**;test-first 時序、minimal implementation、refactor 留在 procedure/review 層。
3. **RED claim(定稿措辭)**:同一 verification subject 曾被執行,並因目標行為尚未成立而正確失敗;支持 RED→GREEN 狀態轉變,不支持完整 TDD history。(不寫「在某 artifact state 下」——本 change 不做 state identity。)
4. **有效 RED = behavioral failure**,SyntaxError/import error/dependency error/harness error 不算(設計依據:skill 的 Verify RED 條件)。
5. **RED↔GREEN subject 同一性**是機械可驗的承重接點。
6. **最小 Evidence Contract**:required 五欄(RED: subject/outcome/failure output;GREEN: subject/outcome)+ supporting 一欄(invocation——reproducibility 用,useful 不升格 required)。
7. **假 state ref 移除**:不能區分狀態的欄位是假裝在保證;「未來綁 digest」記為方向。
8. **suite-green 留 change-level**(有意識偏離 skill 原文:per-task 證據要最小)。
9. **明確不做**:完整時序 provenance/不可偽造 Evidence/Harness 自動捕獲/完整 JSON schema/executor identity/每步 procedure evidence/per-task full regression/測試品質機械評分/正式 digest·freshness——全記為 Gate 強化路徑。
10. **宣稱範圍限定**:「淨升級」只指 **Harness 可驗證 assurance**(舊制驗證了零→新制機械四條+review 四條);不宣稱能證明 Evidence 真偽或 test-first history。最弱情境(self-review + 事後補造)穿得過,設計文件必須明寫(S6/Gate 職責,非本 change)。

## 已知連動(進 tasks 的跨檔耦合)

schema description「TDD arrives via plan.md task content」須改為證據契約說法;bridge README 設計觸點 + adopters fragment(en/zh-TW)同步;templates/plan.md 與 tasks.md 重寫(2026-08-27「plan.md 17 行空殼歸誰」未決題就此收);writing-plans 若移出 required skills,description 清單與 plan PRECHECK 連動(PRECHECK 隨 invoke 移除,替代品=新契約條文,design 明寫非紅旗);plan↔tasks 1:1 防漂:plan 條目標題=task 編號 + verify 計數交叉核對。

## Q4:Producer 選型(2026-09-01 拍板)

**拍板:A(agent direct generation),C 作有觸發條件的升級路徑,D 維持 §9.3 獨立工作線,B 淘汰。**

**A 的 v1 假設(使用者定稿)**:Plan Contract 已足夠明確,先驗證 Agent 是否能直接從 tasks.md + design/spec 穩定產生合格 Plan;在證據顯示需要前,不新增 Procedure Skill dependency。性質變化:舊制是 skill 決定 plan 怎麼寫、我們跟著它的 microsteps;新制是我們先定好契約與填寫規則,agent 把已知資訊(task 要完成什麼、design 的架構邊界、spec 的需求、tasks.md 的 TDD policy)填進表格——「填好已定義清楚的表格」與「教 agent 規劃複雜軟體」不是同一件事。

**A 的 residual risk(使用者修正,不得說滿)**:雙落點機械檢查只托底**可機械檢查的 contract completeness**(task coverage、必要欄位、TDD annotation/evidence 存在與格式);Plan 的**語意品質**——outcome 是否具體、acceptance 是否真的可驗、boundary/interface 是否正確——仍依賴 producer 品質 + Review。「Acceptance: 登入功能正常」這種爛 plan 形式上全過、機器挑不出來。分層:Plan Contract 規定該提供哪些資訊 → agent 產內容 → 機械 Verify 抓結構問題 → Review 判內容是否清楚、可驗、沒亂寫。

**C 的升級 trigger(現在留下,不是模糊的「以後再說」)**:dogfood / review 反覆出現以下任一——acceptance 模糊不可驗、task boundary 經常錯、interfaces/dependencies 經常漏、reviewer 每次需大量重寫 plan、不同 producer 品質差異過大 → 即為「Plan Contract 不足以穩定引導 producer」的證據 → 開 bounded spike 比較 direct generation vs Harness-native contract-planning skill,再決定是否升為標準 producer(§9 spike 治理)。

**writing-plans 的處置**:**移除 normative dependency 與 PRECHECK,但不禁止**——executor 遇到複雜 task 自認需要更細 decomposition 時,可自行把它當 optional planning aid;但它產生的 microsteps 不能反過來定義 plan.md 的法定格式。

**/to-tickets 的處置**:維持 Plan Contract 的 **design reference**(其 end-to-end outcome / acceptance criteria / dependency / avoid-stale 原則已被吸收進契約),不形成 runtime/plugin dependency。不是「沒用了」,是「不 invoke 它」。

**設計哲學句(使用者原話)**:不要因為擔心 Agent 可能做不好,就預先把路徑全部鎖死;先把成功條件與邊界定清楚,再用實際證據決定需不需要更多程序控制。

## Q5:Schema versioning(2026-09-01 拍板)

**拍板:schema major 升 2,bundle 依既有 policy 進 2.0.0。**

**主要 breaking fact(使用者定調的主次順序,design 必須照此寫)**:v2 引入新的 normative Plan/TDD contract,使部分原本合法的 v1 change(tasks.md 無 TDD 標註)在未 migration 前無法通過新版 verification——「以前合法的東西,升級之後變成不合法」即是 breaking 的定義,這條獨立成立、與 PRECHECK 之辨無關。**次要因素**:plan PRECHECK 移除命中 README Versioning policy 字面(PRECHECK shape 屬 schema major 材料)。**不採**「維持 v1 並修改 policy」——那是為了讓本次 change 看起來 non-breaking 而重定義 breaking,且破壞 v1.x compatibility promise。

**技術風險已實測排除**(2026-09-01,openspec 1.3.1,scratchpad 隔離專案):`version: 2` 下 validate / schemas / new change / status / instructions 全鏈路正常;CLI 對 version 欄位無特殊行為。

**Design 須納入**:最小 v1→v2 migration path(補 tasks.md 標註 → applicable task 補 evidence → plan.md 遷至新 shape → writing-plans 不再是 required dependency)、compatibility 表 v2 列、version-check.yml grep 連動;**不延伸其他 migration framework**。

**觀感註**(使用者):才 1.0.1 就跳 2.0.0 看起來快,但版本號不是里程碑獎牌,是相容性訊號——真 breaking 就早升,比硬塞進 1.1 健康。
