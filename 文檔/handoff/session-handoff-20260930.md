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
