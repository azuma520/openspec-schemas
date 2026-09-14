# loosen-plan：SDD 工作區報告（保存副本）

這十二份報告原本只存在於 git-ignored 的 SDD 工作區 `.superpowers/sdd/plan/`。工作區在 `loosen-plan` / `fix-v2-blocking-defects`
收尾時移除,而下表「引用者」欄的永久文件在它還存在時就把它們當證據引用了——teardown 後那些引用會失效,故在此保存**逐位元組相同**
的副本（2026-09-14,teardown 前的保存確認）。每一檔都經 SHA-256 逐檔比對與來源相同。

⚠️ **「逐位元組相同」需要一條 `.gitattributes` 規則才成立。** 這十二份原檔**換行符並不一致**:
十一份是 LF,`task-1.1-brief.md` 是 CRLF（88 行）。本 repo 的 `core.autocrlf=true` 會在 `git add` 時把 CRLF
正規化成 LF、在 checkout 時把 LF 換成 CRLF——兩個方向都會讓工作區或 blob 不再等於原檔,保存所宣稱的那個
性質當場失效,且不會有任何錯誤訊息。`-text` 的作用是**兩個方向都不轉換**,所以每一份都照它原本的樣子存與取,
不需要先把它們統一成同一種換行符。`.gitattributes` 因此對本目錄與姊妹目錄釘了 `-text`（不是 `text eol=lf`:
那是「釘成 LF」,這裡要的是「一個位元組都不要動」）。量測方式,可自行複跑:

```bash
# staged blob 應等於原檔的未過濾雜湊
git ls-files -s -- docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/<檔名>
git hash-object --no-filters <原檔路徑>
```

⚠️ **逐位元組相同救得回內容與行號,救不回檔案 metadata。** 副本的 mtime 是複製當下的時間,不是原檔的（例:`task-1.1-brief.md` 原檔 2026-09-07 16:17,副本 2026-09-14）。用 `cp -p` 也不解決——**git 不儲存 mtime**,任何一次新 clone 都會重設。因此凡是靠檔案時間成立的宣稱（例「哪一份是第一個產出的 artifact」、耗時統計）在保存後**仍然不可複驗**;可複驗的是內容與行號引用。

**保存判準：只保存「已有永久 consumer」的檔案。** 工作區共 72 檔,拆分為:本目錄新保存 **12** 檔、姊妹目錄 `../2026-09-08-fix-v2-review-reports/` 於 2026-09-10 已保存 **2** 檔、其餘 **58** 檔無任何永久文件引用,隨 teardown 一併刪除。
這不是把整個 SDD 工作區升級成永久資產,也不是新增一套 evidence 治理架構——只是把已被永久成果依賴的那幾份救出來。

| 檔案 | 來源 | 引用者 |
|---|---|---|
| `code-review-fallback.md` | `.superpowers/sdd/plan/code-review-fallback.md` | `research/2026-09-09-review-provenance-analysis.md`、`research/2026-09-10-contract-drift-archaeology.md`、`archive/2026-09-14-fix-v2-blocking-defects/retrospective.md` |
| `final-review.md` | `.superpowers/sdd/plan/final-review.md` | `research/2026-09-10-contract-drift-archaeology.md`、`archive/2026-09-14-fix-v2-blocking-defects/retrospective.md` |
| `progress.md` | `.superpowers/sdd/plan/progress.md` | `research/2026-09-10-contract-drift-archaeology.md`、`retrospectives/2026-09-03-loosen-plan-execution.md`、`poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md`、`archive/2026-09-04-loosen-plan/errata.md`、`archive/2026-09-14-fix-v2-blocking-defects/retrospective.md` |
| `review-1.1-1.3.md` | `.superpowers/sdd/plan/review-1.1-1.3.md` | `research/2026-09-09-review-provenance-analysis.md` |
| `review-2.1.md` | `.superpowers/sdd/plan/review-2.1.md` | `research/2026-09-09-review-provenance-analysis.md` |
| `review-2.2.md` | `.superpowers/sdd/plan/review-2.2.md` | `research/2026-09-09-review-provenance-analysis.md` |
| `review-2.3.md` | `.superpowers/sdd/plan/review-2.3.md` | `research/2026-09-09-review-provenance-analysis.md` |
| `task-1.1-brief.md` | `.superpowers/sdd/plan/task-1.1-brief.md` | `archive/2026-09-14-fix-v2-blocking-defects/retrospective.md` |
| `task-2.2-red-walk.md` | `.superpowers/sdd/plan/task-2.2-red-walk.md` | `archive/2026-09-14-fix-v2-blocking-defects/retrospective.md` |
| `task-2.3-red-walk.md` | `.superpowers/sdd/plan/task-2.3-red-walk.md` | `archive/2026-09-14-fix-v2-blocking-defects/tasks.md` |
| `task-1.1-1.3-report.md` | `.superpowers/sdd/plan/task-1.1-1.3-report.md` | 本目錄的 `review-1.1-1.3.md`（二階依賴:保存下來的報告自己引用它,故一併保存） |
| `task-4.1-4.2-report.md` | `.superpowers/sdd/plan/task-4.1-4.2-report.md` | `poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md`、`archive/2026-09-04-loosen-plan/errata.md` |

**已封存的 change 未被改寫。** `archive/` 底下的文件保留當時的敘述與判定,只以 relocation note / errata 附加說明舊路徑已搬至本目錄;
現行文件（`docs/superpowers/research/`、`poc/`、`retrospectives/`）則直接把舊路徑改成本目錄的路徑。

同型事故的先例見 `openspec/changes/archive/2026-09-04-loosen-plan/errata.md:46`;姊妹目錄
`../2026-09-08-fix-v2-review-reports/` 以同一理由保存了另外兩份。
