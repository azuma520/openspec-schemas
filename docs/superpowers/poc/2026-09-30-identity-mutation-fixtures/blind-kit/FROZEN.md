# 盲測器材凍結紀錄（task 1.3）

凍結日期：2026-09-30。凍結範圍：`prompt.md`、`procedure.md`，以及 RED 執行用的規則檔 `schema-red.yaml`。這三份檔案在 2.1（RED）開跑前不再變動；3.1（GREEN）只允許替換規則檔內容,`prompt.md`、`procedure.md` 必須逐位元組沿用同一份（見下方 hash）。

## SHA-256

| 檔案 | SHA-256 |
|---|---|
| `prompt.md` | `4743f51ba378cd9b03a52087dbab2a3772f6f798cb87521e9a46c2e44177103f` |
| `procedure.md` | `745ba7dcd3ab636c4f70eb6021d4d7c43b474646755f6e45fd2d35d2eda34679` |
| `schema-red.yaml`（RED 規則檔） | `546e27268f3b8af56aa76200b290c0fd0485d66c7191345d0f602007a0be07b9` |

## 規則來源（RED／GREEN 只有這一個變數）

- **RED**：`git show 42c3d24:superpowers-bridge/schema.yaml`。commit `42c3d24` 是本 branch（`worktree-requirement-scenario-identity`）目前的 base commit，且已用 `git merge-base HEAD main` 驗證等於 `42c3d24`——即這個 branch 目前尚未對 `superpowers-bridge/schema.yaml` 做任何 schema 編輯（`git diff 42c3d24 -- superpowers-bridge/schema.yaml` 無輸出）。上表的 `schema-red.yaml` 就是這個指令取出的全文,與工作樹目前的 `superpowers-bridge/schema.yaml` 逐位元組相同(已用 `sha256sum` 交叉核對,兩者雜湊一致)。
- **GREEN**：task 3.1 把 check 13 寫進 `superpowers-bridge/schema.yaml` 之後,working tree 當時的那份全文。取得方式與 RED 相同的動作——直接讀 `superpowers-bridge/schema.yaml`——只是取的時間點不同,不是另一套指令。
- `prompt.md` 與 `procedure.md` 只以固定檔名 `schema.yaml` 稱呼規則檔,不寫死任何檢查編號或內容,所以規則來源變動時,這兩份檔案不需要跟著改。

## GREEN 重新產生的程序

見 `procedure.md` 的「GREEN 執行的產生程序」一節——由派工者（不是盲測執行者）在 task 3.1 完成後執行:換規則檔內容、重新打亂 fixture 代號（不沿用 RED 用過的順序或代號）、產出兩份實體分開但逐位元組相同的 kit 給 GREEN 的兩位執行者。凍結的是「怎麼做」這個程序本身,不是某一次打亂的結果——打亂結果本來就該每次重新產生,以避免執行者沿用舊答案。

## 已知限制

見 `procedure.md` 末段——「不要讀 kit 以外的檔案」只是指示,不是技術隔離。執行者是具備檔案系統存取能力的 agent,遵守與否無法被這份器材本身偵測。這一點會寫進 5.3 的觀察紀錄。

## 交給執行者的副本放在哪裡

打亂後的 fixture 副本與規則檔的可執行複本,連同 `prompt.md`／`procedure.md` 的副本,放在 repo 之外的暫存目錄（RED：scratchpad 底下的 `blind/red/kit/`）。打亂代號 ↔ 原始 fixture 名稱的對照表放在該 kit 目錄之外的同一層（`blind/red/mapping.md`）,不進 kit、不交給執行者。本檔（`blind-kit/` 底下）保留的是**凍結證據**（prompt、procedure、RED 規則檔全文與雜湊）,不是執行者實際收到的目錄結構。
