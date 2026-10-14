# Session Handoff — 2026-10-14

<!--
本檔每個 session 結束時 append 一個 ## Session HH:MM 區塊。
六欄 heading 順序固定，缺漏會被 Stop hook block。
四欄內 sub-segment marker（**【紀律接力】** / **【當日洞見】**）缺漏會 Stop hook ⚠️ Warn（不 block）。
-->

## Session 09:33

### 一、本 session 主題

接續 2026-10-13 10:03 之後重開的 session（開工於 2026-10-13T10:05）。任務是在 Superpowers 7.0 下 dogfood change `align-decision-handoffs`（superpowers-bridge schema）：從 brainstorm 一路做到 tasks。中間跨過午夜，本區塊在 10/14 收工。依使用者裁定停在 tasks 審查完成、plan 尚未開始的交接點。

### 二、完成事項

- **change `align-decision-handoffs`：4/8 個 artifact 完成，外加 tasks**（目錄未 commit，仍在 main 的 working tree）：
  - `brainstorm.md`：§0–§7 是決策紀錄與核可紀錄；§8 是核可後的使用者裁定，append 到第 19 點。
  - `proposal.md`、`design.md`（D1–D14）：文件審查共 11 輪，第 11 輪 ✅ Mergeable。
  - `specs/decision-handoffs/spec.md`（REQ-1–13）、`specs/default-schema-setup/spec.md`（REQ-1–6）：兩輪審查，第 2 輪 ✅ Mergeable。
  - `tasks.md`：六組、28 步；TDD applicable 只有 4.2（安裝程序）與 5.1（`version-check.yml` 讀列）兩項。兩輪審查都是 ✅ Mergeable，最後一輪換了新的審查對話（第 3 輪後換新 thread）。
  - `openspec validate align-decision-handoffs --strict` 通過；`doc_review pass` 已記（digest `sha256:65db5f80…`，2026-10-14T01:32Z）。
- **重大裁定**（全文見 brainstorm §8，這裡只列題目）：
  - v6 只支援 Superpowers 7.0.0；schema major 5 → 6、bundle 6.0.0。
  - v6 在獨立 branch 上完成並驗證，通過後才進 main；合併、push、tag 各自取得授權。
  - 預設入口改成 propose；安裝與升級時寫入預設 schema 並實測。
  - D14：proposal 與 design 分工，起因是本 change 自己 dogfood 時發現的漂移。
  - specs 階段：確認紀錄只能記錄使用者實際作出的確認；手動建立 brainstorm.md 的模板要加註解。
  - tasks 階段：`version-check.yml` 要用 v5／v6 兩列標記值不同的副本測，避免假通過；同一組 RED／GREEN 要用同一個 CLI 版本、同一套環境。
- **審查載體**：Codex 額度用完，doc_review 從 2026-10-13T07:13Z 起改由 contract-neutral-reviewer 代審（sticky）；另經使用者同意，加派 Fable 一次。
- **工作地圖**：`task-20260826-fix-brainstorming-drift` TODO → DOING。

### 三、未完事項 / 接力棒

- [#接力] **下個 session 從 plan 開始**（使用者裁定）。動手前先決定：tasks 最後一輪審查留下的 5 條 🟡 要不要在寫 plan 時一起修、併入 plan 那一輪審查。報告在本 session scratchpad 的 `docrev4/report.md`，scratchpad 清掉就沒了，所以要點抄在這裡：
  1. **6.2「舊句已不存在」用字串搜尋會假通過**：v5 `schema.yaml` 的舊句被 YAML 換行拆開（`may require`／`inference…` 第 108–109 行；`typically a decision`／`log` 第 50–51 行），未修改前 `grep "may require inference"` 就回 0。要先在 v5 原文證明抓得到，再拿去驗 v6。
  2. 2.6 的理由寫「由 6.1／6.3／6.6 檢查」，但三項都沒讀 `version: 6` 與 `VERSION` 的 `6.0.0`。
  3. 1.1 腳本的回報欄位沒有程序輸出、有沒有停下、有沒有詢問，REQ-2-S7／REQ-3-S2／REQ-4-S1 判斷不了；probe 指的是哪一個沒寫清楚；第 36–38 行「nothing for v5 to get wrong」不精確。
  4. subject 沒帶上安裝方法，多種方法跑同一案例時 RED subject 會重複，verify 會擋；prompt 方法沒寫清楚是 install、upgrade 還是兩者都跑。
  5. brainstorm §8 標題寫「第 18 點起於 specs 階段」，但第 19 點是 tasks 階段的裁定。
  - 另有 5 條 ⚪：RED／GREEN 的 bridge 版本與 clone 來源（main 仍是 v5）；互動式 `openspec init` 可能要使用者在終端機跑；5.5 的 append-only 證據沒寫進 verify.md；6.4 沒涵蓋附 Rulings 清單的開工紀錄形狀；§8 第 19 點的 1.14.1 從 D9／D12 沒有指回。
- [#接力] **plan 之後的順序**：
  - apply 前：建 v6 branch，在 branch 上 commit change 目錄（各自授權）。
  - apply（Start confirmation）→ verify → retrospective → archive。retrospective 必列 proposal／design 漂移的觀察。archive 在 Windows 上照 cp → diff → 使用者 rm。
  - 之後是 7.0 驗證輪，最後發版（各自授權）。
- [#接力] **待 commit（使用者裁定：不自動提交，main 日常紀錄與 v6 change 分開）**：
  - main：`backlog.md`（第 80 行 paused）、`workflow-harness/work-map.jsonl`、本 handoff 檔。
  - v6 branch：整個 `openspec/changes/align-decision-handoffs/`。
- [#待確認] **precommit 輕量 (b) 本次沒做**。原本排在收工時做：在根 CLAUDE.md 的 sd0x 退場段加一行「查 precommit 在 Windows 能否叫起 npm」，並加 backlog 指標。這次沒做，是因為使用者最新裁定「本輪不增加新治理程序」，我判斷這條也屬於那一類。這是我的解讀，要不要做、什麼時候做，由使用者決定。另外兩點要照實交代：CLAUDE.md 雖然每次都會載入，但升級流程不會讀那一段，所以它不是可靠的觸發點；而且要和 v6 分開審。
- [#接力] **OpenSpec 版本落差**：npm 最新是 1.14.1（2026-10-14 查），Compatibility 宣告 1.14.0，本機 1.3.1。依使用者裁定，本次只記錄、依 1.14.0 驗證。每週檢查會不會開提醒，以實際執行結果為準；我先前說「應該會開 issue」是推測。
- [#接力] **工作地圖**：`task-20260929-verification-strategy-research` 底下有 3 個 TODO 子項，下一步要挑哪一個，本次沒問，待使用者決定。
- [#接力] scratchpad 清理待使用者決定：
  - 本 session：`consult-tier/`、`docrev1/`～`docrev4/`、`proptest/`。
  - 上個 session：`upstream/`、`sd0x511/`、`ctl/`、`ctl2/`。
- [#不重議] brainstorm §8 第 1–19 點的所有裁定；proposal 與 design 已收斂，不退回，除非修改時發現與既有決策真的矛盾。

### 四、洞見 / 反省

**【紀律接力】**

- **說過頭／絕對句**（沿用）：spec 初稿寫了「SHALL NOT … rerun the whole discussion」，比 design 嚴，我自己抓到後改成「need not」。審查也抓到 REQ-1「The one exception」漏了第二種情況。共同形狀和以前一樣：寫 SHALL／SHALL NOT 時，沒有回頭對照 design 的每一個例外。
- **一個缺陷＝一類**（本 session 多次）：proposal 與 design 漂移在第 3、4、6 輪反覆出現，根因是我只修審查點名的那一處。第 6 輪之後改成送審前先跨文件掃同一個概念，之後才收斂。
- **precommit 缺口**：backlog 第 80 行，見三的 [#待確認]。

**【當日洞見】**

- **低嚴重度建議可以併進下一份 artifact 的審查輪**：specs 第 2 輪、tasks 第 3 輪留下的小建議，都改完後跟下一份文件一起送審，省下單獨審查的輪次，也沒有漏。前提是每次都要明講「這批修改還沒審過」。本 session 有一次使用者以為 tasks「審查中」，其實是改完還沒送審，我當場更正。
- **字串搜尋做「舊句已刪除」的檢查，碰到 YAML 換行會在修改前就是綠的**（tasks 第 4 輪審查發現）。這正是全域 CLAUDE.md「先讀實際驗到什麼」與「宣稱守住 X 時當場破壞 X 跑一次」那兩條要防的事；這次是審查員抓到，不是我先想到。
- 使用者的裁定「接受審查通過，但影響實作正確性的建議不能只因為通過就忽略」；我的做法是用「不修會讓 AI 讀到互相矛盾的條文、會讓驗收假通過」來判斷要不要現在修。
- 跨午夜後 Stop hook 連擋 4 次，要求寫 10/14 的 handoff。我選擇不提前收工、繼續做到使用者裁定的交接點，每次被擋都照實說明原因。

**【學習候選】**

- **Case**：tasks 6.2 用字串搜尋確認舊句已刪除，但 v5 原文的舊句被 YAML 換行拆開，修改前就搜不到，檢查在改之前就會是綠的。
- **Candidate Pattern**：用「搜不到」當「已刪除」的證據時，要先在修改前的原文上證明搜得到（正控制組）。適用範圍：靜態的不存在檢查。不適用：用解析器讀結構的檢查。
- **Evidence**：只有本次一例，而且是審查員實測發現的，屬 Hypothesis。全域 CLAUDE.md「宣稱這條測試守住 X 時當場破壞 X 跑一次」已經涵蓋同一個原理。
- **Minimum Sufficient Intervention**：不新增規則，寫 plan 時把正控制組寫進 6.2 的證據要求（見三，第 1 條）。
- **Promotion**：History only；既有規則已涵蓋，這次屬執行時漏用。

### 五、檔案異動

- 本 session 沒有 commit（錨點 `174e5c5..HEAD` 為空）。
- 未提交：
  - `openspec/changes/align-decision-handoffs/`（新增：`.openspec.yaml`、brainstorm、proposal、design、specs 兩份、tasks）
  - `backlog.md`（第 80 行 paused）
  - `workflow-harness/work-map.jsonl`（fix-brainstorming-drift → DOING）
  - 本 handoff 檔
- 不進版控：auto-memory 新增 `feedback_ship_then_learn_from_adopters.md`，並更新 MEMORY.md 索引。

### 六、下一步建議

- 先請使用者決定 tasks 那 5 條 🟡 是否在寫 plan 時一起修（建議：一起修、併入 plan 審查）。之後跑 `/opsx:continue align-decision-handoffs` 寫 plan。
- commit 等使用者分別授權：main 上的日常紀錄一筆，v6 branch 建立後 change 目錄一筆。
- precommit (b) 要不要做，由使用者決定。
