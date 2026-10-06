# fix-executing-plans-rationale — Plan Contract

> **For agentic workers:** 本 change 依 design D5 由主 session inline 執行，不走
> subagent-driven-development；品質由外部審查（文件審＋程式碼審）多輪把關。
> Each entry states what "done" means for one task, not how to get there.

**Goal:** 把 bridge 拒用 `superpowers:executing-plans` 當 apply fallback 的理由，在 schema、兩份 README 與 CLAUDE.md 改成符合修改後 REQ-3 的查證事實；結論（不支援）不變。

**Pointers:** `specs/tdd-claim-accuracy/spec.md`（REQ-3 修改版）；`design.md`（D1–D6）。

**Global constraints (verbatim from the specs; every entry below is bound by them):**

- The rationale SHALL rest on verified structural facts about `superpowers:executing-plans` itself everywhere the bridge explains why it is not supported as an apply fallback: it runs without a reviewer per task and reviews the whole branch once at the end, and on a platform without a subagent tool — the situation a fallback would serve — that final review is performed by the author.
- The bridge's apply relies on independent review during execution (after each task, or after each batch of small same-shape tasks, rather than only at the end).
- The rationale SHALL NOT rest on what upstream recommends choosing between executors, and SHALL NOT state that executing-plans dispatches no independent reviewer at all — with a subagent tool it dispatches one for the final review.
- The rationale SHALL NOT use TDD as a differentiator between the two executors.
- Surfaces SHALL NOT describe plan.md task content as the carrier of that requirement — under the Plan Contract plan.md holds contract entries and no task list.

---

## 1.1 — schema.yaml 檔頭註解

- **Delivers:** schema.yaml 檔頭 Requirements 註解中說明「為何要求 subagent 平台」的那句，改為符合 REQ-3 的理由。
- **Acceptance:** 該註解不再含「dispatches no independent reviewer」的無條件說法；理由陳述「沒有每個任務的審查、無 subagent 時最後審查為作者自審」；不引用上游建議；`openspec schema validate superpowers-bridge` 通過。
- **Blocked by:** none

## 1.2 — schema.yaml apply instruction 的 fallback 段

- **Delivers:** apply instruction 中「This schema does NOT support `superpowers:executing-plans`」段改為符合 REQ-3 的理由，含改寫後的 TDD 推理句。
- **Acceptance:** 該段逐句可對應到 REQ-3 的一條規範或 executing-plans 6.4.1 原文的一處；不含「upstream itself directs users to subagent-driven-development whenever subagents are available」或等義句；TDD 句不再宣稱 TDD 不經過任何一個執行者，改為經 tasks.md 標註與證據契約送達；「use the built-in `spec-driven` schema instead」的指引保留。
- **Blocked by:** none

## 2.1 — README.md 三段

- **Delivers:** README.md 中說明 executing-plans 拒用理由的三段（§ Seven Superpowers touchpoints 表下段落、§ 4. Opinionated、§ Fallback strategy 的 `apply` phase 列）與 REQ-3 一致。
- **Acceptance:** 三段都不含無條件的「dispatches no independent reviewer」、不含「upstream directs users to SDD whenever subagents are available」或等義句、不以上游建議為理由；第 563–564 行與第 605 行的查核紀錄列內容不變（`git diff` 對這幾行無改動）。
- **Blocked by:** none
- **Interfaces:** 與 2.2 共用同一組論點；2.2 的繁中段落須與本任務的英文段落逐段語意一致。

## 2.2 — README.zh-TW.md 三段

- **Delivers:** README.zh-TW.md 對應三段與 2.1 語意一致的繁中版本。
- **Acceptance:** 三段逐段與 2.1 改後的英文段落表達相同論點（無增減論點）；同樣不含被 REQ-3-S3 列為已廢止的說法；查核紀錄列不變。
- **Blocked by:** 2.1
- **Interfaces:** 消費 2.1 改後的英文段落作為翻譯來源。

## 2.3 — README「Schema-level vs prompt-level integration」維護說明

- **Delivers:** 兩份 README 該節不再宣稱上游行為改版時 schema 不必修改，改為說明：結構驗證不受影響，但描述上游行為的 instruction 須對照新版重新核對並修正；必要 skill 改名或移除由 PRECHECK 擋下。
- **Acceptance:** 兩份 README 該節都不含「schema doesn't change」/「本 schema 不用改」或等義句；兩份語意一致；「PRECHECK 擋下」只限定於必要 skill。
- **Blocked by:** none

## 3.1 — CLAUDE.md 紅旗

- **Delivers:** repo CLAUDE.md「修 schema 時的紅旗」中 executing-plans 那條改為符合 REQ-3 的理由，並含一句指向正式設計 §5 與 `task-20260901-claudemd-governance-rewrite` 的預告。
- **Acceptance:** 該條不含 REQ-3-S3 列為已廢止的說法；含正式設計 §5 與該工作代號的預告句；該條仍以 ❌ 開頭、仍禁止把 executing-plans 加為 fallback。
- **Blocked by:** none

## 3.2 — 同步、結構驗證與殘留搜尋

- **Delivers:** dogfood 副本與根目錄 `superpowers-bridge/` 一致；schema 結構驗證通過；全 repo 不再有現行表面陳述已廢止的說法。
- **Acceptance:** `diff -rq superpowers-bridge openspec/schemas/superpowers-bridge` 無輸出；`openspec schema validate superpowers-bridge` 通過且 `openspec schemas` 列出它；對「dispatches no independent reviewer」「directs users to `subagent-driven-development`」「不派任何獨立審查者」「上游自己」等字串的全 repo 搜尋，命中只允許四類：歷史紀錄（`openspec/changes/archive/`、`docs/superpowers/` 下的報告、實驗快照與複盤、handoff、README 查核紀錄列與 S13/S14 列）、歸檔時才由本 change 的 delta 取代的 living spec `openspec/specs/tdd-claim-accuracy/spec.md`、本 change 自己描述舊說法的文件，以及新文字中明示「已不成立」的引用；每筆命中逐一標明屬於哪一類。
- **Blocked by:** 1.1, 1.2, 2.1, 2.2, 2.3, 3.1
