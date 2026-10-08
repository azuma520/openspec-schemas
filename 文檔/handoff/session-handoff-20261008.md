<!--
workflow-harness — Handoff template
對應 inventory：A5 六欄 schema、A6 append-only、A7 檔名 schema
檔名：文檔/handoff/session-handoff-{DATE:YYYYMMDD}.md
規則：append-only — 同日多 session append 多個「## Session HH:MM」區塊；前段不可改
-->

# Session Handoff — 2026-10-08

## Session 08:04

### 一、本 session 主題

（2026-10-07 17:47 開工、跨日於 2026-10-08 收工。）先做收尾雜務（push、scratchpad、`v3.0.0` tag 決策），再寫 C′ change `task-prefixed-plan-headings` 的 `design` 與 `proposal`。過程中使用者裁定版本與 release tag 規則，並決定 `release-versioning` 獨立成規格。文件審：Codex 兩輪（r2 ✅ Mergeable）、Fable 一輪 ✅。

### 二、完成事項

- 開工三步完成；主線照「2 先作、然後作 1」。
- **雜務**：push 完成（目前 main 與 origin 同步，0 筆領先）。scratchpad 清理：AI 的 `rm` 被權限擋，已給使用者 `!` 指令（是否已跑未確認）。
- **使用者裁定**（全文已寫進 design D6、proposal「版本與發布」）：
  - v4 Compatibility 列的「Baseline as of」填 `pending`，等對該列版本跑完完整流程才填；C′ 自己的 dogfood 不算完整相容重驗。
  - 方案 A：自 bundle 4.0.0 起，每個 release 打同版本 tag `vX.Y.Z`。這是落實既有 CLAUDE.md 規則，不是新政策。不提早建 v4.0.0、不補打 v3.0.0；v3→v4 退回用 SHA；本 change 修掉 README「v3.0.0 tag 已建立」的錯誤陳述。README 改用規則式寫法：「每個 bundle release 以同版本 Git tag `vX.Y.Z` 標記；此 release discipline 自 bundle 4.0.0 起實際執行。」
  - release commit 指 archive、最終驗證與 release 連動文件都完成後的最後一個 commit，不一定是 archive commit。順序：打 tag → push main 與 tag → 確認遠端 tag 指向該 commit。
  - v4.0.0 打 tag 放在工作地圖／release 收尾，不放進 tasks.md（放 tasks.md 會和 check 2 及 retrospective 時序衝突）。**C′ 的完成條件包含：遠端 v4.0.0 tag 已確認指向正確的 release commit。**
  - `release-versioning` 獨立成新規格。
- **`design.md`**（D1–D8、Risks、Migration、Open Questions）與 **`proposal.md`** 已寫完。change 進度 3/8，下一個是 `specs`。
- **登記** `task-20261007-version-tag-reminder`（TODO，掛 next-gen 下）：乙案，每週版本檢查遇到 VERSION 沒有對應 tag 時，在既有 issue 多加一行提醒、不讓 CI 變紅；v4.0.0 發布後再評估要不要做。
- **文件審**：
  - Codex r1 ⛔：🔴 `git ls-remote --tags origin v4.0.0` 對 annotated tag 回的是 tag 物件本身的 SHA，不是它指向的 commit。改用 `'refs/tags/v4.0.0^{}'`（peeled ref），並在拋棄式 repo 實測確認。另修 5 句說過頭的話。
  - Codex r2 ✅ Mergeable（thread `01a115d8-2c5d-70b0-843b-1cce29e812a5`，本對話已回覆 2 次）。
  - Fable 獨立審 ✅：實跑上游 task-brief，D3、D4 的說法都成立。
  - 「遠端沒有任何 tag」這句我自己查過：`git ls-remote --tags origin | wc -l` → 0。
  - 已記錄 `review-state note doc_review pass`。
- 封裝候選檢查：唯一 open 的 `[SOP 候選]`（precommit 入口）本 session 沒有觸發，不 bump。

### 三、未完事項 / 接力棒

- [#接力] C′ 進度 3/8，下一步 `/opsx:continue task-prefixed-plan-headings` 寫 `specs`：
  - `plan-contract` 的 delta：ADDED「條目標題辨識」需求與情境；REQ-1 的 1:1 規則不動。
  - 新的 `release-versioning` spec。
  - **寫 SHALL 條文前，先讀 schema check 12 的實作細節與特例**（全域規則）。
- [#接力] `design.md`、`proposal.md` 與工作地圖登記都還沒 commit，見本收工 commit。
- [#接力] **工作地圖名稱說過頭**：`task-20261007-version-tag-reminder` 名稱寫了「v1–v3 靜默失效三次」，但規則是什麼時候寫進文件的沒查過，這個說法沒有依據。名稱建立後不可改；要改就是 CANCELLED 再重登，留給使用者決定。
- [#接力] **C′ 完成條件**：`task-20261002-task-brief-heading-compat` 要到 archive、最終驗證、release 連動文件都做完，打 v4.0.0 annotated tag、push，並用 `git ls-remote --exit-code --tags origin 'refs/tags/v4.0.0^{}'` 確認遠端 tag 指向 release commit 後，才能標 DONE。push tag 要使用者當次授權。
- [#接力] scratchpad 待清：本 session 的 `dr1/`、`dr2/`、`fable/`、`tagtest/`；上個 session 的審查暫存（已給 `!` 指令，是否已跑未確認）；專案 scratchpad 底下約 50 個舊 session 目錄要不要清，由使用者決定。
- [#不重議] 本 session 的版本、tag 裁定（見「二」），以及 design D1–D8。

### 四、洞見 / 反省

**【紀律接力】**

- **修正句說過頭**（沿用，本 session 5 次以上）：
  - 「不讓既有 plan 失效」
  - 「不改會讓 CI fail」（實際是不會 fail，只是默默讀到 v3 列）
  - 「規則靜默失效三次」（沒查規則何時寫入）
  - 「附三句」（實際三句加一句建議）
  - 「check 13 本身不改」

  另有一處寫進了改不掉的地方：工作地圖名稱。做法照舊：寫出替代句後，再過一次例外檢查；**寫進不可改的載體（record 名稱、tag）之前多查一次**。
- **說要先做的查核，被授權後跳過**（沿用）：本 session 未發生。
- **審查等級傳低了**（沿用）：本 session 未發生。

**【當日洞見】**

- **annotated tag 的遠端確認要看 peeled ref**：`ls-remote` 不加 `^{}` 拿到的是 tag 物件本身的 SHA，拿去和 commit 比一定對不上。Codex 抓到，我在拋棄式 repo 實測確認。
- **CLAUDE.md 跨檔耦合表寫的「CI 直接 fail」不成立**：新增 v4 列、v3 列還在時，`grep | head -1` 會默默讀到 v3 列。已列入 C′ 的 D8 一併修正。
- **把步驟塞進 tasks.md 前，先看 schema 的檢查時序**：打 tag 一定發生在 archive 之後，放進 tasks.md 會和 check 2 及 retrospective 衝突，改由工作地圖的完成條件承載。
- **沿用交接裡的數字當現況**：開工時照抄 handoff 的「5 筆未 push」，報成 6 筆，實際是 8 筆。跟昨天的「Compatibility 5.1.0 一路沿用」是同一種形狀：拿上次記下的值當成現在的事實。

【學習候選】

- **Case**：開工時拿交接裡的未 push 筆數當現況報出去（6 筆，實際 8 筆）；昨天 Compatibility 的 5.1.0 也是沿用未重驗的值。
- **Candidate Pattern**：交接或文件裡的「狀態類數字」（筆數、版本、計數）引用到現在的判斷前，先用一條指令重算。只適用於會隨時間改變的狀態值；已決定的事項不適用。
- **Evidence**：2 例，形狀相近但載體不同（handoff 數字、README 表格值），**Hypothesis**。
- **Minimum Sufficient Intervention**：不新增規則。開工 hook 若要注入交接數字，可以順手附上即時 `git rev-list --count origin/main..HEAD`，要不要做由使用者決定。觀察中。
- **Promotion**：History only（如果使用者認為兩例屬同一類，可升 Pattern Candidate）。

### 五、檔案異動

錨來源：本 session 開工 commit（3d04040、開工於 2026-10-07T17:47:03）——列 3d04040..HEAD（本 session 沒有中途 commit；以下是 working tree 改動）

- `openspec/changes/task-prefixed-plan-headings/design.md`（新）：D1–D8、Risks、Migration、Open Questions
- `openspec/changes/task-prefixed-plan-headings/proposal.md`（新）：Why、What Changes、Capabilities（新 `release-versioning`、修改 `plan-contract`）、Impact
- `workflow-harness/work-map.jsonl`：新增 `task-20261007-version-tag-reminder`
- 本交接檔（新）

### 六、下一步建議

1. 主線：`/opsx:continue task-prefixed-plan-headings` 寫 `specs`（`plan-contract` delta 加上新的 `release-versioning`）。寫完一樣走文件審；Codex thread 還能再回覆 1 次，再多就換新對話。
2. 不搶主線：清 scratchpad，並決定 `version-tag-reminder` 名稱裡說過頭的那句要不要處理（不處理也可以，交接已記錄）。

## Session 09:29

### 一、本 session 主題

先收尾上一份交接留下的事（工作地圖名稱那句話查證、清 scratchpad），再把 C′ change `task-prefixed-plan-headings` 從 3/8 推到 6/8：寫完 `specs`、`tasks`、`plan`，規劃階段全部完成。過程中使用者裁定補上第三項 breaking。

### 二、完成事項

- 開工三步完成；照使用者指示「先做 2（名稱那句、清 scratchpad）再做 1（specs）」。
- **工作地圖名稱那句話查證成立，不改**：打 tag 的規則最晚在第一次宣告 bundle 1.0.0 時就已存在（2026-05-14 commit `f7624d6`）；1.0.0、1.0.1、2.0.0、3.0.0 四個 release 在 fork 與原作者 repo 都沒有 tag。名稱寫「v1–v3 三次」照 schema major 算成立，照發版次數算是 4 次，屬偏保守。
- **scratchpad**：51 個舊 session 目錄（約 33MB）由使用者以 `!` 指令刪除；本 session 的審查暫存也都已清空並確認。
- **specs**（commit `238ecbe`）：`plan-contract` 新增 REQ-4「條目標題辨識」（10 個情境）；新規格 `release-versioning`（REQ-1–4）。寫條文前讀了 check 12 的每個特例，條文裡明寫 v2/v3 日期與舊退回說明不在範圍。
- **使用者裁定 A**：`##1.1`、縮排的 ` ## 1.1` 在 v4 不再是條目，列為第三項 breaking，已同步到 proposal、design（D2 相容性、Risks、Migration、D7 新增測試資料列）。三種例外都以兩條路徑掃過 repo 全部 45 個 `plan.md`，皆 0 筆。design D6 改寫成查證過的 tag 歷史。
- **tasks**（commit `1efb729`）：18 步、4 組（測試資料先建 → schema → 連動文件 → 整合）；只有 2.2 是 `TDD: applicable`。
- **plan**（本收工 commit）：18 個條目全用 `## Task <n>` 寫法，開頭聲明刻意比安裝的 v3 說明新、1:1 檢查要等 4.1 同步後才有效。以 v4 規則自查 18↔18 對應、無重複；8 條規格引文逐字比對通過。
- **文件審**（Codex，共 3 個新對話）：
  - specs + proposal/design：r1 ⛔（🔴 fixtures README 路徑錯；🟡 縮排 H2 其實是 Markdown H2、47 應為 45）→ 全修 → r2 ✅（thread `01a118fa-f582-7213-ac3c-bf05c540ef5a`，已回覆 1 次）。
  - tasks：r1 ✅（thread `01a1190a-9be5-7ad2-9e99-3ed3e8d9a50c`）。
  - plan：r1 ✅ 附 🟡（4.1 前置漏了 3.3/3.4/3.8）→ 修 → r2 ✅（thread `01a1191b-391b-7573-8fc1-a58470eb655f`，已回覆 1 次）。
  - 各輪都記了 `review-state note doc_review pass`。
- 封裝候選檢查：唯一 open 的 `[SOP 候選]`（precommit 入口）本 session 沒有觸發，不 bump。
- 工作地圖：「納入 execution record capability」標為 NEXT（它是「§7 Completion Gate 落地」唯一的子項）。

### 三、未完事項 / 接力棒

- [#接力] C′ 進度 6/8，下一步 `/opsx:apply task-prefixed-plan-headings`。照 tasks.md 順序：先建測試資料（1.1–1.3），**在改 schema 之前**跑出 2.2 的 RED（盲測：執行的 Agent 不可看到 fixtures README）。
- [#接力] tasks 3.8 需要「第一個 `version: 4` commit」先存在才能填退回 SHA → apply 中途要請使用者授權一次 commit。
- [#接力] 本機領先遠端 3 個 commit（`238ecbe`、`1efb729`、本收工 commit），push 需使用者授權。
- [#接力] C′ 完成條件不變：archive、最終驗證、release 連動文件完成後打 v4.0.0 annotated tag、push，並用 `'refs/tags/v4.0.0^{}'` 確認遠端指向 release commit，才能把 `task-20261002-task-brief-heading-compat` 標 DONE。
- [#接力] 研究題 Verification Strategy 底下 3 條 TODO 尚未選定下一步（使用者未指定）。
- [#不重議] 第三項 breaking（裁定 A）；工作地圖名稱那句不改；上個 session 的版本、tag 裁定與 design D1–D8。

### 四、洞見 / 反省

**【紀律接力】**

- **說過頭的句子**（沿用，本 session 3 次：1 次自己抓到、2 次被 Codex 抓到）：
  - 「`##1.1` 和 ` ## 1.1` 在 Markdown 都不是 H2」：縮排 1–3 格其實仍是 H2（Codex 抓到）
  - 「47 個 plan.md」：`*plan.md` 把 `merge-plan.md` 也算進去，實際 45 個（Codex 抓到）
  - 「規則比 1.0.0 早」：其實是同一個 commit，改成「最晚在第一次宣告 1.0.0 時」（自己抓到）

  做法照舊，另加一條：**附和使用者裁定時，裁定裡的事實型理由也要逐條驗**——這次回「同意」時沒驗「符合正常 Markdown heading」這個前提。
- **說要先做的查核，被授權後跳過**（沿用）：本 session 未發生。
- **審查等級傳低了**（沿用）：本 session 未發生。

**【當日洞見】**

- **寫條文前去讀實作的每個特例，這次真的抓到東西**：check 12 現行條文沒要求 `##` 後有空白、也沒限定 `##` 在行首；design 漏列了這項 breaking，是讀特例分支時才發現的。
- **「找不到來源」不等於「說法錯」**：交接說工作地圖名稱「沒依據」，實際查 git 歷史後那句話成立，只是當初沒查就寫。
- **計數用的搜尋條件要精確對到檔名**：`*plan.md` 會連 `merge-plan.md` 一起抓。

【學習候選】

- **Case**：使用者貼來的裁定附了理由（「符合正常 Markdown heading」），我回「同意」時沒驗這個前提，後來 Codex 審查才發現它只對一半。
- **Candidate Pattern**：附和或照辦裁定時，裁定裡出現的事實型理由要跟自己寫的句子一樣過例外檢查。只適用於可查證的事實；價值判斷不適用。
- **Evidence**：本次 1 例，**Hypothesis**。
- **Minimum Sufficient Intervention**：不新增規則，併入既有「說過頭的句子」紀律接力觀察。
- **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（e139fc1、開工於 2026-10-08T08:34:38）——列 e139fc1..HEAD

- `238ecbe`：`openspec/changes/task-prefixed-plan-headings/specs/plan-contract/spec.md`（新）、`specs/release-versioning/spec.md`（新）、`proposal.md`、`design.md`（第三項 breaking、D6 歷史、fixtures README 路徑）
- `1efb729`：`openspec/changes/task-prefixed-plan-headings/tasks.md`（新）
- 本收工 commit：`openspec/changes/task-prefixed-plan-headings/plan.md`（新）、`workflow-harness/work-map.jsonl`（一筆標 NEXT）、本交接檔

### 六、下一步建議

1. 主線：`/opsx:apply task-prefixed-plan-headings`，從測試資料 1.1–1.3 開始，改 schema 前先拿到 2.2 的 RED。
2. 不搶主線：push 本機領先的 3 個 commit（需授權）；研究題 Verification Strategy 要不要選定下一步。
