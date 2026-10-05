# Verification Strategy 第二步：一般程式對照案例 `fix-deferred-verification-resurface`（2026-10-05）

> **定位**：分析參考，不是規範、不是研究結論。Verification Strategy 第二步的**第一個一般程式對照案例**（起點備忘 `./2026-10-02-verification-strategy-step2-starting-memo.md` §7 的「對照組」題）。受測案例在另一個 repo：workflow-harness 的 archived change `2026-09-30-fix-deferred-verification-resurface`。
>
> **目的**（使用者 2026-10-05 原話）：這一步不是直接研究「驗證工具本身要不要被驗」，而是先確認目前長出來的 Verification Strategy，有沒有被前面那些規則文字／agent-mediated 案例帶偏。
>
> **做法**：沿用內部證據盤點表 `./2026-10-02-verification-evidence-inventory.md`（下稱「盤點表」）的 §0／層表／finding 表欄位與記錄規則，另加逐 claim 的主鏈表（Claim → Oracle／Method → RED/GREEN → Review → Completion）。第一輪由唯讀 subagent 盤點、主 session 抽查關鍵出處（起點備忘第 60 行、`290850b`）。
>
> **三種內容分開寫**：
> - **來源事實**：無標記、附出處（§0–§2、§4 的表格）。
> - **從案例得到的觀察**：§3 的「判定」欄（順／改／不適用／新）與說明。「改」欄裡「要分成…」「要能標…」是**單案例下的提議**，依 §6 裁定**不據此修改盤點表**。
> - **單案例推論／假說**：一律標【推論】，集中在 §5。只有一個對照案例，**不得升格為一般規則**。
>
> 【未查證】＝沒查到。
>
> **路徑縮寫**：`CH/`＝workflow-harness 的 `openspec/changes/archive/2026-09-30-fix-deferred-verification-resurface/`（進版控）。以下三者都在 **repo 外、沒有保存保證**（見 §0）：`TR`＝該 change 主 session 的 Claude Code 逐字紀錄 `~/.claude/projects/D--workflow-harness/581c70bd-4aa6-4f59-a220-dec9fbfc4c63.jsonl`（數字＝該檔第幾行）；`SP/`＝該 session 的 scratchpad `%TEMP%/claude/D--workflow-harness/581c70bd-4aa6-4f59-a220-dec9fbfc4c63/scratchpad/`；`RO1`＝Codex 對話 `~/.codex/sessions/2026/09/30/rollout-2026-09-30T09-45-13-01a0effc-….jsonl`（R1–R3 同一 thread）、`RO2`＝同目錄 `rollout-2026-09-30T15-27-18-01a0f135-….jsonl`（整分支補審）。「帳本」＝`CH/review-findings.md`。

---

**案例一句話**：驗收節點用「result 欄是不是 `—`」代表「還沒結案」，但規格自己的延期寫法會把 result 填上字，於是延期的節點到新日期不會被提醒、週檢還會把相關 backlog 行當成可刪（9/29 已真的誤刪 3 條，`290850b`）。修法是在 Python 解析器加一個共用判斷 `is_open`，兩個下游改用它，加上出貨文字、四份規格與資料修復（`CH/proposal.md:3-24`、`CH/design.md:3-13`）。受測對象是**一般 Python 程式＋測試**，但同一個 change 也夾帶「agent 讀了文字要照做」的部分。

---

## §0 來源完整性

| 來源 | 讀了什麼 | 還在嗎 | 缺什麼 |
|---|---|---|---|
| change 文件（進版控） | `CH/` 全部 15 個版控檔全文（13 份 artifact／中繼檔＋`evidence/` 兩檔） | 在 repo | `review-findings.md` 是主 session **轉述**的帳本，不是原文 |
| commit 紀錄 | `c0bf6a9`…`5655eb4` 共 16 個 commit 的訊息與 stat | 在 repo | — |
| handoff | `文檔/handoff/session-handoff-20260930.md` 16:22、18:16 區塊全文 | 在 repo | — |
| 變異測試樣本帳 | `文檔/變異稽核/119-樣本帳.md:35`（樣本＃9） | 在 repo | 每隻突變體被**哪條測試**殺死沒有記錄（runner JSON 只列活口，`SP/mut-vp*.json` 鍵名清單） |
| **Codex 原始對話** | `RO1`（R1–R3，55 次 tool call）、`RO2`（補審，23 次） | **在 repo 外仍存在** | 無保存保證（不在版控）；`SP/r1.json`、`r1b.json`、`r2.json`、`r3.json`、`cb.json` 存在但**沒讀** |
| **Codex 派工 prompt** | `SP/codex-r1-prompt.md`、`SP/codex-branch-review.md` 全文 | repo 外仍存在 | R2、R3 的 prompt 只在 `RO1` 的 user 訊息裡（已讀） |
| **Fable 備援審查原文** | `…/581c70bd-…/subagents/agent-a349d5ac….jsonl`（R4，51 次 tool use）、`agent-a847417b….jsonl`（程式碼審，84 次） | repo 外仍存在 | 程式碼審第一輪的原文我只讀了該檔**最後一則**（第二輪）；第一輪內容依帳本 `CH/review-findings.md:64` |
| **RED／GREEN 原始輸出** | `TR` 中所有 pytest／反向對照／變異 runner 呼叫（我用腳本抽出結果行） | repo 外仍存在 | Task 1 的 RED 只留「17 failed」與作者一句「原因是屬性不存在」（`TR` 1725、1730），失敗型別原文沒抽到 |
| 反向對照工具與變異輸出 | `SP/mutants.py`、`SP/mut-vp{,2,3}.json` 摘要、`mut-vp.err` | repo 外仍存在 | — |
| coverage gap 審查 | workflow-harness `CLAUDE.md:98` 規定 archive 前要跑 | — | **change 內沒有任何紀錄**（`grep coverage`／`test-review` 0 命中相關段）；有沒有跑【未查證】 |
| dogfood（agent 行為） | `CH/verify.md:73` 指定「最近一次機會＝2026-10-15」 | — | **尚未發生**（今天 2026-10-05） |

**和盤點表 §0 的差別**：盤點表六個來源都缺原始報告；這個案例的原始報告幾乎都還在——但**全部在 repo 外**（Codex session 目錄、Claude 逐字紀錄、scratchpad），只是還沒被清掉。進 repo 的只有轉述。

---

## §1 主鏈拆解（Claim → Oracle／Method → RED/GREEN → Review → Completion）

「RED」欄分兩種：**實作前 RED**（新測試先跑、確認會失敗）與**反向對照**（實作完成後故意裝回壞實作，看測試會不會轉紅；workflow-harness 規則 `CLAUDE.md:100` 叫「G13 ③ 反向對照通例」）。

| # | Claim（出處） | Oracle／方法 | RED／GREEN 證據 | 碰過它的審查 | 怎麼判完成 |
|---|---|---|---|---|---|
| C1 | **共用「未結案」定義**：`—` 一律 open；或未勾選且 result 欄有合法 `延期 → 日期`（只讀 result、反引號內不算、日期後不接數字、取最後一個、`->` 等價）（`CH/specs/observation-checkpoint/spec.md:3-74`，11 個 scenario） | 單元測試 `TestOpenStatus` 20 條（diff `f6816b8..ad71178`） | 實作前 RED：17 failed，原因是 `is_open` 屬性不存在（`TR` 1725、1730）——**例外型失敗，不是行為型**；GREEN 71 passed（`TR` 1753）。反向對照 6 個壞實作 → 8 條測試轉紅、全為 AssertionError（`TR` 1780、1811）。變異 runner 24 隻：殺 22→補測後 23，剩 1 隻判等價（`SP/mut-vp.json`、`mut-vp2.json`；樣本帳＃9）。箭頭相容：RED 1 failed（`TR` 2459），2 個壞實作轉紅（`TR` 2478） | Codex R1（F1 互斥、F4 regex 尾碼，**審的是 plan 裡還沒落地的程式碼**）、R2（R2-F9 反向對照會崩潰）、Fable R4、strict-reviewer 兩輪、Codex 補審 | verify §5 列出測試、反向對照與變異三數（`CH/verify.md:68-71`） |
| C2 | **到日提醒**：open 且「有效到期日」≤ 今天才浮現；延期者以最後延期日為準，排序與顯示同用此日（`spec.md:80`、`125-153`） | `TestFindDueNodes` 7 條＋`test_deferred_surface_shows_deferral_date` | RED 4 failed（`TR` 1878，此時 `is_open` 已存在，屬行為型）；反向對照 3 個壞實作各自轉紅（`TR` 1897）。真實資料：`find_due_nodes` 10/14→0、10/15→恰好 5 個（`ed1bae2` 訊息；`CH/verify.md:72`） | Codex R1 F6（原計畫的測試守不到顯示日期與排序 → 補兩條） | 同上＋真實資料回讀 |
| C3 | **提醒 ≠ 開窗**，提醒可能被 2048 位元組上限截斷（`spec.md:80` 末句、`86`） | 無程式 oracle；Fable R4 量了五筆提醒的位元組數（1187／935／809／2659／3057） | 無 RED／GREEN（文字宣稱） | Codex R1 F3、Fable R4-1 | 規格改寫；`verify.md:73` 列為「prose 但書」 |
| C4 | **寫回前置核對**：任何入口寫判定或開窗前，agent 必須回讀節點整行、前置未滿足只能延期（`spec.md:159`、`193-196`） | 無程式 oracle；出貨文字寫進 `commands/end-session.md`、`templates/驗收節點.md`（`aa99c87`） | 無 | Codex R2-F3、R3-F2（**兩輪半修**）、R4 確認 | **完成時仍開著**：`verify.md:73`「只能靠真實 session dogfood 驗（最近機會 10/15）」；Overall 判 PASS WITH WARNINGS（`verify.md:80`） |
| C5 | **延期寫法**：agent 延期時寫 `🟡 原因 \| 延期 → 日期`、不打勾（`spec.md:173`、`228-231`） | 措辭守門測試 `assertIn("延期中", skill)`（只驗 SKILL.md 有這幾個字） | 守門測試 RED 1 failed（`TR` 2007）→ GREEN | Codex R2-F2（半修）、R2-F10、Fable R4 P3 | 文字有沒有寫到＝有測；agent 會不會照寫＝沒驗（`design.md:57` 自承「無機器檢查」） |
| C6 | **graduated 清掃**：仍有 open 節點指向該載體就不可刪，含週檢計畫 `build_plan` 與刪除前重查（`spec.md:242-251`、`306-314`；`backlog-triage/spec.md:5-20`） | `TestGraduatedPredicate` 5 條（含 consumer 層 2 條） | RED 4 failed（`TR` 1923）；反向對照 1 個壞實作 → 4 條轉紅（`TR` 1964）。真實資料：`build_plan` 無清掃候選、還原的 3 條皆 `flying`（`0d027c5` 訊息） | Codex R3-F8（原本只測判斷函式、沒測 consumer） | verify §5 |
| C7 | 另兩份規格（backlog-management、packaging-candidate）只換判準句（`specs/*/spec.md`） | `openspec validate --strict`、`test_change_delta_integrity`（`TR` 864：107 passed）；Fable R4 用 difflib 逐字比對 live；archive 後 `rg` 查殘留（task 4.2b） | 無 RED | R2-F8（Codex 在第 2 輪才發現這兩份要改） | verify §3 |
| C8 | **資料修復**：5 個節點只在行尾附加延期段、原文不動（`tasks.md:35`） | 逐 byte 前後比對＋解析器回讀 | 前後對帳通過（strict-reviewer r2，Fable 程式碼審原文） | strict r2、Codex 補審 | commit `ed1bae2` |
| C9 | **資料還原**：9/29 誤刪的 3 條首行逐字插回原子彈行正上方（`tasks.md:40`） | 與 `290850b^` 逐字比對、`lint_backlog`、`find_graduated_items` | 通過（`0d027c5`；strict r2；Codex 補審 `RO2`） | Fable R4-2（原計畫「逐字放回」會放錯位置） | 同上 |
| C10 | **缺陷存在**：修前 10/15 的 5 個節點一個都不會被提醒（`proposal.md:3`） | 可重跑探針 `CH/evidence/延期節點現況探針.py` | 修前輸出「挑出 0 個」、合成延期節點不被挑出（`…-20260930.txt:8-9`）；Codex R1、R2 各自重跑一次（`RO1` F7、R2-F7） | Codex R1 F7（原本只有一句「實跑確認」、沒附可重跑證據） | brainstorm 引用 |
| C11 | **不退化**：全量測試 | `pytest hooks` | 3290→3293 passed／3 failed，3 條為基準 `f6816b8` 就失敗（`TR` 1650、2050；`verify.md:69`） | strict r2 重跑；Codex 補審**跑不起來**（見 §4 A8） | verify 註明 3 條基準既有 |
| C12 | **已知不涵蓋**：條件式節點在清掃中仍算已開獎，但workflow-harness 零活體（`design.md:55`） | 探針第 [3] 段 | 輸出：兩個真條件式節點都不引用 graduated 載體（`…txt:10-18`） | Codex R2-F11（原本沒有可重跑查法）→ **追查時發現 9/29 已有活體受害** | 寫入 design Risks |

---

## §2 層表與 finding 表（照盤點表格式）

### 2a. 層表

| 層 | claim／oracle | 執行者與強制機制 | 成本 proxy | 受測快照 | 抓到的 finding | 已知漏抓 |
|---|---|---|---|---|---|---|
| L1 Codex 文件審 R1–R3（同 thread） | 文件與 plan 的程式碼正確、一致／Codex 自讀 repo、會實跑 regex 與探針 | Codex `gpt-6-sol`、唯讀；使用者流程要求，無程式強制 | 3 輪、55 次 tool call（`RO1`） | R1 `c0bf6a9`；R2 `a9bc844`；R3 `bc04b07` | F1–F7、R2-F2／F3（半修）、R2-F8–F11、R3-F2、R3-F7、R3-F8 | R4-1（R3 審過 `bc04b07`，該句就在其中）；CB-F2（R1 prompt 要求全 repo rg，`SP/codex-r1-prompt.md`） |
| L2 Fable R4 文件審（備援） | 同上 | `tech-spec-reviewer`（Fable）；Codex 額度用盡、使用者裁定 | 1 輪、51 次 tool use | `3723757` | R4-1、R4-2、R4-P3×7 | CB-F2（R4 自述搜過 `unfilled` 等詞，未命中英文 `result filled`） |
| L3 作者 TDD 循環 | 每個 scenario 的行為／pytest 斷言 | 主 session；plan 寫死「先紅後綠」 | 每 Task 1 次 RED＋1 次 GREEN | worktree 各 Task | 無 finding（產出證據） | — |
| L4 反向對照（手工壞實作） | 測試分得出指定的錯／`SP/mutants.py` 逐一裝回壞實作 | 主 session；workflow-harness `CLAUDE.md:100`「沒做不算寫完」，無程式強制 | 10 個壞實作，每個 <1 秒 | 各 Task 完成後 | （本身沒抓到缺陷；10 個全轉紅） | 變異 id 12「迴圈提前結束」（樣本帳＃9） |
| L5 鑑別力閘 hook | 寫新測試時當場回答「什麼壞實作會讓它紅」 | `.claude/scripts/discernment_gate.py`，PreToolUse 程式 hook：每 session 第一次擋、之後提醒；自承「驗不到問句被認真回答」 | 「兩度要求答 Gate 問句」（`CH/retrospective.md:41`） | — | 無 | — |
| L6 變異測試 runner | 測試套的判別力／mutmut 2.5.1＋runner 自驗 V1–V7 | 主 session 決定何時跑；runner 自己檢查可信度（`SP/mut-vp.json` checks 全 pass） | 3 批 × 24 隻、單輪約 5.9 秒（`SP/mut-vp.err`） | `f6816b8` 起的改動行 | id 12 真缺口 | 測試檔／重排語句類（工具固定邊界，樣本帳＃8） |
| L7 全量測試＋結構驗證 | 不退化、delta 結構合法 | pytest、`openspec validate --strict`（程式）；何時跑由 agent 決定 | 全量約 210 秒（`TR` 1650、2050） | 各階段 | 無新失敗 | — |
| L8 真實資料回讀 | 修好後在workflow-harness 真資料上行為正確 | 主 session 腳本 | 數次 | `ed1bae2`、`0d027c5` | 無 | — |
| L9 strict-reviewer 程式碼審 r1／r2（備援） | 程式、測試、出貨文字、資料修復正確 | Fable；Codex 額度用盡 | 2 輪、84 次 tool use（同一 agent 續問） | r1 `f6816b8..`；r2 `d34967b^..db9b6e4` | r1：P2×1、P3×5；r2：P3×2 | CB-F1、CB-F2 |
| L10 Codex 整分支補審 | 同上，補備援的獨立性缺口 | `gpt-6.1-sol`；全域規則「備援完成者，外部恢復後須補審」 | 1 輪、23 次 tool call（`RO2`） | `f6816b8..` 完整分支 | CB-F1、CB-F2 | **全量 pytest 在唯讀沙箱跑不起來**，改跑 140 條（`RO2` 第 90、140 行）；帳本沒寫 |
| L11 擴散檢查（task 4.3） | 舊說法全部清掉／`rg` 中文舊字串 | 主 session，invoke `review-fix-propagation` skill | 未知 | 實作後 | （帳本未列） | CB-F2 英文註解（`tasks.md:31`） |
| L12 verify | 所有 task 完成、規格與實作對得上 | 主 session 自己做（`verify.md:5`） | 1 次 | `ad71178` | 無 | coverage gap 那一步沒有紀錄（見 §0） |
| L13 作者自述 | 「清掃 bug 目前沒有實際受害」 | 主 session，無強制 | — | — | （本身是錯誤，見 F-S1） | — |

### 2b. finding 表

「半修」：同一缺陷修正後、下一輪又被指出。依盤點表定義（「重新發現＝同一缺陷先前已被記錄（含被 defer）」），半修屬於「重新」；本表另標出來，是因為它和「曾 defer 又被抓到」的成因不同（見 §3a）。「如果沒抓到會怎樣」除標明「已發生」者外都是【推論】。

| # | 層 | finding | 原標 | 首次／重新 | 前一層已漏過 | 如果沒抓到會怎樣 | 出處 |
|---|---|---|---|---|---|---|---|
| F1 | L1 R1 | ADDED「`—` 一律 open」與到日偵測「已勾選不浮現」互斥 | P1 | 首次 | — | 實作只能違反其中一條規格 | `RO1` F1；帳本:9 |
| F2 | L1 R1 | 延期寫回格式與資料任務互斥 | P1 | 首次 | — | 資料修復寫出不合規格的延期段 | 帳本:10 |
| F3 | L1 R1 | 「10/15 恰好提醒五筆」混淆提醒與開窗 | P1 | 首次 | — | 10/15 對前置未滿足的節點開窗、寫錯判定 | 帳本:11 |
| F4 | L1 R1 | regex 會把 `2026-10-150` 截成合法日期（Codex 實跑 `re.findall`） | P2 | 首次 | — | 錯誤日期被當延期 | 帳本:12 |
| F5 | L1 R1 | 出貨文字另兩處舊判準 | P2 | 首次 | — | 週檢 skill 仍教 agent 用舊判準刪行 | 帳本:13 |
| F6 | L1 R1 | 測試守不到顯示日期與混合排序 | P2 | 首次 | — | 顯示錯日期而測試全綠（假 GREEN） | 帳本:14 |
| F7 | L1 R1 | 「實跑確認五筆全漏」無可重跑證據 | P2 | 首次 | — | 決策依據不可複查 | 帳本:15 |
| R2-F2／F3 | L1 R2 | F2、F3 只改了 spec、plan 與步驟清單沒改 | P1 | **半修**（F2、F3 的殘留） | — | 同 F2、F3 | 帳本:25-26、34 |
| R2-F8 | L1 R2 | 另兩份 live 規格仍用舊判準 | P1 | 首次 | **L1 R1**（prompt 要求全 repo rg） | archive 後留下互斥的 live 規格 | 帳本:27 |
| R2-F9 | L1 R2 | 計畫的反向對照 4 會讓 regex 崩潰，轉紅只證明崩潰 | P2 | 首次 | L1 R1（同段 plan） | **反向對照給出假的「抓得到」** | 帳本:28 |
| R2-F10 | L1 R2 | 收工摘要與模板總覽仍寫「打勾」 | P2 | 首次 | L1 R1 | 延期的節點被誤打勾 | 帳本:29 |
| R2-F11 | L1 R2 | 「條件式節點零活體」無可重跑查法 | P2 | 首次 | — | **追查時發現 9/29 已誤刪 3 條（已發生）** | 帳本:30 |
| R3-F2 | L1 R3 | 前置核對只蓋「答要」一個入口 | P1 | **半修**（第二次） | — | 從其他入口寫入判定 | 帳本:42 |
| R3-F7 | L1 R3 | 把 9/29 誤刪全歸因於本缺陷；計畫沒安排還原 | P1（回顧改標 📌 nit，`retrospective.md:21`） | 首次（**修正引入**：該句在 `bc04b07` 才出現） | — | 只修程式、3 條誤刪行永遠不回來 | 帳本:43；`git show bc04b07` |
| R3-F8 | L1 R3 | 清掃測試只測判斷函式、沒測 consumer | P2 | 首次 | L1 R1、R2 | consumer 層退化不會被測到 | 帳本:44 |
| R4-1 | L2 | 「提醒會顯示前置文字」不成立（2048 位元組截斷） | P2 | 首次（**修正引入**：`bc04b07`） | **L1 R3**（審過 `bc04b07`） | agent 依賴提醒內容、看不到前置 | 帳本:54；Fable 原文 |
| R4-2 | L2 | 「逐字放回」會放錯位置或重複 | P2 | 首次 | L1 R3（R3-F7 只要求「安排處置」） | 還原出錯位的 backlog | 帳本:55 |
| R4-P3 | L2 | 7 條：第三呼叫端未列、殘留註解、**措辭守門測試改後仍綠**等 | P3 ×7 | 首次 | — | — | 帳本:56 |
| S1 | L9 r1 | 資料補段未落地；樣本帳等價理由歸因錯；docstring 等 | P2×1、P3×5 | 首次 | — | 等價理由錯 → 後人以為拿掉 future import 就殺得掉 | 帳本:64 |
| M12 | L6 | 「先無效、後合法」的延期段被漏判（`continue`→`break` 活口） | 判「真缺口」 | 首次 | **L4**（6 個手工壞實作都沒想到） | 該形狀的節點靜默不提醒 | 樣本帳＃9 |
| S2 | L9 r2 | commit 訊息「diff 僅 +3 行」不精確；tasks 未勾 | P3 ×2 | 首次 | — | — | 帳本:66 |
| CB-F1 | L10 | SKILL.md 沒寫 `->` 相容 | P3 | 首次 | L9 r2（審過箭頭 commit） | 文件與實作說法不一 | `RO2`；帳本:74 |
| CB-F2 | L10 | `backlog_parser.py:53` 英文註解仍是舊判準 | P3 | 首次（舊碼殘留） | **L11、L1 R1–R3、L2、L9 兩輪** | 註解誤導後人 | `RO2`；帳本:75 |
| F-S1 | L13 | 作者先說「清掃 bug 沒有實際受害」——錯 | 回顧標 🔴 blocking | 作者自己製造的錯，不是偵測 | — | 使用者以為不用還原資料 | `retrospective.md:18` |

---

## §3 框架適配紀錄（本步核心）

判定：**順**＝原定義直接可用；**改**＝要改定義才放得進；**不適用**；**新**＝這案例出現框架沒有的東西。

### 3a. 欄位

| 欄位 | 判定 | 具體例子 |
|---|---|---|
| §0 來源完整性 | **改** | 盤點表的問題是「原始報告不見了」；這裡是「原始報告都還在，但全在 repo 外、沒有保存保證，進 repo 的只有轉述」。欄位要分成：進版控／repo 外仍在／已消失 |
| 驗證層／方法 | **改** | 審查層是一層一層的，但 TDD、反向對照、變異測試一次覆蓋幾十條 claim。只用層表會把「C1 有 20 條測試」壓成一格，所以本文另做了 §1 逐 claim 表。程式案例的主單位是 **claim（scenario）**，不是層 |
| claim／oracle | **順，且更清楚** | 每條測試就是一個 oracle、對應一個 scenario；R1 F6、R3-F8 正是「oracle 沒對準 claim」（只驗入列、不驗顯示；只測函式、不測 consumer）。P3 在程式案例**一樣成立** |
| 執行者與強制機制 | **改（要拆兩欄）** | 「誰判」和「誰決定跑」在這裡分開：pytest、變異 runner、`openspec validate` 的判定是程式，但**何時跑、跑不跑由 agent 決定**；鑑別力閘是程式 hook，但只保證問題被送到，不保證認真回答（`discernment_gate.py` 檔頭） |
| 成本 proxy | **順（資料比較多）** | 有 tool call 數（55、23、51、84）、全量測試約 210 秒（實測）；變異一批約 2.4 分是 runner 依單輪 5.90 秒的**預估**（`SP/mut-vp.err`），不是整批實測；仍沒有 token 與實際花的時間 |
| 受測快照 | **順** | 每輪都有 commit hash（`c0bf6a9`→`a9bc844`→`bc04b07`→`3723757`→`f6816b8`→`ad71178`） |
| 已知漏抓 | **順** | R4-1、CB-F2、M12 都填得出「哪一層在範圍內但沒抓到」 |
| 嚴重度 | **順，但跨層會被改標** | Codex P1 的 R3-F7，回顧改標 📌 nit；回顧裡最高的 🔴 根本不是審查 finding，是作者自己的錯誤斷言（F-S1） |
| 首次／重新 | **順，但可能要細分** | 盤點表定義「重新發現＝同一缺陷先前已被記錄（含被 defer）」（盤點表 §2 開頭）。這裡的重新發現都是**修了但沒修完、下一輪再被指出（半修）**（R2-F2／F3、R3-F2），落在這個定義內；另有**修正動作自己帶進新錯**（R3-F7、R4-1 都在 `bc04b07` 才出現），盤點表現以「首次（修正引入）」註記（F-VS2、F-VS11）。單案例下的提議：「重新」底下細分「曾 defer」與「半修」，「修正引入」由註記改成獨立類別（見 §5 H3） |
| 前一層是否已漏過 | **改** | 層不是依序排的：文件審 R1–R4 發生在**程式還沒寫之前**，審的是 plan 裡的程式碼（F4 是 Codex 直接跑 plan 的 regex 抓到的）。「前一層」要改成「先前任何一個範圍內有它的時點」 |
| 如果沒抓到會怎樣 | **新** | 盤點表規定一律是推論。這裡有**已發生的後果**：舊判準造成 9/29 真的誤刪 3 條（`290850b`），是 R2-F11 追查時才發現。欄位要能標「已發生（附出處）」和「推論」 |

### 3b. 觀察 O1–O8

| 觀察 | 判定 | 這個案例的情況 |
|---|---|---|
| O1 後層抓到前層漏的 | **順** | R4-1（R3 漏）、CB-F2（五層漏）、M12（手工反向對照漏、工具抓到）。同樣不能推論原因：快照與模型都不同 |
| O2 讓證據失真的多落在器材 | **順，但「器材」定義要改** | R2-F9（反向對照會假紅）、F6／R3-F8（測試守不到 → 假綠）、M12、措辭守門測試改後仍綠（R4-P3）。**在程式案例裡，測試同時是器材也是交付物**，盤點表「器材 vs 受測產品」的二分放不進去 |
| O3 原標嚴重度和後果不一致 | **順** | R3-F7：Codex P1、回顧 nit，但沒抓到的話 3 條誤刪行不會還原 |
| O4 平行第二執行者 | **不適用** | 本案沒有平行執行者；備援與 Codex 是先後補審 |
| O5 重新發現佔可觀比例 | **順（成因不同）** | 這裡的重新發現都是「半修」（R1→R2→R3 共 3 條），沒有「曾 defer 又抓到」；兩者都在盤點表的「重新」定義內，但成因不同 |
| O6 證據壽命 | **改（部分反例）** | 原始紀錄都還在，所以「已經消失」不成立；但它們全在 repo 外，壽命取決於沒人清理。帳本的轉述有漏：沒寫 Codex 補審跑不起全量測試、沒寫 Codex R1 自己重跑探針 |
| O7 強制機制幾乎都是 agent 照文字執行 | **改（部分成立）** | oracle 多半是程式（pytest、runner V1–V7、strict validate），也有一個程式 hook；但**觸發時機與完成判定**仍由 agent 決定（verify 是主 session 自己做，`verify.md:5`），coverage gap 那一步沒有紀錄 |
| O8 成本大多未知 | **改（這案例資料較多）** | 原始紀錄還在，所以數得出 tool call 數與部分執行時間（全量測試為實測、變異整批為 runner 預估）；token 仍未知 |

### 3c. 框架沒有、這案例出現的東西

1. **實作前 RED 不一定有判別力**：Task 1 的 RED 是「屬性不存在」的例外（`TR` 1725、1730），什麼也證明不了；真正證明「測試分得出錯」的是**反向對照與變異測試**，而且手工反向對照漏了 M12。起點備忘 §5 第 3 條寫「TDD 把判別力檢查內建在 RED→GREEN 流程裡；對原本就採 TDD 的任務，通常不需要另外設計一套負向對照」——**這個案例不支持那句**：workflow-harness 規則本身就要求另做反向對照（其 `CLAUDE.md:100`），也實際跑了變異測試。【推論】這句可能是從規則文字類案例（那裡 RED 是「錯誤判定」，本身就有判別力）推出來的。
2. **判別力有兩種粒度**：反向對照是「每條測試 → 每個壞實作」；變異 runner 只給整批分數，**沒記哪條測試殺了哪隻**（`SP/mut-vp*.json` 只列活口）。Task 1 原本的 17 條測試中，有 9 條沒有任何手工壞實作讓它轉紅（`TR` 1780 對照測試清單）（例如 `test_deferral_without_spaces_counts`、`test_multiple_deferrals_use_last`），它們個別的判別力【未查證】。
3. **同一個 change 裡有兩種受測對象**：程式（C1、C2、C6）有完整 RED/GREEN；agent 行為（C4、C5）沒有任何 oracle，**完成時仍開著**，verify 用「PASS WITH WARNINGS」＋「10/15 dogfood」帶過。框架沒有「完成時仍開著的 claim、預定什麼時候驗」這個欄位。起點備忘 §2「分流單位是 claim、不是整個 change」在這裡得到一個實例。
4. **審查在程式寫出前就當 oracle**：Codex 讀 plan 裡的程式碼並實際執行 regex（F4）、推演反向對照會崩潰（R2-F9）。這是「在 RED 之前驗器材」，盤點表的層都是審已經存在的東西。
5. **真實資料上的 RED**：探針在修前用workflow-harness 真資料跑出「挑出 0 個」（C10），修後回讀「10/15 挑出 5 個」（C2）。這是單元測試以外的另一組前後對照，盤點表沒有這個層。
6. **被缺陷本身污染的量測**：探針第 [3] 段量到「backlog 帶 graduated 的條目：0 條」（`…txt:18`），這個 0 是 9/29 誤刪造成的，原本被當成「零活體」的佐證。框架沒有欄位處理「量到的環境已經被受測缺陷改過」。
7. **基準就有的失敗**：全量測試 3 條失敗是基準既有的，完成判定靠「與基準相同」排除（`verify.md:69`）。框架沒有「基準噪音」這欄。

**3d 的「有沒有被帶偏」整理在 §5。**

---

## §4 A 的順帶樣本：驗證器材自己出錯

| # | 器材 | 出了什麼錯 | 後果／是否靜默 | 誰發現 | 出處 |
|---|---|---|---|---|---|
| A1 | plan 的反向對照 #4 | 壞實作把 regex 改成 `r"延期"`，`m.group(1)` 會拋 IndexError；轉紅只證明崩潰 | 會給出「測試抓得到」的假證據；**跑之前被攔下** | Codex R2（推演） | 帳本:28；`RO1` R2-F9 |
| A2 | `SP/mutants.py`（反向對照腳本） | 前兩版判不出失敗型別，每條都印 `(?)`；第三版才改對 | 不靜默（顯示 `?`）；作者另抽一個壞實作手動確認後才修 | 作者 | `TR` 1780、1790、1803、1811 |
| A3 | 測試套（plan 原稿） | 只斷言延期節點有入列，沒驗顯示日期與排序 | 顯示錯日期也全綠（假 GREEN）；實作前補上 | Codex R1 F6 | 帳本:14 |
| A4 | 測試套（plan 原稿） | 只測判斷函式，沒測 `build_plan` 與刪除前重查 | consumer 層退化測不到；實作前補上 | Codex R3-F8 | 帳本:44 |
| A5 | 測試套（實作後） | 「先無效、後合法」的延期段沒有測試 | 變異 id 12 活下來；補測試後殺掉 | 變異 runner | 樣本帳＃9；`fcd5695` |
| A6 | 措辭守門測試 `test_graduated_predicate_wording_present` | 判準改寫後仍綠，已不再守住措辭 | 假綠；補 `assertIn("延期中")` | Fable R4 | 帳本:56；`aa99c87` |
| A7 | 變異活口的等價判定（人判） | 判定對、理由錯（歸因 future import，實為 PEP 526） | 後人照錯的理由去「殺」它 | strict-reviewer r1 | 樣本帳＃9；`d34967b` |
| A8 | Codex 補審的執行環境 | 唯讀沙箱建不了暫存目錄，全量 pytest 跑不起來，改跑 140 條 | 該層證據比帳本寫的窄；**帳本沒記** | Codex 自述 | `RO2` 第 90、140 行；帳本:70 |
| A9 | 探針的出處標記 | brainstorm 寫輸出來自 HEAD `c0bf6a9`，輸出檔第一行是 `a9bc844`；兩版的解析器程式相同，結果不受影響 | 出處標錯、數字不受影響 | 本盤點（核對 commit stat） | `CH/brainstorm.md:7`；`…txt:1` |
| A10 | 探針第 [3] 段的篩選條件 | 用字串 `"延期 →" not in result`，和正式 regex 不同（不認 `->`、不認無空白）【推論：遇到那些寫法會分錯】；當時資料沒有這些寫法 | 當時無實際失真 | 本盤點 | `CH/evidence/延期節點現況探針.py:47` |
| A11 | commit 訊息的回讀宣稱 | 「diff 僅 +3 行」實為 +3 條目另改 1 行 | 紀錄的數字不精確 | strict-reviewer r2 | 帳本:66 |

---

---

## §5 單案例推論與假說（不升格）

以下全部是【推論】，只有一個對照案例支撐。用途是決定下一個對照案例要看什麼，不是修改框架的依據。

| # | 假說 | 依據（本案例） | 要怎樣才算成立 |
|---|---|---|---|
| H1 | 起點備忘 §5 第 3 條「TDD 把判別力檢查內建在 RED→GREEN 流程裡；對原本就採 TDD 的任務，通常不需要另外設計一套負向對照」**在本案例不成立**；那句可能是從規則文字類案例（RED 是「錯誤判定」，本身就有判別力）推出來的 | §3c-1：Task 1 的實作前 RED 是「屬性不存在」的例外；判別力來自反向對照與變異測試，手工反向對照還漏了 M12 | 第二個程式案例也出現「實作前 RED 無判別力、要靠另做的負向對照」 |
| H2 | 程式案例的主單位是 **claim（scenario）**，不是驗證層 | §3a「驗證層／方法」：TDD、反向對照、變異測試一次覆蓋幾十條 claim，層表壓不下 | 第二個程式案例同樣需要逐 claim 表才記得下 |
| H3 | finding 生命週期可能需要細分：「重新」底下分「曾 defer」與「半修」，「修正引入」由註記改成獨立類別；「如果沒抓到會怎樣」要能分「已發生（附出處）／推論」 | §3a；R2-F2／F3、R3-F2（半修）；R3-F7、R4-1（修正引入）；R2-F11 追出 9/29 已誤刪 3 條（`290850b`） | 第二個程式案例也出現半修或已發生的後果。盤點表本身也有修正引入的例子（F-VS2、F-VS11），但那些在規則文字類案例裡 |
| H4 | 在程式案例裡，**測試同時是驗證器材和交付物**，盤點表 O2「器材 vs 受測產品」的二分放不進去 | §3b O2；§4 A3–A6 | 第二個程式案例的器材缺陷同樣落在交付的測試套上 |
| H5 | P2（TDD applicability 之爭）的份量**可能是規則文字類案例放大的** | 原盤點判斷：程式部分大家都同意要 TDD，agent 照文字做的部分大家都同意測不了，這個案例完全沒出現爭議 | 第二個程式案例同樣沒有 applicability 爭議 |

**沒被帶偏（換到程式案例仍成立）的觀察**：P3「oracle 對準 claim」（F6、R3-F8、R2-F9）、O1、O2、O3。這也只是單案例，同樣不升格。

---

## §6 使用者裁定（2026-10-05）

- **盤點表的欄位與分類暫不修改**（「甲」）。H3 的「已發生 vs 推論」、「半修」、「修正引入」先記在本文件；等**至少再有一個一般程式案例**，看這些現象是否重複出現，再決定要不要改盤點表欄位。盤點表同日補記的 F-VS11 照現有欄位填，以「首次（修正引入）」註記，並指回本文件。
- 本案例出現的「驗證器材自己出錯」（§4）**順便當 A 題的樣本**；A「驗證工具本身也要被驗」不獨立開題。C「Harness 地基是 agent 執行的文字」保留，不在這一步展開。
- 做完這一輪事實盤點後，再判斷 A 與 C 誰值得升成下一個研究題。

---

## §7 沒查的範圍

- `SP/r1.json`、`r1b.json`、`r2.json`、`r3.json`、`cb.json`、`mutants.py` 以外的 scratchpad 腳本都沒讀；`RO1`／`RO2` 只抽了 user／assistant 訊息，沒逐一看 55＋23 次 tool call 的內容。
- strict-reviewer 第一輪原文沒讀（只讀該 agent 最後一則）；Fable R4 只讀 prompt 與最終回報。
- 主 session 逐字紀錄只用腳本抽了 pytest／反向對照／runner 的結果行與第 1700–1830 行；其他段沒讀，所以「coverage gap 有沒有跑」【未查證】。
- 變異 runner 的 `survivors`、`baseline` 內容沒讀；哪條測試殺哪隻突變體沒有資料。
- 規格 scenario → 測試的對應只用測試名稱與 plan 對照，沒有逐條讀斷言內文（strict-reviewer 與 Codex 補審有讀，我引用它們的結論）。
- 10/15 dogfood 還沒發生；改動上線後（10/1 之後的 `#164`、審查帳本計數器等 change）有沒有再碰到這段程式，沒查。
- 只有一個對照案例；沒找 workflow-harness 其他已 archive 的程式 change 比較。
