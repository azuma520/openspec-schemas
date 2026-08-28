# Phase 1 — Core Mechanism 結果（2026-08-28 實跑）

> PoC spec §5 的產出。**Core Mechanism: PASS（6/6 案例判定全對）。**
> 憑據：本目錄 `gate_check.py` 對 `fixture/` 實跑輸出（下方原樣貼上）＋十個變異測試全數如預期。

## 實跑輸出（原樣）

```
Gate report for change 'poc-traceability' (6 requirements via CLI JSON)

  REQ-A    PASS  OK             (REQ-A expired token rejection)
  REQ-B    BLOCK NO_TASK        (REQ-B audit log retention)
  REQ-C    BLOCK NO_RESULT      (REQ-C rate limiting)
  REQ-D    BLOCK RESULT_FAIL    (REQ-D password hashing)
  REQ-E    BLOCK EMPTY_EVIDENCE (REQ-E input validation)
  REQ-F    BLOCK CONFLICT       (REQ-F session timeout)

  REQ-A    expected PASS/OK             got PASS/OK             MATCH
  REQ-B    expected BLOCK/NO_TASK        got BLOCK/NO_TASK        MATCH
  REQ-C    expected BLOCK/NO_RESULT      got BLOCK/NO_RESULT      MATCH
  REQ-D    expected BLOCK/RESULT_FAIL    got BLOCK/RESULT_FAIL    MATCH
  REQ-E    expected BLOCK/EMPTY_EVIDENCE got BLOCK/EMPTY_EVIDENCE MATCH
  REQ-F    expected BLOCK/CONFLICT       got BLOCK/CONFLICT       MATCH

Core Mechanism: PASS (6/6 cases correct)
```

重現指令（於本目錄）：`python gate_check.py fixture poc-traceability --expected expected-phase1.json`（exit 0）。

## 假綠防護：十個變異測試（scratchpad 複本上執行，fixture 本體未動）

第一次實跑即 6/6 全對，依複審紀律先當場破壞每條判斷路徑驗證會轉紅（M1–M5）；
其後兩輪 code review 各抓到一個 coverage 判定漏洞（見下節），修復各自配上打到該漏洞的變異（M6–M10）：

| 變異 | 期望 | 實得 |
|---|---|---|
| M1 REQ-B 補上 task | REQ-B 轉 NO_RESULT → MISMATCH，exit 1 | 如期望 |
| M2 REQ-E evidence 補非空 | REQ-E 轉 PASS → MISMATCH，exit 1 | 如期望 |
| M3 移除 REQ-F 的 FAIL 筆 | REQ-F 轉 PASS → MISMATCH，exit 1 | 如期望 |
| M4 tasks.md 引用不存在的 REQ-Z | INTEGRITY ERROR，exit 2 | 如期望 |
| M5 破壞一條 Requirement 標題行 | 標題數與 CLI JSON 數不符 → exit 2 | 如期望 |
| M6 孤兒 Contracts 標註（上方無 checkbox） | INTEGRITY ERROR，exit 2 | 如期望 |
| M7 REQ-E evidence 為 null | 正常化為空 → 仍判 EMPTY_EVIDENCE，exit 0 | 如期望 |
| M8 evidence 型別為數字 | INTEGRITY ERROR，exit 2 | 如期望 |
| M9 與 checkbox 同層級的 Contracts 標註 | INTEGRITY ERROR，exit 2 | 如期望 |
| M10 較 checkbox 更淺縮排的 Contracts 標註 | INTEGRITY ERROR，exit 2 | 如期望 |

（expected 判定表先於 gate 邏輯寫定——`expected-phase1.json` 在 `gate_check.py` 動筆前落檔。）

## Code review 輪次（Codex，standard tier）

| 輪 | 結果 | 內容 |
|---|---|---|
| 1 | ⛔ Blocked | P1：`- Contracts:` 行未驗證附屬於 task checkbox，孤兒標註＋一筆 PASS 可偽造 coverage；P2：results 欄位無型別驗證，`evidence: null` 會 crash 而非判 BLOCK。兩者同檔一併修（P2 屬 sub-threshold，因同檔開著順手修，非另開修復輪） |
| 2 | ⛔ Blocked | P1：第一版修法只看相鄰不看縮排——同層級 sibling `- Contracts:` 仍被算 attached。改為記錄 checkbox 縮排、標註必須嚴格更深 |
| 3 | ✅ Ready | 複驗零新缺陷，gate_reason=NONE |

## 實作時定案的 provisional 決定（全部僅限本 PoC，非正式 schema）

| 決定 | 內容 | 理由 |
|---|---|---|
| Contracts key | Requirement 標題第一個 token 為 contract ID（`### Requirement: REQ-A <desc>` → `REQ-A`）；重複 ID 直接 abort | Step 0 發現 #3 三選項中選「自抽標題行」：位置序號脆弱、全文 text 過長；一行正則抽取＋與 CLI JSON requirement 數交叉核對，非重解 Markdown |
| Results 載體 | `verification-results.json`（list of `{contract, status, evidence}`） | 標準庫 `json` 直接吃，三欄不多不少（spec §7） |
| tasks.md 標註 | checkbox 下縮排一行 `- Contracts: REQ-X[, REQ-Y]`，且縮排必須嚴格深於其 checkbox（孤兒／同層／更淺縮排一律 INTEGRITY ERROR）；允許 `REQ-A/scenario 名`，coverage 收斂到 `/` 前的 Requirement | 對真格式 tasks.md 是純追加、不動既有形狀；附屬關係用縮排機械判定（review 輪 1、2 的修正）；scenario-level reference 允許但非 Core 必要（spec §1 粒度邊界） |
| Gate 判定順序 | NO_TASK → NO_RESULT → CONFLICT → RESULT_FAIL → EMPTY_EVIDENCE → PASS（首個不過即定案） | fail-closed：衝突優先於單一 FAIL；evidence 檢查涵蓋所有筆 |
| 引用完整性 | tasks.md / results 引用不存在的 contract ⇒ exit 2（INTEGRITY ERROR），不進 Gate 判定 | 壞引用若靜默略過，coverage 會被幽靈引用撐出假 PASS |
| results 型別驗證 | 每筆須為物件、contract/status 為字串、evidence 為字串或 null（null 正常化為空字串 → 判 EMPTY_EVIDENCE）；其餘型別 ⇒ exit 2 | 壞資料要嘛正常進 Gate 判定、要嘛顯式 INTEGRITY ERROR，不允許 crash（review 輪 1 P2） |

## 附帶實測發現（供後續正式設計）

- 最小結構再確認：手造 change 僅需 `openspec/changes/<id>/proposal.md` ＋ `specs/`，`show --json` / `validate --json` 即可讀，無需 init / config（Step 0 發現 #1 的再現，本次在 fixture 落點原地驗證）。
- M5 的細節：標題行破壞後 CLI JSON 仍報 6 條 requirement（CLI 對 `### Requirement` 後綴寬鬆），是「標題抽取 vs CLI 計數」交叉核對抓到不一致——單靠任一來源都會漏。

## 結論語意（照 spec §8）

Core（Phase 1）= **PASS**。依規則可進 Phase 2（真 artifact smoke）。
**尚不得宣稱**：PoC 整體成立、可整合進目前 bridge（那要等 Integration PASS）；Scenario-level traceability 已證明；語意正確性有任何覆蓋（§3 non-goals 未動）。
