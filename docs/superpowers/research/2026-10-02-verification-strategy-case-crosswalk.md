# Verification Strategy 第一步：三個案例 × 既有研究對照（2026-10-02）

> **定位**：分析參考，不是規範、不是提案。這是 work-map `task-20260929-verification-strategy-research` 的第一步（2026-10-02 使用者裁定）：**不提新理論**，先把三個已結案的實際案例，與既有研究逐項對照。
>
> **上層三問**（使用者定調）：**驗什麼**（Claim）／**怎麼驗**（Method）／**驗到哪停**（Depth／stopping condition）。
>
> **方法宣告**：每格註明出處。§1 只列事實；§2 分「事實／推論」兩欄；§3 列待使用者裁定的問題，**不拍板**。本步只讀 repo 內材料、**沒有讀任何外部來源**——work-map 研究題提到的外部做法摘要（Anthropic／OpenAI eval、Cucumber、OPA、Promptfoo）留到後續步驟，屆時讀原文、附出處。
>
> **verify-sync lifecycle** 子題（`task-20260930-verify-sync-lifecycle`）在本文只當 §2 P6 的一筆輸入，**不當研究入口**（2026-10-02 使用者裁定）。

---

## 0. 範圍與來源

| 代號 | 來源 | 讀法 |
|---|---|---|
| **ID** | change `requirement-scenario-identity`（archive `2026-10-01-…`）：`retrospective.md`、`design.md` Open Questions、`brainstorm.md` Q8–Q14；`docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/README.md`（§1–§5） | retrospective、poc README 全文；design 讀 D10 之後到結尾；brainstorm 只用 grep 定位 Q14 相關行 |
| **RS** | change `retro-skill-inventory`（archive `2026-10-02-…`）：`retrospective.md`、`tasks.md`、`apply-evidence.md` | 三份全文 |
| **I2** | `docs/superpowers/poc/2026-10-02-issue2-compat-spike/report.md`；使用者對 A1／B1 的裁定與 `raw/` 精簡檔數，見 `文檔/handoff/session-handoff-20261002.md` 15:20 區塊「二、完成事項」（report 本身只記建議與選項） | report 全文；handoff 只讀該段 |
| **TE** | `research/2026-09-01-tdd-evidence-analysis.md` | 全文 |
| **PS** | `research/2026-09-01-plan-structure-comparison.md` | 全文 |
| **CD** | `research/2026-09-10-contract-drift-archaeology.md` | 全文 |
| 對照用 | 正式設計 `specs/2026-09-01-bridge-guarantee-formal-design.md` §4.3；主 spec `openspec/specs/tdd-evidence-contract/spec.md` REQ-1、REQ-2 | §4.3 全節；spec 只讀 grep 命中的行 |

**沒讀的**：ID 的 `verify.md`、`sdd-ledger.md`、`migration-acceptance.md`、`blind-runs/` 原始報告（本文引用的是 retrospective 與 poc README 對它們的轉述）；RS 的 `verify.md`、`design.md`；`research/2026-09-09-review-provenance-analysis.md`、`2026-09-21-…`、`2026-09-23-…` 三份研究（不在指定範圍內，P7 有一處只引用 CD 對 provenance 分析的轉述）。

---

## 1. 案例卡：每一個驗證動作的 Claim／Method／Depth

每列是案例中一個**實際發生的**驗證動作。「代理指標落差」欄記錄的是：量到的東西不等於要證明的宣稱，而且有紀錄可以佐證的情形。

### 1a. ID — requirement-scenario-identity（新增 verify check 13：身分完整性規則）

| # | Claim（要證明什麼） | Method（怎麼驗） | Depth／停在哪 | 結果 | 代理指標落差 |
|---|---|---|---|---|---|
| ID-1 | 舊規則（checks 1–12）**抓不到**身分缺陷 | RED：1 位無脈絡的 sonnet 盲測執行者，用舊規則跑 22 個打亂命名的 fixture | 17 個植入缺陷的 fixture（16 個預期「違規」、`u01` 預期「無法判定」）全部判完 | 22/22 `PASS {}`，前提成立（poc README §3a） | — |
| ID-2 | 新規則**抓得到**，且類別判對 | GREEN：2 位互相獨立的執行者，同一份打亂副本；以預期答案表評分（最終判定＋BLOCK 類別集合都要相同） | 評分規則：最終判定與 BLOCK 類別集合都要和預期相同，理由不必逐字一致；兩人判定不一致時不投票、不取多數，該案不算 GREEN（poc README §4） | v2：A、B 各 22/22 MATCH | — |
| ID-3 | 新規則**不誤擋**正向案例 | 5 個 conformance-only fixture 一起跑 | 同 ID-2 | 維持 `通過 {}` | — |
| ID-4 | 規則文字**可被一致執行** | 第二位執行者（B）＋逐輪比對 | 出現不一致就分類：規則文字／器材／執行環境 | r1 抓到規則文字歧義（v13），r2 抓到回報格式自相矛盾（v06）（poc README §5 Q2–Q3） | r1／r2 的「21/22」若不分類，會把器材缺陷當成規則缺陷 |
| ID-5 | 器材修正**沒有改變**基準 | RED replay：v2 器材＋舊規則重跑 | 結果與原 RED 不同就 STOP（使用者裁定，poc README §3b） | 22/22 一致 | — |
| ID-6 | 評分器**分得出**錯誤 | `grade.py --selftest`；I3 定點驗收前先用假報告證明兩條錯誤路徑都回 DIFF | 每條要抓的錯誤路徑都要能改變評分 | 重複案例的漏洞在 GREEN **之後**才被 Codex 抓到（ID retrospective §2） | selftest 沒涵蓋「同一案例出現兩次」→ 注入重複仍 MATCH 22 |
| ID-7 | 規則改了以後，證據**仍對應最終文字** | 被測物改了就重跑（v3），舊 GREEN 降級為 provenance | 規則本體被修正後，由使用者裁定重跑；sha256 記錄的是「規則文字已不同」這件事 | v3：A、B 各 22/22 | 22/22 只證明「沒破壞既有案例」，**不證明 I3 分支**（22 題都沒觸發它）→ 另補 2 題定點驗收，單一執行者、單次樣本 |
| ID-8 | 補號遷移**內容不變**（D7） | 預演歸檔＋逐行比對＋CLI 數量交叉核對 | 字面判準：除標題外逐行一致 | 字面判準沒過（3 行空白差異），改用「排除標題與空白行」的 diff，以 approved deviation 結案（poc README §5「量測本身的教訓」） | **逐行相等 ≠ 內容不變** |
| ID-9 | 歸檔預演**成功** | 看結束碼 | — | 中止時仍回 0（1.3.1） → 改為「結束碼 0 **且** change 已移入 `archive/`」 | **exit 0 ≠ 成功** |
| ID-10 | 驗證所需的 pre-sync 狀態**還在** | — | — | 合法的 sync 會把它吃掉（I3）；本 change 以「依證據依賴局部判無法判定」處理，lifecycle 另立研究題（ID retrospective §5） | 證據的存在依賴操作順序 |
| ID-11 | proposal 新段落（Out of Scope／Assurance Boundary）**有被用到** | 全文搜尋下游引用＋掃 subagent 對話紀錄 | n=1，明寫 inconclusive-positive | 下游沒有引用；真正發揮作用的是 design D10 與 spec owner 規則 | — |

**TDD applicability 的來回**：check 13 是給 agent 照著執行的規則文字，不是程式。這個 task 的標註前後改了三次（Q8 n/a → Q10 applicable → Q11 n/a → Q14 applicable），最後採「**可觀察行為判準**」：只要同一組可重跑的案例在修改前後顯示行為改變，就算 applicable；RED 的內容是「真實的錯誤判定」，不是 `INDETERMINATE`（ID `brainstorm.md` Q14；`design.md` Open Questions 最後一條）。

### 1b. RS — retro-skill-inventory（修正 retrospective 模板 §4 與 schema 指令）

| # | Claim | Method | Depth／停在哪 | 結果 | 代理指標落差 |
|---|---|---|---|---|---|
| RS-1 | 模板 §4 恰好是 REQ-5 的六列 | 讀檔逐條核對 REQ-5-S1..S4（RS `tasks.md` 1.1 的 n/a 理由） | task 審查＋全分支總審 | 通過 | — |
| RS-2 | schema 指令陳述兩類判準 | 讀檔核對 REQ-5-S4 | 兩次 task 審查**沒抓到**排除句漏掉限定條件；opus 全分支總審抓到（RS retrospective §1） | 修正 schema | — |
| RS-3 | 同一缺陷在**所有表面**都修好了 | 備援文件審查（contract-neutral-reviewer）4 輪 | 「🔴 才擋」＋使用者裁定停止（handoff 2026-10-02 15:20 當日洞見） | 第 3 輪才指出模板漏修（RS retrospective §2） | — |
| RS-4 | README 沒有跟 REQ-5 衝突的說法 | 4 條 grep＋指定段落全文讀（`apply-evidence.md` §2.1） | grep 命中逐行歸類 | 無衝突；但 zh-TW 第 413 行**是靠全文讀找到、grep 沒命中** | 記錄的 grep pattern 不足以重現這個結論 |
| RS-5 | CLI 交給 agent 的**實際指令**帶新文字 | `openspec instructions retrospective` 擷取輸出 → 舊句缺席（`grep -c` = 0）、新句存在、表格 6 列、無 `writing-plans` 列（`apply-evidence.md` §2.2） | 修正後重跑一次 | 通過 | — |
| RS-6 | apply 已產出可審的實作（verify PRECHECK 第 1 條） | 數 `merge-base..HEAD` 的 commit 數 > 0 | — | 分支在實作前就有 2 個設計 commit，**實作沒 commit 也會通過**（RS retrospective §5） | **commit 數 > 0 ≠ 實作已 commit**；真正確認的是 check 5 |
| RS-7 | 完成宣告的證據**可追查** | retrospective／verify 引用 SDD ledger 與 scratchpad 報告 | — | ledger 只在 worktree 裡，worktree 一拆就消失（RS retrospective §0、§5） | 證據的壽命比宣告短 |

**TDD applicability**：4 個 task 全標 `n/a`，理由都是 artifact 類型——「template prose; no executable behaviour」「instruction prose passed verbatim」「delivery check of existing CLI behaviour; no new behaviour is introduced」（RS `tasks.md`）。

### 1c. I2 — issue #2 上游相容性 spike（OpenSpec 1.3.1→1.14.0、Superpowers v5.1.0→v6.4.2）

| # | Claim | Method | Depth／停在哪 | 結果 | 代理指標落差 |
|---|---|---|---|---|---|
| I2-1 | 依賴清單**沒有漏** | 全文讀 schema／README（en）＋對整個 bundle 用 6 組 grep 逐筆歸類（I2 §0「窮盡方法」） | 列出沒全文讀的部分（zh-TW README、4 個模板、verify 模板中段），寫明 grep 掃不到「只描述上游行為、沒提 skill 名稱」的句子（I2 §5） | 42 項依賴 | — |
| I2-2 | bridge 用到的 OpenSpec CLI 行為**仍成立** | 同一份 fixture、同一支腳本，兩個版本各跑一次，stdout／stderr／exit code 分開比對 | 20 項雙版對照、1 項單版、3 項讀原文——**方法混合，報告開頭明寫** | 16 成立／8 有變化／0 不成立 | — |
| I2-3 | instruction **原樣**送到 agent | Python 字串相等比對（verify 那份 51,876 字元） | 4 個 artifact | 逐字相同 | **送達 ≠ 遵守**：O6 只證明字串到了 agent 手上，不證明 agent 會照做（I2 §5 自己寫明） |
| I2-4 | bridge 對 Superpowers 的**文字宣稱**仍成立 | 只讀上游原文（SKILL.md、scripts、release notes），只有 S11 實際執行 | 沒跑任何 skill；prompt 層的項目全部是讀原文判斷 | 6 條不成立（其中 S13、S14 兩條是新出現的，都與 executing-plans 有關） | — |
| I2-5 | baseline 可以提高 | 由上述證據＋使用者裁定（report §4 只列建議與選項；裁定紀錄在 handoff，見 §0） | 宣告範圍限定為「**CLI 層級**的確認」（裁定 A1） | OpenSpec→1.14.0；Superpowers 維持 v5.1.0（B1） | 宣告的範圍刻意比「相容」窄，對準實際驗到的東西 |
| I2-6 | 原始輸出**可重現** | 整個 spike 目錄從 213 檔精簡到 29 檔（`raw/` 28 檔＋`report.md`；檔數出處 handoff，見 §0），保留腳本與 `SUMMARY.md` | 「需要原檔可照 SUMMARY 重跑」 | — | 用**可重跑**取代**保存原檔**（與 RS-7 方向相反的取捨） |

---

## 2. 跨案例 pattern × 既有研究

每列是一個在兩個以上案例出現的 pattern。「既有研究怎麼說」只引用 TE／PS／CD 及 §0「對照用」來源原文有寫的部分（P8 另引 RS retrospective）；「推論」欄是我的判斷，不是事實。

| # | Pattern（事實） | 出現在 | 既有研究怎麼說 | 推論：支持／延伸／矛盾 |
|---|---|---|---|---|
| **P1** | **受測對象不同，實際用的驗證方法就不同**：規則文字→盲測 conformance＋mutation fixtures（ID-1~3）；模板與指令文字→讀檔核對＋CLI 送達查驗（RS-1、RS-5）；上游依賴宣稱→雙版實測或讀原文（I2-2、I2-4）；遷移→before/after 對帳（ID-8）；跨文件一致性→grep＋審查（RS-3、RS-4） | ID、RS、I2 | TE §1 把 Skill（程序）／Verification（檢查什麼）／Evidence（憑什麼成立）分三層，但整份只處理「程式行為→TDD」一條路；ID `design.md` Open Questions 列了五條候選路由（程式→TDD；schema 與可機械規則→conformance／mutation；Skill 與文字規則→behavioral eval；跨文件契約→consistency／traceability；migration→before/after） | **延伸**：五條候選路由中，明確出現的是三條（conformance／mutation、consistency、before/after）；behavioral eval 只以 ID 盲測的形式出現，而且和 conformance 是同一個動作；程式→TDD 三案都沒有出現。反過來，**I2 的兩種方法（雙版本對照實測、讀上游原文）不屬於五條中的任何一條**——「對上游依賴的宣稱」是候選清單沒涵蓋的受測對象。部分案例記錄了**本案**為什麼這樣選（例：ID `design.md` D9 的證據策略與理由、poc README §3a 選 sonnet 的理由），但**沒有跨案例共用的路由判準**，也沒有系統性的方法比較——路由是每個 change 各自選的 |
| **P2** | **TDD applicability 的兩種判準並存，同一週的兩個 change 標註方向相反**：ID 對「agent 執行的規則文字」採行為判準→applicable（判準來自 2026-09-07 對 fix-v2 的使用者裁定，ID 在 brainstorm Q14 採用）；RS 對「agent 讀取的指令文字」採 artifact 類型判準→n/a。RS-5 的 CLI 查驗能看出前後差異（改動前的 `schema.yaml`〔`da1e5f2`〕含舊句 1 處，改動後 CLI 輸出 `grep -c` 為 0；改動前的數字是本文事後以 `git show` 重建的），但它驗的是**指令有沒有送達**，不是 **agent 收到後行為有沒有改變**——後者沒有人跑過。ID 的標註則在 n/a 與 applicable 之間來回三次（§1a），每次都牽動 tasks、審查與派工 | ID、RS | 正式設計 §4.3：條文對象是「applicable **executable-behavior code** task」；範圍段寫「改文件、純資料調整等不 applicable」。spec `tdd-evidence-contract` REQ-1：標註是 semantic assertion，由 review 判斷。同 spec REQ-2：RED 的通用條件是「non-pass outcome that is a behavioural failure」，是否屬 behavioural failure 由 review 判斷；另明定**「以閱讀執行的規則」**（these checks themselves, when a change edits them）若 RED 記為 `INDETERMINATE`，SHALL 判為 behavioural failure。TE §4 的 RED 有效性表只列 assertion failure，是 REQ-2 之前的分析版本 | **規範衝突確實存在，但「造成相反處置」的實證不完整**：照 §4.3 的字面，RS 標 n/a 是對的。RS-5 **不能**當成行為判準下的 RED——它是**送達驗證**（claim：CLI 交出正確版本的指令），對這個 claim 它會真的失敗、有價值；但拿它支撐「agent 行為改變」就是 P3 那種 claim 與 oracle 對不上（與 I2-3「送達≠遵守」同型）。要說 RS 在行為判準下會是 applicable，需要一個沒跑過的行為驗證（讓 agent 照新舊指令各寫一次 retrospective §4，比對是否列出 `writing-plans`）。所以目前能確定的是：**兩條判準並存、沒有一條是 owner，已在 ID 造成反覆修改的成本**；兩個 change 的相反標註是否真的是判準造成的不同處置，還沒有實證。**指令送達行為 ≠ agent 執行行為**，這是兩種不同的受測對象。衝突的兩端是正式設計 §4.3（artifact 類型判準）與 2026-09-07 裁定（行為判準），不是 §4.3 與 REQ-2：REQ-2 只規範**已標為 applicable** 的 task 要附什麼證據，`INDETERMINATE` 條款回答的是「若做，RED 可以長什麼樣」，不決定哪些 task 適用（ID brainstorm Q11、design Open Questions）。REQ-2 對規則文字類受測對象**只明文定義了一種 RED 形態**（`INDETERMINATE`）；ID 實際用的是另一種——舊規則給出**錯誤判定**（`PASS {}`），這是否算 behavioural failure 目前交給 review 判斷，ID 依 2026-09-07 裁定處理（brainstorm Q14）。RS 的受測對象（retrospective 指令）也不在 REQ-2 那句的明文範圍內（「these checks themselves」） |
| **P3** | **代理指標對不準宣稱**：exit 0≠歸檔成功（ID-9）；逐行相等≠內容不變（ID-8）；22/22≠I3 分支正確（ID-7）；commit 數>0≠實作已 commit（RS-6）；送達≠遵守（I2-3）；grep pattern≠結論可重現（RS-4） | ID、RS、I2 | TE §6：「不能區分狀態的欄位是假裝在保證，比沒有更糟」（因此拿掉 artifact state ref）；TE §4：RED 的 claim 被兩輪收窄，「不得表述為證明測試在 implementation 前執行過」。CD H8：「散文寫成 deterministic」不等於兩個 agent 會得到同一答案 | **支持且擴大**：TE 只在 TDD 證據欄位上處理這個問題；三個案例顯示它出現在 verify PRECHECK、驗收判準、歸檔判定、依賴查證四個地方。memory `feedback_claim_first_discriminating_oracle`（ID retrospective §6 ②）已把它寫成經驗：先寫 claim，再選一個「claim 為假時一定會變」的觀測量。**目前沒有 schema 表面要求每個驗證動作做這一步**（既有的宣稱邊界是固定文字，見 §3a） |
| **P4** | **評分器／器材本身要先被驗證**：ID 的 grader selftest、凍結器材、RED replay（ID-5、ID-6）。I2 用「同一份 fixture、兩個版本」是**對照實驗的變因控制**（I2-2），不是驗證比對方式分得出錯——兩者是不同的事 | ID（I2 只是相鄰的對照設計） | TE §2：Verify RED 的作用之一是篩掉構造上不可能失敗的測試（tautological test）。CD §2 D 類 5 條：答案表過期 2、缺 fixture 2——「fixture 有效只在有人重推時；答案表是第二份 truth」（CD Q5） | **延伸（單一案例）**：依本表欄位規則，「評分器要先驗」目前只有 ID 一個案例，**還不算跨案例 pattern**，列在這裡是因為它和 TE、CD 的既有論點直接相關。TE 的「RED 篩掉 tautological test」是針對**測試**；ID 顯示**評分器**也需要同一件事（先證明它分得出錯），否則 RED/GREEN 翻轉本身可能是評分器的假象。ID 的教訓是器材要在 RED 之前凍結並自測（ID retrospective §2 第一條） |
| **P5** | **驗到哪停，每個案例各自決定**：ID——兩位獨立執行者逐案一致、不投票（poc README §4），規則一改就重跑（臨場訂的）；RS——文件審查以「🔴 才擋」加使用者裁定停在第 4 輪（「🔴 才擋」來自既有規則，見推論欄）；I2——以「依賴清單窮盡＋明列沒讀的部分」為邊界，宣告只到 CLI 層級 | ID、RS、I2 | TE §3：suite green 不進 per-task 證據，留給 change-level／CI；TE §7：required 與 supporting 分開（「useful 不自動升格 required」）。CD Q4：B 類（判定文字不精確）同族會「逐洞補、補不完」。PS、TE、CD **都沒有定義停止條件**。但 repo 有一套運作中的**審查收斂**停止規則：`.claude/rules/auto-loop.md`（sd0x-dev-flow plugin 安裝）§ Tiers、§ Stall Detection and Diagnosis、§ Sub-Threshold Findings——依 tier 決定哪些嚴重度會擋、剩下的都低於門檻就放行（「80 is a passing grade」）、連續 3 輪沒有關掉任何 finding 就停下來診斷、第 10 輪 checkpoint、第二次撞到輪數上限轉人工；輪數上限本身明寫是「deliberately loose runaway backstop」，不是深度校準 | **三份研究的缺口，不是 repo 的空白**：既有研究沒談 Depth，但 auto-loop 是一個成形的**收斂型**先例，而且已用 tier 把風險接到深度（security／data-integrity 一律 `thorough`）。它管的是**審查意見是否收斂**，不是**證據是否足夠**——ID 的停點（兩位執行者判定一致）收斂的是另一種東西，auto-loop 沒有涵蓋。其數值（輪數上限、80 分）有沒有實測依據，本文沒有查證。三個案例的停點有一個共同形狀——**把沒驗到的範圍明寫出來，讓宣告的範圍比驗證的範圍窄**（ID-7 的「22/22 不證明 I3」、I2-5 的「CLI 層級」、ID-11 的「n=1 inconclusive」），但沒有表面要求每個驗證動作各自這樣寫（既有的固定文字宣稱邊界見 §3a） |
| **P6** | **證據的壽命比宣告短，三個案例三種處理**：ID 把 gitignored 的 ledger 複製進 repo（ID retrospective §3 第 5.3 列）；RS 沒複製，只在 §0 寫明限制（RS-7）；I2 不保存原檔、改保存重跑方法（I2-6）。另有一種是證據被合法操作吃掉（ID-10，verify-sync） | ID、RS、I2 | 正式設計 §4.3（2026-09-23 修訂）：RED 是不可事後重算的歷史事實，GREEN 可重跑但「當時 GREEN」不等於「現在仍 GREEN」，因此 Task 是 owner；TE §8 把「正式 digest·freshness 系統」列為明確不做。CD §2 E 類 8 條：紀錄過期 4、非權威載體 2；H4「`tasks.md` 之外任何載體與事實同步」為不保證項 | **支持，並分出三種子型**：(a) 載體會消失（ledger、scratchpad）；(b) 證據可重算、不必保存原檔（I2 的 raw）；(c) 證據被合法流程消耗（verify-sync）。正式設計 §4.3 已經區分「RED 不可重算／GREEN 可重跑」——(a) 與 (b) 的分界其實就是這條：**不可重算的證據才需要保存，可重算的只需要保存重算方法**。這個判準目前只用在 RED/GREEN |
| **P7** | **誰來驗，影響驗到什麼**：RS 兩次 task 審查沒抓到、opus 總審抓到（RS-2）；ID 的 I3 互斥句通過 task 審查與總審、Codex 才抓到（ID retrospective §2）；ID 選 sonnet 當執行者是**刻意的**，為了「降低強模型用額外推理補足規則歧義造成的假穩定」（poc README §3a）；ID 1.1 由主 session 自做、事後補審 | ID、RS | TE §9 保留意見：assurance 底線繫在「reviewer 真的去讀 RED 輸出」，最弱情境（self-review＋事後補造證據）依然穿得過。CD H11：兩層 review 的差異在**範圍**（task fence vs change-level），不在讀法；H12：自查的錯比 reviewer 的漏更會靜默累積 | **支持，並多一個維度**：既有研究談的是 reviewer 的獨立性與範圍；ID 顯示**執行者的能力**也是驗證方法的一部分——要測「規則文字是否清楚」時，太強的執行者反而會遮蔽問題。這是 ID 的單次實驗設定，poc README 明寫「不是永久的 routing 規則」 |
| **P8** | **同一宣稱寫在多個表面，驗證要涵蓋全部表面**：RS 的排除句 schema 修了、模板漏修（RS-3）；I2 的 executing-plans 理由同時寫在 schema、README en／zh-TW、repo CLAUDE.md 四處（I2 R2） | RS、I2 | CD §2 A 類 32 條（最大宗）；CD Q1：問題單位是「**一規則三讀者**」，不是檔案；CD Q10：最小實驗是「改前 grep → 改 → 改後 grep → `diff -r`」。PS §2 元素 4：Global Constraints 逐字照抄；RS retrospective §6 第二條：逐字副本製造同步義務（正式設計決策表第 2 列「取消人工逐字副本」尚未落地） | **支持**：RS 是 CD 預測的又一個實例（第 N+1 次）。這是 P1 中「跨文件契約→consistency／traceability」那條路由的實際需求；目前的方法仍是人工 grep 與審查輪數 |

**沒有在三案中出現、但既有研究有談的**：PS 的 plan 結構問題只有 RS retrospective §6 一筆「小型 change 的 plan 約一半在重述 tasks」（使用者裁定：部分證據，不能據此推出取消 plan）。TE 的 RED/GREEN 欄位設計，只有 ID 一個案例實際走過，而且受測對象不是程式。

---

## 3. 對三問的初步整理（不拍板）

### 3a. 驗什麼（Claim）

- **事實**：三個案例裡最穩定的做法，是**先把宣告寫得比證據窄**（P5），以及**列出代理指標與 claim 的落差**（P3）。這兩件事目前多半靠作者自覺，或在 retrospective 事後補記。既有的 schema 表面只有固定文字的宣稱邊界（`templates/verify.md` 的「Claim boundary — copy as written, claim no more」、schema check 13 的 13.G CLAIM BOUNDARY），涵蓋的是 deterministic checks 本身，**沒有表面要求每個驗證動作各自寫出範圍**。
- **推論**：TE §4 對 RED 做過的「claim 精確化」，可能是一個可以推廣到所有驗證動作的步驟——每個驗證動作先寫一句「這次能證明什麼、不能證明什麼」。

### 3b. 怎麼驗（Method）

- **事實**：五條候選路由中，三案明確用到三條，另有一種受測對象（上游依賴宣稱）不在清單裡（P1）。TDD applicability 的兩條判準並存、互相衝突，已在 ID 造成反覆修改；RS 的相反標註是否由判準造成，實證不完整（P2）。
- **推論**：研究題原本的問法是「applicability 由 artifact 類型決定，還是由可觀察行為決定」。從 P2 看，更根本的問題可能是：**對「agent 讀取並執行的文字」（schema 指令、模板、check 規則）這一類受測對象，RED 的有效形態是什麼？** spec REQ-2 只對其中一小類——**verify checks 本身，在某個 change 修改它們時**（「these checks themselves, when a change edits them」）——明定一種 RED（規則無法判定而記 `INDETERMINATE`）；其他 agent 讀取的文字（一般 schema 指令、模板）不在該條款範圍內。其餘形態交給 review 判斷「是否為 behavioural failure」。ID 用的「錯誤判定」屬於這個**留給 review 判斷**的範圍——缺的不是定義本身，是判斷的依據沒有寫下來。RS 的「CLI 輸出仍含舊句」則不屬於這一題：它驗的是 **CLI 的送達行為**（RS `tasks.md` 2.2 自己就把受測對象寫成既有的 CLI 行為），不是**下游 agent 的執行行為**；而「哪些 task 適用」的衝突在 §4.3 與 2026-09-07 裁定之間，REQ-2 不決定適用範圍。

### 3c. 驗到哪停（Depth）

- **事實**：三份既有研究沒有處理停止條件，但 repo 的 `auto-loop.md` 有一套運作中的審查收斂規則（P5）。三案的停點分別是「兩位獨立執行者一致」「沒有 🔴＋使用者裁定」「依賴清單窮盡＋明列沒讀的部分」。
- **推論**：停點看起來分兩種——**覆蓋型**（窮盡一個清單：依賴、fixture、表面）與**收斂型**（重複執行直到結果穩定：盲測一致、審查沒有新 🔴）。覆蓋型的停點可以事先定義；收斂型在**審查**這一種上已有 auto-loop 的規則，在其他種類（例如盲測執行者是否一致）上目前都是臨場裁定。

### 3d. 需要你決定的問題

以下都屬於「研究要往哪裡走」的框架選擇，由使用者決定（三題的裁定見 §5）：

1. **P2 要不要當成研究的主軸？** 這是唯一一條「兩個判準並存（正式設計 §4.3 的 artifact 類型判準 vs 2026-09-07 使用者裁定的行為判準）、沒有一條是 owner，而且已經產生實際成本」的 pattern（ID 的標註來回三次；RS 的相反標註是否構成相反處置，見 P2 推論欄，實證不完整）。另一個選擇是把三問平均推進。
2. **下一步要不要開始讀外部來源？** 本步刻意沒讀。P2 的「文字類受測對象的 RED 形態」與 P5 的「收斂型停止條件」，外部的 eval／BDD 做法可能有現成答案；但也可能先在內部案例裡再多收一兩個樣本。
3. **P6 的判準（「不可重算的證據才需要保存，可重算的只保存重算方法」）要不要記成 verify-sync 子題的研究輸入？** 它目前只是從正式設計 §4.3 與 I2-6 推出來的推論。

---

## 4. 未查證與邊界

- **樣本**：三個案例，其中兩個（ID、RS）是 schema change、一個（I2）是 spike；**沒有一個案例是一般應用程式的實作改動、有自己的 TDD 循環**（I2 實際執行了上游 CLI 程式，但那是相容性對照，不是我們改程式）。P1 說「三案沒用到 程式→TDD」是這個樣本的特性，不代表那條路由不重要。
- **只讀轉述**：ID 的盲測原始報告、ledger、migration-acceptance、verify.md 都沒讀全文；ID-4～ID-8 的結論來自 retrospective 與 poc README 的轉述。
- **RS-5 能不能當 RED**：不能，理由有兩層。(1) 它驗的是送達，不是 agent 行為（P2 推論欄）；(2) 即使只當送達驗證的 RED，改動前含舊句也是本文用 `git show da1e5f2:superpowers-bridge/schema.yaml | grep -c "this schema's apply phase"` → `1` 事後重建的，量的是**來源檔**，不是改動前 CLI 實際交出的指令；正式設計 §4.3 把 RED 定為不可事後重算的歷史事實，所以這不能補當 RS 的 RED。
- **既有研究的範圍**：只對照了使用者指定的三份（TE、PS、CD）。`2026-09-09-review-provenance-analysis.md` 與 P7 直接相關，`2026-09-23-requirement-traceability-current-state.md` 與 P8 相關，都**沒有讀**。
- **分類是我的判斷**：§1 的「代理指標落差」欄與 §2 的 pattern 歸類都是事後判斷，換一個人分可能不同。

---

## 5. 使用者裁定（2026-10-02）

> 本節記錄使用者對 §3d 三題的裁定，以及隨裁定新增的研究假說與反例。§1–§4 保持寫作當下的分析原樣。

### 5a. 研究主軸：P2，但先研究「方法邊界」，不急著二選一

> 本節把 P2 當主軸的排序，已由 §5e 重新評估；三層拆法與研究終點仍有效。

研究題**不寫成**「artifact 類型判準 vs 可觀察行為判準，哪個才是正確的 TDD applicability」，因為這樣寫已經預設答案一定是二選一。改寫為：

> **當受測對象不是傳統程式碼，而是會被 agent 讀取、解釋、執行的規則／指令文字時，它的可觀察行為應該如何驗證？其中哪些情況屬於 TDD，哪些應該走另一種驗證方法？**

P2 裡混在一起的三層問題要先拆開：

| 層 | 問題 | 目前歸屬 |
|---|---|---|
| TDD applicability | 要不要走 TDD | 衝突在正式設計 §4.3（artifact 類型判準）與 2026-09-07 裁定（行為判準）之間，沒有 owner |
| RED validity | 如果走 TDD，什麼算有效的 RED | spec `tdd-evidence-contract` REQ-2（通用條件＋規則文字的 `INDETERMINATE` 條款），其餘形態交給 review |
| Verification routing | 這類受測對象最適合用哪種方法驗 | 沒有歸屬；P1 觀察到每個 change 各自臨場選 |

不讓「能做 RED/GREEN」直接等於「就應該叫 TDD」。

**研究的終點**：拆清三層 → 用內部案例與外部資料建立判準 → 回到 §4.3 vs 2026-09-07 裁定，提供足夠依據讓使用者正式裁定 owner。研究是為了讓這個決策可以辯護，不是用來延後決策。

### 5b. 外部研究：現在開始，只查兩條線

原則是「先有問題、再找來源」，不做驗證方法大全。

| 線 | 要回答的問題 | 候選來源 |
|---|---|---|
| 1. 文字類受測對象 | 對規則文字、prompt、schema instruction 這類 agent 執行的文字，外部成熟做法把它當成 test、behavioral eval、conformance test，還是別的東西？失敗基準長什麼樣？ | Anthropic／OpenAI 的 eval 文件（evaluator、grader、coverage、迭代）；Cucumber／BDD（規格與可執行行為的邊界）；Promptfoo 一類 eval framework（prompt／instruction 怎麼建 test case） |
| 2. Stopping condition | 本文觀察到的「覆蓋型」與「收斂型」兩種停止條件（§3c），外部有沒有更成熟的概念、失敗案例或停止規則？ | 同上，依問題取用 |

- ~~**刻意不讀 OPA**~~：work-map 研究題原本列了 OPA，本節當時裁定不讀。**已由 §5f 改為有限度地讀。**
- work-map 研究題的要求照舊：外部做法摘要是另一個 agent 整理的、未查證，研究時要讀原文並附出處。

### 5c. P6 改為待驗證的研究假說，作為 verify-sync 子題的輸入

§3d 第 3 題原本的說法（「不可重算的證據才需要保存，可重算的只保存重算方法」）**已被本 repo 的案例反駁**，修正為：

> **研究假說（未驗證，不是設計原則）**：對結果能穩定重現的驗證，可以優先保存重跑方法，不必保存完整原始輸出；對有歷史性、依賴環境、結果不固定，或由 agent 判斷的驗證，重跑不一定能重建當時的證據，因此可能仍需要保存原始結果與 provenance。

它要撞的反例：

| # | 反例 | 來源 |
|---|---|---|
| C1 | 結果雖然可以重跑，但上游版本已經變了，還算可重算嗎？ | 使用者提出；I2 的 `raw/` 能重跑，前提是 `npx @fission-ai/openspec@1.14.0` 與上游 tag 仍然拿得到 |
| C2 | 測試可以重跑，但當時的環境或 fixture 已經消失，是不是其實不可重算？ | 使用者提出 |
| C3 | GREEN 能重跑，但「當時曾 GREEN」和「現在 GREEN」是不是兩個不同的 claim？ | 使用者提出；正式設計 §4.3 已有同一區分 |
| C4 | **由 agent 執行的驗證，重跑不等於重算**：同一份規則、同一批 fixture，兩位 LLM 執行者在同一輪給出不同結果（ID GREEN r1：A 22/22、B 21/22）；而且這個差異本身就是有用的證據（暴露了規則文字歧義） | 本 repo；poc README §3b、§5 Q2 |

由此可知，evidence lifecycle 至少要區分三個概念：**能不能重新執行**、**能不能重新得到同樣結果**、**能不能重新證明當時發生過**。這三件事不是同一件事。

### 5d. 本文的收尾條件

| 審查 | 角色 | 回答的問題 |
|---|---|---|
| Codex 標準文件審查 | **Gate**：決定本文能不能收尾。照 `codex-invocation.md` 首次派發，不帶要攻擊的方向 | 以現在的內容，有沒有事實錯誤、推論斷裂、來源誤用，或會誤導下一步研究的問題 |
| Codex 研究評論 | **Challenge，不是 Gate** | 就算本文沒寫錯，從它選出的下一步方向有沒有框錯問題、漏掉反例、過度概括 |

- 研究評論只對「下一步怎麼研究」提出不同觀點時，不重跑標準審查。
- 研究評論若抓到本文的事實或推論錯誤，導致正文被修改，標準審查就過時了，修改後要重新走一次 doc re-review。
- 標準審查只剩不阻擋的意見時，本文視為第一步收尾，commit 後進入第二步外部研究。
- 2026-10-02 已有的三輪備援審查（contract-neutral-reviewer，✅ Mergeable）只是過程紀錄，不能取代這次的 Codex 獨立審查。

### 5e. 優先序重新評估（2026-10-02，同日稍晚）

> 本節**取代 §5a 把 P2 當「主軸」的排序**；§5a 的三層拆法、研究終點（最後回到 §4.3 vs 2026-09-07 裁定 owner）與 §5b–§5d 不變（§5b 的 OPA 排除後來由 §5f 修改）。觸發：撰寫者自查發現 P2 用來佐證的 RS-5 驗的是 CLI 送達行為、不是下游 agent 的執行行為，P2 的實證強度因此降級（見 P2 推論欄）；而 P3（代理指標對不準宣稱）在三個案例都出現，但證據強度不同：ID 是**實際發生過**的誤判與修復（評分器重複案例漏洞、歸檔結束碼）；RS 是**可展示的假通過路徑**（PRECHECK commit 數）；I2 是報告自己寫明的**宣稱限制**（送達≠遵守），沒有記錄實際把送達當成遵守。

**新的研究分層**（使用者裁定）：

| 層 | 內容 | 對應 pattern |
|---|---|---|
| 1. Claim ↔ Oracle 對齊（最底層） | 不論最後選 TDD、eval、review、diff 或相容性測試，oracle 沒有對準 claim 就會得到假綠燈 | P3 |
| 2. 依受測對象選方法（含 TDD 的邊界） | §5a 的三層：applicability／RED validity／routing | P1、P2 |
| 3. 驗到哪停 | 覆蓋型與收斂型停止條件 | P5 |
| 跨層 | 證據保存與重現（P6）、驗證者特性（P7）、跨表面覆蓋（P8） | P6、P7、P8 |

研究的問題陳述改為：**一個完成宣告，怎麼找到真正分得出真假的 oracle；再依受測對象選方法；並依風險、成本與證據強度決定驗多深。**

**第二步的研究輸入**（不改第一步的對照正文）：

1. **P3 要研究的是「怎麼確保對齊」，不是再證明「要對齊」。** 「先寫 claim、再選分得出真假的 oracle」已記在 memory `feedback_claim_first_discriminating_oracle`；缺口是 §3a 指出的：沒有表面要求每個驗證動作寫出它的 claim。要回答的是「對齊」能不能被檢查、由誰檢查、在哪個 artifact。
2. **「指令送達行為 ≠ agent 執行行為」是 routing 的一個核心區分**：前者便宜、結果固定，字串比對就能驗；後者貴、結果不固定，要讓執行者實際跑。
3. **對照組：下一個案例刻意選一般應用程式的實作改動。** 三案改動的都是這套系統自己的規則、紀錄或基準宣告（I2 雖然執行了上游 CLI，但不是我們改程式）；優先從 workflow-harness repo 已結案、有「需求 → 程式 → 測試 → 審查 → 完成」的真實案例中找，用同一套欄位重拆。塞得自然，框架才可信；塞得笨重，表示框架被規則文字類案例帶偏了。
4. **風險／保障 vs 成本是決策條件，不是證據鏈上的一個節點**：它影響方法要多重、驗多深、要不要第二位評估者、要保存多少 provenance。repo 已有兩個錨點，第二步從它們接起，不另起架構：正式設計 §2.2（保障能力分 required／degradable，可在 proposal 覆寫）決定「要不要」；`auto-loop.md` 的 tier（fast／standard／thorough，security 與 data-integrity 一律 `thorough`）決定「審查要多深」。正式設計已有「依生效契約選驗證方法」的設計責任（§4 開頭）、降級時優先保留同一套程序；**缺的是一條把成本與風險放進去、實際可操作的「claim → 方法」選擇規則**，而且設計責任與已交付的實作要分開看。
5. **停止條件的外部研究以 auto-loop 為基準**：先把它當成既有的審查收斂規則，再看外部方法能補、反駁或解釋什麼。要分清楚：它管的是審查收斂，不是證據深度；它的數值有沒有實測依據，未查證。

### 5f. Codex 研究評論之後的裁定（2026-10-02）

> Codex 研究評論（Challenge，非 Gate）抓到正文 7 處措辭或出處錯誤，已依使用者裁定修正（P1、P4、§3b、I2-5／I2-6 出處、§4 樣本描述、§5e 兩處）；依 §5d，標準審查因此重跑。研究方向類的挑戰記入第二步起點備忘，不改本文。

- **OPA 改為有限度地讀**：Codex 指出 OPA 的政策規則有可執行的測試與覆蓋率報告，正好是「規則文字怎麼測」的成熟先例，落在 §5b 第 1 條線上。範圍只限這一點，不做驗證方法大全。（Codex 引用的 OPA「Policy Testing」文件本文未查證，第二步讀原文時附出處。）
