# 六個驗收輸入（Q8 鎖定，不增不減）

> 每個輸入都標明**出處**與**是否為構造**。期望判定若涉及未定政策，標「未定」，
> 不由本實驗代拍。判定依據一律引 `superpowers-bridge/schema.yaml` 行號。
>
> **fixture 覆蓋盤點（實查，非推論）**：13 個既有 fixture 位於
> `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/`。
> 對六個輸入逐一 grep 的結果——`###` 標題、`]` 後無空白的 task line、圍籬區塊、
> 同一筆紀錄兩行 `subject:`，**四者在 fixture 全集中命中 0**。
> 這與 `code-rereview-fallback-3.md` 自己記的「三條規則無 fixture」一致並多一條。
> 因此本表六個輸入**沒有一個**能直接取自 fixture，全部來自報告逐字引用或最小構造。

---

## I1 — 同一筆紀錄兩行 `subject:`

**出處**：`docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/codegate-fixes-report.md:82-93`，逐字引用（非構造）。

```
- [x] 1.1 Foo
  - TDD: applicable
  - RED:
    - subject: a::b
    - subject: c::d
    - outcome: FAIL
    - failure: expected X, got undefined
  - GREEN:
    - subject: a::b
    - outcome: PASS
```

**期望判定：BLOCK（已定）**，且恰好兩條 finding：
- check 9 FIELD CARDINALITY（`schema.yaml:634-656`）：RED 帶兩行 `subject:` → BLOCK，點名 `subject:`。
- check 11 stage two（`schema.yaml:747-752`）：該 RED 不進任一 list，RED list `{}`、GREEN list `{a::b}` → `a::b` 有 GREEN 無 RED → BLOCK。
- check 10 **不**報：該紀錄只有一行 `outcome:`，carve-out 不適用（`schema.yaml:692-694`）。
- check 9 的 SUBJECT GRAMMAR **不**在該鍵上評值（`schema.yaml:648-653`）。

**這個輸入的難點**：正確答案不只是「BLOCK」，而是「哪幾條報、哪幾條刻意不報」。只答 BLOCK 不算判對。

---

## I2 — 紀錄完全沒有 `subject:`

**出處**：**最小構造**。取 fixture `f7-blank-spaced-record/tasks.md` 逐字，刪去 RED 的 `- subject:` 那一行；其餘一字未動。

```
- [x] 1 Add email validation
  - TDD: applicable
  - RED:
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS
```

**期望判定：BLOCK（已定）**
- check 9（`schema.yaml:627-628`、`681-685`）：RED 缺必填 `subject:` → BLOCK。
- check 11（`schema.yaml:725-728`）：無 `subject:` 的紀錄不進任一 list → RED list `{}`、GREEN list `{test/auth.test.js::rejects empty email}` → stage two 單向差異 → BLOCK。

---

## I3 — `###` 子標題落在 `##` entry 底下

**出處**：`schema.yaml:810-813` 的規則本文逐字舉例（`### 1.1 — <detail>` 位於 `## 1.1 — <title>` 之下）。plan.md 側最小構造。

```
## 1.1 — Add email validation

### 1.1 — Interface detail
```

**期望判定：這一項本身 NOT BLOCK（已定）**
- check 12（`schema.yaml:810-813`）：`###` 或更深是 entry **內部**的子標題，不被蒐集 → 不構成 `1.1` 重複 key。

**這個輸入測的是「不該報的別報」**，與 I1/I2 方向相反；把 `###` 誤收會造成假 BLOCK。

---

## I4 — `]` 後沒有空白：`- [x]1.1 Foo`

**出處**：`schema.yaml:794` 與 `codegate-fixes-report.md:167`，兩處皆逐字含此字串。

```
- [x]1.1 Foo
  - TDD: applicable
```

**期望判定：BLOCK（已定）**，但有一個**兩段式**的必答點：
- 共用定義段（`schema.yaml:563-566`）：首個非空白字元為 `- [`、一字元、`]` → **它是 TASK LINE**（`]` 後有無空白不影響「是不是 task line」）。
- check 12（`schema.yaml:792-795`）：`]` 後至少要有一個空白字元，沒有 → **沒有 task number** → 這本身就是 check 12 的 defect → BLOCK。**不得**讀成 task number 為 `1.1`。

**難點**：同一行在兩個層級上答案相反（是 task line／不是 task number）。把兩者混為一談就會判錯。

---

## I5 — `## 1x` 開頭的 plan 標題

**出處**：`schema.yaml:807` 逐字列舉（`1x`、`1.1a`、`1.` 三例之一）。

```
## 1x — Add email validation
```
（搭配 tasks.md 側存在 `- [x] 1 Add email validation`）

**期望判定：BLOCK（已定）**
- check 12（`schema.yaml:803-809`）：token 兩側都要被界定，`1x` 的數字後緊接非空白 → **不以數字開頭** → 不帶 entry key，**不得**讀成 key `1` 而把 `x` 忽略。
- 於是 tasks 側的 `1` 找不到對應 entry → stage two 單向差異 → BLOCK。

---

## I6 — 圍籬程式碼區塊裡的 `- [x]`

**出處**：research `2026-09-10-contract-drift-archaeology.md` §2 #53；最小構造如下。

````
## 1. Fixture group

- [x] 1 Add email validation
  - TDD: applicable
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS

範例（僅供說明，不是真的任務）：

```
- [x] 9 這行只是範例
```
````

**期望判定：未定 —— 且「未定」正是這一格的發現。**

窮盡查證結果（`grep -niE "fenc|code block|backtick|html comment|<!--"`）：
`superpowers-bridge/schema.yaml` **全檔零命中**；`templates/tasks.md` 只有它自己用的
`<!--` 註解、沒有任何一句在講圍籬或註解要不要排除。

所以：
- **照字面**，`- [x] 9 這行只是範例` 的首個非空白字元符合 `- [`、一字元、`]` → 它**是** TASK LINE → 沒帶 TDD 標註 → check 8 BLOCK。
- **照意圖**，它顯然不該算。但意圖**沒有寫在任何地方**。

⚠️ 這一格要分兩個量記，不能合併：
1. **有沒有唯一判定** —— Arm 1 其實給得出唯一答案（BLOCK），所以「可判性」這一欄它是通過的。
2. **判定是否合乎意圖** —— 無法評，因為意圖未定。**這是政策缺口，不是 tokenizer 缺口**，結構化不會自己補上它。

把 1 和 2 混在一起記，會讓結構化看起來「修好了一個它其實沒修的東西」。

**現況佐證**：`templates/tasks.md` 的兩個 `<!--` 區塊內沒有任何 `- [` 開頭的行
（`- RED:`、`- invocation:` 皆非），故 bridge 自己的範本目前**沒有**踩到這個洞。
缺口為真、活體實例為零。
