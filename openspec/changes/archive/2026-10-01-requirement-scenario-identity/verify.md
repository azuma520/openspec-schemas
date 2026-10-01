# Verification Report

> 此檔案由 `openspec-verify-change` skill 在 apply 完成後產生，用以確認實作
> 與 specs / design / tasks 的一致性。失敗的檢查須返回對應 artifact 修正後
> 再重跑 verify。

**Change**: `requirement-scenario-identity`
**Verified at**: `2026-10-01 12:12`
**Verifier**: Claude Code（Opus 5.5）主 session，依 `superpowers-bridge` schema v3 的 verify instruction 執行（`openspec-verify-change` skill）；checks 2、3、7–13 的機械部分以 scratchpad 腳本逐字照規則實作，腳本先以刻意弄壞的副本與已知答案的 fixtures 驗過能抓到錯（見各節）

**PRECHECK**：commit evidence `git log --oneline $(git merge-base HEAD origin/main)..HEAD | wc -l` → 33（> 0）；task progress `grep -c '^- \[x\]' tasks.md` → 12（> 0）。兩條皆為正，繼續。（33 大於本 change 實際的 8 個 commit，因為 `origin/main` 落後本機 `main` 28 個 commit，見 §5。）

---

## 1. Structural Validation (`openspec validate --all --json`)

- [x] 全數 items `"valid": true`

**結果**：

```text
{'totals': {'items': 5, 'passed': 5, 'failed': 0},
 'byType': {'change': {'items': 1, 'passed': 1, 'failed': 0},
            'spec': {'items': 4, 'passed': 4, 'failed': 0}}}
```

若有失敗項目，列出 id + issues：

| Item | Type | Issues |
|---|---|---|
| — | — | — |

---

## 2. Task Completion (`tasks.md`)

- [x] 所有 task 的 checkbox 皆為 `- [x]` 或 `- [~]`
      （`- [~]` 是 check 7 定義的 DEFERRED TASK,不是未完成任務;
       它是否已被妥善交代由 check 7 判,不在本項失敗。仍有 `- [ ]` 才需填下表。）

12 條 task line：`- [x]` 12、`- [ ]` 0、`- [~]` 0。

**未完成任務**（若有）：

| Task | 未完成原因 | 是否阻塞 archive |
|---|---|---|
| — | — | — |

---

## 3. Delta Spec Sync State

對每個 `openspec/changes/<name>/specs/` 下的 capability 目錄，與
`openspec/specs/<capability>/spec.md` 比對（ADDED／MODIFIED 比對整個 requirement block 的非空白行，RENAMED 比對 TO 標題在、FROM 標題不在）：

| Capability | Sync 狀態 | 備註 |
|---|---|---|
| `contract-identity` | ✗ Needs sync | 新 capability，主 spec 尚不存在（8 筆 ADDED） |
| `plan-contract` | ✗ Needs sync | 3 筆 RENAMED、3 筆 MODIFIED 都尚未套用（0/6） |
| `repo-guidance` | ✗ Needs sync | `REQ-PB` 的 MODIFIED 尚未套用（標題相同、內容不同；0/1） |
| `tdd-claim-accuracy` | ✗ Needs sync | 4 筆 RENAMED、4 筆 MODIFIED 尚未套用（0/8） |
| `tdd-evidence-contract` | ✗ Needs sync | 3 筆 RENAMED、3 筆 MODIFIED 尚未套用（0/6） |

沒有任何 capability 記為「✓ Already synced」，因此 check 13 的 13.B SYNCED CAPABILITY 規則在本次不適用。

---

## 4. Design / Specs Coherence Spot Check

抽樣比對 `design.md` 的決策是否反映在 `specs/*.md` 的 Requirements 與
Scenarios 中：

| 抽樣項 | design 描述 | specs 對應 | 差距 |
|---|---|---|---|
| D1 版本 | schema major 2 → 3、bundle `3.0.0` | `schema.yaml` `version: 3`、`VERSION` = `3.0.0` | 無 |
| D2 ID 語法 | `REQ-[A-Z0-9]+` 加描述；scenario `<REQ-ID>-S<m>`，m 無前導零 | `contract-identity` REQ-1（S1–S5）；check 13 的 13.A HEADING GRAMMAR 同義 | 無 |
| D3 新號兩層 | 檢查層（大於目前主 spec 最大號、scenario 同 requirement 內比）＋發號層（查歷史最大號，check 不驗） | `contract-identity` REQ-4（S1–S6，S6 為發號層、宣稱邊界）；13.D.3 只讀目前主 spec | 無 |
| D4 同一契約 | 由操作角色判定（MODIFIED 同 ID 合法、ADDED 撞號擋、經 RENAMED TO 對應） | `contract-identity` REQ-3（S1–S6）；13.D.1 | 無 |
| D7 本 repo 補號 | 3 個 capability 共 10 條以 RENAMED 補 `REQ-<n>` 並 MODIFIED 全文；`REQ-PB` 保留、只補 scenario | delta 共 10 組 RENAMED（3＋4＋3）；`repo-guidance` 只有 MODIFIED `REQ-PB`（S1、S2） | 無 |
| D8 新 capability | 規則寫成 `contract-identity`，從 `REQ-1` 起 | `contract-identity` 8 條 ADDED，`REQ-1`–`REQ-8` | 無 |

**漂移警告**（非阻塞）：

- 無

---

## 5. Implementation Signal

- [ ] Worktree 內無未 staged 的檔案
- [ ] 所有相關 commit 已推送

⚠️ 兩項都未成立，皆為已知、非程式碼的狀態：

- 未提交：`docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/sdd-ledger.md` 的 1 行（環境摩擦紀錄：`core.longpaths`，寫於 commit `95e4d87` 之後），加上本檔 `verify.md`。兩者會與 retrospective 產出一起送文件審、再一起 commit。程式碼與 schema 沒有未提交的變更。
- 未推送：分支 `worktree-requirement-scenario-identity` 沒有設定 upstream；push、merge 依使用者 2026-10-01 的授權範圍刻意未做（授權只涵蓋 commit）。

**Commit 範圍**：`42c3d24..95e4d87`（本 change 在本機 `main` 之上的 8 個 commit）。另注意：`origin/main` 落後本機 `main` 28 個 commit，因此 PRECHECK 以 `origin/main` 為基準數到 33。

---

## 6. Front-Door Routing Leak Detector（warning,非阻塞）

設計產出不應落在 `docs/superpowers/specs/`(brainstorm artifact 的
output redirection 會把它導到 `openspec/changes/<name>/brainstorm.md`)。

偵測:

```bash
ls docs/superpowers/specs/*.md 2>/dev/null
```

- [x] 無檔案,或存在的檔案是 schema 安裝前的合法存留

**洩漏清單**（若有）：

| 檔案 | 內容是否已 captured 進 change | 建議動作 |
|---|---|---|
| `2026-05-02-openspec-schemas-monorepo-design.md` | 不屬於本 change（維護者設計文件，早於 schema 安裝） | 保留 |
| `2026-08-27-bridge-guarantee-architecture-direction.md` | 不屬於本 change（方向文件，repo CLAUDE.md 引用為現行依據） | 保留 |
| `2026-08-28-concept-poc-traceability-gate-design.md` | 不屬於本 change（概念 PoC 設計） | 保留 |
| `2026-09-01-bridge-guarantee-formal-design.md` | 不屬於本 change（正式設計，本 change 的上位依據） | 保留 |
| `2026-09-23-formal-design-revision-map.md` | 不屬於本 change（正式設計修訂對照） | 保留 |

本 change 的 8 個 commit（`42c3d24..95e4d87`）沒有新增或修改這個目錄的任何檔案；`git diff --name-status dfaedbee..HEAD` 列出的兩筆變動（修訂對照新增、正式設計修改）來自 `8002fa0`（2026-09-24），在本 change 開分支前就已進 `main`。這個 repo 的 CLAUDE.md 把 `docs/superpowers/specs/` 定為維護者自己開發本 repo 時的設計文件位置，屬於合法、非 schema cycle 的用途。

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

tasks.md 存在，沒有任何 `- [~]` 任務行（0 條），本節依規則留空即 PASS。

| Deferred task (tasks.md) | Equivalent automated test | Coverage assessment | 真正 gap? |
|---|---|---|---|
| — | — | — | — |

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
| 1.1 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ fixtures 是受測素材不是受測對象（R3） |
| 1.2 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ prose/doc-only（R3） |
| 1.3 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ 器材準備，以凍結雜湊控制（R3） |
| 2.1 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ RED 執行步驟，紀錄寫在 3.1（R3） |
| 3.1 | ✓ `TDD: applicable` | ✓ 17 subjects，34 筆紀錄（17 RED＋17 GREEN），必要欄位齊全、無重複鍵，`::` grammar 全部 OK | ✓ RED 皆 `FAIL`、GREEN 皆 `PASS` | ✓ 兩側各自唯一；每個 subject 1 RED＋1 GREEN | ✓ RED `failure:` 是「預期 BLOCK、實際 PASS」的行為失敗（R1）；subject `<fixture>::<預期判定>` 即受測案例（R2） |
| 3.2 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ 作者表面規則文字，無可重跑案例（R3） |
| 4.1 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ template prose（R3） |
| 4.2 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ prose/doc-only（R3） |
| 4.3 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ configuration / prose（R3） |
| 5.1 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ copy step，以 `diff -r` 控制（R3） |
| 5.2 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ 一次性遷移實跑（R3） |
| 5.3 | ✓ `TDD: n/a — …` | N/A | N/A | N/A | ✓ prose/doc-only record（R3） |

Legend: ✓ pass · ⛔ BLOCK (checks 8–11) · N/A (task annotated `n/a`, records not owed).
R4：tasks.md 全部 34 行 `- RED:`／`- GREEN:` 都屬於 3.1（唯一標 `applicable` 的 task），沒有任何標 `n/a` 的 task 帶紀錄。

腳本自我驗證（不是本 change 的證據，只證明這把尺量得到錯）：在 tasks.md 副本上分別①刪掉 1.2 的 TDD 行、②把一筆 GREEN 的 outcome 改成 `FAIL`、③讓兩筆 RED 共用同一 subject，腳本依序回報 check 8 BLOCK、check 10 BLOCK、check 11 兩階段各一筆 finding。

**Check 12, stage one — duplicate keys per side** (each side examined independently;
a repeated key BLOCKs on its own, whatever the other side holds):

| Side | Repeated keys (name each) | Verdict |
|---|---|---|
| `tasks.md` task numbers | — | ✓ |
| `plan.md` entry keys | — | ✓ |

**Check 12, stage two — set equality in both directions** (both differences must be empty):

| `tasks.md` task numbers | `plan.md` entry keys | Only in tasks (no entry) | Only in plan (no task) | Verdict |
|---|---|---|---|---|
| `{1.1, 1.2, 1.3, 2.1, 3.1, 3.2, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3}` | `{1.1, 1.2, 1.3, 2.1, 3.1, 3.2, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3}` | — | — | ✓ |

每條 task line 都有 task number；plan.md 存在，12 個 `##` entry 皆可取得 key。

**Blocking findings** (deterministic checks and review judgements):

- 無

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
> to be — except check 13, which states its own staleness rule (13.F) over the main
> specs and the change's delta files (§9). This is agent-executed like the checks
> themselves: **nothing in this schema detects a stale result.**

本次結果所讀的 tasks.md 是 commit `95e4d87` 的版本（含 3.1 新增的 I3 定點驗收紀錄）；plan.md 最後修改於 `05fd2f8`，該次調整 1.1（Delivers 與 Acceptance）、3.1、5.2 的契約文字，task／plan 的編號對應未改變，因此 check 12 的結論不受影響。

---

## 9. Identity Integrity — Check 13

Reports the verify instruction's check 13 (Requirement / Scenario heading identity). A BLOCK
here means the change is not verified for archive.

Check title, copied from the schema — do not paraphrase:

13. **Identity integrity** (deterministic in what it decides, agent-executed like checks 8-12; BLOCKs are of two kinds)

**Verdict**:

- [x] ✓ PASS — preview 成功，13.C／13.D 沒有任何 finding，13.E 每一項比對都完成且一致
- [ ] ⛔ BLOCK — 至少一項 finding（見下方兩表）

Check 13 的 BLOCK 分兩種、彼此不吸收：同一個 count mismatch 可能同時產生
VIOLATION 與 UNDETERMINABLE 兩種 finding，兩張表都要分別列出，**不得**
合併寫成一句「ID verification failed」。

**VIOLATION findings**（check 完整跑完某條規則後發現違反 REQ-1～REQ-4，
或一個可靠配對的 13.E 比對結果不一致）：

| 依據（13.C / 13.D / 13.E） | 檔案 / heading / 位置 | 說明（雙方數值或內容） |
|---|---|---|
| 無 | — | — |

**UNDETERMINABLE findings**（check 無法可靠跑完——preview 失敗、CLI 輸出
缺資料或形狀不符、配對不可靠；未跑完本身不是違規，也不得記成違規）：

| 依據（13.B / 13.E） | 對象 | 說明 |
|---|---|---|
| 無 | — | — |

若無 finding，兩張表都填「無」——不得省略整個表格。

**執行紀錄**（openspec 1.3.1，2026-10-01）：

- **13.B 預演歸檔**：在 repo 外的暫存目錄複製整個 `openspec/`，執行 `openspec archive requirement-scenario-identity -y`（不帶任何旗標）：exit 0、change 目錄已不在、產生 `archive/2026-10-01-requirement-scenario-identity/`，輸出 `Totals: + 8, ~ 11, - 0, → 10`、`Specs updated successfully.`——三項條件皆成立，預演成功。repo 本身的 `openspec/` 未被修改。check 3 沒有任何 capability 記為已同步，SYNCED CAPABILITY 規則不適用。
- **13.C 候選狀態**（5 個主 spec 全部）：每個 requirement 與 scenario 標題都符合語法、scenario 前綴等於所屬 requirement ID、檔內無重複 requirement ID、requirement 內無重複 scenario ID——0 finding。
- **13.D 目前狀態**：10 組 RENAMED 皆為補號遷移（FROM 無 ID），TO 依序為 `REQ-1`… ，各 capability 主 spec 目前沒有數字 ID（空集合，任何正整數合法）；10 筆 MODIFIED 皆經同檔 RENAMED 的 TO 對應回 FROM（13.D.1 (a)），FROM 的 scenario 無 ID、目前集合為空；`repo-guidance` 的 MODIFIED `REQ-PB` 以 ID 對應主 spec（13.D.1 (b)），主 spec 該 requirement 的 scenario 無 ID；`contract-identity` 為新 capability，8 筆 ADDED（`REQ-1`–`REQ-8`）與其 scenario 皆帶合法 ID、無重號——0 finding。
- **13.E 交叉核對**（只讀 stdout）：候選狀態——`contract-identity` 8／8、`plan-contract` 3／3、`repo-guidance` 1／1、`tdd-claim-accuracy` 4／4、`tdd-evidence-contract` 3／3（文字／CLI `requirementCount`），各 requirement 的 scenario 數逐位置一致；change 層——每個 capability 每種 operation 的筆數一致（ADDED 8、MODIFIED 3＋1＋4＋3、RENAMED 3＋4＋3），ADDED／MODIFIED 每筆的 scenario 數與 RENAMED 每組的 FROM／TO ID 皆一致——每項比對都完成且一致。
- **執行方式與自我驗證**：13.B–13.E 以 scratchpad 腳本逐條照規則實作。第一次執行出現兩個腳本缺陷（Windows `cmd` 不認 `2>/dev/null` 導致 CLI 輸出讀不到、check 3 只比對標題而把 MODIFIED 誤判為已同步），修正後重跑才記錄本節；修正後的腳本對 5 個已知答案的 fixture 判定全部與預期答案一致（`v12` 違規、`u01` 無法判定、`v13` 違規＋無法判定、`v05` 違規、`p04` 通過）。這是對量尺的驗證，不是本 change 的證據。

**宣稱邊界摘要**（僅摘要，不重述規範文字；完整定義見
openspec-schemas repository 的 `openspec/specs/contract-identity/spec.md` 的 REQ-8，
<https://github.com/azuma520/openspec-schemas/blob/main/openspec/specs/contract-identity/spec.md>
——該 spec **不隨** `superpowers-bridge/` bundle 內含，單獨複製 bundle 的專案裡沒有這個檔）：check 13 是一組
決定論、機器可判的規則，由 verify agent 依 instruction 執行；它不是
harness 層強制、不可繞過的 archive-time gate——verify agent 沒跑它時，本
schema 沒有機制攔截這個疏漏。它只確立 candidate state 與本 change 在
13.C 到 13.E 範圍內的結論，**不**確立「退役的 ID 不會被重新配用」、「一個
scenario ID 不會透過 MODIFIED 全文替換或 archive 悄悄消失」、「同一個 ID
底下的語意沒有被弱化」，或「capability 改名後 ID 存活」。

本結果描述的是 commit `95e4d87` 時的主 spec 與 delta 檔；之後若任一被修改，依 13.F 本結果即過期，必須重跑。

---

## Overall Decision

- [ ] ✅ PASS — 可進入 finishing-a-development-branch 與 archive
- [x] ⚠️ PASS WITH WARNINGS — 可進入後續步驟但需注意：§5 有 1 行 ledger 紀錄與本檔尚未 commit、分支未推送（push／merge 不在目前授權內）；§6 偵測到 5 份維護者設計文件，皆為合法存留、非本 change 產出
- [ ] ❌ FAIL — 返回失敗的 artifact 修正後重跑 verify

**下一步**：

寫 retrospective（PRECHECK 會讀本檔的 Overall Decision）→ 本檔、retrospective、answer-key、ledger 與 README 新增段落一起送文件審（fallback 仍 sticky）→ 經使用者授權 commit → archive（使用者協助 `rm`）→ 併回 `main` → `main` 的 `openspec/schemas/` 重新同步到 v3。
