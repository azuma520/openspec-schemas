# Retrospective: requirement-scenario-identity

> Written: 2026-10-01 (after verify recorded ⚠️ PASS WITH WARNINGS)
> Commit range: `42c3d24..95e4d87`
> Worktree: `.claude/worktrees/requirement-scenario-identity`（分支 `worktree-requirement-scenario-identity`）— 尚未 archive、未併回 main、未 push

> **範圍說明。** `42c3d24..95e4d87` 是**實作**範圍。本 change 自己的 artifacts 在開分支前已進 `main`：
> brainstorm／proposal／design／specs 於 `b74354a`（2026-09-29），tasks／plan 於 `7809ef4`（2026-09-30）；
> 這些**初始建立的 commit** 不計入下方 diff；但 tasks／plan 在 `42c3d24..95e4d87` 期間的後續修改（tasks +173／−12、plan +5／−3）仍包含在 §0 的 diff 統計中。

---

## 0. Evidence

- **Commit range**: `42c3d24..95e4d87`（8 commits；`git log --oneline main..HEAD`）
- **Diff size**: **+16739 / −66，278 檔**（`git diff --ignore-cr-at-eol --shortstat 42c3d24..HEAD`）。其中
  `docs/superpowers/poc/` 佔 263 檔、+15900（22 個 fixture 迷你 repo、盲測器材與報告）；其餘 15 檔
  +839／−66，最大單檔 `superpowers-bridge/schema.yaml` +479／−3。
- **Tasks done**: **12/12**（`grep -cE '^\s*- \[x\]' tasks.md` → 12；`- [ ]` 0、`- [~]` 0）
- **Active hours**: 未記錄精確時數。跨 2026-09-29 15:04（開 change）到 2026-10-01 12:12（verify），
  約 5 個 session（各 session 的區塊見 `文檔/handoff/session-handoff-20260929.md`、`-20260930.md`、`-20261001.md`）。
- **Subagent dispatches**: 盲測執行者 **11 次**（RED 1、GREEN r1 2、GREEN r2 2、RED replay 1、GREEN v2 2、
  GREEN v3 2、I3 定點 1；`docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/sdd-ledger.md` 第 53、71、76、85、87、120、123 行）。
  implementer、task 審查、全分支總審、fallback 文件審的派工次數【未精確計數】。Codex 外部派工：文件審（9/30 額度用完前）
  與程式碼審 r1–r3（thread `01a0f4d0-…`，ledger 第 116、118、122 行）。
- **New external dependencies**: none（repo 無 `package.json`、無原始碼；`blind-kit/v2/grade.py` 只用 Python 標準庫，屬證據器材、不隨 bundle 發佈）
- **Bugs encountered post-merge**: n/a — 尚未併回 main、未 push
- **OpenSpec validate state at archive**: **not-run — 尚未 archive**。目前狀態：`openspec validate --all --json` → 5 items、5 passed（verify.md §1）；
  13.B 預演歸檔成功，輸出 `Totals: + 8, ~ 11, - 0, → 10`（verify.md §9）。
- **Test coverage signal**: 無測試框架。替代證據：22 個凍結 fixture 的盲測（RED 22/22 全 `PASS {}`；GREEN v3 兩位執行者各 MATCH 22/DIFF 0/NONCONFORMING 0）；
  17 組 RED/GREEN 紀錄（tasks.md 3.1）；I3 定點驗收 2 題 MATCH 2（`focused-i3/report.md`）；`grade.py --selftest` 16/16；
  `openspec schema validate` ✓。

Commit chain (時序):

```
b74354a (main) docs(openspec): open requirement-scenario-identity change with frozen design artifacts
7809ef4 (main) docs(openspec): add tasks and plan for requirement-scenario-identity
42c3d24 (main, base) chore(handoff): close the 2026-09-30 09:20 session
1de8e10 test(poc): add identity mutation fixtures and blind-test evidence
3780ab3 feat(schema): add stable requirement/scenario IDs and verify check 13 (schema v3)
05fd2f8 docs: sync repo surfaces to schema v3 and record identity task progress
2bc8a56 docs(poc): record identity migration acceptance and pilot observations
01f9825 fix(poc): reject duplicated case sections in the blind-test grader
fc2f1b7 fix(schema): resolve check 13 synced-capability contradiction and doc-review findings
3b8c035 docs(poc): record final-review fixes and GREEN rerun on the final check 13
95e4d87 test(poc): add post-fix I3 focused acceptance and point spec links at the fork
```

尚無 archive commit。

---

## 1. Wins

- [evidence: fixtures README §5 Q1；tasks.md 3.1] **RED → GREEN 翻轉乾淨，而且由對設計無脈絡的執行者判出。** 舊規則（checks 1–12）
  對 17 個植入身分缺陷的 fixture 全部放行 `PASS {}`，證實了 tasks.md 檔頭標為「推論」的前提；寫入 check 13 後同一批全部翻成預期的
  BLOCK 且類別集合正確，5 個正向對照維持通過。判定者看不到預期答案，寫 fixture 的人不判定（2026-09-30 使用者裁定）。
- [evidence: ledger 第 72、77 行；fixtures README §5 Q2] **第二位執行者確實暴露了第一位看不出的不穩定。** round 1 的 B 揭露
  check 13 對「配對不可靠時要不要另計一類」寫得不清楚（v13）；round 2 的 B 揭露回報格式本身會自相矛盾（v06）。兩者分類清楚：
  前者修規則文字，後者修器材，不混在一起。
- [evidence: ledger 第 78、81、86 行；fixtures README §3b] **器材修正沒有變成「重試到綠」。** prompt v2 只改輸出契約，並先用
  「v2 器材＋舊規則」重演 RED（replay 22/22 與原 RED 相同）證明器材修正沒改變 baseline，才放行 GREEN。
- [evidence: ledger 第 117、121 行；tasks.md 3.1「GREEN 後修改紀錄」] **被測物改了就重跑，並如實降級舊證據。** Codex 程式碼審 r1 抓到
  check 13 本體的互斥句，修正後 check 13 已不是盲測過的文字；使用者裁定重跑 GREEN，舊 GREEN 改為 provenance、現在式的
  「與盲測文字逐位元組相同」改寫為歷史敘述。
- [evidence: tasks.md 3.1「證據限制」與「I3 定點驗收」；`focused-i3/answer-key.md`] **證據範圍寫得比結論窄。** 22/22 重跑明寫只證明
  「沒有破壞既有案例」、不證明 I3 分支；後補的 I3 定點驗收再寫明單一執行者、單次樣本、只讀 FINAL、其他 I3 形狀未涵蓋。
- [evidence: ledger 第 123 行] **評分器先證明分得出錯才派工。** I3 定點驗收拆成兩個成對案例（單一案例下「A 被誤判成衝突」不改變 FINAL），
  派工前用假報告證明 grader 對兩條錯誤路徑都回 DIFF。
- [evidence: verify.md §9「執行方式與自我驗證」] **verify 腳本先拿已知答案驗過才採信。** 第一次跑的兩個腳本缺陷（`cmd` 不認
  `2>/dev/null`、check 3 只比標題）都會產生形式正常的錯誤結論，被 5 個已知答案 fixture 抓到。
- [evidence: `migration-acceptance.md`；verify.md §9] **補號遷移一次到位。** 預演歸檔後 10 條 requirement、37 個 scenario 帶 ID，
  `REQ-PB` 補 S1／S2，`contract-identity` 為 `REQ-1`–`REQ-8`，CLI 數量交叉核對一致。

## 2. Misses

- 🟡 [painful | evidence: ledger 第 72、77、78 行] **盲測回報格式沒先定死，多花兩輪 GREEN。** v1 prompt 讓執行者手寫 FINAL 與類別清單，
  B 兩輪各出一種格式問題（漏類別、FINAL 與逐條判定矛盾、簡體類別字）。v2 改成固定 token 與單一權威 FINAL 欄才穩定。
  事後看，「凍結的輸出契約＋grader 自測」應在 RED 之前就位，而不是在 GREEN r2 之後。
- 🟡 [painful | evidence: ledger 第 116、117、119 行] **grader 的重複案例漏洞在 GREEN 之後才被發現。** `grade.py` 對重複的案例段只保留最後一段
  （注入一段重複內容仍得 MATCH 22），由 Codex 程式碼審 r1 抓到。selftest 當時沒有涵蓋「同一案例出現兩次」。修正後重評 3 份正式報告，結果未變。
- 🟡 [painful | evidence: ledger 第 69、116、117 行] **check 13 本體的 I3 互斥句通過了 task 審查與全分支總審。** 13.B／13.E 開頭把已同步 capability 的
  候選態比對列為無法判定，INTERACTION 段卻說預演成功時照常比對。兩句出自 fix round 2–3，直到 Codex r1 才被抓到，代價是一次 GREEN 重跑。
- 🟡 [painful | evidence: ledger 第 8 行] **Task 1.1 由主 session 自做，偏離 SDD。** 已向使用者揭露，並以 strict-reviewer 兩輪獨立審查補救（✅ Ready）。
- 🟡 [painful | evidence: ledger 第 111、112 行] **contract-identity 的 owner 連結出了 repo 就斷。** bundle 表面連到 repo 內的 spec，而 spec 不隨
  bundle 發佈（全分支總審 I1）。改為 GitHub canonical URL 並註明「不隨 bundle 內含」；canonical repo 後來定為 fork `azuma520`（`95e4d87`）。
- 📌 [nit | evidence: `migration-acceptance.md`；ledger 第 102、111 行] **5.2 字面驗收沒過，以 approved deviation 結案。** `repo-guidance` 歸檔後有
  3 行純空白差異。成因後來在總審中找到：`repo-guidance` 是手寫的、`## Requirements` 前後有空行，另外三個主 spec 是 archive 產物；archive 重新
  序列化該段時不保留空行。依使用者裁定只記在本文、不開 backlog。
- 📌 [nit | evidence: ledger 第 100、101 行] **`/smart-commit` 在 worktree 內跑不動。** 隔離拒跑任何 `bash <腳本>`，commit 降級為手動
  `git add/commit` 加等價檢查（使用者選擇）。
- 📌 [nit | evidence: verify.md PRECHECK、§5] **`origin/main` 落後本機 `main` 28 個 commit**，使 verify PRECHECK 數到 33 個 commit（實際 8）。push 前要處理。
- 📌 [nit | evidence: ledger 第 44 行] **Codex 額度 9/30 用完**，文件審改由 contract-neutral-reviewer（Fable）接手並 sticky 到本 change 結束。

## 3. Plan deviations

| Plan task | What changed | Why |
|-----------|--------------|-----|
| 1.1 | 由主 session 自做，非派 implementer | 已揭露；以 strict-reviewer 兩輪補審（ledger 第 8 行） |
| 1.3 / 3.1 | RED 用 prompt v1、GREEN 用 prompt v2，「只有規則來源一個變數」未逐字成立 | GREEN r2 暴露回報格式缺陷；使用者裁定器材修正＋RED replay 對照（22/22 一致）。approved deviation，plan 原文不改（tasks.md 1.3、3.1 驗收紀錄） |
| 2.1 | 曾重新打開，後依「RED provenance 採混合」裁定確認原 RED 有效 | prompt v2 是否需要重跑 RED（ledger 第 79–83 行） |
| 3.1 | GREEN 跑了四輪：r1、r2（器材缺陷，非正式）、v2（正式）、v3（最終文字重跑）；另加 I3 定點驗收 2 題 | r1 規則歧義、r2 器材缺陷、v3 因 check 13 本體修正；I3 分支不在 22 題涵蓋內（tasks.md 3.1） |
| 4.2 | Compatibility v3 列的 Superpowers 欄填宣告基準 v5.1.0，而非「實際驗過的版本」v6.4.1 | 使用者裁定 I-2 B：區分相容基準與實際工作環境，觀察到的版本寫進驗證紀錄（ledger 第 96 行） |
| 5.2 | 「除標題外逐行一致」未成立（3 行空白），以 approved deviation 結案 | 非空白內容一致、D7 的「內容不變」宣稱成立（ledger 第 102 行） |
| 5.3 | ledger 從 gitignored 工作區複製進 repo（`sdd-ledger.md`） | §5 引用 ledger 行號，原檔不在版控（ledger 第 108 行） |
| （新增） | 全分支總審 r1 後的修正、grader fix round 2、check 13 I3 修正 | 總審與正式 gate 的 findings（ledger 第 111–119 行） |

## 4. Skill / workflow compliance

| Skill                                            | Used |
|--------------------------------------------------|------|
| superpowers:brainstorming                        | ✓（`brainstorm.md` 第 4 行：已呼叫 6.4.1，輸出重導到本 change） |
| superpowers:writing-plans                        | N/A — schema v3 的 plan instruction 明寫「No skill invocation is required」（`schema.yaml` plan instruction），plan.md 依 Plan Contract 直接撰寫；未找到呼叫紀錄 |
| superpowers:using-git-worktrees                  | ✓（worktree `.claude/worktrees/requirement-scenario-identity`；`session-handoff-20260930.md` 第 126 行「照 schema apply 用 worktree」） |
| superpowers:subagent-driven-development          | ✓（`sdd-ledger.md`；每 task implementer＋獨立審查，1.1 例外見下） |
| superpowers:test-driven-development (✓ only if the skill was explicitly invoked; write `N/A — annotation-driven` when TDD discipline came from the `TDD:` annotations in `tasks.md` and their RED/GREEN evidence instead) | N/A — annotation-driven（3.1 `TDD: applicable`、17 組 RED/GREEN；其餘 11 個 task 標 `TDD: n/a` 並附理由） |
| (structural via SDD) superpowers:requesting-code-review | ✓（per-task 審查、全分支總審 r1/r2、Codex 程式碼審 r1–r3） |
| superpowers:finishing-a-development-branch       | 尚未 — 屬 archive 之後的步驟，本文寫於 archive 前 |

> 如實勾選。TDD 與 code-review 兩列依上方標註本就是條件性/結構性的——
> `tasks.md` 裡標為 `TDD: n/a` 的 task 不算跳過:那個註記就是宣告本身,
> 它帶的理由由 review 那層判斷。確實被跳過的項目在下方
> `### Deliberately Skipped Skills` subsection 記錄原因與預防方案。

### Deliberately Skipped Skills

> 跳過 skill 是設計的 escape hatch,不是常規路徑。每個刻意跳過的 ✗ 回答以下三題;
> 本節記錄實際發生了什麼——空白代表沒有刻意跳過,不是達標證明。

- **`superpowers:subagent-driven-development`（Task 1.1 的 implementer 派工）**
  - **What was skipped**: SDD 的 sub-step——1.1 沒有派 implementer，由主 session（controller）直接建 fixtures；其餘 11 個 task 照 SDD。
  - **Why this cycle**: ledger 第 8 行記為「executed inline by the controller (deviation from SDD, disclosed to user 2026-09-30)」。
    fixture 作者同時掌握預期答案，盲測設計本就要求「寫 fixture 的人不判定」，作者偏誤的風險因此落在 fixture 本身；這是偏離後才補審的，不是事前判準。
  - **How to prevent recurrence**: `scope-judgment rule` — 產出「受測素材」（fixtures、預期答案）的 task 與產出規則文字的 task 同等派 implementer；
    若選擇自做，事前（而非事後）指定一位看過預期答案、但不擔任盲測執行者的獨立審查者。本次以 strict-reviewer 兩輪補上（使用者裁定 3A）。

> **與 §6 Promote candidates 的關係**:多個 cycle 同 skill 同 `How to prevent`
> 答案 → 該模式應 promote 到 §6,直接觸發 schema / skill PR,不可累積成「常態」。

## 5. Surprises

- **`openspec archive` 中止時結束碼仍是 0**（輸出 `Aborted. No files were changed.`；`author-run.md`）。歸檔成功因此改為「結束碼 0 且 change 已移入 `archive/`」，寫進 check 13 與 5.2。
- **已套用的 MODIFIED 不會讓預演中止，已套用的 RENAMED 會**（ledger 第 69 行，I4）。check 13 原文「任何已套用的 delta 都會中止預演」是錯的，由覆審者一則範圍外附註觸發 controller 實測揪出。
- **`openspec show <change> --json --deltas-only` 會在 stderr 印警告**，混讀 stdout 會解析失敗、被誤判為無法判定；check 13 因此明寫只讀 stdout。
- **合法的 sync 會吃掉 verify 需要的 pre-sync 狀態**（I3，ledger 第 66、67 行）。本 change 以「依證據依賴局部判無法判定」處理，lifecycle 問題另登記為研究題（工作地圖「Verify / Sync lifecycle」），不掛進本 change。
- **執行者的失敗多半出在回報，不在讀規則。** round 2 的 v06 逐條判定正確、FINAL 卻寫錯（ledger 第 77 行）；原先預期 sonnet 的問題會出在理解規則。
- **archive 會重新序列化手寫主 spec 的空行**（ledger 第 111 行）。逐行相等不等於語意契約，5.2 的驗收判準與宣稱沒有對準。
- **Windows worktree 的深路徑超過 git 的 260 字元上限**（ledger 第 125 行）。worktree 根 84 字元＋最深 fixture 路徑 172 字元，在 `.gitattributes` 查詢時失敗；主目錄的 36 字元根則不會。repo 本機 `core.longpaths=true` 只修好這台。
- **worktree 摩擦累計 9 例**（`session-handoff-20260930.md` 第 160 行 8 例＋上一條）：從 `origin/main` 開分支、gitignored dogfood 副本不在 worktree、隔離擋 `orca terminal create` 與 `bash <腳本>`、handoff 路徑解析到 worktree 內等。依使用者裁定只記不修，作為 `task-20260904-worktree-handoff-lifecycle` 的實測案例。
- **D10 觀察題（proposal 新增 `## Out of Scope`、`## Assurance Boundary` 兩段的 dogfood，n=1）：**
  - ① **有沒有被用到**：在 repo 內全文搜尋（排除 fixtures），兩段名稱只出現在 proposal 本身、brainstorm、design 與 0929 handoff；plan、tasks、verify、ledger 都沒有引用。plan 的「Binding non-goals」標明取自 `design.md`，不是 proposal。另掃 9/29 session 的 subagent 對話紀錄，審查者的回覆文字也沒有提到這兩段（只有讀檔時出現）。搜尋只涵蓋 repo 與留存的 scratchpad，已清除的 session 暫存沒查到。
  - ② **owner／摘要／理由分工**：分工大致成立——審查比語意、不比逐字（verify.md §9 只摘要並連 spec；README 同）。唯一缺陷是 owner 連結出了 repo 就斷（§2 第 5 條），屬「摘要指向哪裡」的問題，不是逐字同步的問題。
  - 結論（使用者 2026-10-01 裁定）：記為 **sample 1／inconclusive-positive**——兩段讓 proposal 的邊界讀起來較清楚，但真正發揮 single-owner／宣稱邊界作用的是 design D10 與 spec owner 規則，不是這兩段本身；不足以證明它們應成為所有 change 的固定段落。**不改** `templates/proposal.md`，下一個適合的 change 再 dogfood 一次（見 §6）。

## 6. Promote candidates → long-term learning

> 處置依使用者 2026-10-01 裁定：①② promote、③ 另開修正工作、④ 繼續觀察、⑤ 併入既有 worktree 工作項。
> ①② 共用一個上位原則——**先定義要證明的 claim，再設計有足夠辨識力的 oracle；機械化不等於有效，只有分得出正確與關鍵錯誤的機械判準才算證據**——但保留兩種失敗型態，不揉成一句格言。

- [x] 🟡 **① oracle discrimination：測試開跑前，先證明評分分得出每一條要抓的錯誤路徑。** 兩種不同行為若產生同一個可觀察結果，就拆成各對一個主張的案例；先用假報告讓 grader 對每條錯誤路徑回 DIFF，再派工。 → **Promote to memory** (type: feedback；已寫入，與②同一份：`feedback_claim_first_discriminating_oracle`)
  > **Why**: 本 change 三例同型：grader 對重複案例只取最後一段（注入重複仍 MATCH 22，ledger 第 116 行）；v1 回報格式讓「逐條判對、FINAL 寫錯」無從被分辨（ledger 第 77 行）；I3 單一案例下「A 被誤判成衝突」被 B 的 VIOLATION 吸收（ledger 第 123 行）。
  > **How to apply**: 任何盲測、fixture 評分或驗收腳本開跑前；列出可能的錯誤行為，逐一確認它們會改變評分讀到的欄位。

- [x] 🟡 **② proxy mismatch：驗收判準要對準宣稱，不對準方便量的代理指標。** 「結束碼 0」不等於歸檔成功、「逐行相等」不等於內容不變、「單一 FINAL 類別對了」不等於某條內部分支判對。 → **Promote to memory** (type: feedback；同上一份)
  > **Why**: 同一 change 三例：archive 中止仍回 0（`author-run.md`）；5.2 因 3 行空白差異未過字面判準，而 D7 的語意宣稱其實成立（ledger 第 102、103 行）；I3 分支在 22 題盲測中從未被觸發，FINAL 全對也證明不了它（tasks.md 3.1「證據限制」）。
  > **How to apply**: 寫 plan Acceptance 或 verify 腳本時，先寫出要證明的宣稱，再選一個「宣稱為假時一定會變」的觀測量。

- [ ] 🟡 **③ retrospective 模板的 skill 表仍列 `superpowers:writing-plans`，但 schema 的 plan instruction 已明寫不需要呼叫任何 skill。** → **另開修正工作**（product／template defect，不是長期經驗；修 source：`superpowers-bridge/templates/retrospective.md` §4 表格第 56 行，該列改為條件性說明或移除；不在本 change 動）
  > **Why**: 本文 §4 填表時，該列只能填 N/A 並引 schema 原文自證；schema 開頭列出的 apply-phase skills（`schema.yaml` 第 6–7 行）也不含它。照表填的人可能誤記成「跳過」，製造假 provenance。
  > **How to apply**: 登記為工作地圖上的獨立工作項（掛在 superpowers-bridge 下一代改造底下），由該工作項開 change 修模板。

- [ ] 📌 **④ proposal 的 `## Out of Scope`／`## Assurance Boundary` 兩段：sample 1／inconclusive-positive，不改模板。** → **One-off**（carry forward 到下一個 change 的 retrospective 重評）
  > **Why**: §5 D10 觀察：下游 artifact 沒有引用這兩段，真正發揮作用的是 design D10 與 spec owner 規則。
  > **How to apply**: 下一個用到這兩段的 change，在 retrospective 重答 D10 的兩題；再次證明 review 或 planning 真的用得到，才開 change 改 `templates/proposal.md`。

- [ ] 📌 **⑤ worktree 摩擦（9 例）併入既有工作項，不另立規則。** → **One-off**（已登記：`task-20260904-worktree-handoff-lifecycle`）
  > **Why**: 使用者 2026-09-30 裁定只記不修；長路徑一例另依 ledger 第 125 行「再有一台 Windows、CI 或新 worktree 撞到才升為 repo 路徑預算項」。
  > **How to apply**: 處理該工作項時，以本 change 的 9 例為實測輸入。
