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

# Session Handoff — 2026-09-30

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

## Session 08:39（跨日延續：2026-09-29 15:04 開工的 session，換日後由 Stop hook 要求建檔）

### 一、本 session 主題

0929 已收工（handoff `session-handoff-20260929.md` 的 Session 18:04 區塊、commit `5519c64`）後的換日補記：只做 scratchpad 暫存檔清理。**本 session 實質內容一律以 0929 18:04 區塊為準**。

### 二、完成事項

- scratchpad 暫存檔已由使用者手動刪除（`rsi-*` 檔案、`idtest1`～`idtest4`、`rsi-preview1`），`ls` 確認目錄已空。
- 過程小插曲：清理指令 `rm -f rsi-* … && rm -rf …` 的 `rsi-*` 也比對到資料夾 `rsi-preview1`，`rm -f` 報錯使 `&&` 後段未執行，第二次改為只跑 `rm -rf` 才清完。

### 三、未完事項 / 接力棒

- [#接力] 全部照 0929 18:04 區塊三、六（下一步＝寫 `requirement-scenario-identity` 的 tasks.md，RED 排在改 schema 之前）。
- [#待確認] Stop hook 報「未偵測到本 session 開工讀 handoff」：開工時實際以 `PYTHONUTF8=1` Python 讀了 handoff（全域規則要求含中文檔用 Python 讀），hook 偵測不到非 Read 工具的讀取。是否記進 backlog `[優化建議]` 由使用者決定。

### 四、洞見 / 反省

**【紀律接力】**

- **查「已決」的範圍要含前一個同類 change 的每份 artifact，不只 handoff 與主 spec。**（延續 0929 18:04：TDD applicability 來回三次，直到讀 fix-v2 的 tasks.md 才看到 9/07 使用者裁定。）動作版：動手同類工作前，把上一個同類 change 的 brainstorm／design／tasks 開頭註解列入查已決範圍。attribute：全域 CLAUDE.md「提案前先查已決」。

**【當日洞見】**

- 給使用者用 `!` 跑的刪除指令，glob 同時可能比對到檔案與資料夾時，不要把 `rm -f` 與 `rm -rf` 用 `&&` 串在一起——前段對資料夾報錯就會吃掉後段。

### 五、檔案異動

- 本檔（新建）。repo 內無其他改動；scratchpad 在 repo 外。

### 六、下一步建議

1. 讀 `session-handoff-20260929.md` 的 Session 18:04 區塊與凍結的四份 artifacts，寫 tasks.md。
2. 追 issue #19 有無回應。


## Session 09:20

### 一、本 session 主題

寫 `requirement-scenario-identity` 的 tasks.md 與 plan.md：使用者裁定盲測執行方式（決定一 B、決定二 C），兩份經 Codex 文件審（tasks 2 輪、plan 3 輪）後一起 commit（`7809ef4`）。

### 二、完成事項

- **tasks.md**（12 步驟、5 組）：①身分 mutation fixtures＋盲測器材（開跑前凍結）→ ②RED 盲測 baseline（完成前不得改 `schema.yaml`）→ ③check 13＋GREEN 雙人盲測（同一 task）、specs 作者規則＋`version: 3` → ④連動表面（templates、bridge README en/zh-TW、VERSION、version-check.yml、CLAUDE.md、roadmap、根目錄 README bridges 表）→ ⑤dogfood 同步、補號遷移驗收、Verification Strategy 試行紀錄。檔頭註解承載裁定全文與 RED 順序理由。
- **使用者裁定（2026-09-30）**：判定交給對本 change 無脈絡、看不到預期答案的 subagent；RED 1 位、GREEN／conformance 2 位；同模型（RED 與 GREEN 同一個，派工時明確指定並記錄）、同 blind prompt、同 fixture 副本、同規則來源與操作程序，差別只在獨立 context；執行者不得得知預期判定；兩位不一致不投票、記為 rule ambiguity 並 BLOCK；不做統計實驗；結果表至少記 fixture／預期／RED 實際／GREEN A／GREEN B／是否一致／不一致或失敗類型。AI 補充、使用者同意：PRECHECK 與 check 5 讀 repo git 紀錄，fixture 天生不滿足，標「不適用於 fixture」；RED 問的是「checks 1–12 有沒有任何一條抓到身分缺陷」。
- **plan.md**：12 條合約 entry 與 tasks 1:1；9 條全域約束經程式逐字比對 spec 原文。
- **文件審**：tasks r1 ⛔（3 🔴：`openspec instructions {specs,verify}` 跑不動、bridge README 現行版本句未涵蓋、根目錄 README bridges 表漏列）→ r2 ✅。plan r1 ⛔（2 🔴：3.1／3.2 依賴環、覆蓋清單漏 REQ-4-S6／REQ-7-S1／REQ-7-S3）→ r2 ⛔（拆兩段仍是 task 層級環）→ r3 ✅（原 3.1＋3.2 合併為新 3.1、原 3.3 改編 3.2）。`review-state.js note doc_review pass` 已記；審查暫存檔已由使用者清除。

### 三、未完事項 / 接力棒

- [#接力] **下一步＝apply，從 tasks 1.1 做 fixtures**。開工先讀 tasks.md 檔頭裁定；fixtures 落在 `docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/`，每個是含主 spec＋change 的迷你 `openspec/`。
- [#接力] 歸檔後 follow-up（照舊）：`contract-identity` 的 `## Purpose` 會是 CLI 產生的 TBD，要補。
- [#接力] 未 commit、照舊保留：`backlog-crosscheck-shadow.json`、`2026-08-27-brainstorm-產品承諾.md`。
- [#待確認] Stop hook 偵測不到非 Read 工具讀 handoff（延續 08:39 區塊），使用者尚未決定是否進 backlog。

### 四、洞見 / 反省

**【紀律接力】**

- **TDD applicable 的 task，GREEN 必須在自己的 task 內取得。** Plan Contract 的「Blocked by」以整個 task 為單位；GREEN 若要另一個 task 產出，就形成依賴環，把 task 拆成前後兩段也繞不過（plan r2 Codex 擋下）。動作版：寫 plan 前逐一確認每個 applicable task 的 GREEN 取得在自身 task 內。
- （延續）查「已決」的範圍含上一個同類 change 的所有 artifact——本次先讀 fix-v2 tasks.md 再動筆，照做了。

**【當日洞見】**

- 覆蓋核對要把權威來源全列出來比，不靠記憶列：tasks 1.1 首版漏 3 個 scenario，把 spec 38 個 scenario 全列逐條比才補齊。
- 「schema 改完就無法補 RED」理由不精確：舊規則文字 `git show` 拿得回。RED 排在改 schema 前的真正理由是它記錄「修改前實際跑過」這個事實。
- scratchpad 清理：AI 的 `rm` 被全域 `~/.claude/settings.json` 的 `deny: Bash(rm *)` 擋（對話授權越不過、allow 也蓋不過 deny）。提過三案（維持現狀／移到 ask／專用清理腳本），**使用者 2026-09-30 選維持現狀**：審完由 AI 給指令、使用者用 `!` 跑。不進 backlog。

**【學習候選】**

1. **Case**：plan 首版把 GREEN 取得放在另一個 task，形成依賴環；拆兩段仍不行，最後合併成一個 task。
2. **Candidate Pattern**：TDD 證據（RED／GREEN）由誰產生，要與 task 邊界一致。
3. **Evidence**：本次 1 例。**Hypothesis**。
4. **Minimum Sufficient Intervention**：不新增規則——schema plan instruction 已定義 Blocked by；Observe。
5. **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（7c6842b、開工於 2026-09-30T08:42:48）。

- `7809ef4` docs(openspec): add tasks and plan for requirement-scenario-identity — A `openspec/changes/requirement-scenario-identity/plan.md`、A `openspec/changes/requirement-scenario-identity/tasks.md`
- 本 handoff（本區塊）。
- 非本 session、照舊未 commit：`backlog-crosscheck-shadow.json`、`2026-08-27-brainstorm-產品承諾.md`。

### 六、下一步建議

1. 進 apply：做 tasks 1.1 的 fixtures（先讀 tasks.md 檔頭裁定）。
2. 追 issue #19（sd0x adapter Windows alloc）有無回應。


## Session 17:58

### 一、本 session 主題

`requirement-scenario-identity` apply：**12/12 tasks 全部完成、每個都通過對應 task 審查**，在 worktree 分支 `worktree-requirement-scenario-identity` 上 4 個 commit（未 push、未併 main）。Verification Strategy pilot（RED→GREEN 雙人盲測）跑完。**worktree 保留、不 teardown**；本交接寫在 main（使用者護欄：handoff／work-map owner 在 main）。

### 二、完成事項

- **執行方式**：照 schema apply 用 worktree（使用者裁定 A）＋ subagent-driven-development（每 task implementer＋獨立審查；1.1 為主 session 自做，已揭露並補 strict-reviewer 兩輪 ✅）。所有裁定、執行、審查結果逐筆記在 SDD ledger，已複製進 repo：`docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/sdd-ledger.md`（append-only）。
- **1.1–1.3**：22 個 mutation fixtures（5 正向／16 違規／1 無法判定）、README（預期答案・覆蓋表・結果表）、盲測器材 v1。實測發現 `openspec archive` **中止時結束碼仍是 0** → plan 5.2 驗收與 check 13 成功判準改為「結束碼 0 且 change 已移入 archive/」（使用者 1A）。
- **2.1 RED**（sonnet 盲測、schema 修改前）：22 題全 PASS → 17 個缺陷全被舊規則放行、17 個 TDD subject；執行者其實看到缺陷但 checks 1–12 無規則可擋。
- **3.1 check 13**（Fable 寫）：審查修 4 輪（I1 無 ID 新標題漏報／I2 數量不符後的類別歧義／I3 已 sync capability 被誤判違規→使用者裁定「按 capability 判無法判定、sync 前驗證只是 recovery guidance」／I4 「任何已套用 delta 都會中止歸檔」為假，controller 實測推翻）。
- **GREEN**：r1/r2（器材 v1）B 各錯 1 題（v13 類別漏填；v06 FINAL 與自身判定矛盾）→ 使用者裁定 **修量測器材、不修規則、只重跑一次**；器材 v2（FINAL 唯一權威欄、固定英文代碼、開跑前凍結 grader）；RED provenance 採混合（原始 RED 為正式時序證據、v2 replay 為基線複驗）。**v2 replay 22/22 PASS＝與原始 RED 一致；v2 GREEN A、B 皆 22/22、FINAL 逐行相同** → 17 組 RED/GREEN 寫入 tasks.md 3.1，checks 8–12 腳本驗過。
- **3.2／4.1–4.3**：specs instruction ID 語法與配號兩層、`version: 3`；templates；bridge README en/zh-TW（Why/Migrating v2→v3、check 13 摘要與連結）；VERSION 3.0.0、CI 列鍵 v3、CLAUDE.md、roadmap、根 README。Superpowers baseline 維持 v5.1.0（使用者裁定 B：baseline＝宣告相容基準，v6.4.1 只記為本次 apply 的觀察環境）。
- **5.1–5.3**：dogfood 同步；補號遷移預演歸檔驗收——**approved deviation**：`repo-guidance` 歸檔後 3 行純空白差異、非空白內容一致，plan 原文不改（使用者裁定 A）；5.3 試行觀察寫入 fixtures README §5。
- **文件審**：Codex 兩輪 ✅（plan 1.1/5.2 修訂）→ 第 3 輪 Codex 額度用完 → fallback 改派 contract-neutral-reviewer（Fable）✅ Mergeable（**sticky：本 change 文件審不切回 Codex**）。
- **commit**（執行備援：worktree 隔離擋掉 `/smart-commit` 腳本 → 使用者裁定手動 git add/commit＋等價檢查）：`1de8e10` test(poc)、`3780ab3` feat(schema)、`05fd2f8` docs、`2bc8a56` docs(poc)；無 AI 署名、未 push。

### 三、未完事項 / 接力棒

- [#接力] **下次從 SDD 全分支總審開始**（最強模型、看整個 `42c3d24..worktree-requirement-scenario-identity`；總審要讀 ledger 的 deferred minors）。之後順序：**總審 → 關文件審（sticky fallback：contract-neutral-reviewer／Fable）＋程式碼審（`schema.yaml` 屬 code plane）→ verify → retrospective → archive**。
- [#接力] **archive 需要使用者協助 `rm`**（Windows 目錄鎖：cp → diff -r → 委派使用者 rm；見 memory `feedback_opsx_archive_windows_dir_lock`）。
- [#接力] **worktree 位置**：`C:\Users\user\orca\openspec-schemas\.claude\worktrees\requirement-scenario-identity`（分支 `worktree-requirement-scenario-identity`，tree 乾淨）。下次用 `EnterWorktree path` 進去；本 session 已以 ExitWorktree keep 回到 main 寫交接。worktree 內的 dogfood schema 副本（gitignored）已同步到 v3；**main 的 `openspec/schemas/` 仍是舊 v2 副本**，併回 main 後要重同步。
- [#接力] 盲測 kit／報告的 scratchpad 暫存（`%TEMP%/claude/.../efe9f4f7-.../scratchpad/`）已把正式證據複製進 repo，可清；清理指令收工時由 AI 給、使用者 `!` 跑。
- [#待確認] 要不要把 **verify／sync lifecycle 研究題**登記進工作地圖（「verification 依賴的 pre-sync 狀態會被合法的 sync 步驟消耗」；使用者 2026-09-30 說先只記 ledger、不塞進 Identity change）。
- [#待確認] 要不要把 **5.2 空白行變動的成因**（為何只有 repo-guidance、其餘三個 capability 沒有）開 backlog `[bug]`/`[優化建議]`。
- [#待確認] （延續）Stop hook 偵測不到非 Read 工具讀 handoff。
- [#接力] 未 commit、照舊保留：`backlog-crosscheck-shadow.json`、`2026-08-27-brainstorm-產品承諾.md`。

### 四、洞見 / 反省

**【紀律接力】**

- **驗收指標要直接對到 claim，機械判準也會量錯東西。** 本日兩例：`openspec archive` 中止仍回 0（exit code ≠ 成功）；5.2 逐行比對因空白行失敗而內容其實不變（line equality ≠ 內容契約）。動作版：寫驗收條件時問「這個指標若過，claim 一定成立嗎？若不過，claim 一定不成立嗎？」兩邊都要答得出來。attribute：全域 CLAUDE.md「先讀『實際驗到什麼』再讀『名字說驗什麼』」。
- **看到結果之後才改判準＝移動球門；改量測器材之前要先分清「規則錯」還是「器材錯」。** 本日 v06：判定對、FINAL 抄錯 → 修器材＋凍結＋只重跑一次，不修規則、不 16/17 收掉、不重試到綠。

**【當日洞見】**

- 第二位獨立執行者確實暴露了第一位看不出的不穩定（r1、r2 各一次、不同題）；失敗面分三類：規則理解、執行不穩定、**回報／評分不穩定**（原先沒預想到的第三類）→ 支持「agent 判斷、機械彙總」的方向（觀察，見 fixtures README §5）。
- 審查者列為「範圍外」的觀察不能直接略過：I4（CLI 行為假宣稱）就是從 re-reviewer 的 out-of-scope note 實測挖出來的。
- 自己寫 brief 也會製造缺陷：器材 v2 的 4 代碼集是 brief 規定的，缺「不擋的無結論」槽——審查在 replay 前抓到。
- 具名 Agent 會開 Orca 分頁、不具名不會（已記 memory `named-agents-open-orca-tabs`）。
- **worktree 摩擦 8 例**（使用者裁定：只記不修，作為 `task-20260904-worktree-handoff-lifecycle` 實測案例）：①EnterWorktree 預設從 origin/main 開（本地領先 25 commit）②gitignored dogfood 副本不在 worktree ③隔離拒跑「複雜且碰 worktree 外」的指令 ④worktree 路徑深撞 Windows 260 字元上限 ⑤main 的 dogfood 副本與源差 2 個 template EOL ⑥隔離擋 `orca terminal create`（Codex 看不到分頁）⑦隔離擋任何 `bash <腳本>` → `/smart-commit` 跑不動、降級手動 ⑧`artifact_paths` 依 cwd 把 handoff 解析到 worktree 內 → 需 ExitWorktree keep 回 main 才能照護欄寫交接並 commit。

**【學習候選】**

1. **Case**：驗收判準兩度與 claim 脫鉤（archive exit 0、逐行比對 vs 內容不變），一次在寫 plan 時、一次在驗收時才發現。
2. **Candidate Pattern**：每條機械驗收條件，寫下它要保護的 claim，並確認「指標過 ⇒ claim 成立」與「claim 成立 ⇒ 指標過」兩方向。
3. **Evidence**：本日 2 例（不同載體：CLI 結束碼、文字比對）。**Hypothesis**。
4. **Minimum Sufficient Intervention**：不新增規則——全域 CLAUDE.md 複審紀律已有「先讀實際驗到什麼」；Observe，下次寫 plan 驗收時試用「兩方向」自問。
5. **Promotion**：Pattern Candidate（由使用者決定）。

### 五、檔案異動

錨來源：本 session 開工 commit（42c3d24、開工於 2026-09-30T09:29:45）——列 42c3d24..HEAD（main 上 0 筆）。本 session 的 commit 全在 worktree 分支 `worktree-requirement-scenario-identity`：

- `1de8e10` test(poc): add identity mutation fixtures and blind-test evidence — 234 files（`docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/**`）
- `3780ab3` feat(schema): add stable requirement/scenario IDs and verify check 13 (schema v3) — `superpowers-bridge/{schema.yaml,VERSION,README.md,README.zh-TW.md,templates/spec.md,templates/verify.md}`、`.github/workflows/version-check.yml`
- `05fd2f8` docs: sync repo surfaces to schema v3 and record identity task progress — `CLAUDE.md`、`README.md`、`README.zh-TW.md`、`docs/roadmap{,.zh-TW}.md`、`.gitattributes`、`openspec/changes/requirement-scenario-identity/{plan,tasks}.md`
- `2bc8a56` docs(poc): record identity migration acceptance and pilot observations — fixtures `README.md`、`migration-acceptance.md`、`sdd-ledger.md`、`tasks.md`
- main：本 handoff（本區塊）。memory 新增 `feedback_named_agents_open_orca_tabs.md`（repo 外）。
- 非本 session、照舊未 commit：`backlog-crosscheck-shadow.json`、`2026-08-27-brainstorm-產品承諾.md`。

### 六、下一步建議

1. 進 worktree（`EnterWorktree path`）→ **SDD 全分支總審**（最強模型；帶 ledger deferred minors 清單）。
2. 關文件審（fallback Fable、sticky）＋程式碼審（`schema.yaml`）→ verify → retrospective → archive（使用者協助 rm）→ 併回 main、重同步 main 的 dogfood 副本。
3. 決定兩個 [#待確認]：verify/sync lifecycle 研究題是否登記；5.2 空白行成因是否開 backlog。
