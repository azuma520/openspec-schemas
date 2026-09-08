# Verification Report

> 此檔案由 `openspec-verify-change` skill 在 apply 完成後產生，用以確認實作
> 與 specs / design / tasks 的一致性。失敗的檢查須返回對應 artifact 修正後
> 再重跑 verify。

**Change**: `fix-v2-blocking-defects`
**Verified at**: `2026-09-08 (local)`
**Verifier**: `verify agent (Claude Opus 5), executing superpowers-bridge v2 verify instruction; skill fallback — the numbered checks were run manually and recorded here`

> **執行前提（已查證，非引述他人報告）**：`diff -r --strip-trailing-cr superpowers-bridge
> openspec/schemas/superpowers-bridge` 回空、exit 0 — dogfood 副本與來源一致，故
> `openspec instructions verify` 渲染的是**修好後**的 checks（715 行版本），本報告
> 描述的是修正後的 checker，不是舊副本。
>
> **本次執行的特殊性**：本 change 修的正是 checks 7、9–12 自身。因此這是**修正後
> checker 對真實 change 的第一次執行**，且被檢查的對象就是修正它們的那個 change。
> 所有判定均由本 agent 逐條從 `tasks.md` / `plan.md` / `specs/` 原文推導，
> 未沿用任何既有 review 報告的結論。

---

## 1. Structural Validation (`openspec validate --all --json`)

- [x] 全數 items `"valid": true`

**結果**：

```text
items: 5 — change/fix-v2-blocking-defects, spec/plan-contract, spec/repo-guidance,
           spec/tdd-claim-accuracy, spec/tdd-evidence-contract
summary.totals: { items: 5, passed: 5, failed: 0 }
byType: change 1/1 passed, spec 4/4 passed
```

無 ERROR 級 issue。四筆 `INFO` 級提示（`plan-contract` requirements[0]、
`tdd-claim-accuracy` requirements[1]、`tdd-evidence-contract` requirements[1] 與
requirements[2]：「Requirement text is very long (>500 characters)」）不影響
`"valid": true`。

若有失敗項目，列出 id + issues：

| Item | Type | Issues |
|---|---|---|
| — | — | 無失敗項目 |

---

## 2. Task Completion (`tasks.md`)

- [x] 所有 `- [ ]` 已變為 `- [x]`

機械掃描結果：15 個 task line，checkbox marker 全為 `x`，無 `- [ ]`、無 `- [~]`。
任務編號 `1.1 1.2 1.3 1.4 2.1 2.2 2.3 2.4 3.1 3.2 4.1 4.2 5.1 5.2 5.3`。

**未完成任務**（若有）：

| Task | 未完成原因 | 是否阻塞 archive |
|---|---|---|
| — | 無未完成任務 | — |

---

## 3. Delta Spec Sync State

對每個 `openspec/changes/fix-v2-blocking-defects/specs/` 下的 capability 目錄，與
`openspec/specs/<capability>/spec.md` 比對（逐 requirement 取本文做字元比對）：

| Capability | Sync 狀態 | 備註 |
|---|---|---|
| `plan-contract` | ✗ 待 sync | delta 的 `Plan is a per-task execution contract` 多出兩段 SHALL（1:1 兩階段、plan.md 不得承載 task-level state）與四個 Scenario（duplicate task number / duplicate plan key / unique+equal 通過 / deferral marker 從 tasks.md 讀）。主 spec 尚未含這些段落 |
| `tdd-claim-accuracy` | ✗ 待 sync | delta 對兩個既有 requirement 各加一個 Scenario（`writing-plans` 不再被當 carrier；carrier 全 spec 一致）。**主 spec 的兩處 stale clause 已由任務 4.1 直接修好並 commit（787b14c）**，但 delta 新增的兩個 Scenario 仍待 archive 時併入 |
| `tdd-evidence-contract` | ✗ 待 sync | delta 的 `Applicable tasks require RED and GREEN evidence` 改寫本文（移除「RED 與 GREEN subject 必須相同」的單組配對語句）並新增四段 SHALL（subject 為配對單位、subject grammar、重跑不另計紀錄、判定邊界）與六個 Scenario。主 spec 仍是 pre-fix 版本 |

**判讀**：三個 capability 全為「待 sync」，這是 archive 前的**正常狀態** —— delta spec 正是
`openspec archive` 要併進主 spec 的內容，本 change 也刻意不手動先併（任務 4.1 明寫「Do not touch
the delta spec under this change; it is what `openspec archive` will merge」）。**不阻塞**，但
archive 時必須實際執行 sync，否則主 spec 會停在 pre-fix 語意。

> ⚠️ 本節屬本 agent 判斷點之一：instruction 只要求記錄 ✓/✗/N/A 三態，**未定義 ✗ 是否阻塞**。
> 本報告判為非阻塞，理由如上（sync 是 archive 動作本身的一部分）。

---

## 4. Design / Specs Coherence Spot Check

抽樣比對 `design.md` 的決策是否反映在 `specs/*.md` 的 Requirements 與 Scenarios 中：

| 抽樣項 | design 描述 | specs 對應 | 差距 |
|---|---|---|---|
| D1 | check 12 的 1:1 用「先去重、再集合相等」兩階段實現，兩種失敗給不同訊息 | `plan-contract` delta：「SHALL establish it in two stages … A duplicate on either side SHALL be reported … distinctly from a missing or extra key」＋ 三個 Scenario | 無 |
| D2 | 配對單位由 task 改為 subject；同 task 內 subject 唯一；不用順序配對 | `tdd-evidence-contract` delta：「The pairing unit is the subject, not the task」「Subject values SHALL be unique within a task」「Ordinal pairing … SHALL NOT be used」＋ Scenario「Two subjects under one task both pass」「Duplicate subject on one side blocks」 | 無 |
| D3 | subject grammar 最小可判定：恰好一個 `::`、兩側非空、不再規定路徑語法 | `tdd-evidence-contract` delta「Subject grammar」段＋ Scenario「Subject not matching the grammar blocks」「Unconventional but conforming identifier passes」 | 無 |
| D4 | check 7 改讀 `tasks.md`，其餘判定邏輯一字不動；不採納「deferred 連回 plan 條目」 | `plan-contract` delta：「plan.md SHALL NOT carry task-level state markers … Any deterministic check concerning task state SHALL therefore read tasks.md」＋ Scenario「Deferral marker is read from tasks.md」。新規則確實未出現在任何 spec | 無 |
| D5（schema major 不再 bump） | 版本決策，附「v2 未發版」前提 | 無對應 spec requirement | 見下方漂移警告 |
| D6（雙語 README 同步） | 連動面決策 | 無對應 spec requirement | 見下方漂移警告 |
| Non-Goal 2（不驗 evidence truth） | 明列不重做 evidence system、不驗 evidence truth | `tdd-evidence-contract` delta「Boundary of what these checks decide」段（SHALL verify structure, format and cardinality only） | 無 |

**漂移警告**（非阻塞）：

- D5 與 D6 在 specs 中沒有對應的 requirement。兩者性質上是**流程 / 發版決策**（版本號怎麼定、
  哪些檔案要同 commit 改），不是 capability 行為，落在 spec 之外是合理的；記為觀察而非缺陷。
  D5 的前提已由任務 5.3 於本 artifact 產出前重驗（`git tag -l` 空、`git ls-remote --tags origin`
  空、`git ls-remote origin main` = `5aa19bf`，與本地 tracking ref 相同）。
- `superpowers-bridge/templates/plan.md` 也被改了（entry-key 說明改寫為兩階段），但任務 3.1 的
  文字只點名 `templates/tasks.md` 與 `templates/verify.md`。改動本身與 D1／D6 一致、方向正確；
  記為「任務文字未涵蓋的連動面」觀察，非阻塞。

---

## 5. Implementation Signal

- [ ] Worktree 內無未 staged 的檔案 — **未滿足**
- [ ] 所有相關 commit 已推送 — **未滿足（刻意）**

**Commit 範圍**（若知道）：`5aa19bf..787b14c`（`origin/main` 起算 24 個 commit；其中屬於本
change 的三筆為 `22c15cf` mutation fixtures f8–f13、`cffe99a` 五條 check 的修正、
`787b14c` 連動面 README／templates／CLAUDE.md／canonical spec）。

**未 commit 的工作樹改動（9 個檔案，173 insertions / 31 deletions）**：

| 檔案 | 對應任務 |
|---|---|
| `superpowers-bridge/schema.yaml` | 2.1–2.4（五條 check 的最終修正） |
| `superpowers-bridge/templates/tasks.md`、`templates/plan.md` | 3.1（＋上節記錄的 plan.md 連動） |
| `superpowers-bridge/README.md`、`README.zh-TW.md` | 3.2 |
| `CLAUDE.md` | 4.2 |
| `openspec/changes/fix-v2-blocking-defects/tasks.md` | 各任務的證據紀錄 |
| `openspec/changes/archive/2026-09-04-loosen-plan/errata.md` | 5.2（append-only；現況 33 added / 0 removed，任務紀錄寫 22 added——見 §8 的 5.2 列） |
| `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md` | 1.4 |

**判讀**：實作證據**存在且完整**（commit ＋ 工作樹兩者合計覆蓋全部 15 個任務），但 instruction
第 5 條字面要求的「no unstaged files」目前不成立。未推送是使用者裁定的結果（本 change 在外部
code review 完成前不進 archive、不推送）。記為 **warning，不阻塞本 artifact**；archive 前應
把工作樹改動收成 commit。

> ⚠️ 本節屬本 agent 判斷點之二：instruction 第 5 條只說「Confirm all code changes are
> committed」，**未說明未 commit 時是 FAIL 還是 warning**。本報告判為 warning，理由是證據
> 本身齊備、且未 commit 是進行中狀態而非缺陷；但這是本 agent 的判定，不是文字給的。

---

## 6. Front-Door Routing Leak Detector（warning,非阻塞）

設計產出不應落在 `docs/superpowers/specs/`(brainstorm artifact 的
output redirection 會把它導到 `openspec/changes/<name>/brainstorm.md`)。

偵測:

```bash
ls docs/superpowers/specs/*.md 2>/dev/null
```

- [x] 無檔案,或存在的檔案是 schema 安裝前的合法存留

**WARNING — Front-door routing leak**：`docs/superpowers/specs/` 下存在 4 個 `.md`。

**洩漏清單**：

| 檔案 | 內容是否已 captured 進 change | 建議動作 |
|---|---|---|
| `2026-05-02-openspec-schemas-monorepo-design.md` | N/A — schema 安裝前的 repo 設計 spec，`CLAUDE.md`「相關連結」節直接引用 | 保留 |
| `2026-08-27-bridge-guarantee-architecture-direction.md` | N/A — Bridge Guarantee 方向文件，`CLAUDE.md` 動工門檻節以它為準 | 保留 |
| `2026-08-28-concept-poc-traceability-gate-design.md` | N/A — 概念 PoC 設計，對應 `docs/superpowers/poc/` 的報告 | 保留 |
| `2026-09-01-bridge-guarantee-formal-design.md` | N/A — 正式設計核可文件（雙 YES 閘門的第二個 YES） | 保留 |

**判讀**：四份都不是本 change（或任何 schema-installed cycle）的 brainstorm／design 產出被
導錯地方，而是 repo 自身的方向 / 治理文件，且被 `CLAUDE.md` 當成 authority 引用。屬
instruction 明列的「adopters may have legitimate non-schema use of that directory predating
schema install」情形。**不阻塞，不建議刪除。**

> 不會擋住 archive。新的 schema-installed cycle 產生的洩漏,應搬進
> `openspec/changes/<name>/brainstorm.md` 或 `design.md` 後刪原檔。

---

## 7. Deferred Dogfood vs Automated-Test Equivalence

DEFERRED TASK 的定義：`tasks.md` 裡首個非空白字元為 `- [~]` 的任務行才算。

**掃描結果：`tasks.md` 存在，15 個 task line 的 checkbox marker 全為 `x`，沒有任何 `- [~]`
任務行。** 因此本節依模板規則**留空即 PASS**。

| Deferred task (tasks.md) | Equivalent automated test | Coverage assessment | 真正 gap? |
|---|---|---|---|
| — | — | — | — |

> ⚠️ 一個容易誤判、此處明確排除的情形：`tasks.md` 第 48 行（任務 1.3）與第 109 行
> （2.3 的 `failure:` 欄位）**文字中出現 `[~]`**，描述的是 fixture `f13` 的內容。
> 依 check 7 的定義，標題、內文或紀錄欄位裡的 `[~]` 不是 deferral marker，
> 這兩處**不使本檢查 fire**。本掃描以「行首非空白字元序列為 `- [~]`」機械判定，
> 兩處皆不符合。
>
> `tasks.md` 存在，故不適用「tasks.md absent — deferral state undetermined」分支。

---

## 8. TDD Evidence Contract — Deterministic Checks 8–12

Reports the verify instruction's deterministic checks 8–12. Checks 8–11 are
per task; check 12 is per change. Any BLOCK here means the change is not
verified for archive.

Check titles, copied from the schema's check list — do not paraphrase:

8. **TDD annotation present and well-formed** (deterministic)
9. **RED and GREEN records present, required fields present and non-empty, and every `subject:` value well-formed** (deterministic)
10. **Outcome markers** (deterministic)
11. **Records pair by `subject:` value — unique on each side, then one RED and one GREEN per subject** (deterministic, two stages)
12. **tasks.md task numbers and plan.md entry keys correspond 1:1 — no duplicate on either side, then equal sets** (deterministic, two stages)

**Per-task results** (one row per `- [ ]` / `- [x]` / `- [~]` task line in `tasks.md`):

| Task | Annotation (8) | Records, fields + subject grammar (9) | Outcome markers (10) | Subject pairing (11) | Review judgement (R1–R4) |
|---|---|---|---|---|---|
| 1.1 | ✓ `TDD: n/a — the fixtures are the test material for 2.1 …` | N/A (not applicable) | N/A | N/A | ✓ R3 理由成立（fixture 是 2.1 的測試材料，其正確性由 2.1 的 RED/GREEN 展示）；R4 無 RED/GREEN 紀錄 |
| 1.2 | ✓ `TDD: n/a — test material for 2.2, same terms as 1.1 …` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 1.3 | ✓ `TDD: n/a — test material for 2.3 …` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 1.4 | ✓ `TDD: n/a — prose/doc-only; verified by reading the table …` | N/A | N/A | N/A | ✓ R3 成立（README 表格對目錄清單的雙向比對即其驗證）；R4 無紀錄 |
| 2.1 | ✓ `TDD: applicable` | ✓ 2 subjects（f8、f9），4 筆紀錄；RED 均含 `subject`/`outcome`/`failure`，GREEN 均含 `subject`/`outcome`；無重複 key；`::` grammar 全通過 | ✓ RED `FAIL`/`FAIL`，GREEN `PASS`/`PASS` | ✓ 兩側各自無重複；集合雙向相等 | ✓ R1 兩筆 RED 皆為行為性失敗（「預期 BLOCK 點名重複 key；實際 PASS，集合吃掉重複」），非 harness error；R2 subject 指向 f8/f9 fixture 與期待判定，正對應任務所交付的行為 |
| 2.2 | ✓ `TDD: applicable` | ✓ 3 subjects（f10、f11、f12），6 筆紀錄；必要欄位全備且非空；`::` grammar 全通過 | ✓ RED `FAIL`/`FAIL`/`INDETERMINATE`（皆為單一大寫 token 且非 `PASS`），GREEN 三筆皆 `PASS` | ✓ 兩側各自無重複；集合雙向相等 | ✓ R1：f12 的 `INDETERMINATE` 屬 instruction 明文承認的情形——受測對象是「靠閱讀執行的規則」，RED 記的是**規則本身在該案上無法判定**（可判定性未被滿足），是刻意的行為性失敗而非 malformed；R2 三個 subject 分別對應 grammar、去重、正控制三項交付 |
| 2.3 | ✓ `TDD: applicable` | ✓ 1 subject（f13），2 筆紀錄；必要欄位全備且非空；`::` grammar 通過 | ✓ RED `FAIL`，GREEN `PASS` | ✓ 無重複；集合相等 | ✓ R1 RED 是「check 7 應找到一個 deferred 任務、實際回報 no deferred tasks」，行為性失敗；R2 subject 對應 carrier 遷移的交付行為 |
| 2.4 | ✓ `TDD: n/a — instruction prose; the control is the residual-wording grep …` | N/A | N/A | N/A | ✓ R3 成立（殘留措辭 grep 是可重跑的控制）；R4 無紀錄 |
| 3.1 | ✓ `TDD: n/a — template prose; verified by diffing each template's check list …` | N/A | N/A | N/A | ✓ R3 成立；R4 無 RED/GREEN 紀錄（`Control result` / `Render acceptance` 兩行不是 `- RED:` / `- GREEN:` 紀錄） |
| 3.2 | ✓ `TDD: n/a — prose/doc-only; verified by reading both READMEs …` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 4.1 | ✓ `TDD: n/a — prose/doc-only; the control is a grep for both stale phrasings …` | N/A | N/A | N/A | ✓ R3 成立（本 agent 獨立複跑 grep：`openspec/specs/tdd-claim-accuracy/spec.md` 剩餘的 `writing-plans` / `plan.md` 命中皆為**禁止該措辭**的條文本身，無 carrier 宣稱殘留）；R4 無紀錄 |
| 4.2 | ✓ `TDD: n/a — prose/doc-only; verified by reading version-check.yml's grep line …` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 5.1 | ✓ `TDD: n/a — configuration / copy step …` | N/A | N/A | N/A | ✓ R3 成立（本 agent 獨立複驗：`diff -r --strip-trailing-cr` 來源 vs dogfood 副本回空、exit 0）；R4 無紀錄 |
| 5.2 | ✓ `TDD: n/a — append-only record entry …` | N/A | N/A | N/A | ✓ R3 成立——控制條件是「只有新增、沒有刪除」，本 agent 獨立複跑 `git diff --numstat --ignore-cr-at-eol` 得 **33 added / 0 removed**，刪除數為 0 的實質主張成立。⚠️ 但任務紀錄寫的是「22 added, 0 removed」，與現況的 33 不符——該檔在紀錄寫下後又被追加過（或紀錄已 stale）。新增行數不是控制條件本身，故不構成 R3 違反；記為需在收尾時對齊的紀錄漂移。R4 無 RED/GREEN 紀錄 |
| 5.3 | ✓ `TDD: n/a — a precondition check on repository state …` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |

Legend: ✓ pass · ⛔ BLOCK (checks 8–11) · N/A (task annotated `n/a`, records not owed).
Checks 9–11 examine **every** record a task carries, however many subjects it has —
a defect in the second RED is reported exactly like one in the first. Check 11 runs
two stages and stage one does **not** short-circuit: record both the duplicate-subject
findings (naming the repeated value and the side it repeats on) and the two-direction
set comparison (a subject with a RED and no GREEN, and one with a GREEN and no RED),
even when both hold.
A review-judgement violation (R1 error-output RED, R2 subject does not test the claimed
behaviour, R3 `n/a` reason does not hold, R4 an `n/a` task carrying RED/GREEN records)
is a **blocking finding of the review**, not of a check — record it in the same row and
list it below.

**Check 11 明細（兩階段皆已執行、皆有紀錄）**：

| Task | RED subjects（出現順序） | GREEN subjects（出現順序） | 階段一：任一側重複值 | 階段二：只在 RED / 只在 GREEN | Verdict |
|---|---|---|---|---|---|
| 2.1 | `f8-duplicate-task-number::check 12 BLOCKs naming \`1.1\` as repeated in tasks.md`, `f9-duplicate-plan-key::check 12 BLOCKs naming \`2.3\` as repeated in plan.md` | 同上兩值 | 無 | 空 / 空 | ✓ |
| 2.2 | `f10-subject-without-separator::…`, `f11-duplicate-subject-one-side::…`, `f12-two-subjects-paired::…` | 同上三值 | 無 | 空 / 空 | ✓ |
| 2.3 | `f13-deferred-task-in-tasks::check 7 finds one deferred task and requires §7 enumeration` | 同一值 | 無 | 空 / 空 | ✓ |

**Check 12, stage one — duplicate keys per side**（each side examined independently;
a repeated key BLOCKs on its own, whatever the other side holds）:

| Side | Repeated keys (name each) | Verdict |
|---|---|---|
| `tasks.md` task numbers | 無（15 個編號各出現一次） | ✓ |
| `plan.md` entry keys | 無（15 個 `##` entry key 各出現一次） | ✓ |

補充：`tasks.md` 15 行 task line **全部**在 `]` 後有至少一個空白字元、其後首個 token 皆
符合 `\d+(\.\d+)*` —— 無「task line carrying no task number」的情形。`plan.md` 存在
（135 行），可收集到 entry key，非「plan.md absent」分支；`## Self-review` 不以數字開頭，
依定義不是 entry，未被收集；檔內無 `###` 層級的數字子標題被誤收。

**Check 12, stage two — set equality in both directions**（both differences must be empty）:

| `tasks.md` task numbers | `plan.md` entry keys | Only in tasks (no entry) | Only in plan (no task) | Verdict |
|---|---|---|---|---|
| `{1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 5.3}` | `{1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 5.3}` | 空 | 空 | ✓ |

> Stage one does **not** short-circuit — stage two is evaluated and recorded whatever
> stage one found, and the two messages stay distinct because the repairs differ
> (renumber one of two duplicates; add or remove a key for a missing/extra one).
> Also BLOCK: a task line carrying no task number, no collectable entry key, or no
> plan.md at all — record the last as "plan.md absent — no entry keys to compare",
> never as a set difference.

**Blocking findings** (deterministic checks and review judgements):

- 無。checks 8–12 全數通過，R1–R4 四項 review judgement 亦未發現違反。

**本次執行中，文字未替執行者決定、由本 agent 自行判定之處**（依 instruction「若發現仍需自行
決定之處，應記錄而非默默判定」）：

1. **checks 8–11 的行掃描未排除 HTML comment 與 fenced code block。** 「TASK LINE」與
   「`#` heading」的定義是純粹的行首字元判定，`<!-- -->` 區塊或 ``` 圍欄內若出現形如
   `- [x] 1.1 …` 或 `## 2.1 …` 的行，依字面會被收進來。本 change 的 `tasks.md` 開頭有
   一段 40 行的 HTML comment，本 agent 逐行確認其中**沒有**任何行首為 `- [`、也沒有
   `#` 起首的行，故此模糊處**在本次未觸發**；記為潛在歧義，非本次的 finding。
   （check 12 對 `plan.md` 的 `##` 收集同理。）
2. **check 3 的 ✗ 是否阻塞、check 5 的未 commit 是否為 FAIL**，見 §3 與 §5 的兩處 ⚠️ 標註。

> **Claim boundary — copy as written, claim no more.** These checks are
> deterministic in *what they decide* and agent-executed (instruction-mediated)
> in *how they run*: their execution is the verify agent following the schema
> instruction. This schema requires them to run before archive and to block on
> failure, but this is **not** a Harness-level, mechanically enforced, non-bypassable
> archive-time gate — if the verify agent skips one, no mechanism in this schema
> intercepts the omission, and review of this file is the only backstop. Checks 9–11
> decide **structure, format and cardinality only** — never evidence truth. The checks
> verify the **presence and structure** of the annotations and records; they do
> not establish that the evidence is authentic (the evidence is agent-submitted), do
> not prove a test-first development history, and do not assess semantic quality.

> **Freshness.** Every result above describing `tasks.md` or `plan.md` describes it
> as it was when that check ran. If either file is modified afterwards, the results
> computed from it are **STALE** and those checks must be re-run before archive.
> The affected set derives from each check's **inputs**: an edit to `tasks.md` reaches
> **§2, §7 and §8's checks 8–11 and 12**; an edit to `plan.md` reaches **check 12 only**.
> Scope is deliberately those two files — staleness for the checks reading `specs/`,
> `design.md`, commit state or `docs/` is not addressed here and must not be claimed
> to be. This is agent-executed like the checks themselves: **nothing in this schema
> detects a stale result.**

---

## Overall Decision

- [ ] ✅ PASS — 可進入 finishing-a-development-branch 與 archive
- [x] ⚠️ PASS WITH WARNINGS — 可進入後續步驟但需注意：見下列四點
- [ ] ❌ FAIL — 返回失敗的 artifact 修正後重跑 verify

**警告（皆非本 artifact 的阻塞項，但 archive 前必須處理或已被使用者裁定）**：

1. **code plane 的外部獨立審尚未取得。** doc plane 已由外部審查者（Codex `gpt-5.6-sol`，
   兩批、其中一批三輪）通過；**code plane 的外部審查者不可用（配額），該 gate 由
   contract-aware fallback 審查者承擔**，四輪、九項 findings 全數關閉、終端
   `✅ Ready`。依全域紀律，**fallback 判定是暫時性保證、不是已完成的外部審**——
   本報告不把 code plane 描述為「已外部審查」。使用者已裁定：**本 change 在外部
   code review 完成前不進 archive。**
2. **工作樹尚有 9 個未 commit 檔案**（§5）。實作證據齊備（commit ＋ 工作樹合計覆蓋 15 個
   任務），但 instruction 第 5 條的字面條件未滿足；archive 前應收成 commit。
3. **三個 capability 的 delta spec 尚未併入主 spec**（§3）。這是 archive 動作本身要做的事，
   但必須確實執行，否則主 spec 會停在 pre-fix 語意。
4. **`docs/superpowers/specs/` 存在 4 個 `.md`**（§6）。經逐份確認為 repo 自身的方向 /
   治理文件、被 `CLAUDE.md` 引用，屬 instruction 明列的合法存留，不建議刪除。
5. **任務 5.2 的紀錄與現況有一處數字漂移**：紀錄寫 errata.md「22 added」，現況為
   33 added / 0 removed（§5、§8）。控制條件（刪除數為 0）仍成立，故不是 R3 違反，
   但紀錄應在收尾時對齊實際值。

**下一步**：

1. 把工作樹改動收成 commit（警告 2）。
2. 取得 code plane 的**外部**獨立審查；fallback 的 `✅ Ready` 不取代它（警告 1）。
3. 外部審通過後才產出 retrospective 並執行 archive（archive 時完成 delta spec sync，警告 3）。
4. ⚠️ **Freshness**：步驟 1 若動到 `tasks.md`（例如補紀錄），§2、§7 與 §8 的 checks 8–12
   即為 STALE，必須重跑並更新本檔；只動 `plan.md` 則僅 check 12 需重跑。
