# Q8 實驗證據集（事後救回，2026-09-21）

> **這份目錄不是實驗當時的凍結產物。** 它是 2026-09-21 從一個會被回收的 session
> scratchpad 事後複製出來的。保存的目的只有一個：**保住現存的證據鏈不再繼續流失**。
>
> ⚠️ **保存這個動作不改變任何歷史事實的證明力。** 實驗當時（2026-09-17）與報告
> 提交當時（commit `ff3e806`），repo 內**沒有**這批材料。2026-09-21 的 Codex 文件審
> 依 repo 現況判定「證據鏈不存在、無法獨立稽核」——**那個判定在當時是正確的**。
> 本目錄使後續的重驗成為可能，**不使**「實驗當時已完整凍結／可重現」成為真。
> 任何引用本目錄的文字都不得做這種升級。

## 這批東西怎麼被找到的

2026-09-21 的文件審回報找不到派工檔與產生器。追查時發現它們還活在
`%TEMP%\claude\<專案>\<session-uuid>\scratchpad\` 底下——該目錄會隨 session 回收。
若該輪審查沒有點名這件事，這批材料會在無人察覺的情況下消失，與
2026-09-04 worktree handoff 未追蹤檔永久消失屬同一類事故（證據只存在於會消失的位置）。

## 內容

| 路徑 | 是什麼 |
|---|---|
| `pairs/` | 24 份派給判讀者的完整檔案（4 個 Arm × 6 個輸入）。每份自包含：規則全文 + 待驗的 `tasks.md` / `plan.md` + 作答指令 |
| `generators/gen_pairs.py` | 產生 A1/A2/A3 派工檔的腳本，內含六組輸入的字面來源（`INPUTS`） |
| `generators/gen_arms.py` | 產生 A2 / A3 兩份結構化 Arm 文字 |
| `generators/gen_arm0.py` | 產生 A0 派工檔（重用 `gen_pairs.py` 的 `INPUTS` 與指令文字） |
| `generators/gen_materialized.py` | 產生 `../materialized-inputs.md` |
| `results.json` | 2026-09-17 當天寫下的逐格 verdict 與判定路徑 |

## ⚠️ 證明力分級：哪些是同期產物、哪些不是

**這是本檔最重要的一節。** 三種檔案的證明力不同，不可一概而論。

| 檔案 | 檔案 mtime | 與它所記錄的事件的關係 |
|---|---|---|
| `results.json` | 2026-09-17 18:18 | **同期**。寫於 round 1 當天，早於報告。是本目錄中唯一與 09-17 那一輪同期的紀錄 |
| `generators/gen_pairs.py` | 2026-09-17 18:15 | **同期**。早於 `results.json`，運行後未再被修改 |
| `generators/gen_arms.py` | 2026-09-17 18:13 | **同期** |
| `pairs/A0_I*.md`（6 份） | 2026-09-21 07:59 | **同期**——A0 這一輪本來就是 2026-09-21 才跑的 |
| `generators/gen_arm0.py` | 2026-09-21 07:59 | **同期**（同上） |
| `pairs/A1_*`, `A2_*`, `A3_*`（18 份） | **2026-09-21 08:45** | ❌ **不是同期**。見下 |

**那 18 份是重新產生的，不是 09-17 實際派出去的那些位元組。**
2026-09-21 執行 `gen_materialized.py` 時，它 exec 了 `gen_pairs.py`，而後者會重寫
`pairs/`。09-17 當天產生的原始檔案已被覆寫，**沒有留下任何同期副本**。

可以說的是：`gen_pairs.py` 本身的 mtime（09-17 18:15）早於 `results.json`（18:18），
運行後未再修改，所以這次重新產生**預期**忠實。
不可以說的是：這 18 份「就是當時派出去的檔案」。那個宣稱已經沒有東西可以支持。

## 仍然存在、且本目錄補不上的缺口

1. **沒有任何一格的原始判讀回覆全文**（24 格皆無）。`results.json` 只保留了
   verdict 與一句判定路徑，且僅涵蓋 A1/A2/A3 共 18 格。
2. **A0 那 6 格沒有任何同期紀錄**。A0 的 verdict 只出現在報告裡，沒有
   `results.json` 等價物。
3. **判讀者身分、盲判程序、每格一位 fresh reader 的設計，皆無可稽核紀錄。**
   這些目前只有作者宣稱。
4. **`pre-registration.md` 早於派工**這件事無法佐證——該檔與結果同在
   commit `ff3e806` 首次進入版控。

## 一個由派工檔本身確立的機械事實

`pairs/` 裡任何一份檔案的結尾作答指令都只要求兩行輸出：

```
VERDICT: <PASS 或 BLOCK 或 UNDETERMINED>
BASIS: <一句話說明依據>
```

也就是說，**finding set 在派工設計上就沒有被收集**——不是事後遺失。這一點對
「correctness 該怎麼算」有直接後果，見報告對應段落。

## 重跑這批材料

`generators/` 下三支腳本裡有硬寫的絕對路徑
（`C:/Users/user/orca/openspec-schemas`）。**刻意不修正**：修改腳本就是修改證據，
會使它們不再是當時實際執行的那一份。要重跑請改在自己的環境覆寫該變數，
不要提交對腳本本文的修改。

`gen_arm0.py` 與 `gen_materialized.py` 都會 exec `gen_pairs.py`，因而重寫派工檔。
當時腳本放在 scratchpad、派工檔就寫在腳本旁的 `pairs/`——這正是上面那 18 份失去
同期性的原因。**腳本搬進本目錄後，派工檔的輸出位置是腳本旁的 `generators/pairs/`**
（以 `__file__` 定位），**不是**本目錄保存的 `evidence/pairs/`；後者不會被重跑覆寫。

⚠️ **會被重跑覆寫的是版控內的其他紀錄檔**（2026-09-29 逐支讀 `open(… 'w')` 查證）：

| 腳本 | 寫入 | 位置如何決定 |
|---|---|---|
| `gen_pairs.py` | `generators/pairs/A1–A3_I*.md` | `__file__` |
| `gen_arm0.py` | `generators/pairs/A0_I*.md`；**`../arm0-prose-prefix.md`** | `__file__`；硬寫絕對路徑 |
| `gen_materialized.py` | **`../materialized-inputs.md`** | 硬寫絕對路徑 |
| `gen_arms.py` | **`../arm2-structured.md`、`../arm3-structured-plus-procedure.md`** | **相對於當前工作目錄**，須在 repo 根執行 |

粗體者都是本實驗已凍結的紀錄；重跑前先備份，跑完用 `git diff` 確認、不要提交覆寫。

**`gen_arm0.py` 有一個本目錄未保存的輸入**：`generators/schema_prefix.yaml`
（缺它會在讀檔時中止）。它就是 `e38e817` 父 commit 的 `superpowers-bridge/schema.yaml`，
重建時要寫到 `generators/` 目錄下、且位元不變。在 repo 根執行（Git Bash 與 PowerShell 皆可；
不用 shell 的 `>` 轉向，因 PowerShell 5.1 會轉成 UTF-16）：

```
python -c "import subprocess; open('docs/superpowers/poc/2026-09-17-q8-structured-definition/evidence/generators/schema_prefix.yaml','wb').write(subprocess.check_output(['git','show','e38e817^:superpowers-bridge/schema.yaml']))"
```

（2026-09-29 以同一指令寫到暫存位置實測：產物以 UTF-8 讀取後第 516 行即腳本斷言的
`CHECKS 8-12` 標題行。重建出的檔案不屬證據集，用完刪除、不要提交。）

## 檔案清單（SHA256 前 16 碼，救回當下狀態）

| 路徑 | bytes | sha256[:16] |
|---|---|---|
| `generators/gen_arm0.py` | 2468 | `fe461f4ac5214daa` |
| `generators/gen_arms.py` | 15113 | `2b72c7c9ca617ade` |
| `generators/gen_materialized.py` | 3144 | `f2bcb8827cba5ab7` |
| `generators/gen_pairs.py` | 4062 | `afb67bbff1568a2c` |
| `pairs/A0_I1.md` | 15538 | `8d73d61d00d9fb96` |
| `pairs/A0_I2.md` | 15577 | `13ecddf4c498c2d2` |
| `pairs/A0_I3.md` | 15449 | `180b2af292a3f69b` |
| `pairs/A0_I4.md` | 15384 | `ef2437ddda0762e7` |
| `pairs/A0_I5.md` | 15416 | `7752257e5f0ac36f` |
| `pairs/A0_I6.md` | 15717 | `b679738f334ed57d` |
| `pairs/A1_I1.md` | 19840 | `9401700719c2edf9` |
| `pairs/A1_I2.md` | 19879 | `97f56f4a0967d56f` |
| `pairs/A1_I3.md` | 19751 | `42b1c759629639a2` |
| `pairs/A1_I4.md` | 19686 | `c2a39fb112f373e0` |
| `pairs/A1_I5.md` | 19718 | `f862aad4098ea2cf` |
| `pairs/A1_I6.md` | 20019 | `7990fbf9729665cf` |
| `pairs/A2_I1.md` | 10229 | `310eaf907f6ef5a3` |
| `pairs/A2_I2.md` | 10268 | `4ef3f2e2849388c5` |
| `pairs/A2_I3.md` | 10140 | `0230cf475706292e` |
| `pairs/A2_I4.md` | 10075 | `67782d5879e83e79` |
| `pairs/A2_I5.md` | 10107 | `7e8e11d5643f5fe5` |
| `pairs/A2_I6.md` | 10408 | `b8cc530c72e25b9b` |
| `pairs/A3_I1.md` | 9980 | `06963e27c3cc4ff6` |
| `pairs/A3_I2.md` | 10019 | `c93b82a699f62cae` |
| `pairs/A3_I3.md` | 9891 | `ea69f486506b6411` |
| `pairs/A3_I4.md` | 9826 | `0a3b6df31e441c72` |
| `pairs/A3_I5.md` | 9858 | `c223fecd9ef76a1d` |
| `pairs/A3_I6.md` | 10159 | `23d841733d5da58b` |
| `results.json` | 2338 | `fbeafff54e3c931d` |

這些 hash 記錄的是**救回當下**的內容，不是 09-17 的內容。對那 18 份不同期的檔案而言，
它無法證明與當時派出去的位元組相同。

## 已被這批材料驗證的宣稱

`../materialized-inputs.md` 宣稱其六組 `tasks.md` / `plan.md` 與實際派工檔逐位元相同。
2026-09-21 以本目錄 `pairs/A1_I*.md` 實測：**六組全部逐位元出現**（0 例外）。
⚠️ 受上節限制：驗的是重新產生的那 18 份，不是 09-17 的原件。
