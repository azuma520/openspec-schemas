# fix-v2-blocking-defects：SDD 工作區審查報告（保存副本）

兩份報告原本只存在於 git-ignored 的 SDD 工作區 `.superpowers/sdd/plan/`（由本機 `.git/info/exclude` 排除，`git ls-files` 為空）。
`workflow-harness/work-map.jsonl` 的 `task-20260908-author-surface-gate-alignment` 條目與本 change 的 `retrospective.md`
引用它們作為「25 條規則 × 3 個表面」缺口矩陣的起點證據；工作區 teardown 後引用會失效，故在此保存副本
（2026-09-10，fix-v2 branch review r1 的 P2）。

⚠️ **保證的實際強度（2026-09-15 補記）**：2026-09-10 複製進工作區時與原檔逐位元組相同，但這兩檔在 `bfc8660` 進版控時
`.gitattributes` 的 `-text` 規則**還沒加**（`45b6858` 才加），`core.autocrlf=true` 在 `git add` 時做了 CRLF→LF 正規化——
本日量測：兩份報告 `git ls-files --eol` 皆為 `i/lf w/crlf`，兩者 `git ls-files -s` 的 blob hash 與
`git hash-object --no-filters <工作區檔>` 皆不相等。原檔已隨 teardown 刪除，**blob 是否等於當時原檔現在已不可驗**；
能保證的是內容與行號引用（正規化只動換行符）。姊妹目錄 `../2026-09-03-loosen-plan-sdd-reports/` 是在 `-text` 加入後保存的，
其「staged blob 等於原檔未過濾雜湊」的驗證方式對本目錄**不適用**。work-map 條目文字由登記 runner 管理、未改寫，其引用的檔名以本目錄為準。

| 檔案 | 來源 | 內容 |
|---|---|---|
| `code-rereview-fallback-3.md` | `.superpowers/sdd/plan/code-rereview-fallback-3.md` | 第 3 輪 code re-review（fallback reviewer）：§ Regression 為 13 個 fixture 的獨立再推導 |
| `codegate-fixes-report.md` | `.superpowers/sdd/plan/codegate-fixes-report.md` | code gate 修正報告：規則 × 表面的雙向矩陣與 9 個缺口逐格記錄 |

同型事故的先例見 `openspec/changes/archive/2026-09-04-loosen-plan/errata.md:46`。
