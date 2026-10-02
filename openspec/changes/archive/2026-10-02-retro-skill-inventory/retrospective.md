# Retrospective: retro-skill-inventory

> Written: 2026-10-02 (after verify recorded ⚠️ PASS WITH WARNINGS)
> Commit range: `a8e67b6..055a6ab`（archive commit 另計）
> Worktree: `C:/Users/user/orca/workspaces/openspec-schemas/retro-skill-inventory`（Orca worktree，分支 `azuma520/retro-skill-inventory`）— 尚未 archive、未併回 main、未 push

> **範圍說明。** `a8e67b6` 是 `origin/main`。範圍內 3 個 commit 中，`094dfac`、`da1e5f2` 是 apply 前的設計階段 checkpoint（brainstorm／proposal／design／specs／tasks／plan），
> **主要實作在 `2b1019f`**（使用者 2026-10-02 授權的單次 commit）；**archive 前的完整最終狀態還包含 `055a6ab` 的補修**——其中 `superpowers-bridge/templates/retrospective.md` 說明文字補上 REQ-5 的限定條件（「且不承載上述第二類紀律」，文件審查第 3 輪指出），其餘是本 change 記錄的校正與 verify.md、本檔的入庫。兩者性質不同：前者是依 plan 的實作，後者是 archive 前審查後的補修。verify.md 寫於 `2b1019f` 之後、`055a6ab` 之前，描述的是補修前的樹；補修後的送達重驗記在 `apply-evidence.md`「Pre-archive doc-review fix round」段。

---

## 0. Evidence

- **Commit range**: `a8e67b6..2b1019f`（3 commits；`git log --oneline a8e67b6..HEAD`）
- **Diff size**: 全範圍 **+627 / −8，12 檔**（`git diff --shortstat a8e67b6..HEAD`，含本 change 的 artifacts）；
  實作 commit `da1e5f2..2b1019f` **+163 / −10，4 檔**：`schema.yaml` 20 行、`templates/retrospective.md` 10 行、`tasks.md` 8 行、新檔 `apply-evidence.md` 135 行。
- **Tasks done**: **4/4**（`grep -cE '^\s*- \[x\]' tasks.md` → 4；`- [ ]` 0、`- [~]` 0）
- **Active hours**: 未精確記錄。2026-10-02 07:58 開工（handoff 07:58 區塊）→ 08:01 設計 checkpoint → 10:00 tasks／plan → 10:54 實作 commit → 其後 verify，約 3.5 小時，跨 3 個 session 區塊。
- **Subagent dispatches**: apply 與 verify 共 **8 次**——implementer 3（批次 A、批次 B、final-review 修正）、審查 4（批次 A task 審、批次 B task 審、全分支總審〔opus〕、修正後範圍限定複審）、verify 1〔opus〕。apply 前另有 1 次 Codex 外部文件審（thread `01a0f9fc-…`，handoff 09:58 區塊）。全部紀錄見 SDD ledger `.superpowers/sdd/plan/progress.md`。
  **證據持久性限制**：這份 ledger（以及同目錄的 `batchA-report.md`、`batchB-report.md`）只存在於本 worktree，透過本機 `.git/info/exclude`（`/.superpowers/`）排除在版控之外，**不會隨 archive 保存**；worktree 移除後，本文中「evidence: ledger …」的引用都無法再追查。其中支撐結論的裁定（ruling）已在 §3 逐條重述，SDD 審查結果摘要在本節與 §1–§2。
- **New external dependencies**: none
- **Bugs encountered post-merge**: n/a — 尚未併回 main
- **OpenSpec validate state at archive**: not-run — 尚未 archive；verify 時 `openspec validate --all --json` 6/6 valid（verify.md check 1）；`openspec validate retro-skill-inventory --strict` valid（`apply-evidence.md` §2.2）
- **Test coverage signal**: n/a — 4 個 task 全標 `TDD: n/a`（純文字／模板修改與查驗）；替代證據是 `openspec schema validate`、讀檔逐條核對與 CLI 送達查驗（`apply-evidence.md` §2.2）

Commit chain (時序):

```
094dfac chore(openspec): checkpoint retro-skill-inventory design stage, 2026-10-02 handoff
da1e5f2 chore(openspec): add retro-skill-inventory tasks and plan, record pre-apply review
2b1019f fix: align retrospective §4 skill inventory with REQ-5 two-class criterion
（archive commit 尚未產生）
```

---

## 1. Wins

- [evidence: 本檔 §4 表格] **本 change 改的模板當場被自己用上。** 寫這份 retrospective 時，`openspec instructions retrospective` 交出的已是新的 6 列表格與兩類定義（`apply-evidence.md` §2.2 也記錄了 CLI 送達查驗），不需要另外做 smoke。
- [evidence: ledger「Pre-flight conflict scan」表] SDD 事前衝突掃描在派工前抓到 1.1 驗收條件的內部張力（「note 要陳述兩類定義」對上「既有 note 一行都不能動」），以 ruling（另起新段落）解掉，實作與審查都沒為此來回。
- [evidence: ledger「Final review (opus)」行；`schema.yaml:1524-1526`] 全分支總審抓到 schema 排除句漏了 spec 的限定條件（「且不帶任何第二類紀律」），可能讓 agent 把 TDD 列也排除掉。兩次 task 審查都沒抓到這點；用較強模型做總審有實際收穫。
- [evidence: `batchB-report.md` 的 final-review fix round 段] 修正者發現 evidence 表 zh-TW:413 那格與自己的 grep 對不上，**照實附註、沒有順手改掉**，讓複審得以判定這是證據瑕疵。
- [evidence: Orca worktree `issue2-compat-spike`] issue #2 相容性 spike 在另一個 Orca worktree 平行跑完，與本 change 沒有檔案衝突；spike 的 S11 從上游原文獨立印證了本次 apply 撞到的 task-brief 缺口。

## 2. Misses

- 🟡 [painful | evidence: ledger 第一條 Ruling、verify.md check 5] **schema 的 verify check 5 預設實作已 commit，但本 repo 禁止 AI 自行 commit。** apply 全程不 commit，跑 verify 前必須停下向使用者要一次授權（`2b1019f`）。這是 schema 假設與 repo 規則之間的結構性摩擦，不是本次操作錯誤；09-30 identity change 也遇過同一處。
- 🟡 [painful | evidence: ledger 第二條 Ruling] SDD 的 `scripts/task-brief` 認不得 Plan Contract 的 `## 1.1 —` 標題（exit 3），controller 改用等效抽取繞過。這個缺口自 loosen-plan（2026-09-03）就出現過，bridge 文件沒記，換一個 agent 不一定會繞。已列為待登記的後續工作（見 §6）。
- 📌 [nit | evidence: ledger「Controller slip」行] controller 打包總審資料時下了 `git add -N`（被禁止的 index 寫入），當場以 `git reset -q -- <file>` 撤銷，回讀 index 為空並記入 ledger、向使用者揭露。使用者裁定不因此新增流程規則。
- 📌 [nit | evidence: 備援審查報告（存於 session scratchpad，不隨 archive 保存；結論已轉述於本條）] **本輪文件審查沒有取得 Codex 的獨立審查。** Codex 額度用完（`codex exec` exit 1：usage limit，至 2026-10-04），依規則改由 `contract-neutral-reviewer` 備援審查（✅ Mergeable、0 🔴、4 🟡；sentinel 驗證通過）。4 筆 🟡 中 3 筆是記錄的事實／出處錯誤，使用者 2026-10-02 裁定在 archive 前修正並以同一備援審查者複審，不等 Codex 恢復補審。
- 🟡 [painful | evidence: 文件審查 r3；`apply-evidence.md`「Pre-archive doc-review fix round」段] **同一個缺陷，schema 修了、模板漏修。** 全分支總審抓到 schema 的排除句漏了 REQ-5 的限定條件（「且不帶第二類紀律」），修正時只改了 schema，模板說明裡同樣的句子沒有一起改，直到 archive 前的文件審查第 3 輪才被指出；archive 前已補齊，並掃過本 change 自己的記錄（design、proposal、本檔 §4）。這是既有紀律「修一類缺陷要掃完整 surface」的一個實例，使用者 2026-10-02 裁定不另升格成新規則。
- 📌 [nit | evidence: ledger「Final fix wave」行] evidence 表一格（zh-TW:413）在 SDD 複審後由 controller 直接改正，沒有經過 SDD 複審者，偏離「controller 不自己修」；這格交由 archive 前的文件審查涵蓋（本輪由 contract-neutral-reviewer 備援執行，見本節「本輪文件審查沒有取得 Codex 的獨立審查」那一條）。
- 📌 [nit | evidence: 文件審查第 4 輪報告（session scratchpad，不隨 archive 保存；要點轉述於本條）] **文件審查第 4 輪（✅ Mergeable、0 🔴）的 4 筆非阻擋意見與處置**（使用者 2026-10-02 裁定，不為此開第 5 輪審查）：
  - 🟡 本檔範圍說明原寫「實作只有 `2b1019f`」，漏掉 `055a6ab` 的模板補修 → **已修**（見檔首範圍說明）。
  - 🟡 `plan.md` 1.2 與 `tasks.md` 1.2 的排除句沒帶「不承載第二類紀律」限定條件 → **刻意保留、不是漏同步**：兩者是實作前的契約快照（pre-implementation contract snapshot），不追著後來的補修改寫；`plan.md` 的 global constraints 已逐字綁定 REQ-5 全文，且改動 tasks／plan 會讓 verify check 8–12 的結果過時。
  - ⚪ 本檔兩處引號內的改寫句（「且不帶任何第二類紀律」「且不帶第二類紀律」）不是 schema／模板的逐字原文 → 留作觀察，不改；逐字原文見 `schema.yaml` 的「carrying neither discipline」與模板的「且不承載上述第二類紀律」。
  - ⚪ `apply-evidence.md` 補修重驗段的指令把 `out.txt` 寫在 worktree 根目錄 → 留作觀察（指令衛生問題，不影響證據結論）。

## 3. Plan deviations

| Plan task | What changed | Why |
|-----------|--------------|-----|
| 1.1 | 兩類定義以**新段落**加在表格下方，既有 note 一字不動；design D3 原寫「表格下方既有說明補一句」 | plan 1.1 同時要求「note 陳述兩類」與「既有 note 不動」；改既有 note 會違反後者（ledger pre-flight ruling） |
| 1.1 + 1.2、2.1 + 2.2 | 兩兩合併成一次派工、一次審查 | 1.1／1.2 共用同一判準介面，同一實作者寫兩端較能保持一致；2.1／2.2 都是查驗型（ledger ruling） |
| 1.2 | 全分支總審後改寫排除句，補上 spec 的限定條件 | 原句與 REQ-5 第二段不完全一致（final review Minor #1，ledger ruling） |
| 2.1、2.2 | 查驗結果記在新檔 `apply-evidence.md`，不寫進 tasks.md | plan 只說「記在 verify 能引用的地方」；tasks.md 的 checkbox 下方行會被 verify check 8–12 解析，且 tasks 只寫完成狀態（ledger ruling） |

## 4. Skill / workflow compliance

| Skill                                            | Used |
|--------------------------------------------------|------|
| superpowers:brainstorming                        | ✓（`brainstorm.md`；handoff 07:58 區塊：呼叫 brainstorming 6.4.1，bounded 路徑） |
| superpowers:using-git-worktrees                  | ✓（依 skill Step 1a 用 harness 原生 worktree 工具：Orca `worktree create --base-branch main`） |
| superpowers:subagent-driven-development          | ✓（ledger；兩批 implementer＋task 審查、opus 全分支總審、一次修正＋範圍限定複審） |
| superpowers:test-driven-development (✓ only if the skill was explicitly invoked; write `N/A — annotation-driven` when TDD discipline came from the `TDD:` annotations in `tasks.md` and their RED/GREEN evidence instead) | N/A — annotation-driven（4 個 task 全標 `TDD: n/a` 並附理由；無 RED/GREEN 紀錄要求） |
| (structural via SDD) superpowers:requesting-code-review | ✓（每批 task 審查；全分支總審用 requesting-code-review 的 `code-reviewer.md`） |
| superpowers:finishing-a-development-branch       | 尚未 — 屬 archive 之後的步驟，本文寫於 archive 前 |

> 本表只列兩類項目:(1) schema 明確要求呼叫的 Superpowers skill——
> `brainstorming`(由 `brainstorm` artifact 要求)與 apply pre-flight 要求的
> `using-git-worktrees`、`subagent-driven-development`、`finishing-a-development-branch`;
> (2) schema 要求落實、retrospective 必須記錄其執行情況,但 schema 本身不直接呼叫的
> Superpowers 紀律——`test-driven-development`(由 `tasks.md` 的 `TDD:` 標註與
> RED/GREEN 證據承載)與 `requesting-code-review`(透過 subagent-driven-development
> 結構性達成)。僅被列為「可能有用」、且不承載上述第二類紀律的輔助性 skill
> (例如 `superpowers:writing-plans`)不屬於這兩類,不列入本表。

> 如實勾選。TDD 與 code-review 兩列依上方標註本就是條件性/結構性的——
> `tasks.md` 裡標為 `TDD: n/a` 的 task 不算跳過:那個註記就是宣告本身,
> 它帶的理由由 review 那層判斷。確實被跳過的項目在下方
> `### Deliberately Skipped Skills` subsection 記錄原因與預防方案。

### Deliberately Skipped Skills

（無刻意跳過的項目。finishing 列為「尚未」是時序使然——它在 archive 之後執行，屬 README 設計觸點 #6 的已知限制，不是跳過。）

## 5. Surprises

- **verify PRECHECK 第 1 條可能假性通過。** 它數 `merge-base(HEAD, origin/main)..HEAD` 的 commit 數；本分支在實作 commit 前就已有 2 個設計階段 commit（`094dfac`、`da1e5f2`），所以就算實作沒 commit，這條也會通過。它想證明的是「apply 已產出可審的實作」，實際只證明「分支上有任意 commit」；真正確認實作已 commit 的是 check 5（工作目錄乾淨），兩者不是同一件事（verify.md PRECHECK 段已照實記錄）。
- **Orca 開 worktree 預設從 `origin/main` 起分支。** 本地 main 有 2 個未 push 的 commit（本 change 的 tasks／plan 在裡面），必須指定 `--base-branch main`，否則 worktree 裡根本沒有這個 change。
- **retrospective 引用的證據會隨工作環境消失。** 備援文件審查指出：本文原本把 worktree-local 的 SDD ledger 當成可追溯證據引用，還誤寫成「gitignored」。證據在完成宣告的當下存在，但 worktree 一拆就不見——這不是單純寫錯字，而是又一次碰到「證據生命週期」問題（與 verify／sync 消耗 pre-sync state 同類）。本 change 只把限制講清楚（§0），不修機制。
- **worktree 的 `core.autocrlf=true` 讓 `schema.yaml` 在 checkout 時變成 CRLF**（主目錄的工作副本是 LF）。commit 時 git 轉回 LF，diff 也只含實質改動；但讀 `git diff` 時的 CRLF 警告容易被誤當成實作者改壞了換行（ledger batchA 註記）。

## 6. Promote candidates → long-term learning

- [ ] 🟡 **小型 change 的 plan 約一半在重述 tasks（部分證據）** → **One-off**（記錄即可，不據此改 plan 規則）
  > **Why**: 本次 plan 新增的那一半（範圍不得擴張、README 先回報、1.1↔1.2 介面、2.2 相依）看起來可以併進 tasks 驗收條件；但本次 tasks 是預知有 plan 而刻意寫薄的，證據打折。使用者 2026-10-02 裁定：**不能據此推出應取消 plan**。
  > **How to apply**: 下一代 bridge 討論 plan／tasks 分工時，當作一筆部分證據引用；需要更多「tasks 未刻意寫薄」的 cycle 才能下結論。

- [ ] 🟡 **人工逐字複製 contract 會製造同步義務（既有決定的新實例）** → **Promote to** 既有決定的證據（不新增規則）
  > **Why**: REQ-5 只改了一句（「neither MUST state」→「Both … MUST NOT state」），plan 的 global constraints 逐字副本就得跟著改；這次有程式比對所以沒漂移，但再次證明人工照抄會製造同步義務。對應正式設計 `docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md` 決策表第 2 列「取消人工逐字副本」，該決定尚未落地。使用者 2026-10-02 裁定：記成既有決定的新實例，不另升格。
  > **How to apply**: 實作「改引用／衍生、不人工照抄」那個 change 時，引用本例。

- [ ] 🟡 **verify PRECHECK「commit 數 > 0」是對不準的代理指標** → **Promote to** Verification Strategy 研究（work-map `task-20260929-verification-strategy-research`）
  > **Why**: 見 §5 第一條。檢查名義上確認「apply 已產出可審的實作」，實際只驗到「分支有任意 commit」，會假性通過；這和 check 5 實際確認的事不同。使用者 2026-10-02 裁定：保留，談 Verification Strategy／verify lifecycle 時一起看。
  > **How to apply**: 研究時與「verify 需要的 pre-sync state 會被 sync 消耗」那條子題一併檢討 verify 的前置條件設計。

- [ ] 🟡 **SDD `task-brief` 認不得 Plan Contract 標題** → **Promote to** 後續工作（由 issue #2 收斂時登記，待使用者確認登記內容）
  > **Why**: 見 §2 第二條；spike 報告 R3／S11 從上游原文印證。
  > **How to apply**: 決定只寫進文件，或改標題格式（後者可能動到 check 12、bump schema major）。

- [ ] 🟡 **完成宣告引用的證據，生命週期短於宣告本身（observation）** → **Promote to** 下一代 bridge 討論素材（Verification Strategy 研究的 evidence lifecycle 子題）
  > **Why**: 見 §5。retrospective 與 verify 是會被 archive 永久保存的記錄，卻引用了 worktree 移除後就消失的 ledger。使用者 2026-10-02 裁定：先記 observation，不在本 change 修。
  > **How to apply**: 設計「哪些證據必須隨 archive 保存、哪些可以是暫存」時，以本例為案例。

- [ ] 📌 **controller 打包審查資料時誤下 `git add -N`** → **One-off**（記錄即可）
  > **Why**: 已當場撤銷並揭露；使用者裁定不新增流程規則。
