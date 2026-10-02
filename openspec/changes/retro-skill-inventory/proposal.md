## Why

retrospective 模板 §4 的 skill 表列了 `superpowers:writing-plans`，但 schema 的 plan instruction 明寫產出 plan.md 不需要呼叫任何 skill；照表填的人可能把它記成「跳過」，留下錯誤紀錄（Identity retrospective §6 ③）。查證後發現這只是更深一層矛盾的表現：schema 的 §4 instruction 說「列 apply 階段的 skill」，模板卻列了屬於 brainstorm 階段的 `brainstorming`——兩個 owner 對「這張表該列什麼」的定義本身不一致。每個 change 寫 retrospective 都會照它填，所以現在修。

## What Changes

**retrospective §4 skill inventory 的定義（schema instruction 與模板）**
- From: schema 寫「list each skill in this schema's apply phase」；模板列 7 列，含 `brainstorming`（非 apply 階段）與 `writing-plans`（schema 不要求呼叫）
- To: 兩類項目——① workflow 明確要求呼叫的 Superpowers skill（brainstorming、using-git-worktrees、subagent-driven-development、finishing-a-development-branch）；② schema 要求落實、需在 retrospective 留下執行情況的紀律，即使非 schema 直接 invoke（test-driven-development、requesting-code-review）。`writing-plans` 兩類都不是，從模板刪除；表剩 6 列
- Reason: 讓 schema 與模板對同一張表只有一個定義；retrospective 記的是「bridge 承諾採用的工作方法有沒有落實」，不是函式呼叫紀錄
- Impact: 非破壞性——沒有任何原本合法的 artifact 變不合法；不改 artifact、`requires:` 或 PRECHECK，schema major 維持 3

**不變的部分**
- TDD、code-review 兩列的條件性／結構性標示與「Deliberately Skipped Skills」規則（schema 第 1540 行起）原樣保留
- bridge README 只做一致性核對；brainstorm 預先核對結果為不需修改

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `tdd-claim-accuracy`: 新增 REQ-5，規範 retrospective §4 inventory 包含哪兩類項目、排除僅可私下輔助的 skill。與既有 REQ-4（§4 不誘導假宣稱）同管這張表，保持單一 owner

## Impact

- `superpowers-bridge/templates/retrospective.md`（§4 表格與說明）
- `superpowers-bridge/schema.yaml`（retrospective instruction §4 一段文字）
- `openspec/specs/tdd-claim-accuracy/spec.md`（歸檔時合入 REQ-5）
- 本 repo dogfood 副本 `openspec/schemas/superpowers-bridge/` 需重同步（gitignore，不進 commit）
- 不動：`VERSION`（依既有規則於發版時才動）、bridge README（除非核對發現衝突）、CI／lint／任何 enforcement
- 不處理（記為 observation）：`finishing-a-development-branch` 在 archive 後才執行、retrospective 寫於 archive 前的時序問題（README 設計觸點 #6 範圍）
