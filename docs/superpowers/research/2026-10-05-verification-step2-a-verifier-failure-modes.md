# Verification Strategy 第二步 A：驗證工具會怎麼失效（2026-10-05）

> **定位**：分析參考，不是規範、不是研究結論。work-map `task-20261005-vs-step2-a-verifier-reliability` 的產出。分類是 **working taxonomy**：只用來決定下一題，不代表已證明存在普遍的 failure mode。
>
> **研究問題**（work-map 原文）：我們用來判斷 PASS/FAIL 的 oracle、grader、probe、test harness 本身會以哪些方式失效？需要什麼最低限度的 self-check／negative control，才值得信任它產生的 Verification Result？
>
> **範圍與停止條件**（2026-10-05 使用者裁定）：只用兩組內部證據，先做 failure-mode inventory；不做 C、不改盤點表 taxonomy；（本次 A 的 timebox，非通則）兩組證據整理完成後，若跨組重複出現的 verifier failure mode **少於 3 類**，停止擴張 A、回報「目前跨案例支持不足」，不為湊類別擴大分類、不自動進入外部研究。結尾只回答「A 的結果是否足以讓 C 升成下一題」。
>
> **三種內容分開寫**：來源事實（附出處）；本文的分類判斷（§2，換一個人可能分得不同）；推論一律標【推論】。【未查證】＝沒查到。

---

## §0 證據來源

| 組 | 範圍 | 讀了什麼 |
|---|---|---|
| 第一組（Identity＋RS） | 盤點表 `./2026-10-02-verification-evidence-inventory.md` §3 O2 列的 5 筆：F-ID6、F-ID11、F-ID13、F-ID15、F-RS7 | 盤點表 finding 表；回原始紀錄核對：`docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/sdd-ledger.md` 第 8、43、71–87、111–123 行；Identity archive 的 `retrospective.md` §1、§2、§5、§6 與 `verify.md` 第 9、184、273 行；RS archive 的 `retrospective.md` §5、§6 |
| 第二組（一般程式案例） | 對照文件 `./2026-10-05-verification-comparison-case-resurface.md` §4 的 A1–A11 | 對照文件全文；證據包 `./evidence/2026-10-05-resurface-verifier-pack/` 的 `mut-vp{,2,3}.json`（確認 id 12 在第一批是活口、第二批起消失）與 `PROVENANCE.md` |

**刻意沒算進第一組的相鄰紀錄**（照範圍裁定，只列不計）：F-ID9（盲測執行者逐條判對、FINAL 寫錯，ledger 第 77 行）；Identity verify PRECHECK 因本機 `origin/main` 落後數到 33 個 commit（實際 8，Identity retrospective §2）；F-ID14、F-RS5、F-RS8（紀錄的事實錯誤）；`openspec archive` 中止仍回 exit 0（Identity retrospective §5）。若納入，§2 的 ② 與 ⑦ 會變強；這等於擴大範圍，本文不做。

---

## §1 逐筆清單

「工具種類」：**程式**＝腳本、測試、評分器；**agent 照文字執行**＝由 agent 依 schema／prompt 文字執行的檢查或給 agent 用的格式；**人判**；**紀錄**＝描述驗證的文字。「觸發方式」指這個出錯是被什麼發現的。

| # | 工具 | 工具種類 | 怎麼壞的 | 類別（§2） | 誰發現 | 出處 |
|---|---|---|---|---|---|---|
| F-ID6 | 盲測回報格式 v2 初稿 | agent 照文字執行（給執行者的輸出契約） | 每條 check 只有 4 個 token，沒有不阻擋的「無判定」選項 → 可能讓 RED 翻面 | ③ | 器材 v2 審查 r0（派工前） | ledger 第 84 行 |
| F-ID11 | `blind-kit/v2/grade.py` | 程式 | 同一案例代碼出現兩段時只保留最後一段，注入重複仍 MATCH 22 | ⑤（自測缺口另見 ④） | Codex 程式碼審 r1 | ledger 第 116、119 行；Identity retrospective §2 |
| F-ID13 | retrospective PRECHECK 的 grep | agent 照文字執行 | `templates/verify.md` §9 的 `- [ ] ✅ PASS` 會被 PRECHECK 的 grep 讀到 | ⑤ | 文件審 r1 batch 4 | ledger 第 116 行 |
| F-ID15a | verify 時寫的腳本 | 程式 | Windows `cmd` 不認 `2>/dev/null`，CLI 輸出讀不到 | ② | 見 §5 第 1 條（來源說法不一） | Identity `verify.md` 第 273 行；retrospective §1 |
| F-ID15b | 同上 | 程式 | check 3 只比標題，把 MODIFIED 誤判為已同步 | ① | 同上 | 同上 |
| F-RS7 | verify PRECHECK「commit 數 > 0」 | agent 照文字執行 | 想證明「實作已產出」，實際只證明「分支上有任意 commit」；設計階段的 2 個 commit 就讓它通過 | ① | 紀錄沒寫是誰先指出 | RS retrospective §5 |
| A1 | plan 的反向對照 #4 | 程式 | 壞實作讓 regex 拋 IndexError；轉紅只證明崩潰 | ⑥ | Codex R2（推演，未跑） | 對照文件 §4 |
| A2 | `mutants.py` 前兩版 | 程式 | 判不出失敗型別，每條印 `(?)`（不靜默） | ③ | 作者 | 同上 |
| A3 | 測試套（plan 原稿） | 程式 | 只斷言入列，沒驗顯示日期與排序 | ① | Codex R1 | 同上 |
| A4 | 測試套（plan 原稿） | 程式 | 只測判斷函式，沒測 consumer | ① | Codex R3 | 同上 |
| A5 | 測試套（實作後） | 程式 | 「先無效、後合法」的延期段沒有測試；6 個手工壞實作也沒想到 | ④（測試缺口本身屬條件代表性，見 §2 註） | 變異測試 runner | 同上；`mut-vp.json` 活口 id 12 |
| A6 | 措辭守門測試 | 程式 | 判準改寫後仍綠，只驗字串存在 | ① | Fable R4 | 同上 |
| A7 | 變異活口的等價判定 | 人判 | 判定對、理由錯 | ⑦ | strict-reviewer r1 | 同上 |
| A8 | Codex 補審的執行環境 | agent 照文字執行（審查者在沙箱跑測試） | 唯讀沙箱建不了暫存目錄，全量 pytest 跑不起來、改跑 140 條；帳本沒記 | ② | Codex 自述 | 同上 |
| A9 | 探針的出處標記 | 紀錄 | 寫來自 `c0bf6a9`，輸出檔是 `a9bc844`（數字不受影響） | ⑦ | 對照文件盤點 | 同上 |
| A10 | 探針第 [3] 段的篩選條件 | 程式 | 用字串比對，和正式 regex 不同；【推論】遇到 `->` 或無空白寫法會分錯，當時資料沒有這些寫法 | ⑤（未實際失真） | 對照文件盤點 | 同上 |
| A11 | commit 訊息的回讀宣稱 | 紀錄 | 「diff 僅 +3 行」不精確 | ⑦ | strict-reviewer r2 | 同上 |

---

## §2 分類與跨組計數

**分類原則**：按**壞法**（機制）分，不按後果分。理由：後續要設計的是防範機制，機制分類才對得上「該加哪種 self-check」。

| 類別 | 第一組 | 第二組 | 判定 |
|---|---|---|---|
| ① **只驗了比 claim 更窄的代替品** | F-RS7、F-ID15b | A3、A4、A6 | **跨組，相對穩**（2 對 3） |
| ② **執行環境和預想的不同，結果形式正常** | F-ID15a | A8 | 跨組，**證據弱**（1 對 1） |
| ③ **工具的輸出格式表達不出需要的區分** | F-ID6 | A2 | 跨組，**證據弱**（1 對 1；A2 不靜默） |
| ④ 工具的自我檢查不完整，由另一種形狀的檢查發現 | F-ID11 的 selftest 缺口（Codex 審查抓到） | A5 的手工反向對照缺口（變異測試抓到） | **conditional，不算獨立支持**：兩筆都和其他類別共用同一個 finding |
| ⑤ 文字比對／解析把不該算的內容算進去 | F-ID11、F-ID13 | A10（只有推論，未實際失真） | 第二組無實例 |
| ⑥ 負向對照因錯的原因轉紅 | — | A1 | 單組 |
| ⑦ 驗證本身沒錯，描述它的紀錄錯了 | — | A7、A9、A11 | 單組（第一組的同類紀錄在範圍外，見 §0） |

**敏感度**：F-ID6 若改按後果歸類（可能讓 RED 翻面）會落到 ⑥，則 ③ 消失、⑥ 變成跨組，跨組數仍是 3（不計 ④）。所以「3」不是單一分類方式的產物，但第 3 類靠的都是 1 對 1。

**註**：A5 的「測試套缺一種輸入形狀」與 Identity 的「22 題沒有一題觸發 I3 分支」（起點備忘 §5 第 2 條）屬於**條件代表性**，不是工具本身壞掉；本文不把 coverage 缺口算成 verifier failure mode，留給研究 backlog 的「條件代表性」題。

**停止條件結果**：跨組類別 = 3（①②③），**未觸發停止條件**。這只表示 A 不需要因停止條件而中止，**不代表已證明存在三種普遍的 failure mode**：② 與 ③ 各只有一對實例，① 是唯一兩組各有多筆的類別。

---

## §3 在案例裡實際派上用場的 self-check／negative control

這節回答研究問題的後半：「哪些自我檢查在案例裡真的有用」。只記觀察到的，不推薦做法。

| 自我檢查 | 案例 | 結果 | 怎麼被觸發 | 出處 |
|---|---|---|---|---|
| 評分器自測 `grade.py --selftest` | Identity | 修正前（round 1）15 項通過，但**沒涵蓋**重複案例（F-ID11 漏網）；fix round 2 新增一個走完整評分路徑的重複案例檢查（修改前實跑 `[FAIL]`），修正後 16 項通過 | 主 session 執行；何時跑由 agent 決定 | `blind-kit/v2/FROZEN.md` Fix round 1 第 3 點（15 項）、Fix round 2「修法」（16 項）；修正後結果見 ledger 第 119 行；盤點表 L-ID5 |
| 用假報告試跑評分器 | Identity I3 定點驗收 | 兩條錯誤路徑都回 DIFF、全對回 MATCH 2；無 finding | **使用者裁定**後才做 | ledger 第 123 行；盤點表 L-ID5 |
| 刻意弄壞的副本＋已知答案 fixtures 驗 verify 腳本 | Identity verify | check 13 腳本：修正後對 5 個已知答案全部一致（第 273 行）；checks 8–11 腳本：tasks.md 副本上刻意弄壞的三種錯都被報出（第 184 行） | verify agent 自己做；`schema.yaml` 沒有這項要求（搜 `known answer`／`self-check`／`已知答案` 無相關命中） | `verify.md` 第 9、184、273 行 |
| 手工反向對照（逐一裝回壞實作） | 一般程式案例 | 10 個全轉紅，但**漏了** id 12 | workflow-harness `CLAUDE.md` 規則文字要求（「沒做不算寫完」），無程式強制 | 對照文件 §2 L4 |
| 變異測試 runner（含自身檢查 V1–V7） | 一般程式案例 | 抓到 id 12；V1–V7 三批皆 pass | 主 session 決定何時跑 | `mut-vp*.json` 的 `checks`、`survivors` |
| 審查者在程式寫出前讀 plan 推演／實跑 | 一般程式案例 | 抓到 A1、A3、A4 | 使用者流程要求的文件審，無程式強制 | 對照文件 §3c-4 |

**觀察**（事實）：

- 兩個案例裡，第一道自我檢查都**沒有涵蓋全部錯誤路徑**（selftest 漏重複案例；手工反向對照漏 id 12），是另一種**產生方式不同**的檢查補上的（Codex 審查；變異測試）。
- 觸發方式有四種：使用者裁定、規則文字要求、agent 自己決定、審查流程要求。**沒有一種是程式強制的。**
- 起點備忘 §5 第 3 條「TDD 把判別力檢查內建在 RED→GREEN 流程裡」：第二組 A1（反向對照因崩潰轉紅）與對照文件 §3c-1（Task 1 的 RED 是屬性不存在）顯示 **RED 本身也可能沒有判別力**。這和對照文件 H1 是同一件事，仍只有單案例，不升格。

---

## §4 兩個順帶觀察（範圍收窄）

1. **本組 16 筆（第一組 5 筆拆成 6 列、第二組 11 筆）沒有一筆是由程式強制的 Gate 發現的**；發現者是審查者、作者，或 agent／使用者決定去跑的檢查。這只描述這組樣本，**不能推出「程式 Gate 抓不到這類錯」**——這些案例的流程中，由程式強制的 Gate 本來就很少（盤點表 O7：程式強制的只有 CI 的 `openspec schema validate` 與 version-check、腳本 `grade.py`，而 `grade.py` 何時跑由 agent 決定）。
2. **出錯的工具有不少本身就是程式**（`grade.py`、verify 腳本、測試套、`mutants.py`），而且 ①②③ 每類都至少有一筆程式工具。由此能推出的是一個否定命題：

   > **Programmatic enforcement 是提升可靠性的手段，但不是 verifier correctness 的充分條件。**

   ①②③ 並非程式專屬：F-RS7、F-ID6、A8 是 agent 照文字執行的工具。

---

## §5 未查證與邊界

1. **F-ID15 是怎麼被發現的，兩份來源說法不一**：Identity retrospective §1 寫兩個缺陷「被 5 個已知答案 fixture 抓到」；`verify.md` 第 273 行寫「第一次執行出現兩個腳本缺陷……修正後的腳本對 5 個已知答案的 fixture 判定全部一致」，讀起來是先在執行中出現、修正後才用 fixtures 驗。本文的「誰發現」欄因此不填定論。
2. **第一組只有 5 筆**，且盤點表多數格子是摘要的轉述（盤點表 §0）；轉述漏掉的器材錯誤本文看不到。
3. **分類是本文作者的判斷**。§2 敏感度只試了 F-ID6 一筆換類；其他筆換類的影響沒有逐一試。
4. **觸發方式**只依紀錄明寫的填；`grade.py --selftest` 與變異測試「何時跑由 agent 決定」來自盤點表與對照文件的轉述，沒有回逐字紀錄查。
5. **沒讀外部來源**（OPA 等），依 §6 裁定。

---

## §6 使用者裁定（2026-10-05）與 C 的改題

**裁定**：

1. 本文分類可用，定位為 working taxonomy：① 相對穩；②③ 只寫成「兩組各 1 個實例，達到本次繼續研究的最低門檻，但證據仍弱」；④ conditional、不算獨立支持。保留「按壞法分類」原則。
2. **本輪不讀 OPA**。A 先用內部資料收斂；OPA（policy testing、coverage、negative cases）留給 C 的 targeted external research。外部研究是為了解決已被內部證據證實值得解的問題，不是為了把研究做完整。
3. **A 足以讓 C 升成下一題，但 C 改題。**

**C 的新題名（暫定）**：

> **C｜Completion Gate 的信任鏈：如何確保產生 PASS 的 verifier／oracle／execution environment 足以支撐該 Claim？**

改題理由**只引用 A 跨組成立的 ①②③**：即使 verifier 是程式，也會只驗代替品（①）、受執行環境影響（②）、輸出表達不出必要區分（③）。原題「Harness 的地基是 agent 執行的文字」把問題過早歸因到 agent／prompt。⑥（負向對照假紅）與 coverage 缺口只是**單組／附條件觀察**，留待 C 再看，不拿來支撐改題。

C 底下分兩個子問題：

- **(a) Enforcement／execution**：該跑的 verification 是否真的執行、由誰觸發、漏跑怎麼被擋（承接起點備忘 §4：check 13 明寫沒有機制攔截「漏跑」；§3 的「觸發方式沒有一種是程式強制」是起點證據）。
- **(b) Reliability／correctness**：verification 跑了之後，產生的 PASS 是否值得相信——oracle、工具、判準、環境。

兩者的分界：**程式化可以改善執行一致性與強制，但不自動保證 verifier 判得正確。** 能機械化的 Gate 仍應盡量機械化；Gate 不能只問「有沒有 PASS」，還要問這個 PASS 是由什麼 verification machinery 產生的。

**結尾一句**：A 的結果足以讓 C 升成下一題，條件是 C 改為上述的信任鏈題目、並同時保留 (a)(b) 兩個子問題。
