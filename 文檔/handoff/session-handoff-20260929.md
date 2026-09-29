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

## Session 09:29

### 一、本 session 主題

sd0x-dev-flow 5.0.0 升級步驟 3–6 全部完成；Codex 審查改以 profile 固定模型；研究文件補 Task Context 觀察期收尾（§6），觀察期結案。

### 二、完成事項

- **sd0x 5.0.0 升級**（commit `a702205` 規則、`b5dd966` 腳本升級、`d5a81af` 新腳本、`9c602c5` CLAUDE.md＋安裝紀錄＋work-map）：規則升 10、刪退場 2（`fix-all-issues.md`、`framework.md`，使用者手刪）、新增 2（`override-contract.md`、`git-workflow-project.md`）；`testing-project.md` 補 5.0.0 範本 `paths:`（使用者選甲）；腳本升 10＋新增 9；`.claude/CLAUDE.md` 補 § Contract Triggers、Rules 清單換 5.0.0 版。全部逐檔 `git hash-object` 與外掛一致。文件審查（Codex gpt-6-sol）r2 ✅ Mergeable。程式審查與 `/precommit` 經使用者選乙不跑（commit 說明記 `[DEVIATION]`；`/precommit` 實跑為 `⚠️ NO CHECKS RUN`、前後 tree 不變）。健檢報的「腳本落後」是在裝腳本前開跑的舊結果，已重核為一致。work-map `task-20260929-sd0x-v5-upgrade` → DONE。
- **Codex profile**：`review.config.toml`（`model = "gpt-6-sol"`）放 Orca runtime home 與 `~/.codex` 兩處；`auto-loop-project.md ## Codex Profile` = `review`。以指定不存在模型的 probe profile 實證 `-p` 生效（log `model:` 行跟著變）。memory `feedback_codex_exec_not_mcp` 更新。
- **發現**：sd0x 5.0.0 `codex-exec.js` adapter 在 Windows 上 `alloc` 必失敗（`alloc dir is not 0700`；NTFS chmod 0700 讀回 0666）⇒ 走 adapter 的 Codex 審查在本機第一步即掛；本 session 審查皆直接 `codex exec`。
- **研究文件 §6**（`docs/superpowers/research/2026-09-09-review-provenance-analysis.md`）：Task Context 4 次 pilot 數據表（Pilot 2 拆 2a fallback／2b Codex）＋原始紀錄行號、⑤ 明寫不判、§5.1 前提在 5.0.0 已變（`codex-prompt-branch.md:20` 有 `${FOCUS}`）。Codex 文件審查 4 輪 ✅ Mergeable（r1–r3 各 ⛔，皆為表格與原始紀錄不符）。work-map `task-20260910-task-context-pilot` → DONE。

### 三、未完事項 / 接力棒

- [#接力] 使用者待刪：`$CODEX_HOME/probe.config.toml`（測試用 profile；AI 的 rm 被擋）。指令：`! rm "$CODEX_HOME/probe.config.toml"`。
- [#接力] 研究文件審查延後 2 條 nit：`pilot2-fallback-r2.md:1-8` 改完整路徑；「沒有做這項評估」→「紀錄中沒有這項評估」。
- [#接力] 未 commit、照舊保留：Q8 報告＋`evidence/`＋`recompute-correctness.py`、`backlog-crosscheck-shadow.json`、`2026-08-27-brainstorm-產品承諾.md`。
- [#接力] 新登記：`task-20260929-sd0x-codex-exec-windows`、`task-20260929-branch-focus-reeval`（見六）。
- [#接力] 其餘照舊：Q8 是否改 BLOCKED、重派 Q8 ③ doc review、下一個 traceability implementation change。

### 四、洞見 / 反省

**【紀律接力】**

- **把前一 session 的摘要當事實來源。** 0924 補記有三處比原始紀錄寫得滿（兩種審查者混成一句、「4 次都沒帶偏」、「可歸功 0」），補寫研究文件時直接沿用，每一處都是 Codex 抓到後才回源逐格核對；替代句「每次都不同」本身又是絕對句。⇒ 動作版：引用 handoff 摘要的數字或判斷進交付物時，表格每一格都要能指到原始紀錄某一行；指不到寫「紀錄無此項」，不填 0。attribute：全域 CLAUDE.md「證據先於斷言」＋「修正絕對句時寫出的替代句要再過一次例外檢查」。

**【當日洞見】**

- 上游改版會悄悄推翻研究文件的前提（FOCUS 槽）；引用第三方範本時寫明版本，§6 已照做。
- 外掛新機制要實測才知道能不能用：5.0.0 adapter 在 Windows alloc 必掛，讀文件看不出來。
- smart-commit 的 `alloc` 預設落 Git Bash `/tmp`，被 hook 擋；用 `TMPDIR=<scratchpad>` 解（0924 已記，本次再現、做法有效）。

**【學習候選】**

1. **Case**：補寫研究文件時沿用 0924 摘要的三處過度宣稱，文件審查因此多跑 3 輪。
2. **Candidate Pattern**：handoff 摘要是二手來源；寫進交付物前，每個數字與判斷都要能回指原始紀錄。適用：把舊摘要整理成正式文件；不適用：純轉述接力棒給使用者（仍應標來源）。
3. **Evidence**：本次 3 例＋0924「evidence 欄位出處」猜錯 1 例。因果（摘要壓縮時丟了限定詞）為 **Hypothesis**。
4. **Minimum Sufficient Intervention**：不新增規則——全域「證據先於斷言」已涵蓋，缺的是執行時點。
5. **Promotion**：Case Memory。

### 五、檔案異動

錨來源：本 session 開工 commit（dd82db7、開工於 2026-09-29T08:45:37）——列 dd82db7..HEAD：`a702205`、`b5dd966`、`d5a81af`、`9c602c5`（`.claude/rules/**`、`.claude/scripts/**`、`.claude/CLAUDE.md`、`.sd0x/install-state.json`、`workflow-harness/work-map.jsonl`）。

收工 commit 另含：`.claude/rules/auto-loop-project.md`（`## Codex Profile`）、研究文件 §6、`workflow-harness/work-map.jsonl`（task-context-pilot DONE＋兩條新登記）、本 handoff。

非 repo：`~/.codex/review.config.toml`、`%APPDATA%/orca/codex-runtime-home/home/review.config.toml`（＋待刪 `probe.config.toml`）；memory `feedback_codex_exec_not_mcp.md`、`MEMORY.md`；`.claude_review_state.json`（gitignored，被 5.0.0 遷移刪除）。

### 六、下一步建議

1. Q8：決定是否改 BLOCKED、是否重派 ③ doc review 後 commit 報告與 evidence。
2. `task-20260929-sd0x-codex-exec-windows`：回報上游或在本 repo 記繞道說明（影響之後每次審查怎麼派）。
3. 下一個 traceability implementation change（使用者決定何時開）；`task-20260929-branch-focus-reeval` 可併入其評估。

## Session 10:29

### 一、本 session 主題

開工三步驟後，使用者要求先確認接力棒第 1（Q8）、2（sd0x adapter Windows 失敗）兩件「問題還在不在」再討論解法；確認後裁定第 2 件走 A（本 repo 繞道說明）＋B（回報上游），Q8 甲乙丙改下個 session 討論。

### 二、完成事項

- **Q8 現況確認**（未改任何檔）：報告自 9/21 未動；`inputs-six-cases.md` SHA256 與報告記載一致（`55680e38…`）；重跑 `recompute-correctness.py` 仍得 Correctness 12/12；`schema.yaml` 9/17 起零 commit、`:561` 引文仍在。仍卡三件：9/22 起 ③ doc review 未重派、報告＋`evidence/`＋腳本未 commit、§9 甲乙丙待拍板。
- **adapter Windows 失敗實測重現**：`node .claude/scripts/codex-exec.js --protocol 1 alloc` → `alloc dir is not 0700`、exit 1；repo 副本與 plugin 5.0.0 逐位元相同；`TEMP`/`TMP` 改指 scratchpad 一樣失敗。依 plugin `codex-transport.md` § Completion state machine，alloc 失敗**不算** `codex_fail`、不改派 fallback（我先前對使用者說「會靜默改派」是錯的，已當場更正）。
- **A：`CLAUDE.md` 新增「## Codex 審查在 Windows 本機怎麼派(2026-09-29 起)」**（未 commit，見三）：失敗原因、直接 `codex exec` 的第一輪／resume 指令（旗標放 `resume` 前）、成敗判準（exit 0＋報告非空＋`session id:` 三者皆成立，否則 = `codex_fail` 走 fallback）、保護降級（scratchpad ACL 含 `CodexSandboxUsers` Modify，icacls 實查；owner-only 指令 Git Bash 實測可用）、清理必做（scratchpad 不自動回收，8/14 起舊目錄仍在）、退場條件（完整走一次 adapter 派送成功才刪）。
  - 審查：Codex（gpt-6-sol）r1 ⛔ 5 條、r2 ⛔ 2 條＋1 Nit；r3 撞 Codex 額度（13:06 恢復）→ 使用者同意降級，fallback strict-reviewer r1 ⛔（2 P1＋2 P2＋5 Nit）→ r2 ✅ Mergeable＋1 Nit → 修 Nit 後 r3 ✅ Mergeable。`[REVIEWER_FALLBACK] plane=doc from=codex to=strict-reviewer reason=quota`。`review-state note doc_review pass` 已記——⚠️ 該 digest 同時涵蓋未審的 Q8 報告改動，不代表 Q8 報告已審。
  - 之後又補一行上游 issue 連結 → doc plane 重新打開，未重審。
- **B：上游 issue 已發**：https://github.com/sd0xdev/sd0x-harness/issues/19（使用者核可文字、刪去「Happy to test a fix on Windows.」後發出；回讀 OPEN、內容一致）。上游 repo 已由 `sd0x-dev-flow` 改名 `sd0x-harness`。issue 草稿與 CLAUDE.md 同批審過。
- work-map `task-20260929-sd0x-codex-exec-windows` → **BLOCKED**（等外部：issue #19；runner readback_ok）。doctor 隨即報 `blocked_by_pairing`（BLOCKED 必須帶 `blocked_by`），而 `register update`／`repair` 都沒有設 `blocked_by` 的旗標 → 直接改該行 JSON 加 `"blocked_by": "external"`（只動這一行，`/work-status --json` 回讀 integrity 空、壞筆 0）。這是 writer 的缺口，記一筆：BLOCKED 只能靠手改才合規。record 無欄位可掛 issue 連結，連結在本區塊與 CLAUDE.md。
- 09:29 接力棒「使用者待刪 `probe.config.toml`」：已查 `$CODEX_HOME` 與 `~/.codex` 兩處皆不存在，已清。

### 三、未完事項 / 接力棒

- [#接力] **`CLAUDE.md` 新節未 commit（使用者選甲）**：13:06 後 Codex 補審（降級審查的補審義務＋issue 連結那行的重審），通過後 `node .claude/scripts/review-state.js note doc_review pass` 再 commit。派法照該節本身（直接 `codex exec -p review …`，新 thread）。
- [#接力] **Q8 甲乙丙**：使用者指定下個 session 討論。Q8 報告的 ③ doc review 仍欠（本 session 的 doc_review pass 不涵蓋它）。
- [#接力] 追 issue #19 回應；上游修好後依 CLAUDE.md 該節退場條件驗證、刪節、work-map 那條結案。
- [#接力] 未 commit、照舊保留：Q8 報告＋`evidence/`＋`recompute-correctness.py`、`backlog-crosscheck-shadow.json`、`2026-08-27-brainstorm-產品承諾.md`。
- [#接力] 使用者待決（未回、目前維持現狀）：全域 CLAUDE.md 寫 Codex 審查走 Orca 終端機分頁（看得到、可插話），實際做法是背景 `codex exec`＋落檔。使用者未明確回覆（「2沒問題」回的是 issue 以其帳號公開發出那點），目前照預設維持背景跑法；全域 CLAUDE.md 那句未改。
- [#接力] 09:29 其餘照舊：研究文件 2 條 nit、`task-20260929-branch-focus-reeval`、下一個 traceability change。

### 四、洞見 / 反省

**【紀律接力】**

- **說「系統會怎樣」前先跑一次或讀到規則原文那一行。** 本 session 4 次憑推論說系統行為都錯：①「alloc 失敗會被當 Codex 掛掉、靜默改派」——規則原文明寫不算；②「暫存資料夾只給本人」——icacls 實查不是；③「換暫存位置也失敗」——改的是 `TMPDIR`、Windows Node 不讀它，等於沒測；④「暫存檔隨 session 回收」——8 月舊目錄仍在。①②自查抓到，③④審查抓到；推理每次都說得通，錯在沒碰。⇒ 動作版：寫進交付物的每一條系統行為，當場實跑或讀到原文；做不到標【未查證】。attribute：全域 CLAUDE.md「減少不知道自己不知道 ①能碰就碰」＋「寫規格條文前讀每條 early return / 特例分支」。

**【當日洞見】**

- 繞過 adapter 直接呼叫時，要接手的不只指令，還有 adapter 默默代做的判斷：成敗判準、失敗分流、清理、檔案權限。繞道說明第一版只換了指令，後四項都漏。
- 降級審查（fallback strict-reviewer）抓到 Codex 兩輪沒抓到的兩條 P1（resume 旗標位置、直接呼叫時無人判 `codex_fail`）。樣本 1，**Hypothesis**。
- `review-state note` 綁整個 doc plane digest、不分檔：本次 pass 同時蓋到未審的 Q8 報告。看到「doc_review pass」不能讀成「每份文件都審過」。

**【學習候選】**

1. **Case**：本 session 4 次憑推論宣稱系統行為皆錯（見紀律接力）。
2. **Candidate Pattern**：寫進交付物的系統行為宣稱，當場實跑或讀原文。適用：說明文件、issue、規格；不適用：明標為推測的段落（如 issue 的「Probably affected」節）。
3. **Evidence**：本 session 4 例。
4. **Minimum Sufficient Intervention**：不新增規則——全域「能碰就碰」已涵蓋，缺的是執行時點。
5. **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（23e893a、開工於 2026-09-29T09:46:38）——`23e893a..HEAD` 為空（本 session 收工前零 commit）。

- working tree：`CLAUDE.md`（新節，**本次不 commit**）、`workflow-harness/work-map.jsonl`（codex-exec-windows → BLOCKED）、本 handoff 檔。
- 非 repo：GitHub `sd0xdev/sd0x-harness#19`（新建）；scratchpad 的審查 prompt／報告／log 與 issue 草稿。

### 六、下一步建議

1. 13:06 後 Codex 補審 `CLAUDE.md` 新節 → note pass → commit。
2. Q8 甲乙丙討論（使用者指定），並決定 Q8 報告 ③ doc review 與 commit 時機。
3. 看 issue #19 有無回應。
