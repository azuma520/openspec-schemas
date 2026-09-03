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
entry key 必須放在每個 `##` heading 最前面（`## <task-number> — <title>`），
因為 verify 的 entry-key 檢查讀的就是這個位置；key 對應 tasks.md 的任務
編號，1 對 1，兩邊集合必須完全相同（tasks.md 少一個或 plan.md 多一個都
會擋在 verify）。**這份範例的 entry key 集合 {1.1, 1.2, 2.1} 刻意對齊
templates/tasks.md 範例的任務編號集合——兩份範例本身就是配對的種子，不是
各自獨立的示範。**
-->

## 1.1 — <!-- Task title -->

- **Delivers:** <!-- 這個任務交付什麼端到端行為，不是逐層列實作步驟 -->
- **Acceptance:** <!-- 具體、可驗證的條件；禁止「運作正常」這類無法驗證的說法 -->
- **Blocked by:** <!-- 必須先完成的任務編號，或明寫 "none" -->
- **Interfaces:** <!-- 條件性欄位——只有這個任務與其他任務耦合時才寫：交換的名稱/形狀，以及對方是哪個任務 -->

## 1.2 — <!-- Task title -->

<!-- 這個範例刻意省略 Interfaces 區塊：1.2 與其他任務沒有耦合，示範
「沒耦合就整段省略、不要硬湊」這條規則本身，而不是只在註解裡宣稱它。 -->

- **Delivers:** <!-- 這個任務交付什麼端到端行為，不是逐層列實作步驟 -->
- **Acceptance:** <!-- 具體、可驗證的條件；禁止「運作正常」這類無法驗證的說法 -->
- **Blocked by:** <!-- 必須先完成的任務編號，或明寫 "none" -->

## 2.1 — <!-- Task title -->

- **Delivers:** <!-- 這個任務交付什麼端到端行為，不是逐層列實作步驟 -->
- **Acceptance:** <!-- 具體、可驗證的條件；禁止「運作正常」這類無法驗證的說法 -->
- **Blocked by:** <!-- 必須先完成的任務編號，或明寫 "none" -->
- **Interfaces:** <!-- 條件性欄位——只有這個任務與其他任務耦合時才寫：交換的名稱/形狀，以及對方是哪個任務 -->
