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

## Session 14:50

### 一、本 session 主題

C′ change `task-prefixed-plan-headings` 從 6/8 做到結案並正式發布：照 SDD 跑完 apply（18/18）、verify、retrospective、文件審、archive，fast-forward 併入 `main`、push，建立並推送 repo 第一個 tag `v4.0.0`（schema major 4／bundle 4.0.0）。開工時另回覆 workflow-harness session 一則跨 session 詢問（「規則升級四維度」出處：查 memory 未找到，已照實回覆、未改檔）。

### 二、完成事項

- 開工三步完成；使用者指示「繼續、不用一直問」，主線直接做 apply。
- **Apply（SDD，worktree `.claude/worktrees/task-prefixed-plan-headings`、branch `feat/task-prefixed-plan-headings`）**：
  - fixtures f14–f23（RED→GREEN 3、breaking 3、回歸 3、綜合對照 1）＋ fixtures README 凍結預期。
  - 2.2 TDD：盲測 red-v3（改前條文）3/3 判錯方向正確 → schema 改寫 → green-v4-r1 3/3 正確；紀錄寫在 tasks.md 2.2。2.5：v4-25-r1 10/10；補充 v3-supp 6/6。完整表格與 check-12 sha256 存進 fixtures README §2026-10-08 盲測紀錄（tracked）。
  - schema.yaml：Plan Contract 正面條目規則、check 12 鍵值收集＋fence 開關、check 12/13 不對稱理由、`version: 4`。模板、VERSION 4.0.0、bridge README en/zh（遷移、Known breaking、Compatibility v4 列 `pending`、S11）、version-check.yml 改讀 v4、CLAUDE.md、roadmap、根 README 狀態欄。
  - 4.2：上游 task-brief（Superpowers 6.4.1）抽 1.1/1.2/1.3/4.2，與 plan 原文逐行相同。3.5：workflow_dispatch run `37723513752` 讀到 1.14.0/v5.1.0。
  - 審查：每組任務審＋修正複審、最後整體審（opus）＋一次修正波＋複審；裁定 R1–R16 已端給使用者、無推翻。
- **verify**（獨立 opus 執行者）⚠️ PASS WITH WARNINGS、無 BLOCK；**retrospective** 已寫。
- **文件審**：Codex 4 批全因額度用完失敗（`codex_fail`，reason=quota）→ 改派 `contract-neutral-reviewer`，4 批 ✅ Mergeable（SENTINEL_VALID）；使用者裁定 A 修 4 項會誤導讀者的 🟡（rollback 可達性前提、validate-schemas 觸發條件、design/proposal 過時「0 筆」、retro 不實句）→ 重審 ✅；CLAUDE.md 再一行修正 → 重審 ✅；archive 後兩份主規格審 ✅。
- **Commits（皆使用者當次授權）**：`0b11be5`（實作）、`d5770b4`（收尾＋verify＋retro）、`d2a350c`（archive）。分支 push 兩次。
- **Archive**：暫存複本跑真正 `openspec archive -y` 當標準答案 → 套進 worktree → 使用者 `rm` 原 change 目錄 → `openspec/` 與標準答案 diff 為空、`validate --all` 6/6。
- **發布**：本機 `main` fast-forward 到 `d2a350c` → push `main`（e139fc1..d2a350c）→ CI Validate schemas run `37739053544` success（v4 首次 CI 驗證）→ annotated tag `v4.0.0` 推送，`git ls-remote --exit-code --tags origin 'refs/tags/v4.0.0^{}'` = `d2a350c4a992994f9d054b1cbb00617b53593143`（release commit，使用者裁定 A）。
- 工作地圖 `task-20261002-task-brief-heading-compat` → DONE（readback ok）。
- 封裝候選檢查：唯一 open 的 `[SOP 候選]`（precommit 入口）本 session 未觸發，不 bump。

### 三、未完事項 / 接力棒

- [#接力] **清理（使用者已同意發布後處理，尚未做）**：
  - worktree `.claude/worktrees/task-prefixed-plan-headings`（內含 git-ignored 的 SDD ledger `.superpowers/sdd/plan/`；證據已搬進 tracked 檔、裁定已列給使用者）。worktree 不在 `.worktrees/` 下，移除要用 `git worktree remove`。
  - 本機與遠端分支 `feat/task-prefixed-plan-headings`（遠端停在 `d5770b4`，`d2a350c` 已在 main）：刪遠端分支屬對外動作，需授權。
  - scratchpad（本 session 的 blind/、docrev*/、arch1/、vt-*/ 等）：AI 的 rm 會被擋，給使用者 `!` 指令。
- [#接力] **延後的審查項（記錄，未修）**：`release-versioning` 主規格 Purpose 仍是 archive 自動填的 TBD；plan-contract REQ-4 把「不提前結束」歸給 REQ-1（REQ-1 沒寫）；v1→v2、v2→v3 舊 rollback 仍寫「pin bundle」（設計 Non-Goal）；check 12 理由句缺「as of Superpowers v6.4.1」（R15）；README :580「since v2」與 :657「since v1」措辭；CLAUDE.md:203 重算指令沒寫 `main`、不可 squash 的理由也繫於 `0b11be5`；f18/f19 可能被 markdown 自動格式化「修好」；fixtures README :32 開頭仍寫「v2 checks 8–12」。
- [#接力] **R8 提醒（使用者）**：roadmap「v4 — Released」只在遠端 tag 存在後才成立——現已成立。
- [#接力] Codex 額度：本次 14:47 前用完，之後的審查先確認額度。
- [#不重議] release commit = `d2a350c`；tag 不隨後續交接 commit 移動；整條分支不得 squash／rebase 的規則（已寫進 README 與 CLAUDE.md）；R1–R16。

### 四、洞見 / 反省

**【紀律接力】**

- **說過頭的句子**（沿用，本 session 至少 4 次，3 次被審查抓到、1 次自己抓到）：
  - 「`737aa56` 目前只在承載 v4 的 branch 上」——寫完前一刻我才剛對使用者說過本機 main 也有它（審查抓到）。
  - 「改成『fixtures 以外沒有』」——只改了 README，同類句在 design D2/D4、proposal 沒一起改（審查抓到；一個缺陷＝一類缺陷沒做到）。
  - 存備援審查報告時先存了自己節錄的版本，差點拿節錄版去驗證「原始報告」（自己抓到，改存逐字原文）。
  - check 12「與上游劃分任務一致」（實作子代理寫的、任務審抓到）。

  做法照舊，另加一條：**修一個 finding 時，用 grep 掃同一句話在其他 artifact 的副本**（design / proposal / README 常有同一事實的三份陳述）。
- **說要先做的查核，被授權後跳過**（沿用）：本 session 未發生。
- **審查等級傳低了**（沿用）：本 session 未發生。

**【當日洞見】**

- **證據要寫明落在哪個 tracked 檔**：盲測結果一開始只在 git-excluded 的 SDD ledger，與 loosen-plan 弄丟證據同一形狀；最後整體審查才救回。
- **條文綁 sha 的證據讓後期措辭修正變貴**：check 12 改一個理由句，GREEN 與 2.5 都要重跑；之後用 R15 擋下第三次重跑。
- **worktree 預設從 `origin/main` 起分支**：本機領先遠端時會漏掉 plan，要改從本機 HEAD 開。
- **worktree 隔離檢查會擋含 `git` 字樣的複合指令與 `orca … --shell git-bash`**：拆成單純指令；Orca 分頁派不成時依 CLAUDE.md 改背景 Bash。
- **使用者貼來的裁定裡有一句前提不成立**（「archive 還沒完成」）：照辦結論、更正理由，沒有附和。

【學習候選】

- **Case**：一個 finding 修在 README，同一事實在 design D2/D4 與 proposal 的副本沒改，審查下一輪才指出。
- **Candidate Pattern**：一個 change 內同一事實常有多份陳述（proposal / design / README / retrospective）；修其中一份時，以該事實的關鍵詞 grep 全 change 目錄與連動文件。只適用於「事實陳述」型 finding；措辭風格不適用。
- **Evidence**：本次 1 例；與全域「一個缺陷＝一類缺陷」同類，**Hypothesis**（是既有規則的一個未被觸發的實例，而非新規則）。
- **Minimum Sufficient Intervention**：不新增規則；併入既有「說過頭」紀律接力觀察。
- **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（737aa56、開工於 2026-10-08T09:40:28）——列 737aa56..HEAD

- `0b11be5`：schema.yaml、VERSION、templates/plan.md、bridge README en/zh、根 README en/zh、version-check.yml、CLAUDE.md、roadmap en/zh、fixtures f14–f23 與 fixtures README、change tasks.md
- `d5770b4`：fixtures README（盲測紀錄）、CLAUDE.md、roadmap、bridge README en/zh（rollback SHA 與修正）、design.md、proposal.md、tasks.md、verify.md（新）、retrospective.md（新）
- `d2a350c`：change 目錄移至 `openspec/changes/archive/2026-10-08-task-prefixed-plan-headings/`；`openspec/specs/plan-contract/spec.md`（+REQ-4）、`openspec/specs/release-versioning/spec.md`（新）
- tag `v4.0.0` → `d2a350c`
- 本收工 commit：`workflow-harness/work-map.jsonl`（C′ → DONE）、本交接檔

### 六、下一步建議

1. 清理收尾：worktree 已解除登記、本機分支已刪（`-D`，tip `d2a350c` 在 origin/main）、scratchpad 已清；剩空目錄 `.claude/worktrees/task-prefixed-plan-headings/`（rmdir 回 Device or resource busy，疑本 session 仍持有 handle；下個 session 開工時 `! rmdir` 它）與遠端分支是否刪除。
2. 接續工作地圖：`6.x 相容基準重新定錨`（C′ 的 S11 證據已可納入）；`每週版本檢查加 VERSION 無 tag 提醒`（v4.0.0 已發布，該重新評估）。
3. 延後的審查項（見三）挑要不要開小 change 處理，優先 `release-versioning` Purpose TBD。

## Session 17:15

### 一、本 session 主題

同一 session 14:50 收工後的延續（使用者指示補記，故追加新區塊而非沿用「同 session 只 append 一次」）：決定 v4 之後的方向（6.x 相容基準重新定錨），完成第一步「能力契約缺口盤點」研究與 D1–D5 裁定，修正工作地圖上 execution record 的表示，並完成第一個工作單位「README 上游行為描述更正」（審查通過，待 commit）。

### 二、完成事項

- **方向**：使用者裁定 v4 之後優先做 `task-20261007-superpowers-6x-rebaseline`，先研究盤點、不急著開 change；Completion Gate 等 6.x 對齊後再推進。公開 roadmap 未反映下一代改造，方向收斂後再整理。
- **工作地圖修正**：`task-20261007-formal-design-execution-record` 被 09:29 收工的序 5 自動規則升成 NEXT，與 10/07 B-6 裁定（暫不實作、依賴 Gate 落地）矛盾 → 使用者選 A′：改回 TODO 並改掛到 `task-20260826-superpowers-bridge-next-gen`（Gate 那條不再只有一個子項，不會再被自動升 NEXT）。依賴關係仍由 Gate 那條的 description 與 B-6 承載。
- **研究**：`docs/superpowers/research/2026-10-08-superpowers-6x-capability-gap.md`（研究 agent 產出，索引加一列）。範圍 S4/S5/S12/S14＋S6/S7/S17/S18，確認 S11/S13；新發現 S19（SDD 收尾自叫 finishing）。Codex 文件審 4 輪（同一 thread `01a11a86-6be1-7241-9b65-ae53ef2516d1`，已回覆 3 次）：r1 ⛔（S12 建議改法與上游矛盾）→ 修 → ✅；加 §4 裁定後 r3 ⛔（我寫的「正式設計與 schema 都沒有隔離要求」不成立）→ 修 → r4 ✅。
- **D1–D5 裁定**（記在研究文件 §4）：D1 B（接受上游三路徑，附核可停頓點驗證條件）；D2 只改散文、不升 major；D3 有條件允許降級（三情形＋原則，依 cost-aware policy）；D4 以 `v6.4.1` 為驗證目標與宣告版本；D5 由 B 改 A——本輪就補明「控制權交接」，含工作區保留到 verify 完成且證據持久化之後。
- **commit `6cbf82c`**（使用者授權）：研究文件、研究索引、工作地圖修正。
- **README 中英更正（未 commit）**：S17 安裝指令實際裝 6.4.1、S7 Workspace 改寫為 6.4.1 實際流程＋untracked change 目錄的事實、S12 Completion 三選項與清理條件、S5 Open drift 後加「更正」段（writing-plans 終點 v5.1.0 已有；HARD-GATE v5.1.0 已有、6.4.1 改寫為分段核可）、S14/S12 後續狀態段。查證：v5.1.0 原文以 `gh api …?ref=v5.1.0` 讀、6.3.0/6.4.1 讀本機。新 Codex thread `01a11ac8-0a2a-77d0-aa8a-3becdf3351e2` 一輪 ✅ Mergeable；compatibility 表未動、CI grep 仍讀 1.14.0/v5.1.0、中英 713 行章節對齊、installed copy 已同步。
- 工作地圖：`task-20261007-superpowers-6x-rebaseline` → DOING（本 session 實際推進：研究＋README 更正）。

### 三、未完事項 / 接力棒

- [#接力] README 中英更正若本次未 commit，下次先 commit（審查已過、`doc_review` 已記 pass）。
- [#接力] 下一個工作單位：opsx change「brainstorming 路徑對齊＋S19 交接」（沿用 `task-20260826-fix-brainstorming-drift`）：S4、S5、S6；S19 須在 proposal/tasks **明列為獨立的小範圍相容性修正**；D3 的 apply step 1 措辭可一起；交接契約 4 要點見研究文件 §4.1。使用者本次明示「暫不啟動」。
- [#接力] README 第 632 行（10/02 紀錄列）寫「`v6.4.1` added … a HARD-GATE」不準（HARD-GATE v5.1.0 已有、6.4.1 是改寫）；屬 S4，依「不改舊紀錄句」慣例，於 S4 change 以後續狀態段更正。
- [#接力] 非必修 🟡（README:604 中英）：「bounded 直接進入實作」可補「在對話中的設計核可之後」——記錄、未改。
- [#接力] 第三步驗證追加要求見研究文件 §4.2（D1 核可停頓、D5 控制權交接與工作區保留、D3 情形與紀錄）。
- [#接力] 空目錄 `.claude/worktrees/task-prefixed-plan-headings/` 仍待 session 結束後 `! rmdir`。
- [#接力] 本機 `main` 領先 origin（`181e7a7`、`6cbf82c`，加本收工 commit）；未授權 push。
- [#不重議] D1–D5 裁定；execution record 的 A′ 表示；6.x 先盤點後切 change。

### 四、洞見 / 反省

**【紀律接力】**

- **宣告「沒有」前沒窮舉（本 session 1 次，Codex 抓到）**：我以英文 `isolat|worktree` grep 正式設計得 0 筆，就對使用者與文件宣稱「正式設計與 schema 都沒有隔離要求」；正式設計是中文（「隔離」）、schema 本身就有「isolated workspace」。全域規則「0 命中要換結構不同的路徑交叉驗」沒做到；做法：搜中文文件時中英關鍵字都搜，且先查自己正要談的那個檔（schema）。
- **說過頭的句子**（沿用，本 session 2 次）：上句；以及我在建議裡說「execution record 是 Gate 的前提」——照工作地圖 NEXT 字面推論、沒回讀 B-6 原文（使用者抓到）。
- **附和裁定時驗事實前提**（沿用）：本 session 都有驗（18 項依賴數、S13 已處理、cost-aware 出處、archive 狀態），其中「archive 還沒完成」不成立已更正。

**【當日洞見】**

- **登記工具借 parent/child 表達依賴，會撞上收工的「唯一可升子項自動 NEXT」**：B-6 的替代表示在下一次收工就被翻回；改掛到有 DOING 子項的父項下解決。根因是登記工具不能記「在等哪一筆」，屬 workflow-harness 範疇。
- **上游歷史宣稱要對 tag 原文查**：研究引用的 `git show v5.1.0` 本機無法重現，改用 `gh api …?ref=v5.1.0` 讀 GitHub tag 才驗到，順帶發現 HARD-GATE 的版本說法錯。
- **子流程完成 ≠ 上層流程完成**：SDD 的 Finish 指示呼叫 finishing 並刪工作區，與 bridge 的 verify → retro → archive 交接點衝突；修法是寫明控制權交接，不是新增驗收機制。

【學習候選】

- **Case**：以英文關鍵字搜中文正式設計得 0 筆，宣稱「沒有隔離要求」，Codex 指出中文「隔離」與 schema 原文。
- **Candidate Pattern**：對中文（或混語）文件做否定性宣稱前，關鍵字至少中英各一組，並先搜「正在談的對象本身」。適用於宣告不存在；肯定性引用不適用。
- **Evidence**：本次 1 例；屬全域「宣告沒有前先窮舉」既有規則的又一實例，**Hypothesis**。
- **Minimum Sufficient Intervention**：不新增規則；併入既有紀律接力觀察。
- **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（737aa56、開工於 2026-10-08T09:40:28）——列 737aa56..HEAD（14:50 之後的部分如下）

- `6cbf82c`：`docs/superpowers/research/2026-10-08-superpowers-6x-capability-gap.md`（新）、`docs/superpowers/research/README.md`、`workflow-harness/work-map.jsonl`（execution record → TODO＋改掛）
- 本收工 commit：`workflow-harness/work-map.jsonl`（6.x rebaseline → DOING）、本交接檔；README 中英兩檔依使用者確認決定是否同 commit

### 六、下一步建議

1. 若 README 更正尚未 commit，先 commit；之後清空目錄（rmdir）。
2. 啟動 opsx change「brainstorming 路徑對齊＋S19 交接」（使用者授權後）。
3. 之後第三步：以 `v6.4.1` 跑完整相容性驗證（清單見研究文件 §3.2＋§4.2）。
