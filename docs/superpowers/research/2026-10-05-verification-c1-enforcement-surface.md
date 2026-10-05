# Verification Strategy C1 第一輪：Enforcement surface 與 execution evidence 現況盤點（2026-10-05）

> **定位**：現況盤點，不是設計、不是提案、不是研究結論。work-map `task-20261005-vs-c1-execution-enforcement` 第一輪的產出。本文只回答「現在知道什麼」，不回答「要怎麼改」。
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
| Claude Code PreToolUse hook | 本機已有 hook 用 `permissionDecision: deny` 或 exit 2 擋下工具呼叫，例如（非完整盤點）：`~/.claude/hooks/guard-silent-traps.py`（Bash）、workflow-harness `backlog_write_guard.py`（Edit/Write）、sd0x 5.0.0 `pre-bash-codex-launch-guard.sh`（Bash） | 【未實測】有可攔截工具呼叫的既有機制；**尚未實測拿來攔 `openspec archive`** | 單靠攔 archive 指令不能證明 E2；hook 本身可讀工具輸入、cwd 與檔案（`backlog_write_guard.py` 會讀 backlog 並模擬修改後內容再判定），但這些既有 guard 都沒有建立 verification 執行證據 | 只在裝了 hook 的 Claude Code session 生效；使用者在自己終端機跑會繞過；字串比對可能被繞過或誤擋（sd0x 該 guard 的註解記錄過 regex 的誤擋與漏擋） |
| sd0x review-state／tree digest | 提醒層，設計上 nothing blocks（`.claude/rules/auto-loop.md` § Enforcement） | 不能 | 部分：precommit runner 會自己記錄結論（由執行器記帳）；review 結論由 agent 以 `note` 記下 | 正式設計 §7 已指定借它的 durable state／digest |
| Orca orchestration | `orca --help` 列出 decision gate（`gate-create`／`gate-resolve`）、supervised worker（`worker-read`；`worker-release` 會先封存輸出）、dispatch | 只擋 orchestration task，不擋 archive | 【未實測】supervised worker 的輸出由 runtime 擷取，是否可當證據未查；S6 已實測 review／implementation 兩類 dispatch 的身分可區分 | decision gate 的 `--from` 是自報（正式設計 §2.3）；Orca 不是 hard dependency（G3） |
| git hooks | 本 repo `.git/hooks/` 只有 sample，沒有安裝任何 hook；sd0x `pre-push-gate.sh` 在 `.claude/scripts/`，需另外選擇安裝 | 可以擋 commit／push（archive 結果要 commit 才進版控）【未實測】 | 不能 | 可用 `--no-verify` 跳過；只在本機 |
| CI（GitHub Actions） | 只跑 schema validate 與 version-check | 擋不到本機的 archive；能不能擋 merge 取決於 branch protection【未查】 | 對可由程式重跑的驗證可以：在獨立環境重跑 automated-test，不必相信 agent 自陳【推論，未實作未實測】 | inspection、analysis、manual-demonstration 未必能以程式自動重算 |

### 3.3 E1／E2：「required verification 確實執行」是兩個 claim

- **E1：Gate 是否在關鍵 transition 前真的跑過並 PASS。** §3.2 有可掛的載體（PreToolUse、git hook、CI），但每一種都只罩得住一部分範圍，也都可能被人在流程外繞過。問題在範圍與繞過，【推論】不在「有沒有地方可掛」。
- **E2：Gate 依賴的 verification 本身是否真的執行過。** 可達到的強度與驗證類別（正式設計 §4.2 的 method 封閉集）有關，至少取決於能不能由程式獨立重算：
  - `automated-test`：可由程式在獨立環境自動重跑（CI），或由執行器自己記錄輸出（sd0x precommit runner 的做法），不必依賴 agent 自陳。
  - `inspection`、`analysis`、`manual-demonstration`：未必能以程式自動重算（正式設計 §4.2 所稱「能重算」限程式重算）。可以由獨立執行者重新檢視、分析或操作，但那是一次新的執行；能否取得可信的執行紀錄，要依具體 procedure 與 runtime 判定（例如 Orca 的 runtime 擷取，部分實測）。沒有這類紀錄時，紀錄仍是執行者自陳。
  - 要分清楚三件事：程式重算、重新執行一次驗證、證明某次歷史執行確實發生。
- **E2 按驗證類別分層目前只是觀察，不是產品決策。** 它和 §2「設計內部張力」裡的承諾拆層方向有關，但要不要往那裡走，由使用者決定。

---

## §4 Gap map

| 項目 | 正式流程（現在） | PoC | 正式設計 | 歸類 | 案例 |
|---|---|---|---|---|---|
| 1 必要結果齊不齊、PASS 與否（Requirement 層） | 無機械檢查；verify checks 為文字 | 證過 | §7、I6 | 只有設計＋PoC，未實作 | 無假 PASS 穿透實例 |
| 2 Scenario 層 coverage | 無 | 未證（PoC 以 Requirement 為單位） | I3、§4.2 | 只有設計 | — |
| 3 結果 freshness | 文字要求，無 digest | 未證 | §6、§7 | 只有設計 | 無實例 |
| 4 archive 須有 FRESH Gate PASS | CLI 不檢查 verify／retrospective 完成狀態、Verification Result 或 Gate PASS；bridge 用 `-y` | 未證 | §7 invariant；宿主屬實作 | **真缺口：宿主未定** | — |
| 5 Gate 由誰觸發 | verify 由 apply 步驟 3 文字觸發 | 人工呼叫 | 綁定點已定，宿主屬實作 | **真缺口**（與 4 同源） | — |
| 6 驗證真的執行過的證明（E2） | 無 | 未證（宣稱邊界明示） | §8#5 明說 v1 不保證；machine-captured output 只說「較強 provenance」，沒有載體設計 | **真缺口**（設計自認），可達強度依 method 分層 | A8 一筆 |
| 7 verify 執行者獨立性的 provenance | 無 | — | §2.2 列 degradable；verify 階段載體未實測（§9.2） | 設計內已知的前置確認項 | — |
| 8 驗證工具判得對不對（①） | 審查層 | — | §8#4、§8#9 不保證 | **刻意不保證**（C2） | 2 對 3 |
| 9 執行環境（②） | 無環境紀錄 | — | §8#6 不保證 | **刻意不保證**（C2） | 1 對 1 |
| 10 結果格式表達力（③） | verify.md 三選一勾選 | 只有 PASS／FAIL | Gate 層有 BLOCKED 規則（§6） | Gate 層部分回答；驗證工具層無（C2 候選） | 1 對 1 |

「已實作」一欄沒有任何項目落入：checks 8–13 已實作，但都是 agent 執行的文字，對應的機械版本屬第 1、3 列。

---

## §5 未查證／下一輪候選

**未查證**（本輪不補，避免無限延伸）：

1. 沒實測 PreToolUse hook 攔 `openspec archive -y`。
2. 沒讀 Orca 對 supervised worker 輸出封存的文件，也沒實測它能不能當證據。
3. 沒查 GitHub branch protection。
4. 沒讀 Claude Code hook 文件裡對繞過情形的說明。
5. OpenSpec 1.14.0 只做了關鍵字搜尋，加上讀 archive 的 task 檢查段。
6. spike S1–S4 的細節、handoff、workflow-harness 那邊都沒讀；`gate_check.py` 沒重跑。
7. C 證據整理的 subagent 自述未讀：`blind-kit/v2/FROZEN.md`、Identity verify 腳本、workflow-harness 的 `CH/verify.md` 等。

**下一輪候選**（使用者 2026-10-05 傾向；未拍板）：只挑一個最能增加決策資訊的點，**實測 PreToolUse hook 能不能在真實流程裡可靠攔下 `openspec archive -y`**，直接回答 E1 的可行性。兩個前提：

- 在暫存的測試專案裡做，不裝進日常環境。
- 這只能證明「攔得到」，不能證明「攔下來之後有東西可以判 PASS」，因為正式的 Gate 程式還不存在。

做法 4（prospective validation）的兩個未決題（選哪個真實 change、四欄紀錄放哪裡）同樣等之後再決定。Identity change 曾否決「本版就寫一支像 `gate_check.py` 的腳本」（理由是會長成半套 traceability system，見 `openspec/changes/archive/2026-10-01-requirement-scenario-identity/design.md`），之後若要談 Gate 實作，這筆否決要一起帶上。
