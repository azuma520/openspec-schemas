# Session Handoff — 2026-09-22

## Session 00:40

### 一、本 session 主題

**跨日續跑，非新 session。** 這是 2026-09-21 那個 session 的延續——它仍開著，
正在等 Codex 額度於 **03:16** 恢復後跑第①輪（workflow-harness
`fix-worktree-canonical-root` 程式面第三輪重審）。

本檔在 00:40 建立的唯一原因是**日期跨過午夜、Stop hook 要求當日 handoff 存在**。
**09-21 的工作全部記在 `session-handoff-20260921.md`**（含該檔 `## Session 18:33`
區塊尾端的「追記（同一 session，22:13–23:05）」），本檔不重抄。

### 二、完成事項

**無。** 09-22 到目前為止只有一次等待用的 loop tick（00:40，確認閘門未到、未派工）。
零檔案異動、零 commit、零審查派工。

⚠️ 這一欄是空的，而它應該是空的——**不要為了讓欄位看起來有內容而把昨天的成果
搬過來**。搬過來會讓 09-22 看起來完成了一批其實發生在 09-21 的事。

### 三、未完事項 / 接力棒

- [#接力] **03:16 派第①輪**（使用者 2026-09-21 裁示選乙：這個額度窗專給①，
  不派②③）。原 thread `01a0c33d-78cc-7d41-9a9d-2b2750199ebc` 續審，branch 範圍、
  tier `thorough`。**派工前必須重抓 metadata。**
  要它驗五點：(a) 判別式已由目錄名改為結構性回指檔 `<gitdir>/gitdir`、兩個誤判
  版面已補真 git 反向控制 (b) 三條 P1 回歸測試是否真的守得住 (c) 掃描台帳的
  計數單位與射程更正是否正確 (d) spec 的 `state_root` 契約與不可讀 `commondir`
  條文是否仍與實作一致 (e) **這一輪的修正有沒有再引入新問題**。
- [#接力] **②（workflow-harness 文件面）從未派出、③（Q8 報告）第二輪失敗**，
  兩者皆因額度。順延，等下一個額度窗。
- [#接力] ⚠️ **仍未記任何 pass、仍未 commit。** 兩個 repo 都是 dirty：
  `openspec-schemas`（Q8 報告 + `evidence/` 29 檔 + `recompute-correctness.py`
  + backlog + work-map + 兩份 handoff）、`workflow-harness` worktree
  `.worktrees/fix-issue-4-worktree-canonical-root`（程式 6 檔 + spec + change 文件
  + `resolve-exception-sweep.md`）。
- [#待確認] **②的規則解釋題仍開著**：09-01 定的「條件降級須補 Codex」，
  原意若是「高風險項要有獨立外部審」，fallback 就可能清償；若是指名供應商，
  ②只能等額度。**這是規則解釋、歸使用者**，直接影響還要排幾個額度窗。
- [#不重議] 額度窗的分配已定（乙：①優先）。理由記在 09-21 追記。

### 四、洞見 / 反省

**【紀律接力】**

- **跨日的 loop 會撞上「當日 handoff 不存在」這個閘門，而那不是錯誤、是設計。**
  長時間等待型的 loop（本例等 4 小時）只要跨過午夜就必然觸發。
  ⚠️ 值得記的是**正確反應**：建一份誠實反映「今天還沒做事」的 handoff，
  **而不是**把前一天的成果搬過來充數。後者會讓兩天的紀錄都失真，
  且沒有任何一層會抗議——`missing sections` 一樣是空的。

**【當日洞見】**

- 無。09-22 尚未有實質工作。

### 五、檔案異動

- `文檔/handoff/session-handoff-20260922.md` — 本檔（09-22 唯一的檔案異動）。

09-21 的完整檔案異動清單見 `session-handoff-20260921.md` 的
「五、檔案異動」與其後的追記段。

### 六、下一步建議

1. **03:16 派第①輪**（詳見三欄）。回來後逐條核實再報——09-21 已有一條
   Codex finding 被實測推翻、也有一條是我自己修出來的缺陷，兩個方向都發生過。
2. ①若過，才談②③的排期；**①若再 Blocked，先看是不是又引入新問題**
   （上一輪就是）。
3. 三輪全過之後才談 commit（走 `/smart-commit --execute`）→ PR（需 `plan.md`
   4.4a）→ merge → 更新 plugin cache → 真實 linked worktree dogfood →
   才把 `task-20260915-stop-hook-worktree-root` 標完成。
4. **②的規則解釋題**（fallback 能否清償條件降級義務）待使用者拍板，
   它決定這條線還要吃幾個額度窗。
5. 09-21 未決的兩件仍在：backlog 那條 mature `[優化建議]` 的保留／升級／移除；
   以及 backlog 射程問題（7 條無編號、四輪時間盒 0/4 空轉三週）。


---

### 追記（同一 session，03:18–03:52）—— 第①輪第三次的結果與修正

> 本段是 `## Session 00:40` 區塊的續寫。00:40 當下寫的「二、完成事項：無」在當時為真，
> 未改動。

#### 第①輪第三次：⛔ Blocked，1×P0 + 4×P2

**P0 又是我修出來的，而且是同一個錯誤的第三次。** 真 linked worktree 把 `commondir`
與回指檔**兩者皆刪**，解析結果回到 worktree 自己——Issue #4 的資料遺失路徑從另一側
重新打開。以真 git 實測確認後才動手。

| 輪次 | 我用的判別式 | 錯在哪 |
|---|---|---|
| 第二輪 | `gitdir.parent.name == "worktrees"` | 用**名字**當證據 |
| 第三輪 | 沒有回指檔 ⇒ 是主樹 | 用**缺席**當證據 |
| **第四輪（現行）** | `<gitdir>/config` 存在 **且** 無任何 worktree metadata | 用**存在**當證據 |

⚠️ **前兩次是同一個根因**：「A 不存在，所以是 B」。**缺席分不出「損壞」與「本來就
沒有」**。現行版本改用正面證據——worktree 的 gitdir **沒有** `config`（config 住在
common dir），而 repository 自己的 git dir 一定有；三個版面實測完全可分。

#### 本輪修正與證據

| 項目 | 證據 |
|---|---|
| 判別式改正面認證 | 變異檢查：換回名字版 → **3 條紅**；換回缺席版 → **2 條紅**（含專為 P0 寫的守門測試） |
| P0 守門測試（真 git 造，兩個 metadata 檔皆刪） | 新增 `test_worktree_losing_both_metadata_files_is_unresolved` |
| `config` 不可讀 → unresolved | 新增 `test_unreadable_repo_config_is_unresolved`（fail-closed） |
| `commondir` 的 **open-time** 拒絕 | 新增 `test_commondir_denied_at_open_time_is_unresolved`；原本只覆蓋 stat-time |
| 三個 `RuntimeError` handler 各自獨立注入 | 變異檢查：三個 handler 逐一拿掉，**各抓到一條** |
| Stop AST 守門收緊 | 值必須是 `_gate_state_root`，不只是「有這個關鍵字」 |
| 模組 docstring / spec 步驟 3 / `design.md` / `proposal.md` | 全部改為正面認證敘述，並**明文禁止用缺席或名字判斷** |

**驗證**：`7 failed, 3204 passed, 4 xfailed`——failed 與 baseline 逐條相同，
passed 由 3199 增 **5**，差額剛好是新增的 5 條。`openspec validate --strict` 通過、
link check 乾淨。測試數重新量測：`test_project_state_root.py` **45 → 48**、
`test_paths_runtime_hook_read.py` **8 → 10**，四處文件引用已同步。

#### ⚠️ 兩件我自己抓到、必須記下的事

1. **我又寫了一條比名字弱的測試，是自己的變異檢查抓到的。**
   補 runner 的 `RuntimeError` 測試時，我把 `--root` 塞進 argv，但 `run()` 的 root
   是**關鍵字參數**——argv 的 `--root` 被忽略，`root_in` 成了 `Path.cwd()`，
   注入條件永遠不成立。**測試跑了，但從未到達它宣稱要驗的那一行。**
   拿掉 handler 後測試仍綠，變異檢查才把它照出來。
   ⚠️ 結論不是「要小心」：**變異檢查是唯一能分辨「測試存在」與「測試守得住」的
   動作**，它不是收尾的裝飾。

2. **審查者的建議有一條不能照抄。** 它建議 Stop 的 AST 守門「斷言恰一次
   `resolve_for_hook_read` 呼叫」，但 `stop.py` 實有**兩個**呼叫點（另一個是快取
   未命中的後備路徑，正常流程走不到）。照抄會讓測試因錯誤的理由失敗。
   已改為「恰一個呼叫點傳該關鍵字，且值為 `_gate_state_root`」，並在測試 docstring
   裡寫明為何不照建議做。

#### 待使用者裁示（兩題，本 session 未決）

1. **下一個額度窗怎麼排。** 本窗已用於①。②（從未跑過）、③（第二輪失敗）仍欠，
   ①還需第 4 輪確認修正。
2. ⭐ **要不要換做法。** ①**已連續三輪都是「修好一個、引入一個」**。
   這個速率下，問題可能不在單次修法，而在我對這個 resolver 的判斷本身不可靠。
   值得考慮的替代做法：**先把所有 git 版面列成完整表格、一次定義完整判定矩陣並
   逐格實測**，而不是每輪針對最新 finding 打補丁。
   ⚠️ 這是方法層的決定，歸使用者。

#### 追記後的狀態

- **仍未記任何 pass、仍未 commit。** 兩個 repo 依舊 dirty。
- ①第 4 輪、②首輪、③第 2 輪，三者全欠。
- 09-22 的檔案異動（在原「五、檔案異動」之上）：
  `hooks/lib/project_state_root.py`、`hooks/lib/test_project_state_root.py`、
  `hooks/lib/test_paths_runtime_hook_read.py`、`hooks/test_stop.py`、
  `specs/project-state-root/spec.md`、`design.md`、`proposal.md`、
  `plan.md`、`brainstorm.md`。


---

### 追記二（同一 session，03:52–08:45）—— bounded redesign 完成；三輪外部審全數未取得

> 續寫 `## Session 00:40` 區塊。前兩段在當時為真，未改動。

#### 使用者裁示：停止補單點條件，改做 bounded redesign

同一類身份判斷錯誤連續三輪出現，每輪都是針對最新 finding 補一個條件。
三次根因相同——**用缺席當證據**。裁示要點：只針對 `project_state_root`；
先列出 contract 真正需要處理的 git 版面與 malformed 狀態、完成 decision matrix；
**兩個家族都必須有足夠的正面證據**，同一觀察若也可能來自 metadata 損壞／缺失／
不可讀，就不能拿來認證身份；合法版面盡量用真 git fixture，手工 fixture 只表示
故障狀態；**不擴成通用 git framework**。

#### 已完成（工作本體）

| 步驟 | 內容 | 證據 |
|---|---|---|
| 量測 | 真 git 建 13 個合法版面，逐一記錄 `.git` 種類／`commondir`／回指檔／`config`／認證鏈可觀察值 | 三訊號在健康版面上**完全反相關**：主樹家族只有 `config`，worktree 家族只有 `commondir`+回指檔 |
| 矩陣 | 新檔 `decision-matrix.md`，成為 resolver／spec／design／測試的**單一判定模型來源**；14 種故障狀態逐列 | 量死兩件事：`gitdir.parent.name == "worktrees"` 在**六個版面同時成立**（完全不可分）；L6/L7/L8 與 L5/L9/L10 的唯一區別是 `<common>.parent/.git` 那一格 |
| 模型 | `repo_evidence ∧ ¬worktree_marker` → 主樹；`worktree_evidence ∧ ¬repo_evidence` → 認證鏈；**其餘一切 → `None`** | 最後那一行取代三輪的逐案條件，**自然涵蓋**所有損壞狀態含該 P0 |
| resolver | 重寫為 S1–S4，段號對應矩陣章節；新增 `_readable_text` 把 stat 時與 open 時兩個拒絕點收斂為同一答案 | — |
| 測試 | 補 L9（worktree 內再建）與 M7 兩格；**移除兩條「手工 fixture 表示合法版面」的測試** | 真 git 版已存在，且當初正是為了讓它們過才手動補 `config` |

**驗證（全部仍成立）**：`7 failed / 3205 passed / 4 xfailed`，failed 與
`red-evidence.md` baseline 逐條相同；`test_project_state_root.py` **49 collected** 全綠；
矩陣 **17 格逐格實測 17/17**；`openspec validate --strict` 通過；link check 乾淨。

**變異檢查四項**：名字版判別式 → 3 紅；缺席版判別式 → 2 紅；S3 主樹分支拿掉
`¬worktree_marker` → 2 紅；S3 守門拿掉 `¬repo_evidence` → 1 紅。
⚠️ **最後一項第一次跑是 0 紅**——那個分支根本沒有測試覆蓋，是變異檢查找出來才補的。

**delta-integrity 閘門擋了一次且擋對**：全套一度 9 failed（比 baseline 多 2），
因為 spec 引入 `repo_evidence` 等三個新概念而 `tasks.md` 未提——spec 承諾了沒有
驗收步驟的東西。補 task 3.9 後回到 7。⚠️ **只跑 resolver 那一支測試會漏掉這條。**

#### 三輪外部審：全部未執行成功

使用者告知有額度後，一次扇出①②③，**三個全部因額度耗盡失敗**，下次恢復 **13:19**。

- ① 程式面第 4 次：派出後失敗
- ② 文件面：13 份改動文件超過單 batch 12 檔上限，已拆為規格類（4 spec + 矩陣）與
  敘事類（8 份）兩個 batch；batch 1 派出後失敗，batch 2 未派
- ③ Q8 報告：**回空 content**

⚠️ **③空回應的判讀已更正**：先前記為「thread 可能損壞、需輪替新 thread」，
**該判讀錯誤**。①②幾乎同時回額度錯誤，空 content 應重新解釋為**同一個額度耗盡的
另一種表現形式**。後果是做法不同——**不需要輪替 thread，只要重派**。
（在沒有第二個資料點時就給機制性解釋，那是猜測不是判讀。）

#### 規則解釋題已關閉（使用者 2026-09-22 裁定）

**②的補審義務是 Codex-specific，不是「任一獨立外部審即可」。**
fallback 可以在 Codex 不可用時讓工作暫時往前，**但它沒有把那筆 Codex review debt
消掉**；再跑一次 fallback 只會得到第二份降級審查，不算完成原義務。

⚠️ 射程限定：**這不表示所有高風險審查永遠只能 Codex**——只是這一筆已經產生的
補審義務，當時就是指名 Codex。此題自 09-21 起懸置，現已關閉，agent 不必再猜。

#### 狀態定位（使用者用語）

> **工作本體完成、外部 assurance 尚未清償。不是失敗，也不是要重跑 implementation。
> 下一步只需依序清 review debt。**

#### 待辦（依序）

1. **13:19 後採 strict serial dispatch**：先**只**派①（gate、改動最大、最值得優先
   吃額度），拿到結果再決定②③。**不再一次扇出。**
2. ② 仍欠 **Codex-specific** review（兩個 batch 都要過才算過）。
3. ③ 依序後排，重派即可、不必換 thread。
4. 仍未記任何 pass、仍未 commit；兩個 repo 皆 dirty。

#### 學習點（具體操作經驗，刻意不制度化）

> **派多個高成本審查前，先以最高優先級的那一件做 quota probe；成功後才扇出。**

這次真正的錯不是用錯 thread，而是**把「還有額度」誤當成「足夠同時跑三個重型審查」**。
兩者是不同的事實。⚠️ 同一個 session 稍早我自己寫過「先單獨派①探額度，通了再扇出」，
這次沒照做——因為使用者說有額度，我就把它讀成額度充足。

使用者明示**不要**把這寫成大的制度改造（不重構整套 review orchestration）；
它是一條操作經驗，不是新機制。

#### 本段的檔案異動

- `hooks/lib/project_state_root.py`（resolver 重寫為 S1–S4 + `_readable_text`）
- `hooks/lib/test_project_state_root.py`（49 collected：補 L9／M7×2、移除 2 條手工合法版面、docstring 改為矩陣入口）
- `openspec/changes/fix-worktree-canonical-root/decision-matrix.md`（**新增**）
- 同 change 的 `specs/project-state-root/spec.md`（步驟 3 重寫）、`design.md`（新增 D10）、`tasks.md`（新增 3.9）
- `文檔/handoff/session-handoff-20260922.md` — 本段


---

## Session 10:10（開工 10:10、跨日收工，本區塊寫於 2026-09-23 08:48）

> 這是與上方 `## Session 00:40` **不同的 session**：錨點快照記錄本 session 開工於
> `2026-09-22T10:10:43`、開工 commit `ff3e806`。上方區塊與其兩段追記屬前一個
> session，內容未改動。

### 一、本 session 主題

收掉一條已成熟的 backlog 觀察條目（A）、備妥①新 thread 的 first-dispatch prompt
（B）、核對②文件面的 batch 拆法（C）。

⚠️ **①始終未派出**——13:19 的額度窗在本 session 內過去而未使用。

### 二、完成事項

- **A：mature 條目「讀了名字沒讀它實際說什麼」依裁定關閉（甲案）。**
  主行 + 兩條證據子彈共三行，以三筆 exact-line deletion 經 validated writer
  （`backlog_triage.py execute`）刪除，各自回讀確認落地（`succeeded 3`）。
  驗證：檔案 91 → 88 行、`git diff` 顯示 3 deletions / 0 insertions、剩餘內容逐字
  相同、CRLF 只少 3 個（正是被刪那三行）、2 個既有裸 LF 未動、殘留掃描 0 命中、
  重跑 triage plan 為「0 筆可自動刪、0 筆待判斷、共 0 筆」。
  **裁定理由（使用者）**：機制留下、成熟度管制退出——攔截案例已實際發生，
  原本缺的掛點也已成為既有複審紀律。
- **C：②文件面的 batch 拆法核對成立。** 基線 13 份 `.md` = 規格批 5
  （4 份 spec + `decision-matrix.md`）+ 敘事批 8，兩批都在單 batch 12 檔上限內，
  **不需重拆**。
- **B：①新 thread first-dispatch prompt 定稿**（含使用者兩處收斂：問題 1 的範圍
  由「across every git layout」改為「this change / contract 宣稱支援的 layouts
  + malformed / missing / unreadable 狀態 + 宣稱 scope 有無明顯遺漏」；問題 2 不
  預先告訴 reviewer `decision-matrix.md` 是 source of truth，改由它自己判斷該檔
  在 change 中扮演什麼角色，並言明長期 normative contract 以正式 spec 為準）。
  **未派出。**
- **派工前基線核實（全部實跑、非推論）**：branch 基線 25 檔（11 `.py` / 13 `.md`
  / 1 `.yaml`）；兩層改動——已 commit `0b5cdb6` 21 檔 +2374 / −26，未 commit
  15 檔 +1228 / −187 外加 2 個新檔（`decision-matrix.md` 143 行、
  `resolve-exception-sweep.md` 149 行）；全套測試實跑
  `7 failed / 3205 passed / 4 xfailed`，7 條 failed 與 `red-evidence.md` baseline
  逐條相同；`test_project_state_root.py` 以 `--collect-only` 實測 **49 collected**，
  與文件宣稱一致。

### 三、未完事項 / 接力棒

- [#接力] ⚠️ **①從未派出。** 13:19 的額度窗在本 session 內過去而未使用（停在等
  使用者裁示）。prompt 已定稿、待派。**換新 thread 已拍板**——理由不是舊 thread
  跑太久，而是審查對象的概念模型已換代（前三輪逐案補洞的 resolver → S1–S4
  bounded redesign），fresh reviewer 比保留歷史上下文更有價值。
- [#接力] **② 仍欠 Codex-specific 補審**（兩個 batch 都要過才算過）。
- [#接力] **③ Q8 報告 doc review 待重派**，不必換 thread。
- [#接力] ⚠️ **仍未記任何 pass、仍未 commit。** 兩個 repo 依舊 dirty。
- [#不重議] 額度窗採 **strict serial dispatch**：只派①，拿到有效 verdict 才談②③。
  不再扇出。
- [#不重議] A 已結案（甲案）。未來若出現「掛點應該抓到卻漏掉、事後才發現」的新
  案例，針對**新的 failure mode** 另案處理，**不沿用這個舊 count**。

### 四、洞見 / 反省

**【紀律接力】**

- **寫入前先拿真實內容在記憶體裡跑一次寫入器，是這次唯一擋住「刪出孤兒」的動作。**
  那支 writer 名字說的是刪除條目，實際只刪一行；照 plan 預設輸出直接 confirm，
  會刪掉主行、留下兩條孤兒續行接到**上一條目**底下，而 schema 檢查、parser、lint
  **都不會喊**。
  ⇒ 動作版：**要用一支沒用過的寫入器動真檔前，先拿真實輸入跑一次它的 pure
  function、看它到底改了什麼**——不是讀它的 docstring 推論。
  attribute：複審紀律「先讀『實際驗到什麼』再讀『名字說驗什麼』」。
- **我第一次把這個缺口講成「writer 不支援續行刪除」，比事實寬。** 實測是 writer
  完全支援（續行在 `## 待辦` 的 digest 定址範圍內，`surface` 類的唯一前提是整行
  digest 在該區內唯一），缺口窄很多、在 `plan` 的候選列舉。
  ⇒ **宣告某工具「不支援 X」之前，先真的試著用它做一次 X。**
  attribute：全域 CLAUDE.md「宣告沒有／不存在前先列舉所有可能存放處逐一查完」的
  同型——載體從「東西在不在」換成「工具做不做得到」。

**【當日洞見】**

- **`backlog_triage` writer 的具體 limitation（依使用者裁定只記錄、不展開修復、
  不 bump 任何 count）**：`plan` 對一個條目只產出**第一行**當 `planned_digest`，
  續行不列入候選。**刪除能力本身支援續行**——補上續行的逐字 digest 當額外
  candidate 即可乾淨移除（本次即如此做）。缺口在**候選列舉**，不在刪除能力。
  處理時機：等 workflow-harness 目前這輪 review 收尾後另案處理。
- **收掉一條累積型觀察條目的判準**：那條條目把「規則沒防住的失誤」與「規則抓出來
  的失誤」混計在同一個數字裡（case 5、6 都是**變異檢查**抓到的，而變異檢查正是
  該規則自己的動作版），因此不論累到幾，都回答不了它要問的那個問題「規則有沒有
  效」。另外實測發現該 count 本身嚴重低估：另有 5 次同型案例被明寫「不 bump」
  （0903 / 0907 / 0909 / 0910 ×2），真實復發約 11 次、計數 6——**那個數字量的是
  記錄習慣，不是發生率**。

### 五、檔案異動

- `backlog.md` — 刪除 3 行（mature 條目主行 + 兩條證據子彈）。**本 session 對
  既有檔案的唯一異動。**
- `文檔/handoff/session-handoff-20260923.md` — **新增**。跨日閘門觸發，內容誠實
  記載「09-23 零實質工作」並指向本檔。
- `文檔/handoff/session-handoff-20260922.md` — 本區塊。

⚠️ 其餘 dirty 檔案（Q8 報告、`evidence/`、`work-map.jsonl`、
`session-handoff-20260921.md`、`recompute-correctness.py`、產品承諾 brainstorm）
**全部早於本 session 開工時間 10:10**，屬前一個 session 的遺留，不記在本 session
帳上。

### 六、下一步建議

1. **額度窗一開只派①**，用已定稿的新 thread first-dispatch prompt。strict serial，
   不扇出。
2. ①取得有效 verdict 後才談②（Codex-specific、兩 batch 都要過）與③（重派即可、
   不必換 thread）。
3. 三輪全過才談 commit → PR（需 `plan.md` 4.4a）→ merge → 更新 plugin cache →
   真實 linked worktree dogfood → 才把 `task-20260915-stop-hook-worktree-root`
   標完成。
4. `backlog_triage` plan 的續行候選缺口：等目前這輪 review 收尾後另案處理，
   **審查期間不要動它**（會污染基線）。
5. backlog 射程問題仍在：7 條 open 條目無穩定 `#NNN`、四輪時間盒 0/4、
   W37/W38/W39 三輪永久不計入。A 收掉後少一個受害者，問題本身未解。
