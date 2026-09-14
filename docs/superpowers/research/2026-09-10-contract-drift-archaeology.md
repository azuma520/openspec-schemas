# Contract drift 三方對照：舊設計考古 × fix-v2 dogfood × 前線觀察（2026-09-10）

> **定位**：分析參考，不是規範、不是提案。回答使用者 2026-09-10 提出的研究題——「如何保留 contract-driven workflow 的可靠性優勢，同時降低多表面同步、語意漂移與 review 返工的成本」——的第一步：把**過去的設計假說**、**這次 `fix-v2-blocking-defects` 真實發生的 finding**、**前線執行 Agent 的觀察**三者並排，看哪些舊構想被支持、被反駁、無法判斷。**不決定格式（XML / YAML / DSL）、不建 dependency graph、不建 contract compiler、不新增 reviewer / gate、不改 routing、不把單次 finding 升成通用規則。**
>
> **路徑解析基準**：凡是 branch `368d586..b07d571` 引入或修改的檔案，一律對 worktree `.claude/worktrees/loosen-plan/`（branch `worktree-loosen-plan`，HEAD `b07d571` + 2026-09-10 未 commit 修正）解析——具體是 `superpowers-bridge/**`（`schema.yaml` 全文、templates、兩份 README）、`openspec/changes/fix-v2-blocking-defects/**`、`openspec/specs/tdd-claim-accuracy/spec.md`、`CLAUDE.md`、`workflow-harness/work-map.jsonl`、`.gitattributes`、`docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/**`、`docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/**`、`.superpowers/sdd/plan/*`；這些檔在 `main` 上或不存在、或內容不同（例：`main` 的 `schema.yaml` 只有 583 行）。`.superpowers/` 為 git-ignored 工作區、teardown 後不可複驗（引用時標「ledger」）。**其餘**路徑——`docs/superpowers/specs/*`、`docs/superpowers/poc/2026-08-28-*`、`poc/2026-09-01-*`、`docs/superpowers/research/2026-09-0{1,9}-*`、`文檔/handoff/*`、repo 根討論檔、`Orca Worktree 模型分析.md`——對 `main`（`98cc5e2`）解析。行號皆為寫作當下實讀。
>
> **方法宣告**：§1 的「舊假說」欄逐條註明來源檔與段落；§2 的每條 finding 註明來自哪份報告；§3 分「觀察事實 / 我的推論 / 我的建議」三段，推論與建議不冒充事實。凡需要工具得到的數字，寫「來源 → 方法 → 結果」。

---

## 0. 範圍與來源清單

**研究對象**：change `fix-v2-blocking-defects`（2026-09-07 開、至今未 archive）在 2026-09-07 → 2026-09-10 之間經歷的審查與修正。**§2 的單位是「分類單位」不是原子 finding**：一列可以合併同一份報告裡同型的數個 finding（例：#31 合併 fallback r1 的 M1/M2，#39 合併九個矩陣缺口，#51 合併三個 Nit），也有報告項目沒有進表（見 §5）。下面的計數是分類單位數，**不是** finding 總數。

| 席位 | 時間 | 載體 | 報告位置 |
|---|---|---|---|
| Codex 外部審（code plane，0907） | 2026-09-07 | `gpt-5.6-sol` | 五 P1 逐條查證見 `brainstorm.md` §已查證依據；handoff 20260907 二 |
| SDD 內部席位（11 review + 4 re-review + 1 whole-branch） | 09-07～08 | Opus subagents | ledger `progress.md`；`docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/review-*.md`、`docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/final-review.md` |
| Codex doc gate（change artifacts 兩批） | 09-07、09-08 | `gpt-5.6-sol` | ledger `progress.md:167-183`；handoff 20260907 四、20260908 四 |
| fallback code gate r1–r4 | 2026-09-08 | contract-neutral-reviewer（Opus） | `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/{codegate-fixes-report,code-rereview-fallback-3}.md`（2026-09-10 自 ledger 逐位元組複製進 repo 路徑，**尚未追蹤**：要等本 change 的 commit 納入版控才算永久；commit 前仍只在 worktree 磁碟）；r1 原報告 `code-review-fallback.md` 僅存 ledger |
| Pilot 2 fallback r1 / r2 | 2026-09-10 | contract-neutral-reviewer（Opus） | `文檔/handoff/attachments/20260910-pilot2/pilot2-fallback-r{1,2}.md` |
| Codex 正式 branch review r1 | 2026-09-10 | `gpt-5.6-sol` high | `文檔/handoff/attachments/20260910-pilot2/pilot2-codex-r1.md` + `-record.md` + `-dispositions.md` |
| 作者自查 / 自傷 | 09-08～10 | 主 Agent | handoff 20260908、20260909、20260910 四【紀律接力】 |

**考古來源**（§1）：`docs/superpowers/specs/2026-08-27-bridge-guarantee-architecture-direction.md`、`docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`、`docs/superpowers/poc/2026-08-28-traceability-gate/poc-report.md`、`docs/superpowers/poc/2026-09-01-capability-spikes/spike-report.md`、`docs/superpowers/research/2026-09-01-plan-structure-comparison.md`、repo 根 `2026-08-27-TDD假保證-第三方審查與改寫建議.md`（未進版控）、`openspec/changes/archive/2026-08-31-fix-tdd-transitive-claim/retrospective.md`、`openspec/changes/loosen-plan/{design,brainstorm}.md`（main 上仍為 active 路徑；worktree 已 archive）、`CLAUDE.md`「跨檔耦合」節、handoff 20260826 / 0902 / 0903 / 0907 / 0908 / 0909、`Orca Worktree 模型分析.md`（43,656 行 ChatGPT 匯出，未進版控）。

**搜尋方法**：`rg -i` 掃全 repo（排除 `node_modules`、`.claude/**`、`openspec/schemas/**`）關鍵字 `reverse depend / backlink / single owner / source of truth / duplicated truth / coupling / 耦合 / 連動 / 反向依賴 / 依賴面 / 單一來源 / 唯一來源 / 重複維護 / impact / 影響面 / derived / drift / 漂移`；ChatGPT 匯出另以 `grep -c` 計數後取上下文。**結果**：`reverse dependency`、`backlink`、`impact analysis` 在全部來源 **0 命中**；`影響面` 2 命中（`superpowers-bridge/README.zh-TW.md:175`、`templates/adopters/CLAUDE.md.fragment.zh-TW.md:32`），皆為設計觸點段落「剩下的 unknown 有明確 owner 與影響面」的用語，不是依賴分析。結論收窄為：**沒有找到正式提出反向依賴圖或影響面分析的來源**，最接近的是下面 H1（人工維護的耦合表）與 H7（介面 pair 表）。`source of truth` / `SSOT` / `唯一來源` 的命中分兩群：(i) ChatGPT 匯出 11 命中與方向文件 §6#5，圍繞 `tasks.md` vs ticket / Linear / Orca 狀態（H4）；(ii) repo 內的 **artifact 級 owner 宣告**——`superpowers-bridge/templates/design.md:20`「design.md 是所有技術決策的唯一來源」、`loosen-plan/design.md:42` 與其 delta spec「tasks.md is the SSOT for applicability」、`CLAUDE.md` dogfooding 節「唯一來源是根目錄的 `superpowers-bridge/`」。(ii) 說明 owner 概念在 artifact 層早就有；**沒有一處把「同一條規則在 check 內文 / 作者指令 / 模板 / spec 之間誰是 owner」講清楚**——這正是 §2 最大宗的邊。

---

## 1. 考古：舊假說 → 當時方案 → 當時缺的證據 → fix-v2 dogfood 的判定

| # | 舊問題／舊假說（來源） | 當時 proposed solution | 當時缺什麼證據 | fix-v2 dogfood：支持 / 反駁 / 無法判斷 |
|---|---|---|---|---|
| H1 | **改一處必連動、CI 抓不到** → `CLAUDE.md`「跨檔耦合」表（2026-08-26，handoff 20260826 二：「最關鍵：version-check.yml 用 grep+awk parse README」） | 人工維護的檔案級連動清單（6 列），放在 CLAUDE.md 每 session 載入 | 沒有證據說明**誰在什麼時候讀它**；假設「動工前必讀」就會被套用 | **對本 change 零命中，且它自己漂了**。耦合表六列的觸發條件分別是：Compatibility 表格式、verify / retrospective 時序或 PRECHECK、artifact 增刪或 `requires:` 邊、新 bridge 目錄、README routing、CLI 名稱（`CLAUDE.md`「跨檔耦合」表，worktree 版）。本 change 改的是 check 的**判定文字**，**六列沒有一列描述這種改動**；Compatibility 那列被 task 3.2 驗證為 byte-identical、沒有動。模板、雙語 README、canonical spec、CLAUDE.md 之所以被更新，是 design D6 與 tasks group 3–4 點名的，不是耦合表指引的——retrospective §1 Wins「the coupled-surface table did its job」把 D6 的連動誤記成耦合表的功勞（本文原稿兩度照抄，兩輪 Codex doc review 各抓到一半）。順帶一個事實：`CLAUDE.md`「Schema 修改流程」第 3 步要求連動「同一個 commit」，而 check 內文在 `cffe99a`、連動表面在 `787b14c`，兩個 commit（`git show --stat` 可驗）。0907 Codex P1-5 幾乎是「耦合表是否被遵守」那條題目的直接產物（handoff 20260909 四）——它抓到的正是耦合表本身寫錯（`v1` vs CI 的 `v2`）。**修 finding 級無效**：2026-09-10 修 r1 finding 時三個新缺陷全是「改 A 忘 B」，其中「改 schema 沒同步 dogfood 副本」是 `CLAUDE.md` **dogfooding 節**（`:150-158`「改完 schema 必須重新同步」）明寫的，**不在耦合表六列內**（`:181-190`）——與下方 §2 分佈觀察對 `orig↔copy`（#46）的歸因一致（handoff 20260910 四）。而且**耦合表自己也漂了**：P1-5 就是耦合表寫 `v1`、CI 已抓 `v2`——維護連動的清單本身是另一個需要連動的表面。 |
| H2 | **唯一來源 + 實體副本**：`superpowers-bridge/` 是唯一來源，`openspec/schemas/` 是 gitignored 副本；symlink 不可行（`CLAUDE.md`「本 repo 自己吃自己的 schema」節） | 「改完 schema 必須重新同步」寫成 CLAUDE.md 規則 + `rm -rf && cp -R` 指令 | 副本失同步的頻率；有沒有比「記得跑」更便宜的偵測 | **支持「副本 = 漂移源」**：失同步至少三次（task 5.1 前、2026-09-10 改 apply 指令每 subject 措辭後 fallback r2 抓到 P1——r2 快照行號 `:1177`、現行工作樹 `:1190-1191`、同日再改一次後我先 `diff -r` 才送審）。**也證明了便宜解**：verify 5.1 的控制從「渲染出新標題」改寫成 `diff -r --strip-trailing-cr` 不變量（`tasks.md:146`），一行指令、零判斷；`rm -rf` 被權限系統擋掉兩次後改覆蓋複製，retrospective §2 明寫等價只在「本 change 沒刪檔」時成立。 |
| H3 | **plan ↔ tasks 兩檔手維護會漂** → 「plan 條目標題 = task 編號 + verify 加計數交叉核對」（`research/2026-09-01-plan-structure-comparison.md` §6；`loosen-plan/design.md` §Risks「1:1 task-number keying + set-equality check … equal counts alone cannot detect a missing-plus-extra」） | 機械 key + 集合相等 | 「集合相等」能不能抓重複——當時沒有 fixture 去問 | **一半反駁一半支持**：0907 P1-1 證明集合相等抓不到重複（f8/f9 在舊文字下 PASS，`tasks.md:60,69`）——原方案不足；但「機械交叉核對便宜有效」被支持：修成兩階段後 check 12 在 verify 兩次重跑都機械得出相同結果，且 PoC 早有同型結論「單一來源不夠，交叉核對才抓得到」（`poc-report.md:50`，M5）。 |
| H4 | **`tasks.md` 是 SSOT，ticket / Linear / Orca 狀態是投影，不是第二個 source of truth**（方向文件 §6#5 拍板 2026-08-28；正式設計 §3.2；ChatGPT 匯出 `:18239`「兩個 Source of Truth 的問題」、`:34079`「外部投影」） | 宣告 owner，其餘載體不得改狀態 | 投影機制未實作，無實證 | **無法判斷 SSOT 主張本身**（fix-v2 沒碰 ticket）。但同型問題在 dogfood 裡出現了：work-map 條目引用 `.superpowers/sdd/plan/` 的報告當「起點證據已備妥」（Pilot 2 r1 P2、Codex r1 P2）——正式設計 §8#7 早已明列「`tasks.md` 之外任何載體與事實同步」為**不保證**項；這次是它第一次以 finding 形式出現。 |
| H5 | **plan 內嵌措辭必漂 vs. global constraints 逐字照抄**：兩條並存的舊決定——(a) `fix-tdd-transitive-claim/retrospective.md:43,88`「plan snippet 隨每輪審查漂移，吃掉兩輪 doc review；寫 plan 時引用 spec requirement 而非內嵌全文」（當時判 One-off、先觀察）；(b) `research/2026-09-01-plan-structure-comparison.md:37-38` 的元素表：第 3 列「Architecture / Tech Stack 移除，plan 只引用不重抄（重抄必漂移）」，**第 4 列「Global Constraints 逐條、原文照抄 → 保留」**，落成 schema plan 指令「Global constraints: copied verbatim from the specs」（`schema.yaml:341-342`） | (a) 引用不重抄；(b) global constraints 刻意逐字照抄，理由是它們是「規定契約」的原型 | (a) 只有一例；(b) 沒有人問過「逐字照抄的那一份會不會漂」 | **(a) 支持且重複（N=2）；(b) 被反駁**：Codex r1 P1——`plan.md:17` 逐字引 spec 第 7 行時**砍掉了「on the same side」限定句**，讓引句比原句更矛盾。這正是 (b) 保留的那一格：規定「原文照抄」沒有阻止照抄時截斷；照抄的一份成了第二個要維護的 truth。這不是「同一批人同一週自相矛盾」（本文原稿的誤讀），而是**當時刻意的取捨被 dogfood 推翻**。 |
| H6 | **「綁出處就能偵測漂移」是假保證**（`2026-08-27-TDD假保證-第三方審查與改寫建議.md` P1-4：檔名行號只給可追溯性，沒有重抓 / 雜湊 / diff job 就不會自行偵測） | 措辭降為「使人工重驗可重現」；候選：擴充 `version-check.yml` 比對「宣稱的那幾句出處還在不在」 | 沒有實證說明「不會自行偵測」實際造成多少返工 | **強烈支持**：0909 research 文件 doc gate 7 輪 🔴 全是「引用與來源對不上」（handoff 20260910 四）；verify.md 的 freshness 規則自己明寫「nothing in this schema detects a stale result」，Codex r1 就抓到 verify.md 過期 P1。候選的「宣稱 vs 出處比對 job」至今沒做，也沒人估過成本。 |
| H7 | **preflight 介面 pair 表漏掉真的耦合缺陷**（handoff 20260903 四：列了 `2.1 ↔ 3.1/4.1/6.2` 標 Clean，「從沒問是什麼讓三個消費者跟生產者一致——答案是沒有任何機械手段」） | 觀察，未提方案 | 一例 | **支持**：0908 一個 change 內「指令改了、耦合表面沒改」復發五次、修被點名實例失敗三次、有效的是規則 × 表面**雙向**矩陣（handoff 20260908 四；retrospective §2 第二條）。矩陣是人工一次性產物，存在 git-ignored ledger 與待 commit 的報告副本裡，**下一個 change 不會自動繼承**。 |
| H8 | **deterministic check ≠ mechanically enforced gate；deterministic 只在 what it decides**（`loosen-plan/design.md` D5；正式設計 §2）。「機械可判」的附屬語法要一開始就定義成機械可判（`poc-report.md:49`） | 用散文把規則寫到「兩個 agent 得同一答案」 | 沒有人拿真實輸入去問「兩個 agent 真的會得同一答案嗎」 | **支持「散文 deterministic 不夠」**：0908「deterministic 差三個宣稱」（retrospective §5：兩行 `subject:`、`###`、`]` 後無空白）；0910 又三個（subject uniqueness 字面、plan key 分隔符、圍籬 / 註解）。**除 subject uniqueness 一條是 spec 措辭（A 類 #52）外，其餘都落在 token 化與 record 文法層**（什麼算一個 token、什麼算一行、什麼算一個 heading、malformed record 怎麼處理），不是語意問題。這是 B 方向最直接的證據基礎。 |
| H9 | **Gate-derived freshness：`FRESH / STALE / CONFLICT`、tree digest 基線 fail-closed**（正式設計 §6、§9 結論表第 4 列）——尚未實作 | Bridge Guarantee 正式實作時做 | 成本未知 | **支持需求、無法判斷成本**：verify.md 過期是 Codex r1 的 P1 之一；review-state 從主目錄記的 digest 為 `null`（看不到 worktree 的樹），提醒功能對這個 change 等於沒綁 digest（Pilot 2 record 第 7 項）。 |
| H10 | **「修 A 順手造 B」8 次**（方向文件 §6#1 拍板依據，2026-08-27 三輪審查）→ G1 雙向（No Silent Loss / No Silent Expansion） | 把它寫成核心保證的定義依據 | 規則寫進 always-on 後有沒有降低復發 | **支持問題存在，反駁「寫成規則會減少」**：復發計數 0907 第五次（handoff 20260907 四）、0908 五次、0910 三次，全在規則 always-on 之後。G1b「silent expansion」在 dogfood 也出現實例：R1 `INDETERMINATE` 放寬在 `e38e817` 落地卻未宣告（Pilot 2 r2 P2、retrospective §3）。 |
| H11 | **兩層 review 的差異在範圍，不在讀法**：0908 的「十一席當散文讀、fallback 當演算法讀」已被 `research/2026-09-09-review-provenance-analysis.md:12` 考古判定**不成立**（內部席位自第一席起就被要求走 fixture）；`:47-48` 的結論是 task-level 抓 task fence 內的 fixture / check 缺陷，change-level 額外抓 fence 外的東西，盲點是「作者表面」不屬任何 task | `:49` 候選：change-level 派工單固定加「這次換掉了哪個假設、列出依賴它的表面」；不動 skill、不加席位 | N=1（0907/0908 一個 change） | **支持範圍說**：2026-09-10 fallback 兩輪後 Codex 仍抓到四條 fallback 沒碰的——兩條在契約面（spec 第 7 行措辭、canonical 缺兩條契約，#52、#56），兩條是 check 內文的 tokenizer 缺口（圍籬、分隔符，#53、#54）；前兩條支持「作者表面 / 契約面不屬任何 task」的範圍說，後兩條說明 fallback 兩輪也沒把 tokenizer 洞掃完；反向 fallback 抓到 Codex 沒機會看的「改 A 忘 B」（修後快照）。**不推論模型優劣**——快照、模板、輪次都不同。 |
| H12 | **Independent Review 降級為 self-review 時 assurance 下降**（正式設計 §5：2026-08-27「語意類缺陷自查命中 0%、外部審 100%」，明寫不得泛化） | degradation record | 不得泛化 | **支持、樣本 +1**：本次「已知缺陷清單」5/5 沒被 Codex 報（severity 依 `pilot2-codex-r1-record.md` 第 6 項：兩條 Nit、一條 Missing-Items 類、一條 0909 Codex 判 Important 的縮排口徑、一條已揭露限制），而作者自查在 0910 三次「已核實」的 CRLF 量測前兩次判錯——**自查的錯比 reviewer 的漏更會靜默累積**（handoff 20260910 四）。 |

**考古小結（事實層）**：過去紀錄裡有 owner 宣告（H2、H4）、有連動清單（H1）、有機械交叉核對（H3）、有「重抄必漂」的原則（H5）、有「出處不會自己偵測」的警告（H6）、有 freshness 的設計（H9）。**沒有的**：反向依賴圖、backlink、影響面分析——沒有一份紀錄正式提出過（關鍵字命中見 §0 的限定）。**最值得看的**在 H5：「global constraints 逐字照抄」是 2026-09-01 刻意保留的決定，這次 dogfood 給了它第一個反例。

---

## 2. finding 分類：七類 × artifact role 邊

**分類鍵**：**A** contract drift / 多表面同步失敗（同一規則在兩個表面說法不一致）· **B** semantic ambiguity / 判定文字本身不精確（單一表面內，兩個執行者可得不同判定）· **C** fix-introduced regression（修 X 時製造的）· **D** verification coverage gap（fixture / 答案表 / 控制沒守到）· **E** evidence lifecycle（證據會消失、紀錄過期、宣告缺席）· **F** measurement / diagnostic error（量測方法或前提錯）· **G** 已知且使用者明確 deferred。一條 finding 可有主類＋次類。

**角色邊**（表面 ↔ 表面）：`spec↔check`（canonical 或 delta spec ↔ schema check 內文）· `check↔author`（同一份 `schema.yaml` 內：check 內文 ↔ tasks / plan 作者指令）· `check↔template`· `check↔README`· `check↔fixture`（含答案表 README）· `canonical↔change`（主 spec / proposal / design ↔ change 實際改動）· `orig↔copy`（來源 bundle ↔ dogfood 副本）· `record`（verify / tasks 控制紀錄 / work-map / errata 等紀錄 ↔ 現況）· `intra`（單一表面內部）· `meta`（CLAUDE.md 耦合表、CI、EOL 等治理面）。

| # | 日期 / 席位 | finding（縮寫） | 主類 | 次類 | 邊 | 修的當下若知道 owner / 依賴能否避免？ |
|---|---|---|---|---|---|---|
| 1 | 0907 Codex P1-1 | check 12 名為 1:1 只驗集合相等 | B | — | intra（名 ↔ 實） | 否——需要反例輸入（f8/f9） |
| 2 | 0907 Codex P1-2 | check 9 `subject:` 只驗非空；check 11 假設一 task 一組 | B | A | check↔spec（evidence 語意） | 否 |
| 3 | 0907 Codex P1-3 | check 7 仍讀 `plan.md`，而 Plan Contract 已讓 plan 無任務列 | A | — | spec↔check | **是**：loosen-plan 改 plan 形狀時，若列出「誰讀 plan.md 的任務列」就會看到 check 7 |
| 4 | 0907 Codex P1-4 | canonical `tdd-claim-accuracy` 同檔兩句互斥（tasks vs plan carrier） | A | G（0904 曾 defer） | intra（canonical） | **是**：改 carrier 時 grep 舊 carrier 名 |
| 5 | 0907 Codex P1-5 | `CLAUDE.md` 耦合表寫 v1、CI 抓 v2 | A | meta | meta（耦合表 ↔ CI） | **是**：耦合表那一列自己就是 Compatibility 表的消費者 |
| 6 | 0907 Codex 附帶 | archive 後三條相對連結 DEAD；README 說 `v2.0.0` tag 已建 | E | — | record | 部分（連結可機械驗） |
| 6a | 0907 Codex P2 | check 7「deferred 任務應連回 plan 條目」建議（使用者裁定 observation） | A | G | spec↔check | 部分 |
| 6b | 0907 Codex P2 | plan producer 未宣告對 `design` / `specs` 的直接依賴 | A | G | intra（schema plan artifact） | 是 |
| 6c | 0907 Codex P2 | `templates/tasks.md` 預填看似完成的證據 | E | G | check↔template | 是 |
| 6d | 0907 Codex P2 | README 的 RED outcome 說明寬於 schema（後於 task 3.2 修） | A | — | check↔README | 是 |
| 7 | 0907 doc r1 | check 7 的 `plan.md` 在四處不是一處（task 文字寫窄） | A | D | check↔check（同一 check 內四處 + freshness 表） | **是**：grep 而非讀 |
| 8 | 0907 doc r1 | plan 介面耦合漏 1.4 與 3.2→5.1 | A | — | canonical↔change（plan Interfaces） | 部分 |
| 9 | 0907 doc r2 | f7 被寫成要 RED/GREEN（它沒有 RED 可拿） | C | D | check↔fixture | 否（語意） |
| 10 | 0907 doc r2 | 5.3 被寫成消費 5.1 的 checker（實只跑 git） | C | — | canonical↔change | 否 |
| 11 | SDD 1.1-1.3 | f11 第二筆 RED 的 failure 長得像 harness error | D | — | check↔fixture | 否 |
| 12 | SDD 2.1 | 改 check 12 後，plan 指令 `:285` 仍把 1:1 定義成集合相等（implementer 自抓、scope 擴一句） | A | — | check↔author | **是**（同檔兩段） |
| 13 | SDD 2.1 review | stage-one 短路與否文字兩處相反 | B | — | intra | 否 |
| 14 | SDD 2.2 | R2 review judgement 文字 under-describe（仍講「比對自己」） | A | — | check↔check（判斷段 ↔ check） | **是** |
| 15 | SDD 2.3 review | controller 前提錯：absent tasks.md 不被 checks 2/8-11 擋（vacuous pass） | F | B | intra | 否——推理錯，需要對讀 |
| 16 | SDD 2.4 | 作者指令三處與 check 不一致（at-least-one、identical char） | A | — | check↔author | **是** |
| 17 | SDD 3.1 | 模板兩處比 schema 窄（`tasks.md:22`、`:36-38` 少 invocation）；`templates/plan.md` 需改但 task 沒點名 | A | — | check↔template | **是** |
| 18 | SDD 4.x | 控制紀錄漏寫第三個 grep | E | — | record | 部分 |
| 19 | SDD whole-branch I1 | `templates/plan.md:21` 仍是「1 對 1」舊字 | A | — | check↔template | **是**（sweep） |
| 20 | 同 I2 | 兩份 README `:386` 仍是單組 cardinality | A | — | check↔README | **是**（sweep） |
| 21 | 同 I3 | tasks 1.1–1.4 未打勾 | E | — | record | 是（機械） |
| 22 | 同 I4 | fixtures README f2 答案表對新 check 過期（依 intent 寫非重推） | D | E | check↔fixture | 否——要重推 |
| 23 | 同 I5 | errata E3 事實錯 | E | — | record | 否 |
| 24 | 同 M1 | check 11 對「無 subject 的 record」收集步驟未定義 | B | — | intra | 否 |
| 25 | 0908 doc Codex | `CLAUDE.md:24` 結構樹說「無 openspec/」與 dogfooding 節矛盾 | A | — | intra（CLAUDE.md） | **是**（grep 自己） |
| 26 | 0908 doc Codex | fixtures README f13 列無法區分新舊行為 | D | — | check↔fixture | 否 |
| 27 | 0908 doc Codex | `CLAUDE.md:111` 三檔不存在——**誤報**（worktree 無 untracked） | F | — | meta（reviewer 環境） | — |
| 28 | fallback r1 I1 | record 兩行 `subject:` 無判定 | B | — | intra | 否 |
| 29 | fallback r1 I2 | plan 指令 SELF-REVIEW 仍只要求集合相等（「第八個未對齊表面」） | A | — | check↔author | **是** |
| 30 | fallback r1 I3 | spec 禁 plan 帶狀態標記、check 7 靠它，但沒有作者表面講 | A | — | spec↔author | **是** |
| 31 | fallback r1 M1 / M2 | `###` 子標題被收；`]` 後無空白 | B | — | intra | 否 |
| 32 | fallback r1 M3 | 訊息模板「occurs twice」vs 規則「more than once」 | B | A | intra | 是 |
| 33 | fallback r2 N1 | 模板未鏡像 FIELD CARDINALITY（第三次「指令改了模板沒改」） | A | **C** | check↔template | **是** |
| 34 | fallback r2 Minor 1/2 | SUBJECT GRAMMAR 對重複 subject；多行值 | B | — | intra | 否 |
| 35 | fallback r3 G1 | one-line-field 規則沒進 tasks 指令 | A | C | check↔author | **是** |
| 36 | fallback r3 G2 | task 編號唯一與 1:1 沒進 tasks 指令——**只有雙向矩陣才看到** | A | — | check↔author | **是**，但單向掃描看不到 |
| 37 | fallback r4 | 第五次復發 `templates/tasks.md:49` 少 FORM-decides 限定 | A | C, G | check↔template | **是** |
| 38 | fallback r4 | D2：check 8「多於一行就擋」作者表面沒說 | A | G | check↔author | 是 |
| 39 | fallback r4 | 九個矩陣缺口（分隔符 D1、空行透明 D4…） | A | G | check↔author / template | 是 |
| 40 | fallback r4 | 三條會擋但無 fixture（`###`、`]` 空白、重複鍵） | D | G | check↔fixture | 否 |
| 41 | Pilot 2 r1 P2 | work-map 引用 teardown 後會消失的 `.superpowers/` 報告 | E | — | record | 部分（知道「非權威載體」原則） |
| 42 | Pilot 2 r1 Nit | 「Shared definitions, used by checks 8-11」實為 8-12 | A | B | intra | 是 |
| 43 | Pilot 2 r1 Nit | delta spec `:9` 少 non-overlapping 掃描規則 | A | — | spec↔check | **是** |
| 44 | Pilot 2 r1 Nit | proposal §Impact 漏 `templates/plan.md` | A | E | canonical↔change | 是（機械：改動檔清單 vs §Impact） |
| 45 | Pilot 2 r1 Nit | 模板兩檔 CRLF→LF 翻轉、其餘六檔仍 CRLF | F | meta | meta（EOL） | 是（`ls-files --eol`） |
| 46 | Pilot 2 r2 P1 | dogfood 副本失同步（我改 apply 指令的每 subject 措辭後；r2 快照行號 `:1177`，現行工作樹 `:1190-1191`） | A | **C** | orig↔copy | **是**（`diff -r`） |
| 47 | Pilot 2 r2 P2 | check 10 對「無 outcome 欄」未定義 | B | — | intra | 否 |
| 48 | Pilot 2 r2 P2 | R1 `INDETERMINATE` 放寬未在 proposal / delta / retro 宣告 | A | C（`e38e817` 引入） | canonical↔change | 部分（改 R1 時列「誰宣告 R1」） |
| 49 | Pilot 2 r2 P2 | `.gitattributes` 萬用字元違反同檔 POC 段理由 | C | A | intra（同檔） | 是（讀同檔） |
| 50 | Pilot 2 r2 P2 | 註解說「釘住即止」但 index 仍 CRLF | C | E | record | 是（`ls-files --eol`） |
| 51 | Pilot 2 r2 Nit ×3 | 84 字元行；check 7 grep exit 2 措辭；四點→五點 | B/F/E | — | intra | 是 |
| 52 | Codex r1 P1 | delta `:7`「unique within a task」字面與前句衝突；`plan.md:17` 逐字引用砍掉限定 | A | B | spec↔check、**spec↔plan（逐字複製）** | **是**（複製即依賴） |
| 53 | Codex r1 P1 | check 7 / 8-12 未排除圍籬與 HTML 註解 | B | G | intra | 否 |
| 54 | Codex r1 P1 | check 12 plan key 無分隔符（`## 1x`） | B | — | intra | 否 |
| 55 | Codex r1 P1 | verify.md 過期；補記插進 `diff -r` 指令中間 | E | **C** | record | 是（freshness 規則已寫；插入位置是編輯錯） |
| 56 | Codex r1 P2 | canonical delta 缺 field cardinality / one-line 兩條契約 | A | — | spec↔check | **是** |
| 57 | Codex r1 P2 | 三條規則無 fixture（design `:124` 要求正負例） | D | G | check↔fixture | 否 |
| 58 | Codex r1 P2 | `templates/tasks.md:49` 續行「不算錯」無限定 | A | G | check↔template | 是 |
| 59 | Codex r1 P2 | D2 | A | G | check↔author | 是 |
| 60 | Codex r1 P2 | work-map 路徑仍指 `.superpowers/`（r1 修了 retrospective 沒修 work-map） | E | C | record | **是**（同一字串的第二個出現處） |
| 61 | 自傷 0908/0909/0910 | `grep -c $'\r'` 每行命中；diffstat +406 是 CRLF；「byte-identical」照抄 reviewer | F | — | meta | 是（先餵一個應該失敗的輸入） |
| 62 | 自傷 0910 | 修 spec 第 7 行時先前的 f14 命名與 retrospective「Candidate f14」撞名（本文作者自查，未加 fixture） | C | — | record | 是 |

**計數**（來源 → 方法 → 結果：上表 66 列 → 以腳本讀表的「主類」與「邊」欄計數 → 結果；一列一主類，斜線分隔者取第一個）：

| 類 | 主類計數 | 備註 |
|---|---|---|
| A 多表面同步失敗 | **32** | 其中 `check↔author`（**同一份 `schema.yaml` 內**）7（加上 `spec↔author` 1 與 author/template 合併列 1，作者面共 9）、`check↔template` 5、`spec↔check` 5、`intra` 4、`canonical↔change` 3、`check↔check` 2、`check↔README` 2、`orig↔copy` 1、`meta` 1 |
| B 判定文字不精確 | **12** | 子型：**lexical / tokenizer** 3（#31 `###` 與 `]`、#53 圍籬、#54 `## 1x`）、**record 文法 / cardinality** 5（#2 subject 只驗非空、#24 無 subject、#28 兩行 subject、#34 重複時的 grammar 與多行值、#47 無 outcome）、**集合邏輯** 1（#1 名稱 1:1 vs 集合相等）、**控制流程** 1（#13 短路與否）、**訊息措辭** 2（#32、#51） |
| C 修正引入（主類） | 5（含次類共 12） | 12 條帶 C 的裡面 **6 條同時是 A**、3 條同時是 E——修正回歸的主要形式是「改了一個表面沒改另一個」與「改了內容沒改紀錄」 |
| D fixture / 答案表缺口 | 5 | 答案表（README）過期 2、缺 fixture 2、fixture 設計 2 |
| E 證據生命週期 | 8 | 紀錄過期 4、非權威載體 2、宣告缺席 1、連結死 1 |
| F 量測 / 前提錯 | 4（自傷另計） | CRLF 三次同一坑；reviewer 環境誤報 1；controller 前提 1 |
| G deferred（次類） | 12 | 主類 A 8、D 2、B 1、E 1（#4、#6a、#6b、#6c、#37、#38、#39、#40、#53、#57、#58、#59） |

**分佈觀察（事實）**：A 類 32 條裡，**同一份 `schema.yaml` 內部的 check 內文 ↔ 作者指令**是最大單一邊（7 條，含 spec↔author 與合併列則 9），第二是 check ↔ 模板（5 條）。`CLAUDE.md` 耦合表是**特定觸發**清單，六列在上表**零命中**：`orig↔copy`（#46）來自 CLAUDE.md 另一節「dogfooding」的同步規則，`meta`（#5）是耦合表本身寫錯；**佔最大宗的兩種邊（同檔內部、check ↔ 模板的逐條規則對應）耦合表根本沒有列**——它列「改 schema 的 artifact 增刪要連動 README」，不列「改 check 9 的一句話要連動 tasks 指令的哪一段」。

**「修的當下若知道依賴能否避免」欄**：66 列裡標「是」或「**是**」的 **40 條**（另 6 條「部分」、1 條誤報不適用），其中 A 29、C 3、E 4、B 2、F 2；標「否」的 **19 條**：B 10、D 5、C 2、E 1、F 1、A 0——分界很乾淨：**依賴知識能救的幾乎全是 A，救不了 B 與 D。**

---

## 3. 前線觀察：十題

每題分**觀察事實**（我做過、看過、量過的）/ **我的推論** / **我的建議**。

### Q1 哪些錯誤最像真正的 multi-surface contract drift？

**事實**：§2 A 類 32 條。最典型的五條：#3（loosen-plan 讓 plan 沒有任務列，check 7 仍讀 plan）、#5（耦合表自己漂）、#33/#35/#37（同一條規則進了 check、沒進指令或模板，連續三輪三個不同 reviewer 各抓一次）、#52（plan 逐字引 spec 砍掉限定句）、#46（dogfood 副本）。

**推論**：這些的共同形狀不是「兩個檔」，是「**同一條規則對三種讀者各說一遍**」——checker（check 內文）、作者（tasks / plan 指令 + 模板 + README）、契約（spec delta → canonical）。三種讀者的表述本來就不能逐字相同（作者要讀得懂，checker 要可判，spec 要 SHALL），所以「不一致」是預設狀態，「一致」要靠人每次重新對齊。

**建議**：先不要把它叫「多表面同步失敗」，叫「**一規則三讀者**」——問題的單位是規則，不是檔案。這個改名影響下一步怎麼量：以規則為列、以讀者為欄，就是 0908 那張矩陣。

### Q2 哪些我們可能歸因錯了？

**事實**：
- B 類 12 條：lexical 3、record 文法 5、集合邏輯 1、控制流程 1、訊息措辭 2（子型與列號見 §2 計數表）。它們常被和 A 類一起講成「drift」，但每一條**只涉及一個表面**、兩個執行者。
- #46 dogfood 副本失同步被記成「耦合型修正錯誤」；它其實是 build artifact 沒重建——與語意無關，`diff -r` 一行就判。
- #55 verify 過期被 Codex 列為 P1 與其他 drift 並排；它是 lifecycle（規則早寫「nothing detects stale」）。
- #61 CRLF 三次是量測工具問題，跟契約無關，但它污染了三次「已核實」判斷與整個 0908 的 diffstat。
- #15 controller 前提錯（vacuous pass）被歸到「reviewer 抓到 controller」，其實是**推理**錯：quantifier 對空集的行為。

**推論**：把 B 混進 A 會讓人以為「同步機制」能解決；實際上 B 的解法是把 token 化規則、record 文法與判定程序寫明（或結構化），跟同步無關。把 #46 / #55 混進 A 會讓人以為要治理，實際上是兩個一行指令。

**建議**：報告與複盤時把 A（多讀者）、B（單表面可判性）、E（過期）三個分開統計。這次 66 個分類單位裡真正需要「人去對齊語意」的 A 大約 20 條；其餘 40 條左右有機械或半機械解（估計，非計數）。

### Q3 哪些 finding 修改當下知道 owner / dependency / coupling 就能提早避免？

**事實**：§2 標「是」的 40 條。其中我自己在 2026-09-10 造成的：#46（改 apply 指令措辭沒 `diff -r`）、#49（沒讀同檔 POC 段）、#50（沒 `ls-files --eol`）、#55（補記插錯位置）、#60（修 retrospective 引用沒修 work-map 同字串）。五條裡四條的「依賴」是**同一字串的其他出現處**或**一條既有指令**，不是什麼圖。

**推論**：這 40 條的共同解不是 dependency graph，是「改一句前先 grep 這句的關鍵名詞，改完再 grep 一次」。0908 ledger `progress.md:158` 已裁定「fix dispatch 結尾必須跨表面 sweep 而非逐檔檢查」——**這條裁定寫在 git-ignored 的 ledger 裡，0910 我修 finding 時它不存在於任何我會讀到的地方**。

**建議**：見 Q10。

### Q4 哪些即使知道 dependency 仍需要 reviewer、fixture 或其他驗證？

**事實**：§2 標「否」的 19 條：B 10、D 5，其餘四條是 C / E / F 語意或推理型（#9 f7 沒 RED、#10 5.3 消費 5.1、#15 前提、#23 errata 事實錯）。發現方式：B 靠「當演算法讀」拿具體輸入去問（fallback r1 三條、Codex r1 兩條）；D 靠重推答案（whole-branch I4、0908 doc f13）；#15 靠對讀 quantifier。

**推論**：這些需要的是**反例構造能力**——「給我一個輸入讓兩個讀法分歧」——這是 reviewer 或 fixture 作者的工作，任何依賴資訊都給不了。B 類裡有五個分類單位是**修完一條後同族再冒一條**（#28 兩行 subject → #24 無 subject → #47 無 outcome → #31 `###` 與 `]`（兩條原子 finding）→ #54 `## 1x`），說明散文修法是逐洞補、補不完。

**建議**：B 類不要再逐條用散文補；集中到 B 方向（§4）一次處理共用定義層與判定程序。D 類保留 reviewer 重推答案表的做法（已證有效三次）。

### Q5 現有機制哪些實際有幫助、哪些沒有、為什麼？

| 機制 | 有幫助的證據 | 沒幫助的證據 | 我的推論：為什麼 |
|---|---|---|---|
| `CLAUDE.md` 耦合表 | 0907 Codex 用它出題抓到 P1-5（表自己的內容錯誤） | 六列對本 change 的改動類型零命中——本 change 的連動全靠 design D6 / tasks 點名；修 finding 級三次失效；表自己漂（P1-5） | 它列的是六種**特定觸發**（Compatibility 格式、PRECHECK、artifact 增刪…），不是「改任何規則文字要連動哪裡」；時機是「開工」與「commit 前」 
| plan.md Interfaces（produces / consumes pair） | 0903 preflight 表形式完整 | 0903 自記「漏了真的耦合」；0907 doc r1 漏 1.4 與 3.2→5.1 | 列的是 task 間的介面，不是規則的讀者；且方向對就標 Clean |
| spec delta（SHALL 條文） | Codex r1 拿它當基準抓 #52、#56 | 本身漂（#43、#56 缺兩條；#4 互斥） | spec 是「應然」，沒人機械比它與 check |
| mutation fixtures + 答案表 | 13/13 兩次獨立重推；f12 正向對照守住 grammar | 答案表過期兩次（I4、f13）；三～四條規則無 fixture | fixture 有效**只在有人重推**時；答案表是第二份 truth |
| verify 決定性 checks | 兩次重跑同結果；0910 我用腳本交叉比對 15 task 一致 | 自己的 freshness 靠人；`grep -c` 陷阱 | 「agent-executed」如宣告：不跑就沒有 |
| `diff -r` dogfood 不變量 | 0910 我改 schema 前先跑，零漏 | 沒跑的那次（#46）就漏 | 一行、零判斷、但要**記得跑**——這是它唯一弱點 |
| 規則 × 表面雙向矩陣 | G2、第五次復發、D2 全靠它 | 存在 ledger（gitignored）；下個 change 不繼承；單向版本有盲點 | 人工、一次性；沒有載體 |
| SDD 內部 review（11 task 席 + 1 whole-branch 席） | per-task 正確性穩定；controller 前提被翻；whole-branch 席抓到五條「範圍寫窄」 | 跨文件矛盾（CLAUDE.md:24）0/11；「改 A 忘 B」全靠下一位 reviewer | task 席的範圍 = task fence（provenance 分析 `:48`）；作者表面不屬任何 task，所以只有 change-level 席位會碰到 |
| 外部 Codex | 跨文件矛盾、範圍寫窄、契約缺條、tokenizer 分歧 | 已知缺陷清單 5/5 未報（兩條 Nit、一條 Missing-Items 類、一條 0909 判 Important 的縮排口徑、一條已揭露限制）；環境誤報 1；額度斷供 3 次 | 貴、慢、但看的是整棵樹 |
| fallback（Opus，contract-neutral） | 拿具體輸入去問 check 文字，抓 B 類三條——**跨三個子型**：record 文法 #28（兩行 `subject:`）、lexical #31（`###` 與 `]` 空白）、訊息措辭 #32（「occurs twice」）；「改 A 忘 B」全抓 | 跨文件契約缺條沒抓 | 差異在派工單給的範圍與具體輸入（provenance 分析 `:12` 已否定「內部席位當散文讀」的說法） |
| review-state / Stop hook | — | digest 對 worktree 為 `null`；只提醒 | 綁主目錄 |

### Q6 從操作成本看，哪種改善最便宜但可能最有價值？

**事實**：本次修正裡最便宜的三件事——`diff -r` 一行（#46 的解）、`ls-files --eol`（#45/#50 的解）、`grep` 關鍵名詞跨 bundle（#7/#19/#20/#33/#35/#60 的解）——各自零判斷、秒級；它們涵蓋 §2「是」欄 40 條中的至少 20 條（估計）。

**推論**：這三件事不需要新機制，需要的是**在修 finding 的那一刻被端到眼前**。0908 已裁定但沒載體，0910 就沒發生。

**建議**：Q10。

### Q7 哪些方案看起來漂亮但會讓治理負擔明顯增加？

**推論**（無實證，明標）：
- **每條規則配 stable ID、所有表面引用 ID**：正式設計為 Requirement 做了（§3.1），對「一規則三讀者」推到句子級會把每份表面變成 ID 森林，且 ID 本身要維護——H1 的「清單自己會漂」會重演一層。
- **dependency graph / backlink registry**：要有人維護節點與邊；邊的正確性又需要審查；沒有消費者（沒有工具讀它）時它就是第四份 truth。
- **Doc role 分類擴充**（0909 提過 research 文件被判成 authority）：多一個分類就多一個要對齊的表面。
- **把矩陣做成永久 artifact 每 change 更新**：25 × 3 的表每改一條規則要動一列三格，比改規則本身貴。

### Q8 Structured representation + decision procedure 對哪些 check 最適合？哪些不值得？

**事實**：§2 B 類 12 條分佈：check 12（#1 名實、#13 短路、#31 `###` 與 `]` 空白、#54 `## 1x`）4 條；check 9/10/11（#2 subject 只驗非空、#24 無 subject、#28 兩行 subject、#34 重複時的 grammar 與多行值、#47 無 outcome）5 條；check 7 / 共用定義（#53 圍籬）1 條；訊息與雜項（#32 訊息模板、#51 84 字元行與 exit 2 措辭）2 條。R1–R4、check 3、check 5 的模糊（✗ 擋不擋、未 commit 是否 FAIL）**不是 tokenizer 問題**，是政策未定。

**推論**：
- **最適合**：checks 8–12 共用的「TASK LINE / BELONGS TO / FIELD / 空行透明 / 縮排」定義層——它已經是一個非正式 tokenizer 加 record 文法，12 條 B 裡 lexical 3 條與 record 文法 5 條（共 8 條）落在它的邊界上；#1（集合邏輯）與 #13（控制流程）是判定程序本身的問題，結構化的「判定」段也涵蓋，但不是 tokenizer；訊息措辭 2 條不需要。把它寫成「輸入 → token 化規則 → record 文法 → 集合運算 → 判定」，散文只留理由。這正是 0908 fallback「當演算法讀」在腦中做的事。
- **check 12 與 check 11**：純集合運算，最容易結構化。
- **不值得**：R1–R4（review judgement，本來就不可判）、check 3 / 5（政策問題，寫一句「✗ 是否 blocking」就解，不需結構）、check 6（ls 一下）。
- **check 7**：值得的只有「什麼算 deferred task line」那一段（與共用定義同一層），其餘是流程。

**建議**：若做 B 方向的實驗，範圍就是「共用定義段」一段，不碰個別 check 的政策文字；拿這次六個真實輸入（兩行 subject、無 subject、`###`、`]1.1`、`## 1x`、圍籬內 `- [x]`）當驗收——結構化後每個都必須得到唯一判定。**不決定載體格式。**

### Q9 Reviewer finding 後，Agent 安全修改目前最缺的是什麼？

**事實**：0910 我的五個自傷（Q3 列）都是在**修 reviewer finding 時**造成，全屬「同一字串的其他出現處 / 一條既有指令沒跑」。0907 第五次、0908 五次同型。當時手邊有的：finding 文字（點名一處）、耦合表（檔案級）、SDD fix-round brief（列 finding）。當時沒有的：這條規則還在哪裡出現的清單；改完後的跨表面 sweep 結果。

**推論**：三個候選裡——dependency awareness / fix pattern / targeted regression——最缺的是**fix pattern**：一個「修一句話」的固定動作序列（改前 grep → 改 → 改後 grep → `diff -r` → 列出改到與沒改到的命中）。dependency awareness 是它的副產品（grep 命中就是依賴清單），targeted regression（fixture 重跑）已存在但只在 reviewer 端跑。

**建議**：Q10。

### Q10 如果只能先試一個最小改動，我選什麼？為什麼？

**我的選擇**：把 0908 已裁定、但只活在 gitignored ledger 裡的那句——「**fix dispatch 結尾必須對每個 bridge-owned 表面做跨表面 sweep，不是再做一次逐檔檢查**」（ledger `progress.md:158`）——當成**派工習慣**在接下來 2–3 次「修 reviewer finding」時實際做，形狀固定為四步：改前 `rg` 該規則的關鍵名詞列命中 → 改 → 改後再 `rg` 一次 → `diff -r` 副本；把兩次命中清單與差異貼進修正報告。試行期只記三個數：做了幾次 / 每次命中幾個表面 / reviewer 下一輪還抓到幾條 A 類。

**為什麼是它**：
1. 它對準 §2 最大宗（A 類 32 條裡 20 條以上可被 grep 命中——估計），且對 C 類主要形式（A+C 6 條、E+C 3 條）直接有效。
2. 成本是四個指令，不新增 Skill、gate、contract、格式。
3. 它已經被裁定過一次而失效——失效原因（載體是 ledger）是可觀察的，試行本身就在回答「為什麼既有機制沒幫上忙」。
4. 它與 Task Context 派工習慣同形（派工單層、不進規則），觀察期可並行、指標可比。

**為什麼不是別的**：B 方向（結構化共用定義層）價值高但是設計工作，不是「最小改動」；dependency graph 是 Q7 的第一項；「修正前先讀耦合表」已證明在修 finding 時機不會發生。

**我不同意的一點**：研究題把 A（多表面）列為第一方向，但從§2 看，**單表面可判性（B）與紀錄過期（E）合計 20 條、且 B 是逐洞補不完的那種**；若只優化 A，下一個 change 仍會有 reviewer 用「當演算法讀」再抓五個同族的洞（§1 H8 列的那五個宣稱：**lexical 4**——`###`、`]` 後空白、plan key 分隔符、圍籬 / 註解；**record 文法 1**——兩行 `subject:`；合稱「tokenizer 洞」並不精確）。建議 A 與 B 平行、E 用既有 freshness 規則 + `diff -r` 類一行指令收。

---

## 4. 三方對照總表（把 §1、§2、§3 疊起來）

| 方向 | 舊假說（§1） | dogfood 證據（§2） | 前線判斷（§3） | 下一個最小實驗候選（**不拍板**） |
|---|---|---|---|---|
| A 多表面 | H1 耦合表（檔案級）、H5 重抄必漂（原則有、schema 反向）、H7 矩陣有效無載體 | A 類 32 條；最大邊在同檔內部（7–9）與模板（5）；「是」欄 40 條 | 問題單位是規則不是檔案；解是 grep-sweep fix pattern，不是圖 | Q10 四步派工習慣，2–3 次修正 |
| B 可判性 | H8 散文 deterministic 不夠；PoC「附屬語法一開始就要機械可判」 | B 類 12 條：lexical 3 + record 文法 5 在共用定義層，集合邏輯 1 + 控制流程 1 在判定程序，訊息 2；同族逐洞補五次仍冒 | 共用定義段一段結構化，其餘不碰 | 拿 Q8 建議的**同一組六個真實輸入**（兩行 subject、無 subject、`###`、`]1.1`、`## 1x`、圍籬內 `- [x]`）當驗收的紙上結構化；範圍同 Q8：只做共用定義段，集合邏輯 1 與控制流程 1 屬判定程序、不在本實驗內（不改 schema） |
| C 修正回歸 | H10 G1 拍板依據 8 次；規則 always-on 後仍復發 | C 類含次類 12 條，6 條同時是 A、3 條同時是 E | 缺的是 fix pattern；規則不擋、動作才擋 | 併入 A 的實驗，指標「reviewer 下一輪抓到幾條 A+C」 |
| D 驗證缺口 | H3 集合相等不夠（P1-1）；fixture-first 有效 | D 類 5 條；答案表過期 2 | 保留 reviewer 重推；無 fixture 規則四條已 defer | 不動（已在 follow-up） |
| E 生命週期 | H4 非權威載體不保證、H6 出處不自偵、H9 freshness 未實作 | E 類 8 條；verify 過期 P1；work-map 路徑 | 一行指令能收的先收；freshness 實作是 Bridge Guarantee 的事 | `diff -r`、`ls-files --eol`、改動檔 vs §Impact 三個一行指令列入 fix pattern |
| F 量測 | H12 自查誤差比 reviewer 漏更會累積 | CRLF 三次、diffstat、前提錯 | 「已核實附方法」已裁定 | 不新增 |
| Review 角色 | H11 兩層差在範圍（task fence vs change-level），不在讀法 | Codex 抓契約與跨文件；fallback 抓 B 類三子型（record 文法 / lexical / 訊息）與改 A 忘 B；task 席抓 fence 內 | 便宜的先排掉（A 類 grep、E 類一行指令），貴的留給契約缺條與跨文件矛盾 | 觀察期繼續記七項 |

---

## 5. 未查證與邊界

- 沒有讀 `.superpowers/sdd/plan/` 的 11 份 per-task review 全文，只讀 ledger 摘要與 whole-branch 報告；§2 #11–#18 的分類依 ledger 一句話判，可能有偏。
- ChatGPT 匯出只做關鍵字取上下文，沒有通讀；「反向依賴圖從未被提出」的宣稱範圍是**關鍵字命中 0**，不是「通讀後確認沒有」。
- §2 的「能否提早避免」是我事後判斷，沒有對照組；標「是」不代表當時的 Agent 真的會去做。
- 計數是一列一主類的人工歸類；換一個人分可能差 ±5。
- §2 不是原子清單：0907 Codex 的五條 P2 以 #6、#6a–#6d 收錄；SDD 各 task 席位的 Minor（ledger 記為「N Minor」而未逐條列出者）沒有進表；#31、#39、#51 各合併多條同型 finding。要當 finding 總數用時，回各份報告數。
- 本文件不含 2026-09-10 Codex 複審（尚未送）的結果；送審後若新增 finding，此表要補。
