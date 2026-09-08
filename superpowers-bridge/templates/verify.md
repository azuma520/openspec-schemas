# Verification Report

> 此檔案由 `openspec-verify-change` skill 在 apply 完成後產生，用以確認實作
> 與 specs / design / tasks 的一致性。失敗的檢查須返回對應 artifact 修正後
> 再重跑 verify。

**Change**: `<change-name>`
**Verified at**: `YYYY-MM-DD HH:mm`
**Verifier**: `<who / which agent>`

---

## 1. Structural Validation (`openspec validate --all --json`)

- [ ] 全數 items `"valid": true`

**結果**：

```text
<貼上 openspec validate --all 的輸出摘要>
```

若有失敗項目，列出 id + issues：

| Item | Type | Issues |
|---|---|---|
| — | — | — |

---

## 2. Task Completion (`tasks.md`)

- [ ] 所有 `- [ ]` 已變為 `- [x]`

**未完成任務**（若有）：

| Task | 未完成原因 | 是否阻塞 archive |
|---|---|---|
| — | — | — |

---

## 3. Delta Spec Sync State

對每個 `openspec/changes/<name>/specs/` 下的 capability 目錄，與
`openspec/specs/<capability>/spec.md` 比對：

| Capability | Sync 狀態 | 備註 |
|---|---|---|
| — | ✓ 已 sync / ✗ 待 sync / N/A | — |

---

## 4. Design / Specs Coherence Spot Check

抽樣比對 `design.md` 的決策是否反映在 `specs/*.md` 的 Requirements 與
Scenarios 中：

| 抽樣項 | design 描述 | specs 對應 | 差距 |
|---|---|---|---|
| — | — | — | — |

**漂移警告**（非阻塞）：

- <若有，列出；無則填「無」>

---

## 5. Implementation Signal

- [ ] Worktree 內無未 staged 的檔案
- [ ] 所有相關 commit 已推送

**Commit 範圍**（若知道）：`<from-sha>..<to-sha>`

---

## 6. Front-Door Routing Leak Detector（warning,非阻塞）

設計產出不應落在 `docs/superpowers/specs/`(brainstorm artifact 的
output redirection 會把它導到 `openspec/changes/<name>/brainstorm.md`)。

偵測:

```bash
ls docs/superpowers/specs/*.md 2>/dev/null
```

- [ ] 無檔案,或存在的檔案是 schema 安裝前的合法存留

**洩漏清單**（若有）：

| 檔案 | 內容是否已 captured 進 change | 建議動作 |
|---|---|---|
| — | — | — |

> 不會擋住 archive。新的 schema-installed cycle 產生的洩漏,應搬進
> `openspec/changes/<name>/brainstorm.md` 或 `design.md` 後刪原檔。

---

## 7. Deferred Dogfood vs Automated-Test Equivalence

對 **tasks.md** 中標 `[~]` deferred 的手動 dogfood / smoke 任務,逐項列出
等價的自動化測試覆蓋。DEFERRED TASK 的定義:tasks.md 裡首個非空白字元為
`- [~]` 的任務行才算——標題、內文或紀錄欄位裡出現的 `[~]` 不是 deferral
marker。本檢查只讀 tasks.md:Plan Contract 讓 tasks.md 成為 task-level
state 的載體,其他檔案裡的 `[~]`(包含不合規、仍帶 task row 的 plan.md)
不在本檢查的輸入範圍內,也不會讓它 fire。若沒有等價自動化測試,該項應視為
**真正的 gap** 而非合理 deferral,建議在 retrospective Misses 中記錄。

| Deferred task (tasks.md) | Equivalent automated test | Coverage assessment | 真正 gap? |
|---|---|---|---|
| 例:3.4 `compose up + curl /actuator/health` | `LinebcIntegrationApplicationTests` (Testcontainers,24s) | Spring context boot + Flyway 跑完 + 主要 bean 注入 | ❌ 已等價覆蓋 |
| — | — | — | — |

> **判讀規則**:
> - 「等價」= 自動化測試的 assertion 集合是手動 dogfood 預期 assertion 的超集
> - 「Coverage assessment」= 列出實際被觸及的 layer (context / DB schema / wiring / HTTP path / etc.)
> - 任何「真正 gap = ✅」的列,Overall Decision 仍可 PASS,但須在 retrospective 留 follow-up 條目
> - **每一個** deferred 任務各佔一列,不是只列第一個

> **何時可以整節空白**:tasks.md 完全沒有 `- [~]` 任務行時,本節不需要填
> (空白即 PASS)。只要 tasks.md 出現任何 `- [~]` 任務行,本節必須逐項列出,
> 否則 Overall Decision 應降為 FAIL。
>
> **tasks.md 整個不存在時**:記為「tasks.md absent — deferral state
> undetermined」,**不得**記成「沒有 deferred task」——兩者是不同的結果。
> 本檢查不因此 BLOCK(缺少必要 artifact 是另一種缺陷,由 check 12 與本
> artifact 的 PRECHECK 攔);但這個 undetermined 結果不得被記成 pass。

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
| e.g. 2.1 | ✓ `TDD: applicable` | ✓ 2 subjects, each RED + GREEN complete, `::` grammar OK | ✓ FAIL / PASS on every record | ✓ unique per side; 1 RED + 1 GREEN per subject | ✓ behavioural failure, subject fits |
| e.g. 2.2 | ✓ `TDD: n/a — <reason>` | N/A (not applicable) | N/A | N/A | ✓ reason holds (R3) |
| — | — | — | — | — | — |

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

**Check 12, stage one — duplicate keys per side** (each side examined independently;
a repeated key BLOCKs on its own, whatever the other side holds):

| Side | Repeated keys (name each) | Verdict |
|---|---|---|
| `tasks.md` task numbers | — | ✓ / ⛔ BLOCK |
| `plan.md` entry keys | — | ✓ / ⛔ BLOCK |

**Check 12, stage two — set equality in both directions** (both differences must be empty):

| `tasks.md` task numbers | `plan.md` entry keys | Only in tasks (no entry) | Only in plan (no task) | Verdict |
|---|---|---|---|---|
| `{...}` | `{...}` | — | — | ✓ / ⛔ BLOCK |

> Stage one does **not** short-circuit — stage two is evaluated and recorded whatever
> stage one found, and the two messages stay distinct because the repairs differ
> (renumber one of two duplicates; add or remove a key for a missing/extra one).
> Also BLOCK: a task line carrying no task number, no collectable entry key, or no
> plan.md at all — record the last as "plan.md absent — no entry keys to compare",
> never as a set difference.

**Blocking findings** (deterministic checks and review judgements):

- <list each, or 「無」>

> **Claim boundary — copy as written, claim no more.** These checks are
> deterministic in *what they decide* and agent-executed (instruction-mediated)
> in *how they run*: their execution is the verify agent following the schema
> instruction. This schema requires them to run before archive and to block on
> failure, but this is **not** a Harness-level, mechanically enforced, non-bypassable
> archive-time gate — if the verify agent skips one, no mechanism in this schema
> intercepts the omission, and review of this file is the only backstop. Checks 9–11
> decide **structure, format and cardinality only** — never evidence truth. The checks
> verify the **presence and structure** of the annotations and records; they do not
> establish that the evidence is authentic (the evidence is agent-submitted), do
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
- [ ] ⚠️ PASS WITH WARNINGS — 可進入後續步驟但需注意：`<說明>`
- [ ] ❌ FAIL — 返回失敗的 artifact 修正後重跑 verify

**下一步**：

<說明下一個動作>
