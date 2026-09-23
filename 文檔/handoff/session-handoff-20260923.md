# Session Handoff — 2026-09-23

## Session 08:46

### 一、本 session 主題

**跨日閘門觸發，非新 session。** 2026-09-22 10:10 開工的那個 session 一路跑到
09-23 08:43 才收工；本檔在 08:46 建立的唯一原因是**日期跨過午夜、Stop hook 要求
當日 handoff 存在**。

**09-22 的工作全部記在 `session-handoff-20260922.md`**，本檔不重抄。

### 二、完成事項

**無。** 09-23 到目前為止零實質工作——零檔案異動（本檔除外）、零 commit、
零審查派工。

⚠️ 這一欄是空的，而它應該是空的——**不要為了讓欄位看起來有內容而把 09-22 的
成果搬過來**。

### 三、未完事項 / 接力棒

- [#接力] 09-22 session 的接力棒全部有效，見 `session-handoff-20260922.md`
  的「三、未完事項」與「六、下一步建議」。核心是：**①（workflow-harness 程式面）
  的新 thread first-dispatch prompt 已定稿但從未派出**，13:19 的額度窗在 09-22
  session 內過去而未使用。

### 四、洞見 / 反省

**【紀律接力】**

- **跨日閘門第二次觸發（前一次 2026-09-22 00:40）。** 同一個正確反應：建一份誠實
  反映「今天還沒做事」的 handoff，而不是搬前一天的成果充數。⚠️ 這次的差別是
  **前一天有實質成果**——正因如此，搬過來的誘因比上次大，而沒有任何一層會抗議：
  `missing sections` 一樣是空的。

**【當日洞見】**

- 無。09-23 尚未有實質工作。

### 五、檔案異動

- `文檔/handoff/session-handoff-20260923.md` — 本檔（09-23 唯一的檔案異動）。

09-22 的檔案異動見 `session-handoff-20260922.md`。

### 六、下一步建議

1. 直接讀 `session-handoff-20260922.md` 的「六、下一步建議」照辦，本檔不重抄。
2. 額度窗一開**只派①**（strict serial，不扇出），prompt 已定稿。

---

## Session 11:05（開工 09:04、錨點 d78ca2a）

### 一、本 session 主題

清①（workflow-harness `fix-worktree-canonical-root` 程式面外部審）的 review debt：用新 thread 派第一次審查、逐輪修 finding、逐輪重審。

**狀態定位（照實寫，勿誤讀）：implementation 與本地 verification 已完成；external assurance 尚未取得 PASS。**
①**不是**「基本上已經過了、只差形式確認」——最後一輪 fresh review 仍抓出「兩個 marker 只驗一邊」「no-spawn 宣稱比實際守門範圍大」這類實質問題。

### 二、完成事項

外部審共拿到 **4 次有效 verdict，全部 ⛔ Blocked**；每一輪上一輪的 finding 都經審查者獨立驗證為已解決，無重提。

| 輪 | thread | 結果 | 內容 |
|---|---|---|---|
| 1 | `01a0cbd8`（MCP，5.6-sol） | ⛔ 2×P1 + 3×P2 | 子目錄 harness root 缺席當證據（使用者裁示**乙**：往上遇 linked worktree 入口 → unresolved，不換算回主樹）；`config` 只 stat 未 open；spec 殘留舊模型；封套測試零斷言；台帳母體數 |
| 2 | 同上 | ⛔ 1×P1 + 1×P2 + 1×Nit | 懸空 symlink 標記被 `exists()` 當不存在；design D9 等舊模型殘留（**我上一輪同類掃描漏的**）；台帳行號 |
| 3 | 同上 | ⛔ 1×P2 + 1×Nit | 第 2 輪修法把 `lstat` 錯誤轉成「存在」、被可讀證據越過（**我自己引入**） |
| 4 | **`01a0cc1f`**（新 thread，`codex exec`，5.6-sol） | ⛔ 4×P2 + 1×Nit | 兩個 marker 短路只驗一邊；Stop 擋下訊息宣稱有 `.git`（子目錄情境不實）；no-spawn 守門只蓋 5 個名字；台帳 319→320；fixture 紀律說法過嚴 |

換 thread 的原因：舊 thread 由 MCP 開、`codex exec resume` 撞 `already has an active writer` 鎖；且已達 R-a 輪替門檻（使用者選「新 thread」）。

**目前 worktree 上的本地驗證（全部實跑）：**
- 全套 `7 failed / 3225 passed / 4 xfailed`，**無 error**；7 條 failed 與 `red-evidence.md` baseline 逐條相同（passed 差額 = 本日新增測試數）。
- `openspec validate fix-worktree-canonical-root --strict` 通過。
- 本日新增／修正的行為全數做過變異檢查，對應測試確實轉紅（S0 五項、`config` open-time、懸空標記、`lstat` 錯誤兩種寫法、marker 短路、Stop 訊息、no-spawn 靜態守門）。
- ⚠️ 未解：第 3 輪後第一次全套曾出現 **1 個 error**，重跑與改動檔連跑 5 次皆未重現，**來源未抓到**——不能宣稱與本改動無關；再出現時先抓是哪條。

tasks.md 已記 3.10–3.13（每輪一條，含突變結果）。

### 三、未完事項 / 接力棒

- [#接力] ⚠️ **①仍未 PASS。** 新 thread `01a0cc1f-1b34-79a0-b455-018760cb7eb5` 的**第 2 輪因 Codex quota exhausted 未取得任何 verdict**（log：`try again at 3:04 PM`）。這次失敗**沒有產生 verdict、不算掉 reply round**。
- [#接力] **worktree 已 frozen**：`D:/workflow-harness/.worktrees/fix-issue-4-worktree-canonical-root`，15:04 前（及重審取得 verdict 前）不要再改任何檔案。
- [#接力] **round-2 prompt 已存檔、重派時保持不變**：`C:/Users/user/AppData/Local/Temp/claude/C--Users-user-orca-openspec-schemas/55243412-1bd0-42ba-8bba-719da52aaf79/scratchpad/fresh2-r2-prompt.md`（⚠️ 此為 session scratchpad、可能隨環境清除；遺失時照本段「二」第 4 輪 findings 重寫：列改動檔、要求獨立驗證五條、附測試事實、問是否引入新問題、同輸出格式）。
- [#接力] ⚠️ **仍未記任何 pass、仍未 commit。** 兩個 repo 依舊 dirty。
- [#不重議] **strict serial**：①取得有效 PASS 前，不派②③；PASS 後依序 ② → ③。
- [#不重議] 子目錄 harness root 走**乙**（不做通用往上探索；需要時另開 change）。
- [#不重議] 模型：①的 `01a0cc1f` thread 續用 **gpt-5.6-sol**；②③新 thread 用 **gpt-6-sol**（使用者已確認可用、不必先探）。
- [#操作資訊，不另開工作面] Codex 一律 `codex exec`、不用 MCP；**一律 `-m` 明寫模型**；在 Orca 裡 Codex 實際讀的 config 是 `%APPDATA%\orca\codex-runtime-home\home\config.toml`（不是 `~/.codex/config.toml`）。已記 memory `feedback_codex_exec_not_mcp`。

### 四、洞見 / 反省

**【紀律接力】**

- **修法射程比缺陷窄，同一 session 連發兩次，兩次都是對稱對的其中一邊。** 第 3 輪：`lstat` 錯誤處理只考慮了「無 worktree 證據」那一側；第 4 輪：兩個 marker 只修、只測了 `commondir`。⇒ 動作版：**修的東西若有對稱的另一半（兩個 marker、stat／open 兩個拒絕點、兩個家族），測試 MUST 對兩半參數化，變異檢查也要各拆一次**。attribute：全域 CLAUDE.md「一個缺陷＝一類缺陷」——規則已在，這兩次是沒套到「對稱對」這個形狀。
- **寫修正句時又寫出絕對句**：把「合法版面一律真 git」改寫成「每一種合法版面都至少有一條真 git 測試」，逐一找反例才發現 L1／L2 不成立。attribute：全域 CLAUDE.md「修正絕對句時寫出的替代句要再過一次例外檢查」——這次有照做、當場擋下。

**【當日洞見】**

- **變異檢查照出一條環境依賴的假綠**：`test_not_a_git_repo_returns_itself` 在維護者機器上實際走的是「主樹子目錄」路徑——**家目錄 `C:\Users\user` 本身是 git repo**，暫存目錄在它底下。拿掉「上層無 repo」分支測試仍綠才發現；已改為 stub 探測。
- **使用者指定「沿用同一個 thread」時，我沒提醒 R-a 輪替規則**（該 thread 已回覆 4 次），直到被鎖擋下才一起端出。這是該在指示當下就講的事實（使用者判斷不了沒聽過的規則）。
- **查設定檔要查「實際被讀的那份」**：早上判讀「config 09:57 改成 gpt-6-sol」看的是 `~/.codex/config.toml`，而 Orca 內 Codex 讀的是另一份；由 `codex exec` log 的 warning 路徑才發現。派工因一律 `-m` 明寫而未受影響。

**【學習候選】**

1. **Case**：同一 session 兩次修法只覆蓋對稱對的一邊（`lstat` 錯誤處理、兩個 marker），都由下一輪外部審抓到。
2. **Candidate Pattern**：修的程式若處理一組對稱成員，測試對全部成員參數化、變異對每個成員各拆一次。適用：成員可列舉的對稱結構；不適用：成員無法列舉時。
3. **Evidence**：本 session N=2（同一 change、同一類）；**Hypothesis**——跨 change 是否同樣高發未知。
4. **Minimum Sufficient Intervention**：不新增規則——既有「一個缺陷＝一類缺陷」已涵蓋，缺的是套用時認得「對稱對」這個形狀；先記錄、觀察是否跨 change 再發。
5. **Promotion**：History only。

### 五、檔案異動

**openspec-schemas（本 repo）**：本 session 零 commit；除本區塊外無檔案異動。git status 中的 dirty 檔（Q8 報告、`evidence/`、`work-map.jsonl`、`session-handoff-20260921.md`、`recompute-correctness.py`、產品承諾 brainstorm、`backlog-crosscheck-shadow.json`）**全部早於本 session**，不記在本 session 帳上。

**workflow-harness worktree**（未 commit；本 session 改動）：
- `hooks/lib/project_state_root.py`（S0 往上判定、`config` 真讀、`_entry_present` 以 lstat 判存在且不吸收錯誤、兩 marker 不短路、docstring）
- `hooks/lib/test_project_state_root.py`（49 → **67** collected：S0 子目錄四格、`config` open-time、懸空標記、`lstat` 錯誤兩類、no-spawn 靜態守門與對照、fixture 紀律 docstring 更正）
- `hooks/lib/test_paths_runtime_hook_read.py`（封套測試補斷言）
- `hooks/stop.py`（unresolved 擋下訊息改寫）、`hooks/test_stop.py`（⑥c／⑥d）
- `openspec/changes/fix-worktree-canonical-root/`：`specs/project-state-root/spec.md`、`decision-matrix.md`、`design.md`（D2 標取代、D9 表、D10、新增 D11）、`proposal.md`、`tasks.md`（3.10–3.13）、`plan.md`、`brainstorm.md`、`resolve-exception-sweep.md`

**repo 外**：memory `feedback_codex_exec_not_mcp.md`（新增）+ `MEMORY.md` 索引一行。

### 六、下一步建議

1. **15:04 後**，沿用新 thread `01a0cc1f` 重派①第 2 輪，**prompt 保持不變**：`codex exec resume 01a0cc1f-1b34-79a0-b455-018760cb7eb5 -m gpt-5.6-sol -c sandbox_mode='"read-only"' -c approval_policy='"never"' -o <結果檔> - < <prompt 檔>`（在 worktree 目錄下跑、放背景）。回來逐條實跑驗證再報。
2. ①取得有效 **PASS** 前不派②③；PASS 後：②（Codex-specific、兩 batch：規格類 5 + 敘事類 8，新 thread、**gpt-6-sol**）→ ③（Q8 報告 doc review，新 thread、gpt-6-sol）。
3. 三輪全過才談 commit（走 `/smart-commit --execute`）→ PR（需 `plan.md` 4.4a）→ merge → 更新 plugin cache → 真實 linked worktree dogfood → 才把 `task-20260915-stop-hook-worktree-root` 標完成。
4. 若①再 Blocked：先看是不是上一輪修法引入／半修（本日 4 輪中 2 輪如此），再修。

---

## Session 16:40（進行中快照：traceability 設計裁定；開工 11:31、錨點 d78ca2a）

> **性質：正式修訂前的裁定快照，不是設計文件、不是收工紀錄。** 9/1 Formal Design 本 session **未動**。
> 收工時仍須另跑 `/end-session` 寫收工區塊。

### 一、本 session 主題

需求追溯（Identity + Reference）：先做 repo-grounded 現況盤點並 commit 研究文件，再與使用者逐題裁定設計，
結果是對 2026-09-01 正式設計的一批修訂決定。

### 二、完成事項

- **研究文件落地**：`bb918e1` `docs/superpowers/research/2026-09-23-requirement-traceability-current-state.md`
  + research README 索引一列。fallback 文件審（contract-neutral-reviewer，Codex 額度用完）3 輪，末輪 ✅ Mergeable。
- **本日已拍板（使用者裁定）**：
  - **上位原則**：先定 Artifact 責任 → 要表達的資訊 → 語言／結構 → 出生處與 owner → 最後才決定 ID／reference／機械檢查；**結構化副本仍是副本**；已有 owner 的資訊優先引用或重算。
  - **Proposal**：撤回「Proposal → Requirement ID」（研究文件 §2 那一列與 §7 第 5 題已被推翻）；Proposal 留在 capability 粒度。
  - **Verification 模型**：驗收標的 → 方法 → Evidence → Result → Gate。Task 只保存施工階段的自動測試 RED/GREEN（RED 是不可重算的歷史事實）；inspection／manual-demonstration／analysis 的活動型證據由 `verification-results.json`（append-only 驗收台帳，S5 已決）保存，短證據直接寫、長證據引用 **repo 內已 commit** 的永久檔案（scratchpad、git-ignored ledger、未追蹤檔一律不得作證據落點）。「能重算」只指**程式可重算**。verify.md 是可覆寫的工作報告，不是證據 owner。
  - **Scenario coverage**：v1 仍必做，但 `Scenario → Evidence` 由 **Verification Result** 建立，不由 Task → Scenario 建立；Result 由 verify／review 階段產生，不由 implementer 自我驗收（無獨立 verifier 時依 G3 降級並留紀錄）。Evidence 已有 Task owner 就引用 Task；既有 regression test 等無 Task owner 者由驗證活動自產。Gate 機械查 coverage、freshness、引用存在與結構；不判語意充分性。
  - **Freshness**：v1 維持 coarse digest；**digest domain 由系統固定、不自我指涉**——排除 Result／verify.md／Gate 自己的紀錄與 change 外工作紀錄（如 handoff）；diff-aware invalidation 不拉進 v1。操作原則：候選版本穩定後才產生 Result。
  - **Verification target（甲′）**：Requirement／Scenario 是契約標的（Spec 擁有）；I1–I7 等是完成保障條件（Gate／Completion Contract 擁有）；matrix row／fixture／test case 是驗證材料，不升格為正式 target。後者內部覆蓋完整性不由 Gate 保證 → 補進 §8。佐證：Issue #4 spec `project-state-root/spec.md:39` 已明文「requirement 是契約、matrix 是證據」（維護者 2026-09-22 決定）。
  - **Identity preservation**：OpenSpec 負責 merge，Bridge 負責 stable-ID preservation；重複 ID、RENAMED 前後 ID 不同、未正式處置卻消失 → BLOCK。預演須在暫存複本實跑 OpenSpec archive（CLI 無 dry-run），不重寫 merge；有 delta spec 的 change 不得 `--skip-specs`。此檢查不保證同一 ID 下語意未被改弱（屬 G1a）。
  - **ID lifecycle**：以 capability 為唯一範圍；跨 capability 用 `capability / REQ-x`；退休後**永不重用**；搬移／拆分／合併一律「舊 ID 退休、新 ID 出生」，lineage 只供追溯、**不是 alias**、不繼承舊 Result；Requirement 層沿用 OpenSpec REMOVED 的 Reason + Migration；Scenario 退休需對等的顯式載體（格式未定），且必須記在 change 內隨 archive 保存；**archive 不得任意清理**（no-reuse 靠它，不建 registry）。
  - **舊 ID**：`REQ-PB` grandfathered，不因格式統一改名（已被 `claude-md-phase-boundary/verification-results.json` 引用）。
  - **Decision ID**：change-local；跨 change 引用即 `change / D<n>`；歸檔後不得重排。
  - **Formal Design 修訂治理**：修訂 9/1 本文，不開第二份 normative owner；章節號不動（作廢節保留標題並註明）；歷史引用回看 9/1 commit；修訂另行核可且不使事件閘門退回 NO；②～④ 全裁完後一次修改、一次文件審查；§2.3 措辭收斂與 9 筆 deferred findings 同批；plan「Global constraints 逐字照抄」同批重新裁定（是否為合法例外）。
  - **暫不處理**：capability rename（n=0）列入 §8 不保證，不建機制。
- **實測**（scratchpad，不動 repo）：單一 capability 11 個 RENAMED（補 `REQ-n` 前綴），`openspec validate --strict` 通過且 0 警告、`openspec archive -y` 成功（「→ 11 renamed」），**需求順序保留**。⇒ 現有 10 條補 ID 可按單一 change 規劃；`MAX_DELTAS_PER_CHANGE=10` 限的是 `ChangeSchema.deltas`，不等於 RENAMED 條數（其確切計數對象未追）。跨多個 capability 的情形未測。

### 三、未完事項 / 接力棒

- [#接力] **研究文件待更正兩處**（等正式修訂時一起做，屆時需再過文件審）：§2「Proposal → Requirement」列與 §7 第 5 題已被推翻；§8「RENAMED 後移到末尾」推論被實測推翻。
- [#接力] **未決小題**：Scenario 退休的顯式載體格式（形狀參考 REMOVED 的 Reason + Migration）。
- [#不重議] 上面「本日已拍板」各條，後續直接引用，不重開。
- [#接力] ①（workflow-harness Issue #4 外部審第 2 輪）本 session 未處理；Codex 額度窗 15:04 已開，仍待重派（見上一區塊六-1）。

### 四、洞見 / 反省

**【紀律接力】**

- **照抄 subagent 摘要數字，沒拿它自己的表格重數。** 研究初稿寫「4 可抓／5 助找／9 無助」，實際照表是 1（部分 2）／3／14；我抽查了 3 條事實卻沒驗最重要的那個總數，fallback 審 🔴 才抓到，修正時又寫出重複計數（「4–6 項」），第 2 輪再被抓。⇒ 動作版：**引用 subagent 的彙總數字前，從它的逐列資料重算一次；修正數字後，再用同一份資料重算一次。** attribute：全域 CLAUDE.md「證據先於斷言」＋「修正絕對句時寫出的替代句要再過一次例外檢查」——修正動作本身又是高發場景，這次是數字版。

**【當日洞見】**

- Issue #4 的 proposal 失同步（I3/I5/I6）根因不是「缺 ID」，是 **proposal 重述了 spec／tasks 已擁有的事實**；解法是拿掉副本，不是加比對。

### 五、檔案異動

- `docs/superpowers/research/2026-09-23-requirement-traceability-current-state.md`（新增，`bb918e1`）
- `docs/superpowers/research/README.md`（索引一列，`bb918e1`）
- 本區塊（未 commit）

### 六、下一步建議

1. **Next：依今日裁定製作 2026-09-01 Formal Design 的章節修訂 map；先列「哪一節改什麼、為什麼」，尚不直接修改正式設計。**

---

## Session 16:41（收工；同一 session，開工 11:21、錨點 d78ca2a）

### 一、本 session 主題

同上一區塊（16:40 快照）：需求追溯現況盤點 + 設計裁定。本區塊只補收工資訊，內容不重抄。

### 二、完成事項

- 見 16:40 快照「二」（研究文件 `bb918e1` + 本日全部裁定 + RENAMED 實測）。
- 收工結算：新登記 leftover `task-20260923-formal-design-revision-map`（掛 `task-20260826-superpowers-bridge-next-gen`）。既有「正式設計 §2.3 措辭收斂」一筆併入同批修訂，狀態不動、待修訂完成時一起結案。

### 三、未完事項 / 接力棒

- [#接力] 見 16:40 快照「三」（研究文件兩處待更正、Scenario 退休載體格式未決）。
- [#接力] ⚠️ ①（workflow-harness Issue #4 外部審第 2 輪）**仍未重派**；Codex 額度窗 15:04 已開。worktree 仍 frozen、prompt 檔仍在上上個 session 的 scratchpad（見 11:05 區塊「三」「六」）。

### 四、洞見 / 反省

**【紀律接力】**

- **引用 subagent 的彙總數字前，先從它的逐列資料重算；修正數字後，再用同一份資料重算一次。** 研究初稿照抄摘要「4 可抓／5 助找／9 無助」，照表實為 1（部分 2）／3／14；修正時又寫出重複計數「4–6 項」，fallback 文件審前後抓了兩次。attribute：全域 CLAUDE.md「證據先於斷言」＋「修正時寫出的替代句要再過一次檢查」。

**【當日洞見】**

- Issue #4 的 proposal 失同步，根因是它重述了 spec／tasks 已擁有的事實，不是缺 ID；解法是拿掉副本，不是加比對。
- reference 在 Issue #4 的 18 個真實缺陷中只對 4 項（約 22%）有幫助，最嚴重的幾項都幫不上。追溯機制的價值是「列出該看的地方」，不是正確性保證。

**【學習候選】**

1. **Case**：照抄 subagent 摘要裡的總數，沒有用它的逐列表格重算。
2. **Candidate Pattern**：引用他人彙總數字時，從原始逐列資料重算一次。適用於手上有原始資料的情況；拿不到原始資料時不適用。
3. **Evidence**：今天 1 個 case（同一件事錯兩次）；**Hypothesis**。
4. **Minimum Sufficient Intervention**：不新增規則，既有「證據先於斷言」已涵蓋；先觀察。
5. **Promotion**：History only。

### 五、檔案異動

- `bb918e1`：`docs/superpowers/research/2026-09-23-requirement-traceability-current-state.md`（新增）、`docs/superpowers/research/README.md`
- 本檔（16:40 快照 + 本區塊）、`workflow-harness/work-map.jsonl`（新增 leftover 一行）
- 錨來源：本 session 開工 commit（d78ca2a、開工於 2026-09-23T11:21:51）——列 d78ca2a..HEAD

### 六、下一步建議

1. **製作 09-01 正式設計的章節修訂 map**（`task-20260923-formal-design-revision-map`）：依 16:40 快照的裁定，列「哪一節改什麼、為什麼」，不直接修改正式設計。
2. ①：Codex 額度已恢復，可先在背景重派第 2 輪（prompt 不變），與 1 不互相影響；strict serial 仍適用（①PASS 前不派②③）。
