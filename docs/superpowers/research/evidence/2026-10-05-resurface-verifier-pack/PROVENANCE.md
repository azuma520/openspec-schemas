# 最小證據包：`fix-deferred-verification-resurface` 的驗證器材原始輸出

> **為什麼存在**：Verification Strategy 第二步 A（驗證工具本身是否可靠）要用到下列檔案，它們原本只在另一個 repo 某個 session 的暫存區裡，沒有保存保證。這裡是**逐 byte 複製**（複製時與來源 `cmp` 相同），只為保住研究輸入；**不是**處理盤點表 §0／O6 的證據壽命問題（使用者 2026-10-05 裁定：那題先不碰）。
>
> **只收「下次可能消失、A 直接會用」的檔**。逐字對話紀錄與 Codex 對話**不複製**，以原始位置指回去（見最後一節）。

## 來源

| 項目 | 值 |
|---|---|
| repo | workflow-harness（本機 `D:/workflow-harness`） |
| 案例 | archived change `openspec/changes/archive/2026-09-30-fix-deferred-verification-resurface/` |
| 原始位置 | 該 change 主 session 的 Claude Code scratchpad：`%TEMP%/claude/D--workflow-harness/581c70bd-4aa6-4f59-a220-dec9fbfc4c63/scratchpad/` |
| 複製日 | 2026-10-05 |
| 引用它的研究文件 | `../../2026-10-05-verification-comparison-case-resurface.md`（下稱「對照文件」；文中以 `SP/` 指這個暫存區） |

## 檔案與它支撐的觀察

SHA-256 只列前 16 碼。

| 檔案 | SHA-256（前 16） | 原檔時間 | 內容 | 對照文件中支撐的地方 |
|---|---|---|---|---|
| `mutants.py` | `ee3821db112117d3` | 2026-09-30 11:29 | 手工反向對照腳本（逐一裝回壞實作、跑測試、印失敗型別） | 層表 L4；§4 A2。**只有最後一版**——A2 說的「前兩版判不出失敗型別」那兩版沒有留下，只能從逐字紀錄指回（對照文件 `TR` 1780、1790、1803、1811） |
| `mut-vp.json` | `090a1a7b1b155236` | 2026-09-30 11:39 | 變異 runner（`mutation-runner/v1`，mutmut 2.5.1）第一批結果；`survivors` 2 筆 | §1 C1「殺 22」；層表 L6；§3c-2「只列活口、沒記哪條測試殺了哪隻」 |
| `mut-vp.err` | `efdaf7793006dade` | 2026-09-30 11:39 | 同批的 runner 摘要：24 隻、單輪 5.90 秒 → **預估** 142 秒、殺 22／活 2 | 層表 L6 的成本；§3a「成本 proxy」（預估、非實測） |
| `mut-vp2.json` | `a24d062980001834` | 2026-09-30 11:40 | 第二批結果；`survivors` 1 筆 | §1 C1「補測後 23、剩 1 隻判等價」；§4 A5 |
| `mut-vp2.err` | `37654e4f2bf1fa14` | 2026-09-30 11:40 | 第二批摘要：殺 23／活 1、單輪 5.64 秒 | 同上 |
| `mut-vp3.json` | `3c08249e737b6fd9` | 2026-09-30 15:25 | 第三批結果；`target_sha256` 與前兩批不同（受測檔已改動）；`survivors` 1 筆 | 對照文件以 `SP/mut-vp*.json` 統稱引用；**這一批對應哪一步改動，對照文件沒有逐一指明【未查證】** |
| `mut-vp3.err` | `474c55447d6ad071` | 2026-09-30 15:25 | 第三批摘要：殺 23／活 1、單輪 5.79 秒 | 同上 |

JSON 裡的路徑（`target`、`tests`、`cwd`）指向當時的 worktree `D:\workflow-harness\.claude\worktrees\fix-deferred-verification-resurface\`，該 worktree 現已不存在；比對受測檔時用 `target_sha256` 與 `patch_from: f6816b8`。

## 沒有複製、以原始位置指回的來源

| 來源 | 位置 | 為什麼不複製 |
|---|---|---|
| 主 session 逐字紀錄（對照文件的 `TR`） | `~/.claude/projects/D--workflow-harness/581c70bd-4aa6-4f59-a220-dec9fbfc4c63.jsonl` | 整份對話、體積大；對照文件已逐行號引用 |
| Codex 對話（`RO1`、`RO2`） | `~/.codex/sessions/2026/09/30/` 下 thread `01a0effc-…`、`01a0f135-…` 的 rollout 檔 | 同上 |
| 探針與輸出 | workflow-harness repo 內 `CH/evidence/`（已進版控） | 已有保存保證 |
