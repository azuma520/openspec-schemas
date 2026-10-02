# Research(分析參考)

維護者在 schema 設計期間對成熟來源(既有 skill、上游實作)做的拆解分析。**定位:分析參考,不是規範**——正式拍板以對應 change 的 artifacts 或 `../specs/` 的設計文件為準;這裡保存「為什麼這樣判」的推導過程,供未來重複使用。

與鄰居的分工:`../specs/` 放設計定案、`../poc/` 放實測取事實(spike / PoC 報告)、本目錄放**文獻級拆解與比較**(讀 skill 全文後的結構分析)與**審查行為的實證考古**(讀 transcript / rollout 後的來源分析)。

## 索引

| 文件 | 議題 | 服務的 change |
|---|---|---|
| [2026-09-01-plan-structure-comparison.md](./2026-09-01-plan-structure-comparison.md) | Plan 結構比較:writing-plans vs /to-tickets 逐元素判定 → Plan Contract 保留/修改/移除/新增;producer 選型查證(/to-tickets 四個不可直接 invoke 的事實) | loosen-plan |
| [2026-09-01-tdd-evidence-analysis.md](./2026-09-01-tdd-evidence-analysis.md) | TDD Evidence:從成熟 skill 程序反推證據節點;RED/GREEN claim 精確化與有效性判準;最小 Evidence Contract 七欄位;機械可驗/review 判斷分工;concept vs first carrier | loosen-plan |
| [2026-09-09-review-provenance-analysis.md](./2026-09-09-review-provenance-analysis.md) | 審查行為來源考古:「當演算法讀」A–E 分類、0907 Codex 外部審 48 次 tool call 重建、五個 P1 的關係與唯一明確擴散鏈、H1–H4 判定、兩層 review 分工觀察;修正「十一席當散文讀」與「五 P1 一個形狀」兩條事後歸納的來源與適用範圍;§5 既有 review 能力對照(九項 pattern A–D 分類、0907 繞過 skill 的查證)與「不造新系統、先修 invocation、FOCUS 試用(承載方式待裁定)」裁定 | fix-v2-blocking-defects(複盤 D1/D4) |
| [2026-09-10-contract-drift-archaeology.md](./2026-09-10-contract-drift-archaeology.md) | Contract drift 三方對照:過去 dependency / coupling / SSOT 設計假說考古(H1–H12,四欄:舊假說 → 當時方案 → 缺的證據 → dogfood 判定;未找到正式提出反向依賴圖的來源)、fix-v2 審查輪次的 finding 分成 66 個分類單位(七類 × artifact-role 邊;A 多表面 32 / B 可判性 12 / E 生命週期 8,「知道依賴能否避免」的分界)、前線十題(事實 / 推論 / 建議分開;最小實驗候選:修 finding 的四步 grep-sweep 派工習慣;不拍板) | fix-v2-blocking-defects(review 觀察期) |
| [2026-09-23-requirement-traceability-current-state.md](./2026-09-23-requirement-traceability-current-state.md) | 需求追溯(Identity + Reference)current-state / gap analysis:正式設計 §3 已決但 I1–I3 零實作;Task→Decision 與 Task→測試證據是實際在用的載體;三處設計與實作演化的衝突(Decision ID、雙證據載體、RENAMED 保 ID),另記分段實作與正式設計 §9.3 的衝突;Issue #4 18 項缺陷中 reference 有幫助 4 項(可機械抓到 1、部分 2)、無幫助 14;不取代正式設計 | 無(待使用者逐題裁定 §7) |
| [2026-10-02-verification-strategy-case-crosswalk.md](./2026-10-02-verification-strategy-case-crosswalk.md) | Verification Strategy 研究第一步:Identity、retro-skill-inventory、issue #2 三案例的驗證動作逐列拆成 Claim / Method / Depth,與 TDD Evidence、Plan Structure、contract drift 三份研究對照;八個跨案例 pattern(P1 路由臨場選、P2 TDD applicability 兩判準並存、相反處置的實證不完整、P3 代理指標對不準、P5 停止條件三份研究沒談、但 auto-loop 有審查收斂先例、P6 證據壽命三子型…);只讀 repo 內材料、未讀外部來源;§3d 三題已於 §5 裁定(P2 拆成 applicability / RED validity / routing 三層、外部研究只查兩條線(OPA 先排除、§5f 改為有限度讀)、P6 改為待驗證假說並列四個反例);§5e 優先序重評:P3 Claim↔Oracle 對齊為最底層,P2 降為方法選擇層的一部分 | 無(研究題 `task-20260929-verification-strategy-research`) |
