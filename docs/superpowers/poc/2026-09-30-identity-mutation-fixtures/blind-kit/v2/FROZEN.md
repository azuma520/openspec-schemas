# 盲測器材凍結紀錄 v2（output contract repair，task 3.1 instrument repair）

凍結日期：2026-09-30（fix round 1 於同日完成，見下方「Fix round 1」節）。凍結範圍：`v2/prompt.md`、`v2/procedure.md`、`v2/grade.py`。這三份檔案在任何 v2 重跑（RED 重跑或 GREEN 重跑）開跑前不再變動。

修這一版的理由（user ruling 2026-09-30）：v1 的盲測 prompt 產生了一個回報缺陷——執行者在同一份報告裡，對某條檢查寫下 BLOCK/違規的判定，卻又手寫一行 `FINAL: PASS` 的最終結論（見 `blind-runs/green-r1/report-green-A.md`、`report-green-B.md`、`blind-runs/green-r2/report-green-A.md`、`report-green-B.md` 裡多處 `BLOCK 類別` 之後緊接 `FINAL: PASS` 的例子）；執行者也把類別字寫成簡體或簡繁混雜（`违规`、`違规`、`无法判定`），或寫非標準的每條檢查標籤（`BLOCK 類別: (none)`），使評分不可靠。v2 只修這個輸出契約，不動判斷邏輯、不動 fixtures、不動規則來源。

## SHA-256（fix round 2 之後的目前值；更早的值見「Fix round 1」「Fix round 2」節）

| 檔案 | SHA-256 |
|---|---|
| `v2/prompt.md` | `61871c23e2da1e504a7b68276fe2a566459b99119034d80099897a06c7ee5ca8` |
| `v2/procedure.md` | `fe431e4edf16f059120c64d65af7dc97854636364f61b9a5c77bdfa3e249c492` |
| `v2/grade.py` | `ebf174df491b2772a1b6a0bc64e82686e3a1602a8e939dec8b066502216e9adf`（fix round 2；round 1 值 `c9484c00…ebe0` 是 2026-09-30 官方評分當時使用的版本） |

## v1 → v2 diff summary（只改輸出契約）

`diff blind-kit/prompt.md blind-kit/v2/prompt.md` 與 `diff blind-kit/procedure.md blind-kit/v2/procedure.md` 的完整輸出見 task 報告；摘要如下——**只有輸出/回報契約變了，其餘（輸入怎麼給、怎麼找檢查對象、寫入類指令要用複本、天生不適用的判斷依據、禁止讀取範圍、GREEN 重新產生程序、已知限制）逐字沿用 v1**：

- 每條檢查的判定 token 從五種（`PASS`／`BLOCK`／`WARN`／`不適用於 fixture`／`無法判定`）收斂為四個固定 ASCII token：`PASS`／`BLOCK`／`WARN`／`NOT_APPLICABLE`（與 v1 的「不適用於 fixture」同義）。
- 移除獨立的每條檢查「BLOCK 類別」行（v1 的第 4 步、報告格式裡的 `BLOCK 類別: ...` 行）——這一行在 v1 是造成混寫的第二個自由格式來源。判斷 BLOCK 屬於「違規」或「無法判定」（或兩者）仍要做，但只彙整進案例層的 FINAL 行，不再逐條檢查另起一行。
- 每個案例唯一的權威結論行改成嚴格的兩種形式之一：`FINAL: PASS` 或 `FINAL: BLOCK | categories=<list>`，`<list>` 是 `VIOLATION`／`UNDETERMINABLE` 的逗號分隔、不含空格子集合，各 token 最多一次、不可為空、不可用其他語言或佔位字。v1 的 `FINAL: <PASS|BLOCK> categories={...}` 大括號形式、任何翻譯或簡體字、`(none)` 之類佔位字，在 v2 一律視為不合規輸出。
- `procedure.md` 只同步改了一處：「一律回報「不適用於 fixture」」改成「一律回報 `NOT_APPLICABLE`」——因為這句本身就是輸出格式指示。
- 標題加註 `v2`。除此之外每一段文字逐字相同（可用上面兩條 `diff` 指令自行核對）。

## 規則來源（與 v1 相同，v2 不改變這個變數）

- **RED**：仍是 `blind-kit/schema-red.yaml`（`git show 42c3d24:superpowers-bridge/schema.yaml`，已凍結，v1、v2 共用同一份）。
- **GREEN**：仍是 task 3.1 寫入 check 13 之後、當前 working tree 的 `superpowers-bridge/schema.yaml`。本次凍結時核對其 SHA-256：

  ```
  f2eea915b79bfb35f9d45bde937c7790ee950469f38aa9372893bce2ee3b2a7a
  ```

  與本 brief 指定的預期雜湊一致（未 BLOCKED）。

  （2026-10-01 後記：check 13 本體其後因 I3 分支互斥句修正；對最終規則檔 `a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504` 以同一份 v2 prompt／procedure 與 fix round 2 grader 重跑 GREEN，見 `../../blind-runs/v3-green/` 與 README §3。）

## `grade.py` 用法

```bash
python grade.py <report_file> <mapping_file> <readme_answer_key>
python grade.py --selftest   # 驗證 grader 本身：PASS、BLOCK 各類別組合、每一種不合規形式都被正確分類
```

輸出：對答案表裡每個 fixture 印一行 `MATCH` / `DIFF` / `NONCONFORMING_OUTPUT`，最後印總計。任何 FINAL 行不合規（缺、重複、格式錯、未知 token、非 ASCII、佔位字）一律 `NONCONFORMING_OUTPUT`，絕不猜測。

## 停用規則

若 v2 重跑仍出現同一類輸出不穩定（例如逐條判定與 FINAL 結論矛盾、類別字仍混寫語言或腳本、grader 判為 NONCONFORMING_OUTPUT 的比例異常高），**不做 v3**——回頭檢討是不是執行者本身（而非器材文字）的問題，交還使用者裁定，不再自行迭代 prompt 措辭。

## 已知限制（沿用 v1）

見 `procedure.md` 末段——「不要讀 kit 以外的檔案」只是指示，不是技術隔離；執行者的沙箱權限允許讀到 kit 以外的內容，這份器材的盲測性質建立在執行者遵守指示之上。

## Fix round 1（2026-09-30，review finding：round 0 的輸出契約本身有缺陷,不是執行問題）

**發現**：round 0 把每條檢查的判定收斂成四個固定 token（`PASS`／`BLOCK`／`WARN`／`NOT_APPLICABLE`）,拿掉了 v1 原本用來裝「這條檢查沒得出結論、但這條檢查自己的規則文字沒規定得不出結論要擋下」的那個獨立、non-blocking 的「無法判定」欄位。這使得凡是遇到這種情況的執行者,在四個 token 裡找不到位置可以放,只能塞進 `BLOCK`——而至少兩類真實案例會撞到這個洞：check 5（判定依據是 working-tree 狀態,曾被某位執行者誤判為不屬於 round 0 的 git-history NOT_APPLICABLE 範圍,結果對全部 22 個案例都手寫成獨立的「無法判定」而非 BLOCK）,以及 check 7 自己的規則文字（tasks.md 不存在時「無法判定……不因此 BLOCK」）。round 0 的四 token 集合會逼這類執行者把它們改記成 `BLOCK`,而 round 0 的評分模型是「最終判定必須與 RED baseline 相同」,這會把全部 22 個 RED 判定翻盤——違反「重跑必須重現原始 RED 判定」的前提。這個缺陷在 brief（controller 給的規格）本身,不是我的執行落差。

**修法（仍只動輸出契約,不動判斷邏輯、不動 fixtures、不動規則來源）**：

1. `prompt.md` 第 3 步新增第五個固定 ASCII token `NO_VERDICT`：嚴格定義為「檢查沒得出 PASS/BLOCK/WARN 結論,且這條檢查自己的規則文字沒有規定『得不出結論』要擋下」——`NO_VERDICT` 永遠不 BLOCK、永遠不貢獻任何 FINAL category；反過來,若規則文字明講得不出結論要擋下,執行者仍必須寫 `BLOCK`（並依第 4 步標注屬於「違規」還是「無法判定」）。沒有指名任何檢查編號——定義完全依「這條檢查自己的規則文字怎麼規定」判斷,通用於所有檢查。
2. `procedure.md` 的 `NOT_APPLICABLE` carve-out從只提「git 歷史」擴大成「git 狀態——commit 歷史或 working-tree 狀態,兩者皆屬此列」，恢復 v1 原本 carve-out 的實際涵蓋範圍（v1 procedure.md 本身就同時提「git 歷史」與「worktree 未提交變更與 commit range」兩種依據,round 0 的措辭誤窄化成只剩「git 歷史」一種）。同樣沒有指名任何檢查編號。
3. `grade.py`：確認不需要改動——grader 只讀 FINAL 那一行,從不檢視逐條檢查的 token,所以 `NO_VERDICT` 對 grader 的 FINAL 語法完全不可見。已在 docstring 加一段說明並在 `run_selftest()` 新增一個案例（一個 PASS 案例、其中一條檢查標成 `NO_VERDICT`）驗證這一點——自測結果見下方，全部 15 案例（含新案例）通過。

### Round 0 → round 1 hashes

| 檔案 | round 0 SHA-256（已作廢） | round 1 SHA-256（目前值,同上表） |
|---|---|---|
| `v2/prompt.md` | `469a94ef9c7ba00efcd7b480103303b7a61f89eada56249a0843a7903456294e` | `61871c23e2da1e504a7b68276fe2a566459b99119034d80099897a06c7ee5ca8` |
| `v2/procedure.md` | `2c6e44ab4e1a7a6c7a88673461410d361e3c91736083ef648ec0d01096062d9a` | `fe431e4edf16f059120c64d65af7dc97854636364f61b9a5c77bdfa3e249c492` |
| `v2/grade.py` | `ab348979b42c25d0422a688e22796eb3e805431d9ec22794c3d6eb7eb42919b3` | `c9484c00c4ac545af6e3046a91303c20d177f62b409b3a5b7a8b44e4e529ebe0` |

完整 round 0 → round 1 diff 見 task 報告 `task-instrument-v2-report.md` 的「Fix round 1」節。working-tree `superpowers-bridge/schema.yaml` 未受影響,雜湊仍是 `f2eea915b79bfb35f9d45bde937c7790ee950469f38aa9372893bce2ee3b2a7a`。

### 遺留項目

`blind-kit/v2/__pycache__/` 目錄是本次自測時 `python -c "import grade"` 產生的副作用,不屬於凍結集合,但本 session 的 rm 權限被拒（sandbox deny）,無法自行刪除。留給有 rm 權限的人清掉；它不影響 `prompt.md`／`procedure.md`／`grade.py` 三份凍結檔案的雜湊或內容。

## Fix round 2（2026-10-01，使用後修正：code review r1 P1）

**發現**（Codex code review r1）：`split_report_into_cases` 把同一個案例代號的多個 `## <case>` 區段存進字典時，後一段直接覆蓋前一段；被覆蓋的區段完全不經過 FINAL 檢查。Codex 實測：在官方 GREEN-A 報告前插入另一段寫 `FINAL: PASS` 的 `## case-11`，舊 grader 仍回報 `MATCH=22, NONCONFORMING_OUTPUT=0`。這是器材缺陷，不是規則或執行者的問題。

**修法**（只動 `grade.py`；`prompt.md`、`procedure.md` 不動）：`split_report_into_cases` 另外回傳重複出現的案例代號；`grade()` 對這些代號一律判 `NONCONFORMING_OUTPUT`（「case … has more than one section」），不評分。`run_selftest()` 新增一個走完整評分路徑的案例（同一代號兩段、前後結論矛盾）——修改前實跑為 `[FAIL]`（舊 grader 判成 MATCH），修改後通過；自測全部 16 案例通過。

**對既有結論的影響**（使用者裁定 2026-10-01：修器材、重評既有報告、不重派執行者；任何一份結果改變就停）：以 round 1 grader（`c9484c00…ebe0`，取自 HEAD）與 fix round 2 grader 分別評分三份官方報告，逐案例比對：

| 報告 | round 1 grader | fix round 2 grader | 逐案例相同 |
|---|---|---|---|
| `blind-runs/v2-green/report-green-A.md` | MATCH 22 / DIFF 0 / NONCONFORMING 0 | MATCH 22 / DIFF 0 / NONCONFORMING 0 | 是 |
| `blind-runs/v2-green/report-green-B.md` | MATCH 22 / DIFF 0 / NONCONFORMING 0 | MATCH 22 / DIFF 0 / NONCONFORMING 0 | 是 |
| `blind-runs/v2-replay/report-replay.md` | MATCH 5 / DIFF 17 / NONCONFORMING 0 | MATCH 5 / DIFF 17 / NONCONFORMING 0 | 是 |

三份報告各有 22 個案例區段、沒有重複代號，所以舊 grader 的缺陷在官方評分時沒有被觸發；修正後正式結果不變。

| 檔案 | round 1 SHA-256（官方評分時使用） | round 2 SHA-256（目前值） |
|---|---|---|
| `v2/grade.py` | `c9484c00c4ac545af6e3046a91303c20d177f62b409b3a5b7a8b44e4e529ebe0` | `ebf174df491b2772a1b6a0bc64e82686e3a1602a8e939dec8b066502216e9adf` |
