## Context

bridge 在五個表面說明「為什麼不接受 `superpowers:executing-plans` 當 apply fallback」，行號以改動前 `a136720` 為準：

| 表面 | 位置 |
|---|---|
| 正式規格 | `openspec/specs/tdd-claim-accuracy/spec.md` REQ-3（第 61–87 行，含 S1、S2 兩個 Scenario） |
| schema 檔頭註解 | `superpowers-bridge/schema.yaml` 第 8–12 行（Requirements 段） |
| schema apply instruction | 同檔第 1707–1718 行（「This schema does NOT support…」段） |
| README 英／繁 | § Seven Superpowers touchpoints 表下「No `executing-plans` fallback」段（第 312 行）；§ 4. Opinionated: subagent platforms only, no manual fallback（第 462 行）；§ Fallback strategy 的 `apply` phase 列（第 660 行） |
| 維護者守則 | repo `CLAUDE.md` 第 252 行，「修 schema 時的紅旗」executing-plans 那條 |

五處都陳述同一組理由：①「不派任何獨立審查者，單一 agent 自做自查」②「上游在有 subagent 時一律導向 SDD」③「TDD 不是差異點」。REQ-3 用 SHALL 規定理由必須是 ①②，其餘四處依它而寫。

Superpowers v6.4.1 重寫了 executing-plans（逐行對照見 brainstorm §1.3）：有 subagent 時最後派一次全分支獨立審查、沒有時由作者自審；兩種情況都沒有每個任務的審查；上游把它與 SDD 當作由使用者挑選的兩條路；它現在無條件載入 TDD skill。①一半失效、②失效、③的結論成立但 REQ-3 的推理句（「TDD 不經過任何一個執行者」）失效。v6.3.0 原文仍是舊說法（brainstorm §1.4），所以這是上游改版造成的失效。

約束：結論（不支援）不變，見 brainstorm Q1、Q5；放寬與否屬 `task-20260901-claudemd-governance-rewrite`。

## Goals / Non-Goals

**Goals:**

- REQ-3 改寫為只陳述查證過的事實；五個表面與它一致。
- 修正後的文字不依賴「上游怎麼建議」，只依賴 executing-plans 自己的審查結構——上游建議會再變，審查結構是 bridge 真正在意的東西。
- `CLAUDE.md` 紅旗註明此禁令之後依正式設計 §5 改寫。

**Non-Goals:**

- 不改「不支援 executing-plans」的結論，不新增降級路徑。
- 不改正式設計文件（`2026-09-01-bridge-guarantee-formal-design.md`）。
- 不改 README 查核紀錄表的歷史列。
- 不動 `VERSION`、不發版、不打 tag。
- 不新增 lint、CI、verify check 或任何 enforcement。

## Decisions

### D1：先改規格，再讓四個表面跟著規格

- **選擇**：REQ-3 是唯一的理由 owner；四個表面的措辭由 REQ-3 推出。
- **理由**：REQ-3 用 SHALL 規定了舊理由；只改表面，之後照規格驗會把正確文字判成不合規。
- **已考慮 alternative**：只改表面、把 REQ-3 留給下次——拒絕，會製造「規格比實作嚴」的假合規（後人照規格把正確文字改回錯的）。

### D2：理由只寫 executing-plans 自己的審查結構，刪掉「上游建議」那句

- **選擇**：理由為兩點——(a) 沒有每個任務的審查，只在最後審整條分支一次；(b) 沒有 subagent 的平台上那次只能由作者自審，而 fallback 正是發生在這種平台。bridge 的 apply 依賴「執行過程中就有獨立審查」的結構：每個任務，或每批同類小任務，做完就審（`schema.yaml` 第 1700–1705 行已寫明 SDD 可合批、不是嚴格每任務一位審查者），不是只在最後審。
- **理由**：(a)(b) 都直接引自 executing-plans 原文且兩版（6.4.1、6.4.2）一致；(b) 正好對準 fallback 的情境。「上游怎麼建議」是第三方意見，上一次就是因為它改了才讓我們的說法失效。
- **已考慮 alternative**：改寫成新版上游建議（「使用者想要每個任務都審時，上游建議用 SDD」）——拒絕，同樣依賴第三方措辭，下次改版又會失效。

### D3：TDD 段保留結論、改推理

- **選擇**：保留「TDD 不是差異點」；推理改為「bridge 的 TDD 要求經 tasks.md 的 applicability 標註與 tdd-evidence-contract 的證據送達執行者，與哪個執行者無關」，刪除「它不經過任何一個執行者」。
- **理由**：executing-plans 現在第 149 行無條件載入 TDD，舊推理句不再成立；結論靠 bridge 自己的承載機制成立，不需要對上游 TDD 行為下斷言。
- **已考慮 alternative**：改寫成「兩個執行者都會帶 TDD」——拒絕，SDD 端仍是條件式（`implementer-prompt.md:36`），且這又是對上游行為的斷言。

### D4：預告句只放 CLAUDE.md

- **選擇**：只在 `CLAUDE.md` 紅旗加一句「此禁令依正式設計 §5 之後改寫為 capability / evidence / degradation 語言（`task-20260901-claudemd-governance-rewrite`）」。
- **理由**：風險只在維護者面——之後的 agent 可能把紅旗當永久規定，拿來反對 §5 改寫。採用者讀 schema / README，「之後可能會改」對他們無用（brainstorm Q4，使用者裁定）。
- **已考慮 alternative**：五處都加——拒絕，對採用者是雜訊。

### D5：主 session 直接執行，不走 worktree / SDD

- **選擇**：inline 執行，品質由外部審查多輪把關（文件審＋程式碼審，`schema.yaml` 屬 code plane）。
- **理由**：全是文字更正、變更面在本設計已凍結；先例 `openspec/changes/archive/2026-08-31-fix-tdd-transitive-claim/retrospective.md` 第 69–72 行記錄了相同判斷。
- **已考慮 alternative**：照 apply instruction 走 worktree＋SDD——拒絕，對五處文字修改成本不成比例，且 dogfood 副本在 worktree 內會與主 tree 的 opsx 指令互踩（同一先例）。retrospective 須在「Deliberately Skipped Skills」誠實記錄此偏離。

### D6：README 查核紀錄的歷史列不改

- **選擇**：README 第 563–564 行（2026-08-26「✅ Still true」）原樣保留。
- **理由**：它是當時查核結果的紀錄；第 605 行 S13 列已寫明「This supersedes the 2026-08-26 "✅ Still true" row above」。改寫紀錄會毀掉歷史。

## Risks / Trade-offs

- [Risk] 新理由保留禁令，與正式設計 §2.2（Independent Review = degradable）不一致 → Mitigation: brainstorm §三 記錄矛盾與保留理由；CLAUDE.md 預告句指向負責改寫的工作。
- [Risk] 修正句本身寫成新的絕對句（全域守則記錄的高發場景）→ Mitigation: 每句新理由對應到 executing-plans 原文行號（tasks / verify 逐句對照）；外部審查專看此項。
- [Risk] 中英 README 改得不一致 → Mitigation: 同一 task 內兩份一起改，verify 逐段比對語意。
- [Trade-off] 不依賴上游建議，理由變得比較「bridge 本位」，讀者看不到上游怎麼建議 → 接受：上游建議屬於上游文件，bridge 該說的是自己為什麼不接受。

## Migration Plan

N/A — 本 change 不涉及部署變更。不讓任何原本合法的 artifact 變不合法，schema major 維持 3；改完後重同步 dogfood 副本並跑 `openspec schema validate superpowers-bridge`。Rollback：revert 本 change 的 commit。

## Open Questions

（無。是否允許 executing-plans、審查頻率路由皆屬另案，見 Non-Goals。）
