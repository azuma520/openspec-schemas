# Research(分析參考)

維護者在 schema 設計期間對成熟來源(既有 skill、上游實作)做的拆解分析。**定位:分析參考,不是規範**——正式拍板以對應 change 的 artifacts 或 `../specs/` 的設計文件為準;這裡保存「為什麼這樣判」的推導過程,供未來重複使用。

與鄰居的分工:`../specs/` 放設計定案、`../poc/` 放實測取事實(spike / PoC 報告)、本目錄放**文獻級拆解與比較**(讀 skill 全文後的結構分析)。

## 索引

| 文件 | 議題 | 服務的 change |
|---|---|---|
| [2026-09-01-plan-structure-comparison.md](./2026-09-01-plan-structure-comparison.md) | Plan 結構比較:writing-plans vs /to-tickets 逐元素判定 → Plan Contract 保留/修改/移除/新增;producer 選型查證(/to-tickets 四個不可直接 invoke 的事實) | loosen-plan |
| [2026-09-01-tdd-evidence-analysis.md](./2026-09-01-tdd-evidence-analysis.md) | TDD Evidence:從成熟 skill 程序反推證據節點;RED/GREEN claim 精確化與有效性判準;最小 Evidence Contract 七欄位;機械可驗/review 判斷分工;concept vs first carrier | loosen-plan |
