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
