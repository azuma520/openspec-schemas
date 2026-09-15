# Session Handoff — 2026-09-11

<!--
本檔每個 session 結束時 append 一個 ## Session HH:MM 區塊。
六欄 heading 順序固定，缺漏會被 Stop hook block。
四欄內 sub-segment marker（**【紀律接力】** / **【當日洞見】**）缺漏會 Stop hook ⚠️ Warn（不 block）。
-->

## Session 08:15

### 一、本 session 主題

**承 2026-09-10 未收工的 session（跨日）：fix-v2-blocking-defects 收尾 + research 文件 doc gate。** ⚠️ 本區塊在 session **進行中**寫入（跨日觸發 Stop hook），非收工紀錄；收工時以 `/end-session` 補完。0910 的 session 沒有跑 `/end-session`（使用者下班、session 保持開啟），0910 的正式收工紀錄也待補。昨日主線：Codex 正式 branch review r1（⛔ 4 P1 + 5 P2）→ 使用者採甲（四條對既有裁定記 USER_SKIPPED、修五條）→ verify 由主 session 重跑 → contract drift 三方對照研究文件 → 使用者收斂研究（Q10 四步 sweep 為觀察期習慣、A/B 平行、不擴研究、work-map 採手改）。

### 二、完成事項

- 08:10 確認：昨晚 19:47 的 session-only 定時提醒未觸發（session 關閉即消失）；work-map `.superpowers` 引用仍 1 處（使用者尚未手改）；worktree HEAD `b07d571`、11 個改動檔狀態與昨日快照 r3 相同。
- research doc gate：昨日 r1（8 🔴）、r2（6 🔴）全部修畢；今晨原 thread `01a08aa4` 已不存在（MCP 過夜重啟），記 `[THREAD_ROTATED]`，依首派契約開新 thread 重派（含 Task Context 五格），背景執行中。
- 已請使用者手改 worktree `workflow-harness/work-map.jsonl` 第 20 行的 `.superpowers/sdd/plan/` 引用為永久副本路徑。

### 三、未完事項 / 接力棒

- [#接力] **research doc gate 新 thread 回報後**：逐條回源核實、修屬實 🔴、pass 則 `review-state note doc_review pass`；舊 thread 的 r1/r2 finding 由本端對帳（記錄在 `文檔/handoff/attachments/20260910-pilot2/pilot3-research-doc-review-r1.md`）。fast tier cap 6（已用 2 輪 + 本輪）。
- [#接力] **fix-v2 Codex 複審**：等使用者改完 work-map → 回讀確認 → 重 hash 快照（附錄 `pilot2-snapshot.md` 追加 r4）→ 原 thread `01a08a0b` 預期也已失效，開新 thread 首派（metadata + 更正後 39 檔 baseline；四條 USER_SKIPPED 報告回來後對帳，不進 prompt）。派工單草稿在 scratchpad `fixv2-codex-reply-r2.md`（若改首派，只取其 baseline / 修正清單當 metadata）。
- [#接力] Codex ✅ 後收尾順序（使用者 0910 拍板）：smart-commit worktree（含 3 個未追蹤 review 報告）→ tasks.md 若有動則 verify 重跑 → retrospective 補記 → archive（cp + diff -r + 委派使用者 rm）→ 併 main（work-map.jsonl 兩邊各有對方沒有的條目，要手動合）→ push。
- [#接力] 0910 handoff 正式收工區塊待補（`/end-session` 時一併處理，或於本 session 收工時在 0910 檔 append）。
- [#不重議] 研究到此收斂、不再擴；不新增 Skill / Gate；B 方向另開小實驗；Codex 失敗不派 fallback。

### 四、洞見 / 反省

**【紀律接力】**

- [#觀察] session-only 的排程提醒在使用者關閉視窗後不會存活；「下班前設提醒」若要跨夜有效，需要的是 durable 排程（本 harness 無），或改寫成接力棒讓下個 session 開工執行。
- [#觀察] Codex MCP thread 過夜失效（`Session not found`），loop review 的「同 thread 複審」在跨日時一律要走 `[THREAD_ROTATED]` 首派；scope baseline 與 dispositions 依規則留在本端對帳。

**【當日洞見】**

- 待本 session 收工補。

### 五、檔案異動

錨來源：本 session 承 2026-09-10 09:07 開工 commit（5aa19bf）——列 5aa19bf..HEAD

`5aa19bf..HEAD`（main）：`fc8f552` research provenance analysis、`98cc5e2` work-map pilot 登記（皆 0910）。

main working tree（未 commit）：`docs/superpowers/research/2026-09-10-contract-drift-archaeology.md`（新、未追蹤，doc gate 進行中）、`docs/superpowers/research/README.md`（M，索引列）、`文檔/handoff/attachments/20260910-pilot2/`（未追蹤：Codex r1 報告、七項紀錄、dispositions、sealed lists、Pilot 3 紀錄、快照 r3）、本檔。

worktree `.claude/worktrees/loosen-plan`（HEAD `b07d571`，未 commit、等 Codex ✅）：`.gitattributes`、`openspec/changes/fix-v2-blocking-defects/{plan,proposal,retrospective,tasks,verify}.md`、`specs/tdd-evidence-contract/spec.md`、`superpowers-bridge/schema.yaml`（MM）、`templates/{design,plan,spec}.md`（staged EOL）、未追蹤 `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/`（3 檔）。

**無專案資料夾** → Changelog skip。**驗收節點無實條目** → skip。**work-map**：本 session 零 record 狀態變化。

### 六、下一步建議

1. 收 research doc gate（新 thread 回報 → 核實 → pass 或再一輪）。
2. 使用者改完 work-map 後送 fix-v2 Codex 複審（新 thread 首派）。
3. Codex ✅ 後照收尾順序走到 push；每個 git 寫入動作都等使用者核准。


## Session 08:31

### 一、本 session 主題

**收工紀錄。** 本 session 承 0910 未收工（跨日），08:10 接續：work-map 由使用者手改並驗證；兩個 Codex thread 過夜失效 → 各記 `[THREAD_ROTATED]` 首派；research doc gate 新 thread r1 抓 5 條新 🔴（全屬實、已修），r2 與 fix-v2 首派皆撞 Codex 額度（13:12 恢復）。使用者決定先收工。

### 二、完成事項

- work-map 修正：使用者以 `sed` 改 worktree `workflow-harness/work-map.jsonl` 條目 `task-20260908-author-surface-gate-alignment` 的 `.superpowers/sdd/plan/` 引用為永久副本路徑；本端驗證只有 `name` 欄變、其餘行逐字相同；快照 r4 記入 `pilot2-snapshot.md`（blob `ddcdf58`）。
- research doc gate 新 thread（`01a08dce`）r1：⛔ 5 🔴 + 2 🟡，Context mismatch 1（解析基準寫窄）。五條全屬實並修：解析基準改為列舉 branch 觸及的所有路徑族；報告副本標「尚未追蹤」；H1 改為「耦合表六列對本 change 零命中、連動來自 D6」（retrospective 歸功耦合表為紀錄錯誤）；§0 SSOT 搜尋補 artifact 級 owner 宣告（`templates/design.md:20`、`loosen-plan/design.md:42`、CLAUDE.md dogfooding）；B 類重編為五子型（lexical 3 / record 文法 5 / 集合邏輯 1 / 控制流程 1 / 訊息 2）並重生所有依賴句。`doc_review fail` r3 已記。
- 今日 handoff 08:15 進行中區塊；0910 補記正式收工區塊。
- 封裝候選檢查：backlog 無未結案 `[SOP 候選]`；使用者已明示不新增機制，痛點記入四。

### 三、未完事項 / 接力棒

- [#接力] **13:12 後**：①`codex-reply` thread `01a08dce-afeb-73f0-8dfd-361714bcbea9` 送 research doc gate r2（re-review 模板；五條 🔴 已修；cap 6、已用 3 輪）；✅ 記 `doc_review pass` 後 research 文件 + README 索引列走直接 commit（smart-commit --execute、使用者核准）。②fix-v2 branch review **新 thread 首派**（thread `01a08a0b` 已失效；prompt = 0911 08:15 送出的那份：Task Context 五格、39 檔 + 3 個未追蹤報告的 baseline、`gpt-5.6-sol` high、cwd worktree）；回來驗 sentinel、逐條回源、四條 `[USER_SKIPPED]`（`pilot2-codex-r1-dispositions.md`）與 sealed list 對帳、記七項。③Codex ✅ 後收尾：smart-commit worktree（含 3 個未追蹤報告）→ tasks.md 若動則 verify 重跑 → retrospective 補記 → archive（cp + diff -r + 委派使用者 rm）→ 併 main（work-map.jsonl 兩邊各有對方沒有的條目、手動合）→ push。每個 git 寫入都等使用者核准。
- [#接力] Q10 四步 sweep 觀察期：下次修 reviewer finding 起執行（改前 `rg` 命中 → 改 → 改後 `rg` → `diff -r`），只記三個數（做了幾次 / 每次命中幾個表面 / 下一輪 reviewer 還抓到幾條多表面型）。
- [#接力] B 方向小實驗待另開：拿 §2 B 類真實輸入做共用定義層的紙上結構化，不改 schema、不定格式。
- [#不重議] 不新增 Skill / Gate / reviewer 層 / routing；Codex 失敗不派 fallback；研究不再擴。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] 修 review finding 時又照抄了紀錄裡的斷言當事實兩次（retrospective 的「同 commit」、0909 已更正的「內部席位當散文讀」），加上把 `:146` 改錯成 `:147`——都在 Codex doc review 抓到。既有規則「finding 裡的事實宣稱與文件原句同等地位、都要回源」涵蓋，N 再 +2，不新增規則。
- [#反] 用腳本重算表格計數時只數了主類欄、沒數次類欄（G 8 → 實為 12）；「來源 → 方法 → 結果」的方法欄寫了，但方法本身漏了一欄。同族：CRLF 量測。
- [#接力] 使用者 09-10 收斂裁定：Q10 四步 sweep 為後續 2–3 次 fix finding 的觀察期習慣（不升 Skill/Gate）；A/B 平行、B 另開小實驗；研究到此不擴；work-map 採手改（記 tooling observation：`work_status_register.py` 沒有描述修正原語）。已寫 memory。
- [#接力] Codex MCP thread 過夜失效、session-only 排程隨視窗消失——跨夜的接續只能靠接力棒，不能靠 thread 或 cron。

**【當日洞見】**

- 換 thread 等於換一雙眼睛：research 文件同一版本，舊 thread 兩輪沒抓到的 5 條 🔴，新 thread 第一輪全抓到、全屬實。「同 thread 複審」省 context 的代價是 reviewer 會被自己前兩輪的框架帶著走。
- 耦合表對 fix-v2 的改動類型六列零命中——連動之所以發生，是 design D6 點名，不是表；而 retrospective 把功勞記給表，我照抄了兩次才被抓出來。
- fix-v2 收尾在等 Codex 額度（13:12），已知缺陷清單與四條 USER_SKIPPED 都準備好對帳。

**【學習候選】**

1. **Case**：修 finding 時把「紀錄／reviewer 的斷言」抄成事實，本週第 4 例。
2. **Candidate Pattern**：引用任何紀錄的宣稱前，先跑一次能證偽它的最小命令（`git show --stat`、行號回讀）。
3. **Evidence**：N=4 跨三種載體（retrospective、research、review finding）；Hypothesis：紀錄越權威越容易被免驗。
4. **Minimum Sufficient Intervention**：不新增規則；既有「證據先於斷言」涵蓋；掛點＝Codex doc review 每次都抓得到。
5. **Promotion**：Case Memory。

### 五、檔案異動

錨來源：本 session 開工 commit（98cc5e2、開工於 2026-09-10T14:16:03）——列 98cc5e2..HEAD

`98cc5e2..HEAD` 為空（main 無新 commit）。working tree：

- main：`docs/superpowers/research/2026-09-10-contract-drift-archaeology.md`（未追蹤，doc gate ⛔ r3）、`docs/superpowers/research/README.md`（M）、`文檔/handoff/attachments/20260910-pilot2/`（未追蹤：Codex r1 報告、record、dispositions、sealed lists、Pilot 3 紀錄、snapshot r3/r4）、`文檔/handoff/session-handoff-2026091{0,1}.md`（慣例不進版控）。
- worktree `.claude/worktrees/loosen-plan`（HEAD `b07d571`）：`.gitattributes`、`openspec/changes/fix-v2-blocking-defects/{plan,proposal,retrospective,tasks,verify}.md`、`specs/tdd-evidence-contract/spec.md`、`superpowers-bridge/schema.yaml`（MM）、`templates/{design,plan,spec}.md`（staged EOL）、`workflow-harness/work-map.jsonl`（使用者手改）、未追蹤 `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/`。

**未 commit**：doc gate 與 code gate 皆 ⛔（等 Codex），依 terminal completion invariant 不收 commit。**無專案資料夾** → Changelog skip。**驗收節點無實條目** → skip。**work-map（main）零變更** → 結算 no-op。

### 六、下一步建議

1. **13:12 後先收 research doc gate**：`codex-reply` thread `01a08dce`（五條 🔴 已修）；✅ 後記 pass、smart-commit research 文件 + README 索引列。
2. **再送 fix-v2 branch review 新 thread 首派**（prompt 見 0911 08:15 那份；四條 USER_SKIPPED 報告回來後對帳）；✅ 後照接力棒收尾順序走到 push，每個 git 寫入等使用者核准。
3. **Q10 四步 sweep** 從下一次修 reviewer finding 開始執行並記三個數。
