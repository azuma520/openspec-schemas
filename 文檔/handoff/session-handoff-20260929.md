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

> **10:29 區塊補記（收工 commit `acbe83f` 之後）**：使用者裁定 Codex 審查改在 **Orca 分頁跑 `codex exec`（甲）**——`orca terminal create --shell git-bash --command "<同 CLAUDE.md 那條 codex exec 指令，輸出 tee 進 log>"`，使用者看得到過程、不能中途插話；報告仍 `-o` 落檔、成敗判準不變。否決乙（互動版 `codex`：可插話但無報告檔、成敗判準要重設計）。**尚未實測**。⇒ 接力棒第 1 條（13:06 後 Codex 補審 CLAUDE.md）改用此法派，順便實測；可行則把 CLAUDE.md 該節的派法改成 Orca 分頁、併入同一次補審。本補記未 commit。

## Session 14:52

### 一、本 session 主題

Q8 收尾（裁定丙）＋主線下一步排定（A 需求追蹤拆塊、Identity 先做、B 延到 `Contracts:` 那塊再挑）＋ Q8 報告與 `CLAUDE.md` 繞道節的 Codex 文件審（改在 Orca 分頁跑，首次實測）。

### 二、完成事項

- **Q8 裁定丙（收掉、不做第二輪）**：報告 §9 新增「裁定（2026-09-29）」小節，記 §7 三個發現各自去處；work-map `task-20260915-b-structured-definition-experiment` → DONE（readback_ok）。
- **主線排序裁定（使用者選方案一）**：A「需求追蹤正式實作」拆成 Identity → Task→Requirement（`Contracts:`）→ 驗收台帳 → Gate/freshness → 歸檔身分檢查。新登記 `task-20260929-requirement-scenario-identity`（NEXT，掛主線下）：只做 §3.1 stable ID 身分層，不加 `Contracts:`、不做 `verification-results.json`。B（作者表面對齊）不單獨開、不整包併入：做到 `Contracts:` 那塊時，把 9/8 matrix 原 finding 凍結成清單，逐項問「不處理的話，新增 `Contracts:` 後 task 附屬行會不會出現兩套不一致的規則」，會才收、不會留在 B。依據：B 的 7 個延後缺口只有 D2 是「照說明寫卻被擋」，其餘 6 條皆為檢查比說明寬（9/8 報告 Deferral safety 表）。
- **正式設計文件頭狀態句已更新**：改為「2026-09-24 經使用者核可（`8002fa0`）、正文自核可後未改」（`git diff 8002fa0` 確認僅此一行）。
- **Q8 報告＋`evidence/README.md`＋正式設計文件頭：Codex 文件審 3 輪 ✅ Mergeable**（thread `01a0ebd4`）。開工以為 Codex 沒額度，照規矩先試一次才發現可用——**不是降級審查**。修正：重跑指令改 `python -X utf8 …`（任何 shell 可跑，實跑 12/12）；§9 標題改為已拍板；README 重跑段改正輸出位置（`generators/pairs/`，非 `evidence/pairs/`）；補 `gen_arm0.py` 缺的 `schema_prefix.yaml` 重建指令（位元不變寫法、實測第 516 行為 `CHECKS 8-12`）。同類掃描另抓到 Codex 沒抓到的：`gen_arm0.py`／`gen_materialized.py`／`gen_arms.py` 重跑會**覆寫已凍結的紀錄檔**（arm0／materialized-inputs／arm2／arm3），已列表警告。
- **`CLAUDE.md`「Codex 審查在 Windows 本機怎麼派」節：Codex 補審 3 輪 ✅ Mergeable**（thread `01a0ebdb`，三輪皆在 Orca 分頁跑）。r1 ⛔ 3 條（adapter 代做的檢查未補、「任一不成立＝codex_fail」過寬、`tee` 吃結束碼）→ 改寫：派法改 Orca 分頁（腳本＋`${PIPESTATUS[0]}` 寫結束碼檔、`orca terminal create` 只代表分頁開成）、補「開跑前查 profile 檔／跑完後查結束碼＋報告為一般非空檔＋`session id` 且續輪須等於帶入 id」、沒結果時分三種（設定錯＝不改派／狀態不明＝gate 開著／已結束不合格＝才是 codex_fail）；另記 `CODEX_HOME` 在本機 Claude Code 的 Bash 裡指向 `%APPDATA%\orca\codex-runtime-home\home`（兩處各一份 `review.config.toml`）、`codex exec` 旗標錯回 exit 2（實測）。r2 ⛔ 1 條（直接 Bash 版重導順序寫反）→ 修 → r3 ✅。上個 session 的降級審查補審義務就此結清。
- `node .claude/scripts/review-state.js note doc_review pass` 已記（涵蓋上面兩批、兩批最新一輪皆 ✅）。⚠️ 本 handoff 區塊寫於 note 之後，未經審查。
- 10:29 補記裡的 Orca 分頁指令（`tee` 進 log）已由 `CLAUDE.md` 該節取代；該補記為歷史紀錄、依 append-only 不改。

### 三、未完事項 / 接力棒

- [#接力] **程式碼審查這關依使用者決定不跑**：Q8 資料夾 5 支 `.py`（`recompute-correctness.py`＋`evidence/generators/` 4 支）是凍結證據、不得修改，使用者裁定不審。code_review 未記 pass，是刻意的。
- [#接力] **commit 狀態**：見本區塊五（依收工時使用者決定）。
- [#接力] Identity 實作：已是主線下一步，下個 session 可開 change（先盤點要動哪些檔、規模多大——本 session 未估）。
- [#接力] 追 issue #19；照舊：研究文件 2 條 nit、`task-20260929-branch-focus-reeval`。
- [#接力] 使用者待刪（AI 無 rm 權限）：scratchpad 內本 session 的 `claudemd-*` prompt／報告／log／結束碼檔與 `run-claudemd-*.sh`。

### 四、洞見 / 反省

**【紀律接力】**

- **拿來當決策前提的外部狀態，不管是誰說的，動手前先實際碰一次。** 本 session 開工時雙方都以為 Codex 沒額度，差點直接走降級審查；照規矩先試一次，Codex 可用，省掉一整輪降級審與之後的補審。上個 session 是「說系統會怎樣前先跑一次」，這次延伸到「別人告訴我的前提」。attribute：全域 CLAUDE.md「能碰就碰」。

**【當日洞見】**

- B（作者表面對齊）的 7 個缺口只有 D2 會讓作者照說明寫卻被擋；名字聽起來多嚴重 ≠ 風險多大，要逐格看方向。
- 修一條 review finding 時順著同類掃，抓到 Codex 沒抓到的（3 支腳本會覆寫凍結紀錄）——「一個缺陷＝一類缺陷」再得一例。
- 審查者互補再得一例（方向與上個 session 相反）：上個 session 備援 strict-reviewer 抓到 Codex 兩輪沒抓到的兩條 P1；這次 Codex 抓到那個備援審查員放過的 3 條 🔴＋1 條。樣本 2，**Hypothesis**：換審查者本身就有增益，不是誰固定比較強。
- `review-state` 的 doc plane 不分檔案，第 2 次卡住（上次 10:29 蓋到未審的 Q8；這次 Q8 過了卻要等 `CLAUDE.md` 才能記）。是否進 backlog `[優化建議]` 待使用者決定。

**【學習候選】**

1. **Case**：開工以為 Codex 沒額度，照規矩先試一次才發現可用。
2. **Candidate Pattern**：外部服務狀態（額度、連線、權限）要當決策前提前，先實際試一次。適用：決定要不要降級、要不要換路；不適用：試一次本身有成本或副作用。
3. **Evidence**：本 session 1 例，Hypothesis。
4. **Minimum Sufficient Intervention**：不新增規則——全域「能碰就碰」已涵蓋。
5. **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（acbe83f、開工於 2026-09-29T11:20:40）——`acbe83f..HEAD` 為空（收工前零 commit）。

- working tree（本 session 改）：`CLAUDE.md`（繞道節改寫）、`docs/superpowers/poc/2026-09-17-q8-structured-definition/results-and-next-step.md`（§9 裁定＋修正）、`…/evidence/README.md`（新檔，重跑段修正）、`docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`（文件頭一行）、`workflow-harness/work-map.jsonl`（Q8 DONE、Identity 新增）、本 handoff。
- 非本 session、照舊未 commit：`backlog-crosscheck-shadow.json`、`2026-08-27-brainstorm-產品承諾.md`、`recompute-correctness.py` 與 `evidence/` 其餘檔（09-21 產物）。

### 六、下一步建議

1. commit 本 session 成果（若收工時未 commit）。
2. 開 Identity 實作 change（主線下一步）：先盤點範圍再 `openspec new change`。
3. 看 issue #19 有無回應。

## Session 18:04

### 一、本 session 主題

開工三步驟後清兩個小尾巴，接著開 Identity 實作 change（`requirement-scenario-identity`）：範圍盤點（含 CLI 實測）→ brainstorm → proposal → design → specs，經 Codex 2 輪＋Fable 代審 3 輪文件審，最終 ✅ Mergeable 並**凍結設計 artifacts**。tasks.md 留到下個 session。

### 二、完成事項

- **小尾巴**：研究文件 `2026-09-09-review-provenance-analysis.md` 兩條延後 nit 已修（:117 完整路徑、:123「紀錄中沒有這項評估」）；上個 session 待刪的審查暫存檔與 `probe.config.toml` 查過已不存在。
- **Identity change 開立**：`openspec/changes/requirement-scenario-identity/`（schema `superpowers-bridge`）。產出 brainstorm（Q1–Q14 決策鏈）、proposal、design（D1–D10）、specs（新 capability `contract-identity` 8 條 REQ；`plan-contract` / `tdd-claim-accuracy` / `tdd-evidence-contract` / `repo-guidance` 四份補號 delta）。`openspec validate --strict` valid。
- **CLI 實測**（scratchpad，openspec 1.3.1）：帶 ID 標題在 validate / archive 下正常；本 repo 實際 specs 一次補號（10 req / 37 scenario）後合併結果逐行一致；**CLI 不擋重號**（同 capability 兩個 `REQ-1` 照樣合併）；spec 層 CLI JSON 不吐標題、只給 `requirementCount` 與 scenarios 陣列。
- **使用者主要裁定**：升 schema major 3（版本號＝相容性邊界、不綁 roadmap）；既有 spec 一次補完、不留 legacy 例外；check 13 為 verify 內 agent 執行的固定判準、不是 executable Gate；本 change 只做「當下就判得出」的身分完整性，退休不重用／歸檔身分消失／scenario 退休格式留到歸檔身分檢查；新號配置分兩層（check 13 只驗「數字且大於目前最大號」，發號須查歷史最大號）；「同一契約」由 OpenSpec 操作角色判定；check 13 以「預演歸檔後」為驗收對象、「歸檔前」為判斷基準；BLOCK 分「違規」與「無法判定」、皆無降級出口（I1 為 Core Invariant）；宣稱邊界 owner 是 `contract-identity` spec，proposal 摘要／design 說理由；proposal 新增 `## Out of Scope`、`## Assurance Boundary` 兩段作 dogfood。
- **TDD applicability 最終採行為判準（Q14）**：第 13 條相關 task 標 `TDD: applicable`（依 2026-09-07 使用者對 fix-v2 的裁定）；只有「舊 verify 判定與新契約不一致」的 fixture 是 TDD subject，RED 必須在改 schema 前實跑；正向範例只作 conformance evidence。§4.3（artifact 類型判準）與 9/07（可觀察行為判準）的落差不在本 change 解決。
- **文件審**：Codex r1 ⛔（2 🔴：遷移指南與全域檢查衝突、TDD 理由與 INDETERMINATE 條款衝突）→ r2 ⛔（1 🔴：REQ-5-S1 殘留）→ r3 `codex_fail`（額度用完，log `You've hit your usage limit`）→ `[REVIEWER_FALLBACK] plane=doc_review from=codex to=contract-neutral-reviewer reason=quota | 2026-09-29T09:04:59Z`（Fable）→ Fable 3 輪皆 ✅ Mergeable（第 1 輪 4 🟡、第 2 輪 3 🟡 經使用者裁定現修；第 3 輪 0 🟡）。sentinel 皆以 `validate-family-sentinel.js doc` 驗過（報告為轉錄檔、原文在背景任務通知），`review-state.js note doc_review pass` 已記。
- work-map：`task-20260929-requirement-scenario-identity` NEXT → DOING。

### 三、未完事項 / 接力棒

- [#接力] **下一步＝寫 tasks.md**（design artifacts 已凍結；除非拆 task 時暴露真正的新設計缺口，否則不重開設計）。tasks 須寫入：
  - **RED 取得必須排在修改 `schema.yaml` 之前**（改了就補不回來）；RED/GREEN 同一 fixture、同一執行方式，唯一變數是第 13 條。「舊 verify 會放行缺 ID fixture」目前仍是推論，由 RED task 實跑確認。
  - 正向 fixture 不記 RED——**刻意與 fix-v2 的 f12 前例（RED `INDETERMINATE`）不同**，D9 已定，tasks 開頭再提醒一次。
  - Q13 兩個實作細節寫進驗收條件：`openspec show <change> --json --deltas-only` 只讀 stdout（stderr 會有 `Warning: Ignoring flags not applicable to change: scenarios`）；change JSON 的情境欄位是 `requirement.scenarios`。
  - **Verification Strategy 試行**（不擴 scope、不改正式契約）：證據分兩條線——regression（RED→GREEN）與 conformance suite（整組正反例＋邊界逐案記 expected / actual）；另記 agent 判錯的型態（規則不清、讀錯狀態、CLI 資料不足、操作對應不清、忽略規則、重跑不一致）。這是實驗性觀察：不修改已凍結的正式設計、不提前實作 executable Gate；完成後以本 change 的實際證據研究「不同 artifact / claim 應採哪種 verification strategy」。**寫 tasks 時待裁**：誰跑 fixture（§4.2「不由 implementer 自我驗收」傾向獨立 subagent）；重跑次數（「2 個獨立執行者各跑 1 次」只是候選，是否為最低成本方案由本次試行驗證，不因外部文章直接定為規則）。
- [#接力] **歸檔後 follow-up（不能放進 tasks）**：`contract-identity` archive 後 `## Purpose` 會是 CLI 產生的 `TBD`，要補正式說明（loosen-plan 前例）。
- [#接力] **延後的 Fable ⚪**：design D9 未寫明與 f12 前例的差異（改在 tasks 開頭提醒）；brainstorm Q8 被推翻的祈使句可加刪除線（紀錄性，不修）。
- [#接力] **Codex 是否補審**：使用者判準＝看 Fable finding 性質；本次都是規格精確度／摘要落差／實證理由，**不需**為此等 Codex。Codex 額度 19:23 恢復。
- [#接力] 新登記研究題 `task-20260929-verification-strategy-research`（work-map，掛主線下）。**外部研究入口**（使用者 2026-09-29 已查核原文；連結與正式引用待研究時補）：
  - Anthropic — Demystifying evals for AI agents（eval 拆成 task / trial / grader / trace / outcome；輸出有變異故同一 task 跑多次 trial；從真實失敗案例建 eval suite）
  - OpenAI — Evaluation best practices（eval-driven development、task-specific eval、持續累積案例、能自動化就自動化）
  - Cucumber — Behaviour-Driven Development（先以具體例子說清 expected behavior，再變成 executable specification）
  - OPA — Policy Testing（declarative policy 另建 policy test cases，驗 allow / deny 結果）
  - （第二級參考：Promptfoo，LLM / agent case suite 與 adversarial cases）
  這些來源支持「案例集、重複 trial、policy / conformance testing」等做法，但**尚未裁定如何映射到 workflow-harness**——它們是研究輸入，不是規範依據。
- [#接力] 使用者待刪（AI 無 rm 權限）：scratchpad `C:/Users/user/AppData/Local/Temp/claude/C--Users-user-orca-openspec-schemas/218f9f89-7661-4111-a7ed-820462929ebc/scratchpad/` 下 `rsi-*`、`run-rsi-*`、`idtest*`、`rsi-preview1`、`expected*.json`。
- [#接力] 未 commit、照舊保留：`backlog-crosscheck-shadow.json`（開工前已修改）、`2026-08-27-brainstorm-產品承諾.md`。

### 四、洞見 / 反省

**【紀律接力】**

- **查「已決」的範圍要含前一個同類 change 的每份 artifact，不只 handoff 與主 spec。** 本次 TDD applicability 在 n/a／applicable 間來回三次，直到寫 tasks 前讀 fix-v2 的 tasks.md 才看到 9/07 使用者裁定；正式設計 §4.3 也是被 Codex 點出衝突後才讀。兩次漏查都是「已寫下、但不在預設查詢範圍」的決定。動作版：動手同類工作前，把上一個同類 change 的 brainstorm／design／tasks 開頭註解列入查已決範圍。attribute：全域 CLAUDE.md「提案前先查已決」＋「宣告不存在前先列舉所有存放處」。

**【當日洞見】**

- `Mergeable` ≠ 所有 finding 都可延後：在 design → tasks 邊界上，會影響 task 推導的 🟡 也現在修；tasks 承接設計、不替設計補洞（例：REQ-6 未寫 CLI 要在暫存複本跑——會成功執行卻比錯對象）。
- D10 分工（spec＝owner、proposal 摘要、design 理由）第一次實跑就抓到 2 次 proposal 摘要落後 owner，都是審查者抓到、不是作者自查。
- 審查者互補再得一例：Codex 抓到跨契約的 TDD 衝突；Fable 讀 CLI 原始碼抓到「MODIFIED 對不回 FROM」的規則缺口並更正 `MAX_DELTAS` 推論理由。累計樣本 3，**Hypothesis**：換審查者本身有增益。
- 外部成熟做法（使用者已查核原文，見三「外部研究入口」）：規則／Skill／policy 用案例集做回歸與符合性驗證，要強制的才升 executable Gate——與本 change 的 regression＋conformance 雙線方向一致；如何映射到 workflow-harness 尚未裁定。

**【學習候選】**

1. **Case**：TDD applicability 來回 Q8 → Q10 → Q11 → Q14，每次推翻都因讀到新的「已寫下的決定」（Codex 引 INDETERMINATE 條款、正式設計 §4.3、9/07 裁定）。
2. **Candidate Pattern**：做判斷前，前一個同類 change 的所有 artifact 都是查已決的範圍。
3. **Evidence**：本次 1 例；全域規則已把「已決事項重問」列為高頻摩擦。**Hypothesis**。
4. **Minimum Sufficient Intervention**：不新增規則——全域「提案前先查已決」已涵蓋，缺的是查詢範圍；先以紀律接力提醒下個 session。
5. **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（6e6b2fb、開工於 2026-09-29T15:04:31）。收工時經 `/smart-commit --execute`（使用者核可）提交三筆：`fae111c`（研究文件 nit）、`b74354a`（Identity change 設計 artifacts，9 檔）、以及收錄本 handoff 與 work-map 的 handoff commit。

- working tree（本 session 改）：`docs/superpowers/research/2026-09-09-review-provenance-analysis.md`（兩條 nit）、`openspec/changes/requirement-scenario-identity/`（新目錄：`.openspec.yaml`、brainstorm、proposal、design、specs × 5）、`workflow-harness/work-map.jsonl`（Identity → DOING、新增研究題）、本 handoff。
- 非本 session、照舊未 commit：`backlog-crosscheck-shadow.json`、`2026-08-27-brainstorm-產品承諾.md`。

### 六、下一步建議

1. 讀本區塊與凍結的四份 artifacts，寫 `requirement-scenario-identity` 的 tasks.md（RED 排在改 schema 之前；納入 Verification Strategy 試行；Q13 兩個實作細節入驗收條件）。
2. 接著寫 plan.md 並進 apply，第一個執行步驟是取得 RED。
3. 追 issue #19（sd0x adapter Windows alloc）有無回應。
