# [Feature Name] — Plan Contract

> **For agentic workers:** Use superpowers:subagent-driven-development
> to implement this plan task-by-task. Each entry states what "done"
> means for one task, not how to get there — two executors may satisfy
> the same entry by different paths and both conform.

**Goal:** <!-- 一到兩句話：這個 change 交付什麼 -->

**Pointers:** <!-- 這個 change 的 specs/ 檔案 + design.md；架構與技術棧決策放那邊參照，這裡不重複 -->

**Global constraints (verbatim from the specs; every entry below is bound by them):**

<!-- 從 specs/ 逐字複製、每條一個 bullet；不是改寫、不是摘要 -->

---

<!--
每個 entry 寫成行首的 `##` heading，`##` 後接空白，再接 entry key：
建議寫法（canonical）是 `## Task <task-number> — <title>`，舊寫法（legacy）
`## <task-number> — <title>` 仍接受。固定字 `Task`（大小寫精確）只用來
辨認寫法、不屬於 key，所以 `## Task 1.1` 與 `## 1.1` 的 key 都是 `1.1`，
同一份 plan 兩者並存就是重複。key 只能放在最前面，或放在 `Task` 之後、
兩者之間隔一個以上的 space 或 tab（`## Task1.1` 不是 entry），因為
verify 的 entry-key 檢查讀的就是這個位置（完整規則見 schema 的 Plan
Contract）；key 對應 tasks.md 的任務編號，1 對 1 是兩個條件：先確認
任一邊都沒有重複的 key（同一個編號出現兩次就是 BLOCK，訊息與「少一個 /
多一個」不同），再把兩邊化為集合、雙向比對必須完全相同（tasks.md 少一個
或 plan.md 多一個都會擋在 verify）。**這份範例的 entry key 集合
{1.1, 1.2, 2.1} 刻意對齊 templates/tasks.md 範例的任務編號集合——兩份範例本身就是配對的種子，不是
各自獨立的示範。**
-->

## Task 1.1 — <!-- Task title -->

- **Delivers:** <!-- 這個任務交付什麼端到端行為，不是逐層列實作步驟 -->
- **Acceptance:** <!-- 具體、可驗證的條件；禁止「運作正常」這類無法驗證的說法 -->
- **Blocked by:** <!-- 必須先完成的任務編號，或明寫 "none" -->
- **Interfaces:** <!-- 條件性欄位——只有這個任務與其他任務耦合時才寫：交換的名稱/形狀，以及對方是哪個任務 -->

## Task 1.2 — <!-- Task title -->

<!-- 這個範例刻意省略 Interfaces 區塊：1.2 與其他任務沒有耦合，示範
「沒耦合就整段省略、不要硬湊」這條規則本身，而不是只在註解裡宣稱它。 -->

- **Delivers:** <!-- 這個任務交付什麼端到端行為，不是逐層列實作步驟 -->
- **Acceptance:** <!-- 具體、可驗證的條件；禁止「運作正常」這類無法驗證的說法 -->
- **Blocked by:** <!-- 必須先完成的任務編號，或明寫 "none" -->

## Task 2.1 — <!-- Task title -->

- **Delivers:** <!-- 這個任務交付什麼端到端行為，不是逐層列實作步驟 -->
- **Acceptance:** <!-- 具體、可驗證的條件；禁止「運作正常」這類無法驗證的說法 -->
- **Blocked by:** <!-- 必須先完成的任務編號，或明寫 "none" -->
- **Interfaces:** <!-- 條件性欄位——只有這個任務與其他任務耦合時才寫：交換的名稱/形狀，以及對方是哪個任務 -->
