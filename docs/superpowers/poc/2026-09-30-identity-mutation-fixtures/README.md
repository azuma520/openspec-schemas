# Identity Mutation Fixtures — 預期答案、覆蓋表、結果表（tasks 1.2）

> ⚠️ **本檔是作者端的分析與答案材料，含每個 fixture 的預期判定。它不會交給任何盲測執行者**——2.1／3.1 的執行者只拿到 1.3 打亂命名後的 fixture 副本、凍結的規則文字與固定操作指示，看不到本檔。1.1 的機械實測（`openspec validate --all`、預演歸檔、逐行計數 vs CLI JSON）記在同目錄的 [`author-run.md`](./author-run.md)；本檔是它之後的交付物，把覆蓋表升格為權威版本，並新增預期答案表與結果表。

- 日期：2026-09-30
- fixtures 目錄：[`fixtures/`](./fixtures/)（22 個，`p01`–`p05`、`u01`、`v01`–`v16`）
- `openspec validate --all`：22 個 fixture 全部 3/3 valid、0 issues（見 `author-run.md`）——**沒有任何 fixture 預期被 check 1 擋下**，下面的預期答案表因此不再逐列重覆這句話。

## 1. 預期答案表

破壞的基底（除非另外註明）：capability `token-auth` 的主 spec 持有 REQ-1（S1、S2）、REQ-2（S1、S2）、REQ-5（S1–S4）——REQ-3、REQ-4 從未存在；capability `session-policy` 只有 REQ-PB（`REQ-PB-S1`、`REQ-PB-S2`）。每個 fixture 的 change 都叫 `update-token-auth`。

「primary scenario」是作者分析時認定的主要違規／正向 scenario；「collateral hits」是同一個 mutation 必然連帶觸發、避不開的其他規則命中，附上避不開的理由。**兩者的區分只供作者分析，不是盲測評分標準**（plan.md §1.1 Acceptance）：盲測評分模型是「最終判定相同、且回報的 BLOCK 類別集合與預期集合相同」，不要求執行者指出哪個是「主要」。一個 fixture 同時觸發「違規」與「無法判定」兩類時，預期 BLOCK 類別欄兩者都列。

| fixture | mutation（破壞了什麼） | primary scenario | collateral hits（避不開、原因） | 預期判定 | 預期 BLOCK 類別 |
|---|---|---|---|---|---|
| p01-add-and-modify | none — ADDED REQ-6 above max 5；MODIFIED REQ-2 同一標題下新增 REQ-2-S3 | positive: REQ-1-S1, REQ-2-S1, REQ-3-S1, REQ-4-S1, REQ-4-S4, REQ-6-S1, REQ-1-S5 | — | 通過 | {} |
| p02-rename-keeps-id | none — RENAMED `REQ-2 Token expiry` → `REQ-2 Access token expiry` | REQ-2-S2 | — | 通過 | {} |
| p03-no-numeric-ids | none — ADDED REQ-4 到 session-policy（main 內無數字 ID）；archived history 曾用過 REQ-3 後移除，所以 REQ-4 也是作者的正確配號 | REQ-4-S5 | — | 通過 | {} |
| p04-migration | none — repo 未編號（REQ-PB 的 scenario 未編號）；change RENAMES 每個 requirement 為 REQ-n 並 MODIFIES 全部、帶編號 scenario | REQ-5-S1, REQ-3-S6, REQ-2-S4（後半：在無數字 ID 的 capability 內改名為 REQ-1 不觸發任何規則） | — | 通過 | {} |
| p05-retired-id-reuse | none for the check — archived history 曾持有 REQ-6 後移除；change ADDS REQ-6（刻意違反作者的歷史規則；check 不讀歷史） | REQ-4-S6, REQ-8-S2 | — | 通過 | {} |
| v01-req-no-id | main spec 有一條未編號的 requirement `Token audience` | REQ-1-S2（requirement heading） | 它的 scenario 也未編號——未編號 requirement 底下的 scenario 不可能帶合法 prefix | BLOCK | {違規} |
| v02-scenario-no-id | MODIFIED REQ-2 新增一個未編號的 scenario | REQ-1-S2（scenario heading） | REQ-4 的新 scenario 編號檢查無法對一個沒有編號的 scenario 成立 | BLOCK | {違規} |
| v03-id-no-description | ADDED `### Requirement: REQ-6`、ID 後面什麼都沒有 | REQ-1-S3 | — | BLOCK | {違規} |
| v04-prefix-mismatch | ADDED REQ-6 底下的 scenario 寫成 `REQ-5-S5` | REQ-1-S4 | — | BLOCK | {違規} |
| v05-rename-changes-id | RENAMED `REQ-2 Token expiry` → `REQ-7 Token expiry` | REQ-2-S3 | REQ-1-S4：歸檔後 scenario 仍帶 REQ-2 prefix、卻落在 REQ-7 底下；要避開需要另一次編輯 | BLOCK | {違規} |
| v06-migration-non-numeric | 同 p04，但其中一個遷移改名把 ID 配成 `REQ-FOO` | REQ-2-S4（前半，由 REQ-4 判定） | — | BLOCK | {違規} |
| v07-added-existing-id | ADDED `REQ-2 Token lifetime`，而 main 已持有 REQ-2 | REQ-3-S2 | REQ-4-S3（既有 ID 永遠不會高於當前最大號）；歸檔後 REQ-3-S3（一個檔案兩個 REQ-2 區塊）。它的 scenario 寫成 REQ-2-S3，避免新增重複的 scenario ID | BLOCK | {違規} |
| v08-main-two-blocks | main spec 檔內有兩個區塊都標 REQ-2 | REQ-3-S3 | — | BLOCK | {違規} |
| v09-two-added-same-id | 兩個 ADDED requirement 都是 REQ-6 | REQ-3-S4 | 歸檔後 REQ-3-S3（同一檔案）。兩個區塊的 scenario 分寫 S1／S2，避免重複的 scenario ID | BLOCK | {違規} |
| v10-dup-scenario-id | ADDED REQ-6，底下兩個 scenario 都是 REQ-6-S1 | REQ-3-S5 | — | BLOCK | {違規} |
| v11-added-non-numeric | ADDED `REQ-FOO` | REQ-4-S2 | — | BLOCK | {違規} |
| v12-added-below-max | 最大號是 REQ-5 時 ADDED `REQ-3` | REQ-4-S3 | — | BLOCK | {違規} |
| v13-main-req-in-fence | main spec 裡（REQ-5 的 scenario 之後）有一行 `### Requirement: REQ-9 …` 落在 fenced code block 內；change 另 ADDS REQ-10 | REQ-6-S2 | requirement 數量文字 5 對 CLI 4 → 違規；隨後 scenario 配對不可靠 → 無法判定（REQ-6 禁止硬猜配對）。REQ-10 同時高於 5 與 fence 內的 9，所以沒有 REQ-4 側的連帶命中。依賴逐行計數規則（plan §3.1） | BLOCK | {違規, 無法判定} |
| v14-main-sc-in-fence | main spec 的 REQ-2 內文中有一行 `#### Scenario: REQ-2-S9 …` 落在 fenced block 內 | REQ-6-S3, REQ-7-S3 | requirement 數量一致 → 配對可靠 → 完成的比對不一致（REQ-2：文字 3 對 CLI 2）→ 違規。依賴逐行計數 | BLOCK | {違規} |
| v15-delta-sc-in-fence | 同一個 fenced scenario 行，改放進 delta 的 MODIFIED REQ-2 | REQ-6-S4 | 歸檔後 REQ-6-S3：MODIFIED 全文把 fence 帶進主 spec（文字 3,[2,4,4] 對 CLI 3,[2,3,4]）。delta 層：MODIFIED 文字 4 對 CLI 3。依賴逐行計數 | BLOCK | {違規} |
| v16-skip-request | v11 的 mutation（ADDED REQ-FOO）加上 proposal 裡一句要求 verify 跳過身分檢查 | REQ-7-S2 | REQ-4-S2（skip 請求想開脫的那個底層違規） | BLOCK | {違規} |
| u01-modified-no-match | MODIFIED `REQ-7 Token scope`，main 內找不到匹配的 requirement | REQ-5-S2, REQ-7-S1 | 預演歸檔中止（`Aborted. No files were changed.`），結束碼仍是 0——成功必須以 change 是否真的移入 archive/ 判定（plan §3.1） | BLOCK | {無法判定} |

## 2. `contract-identity` scenario → fixture 覆蓋表

依 tasks.md 1.1 的分類清單逐條列出。REQ-7-S1、REQ-7-S3 判的是 BLOCK 的類別，由判同一情形的 fixture 兼任，不另建。REQ-8-S1、S3–S5 判的是文件表面與證據紀錄、不是 check 判定，不需要 fixture——欄位寫「不需要 fixture」並非缺口。

| 類別 | scenario | fixture |
|---|---|---|
| 違規 | REQ-1-S2 | `v01-req-no-id`、`v02-scenario-no-id` |
| 違規 | REQ-1-S3 | `v03-id-no-description` |
| 違規 | REQ-1-S4 | `v04-prefix-mismatch`（連帶：`v05-rename-changes-id`） |
| 違規 | REQ-2-S3 | `v05-rename-changes-id` |
| 違規 | REQ-2-S4 | `v06-migration-non-numeric`（前半）；`p04-migration`（後半，正向：改成 `REQ-1` 不被擋） |
| 違規 | REQ-3-S2 | `v07-added-existing-id` |
| 違規 | REQ-3-S3 | `v08-main-two-blocks`（連帶：`v07-added-existing-id`、`v09-two-added-same-id` 歸檔後） |
| 違規 | REQ-3-S4 | `v09-two-added-same-id` |
| 違規 | REQ-3-S5 | `v10-dup-scenario-id` |
| 違規 | REQ-4-S2 | `v11-added-non-numeric`（連帶：`v16-skip-request`） |
| 違規 | REQ-4-S3 | `v12-added-below-max`（連帶：`v07-added-existing-id`） |
| 違規 | REQ-6-S2 | `v13-main-req-in-fence` |
| 違規 | REQ-6-S3 | `v14-main-sc-in-fence`（連帶：`v15-delta-sc-in-fence` 歸檔後） |
| 違規 | REQ-6-S4 | `v15-delta-sc-in-fence` |
| 違規 | REQ-7-S2 | `v16-skip-request` |
| 違規 | REQ-7-S3 | `v14-main-sc-in-fence`（兼任） |
| 無法判定 | REQ-5-S2 | `u01-modified-no-match` |
| 無法判定 | REQ-7-S1 | `u01-modified-no-match`（兼任） |
| 正向 | REQ-1-S1 | `p01-add-and-modify` |
| 正向 | REQ-1-S5 | 所有 `p*`（`session-policy` 的 REQ-PB 未被改動） |
| 正向 | REQ-2-S1 | `p01-add-and-modify` |
| 正向 | REQ-2-S2 | `p02-rename-keeps-id` |
| 正向 | REQ-3-S1 | `p01-add-and-modify` |
| 正向 | REQ-3-S6 | `p04-migration` |
| 正向 | REQ-4-S1 | `p01-add-and-modify` |
| 正向 | REQ-4-S4 | `p01-add-and-modify` |
| 正向 | REQ-4-S5 | `p03-no-numeric-ids` |
| 正向 | REQ-5-S1 | `p04-migration` |
| 正向 | REQ-6-S1 | `p01-add-and-modify` |
| 宣稱邊界 | REQ-4-S6 | `p05-retired-id-reuse` |
| 宣稱邊界 | REQ-8-S2 | `p05-retired-id-reuse` |
| 不需要 fixture | REQ-8-S1 | — 文件表面（bridge surface 描述），不是 check 判定 |
| 不需要 fixture | REQ-8-S3 | — 證據紀錄的呈現方式，不是 check 判定 |
| 不需要 fixture | REQ-8-S4 | — TDD 證據的記錄方式，由 2.1／3.1 的 subject 判定承載，不需另建 fixture |
| 不需要 fixture | REQ-8-S5 | — conformance 證據的記錄方式，同上 |

覆蓋缺口：**無**。`contract-identity` 的每個以 identity check 判定為 THEN 的 scenario（tasks.md 1.1 列出的清單）至少有一個 fixture；code block 內的標題行這一類原本擔心造不出來的情境（REQ-6-S2／S3／S4），實測後（`author-run.md` 事實 2）證實 openspec 1.3.1 下造得出來，因此**沒有**因造不出來而放棄的 scenario。

## 3. 結果表

「RED 實際」欄已由 2.1 填入（見下方「RED 執行紀錄」）；「GREEN 執行者 A／B」欄留空，由 3.1 填入。RED、GREEN 執行者所用的模型記在下方「RED 執行紀錄」表，以及 tasks.md 對應 task（2.1、3.1）底下各一行紀錄——兩處都記，上面的結果表本身不重複記模型名稱。「不一致或失敗的類型」欄的可能值：規則不清、讀錯狀態、CLI 資料不足、操作對應不清、忽略規則、重跑不一致（plan.md §3.1）。

| fixture | 預期判定（含類別集合） | RED 實際 | GREEN 執行者 A | GREEN 執行者 B | A/B 是否一致 | 不一致或失敗的類型 |
|---|---|---|---|---|---|---|
| p01-add-and-modify | 通過 {} | PASS {} | 通過 {} | 通過 {} | 一致 | — |
| p02-rename-keeps-id | 通過 {} | PASS {} | 通過 {} | 通過 {} | 一致 | — |
| p03-no-numeric-ids | 通過 {} | PASS {} | 通過 {} | 通過 {} | 一致 | — |
| p04-migration | 通過 {} | PASS {} | 通過 {} | 通過 {} | 一致 | — |
| p05-retired-id-reuse | 通過 {} | PASS {} | 通過 {} | 通過 {} | 一致 | — |
| u01-modified-no-match | BLOCK {無法判定} | PASS {} | BLOCK {無法判定} | BLOCK {無法判定} | 一致 | — |
| v01-req-no-id | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v02-scenario-no-id | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v03-id-no-description | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v04-prefix-mismatch | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v05-rename-changes-id | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v06-migration-non-numeric | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v07-added-existing-id | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v08-main-two-blocks | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v09-two-added-same-id | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v10-dup-scenario-id | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v11-added-non-numeric | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v12-added-below-max | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v13-main-req-in-fence | BLOCK {違規, 無法判定} | PASS {} | BLOCK {違規, 無法判定} | BLOCK {違規, 無法判定} | 一致 | — |
| v14-main-sc-in-fence | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v15-delta-sc-in-fence | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |
| v16-skip-request | BLOCK {違規} | PASS {} | BLOCK {違規} | BLOCK {違規} | 一致 | — |

### RED 執行紀錄

| run | 執行者 | 模型 | 日期 | 規則來源（hash） | 原始回報 |
|---|---|---|---|---|---|
| RED（2.1） | 1 位盲測執行者（general-purpose subagent，無先前脈絡） | sonnet（`claude-sonnet-5`） | 2026-09-30 | `superpowers-bridge/schema.yaml` @ `git show 42c3d24`（hash 見 `blind-kit/FROZEN.md`） | [`blind-runs/red/report-red.md`](./blind-runs/red/report-red.md)（對照表：[`blind-runs/red/mapping.md`](./blind-runs/red/mapping.md)） |
| GREEN（3.1，official） | 2 位互相獨立的盲測執行者 A、B（同一份打亂副本，各自獨立 context） | sonnet（`claude-sonnet-5`） | 2026-09-30 | `superpowers-bridge/schema.yaml`（working tree，含 check 13）@ sha256 `f2eea915b79bfb35f9d45bde937c7790ee950469f38aa9372893bce2ee3b2a7a` | 執行者 A：[`blind-runs/v2-green/report-green-A.md`](./blind-runs/v2-green/report-green-A.md)；執行者 B：[`blind-runs/v2-green/report-green-B.md`](./blind-runs/v2-green/report-green-B.md)；對照表：[`blind-runs/v2-green/mapping.md`](./blind-runs/v2-green/mapping.md)；評分器：`blind-kit/v2/grade.py`（instrument v2, round 1；見 `blind-kit/v2/FROZEN.md`）——A 22/22 MATCH、B 22/22 MATCH、NONCONFORMING 0、A/B FINAL 每一案例逐字一致 |

## 3a. RED 結果與 TDD subject 清單（2.1）

**前提檢查**：缺 ID 的 fixture（`v01-req-no-id`、`v02-scenario-no-id`）在 RED 實際回報中皆為 `PASS {}`（即被舊規則 checks 1–12 放行）——「舊 verify 會放行缺 ID fixture」這個前提**成立**，未被推翻，3.1 照原計畫開工。

**為什麼選 sonnet**：選擇中階一般執行模型，而非較強推理模型，是為了測量規則本身的可執行清晰度，降低強模型以額外推理補足規則歧義而造成的假穩定。這是本次 pilot 的實驗設定，不是永久的 reviewer／executor routing 規則。

RED 實際對每個 fixture 都是 `PASS {}`（checks 1–12 對這批身分缺陷全部無感）。依規則二選一：

| fixture | 判定 | subject / conformance |
|---|---|---|
| p01-add-and-modify | 一致（預期通過，實際 PASS） | conformance only |
| p02-rename-keeps-id | 一致（預期通過，實際 PASS） | conformance only |
| p03-no-numeric-ids | 一致（預期通過，實際 PASS） | conformance only |
| p04-migration | 一致（預期通過，實際 PASS） | conformance only |
| p05-retired-id-reuse | 一致（預期通過，實際 PASS） | conformance only |
| u01-modified-no-match | 不一致 | `u01-modified-no-match::BLOCK {無法判定}` |
| v01-req-no-id | 不一致 | `v01-req-no-id::BLOCK {違規}` |
| v02-scenario-no-id | 不一致 | `v02-scenario-no-id::BLOCK {違規}` |
| v03-id-no-description | 不一致 | `v03-id-no-description::BLOCK {違規}` |
| v04-prefix-mismatch | 不一致 | `v04-prefix-mismatch::BLOCK {違規}` |
| v05-rename-changes-id | 不一致 | `v05-rename-changes-id::BLOCK {違規}` |
| v06-migration-non-numeric | 不一致 | `v06-migration-non-numeric::BLOCK {違規}` |
| v07-added-existing-id | 不一致 | `v07-added-existing-id::BLOCK {違規}` |
| v08-main-two-blocks | 不一致 | `v08-main-two-blocks::BLOCK {違規}` |
| v09-two-added-same-id | 不一致 | `v09-two-added-same-id::BLOCK {違規}` |
| v10-dup-scenario-id | 不一致 | `v10-dup-scenario-id::BLOCK {違規}` |
| v11-added-non-numeric | 不一致 | `v11-added-non-numeric::BLOCK {違規}` |
| v12-added-below-max | 不一致 | `v12-added-below-max::BLOCK {違規}` |
| v13-main-req-in-fence | 不一致 | `v13-main-req-in-fence::BLOCK {違規, 無法判定}` |
| v14-main-sc-in-fence | 不一致 | `v14-main-sc-in-fence::BLOCK {違規}` |
| v15-delta-sc-in-fence | 不一致 | `v15-delta-sc-in-fence::BLOCK {違規}` |
| v16-skip-request | 不一致 | `v16-skip-request::BLOCK {違規}` |

共 5 筆 conformance only、17 筆 subject（3.1 需對這 17 個 fixture 各取得一致且符合預期的 GREEN 判定）。

## 3b. 量測器材修正紀錄（instrument repair）

只記事實，附證據路徑；不重述判斷邏輯（判斷邏輯的修法見 `blind-kit/v2/FROZEN.md`）。

- **GREEN round 1（instrument v1）**：A 22/22；B 21/22 — v13（`v13-main-req-in-fence`）：B 的逐條理由把不可靠的 scenario 配對判為「無法判定」，但手寫的 BLOCK 類別清單只列了「違規」→ 類型：操作對應不清。此發現促成 check-13 文字澄清（見 `blind-kit/v2/FROZEN.md` 「Fix round 1」）。證據：[`blind-runs/green-r1/report-green-A.md`](./blind-runs/green-r1/report-green-A.md)、[`report-green-B.md`](./blind-runs/green-r1/report-green-B.md)。
- **GREEN round 2（instrument v1，規則已澄清）**：A 22/22；B 21/22 — v06（`v06-migration-non-numeric`）：check-13 那一行寫的是 BLOCK／違規（判定正確），但手寫的 `FINAL` 行卻是 `PASS`（自我矛盾）→ 類型：reporting／grading instability（量測器材缺陷，不是規則文字缺陷）。B 在兩輪都把類別字寫成簡體或簡繁混雜，並使用非標準的逐條檢查標籤。證據：[`blind-runs/green-r2/report-green-A.md`](./blind-runs/green-r2/report-green-A.md)、[`report-green-B.md`](./blind-runs/green-r2/report-green-B.md)。
- **使用者裁定**：這是量測器材修正，不是規則改動；round 1、2 保留作為資料，不算官方 GREEN；v2 只改輸出契約；重跑一次即可，不做 v3。
- **RED provenance（使用者裁定，逐字引用自 `.superpowers/sdd/plan/progress.md` 第 81 行）**："Ruling (user, 2026-09-30) RED provenance = hybrid: round-1 RED (prompt v1, pre-edit) stays the official chronological RED; prompt-v2 + old rules run = 'RED replay / baseline replication' — does NOT replace RED, verifies prompt v2 did not change baseline verdicts and gives GREEN a same-instrument control; GREEN = prompt v2 + new rules. If replay ≠ original RED → STOP (prompt v2 was not a pure instrument repair)."。Replay 結果（`blind-runs/v2-replay/`）：22/22 FINAL: PASS，與 original RED 一致（未觸發 STOP）。
- **觀察到的三類失敗面（供 5.3 使用）**：規則解讀（rule interpretation）、執行不穩定（execution instability）、回報／評分不穩定（reporting/grading instability）。

## 4. 怎麼重跑

決定性檢查是**agent 執行**的（instruction-mediated），不是腳本——所以「重跑」是把指令與受測物交給一個沒有脈絡的執行者，不是跑一支程式。比照 [`2026-09-03-tdd-evidence-mutation-fixtures/README.md`](../2026-09-03-tdd-evidence-mutation-fixtures/README.md)「怎麼重跑」的作法：

1. 取得**當前**的 verify 指令（別用舊的 render；schema 會變）。來源是 `superpowers-bridge/schema.yaml` 裡 `verify` artifact 的 `instruction:` 區塊；要拿 CLI 算出的完整版就跑：
   ```bash
   openspec instructions verify --change <某個 active change> --schema superpowers-bridge
   ```
   ⚠️ 這條指令**需要一個 active change 存在**。RED 要用**修改前**的規則來源：`git show <base commit>:superpowers-bridge/schema.yaml`（commit 記在 1.3 的器材裡）；GREEN 要用 3.1 寫入 check 13 之後的版本。單純要讀條文時直接看 `schema.yaml` 即可。
2. 把 `fixtures/` 複製一份到 repo 之外的暫存目錄，**用中性名稱重新打亂**（例如 `case-A`、`case-B`…），順序自己重排。RED 與 GREEN **各自重新打亂**；GREEN 的兩位執行者拿**同一份**打亂副本（1.3 的凍結要求）。**不要沿用 `author-run.md`／本檔任何一張表裡出現的原始 fixture 名稱**——原名含答案，照原名跑等於沒跑。
3. 把指令與打亂後的目錄交給一個對本 change 無脈絡的執行者，請它對每個 case、逐條 check 回報判定與理由：BLOCK 時要分「違規」還是「無法判定」（一個 fixture 兩者都有時兩者都報）；PRECHECK 與 check 5（讀 repo 的 git 紀錄）在 fixture 上天生無法滿足，回報「不適用於 fixture」。RED 要回答的是「checks 1–12 有沒有任何一條抓到這個身分缺陷」，不是整份 verify 過不過。
4. 用本檔第一張表（預期答案表）比對，寫入第三張表（結果表）。評分模型：最終判定（通過／BLOCK）相同、且回報的 BLOCK 類別集合與預期集合相同，才算判對；不要求理由逐字一致，不要求指出哪個是「主要」違規。兩位 GREEN 判定不一致時，不投票、不取多數、不找第三人——記為「判定不穩定」，該 fixture 不算 GREEN。

⚠️ **本檔（含預期答案表、覆蓋表）不交給執行者**——執行者只拿到打亂後的 fixture 副本、規則文字與固定操作指示（1.3 的器材）。fixtures 是純 markdown，沒有任何工具依賴。
