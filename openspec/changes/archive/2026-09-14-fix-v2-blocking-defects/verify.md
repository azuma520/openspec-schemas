# Verification Report

> 此檔案由 `openspec-verify-change` skill 在 apply 完成後產生，用以確認實作
> 與 specs / design / tasks 的一致性。失敗的檢查須返回對應 artifact 修正後
> 再重跑 verify。

**Change**: `fix-v2-blocking-defects`
**Verified at**: `2026-09-10 17:03 (local)`
**Verifier**: `verify agent (Claude Fable 5.1, main session), executing superpowers-bridge v2 verify instruction; fresh re-run after the 2026-09-10 edits (the 2026-09-08 run is superseded — tasks.md, schema.yaml, the delta spec and plan.md changed after it); skill fallback — the numbered checks were run manually and recorded here`

> **執行前提（已查證，非引述他人報告）**：`diff -r --strip-trailing-cr superpowers-bridge
> openspec/schemas/superpowers-bridge` 回空、exit 0（2026-09-10 17:0x，於 check 12 的
> plan-key 分隔符條文寫入 `schema.yaml` 並以 `cp -R superpowers-bridge/. openspec/schemas/superpowers-bridge/`
> 覆蓋同步之後量測）— dogfood 副本與來源一致，故本報告描述的是**含 2026-09-10 修正**的 checker。
> `openspec schema validate superpowers-bridge` → `✓ Schema 'superpowers-bridge' is valid`；`openspec schemas` 列出 1 筆。
>
> **本次重跑的原因（freshness）**：2026-09-08 的 verify 之後，`tasks.md`（5.1 控制紀錄補記）、
> `plan.md`（第 17 行 global constraint 引句）、`schema.yaml`（check 12 plan-key 分隔符、apply 指令
> 每 subject 措辭）、`specs/tdd-evidence-contract/spec.md`（subject 唯一性措辭、record field form
> 條款與兩個 Scenario）皆有修改。依 freshness 規則，`tasks.md` 的修改使 §2、§7 與 §8 的 checks 8–12
> 全部 STALE，故整份重跑；不只重跑受影響的節，因為其餘節的輸入（specs、commit 狀態）也變了。
>
> **本次執行的特殊性**（承 2026-09-08）：本 change 修的正是 checks 2、7、9–12 自身（check 2 為 2026-09-11 追加），被檢查的對象就是修正
> 它們的那個 change。所有判定均由本 agent 逐條從 `tasks.md` / `plan.md` / `specs/` 原文推導；checks 7–12
> 另以一支照條文字面寫成的一次性 Python 掃描做交叉比對（方法列於 §8），未沿用任何 review 報告的結論。

---

## 1. Structural Validation (`openspec validate --all --json`)

- [x] 全數 items `"valid": true`

**結果**：

```text
items: 5 — change/fix-v2-blocking-defects, spec/plan-contract, spec/repo-guidance,
           spec/tdd-claim-accuracy, spec/tdd-evidence-contract
all five: "valid": true, exit 0  (run 2026-09-10 16:5x from the worktree root)
```

無 ERROR 級 issue。四筆 `INFO` 級提示（`plan-contract` requirements[0]、`tdd-claim-accuracy`
requirements[1]、`tdd-evidence-contract` requirements[1] 與 requirements[2]：「Requirement text is
very long (>500 characters)」）不影響 `"valid": true`；`tdd-evidence-contract` requirements[1]
因本日新增 record field form 段落而更長，仍為 INFO。

| Item | Type | Issues |
|---|---|---|
| — | — | 無失敗項目 |

---

## 2. Task Completion (`tasks.md`)

- [x] 所有 task 的 checkbox 皆為 `- [x]` 或 `- [~]`（本 change 實測:15 筆全為 `x`、`[~]` 零筆）

機械掃描結果（來源 `tasks.md` 152 行 → 方法：行首非空白字元為 `- [` + 一字元 + `]` 者為 task line →
結果）：15 個 task line，checkbox marker 全為 `x`，無 `- [ ]`、無 `- [~]`。

> **條文修訂註記（2026-09-11，Codex branch review r1 的 P1）**：check 2 的措辭本日由
> 「每個 checkbox 必須是 `- [x]`」改為「必須是 `- [x]` 或 `- [~]`」，並明寫 `- [~]` 屬 check 7
> 定義的 DEFERRED TASK、不在本檢查失敗。**本節記錄的結果不受影響**：掃描結果是 15 個 task line
> 全為 `x`、`- [~]` 零筆，在修訂前後的措辭下都判 PASS，因此未重跑本節。
> `tasks.md` 與 `plan.md` 本輪皆未修改，下方 §Freshness 列的兩個重跑條件都沒有觸發。
> ⚠️ 順帶記一個缺口（不在本 change 修正範圍）：§Freshness 只涵蓋 `tasks.md` / `plan.md` 被改動的情形，
> **沒有涵蓋「check 條文本身被改動」**——本次即屬後者，靠人工判斷結果是否仍成立。
任務編號 `1.1 1.2 1.3 1.4 2.1 2.2 2.3 2.4 3.1 3.2 4.1 4.2 5.1 5.2 5.3`。
`grep -c '^- \[x\]'` → 15（PRECHECK 第 2 項 > 0）；`git log --oneline 368d586..HEAD | wc -l` → 9（PRECHECK 第 1 項 > 0）。

**未完成任務**（若有）：

| Task | 未完成原因 | 是否阻塞 archive |
|---|---|---|
| — | 無未完成任務 | — |

---

## 3. Delta Spec Sync State

對每個 `openspec/changes/fix-v2-blocking-defects/specs/` 下的 capability 目錄，與
`openspec/specs/<capability>/spec.md` 比對（方法：`git diff --stat 368d586 -- openspec/specs/<cap>/spec.md`
看主 spec 在本 branch 是否被動過，再逐 requirement / scenario 標題比對 delta 與主 spec）：

| Capability | Sync 狀態 | 備註 |
|---|---|---|
| `plan-contract` | ✗ 待 sync | 主 spec 在本 branch 未被動過（diff --stat 空）。delta 的 `Plan is a per-task execution contract` 多出兩段 SHALL（1:1 兩階段、plan.md 不得承載 task-level state）與四個 Scenario（duplicate task number / duplicate plan key / unique+equal 通過 / deferral marker 從 tasks.md 讀）。 |
| `tdd-claim-accuracy` | ✗ 待 sync | 主 spec 的兩處 stale clause 已由任務 4.1 修好並 commit（`787b14c`，本 branch 對主 spec 13 insertions / 6 deletions），但 delta 新增的兩個 Scenario（`writing-plans is no longer cited as the carrier`、`Carrier named consistently across the spec`）仍待 archive 併入 |
| `tdd-evidence-contract` | ✗ 待 sync | 主 spec 在本 branch 未被動過。delta 改寫 `Applicable tasks require RED and GREEN evidence` 本文，並含六段粗體條款（pairing unit、subject grammar、**record field form（2026-09-10 新增）**、completion evidence、boundary）與**十一個** Scenario（2026-09-10 新增 `Repeated field key in one record blocks`、`Wrapped value is not a field`）。主 spec 仍是 pre-fix 版本 |

**判讀**：三個 capability 全為「待 sync」，這是 archive 前的**正常狀態** —— delta spec 正是
`openspec archive` 要併進主 spec 的內容，本 change 刻意不手動先併（任務 4.1 明寫）。**不阻塞**，但
archive 時必須實際執行 sync，否則主 spec 會停在 pre-fix 語意。

> ⚠️ 判斷點之一（承 2026-09-08）：instruction 只要求記錄 ✓/✗/N/A 三態，**未定義 ✗ 是否阻塞**。
> 本報告判為非阻塞，理由如上。

---

## 4. Design / Specs Coherence Spot Check

抽樣比對 `design.md` 的決策是否反映在 `specs/*.md` 的 Requirements 與 Scenarios 中：

| 抽樣項 | design 描述 | specs 對應 | 差距 |
|---|---|---|---|
| D1 | check 12 的 1:1 用「先去重、再集合相等」兩階段實現，兩種失敗給不同訊息 | `plan-contract` delta：「SHALL establish it in two stages … A duplicate on either side SHALL be reported … distinctly from a missing or extra key」＋ 三個 Scenario | 無 |
| D2 | 配對單位由 task 改為 subject；同 task 內 subject 每側唯一；不用順序配對 | `tdd-evidence-contract` delta：「The pairing unit is the subject, not the task」「Subject values SHALL be unique within each side of a task — at most one RED record and at most one GREEN record per subject」（2026-09-10 由「unique within a task」改寫，消除與前句「每 subject 各一 RED 一 GREEN」的字面衝突；`plan.md:17` 引句同步）「Ordinal pairing … SHALL NOT be used」＋ Scenario「Two subjects under one task both pass」「Duplicate subject on one side blocks」 | 無 |
| D3 | subject grammar 最小可判定：恰好一個 `::`、兩側非空、不再規定路徑語法 | `tdd-evidence-contract` delta「Subject grammar」段＋ Scenario「Subject not matching the grammar blocks」「Unconventional but conforming identifier passes」 | 無 |
| D4 | check 7 改讀 `tasks.md`，其餘判定邏輯一字不動；不採納「deferred 連回 plan 條目」 | `plan-contract` delta：「plan.md SHALL NOT carry task-level state markers … Any deterministic check concerning task state SHALL therefore read tasks.md」＋ Scenario「Deferral marker is read from tasks.md」 | 無 |
| check 9 的 field cardinality / one-line field（design §Risks「修 checker 的同時把 checker 改壞」mitigation 所涵蓋的檢查行為） | schema check 9「FIELD CARDINALITY」「A FIELD IS EXACTLY ONE LINE」 | `tdd-evidence-contract` delta「Record field form」段（2026-09-10 新增）＋ Scenario「Repeated field key in one record blocks」「Wrapped value is not a field」 | 無（2026-09-10 前為漂移：schema 有、canonical 無） |
| check 12 plan-key 分隔符（2026-09-10 新增於 schema check 12 與 `plan` 指令） | `plan` 指令：數字後接 whitespace 或行尾，`## 1x` / `## 1.1a` 不是 entry | `plan-contract` delta 的「one-to-one … deterministic verify check SHALL establish it in two stages」未提 key 的字元邊界 | **輕微漂移**：spec 條文說 key 對應而未定義 key 的 token 邊界；schema 與 plan 指令已定義。記為觀察，非阻塞（spec 對 grammar 的沉默不與 schema 衝突；是否把邊界寫進 canonical spec 交 archive 前決定） |
| D5（schema major 不再 bump） | 版本決策，附「v2 未發版」前提 | 無對應 spec requirement | 見下方漂移警告 |
| D6（雙語 README 同步） | 連動面決策 | 無對應 spec requirement | 見下方漂移警告 |
| Non-Goal 2（不驗 evidence truth） | 不驗 evidence truth | `tdd-evidence-contract` delta「Boundary of what these checks decide」段 | 無 |

**漂移警告**（非阻塞）：

- D5 與 D6 在 specs 中沒有對應 requirement。兩者是**流程 / 發版決策**，不是 capability 行為；記為觀察。
  D5 的前提已於本 artifact 產出前重驗（見 §8 的 5.3 列）。
- check 12 plan-key 分隔符：schema 與 `plan` 指令已寫明，`plan-contract` delta 未寫（上表第 6 列）。
- `superpowers-bridge/templates/plan.md` 的改動（entry-key 說明兩階段）仍是任務 3.1 文字未點名的連動面（承 2026-09-08）。

---

## 5. Implementation Signal

- [ ] Worktree 內無未 staged 的檔案 — **未滿足**
- [ ] 所有相關 commit 已推送 — **未滿足（刻意）**

**Commit 範圍**：`368d586..b07d571`（本 change 的 9 個 commit：`a78d45d` 開 change → `ad92839`、`6c4605e`
work-map → `3eba33d` tasks+plan → `22c15cf` fixtures f8–f13 → `cffe99a` 五條 check → `787b14c` 連動面 →
`e38e817` code-plane findings + verify → `b07d571` retrospective + follow-up 登記）。`origin/main` = `5aa19bf`，
本 branch 未推送。

**未 commit 的工作樹改動**（`git status --short`，2026-09-10 17:0x）：

| 檔案 | 狀態 | 對應 |
|---|---|---|
| `.gitattributes` | M | branch review r1/r2 finding：bridge 目錄逐副檔名 `eol=lf` |
| `superpowers-bridge/schema.yaml` | MM（staged：apply 指令每 subject 措辭；unstaged：check 12 plan-key 分隔符、`plan` 指令同句） | r1 finding + Codex r1 P1 |
| `superpowers-bridge/templates/{design,plan,spec}.md` | M（staged，`git add --renormalize` 的純 EOL 差異） | r2 finding |
| `openspec/changes/fix-v2-blocking-defects/{proposal,retrospective,tasks,plan,verify}.md`、`specs/tdd-evidence-contract/spec.md` | M | r2 / Codex r1 findings 的宣告、措辭、條款與本檔 |
| `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/`（3 檔） | 未追蹤 | r1 finding：review 報告永久保存；`retrospective.md` 已引用，**commit 時必須一併納入** |
| `文檔/handoff/session-handoff-2026090{3,4,7,8}.md` | 未追蹤 | 非本 change 交付物，慣例不進版控 |

`git diff --check 368d586` → 無 whitespace 錯誤（exit 0；只印 EOL 轉換 warning）。
`git ls-files --eol superpowers-bridge` → 14 個 blob 全部 `i/lf`（10 個工作樹 `w/crlf`、4 個 `w/lf`）。

**判讀**：實作證據存在且完整（commit ＋ 工作樹合計覆蓋全部 15 個任務與三輪 review 修正），但 instruction
第 5 條字面要求的「no unstaged files」不成立。未 commit / 未推送是使用者裁定（外部 code review ✅ 前凍結）。
記為 **warning，不阻塞本 artifact**；archive 前應把工作樹改動收成 commit。

> ⚠️ 判斷點之二（承 2026-09-08）：instruction 第 5 條未說明未 commit 時是 FAIL 還是 warning。本報告判為 warning。

---

## 6. Front-Door Routing Leak Detector（warning,非阻塞）

設計產出不應落在 `docs/superpowers/specs/`(brainstorm artifact 的
output redirection 會把它導到 `openspec/changes/<name>/brainstorm.md`)。

偵測:

```bash
ls docs/superpowers/specs/*.md 2>/dev/null
```

- [x] 無檔案,或存在的檔案是 schema 安裝前的合法存留

**WARNING — Front-door routing leak**：`docs/superpowers/specs/` 下存在 4 個 `.md`（`ls | wc -l` → 4，與 2026-09-08 相同）。

| 檔案 | 內容是否已 captured 進 change | 建議動作 |
|---|---|---|
| `2026-05-02-openspec-schemas-monorepo-design.md` | N/A — schema 安裝前的 repo 設計 spec，`CLAUDE.md`「相關連結」引用 | 保留 |
| `2026-08-27-bridge-guarantee-architecture-direction.md` | N/A — Bridge Guarantee 方向文件，`CLAUDE.md` 動工門檻節以它為準 | 保留 |
| `2026-08-28-concept-poc-traceability-gate-design.md` | N/A — 概念 PoC 設計 | 保留 |
| `2026-09-01-bridge-guarantee-formal-design.md` | N/A — 正式設計核可文件 | 保留 |

**判讀**：四份皆為 repo 自身的方向 / 治理文件，屬 instruction 明列的「legitimate non-schema use … predating
schema install」。**不阻塞，不建議刪除。**

> 不會擋住 archive。新的 schema-installed cycle 產生的洩漏,應搬進
> `openspec/changes/<name>/brainstorm.md` 或 `design.md` 後刪原檔。

---

## 7. Deferred Dogfood vs Automated-Test Equivalence

DEFERRED TASK 的定義：`tasks.md` 裡首個非空白字元為 `- [~]` 的任務行才算。

**掃描結果：`tasks.md` 存在，15 個 task line 的 checkbox marker 全為 `x`，沒有任何 `- [~]` 任務行。**
因此本節依模板規則**留空即 PASS**。

| Deferred task (tasks.md) | Equivalent automated test | Coverage assessment | 真正 gap? |
|---|---|---|---|
| — | — | — | — |

> ⚠️ 明確排除的情形（承 2026-09-08）：`tasks.md` 第 48 行（任務 1.3）與第 109 行（2.3 的 `failure:`
> 欄位）**文字中出現 `[~]`**，描述的是 fixture `f13`。依 check 7 定義，標題、內文或紀錄欄位裡的 `[~]`
> 不是 deferral marker，兩處不使本檢查 fire。
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

**方法（來源 → 方法 → 結果）**：來源 `tasks.md`（152 行）與 `plan.md`（135 行，2026-09-10 17:0x 工作樹）→
逐行人讀，並以一支照 schema 條文字面寫成的一次性 Python 掃描交叉比對（TASK LINE / BELONGS TO / 空行透明 /
任意深縮排 / FIELD 為 `- <key>: <value>` 單行 / 每 record 每 key 至多一次 / subject `::` 恰一且兩側非空 /
outcome token 規則 / check 11 兩階段 / check 12 兩階段含 `]` 後至少一個空白與 `##` 層級）→ 兩種方法對 15 個
task、12 筆 record、15+15 個 key 得到相同結果。

**Per-task results** (one row per `- [ ]` / `- [x]` / `- [~]` task line in `tasks.md`):

| Task | Annotation (8) | Records, fields + subject grammar (9) | Outcome markers (10) | Subject pairing (11) | Review judgement (R1–R4) |
|---|---|---|---|---|---|
| 1.1 | ✓ `TDD: n/a — the fixtures are the test material for 2.1 …` | N/A (not applicable) | N/A | N/A | ✓ R3 理由成立（fixture 是 2.1 的測試材料，正確性由 2.1 的 RED/GREEN 展示）；R4 無紀錄 |
| 1.2 | ✓ `TDD: n/a — test material for 2.2, same terms as 1.1 …` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 1.3 | ✓ `TDD: n/a — test material for 2.3 …` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 1.4 | ✓ `TDD: n/a — prose/doc-only; verified by reading the table …` | N/A | N/A | N/A | ✓ R3 成立（fixtures 目錄 13 個子目錄 ↔ README 表 13 列，`ls` 對表逐一比對）；R4 無紀錄 |
| 2.1 | ✓ `TDD: applicable` | ✓ 2 subjects（f8、f9），4 筆紀錄；RED 均含 `subject`/`outcome`/`failure`（＋ `invocation`），GREEN 均含 `subject`/`outcome`（＋ `invocation`）；每筆紀錄無重複 key；`::` grammar 全通過 | ✓ RED `FAIL`/`FAIL`，GREEN `PASS`/`PASS` | ✓ 兩側各自無重複；集合雙向相等 | ✓ R1 兩筆 RED 皆為行為性失敗（預期 BLOCK 點名重複 key；實際 PASS，集合吃掉重複）；R2 subject 指向 f8/f9 與期待判定，對應任務交付的行為 |
| 2.2 | ✓ `TDD: applicable` | ✓ 3 subjects（f10、f11、f12），6 筆紀錄；必要欄位全備且非空；每筆紀錄無重複 key；`::` grammar 全通過 | ✓ RED `FAIL`/`FAIL`/`INDETERMINATE`（皆為單一大寫 token 且非 `PASS`），GREEN 三筆皆 `PASS` | ✓ 兩側各自無重複；集合雙向相等 | ✓ R1：f12 的 `INDETERMINATE` 屬 instruction 明文承認的情形（受測對象是靠閱讀執行的規則，RED 記的是規則本身無法判定，可判定性未被滿足）——**此讀法已於 proposal §Impact、`tdd-evidence-contract` delta 與 retrospective §3 宣告**（2026-09-10 補宣告），且 `INDETERMINATE` 只在 RED 側、不等於 `PASS`、不替代 GREEN；R2 三個 subject 分別對應 grammar / 每側唯一 / 正向對照三個交付行為 |
| 2.3 | ✓ `TDD: applicable` | ✓ 1 subject（f13），2 筆紀錄；必要欄位全備且非空；無重複 key；`::` grammar 通過 | ✓ RED `FAIL`，GREEN `PASS` | ✓ 無重複；集合相等 | ✓ R1 RED 是「check 7 應找到一個 deferred 任務、實際回報 no deferred tasks」，行為性失敗；R2 subject 對應 carrier 遷移 |
| 2.4 | ✓ `TDD: n/a — instruction prose; the control is the residual-wording grep …` | N/A | N/A | N/A | ✓ R3 成立（本 agent 複跑：`grep -n "a RED record and a GREEN record" superpowers-bridge/schema.yaml` → 0 hit；apply 指令 `:1177-1180` 於 2026-09-10 已改為每 subject 措辭，該處原為 YAML 換行切開、單行 grep 掃不到的殘留，此次以多行讀取確認清除）；R4 無紀錄 |
| 3.1 | ✓ `TDD: n/a — template prose; verified by diffing each template's check list …` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄（`Control result` / `Render acceptance` 兩行不是 `- RED:` / `- GREEN:` 紀錄） |
| 3.2 | ✓ `TDD: n/a — prose/doc-only; verified by reading both READMEs …` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 4.1 | ✓ `TDD: n/a — prose/doc-only; the control is a grep for both stale phrasings …` | N/A | N/A | N/A | ✓ R3 成立（主 spec 於 `787b14c` 修正，本 branch diff 13/6）；R4 無紀錄 |
| 4.2 | ✓ `TDD: n/a — prose/doc-only; verified by reading version-check.yml's grep line …` | N/A | N/A | N/A | ✓ R3 成立；R4 無紀錄 |
| 5.1 | ✓ `TDD: n/a — configuration / copy step …` | N/A | N/A | N/A | ✓ R3 成立（本 agent 複驗：`diff -r --strip-trailing-cr superpowers-bridge openspec/schemas/superpowers-bridge` 回空、exit 0，於 2026-09-10 的 schema 修改**之後**量測；控制條件為 `diff -r` 不變量）；R4 無紀錄 |
| 5.2 | ✓ `TDD: n/a — append-only record entry …` | N/A | N/A | N/A | ✓ R3 成立（本 agent 複跑 `git diff --numstat --ignore-cr-at-eol 368d586 -- openspec/changes/archive/2026-09-04-loosen-plan/errata.md` → `33 0`；刪除數 0 的不變量成立，紀錄本身已改寫為不變量陳述、2026-09-08 的「22 vs 33」漂移已消除）；R4 無紀錄 |
| 5.3 | ✓ `TDD: n/a — a precondition check on repository state …` | N/A | N/A | N/A | ✓ R3 成立（本 agent 於本檔產出前重驗：`git tag -l` 空；`git ls-remote --tags origin` 空、exit 0；`git ls-remote origin main` → `5aa19bf…`，與本地 `origin/main` 相同；D5 前提仍成立）；R4 無紀錄 |

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

補充：`tasks.md` 15 行 task line **全部**在 `]` 後有至少一個空白字元、其後首個 token 皆符合
`\d+(\.\d+)*` —— 無「task line carrying no task number」。`plan.md` 存在（135 行），可收集到 entry key；
15 個 `##` entry heading 的 leading token 之後**皆接空白**（2026-09-10 新增的分隔符規則下全部合格，無
`## 1x` 型 heading）；`# fix-v2-blocking-defects — Plan Contract` 與 `## Self-review` 不以數字開頭，非 entry；
檔內無 `###` 層級的數字子標題。

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

**本次執行中，文字未替執行者決定、由本 agent 自行判定之處**：

1. **checks 7–12 的行掃描未排除 HTML comment 與 fenced code block**（承 2026-09-08 note 1）。本 change 的
   `tasks.md` 開頭 40 行 HTML comment 內，本 agent 以掃描確認**沒有**行首為 `- [` 或 `#` 的行（0 hit），
   `plan.md` 亦無圍籬區塊；此模糊處本次未觸發。已由使用者裁定為 follow-up（work-map
   `task-20260908-author-surface-gate-alignment`），2026-09-10 Codex branch review 再次指出、記 `[USER_SKIPPED]`。
2. **check 3 的 ✗ 是否阻塞、check 5 的未 commit 是否為 FAIL**，見 §3 與 §5 的 ⚠️ 標註。

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
- [x] ⚠️ PASS WITH WARNINGS — 可進入後續步驟但需注意：見下列五點
- [ ] ❌ FAIL — 返回失敗的 artifact 修正後重跑 verify

**警告（皆非本 artifact 的阻塞項，但 archive 前必須處理或已被使用者裁定）**：

1. **code plane 的外部獨立審尚未關閉。** 2026-09-10 Codex（`gpt-5.6-sol`）正式 branch review r1 判
   `⛔ Blocked`（4 P1 + 5 P2）；使用者裁定：4 條對應既有延後裁定者記 `[USER_SKIPPED]`，其餘 5 條修正（本檔
   即其中「fresh rerun verify」一項），修正後送 Codex 同 thread 複審。**本 change 在 Codex ✅ 前不進 archive。**
   fallback 判定（2026-09-10 r1/r2）是暫時性保證、不是已完成的外部審。
2. **工作樹尚有未 commit 檔案**（§5：7 個修改、3 個 staged EOL、1 個未追蹤目錄）。archive 前應收成一個
   commit，且**必須包含** `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/`。
3. **三個 capability 的 delta spec 尚未併入主 spec**（§3）。archive 時完成 sync。
4. **`docs/superpowers/specs/` 存在 4 個 `.md`**（§6），合法存留，不建議刪除。
5. **check 12 plan-key 分隔符規則沒有 fixture**（§4 第 6 列；retrospective §5「四條會擋但無 fixture 的規則」）。
   同族三條已由使用者裁定為 follow-up；此條同批。

**下一步**：

1. 送 Codex 同 thread 複審（附 `[USER_SKIPPED]` 四條與更正後的 baseline）。
2. Codex ✅ 後：把工作樹改動收成 commit（警告 2）→ retrospective 補記 → archive（完成 delta sync，警告 3）→ 併回 main → push。
3. ⚠️ **Freshness**：步驟 2 若再動到 `tasks.md`，§2、§7 與 §8 的 checks 8–12 即為 STALE，必須重跑並更新本檔；
   只動 `plan.md` 則僅 check 12 需重跑。
