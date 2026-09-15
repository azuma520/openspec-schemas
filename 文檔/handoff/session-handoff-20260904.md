# Session Handoff — 2026-09-04

## Session 08:17

### 一、本 session 主題

**跨午夜的收尾段。** 這個 session 的實質工作記在 `session-handoff-20260903.md` 的 `## Session 17:18` 區塊（loosen-plan 的 verify / retrospective / 執行報告 + doc gate 三輪）；使用者在 commit 確認的提問上隔夜才回覆，於是收尾動作落在 09-04 清晨。本區塊只記 09-04 這一段，**不重貼前一份**。

### 二、完成事項

- **`f77ae02` `chore(work-map): register the loosen-plan close-out task as NEXT`** —— 把 `task-20260903-loosen-plan-close` 入庫（archive / 刪 SDD 工作區 / push + PR / 補驗 9.1 CI 四件事）。經 register writer 寫入並 readback；`verify-last` exit 0、無 AI attribution trailer。
- **結算 marker 寫入**（`settled`, `f77ae02`），已確認被 `.gitignore:41` 忽略、不進 commit。
- **確認工作目錄乾淨**：只剩刻意排除的 `文檔/handoff/session-handoff-20260903.md`（handoff 屬 main，不進本 branch）。
- **`02a3385` `feat(schema): a recorded check result goes stale when its input changes`** —— 使用者裁定 carried-forward #6（檢查新鮮度）為**已實測的假放行**，須在出貨前補到「當前架構真正能提供的保證程度」。`verify` 指令加入 freshness 要求：已記錄的結果描述的是檢查當下的 artifact，之後改動 `tasks.md` / `plan.md` 會使**由該檔算出的每一筆結果**變成 STALE、必須在 archive 前重跑。**受影響集合由各檢查的輸入推導**（動 `tasks.md` → check 2、8–11、12；動 `plan.md` → check 7、12），並明文限定範圍在這兩個檔。**嚴格定位為 agent-executed**：不計算也不比對 digest，各表面不得宣稱機械保證。鏡像到模板、雙語 README 設計觸點 #3、`tdd-evidence-contract` spec（條文 + 新 scenario），兩份紀錄同步，執行報告加**有日期的後記**而非改寫。schema hunk 純新增（刪除 0 行），guardrail 8 成立。
- **兩輪 targeted review**：第一輪抓到 🔴 —— 規則自己的列舉只涵蓋「本 change 新增的檢查 8–12」，漏掉同樣讀那兩個檔的 **check 2 與 check 7**（與 R32 同型：把列舉當成 scope）。修正為按輸入推導後，第二輪 `✅ Mergeable`、🔴 零；第二輪 reviewer 自行重導整張映射表，並讀了安裝好的 OpenSpec CLI parser 原始碼確認 check 1 不讀 `tasks.md`。
- **`/end-session` 第六步與 Anchor #4 衝突已浮出並繞開**：`/end-session` 要求自己跑 `git commit`，但 Anchor Register #4 的授權清單是封閉的（`/push-ci`、`/smart-commit --execute`、`/epic-merge`），`/end-session` 不在其中。未自行開例外，改走 `/smart-commit --execute`。**此衝突尚未有裁定，列為後續待處理。**

### 三、未完事項 / 接力棒

與 09-03 區塊同一份，未變動 —— **`task-20260903-loosen-plan-close`（狀態 `NEXT`）**：

1. `openspec archive` —— Windows 目錄鎖 3/3 複現，`cp -r` → `diff -r` 驗 IDENTICAL → **`rm -rf` 委派使用者**
2. 刪 `.superpowers/` SDD 工作區（執行報告已進版控，安全）
3. `finishing-a-development-branch` → push + PR（apply step 6，本 repo 首次）
4. push 後補驗 **task 9.1 的 live Actions run**

**待使用者裁定**：`verify.md` carried-forward #6 —— schema 沒有任何一層擁有「檢查新鮮度」。

### 四、洞見 / 反省

**【紀律接力】**

- [#觀察] **一個 session 的「今天」可以跨日，而 handoff 的檔名綁的是收工當下的日期。** 本次實測：handoff 內容寫於 09-03 17:18 並存進 0903 檔，但收尾 commit 落在 09-04 08:17，Stop hook 因此 block 並要求 0904 檔。**attribute:** A7 檔名 schema 綁日期、Stop hook 依當下 wall-clock 檢查。**propose action:** 這不是缺陷、是規則按設計運作；正確處置是**在今日檔補一個接續區塊並指回前一份**，而不是把 0903 的內容複製過來 —— 複製會讓同一件事在兩處各有一份「原始紀錄」，日後無從判斷哪份是真的。

- [#反] **規則執行到位，目的沒有達成 —— handoff 差點跟著 worktree 一起消失。** 使用者的裁定「handoff 屬 main、不得進這支 branch」是對的（先前六份確實都在 main 的歷史裡），我也一路忠實排除。但**漏的是下半句**：不進這支 branch，那要進哪裡？兩份 handoff 因此只存在於 worktree 磁碟上、不在任何 commit 裡，而 worktree 在 push + PR 之後會被移除 —— 未追蹤檔案一刪即永久消失。同時，下個 session 若在主目錄開工，讀到的最新 handoff 會是 `20260902`，**整整兩天的交接內容讀不到**。**attribute:** 這與本 session 剛補的 freshness 缺口同型 —— 每一步都正確，但沒有任何一層負責「讓結果落到它該在的地方並保持有效」。**propose action:** 已止血（複製回主目錄）。使用者裁定**制度另開 change**：worktree → main 的 handoff lifecycle（owner 是誰、哪個階段負責 transfer、誰驗證成功、teardown 是否該 block、多 worktree / main 不乾淨怎麼辦）屬流程契約，不在 loosen-plan 收尾時順手改。

**【當日洞見】**

- **「現在救資料；之後改制度」是一條可重複使用的判準。** 使用者裁定：**已知會造成資料遺失或錯誤放行的風險，先用最小方式止血；要把止血方式升級成系統長期規則，再另外設計。** 本 session 兩次命中同一形狀 —— ① freshness：已發生假 PASS → 先補一句最小 instruction，digest-based 機械版另開 change；② handoff：檔案可能遺失 → 先搬回 canonical location，lifecycle / teardown guard 另開 change。兩次的共同點是**拒絕在收尾時順手擴張**，同時也拒絕「等新 change 再說」而讓已知風險留著。
- **等待使用者回覆的時間會被計入 session 的跨度，而不是被排除。** 這決定了 handoff 的日期歸屬 —— 對「一次工作」的直覺切法（同一串對話＝同一天）與檔名規則的切法（收工當下的日曆日）在跨午夜時會分岔。記下來是因為它只在跨午夜時才看得見，而那正是最容易把兩份紀錄搞混的時刻。

### 五、檔案異動

錨來源：延續 09-03 區塊的視窗（共用 per-cwd 時間戳 N=3h，起點 2026-09-03T14:58:43）——本區塊僅新增下列一筆

```
02a3385 feat(schema): a recorded check result goes stale when its input changes
M	docs/superpowers/retrospectives/2026-09-03-loosen-plan-execution.md
M	openspec/changes/loosen-plan/retrospective.md
M	openspec/changes/loosen-plan/specs/tdd-evidence-contract/spec.md
M	openspec/changes/loosen-plan/verify.md
M	superpowers-bridge/README.md
M	superpowers-bridge/README.zh-TW.md
M	superpowers-bridge/schema.yaml
M	superpowers-bridge/templates/verify.md

f77ae02 chore(work-map): register the loosen-plan close-out task as NEXT
M	workflow-harness/work-map.jsonl
```

未追蹤且刻意排除：`文檔/handoff/session-handoff-20260903.md` 與本檔（handoff 屬 main）。

⚠️ **兩份 handoff 的落點問題已於本 session 末發現並止血** —— 見「四、洞見」。它們原本**只存在於 worktree 磁碟上、不在任何 commit 裡**，而 worktree 在 push + PR 後會被移除；已複製回主目錄 `文檔/handoff/`，待在 main 上以既有受控流程 commit。

**無專案資料夾**（`artifact_paths children --key projects_dir` 回空）→ 專案 Changelog 這步 skip。

### 六、下一步建議

1. **`openspec archive`** —— `cp -r` + `diff -r` 驗 IDENTICAL，然後**請使用者跑 `rm -rf openspec/changes/loosen-plan`**。CLAUDE.md 已載明別先試 `mv`。
2. **刪 `.superpowers/` SDD 工作區** —— SDD Finish 步驟要求；執行報告已搬進版控故安全。
3. **`finishing-a-development-branch` → push + PR** —— apply step 6，本 repo 首次真正 dogfood。push 前確認 `文檔/handoff/` 仍在 branch 外。
4. **push 後補驗 task 9.1 的 live Actions run**，回填 `verify.md` §10 的 owed verification。
5. **裁定 carried-forward #6**（schema 的檢查新鮮度缺口）—— 決定 v2 是否帶著一個已知結構性缺口出貨、以及要不要開新 change。
