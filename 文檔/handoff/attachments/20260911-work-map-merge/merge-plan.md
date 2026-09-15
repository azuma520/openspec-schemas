# work-map 合併差異盤點與收尾計畫（2026-09-11）

> 盤點時間：2026-09-11 09:31。**本文件只做盤點與計畫，未執行任何合併、未改任何 repo 檔案。**
> 產出時的 HEAD：main `98cc5e2`、worktree-loosen-plan `b07d571`、merge-base `5aa19bf`。
> 所有 git 寫入動作皆列為「委派使用者執行」——AI 不跑 add / commit / merge / push。

## 0. 一句話結論

兩邊的 work-map 是**純新增對純新增**、零筆內容相衝；`git merge` 會報一個衝突，但那是
「兩邊都在檔尾 append」造成的位置衝突，解法是兩塊都留、刪掉標記，**不需要任何取捨判斷**。

## 1. 差異盤點（證據）

量測方法：以 `git show <ref>:workflow-harness/work-map.jsonl` 取三個版本（merge-base / main HEAD /
worktree HEAD），逐行 `json.loads` 後以 `id` 為鍵比對。

| 版本 | 記錄數 |
|---|---|
| merge-base `5aa19bf` | 13 |
| main `98cc5e2` | 14（+1） |
| worktree `b07d571` | 20（+7） |
| 合併後應為 | **21** |

**兩邊都有且逐欄相同：13 筆**（即 merge-base 的全部，兩邊都沒動過任何一筆）。
**兩邊都有但內容不同：0 筆。**

只在 main 有（1 筆）：

| id | status |
|---|---|
| `task-20260910-task-context-pilot` | DOING |

只在 worktree 有（7 筆）：

| id | status |
|---|---|
| `task-20260903-loosen-plan-close` | DOING |
| `task-20260904-worktree-handoff-lifecycle` | TODO |
| `task-20260904-spec-contradiction-cleanup` | DONE |
| `task-20260904-reviewer-verdict-delivery` | TODO |
| `task-20260907-fix-v2-blocking-defects` | DOING |
| `task-20260907-end-session-commit-delegation` | TODO |
| `task-20260908-author-surface-gate-alignment` | TODO |

## 2. 衝突的實際形狀

`git merge-tree --write-tree main worktree-loosen-plan` 的結果：**整個合併只有一個衝突檔**，
就是 `workflow-harness/work-map.jsonl`。用 `git merge-file` 重現後，衝突區塊長這樣：

```
1-13 行   共同的 13 筆（無衝突）
<<<<<<< main
14 行      task-20260910-task-context-pilot
=======
15-21 行   worktree 的 7 筆
>>>>>>> worktree
```

兩側沒有任何一筆 id 重疊，所以**「兩塊都保留」就是正確且無損的解**。

## 3. 其他檔案不會衝突（已查證）

以 merge-base 為基準列出兩邊各自動過的檔案並取交集：

- main 自 merge-base 以來動過 3 個檔：兩個 research 文件 + `work-map.jsonl`。
- worktree 自 merge-base 以來動過 83 個檔（含未 commit）。
- **交集只有 `workflow-harness/work-map.jsonl` 一個。**

## 4. 兩個容易被誤判的點

**(a) 換行符差異是假警報。** main 的工作區檔案是 CRLF、worktree 的是 LF，看起來像整檔都不一樣；
但三個版本的 **blob 全是 LF**（`git show` 出來逐位元組驗過），CRLF 只是 `core.autocrlf=true` 在
checkout 時換的，`git add` 會正規化回去。`workflow-harness/**` 不在 `.gitattributes` 的任何一條規則裡，
但因為 blob 已經是 LF，這件事對本次合併零影響。**不要為了它去動 .gitattributes。**

**(b) 剩下那個 `.superpowers/` 引用不是漏網之魚。** worktree 工作區的 work-map 還有 1 處 `.superpowers/`，
在 `task-20260903-loosen-plan-close` 這筆裡，內容是「刪 .superpowers/ SDD 工作區」——那是**還沒做的步驟**，
不是過期路徑引用。該目錄目前確實還在磁碟上。**不要把它一起改掉。**

## 5. 合併必須排在「worktree 的 work-map 提交」之後

worktree 的 `work-map.jsonl` 目前有一處**未 commit**的修正：使用者 09-11 用 `sed` 把
`task-20260908-author-surface-gate-alignment` 裡的報告路徑從 `.superpowers/sdd/plan/` 改成永久副本
`docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/`。

這個修正**只在工作區、不在 `b07d571`**。若在提交它之前就合併，合併結果會帶著舊路徑進 main，
而且不會有任何錯誤訊息。所以順序是硬的：**先 smart-commit worktree，再合併。**

## 6. 合併結果已預先驗證（唯讀）

在 scratchpad 沙盒裡組出合併候選（13 共同 + 7 worktree + 1 main），用**真的 work-status 引擎**跑過：

- 21 筆，id 無重複
- `parent` 全部指得到，無指向不存在的 record
- 關係無環
- 無「上層已結案而底下仍未完」
- 引擎完整性輸出只有既有那個 `evidence` 未知欄位的前向相容警告（合併前就有，與合併無關）

⚠️ 這次驗證用的是 worktree **HEAD** 版，所以候選檔裡仍帶第 5 節說的舊路徑。合併照本計畫的順序做
（先提交再合併）就不會有這個問題；合併後請重跑一次 `/work-status` 當作終驗。

## 7. 收尾順序（承 09-10 使用者拍板，本次盤點只補進 work-map 這一段的細節）

每一個 git 寫入動作都等使用者核准後由使用者執行。

1. **smart-commit worktree** — 含 3 個未追蹤的 review 報告，以及第 5 節那個 work-map 修正。
2. tasks.md 若有動 → verify 重跑。
3. retrospective 補記。
4. **archive** — Windows 目錄鎖，走 `cp -r` + `diff -r` 驗 IDENTICAL + 委派使用者 `rm -rf`。
5. **併 main** — 見下方 8。
6. **push** — main 目前領先 `origin/main` 2 個 commit（`fc8f552`、`98cc5e2`）尚未推。

## 8. 併 main 的兩條路（**需要使用者拍板**）

work-map record `task-20260903-loosen-plan-close` 寫的是「走 push + PR（本 repo 首次）」。
目前 `worktree-loosen-plan` 是純本地分支、沒推過，也沒有開著的 PR。衝突在哪裡解，決定路線：

**路線甲：先在分支上解，再開 PR。** 在 worktree 執行 `git merge main`，當場解掉那個 append 衝突，
之後推分支、開 PR 時是乾淨的快轉。好處是衝突在本機解、PR 頁面乾淨、審查看到的就是最終狀態；
代價是分支歷史多一個 merge commit。

**路線乙：直接在 main 上合併，不走 PR。** 在 main 執行 `git merge worktree-loosen-plan`，解衝突後推。
好處是少一層流程；代價是放棄了那筆 record 自己寫的「push + PR、本 repo 首次」這個意圖——
那是當初刻意要練的一步。

我的建議是**路線甲**，理由是它同時滿足「衝突在本機解」跟「走一次 PR」兩件事，而那筆 record 把
PR 明文寫成本次的目標之一。但這條歸使用者決定。

**衝突的解法兩條路一樣**：保留 `<<<<<<<` 與 `>>>>>>>` 之間的兩塊全部內容、刪掉三行標記。
建議的擺放順序是 worktree 的 7 筆（0903–0908）在前、main 的 1 筆（0910）在後，讓檔案維持日期遞增。
解完後跑 `/work-status`，看到 21 筆、完整性只剩既有那個 `evidence` 警告，就算對。

## 9. 我沒查的

- push 前 D5「v2 未發版」的前提要複驗。本次順手看了一眼 `git tag -l` 是空的，但那是 09-11 早上的狀態，
  push 當下要重看。
- 兩邊 `backlog.md` 也各自存在（worktree 有一份），本次盤點**只涵蓋 work-map**，沒比對 backlog。
  不過第 3 節的交集查證顯示 `backlog.md` 不在 main 動過的檔裡，所以合併不會衝突。
