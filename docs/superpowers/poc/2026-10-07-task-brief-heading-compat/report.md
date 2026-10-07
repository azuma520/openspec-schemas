# task-brief 標題相容性 spike：從「轉接層」改判為「Plan Contract 改用 `## Task N —`」

- 日期：2026-10-07
- 性質：研究 / 取事實（spike）＋決策紀錄。spike 階段沒有修改 `superpowers-bridge/`、`.github/` 或 `openspec/`
- 對應工作：`task-20261002-task-brief-heading-compat`（本日改為「接下來要做」）
- 前身：[`2026-10-02-issue2-compat-spike/report.md`](../2026-10-02-issue2-compat-spike/report.md) 的 S11 / R3，與該報告第 236 行留下的未實測項（`task-brief` 能否處理帶小數點的編號）
- 原始輸出：`raw/`（`run.sh` 可重跑，`output.txt` 為 2026-10-07 的輸出；fixture 兩份；放棄方案 B 的雛形腳本）

---

## 結論

**定案（使用者 2026-10-07 裁定）：採 C′——Plan Contract 的條目標題改以 `## Task <編號> — <標題>` 為建議寫法，check 12 在相容期同時接受舊的 `## <編號> — …`；schema major 3 → 4。不做轉接層（B），不改本機上游副本、不發上游 PR（D）。**

理由一句話：上游 `task-brief` 本來就讀得懂 `## Task 1.1 — …`，不相容的只是 bridge 目前選用的標題表面格式；讓 contract 接上既有能力，比另建一層程式碼便宜，也沒有「兩份說明打架、主代理聽哪份」的問題。

## 起點問題

SDD（Superpowers v6.0.0 起）規定主代理派工前跑 `bash scripts/task-brief PLAN_FILE N`，把該任務全文抽成簡報檔；這份簡報檔是執行子代理的唯一需求來源、回報檔依它命名、審查子代理也拿同一份審（[SKILL.md@v6.4.1 第 251–262 行](https://github.com/obra/superpowers/blob/v6.4.1/skills/subagent-driven-development/SKILL.md)）。`task-brief` 只認 `^#+ Task <N>` 標題（[task-brief@v6.4.1 第 30–36 行](https://github.com/obra/superpowers/blob/v6.4.1/skills/subagent-driven-development/scripts/task-brief)），bridge 的 Plan Contract 寫成 `## 1.1 — …`（`schema.yaml` 第 377–399 行），因此 exit 3。9/03 dogfood 撞過一次，當時由主代理手工抽取繞過。

本機核對：`claude-plugins-official/superpowers/6.4.1` 的 `task-brief`、`sdd-workspace`、`SKILL.md` 與上游 `v6.4.1` 標籤逐檔相同（去除 CR 後比對）；`superpowers-marketplace/superpowers/6.4.2` 的 `task-brief` 與 6.4.1 相同。

## 決策軌跡

| 步驟 | 內容 | 結果 |
|---|---|---|
| 1 | 列出四條路：A 主代理手工抽簡報、B bridge 自帶轉接層、C 改標題格式、D 改上游 | — |
| 2 | 查上游貢獻規範與既有 issue / PR | D 的 PR 版本放棄：上游 `AGENTS.md` 禁止打包與重複提交，前綴誤抓（#2405、#2175 / PR #2176）與吞掉尾段（#2406 / PR #2359）都已有人回報且有 PR 未合併；原「上游回報草稿」工作取消 |
| 3 | 傾向 B，並定義為「薄轉接層」：工作目錄沿用上游 `sdd-workspace`，bridge 只解析自己的條目邊界 | 進 spike |
| 4 | B 的 spike（四題，見下節） | PASS |
| 5 | Fable 獨立審：實跑上游 `task-brief` 於 `## Task 1.1 — …`，結果正常；指出 B 的結構弱點 | 主 session 重跑確認（`raw/output.txt` 第 3 段） |
| 6 | 改判 C′；查 Plan Contract 原文判定版本號 | major 3 → 4（見「版本號」節） |

### B 的 spike（已放棄，結果保留供日後參考）

1. 主代理知道 SDD 腳本目錄：Claude Code 載入 skill 時給出 `Base directory for this skill: …`。本機同時啟用 6.4.1 與 6.4.2 兩份 Superpowers，實際載入並給出路徑的是 6.4.1，即路徑跟著實際載入的那份走，不是「最新那份」；**真正換版的情境沒有模擬**。
2. 轉接層不需自行定位上游：SDD 開工時本就要求主代理跑 `sdd-workspace`，轉接層只需接收輸出檔路徑。
3. `sdd-workspace` 對 bridge 的計畫檔正常（rc=0）；兩個 change 的計畫檔同名 `plan.md` 時自動分成 `plan/`、`plan-other/`（`raw/output.txt` 第 1 段）。
4. 雛形第一版要 `1.1` 時誤抓 `1.10`：awk 把 `"1.1"` 與 `"1.10"` 當數字比較。改字串比較後六種情況正確（第 4 段）。**此錯屬雛形本身，上游腳本沒有**——上游把編號字串拼進 regex，`1.1` 與 `1.10` 分得開（第 3 段）。

### 為什麼放棄 B

- **兩份說明衝突**：SDD 原文要主代理跑「這個 skill 自己的」`task-brief`，B 要 apply 說明改叫別的腳本。主代理照 SDD 原文跑上游、exit 3、再自行繞過時，轉接層根本沒被叫到，而測試與 CI 仍全綠——這個失敗沒有任何一層會喊。
- **成本為零外部使用者而付**：本 repo 第一份可執行程式，連帶要處理 CRLF、執行權限、CI 測試步驟，CLAUDE.md「沒有原始碼」的描述也要改。
- C′ 讓上游腳本直接成功，上述問題整個不存在。

## 上游 `task-brief` 對 `## Task <編號> —` 的實測（`raw/output.txt` 第 3 段）

| 要求編號 | 結果 | 說明 |
|---|---|---|
| `1.1` | 正確 | 只取到 1.1；程式碼區塊內的 `## Task 2.1 — fenced` 屬 1.1 內文，未被當成新條目 |
| `1.10`、`1.2` | 正確 | 各自只取到自己 |
| `2.1`（最後一項） | 多吞一段 | 後面的 `## Self-review` 被一起抽進簡報（上游 #2406 同類），只是雜訊、不會讓流程失敗 |
| `1`、`2` | 多抓 | 要求 `1` 取到所有 `1.x`、要求 `2` 取到 `2.1`（連同其後的 `## Self-review`）。這是上游的前綴問題，規則是通用的：要求任一整數編號 N 時，都會連帶取到所有 `N.x`（以 `1`、`2` 實測，其餘整數依同一 regex 推得）。只有任務編號裡有整數 N 時才會被要求、才會發生 |

另依 regex 推得（**未實測**）：要求 `1.1` 時，`1.1.1` 與 `101` 這類編號也會被抓進來（`.` 在 regex 中可配任意字元、`.1` 後非數字即成立）。

## 版本號：major 3 → 4

CLAUDE.md 的升版條件之一是「原本合法的 artifact 變不合法（獨立即足夠）」。判斷關鍵是：被重新解讀的舊寫法，以前是受規格保障的合法內容，還是只是 parser 沒理它。

Plan Contract 原文（`schema.yaml` 第 396–398 行）：「A `##` heading that does not begin with a number is not an entry (this plan's own header, a self-review section).」——不以數字開頭的 `##` 標題是**明文承認**的非條目段落。因此舊計畫裡的 `## Task 3 備註` 或 `## Task 3 — 備註` 原本合法，C′ 之後會被讀成條目鍵 `3`，可能讓原本通過 check 12 的計畫變成不通過。只要新增 `Task` 形式，就必然存在這類重新解讀，限定後面要接破折號也閃不掉。

查證範圍：本 repo 所有 `plan.md` 沒有任何 `##` 層級的 `Task` 標題（唯一的 `### Task N:` 在 2026-08-31 封存的 change，check 12 不讀 `###`）；歷史 `tasks.md` 沒有整數或三層編號。這只支持「遷移風險低」，不推得「沒有破壞相容」。外部使用者目前為零（使用者 2026-10-07 確認），正是升版成本最低的時候。

## 不新增的規則

以下兩項都由上游的解析問題引起；為它們收緊 bridge 自己的 contract 本身就是另一次破壞相容，因此只寫建議、不做檢查：

- 最後一項吞掉尾段：Plan 說明加一句建議「非條目段落放在第一個條目之前」。Plan Contract 目前允許自我檢查段放在任何位置。
- 整數編號（如 `1`、`2`）與三層編號（如 `1.1.1`）：check 12 的編號文法是 `\d+(\.\d+)*`（`schema.yaml` 第 823 行），兩者都合法；不鎖成 `x.y`。

## 正式 change 要連動的地方（開 change 時核對，非完整清單）

- `schema.yaml`：Plan Contract 條目寫法（第 377–399 行）、check 12 收集條目鍵的文法（第 817 行起）、`version: 3` → `4`、apply 說明（第 1661 行起）視需要補一句。
- `templates/plan.md` 三個條目標題。
- `superpowers-bridge/VERSION` 3.0.0 → 4.0.0。
- bridge README（en + zh-TW）：Artifact / Plan 段、S11 那一列與「後續狀態」段、Compatibility 表的列鍵 `v3` → `v4`、Versioning 段的 migration guide。
- `.github/workflows/version-check.yml` 第 44 行的 `grep -E '^\| v3 \| \`'` 必須與 Compatibility 表同步，否則 CI 失敗。
- repo CLAUDE.md 寫死 `version: 3` / `v3` / `3.x.y` 的段落（「兩個版本號別搞混」表、跨檔耦合表等）。
- adopters fragment 是否提到標題形式：**未查**。
- 驗證不是單元測試，而是整條流程：bridge 產出 `## Task 1.1 —` → 原版上游 `task-brief` 抽取 → 執行子代理用該簡報 → 審查子代理用同一份簡報，跑完一輪並留證據。

## 未查證 / 限制

- 只在 Claude Code 上測；其他平台未測。
- `sdd-workspace` 在 Git Bash 下印出 `/tmp/...` 形式的路徑，子代理的讀檔工具在 Windows 上能否直接讀，未測（上游 `task-brief` 印的是同一種路徑，非本變更引入）。
- 上游 issue / PR 狀態為 2026-10-07 查詢當下；之後可能變動。
