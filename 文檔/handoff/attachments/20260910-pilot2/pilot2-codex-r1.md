<!-- Codex formal branch review r1 — dispatched 2026-09-10 ~06:29Z, threadId 01a08a0b-45fd-7c91-9dfd-bb5135b6bf8a, model gpt-5.6-sol high, read-only, cwd worktree loosen-plan, snapshot HEAD b07d571 + frozen working tree -->
### Context mismatch

目前 working tree 與 frozen baseline 不完全一致：

- 實際有 39 個 tracked files 相較 base 有差異；清單未含 `.gitattributes`、`superpowers-bridge/templates/design.md`、`superpowers-bridge/templates/spec.md`。
- 另新增 3 個未追蹤 review-report files，不在列出的四個 handoff baseline 中。
- `proposal.md` 現在另納入 R1 `INDETERMINATE` 規則變更，超出任務座標所列的五項修復。

### Branch Overview

此 branch 收緊 v2 的 TDD evidence 與 plan/task 對應契約，並同步修正 check 7、相關模板、雙語文件、規格與 mutation fixtures。

### Review Summary

| Dimension | Rating | Notes |
| -------------------- | ---------- | ----- |
| Feature Completeness | ⭐⭐☆☆☆ | 五項主要修復多數已落地，但仍有決定性邊界、canonical delta 與 stale verify 問題 |
| Code Quality | ⭐⭐☆☆☆ | 條文很詳細，但數個合法邊界仍可得到不同判定或與作者表面矛盾 |
| Security | ⭐⭐⭐⭐⭐ | 未發現安全性、權限或敏感資料問題 |
| Performance | ⭐⭐⭐⭐⭐ | 純 YAML／Markdown 契約變更，無顯著效能風險 |
| Test Coverage | ⭐⭐☆☆☆ | 13 個 fixtures 有價值，但數個本 branch 新增的 blocking 分支沒有 mutation coverage |

### Findings

#### P0

None.

#### P1

- [openspec/changes/fix-v2-blocking-defects/specs/tdd-evidence-contract/spec.md:7] Normative delta 先要求每個 subject 各有一筆 RED 與 GREEN，隨即又寫「Subject values SHALL be unique within a task」；依字面，任何正常配對都會因同一 subject 在 RED/GREEN 各出現一次而違規，但 schema check 11 只要求「每一側」唯一。f12 因此可被一個 agent 判為合規、另一個 agent 依 SHALL 判為違規。改成 `unique within each side of a task`，並同步修正 plan.md 第 17 行的逐字 global constraint。 | origin=in-diff scope_reason=diff-file scope=in-scope evidence=openspec/changes/fix-v2-blocking-defects/specs/tdd-evidence-contract/spec.md:7
- [superpowers-bridge/schema.yaml:497] Check 7 把任何首個非空白字元為 `- [~]` 的實體行都定義成 deferred task，未排除 fenced code block 或 HTML comment；沒有真實 deferred task、只有文件範例的 tasks.md 仍會被要求填 §7，空白時遭錯誤 BLOCK。應明定並實作 Markdown lexical boundary，或明確禁止／忽略 comment 與 fence 中的 marker，並加入反例 fixture。 | origin=in-diff scope_reason=diff-file scope=in-scope evidence=superpowers-bridge/schema.yaml:497
- [superpowers-bridge/schema.yaml:789] Check 12 的 plan key 定義為 leading `\d+(\.\d+)*`「token」，卻沒有規定數字後的終止邊界；對 `## 1x — title`，regex-prefix 讀法會收集 key `1`，whitespace-token 讀法則認定 `1x` 非數字，造成同一輸入 PASS/BLOCK 不一致。應規定完整 key grammar 與尾端 delimiter，例如數字後必須是 whitespace 或行尾，並加入該邊界 fixture。 | origin=pre-existing scope_reason=diff-file scope=in-scope evidence=git-blame:932a044b@superpowers-bridge/schema.yaml:789
- [openspec/changes/fix-v2-blocking-defects/verify.md:8] Verify 仍標示 2026-09-08 執行，但 tasks.md 與 checker 在 2026-09-10 又被修改；現行 freshness 契約明定任何 tasks.md 修改都使 checks 2、7、8–12 結果 stale。第 11 行的補記只重跑 bundle sync/schema validation，還把原 `diff -r` 命令切斷，沒有證據顯示完整 checks 已重跑。應在所有修訂完成後重新產生 verify.md、更新時間與各節結果。 | origin=in-diff scope_reason=diff-file scope=in-scope evidence=openspec/changes/fix-v2-blocking-defects/verify.md:8

#### P2

- [openspec/changes/fix-v2-blocking-defects/specs/tdd-evidence-contract/spec.md:3] Schema 新增「每筆 record 的每個 field key 至多一次」及 one-line field parsing，但 MODIFIED canonical requirement 沒有載明這兩條契約；archive 後 canonical spec 無法完整描述 check 9 實際會 BLOCK 的輸入。應把 field cardinality、單行值與重複 key 行為納入 requirement/scenario。 | origin=in-diff scope_reason=diff-file scope=in-scope evidence=superpowers-bridge/schema.yaml:627
- [openspec/changes/fix-v2-blocking-defects/design.md:124] Design 要求每項新增或修改的判定都有正負 mutation fixture，但本 branch 新增的 repeated-field-key、`]` 後缺 whitespace、plan 中 `###` 非 entry 三個 blocking 分支均沒有 fixture；retrospective 第 234 行也確認它們僅靠閱讀驗證。應補最小負例及必要正向控制。 | origin=in-diff scope_reason=diff-file scope=in-scope evidence=openspec/changes/fix-v2-blocking-defects/design.md:124
- [superpowers-bridge/templates/tasks.md:49] Template 無條件宣稱換行續寫「不算錯、只是不被讀入」，但 schema 明定若續行本身符合 `- <key>: <value>` 就是 field，若重複既有 key 會 BLOCK；作者依模板貼入以 `- outcome:` 開頭的錯誤輸出時會得到意外拒絕。應同步加入 schema 的「FORM, not intent」限定。 | origin=in-diff scope_reason=diff-file scope=in-scope evidence=superpowers-bridge/templates/tasks.md:49
- [superpowers-bridge/schema.yaml:175] 作者 instruction 與 tasks template 只要求 task「帶一個」合法 TDD annotation，沒有明說至多一行；check 8 卻明確在多於一個合法 annotation 時 BLOCK。應在兩個作者表面明訂 exactly one annotation line，並補 duplicate-annotation fixture。 | origin=pre-existing scope_reason=diff-file scope=in-scope evidence=git-blame:932a044b@superpowers-bridge/schema.yaml:175
- [workflow-harness/work-map.jsonl:20] 新增的 follow-up 條目仍引用 teardown 後會消失的 `.superpowers/sdd/plan/code-rereview-fallback-3.md`；雖然 branch 新增了永久保存副本，work-map 沒改到該路徑，讀者無法從登記項直接追到證據。應透過管理該檔的 runner 將兩個引用更新為 `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/`。 | origin=in-diff scope_reason=diff-file scope=in-scope evidence=workflow-harness/work-map.jsonl:20

### Missing Items

- Missing mutation fixtures for fenced/comment task-like lines、plan-key delimiter、duplicate field keys、duplicate TDD annotations、no-space checkbox 與 `###` subheading。
- Missing canonical-spec clauses for record field cardinality and one-line parsing.
- Missing fresh verify run after the 2026-09-10 working-tree edits.
- The three preserved review-report files must be tracked before merge because retrospective.md now depends on them.

### Merge Gate

`openspec schema validate superpowers-bridge`、`openspec validate --all --json`（5/5）、JSON/JSONL parsing、bundle/dogfood byte comparison 與 `git diff --check` 均通過；但上述 in-scope P1/P2 仍屬 blocking。

⛔ Blocked — deterministic edge cases、canonical contract drift、coverage gaps 與 stale verification 尚未關閉。

gate_reason=IN_SCOPE_BLOCKING
