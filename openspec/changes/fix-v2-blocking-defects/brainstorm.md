# Brainstorm — fix-v2-blocking-defects（2026-09-07）

> Raw capture：決策日誌。分類：**corrective**（修既有 v2 契約的 correctness 缺陷，不新增能力）。
> **本檔以手寫方式建立**，未跑 `superpowers:brainstorming`——這是 schema `brainstorm` artifact instruction 明列的
> 出口（"explicitly opt to write brainstorm.md manually"），由使用者於 2026-09-07 明確選擇，非靜默降級。
> 理由：五條缺陷的問題、風險、設計取捨、最小修法與 non-goals 已於本次對話逐條裁定完畢，
> 跑完整流程只會重問已決事項。本檔的目的是**保存已完成的決策鏈**，作為 design / plan 的來源，
> 不是重新產生方案。
>
> 背景輸入：`loosen-plan` archive 紀錄（[errata](../archive/2026-09-04-loosen-plan/errata.md)、
> [verify](../archive/2026-09-04-loosen-plan/verify.md)）、post-archive 獨立 Codex review（2026-09-07 10:2x，
> thread `01a079b1-8828-7202-9bb8-817ea1a4d59f`）。

## 背景

`loosen-plan`（schema major 1 → 2，Plan Contract + TDD 證據契約）於 2026-09-04 archive，
兩個審查 plane 當時皆由 fallback 審查者承擔（Codex 配額耗盡）。

全域紀律規定 fallback 是**有條件的降級**：高風險項目不得就此結案，外部審恢復後必須補審。
2026-09-07 Codex 配額恢復後補派 code plane 外部審，範圍 `origin/main..HEAD`（16 commits、55 檔）。

**結果：⛔ Blocked，5 個 P1 + 5 個 P2。** 這證實了補審的必要性——這五條全部是
fallback 審查與本 repo 自身雙 gate 都沒抓到的 correctness 缺陷。

### 已查證依據（不是照單全收 reviewer 的話）

補審回報後逐條回原始碼獨立查證，**五條全部成立、無誤報**：

| P1 | 查證方式 | 結果 |
|---|---|---|
| 1 | 讀 `schema.yaml:548` | 明文「比較兩個集合的雙向差異」，全條無任何排除重複的段落；而 `:531`、`:553` 兩處自稱 "keyed 1:1" |
| 2 | 讀 `schema.yaml:498`、`:517` | `subject:` 只要求 trim 後非空、無格式文法；check 11 整條建立在「一 task 只有一組 RED/GREEN」前提上 |
| 3 | 讀 `schema.yaml:421` | 確為 `If plan.md has any tasks marked [~]`，而 v2 的 `templates/plan.md` 已無任務清單 |
| 4 | 讀 `openspec/specs/tdd-claim-accuracy/spec.md` | 同檔 `:42` 說走 `tasks.md`、`:59-61` 說走 `plan.md`，直接互斥 |
| 5 | 讀 `.github/workflows/version-check.yml:44` 對照 `CLAUDE.md` 耦合表 | CI 實際抓 `^\| v2 \| `，耦合表仍寫它抓 `v1` |

⚠️ P1-1 與 P1-2 屬同一個已知形態：**名稱宣稱的範圍對不上實際斷言**（check 12 叫 "1:1" 卻只驗集合相等；
check 9 叫「必要欄位齊備」卻只驗非空）。此類缺陷的症狀是「一切正常」——驗證全過、無人抗議，
只會被事後交叉比對發現。

## Q1：第 4 條要不要維持既有的「延後」裁定？

**背景**：`openspec/specs/tdd-claim-accuracy/spec.md` 那兩處矛盾**在 2026-09-04 已被發現並登記**為
`task-20260904-spec-contradiction-cleanup`，當時裁定是「另開最小 follow-up change 處理，
不在 loosen-plan 收尾時順手改」，連確切行號（`:21-22` 跨行、`:60`）都寫進了接力棒。

**拍板：不再延後，納入本 change**（使用者，2026-09-07）。

理由是**新證據改變了原本的風險判斷**：獨立 Reviewer 在完全不知道既有討論的情況下再次抓到同一處，
且理由與當初延後時考慮的不同——**canonical spec 會直接給未來執行者互相衝突的現行規則**。
一份規範性文件內部自我矛盾，會讓後人把 v2 刻意移除的載體再裝回去。

> 判準記錄：這不是推翻原裁定，是原裁定的前提（「這兩句只是待清理的陳跡、不會誤導人」）被新證據推翻。

## Q2：修法要修到多深？

**拍板：已知語意就直接修；只有語意本身還不清楚的地方才做最小設計**（使用者，2026-09-07）。

原則：**修 blocking，不追求把整套系統一次做成終局。**

逐條的修法邊界：

### P1-1 — check 12 的 one-to-one 修正

- **缺陷**：只做 ID set equality。重複 key 會被集合吃掉——`tasks.md` 兩個 `1.1` 對上 `plan.md` 一個 `1.1`，
  集合相等、通過，但實際上有一個任務沒有自己的契約條目。
- **最小修法**：兩邊 key 都必須**先保證無重複**，再做集合相等。
  即 `duplicate → BLOCK`；`unique + same set → PASS`。
- **non-goal**：不重新設計 traceability。

### P1-2 — Evidence deterministic semantics

- **缺陷**：`subject:` 無格式文法（任務指令要求 `檔名::測試名`，checker 只驗非空）；
  未明確拒絕重複的 RED/GREEN 紀錄與重複的必要欄位，使 check 10-11 無法決定性地選出唯一結果。
  後果：結構上無效或互相衝突的證據可以通過，或**不同 agent 得出不同判定**——而這套 check 自稱「決定性」。
- **最小 contract（本條按此收斂，不做 Evidence 管理系統）**：
  1. 一個 task **可以有多個** Evidence subject；
  2. subject 必須符合既定 `file::test` grammar；
  3. 同一 task 內 subject **必須唯一**；
  4. 每個 subject 必須**恰好有一個 RED 與一個 GREEN**；
  5. 多次執行歷史**不納入** completion evidence；
  6. checker **只驗結構、格式與 cardinality**，不宣稱驗證 evidence truth。
- **責任邊界（明文保留給人）**：Reviewer 仍負責判斷 Evidence 是否可信、是否真的代表 test-first、
  RED/GREEN 是否語意成立。checker 不得宣稱它驗了這些。
- **note**：第 4 點是對 check 11 的**語意變更**而非補漏——現行 check 11 建立在「一 task 一組 RED/GREEN」
  的前提上，需重寫為 per-subject 配對。

### P1-3 — check 7 carrier migration

- **缺陷**：v2 已把 `[~]` 標記移到 `tasks.md`，check 7 仍掃 `plan.md`。這是 migration 漏改：
  在 v2 底下這道檢查**永遠不會被觸發**。
- **最小修法**：直接改成檢查現行 carrier，並補正負案例。
- **non-goal**：不重新設計規則。

### P1-4 — canonical spec contradiction

- **缺陷**：同一份 spec，`:42` 與 `:59-61` 對 TDD 載體給出互斥的現行規則。
- **最小修法**：修掉那兩條仍引用舊 TDD carrier 的 stale clause，讓現行 spec 只保留 v2 的單一答案。
- **定位**：consistency repair，不是新功能。

### P1-5 — CLAUDE.md coupling table

- **缺陷**：CI 已改抓 `v2`，coupling table 還寫 `v1`。
- **最小修法**：更新成現況。
- **附帶價值**：這張表本來就是**防漏改**用的，它自己漏改了——本次可當 regression case。

## Q3：已 archive 的 loosen-plan 紀錄怎麼處理？

**拍板：不回頭改寫已 archive 的 loosen-plan**（使用者，2026-09-07）。

- 原 `verify.md` / `retrospective.md` 維持 **append-only**，一字不改寫。
- 若需要，只在 `errata.md` 追加**一條很短的 pointer**：post-archive independent review 發現
  5 個 blocking correctness defects，修復由本 follow-up change 承接。

理由：archive 紀錄記的是「當時的狀態與當時的判定」，事後改寫會摧毀唯一一份時點證據。
這與既有的 errata 處理方式（E1 / E2）一致。

## Scope

**只收這 5 個 P1。** 原 `task-20260904-spec-contradiction-cleanup` 的工作**併入本 change**，
不再另開一條重複的追蹤條目。

## Non-goals（明列，避免收尾時漂移）

1. **不納入 P2**——除非某個 P2 直接影響這 5 個 P1 的修復正確性，否則全部先記 observation / follow-up。
2. **不重做 Evidence system**——P1-2 按上述最小 contract 收斂即止。
3. **不重開 loosen-plan**——不改寫已 archive 的任何 artifact。
4. **不順手做其他治理優化**——不因收尾時看到其他可改善項目而開新支線。

## 完成條件

本 change **只驗這 5 個 P1 的修復**。沒有 blocking finding 後 archive，
再回到原本被擋住的 push → PR → CI。
