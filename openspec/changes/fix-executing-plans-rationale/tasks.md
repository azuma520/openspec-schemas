## 1. schema.yaml

- [x] 1.1 改寫 schema.yaml 檔頭 Requirements 註解中「because the alternative executor (executing-plans) dispatches no independent reviewer」那句，使其符合 REQ-3
  - TDD: n/a — prose-only：YAML 註解文字，無可單元測試的行為；正確性由 REQ-3 逐句對照與外部審查判定
- [x] 1.2 改寫 schema.yaml apply instruction 的「This schema does NOT support `superpowers:executing-plans`」段，使其符合 REQ-3（含 TDD 推理句）
  - TDD: n/a — prose-only：instruction 文字，schema validate 不讀 prompt 內容；正確性由 REQ-3 逐句對照與外部審查判定

## 2. bridge README

- [x] 2.1 改寫 README.md 三段：§ Seven Superpowers touchpoints 表下「No `executing-plans` fallback」段、§ 4. Opinionated: subagent platforms only, no manual fallback、§ Fallback strategy 的 `apply` phase 列
  - TDD: n/a — prose-only：說明文件
- [x] 2.2 改寫 README.zh-TW.md 對應三段，語意與 2.1 一致
  - TDD: n/a — prose-only：說明文件翻譯
- [x] 2.3 改寫兩份 README § 2. Schema-level vs prompt-level integration 中「上游升版 skill 行為時 schema 不用改，只有改名或移除才要動」的說法（本 change 本身即為反例；文件審查 r1 🔴）
  - TDD: n/a — prose-only：說明文件

## 3. 維護者守則與收尾

- [x] 3.1 改寫 repo CLAUDE.md「修 schema 時的紅旗」executing-plans 那條，使其符合 REQ-3，並加一句：此禁令依正式設計 §5 之後改寫為 capability / evidence / degradation 語言（`task-20260901-claudemd-governance-rewrite`）
  - TDD: n/a — prose-only：維護者守則
- [x] 3.2 重同步 dogfood 副本、跑 `openspec schema validate superpowers-bridge` 與 `openspec schemas`，並全 repo 搜尋舊說法殘留（排除歷史紀錄）
  - TDD: n/a — configuration / 查驗：同步與結構驗證，無新行為
