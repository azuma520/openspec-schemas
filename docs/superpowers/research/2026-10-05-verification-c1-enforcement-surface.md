# Verification Strategy C1 第一輪：Enforcement surface 與 execution evidence 現況盤點（2026-10-05）

> **定位**：現況盤點，不是設計、不是提案、不是研究結論。work-map `task-20261005-vs-c1-execution-enforcement` 第一輪的產出；第二輪（work-map `task-20261005-vs-c1-hook-archive-probe`，同日）只補一個實測點，見 §3.4；第三輪（work-map `task-20261006-vs-c1-runtime-execution-record`，2026-10-06）回答 E2 的一個子題，見 §3.5。本文只回答「現在知道什麼」，不回答「要怎麼改」。
>
> **研究問題**（2026-10-05 使用者裁定）：C 原題「Completion Gate 的信任鏈」拆成 C1（required verification 是否真的執行、由誰觸發、漏跑在哪個 state transition 被攔，先做）與 C2（跑過之後的 PASS 值不值得信，延後、不取消，work-map `task-20261005-vs-c2-verifier-correctness`）。本輪只做 C1，不設計 Gate、不讀 OPA。
>
> **三層分開寫**（使用者裁定，全文守住）：**正式流程現在有什麼**／**PoC 證明過什麼做得到**／**正式設計打算做到什麼**。PoC 能做到、設計打算做到的，都不算現況。
>
> **三種內容分開寫**：來源事實（附出處）；本文的整理判斷；推論一律標【推論】。【未查證】＝沒查到或沒實測。版本基準：repo HEAD `93eac9c`；本機全域 OpenSpec 1.3.1；新版對照 OpenSpec 1.14.0。

---

## §0 讀了什麼

| 材料 | 讀法 |
|---|---|
| 方向文件 `../specs/2026-08-27-bridge-guarantee-architecture-direction.md` | 全文 |
| 正式設計 `../specs/2026-09-01-bridge-guarantee-formal-design.md`（現行核可版 `8002fa0`） | 全文 |
| 需求追溯現況 `./2026-09-23-requirement-traceability-current-state.md` | 全文 |
| traceability-gate PoC `../poc/2026-08-28-traceability-gate/` | `poc-report.md`、`phase1-core-results.md`、`step0-capability-inventory.md`、`gate_check.py` 全文；未重跑 |
| capability spike `../poc/2026-09-01-capability-spikes/spike-report.md` | 只以關鍵字（archive、hook、provenance 等）搜尋後讀命中段 |
| issue #2 相容性 spike `../poc/2026-10-02-issue2-compat-spike/report.md` | 以關鍵字（archive、hook、version 等）搜尋後讀命中段 |
| `superpowers-bridge/schema.yaml` | verify PRECHECK、check 13（含 13.G）、ENFORCEMENT BOUNDARY of checks 8-12、FRESHNESS 段、retrospective PRECHECK、apply 步驟 3–6 |
| OpenSpec 1.14.0 原始碼 | 本機 npx 快取的 `@fission-ai/openspec@1.14.0` `dist/`：關鍵字搜尋 `post_apply`／`preArchive`／`hook`／`lifecycle`，並讀 `core/archive.js` 的未完成 task 檢查段 |
| 本機 hook 設定 | `~/.claude/settings.json` 的 `hooks`；`~/.claude/plugins/cache/` 下各 plugin 的 `hooks/hooks.json`；本 repo `.git/hooks/` |
| Orca CLI | `orca --help` 的指令清單（未讀各指令文件） |
| C 的證據整理 | 一個唯讀 subagent 依 A 文件、起點備忘、盤點表與其引用的原始紀錄整理；主 session 抽查 5 處引文與原文相符（schema.yaml 13.G、verify PRECHECK、ENFORCEMENT BOUNDARY、正式設計 §8 第 4–6 條、Identity ledger 第 84 行），其餘未逐筆覆核 |

---

## §1 現況三層

### 1.1 正式流程現在有什麼

**對「必要 verification 是否已執行」，正式流程在 change 層級沒有任何機械檢查。** 例外與相鄰的機械檢查只有下面幾項，都不檢查 verification：

- CI（`validate-schemas.yml`）只驗 schema 檔本身的結構，不碰任何 change（repo `CLAUDE.md`「沒有 build / test / lint」節）。
- `openspec archive` 自己會驗 delta spec 能否合併，不能合併就中止（issue #2 spike O18：1.3.1 中止時 exit 0、1.14.0 改回 exit 1）。這是 spec 結構的檢查，不是 verification 的檢查。
- `openspec archive` 對未完成 task：1.3.1 只警告（方向文件 §6#6）；1.14.0 在非互動、未加 `--yes` 時會擋（`core/archive.js` 拋 `archive_tasks_incomplete`，約第 1279–1303 行），加 `--yes` 只印警告後繼續。**bridge apply 步驟 5 寫的就是 `openspec archive -y`**，所以這道檢查在 bridge 流程裡被跳過。

verification 本身的執行全部是文字要求，由 agent 照做：

| 環節 | 載體 | 誰執行 | schema 自述的邊界 |
|---|---|---|---|
| 觸發 verify | apply 步驟 3「When all tasks are done, produce the `verify` artifact…」 | agent 照文字 | — |
| verify 開跑前檢查 | verify PRECHECK：commit 數 > 0、`- [x]` 數 > 0 | agent 照文字 | commit 數只證明分支上有任意 commit（F-RS7，見 §2） |
| checks 1–12 | verify instruction | agent 照文字 | 「If the verify agent does not execute one of them, no mechanism in this schema intercepts the omission; review of verify.md is the only backstop.」（ENFORCEMENT BOUNDARY） |
| check 13 | verify instruction | agent 照文字 | 「It is NOT a non-bypassable executable gate … nothing in this schema intercepts the omission.」（13.G） |
| 結果過期 | FRESHNESS 段 | agent 照文字 | 「Nothing in this schema detects a stale result — there is no digest of the checked state」 |
| retrospective 開跑前檢查 | 只檢查 verify.md 恰好勾一格且不是 FAIL | agent 照文字 | 不管這個 PASS 怎麼來的 |
| archive | apply 步驟 5 文字 | agent 照文字跑 CLI | CLI 會檢查 proposal.md（非阻擋警告）、驗 delta specs、看 task 進度，但不檢查 verify／retrospective 的完成狀態或任何 Verification Result／Gate PASS，見 §3.1 |

### 1.2 PoC 證明過什麼

`gate_check.py`（throwaway，2026-08-28）證明了：給定 `tasks.md` 的 `- Contracts:` 標註與 `verification-results.json`，可以**機械判定每條 requirement** 有沒有 task 承接、有沒有結果、有沒有 FAIL、PASS 與 FAIL 是否並存、evidence 是否為空；壞引用 exit 2；10 個變異測試都轉紅（`phase1-core-results.md`）；並在一個真實 change（`claude-md-phase-boundary`）上 PASS（`poc-report.md`）。

**`gate_check.py` 證明的是 feasibility，不是現行保證。** 它沒有接進任何流程（要人手動呼叫），正式 bridge 也沒有引用它（9/23 現況研究 §1「Completion Gate｜只有 PoC throwaway `gate_check.py`」）。它也沒有證明下面這些：

- 驗證真的執行過：status／evidence 由 agent 寫（`poc-report.md` 宣稱邊界）。
- freshness。
- Scenario 層 coverage：它的 coverage 以 Requirement 為單位。
- BLOCKED 狀態：只收 PASS／FAIL。
- method 欄位。

### 1.3 正式設計打算做到什麼

- Gate 由 Harness 機械判定，不是 Agent prompt（§7、方向文件護欄 5）。
- 綁定點：tasks 全 `[x]` → 跑 Gate → Gate PASS＝Change Complete → 才可 archive（§7、方向文件 §6#6）。
- archive 時要**機械確認存在 FRESH 的 Gate PASS**。`gate-pass.json` 這類檔案「是稽核紀錄，不是通行證」，因為 Agent 也寫得出 `"status": "PASS"`（§7、spike S5）。
- freshness 以 coarse digest 判定（§6）；I6 以每個必要 Scenario 的有效判定為單位（§2.1）。
- **宿主與呼叫方式未定**：「具體宿主與呼叫方式屬實作」（§7 實作歸屬）。查了正式設計 §7、spike 報告 S5、方向文件 §6#6，都沒有指定由誰在 archive 前攔下。handoff 未查。

---

## §2 C 的兩個子問題

### (a) Enforcement：該跑的驗證有沒有真的跑、漏跑會不會被攔

- 正式流程：見 §1.1。唯一後盾是審查 verify.md（schema 原文）。
- 實際發生過的「跑得比宣稱少而且沒被記下」只找到一筆：A8，Codex 補審原本要跑全量 pytest，因唯讀沙箱建不了暫存目錄，改成只跑 140 條，帳本沒記範圍縮小（A 文件 §1 A8；subagent 回原始 rollout 核對）。
- 「漏跑整個 check、事後才發現」的原始紀錄：在 A 文件、盤點表、兩份 retrospective 裡都沒找到。

### (b) Reliability：跑出來的 PASS 值不值得信

- PASS 現在依賴：agent 照文字執行 check；實作者自己寫的測試（checks 8–11 只驗 RED/GREEN 紀錄存在、結構對，ENFORCEMENT BOUNDARY 第三點）；審查層（Codex 或 fallback reviewer）；開發機環境，沒有環境紀錄。
- 正式設計明列**不保證**：Reviewer／Verification 判斷正確（§8#4）、Evidence 為真（§8#5）、digest 以外的執行環境（§8#6）、驗證材料的內部覆蓋（§8#9）。Gate「不判語意充分性」（§4.2）。依設計，(b) 交給 review 層。
- 有案例的風險（A 文件 §2，`4a45721` 版計數）：① 只驗了比 claim 窄的代替品，2 對 3；② 執行環境偏差，1 對 1；③ 輸出格式表達不出需要的區分，1 對 1，而且成不成立取決於怎麼分類。**全部在完成前就被抓到，沒有假 PASS 一路走到 archive 的實例**。

### 設計內部張力（C1 的決策背景，不另立工作）

**產品承諾要求「必要 verification 已實際執行」，但目前設計允許 execution result／evidence 由 Agent 自陳，而正式流程又沒有機械方式確認 verification 真的發生。**

- 承諾端：方向文件 G2「必要 verification 已實際執行並取得可接受結果」；§1.1 核心句「未完成必要驗證的工作，不得被宣稱為完成」。
- 設計端：正式設計 §8#4「Harness 保證這些檢查被要求、被執行、被記錄與處置」；同節 §8#5「status/evidence 在 v1 可由 Agent 寫出」。
- 【推論】依 §8#5 與 PoC 宣稱邊界，v1 Gate 實際能判定的是「存在結構合格、仍 FRESH 的執行紀錄」；紀錄是否屬實落在 review 層。所以 §8#4 的「被執行」在 v1 撐不住字面意思。(a)/(b) 的分界在「驗證真的跑過嗎」這一格上不乾淨。
- 後續可能的產品決策方向包括補機制、收窄承諾，或其他方向（例如承諾拆層）；**本研究不預設結論**。收窄承諾動到的是 G2 與整條 `Guarantee → Completion Contract → Verification → Gate` 的推導，屬產品承諾層級的決策，不是 §8 的措辭修正。

---

## §3 C1 第一輪查證

### 3.1 新版 OpenSpec 有沒有改變 8/28 的限制

**基本上沒變。** 方向文件 §6#6（讀 1.3.1 原始碼）的結論是：OpenSpec 沒有 Change Complete 狀態，archive 是收檔不是驗收，沒有 post_apply hook。對照 1.14.0：

- 在 1.14.0 `dist/` 搜 `post_apply`、`postApply`、`pre_archive`、`preArchive`、`hook`、`lifecycle`：沒有任何 archive 或 apply 的 hook；唯一命中「lifecycle」的是 UI 輸入處理、`store` 指令與 onboarding 說明文字。`core/project-config.js`、`config-schema.js`、`global-config.js`、`change-status-policy.js` 沒有使用者可定義的 hook 或指令。
- archive 的未完成 task 檢查變嚴，但 `--yes` 可以跳過（§1.1），bridge 用的正是 `-y`。
- 1.13.1 起 `[~]` 也算未完成（issue #2 spike O9）。
- 1.14.0 的 verify skill 會把未完成 task 列為 CRITICAL（spike O12）。這是給 agent 的 prompt，不是 CLI 層的阻擋。
- 本文**沒有**逐檔讀 1.14.0 原始碼，只做了上述關鍵字搜尋，並讀了 archive 的 task 檢查段。

### 3.2 OpenSpec 以外既有的 enforcement surface

| 載體 | 現況（事實） | 能不能在 archive 前擋（E1） | 能不能證明驗證真的跑過（E2） | 限制 |
|---|---|---|---|---|
| Claude Code PreToolUse hook | 本機已有 hook 用 `permissionDecision: deny` 或 exit 2 擋下工具呼叫，例如（非完整盤點）：`~/.claude/hooks/guard-silent-traps.py`（Bash）、workflow-harness `backlog_write_guard.py`（Edit/Write）、sd0x 5.0.0 `pre-bash-codex-launch-guard.sh`（Bash） | **第二輪已實測（§3.4）**：可攔直接的 archive 呼叫，四種啟動設定（對應 default、auto、bypassPermissions 三種 runtime 權限模式）都攔住；受測形式可被間接執行繞過，且有誤擋 | 單靠攔 archive 指令不能證明 E2；hook 本身可讀工具輸入、cwd 與檔案（`backlog_write_guard.py` 會讀 backlog 並模擬修改後內容再判定），但這些既有 guard 都沒有建立 verification 執行證據 | 只在裝了 hook 的 Claude Code session 生效；使用者在自己終端機跑會繞過；字串比對可能被繞過或誤擋（sd0x 該 guard 的註解記錄過 regex 的誤擋與漏擋；§3.4 實測兩者都出現） |
| sd0x review-state／tree digest | 提醒層，設計上 nothing blocks（`.claude/rules/auto-loop.md` § Enforcement） | 不能 | 部分：precommit runner 會自己記錄結論（由執行器記帳）；review 結論由 agent 以 `note` 記下 | 正式設計 §7 已指定借它的 durable state／digest |
| Orca orchestration | `orca --help` 列出 decision gate（`gate-create`／`gate-resolve`）、supervised worker（`worker-read`；`worker-release` 會先封存輸出）、dispatch | 只擋 orchestration task，不擋 archive | 第三輪文件分析（§3.5.1）：`worker-read` 優先讀 provider 自己的對話紀錄，沒有就讀終端機輸出，不另外產生獨立紀錄；可當弱證據，不構成新的 trust boundary。S6 已實測 review／implementation 兩類 dispatch 的身分可區分 | decision gate 的 `--from` 是自報（正式設計 §2.3）；Orca 不是 hard dependency（G3） |
| git hooks | 本 repo `.git/hooks/` 只有 sample，沒有安裝任何 hook；sd0x `pre-push-gate.sh` 在 `.claude/scripts/`，需另外選擇安裝 | 可以擋 commit／push（archive 結果要 commit 才進版控）【未實測】 | 不能 | 可用 `--no-verify` 跳過；只在本機 |
| CI（GitHub Actions） | 只跑 schema validate 與 version-check | 擋不到本機的 archive；能不能擋 merge 取決於 branch protection【未查】 | 對可由程式重跑的驗證可以：在獨立環境重跑 automated-test，不必相信 agent 自陳【推論，未實作未實測】 | inspection、analysis、manual-demonstration 未必能以程式自動重算 |

### 3.3 E1／E2：「required verification 確實執行」是兩個 claim

- **E1：Gate 是否在關鍵 transition 前真的跑過並 PASS。** §3.2 有可掛的載體（PreToolUse、git hook、CI），但每一種都只罩得住一部分範圍，也都可能被人在流程外繞過。問題在範圍與繞過，【推論】不在「有沒有地方可掛」。其中 PreToolUse 已在第二輪實測（§3.4）：攔得住直接呼叫，也測到流程內的間接執行繞過。
- **E2：Gate 依賴的 verification 本身是否真的執行過。** 可達到的強度與驗證類別（正式設計 §4.2 的 method 封閉集）有關，至少取決於能不能由程式獨立重算：
  - `automated-test`：可由程式在獨立環境自動重跑（CI），或由執行器自己記錄輸出（sd0x precommit runner 的做法），不必依賴 agent 自陳。
  - `inspection`、`analysis`、`manual-demonstration`：未必能以程式自動重算（正式設計 §4.2 所稱「能重算」限程式重算）。可以由獨立執行者重新檢視、分析或操作，但那是一次新的執行；能否取得可信的執行紀錄，要依具體 procedure 與 runtime 判定（第三輪 §3.5：關鍵在紀錄有沒有離開受觀察 agent 寫得到的範圍；外送遙測的內容可判別性已實測成立，trust boundary 只有文件支持）。沒有這類紀錄時，紀錄仍是執行者自陳。
  - 要分清楚三件事：程式重算、重新執行一次驗證、證明某次歷史執行確實發生。
- **E2 按驗證類別分層目前只是觀察，不是產品決策。** 它和 §2「設計內部張力」裡的承諾拆層方向有關，但要不要往那裡走，由使用者決定。

### 3.4 第二輪實測：PreToolUse hook 攔 `openspec archive -y`（E1 可行性）

**要證明的 claim**：在專案自己的 `.claude/settings.json` 掛一個 PreToolUse hook，真實的 Claude Code session 透過 Bash 工具執行 `openspec archive … -y` 時，hook 會攔下來，change 不會被收檔。只證明「攔得到」；攔下來之後有沒有東西判 PASS 不在範圍內（正式 Gate 不存在）。

**做法**（證據包：`./evidence/2026-10-05-c1-hook-archive-probe/`，`PROVENANCE.md` 記來源、雜湊、重現方式）：

- 在 session scratchpad 建暫存測試專案，hook 只放在該專案的 `.claude/settings.json`；全域 `~/.claude` 與本 repo 都沒動。
- 受測 hook：matcher `Bash`，用 regex 比對指令字面裡 `openspec … archive`，命中就回 `permissionDecision: deny`。這是刻意簡單的偵測器，目的是量出會漏什麼，不是做到完美。
- 每一案三個判準：(a) 檔案系統——change 目錄還在、`archive/` 沒有新項目；(b) hook 紀錄多一行；(c) 工具結果顯示被拒、`permission_denials` 有該呼叫。
- 先跑**對照組**（拿掉 hook）：archive 必須成功、判準 (a) 必須讀到「已收檔」。對照組沒成功就代表判準分不出「攔住」和「fixture 壞掉」。
- Layer 1 把 18 個指令直接餵給 hook 腳本，只測偵測器；Layer 2 在測試專案裡跑巢狀 `claude -p`，測真實 runtime。
- 環境：Claude Code 2.1.289、OpenSpec 1.3.1、Python 3.13.5、Windows 11。

**證據分三級**：

| 級別 | 結果 |
|---|---|
| **主 session 親自重跑確認** | ① 對照組（無 hook、bypass 模式）：archive 成功，change 被搬進 `archive/2026-10-05-probe-x`（`logs/main-ctrl-bypass.*`）。② 掛 hook、bypass 模式：change 沒被收檔，hook 紀錄一行 `deny`，工具結果為 `PreToolUse:Bash hook error: C1-PROBE…`、`permission_denials` 含該呼叫（`logs/main-h-bypass.*`）。③ 把 `C=archive; openspec $C probe-x -y` 與 `bash a.sh` 直接餵給 hook：判為放行；`echo "openspec archive"`：判為拒絕（`hook.log` 最後三行） |
| **subagent 單次回報，主 session 未端到端重跑**（每案 1 次） | ① 對照組在 bypass／default／未指定（全域預設 auto）三種模式都收檔成功。② 掛 hook 後在四種啟動設定都沒收檔，各有一行 `deny`：`--permission-mode default`、未指定（全域預設 auto）、`--permission-mode bypassPermissions`、`--dangerously-skip-permissions`。後兩者 runtime 回報的權限模式都是 `bypassPermissions`，所以實際涵蓋三種權限模式。③ hook 的 deny 蓋過全域 `permissions.allow` 的 `Bash(*)`。④ 實際收檔成功的繞過：agent 先用 Write 工具把 archive 指令寫進 `a.sh` 再 `bash a.sh`（hook 只看到 `bash a.sh`，Write 那一步不經 `Bash` matcher）；以及 `C=archive; openspec $C probe-x -y`。⑤ Layer 1：14 個應擋的寫法漏 4 個（腳本檔、變數藏子指令、變數藏執行檔、`arch''ive`），4 個無害指令誤擋 1 個（`echo "openspec archive"`）；`mv …/archive/…` 與 `node …/openspec.js archive` 被擋只是路徑字面剛好含 `openspec` 與 `archive`。⑥ 被拒後，巢狀 agent 兩次都沒有自己改走別的路（其中一次 prompt 明說「被擋就試別的方法」，agent 讀了 `.claude/settings.json` 後拒絕繞過） |
| **未測** | hook 當掉或逾時、改用 exit 2 擋、互動 session、會真的跳權限詢問的情境（全域允許 `Bash(*)`，default 模式實際沒有詢問）、Agent SDK 與 subagent、`settings.local.json` 與 managed settings、`/opsx:archive` 完整流程、agent 改 settings 把 hook 拿掉、PowerShell 與 MCP 工具、重複執行；也沒讀 Claude Code 官方文件對 hook 與權限模式關係的說明 |

**判讀**：

- **E1 的 feasibility 從推測變成有實驗支持**：PreToolUse hook 可以當 archive 前的攔截點，而且在本機測到的三種 runtime 權限模式（default、auto、bypassPermissions）下都會觸發（bypassPermissions 經主 session 重跑；default、auto 與 `--dangerously-skip-permissions` 啟動的那一案為單次回報）。
- **強度有限**：本次受測的形式（`Bash` matcher＋指令字面比對）提供的是 **direct-path enforcement**——擋得住照流程或不小心直接跑的 archive；它**不構成不可繞過的 archive boundary**：間接執行（腳本檔、變數）實際繞過，另有誤擋，再加上 §3.2 已列的「使用者在自己終端機跑」這條 session 外的路。
- 【推論】要補上漏洞，得換別的層，例如檢查 Write／Edit 寫進檔案的內容、包住 `openspec` 執行檔、或事後檢查 `openspec/changes/archive/` 的異動；這些都沒測。
- 【推論】「被拒後 agent 沒繞路」反映的是載入使用者全域設定與 plugin 的這個環境、每案 1 次，不能當成模型的穩定行為，也不能拿來支撐 enforcement 強度。
- 觀察限制：stream-json 在 PreToolUse hook 執行時不送事件（只有 SessionStart 有），所以 hook 有沒有跑，直接證據只有 hook 自己寫的紀錄檔。

### 3.5 第三輪：由系統自動保存的執行紀錄能否分辨「真的做了」與「只宣稱做了」（E2）

work-map `task-20261006-vs-c1-runtime-execution-record`（2026-10-06 使用者拍板）。

**研究問題**：受觀察 agent 之外自動保存的 execution events，能否區分「required verification actions 真正發生」與「agent 僅宣稱發生」？目標是**通用判準**，Claude Code、Orca 只是拿來驗證判準的實例；產品名不進判準。

**邊界**（使用者拍板）：

- 紀錄裡看得到讀檔等工具呼叫，最多只等於「required execution actions 有發生」，**不等於人工檢查完成**；檢查判得對不對屬 C2。
- 不設計 Gate、不改 schema、不寫 README。
- 保證強度要按**驗證類型**分，不按整體環境分（例如 CI 只強化程式測試，對人工檢查無幫助）。

**判準**（四條，開讀前定）：① 紀錄由 runtime 寫入，不是 agent 自述；② 對得回哪一次執行；③ 看得出某件事**沒有**發生；④ 受觀察 agent 改不到紀錄。

**結論分類**（開跑前凍結，取最嚴格版本）：**可行**＝T1 與 T2 都實測成立；**部分可行**＝T1 實測成立、T2 只有文件支持；**不足**＝T1 實測不成立。T1＝內容可判別性（事件能否分出讀過／沒讀）；T2＝trust boundary（紀錄送出後 agent 改不到）。

#### 3.5.1 文件層：三個候選對照判準

| 判準 | Claude Code 本機對話紀錄 | Orca worker 輸出擷取 | Claude Code 遙測匯出（OpenTelemetry） |
|---|---|---|---|
| ① runtime 寫入 | 有工具呼叫的輸入與結果（本機實物：`tool_use`、`toolUseResult` 欄位） | 不另寫一份：`worker-read` 說明原文為 "The default auto source uses an exact hook-reported transcript when available and otherwise returns labeled terminal output."（`orca orchestration worker-read --help`，Orca 1.4.220）；完成回報 `worker_done` 由 worker 自己發（`orca skills get orchestration`） | 每次工具執行一筆 `claude_code.tool_result`（monitoring-usage 文件） |
| ② 對應哪次執行 | session id、`parentUuid` 串接 | Dispatch ID；說明明寫 lifecycle authority 不以 provider transcript 為準 | `session.id`、`prompt.id`、`tool_use_id`（可與 hook 輸入的 `tool_use_id` 對上，monitoring-usage 文件） |
| ③ 看得出沒做 | 【未實測】 | 同左 | 本輪實測，見 §3.5.2 |
| ④ agent 改不到 | **不成立**：檔案屬同一個 OS 帳號（本機 `rw-r--r--`）；官方文件只說格式為內部、每版可能變，沒有任何完整性保護的說明（sessions 文件） | **不成立**：讀的是左欄那份紀錄；封存位置與權限【未查證】 | **文件支持、未實測**：事件送到外部收集端後不在 agent 寫入範圍；管理員可用 managed settings 設定 `OTEL_EXPORTER_OTLP_*`，Claude Code 啟動時移除衝突的開發者設定（monitoring-usage 文件） |

**整理判斷**：有區別力的性質不是「有沒有紀錄」，而是**紀錄有沒有離開受觀察 agent 寫得到的範圍**。本機紀錄（含 Orca 讀到並封存的那份）在「未被竄改」的前提下能證明工具呼叫發生過，**可當弱證據，不足以支撐「不必相信受觀察 agent」的強 claim**；Orca 沒有形成新的 trust boundary，以文件分析收掉、不另實測。

#### 3.5.2 實測：遙測事件的內容可判別性（T1）

**做法**（證據包：`./evidence/2026-10-06-c1-telemetry-execution-probe/`，`PROVENANCE.md` 記來源、雜湊、prompt 原文與重現方式）：

- 暫存測試專案放 `a.md`、`b.md`、`c.md`（指定要讀）與 `decoy.md`（誘餌）；Claude Code 2.1.290 以環境變數把 OTel logs 用 http/json 送到本機收集端，`OTEL_LOG_TOOL_DETAILS=1`。全域設定與本 repo 都沒動。
- 判讀腳本只看遙測事件：同一 session 中三個指定檔都有成功的 `Read` 工具結果才判 `READ_ALL`；有事件但缺任一檔判 `NOT_READ`；該 session 沒有任何事件判 `NO_EVENTS`（**沒有遙測不等於沒讀**，所以與 `NOT_READ` 分開）。
- 開跑前先用假事件自檢，證明判讀分得出對錯；看過真實資料後腳本有改，改完重跑全部假事件（見「判讀腳本的版本」）。

**證據**（全部由主 session 執行，各 1 次）：

| 案 | agent 實際做的事 | agent 最後的輸出 | 遙測判讀 |
|---|---|---|---|
| 假事件 8 組 | — | — | 讀全 2 組 → `READ_ALL`；無工具結果、讀誘餌、讀取失敗、只在 Bash 字串出現檔名、相似檔名 5 組 → `NOT_READ`；只有別的 session 1 組 → `NO_EVENTS`，全符合預期 |
| 正向 | 讀了 a、b、c（遙測 3 筆 `tool_result`／`Read`，主 session 看過原始事件） | 一致性判斷＋`VERDICT: PASS` | `READ_ALL` |
| 反向一 | 沒讀 | 拒絕照抄假宣稱 | `NOT_READ`（0 筆工具結果） |
| 反向二（對照組） | 沒讀 | **`VERDICT: PASS - I reviewed a.md, b.md and c.md …`** | `NOT_READ`（0 筆工具結果） |

**判讀腳本的版本**：開跑前版本從 `tool_parameters` 取參數；讀檔路徑實際在 **`tool_input`**，v1 因此把真實正向判成 `NOT_READ`。這是**本研究讀錯欄位**，不是文件有誤：monitoring-usage 文件的 Tool result 事件段寫明 `tool_input`（`OTEL_LOG_TOOL_DETAILS=1` 時）帶檔案路徑等工具參數、適用所有工具，`tool_parameters` 只帶 Bash 指令、MCP 與 skill 名稱等特定工具摘要；當時是透過摘要工具讀文件，摘要漏了 `tool_input`（2026-10-06 下載原文確認）。改成讀 `tool_input`、解析 `file_path` 後以檔名完全比對，重跑假事件（新增 `tool_input` 形與相似檔名兩組）全符合後，才判讀真實 session。兩版都在證據包內。

**其他觀察**（來源事實）：使用者 prompt 與 assistant 回覆在事件中為 `<REDACTED>`，所以遙測只呈現**動作**，不含 agent 的宣稱內容——宣稱要從最終輸出取，兩者天然分開；每筆事件都帶帳號屬性（email、account id 等），證據包已刪除。

**判讀**：

- **T1：實測成立。** 在本次形式下，遙測事件分得出「三檔都讀過」與「沒讀卻宣稱 PASS」。
- **T2：文件支持、未實測。** 本輪的收集端在本機、同一帳號，agent 理論上碰得到，所以本輪**沒有**實測防竄改。
- **依凍結的分類：部分可行。**
- 本輪結論的範圍限制：
  - 判準把「必要動作」定義為 `Read` 工具成功讀取指定檔；依腳本邏輯，agent 若用 Bash `cat` 讀檔，會被判 `NOT_READ`（假陰性；未以假事件或實測驗證——`neg_otherreader` 假事件只驗了「Bash 指令字串裡出現檔名不算讀檔」，它用的是 `echo`）。「哪些動作算數」屬之後的產品／Gate 規則。
  - 每案 1 次、單一 runtime（Claude Code 2.1.290、Windows）、巢狀 `claude -p`；互動 session、subagent、長 session 的事件完整性未測。
  - 文件寫明 `tool_input` 單一值超過 512 字元會截斷、整體上限約 4K 字元；本輪路徑都短，未遇到。路徑過長時檔名可能被截掉，判讀會失準。
  - 【推論】收集端若不驗證來源，agent 可以自己往收集端送假的 `Read` 事件——這是 T2 的一部分，不是 T1；收集端要能辨認事件來源，本輪沒查。

---

## §4 Gap map

| 項目 | 正式流程（現在） | PoC | 正式設計 | 歸類 | 案例 |
|---|---|---|---|---|---|
| 1 必要結果齊不齊、PASS 與否（Requirement 層） | 無機械檢查；verify checks 為文字 | 證過 | §7、I6 | 只有設計＋PoC，未實作 | 無假 PASS 穿透實例 |
| 2 Scenario 層 coverage | 無 | 未證（PoC 以 Requirement 為單位） | I3、§4.2 | 只有設計 | — |
| 3 結果 freshness | 文字要求，無 digest | 未證 | §6、§7 | 只有設計 | 無實例 |
| 4 archive 須有 FRESH Gate PASS | CLI 不檢查 verify／retrospective 完成狀態、Verification Result 或 Gate PASS；bridge 用 `-y` | 未證；候選宿主 PreToolUse 已實測攔截點（§3.4），強度只到 direct-path | §7 invariant；宿主屬實作 | **真缺口：宿主未定** | — |
| 5 Gate 由誰觸發 | verify 由 apply 步驟 3 文字觸發 | 人工呼叫 | 綁定點已定，宿主屬實作 | **真缺口**（與 4 同源） | — |
| 6 驗證真的執行過的證明（E2） | 無 | 未證（宣稱邊界明示） | §8#5 明說 v1 不保證；machine-captured output 只說「較強 provenance」，沒有載體設計 | **真缺口**（設計自認），可達強度依 method 分層；候選載體（外送遙測）T1 實測成立、T2 只有文件支持（§3.5，部分可行） | A8 一筆 |
| 7 verify 執行者獨立性的 provenance | 無 | — | §2.2 列 degradable；verify 階段載體未實測（§9.2） | 設計內已知的前置確認項 | — |
| 8 驗證工具判得對不對（①） | 審查層 | — | §8#4、§8#9 不保證 | **刻意不保證**（C2） | 2 對 3 |
| 9 執行環境（②） | 無環境紀錄 | — | §8#6 不保證 | **刻意不保證**（C2） | 1 對 1 |
| 10 結果格式表達力（③） | verify.md 三選一勾選 | 只有 PASS／FAIL | Gate 層有 BLOCKED 規則（§6） | Gate 層部分回答；驗證工具層無（C2 候選） | 1 對 1 |

「已實作」一欄沒有任何項目落入：checks 8–13 已實作，但都是 agent 執行的文字，對應的機械版本屬第 1、3 列。

---

## §5 未查證／下一輪候選

**未查證**（本輪不補，避免無限延伸）：

1. ~~沒實測 PreToolUse hook 攔 `openspec archive -y`。~~ 第二輪已實測，見 §3.4；該節「未測」一列是它自己的剩餘邊界。
2. ~~沒讀 Orca 對 supervised worker 輸出封存的文件，也沒實測它能不能當證據。~~ 第三輪已讀 CLI 說明與 orchestration 說明（§3.5.1），以文件分析收掉、不另實測；封存位置與權限仍未查。
3. 沒查 GitHub branch protection。
4. 沒讀 Claude Code hook 文件裡對繞過情形的說明。
5. OpenSpec 1.14.0 只做了關鍵字搜尋，加上讀 archive 的 task 檢查段。
6. spike S1–S4 的細節、handoff、workflow-harness 那邊都沒讀；`gate_check.py` 沒重跑。
7. C 證據整理的 subagent 自述未讀：`blind-kit/v2/FROZEN.md`、Identity verify 腳本、workflow-harness 的 `CH/verify.md` 等。
8. （第三輪）**誰核對執行紀錄**：agent 指出紀錄在哪，不等於紀錄已被獨立核對；核對者若仍是同一個 actor，assurance 沒有增加。屬 Gate 設計，本研究不處理。
9. （第三輪）T2 未實測：外送後 agent 改不到、managed settings 蓋掉開發者設定，都只有文件支持；收集端能否辨認事件來源（防 agent 自己送假事件）沒查。
10. （第三輪）第二個 runtime：Codex 等其他 agent runtime 有沒有同等的執行事件外送，沒查。結果正面之後再做文件層對照，用來驗證判準的泛用性。
11. （第三輪）下游用途，不登記工作：README／教學將來可說明「要較強的完成保證，執行環境需具備哪些能力」，寫法是「驗證類型 × 環境能力 → 可支撐的保證」，產品名只當例子；順序是研究站住 → 正式設計吸收 → 才更新文件。

**下一輪候選**（使用者 2026-10-05 傾向；後於同日拍板，第二輪已完成，結果見 §3.4）：只挑一個最能增加決策資訊的點，**實測 PreToolUse hook 能不能在真實流程裡可靠攔下 `openspec archive -y`**，直接回答 E1 的可行性。兩個前提：

- 在暫存的測試專案裡做，不裝進日常環境。
- 這只能證明「攔得到」，不能證明「攔下來之後有東西可以判 PASS」，因為正式的 Gate 程式還不存在。

做法 4（prospective validation）的兩個未決題（選哪個真實 change、四欄紀錄放哪裡）同樣等之後再決定。Identity change 曾否決「本版就寫一支像 `gate_check.py` 的腳本」（理由是會長成半套 traceability system，見 `openspec/changes/archive/2026-10-01-requirement-scenario-identity/design.md`），之後若要談 Gate 實作，這筆否決要一起帶上。
