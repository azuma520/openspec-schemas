# 作者端實測紀錄（tasks 1.1）

> 這份是**寫 fixture 的人**對 `fixtures/` 做的機械實測：每個 fixture 能不能通過 `openspec validate --all`、預演歸檔能不能產生候選狀態、逐行計數與 CLI JSON 是否一致。它**不是**盲測判定——判定由 2.1／3.1 的盲測執行者依 verify 規則做出。本檔放在 `fixtures/` 之外，不會進入交給執行者的打亂副本。

- 日期：2026-09-30
- OpenSpec CLI：`1.3.1`
- 環境：Windows 11，Git Bash；每個 fixture 複製兩份到 repo 外的暫存目錄，一份跑 validate 與 change 層 show，一份跑預演歸檔。

## 怎麼跑的

在 fixture 複本根目錄（含 `openspec/` 的那層）執行：

```bash
openspec validate --all --json                         # check 1 的輸入
openspec show update-token-auth --json --deltas-only   # change 層 CLI 計數（只讀 stdout）
openspec archive update-token-auth -y                  # 預演歸檔，在另一份複本上跑
openspec show <capability> --type spec --json          # 預演後、在同一份複本內跑
```

「逐行計數」＝一行以 `### Requirement:` 開頭算一條 requirement，以 `#### Scenario:` 開頭算一個 scenario，歸給它上方最近的 requirement；不辨識 code block。這是本檔的量法，**不是** check 13 的規則文字（那在 3.1 才寫）。

## 結果

| fixture | `validate --all`（valid 項數／總數；issues） | 預演歸檔：exit code／change 目錄移入 archive | 預演後主 spec：逐行計數 vs CLI（requirement 數, 各 requirement 的 scenario 數） |
|---|---|---|---|
| `p01-add-and-modify` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (4, [2, 3, 4, 2]) vs CLI (4, [2, 3, 4, 2]) |
| `p02-rename-keeps-id` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (3, [2, 4, 2]) vs CLI (3, [2, 4, 2]) |
| `p03-no-numeric-ids` | 3/3；0 | 0／是 | session-policy: 文字 (2, [2, 1]) vs CLI (2, [2, 1])<br>token-auth: 文字 (3, [2, 2, 4]) vs CLI (3, [2, 2, 4]) |
| `p04-migration` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (2, [2, 2]) vs CLI (2, [2, 2]) |
| `p05-retired-id-reuse` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (4, [2, 2, 4, 2]) vs CLI (4, [2, 2, 4, 2]) |
| `u01-modified-no-match` | 3/3；0 | 0／否（輸出：token-auth MODIFIED failed for header "### Requirement: REQ-7 Token scope" - not found / Aborted. No files were changed.） | 無（未產生候選狀態） |
| `v01-req-no-id` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (5, [2, 2, 1, 4, 2]) vs CLI (5, [2, 2, 1, 4, 2]) |
| `v02-scenario-no-id` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (3, [2, 3, 4]) vs CLI (3, [2, 3, 4]) |
| `v03-id-no-description` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (4, [2, 2, 4, 2]) vs CLI (4, [2, 2, 4, 2]) |
| `v04-prefix-mismatch` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (4, [2, 2, 4, 2]) vs CLI (4, [2, 2, 4, 2]) |
| `v05-rename-changes-id` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (3, [2, 4, 2]) vs CLI (3, [2, 4, 2]) |
| `v06-migration-non-numeric` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (2, [2, 2]) vs CLI (2, [2, 2]) |
| `v07-added-existing-id` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (4, [2, 2, 4, 1]) vs CLI (4, [2, 2, 4, 1]) |
| `v08-main-two-blocks` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (5, [2, 2, 1, 4, 2]) vs CLI (5, [2, 2, 1, 4, 2]) |
| `v09-two-added-same-id` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (5, [2, 2, 4, 1, 1]) vs CLI (5, [2, 2, 4, 1, 1]) |
| `v10-dup-scenario-id` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (4, [2, 2, 4, 2]) vs CLI (4, [2, 2, 4, 2]) |
| `v11-added-non-numeric` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (4, [2, 2, 4, 2]) vs CLI (4, [2, 2, 4, 2]) |
| `v12-added-below-max` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (4, [2, 2, 4, 2]) vs CLI (4, [2, 2, 4, 2]) |
| `v13-main-req-in-fence` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (5, [2, 2, 4, 0, 2]) vs CLI (4, [2, 2, 4, 2]) **不一致** |
| `v14-main-sc-in-fence` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (4, [2, 3, 4, 2]) vs CLI (4, [2, 2, 4, 2]) **不一致** |
| `v15-delta-sc-in-fence` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (3, [2, 4, 4]) vs CLI (3, [2, 3, 4]) **不一致** |
| `v16-skip-request` | 3/3；0 | 0／是 | session-policy: 文字 (1, [2]) vs CLI (1, [2])<br>token-auth: 文字 (4, [2, 2, 4, 2]) vs CLI (4, [2, 2, 4, 2]) |

change 層（`--deltas-only`，歸檔前）：只有 `v15-delta-sc-in-fence` 不一致——delta 檔 MODIFIED `REQ-2` 逐行數到 4 個 scenario，CLI 該筆 `requirement.scenarios` 長度 3。其餘 21 個 fixture 各 operation 的筆數與 scenario 數皆一致（RENAMED 以 `rename.from`／`rename.to` 對讀，與 delta 檔相同）。

## 實測得到的 CLI 事實（openspec 1.3.1）

1. **預演歸檔失敗時 exit code 仍是 0。** `u01` 的 MODIFIED 標題在主 spec 找不到：archive 印出 `MODIFIED failed … not found` 與 `Aborted. No files were changed.`，change 目錄留在原處，**結束碼 0**。⇒ 判定「預演歸檔成功」不能只看結束碼；本檔改以「`changes/<change>/` 已不存在、且 `changes/archive/` 下出現 `*-<change>/`」判定。影響：3.1 的 check 13 規則文字要寫明成功判準；plan.md 5.2 的驗收原本只寫「結束碼是 0」，已依本項實測修訂為「結束碼 0 且歸檔狀態轉換確實發生」（2026-09-30 使用者裁定）。
2. **code block 內的標題行：逐行計數算得到，CLI 看不到。** `validate` 照樣通過。requirement 層（`v13`）與 scenario 層（`v14`、`v15`）都造得出來，因此 `contract-identity` REQ-6-S2／S3／S4 **沒有覆蓋缺口**。
3. **反方向也存在：CLI 認得、嚴格逐行比對認不得。** 另以探測腳本實測（未做成 fixture）：`###  Requirement:`（兩個空格）與 `### requirement:`（小寫）CLI 都算成 requirement；`####  Scenario:`、`#### scenario:` 同樣被 CLI 算進 scenario。`### Requirement:REQ-3`（冒號後無空白）雙方都算。`##### Scenario:` 要看位置：接在已有 `####` scenario 之後時雙方都不算；是某條 requirement 底下唯一的子標題時，CLI 會把它算成 scenario（該條 `scenarios` 長度 1），逐行計數不算（fixture 審查者以探測腳本發現，作者以最小探測重跑確認）。這一類若出現，交叉核對同樣會不一致（方向相反）；是否另做 fixture 不在 1.1 清單內，記為觀察。
4. **fixture 內不需安裝 schema。** change 的 `.openspec.yaml` 寫 `schema: superpowers-bridge`，但 fixture 沒有 `openspec/schemas/`；`openspec status` 會退回顯示 `spec-driven`，`validate`、`show`、`archive` 皆不受影響。

## 覆蓋缺口

無。依據是建 fixture 時的對照（下表）；tasks.md 1.1 列出的每個 scenario 都至少有一個 fixture。正式的 scenario → fixture 覆蓋表是 tasks 1.2 README 的交付物，建立後以它為準，本表只記建 fixture 當下的對照。

| 類別 | scenario | fixture |
|---|---|---|
| 違規 | REQ-1-S2 | `v01-req-no-id`、`v02-scenario-no-id` |
| 違規 | REQ-1-S3 | `v03-id-no-description` |
| 違規 | REQ-1-S4 | `v04-prefix-mismatch` |
| 違規 | REQ-2-S3 | `v05-rename-changes-id` |
| 違規 | REQ-2-S4 | `v06-migration-non-numeric`（前半）；`p04-migration`（後半：改成 `REQ-1` 不被擋） |
| 違規 | REQ-3-S2 | `v07-added-existing-id` |
| 違規 | REQ-3-S3 | `v08-main-two-blocks` |
| 違規 | REQ-3-S4 | `v09-two-added-same-id` |
| 違規 | REQ-3-S5 | `v10-dup-scenario-id` |
| 違規 | REQ-4-S2 | `v11-added-non-numeric` |
| 違規 | REQ-4-S3 | `v12-added-below-max` |
| 違規 | REQ-6-S2 | `v13-main-req-in-fence` |
| 違規 | REQ-6-S3 | `v14-main-sc-in-fence` |
| 違規 | REQ-6-S4 | `v15-delta-sc-in-fence` |
| 違規 | REQ-7-S2 | `v16-skip-request` |
| 違規 | REQ-7-S3 | `v14-main-sc-in-fence`（兼任） |
| 無法判定 | REQ-5-S2、REQ-7-S1 | `u01-modified-no-match` |
| 正向 | REQ-1-S1、REQ-2-S1、REQ-3-S1、REQ-4-S1、REQ-4-S4、REQ-6-S1 | `p01-add-and-modify` |
| 正向 | REQ-1-S5 | 所有 `p*`（`session-policy` 的 `REQ-PB` 未被改動） |
| 正向 | REQ-2-S2 | `p02-rename-keeps-id` |
| 正向 | REQ-3-S6、REQ-5-S1 | `p04-migration` |
| 正向 | REQ-4-S5 | `p03-no-numeric-ids` |
| 宣稱邊界 | REQ-4-S6、REQ-8-S2 | `p05-retired-id-reuse` |
