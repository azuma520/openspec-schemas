# 審查行為來源分析——「當演算法讀」與 0907 Codex 外部審的考古(2026-09-09)

> 定位:**初步觀察記錄,不是規範、不是提案**。兩輪只讀考古(2026-09-08 晚、2026-09-09)的結論與可回查位置,供 `fix-v2-blocking-defects` 複盤 D1/D4 與後續派工設計引用。
> 所有關鍵判斷附原始 transcript / rollout 位置;凡涉及動機的判斷一律標「推論」。
> 服務的 change:`fix-v2-blocking-defects`(凍結中,未 archive)。
> **路徑解析基準**:本文所有 repo 相對路徑與行號,除非另註,皆對 worktree `.claude/worktrees/loosen-plan/`(branch `worktree-loosen-plan`,2026-09-09 tip `b07d571`)解析;該 branch 落地前在 `main` 上解析不到或會解析到不相干的文字(例:`main` 的 `schema.yaml` 僅 583 行)。裸寫 `schema.yaml` 指 `superpowers-bridge/schema.yaml`;`brainstorm.md` / `design.md` / `proposal.md` / `tasks.md` / `retrospective.md` 指 `openspec/changes/fix-v2-blocking-defects/` 下的檔;handoff 指 `文檔/handoff/` 下的檔(未追蹤)。§2 例外:該節行號對 `02a3385`(`schema.yaml` 最後一次變更的 commit)解析;0907 review 當時的 branch tip 實為 `b2e377e`(rollout `session_meta.git` 的 `commit_hash`;`[1]` 的 `git status --short --branch` 標 `## worktree-loosen-plan`、其 `git log` 首筆即 `b2e377e`),兩個 revision 的 `schema.yaml` blob 相同(`75522885`),行號互通。§5 引用的 plugin 檔以安裝版本為準:sd0x-dev-flow `4.3.1`、superpowers `6.3.0`(plugin cache 升級後行號可能漂移)。

## 0. 三個被推翻或修正的既有紀錄

| 既有紀錄 | 出處 | 考古結果 |
|---|---|---|
| 「十一個內部席位當散文讀,fallback 當演算法讀」 | `session-handoff-20260908.md:146`(「哪一層抓到什麼」)、`retrospective.md:215-216`(§5 Surprises「reading the checks as an algorithm rather than as prose」) | **不成立**。內部審查派工單自第一席(2026-09-07 08:24:32Z,`Review tasks 1.1-1.3 fixtures`)起就要求自己走 fixture(「hand-walking the check text against a fixture」「Walk them」)並回報無法驗證項;第三席(08:51:07Z,`review-21-check12`;第二席為 08:33:15Z `review-14-readme`)起明文「executing only the written steps」、列未決邊界;`review-2.2.md` 開頭自述「every verdict… walking the fixture text against the schema text myself」。差異在**範圍**(task fence vs 整個 change)與明文「as an algorithm」框架,不在散文 vs 演算法 |
| 「五個 P1 一個形狀:名稱宣稱 > 實際斷言」 | 主 Agent 2026-09-08T04:48:59Z 的 Codex 派工單「All five had the same shape」(Claude transcript session `6612dd36`),同一主張以改寫形式進入 fallback 報告 `docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/code-review-fallback.md:8`(「five defects of one shape」);該報告當時**未進版控**,2026-09-14 teardown 前已保存逐位元組副本至上列路徑(原 `.superpowers/sdd/plan/code-review-fallback.md`);Claude transcript 仍未進版控。版控內的 `brainstorm.md:37`、`design.md:17`、`proposal.md:5` 只把該形態套在 P1-1、P1-2(2026-09-09 doc review 抓到本列原標 `brainstorm.md` 為來源,屬誤植,已更正) | Codex 原始輸出(rollout 02:42:42Z 中途訊息)自分**三類**:deterministic 檢查的 cardinality 漏洞(P1-1、P1-2)/ 規範性文件的 v1 殘留(P1-4、P1-5)/ 格式換掉後不可達的舊邏輯(P1-3)。「一個形狀」對 1、2 貼切(與 brainstorm 一致),對 3、4、5 是派工單的事後套用 |
| 「fallback 的演算法派工單是為 fallback 寫的」 | 隱含於 handoff | 同一份文本先於 04:48:59Z 派給 Codex,04:52 配額耗盡後幾乎原文轉派 fallback(同結構、同六個審查維度、`## Review it as an algorithm` 的標題與六個維度順序相同,但該節每一句都經壓縮改寫、無一句逐字相同——2026-09-09 實測兩份 prompt 該節 10 行僅標題行相同;差異約二十處 hunk:包裝句、逐句壓縮改寫、「eleven internal review seats」一句、以及要求先落檔的段落) |

## 1. 「當演算法讀」的來源分類

分類圖例:**A** skill 層本來就有 / **B** 上位規則(全域或專案 CLAUDE.md、rules),派工單只是把它重述或套到具體檔案上仍算 B / **C** 主 Agent 派工單新增了上位規則沒有的措辭或操作(例如「as an algorithm」框架、邊界清單)/ **D** reviewer 自構、派工未要求 / **E** 多來源共同形成(無單一來源)。「E 偏 C」表示多來源,但明文措辭主要來自派工單。

| 行為 | 分類 | 依據(可回查) |
|---|---|---|
| 不只信規則名稱,看它實際判定什麼 | **B**(上位規則,主 Agent 具體化) | `~/.claude/CLAUDE.md:30` 複審紀律;內部派工 `review-21-check12`(session `6612dd36` 2026-09-07T08:51Z)「would a reader executing only the written steps reach the verdict the title promises?」 |
| 當演算法逐步重推 | **E 偏 C** | 題材:`schema.yaml:548` 自述 DETERMINISTIC;操作化:上述內部派工(C);明文「Review it as an algorithm / two competent executors」:Codex 派工 2026-09-08T04:48:59Z(C)。skill 層無此語言 |
| 主動構造反例 | **E** | 全域規則「絕對斷言前先找反例」(`CLAUDE.md:23`);專案 mutation fixtures(`docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md:20`);派工邊界清單(C);清單外的 I1/M1/M2 是 reviewer 自構(D) |
| 自己重做判定 | **E** | 使用者裁定 2026-09-07T07:04Z(session `9a608a2e`)→ `tasks.md` 前言;派工 self-application(C);把 check 實作成腳本跑 fixture 是 fallback reviewer 自選(subagent `agent-afallback-code-review-f42671c3263cd082` tool 13–15)(D) |
| 純 A(skill 本來就有) | 無 | `contract-neutral-reviewer.md`、`codex-prompt-fast.md`、`review-common.md`、SDD `task-reviewer-prompt.md` 只提供獨立研究 / 別信報告 / 「boundary conditions」一詞 |

fallback 第一輪三個 Important 的性質:I3 跨表面(對象是 change 自己的 delta spec,落在 task fence 外、final-review 六表面清單外);I2 **在範圍內仍漏**——其表面(`schema.yaml` 的 `plan` 指令 SELF-REVIEW)與主張(check 12 兩階段)都在 final-review 派工單(2026-09-08T02:44:13Z)第 1 項「six places / load-bearing claims」清單上,該席仍未抓到;I1 清單外反例。**只有一個可由範圍差解釋(I3),一個是範圍到位仍漏(I2),一個由反例構造解釋(I1)**——範圍差對 D4 的解釋力比原先寫的弱;這是「變數是提問方式不是模型」的相關性證據,非因果。fallback 的 27 個 thinking 區塊全空,reviewer 為何想到 I1 不可回查。

## 2. 0907 Codex 外部審重建

(本節 `schema.yaml:N` 行號皆對 `02a3385` 解析——那是 `schema.yaml` 最後一次變更的 commit,不是 0907 review 當時的 branch tip;當時 tip 是 `b2e377e`(rollout `session_meta.git` 的 `commit_hash`;`[1]` 的 `git log` 首筆同;`[30]` 的 decorated log 亦標 `b2e377e (HEAD -> worktree-loosen-plan)`),兩者 `schema.yaml` blob 相同,行號互通;與 §1 / §5 引用的現行 tip 不同。)原始資料:`~/.codex/sessions/2026/09/07/rollout-2026-09-07T10-27-53-01a079b1-8828-7202-9bb8-817ea1a4d59f.jsonl`(48 次工具呼叫 `[n]`、5 段中途訊息 + 1 份最終報告(02:46:00Z)、69 個 reasoning **全加密無摘要**)。Claude 側:project dir `C--Users-user-orca-openspec-schemas--claude-worktrees-loosen-plan`,session `c8bf3e6a`,派工 02:27:52Z。模型 `gpt-5.6-sol` / effort high / read-only。

**Prompt 來歷**:主 Agent 派工前**沒有**呼叫任何 review skill(該 session 的 Skill 呼叫只有 01:05Z `work-status`,派工後為 `backlog-triage`、`smart-commit`,皆與 review 無關)、沒有讀任何 `codex-prompt-*.md`。骨架來自 `.claude/rules/codex-invocation.md`(獨立研究、不餵結論),「What to look for」七條是主 Agent 把 repo `CLAUDE.md`(耦合表、紅旗、version-check grep、兩個版本號)翻成題目。prompt 有跨表面比對提示、無程序推演 / 反例 / 重跑提示。

**Codex 實際順序**:`[1]` 自寫五步計畫 + git 盤點 → `[7]` 全文讀 CLAUDE.md → `[8]` schema diff(截斷)→ `[9]–[11]` 改讀 schema 全文 → 02:30:36Z 自述「行為轉移已清楚,現在找每一個舊 plan 形狀假設的殘留」→ `[12]` 讀模板 → 02:32:52Z 找到 check 7(P1-3)→ `[21]–[23]` 讀六份 spec + 一條 rg 同時掃殘留用語與 `[~]`(P1-4)→ `[36]` 重現 CI grep/awk(P1-5)→ `[45]` blame 溯源(`[44]` 為 update_plan 宣告) → `[47]` 程式數 plan 模板 checkbox(base 2 / HEAD 0)→ 報告。

**五個 P1 的關係**:P1-3 → P1-4 有明確擴散鏈;P1-5 獨立;P1-1、P1-2 同在 `[10]` 讀到,無可見擴散動作,反例只出現在報告文字、未執行。「testing against fixtures」(02:32:52Z 自述)在工具紀錄裡是**閱讀** `[35]`,不是執行。

**有證據的 pattern**:由宣稱反查(P1-1/2 措辭;`[47]` 量測)、跨文件一致性(prompt 明列)、producer/consumer 對讀(`:205` 對 `:486`;自選)、找舊假設殘留(自述策略;自選)、沿 finding 擴散(`[22]` 單一 rg;自選,限殘留類)、溯源(prompt 要求)。無證據:執行式程序推演。

**H1–H4**:H1 跨邊界——中(策略自述一致,但 prompt 與 diff 本就跨表面);H2 宣稱反查——弱到中(鏡頭由 prompt 給);H3 擴散——強(限殘留類)/ 無(限決定性檢查類);H4 模型 vs prompt——**單次資料不能判斷**,無對照組。

## 3. 觀察者判斷(非規範)

- **最高價值習慣**:先問「這次改動換掉了哪個結構性假設」,再找哪些層沒跟上;其次是「宣稱能量就量」(三次自選量測全命中)。
- **兩層分工**:方向合理、邊界錯位。task-level 的價值在「證據真不真」,change-level 在「結構換了誰沒跟上」;目前 task-level 也被要求走 fixture / 邊界,與 change-level 重做。盲點是「作者表面」(模板、SELF-REVIEW、delta spec SHALL NOT)不屬任何 task。
- **低 ROI 區**:純文件 task 的 review + re-review 雙席位,本 change 對 blocking finding 貢獻為零。fixture / 檢查類 task-level review 則有貢獻:`docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/review-1.1-1.3.md:45-83`、`docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/review-2.1.md:44-73`、`docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/review-2.3.md:141-197` 各有 Important 發現且 task verdict 為 `Needs fixes`。兩層的差異在**範圍**(同 §0 考古結果):task-level 抓 task fence 內的 fixture / check 缺陷;change-level 額外抓到 fence 外的東西——跨表面依賴、舊假設殘留、final-review 表面清單外的對象(§2 的 P1-3/P1-4、fallback 第一輪 I3)。原先「全部 blocking finding 來自三個 change-level 席位」是過度概括,已由上列三份 task review 記錄反駁。
- **最小改善候選**(尚未拍板):change-level 派工單固定加「這次換掉了哪個假設、列出依賴它的表面」一句;不動 skill、不加席位。理由:最有效的 prompt 沒經過 skill;fallback 與內部席位同模型。
- **保留觀察的三個 pattern**:①換掉假設 → 找殘留(觀察非換形狀 change 會不會空轉);②作者表面與檢查器對讀(觀察寫進派工後內部席位能否抓到 I2/I3 類;注意 I2 的表面已在 final-review 派工單上仍漏,單靠列表面不夠,可能還需要「對讀」這個動作本身被點名);③宣稱能量就量(觀察命中率是否維持)。

## 4. 待更正的既有紀錄(下個 session)

- `retrospective.md:215-216`(§5 Surprises,「reading the checks as an algorithm rather than as prose」)與 `session-handoff-20260908.md:146-147`(§四【當日洞見】第 1、2 條,「哪一層抓到什麼」「當散文讀」):改為「差在範圍與明文框架」。
- D1/D4 複盤若以「名稱大於斷言」為前提,前提先改為 Codex 的三類分組。

## 5. 既有 review 能力對照與結論(2026-09-09 第二輪,使用者裁定)

> 問題:我們是不是已經有現成的 review 能力,只是這次沒有正確使用?以下對照結果為唯讀盤點,原文位置皆可回查;裁定由使用者於 2026-09-09 作出(Claude session `133797d7`,使用者訊息 `2026-09-09T01:46:32Z`:「先別造新的 Review 系統……優先問題是既有 Skill 沒走正常路徑……透過現成 FOCUS 先試用」;其後發現 branch 模板無 `FOCUS` 而改列 A/B 替代方案,是審查修正、不是該裁定的一部分)。

### 5.1 裁定

**先不造新的 review 系統。** 現有 SDD 兩層審(task reviewer + whole-branch reviewer)加 sd0x Codex review skill 已覆蓋大部分架構。優先順序:①修 invocation——change-level 外部審走 `/codex-review-branch`、loop 內走 `/codex-review-fast`,不再由主 Agent 自組 prompt 直呼 MCP;②實戰新冒出的高價值題目(見 5.4)先用模板既有的槽試用、不改 skill——**但同日 doc review 查證:`FOCUS` 槽只存在於 fast / full 模板(`codex-prompt-fast.md:22`、`codex-prompt-full.md:25`),branch 模板沒有;而 fast / full 的 baseline 是 `git diff HEAD`(僅未 commit 改動,`codex-code-review/SKILL.md:77`),審不到已 commit 的分支。change-level 外部審目前沒有任何路徑能同時保留 skill 契約又裝下這些題目。** 【待裁定】兩條路:A. 小幅補 skill——在 branch 模板加同形的 `${FOCUS}` 一行(plugin cache 內改動會被更新覆蓋,正式做法是上游 PR 或專案層 override);B. 走 `/codex-review-branch` 流程(baseline、tier、gate 全保留),prompt 在模板後附加一段 Focus Area(等於局部自組,但契約不丟);③在 A/B 拍板前 skill 本體不改;④兩個反向限制(5.3 的 D 列)只觀察、等實例。

### 5.2 「該走 skill 卻繞過」的查證(2026-09-07 外部審)

| 層 | 內容 | 出處 |
|---|---|---|
| 明文設計 | code 檔改完走 `/codex-review-fast`;branch 級走 `/codex-review-branch`(tier 自動 thorough、P2 擋);prompt 用 references 模板、不臨場自組 | `.claude/CLAUDE.md:12`、`:34`;`codex-review-fast/SKILL.md:34`;`codex-review-branch/SKILL.md:25`(thorough);`rules/codex-invocation.md`「Use the prompt template from @skills/*/references/ rather than composing one ad hoc」 |
| 實際執行 | 主 Agent 02:16:33Z 自建任務寫「走 /codex-review-branch」;02:17:59Z「照規矩只給中繼資料」後直接 `mcp__codex__codex`(02:18:15Z 撞配額,02:27:52Z 同 prompt 重派)。全程零 review skill 呼叫(`codex-review-branch` / `codex-code-review` 皆未 invoke;session 內僅有 `work-status`、`backlog-triage`、`smart-commit` 三次無關 Skill 呼叫)、零讀取 `codex-prompt-*.md` / `review-common.md` | Claude transcript `c8bf3e6a`(worktree project dir) |
| 差異 | 少:凍結 baseline、tier 解析(prompt 自寫「no P0/P1 → Ready」等於 standard,branch 應為 thorough)、scope 四欄位、gate_reason、verdict 落 review-state。多:七條 repo 特定題目(耦合表、紅旗、CI grep 形狀、版本號、「被 repo 自己反駁的宣稱」),模板只有 `FOCUS` 一行能裝 | 同上;`codex-prompt-fast.md:22` |
| 為什麼(全為 hypothesis,thinking 區塊皆空) | H-a(有文字支撐):「照規矩」照的是 always-on 的 `codex-invocation.md`,skill 本體要 invoke 才載入,規則比 skill 近一跳。H-b:動手時是「載入工具」而非「載入 skill」。H-c:repo 無 src/,模板 research 指令看似不合用——transcript 無此陳述,純推測 | — |
| 累積 | 09-08T04:48Z 的 schema 審同形態(直接 MCP、自組 prompt)。N=2,是 pattern 非單次 | session `6612dd36` |

結論:這不是「skill 沒價值」,是「skill 被繞過」;但繞過同時暴露「模板裝不下 repo 特定題目」這個真缺口,兩件事分開記。

### 5.3 九項實戰 pattern 對既有 skill / rule 的分類

A 已明文 / B 原則有但不具體 / C 沒有 / D 現有規則會限制。

| pattern | 分類 | 原文位置 |
|---|---|---|
| 程序推演(照 PASS/BLOCK 文字走一次) | sd0x 模板 C;全域規則 B | 全域 `CLAUDE.md:30`(寫給我方非 reviewer);SDD `task-reviewer-prompt.md:64-71`「Do Not Trust the Report」;明文「as an algorithm」只在 09-08 派工單 |
| change 換掉了什麼核心假設 | B(弱) | branch prompt `:57-58`「main purpose of this branch」;`code-reviewer.md:73-74`「Migration strategy if schema changed」;無處要求先命名假設 |
| 找舊假設殘留 | sd0x C;全域 B;scope 規則 **D** | 全域 `:29`(抓到後掃同類);專案 CLAUDE.md 耦合表(已知殘留點)。D:`scope-discipline.md` § Scope Determination「非程式檔條件 2 永遠為否」→ 本 repo 未觸碰檔案裡的殘留必然 out-of-scope、非 critical 不擋。Codex 內建 `review-agent:32`「It was introduced by the reviewed change」為必要條件(未啟用,潛在 D) |
| producer / consumer 對讀 | B | SDD `task-reviewer-prompt.md:48-50`(contract 改了查 call sites);branch prompt `:54`;全域 `:23`(作者側);09-08 派工單「Interface agreement 雙向」為 C |
| change-level 跨邊界一致性 | 專案層 A;skill 層 B | 專案 CLAUDE.md 耦合表;SDD `SKILL.md:8`、`task-reviewer-prompt.md:17-19`;`code-reviewer.md:64`;branch prompt `:64-67` |
| finding 後搜同類 | 全域 A;模板 B | 全域 `:29`(寫給修的一方);fast prompt `:69` Gap check;`review-agent:17-18`「Continue through the whole diff after finding the first issue」(只要求讀完整個 diff,不要求搜同形缺陷) |
| self-application | reviewer 側 C;流程側 B | 只在 09-08 派工單;verify artifact 本就對 change 自己跑 checks 8-12(`schema.yaml:1184-1188`),但那是 verify agent |
| 能量就量 | 作者側 A;SDD reviewer 側 **D** | `verification-before-completion:14-35`、全域 `:14`、`:23`。D:`task-reviewer-prompt.md:73-82`「Do not re-run the suite ... recommend it instead」;fast prompt `:65` 要的是 file:line 引文,是讀不是量 |
| 反例 / boundary case | 作者側 A;reviewer 側 B | 全域 `:23`、`:30`;fixtures README:20;模板僅 `codex-prompt-fast.md:56`「boundary conditions」一詞;邊界清單只在 09-08 派工單 |

相似構想:「局部深審 + change-level 整合審」是 SDD **原文要求**(`SKILL.md:8`、`task-reviewer-prompt.md:17-19`、`re-review-prompt.md:60-62`、`schema.yaml:1197-1201`),差在 whole-branch 模板是通用 checklist、無整合視角題目;「先命名被換假設再沿依賴找殘留」只能從 `task-reviewer-prompt.md:48-50` + 全域 `:29` **合理推導**,無處要求該順序。

### 5.4 待 5.1 A/B 拍板後試用的題目(承載方式未定,不改 skill)

1. 本次改動換掉了哪個結構性假設;列出依賴它的每個表面,逐一查有沒有跟上。
2. 專案 CLAUDE.md 耦合表與紅旗表是否被遵守;CI grep 形狀是否仍成立。
3. self-application:change 自己的 tasks.md / plan.md 對新檢查是否通過。
4. 任何被 repo 自己反駁的宣稱。

單次證據(非規律):2026-09-09 code plane 補審把題目 1 加進派工單,Codex 的表面清單直接命中 `schema.yaml:1177` apply 指令殘留的單一對措辭。該句 fallback 曾以 grep 宣稱零命中——原文在 1177/1178 行間換行,單行 grep 掃不到;是「範圍化 grep 被當完整掃描」的量測工具版。

### 5.5 未查

0907 有無執行 `review-state.js note`;`pr-review-toolkit` plugin 是否安裝;Codex 端 `~/.codex/skills/` 在 MCP session 是否自動載入(僅確認 0907 rollout 無 skill 載入呼叫;文字命中 9 處未逐一辨源)。
