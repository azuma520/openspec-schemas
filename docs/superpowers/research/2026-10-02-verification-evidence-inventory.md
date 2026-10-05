# Verification Strategy 第二步：內部證據盤點表（2026-10-02）

> **定位**：分析參考，不是規範、不是研究結論。這是 work-map `task-20261002-vs-step2-evidence-inventory` 的產出，依起點備忘 `./2026-10-02-verification-strategy-step2-starting-memo.md` §6 的欄位與記錄規則，把 repo 裡已有的驗證紀錄整理成表。**在讀任何外部資料之前做**（研究程序裁定）。
>
> **目的**（照抄備忘 §6）：盤點的目的不是比較哪個審查者比較強，而是辨識每一層驗證對最終交付可靠度提供了哪些不可替代、或與其他層重複的增量價值。
>
> **記錄規則**（照備忘 §6）：缺的成本資料標「未知」，不估；區分**首次發現**與**重新發現**；「增量價值」只寫成**觀察到的額外偵測**，因果結論留給有對照的比較；contract drift 研究的計數是分類單位，不是原始 finding 總數；**不算 ROI、不排審查者名次**。不同快照、範圍、輪次的比較都要標明。
>
> **欄位怎麼放**：備忘 §6 的十個欄位分成兩張表——**層表**（每個驗證層一列：驗證層／方法、claim／oracle、執行者與強制機制、成本 proxy、受測快照、已知漏抓）與 **finding 表**（每個 finding 一列：嚴重度、首次／重新發現、前一層是否已漏過、如果沒抓到會怎樣）。「抓到的 finding」欄在層表裡以 finding 編號指過去。**「如果沒抓到會怎樣」一律是推論**，不是事實。嚴重度照來源原本的標法（🔴／🟡、P0–P2、Important／Minor），不換算。

---

## 0. 資料來源與完整性

備忘 §6 要求開工前先確認來源是否齊全。結果：**每個案例都有一部分原始審查報告已經不存在**，只剩摘要。這本身就是 P6「證據壽命比宣告短」的又一個實例（見 §3 O6）。

| 代號 | 案例 | 讀了什麼 | 還在嗎 | 缺什麼 |
|---|---|---|---|---|
| **CD** | `fix-v2-blocking-defects`（2026-09-07～10） | `./2026-09-10-contract-drift-archaeology.md` 全文 | 研究文件在 repo | §2 是 66 個**分類單位**（一列可合併多條 finding；SDD 各 task 席的 Minor 沒進表，見該文 §5）；本文只做**按席位彙總**，沒回各份原始報告數原子 finding |
| **ID** | `requirement-scenario-identity`（2026-09-29～10-01） | archive 的 `retrospective.md` 全文；`docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/sdd-ledger.md` 全文（126 行，append-only，已進 repo） | ledger 與 retrospective 在 repo | 全分支總審 r1 報告「kept in session scratchpad」（ledger 第 111 行），已不存在；各 task 審查報告、fallback 文件審報告原文都不在 repo，只有 ledger 一行摘要；task 1.1 fixture 審查（strict-reviewer 兩輪）的 finding 內容 ledger 沒記 |
| **RS** | `retro-skill-inventory`（2026-10-02） | archive 的 `retrospective.md`、`apply-evidence.md` 全文；handoff 2026-10-02 07:58／09:58／15:20 區塊 | retrospective、apply-evidence、handoff 在 repo | **SDD ledger 與 batch 報告隨 worktree 移除已消失**（RS retrospective §0 事先寫明；`C:/Users/user/orca/workspaces/openspec-schemas/`（repo 外）2026-10-02 實查為空）；fallback 文件審 4 輪報告存於 session scratchpad、已不存在（RS retrospective §2 轉述） |
| **I2** | issue #2 上游相容性 spike（2026-10-02） | `docs/superpowers/poc/2026-10-02-issue2-compat-spike/report.md`（grep 定位後讀相關段）；handoff 15:20 區塊 | report 在 repo | Codex 文件審 2 批的報告原文不在 repo，只有 handoff 一句摘要；thread id 未記錄 |
| **VS1** | Verification Strategy 第一步對照文件（2026-10-02） | `./2026-10-02-verification-strategy-case-crosswalk.md` §5d、§5e、§5f；handoff 17:46 區塊 | 文件與 handoff 在 repo | fallback 3 輪、Codex 標準審查、Codex 研究評論的報告原文都在 session scratchpad，已不存在；「研究評論抓到 7 處」的逐條內容只剩 §5f 一句列舉 |
| **VS2** | 本 session：第二步備忘＋`.gitignore` 退役＋產品承諾比對（2026-10-02） | 本 session 對話中的審查報告與 agent 回報（第一手） | 報告檔已依 `CLAUDE.md` 清理規則刪除；結論在本表與備忘 §8、commit `3cc1ad2`、`65c2ee4` | 只有本表這份轉述 |

**沒有納入的**：`loosen-plan`、`fix-tdd-transitive-claim`、`fix-v2-blocking-defects` 三個已 archive change 的 retrospective（CD 列讀的是研究文件，不是 fix-v2 的 retrospective）；備忘 §7 的「對照組」（workflow-harness 一般程式案例）留到後面。

---

## 1. 層表

### 1a. CD — fix-v2（按席位彙總 CD §2）

CD §2 的 66 個分類單位依「日期／席位」欄歸到 9 個席位（腳本讀表，一列一席位；`同 I2`～`同 M1` 歸全分支總審）。「能否避免」是 CD 的欄位「修的當下若知道 owner／依賴能否避免」，是 CD 作者的事後判斷。

**claim／oracle 與執行者、強制機制**：CD §0 只記各席位的載體與模型（例：Codex `gpt-5.6-sol`、Opus subagent、contract-neutral-reviewer），沒有記各席位要證明什麼、怎麼觀察、靠什麼保證真的跑了；本表這兩欄對 CD 一律視為**未知**，不從載體推。

| 席位 | 單位數 | 主類（A 多表面／B 可判性／C 修正引入／D fixture／E 生命週期／F 量測） | 能否避免：是／部分／否 | 成本 proxy | 已知漏抓與增量（CD 原文） |
|---|---|---|---|---|---|
| Codex 外部審 0907（code） | 10 | A 6、B 2、E 2 | 6／2／2 | 未知（額度斷供 3 次，CD Q5） | —（CD 沒有這一席的漏抓紀錄） |
| Codex doc gate 0907 | 4 | A 2、C 2 | 1／1／2 | 未知 | — |
| SDD task 席（11 review＋4 re-review） | 8 | A 4、B 1、D 1、E 1、F 1 | 4／1／3 | 15 次派工（CD §0） | 跨文件矛盾（`CLAUDE.md:24`）0/11（CD Q5）；task 席範圍＝task fence（CD H11） |
| SDD 全分支總審 | 6 | A 2、E 2、B 1、D 1 | 3／0／3 | 1 次派工 | 抓到五條「範圍寫窄」（CD Q5） |
| Codex doc gate 0908 | 3 | A 1、D 1、F 1 | 1／0／1（1 條誤報） | 未知 | 1 條是 reviewer 環境誤報（#27） |
| fallback code gate r1–r4 | 13 | A 8、B 4、D 1 | 9／0／4 | 4 輪 | 「改 A 忘 B」全抓；跨文件契約缺條沒抓（CD Q5）；G2 只有雙向矩陣才看到（#36） |
| Pilot 2 fallback r1／r2 | 11 | A 5、B 2、C 2、E 1、F 1 | 8／2／1 | 2 輪 | 之後 Codex 0910 仍抓到 4 條 fallback 沒碰的（CD H11） |
| Codex branch review 0910 | 9 | A 4、B 2、E 2、D 1 | 6／0／3 | 1 輪 | 作者事先列的已知缺陷 5/5 沒報（CD H12）；9 條中 4 條帶 G（deferred）標記，是重新發現（見 F 表註） |
| 作者自查／自傷 | 2 | F 1、C 1 | 2／0／0 | — | 這兩條是作者**製造**的錯，不是偵測；CRLF 量測前兩次「已核實」判錯（CD H12） |

**受測快照**：各席位審的快照不同（0907 起點 → 0908 修正後 → 0910 修正後），CD H11 明寫「不推論模型優劣——快照、模板、輪次都不同」。

### 1b. ID — requirement-scenario-identity

| 層 | claim／oracle | 執行者與強制機制 | 成本 proxy | 受測快照 | 抓到的 finding | 已知漏抓 |
|---|---|---|---|---|---|---|
| L-ID1 fixture 審查（task 1.1 偏離 SDD 的補救） | fixture 與突變說明正確／審查者讀檔判斷 | strict-reviewer；使用者裁定 3A 指定 | 2 輪 | task 1.1 產出 | 內容未記錄（ledger 第 8 行只記 ✅ Ready r2；第 19 行提到 reviewer F6） | 未知 |
| L-ID2 SDD task 審查與 re-review | 每個 task 符合 spec 與 plan／審查者讀 diff 判斷 | Opus／fable subagent；SDD skill 結構性派工，agent 照 skill 執行 | 派工次數【未精確計數】（ID retrospective §0） | 各 task 未 commit 的工作樹 | F-ID1～F-ID4、F-ID6、F-ID7；另 deferred minor 至少 15 條（ledger 第 36～107 行） | check 13 的 I3 互斥句（fix round 2–3 引入）→ F-ID12 |
| L-ID3 controller 實測（probe） | 規則文字對 CLI 行為的描述為真／實際跑 CLI | 主 session；無強制，視情況做 | 未知 | CLI 1.3.1 | F-ID5（觸發來源：re-reviewer 的範圍外附註）；歸檔中止仍回 exit 0、stderr 警告（ID retrospective §5） | — |
| L-ID4 盲測執行者 | 規則文字**可被一致執行**、新規則抓得到且不誤擋／22 個凍結 fixture＋預期答案表，最終判定與 BLOCK 類別集合都要相同 | 無脈絡 sonnet subagent；凍結器材、`grade.py` 評分，執行者「不讀 repo」只靠指示（ledger 第 43 行） | 11 次派工（ID retrospective §0）；每次執行者 run 約 20 分鐘（ledger 第 73 行的事前估計，不是實測耗時） | RED：`42c3d24` 的規則；GREEN：四輪、三版規則文字（r1 `7e9fbca1…`；r2 與 v2 同為 `f2eea915…`，v2 只修器材；v3 `a78e207c…`；ledger 第 71、76、87、120 行） | F-ID8、F-ID9 | 22 題沒有一題觸發 I3 分支（ID-7）；執行者 A 兩輪都 22/22，兩個問題都只由 B 暴露 |
| L-ID5 評分器自測與試跑 | 評分器分得出每條錯誤路徑／`grade.py --selftest`；I3 定點驗收前用假報告試跑 | 主 session；selftest 是腳本，試跑是使用者裁定後才做 | selftest 16 項 | `grade.py` 各版 | I3 試跑：兩條錯誤路徑都回 DIFF、全對的假報告回 MATCH 2（ledger 第 123 行；無 finding） | 「同一案例出現兩次」不在 selftest → F-ID11 |
| L-ID6 SDD 全分支總審 r1／r2 | 整個分支一致、可交付／審查者讀全範圍 | general-purpose reviewer（fable）；SDD skill 結構性派工 | 2 輪 | `42c3d24..2bc8a56`，r2 為修正後 | F-ID10a～d；r1 另 7 Minor、r2 3 Minor；找到 5.2 空白行差異的成因 | I3 互斥句、grader 重複案例 → F-ID11、F-ID12 |
| L-ID7 Codex 程式碼審 r1–r3 | 程式與 schema 無缺陷／Codex 自行讀 repo | Codex `gpt-6.1-sol`（`codex exec -p review`）；auto-loop 程式碼平面要求，hook 只提醒 | 3 輪（同一 thread） | r1：總審修正後；r2、r3：修正後 | F-ID11、F-ID12 | — |
| L-ID8 文件審（Codex＋fallback） | 文件正確、內部一致／審查者讀檔 | 9/30 前 Codex；額度用完後 contract-neutral-reviewer（fable，sticky） | Codex 2 輪＋fallback fb1、r1（4 批）、r2（2 批）、final r1（2 批）；最後一次窄複審改回 Codex（ledger 第 126 行） | 各輪工作樹 | F-ID13、F-ID14；fb1 的 4 條 🟡／⚪ 中 2 條轉成裁定 | 未知 |
| L-ID9 verify 決定性 checks＋腳本自驗 | 13 項 checks 成立／agent 照 schema 文字執行，部分用腳本 | verify agent；腳本先用 5 個已知答案 fixture 驗過才採信 | 未知 | 總審與 gate 修正後 | F-ID15 | PRECHECK 數到 33 個 commit（實際 8，因 origin 落後；ID retrospective §2） |

### 1c. RS — retro-skill-inventory

| 層 | claim／oracle | 執行者與強制機制 | 成本 proxy | 受測快照 | 抓到的 finding | 已知漏抓 |
|---|---|---|---|---|---|---|
| L-RS1 apply 前 Codex 文件審 | spec／design／tasks／plan 成熟、可實作／Codex 讀 6 檔（全部升 full-design） | Codex；**v3 schema 沒有這道正式 gate**，使用者要求才做（handoff 09:58） | 1 輪（thread `01a0f9fc-…`） | 實作前的設計 artifacts | F-RS1、F-RS2 | — |
| L-RS2 SDD 事前衝突掃描 | task 驗收條件之間沒有矛盾／controller 讀 plan | 主 session；SDD skill 要求 | 未知 | plan、tasks | F-RS3 | — |
| L-RS3 SDD task 審查（批次 A、B） | 每批符合 spec／審查者讀 diff | subagent；SDD 結構性派工 | 2 次 | 批次 A、B 的工作樹 | 未記錄 | schema 排除句漏限定條件 → F-RS4 |
| L-RS4 SDD 全分支總審 | 整個分支與 REQ-5 一致／審查者讀全範圍（`code-reviewer.md`） | opus subagent；SDD 結構性派工 | 1 次 | `a8e67b6..` 實作後工作樹 | F-RS4 | 模板同一句沒點出 → F-RS6（其後修正範圍只限 schema） |
| L-RS5 修正後範圍限定複審 | 修正正確／審查者只看修正 | subagent | 1 次 | 修正後 | 未記錄 | 模板同一句 → F-RS6 |
| L-RS6 實作者自報 | 自己的證據表與 grep 一致 | implementer；無強制 | — | 2.1 證據表 | F-RS5 | — |
| L-RS7 CLI 送達查驗（task 2.2） | CLI 交給 agent 的指令帶新文字／擷取 `openspec instructions` 輸出 grep | implementer；plan 指定 | 修正前後各 1 次 | dogfood 副本 | 無（通過） | 驗的是**送達**，不是 agent 讀了之後的行為（VS1 P2） |
| L-RS8 verify | 13 項 checks／agent 照 schema 文字執行 | opus subagent | 1 次 | `2b1019f` | F-RS7 | — |
| L-RS9 程式碼審（schema） | schema 改動無缺陷 | strict-reviewer（Codex 額度用完的 fallback） | 1 輪 | `055a6ab` 前 | 無（✅ Ready） | 未知 |
| L-RS10 文件審 fallback 4 輪 | 文件正確／審查者讀檔 | contract-neutral-reviewer（Codex 額度用完） | 4 輪 | 各輪修正後 | F-RS6、F-RS8、F-RS9 | 未知 |

### 1d. I2 — issue #2 上游相容性

| 層 | claim／oracle | 執行者與強制機制 | 成本 proxy | 受測快照 | 抓到的 finding | 已知漏抓 |
|---|---|---|---|---|---|---|
| L-I2a 每週 version-check（CI） | ①上游有沒有比釘住版本新的 release ②bridge 在最新 OpenSpec 下仍通過結構驗證／① npm 與 GitHub release 比字串 ② 安裝最新 OpenSpec 跑 `openspec schema validate`；任一上游版本與釘住版本不同、或 ② 結構驗證失敗，就開或更新 drift issue；② 失敗另讓 workflow 判失敗（`.github/workflows/version-check.yml`） | GitHub Actions 排程，**程式執行** | 每週 1 次自動 | README 釘住的版本；最新 OpenSpec | F-I2a | 驗得到版本與 schema 結構；驗不到指令文字的語意、CLI 行為細節與 Superpowers 的行為（CLAUDE.md 寫明結構驗證刪掉 `requires:` 邊也照樣通過） |
| L-I2b 相容性 spike | bridge 依賴的上游行為與文字宣稱仍成立／同一支腳本雙版對照實測＋讀上游原文 | Orca agent；使用者排序後才做 | 1 個 agent；raw 213 檔精簡為 29 檔（handoff 15:20） | OpenSpec 1.3.1 vs 1.14.0；Superpowers v5.1.0 vs v6.4.2 | F-I2b | Superpowers 沒有實際跑任何 skill（report 末段「沒查的」） |
| L-I2c Codex 文件審（2 批） | spike 報告正確、可重現／Codex 讀檔 | Codex | 2 批 × 2 輪（同 thread 續審） | spike 報告 | F-I2c | 未知 |

### 1e. VS1 — 第一步對照文件

| 層 | claim／oracle | 執行者與強制機制 | 成本 proxy | 受測快照 | 抓到的 finding | 已知漏抓 |
|---|---|---|---|---|---|---|
| L-VS1a fallback 文件審 3 輪 | 文件正確 | contract-neutral-reviewer（當時 Codex 視為不可用） | 3 輪 | 各輪修正後 | F-VS1、F-VS2 | 正文 7 處措辭／出處錯誤 → F-VS4 |
| L-VS1b Codex 標準文件審（Gate） | 文件沒有事實錯誤、推論斷裂、來源誤用（VS1 §5d） | Codex；使用者裁定補做 | 1 輪＋修正後複審 1 輪 | fallback 3 輪後 | F-VS3 | 同上 → F-VS4 |
| L-VS1c Codex 研究評論（Challenge，非 Gate） | 下一步方向有沒有框錯、漏反例（VS1 §5d） | Codex；使用者裁定 | 1 輪 | 同上 | F-VS4；研究方向類挑戰另記進備忘 | — |
| L-VS1d 撰寫者自查與使用者追問 | 推論鏈成立 | 主 session；無強制 | — | 寫作中 | F-VS5、F-VS6 | — |

### 1f. VS2 — 本 session

| 層 | claim／oracle | 執行者與強制機制 | 成本 proxy | 受測快照 | 抓到的 finding | 已知漏抓 |
|---|---|---|---|---|---|---|
| L-VS2a Codex 文件審 r1／r2 | 備忘與索引正確、引用與出處相符 | Codex；auto-loop 文件平面要求，hook 只提醒 | 2 輪（同 thread） | r1：補索引後；r2：修 §6、補 §8 後 | F-VS7 | 未知 |
| L-VS2b 語意比對 agent | brainstorm 的承諾已被正式文件完整承接／逐要素對照正式文件原句 | general-purpose subagent；使用者指示 | 1 次派工 | 方向文件、正式設計、brainstorm | F-VS8 | agent 自列沒讀的 handoff、spike、spec |
| L-VS2c 主 session 複核 agent 出處 | agent 引用的章節與行號為真／開檔 grep | 主 session；全域規則「證據先於斷言」 | 2 次指令 | 同上 | 無（都對得上） | — |
| L-VS2d Codex 程式碼審＋precommit 替代 | `.gitignore` 只忽略目標檔／Codex 讀 repo；`git check-ignore`；schema validate | Codex＋主 session；precommit runner 回 `⚠️ NO CHECKS RUN`（repo 沒有 lint／測試） | 1 輪＋2 個指令 | `.gitignore` 一行 | 無 | — |
| L-VS2e 本文件自己的文件審：fallback（fable）→ Codex | 本盤點表正確、引用與計數相符 | Codex 額度用完（exit 1）→ contract-neutral-reviewer（fable，使用者指定），額度恢復後依使用者裁定排程補跑 Codex 首次派發 | fallback 1 次；Codex 3 輪（同 thread） | fallback：初稿；Codex r1：依 fallback 意見修正後（修正沒有動到 Codex 抓到的三格）；r2：修 F-VS10 後；r3：修 F-VS11 後 | F-VS9、F-VS10、F-VS11 | fallback 漏了 F-VS10 的三條 |

---

## 2. finding 表

「首次／重新」：重新發現＝同一缺陷先前已被記錄（含被 defer）。「前一層已漏過」：同一缺陷在**較早的某一層**的受測範圍內、但那層沒報；寫出是哪一層。「如果沒抓到會怎樣」是**推論**。

| # | 層 | finding | 嚴重度（原標） | 首次／重新 | 前一層已漏過 | 如果沒抓到會怎樣（推論） | 出處 |
|---|---|---|---|---|---|---|---|
| F-ID1 | L-ID2 | 預期答案表把 v07 誤列為 REQ-1-S4 的連帶命中 | Important | 首次 | — | 盲測以錯的預期答案評分 | ledger 第 35 行 |
| F-ID2 | L-ID2 | 預演失敗時，沒有 ID 的新標題不會被回報 | Important（I1） | 首次 | — | 規則漏報一類違規 | ledger 第 58 行 |
| F-ID3 | L-ID2 | 數量對不上時 RENAMED／REMOVED 的類別集合有歧義 | Important（I2） | 首次 | — | 執行者判定分歧 | ledger 第 58 行 |
| F-ID4 | L-ID2 | 已同步 capability 的狀態衝突（spec 層級，交使用者） | Important（I3） | 首次 | — | 規則對合法流程給錯判；後來成為 verify-sync 研究題 | ledger 第 58、66、67 行 |
| F-ID5 | L-ID3 | 規則宣稱「任何已套用的 delta 都會中止預演」為假（MODIFIED 不會） | 列為 I4 | 首次 | re-reviewer 只以範圍外附註提起，由 controller 實測坐實 | 規則對真實 CLI 行為描述錯誤 | ledger 第 69 行 |
| F-ID6 | L-ID2（器材 v2 審查） | 新回報格式沒有「無判定」選項，可能讓 RED 翻面 | Important | 首次 | — | **RED 基準被器材改變**，GREEN 的對照失真 | ledger 第 84 行 |
| F-ID7 | L-ID2 | 4.2／4.3 五項（無 ID 標題文法與 spec 連結、Superpowers 基準版本與 README 政策矛盾、跨檔判準措辭不一、驗證紀錄寫錯 check 編號、zh 用語） | Important ×5 | 首次 | — | README 與 Compatibility 表對外說法自相矛盾 | ledger 第 93 行 |
| F-ID8 | L-ID4 | 盲測 r1：B 揭露規則對「配對不可靠時要不要另計一類」寫得不清楚（v13） | 盲測不一致 | 首次 | 執行者 A 同輪 22/22 | 規則歧義被 A 的 22/22 遮住 | ledger 第 72 行 |
| F-ID9 | L-ID4 | 盲測 r2：B 逐條判對、FINAL 寫錯（v06），回報格式自相矛盾 | 盲測不一致 | 首次 | 執行者 A 同輪 22/22 | 器材缺陷被誤當規則缺陷，或反之 | ledger 第 77 行 |
| F-ID10a | L-ID6 | contract-identity 的 owner 連結出了 repo 就斷 | Important（I1） | **重新**（task 4.2 的 deferred minor：README 的相對 spec 連結在採用者複本裡解析不到，Minor） | task 審查已發現但判 Minor 並 defer；總審另寫「HEAD 上也無法解析」，這部分是否為新資訊，紀錄不足以判斷 | 採用者拿到的 bundle 指向不存在的位置 | ledger 第 95、111 行 |
| F-ID10b | L-ID6 | FRESHNESS 段與 13.F 矛盾 | Important（I2） | **重新**（task 3.1 的 deferred M1，Minor） | task 審查已發現但判 Minor 並 defer | 規則兩段互斥 | ledger 第 59、111 行 |
| F-ID10c | L-ID6 | prompt v1→v2 的裁定沒寫回 tasks 1.3／3.1 | Important（I3） | 首次 | — | 紀錄與實際做法不符 | ledger 第 111 行 |
| F-ID10d | L-ID6 | 遷移第 4 步漏了其他進行中 change 的過期標題 | Important（I4） | 首次 | — | 採用者遷移後留下過期標題 | ledger 第 111 行 |
| F-ID11 | L-ID7 | `grade.py` 對重複的案例段只保留最後一段（注入重複仍 MATCH 22） | P1 | 首次 | L-ID5 selftest、L-ID6 總審 | **評分器可給出假 GREEN**；修正後重評 3 份正式報告，結果未變 | ledger 第 116、119 行；ID retrospective §2 |
| F-ID12 | L-ID7 | check 13 的 13.B／13.E 開頭與 INTERACTION 段互斥 | P2 | 首次 | L-ID2 task 審查、L-ID6 總審 | 出貨的規則文字自相矛盾；修正後 GREEN 重跑（v3） | ledger 第 116、117 行 |
| F-ID13 | L-ID8（r1 batch 4） | `templates/verify.md` §9 的 `- [ ] ✅ PASS` 與 retrospective PRECHECK 的 grep 撞在一起；zh-TW 第 2 步多一條禁令 | ⛔（batch 4） | 首次 | — | retrospective PRECHECK 讀錯 verify 結果 | ledger 第 116 行（執行者依 sticky fallback 推定，ledger 該行未寫） |
| F-ID14 | L-ID8（final r1） | verify.md 新鮮度註記寫錯 plan.md 最後修改點；retrospective 範圍說明寫錯 diff 統計範圍 | 🟡 ×2（確認為事實錯誤） | 首次 | — | 紀錄的事實錯誤 | ledger 第 126 行 |
| F-ID15 | L-ID9（腳本自驗） | verify 腳本兩個缺陷：`cmd` 不認 `2>/dev/null`、check 3 只比標題 | 未標 | 首次 | — | **verify 產生形式正常的錯誤結論** | ID retrospective §1 |
| F-RS1 | L-RS1 | REQ-5「neither MUST state」語意歧義 → 改「Both … MUST NOT state」 | 🟡 | 首次 | — | 實作照歧義版本做（handoff 09:58 當日洞見） | handoff 09:58 |
| F-RS2 | L-RS1 | plan 1.1 缺「產出供 2.2 查驗的 template」反向介面 | ⚪ | 首次 | — | — | handoff 09:58 |
| F-RS3 | L-RS2 | 1.1 驗收條件內部張力（要陳述兩類定義 vs 既有 note 不能動） | 未標 | 首次 | — | 實作與審查來回 | RS retrospective §1、§3 |
| F-RS4 | L-RS4 | schema 排除句漏了 REQ-5 的限定條件 | **Minor**（final review Minor #1） | 首次 | L-RS3 兩次 task 審查 | agent 可能把 TDD 列也排除，retrospective 記錯 | RS retrospective §1、§3 |
| F-RS5 | L-RS6 | 證據表 zh-TW:413 那格與自己的 grep 對不上，照實附註 | 未標 | 首次 | — | 證據表引用的 grep 重現不出結論 | RS retrospective §1；`apply-evidence.md` 表 #1 |
| F-RS6 | L-RS10（r3） | 模板說明同一句沒補限定條件（schema 修了、模板漏修） | 🟡 | 首次 | L-RS4 總審（只點 schema）、L-RS5 複審 | 模板與 schema 說法不一 | RS retrospective §2 |
| F-RS7 | L-RS8 | PRECHECK「commit 數 > 0」可假性通過（verify.md PRECHECK 段已記錄；是 verify agent 還是 controller 先指出，紀錄沒寫） | 未標 | 首次 | — | 實作沒 commit 也過 PRECHECK | RS retrospective §5 |
| F-RS8 | L-RS10（r1） | 4 🟡，其中 3 筆是紀錄的事實／出處錯誤（含把 worktree-local ledger 誤寫成 gitignored） | 🟡 ×4 | 首次 | — | 紀錄的事實錯誤；觸發「證據壽命」觀察 | RS retrospective §2、§5 |
| F-RS9 | L-RS10（r4） | 範圍說明漏了 `055a6ab` 補修等 4 條非阻擋意見 | 🟡 ×2、⚪ ×2 | 首次 | — | — | RS retrospective §2 |
| F-I2a | L-I2a | OpenSpec 與 Superpowers 都有比釘住版本新的 release（開 issue #2）；最新 OpenSpec 下結構驗證通過（run 成功） | — | 首次 | — | 不知道上游漂移 | handoff 15:20；`CLAUDE.md`「CI／自動化的既有約定」 |
| F-I2b | L-I2b | Superpowers 6 條 bridge 宣稱不成立（含新出現的 S13、S14）；OpenSpec 8 項有變化 | 報告分級（R2 中高等） | 首次 | L-I2a 只驗到版本號與 schema 結構 | bridge 的拒用理由與文件宣稱錯誤卻沒人知道 | spike `report.md` 開頭摘要與 R2 |
| F-I2c | L-I2c | 查證範圍說太廣；重現說明跑不動 | 🔴 ×2 | 首次 | — | 讀者以為驗得比實際廣；照說明重跑會失敗 | handoff 15:20 |
| F-VS1 | L-VS1a（r1） | 拿自標「不是規範」的 TE 當標準，REQ-2 其實已涵蓋 | 🔴 | 首次 | — | 錯的規範依據 | handoff 17:46 |
| F-VS2 | L-VS1a（r2） | 修 r1 時把衝突兩端寫錯（§4.3 vs REQ-2） | 🟡 | 首次（**修正引入**） | — | 研究主軸指向錯的衝突 | handoff 17:46 |
| F-VS3 | L-VS1b | P1 過度宣稱 | 🟡 | 首次 | — | — | handoff 17:46 |
| F-VS4 | L-VS1c | 正文 7 處措辭／出處錯誤 | 未知（研究評論不用 Gate 分級） | 首次 | L-VS1a 3 輪、L-VS1b | 錯誤出處進入第二步 | VS1 §5f；handoff 17:46 |
| F-VS5 | L-VS1d | P2 用來佐證的 RS-5 驗的是送達、不是 agent 行為 | — | 首次 | — | P2 的實證強度被高估 | VS1 §5e |
| F-VS6 | L-VS1d（使用者追問） | 撰寫者舉的例子（以 RS-5 支撐行為驗證）正是 P3 在批評的毛病 | — | 首次 | 撰寫者自查 | 同上 | handoff 17:46 當日洞見 |
| F-VS7 | L-VS2a（r1） | 「66 個 finding」與同文的「分類單位」說明不一致 | 🟡 | 首次（備忘第 84 行與 CD §0 只寫了計數規則，沒有記錄過這個誤寫） | — | 讀者把 66 當 finding 總數 | 本 session |
| F-VS8 | L-VS2b | 正式設計沒有 G2；承諾措辭比正式設計 §8 的實際保證強；方向文件的「required Review = PASS」正式設計沒列 | 未分級（交使用者裁定） | 首次 | — | 以為正式設計是唯一來源而刪方向文件，G1–G3 的定義就斷掉 | 備忘 §8 |
| F-VS9 | L-VS2e（fallback） | 評分器試跑寫成三條錯誤路徑（實為兩條＋全對對照）；盲測規則寫成四版（實為三版）；一格把作者推論標成「CD 原文」 | 🟡 ×3、⚪ ×2 | 首次 | — | 錯的數字與出處進入研究 | 本 session |
| F-VS10 | L-VS2e（Codex） | F-ID10a 誤標首次（ledger 第 95 行已記）；F-VS7 誤標重新發現；把 version-check 寫成只比版本號（實際還跑最新 OpenSpec 的結構驗證） | 🔴 ×3 | 首次 | L-VS2e fallback（初稿上這三格就已存在） | 本表的「首次／重新」與「前一層已漏」欄算錯，**正好是本表要回答的增量問題** | 本 session |
| F-VS11 | L-VS2e（Codex r2） | 修 F-VS10 第三條時把 drift issue 的觸發條件寫反：把②定義成「結構驗證通過」，接著寫「任一成立就開或更新 drift issue」，等於宣稱驗證通過也會觸發；實際條件是任一上游版本與釘住版本不同，或結構驗證失敗（`version-check.yml` 的 `Open or update drift issue` step 的 `if:`） | 🔴 | 首次（**修正引入**：r1 修正時寫入；2026-10-05 補記。對照組研究提議在「重新」底下細分「半修」、並把「修正引入」由註記改成獨立類別，見 `./2026-10-05-verification-comparison-case-resurface.md` §3，本表暫不改分類） | —（該句在 r2 的受測快照才出現，先前沒有任何一層審過它） | 讀者以為版本一致、驗證通過時也會更新 issue，對 CI 能力的描述與實作相反 | Codex 原始對話 `~/.codex/sessions/2026/10/02/rollout-2026-10-02T21-52-19-01a0fce3-….jsonl`（repo 外、無保存保證）；handoff 20261005 |

**CD 的重新發現**（不逐條列入上表）：Codex 0910 的 9 個單位中，#53、#57、#58、#59 帶 G 標記（先前已 defer），屬重新發現；例如 #59 即 fallback r4 的 #38（D2）。

---

## 3. 觀察

分「事實」與「推論」。事實只寫**觀察到的額外偵測**，不寫「哪一層比較好」。

### 事實

- **O1 每個有多層的案例，都有「後面一層抓到、前面一層在受測範圍內漏掉」的缺陷**：RS 的 F-RS4（兩次 task 審查 → 總審）、F-RS6（總審與複審 → fallback r3）；ID 的 F-ID11、F-ID12（task 審查、總審、selftest → Codex）；VS1 的 F-VS4（fallback 3 輪＋Codex 標準審查 → 研究評論）；CD 的 4 個單位（Pilot 2 fallback 2 輪 → Codex 0910，CD H11）；本文件自己的 F-VS10（fallback → Codex）。**每一例的前後兩層審的快照、範圍、模板都不同**，所以這只說明「後一層提供了額外偵測」，不說明原因。
- **O2 會讓證據本身失真的 finding，大多落在「驗證器材」上，不在受測產品上**：F-ID6（盲測回報格式可能讓 RED 翻面）、F-ID11（評分器可給假 GREEN）、F-ID15（verify 腳本產生形式正常的錯誤結論）、F-ID13（PRECHECK 的 grep 會撞到模板字串）、F-RS7（PRECHECK 假性通過）。這 5 條至少由 4 種不同的層抓到（task 審查、Codex 程式碼審、腳本自驗、文件審；F-RS7 由誰先指出紀錄沒寫）。
- **O3 原標嚴重度和後果不一定對得上**：F-RS4 原標 Minor，後果是 retrospective 記錯；F-ID10a、F-ID10b 都是先被 task 審查判 Minor 並 defer，總審再發現時升為 Important；F-ID12 原標 P2，代價是一次 GREEN 重跑。
- **O4 平行的第二個執行者提供了額外偵測**：F-ID8、F-ID9 都是執行者 A 同輪 22/22、只有 B 暴露。
- **O5 重新發現佔了可觀的審查輸出**：CD Codex 0910 的 9 個單位有 4 個是已 defer 的；ID 的 F-ID10a、F-ID10b（ID 全分支總審 r1 的 4 個 Important 裡有 2 個）。
- **O6 盤點表自己受證據壽命限制**：§0 的六個來源都缺原始報告，RS 的 SDD ledger 已整份消失；本表多數格子是摘要的轉述，**不是原始紀錄**。
- **O7 強制機制幾乎都是「agent 照文字執行」**：程式強制的只有 CI 的 `openspec schema validate` 與 version-check（含用最新 OpenSpec 跑結構驗證）、腳本 `grade.py`（但何時跑由 agent 決定）；auto-loop 的審查要求由 hook **提醒**、不擋；verify checks 由 agent 照 schema 文字執行。這與備忘 §4 的風險一致。
- **O8 成本資料大多是「未知」**：派工次數只有 ID 的盲測（11 次）、RS 的 apply／verify（8 次）、CD 的 SDD 席位（16 次）有記；Codex 的 token、各層實際耗時都沒有紀錄。

### 推論（不是事實）

- O2 若在更多案例成立，表示**驗證器材需要和受測產品一樣被驗**（VS1 P4 從單一案例延伸到多種器材）；這與 P3 Claim↔Oracle 對齊是同一層的問題——器材壞了，oracle 就對不準 claim。
- O3 表示**不能用原標嚴重度當「增量價值」的代理指標**；本表「如果沒抓到會怎樣」欄是更接近的量，但它是推論。
- O1 與 O8 合起來：現有資料能回答「哪一層有額外偵測」，**回答不了「那一層值不值得它的成本」**，因為成本那一側幾乎沒資料。要做備忘 §0 的成本效益判斷，之後的案例得開始記成本（至少派工次數與輪數）。

---

## 4. 未查證與邊界

- **只讀摘要**：ID 的各 task 審查、fallback 文件審，RS 的全部 SDD 與 fallback 報告，VS1 的全部審查報告，原文都不在了；本表依 ledger、retrospective、handoff 的轉述。轉述本身漏掉的 finding，本表也看不到。
- **CD 只做席位彙總**，沒有回各份原始報告逐條檢查，也沒有逐單位判斷首次或重新發現（只標出 G 標記的 4 個）。
- **「前一層已漏過」只在紀錄明寫時填**；沒寫的不代表沒漏。
- **「如果沒抓到會怎樣」全部是推論**，沒有一條實際放行過來驗證後果。
- **沒有對照組**：所有案例都是這套系統自己的規則、紀錄或基準宣告；沒有一般應用程式的 TDD 案例（備忘 §7 的對照組題）。
- **分類是我的判斷**：層的切法（例如把 controller 實測獨立成一層、把器材審查歸在 task 審查）換一個人可能不同。
