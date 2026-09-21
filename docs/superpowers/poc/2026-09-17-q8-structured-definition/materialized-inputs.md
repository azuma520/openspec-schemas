# 實際餵給判讀者的輸入（materialized inputs）

> **這份檔案為什麼存在**：`inputs-six-cases.md`（SHA256 凍結）描述的是六個案例的**由來與
> 事前判定**，它**不含**每個案例完整的 `tasks.md` / `plan.md` 兩側材料——I3 與 I5 在該檔
> 裡只有 plan.md 片段。實際派給判讀者的是下面這六組完整配對。
>
> 這個落差是 2026-09-21 的 fallback 文件審抓到的：報告 §6 的「機械驗證」區塊標稱
> 出自「六個輸入檔」，但那些數字其實是對這些 materialized 配對跑的，而當時 repo 內
> 沒有任何一份檔案記載它們。**凍結檔未被修改**；本檔是補上缺的那一半記錄。
>
> 每組的 plan.md 為最小構造，選擇原則是**不引入自身的 finding**，除了 I3 與 I5——
> 那兩組的 plan.md 本身就是案例的主體。
>
> 產生來源：`gen_pairs.py` 的 `INPUTS`（session scratchpad）。下方內容已驗證與實際
> 派工的配對檔逐位元相同，驗證方法見本檔末。

## I1 — 同一筆紀錄兩行 `subject:`
### `tasks.md`
````markdown
## 1. Group

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
````
### `plan.md`
````markdown
## 1.1 — Foo
````

## I2 — 紀錄完全沒有 `subject:`
### `tasks.md`
````markdown
## 1. Group

- [x] 1 Add email validation
  - TDD: applicable
  - RED:
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS
````
### `plan.md`
````markdown
## 1 — Add email validation
````

## I3 — `###` 子標題落在 `##` entry 底下
### `tasks.md`
````markdown
## 1. Group

- [x] 1.1 Add email validation
  - TDD: n/a — prose-only
````
### `plan.md`
````markdown
## 1.1 — Add email validation

### 1.1 — Interface detail
````

## I4 — `]` 後沒有空白：`- [x]1.1 Foo`
### `tasks.md`
````markdown
## 1. Group

- [x]1.1 Foo
  - TDD: n/a — prose-only
````
### `plan.md`
````markdown
## 1.1 — Foo
````

## I5 — `## 1x` 開頭的 plan 標題
### `tasks.md`
````markdown
## 1. Group

- [x] 1 Add email validation
  - TDD: n/a — prose-only
````
### `plan.md`
````markdown
## 1x — Add email validation
````

## I6 — 圍籬程式碼區塊裡的 `- [x]`
### `tasks.md`
````markdown
## 1. Group

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
### `plan.md`
````markdown
## 1 — Add email validation
````

## 驗證
本檔每組 `tasks.md` / `plan.md` 區塊，與實際派給判讀者的配對檔 （`pairs/A1_I*.md` 等 24 份）中的對應區塊做子字串比對：

| 案例 | tasks.md 逐位元相同 | plan.md 逐位元相同 |
|---|---|---|
| I1 | ✅ | ✅ |
| I2 | ✅ | ✅ |
| I3 | ✅ | ✅ |
| I4 | ✅ | ✅ |
| I5 | ✅ | ✅ |
| I6 | ✅ | ✅ |
