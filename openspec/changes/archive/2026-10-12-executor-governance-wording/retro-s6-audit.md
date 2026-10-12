> **保存說明（2026-10-12，實作者加註）**：本檔是 retrospective §5 引用的盤點表，原樣自 session scratchpad 複製進 change 目錄保存，內容未改。由盤點 agent 唯讀產出。
> 「遲到等價」判準（下方「判讀規則」第二點）已由使用者 2026-10-12 裁定：1.3、3.6 算「已做到（遲到）」。依此，計數為 DONE 10、NOT DONE 12；下方「計數」表保留盤點當時的嚴格判準數字。

# 封存 change 複盤 §6「Promote candidates」落地稽核

- 稽核日：2026-10-12；唯讀，沒有改任何 repo 檔案
- 範圍：`openspec/changes/archive/*/retrospective.md` 共 7 份，§6 共 **35 條**（3+6+7+5+6+3+5）。另有 `2026-08-31-claude-md-phase-boundary` 這個封存 change，它沒有 retrospective.md，所以不在範圍內
- 勾選狀態：35 條中只有 identity ①② 兩條是 `[x]`，其餘 33 條都是 `[ ]`。**勾選框不能當作落地證據**：10/06 的 handoff:205 記載使用者的決定是「歸檔的複盤不改，以 handoff 當處理紀錄」，所以已處理的條目也維持 `[ ]`（例如 2.6、6.3）

## 判讀規則

- **DONE**：在指定的目的地或等價位置找到內容，附 path:line 與日期。日期用 `git log -S` 定，記憶檔不進 git，改用 frontmatter 的 `modified` 欄。
- **「遲到等價」歸為 NOT DONE**（這是我自己定的判準，請你確認）：如果等價內容是後來**同一問題再次發生**時，從別的路徑寫進去的，而且沒有引用本條候選，我就把本條歸為 NOT DONE，並標註「遲到等價」。理由是本條候選本身沒有被執行。如果改用字面判準（只要有等價內容就算 DONE），1.3 與 3.6 會改歸 DONE。
- **One-off 條目**：只有複盤本文（或使用者裁定紀錄）明寫這是刻意決定時，才歸為 DECIDED-NO，並引用原文。

## 搜尋範圍（每條都跑過）

專案 `CLAUDE.md`、`.claude/CLAUDE.md`、`.claude/rules/*.md`、全域 `~/.claude/CLAUDE.md`、`superpowers-bridge/schema.yaml`、`templates/**`、`README*.md`、根目錄 README（en／zh-TW）、`openspec/specs/**`，以及 `~/.claude/projects/*/memory/**/*.md` 全部 20 個記憶目錄（含 `_to-delete/` 子目錄）。另外搜了 `backlog.md`、`驗收節點.md`、`workflow-harness/work-map.jsonl`、`文檔/handoff/*.md` 全部 29 份，以及 `openspec/changes/**`（含進行中的 `executor-governance-wording`）。

有針對性地補讀了這些檔案：`docs/superpowers/research/*`、`docs/superpowers/retrospectives/*`、fixtures README、`~/.claude/skills/review-fix-propagation/**`。搜尋方式是 Python 正規表示式（`PYTHONUTF8=1`），中英關鍵字並用。

## 總表

| # | 來源（封存日）| 條目 | 嚴重度 | 指定目的地 | 勾選 | 分類 | 證據 |
|---|---|---|---|---|---|---|---|
| 1.1 | fix-tdd-transitive-claim (08-31) | 修絕對句時寫出的替代句要再過一次例外檢查 | 🟡 | One-off | [ ] | **DECIDED-NO** | 複盤原文寫「全域 CLAUDE.md『證據先於斷言』已有此條；……不新增規則，樣本記在 handoff」。這條規則在本條之前就存在：`~/.claude/CLAUDE.md:23`，自述「N=7，2026-08-15 自 backlog 升 always-on」。樣本確實記在 handoff 0831:63（第 10、11 例）。 |
| 1.2 | 同上 | plan 不要把「會被審查迭代的交付句」逐字寫死，改成引用 spec | 📌 | One-off（先觀察；再發生就升成 plan.instruction 的一句話） | [ ] | **DECIDED-NO** | 複盤原文寫「先觀察；若下個 change 再發生 plan 追平成本，升為 schema plan.instruction 的一句話」，handoff 0831:76 也同樣寫「先觀察」。⚠️ **觸發條件看起來已成立，但沒有人升級**：research `2026-09-10-contract-drift-archaeology.md:39`（H5）把本條和「global constraints 逐字照抄」並列；retro-skill-inventory 的 §6 第 2 條（10-02）再記一次「人工逐字複製 contract 會製造同步義務」。schema `plan` instruction 裡沒有找到「引用 spec、不內嵌全文」這類句子。 |
| 1.3 | 同上 | smart-commit alloc 的 /tmp 訊息檔在 Windows 要先 cygpath 再 Write | 📌 | 本專案 memory（feedback） | [ ] | **NOT DONE（遲到等價）** | 08-31 當時沒有寫進 memory，只記在 handoff 0831:68。**10-07 同一問題再次發生**後，才寫了 `memory/feedback_smart_commit_tmpdir_windows.md`（modified 2026-10-07T01:54Z）。修法換成 `TMPDIR=<scratchpad>`，而且檔內自稱「2026-10-07 第一次撞到（1 例）」，沒有引用 08-31 那一例。 |
| 2.1 | loosen-plan (09-04) | 一個什麼都沒讀到的讀取者回報 0，和一個全部讀完的讀取者回報 0，輸出一模一樣（「預期 0」的檢查要附正向對照） | 🔴 | CLAUDE.md（強化「0 命中 ≠ 不存在」） | [ ] | **NOT DONE** | `~/.claude/CLAUDE.md:24` 的「0 命中要換路徑交叉驗」是 08-12 就有的條文，裡面沒有「正向對照」或「回報讀不到哪些檔」。全部位置搜「positive control／正向對照／read nothing」都是 0 筆，命中只出現在 handoff 0903:108 這筆紀錄。相關的是 `memory/feedback_claim_first_discriminating_oracle.md`（10-01，來源是 identity 複盤），它涵蓋「oracle 分辨不出兩種行為」，但不是「預期 0 的檢查要附正向對照」這個形狀，也沒有引用本條。**再次發生**：handoff 0914:356（`grep -c $'\r'` 回傳行數，被當成證據，非零命中也不可信）；使用者 09-14 裁定這次不開 backlog（handoff 0914:350）。 |
| 2.2 | 同上 | 兩個語系說法一致，不代表內容正確（翻譯要對照權威來源，不要對照另一個語系） | 🔴 | CLAUDE.md | [ ] | **NOT DONE** | 專案與全域 CLAUDE.md、rules、memory、backlog、work-map 都搜不到（關鍵字：counterpart locale／Bilingual agreement／雙語一致／權威來源）。專案 CLAUDE.md 的「雙語策略」節只講翻譯同步，沒有這條。handoff 也沒有任何處置紀錄。 |
| 2.3 | 同上 | 重用一個 skill，不會一併繼承它的權限假設（SDD 依賴 implementer commit，本 repo 禁止 agent commit） | 🟡 | schema／bridge README 整合段加一行 | [ ] | **NOT DONE** | `schema.yaml`、bridge README（en／zh）搜 implementer／subagent 加 commit、permission 的組合都是 0 筆。事實基礎只寫在 `docs/superpowers/retrospectives/2026-09-03-loosen-plan-execution.md` §7，§9:196 標「Anchor #4 正式檢討……未排期」，work-map 沒有登記。**再次發生**：task-prefixed-plan-headings 複盤 :11、:55（R1：「子代理不 commit；審查用工作區 diff……SDD 原本的實作者自己 commit 會違反」），10-08 又臨場處理了一次。 |
| 2.4 | 同上 | 逐條目的欄位，看不見那個條目本身看不到的耦合邊（Interfaces 欄位） | 📌 | one-off（當作 D3 觸發觀察，N=1，先不動） | [ ] | **DECIDED-NO** | 複盤原文寫「hold as a D3 trigger observation at N=1; do not act yet」。⚠️ **觸發條件已發生**：handoff 0907:210 記錄 fix-v2 plan 的 doc gate 第一輪 🔴「plan 介面耦合漏 1.4 與 3.2→5.1」（N=2）。但沒有找到 graph-level 檢查或改欄位範圍的後續動作；schema 的 Interfaces 雙向提問（`schema.yaml:493-494`）是 09-02 `932a044` 就有的。 |
| 2.5 | 同上 | 先宣告要作廢第一次量測，再看替代結果 | 🟡 | memory（feedback） | [ ] | **NOT DONE** | 全部記憶目錄搜「discard／作廢／丟棄」都沒有對應條目，命中的只有無關內容。本條只在 loosen-plan 當次照做過（handoff 0903:82「裁定寫在 run 2 存在之前」）。之後沒有找到同型再次發生。 |
| 2.6 | 同上 | 誠實通過的檢查，在受檢對象改變後不會自動失效（新鮮度） | 🔴 | schema | [ ] | **DONE** | `superpowers-bridge/schema.yaml:1489-1515`「FRESHNESS of a recorded check result」，`templates/verify.md:207`；commit `02a3385`（2026-09-04 09:49），晚於複盤 `84df208`（09-03）。依據是使用者 09-04 的裁定（handoff 0904:14）。機械化版本（digest）刻意不做。 |
| 3.1 | fix-v2-blocking-defects (09-14) | 一條規則在某個表面改了，要雙向掃過所有陳述同族規則的表面（規則 × 表面矩陣） | 🔴 | memory（feedback） | [ ] | **DECIDED-NO** | 處理路徑是 research `2026-09-10-contract-drift-archaeology.md`（H7 :41、:196「矩陣有效無載體」、:216 否定「把矩陣做成永久 artifact」），接著是使用者裁定，記在 `memory/feedback_review_observation_protocol.md:23,25`：09-11「A2（一規則三讀者＝矩陣）**暫緩**」；09-14「不新增 A1 Skill、不新增 Gate、不維持平行規則」，只把較窄的「搜舊說法」回灌到 `~/.claude/skills/review-fix-propagation/SKILL.md:20`。「雙向、空白格也要標」這個形狀沒有寫進任何記憶。 |
| 3.2 | 同上 | fallback 審查結論足以讓工作繼續，但不足以宣告完成；界線在不可逆動作 | 🔴 | memory（feedback） | [ ] | **NOT DONE** | 所有記憶目錄搜 fallback 搭配 archive／不可逆／結案都是 0 筆。全域 `~/.claude/CLAUDE.md:31` 有較弱的「降級有條件、非免票（2026-09-01）：高風險項不得就此結案、外部審恢復後必須補審」，這條早於本條（09-08），也不是以不可逆動作劃界。**行為上的反例**：task-prefixed-plan-headings（schema major 4 發布）的文件審查 4 批全是 fallback（Codex 額度用完）就 archive、push 並打 `v4.0.0` tag（handoff 1008:180-183）。 |
| 3.3 | 同上 | 相信 agent 最後一則訊息之前，先看工作樹（兩個方向都要） | 🔴 | memory（feedback） | [ ] | **NOT DONE** | 所有記憶目錄搜 idle 通知／inbox／working tree before／工作樹都是 0 筆（只命中無關的 networkidle、tui-idle）。之後沒有用關鍵字找到同型再次發生（沒有逐篇讀）。 |
| 3.4 | 同上 | 裁定某個前提之前先驗證前提；空集合上的全稱檢查是空成立，不是真的檢查 | 🟡 | memory（feedback） | [ ] | **NOT DONE** | 記憶目錄搜 vacuous／空集合／空跑：只命中無關的 workflow-harness 刪碼條目。schema 內 `:621`、`:938` 的 vacuous 字樣是產品條文修正，不是經驗記錄。之後沒有找到同型再次發生。 |
| 3.5 | 同上 | 凡是用 diff「大小」做判斷，一律加 `--ignore-cr-at-eol` | 🟡 | 專案 CLAUDE.md | [ ] | **NOT DONE** | 專案 CLAUDE.md、`.claude/rules`、bridge 都搜不到 `ignore-cr-at-eol`。部分緩解：`.gitattributes` 已把 `superpowers-bridge/**` 釘成 LF（`4626e96`，09-14），所以 bridge 檔不再膨脹；但 `core.autocrlf=true`，根目錄 `CLAUDE.md`、`openspec/changes/**` 的工作區副本仍是 CRLF（`git ls-files --eol` 實測 CLAUDE.md `w/crlf`）。之後的做法不一致：identity §0 有加 flag，task-prefixed §0 用不帶 flag 的工作區 `git diff --shortstat 737aa56`（是否膨脹【未驗】）。 |
| 3.6 | 同上 | 答案表要記「分得出對錯的結果」，不是記意圖 | 🟡 | fixtures README 慣例 | [ ] | **NOT DONE（遲到等價）** | fixtures README 沒有寫成慣例（搜 intent／answer key／discrimin／分辨都是 0 筆）。**同型再次發生**：identity change 三例（grader 對重複案例只取最後一段等，見其複盤 §6①）。之後由 identity 複盤寫入 `memory/feedback_claim_first_discriminating_oracle.md`（10-01），內容等價，但沒有引用本條。fixtures README:62（10-08）已經照這個原則拆分 f20–f22。 |
| 3.7 | 同上 | `cp -R` 不先 `rm -rf`，只有在來源沒刪任何檔時才等價 | 📌 | One-off | [ ] | **DECIDED-NO** | 複盤原文寫「it does not generalise into a rule, it generalises into a *check*」，並註明「recorded; already stated in tasks.md task 5.1's control record」。⚠️ **同型再次發生**：task-prefixed 複盤 §6 第 3 條（:108）建議「`rm -rf` 會被擋，用覆蓋複製」，但沒有附上「目的地有、來源沒有的檔案要先列出」這個檢查。 |
| 4.1 | requirement-scenario-identity (10-01) | ① oracle discrimination | 🟡 | memory（feedback） | [x] | **DONE** | `~/.claude/projects/C--Users-user-orca-openspec-schemas/memory/feedback_claim_first_discriminating_oracle.md`（modified 2026-10-01T08:13Z），MEMORY.md:12 有索引。依據是使用者 10-01 的裁定（handoff 1001:145）。 |
| 4.2 | 同上 | ② proxy mismatch | 🟡 | memory（feedback，與①同檔） | [x] | **DONE** | 同上，第 2 點。 |
| 4.3 | 同上 | ③ retrospective 模板的 skill 表仍列 writing-plans | 🟡 | 另開修正工作 | [ ] | **DONE** | work-map `task-20261001-retro-template-writing-plans` 已 DONE（10-02）；`superpowers-bridge/templates/retrospective.md:69`「(例如 `superpowers:writing-plans`)不屬於這兩類,不列入本表」，commit `2b1019f`（2026-10-02）。 |
| 4.4 | 同上 | ④ proposal 的 Out of Scope／Assurance Boundary 兩段，不改模板 | 📌 | One-off（帶到下一個 change 重評） | [ ] | **DECIDED-NO** | 複盤前言寫「④ 繼續觀察」（使用者 10-01 裁定，handoff 1001:145）。重評的觸發條件是「下一個用到這兩段的 change」，但這個條件至今沒有發生：所有封存與進行中 change 的 proposal 只有 identity 本身有這兩段（grep 標題實測）。 |
| 4.5 | 同上 | ⑤ worktree 摩擦 9 例併入既有工作項 | 📌 | One-off（併入既有工作項） | [ ] | **REGISTERED** | `task-20260904-worktree-handoff-lifecycle`，狀態 TODO（status_changed 09-04）。注意：該工作項的 name／description 沒有提到這 9 例，兩者的連結只存在於複盤與 handoff 1001:145。 |
| 5.1 | retro-skill-inventory (10-02) | 小型 change 的 plan 約一半在重述 tasks | 🟡 | One-off | [ ] | **DECIDED-NO** | 複盤原文寫「使用者 2026-10-02 裁定：**不能據此推出應取消 plan**」，處置欄寫「記錄即可，不據此改 plan 規則」。 |
| 5.2 | 同上 | 人工逐字複製 contract 會製造同步義務 | 🟡 | 作為既有決定的證據（不新增規則） | [ ] | **DECIDED-NO** | 複盤原文寫「使用者 2026-10-02 裁定：記成既有決定的新實例，不另升格」。底層決定見正式設計 `2026-09-01-bridge-guarantee-formal-design.md:357` 第 2 列「取消人工逐字副本」，該決定**尚未落地，work-map 也沒有對應工作項**（搜「逐字副本」只命中正式設計與 research）。 |
| 5.3 | 同上 | verify PRECHECK「commit 數 > 0」是對不準的代理指標 | 🟡 | Verification Strategy 研究 | [ ] | **DONE**（目的地是研究，研究已收錄） | `docs/superpowers/research/2026-10-02-verification-strategy-case-crosswalk.md:60`（RS-6）、:86（P3）；`2026-10-02-verification-evidence-inventory.md:140`（F-RS7）；`2026-10-05-verification-c1-enforcement-surface.md:46`。注意：schema 的 PRECHECK 本身沒有改（`schema.yaml:509` 仍是數 commit），研究工作項 `task-20260929-verification-strategy-research` 仍在 DOING。 |
| 5.4 | 同上 | SDD `task-brief` 認不得 Plan Contract 標題 | 🟡 | 後續工作 | [ ] | **DONE** | `task-20261002-task-brief-heading-compat` 已 DONE（10-08）；change `2026-10-08-task-prefixed-plan-headings` 已封存，schema major 4、tag `v4.0.0`（handoff 1008:183）。 |
| 5.5 | 同上 | 完成宣告引用的證據，壽命比宣告本身短 | 🟡 | 下一代 bridge 討論素材（VS 研究的 evidence lifecycle 子題） | [ ] | **DONE**（作為研究素材） | crosswalk `:61`（RS-7）、`:89`（P6）、`:185`，commit `57ea8eb`（2026-10-02）。**之後再次發生**：task-prefixed 複盤 §6 第 1 條「盲測結果只記在 git-excluded 的 SDD ledger」（handoff 1008:214）。 |
| 5.6 | 同上 | controller 誤下 `git add -N` | 📌 | One-off | [ ] | **DECIDED-NO** | 複盤原文寫「已當場撤銷並揭露；使用者裁定不新增流程規則」。 |
| 6.1 | fix-executing-plans-rationale (10-06) | 純措辭更正型 change 的執行路徑要明文化（第二次跳過 SDD） | 🟡 | schema apply instruction，併入 governance-rewrite | [ ] | **REGISTERED** | 10-06 裁定「(a) 併入 `task-20260901-claudemd-governance-rewrite`」（handoff 1006:201），該工作項目前 DOING。部分已落地：`2551ea0`（10-12，schema major 5）的 `schema.yaml:1851-1860` 把三種情境分開，「有 SDD 但經裁定刻意略過」寫成例外偏離。但「沒有 SDD 時以什麼審查與紀錄滿足獨立審查」使用者選擇延後，另登記為 `task-20261012-non-sdd-execution-support`（TODO；handoff 1012:21,32）。這次的 change 本身也沒跑 SDD，算是具名例外（第三例）。 |
| 6.2 | 同上 | 修「上游改版讓說法失效」時，順便搜處理上游改版的後設說法 | 🟡 | memory（Hypothesis） | [ ] | **DECIDED-NO** | handoff 1006:202「(b) 修上游改版失效時一併搜維護說明 → **不存記憶**，留在複盤當案例（1 例 Hypothesis；本益比低、現有文件審已接得住）」；1006:215、1007:24 也重申這點，標記為 `[#不重議]`。 |
| 6.3 | 同上 | 引用上游原文當查證依據時，連結要指向固定版本標籤 | 📌 | bridge README 撰寫慣例或 CLAUDE.md 雙語策略 | [ ] | **DONE** | 專案 `CLAUDE.md:66`「**引用上游原文當查證依據**(2026-10-06 起)」，commit `56381dc`（2026-10-06），文末引用本條候選。 |
| 7.1 | task-prefixed-plan-headings (10-08) | plan 寫「recorded」的驗收條件，要寫明記在哪個進版控的檔 | 🟡 | schema（plan instruction 的 Acceptance 說明） | [ ] | **NOT DONE** | `schema.yaml` 與 `templates/plan.md` 搜 tracked／version control／版控都沒有這類要求（唯一命中 `:193` 是 checkbox 追蹤）。**同型寫法再次出現**：進行中 change `executor-governance-wording/plan.md`（工作區版本）第 117、156、162、168 行用「recorded …」，沒寫落在哪個檔。這一次沒有跑 SDD，所以沒有造成證據遺失。 |
| 7.2 | 同上 | 狀態宣告寫進 tracked 檔時，同時登記誰在什麼事件後負責更新它 | 🟡 | memory（feedback） | [ ] | **NOT DONE** | 所有記憶目錄搜狀態宣告／尚未盲測／目前尚未／負責更新都是 0 筆。之後沒有找到同型再次發生。進行中 change 的 verify.md:350、:681 自帶 13.F 新鮮度說明，但那是 schema 的要求，不是本條。 |
| 7.3 | 同上 | 改了 `superpowers-bridge/` 之後、跑任何 openspec 指令之前，重新同步已安裝副本 | 🟡 | 專案 CLAUDE.md「自己吃自己的 schema」節 | [ ] | **NOT DONE** | `CLAUDE.md:157-159` 仍是 08-26（`9e9ea40`）的原文：只寫「改完 schema 必須重新同步」並附 `rm -rf && cp -R`。沒有擴大到 README 等任何 bridge 檔，沒有寫「verify／archive 前」，也沒有覆蓋複製加 `diff -r` 的替代做法。實務上有照做：進行中 change 的 verify.md:58 `diff -rq` 無差異；本次實測 `diff -rq` 也一致。 |
| 7.4 | 同上 | 證據綁定條文 sha 時，後期修措辭前先算重跑成本 | 📌 | One-off | [ ] | **DECIDED-NO** | 複盤原文寫「**One-off**（本次以 R15 處理）……僅當一個 change 的證據綁定被測條文的 hash 時適用」。R15 屬於 R1–R16 裁定，handoff 1008:178 記載「已端給使用者、無推翻」。 |
| 7.5 | 同上 | 升 schema major 的連動清單要包含根目錄 README 的 bridges 狀態欄 | 📌 | 專案 CLAUDE.md「跨檔耦合」表 | [ ] | **NOT DONE** | `CLAUDE.md:189`（artifact 增刪列）仍只列 bridge README、templates、roadmap；`2551ea0` 改了耦合表的版本號，但沒有加這一欄。實務上下一次升 major（v5，`executor-governance-wording` design.md:148、tasks.md 4.3）有改到，`2551ea0` 有改根 README，所以**本條之後沒有再次發生**。本條之前已發生兩次：v3 tasks r1 被審查抓到（handoff 0930:74），v4 D8 漏列（task-prefixed 複盤 :45）。 |

## 計數

| 分類 | 數量 | 條目 |
|---|---|---|
| DONE | 8 | 2.6、4.1、4.2、4.3、5.3、5.4、5.5、6.3 |
| REGISTERED | 2 | 4.5、6.1 |
| DECIDED-NO | 11 | 1.1、1.2、2.4、3.1、3.7、4.4、5.1、5.2、5.6、6.2、7.4 |
| OBSOLETE | 0 | — |
| NOT DONE | 14 | 1.3*、2.1、2.2、2.3、2.5、3.2、3.3、3.4、3.5、3.6*、7.1、7.2、7.3、7.5 |
| UNCERTAIN | 0 | — |

\* 標「遲到等價」。若改用字面判準，DONE 會變成 10、NOT DONE 變成 12。

## 觀察（不屬於單一條目）

- **NOT DONE 集中在兩份複盤**：loosen-plan 的 6 條中有 4 條、fix-v2 的 7 條中有 5 條，目的地都是 memory 或 CLAUDE.md，而這兩份複盤**都沒有找到使用者逐條裁定的紀錄**。identity（10-01）、retro-skill-inventory（10-02）、fix-executing-plans（10-06）這三份，都有使用者逐條裁定（分別見 handoff 1001:145、該份複盤 §6 本文、handoff 1006:200），落地率也明顯變高。task-prefixed（10-08）是例外：5 條裡有 4 條沒處理，handoff 1008 也沒有逐條裁定紀錄。
- **「先觀察」條目的觸發條件已成立，但沒人回頭看**：1.2（10-02 再發生）、2.4（09-07 再發生）、3.7（10-08 再發生）。這類觀察條目沒有任何承接點，再次發生時沒有東西會提醒。
- **勾選框長期是 `[ ]`**：因為 10-06 的決定是不改已歸檔的複盤，所以要看處理狀態只能去翻 handoff。

## 沒能搜尋的地方

- 全域 `~/.claude/CLAUDE.md` 不在任何 git repo 裡，無法用 `git log -S` 定出某段文字何時出現，只能靠條文自帶的日期註記。
- 已刪除的 SDD 工作區與 worktree 內的 ledger（例如 loosen-plan、identity、task-prefixed 的 `.superpowers/sdd/`）。殘留目錄 `.claude/worktrees/task-prefixed-plan-headings/` 實測 0 個檔案。
- Claude Code／Orca 的對話紀錄、Codex 對話。
- 其他 repo 的 handoff 與 `docs`（例如 workflow-harness repo 本體）。這次只搜了它們在 `~/.claude/projects/*/memory` 的記憶。
- `~/.claude/skills/` 底下，只讀了 `review-fix-propagation`，其他 skill 沒有逐一搜。
- GitHub issues／PR 留言。
- `docs/superpowers/**` 沒有全文逐條搜，只做了針對性 grep（research、retrospectives、fixtures README）。
- 「再次發生」的判斷是用關鍵字搜 09-15 之後的 handoff、各封存 change 的 md，以及進行中 change 的 md，**沒有逐篇通讀**。所以「之後沒有找到同型再次發生」的意思是「沒搜到」，不代表沒發生。
