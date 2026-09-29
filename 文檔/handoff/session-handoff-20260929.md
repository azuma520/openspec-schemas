<!--
workflow-harness — Handoff template
對應 inventory：A5 六欄 schema、A6 append-only、A7 檔名 schema
檔名：文檔/handoff/session-handoff-{DATE:YYYYMMDD}.md
規則：append-only — 同日多 session append 多個「## Session HH:MM」區塊；前段不可改

schema 變更紀錄：
- 原七欄 schema（一/二/三/四=洞見+阻塞/五=複盤/六=檔案異動/七=下一步建議）已於 change `refactor-handoff-schema` 合併
- 五整欄刪、合進新四（改名「洞見 / 反省」）；舊六七編號升階為新五六
- 新四加 sub-segment【紀律接力】+【當日洞見】、三+四加 tag 字典
-->

# Session Handoff — 2026-09-29

<!--
本檔每個 session 結束時 append 一個 ## Session HH:MM 區塊。
六欄 heading 順序固定，缺漏會被 Stop hook block。
四欄內 sub-segment marker（**【紀律接力】** / **【當日洞見】**）缺漏會 Stop hook ⚠️ Warn（不 block）。
-->

<!--
HH:MM 必須是寫入當下 wall-clock；不可從前一區塊推延。取時用：
  python -c "import datetime; print(datetime.datetime.now().strftime('%H:%M'))"
Python 失敗 → 寫 ??:?? + 區塊內附註原因。
-->

## Session 08:03（跨日延續：2026-09-24 16:39 開工的 session，換日後由 Stop hook 要求建檔）

### 一、本 session 主題

0924 已收工（commit `5d4e69c`）後的兩則補記：workflow-harness 更正發版評估（alpha.19 再延後）；以及 Stop hook 輸出揭露 **live hook 實際執行的是 `D:\workflow-harness` 工作目錄、不是 plugin 快取 alpha.18**——推翻 0924 交接的「Issue #4 未上線」說法。

### 二、完成事項

- **查證 live hook 來源**：本次 Stop hook 的命令是 `python "D:\workflow-harness/hooks/stop.py"`；`D:\workflow-harness` 目前在 main `a969399`，`3238853`（Issue #4 修正）是其祖先，`hooks/stop.py:219` 已呼叫 `resolve_for_hook_read`。⇒ **Issue #4 修正已在 live 生效**。
- 轉告使用者 workflow-harness-20 的發版評估更正：掃描器出貨前置多一條 #142（backlog `<!-- -->` 註解內 `- ` 開頭散文被兩個 reader 當成條目、零診斷）；使用者已在該 session 拍板發版前修；5.3 已完成（`a969399`）、12.5 外審 Round 2 ⛔（4 P1＋7 P2/P3）處置中。

### 三、未完事項 / 接力棒

- [#接力] **0924 交接三的「Issue #4 未上線、等 alpha.19」前提不成立**（live hook = `D:\workflow-harness` 工作樹，不是快取）。下次開工要重判：①Issue #4 與 work-map `task-20260915-stop-hook-worktree-root` 是否現在就可以結（修正已在 live、0924 實測通過）②0924 那份「發版會把未過審掃描器帶上線」的顧慮——若 live 本來就跑工作樹，掃描器（含未 commit 的改動）**已經**在使用者機器上執行，這要告知 workflow-harness-20。【未查證】hook 何時、為何解析到 `D:\workflow-harness` 而非快取（`installed_plugins.json` 仍記 installPath＝快取 alpha.18；`known_marketplaces.json` 的 workflow-harness 來源是 directory `D:\workflow-harness`）。
- [#接力] 0924 交接三、六其餘各條照舊（Issue #4 收尾雜事、Task Context 甲／乙與 ⑤、Q8 狀態、traceability change）。
- [#接力] 0924 交接檔尾的「18:xx 補記」（Task Context 紀錄整理）**未 commit**，與本檔一起下次 commit。

### 四、洞見 / 反省

**【紀律接力】**

- **把「live 跑哪一份」當成推論，沒有實測。** 0924 從 `installed_plugins.json` 與 9/14 交接的「版本不變不重抄」推出「live＝快取 alpha.18」，並據此建議使用者選 B（不發版）、Issue #4 維持 open；但同一天每次 SessionStart／Stop 的 hook 命令路徑其實都看得到（`/work-status` 注入的就是 `D:/workflow-harness/...`）。能碰就碰：宣稱「某個 runtime 跑哪份程式」前，先看實際被執行的命令路徑。attribute：全域 CLAUDE.md「減少不知道自己不知道 ①能碰就碰」＋六軸「對象（量的是這個環境嗎？）」。

**【當日洞見】**

- 沒有額外洞見（本區塊只是補記）。

### 五、檔案異動

- 本 handoff 檔（新建）。0924 交接檔尾補記未 commit。

### 六、下一步建議

1. 重判 Issue #4 是否可結、並把「live 跑的是工作樹」告知 workflow-harness-20（見三第一條）。
2. 0924 交接六的其餘三條照舊。

## Session 08:35

### 一、本 session 主題

開工三步驟後處理接力棒第 1 條（Issue #4 重判）與第 2 條中的 Task Context 甲／乙；途中使用者告知 sd0x 改版，決定先升級 sd0x（4.3.1 → 5.0.0）再做甲。本 session 做到升級步驟 1（plugin 更新），使用者要重開 session 讓新版生效，後續步驟接力。

### 二、完成事項

- **Issue #4 重判 → 使用者裁定 A（現在結案）＋甲（收尾交 workflow-harness-20）**。查證事實：live hook＝`D:\workflow-harness` 工作目錄（`~/.claude/settings.json` 的 marketplace 來源為 directory `D:\workflow-harness`；本 session `/work-status` 注入路徑即此）；該目錄 HEAD `a969399` 含修正 `3238853`（`merge-base --is-ancestor` 通過）；PR #6 已 merge（`4af3f6a`，2026-09-24）；9/24 真實 linked worktree dogfood 通過。「為何 installed_plugins.json 記快取 alpha.18 卻跑工作目錄」的機制【未查證】。
- work-map `task-20260915-stop-hook-worktree-root` → **DONE**（runner update，readback_ok）。
- **SendMessage 給 workflow-harness-20**（08:1x，對方 busy、訊息排入佇列、尚無回覆）：live 路徑更正（含「其未 commit 的 `hooks/lib/backlog_parser.py` 改動每次 hook 都在跑」）＋使用者裁定＋收尾四件：tasks 4.4/4.5 打勾（4.5 記偏離 design.md:79 的理由）、`openspec archive fix-worktree-canonical-root`、移除 `.worktrees/fix-issue-4-worktree-canonical-root` 與本機分支（遠端分支刪否由使用者定）、Issue #4 留言後關閉。
- **Task Context 甲／乙**：已向使用者解釋 Task Context 是什麼（9/10 派工五格習慣＋禁放清單）；回源核對 pilot 紀錄（`文檔/handoff/attachments/20260910-pilot2/`）數字與 0924 補記一致。使用者選 **甲（補寫短節）**。額外觀察：Pilot 2 漏抓的 5 條多為 Nit／缺 fixture 類小毛病（hypothesis：審查者把力氣放在大問題，非盲點）。
- **sd0x 升級盤點**：本機 4.3.1（8/26）、上游 v5.0.0（9/26，中間 4.4–4.7）。重點：4.6 Codex 審查改走 `codex exec`；4.7 goal-mode commits（使用者設 goal 期間 `/smart-commit --execute` 可免逐次詢問、`/push-ci` 可由模型發起）；5.0 規則按需載入、`fix-all-issues.md`／`framework.md` 退場、新增 `override-contract.md`；5.0 的 `codex-prompt-branch.md` 已有 `${FOCUS}` 槽（研究文件 §5.1 A/B 題的前提在上游已變）。本 repo 的 15 個 managed rules 與 4.3.1 原版逐檔一致（僅 `*-project.md` 兩個使用者檔不同）；掃 `C:\Users\user\orca\*`、`D:\Work\*`、`D:\*` 只有本 repo 有 `.sd0x/install-state.json`（其他位置未掃）。
- **升級步驟 1 完成**：`claude plugin marketplace update sd0xdev-marketplace` ＋ `claude plugin update sd0x-dev-flow@sd0xdev-marketplace` → `installed_plugins.json` 記 5.0.0、installPath 指 `.../sd0x-dev-flow/5.0.0`；舊 `4.3.1/` 快取目錄仍在。本 session 仍載入 4.3.1，需重開。

### 三、未完事項 / 接力棒

- [#接力] **sd0x 5.0.0 升級步驟 3–6**（work-map `task-20260929-sd0x-v5-upgrade`）：③ `/install-rules --all`（升級未改過的 rules、移除 `fix-all-issues.md`／`framework.md`、裝 `override-contract.md`）④ 把 plugin `CLAUDE.template.md` 的 § Contract Triggers 複製進 `.claude/CLAUDE.md` ⑤ `/claude-health --scope sync`、逐檔看 git diff、查 `.claude/scripts/` 是否要 `/install-scripts`（遷移指南沒提）、**commit 前先讀新裝的 `git-workflow-project.md` 與 4.7 goal-mode 授權說明**（與「commit 要使用者核可」習慣相關，細節【未查證】）、用新版 `/codex-review-doc` 審改動的 .md ⑥ `/smart-commit --execute`（使用者核可）。遷移指南在 plugin `CHANGELOG.md` § 5.0.0 → Upgrading an installed project。plugin 退回 4.3.1 的方式【未查證】。
- [#接力] **升級完成後做甲**：在 `docs/superpowers/research/2026-09-09-review-provenance-analysis.md` 補短節（約十幾行）：4 次 pilot 數據表並連原始紀錄、標「觀察非結論、樣本小」、「漏抓多為小毛病」標 hypothesis、不寫流程改動；另加一行註記「§5.1 前提（branch 範本無 FOCUS）在上游 5.0.0 已改變」、不改寫原分析。→ 文件審查 → work-map `task-20260910-task-context-pilot` 標 DONE。
- [#待確認] **⑤（Pilot 1/2 findings 與 miss 是否服務實際風險）**：我建議 ii「明寫決定不判」，使用者未明示；未回覆則照 ii 寫。
- [#接力] **Issue #4 收尾在 workflow-harness-20**：GitHub Issue #4 目前仍 OPEN，等它做完；下次開工確認是否已回覆／關閉。
- [#接力] 未 commit 且本次刻意不收：Q8 報告＋`evidence/`＋`recompute-correctness.py`（等 ③ doc review 重派）、`2026-08-27-brainstorm-產品承諾.md`（8/27 起未追蹤）、`backlog-crosscheck-shadow.json`（開工前已修改、來源未查）。
- [#接力] 0924 交接六其餘：Q8 是否改 BLOCKED、下一個 traceability implementation change，照舊待使用者。

### 四、洞見 / 反省

**【紀律接力】**

- **已決事項要先確認前提今天還成立，再決定照辦或重端。** 9/24 使用者定「等 alpha.19 上線再關 Issue #4」，前提「修正尚未上線」已被推翻；本次把它重新端給使用者決定，而不是照舊辦或自行改掉。「提案前先查已決」的補充：查到已決時一併檢查它的前提。attribute：全域 CLAUDE.md 動工硬 gate「提案前先查已決」＋六軸「前提（前提今天還成立嗎？）」。

**【當日洞見】**

- 上游改版會讓研究文件的前提過期：研究 §5.1 A/B 題的前提（branch 範本無 FOCUS）在 sd0x 5.0.0 已不成立。引用第三方範本行號的研究應寫明當時版本——在甲的補寫中順手處理。
- workflow-harness 以 directory marketplace 安裝，live＝工作目錄，連未 commit 的改動也會被 hook 執行。

**【學習候選】**

沒有。

### 五、檔案異動

- 本 session 無新 commit（錨：開工 commit `5d4e69c`，`5d4e69c..HEAD` 為空）。
- working tree：`workflow-harness/work-map.jsonl`（Issue #4 → DONE；新增 `task-20260929-sd0x-v5-upgrade`）、本 handoff 檔。
- 本 repo 外：`~/.claude/plugins/`（sd0x plugin 更新至 5.0.0）。

### 六、下一步建議

1. 重開 session 後接 sd0x 升級步驟 3–6（見三第一條）。
2. 升級完成後做甲（研究文件短節 → 文件審查 → task-context-pilot DONE）。
3. 確認 workflow-harness-20 是否已完成 Issue #4 收尾並關閉 Issue。
