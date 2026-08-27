<!--
Raw capture of superpowers:brainstorming output.
2026-08-27 重寫（非打補丁）。前一版 commit f8a1455 已被第三方審查判定不通過
（2 P0 / **9** P1 / 2 P2），審查全文見 repo 根 `2026-08-27-TDD假保證-第三方審查與改寫建議.md`。
⚠️ 該審查文件**自己的表頭寫「7 個 P1」，但它實列 P1-1 ~ P1-9**（`grep -c "^### P1-"` = 9）。
本檔前一稿照抄了它的表頭數字——**抄別人的數字等於自己的宣稱**，該自己數一遍。
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

上游 `subagent-driven-development` 整個資料夾（v6.3.0）裡 TDD 字樣**只有 4 處**（2026-08-27 實掃）：
**3 條是條件句，第 4 條是無條件的「假設別人已經給了」**——後者不是保證，是上游自己的契約裂縫（見 §2.6）。

| 出處 | 原文 |
|---|---|
| `implementer-prompt.md:36` | `Write tests (following TDD **if task says to**)` |
| `implementer-prompt.md:113` | `Did I follow TDD **if required**?` |
| `implementer-prompt.md:133` | `**TDD Evidence** (**if** TDD was required for this task)` |
| `task-reviewer-prompt.md:75` | `The implementer already ran the tests and reported results with TDD` |

**「有條件的」被我方寫成了「一定會」。**

### 1.2 危害鏈（**條件性的**，不是必然發生）

⚠️ **本節在 2026-08-27 第二輪審查後改寫。** 前一版把下面這條路徑寫成標準結局，
並附上「整條流程跑完一個測試都沒寫」的斷言——**那是把條件性風險寫成確定後果，
且無任何實際 cycle 的證據**。這正是本 change 在修的病的鏡像方向（見 §五 #5）。

正常路徑上 TDD **通常會到達實作者**，理由見 §2.3：本 schema 的 plan artifact
確實 invoke `superpowers:writing-plans`，而**它的標準任務格式含 TDD 微步驟**。

⚠️ **但這是慣例，不是保證**（2026-08-27 第三輪審查後收窄）：`writing-plans` 是照模板行事的
skill，「plan artifact invoke 了它」推不出「每張任務都會帶 TDD 步驟」——那正是本文件
自己命名的「**把引用寫成執行**」。而且上游明說純文件類工作不該有測試
（`writing-good-tests.md:154`：`trivial code and human prose earn none`），
所以對本 repo 大量的 prose 任務，「不會消失」本來就不成立。

假宣稱真正的危害是**拆掉備援、並誤述 TDD 的來源**：

```
schema 告訴 agent：後面會自動做 TDD，你不用管
        ↓
agent 不再自行確認任務單有沒有要求 TDD —— 它照我方的話做，沒有錯
        ↓
只要有任何一條路徑讓任務單不帶 TDD 要求
（plan 走手寫備援、writing-plans 對某類任務不產生測試步驟、
  或未來「plan 放寬」把微步驟拿掉）
        ↓
沒有任何一層「**負責**」發現 —— 因為文件說那是自動的
```

也就是說：假宣稱本身不製造失敗，**它移除了「有人該去發現」這件事**。
而 8/26 的討論素材 §1.3 已指出下一步就會踩到：
「**放寬 plan 而沒有替代管道，會靜默地把 TDD 一起拿掉**」——
到那時，這句假宣稱就是唯一還在說「別擔心，它是自動的」的東西。

這類錯誤的**症狀是「一切正常」**：schema validate 通過、CI 全綠、流程每步打勾。
它不會自己出事，所以「等它出事再修」的機制永遠抓不到它。

### 1.3 它是病，不是單一缺陷

同一形狀在 24 小時內出現**四次**，載體各不相同：

| 誰 | 犯了什麼 |
|---|---|
| 原作者 | 把上游的 `should use`（建議清單）讀成 `internally enforces`（強制） |
| 2026-08-26 | 修了 Compatibility 表一列，沒往外掃同類（半修） |
| 2026-08-27 `f8a1455` 版 | 在一份修假保證的文件裡，寫了**三個**新的假保證（§五 #2-#4） |
| 2026-08-27 重寫版 | 修掉那三個的同時，又寫了**五個**新的（§五 #5-#9），其中一個直接落在要寫進 `schema.yaml` 的交付句上 |

四次的共同形狀：**以為寫下來就會發生**。
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

### 2.3 我方的兩道閘口現況——**一道在、一道只有備援路徑上會斷**

⚠️ 本節在 2026-08-27 第二輪審查後改寫。前一版寫「兩道都拆掉了」，**是錯的**。

| 上游的閘口 | 我方現況（2026-08-27 逐行實查） |
|---|---|
| ① 計畫帶 TDD 微步驟 | **正常路徑上在。** `schema.yaml:178` 明確 `Use the Skill tool to invoke **superpowers:writing-plans**`，第 186 行寫 `Break each task into 2-5 minute micro-steps (TDD style)`。<br>**但備援路徑上斷**：同段 PRECHECK 允許「skill 缺席時使用者自行照模板手寫」，而 `templates/plan.md` 全檔 **17 行**、步驟只有兩行空殼（`- [ ] **Step 1:**` / `- [ ] **Step 2:**`，各帶一個 `<!-- micro-step -->` 註解），**無任何 TDD 結構**。 |
| ② 交件附 RED/GREEN 證據 | **我方沒有要求。** `schema.yaml` 全檔 `RED`/`GREEN` 只有 **1 筆**——第 512 行的 `follows RED-GREEN-REFACTOR`，正是要刪的假宣稱本體。第 201/206 行的 evidence 指的是 commit 數，不是 TDD 證據。<br>上游的 `implementer-prompt.md:133` 仍會在「任務有要求 TDD」時索取該證據，所以這一道**存在於上游、但我方沒有接住它**。 |

⚠️ **前一版此處寫「全檔 grep RED/GREEN → 0 筆」是錯的**，而錯法值得記：
當時那條指令結尾接了 `| head`，**輸出被截斷在第 10 行**，而第 512 行落在截斷點之後。
**把輸出切掉，然後對切掉的部分下結論。** 同一天的紀律接力第 2 條逐字記過同型事故。

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
⚠️ **射程限定（2026-08-27 第二輪審查後收窄）**：下面這兩個分類器管的是
**「一份 `.md` 該用多深的 profile 審、它是權威還是記錄」**。它們**不回答**
「這個改動屬於 Q1 四類的哪一類」，尤其不回答「**這個改動有沒有可執行行為、
因此要不要真 TDD**」。前一版把它們寫成「兩個怕的東西都已被解掉」是**講過頭**。

⇒ **8/27 審查 P1-6 的核心問題仍未解**：邊界由誰、在何時、按什麼判斷？
它是 **Change 2 的題目**，不得因本文件的措辭而被當成已決引用。

在**文件審查深度**這個較窄的問題上，兩個怕的東西確實已被解掉
（2026-08-27 讀實作確認）：

| 現成分類器 | 分不出來時 |
|---|---|
| `resolve-review-profile.js` | 未知分類 → `full-design`（最深，五維度全審） |
| `update-docs` 的 `resolveDocRole()` | 落不進任何規則 → fallback = 現行權威（欠對齊那一類） |

兩者都**猜不到就往嚴的方向倒**，且明文 `never chosen by hand at dispatch time`。

⚠️ **已知邊界（讀實作得出，非讀說明）**：
`resolve-review-profile.js:52` 的 `INSTRUCTION_SURFACE = /^(?:skills|rules|agents|commands)\//`
是**寫死的正則、無設定可加**；且 `doc-review` 的目標集合**篩成 `.md`**。
⇒ `schema.yaml` 屬程式碼類、走 `/codex-review-fast`，**不會進文件審查**。
⇒ `templates/*.md` 會進，但會被判成一般文件。該分類器允許**往深指定**（`deeper()`
只准加深、不准變淺），故審模板時明確指定按指令面（`executable`）審即可，不必改任何程式。

⚠️ 但注意 `deeper()` 是**單向**的：若某檔已被判成比 `executable`（rank 2）更深的
`full-design`（rank 3），指定 `executable` **不會生效**，仍以較深者為準。
結果無害（審得更深），但不要把「我指定了 X」寫成「它就會按 X 審」。

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

⇒ **本 change 只做**：刪掉假保證 + 補一句老實話。

**老實話的草案措辭**（⚠️ 這句會寫進 `schema.yaml`，本身就是對外宣稱，
所以它自己也必須通過「不得把慣例寫成保證」這一關）：

> TDD 是否執行，取決於該張任務單有沒有要求。
> `writing-plans` 的標準任務格式**含** TDD 微步驟，但是否逐張帶上取決於它對任務類型的判斷
> （上游明訂純散文類工作不需要測試）。
> **本 schema 本身不強制、也不驗證**；若任務單沒帶 TDD 要求，本 schema 沒有任何一層**保證**會補上。

⚠️ 前一稿此處寫「手寫備援路徑上**沒有任何一層會**補上它」——**是絕對否定、不成立**：
上游 TDD skill 自己的觸發描述是 `Use when implementing any feature or bugfix`，
subagent 有可能自行觸發它；retrospective 的合規表也是一道弱的事後偵測。
成立的說法是「**沒有任何保證會補上的層**」——把「大概不會」寫成「一定不會」，
是 §五 #5 定義的同型鏡像，這是本文件第三次犯它。

> 前一版此處另列了「把兩個 ✅ 降級」一項——那是 `f8a1455` 版自己新造的假保證，
> 該版已被整份取代，該項已完成，不再是本 change 的待辦。留在此處會誤導。
> 全部假保證的降級結果見 §五。

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

### Q6：全域複審紀律要不要改？→ **不改全域檔，本 repo 照現況執行**

8/27 審查 P1-9 第 2 點要求「同步更新全域 `CLAUDE.md` 複審紀律，或標本 repo 例外」。

**決議**：不動全域檔。兩個理由，第二個才是本輪真正生效的那個：

1. 那條規矩講的是「**Codex 不可用時找誰替補**」，與「**第二視角找誰**」（Q5，已定 `agy`）
   是兩件事，兩者並不牴觸。全域檔屬使用者所有。
2. ⚠️ **本輪實際上並沒有照那條規矩的順序走**——它寫的是
   「Codex 不可用 → 先用其他既有審查方式（strict-reviewer / 確定性驗證），
   確有必要才升 Fable」，而本輪是**使用者當場直接指定 Fable**，跳過了 strict-reviewer。
   **依據是「使用者指定優先」，不是「規矩允許」。** 這一點必須寫明，
   否則下次會有人把本輪當成「規矩就是這樣走」的先例。

**本 repo 的實際 fallback 鏈**（2026-08-27 當日全部觸發過，非紙上規劃）：

```
Codex（主審）→ 額度用盡
  → agy（第二視角）→ headless 讀檔權限被拒、且 exit code 為 0（跑失敗卻回報成功）
    → Fable 代審（使用者當場指定）→ 產出完整報告，本輪的實際審查者
    → 併行：確定性驗證（換一條結構不同的搜尋路徑自查）
```

⚠️ 記一筆：agy 在 headless 下**失敗卻回傳 exit code 0**。
不讀輸出就會把「沒產出」當成「審過了」——又一次「症狀是一切正常」。

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
| `superpowers-bridge/README.md` | 213, 247, 282, 304, **305**, 328, 368, 381, 383, **443**, 445 | 假保證本體 |
| `superpowers-bridge/README.md` | 310, 449, 553 | fallback 理由（依賴同一前提） |
| `superpowers-bridge/README.zh-TW.md` | 213, 247, 282, 304, **305**, 328, 368, **381**, 383, **443**, 445 | 假保證本體 |
| `superpowers-bridge/README.zh-TW.md` | 310, 449, 553 | fallback 理由 |
| `superpowers-bridge/templates/retrospective.md` | **55-78 整段** | **誘導型**（見 4.4） |
| `CLAUDE.md` | 207 | 紅旗清單引用同一前提 |

**合計 35 段**：schema 5 + README 英 14 + README 繁 14 + retrospective 1 + CLAUDE 1。
中英 README 逐項對稱（各 14），去重後的**邏輯位置為 21 個**：5 + 14 + 1 + 1。

**第三條驗證路徑（中英對稱比對，2026-08-27）**——前兩條是「搜關鍵字」與「搜句型」，
這一條改為**逐檔窮舉 + 中英逐行對照**，因為前兩次的漏都出在「同一件事的另一種寫法」：

| 檢查 | 結果 |
|---|---|
| 英文 README 全部命中（`tdd\|test-driven\|red.green\|transitiv\|do NOT need to invoke`，**不分大小寫、不截斷**） | 23 行 = 必改 14 + 不改 9，**無剩餘** |
| 繁中 README（同上 + 中文譯法 `傳遞\|自動`） | 同樣 23 行，另 6 行（110/136/183/373/512/520）是與本題無關的「自動」用法（目錄覆蓋、升級 ack 等） |
| 中英逐行對稱 | 14 個行號**完全一致**，逐行取出內容核對，一一對應 |

⇒ 三條路徑收斂於 35 / 21。但**仍不得當作窮舉證明**——理由見下。

> ⚠️ 這個數字在 2026-08-27 被改過兩次，兩次都是**算術本身**出錯，值得留著當紀錄：
> `f8a1455` 版寫「10 處」（任何算法都得不到 10）→ 本版初稿寫「合計 34」（實際加起來 30）
> → 補上交叉驗證的 3 段後寫「33 段 / 19 個位置」（33 內部一致，但 **19 算不出來**：
> 當時中文 14 行比英文 12 行多 2，去重不可能得到 19，19 只能由 33−14 得出，
> 即假設「中文全是英文的重複」——而該假設與自己列的行數矛盾）
> → 補上英文漏掉的 305、443 後，中英對稱各 14，才得到 **35 段 / 21 個位置**。
>
> **一份專門修「沒人會去驗的數字」的文件，自己的數字錯了三次。** 前兩次是自查抓到的，
> 第三次是外部審查抓到的——正是擴散檢查維度 7/8/9 那條「必須外部跑、當事人不知道自己在猜」。

> ⚠️ 上表的行號是 2026-08-27 掃描當下的值。開始修改後行號會位移，
> **以「哪一段講什麼」為準，不以行號為準**；行號只用來重新定位。

### 4.1a 本清單前兩版共漏了**五段 + 一處範圍低估**——方法本身的證據

第一次掃描用關鍵字 `TDD|test-driven|RED.GREEN|do NOT need to invoke|transitiv`
（**區分大小寫**），得到 30 段。
接著用**結構完全不同的第二條路徑**（改搜「宣稱自動發生」的句型：
`automatic|no need|不用|自動|enforce|強制|每一?[張個]|every task`）交叉驗證，
又由第二輪外部審查補上英文兩行。

**五段漏列**（計入 30 → 35 的差額）：

| 漏掉的 | 為什麼沒抓到 |
|---|---|
| `README.zh-TW.md:381`「每個 subagent **自動傳遞**」 | 它是英文 `transitively activates` 的中譯。**關鍵字掃描抓不到翻譯。** |
| `README.zh-TW.md:305, 443`「**傳遞**」 | 同上 |
| `README.md:305, 443`（英文） | 原文寫的是大寫 `Transitive`，而掃描 pattern 是**區分大小寫**的 `transitiv`。<br>⚠️ 這一項**不是**跨語言問題——它就在英文原檔裡、就含那個字，**第一次掃描本該命中**。<br>是第二輪外部審查（Fable，2026-08-27）抓到的，我兩輪自查都沒抓到。 |

**另有一處範圍低估**（**不計入段數**，因為它本來就在清單裡、只是圈小了）：
`retrospective.md` 的誘導範圍實為 **55-78**（且實際延伸到 :84，見 §4.4），非 59-60。
漏的原因不同：那些誘導語句（「Default expectation: 全部 ✓」「每個 ✗ 必須回答三題」
「不可寫『不需要』」）**一個 TDD 關鍵字都沒有**。

**這正是審查 P1-3 的論點的實證**：可窮舉性取決於**判準的形狀**，不是內容的載體。
「這句話有沒有出現」可判定；「這句話是不是在宣稱某事自動發生」不可用精確搜尋窮舉——
跨語言翻譯、大小寫、同義改寫都會逃逸。

⇒ **本清單的凍結對象是「開始修改後不得重跑探索」，不是「不得修正錯誤」。**
上述**五段全部是在動筆修改之前**補上的（繁中三段由第二條路徑、英文兩段由外部審查），
並非事後吸收變髒的檔案。
仍應假設本清單不完整：**修改時每一段都要重新確認，不可把清單當窮舉證明。**

### 4.2 不改（已誠實標定 / 中性）

| 檔 | 行 | 理由 |
|---|---|---|
| `superpowers-bridge/README.md` / `.zh-TW.md` | 500, 501, 506 | 已標 ❌ False / ⚠️ 不是每張 task / Open drift |
| `superpowers-bridge/README.md` / `.zh-TW.md` | 498 | 「`executing-plans` 不提 TDD 也不提 code-review」是**已查證為真的事實**；垮掉的是由它推出的對比（見 4.3），不是它本身 |
| `superpowers-bridge/README.md` / `.zh-TW.md` | 123, 126, 211, 497, 518 | 描述格式或 skill 清單，不含錯誤前提 |
| `docs/roadmap.md` / `.zh-TW.md` | 17 | backlog 條目，非宣稱 |
| `.github/workflows/version-check.yml` | 132 | issue 範本裡的 `transitive deps`，指的是「上游改了傳遞依賴要人去讀 release notes」，中性且正確 |
| `workflow-harness/work-map.jsonl` | 4 筆 `TDD` | **記錄類**（工作登記），不改寫 |
| `文檔/handoff/**`、repo 根討論素材、`openspec/changes/**/archive` | — | **記錄類，append-only 不改寫**（`update-docs` 四分類：記錄與今天的程式不一致，那個不一致本身就是記錄） |

### 4.2a 兩處需要判斷、不是單純中性的

| 檔 | 行 | 為什麼要單獨列 |
|---|---|---|
| `README.md` / `README.zh-TW.md`（頂層） | 11 | ⚠️ **前一版把理由寫成「只列 skill 名稱」，那是事實錯誤**：原文寫的是 `TDD-via-subagents`，而**這不是任何一個 skill 的名字**，它是「TDD 靠 subagent 自動發生」這個錯誤前提的壓縮寫法。最終或許措辭微調即可，但它**不是中性描述**，不能用錯誤理由歸進不改。→ **列入待判斷**（§七） |
| `superpowers-bridge/schema.yaml` | 186 | `Break each task into 2-5 minute micro-steps (TDD style)` 是**對 `writing-plans` 行為的真實描述**（已對上游原文查證，見 §2.2），大概不必改。但它是本 change 主題範圍內的真宣稱，明列以免日後被誤讀成漏掃 |

### 4.3 fallback 理由為什麼也要改（前一版漏列）

現行 README/schema 的論證是：「`executing-plans` **不會** transitive 帶起 TDD 與 code-review，
所以本 schema 不支援它。」

**這個對比在 TDD 那半垮了**——`subagent-driven-development` 也不會**無條件**帶起 TDD
（它靠 `writing-plans` 把微步驟寫進任務，見 §2.2）。所以「我們有、它沒有」在 TDD 上不成立。

⚠️ **但 code-review 那半只是弱化，沒有垮**（2026-08-27 第二輪審查收窄）：
SDD 對 code-review 仍有**結構性**的派發——每張任務一個 reviewer、最後一次整體 review
寫在它的 SKILL.md 結構裡。README:501 自己已標成
「⚠️ 成立，但不是每張 task 一個」。

⇒ 結論（不支援 `executing-plans`）可能仍然成立，但**理由要重寫**：
不能再用「它不帶 TDD 而我們帶」這個已經不成立的對比，
code-review 那半則要照 501 行既有的誠實標定收窄措辭，不是整段刪掉。

### 4.4 `retrospective.md` 是誘導型，不是描述型

誘導不是出在那兩列表格本身（`:59-60` 只是 `(transitive)` 標記的兩列），
而是出在**包住它的整段**（逐行實查，2026-08-27）：

| 行 | 誘導在哪 |
|---|---|
| `:63-65` | `**Default expectation**: 全部 ✓。每個 skill 都是 schema 設計的一部分，跳過屬於異常情境` |
| `:69-70` | 「跳過 skill 是設計的 escape hatch，不是常規路徑……整節空白（全綠）是預期狀態」 |
| `:74` | 打 ✗ 時「**不可寫『不需要』/『太小』/『沒時間』**」——把最誠實的理由列為禁止 |

它不叫人停手，但**它叫人打勾**——同樣是驅動行為的句子。
⇒ 前一版的兩類切分（解除型／描述型）漏了這一種，是判準漏，不是分類錯。

⚠️ **本節在 2026-08-27 第三輪審查前，仍寫著「`:59-60` 會要求預設全部打 ✓」**——
4.1 與 4.1a 已改成 55-78，這裡沒跟上。**這正是「一個缺陷＝一類缺陷」沒掃乾淨的實例，
而且就發生在本文件內部。**

⚠️ 範圍端點也要注意：誘導 block 實際延伸到 `:80`（one-off 選項）與 `:82-84`（§6 關聯註），
「55-78」是切在清單中間的。修改時以**整段語意**為準，不以這個行號區間為準。

---

## 五、本次修正的九個假保證（其中八個是我方自己寫的）

| # | 原本寫法 | 問題 | 改成 |
|---|---|---|---|
| 1 | 「上游 internally enforces TDD」 | 把建議寫成保證 | 據實：條件性，取決於任務單 |
| 2 | 「沒有 Propagation Check Report 不算修完」標 ✅ 擋得住 | 把政策寫成閘門（無 CI job、無失敗條件；且「有報告」≠「真的跑過」） | ⚠️ 政策層，擋不住 |
| 3 | 「綁出處就能偵測漂移」 | 出處只提供可追溯性，不會自行偵測 | 「使人工重驗可重現」 |
| 4 | 「`strict-reviewer` 結構上抓不到」 | 把機率寫成保證（**方向相反**的同一種病） | 「預設題目下高機率漏掉」；刪掉無出處的那句 |
| **5** | **「我方把兩道閘口都拆掉了」**（本文件初稿，§2.3） | **把「有條件存在」寫成「確定不在」——同樣是方向相反的鏡像。** 而且我讀過 `schema.yaml:178` 那句 invoke `writing-plans`，仍寫下相反結論 | §2.3 改為逐道分述：①正常路徑在、備援路徑斷；②上游有、我方沒接住 |
| **6** | **「兩個現成分類器把兩個怕的東西都解掉了」**（本文件初稿，Q2） | **把射程講過頭**：它們管的是「.md 該審多深」，不管「這個改動要不要 TDD」。若被 Change 2 當已決引用，會讓 P1-6 那題被誤認為已解 | Q2 加射程限定，明寫「P1-6 仍未解，是 Change 2 的題目」 |
| **7** | **「正常路徑上 TDD 不會消失」**（第二稿 §1.2） | **把慣例寫成保證**——`writing-plans` 是照模板行事的 skill，「invoke 了它」推不出「每張任務都帶 TDD」。而且上游明訂純散文不需測試，本 repo 大量任務正屬此類。**同一節三行後又列出它消失的方式**，自相矛盾 | 改條件式：「標準任務格式**含** TDD 微步驟，是否逐張帶上取決於任務類型」 |
| **8** | **「手寫備援路徑上沒有任何一層會補上它」**（第二稿 Q3，**且該句要寫進 `schema.yaml`**） | 絕對否定的鏡像。上游 TDD skill 觸發描述為 `any feature or bugfix`，可能自行觸發；retrospective 合規表也是弱偵測層 | 改「沒有任何**保證會**補上的層」 |
| **9** | **「4 處全是條件句」**（初稿起 §1.1） | 第 4 處（`task-reviewer-prompt.md:75`）是**無條件假設**，而 §2.6 自己就是這樣定性它的——同一文件前後打架 | 改「3 條條件句 + 1 條無條件假設」 |

> #5、#6 由第二輪外部審查抓到；**#7、#8、#9 由第三輪抓到——而 #7 #8 是修 #5 時新造的**。
> 每一輪自查都說「這次乾淨了」，每一輪外部審查都還能抓到同型的新實例。
> 這正是擴散檢查維度 7/8/9 的結構理由：**當事人不知道自己在猜。**
>
> ⚠️ 特別記 #8：那句話**是要寫進 `schema.yaml` 的交付句**。
> 也就是說——**在一份修假保證的文件裡，我把一個新的假保證寫進了要交付的產物本身。**

---

## 六、明確不做

- ❌ **不做自動殘留檢查腳本 / CI 黑名單**（理由見 Q3）
- ❌ **不建立證據機制**（Change 2 的範圍）
- ❌ **不改 schema major**（本 change 不動 artifact 圖與 `requires:` 邊）
- ❌ **不改寫記錄類文件**（handoff、討論素材、archive）
- ❌ **不把 Codex / agy 寫進對外契約**

---

## 七、未決 / 待確認

> ⚠️ **本節只列會影響本 change 完成判準的事。**
> 與「刪掉假宣稱」無依賴的工作**不放這裡**——否則本 change 的完成會被無關工作纏住。

- [ ] 不支援 `executing-plans` 的**新理由**要怎麼寫（4.3）——需重新查 `executing-plans` 的實際內容再定
- [ ] 頂層 `README.md` / `README.zh-TW.md` 第 11 行的 `TDD-via-subagents` 怎麼改（4.2a）——它不是 skill 名稱，是錯誤前提的壓縮寫法
- [ ] 本 change 是否順帶修 `templates/plan.md` 的 17 行空殼——它是閘口①的備援斷點（§2.3），但與「plan 放寬」那條工作重疊，可能該歸那邊

### 七之二、已拍板但不屬本 change 的動作（獨立追蹤，不阻擋本 change 收尾）

- [ ] **開放 `review-fix-propagation`**（抽出、加 MIT LICENSE、公開）——使用者 2026-08-27 已拍板要做。
      與「刪掉假宣稱」**無依賴**：本 change 不需要它公開就能完成；
      它是 Q1 那張四類分工表對**採用者**生效的前提，屬 Change 2 / bridge 對外契約的射程。

---

## 八、審查安排

- 主審：Codex（`/codex-review-doc`）
- 第二視角：`agy --model gemini-3.7-flash-high`
- 本輪實際執行者：**Fable 代審**（Codex 額度用盡、agy 權限受阻，使用者指定）
- 三者皆為**本機開發前提**，不進對外契約

⚠️ **不要寫「指定按指令面 profile 審」**：本檔在分類器眼中是未知分類 → `full-design`（rank 3），
而 `executable` 是 rank 2，`deeper()` 只准加深，指定不會生效（結果無害，但描述會與實際不符）。
