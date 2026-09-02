# TDD Evidence 分析:從成熟 Skill 程序反推最小證據契約

> 2026-09-01 loosen-plan change brainstorming 期間的分析。方法論(使用者定調):**不從「Evidence 要存哪些欄位」開始設計;先回答「我們到底想證明什麼」**——從成熟 TDD skill 的實際程序出發,反推哪些節點值得 Evidence 化。
> **定位:分析參考,不是規範**——正式拍板以 `openspec/changes/loosen-plan/` 的 change artifacts 為準。與正式設計 §4.3(TDD 證據契約)、spike 報告 S4(applicability 標註)銜接。
> 來源:兩個 skill 均全文閱讀(2026-09-01)——superpowers:test-driven-development(320 行,**主要參考**:程序完整、每個驗證節點有精確合格條件)、mattpocock-skills:tdd(36 行主檔,輔助參考:seams、tautological anti-pattern、refactor 不屬 loop)。

## 1. 三層區分(不可混)

| 層 | 是什麼 | 歸誰 |
|---|---|---|
| TDD Skill | 怎麼做(procedure) | 成熟 Skill 負責,**不搬進 Harness** |
| Verification | 要檢查什麼 | 驗證節點的定義 |
| Evidence | 憑什麼說檢查結果成立 | Completion claim 的佐證 |

## 2. Skill 實際程序與每步在防什麼

superpowers:test-driven-development 的程序(照原文,未改寫):

| 步驟 | 內容 | 防的失敗 |
|---|---|---|
| RED | 寫一個最小失敗測試(一個行為、真碼不 mock) | — |
| Verify RED | 跑它;確認**失敗而非報錯**、失敗訊息符合預期、失敗原因是**功能還不存在**(不是 typo/import 錯)。直接過→在測既有行為;報錯→修到「正確地失敗」 | 測試根本抓不到東西(「沒看它失敗過,你就不知道它測的是不是對的東西」);順帶篩掉 tautological test(構造上不可能失敗的測試產不出真 RED——Matt 版點名的 anti-pattern) |
| GREEN | 剛好讓測試過的最小實作 | 超出測試覆蓋的行為偷渡 |
| Verify GREEN | 再跑;目標測試過、**其他測試也過**、輸出乾淨 | 行為真的成立(唯一正向證明點);局部綠全局紅(迴歸);被 warning 淹沒的隱性失敗 |
| REFACTOR | 綠了之後;保持綠、不加行為 | 清理時偷改行為 |

外圈:Iron Law(先寫了碼就刪掉重來)、完工 checklist。Matt 補充:測試只寫在事先確認的 seams;refactor 屬 review 階段不屬 loop。

## 3. Procedure / Verification Point / Evidence Candidate 分類

| 節點 | 分類 | 理由 |
|---|---|---|
| 先寫測試(時序本身) | Procedure only | 不可觀察——除非完整 history provenance(明確不做;RED/GREEN 可事後製造,正式設計 §4.3 誠實邊界已載) |
| Iron Law / 刪碼重來 / GREEN 最小性 | Procedure only | 行為紀律,無觀察點/「最小」不可機械判定 |
| **Verify RED 的那次執行** | **Evidence Candidate** | 有 claim、有可觀察輸出 |
| 失敗原因確認 | Verification Point,併入 RED 有效性條件 | 不是獨立證據,是「什麼算有效 RED」的判準 |
| **Verify GREEN 的那次執行** | **Evidence Candidate** | 同上 |
| 其他測試也過(suite green) | Verification Point | 屬迴歸關注,**不進 per-task 證據**——留給 change-level verification / CI(有意識偏離 skill 原文,理由:per-task 證據要最小,塞進每張 task 在無測試框架的 repo 會逼硬掰) |
| Refactor 後再綠 | Verification Point | refactor 屬 review 階段(Matt);證據過期是 freshness 問題,正式解是 Gate digest(後續),不造半套 |
| Seams / 測試品質規則 | Procedure(語意層) | 歸 review 判斷 |

## 4. RED / GREEN 的 claim 與有效性

**RED 證明的 claim(精確版,2026-09-01 使用者兩輪修正定稿)**:

> 同一 verification subject 曾被執行,並**因目標行為尚未成立而正確失敗**;支持 RED→GREEN 狀態轉變,不支持完整 TDD history。

不得表述為「證明測試在 implementation 前執行過」;也不寫「在某 artifact state 下」——本 change 明確不做 state identity/digest,措辭不得暗示有狀態識別能力。

RED 有效性(從 skill 的 Verify RED 條件翻譯):

| 觀察到的結果 | 有效嗎 |
|---|---|
| assertion failure,訊息顯示預期行為未成立 | ✅ 唯一有效形態(behavioral failure) |
| SyntaxError / import error / dependency missing | ❌ error 不是 fail——skill 原文明令「修到正確地失敗為止」,連 skill 自己都不承認是 RED |
| harness 崩潰、超時 | ❌ 同上 |
| 別的測試失敗、目標測試沒跑到 | ❌ subject 不符 |
| 測試直接通過 | ❌(在測既有行為) |

**GREEN 的 claim**:同一 subject 執行並 PASS。

**承重接點**:RED↔GREEN 的 **subject 同一性**是機械可驗的相等性檢查——RED 測 A、GREEN 測 B,兩張「結構合格」的證據合起來什麼都沒證明。

## 5. v1 機械可驗 vs Reviewer 判斷

| v1 機械可驗(grep 級) | v1 Reviewer 判斷 |
|---|---|
| 每 task 有 TDD 標註、格式合法 | `n/a` 理由是否成立(標註是 semantic assertion——S4 拍板) |
| applicable task 的 RED、GREEN 兩筆存在 | RED 失敗輸出真是「行為未成立」而非環境錯(fail/error 之辨的殘餘) |
| 兩筆 subject 字面相等 | subject 指的測試真的驗了該 task 宣稱的行為(測對東西) |
| RED 帶非通過、GREEN 帶通過標記 | 證據真偽(v1 由 agent 提交——宣稱邊界與 S2/S5 同句) |

## 6. Concept vs first carrier(哪些欄位不是 architecture invariant)

| 概念(invariant) | v1 載體(可換) |
|---|---|
| verification method / invocation | shell command 字串 |
| verification subject | `測試檔::測試名` 字面 |
| 紀錄存放處 | plan/tasks instruction 的最小約定(正式 JSON 載體歸 S5 後續 change) |
| artifact state ref | **v1 移除,不設欄位**。RED 幾乎必然發生在 commit 前,commit hash 指不到「行為未成立狀態」;不能區分狀態的欄位是假裝在保證,比沒有更糟。「行為未成立」在 v1 的實際證據是失敗輸出本身(review 判)。「未來綁 artifact state(digest)」記為設計方向,欄位等 Gate change |

## 7. 最小 Evidence Contract(loosen-plan 收斂版,2026-09-01)

```text
tasks.md = TDD applicability 的 SSOT:
  每 task 標 `TDD: applicable` 或 `TDD: n/a — <理由>`;缺標註 = fail-closed

applicable task 完成宣告必附(required——completion claim 的最小必要集合):

RED:
- subject:verification subject 指認(v1 載體:測試檔::測試名)
- outcome:非通過,且為 behavioral failure 而非 error
- failure output:失敗輸出節錄,足以顯示目標行為當時尚未成立

GREEN:
- subject:與 RED 相同(機械驗相等)
- outcome:通過

supporting(建議附、非 required,缺之不構成 fail-closed):
- invocation:怎麼跑的(v1 載體:command)——服務 reproducibility 與 review 深查
```

**invocation 降為 supporting 的理由**(2026-09-01 以「支持有限完成宣稱所需的最小必要集合」重檢):completion claim 的判定輸入——機械四條(標註、兩筆存在、subject 相等、fail/pass 標記)與 review 三條(n/a 理由、失敗原因、測對東西)——**沒有一條以 invocation 為輸入**;失敗輸出本身通常已含測試名與斷言訊息,足供 review 解讀。invocation 服務的是「重跑驗證」(reproducibility),那是 review 深查的手段、不是宣稱成立的構成要件。useful 不自動升格 required;fail-closed 只綁 required 集合。

五個 required 欄位 + 一個 supporting、零新檔案格式、零 runtime 依賴。skill 的 TDD 例外清單(throwaway prototype / generated code / config files)可當 `n/a` 理由詞彙種子。

## 8. 明確不做清單(記為 Bridge Guarantee / Gate 強化路徑)

完整 TDD 時序 provenance/不可偽造 Evidence/Harness 自動捕獲 command 與 exit code/完整 Evidence JSON schema/executor identity/每步 procedure evidence/per-task full regression suite evidence/測試品質與 coverage 機械評分/正式 digest·freshness 系統。

Evidence 產生方式的比較結論:Harness 直接捕獲可信度最高但 v1 無 runtime 可用(事實不是選擇);**v1 落點=Agent 提交結構化紀錄+機械驗結構與 join**;Agent 純文字自述是要淘汰的現狀。

## 9. 換軌前後的 assurance 誠實盤點

舊制(writing-plans micro-step)實況:**規定了步驟、驗證了零**——現行 apply instruction 明文承認「this schema itself neither enforces nor verifies TDD」,plan 有沒有 TDD 微步驟取決於 writing-plans 對 task 型別的判斷,無任何一層保證補上。新制:不規定步驟、機械驗四條+review 判四條。從 zero evidence 到 structured evidence with mechanical presence checks,**是加嚴不是放寬;放寬的只有路徑自由度**。

**「淨升級」的宣稱範圍限定(2026-09-01 定稿)**:升級的是 **Harness 可驗證的 assurance**(從零機械檢查到四條機械檢查);**不宣稱**能證明 Evidence 真偽或完整 test-first history——那兩項在新舊兩制下同樣無保證,不在比較軸上。

保留意見(宣稱邊界必寫):這套的 assurance 底線繫在「reviewer 真的去讀 RED 輸出」上,而 review independence 在 v1 是 degradable——最弱情境(self-review+事後補造證據)依然穿得過。這不是 loosen-plan 能解的(S6/Gate 職責),但設計文件不得只寫「有 review 層把關」而不寫最弱情境。
