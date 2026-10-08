# Retrospective: task-prefixed-plan-headings

> Written: 2026-10-08 (after verify passed — ⚠️ PASS WITH WARNINGS)
> Commit range: `737aa56..0b11be5`（實作至 3.7 加 rollback 佔位字串）；其後的 3.8 SHA 替換、最後整體審查的修正、verify 與本檔尚未 commit，隨下一個 commit / 歸檔提交
> Worktree: `.claude/worktrees/task-prefixed-plan-headings`（branch `feat/task-prefixed-plan-headings`，已 push 到 origin，指向 `0b11be5`）

---

## 0. Evidence

- **Commit range**: `737aa56..0b11be5`（1 commit，使用者當次授權）。實作期間刻意不讓子代理 commit（見 §3 R1），所以只有一個實作 commit
- **Diff size**: `git diff --shortstat 737aa56`（只算已追蹤檔案在工作區的改動，不含尚未追蹤的 verify.md 與本檔）→ 34 files, +499 / −97（寫作當下）；`0b11be5` 本身 33 files, +409 / −90
- **Tasks done**: 18/18（`grep -cE '^\s*- \[x\]' tasks.md` → 18；`- [ ]` → 0）
- **Active hours**: apply 階段約 1 小時（SDD 工作區建立 10:46，本檔寫於 11:45，同日）。brainstorm / design / specs / tasks / plan 在前兩個 session 完成，不計入
- **Subagent dispatches**: 19 次新派遣 + 4 次續派（resume）。新派遣：實作 4（fixtures、schema、文件、最後修正）、任務審查與複審 8、盲測執行者 6（red-v3、v3-supp、green-v4、v4-25、green-v4-r1、v4-25-r1）、verify 執行者 1。全部指定模型（實作與重要審查 opus，盲測與小範圍複審 sonnet）
- **New external dependencies**: none
- **Bugs encountered post-merge**: n/a — 尚未 merge
- **OpenSpec validate state at archive**: 歸檔前尚待最後一次確認。apply 期間：本機 CLI 1.3.1 在乾淨專案 `openspec schema validate superpowers-bridge` pass、`openspec schemas` 列得出（task 4.1）；verify check 1 記 `openspec validate --all` 6/6 valid。`validate-schemas.yml` CI 未在 branch 上觸發（只在 main / PR / 手動），**不可說 CI 綠**
- **Test coverage signal**: instruction 層的行為證據，agent 執行的盲測，不是自動化測試。2.2：f14–f16 各一組 RED（改前條文）+ GREEN（改後條文），3/3 方向正確；2.5：f17–f23、f5、f8、f9 共 10 份 v4 判定 10/10 符合凍結預期；補充：f17–f22 的 v3 判定 6/6 符合。完整紀錄在 `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md` § 2026-10-08 盲測紀錄。另：上游 `task-brief`（Superpowers 6.4.1）對本 change 的 plan.md 抽出 1.1、1.2、1.3、4.2，與原文逐行相同（task 4.2）；`version-check.yml` 手動觸發 run `37723513752` success，讀到 `OpenSpec=1.14.0, Superpowers=v5.1.0`

Commit chain (時序):

```
737aa56 docs(openspec): add plan for task-prefixed-plan-headings; record the session
0b11be5 feat(superpowers-bridge): recognise Task-prefixed plan entries; schema major 4
<下一個 commit：3.8 SHA、最後整體審查修正、verify、retrospective>
<archive commit>
```

---

## 1. Wins

- [evidence: tasks.md 2.2 RED/GREEN；fixtures README § 2026-10-08 盲測紀錄] **RED 真的在改條文之前取得。** 先建 fixtures、先用改前的 check 12 盲測，再讓子代理改 schema。f16 的 RED 是「v3 判 PASS」——正確答案是 BLOCK——這種「通過才是錯」的方向，只有照 tasks.md 開頭的四條邊界逐案寫預期 vs 實際才不會寫反。
- [evidence: progress ledger Ruling R2、R3] **pre-flight 掃描在動工前抓到 design 表格的設計錯誤。** D7 把 `##1.1` 與 ` ## 1.1` 寫成同一份 fixture；合在一起在 v3 會收到兩次 `1.1`、被第一階段擋下，與凍結的「v3 PASS」對不上。拆成兩份（R2）、near-miss 拆三份（R3）都在派工前決定。
- [evidence: 盲測 v3-supp] **趁改條文前多跑一次補充盲測，把「這是破壞性變更」從推論變成觀察。** f18、f19 的 v3 PASS 原本只是作者照字面推的，審查還質疑過 CommonMark 讀法；改前跑一次 6/6 符合，之後就再也跑不到舊條文。
- [evidence: 任務審查 g2、g3、最後整體審查] **獨立審查一再抓到「說過頭」的句子**：check 12 說要「與上游劃分任務方式一致」（只有 fence 一致）、S11 寫上游「只認 `## Task N`」（上游任何層級都認）、遷移說明寫 fence 錯位「只會」表現成缺鍵、roadmap「只有 task-brief 認得」。這正是本 change 的規格（REQ-4 guidance 只能宣稱 recognition）要防的同一類錯。
- [evidence: 3.8 checkout；`git log -S'version: 4'`] **rollback SHA 實際 checkout 驗過**，用暫時 worktree 不動目前分支；之後 push 後再用 `merge-base --is-ancestor` 確認遠端可達。
- [evidence: run 37723513752] **3.5 被審查點出只完成一半後，先取消勾選、push 後補跑才勾回**（R13），沒有讓 tasks.md 的勾選說得比實際多。

## 2. Misses

- 🟡 [painful | evidence: 最後整體審查 Important 1、2] **盲測證據一開始只放在會被刪掉的地方。** 結果只寫在 git-excluded 的 SDD ledger 與 scratchpad；fixtures README 還留著 task 1.3 寫的「尚未盲測」，跑完之後沒有任何 task 負責更新——等於把 `loosen-plan` 弄丟證據的情況重演一次，到最後整體審查才補進 tracked 檔。根因是 plan 的 2.5 只寫「recorded」沒寫記在哪（§3、§6）。
- 🟡 [painful | evidence: g2 fix round；green-v4 → green-v4-r1] **check 12 改字之後綠燈要整組重跑。** 審查要求修掉 check 12 理由句的過度宣稱，條文 sha 變了，GREEN 與 2.5 都重跑一次；最後整體審查又建議加版本註記，這次用 R15 延後，避免第三次重跑。條文與證據綁 sha 是對的，但代價是後期的措辭修正變貴。
- 🟡 [painful | evidence: g3 review Important 1、2] **design D8 的連動檔案清單漏了兩處**：根目錄 README 的 bridges 表狀態欄（上一次升 major 有改，commit `05fd2f8`），以及 D6 自己要求寫明的「不可 squash / rebase」前提。都是審查抓到、R9 與最後修正補上。
- 🟡 [painful | evidence: verify 執行者回報的待處理事項] **apply 期間讓已安裝副本落後**：4.1 同步後，最後修正又改了 bridge README，verify 才發現副本不同步。每次動 `superpowers-bridge/` 之後都要重新同步，這條在 CLAUDE.md 有寫，但沒有掛在 apply 流程上。
- 📌 [nit | evidence: fixtures README § 2026-10-08 盲測紀錄「協定偏差」] 盲測執行者一次拿 3–10 個 case 目錄，不是「一次只交付一份 fixture」。每個 case 仍獨立、名稱中性、看不到 README，但與文字規定不符，已照實記錄。
- 📌 [nit | evidence: v4-25-r1 執行者報告] v4 check 12 條文直接舉出 ` ## 1.1`、`##1.1`、`## task 1.1`、`1.1a` 等寫法當例子，f18–f22 的盲測因此是「對照例子」而非「套用通則」，鑑別力比 f14–f16、f23 弱。
- 📌 [nit | evidence: Ruling R3] REQ-4-S6 的 `## Tasks 1.1`、`## Task1.1`，以及 S5、S8、S9、S10 沒有 fixture。

## 3. Plan deviations

| Plan task | What changed | Why |
|-----------|--------------|-----|
| 全部 | 子代理不 commit；審查用工作區 diff，不用 commit 範圍；整個實作只有一個 commit（R1） | 本 repo 的 Anchor Register #4 規定 commit 要使用者當次授權；SDD 原本的「實作者自己 commit」會違反 |
| 1.2 | `##1.1` / ` ## 1.1` 拆兩份（f18、f19）；near-miss 拆三份（f20–f22）（R2、R3） | 合併的 fixture 在 v3 會被重複鍵擋下，或讓兩種錯誤接受的寫法偽裝成預期的 BLOCK |
| 2.2 | GREEN 跑了兩次，以 green-v4-r1 為準 | 審查要求修 check 12 理由句的過度宣稱，條文 sha 改變 |
| 2.5 | 同上重跑 v4-25-r1；另加 v3-supp 補充盲測（tasks 未要求） | 讓破壞性變更的 v3 判定有觀察證據 |
| 3.3 / 3.4 | 範圍外多改根目錄 README 的 bridges 狀態欄（R9） | 上一次升 major 有改，D8 漏列 |
| 3.5 | 一度取消勾選，push + workflow_dispatch 後才勾回（R13） | acceptance 有 push 後的一半 |
| 3.6 | CLAUDE.md 多寫 rollback SHA 的 merge 前提與重算步驟、CI 失敗的第二條路徑 | 最後整體審查 Important 3、Minor 5 |
| 3.8 | SHA 替換由 controller 直接做（R12） | 4 個相同的機械式替換，以 grep 驗證，最後整體審查覆蓋 |
| 4.2 | 在任何修改之前就先跑 | 不依賴其他 task；越早證明 Task 寫法能被上游抽出越好 |
| 延後 | check 12 理由句加「as of Superpowers v6.4.1」不做（R15） | 再改 check 12 會讓 GREEN / 2.5 的 sha 綁定失效 |

## 4. Skill / workflow compliance

| Skill                                            | Used |
|--------------------------------------------------|------|
| superpowers:brainstorming                        | ✓（前一個 session，產出 brainstorm.md） |
| superpowers:using-git-worktrees                  | ✓（以 `git worktree add … HEAD` 建立再用 `EnterWorktree` 進入；刻意不用預設的 `origin/main` 起點，因本機領先遠端 3 個 commit、plan 在其中） |
| superpowers:subagent-driven-development          | ✓（ledger、pre-flight 表、每組任務審查 + 修正複審、最後整體審查 + 一次修正 + 複審） |
| superpowers:test-driven-development (✓ only if the skill was explicitly invoked; write `N/A — annotation-driven` when TDD discipline came from the `TDD:` annotations in `tasks.md` and their RED/GREEN evidence instead) | N/A — annotation-driven（2.2 為唯一 `applicable`，RED/GREEN 由盲測取得） |
| (structural via SDD) superpowers:requesting-code-review | ✓（最後整體審查用其 `code-reviewer.md`，opus） |
| superpowers:finishing-a-development-branch       | 待執行（archive 之後） |

> 本表只列兩類項目:(1) schema 明確要求呼叫的 Superpowers skill——
> `brainstorming`(由 `brainstorm` artifact 要求)與 apply pre-flight 要求的
> `using-git-worktrees`、`subagent-driven-development`、`finishing-a-development-branch`;
> (2) schema 要求落實、retrospective 必須記錄其執行情況,但 schema 本身不直接呼叫的
> Superpowers 紀律——`test-driven-development`(由 `tasks.md` 的 `TDD:` 標註與
> RED/GREEN 證據承載)與 `requesting-code-review`(透過 subagent-driven-development
> 結構性達成)。

### Deliberately Skipped Skills

（沒有刻意跳過的 skill。`finishing-a-development-branch` 尚未執行是時序——它在 archive 之後——不是跳過。SDD 內部有一處偏離：實作者不 commit，見 §3 第一列與 R1；這是 repo 規則優先於 skill 步驟，不是跳過 skill。）

## 5. Surprises

- **design 的「本 repo 三種情況都沒有」在 apply 後變成假的**：新加的 fixtures 正是故意寫成那三種情況。apply 時只改了 bridge README（en + zh-TW）的遷移說明，改成「fixtures 以外沒有」；design D2、D4 與 proposal 的同類說法漏改，到文件審查才被指出，之後補註「掃描早於 fixtures」。
- **v3 條文照字面真的會收 `##1.1` 和 ` ## 1.1`**：原以為可能只是條文漏寫；盲測執行者照字面讀確實收了，所以第三項 breaking 是真的行為改變。
- **本機 OpenSpec CLI 是 1.3.1，Compatibility 表 v4 列寫 1.14.0**：v4 列沿用 v3 列的值，本機驗證並未用 1.14.0。
- **`validate-schemas.yml` 不在 feature branch 的 push 上觸發**：原以為 push 後兩支 workflow 都會跑。
- **`rm -rf` 被權限擋下**：同步副本改用覆蓋複製 + `diff -r` 驗證；CLAUDE.md 已記載 AI 的 `rm` 會被擋，但寫的是 archive 情境。

## 6. Promote candidates → long-term learning

- [ ] 🟡 **plan 寫「recorded」的驗收條件要寫明記在哪個 tracked 檔** → **Promote to schema**（`plan` instruction 的 Acceptance criteria 說明）
  > **Why**: 本 change 2.5 只寫「recorded … beside the frozen expectation」，結果只記在 git-excluded 的 SDD ledger；`loosen-plan` 也是同樣原因弄丟盲測證據（fixtures README § 證據來源）。兩次。
  > **How to apply**: 寫 plan entry 時，凡驗收條件是「留下紀錄 / 證據」，寫出它要落在哪個進版控的檔案；reviewer 看到沒寫位置的「recorded」就當成缺陷。
- [ ] 🟡 **任何「狀態宣告」寫進 tracked 檔時（尚未盲測、已驗證、CI 綠），同時登記「誰在什麼事件後負責更新它」** → **Promote to memory**（type: feedback）
  > **Why**: task 1.3 寫的「f14–f23 尚未盲測」在盲測跑完後沒有任何 task 更新，變成假陳述，到最後整體審查才抓到。
  > **How to apply**: 寫「目前尚未 X」這類句子時，檢查 tasks.md 有沒有一個之後的 task 會讓它過期；有就在那個 task 加一句更新它。
- [ ] 🟡 **改了 `superpowers-bridge/` 之後、跑任何 openspec 指令之前，重新同步已安裝副本** → **Promote to project CLAUDE.md**（「本 repo 自己吃自己的 schema」節）
  > **Why**: 本 change 4.1 同步後又改了 README，verify 才發現副本不同步。
  > **How to apply**: verify、archive 前固定跑一次 `cp -R superpowers-bridge/. openspec/schemas/superpowers-bridge/` + `diff -r`（`rm -rf` 會被擋，用覆蓋複製）。
- [ ] 📌 **條文綁 sha 的證據，在後期措辭修正時要先算重跑成本再決定修不修** → **One-off**（本次以 R15 處理）
  > **Why**: green 已重跑一次；再加一個版本註記會第三次重跑。
  > **How to apply**: 僅當一個 change 的證據綁定被測條文的 hash 時適用。
- [ ] 📌 **升 schema major 的連動清單要包含根目錄 README 的 bridges 狀態欄** → **Promote to project CLAUDE.md**（「跨檔耦合」表）
  > **Why**: D8 漏列，上一次升 major（`05fd2f8`）有改。
  > **How to apply**: 下次升 major 時照跨檔耦合表逐列核對。
