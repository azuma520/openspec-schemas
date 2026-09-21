# tasks.md / plan.md 驗證規則

## PART I — 定義層（結構化）

本節只定義「怎麼從文字取出東西」，不含任何判定。

下述 checks 8-12 皆為 **DETERMINISTIC**：各自依固定規則讀文字決定判定，不含判斷取捨。標註文法與紀錄形狀的定義來自 `tasks` artifact 的指令；這些 check 讀的正是該文法，不另外增加任何東西。

### §L 詞法層

| id | 定義 |
|---|---|
| L1 | `INDENT(x)` = 行 `x` 的前導空白字元數。 |
| L2 | `BLANK(x)` = 行 `x` 不含任何非空白字元。 |
| L3 | `TASKLINE(x)` = `x` 的首批非空白字元依序為 `- [`、**恰一個字元**、`]`。（`- [ ]`、`- [x]`、`- [~]` 一律成立。） |
| L4 | `HEADING(x)` = `x` 的首個非空白字元為 `#`。 |

### §N 巢狀層

設 `t` 為一個 task line，`N = INDENT(t)`。

| id | 定義 |
|---|---|
| N1 | `RANGE(t)` = `t` 之後的行，止於**第一個非空白**且滿足（`TASKLINE(y)` 或 `HEADING(y)`）且 `INDENT(y) <= N` 的行 `y`（不含 `y`）；若無此行則止於檔尾。 |
| N2 | `BELONGS(x, t)` = `x` 屬於 `RANGE(t)` 且 `INDENT(x) > N`。 |
| N3 | **任何** `INDENT(x) > N` 皆成立。不要求特定縮排寬度。 |
| N4 | **空白行透明**：空白行不屬於任何東西、也不終止任何東西；跳過它繼續讀。 |

### §R 紀錄層

| id | 定義 |
|---|---|
| R1 | `RECORD(r, t)` = `BELONGS(r, t)` 且 `r` 去縮排後為 `- RED:` 或 `- GREEN:`。設 `R = INDENT(r)`。 |
| R2 | `RANGE(r)` = `r` 之後的行，止於**第一個非空白**且 `INDENT(z) <= R` 的行 `z`（不含 `z`）。 |
| R3 | `FIELD(f, r)` = `f` 屬於 `RANGE(r)` 且 `INDENT(f) > R` 且 `f` 去縮排後形如 `- <key>: <value>`。 |
| R4 | **一個 field 恰為一行**；其值止於該行行尾。 |
| R5 | `RANGE(r)` 內**不**符合 R3 的行：不是 field、**不是上一個 field 的續行**、不貢獻任何東西、**其存在本身不是錯誤**。 |
| R6 | **CARDINALITY**：同一筆紀錄內，每個 key **至多出現一次**。此規則適用每個 key，不分必填與否。 |
| R7 | `REQUIRED(RED)` = {`subject`, `outcome`, `failure`}；`REQUIRED(GREEN)` = {`subject`, `outcome`}；`invocation` **從不**必填。 |

### §V 值文法

| id | 定義 |
|---|---|
| V1 | `SUBJECT_OK(v)`：令 `w = trim(v)`；由左而右掃描 `w` 尋找兩字元序列 `::`，**比對到就消耗、不重疊**（故 `a:::b` 含**一**次）。成立當且僅當恰好一次**且**其左右兩側 trim 後皆非空。**除此之外一律不限制**——不限路徑寫法、不限副檔名、不限測試名稱字元。 |
| V2 | `OUTCOME_GREEN_OK(v)` 成立當且僅當 `trim(v)` **恰為** token `PASS`。 |
| V3 | `OUTCOME_RED_OK(v)` 成立當且僅當 `trim(v)` 為單一 token、僅含大寫 A-Z、不含空白，**且不為** `PASS`。 |
| V4 | `NONEMPTY(v)` 成立當且僅當 `trim(v)` 不為空字串。 |

### §A 標註文法

| id | 定義 |
|---|---|
| A1 | `TDD_LINE(x, t)` = `BELONGS(x, t)` 且 `x` 去縮排後為 `- TDD: applicable` **或** `- TDD: n/a <SEP> <reason>`，其中 `<SEP>` 為 `—`、`–`、`-`、`--` 四者之一（僅此四者）且 `NONEMPTY(reason)`。**開頭的 `- ` 是必要形式的一部分。** |

### §K 鍵文法

| id | 定義 |
|---|---|
| K1 | `TASKNUM(t)`：`t` 的 checkbox `]` 之後**必須至少有一個空白字元**；其後緊接的 token 若符合 `\d+(\.\d+)*` 則為 `TASKNUM`。`]` 後無空白 → **無 TASKNUM**。該 token 非數字 → **無 TASKNUM**。 |
| K2 | `ENTRYKEY(h)`：**僅**對層級**恰為 `##`** 的標題成立。自 `##` 後第一個非空白字元起取前導 `\d+(\.\d+)*` token；該 token **末位數字的下一個字元必須是空白或行尾**。否則**無 ENTRYKEY**。`###` 或更深**不蒐集**——它是某個 entry **內部**的子標題。 |

## PART III — 判定程序（可執行順序）

> 輸入：`tasks.md` 的行序列；`plan.md` 的行序列（或「不存在」）。
> 輸出：一組 finding。**finding 集合為空 ⟺ PASS**；否則 **BLOCK**。
> **沒有任何步驟會短路**：每一步都跑完，findings 累加。

```
P0.  T := [ t : TASKLINE(t) ]                      # 依出現順序（L3）

P1.  對每個 t 屬於 T：                              # check 8
       A(t) := [ x : TDD_LINE(x, t) ]              # A1 + N2
       若 |A(t)| 不等於 1 → emit F8(t, |A(t)|)

P2.  APPLICABLE := [ t 屬於 T : |A(t)| = 1 且 A(t)[0] 為 "- TDD: applicable" ]

P3.  對每個 t 屬於 APPLICABLE：                     # check 9 存在性
       REDS   := [ r : RECORD(r,t) 且 r 為 "- RED:"   ]
       GREENS := [ r : RECORD(r,t) 且 r 為 "- GREEN:" ]
       若 |REDS|   = 0 → emit F9_missing(t, RED)
       若 |GREENS| = 0 → emit F9_missing(t, GREEN)

P4.  對每個 t 屬於 APPLICABLE、每筆紀錄 r 屬於 REDS 或 GREENS：
       FIELDS(r) := { f : FIELD(f, r) }            # R3；R5 的行直接丟棄
       DUP(r)    := { k : k 在 FIELDS(r) 出現超過一次 }        # R6
       對每個 k 屬於 DUP(r) → emit F9_dup(r, k)
       # 注意：k 屬於 DUP(r) 的鍵，以下 P4 尾段、P5、P6 一律跳過它
       對每個 k 屬於 REQUIRED(type(r)) 且 k 不屬於 DUP(r)：     # R7
         若 k 不屬於 FIELDS(r)        → emit F9_missing_field(r, k)
         否則若 NONEMPTY(value) 不成立 → emit F9_empty(r, k)

P5.  對每個上述 r，若 subject 屬於 FIELDS(r) 且 subject 不屬於 DUP(r)：  # check 9 文法
       若 SUBJECT_OK(value) 不成立   → emit F9_grammar(r, value)

P6.  對每個上述 r：                                 # check 10
       若 outcome 屬於 DUP(r)        → 不產出判定（已由 P4 回報）
       否則若 outcome 不屬於 FIELDS(r) → 不產出判定（已由 P4 回報）
       否則 type(r)=GREEN 且 OUTCOME_GREEN_OK(v) 不成立 → emit F10(r, v)
            type(r)=RED   且 OUTCOME_RED_OK(v)   不成立 → emit F10(r, v)

P7.  對每個 t 屬於 APPLICABLE：                     # check 11
       RL := [ trim(subject 值) : r 屬於 REDS,   subject 屬於 FIELDS(r), subject 不屬於 DUP(r) ]
       GL := [ trim(subject 值) : r 屬於 GREENS, subject 屬於 FIELDS(r), subject 不屬於 DUP(r) ]
       # 順序保留；值視為不透明字串，逐字元比較
       # STAGE ONE（不短路）
       對每個在 RL 出現超過一次的值 v → emit F11_dup(t, v, RED)
       對每個在 GL 出現超過一次的值 v → emit F11_dup(t, v, GREEN)
       # STAGE TWO（無論 STAGE ONE 結果為何都執行）
       對每個 v 屬於 set(RL) 但不屬於 set(GL) → emit F11_unpaired(t, v, RED_only)
       對每個 v 屬於 set(GL) 但不屬於 set(RL) → emit F11_unpaired(t, v, GREEN_only)

P8.  # check 12
     TN := [ TASKNUM(t) : t 屬於 T 且 TASKNUM(t) 存在 ]        # K1
     對每個 t 屬於 T 且 TASKNUM(t) 不存在 → emit F12_no_number(t)
     若 plan.md 不存在 → emit F12_no_plan（訊息："plan.md absent — no entry keys to compare"）
     否則 EK := [ ENTRYKEY(h) : h 為 plan.md 的 "##" 標題且 ENTRYKEY 存在 ]   # K2
       若 EK 為空 → emit F12_no_keys
       # STAGE ONE（不短路）
       對每個在 TN 出現超過一次的 k → emit F12_dup(k, tasks)
       對每個在 EK 出現超過一次的 k → emit F12_dup(k, plan)
       # STAGE TWO（無論 STAGE ONE 結果為何都執行）
       對每個 k 屬於 set(TN) 但不屬於 set(EK) → emit F12_missing(k, no_entry)
       對每個 k 屬於 set(EK) 但不屬於 set(TN) → emit F12_missing(k, no_task)

P9.  findings 為空 → PASS；否則 BLOCK。
```

### 程序附註（理由，非規則）

- **P4 的 `DUP` 豁免只及於重複的那個鍵。** 一筆因 `failure:` 重複被擋的紀錄，其單一 `subject:` 仍走 P5。理由：若對重複鍵評值，執行者得選讀哪一個值，兩個執行者會對同一輸入得出相反判定。
- **STAGE ONE 先於 STAGE TWO 且不短路。** 集合會吸收重複，集合比對根本看不見重複；而兩者修法不同（重新命名 vs 補上缺的一側），故訊息必須可分辨。
- **P7 的配對絕不依序位。** 序位配對會讓插入一筆紀錄就靜默重配它之後的每一筆。
- **N3 的任何縮排寬度。** 契約要求的是巢狀，不是欄位寬度；被 formatter 重排縮排的合規檔案不得因此被擋。
- **重跑測試不會多出一筆紀錄。** 一個 subject 永遠一 RED 一 GREEN，不論執行過幾次；唯一性正是配對之所以可判的原因。
- **P8 兩個 stage 合起來就是 1:1 宣稱的全部。** 各側唯一加上集合相等，恰好是兩組 key 之間的雙射；本步驟只讀 key，entry 的契約文字是否描述了它那個任務屬 review judgement。
- **本程序只決定結構、形式與基數。** 它**絕不**決定證據真偽——具名測試是否存在、是否測了任務宣稱交付的行為、記錄的 outcome 是否真的發生過、RED 是否先於實作取得，皆不在此決定。
