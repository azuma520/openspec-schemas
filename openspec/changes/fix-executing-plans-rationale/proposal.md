## Why

bridge 拒用 `superpowers:executing-plans` 當 apply fallback，寫的理由有兩句已不成立：Superpowers v6.4.1 重寫了 executing-plans，有 subagent 時最後會派一次全分支獨立審查，上游也不再「有 subagent 就一律導向 SDD」，改成兩條路由使用者挑。這不是 8/31 查錯，是上游改版後我們沒跟上（v6.3.0 原文仍是舊說法）。錯誤說法的源頭是正式規格 `tdd-claim-accuracy` REQ-3——它用 SHALL 規定理由必須是那兩句，只改文件不改規格，下次照規格檢查會被改回錯的。schema、兩份 README、CLAUDE.md 都對採用者與維護者宣告一件不成立的事，所以現在修。

## What Changes

**executing-plans 拒用理由（REQ-3 與所有陳述它的表面）**
- From: 「它不派任何獨立審查者、單一 agent 自做自查」「上游在有 subagent 時一律導向 SDD」；TDD 推理句為「TDD 不經過任何一個執行者」
- To: 「它沒有每個任務的審查，只在最後審整條分支一次；沒有 subagent 的平台上（fallback 會發生的情境）那次只能由作者自審；bridge 的 apply 依賴「執行過程中就有獨立審查」的結構（每個任務，或每批同類小任務，做完就審，不是只在最後審），所以不接受它」。TDD 仍不是差異點，理由改為「bridge 的 TDD 要求經 tasks.md 標註與證據契約送達執行者，與哪個執行者無關」
- Reason: 上游 v6.4.1 原文（`executing-plans/SKILL.md` 開頭段、§ Final Review、§ When to Use）使舊理由失效；結論本身仍站得住
- Impact: 非破壞性——結論不變（仍不支援），沒有任何原本合法的 artifact 變不合法；不改 artifact、`requires:` 或 PRECHECK，schema major 維持 3

**CLAUDE.md 紅旗加一句預告（僅維護者面）**
- 註明此禁令依正式設計 §5 之後會改寫為 capability / evidence / degradation 語言，由 `task-20260901-claudemd-governance-rewrite` 負責。schema 與 README 不加

**不變的部分**
- 「不接受 executing-plans 當 fallback」這個結論
- README 查核紀錄表中 2026-08-26「✅ Still true」那列（歷史紀錄；其下已有 S13 取代列）

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `tdd-claim-accuracy`: 改寫 REQ-3——拒用理由改為查證過的審查結構事實（無每任務審查；無 subagent 時最後審查為自審），刪除「上游一律導向 SDD」，TDD 推理句改為經 tasks.md 送達

## Impact

- `openspec/specs/tdd-claim-accuracy/spec.md`（歸檔時合入 REQ-3 修改）
- `superpowers-bridge/schema.yaml`（檔頭 Requirements 註解、apply instruction 的 fallback 段）
- `superpowers-bridge/README.md`、`README.zh-TW.md`（§ Seven Superpowers touchpoints 表下的「No `executing-plans` fallback」段、§ 4. Opinionated: subagent platforms only、§ Fallback strategy 的 `apply` phase 列、§ 2. Schema-level vs prompt-level integration 的維護說明；繁中版對應段）
- `CLAUDE.md`（「修 schema 時的紅旗」executing-plans 那條）
- 本 repo dogfood 副本 `openspec/schemas/superpowers-bridge/` 需重同步（gitignore，不進 commit）
- 不動：`VERSION`（發版時才動）、正式設計文件、CI
- 不處理（另案）：是否允許 executing-plans、審查頻率路由——`task-20260901-claudemd-governance-rewrite`
