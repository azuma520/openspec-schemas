<!--
Raw capture of superpowers:brainstorming output.

本檔原樣捕捉 brainstorming skill 的產出，不強制結構。
Skill 的自然產出通常是 decision log 格式（背景 → 決議鏈 Q1-Qn → 設計取捨），
但依對話內容可能有不同組織方式。

design.md 從本檔萃取並重新整理為結構化設計文件。

不要將本檔的內容複製到 design.md — design.md 是獨立的重組產物，
兩者互補但不重疊。
-->

# Brainstorm — executor-governance-wording

日期：2026-10-08（session 開工於 17:15 收工之後）
工作地圖：`task-20260901-claudemd-governance-rewrite`
Superpowers brainstorming skill：v6.4.1（本機 `claude-plugins-official/superpowers/6.4.1`）

## 分類

**Bounded**：改的是 repo 內既有的文字與指令（CLAUDE.md、bridge README 中英、`schema.yaml` 的說明與 apply / retrospective 指令、`templates/retrospective.md`、living spec），沒有新流程、新執行器或新檢查。依 D1 裁定（`docs/superpowers/research/2026-10-08-superpowers-6x-capability-gap.md` §4），不論路徑，設計寫進本檔後停下等核可。使用者同意此分類。

## 背景

- 正式設計 §5（`docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md` 第 195–222 行）：execution-path agnostic, contract-governed——任何執行路徑只要具備所需能力、或依 G3 合法降級並留 degradation record 即可；失去的是 required 保證 → BLOCK、不得降級；Evidence 不能把不存在的 capability 變成存在。第 222 行明寫 CLAUDE.md「禁止 executing-plans 當 fallback」紅旗由後續 implementation change 改寫為 capability / evidence / degradation 語言。
- CLAUDE.md 第 258 行的紅旗仍是舊的工具禁令，句尾帶「⚠️ 之後要改寫」。
- 2026-10-06 使用者裁定併入兩項（工作地圖 name 原文）：① 純措辭更正型 change 的執行路徑明文化（來源 `openspec/changes/archive/2026-10-06-fix-executing-plans-rationale/retrospective.md` §6 第 1 條，該條寫 **Promote to schema（apply instruction）**）；② bridge README 中英文談 executing-plans 的兩段（Seven Superpowers touchpoints 段提示框、設計觸點 #4）把理由與證據分開。
- 前置事實：`fix-executing-plans-rationale`（2026-10-05/06，commit `9ef62c2`）只修了理由使之符合 v6.4.1，使用者當時裁定「只修理由、不重評 fallback」。

## 探索中發現的事實

1. **同類問題不只在 README 兩段。** `schema.yaml` 的 `description`（第 8–12 行，CLI 會讀的 YAML 值）與 apply 指令（約第 1795–1806 行）同樣把設計理由與 executing-plans 的上游行為寫在同一句。README 另有第 392 行（apply 段一句指向設計觸點）、第 702 行（Capability detection 段的 apply 備援說明）談到同一理由。依「一個缺陷＝一類缺陷」一併處理。
2. **CLAUDE.md 一改會與 schema 現行行為脫節。** schema 現在沒有 subagent 就在 Step 0 STOP、請改用 `spec-driven`；§5 說 harness 不挑執行器，但 schema 目前是挑的。
3. **living spec 規定了理由的位置與形式。** `openspec/specs/tdd-claim-accuracy/spec.md` REQ-3（第 61–103 行）要求「everywhere the bridge explains why it is not supported as an apply fallback」理由都建立在 executing-plans 自身的結構事實上；情境 S1、S3 點名的範圍是 schema.yaml、兩份 README 與 **CLAUDE.md 紅旗清單**。這與 ②（理由與證據分開）及紅旗改寫直接衝突——只改文件不改 REQ-3，新文件會違反現行規格。
4. **retrospective 的紀錄位置是現成的。** `schema.yaml` retrospective 指令 §4 的 skipped-skill rules（約第 1640–1660 行）已要求每個略過的 skill 回答三題（What was skipped / Why this cycle / How to prevent recurrence），模板 `templates/retrospective.md` 有 `### Deliberately Skipped Skills`。
5. **verify 不讀 SDD 的產物。** `schema.yaml` 內沒有 `.superpowers/sdd`、ledger 一類的引用，所以本 change 不跑 SDD 不會撞到機械阻擋。
6. **只有 `tdd-claim-accuracy` 擁有 retrospective 略過規則的規格。** 其他五份 living spec（contract-identity、plan-contract、release-versioning、repo-guidance、tdd-evidence-contract）都沒有。REQ-4 目前只管 `templates/retrospective.md`；REQ-5 末段「skipped-skill rules … stay as they are」是 REQ-5 自身不改它們的聲明，不禁止其他 requirement 調整。

## 決議鏈

**Q1：範圍要多大？**
選項：A 只改說明文字（含 schema 裡的理由措辭），不改 schema 行為；B 另外讓 apply 接受無 SDD 的合法降級路徑；C 只改 CLAUDE.md。
**裁定：A**，附三個邊界——
- 本輪修正 CLAUDE.md、README 中英與 schema 中混合治理理由與上游版本事實的說明。
- 不修改 Apply Step 0 的 STOP 行為，不新增 fallback、審查機制或降級資料結構。
- 「是否支援無 SDD 的能力等價或合法降級執行」留待後續依正式設計 §9 研究與裁定，不當作本次已完成的功能。

使用者補充的區分：要移除的是不合理的**工具禁令**，不是立即放寬 Bridge 現有的**能力保障**。降級紀錄只揭露失去的保障，不能自動授權取消必要保障；某 change 要求獨立審查而替代模式無法提供，就應停止或找真正能滿足要求的方法。

schema 的說明要清楚表達兩件事：
1. 一般原則：執行模式以能力、審查獨立性及可取得的證據判斷，而不是依工具名稱一律禁止。
2. 目前限制：本版 Bridge 的 Apply 仍要求 SDD；沒有必要能力時維持 Step 0 STOP，不自動切換到 executing-plans。

A 是治理說明對齊，不是宣稱 §5 的彈性執行能力已落地。

**Q2：要不要開 opsx change？**
**裁定：開小型 opsx change。** 因為 `schema.yaml` 也要改，依三軌制不因只改措辭跳過程序。版本號先核對 Versioning 判準再決定，不預設 patch。

**Q3：「沒有能力執行 SDD」與「有能力但刻意不用」怎麼區分？①要寫成什麼？**
複盤 §6 第 1 條的情境（8/31 `fix-tdd-transitive-claim`、10/06 `fix-executing-plans-rationale`）是本機**有** subagent、經使用者同意**刻意不跑** SDD，與「沒有 subagent 的平台」不同；「目前限制：Apply 仍要求 SDD」碰不到這個情境。

**裁定：** 三種情境分開——

| 情境 | 定位 | 處理原則 |
|---|---|---|
| 沒有 subagent 能力 | 能力不足 | 依現行 Step 0 停止 |
| 有 SDD，正常執行 | 正式支援路徑 | 按契約完成逐項與整體審查 |
| 有 SDD，但刻意不使用 | 例外偏離 | 需使用者明確裁定；記錄替代措施及失去的保障；不得宣稱等同 SDD |

第三種**不是新支援的執行模式**。規則核心（使用者原文）：

> 若經使用者明確裁定而刻意略過 SDD，應於 retrospective 的既有 Deliberately Skipped Skills 段落，如實記錄原因、實際執行與審查方式、替代驗證措施，以及未能提供的 SDD 保障。這項紀錄僅揭露流程偏離，不代表該執行方式已獲 Bridge 正式支援，也不能將未達成的必要保障視為已完成。

若現行 schema 的強制要求不允許這種例外，不能只靠 retrospective 紀錄宣稱流程符合契約；必須誠實標示為非標準執行。不新增機械檢查或降級資料結構。

**Q4：本 change 自己的 apply 要不要跑 SDD？**
**裁定：不跑，只限本次，作為具名、經核可的流程例外。** 理由：修改集中在治理說明與指令措辭；不新增程式功能或執行器；已知 worktree 會與 dogfood 環境的 opsx 指令互相干擾（10/06 同因）；可透過獨立 Codex 文件審查、變更差異檢查與完整 bridge verify 提供與風險相稱的檢查。

必須記錄：沒有執行 SDD，就沒有 SDD 的逐 task 獨立審查流程；外部審查不能直接聲稱與其能力等價。不得把本次當作正式支援非 SDD 執行模式的驗證成功，也不得聲稱完全符合現行 SDD 執行契約。連續第三次這樣做，不自動升格為正式支援模式（那是 §9 的事）。若遇到明確不可略過的強制阻擋，停止並回報，不自行繞過。

**Q5：版本號會不會被 retrospective 的新說明牽動？**
README Versioning 段：previously-valid artifacts becoming invalid 獨立即足以升 schema major。若在 retrospective 指令新增必填欄位，舊 retrospective 可能被認定不合法。
**方向：** 不新增欄位，寫成「既有三題在經裁定的略過時如何回答」。最終是否為 patch 依 Versioning 判準於 proposal 確認，不預先指定。

**Q6：例外情況下「How to prevent recurrence」怎麼寫？**
核可過的偏離不是要預防的錯誤。
**裁定：** 要避免的是 agent **未經授權**自行偏離流程、**未揭露**的保障缺口、事後把缺少的保障說成已具備（**不實的符合性宣稱**）；不是禁止所有經明確裁定的例外。因此該題記錄「如何揭露偏離、證據保存在哪裡」，不新增強制控制機制。

**Q7：是否重新討論 §5 的能力導向原則？**
**裁定：不重議。** 本次是把既有設計原則落實到文件與指令。三個層次各司其職：

| 層次 | 關心的事 | 舉例 |
|---|---|---|
| 能力（Capability） | 系統能做什麼 | 執行測試、獨立審查、追蹤需求 |
| 保障（Assurance） | 如何確認能力確實發揮作用 | 審查者具備獨立性、結果有可核對的證據 |
| 工具與流程（Mechanism） | 用什麼方式實現 | SDD、Codex、CI、其他 Agent 工作流 |

執行過某工具 ≠ 取得某保障。「規定證據，不規定步驟」不是不要步驟，而是不把特定步驟誤當成真正追求的保障。

## 核可的設計（六個修改面）

| # | 位置 | 改成什麼 |
|---|---|---|
| 1 | CLAUDE.md 第 258 行紅旗 | 刪「⚠️ 之後要改寫」句。禁令從「不准加 executing-plans」改為能力與保障導向：不准加入不具備 apply 所需能力（執行中的獨立審查）、又未依 §5 合法降級的執行方式；不准把降級紀錄當成保障已滿足。註明目前限制：本版只支援 SDD |
| 2 | `schema.yaml` description（第 8–12 行）、apply 約第 1795 行 | 拆成一般原則＋目前限制；executing-plans 的具體行為改指向 README 的紀錄 |
| 3 | `schema.yaml` apply 指令 | 寫明三種情境：無 subagent 能力 → Step 0 STOP（現行）；有 SDD → 照契約；有 SDD 但經使用者明確裁定刻意略過 → 例外偏離、非支援模式、不得稱等同 SDD、記在 retrospective |
| 4 | `schema.yaml` retrospective skipped-skill rules＋`templates/retrospective.md` 第 74 行附近說明 | 不加欄位；說明經裁定的略過如何回答既有三題：What was skipped 寫出失去的保障；Why this cycle 寫出使用者裁定、實際執行方式與替代審查／驗證；How to prevent recurrence 針對未授權偏離、未揭露缺口、不實符合宣稱，寫出本次如何揭露、證據在哪 |
| 5 | README 中英：第 313 行提示框、第 392 行、設計觸點 #4（第 463 行）、第 702 行 | 只寫理由，連到 Re-verification log；在紀錄補上 executing-plans 的完整事實與查證版本（現有 S13 列只寫 v6.4.1，提示框寫 v6.4.1–v6.4.2）。舊的帶日期紀錄列不改 |
| 6 | living spec `tdd-claim-accuracy` | **MODIFIED REQ-3**：設計理由與版本證據分離——設計說明／schema／CLAUDE.md 說明 Bridge 要求的能力、保障與執行限制，並引用已查證的版本事實；Re-verification log 記錄特定上游版本提供／缺少哪些能力及查證來源；CLAUDE.md 紅旗移出「逐處陳述 executing-plans 版本事實」的範圍。原 REQ-3 三條禁令保留（不以上游推薦為理由、不說它完全沒有獨立審查、不以 TDD 為區分）。移出範圍不代表紅旗可用缺乏依據的理由。**MODIFIED REQ-4**：刻意略過 SDD 的揭露方式併入（使用者偏好整合既有 REQ-4，不新增獨立 requirement），適用範圍由模板擴及 `schema.yaml` retrospective 略過規則 |

## 範圍邊界

- 不改 Step 0 的 STOP；不開放新的執行方式；不新增 fallback、機械檢查或降級資料結構。
- 刻意略過 SDD 只寫成偏離紀錄，不是放行指示：「使用者同意 → 寫進 retrospective → 就算完全符合 Bridge」不成立。
- 版本號依 Versioning 規則於 proposal 決定。

## 驗證

無程式碼；`tasks.md` 全部 `TDD: n/a` 並附理由。驗證：
- 逐項搜尋：REQ-3 列為已取代的舊說法不再出現，新說法在每個修改面都到位。
- `openspec schema validate superpowers-bridge`（照 repo CLAUDE.md 的本地驗證流程）。
- Codex 文件審查。
- bridge verify。

另須確認三個語意未被意外改變（併入文件審查與 verify，不新增機械檢查）：
1. 沒有 subagent 時仍會 STOP。
2. 有 SDD 時仍走正式執行路徑。
3. 刻意略過 SDD 的紀錄不會被解讀為已滿足必要保障。

## 執行方式

依 Q4 裁定：主 session 執行、不跑 SDD（具名例外），retrospective 如實記錄偏離與保障差異。
