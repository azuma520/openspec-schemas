# 最小證據包：C1 第二輪 PreToolUse hook 攔 `openspec archive -y` 實測

> **為什麼存在**：C1 研究文件 §3.4（`../../2026-10-05-verification-c1-enforcement-surface.md`）的實測結果原本只在本 session 的 Claude Code scratchpad 裡，沒有保存保證。這裡是**逐 byte 複製**（複製時與來源 `cmp` 相同），只收「重現實測所需的腳本」與「支撐結論的判讀紀錄」。
>
> **沒有收**：巢狀 session 的完整 stream-json 逐字輸出（`logs/*.jsonl`，共約 740K，內含使用者全域設定與 plugin 注入的 SessionStart 內容）與 `logs/*.stderr`（13 份內容都只有一行相同的 MCP enterprise-policy 警告）。`logs/*.summary.txt` 是由 `extract.py` 從 `.jsonl` 抽出的事件摘要，判讀以它為準。

## 來源

| 項目 | 值 |
|---|---|
| 原始位置 | `%TEMP%/claude/C--Users-user-orca-openspec-schemas/88aae4de-4371-4663-80b8-dfe9fac6fb11/scratchpad/c1-hook-probe/` |
| 實測日 | 2026-10-05（hook.log 時間 15:54–16:00，台北時間） |
| 環境 | Claude Code 2.1.289、OpenSpec 1.3.1（全域）、Python 3.13.5、Windows 11 Pro 10.0.26200、Git Bash MINGW64 3.6.3 |
| 執行者 | 一次性 subagent 跑設定、Layer 1、Layer 2 全部案例；主 session 另外重跑 `main-ctrl-bypass`、`main-h-bypass` 兩案，以及 Layer 1 的三個指令（hook.log 最後三行，`permission_mode` 為 `None`） |
| 全域設定 | 只讀未改：`~/.claude/settings.json` 為 `defaultMode: auto`、`permissions.allow` 含 `Bash(*)`；全域 PreToolUse hook 有 `guard-silent-traps.py`（matcher Bash）與 Orca `claude-hook.cmd`（matcher `*`） |

## 重現方式

腳本內寫死上述 scratchpad 的絕對路徑；在別處重現要先改 `run.sh`、`reset.sh`、`oracle.sh`、`settings.hook.json` 裡的路徑。測試專案 `proj/` 本身沒有收：它是 `git init` → `openspec init --tools none .` → `openspec new change probe-x` 產生的，`probe-x.bare/` 是 change 的原始樣板（只有 `.openspec.yaml`）。每一案開跑前 `reset.sh` 會重建 change、清空 `archive/`。

- Layer 1（只測 hook 的判斷）：`python layer1.py > layer1.out`（結果印在 stdout，要自己轉向）。`hook.py` 的紀錄路徑寫死為同目錄的 `hook.log`（`layer1.py` 設的 `C1_LAYER` 環境變數沒有被讀），所以 Layer 1 與 Layer 2 的紀錄會寫進同一個檔；要分開就得在兩層之間自己把 `hook.log` 改名。本包的 `hook.layer1.log` 就是這樣留下的：18 行、時間 15:52:21–15:52:22，早於 Layer 2 第一行（15:54:19）；改名用的指令 subagent 沒有記錄。
- Layer 2（真實巢狀 Claude Code）：`bash run.sh <案名> <hook|nohook> "<權限參數>" "<prompt>"`，跑 `claude -p … --output-format stream-json --verbose --max-turns 8`，結果寫 `logs/<案名>.meta`（三個判準中的檔案系統與 hook 紀錄行數）；`python extract.py logs/<案名>.jsonl` 產生 `.summary.txt`（工具呼叫、工具結果、`permission_denials`）。

## 檔案

SHA-256 只列前 16 碼。

| 檔案 | SHA-256（前 16） | 內容 |
|---|---|---|
| `hook.py` | `25269a8510a386ef` | 受測 hook：regex `\bopenspec\b[^;&|\n]*\barchive\b` 比對 Bash 指令，命中即輸出 `permissionDecision: deny`（exit 0）；JSON 解析失敗時放行 |
| `settings.hook.json` | `83f00d0b065a2336` | 測試專案 `.claude/settings.json` 的掛 hook 版本（PreToolUse、matcher `Bash`） |
| `settings.nohook.json` | `ca3d163bab055381` | 對照組版本（`{}`） |
| `run.sh` | `491aac91b66d0eac` | Layer 2 單案執行器 |
| `reset.sh` | `e4ee511c2ac4373f` | 重建 fixture |
| `oracle.sh` | `52880047554cfc1c` | 判準 (a)：`probe-x` 還在不在、`archive/` 有幾筆；並印 hook.log 行數 |
| `extract.py` | `9d31c678b8a83afb` | 從 stream-json 抽事件摘要 |
| `layer1.py` / `layer1.out` | `71115bc08e80cd7f` / `ba023d49aa633b85` | Layer 1 的 18 個指令與結果 |
| `hook.log` | `13cb6c3296feba91` | Layer 2 期間 hook 每次被呼叫的紀錄（時間、事件、工具、權限模式、決定、指令）；最後三行是主 session 的 Layer 1 抽查 |
| `hook.layer1.log` | `8cc74fea94e7d371` | Layer 1 期間的 hook 紀錄（由 `hook.log` 改名而來，見「重現方式」） |
| `probe-x.bare/.openspec.yaml` | `c956e2a907cf0aa2` | fixture 樣板 |
| `logs/<案名>.meta`、`logs/<案名>.summary.txt` | 13 案 × 2 | `ctrl-*`（無 hook 對照）、`h-*`（掛 hook）、`main-*`（主 session 重跑） |

## 沒有複製、以原始位置指回的來源

| 來源 | 位置 | 為什麼不複製 |
|---|---|---|
| 巢狀 session 完整輸出 | 上述 scratchpad `logs/*.jsonl` | 體積大、含使用者全域環境注入內容；判讀所需事件已在 `.summary.txt`。scratchpad 不保證保存 |
| 巢狀 session 逐字紀錄 | `~/.claude/projects/` 下以測試專案路徑命名的目錄 | 同上 |
