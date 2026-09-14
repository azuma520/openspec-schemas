# fix-v2-blocking-defects：SDD 工作區審查報告（保存副本）

兩份報告原本只存在於 git-ignored 的 SDD 工作區 `.superpowers/sdd/plan/`（由本機 `.git/info/exclude` 排除，`git ls-files` 為空）。
`workflow-harness/work-map.jsonl` 的 `task-20260908-author-surface-gate-alignment` 條目與本 change 的 `retrospective.md`
引用它們作為「25 條規則 × 3 個表面」缺口矩陣的起點證據；工作區 teardown 後引用會失效，故在此保存**逐位元組相同**的副本
（2026-09-10，fix-v2 branch review r1 的 P2）。work-map 條目文字由登記 runner 管理、未改寫，其引用的檔名以本目錄為準。

| 檔案 | 來源 | 內容 |
|---|---|---|
| `code-rereview-fallback-3.md` | `.superpowers/sdd/plan/code-rereview-fallback-3.md` | 第 3 輪 code re-review（fallback reviewer）：§ Regression 為 13 個 fixture 的獨立再推導 |
| `codegate-fixes-report.md` | `.superpowers/sdd/plan/codegate-fixes-report.md` | code gate 修正報告：規則 × 表面的雙向矩陣與 9 個缺口逐格記錄 |

同型事故的先例見 `openspec/changes/archive/2026-09-04-loosen-plan/errata.md:46`。
