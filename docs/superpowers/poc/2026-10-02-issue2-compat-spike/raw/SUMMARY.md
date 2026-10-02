# 原始輸出機械摘要（2026-10-02 spike）

這份摘要是在刪除大部分原始輸出**之前**，用 Python 讀過當時 `out-v1.3.1/` 和 `out-v1.14.0/` 底下全部檔案機械產生的。那些檔案大多沒有保留（raw output not retained），還在的只有文末清單列出的幾個；下表其他步驟的數字只記在這裡，要原檔就照下一節重跑。產生方式：

- **exit code**：讀 `<步驟>.exit` 檔。
- **stdout 相同**：先把兩版輸出裡的 scratch 目錄名（`run-v131` / `run-v1140`、`tmp-v131` / `tmp-v1140`）正規化成同一個字，再逐字比對。
- **JSON 欄位**：把 JSON 攤平成「欄位路徑」的集合，算兩版之間的差集。

2026-10-02 依使用者裁定精簡了原始輸出，保留哪些檔見文末清單。

## 版本與重現方式

| 項目 | 值 |
|---|---|
| 基準 CLI | `openspec`（本機全域安裝，1.3.1） |
| 新版 CLI | `npx -y @fission-ai/openspec@1.14.0` |
| 環境變數 | `OPENSPEC_TELEMETRY=0 OPENSPEC_NO_UPDATE_CHECK=1 NO_COLOR=1` |
| 平台 | Windows 11 + Git Bash |
| 準備 | 在 repo 外開一個空的 scratch 目錄，`export S=<該目錄>`；兩支腳本都只寫進 `$S`，輸出在 `$S/out-<label>/` |
| 步驟 00–17 | `bash run.sh <label> <openspec 指令...>`（例：`bash run.sh v131 openspec`、`bash run.sh v1140 npx -y @fission-ai/openspec@1.14.0`）。fixture 從腳本所在目錄讀；bridge 從腳本所在的 repo 複製（`git rev-parse --show-toplevel`，可用 `REPO=<repo 根目錄>` 覆寫）；git 不保存的空目錄 `openspec/schemas/`、`openspec/changes/` 由腳本自己建立 |
| 步驟 18–20 | 同一個 `S` 底下 `bash extra-cases.sh <label> <openspec 指令...>`，要先跑過同一個 label 的 run.sh；需要 `git`（`20-init`）和 `python`（`18-synced`）。這支腳本依 spike 當時實際執行過的指令重建 |
| 沒寫成可執行步驟 | `19-repo-validate-archived`、`19b-list-archived`（只在 1.14.0 跑過）只在 extra-cases.sh 末尾的註解列出指令 |
| 重跑確認（2026-10-02） | 把兩支腳本和 fixture 的檔案複製到 repo 外（不含空目錄，模擬 clone 下來的狀態），用新的 `S` 對兩版各跑 run.sh 與 extra-cases.sh：文末保留的原始檔中，`00-version`、`14b-list`、`15-archive-preview`、`18-conflict`（`.out` 與 `.exit`）兩版都逐字相同；`09b-instr-apply-text`（兩版）和 1.14.0 的 `20-status-planonly` 只差輸出裡印出的 scratch 絕對路徑，1.3.1 的 `20-status-planonly` 逐字相同。非 0 的 exit 只有 `19-h3-scenario`（兩版）、`16-archive-abort` 和 `18-conflict`（1.14.0），和下兩節一致 |

## 每個步驟在兩版的結果

「—」表示那一步當時沒有把 exit code 存成檔案。步驟 19、20 的 exit code 是在終端機上直接看到的，列在下一節。

| 步驟 | 1.3.1 exit | 1.14.0 exit | exit 相同？ | stdout 相同？ | JSON 欄位（1.3.1 → 1.14.0） |
|---|---|---|---|---|---|
| `00-version` | 0 | 0 | 相同 | 不同 | 非 JSON |
| `01-schema-validate` | 0 | 0 | 相同 | 相同 | 非 JSON |
| `02-schemas` | 0 | 0 | 相同 | 相同 | 非 JSON |
| `03-schemas-json` | 0 | 0 | 相同 | 相同 | 移除 0 / 新增 0 |
| `04-new-change` | 0 | 0 | 相同 | 不同 | 非 JSON |
| `05-status-empty` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 53 |
| `06-instr-brainstorm-json` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 10 |
| `06b-instr-brainstorm-text` | 0 | 0 | 相同 | 不同 | 非 JSON |
| `07-instr-apply-blocked` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 5 |
| `08-status-full` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 53 |
| `08b-status-text` | 0 | 0 | 相同 | 不同 | 非 JSON |
| `09-instr-apply-json` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 6 |
| `09b-instr-apply-text` | 0 | 0 | 相同 | 不同 | 非 JSON |
| `10-instr-verify-json` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 10 |
| `10b-instr-retro-json` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 10 |
| `10c-instr-plan-json` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 10 |
| `11-validate-all` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 3 |
| `11b-validate-change-strict` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 3 |
| `12-show-deltas` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 7 |
| `13-show-spec` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 5 |
| `14-list-json` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 3 |
| `14b-list` | 0 | 0 | 相同 | 不同 | 非 JSON |
| `15-archive-preview` | 0 | 0 | 相同 | 不同 | 非 JSON |
| `15d-show-candidate` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 5 |
| `16-archive-abort` | 0 | 1 | 不同 | 不同 | 非 JSON |
| `17-repo-validate-all` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 3 |
| `17b-repo-list-specs` | 0 | 0 | 相同 | 不同 | 非 JSON |
| `17c-repo-show-contract-identity` | 0 | 0 | 相同 | 不同 | 移除 0 / 新增 5 |
| `18-conflict` | 0 | 1 | 不同 | 不同 | 非 JSON |
| `18-synced` | 0 | 0 | 相同 | 不同 | 非 JSON |
| `19-h3-scenario` | — | — | 未存檔 | 不同 | 非 JSON |
| `19-repo-validate-archived` | — | — | 未存檔 | 只有 1.14.0 有跑 |  |
| `19b-list-archived` | — | — | 未存檔 | 只有 1.14.0 有跑 |  |
| `20-init` | — | — | 未存檔 | 不同 | 非 JSON |
| `20-status-planonly` | — | — | 未存檔 | 不同 | 非 JSON |
| `20b-status-planonly` | — | — | 未存檔 | 不同 | 移除 0 / 新增 53 |
| `20c-apply-planonly` | — | — | 未存檔 | 不同 | 移除 0 / 新增 6 |

讀法：

- **exit code 只有兩步不同**：`16-archive-abort` 和 `18-conflict`。兩步都是 archive 被擋下的情境，1.3.1 回 0、1.14.0 回 1，對應報告的 O18。
- **JSON 欄位只增不減**：所有能解析成 JSON 的輸出，「移除」欄都是 0。
- **`00-version` 的 stdout 不同**，只是因為版本號本身不一樣。

## 終端機上直接看到的結果（沒有存成 `.exit` 檔）

| 步驟 | 1.3.1 | 1.14.0 |
|---|---|---|
| `19-h3-scenario` | exit 1，訊息 `Unknown item 'h3'`。1.3.1 要求 change 底下有 proposal.md 才找得到它，所以這一步在 1.3.1 沒有對照到 | exit 1。INFO：「is not a "### Requirement:" header and is ignored」；ERROR：「must include at least one scenario」 |
| `20-init` | exit 0，產生 11 個 skill 和 11 個 `/opsx` 指令 | exit 0，產生同一組 11 個 skill 和 11 個指令 |

## instruction 有沒有原樣交給 agent（O6、O7）

| 版本 | 步驟 | artifact | 和 schema.yaml 原文逐字相同？ |
|---|---|---|---|
| 1.3.1 / 1.14.0 | `06-instr-brainstorm-json` | brainstorm | 是 / 是 |
| 1.3.1 / 1.14.0 | `10c-instr-plan-json` | plan | 是 / 是 |
| 1.3.1 / 1.14.0 | `10-instr-verify-json` | verify | 是 / 是 |
| 1.3.1 / 1.14.0 | `10b-instr-retro-json` | retrospective | 是 / 是 |
| 1.14.0 | `09-instr-apply-json` | apply | 是（等於 `apply.instruction` 去掉結尾換行，前後沒有附加文字） |
| 1.3.1 | `09-instr-apply-json` | apply | 否。這裡回的是 `state: all_done`，CLI 改給「All tasks are complete!」的提示，原因是 1.3.1 把 `[~]` 那行整個丟掉了（見下一節） |

## `[~]` 的差異（O9、O12）

| 步驟 | 1.3.1 | 1.14.0 |
|---|---|---|
| `09-instr-apply-json` 的 progress | total 2 / complete 2 / remaining 0（`1.2` 那行不見了） | total 3 / complete 2 / remaining 1（`1.2 Manual smoke on staging` 標成 done=false） |
| `14b-list`（原始檔有保留） | `✓ Complete` | `2/3 tasks` |
| `09b-instr-apply-text`（原始檔有保留） | 沒有列出 1.2 | `- [ ] 1.2 Manual smoke on staging` |
| `15-archive-preview`（原始檔有保留） | `Task status: ✓ Complete` | `Warning: 1 incomplete task(s) found. Continuing due to --yes flag.` |

## 報告各項對應到哪些步驟（支撐「24 項、0 項不成立」）

| 報告項目 | 依據的步驟 | 判定 |
|---|---|---|
| O1、O3 | `01-schema-validate` | 成立 |
| O2 | `02-schemas`、`03-schemas-json` | 成立 |
| O4 | `04-new-change` | 成立（輸出格式有改） |
| O5 | `05-status-empty`、`08-status-full` | 成立 |
| O6 | 上面的 instruction 表 | 成立 |
| O7、O8 | `07-instr-apply-blocked`、`09-instr-apply-json` | 成立 |
| O9 | `09`、`09b`、`14b`、`15-archive-preview` | 有變化需評估 |
| O10、O23 | `20-init` | 成立 |
| O11、O12 | 讀 `20-init` 產生的 SKILL.md 原文（行號在報告第 2 節） | O11 成立；O12 有變化需評估 |
| O13 | `11-validate-all`、`11b-validate-change-strict` | 成立 |
| O14 | `12-show-deltas`、`13-show-spec`、`15-archive-preview` | 成立 |
| O15 | `19-h3-scenario` | 有變化需評估 |
| O16 | 原始碼註解（見報告第 2 節） | 成立 |
| O17 | `15-archive-preview`，以及當時對 archive 之後的目錄和合併出的 spec 做的比對 | 成立 |
| O18 | `16-archive-abort`、`18-conflict` | 有變化需評估 |
| O19 | `18-synced` | 有變化需評估 |
| O20 | `13-show-spec`、`15d-show-candidate`、`17c-repo-show-contract-identity` | 有變化需評估 |
| O21 | `12-show-deltas` | 有變化需評估 |
| O22 | `14-list-json`、`14b-list`、`02-schemas` | 成立 |
| O24 | `20-status-planonly` | 有變化需評估 |

合計：16 項成立、8 項有變化需評估、0 項不成立。

## 保留下來的原始檔

| 檔案 | 用途 |
|---|---|
| `run.sh`、`extra-cases.sh`、`fixture/` | 重現實驗 |
| `out-v1.3.1/00-version.out`、`out-v1.14.0/00-version.out` | 證明兩個 CLI 的版本 |
| `out-*/14b-list.out`、`out-*/09b-instr-apply-text.out`、`out-*/15-archive-preview.out` | `[~]` 的差異（O9 / O12） |
| `out-*/18-conflict.out`、`out-*/18-conflict.exit` | archive 被擋時的 exit code：1.3.1 是 0、1.14.0 是 1（O18） |
| `out-*/20-status-planonly.out` | 只做到 plan 時的 `Next:` 那一行（O24；1.3.1 沒有這行） |
| `sdd-task-brief-probe.txt` | SDD 的 `task-brief` 碰到 `## 1.1 —` 這種標題時回 exit 3（S11） |

`executing-plans` 的新行為（S13 / S14）沒有原始輸出檔，證據是報告第 2b 節引用的 v6.4.2 SKILL.md 原文和行號。
