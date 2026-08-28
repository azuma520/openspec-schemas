# 概念 PoC：最小 Traceability + Completion Gate 可行性驗證

> 2026-08-28 brainstorming 定案（使用者逐題核可）。上游：[`2026-08-27-bridge-guarantee-architecture-direction.md`](./2026-08-27-bridge-guarantee-architecture-direction.md) §7 與護欄 10。
>
> **本 PoC 不以建立正式 Harness 為目標**——產出是一個答案（hypothesis 成立與否），不是要保留維護的程式碼。PoC 之前與期間不動 `schema.yaml`、**不新增正式 artifact type、不修改 schema artifact graph**；PoC 得使用 provisional result fixture 作為實驗載體（§7）——它是實驗用暫定檔，不是正式 artifact。
>
> 方向文件 §7 說 PoC「作為一個 change 走正常流程」——此處「正常流程」指 brainstorm → spec → 核可這個順序，不是 opsx change 容器（依三軌制，研究／評估類走直接 commit；Phase 2 的 specimen 才是真的 opsx change）。

---

## 1. Hypothesis

> 如果 Requirement / Scenario 能被機械追蹤到承接的 Task，且必要的 Verification Result 能被機械追蹤回對應 Contract，那 Harness 應能依據結構化 Verification Record 的存在與狀態，機械判定該 Contract 是否具備 Complete 資格，而不只依賴裸露的 completion claim。

**宣稱邊界**：本 PoC 不宣稱消除 Agent 自我宣稱——`status: PASS` 與 `evidence` 仍可能由 Agent 寫出。它只證明 Completion Gate 可以從「裸 completion claim」升級為依賴結構化 Verification Record（contract + status + evidence）的機械判定。

**粒度邊界**：Core 判準以 **Requirement 為單位**（§7）——本 PoC 實際證明的是 `Requirement → Task` 與 `Requirement → Verification Result` 可機械追蹤；Scenario-level reference 允許但**不是 Core PASS 的必要條件**。PoC PASS 後不得宣稱「Requirement / Scenario 都已被完整證明可 trace」——Scenario 級 traceability 尚未被完整證明。

## 2. 真正要驗的兩條線

五層鏈（Requirement/Scenario → Task → Verification Method → Verification Result → Gate）只是示意，**不是資料模型**（Task 是否串在 Verification 中間，不在本 PoC 鎖死；Verification Method 也刻意不進最小 Result 欄位——見 §7「再多就偷塞設計」）。要驗的是兩個可證偽的命題：

| 線 | 命題 |
|---|---|
| Requirement/Scenario → Task | 原本的承諾沒有在拆 Task 時消失（可機械檢查 coverage） |
| Requirement/Scenario → Verification Result | 每條需要驗證的 Contract 都找得到掛回它的 Result（可機械檢查 reference） |

Gate 據此問三件事：這條 Contract 有 Task 承接嗎？需要的 Verification Result 存在嗎？Result = PASS 嗎？——全 YES 才有 Complete 資格。（完整檢查集另含 §7 的 evidence 非空與 CONFLICT fail-closed 判定；從本節單獨實作是不夠的。）

本 PoC 驗的是 **Structural Traceability（結構可追溯性，「有沒有接起來」）**，不是 **Semantic Correctness（語意正確性，「接得對不對」）**。前者機械處理；後者需要 Contract Verification / review / test quality judgment，屬後續階段。

## 3. Non-goals（顯式清單）

以下全部**不在**本 PoC 範圍，任何一項若在實作中被「順便」加入即為範圍違反：

1. **語意正確性**——一筆宣稱驗 REQ-A 的 Result，其內容是否真的在驗 REQ-A（例：test 實際只測了正常 Token 回 200，卻掛在「過期 Token 回 401」上），機器只看 reference 抓不到。
2. **Evidence 真偽與充分性**——command 真的跑過嗎、憑據夠不夠力，Gate 不驗。
3. **Freshness / superseded**——「舊 FAIL → 重驗 → 新 PASS → 舊結果作廢」的生命週期不做；本階段衝突一律 fail-closed（§7）。
4. **G1b expansion detection**、**G3 degradation**、**review integration**、**parallel execution**。
5. **Schema / 資料模型正式化**——本 PoC 的一切新形狀均為 provisional（§7）。

## 4. Step 0：Tool Capability Preflight（開工前置確認）

原則（方向文件護欄 1、2 的直接應用）：

> **PoC 開工前先做 capability inventory：已有 CLI 能機械回答的問題一律優先復用；只有現有工具真的沒有的能力，才由 PoC 補。**

這**不是全面工具盤點**——只確認本 PoC 真的依賴的能力，分三類：

| 類 | 對象 | 要確認什麼 |
|---|---|---|
| 一、開工前必確認（blocking） | OpenSpec CLI | ① 實際版本 ② repo 目前 resolve 到哪個 schema、來源在哪 ③ CLI 產生的真 change 目錄實際長什麼樣 ④ Requirement / Scenario / `tasks.md` 的實際 Markdown 形狀 ⑤ 哪些指令有 machine-readable（`--json`）輸出——候選：`schemas` / `templates` / `validate` / `show` / `status` / `new change`，**確切指令形以 `openspec --help` 實查為準，不照本表字面** ⑥ `validate` 實際檢查哪些東西 |
| 二、確認存在即可，不深入 | Python runtime | 有沒有、版本、repo 既有使用慣例。**不**引入 Pydantic / graph library / SQLite / JSON Schema framework——現在都不需要 |
| 三、參考、非 PoC 依賴 | Matt `/to-tickets`、sd0x、Orca、Superpowers | 明記即可：`/to-tickets` 是未來 Task Decomposition 候選、本 PoC 不依賴（Phase 1 的 Task 是 fixture、Phase 2 只是 provisional 標註）；sd0x 是 Gate / state 設計思想的 reference implementation、非 Phase 1 runtime dependency；Orca dispatch / TDD / review orchestration / parallel execution 完全不進本 PoC |

**產出**：一份很短的 capability inventory，三欄——Can reuse（例：OpenSpec CLI JSON 可供哪些資料）／ Need PoC code（例：Contracts reference 解析、provisional Result 解析、Gate 邏輯）／ Do not need（例：新 OpenSpec parser、資料庫、sd0x 整合、Orca、`/to-tickets`）。
**（已執行，2026-08-28）**：結果見 [`../poc/2026-08-28-traceability-gate/step0-capability-inventory.md`](../poc/2026-08-28-traceability-gate/step0-capability-inventory.md)——含三個關鍵實測發現（手造 change 需 `proposal.md` 即可被 CLI JSON 讀取；change 層 JSON 不含 Requirement 標題名；最小新增面積＝Task reference + Result interface + Gate）。

這不只是工具檢查——**它直接決定 PoC 的最小新增面積**：「原以為需要 A、B、C，實查 OpenSpec 已提供 A、B，PoC 真正只需補 C」。若最終發現真正缺口只是 Task reference + Verification Result interface + Gate（而非一整個 Traceability Framework），那本身就是給後續正式設計的重要架構訊號。

**判準**：若 Requirement / Scenario 已能透過 CLI JSON 可靠取得，PoC validator **不得**自己用 regex 重解 Markdown——防的正是「花半天寫 parser，跑完才發現 `openspec show --json` 本來就會吐資料」。Preflight 結果與本 spec 假設矛盾時（例：CLI 給不出假設的資料形狀），停下回報、修 spec，不硬做。

## 5. Phase 1：Synthetic Fixture（機制驗證）

手造一個**模仿真實 OpenSpec 形狀**的迷你 change 目錄：真格式 `specs/`（Requirement / Scenario 標題結構照 OpenSpec 慣例）＋真格式 `tasks.md`（加 provisional Contracts 標註）＋新發明的最小 results 檔。刻意選真形狀而非自由 JSON：讓 parser / reference / coverage 的整合風險在 Phase 1 就暴露，而不是延後到 Phase 2。

六個案例**全為必做**（REQ-C~F 不是選配——「沒有結果」「結果是 FAIL」「結果無憑據」「結果互相衝突」在實作裡各是一條判斷路徑，Gate 的每一條 BLOCK 路徑都要有一個把它打到的案例，否則該路徑等於未被證明）：

| 案例 | 狀態 | 期望 Gate 判定 |
|---|---|---|
| REQ-A | 有 Task 承接、Result = PASS、evidence 非空 | PASS |
| REQ-B | 沒有 Task 承接 | BLOCK |
| REQ-C | 有 Task、沒有 Verification Result | BLOCK |
| REQ-D | 有 Task、Result = FAIL | BLOCK |
| REQ-E | 有 Task、Result = PASS、evidence 空 | BLOCK |
| REQ-F | 有 Task、同一 Contract 兩筆衝突 Result（PASS＋FAIL） | BLOCK（CONFLICT，§7 fail-closed） |

**Core Mechanism PASS ⇔ 六案例判定全對。** 任何一例判錯＝機制問題：停在 Phase 1、回頭改設計，不進 Phase 2。

## 6. Phase 2：Real Artifact Smoke（整合驗證）

僅在 Core Mechanism PASS 後執行。用 OpenSpec CLI 新立一個極小真實 change——內容為「CLAUDE.md 階段界線重表述」（方向文件 §6 未決 #2，本來就要做的真工作）——當 specimen，走一次 happy path：

```
真實 Requirement / Scenario 讀得到
  → 真實 Task + provisional Contracts 標註建得起 reference
  → Inspection 型 Verification Result 掛得回 Contract
  → Gate 依這些資料 PASS
```

- **刻意選文件型 change**：其 Verification Result 為 Inspection 型（evidence 例：`inspected CLAUDE.md against approved requirement; wording reflects the agreed phase boundary`），驗證 Result / Evidence 機制不只適用於 automated test。
- **Routing exception（明記）**：三軌制下純文件小改平時走直接 commit、不進 opsx change。這次讓它走完整鏈**是實驗本身**——它是 PoC specimen（風險低、結果易判讀、由 CLI 產生真實 artifacts），不是 workflow 政策改變；本 spec 不將小文件變更升格為必走 OpenSpec 的工作類型。
- **不順便測更多**：Phase 2 只驗上面四步。任何 §3 non-goal 項目不因「這是真 change」而加入。
- 不故意破壞真資料——負面案例已由 Phase 1 覆蓋。

**Integration PASS ⇔ smoke 走通。**

## 7. Provisional Representations（暫定形狀，非正式 schema）

本 PoC 新增的兩個形狀**全部標 provisional**——要驗的是「這種關係是否可行」，不是「這個 syntax 是最終標準」。PoC 完成後再依結果決定正式資料形狀。

| 形狀 | 內容 | 責任 |
|---|---|---|
| Task 的 Contracts 標註 | `tasks.md` 內每張 Task 標明承接哪些 Requirement / Scenario（即方向文件 §4.1 要補的欄；具體寫法實作時定，provisional） | 回答「我承接誰」 |
| 最小 Verification Result | 三欄：`contract`（我在證明誰）＋ `status`（PASS / FAIL）＋ `evidence`（我憑什麼這樣判，一行字：跑了什麼命令／看了什麼／輸出在哪） | 回答「這條 Contract 驗得怎樣、憑什麼」 |

三欄的邊界：再少（拿掉 evidence）就退化成裸 PASS；再多（method / timestamp / actor）就把後續正式設計偷塞進 PoC。**Evidence 在本階段只要求存在**（Gate 檢查非空），用來回答「PASS 憑什麼」；Gate 不驗其真偽、充分性或語意對應。

**Contract 粒度（provisional）**：coverage 以 Requirement 為單位判定；reference 語法允許指到 Scenario。粒度的正式答案不在本 PoC 定死。

**衝突 fail-closed**：同一 Contract 出現互相衝突的 Result（一 PASS 一 FAIL）→ CONFLICT → BLOCK。第一版不做「哪筆較新／較可信」的聰明判斷（那是 freshness 的事）。未能唯一判定有效 PASS 前，一律 BLOCK。

## 8. 結論語意（兩階段分開判讀）

| Core（Phase 1） | Integration（Phase 2） | PoC 整體結論 |
|---|---|---|
| PASS | PASS | **concept supported**——這條機械鏈能在目前的 OpenSpec bridge 裡成立 |
| PASS | FAIL | 機制成立，但目前 artifact integration 不成立（合法結論；失敗訊號指向 parser / artifact 結構，不是 Gate 邏輯） |
| FAIL | （不執行） | 機制不成立；失敗訊號指向 traceability / Gate 邏輯，回頭改設計 |

Fixture green ≠ Repository integration green：**在 Integration PASS 之前，不得宣稱整個 PoC 已證明可整合進目前 bridge。**

## 9. 實作邊界

- **檢查器（validator）**：Python、只用標準庫、唯讀（修改 0 檔）、輸出人讀判定＋exit code。**全程標 throwaway**——它是 PoC 的證據，不是產品；PoC 結束後留檔不維護。
- **落點**：fixture＋檢查器＋PoC 報告放 `docs/superpowers/poc/2026-08-28-traceability-gate/`。
- **不動 `schema.yaml`、不新增正式 artifact type、不修改 schema artifact graph、不改任何現行 bridge 行為。** provisional result fixture 是實驗載體、不是正式 artifact（§7）。

## 10. 產出：PoC 報告

回答兩件事：

1. **Hypothesis 成立與否**（依 §8 三種結論之一，附六案例＋smoke 的實際輸出為證據）。
2. **最小可行載體是什麼**。若答案是「現有 OpenSpec header + tasks.md Contract reference + 最小 Result 檔 + 小 validator 就夠」，明寫——那是好結局，代表不需要更重的機制就能支撐目前這層保證。但必須區分：
   - PoC **證明**：這個載體足以支撐目前 hypothesis；
   - PoC **不證明**：這個載體就是正式架構的最佳／最終資料模型（stable ID、freshness、richer result 是否需要，是後續設計的題目，不因本 PoC 的「夠用」而被預先否決）。
