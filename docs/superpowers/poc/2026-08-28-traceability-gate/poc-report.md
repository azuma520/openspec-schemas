# PoC 報告：最小 Traceability + Completion Gate（2026-08-28）

> PoC spec（[設計文件](../../specs/2026-08-28-concept-poc-traceability-gate-design.md)）§10 的產出。
> Phase 1 憑據見 [phase1-core-results.md](./phase1-core-results.md)；Phase 2 憑據見下方原樣輸出。

## 結論（照 spec §8）

| Core（Phase 1） | Integration（Phase 2） | PoC 整體結論 |
|---|---|---|
| **PASS**（6/6 案例＋10 變異全如預期） | **PASS**（真 change smoke 四步走通） | **concept supported**——這條機械鏈能在目前的 OpenSpec bridge 裡成立 |

## 問題一：Hypothesis 成立與否

**成立（concept supported）**。Completion Gate 可以從「裸 completion claim」升級為依賴結構化 Verification Record（contract + status + evidence）的機械判定：

- **Phase 1（機制）**：六案例（有任務有 PASS 有憑據／無任務／無結果／結果 FAIL／憑據空／結果衝突）判定全對；每條 BLOCK 路徑都有變異證明會轉紅，非假綠。
- **Phase 2（整合）**：specimen 為真實工作「CLAUDE.md 階段界線重表述」（方向文件 §6 未決 #2，使用者 2026-08-28 拍板甲案措辭），以 `openspec new change claude-md-phase-boundary --schema superpowers-bridge` 建立、CLI validate 通過。happy path 實跑輸出（原樣）：

```
Gate report for change 'claude-md-phase-boundary' (1 requirements via CLI JSON)

  REQ-PB   PASS  OK             (REQ-PB event-gated schema work boundary)

Gate: PASS
```

  四步逐一成立：①真實 Requirement/Scenario 由 `openspec show --json --deltas-only` 讀到②真實 Task＋provisional Contracts 標註建起 reference③**Inspection 型** Verification Result 掛回 Contract（證明 Result/Evidence 機制不限 automated test）④Gate 依這些資料 PASS。

**宣稱邊界（不因 PASS 而擴大）**：未消除 Agent 自我宣稱（status/evidence 仍可由 Agent 寫出）；未證明語意正確性、evidence 真偽、freshness（spec §3 non-goals 未動）；Scenario-level traceability 未被完整證明（coverage 以 Requirement 為單位）。

## 問題二：最小可行載體是什麼

**現有 OpenSpec 結構 + 三個小補充就夠**，不需要一整個 Traceability Framework：

| 缺口 | 載體（全部 provisional） |
|---|---|
| Task 承接誰 | `tasks.md` checkbox 下縮排 `- Contracts: <ID>`（縮排嚴格深於 checkbox） |
| Contract 驗得怎樣、憑什麼 | `verification-results.json` 三欄（contract / status / evidence） |
| Complete 資格判定 | 一支小型標準庫 Gate（`gate_check.py`；coverage / result / evidence 非空 / CONFLICT fail-closed） |

Requirement/Scenario 讀取全數復用 CLI JSON（Step 0 判準守住：validator 未重解 Markdown；唯一補充是一行標題抽取＋與 CLI 計數交叉核對）。

**必須區分**：
- PoC **證明**：這個載體足以支撐目前 hypothesis。
- PoC **不證明**：這個載體就是正式架構的最佳／最終資料模型——stable ID、freshness、richer result 是否需要，是後續正式設計的題目，不因本 PoC 的「夠用」而被預先否決。

## 過程中的架構訊號（供正式設計）

1. **連這麼小的 Gate 也會有結構檢查被繞過的洞**：兩輪 code review 各抓到一個 coverage 偽造路徑（孤兒標註／同層 sibling 標註），都要靠「附屬關係的機械定義」（縮排）補死——正式設計時 Contracts 標註的附屬語法要一開始就定義成機械可判。
2. **單一來源不夠，交叉核對才抓得到**：標題抽取數 vs CLI JSON requirement 數的比對，實際攔下 CLI 對破損標題行的寬鬆解析（M5）。
3. **change 層 CLI JSON 不含 Requirement 標題名**（Step 0 發現 #3）：正式設計若要用標題名當 contract key，抽取責任落在 Gate 側；或改推 stable ID。
