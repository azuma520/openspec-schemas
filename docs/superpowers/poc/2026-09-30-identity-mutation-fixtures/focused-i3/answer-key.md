# post-fix I3 focused acceptance — 2 paired cases：預期答案

> ⚠️ 作者端材料，**不交給執行者**。本檔在派工前凍結（SHA-256 記在 `../sdd-ledger.md` 對應段落），派工後不再修改。

- 日期：2026-10-01
- 性質：盲測組外、check 13 修正後的**定點驗收**（post-fix focused acceptance），兩個案例成對設計。**不是**凍結 22 案例盲測組的第 23、24 題，也不改變那組的範圍、雜湊或結論。
- 受測規則：最終 HEAD 的 `superpowers-bridge/schema.yaml`（check 13 含 I3 分支修正，見 `../blind-kit/v2/FROZEN.md` 2026-10-01 後記）。
- 器材：沿用凍結的 `../blind-kit/v2/prompt.md`、`procedure.md`、`grade.py`（fix round 2），三者不改。
- 評分：`grade.py` 只讀每個案例的 `FINAL` 行；下表就是它讀的答案表（欄位形狀與 `../README.md` §1 相同）。

## 為什麼是兩個案例

只用第一個案例時，「A 被誤判成編號衝突」與「正確判定」會得到同一個 `FINAL`——B 本來就貢獻 `VIOLATION`，誤判多出的 `VIOLATION` 被吸收掉，評分讀不出差別。第二個案例拿掉 B 的違規，讓這個誤判路徑在 `FINAL` 上可見。兩個案例各對一個主張：

| 案例 | 主張 |
|---|---|
| `i3-mixed-synced-and-violation` | A 已同步使歸檔預演中止，但 B 只依賴歸檔前狀態就能判定的違規仍要保留（check 13 是依 capability、依證據依賴局部退化，不是整條停止） |
| `i3-synced-only` | A 已同步進 main 的 `REQ-1` 不得被重新判成編號衝突或任何違規（13.B SYNCED CAPABILITY：違規不得以同步後的 main spec 為基準） |

## 共同基底

兩個案例都從 `../fixtures/v12-added-below-max` 複製而來（`token-auth` 主 spec 持有 REQ-1、REQ-2、REQ-5；`session-policy` 只有 REQ-PB），change 仍叫 `update-token-auth`，另外：

- **A＝`session-policy`，已同步**：delta 以 ADDED 新增 `REQ-1 Session absolute lifetime`（含 `REQ-1-S1`），主 spec 已含逐字相同的這條 requirement——check 3 應記為「✓ Already synced」。若不套用同步規則，它會被讀成「ADDED 的 ID 主 spec 已持有」的衝突，且 `REQ-1` 不大於目前最大數字 ID 1。
- **proposal 多一行**：兩個案例的 `proposal.md` 都在 What Changes 與 Modified Capabilities 各加一行 `session-policy`，讓 proposal 與實際 delta 涵蓋的 capability 一致。這行只存在測試案例中；依既有慣例，案例檔本身不列入正式文件審範圍（審的是本檔與 ledger 紀錄）。

作者端實測（openspec 1.3.1，2026-10-01，在 scratchpad 複本上）：兩個案例 `openspec validate --all --json` 皆 3 項 valid、0 issues；`openspec show update-token-auth --json --deltas-only` 皆為 `session-policy ADDED`（1 個 scenario）與 `token-auth ADDED`（2 個 scenario）；歸檔預演皆印出 `session-policy ADDED failed for header "### Requirement: REQ-1 Session absolute lifetime" - already exists` 與 `Aborted. No files were changed.`、exit 0、change 目錄仍在、`archive/` 下沒有新目錄——預演依 13.B 判定為失敗，且失敗原因只來自 A。

## 預期答案表

| fixture | mutation（破壞了什麼） | primary scenario | collateral hits（避不開、原因） | 預期判定 | 預期 BLOCK 類別 |
|---|---|---|---|---|---|
| i3-mixed-synced-and-violation | A（session-policy）已同步；B（token-auth）未同步、ADDED `REQ-3` 而目前最大號是 REQ-5 | 13.D.3（B 的新 ID 低於最大號）；13.B SYNCED CAPABILITY（A） | 預演因 A 中止 → 無法判定，13.C 與 13.E 候選狀態半邊對兩個 capability 都不評估；A 讀主 spec 的判斷記為無法判定（required pre-sync state unavailable）；B 的 13.D 照常跑出違規 | BLOCK | {違規, 無法判定} |
| i3-synced-only | A 同上；B 改為合法的 ADDED `REQ-6`（高於 REQ-5），不提供任何違規 | 13.B SYNCED CAPABILITY（A 的 REQ-1 不得判成衝突） | 預演因 A 中止 → 無法判定；A 讀主 spec 的判斷記為無法判定；B 的 13.D 跑完、無發現 | BLOCK | {無法判定} |

## 停止條件（2026-10-01 使用者裁定）

一位全新 Sonnet、一次跑完兩個案例、不重試。任一案例 `DIFF` 或 `NONCONFORMING_OUTPUT` 即視為定點驗收未通過，停在 verify 前處理；不補派第二位、不多數決、不重跑到過。
