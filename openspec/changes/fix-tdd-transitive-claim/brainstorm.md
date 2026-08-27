<!--
Raw capture of superpowers:brainstorming output.
2026-08-27 重寫（非打補丁）。前一版 commit f8a1455 已被第三方審查判定不通過
（2 P0 / 7 P1 / 2 P2），審查全文見 repo 根 `2026-08-27-TDD假保證-第三方審查與改寫建議.md`。
重寫理由：P0-1 與 P1-3 動到的是問題的切分方式，不是細節。
-->

# Brainstorm — fix-tdd-transitive-claim

> **本 change 的一句話**：刪掉 schema 與 README 裡「上游會自動幫你執行 TDD」這個
> 錯誤宣稱，並補上一句老實話。**不在本 change 內建立證據機制**——那是另一件工作。

---

## 一、背景：這不是錯字，是一類病

### 1.1 事實

`superpowers-bridge/schema.yaml:507-513` 對執行的 agent 說：

> IMPORTANT — transitive skill activation:
> subagent-driven-development **internally enforces** the following skills,
> **so you do NOT need to invoke them manually**:
> - **superpowers:test-driven-development** — **every task** follows RED-GREEN-REFACTOR.

上游 `subagent-driven-development` 整個資料夾（v6.3.0）裡 TDD 字樣**只有 4 處，全是條件句**
（2026-08-27 實掃）：

| 出處 | 原文 |
|---|---|
| `implementer-prompt.md:36` | `Write tests (following TDD **if task says to**)` |
| `implementer-prompt.md:113` | `Did I follow TDD **if required**?` |
| `implementer-prompt.md:133` | `**TDD Evidence** (**if** TDD was required for this task)` |
| `task-reviewer-prompt.md:75` | `The implementer already ran the tests and reported results with TDD` |

**「有條件的」被我方寫成了「一定會」。**

### 1.2 後果鏈（為什麼這比一般的文件錯誤嚴重）

```
schema 告訴 agent：後面會自動做 TDD，你不用管
        ↓
agent 照做 —— 它沒有錯
        ↓
上游只在「任務單有寫」時才做 TDD
        ↓
我方任務單沒寫（因為以為自動）
        ↓
整條流程跑完，一個測試都沒寫 —— 而且全綠、無人抗議
```

這類錯誤的**症狀就是「一切正常」**：schema validate 通過、CI 全綠、流程每步打勾。
它不會出事，所以「等它出事再修」的機制永遠抓不到它。

### 1.3 它是病，不是單一缺陷

同一形狀在 24 小時內出現三次，載體各不相同：

| 誰 | 犯了什麼 |
|---|---|
| 原作者 | 把上游的 `should use`（建議清單）讀成 `internally enforces`（強制） |
| 2026-08-26 | 修了 Compatibility 表一列，沒往外掃同類（半修） |
| 2026-08-27 | 在一份修假保證的文件裡，寫了三個新的假保證（見 §五） |

三次的共同形狀：**以為寫下來就會發生**。
- 把「建議」寫成「保證」
- 把「政策」寫成「閘門」
- 把「引用」寫成「執行」

### 1.4 本 repo 的特殊性（本次討論定調的主軸）

一般專案裡文件是**描述**程式；文件錯了程式照樣對。
**本 repo 沒有程式** —— `schema.yaml` 不描述行為，**它本身就是行為**：agent 讀它、照著做。

> **在這裡，文件寫錯 ≠ 說明書寫錯，文件寫錯 = 產品壞了。**
> 功能要對齊 ⇒ 文件就是功能 ⇒ 所以文件必須對齊。

推論：**上游「純散文不必有測試」（`writing-good-tests.md:154`：
`trivial code and human prose earn none`）那條例外，在本 repo 幾乎沒有適用對象。**
連 README 都不是純描述——採用者是讀了 README 才決定要不要用。
分界不是「散文 vs 指令」，是**有沒有做出宣稱**。

---

## 二、查證事實（全部 2026-08-27 親自複查）

### 2.1 上游從未強制過 TDD——不是漂移，是基準版即誤讀

- `README.md:485-487` 的相容性表釘的是 `v5.1.0`（**已查證**，前一版誤留為「未查」）。
- 5.1.0 只有 `Subagents follow TDD naturally`（宣傳語）與
  `Subagents should use: test-driven-development`（建議清單）。
- `internally enforces` 在**已查的三版**（5.1.0 / 6.2.0 / 6.3.0）都找不到來源。
  ⚠️ 措辭限定為「已查的三版」，不寫「任何一版」——未查全部版本。

### 2.2 TDD 實際上靠什麼到達實作者

靠 `writing-plans` 把微步驟寫進每張任務（`writing-plans/SKILL.md:98` 起的標準任務格式）：

```
Step 1: Write the failing test
Step 2: Run test to verify it fails
Step 3: Write minimal implementation
Step 4: Run test to verify it passes
Step 5: Commit
```

**TDD 不是執行器的功能，是計畫的內容。** 執行器只是照任務單做事的人。

上游另有第二道：實作者交報告時必須附 **TDD Evidence**——
RED 跑了什麼指令、失敗輸出、為什麼預期失敗；GREEN 跑了什麼指令、通過輸出
（`implementer-prompt.md:133`）。

### 2.3 我方把兩道都拆掉了

| 上游的閘口 | 我方現況（2026-08-27 實查） |
|---|---|
| ① 計畫帶 TDD 微步驟 | `templates/plan.md` 全檔 **17 行**，步驟只有一句 `- [ ] **Step 1:** <!-- micro-step -->`，**無任何 TDD 結構** |
| ② 交件附 RED/GREEN 證據 | `schema.yaml` 全檔 grep `RED` / `GREEN` → **0 筆**（第 201/206 行的 evidence 指的是 commit 數，不是 TDD 證據） |

**兩道都拆掉，然後在文件上寫「它會自動做」。**

### 2.4 上游 TDD skill 自己列了例外，而例外要問人類

`test-driven-development/SKILL.md:24-27` 逐字：

```
**Exceptions (ask your human partner):**
- Throwaway prototypes
- Generated code
- Configuration files
```

⇒ **上游沒有明說「為什麼不預設 TDD」**（已搜三個 skill 資料夾，無此說明），
但理由是結構性的：**既有例外、且例外要人判斷，執行器就不能無條件強制。**

⚠️ 第三種例外正是 configuration files，而 `schema.yaml` 就是 configuration。

### 2.5 上游禁止用 grep 當測試，但它給了替代方案

`writing-good-tests.md:177` 逐字：

```
| Test a script or document | Run it / pressure-test its consumer; never grep its text |
```

**它不是說「文件不能驗」，是說「要驗文件，就去跑它 / 對它的使用者施壓，別搜字面」。**
讀我方 schema 的「使用者」就是 agent。前一版設計把 grep 稱作 TDD，與此正面衝突。

### 2.6 上游自身的契約裂縫（非我方造成）

`task-reviewer-prompt.md:75` **假設**實作者已提供 TDD evidence，
但實作者只在任務要求時提供（`implementer-prompt.md:36`）。
來源：2026-08-26 審查文件 §3.5。

---

## 三、決策鏈

### Q1：文件類改動要什麼證據？→ **用現成的四類分工，不造新詞**

| 改的是什麼 | 要求什麼 | 用誰的 | 授權 |
|---|---|---|---|
| 有可執行行為 | 真 TDD，RED→GREEN | `superpowers:test-driven-development` | MIT ✅ |
| 給 agent 讀的指令文字 | 外部審查者按「指令面」問法審（「這個指令還執行得動嗎？有沒有互相衝突的指令？」） | `sd0x-dev-flow` 的 `doc-review` `executable` profile | MIT ✅ |
| 同一句話散落多處 | 9 維度擴散檢查；維度 7/8/9 **必須外部跑** | `review-fix-propagation` | 待開放（見 Q1a） |
| 純措辭（讀起來順不順） | 不要求 | — | — |

**四類各有各的名字，不冒用彼此。** 特別是：**擴散檢查不是測試，不得宣稱它是。**

理由：使用者定調「**先把現有開源資源整合進系統節點，成為大系統後再看要不要優化**」。
前兩者是公開、MIT、有實際使用紀錄的成品，直接接進來當節點，不自己發明。

### Q1a：`review-fix-propagation` 的可得性 → **開放**

實查（2026-08-27）：
- `superpowers` = `anthropics/claude-plugins-official` / `obra/superpowers-marketplace`，**MIT、公開**
- `sd0x-dev-flow` = `sd0xdev/sd0x-dev-flow`，**MIT、公開**
- `review-fix-propagation` = `github.com/azuma520/workflow-harness`，**匿名存取 404（私有）、無 LICENSE 檔**

使用者拍板：**開放**（本人開發）。
公開範圍建議（沿用本 repo 8/27「原始逐字稿不進版控」先例）：
`SKILL.md` + `references/propagation-checklist.md` + `references/dogfood-history.md` + `evals/evals.json`；
`references/參考意見.md`（550 行外部 AI 顧問逐字稿）留在私有——其內容 SKILL.md 已吸收，
且無連結指向它。已掃描：**四份檔案皆無憑證、金鑰、個資或內部路徑**。

### Q1b：對採用者怎麼收 → **宣告依賴 + PRECHECK + 教安裝**

使用者定調：「不可把『你有某個 skill』**偷偷**變成別人的必要條件」指的是**偷偷**，不是不可依賴。
**系統若包含某個 skill，正確做法是把條件說清楚並協助安裝。**

⇒ 沿用 bridge v1 對 Superpowers 已在做的模式（Layer 1 PRECHECK：缺失就 STOP，不靜默降級），
不新發明機制。

### Q2：要不要定分類表？→ **要，但直接用現成分類器的輸出，不自己編**

前一版的取捨是「甲（定分類表）怕清單外沒歸屬 / 乙（每張任務自陳判準）怕判準寫太鬆」。
**兩個怕的東西在現成實作裡都已被解掉**（2026-08-27 讀實作確認）：

| 現成分類器 | 分不出來時 |
|---|---|
| `resolve-review-profile.js` | 未知分類 → `full-design`（最深，五維度全審） |
| `update-docs` 的 `resolveDocRole()` | 落不進任何規則 → fallback = 現行權威（欠對齊那一類） |

兩者都**猜不到就往嚴的方向倒**，且明文 `never chosen by hand at dispatch time`。

⚠️ **已知邊界（讀實作得出，非讀說明）**：
`resolve-review-profile.js:52` 的 `INSTRUCTION_SURFACE = /^(?:skills|rules|agents|commands)\//`
是**寫死的正則、無設定可加**；且 `doc-review` 的目標集合**篩成 `.md`**。
⇒ `schema.yaml` 屬程式碼類、走 `/codex-review-fast`，**不會進文件審查**。
⇒ `templates/*.md` 會進，但會被判成一般文件。該分類器允許**往深指定**（`deeper()`），
故審模板時明確指定按指令面審即可，不必改任何程式。

### Q3：真閘門現在做嗎？→ **不做。Change 1 只刪不補，但要留一句老實話**

第一性拆解的結論：

1. **想蓋的關卡擋不住實際發生過的那次失敗。** 關卡只能擋「已知是錯的那幾句」，
   而當初的問題是沒有人知道那句話是錯的。
2. **黑名單這招在使用者自己的紀錄裡已失敗過**：全域 CLAUDE.md 複審紀律記載
   「防絕對化黑名單三個精確字串被改寫措辭繞過，且 CLI 分支從未被測」。
   同形狀、同坑，而且失敗時是綠的。
3. **8/26 已查出 D4（controller 手抄證據）證明力不足**：同一 commit 裡測試與實作都在，
   只能證明「現在綠」，不能證明「先紅後綠」；且審查者被明令不要重跑實作者跑過的測試
   （來源：8/26 審查文件 §3.4）。現在補等於補一個已知會被推翻的東西。

⇒ **本 change 只做**：刪掉假保證 + 補一句老實話
（「TDD 是否執行取決於任務單有無要求；本 schema 目前不強制」）
+ 把「沒有檢查報告不算修完」那兩個 ✅ 降級成「⚠️ 政策層，擋不住」，
並寫明「唯一真的擋得住的是會失敗的自動關卡」。

**證據機制（閘口②）留給 Change 2。** 位置已知（交件節點）、格式上游已有，但需重新設計。

### Q4：與 Change 2 合併嗎？→ **拆開**（引用已決，不重議）

出處：
- 2026-08-26 審查文件 §5 結尾逐字：「**Roadmap 的 Change 1（修正錯誤宣稱）不受影響，可照原計畫進行。**」
- 同文件 Codex 建議 #2：「把 traceability 與 TDD 修復拆成不同 change——
  兩者不應共用『必要性』論證。」

⚠️ 8/27 上午曾決定合併；**該決定作廢**，回到 8/26 的拆分。

### Q5：第二視角用誰？→ **`agy`**（引用已決，不重議）

出處：專案 memory `reference_third-brain-agy-pointer`（2026-08-27 使用者拍板 + 本機實測）。

```bash
"C:/Users/user/AppData/Local/agy/bin/agy.exe" -p "$(cat brief.md)" \
  --model gemini-3.7-flash-high --output-format text --print-timeout 10m
```

⚠️ `--effort` 不換模型、指定錯不報錯（症狀是「一切正常」）。
⚠️ 這是**本機開發前提，不進 bridge 對外契約**——採用者不必有 Codex 或 agy。

---

## 四、變更面清單（Affected Surface）— **算一次，凍結**

依 `.claude/rules/scope-discipline.md` 三條件計算。
**本清單凍結；後續任何路徑不得重算**（重算會把修改過程中變髒的檔一併吸收）。

掃描方式（2026-08-27）：`git ls-files` 排除 `.claude/`、`openspec/schemas/`、`docs/superpowers/`，
以 `TDD|test-driven|RED.GREEN|do NOT need to invoke|transitiv` 掃描。

### 4.1 必改（依賴錯誤前提）

| 檔 | 行 | 類型 |
|---|---|---|
| `superpowers-bridge/schema.yaml` | 10-11, 20, 474, 507-518, 522-525 | 假保證本體 + fallback 理由 |
| `superpowers-bridge/README.md` | 213, 247, 282, 304, 328, 368, 381, 383, 445 | 假保證本體 |
| `superpowers-bridge/README.md` | 310, 449, 553 | fallback 理由（依賴同一前提） |
| `superpowers-bridge/README.zh-TW.md` | 213, 247, 282, 304, 305, 328, 368, **381**, 383, **443**, 445 | 假保證本體 |
| `superpowers-bridge/README.zh-TW.md` | 310, 449, 553 | fallback 理由 |
| `superpowers-bridge/templates/retrospective.md` | **55-78 整段** | **誘導型**（見 4.4） |
| `CLAUDE.md` | 207 | 紅旗清單引用同一前提 |

**合計 33 段**：schema 5 + README 英 12 + README 繁 14 + retrospective 1 + CLAUDE 1。
若把中英 README 視為同一邏輯位置則為 **19 個位置**。
前一版寫「10 處」——**任何算法都得不到 10**。

> ⚠️ 上表的行號是 2026-08-27 掃描當下的值。開始修改後行號會位移，
> **以「哪一段講什麼」為準，不以行號為準**；行號只用來重新定位。

### 4.2a 本清單的第一版漏了三處——方法本身的證據

第一次掃描用關鍵字 `TDD|test-driven|RED.GREEN|transitiv`，得到 30 段。
接著用**結構完全不同的第二條路徑**（改搜「宣稱自動發生」的句型：
`automatic|no need|不用|自動|enforce|強制|每一?[張個]|every task`）交叉驗證，多抓到：

| 漏掉的 | 為什麼第一次沒抓到 |
|---|---|
| `README.zh-TW.md:381`「每個 subagent **自動傳遞**」 | 它是英文 `transitively activates` 的中譯。**關鍵字掃描抓不到翻譯。** |
| `README.zh-TW.md:305, 443`「**傳遞**」 | 同上 |
| `retrospective.md` 誘導範圍實為 **55-78**，非 59-60 | 誘導語句（「Default expectation: 全部 ✓」「每個 ✗ 必須回答三題」「不可寫『不需要』」）**不含任何 TDD 關鍵字** |

**這正是審查 P1-3 的論點的實證**：可窮舉性取決於**判準的形狀**，不是內容的載體。
「這句話有沒有出現」可判定；「這句話是不是在宣稱某事自動發生」不可用精確搜尋窮舉——
跨語言翻譯與同義改寫都會逃逸。

⇒ **本清單的凍結對象是「開始修改後不得重跑探索」，不是「不得修正錯誤」。**
上面三處是在**動筆修改之前**、由第二條路徑交叉驗證補上的，並非事後吸收變髒的檔案。
仍應假設本清單不完整：**修改時每一段都要重新確認，不可把清單當窮舉證明。**

### 4.2 不改（已誠實標定 / 中性）

| 檔 | 行 | 理由 |
|---|---|---|
| `superpowers-bridge/README.md` / `.zh-TW.md` | 500, 501, 506 | 已標 ❌ False / ⚠️ 不是每張 task / Open drift |
| `superpowers-bridge/README.md` / `.zh-TW.md` | 498 | 「`executing-plans` 不提 TDD 也不提 code-review」是**已查證為真的事實**；垮掉的是由它推出的對比（見 4.3），不是它本身 |
| `superpowers-bridge/README.md` / `.zh-TW.md` | 123, 126, 211, 497, 518 | 描述格式或 skill 清單，不含錯誤前提 |
| `README.md` / `README.zh-TW.md`（頂層） | 11 | 只列 skill 名稱 |
| `docs/roadmap.md` / `.zh-TW.md` | 17 | backlog 條目，非宣稱 |
| `文檔/handoff/**`、repo 根討論素材、`openspec/changes/**/archive` | — | **記錄類，append-only 不改寫**（`update-docs` 四分類：記錄與今天的程式不一致，那個不一致本身就是記錄） |

### 4.3 fallback 理由為什麼也要改（前一版漏列）

現行 README/schema 的論證是：「`executing-plans` **不會** transitive 帶起 TDD 與 code-review，
所以本 schema 不支援它。」

**這個對比垮了**——`subagent-driven-development` 本來也不會無條件帶起 TDD。兩者都不帶。
結論（不支援 `executing-plans`）可能仍然成立，但**理由要重寫**，不能再用這個對比。

### 4.4 `retrospective.md` 是誘導型，不是描述型

`templates/retrospective.md:59-60` 會要求**預設全部打 ✓、打 ✗ 必須解釋**。
它不叫人停手，但**它叫人打勾**——同樣是驅動行為的句子。
⇒ 前一版的兩類切分（解除型／描述型）漏了這一種，是判準漏，不是分類錯。

---

## 五、本次修正的四個假保證（含前一版自己新造的三個）

| # | 原本寫法 | 問題 | 改成 |
|---|---|---|---|
| 1 | 「上游 internally enforces TDD」 | 把建議寫成保證 | 據實：條件性，取決於任務單 |
| 2 | 「沒有 Propagation Check Report 不算修完」標 ✅ 擋得住 | 把政策寫成閘門（無 CI job、無失敗條件；且「有報告」≠「真的跑過」） | ⚠️ 政策層，擋不住 |
| 3 | 「綁出處就能偵測漂移」 | 出處只提供可追溯性，不會自行偵測 | 「使人工重驗可重現」 |
| 4 | 「`strict-reviewer` 結構上抓不到」 | 把機率寫成保證（方向相反的同一種病） | 「預設題目下高機率漏掉」；刪掉無出處的那句 |

---

## 六、明確不做

- ❌ **不做自動殘留檢查腳本 / CI 黑名單**（理由見 Q3）
- ❌ **不建立證據機制**（Change 2 的範圍）
- ❌ **不改 schema major**（本 change 不動 artifact 圖與 `requires:` 邊）
- ❌ **不改寫記錄類文件**（handoff、討論素材、archive）
- ❌ **不把 Codex / agy 寫進對外契約**

---

## 七、未決 / 待確認

- [ ] `review-fix-propagation` 的實際開放動作（抽出、加 MIT LICENSE、公開）——使用者已拍板要做，尚未執行
- [ ] 不支援 `executing-plans` 的**新理由**要怎麼寫（4.3）——需重新查 `executing-plans` 的實際內容再定
- [ ] 本 change 是否順帶修 `templates/plan.md` 的 17 行空殼——它與「plan 放寬」那條工作重疊，可能該歸那邊

---

## 八、審查安排

- 主審：Codex（`/codex-review-doc`，指定按指令面 profile）
- 交叉驗證：`agy --model gemini-3.7-flash-high`
- 兩者皆為**本機開發前提**，不進對外契約
