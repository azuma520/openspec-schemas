# 事前登記（pre-registration）

登記時間：2026-09-17，**在任何判讀者被派出之前**。

## 被凍結的是什麼

`inputs-six-cases.md` 裡的六個 expected verdict。

```
SHA256(inputs-six-cases.md) = 55680e38cf37408edf5947889de3eb7b0f3d71201b6324d5263e01996dcb1209
```

看到結果之後 **MUST NOT** 修改該檔的期望判定。若判讀結果顯示某個 expected
本身是錯的，記為 **experiment specification defect**，與 Agreement / Correctness
分開列，不得回頭改答案再宣稱一致。

## 三個量測（本輪唯一的主指標）

| 指標 | 定義 | 怎麼算 |
|---|---|---|
| **Determinacy 可判性** | 判讀者給得出 `PASS` 或 `BLOCK`，而不是 `UNDETERMINED` | 非 UNDETERMINED 的格數 ÷ 總格數 |
| **Agreement 一致性** | 獨立判讀者對同一格是否給同一答案 | 只在有重跑的格子上算 |
| **Correctness 對事前答案** | 與上方凍結的 expected verdict 是否一致 | 相符格數 ÷ 總格數 |

⚠️ 本輪量的**不是**「同一個 Agent 重複判是否穩定」。派的是 fresh independent
reader，所以真正量到的是：**同一模型、同一派工條件下，不同獨立判讀者對同一
文本與同一輸入會不會得到不同答案**——即「這種寫法會不會讓不同 Agent 各自
理解成不同東西」。

## I6 的特別處置

I6（圍籬內 `- [x]`）**從主比較中分離**，因為它是 **policy gap**：
`schema.yaml` 全檔沒有一句規定圍籬 / HTML 註解要不要排除（grep 零命中）。

- 它的 Determinacy **照常計入**（文字能不能給出唯一判定，是可判性問題）。
- 它的 Correctness **不計入**，且 **MUST NOT** 被讀成任何 Arm 的改善或失敗——
  結構化表示不會憑空補出一條沒人寫過的政策。

## 結論邊界（事前就寫死，避免事後放寬）

1. 六個輸入**沒有一個**直接取自既有 fixture；其中四項在 13 個 fixture 全集中
   命中 0。因此本輪 **MUST NOT** 宣稱「改善了既有 fixture 覆蓋的行為」。
   可宣稱的範圍只有：**針對六個真實 finding / boundary case 的判讀實驗**。
2. `Shared definitions, used by checks 8-11` 實際射程含 check 12——記為
   finding，**不是** B 實驗的結果，不進三個指標。
3. 本輪不改 `schema.yaml`、不補 fixture、不修上述那句、不處理 I6 的 policy
   gap。全部只記 finding。

## 已知污染源（誠實記錄，不辯解）

- **Arm 2 / Arm 3 由我撰寫，而我已知六個 expected verdict。** 緩解：Arm 2/3 的
  內容只能來自 Arm 1 的重新表達，**不得新增任何 Arm 1 沒有的規則**——特別是
  不得加入任何一句解決 I6 的話。資訊量對等性在派工前逐條自查並記錄。
- **判讀者是有工具的 subagent，理論上可能去翻 repo 找到答案。** 緩解：派工詞
  明令不得使用任何工具、不得讀任何檔案，材料自足。此風險記為限制，不宣稱已
  消除。
