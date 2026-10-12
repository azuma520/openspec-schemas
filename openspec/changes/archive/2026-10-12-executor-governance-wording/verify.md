# Verification Report

> 此檔案由 `openspec-verify-change` skill 在 apply 完成後產生，用以確認實作
> 與 specs / design / tasks 的一致性。失敗的檢查須返回對應 artifact 修正後
> 再重跑 verify。

**Change**: `executor-governance-wording`
**Verified at**: `2026-10-12 12:07`（+0800；HEAD `ba68235`，工作樹乾淨）
**Verifier**: 獨立 verify subagent（model Opus 5.5），本 change 的**備援載體**——第一個被派出的 verify agent（model Fable）因用量上限中途終止，未寫出 verify.md；它留在 scratchpad 的中間檔（`checks8to12.py`、`residue.py`、`preview13-*`、`diff-*.txt` 等）**未被沿用**，本報告的每一項都由本 agent 重跑取得。

**驗證者獨立性（照實說）**：本 agent 不是實作者，但與實作者**由同一個 session 派出**，且與實作者是**同一模型家族**。這是「另一個 context 重跑檢查」，不是外部或跨模型的獨立審查；下面的結論應依此打折看待。

**本次執行的流程**：PRECHECK → invoke `openspec-verify-change` skill（completeness / correctness / coherence 三維）→ schema 的 check 1–13 與 review judgement R1–R4 → 實作者筆記（tasks 6.2–6.4）逐項重跑比對。

### PRECHECK — implementation evidence

| 指令 | 結果 |
|---|---|
| `git log --oneline $(git merge-base HEAD origin/main)..HEAD \| wc -l` | **4**（merge-base `b40e059`）→ > 0，通過 |
| `grep -c '^- \[x\]' openspec/changes/executor-governance-wording/tasks.md` | **20**（task 行共 20 條）→ > 0，通過 |

**commit 範圍的組成**（數字 4 不等於「4 個實作 commit」）：

| Commit | 內容 | 是否本 change 的實作 |
|---|---|---|
| `213a6fb` | 開 change、寫 brainstorm（`.openspec.yaml`、`brainstorm.md`） | 否（規劃 artifact） |
| `80fd84b` | handoff 與工作地圖紀錄（`文檔/handoff/…`、`workflow-harness/work-map.jsonl`） | 否 |
| **`2551ea0`** | **本 change 的實作**：proposal / design / specs / tasks / plan，加上 `schema.yaml`、`templates/retrospective.md`、`VERSION`、兩份 bridge README、`version-check.yml`、`CLAUDE.md`、頂層 README 中英、roadmap 中英（17 檔，+852 / −52） | **是——唯一的實作 commit** |
| `ba68235` | backlog 週檢紀錄（`backlog.md`、`backlog-crosscheck-shadow.json`） | 否 |

### 執行方式的偏離（必須記錄，非等效）

本 change 的 apply **沒有跑 `superpowers:subagent-driven-development`**。這是 brainstorm Q4 的具名、經使用者核可、**只限本 change** 的例外（`brainstorm.md` Q4；`plan.md` 開頭的 Execution 段）。它**不是**受支援的執行模式。

- **沒取得的保障**：SDD 的逐 task 獨立審查（執行過程中的獨立審查）。這次的實作是在主 session 一次完成、單一 commit `2551ea0`，執行過程中沒有任何逐 task 的獨立審查點。
- **替代做法**：fallback reviewer（model Fable）做了外部審查——proposal / design / specs 的文件審查、tasks / plan 的文件審查、task 1.5 的文件審查、完整實作的文件審查，以及 `.github/workflows/version-check.yml` 的 code review，皆以 ✅ 結束（此為派工方提供的事實；本 agent **未**重讀那些審查報告）。加上本 verify。
- **不等效**：上述替代審查都是**事後**對產出物的審查，不是執行過程中逐 task 的審查；不得把它們寫成等同 SDD，也不得寫成本 change 符合 bridge 的執行契約。這個偏離要由 retrospective 依本 change 新寫的 REQ-4 規則記錄（含前例次數與位置：8/31 `fix-tdd-transitive-claim`、10/06 `fix-executing-plans-rationale`，本次為第三例，依 design Risks 段應列 §6 Promote candidate）。

---

## 1. Structural Validation (`openspec validate --all --json`)

- [x] 全數 items `"valid": true`

**結果**：

```text
openspec 1.3.1（本機 `openspec --version`）
openspec validate --all --json → exit 0
totals: items 7, passed 7, failed 0
  change: 1/1  (executor-governance-wording)
  spec:   6/6  (contract-identity, plan-contract, release-versioning,
                repo-guidance, tdd-claim-accuracy, tdd-evidence-contract)

openspec validate executor-governance-wording → "Change 'executor-governance-wording' is valid"

# task 6.1 / CI 等價驗證
diff -rq superpowers-bridge openspec/schemas/superpowers-bridge → 無輸出（exit 0，dogfood 副本與來源一致）
openspec schema validate superpowers-bridge（repo 內 dogfood）→ ✓ Schema 'superpowers-bridge' is valid
全新 scratch 專案（cp -R superpowers-bridge → <scratch>/openspec/schemas/）:
  openspec schema validate superpowers-bridge → ✓ valid, exit 0
  openspec schemas → 列出 "superpowers-bridge (project)"，description 為改寫後的新文字
```

若有失敗項目，列出 id + issues：

| Item | Type | Issues |
|---|---|---|
| — | — | — |

> 提醒（repo CLAUDE.md 已載明）：schema validate 只驗結構，`instruction:` 內的 prompt 文字改壞了也是綠的。本 change 幾乎全是 prompt / 文件文字，所以本節的「綠」只說明結構沒壞，不說明文字正確；文字正確性見 §4 與下方「實作對照」。

---

## 2. Task Completion (`tasks.md`)

- [x] 所有 task 的 checkbox 皆為 `- [x]` 或 `- [~]`
      （20 條 task 行全部 `- [x]`；無 `- [ ]`、無 `- [~]`）

**未完成任務**（若有）：

| Task | 未完成原因 | 是否阻塞 archive |
|---|---|---|
| — | — | — |

> tasks.md 末尾的 HTML 註解列出「不在本清單內」的發版步驟（archive 後打 `v5.0.0` annotated tag、經授權 push、確認遠端 `refs/tags/v5.0.0^{}`、roadmap 補 Released 標記）。依 `release-versioning` REQ-1 它掛在工作地圖紀錄，不是 task 行，本檢查不計入；但它**尚未發生**（本機與 `origin` 目前只有 `v4.0.0`，剝開後 `d2a350c`；無 `v5*` tag）。

---

## 3. Delta Spec Sync State

對每個 `openspec/changes/<name>/specs/` 下的 capability 目錄，與
`openspec/specs/<capability>/spec.md` 比對：

| Capability | Sync 狀態 | 備註 |
|---|---|---|
| `tdd-claim-accuracy` | ✗ Needs sync | delta MODIFIED REQ-3、REQ-4。main spec 仍是舊文字：REQ-3 只有 S1–S3（delta 多 S4）、REQ-4 只有 S1（delta 多 S2、S3），區塊全文不相等 |
| `release-versioning` | ✗ Needs sync | delta MODIFIED REQ-3（改寫 S2）。main spec 的 REQ-3-S2 仍寫「reads the v4 row」，區塊全文不相等 |

> 兩者都是 archive 前的正常狀態（尚未 archive）。archive preview（§9）已確認 `openspec archive` 會把三個 MODIFIED 合入（`~ 1 modified` / `~ 2 modified`）。在 archive 之前，main spec `release-versioning` REQ-3-S2 與 `version-check.yml` 讀 v5 列的現況互相矛盾——這是預期中的過渡狀態，archive 後消失。

---

## 4. Design / Specs Coherence Spot Check

抽樣比對 `design.md` 的決策是否反映在 `specs/*.md` 的 Requirements 與
Scenarios 中：

| 抽樣項 | design 描述 | specs 對應 | 差距 |
|---|---|---|---|
| D1 能力 + 限制 + 引用 log | 設計說明只寫所需能力、目前限制、引用 Re-verification log | `tdd-claim-accuracy` REQ-3 第 1–2 段、S4 | 一致 |
| D2 log 新段 | log 末端新增一段，寫無逐 task 審查、最後一次審查、無 subagent 時作者自審、載入 TDD；舊列不改 | REQ-3 第 2 段（log SHALL state …；Dated entries stay）、S3 | 一致 |
| D3 apply 三種情境 + 1.5 Step 0 句修正 | apply 指令寫明三種情境；Step 0 不再指向不存在的 manual fallback | REQ-3 只管「排除理由」、REQ-4 只管 retrospective 紀錄 | **無對應 requirement**（見下方漂移警告 1） |
| D4 retrospective 三題答法、`one-off` 字面對齊、裁定只限本 change、前例次數 | 不加欄位、不加選項 | `tdd-claim-accuracy` REQ-4 第 2–5 段、S2、S3 | 一致 |
| D5 CLAUDE.md 紅旗 | 能力導向、引用 log、刪版本沿革與「之後要改寫」 | REQ-3（CLAUDE.md red-flag list SHALL refer to the log，不必重述事實） | 一致 |
| D8 schema major 5、version-check 列鍵 | `version: 5`、`VERSION 5.0.0`、grep 列鍵 `v5` | `release-versioning` REQ-3-S2（讀的列 = 發布中的 schema major，不宣稱自動找最新列） | 一致 |

**實作對照**（skill 的 correctness 維度；逐處讀 `git show 2551ea0` 與現檔）：

- REQ-3 點名的每個設計面都同時寫了「能力」與「目前限制（缺能力 Step 0 STOP、不改用 executing-plans）」並引用 log：`schema.yaml` description（第 9–14 行）、apply 第 2 步（約第 1829–1846 行）、bridge README 中英的 No `executing-plans` fallback 提示框、設計觸點 #4、Fallback strategy 的 `apply` 列、`CLAUDE.md` 紅旗。這些位置都已不含逐版本的機制描述（`git grep` 見 §「實作者筆記重跑」6.2）。
- Re-verification log 新段 `#### executing-plans review structure`（中文 `#### executing-plans 審查結構`）在 `### Re-verification log` 下一層、標題無日期與版本號；內容含無逐 task 審查、最後一次審整條分支（有 subagent 派新審查者 / 無則作者自審）、載入 `test-driven-development`、v6.4.1 固定標籤連結、v6.4.2 spike 比對、「僅文件，基準不移動」。既有帶日期列與 follow-up 段在 diff 中無變動。
- README 中英頁內錨點連結全數可解析（以 GitHub 式 slug 規則對兩份 README 全部 `](#…)` 計算：en 13 個、zh-TW 12 個，0 個解析不到；含 `#executing-plans-review-structure`、`#executing-plans-審查結構`、`#migrating-v4--v5`、`#從-v4-遷移到-v5`、`#fallback-strategy`、`#降級策略`）。
- 模板 `one-off` 選項字面已是 `one-off — schema boundary case`，選項仍為 5 個，與 `schema.yaml` 字面一致；`no prevention possible` 全 repo 現行文件 0 筆。
- 頂層 README 中英各只改第 11 行 Status 欄；roadmap 中英新增 `## v5` 段，標題未標 Released / 已釋出。

**漂移警告**（非阻塞）：

1. **D3（apply 三種情境）與 task 1.5（Step 0 句修正）沒有 spec requirement 承載。** 第三種情境「經裁定略過 SDD 是例外、不是支援模式、做不到必要保障就停止」以及 Step 0「沒有內部 manual fallback、agent 不得自行切換 schema」是規範性的 instruction 文字，但 `tdd-claim-accuracy` REQ-3（只管排除理由）與 REQ-4（只管 retrospective 紀錄）都沒有涵蓋。後果：日後有人改掉這段 apply 文字，沒有任何 spec 條文可以對照指出它退化。是否補一條 requirement 屬使用者判斷，本 verify 不代決。
2. **zh-TW log 新段的反向連結比 en 少一個**：en 版連到觸點提示框、設計觸點 #4、fallback strategy 三處；zh-TW 版的「設計觸點 #4」是純文字、沒有連結（其他兩處有）。語意一致，屬連結層面的小差異（task 3.4 的驗收是「語意一致」，不構成不符）。

---

## 5. Implementation Signal

- [x] Worktree 內無未 staged 的檔案（`git status --short` 無輸出；跑完 precommit runner 後再查一次仍無輸出）
- [ ] 所有相關 commit 已推送——**未推送**：`main...origin/main [ahead 4]`。push 屬受管制操作，需使用者當次授權；task 4.2 註明的 push 後 `workflow_dispatch` 實跑也因此尚未發生。

**Commit 範圍**（若知道）：`b40e059..ba68235`（4 個 commit）；**本 change 的實作只在 `2551ea0`**，其餘三個不是實作（見 PRECHECK 表）。

**Precommit（照實記錄，不是通過）**：本 agent 重跑 `node .claude/scripts/precommit-runner.js`，結果與實作者回報相同：

```text
- ⏭️ comment_blocks (skipped: checker missing)
- ⏭️ lint_fix (skipped: script missing)
- ⏭️ build (skipped: script missing)
- ⏭️ test_unit (skipped: script missing)
## Overall: ⚠️ NO CHECKS RUN (no runnable scripts — configure lint/build/test or run ecosystem checks)
```

- 這是**沒有執行任何檢查**，不是 PASS（runner 找不到它認得的 lint / build / test 設定；backlog 已知項，第 5 例）。
- **本 verify 實際跑過的替代驗證**：`openspec validate --all --json`、`openspec validate <change>`、dogfood 與全新 scratch 專案兩處的 `openspec schema validate` + `openspec schemas`、`diff -rq` 副本一致性、`version-check.yml` 該 step 原樣取出實跑（§「實作者筆記重跑」6.4）、README 錨點解析、`git grep` 殘留搜尋、check 8–13 的程式化判讀與 archive preview。
- **剩下的限制**：沒有任何 lint / 格式 / 連結檢查器跑過 Markdown 與 YAML 文字本身（例如 `check-doc-links.js` 存在但未被 runner 接上，本 verify 也未另跑它）；prompt 文字的正確性只有人讀與上述 fallback reviewer 的文件審查承擔；`version-check.yml` 在 GitHub Actions 上的實際執行要等 push 後才有。

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
| `2026-05-02-openspec-schemas-monorepo-design.md`（`3255710`） | 不屬本 change | 不動——維護者的設計文件 |
| `2026-08-27-bridge-guarantee-architecture-direction.md`（`b1abd82`） | 不屬本 change | 不動——repo CLAUDE.md 指定的方向文件 |
| `2026-08-28-concept-poc-traceability-gate-design.md`（`7f80084`） | 不屬本 change | 不動 |
| `2026-09-01-bridge-guarantee-formal-design.md`（`f80fc7b`） | 不屬本 change（本 change 引用其 §5，且 proposal 明列不改它） | 不動 |
| `2026-09-23-formal-design-revision-map.md`（`8002fa0`） | 不屬本 change | 不動 |

> 5 個檔案存在，**WARNING 照規定列出**。`git diff --name-only b40e059..HEAD -- docs/superpowers/specs` 無輸出：本 change 的 commit 範圍沒有新增或修改這個目錄的任何檔案，這些都是 repo CLAUDE.md「結構約定」所列、維護者開發本 repo 用的 superpowers 產出，不是本 change 的前門洩漏。不會擋住 archive。

---

## 7. Deferred Dogfood vs Automated-Test Equivalence

對 **tasks.md** 中標 `[~]` deferred 的手動 dogfood / smoke 任務,逐項列出
等價的自動化測試覆蓋。

| Deferred task (tasks.md) | Equivalent automated test | Coverage assessment | 真正 gap? |
|---|---|---|---|
| — | — | — | — |

> tasks.md 存在，共 20 條 task 行，**沒有任何 `- [~]` task 行**（逐行比對首個非空白字元）→ 本節空白即 PASS。
> 附記（不屬本檢查）：task 4.2 文字裡的「push 後另以 `workflow_dispatch` 跑一次，不屬本任務完成條件」不是 `[~]` 標記，本檢查不讀它；它是 §5 記錄的未推送後續動作。

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

判讀方式：以腳本依 instruction 的 TASK LINE / BELONGS TO / 空行透明規則逐行取出每條 task 的所屬行，計算 `- TDD:` 行數與是否符合兩種格式（分隔符限 `—` `–` `-` `--`、reason trim 後非空），並計 `- RED:` / `- GREEN:` 行數。20 條皆為恰好一條、格式正確的 `- TDD: n/a — <reason>`（分隔符為 em dash），RED / GREEN 皆 0。

| Task | Annotation (8) | Records, fields + subject grammar (9) | Outcome markers (10) | Subject pairing (11) | Review judgement (R1–R4) |
|---|---|---|---|---|---|
| 1.1 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立（YAML `description` 文字，CLI 只顯示） |
| 1.2 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立（instruction 文字，validate 不讀 prompt） |
| 1.3 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立 |
| 1.4 | ✓ `TDD: n/a — configuration…` | N/A | N/A | N/A | ✓ R3 成立（版本識別值；validate / schemas 已重跑通過） |
| 1.5 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立 |
| 2.1 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立 |
| 3.1 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立 |
| 3.2 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立 |
| 3.3 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立（表格形狀由 4.2 / 6.4 的實跑承擔） |
| 3.4 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立 |
| 4.1 | ✓ `TDD: n/a — configuration…` | N/A | N/A | N/A | ✓ R3 成立 |
| 4.2 | ✓ `TDD: n/a — configuration…` | N/A | N/A | N/A | ✓ R3 成立，附註：改的是 CI workflow 的 shell step（只換一個字面列鍵 `v4`→`v5`），算 configuration 合理；但它宣稱的「本機實跑確認」**分辨不出列鍵對錯**（見 6.4 重跑的變異測試），列鍵正確性實際靠讀檔確認 |
| 4.3 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立 |
| 4.4 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立 |
| 5.1 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立 |
| 5.2 | ✓ `TDD: n/a — prose-only…` | N/A | N/A | N/A | ✓ R3 成立 |
| 6.1 | ✓ `TDD: n/a — configuration / 查驗…` | N/A | N/A | N/A | ✓ R3 成立（查驗，無新行為） |
| 6.2 | ✓ `TDD: n/a — 查驗…` | N/A | N/A | N/A | ✓ R3 成立 |
| 6.3 | ✓ `TDD: n/a — 查驗…` | N/A | N/A | N/A | ✓ R3 成立 |
| 6.4 | ✓ `TDD: n/a — 查驗…` | N/A | N/A | N/A | ✓ R3 成立 |

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

R1、R2：沒有 `applicable` 任務，不適用。R4：20 條 `n/a` 任務都沒有 RED / GREEN 紀錄，無 finding。

**Check 12, stage one — duplicate keys per side** (each side examined independently;
a repeated key BLOCKs on its own, whatever the other side holds):

| Side | Repeated keys (name each) | Verdict |
|---|---|---|
| `tasks.md` task numbers | — | ✓ |
| `plan.md` entry keys | — | ✓ |

**Check 12, stage two — set equality in both directions** (both differences must be empty):

| `tasks.md` task numbers | `plan.md` entry keys | Only in tasks (no entry) | Only in plan (no task) | Verdict |
|---|---|---|---|---|
| `{1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 6.1, 6.2, 6.3, 6.4}` | `{1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 6.1, 6.2, 6.3, 6.4}`（全部為 canonical `## Task <n> — …` 形式；plan.md 無 column-0 backtick fence） | — | — | ✓ |

> 每條 task 行的 `]` 後都有空白、首 token 都符合 `\d+(\.\d+)*`；plan.md 存在且收得到 20 個 entry key；plan.md 沒有任何非條目的 `##` 標題（標題列是單一 `#`），也沒有 backtick fence。

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

---

## 9. Identity Integrity — Check 13

Reports the verify instruction's check 13 (Requirement / Scenario heading identity). A BLOCK
here means the change is not verified for archive.

Check title, copied from the schema — do not paraphrase:

13. **Identity integrity** (deterministic in what it decides, agent-executed like checks 8-12; BLOCKs are of two kinds)

**Verdict**:

- [x] ✓ PASS — preview 成功，13.C／13.D 沒有任何 finding，13.E 每一項比對都完成且一致
- [ ] ⛔ BLOCK — 至少一項 finding（見下方兩表）

**13.B archive preview**：把 repo 整個 `openspec/` 複製到 repo 外、全新的 scratch 目錄（session scratchpad 下 `v2-preview13/`），在該目錄跑 `openspec archive executor-governance-wording -y`（無其他旗標）。三個成功條件皆成立：exit code `0`；`openspec/changes/executor-governance-wording/` 已不存在；`openspec/changes/archive/2026-10-12-executor-governance-wording/` 存在。輸出：`release-versioning: ~ 1 modified`、`tdd-claim-accuracy: ~ 2 modified`、`Totals: + 0, ~ 3, - 0, → 0`。repo 自己的 `openspec/` 未被修改（`git status` 乾淨）。check 3 兩個 capability 都記為 Needs sync，所以沒有 SYNCED CAPABILITY 的不可判定情形。

**13.C candidate state**（preview 產出的全部 6 個 main spec）：每個 requirement heading 都有合法 ID、每個 scenario heading 都符合 `<REQ-ID>-S<m>` 且 REQ-ID 等於所屬區塊；同檔無重複 requirement ID、同區塊無重複 scenario ID。

**13.D current state**：兩個 delta 檔都只有 `## MODIFIED Requirements`（無 ADDED / REMOVED / RENAMED）。三個 MODIFIED 條目都依 13.D.1(b) 以 ID 解析到 main spec 的同 ID requirement（`tdd-claim-accuracy` REQ-3、REQ-4；`release-versioning` REQ-3）。新 scenario：`REQ-3-S4`（現有最大 S3）、`REQ-4-S2`、`REQ-4-S3`（現有最大 S1）皆大於現有最大值；`release-versioning` REQ-3 的 S1、S2 是既有 ID，不算新。無 13.D.3 違反。

**13.E 與 CLI 交叉比對**（只讀 stdout，stderr 導走）：

| 比對 | 文字計數 | CLI | 結果 |
|---|---|---|---|
| 候選 `contract-identity` requirementCount / 各 req scenario 數 | 8 / [5,4,6,6,2,4,3,5] | 8 / [5,4,6,6,2,4,3,5] | 一致 |
| 候選 `plan-contract` | 4 / [7,2,2,10] | 4 / [7,2,2,10] | 一致 |
| 候選 `release-versioning` | 4 / [3,1,2,2] | 4 / [3,1,2,2] | 一致 |
| 候選 `repo-guidance` | 1 / [2] | 1 / [2] | 一致 |
| 候選 `tdd-claim-accuracy` | 5 / [3,2,4,3,4] | 5 / [3,2,4,3,4] | 一致 |
| 候選 `tdd-evidence-contract` | 3 / [2,12,4] | 3 / [2,12,4] | 一致 |
| change `release-versioning` MODIFIED 條目數 / #1 scenario 數 | 1 / 2 | 1 / 2 | 一致 |
| change `tdd-claim-accuracy` MODIFIED 條目數 / #1、#2 scenario 數 | 2 / 4, 3 | 2 / 4, 3 | 一致 |

Check 13 的 BLOCK 分兩種、彼此不吸收：同一個 count mismatch 可能同時產生
VIOLATION 與 UNDETERMINABLE 兩種 finding，兩張表都要分別列出，**不得**
合併寫成一句「ID verification failed」。

**VIOLATION findings**（check 完整跑完某條規則後發現違反 REQ-1～REQ-4，
或一個可靠配對的 13.E 比對結果不一致）：

| 依據（13.C / 13.D / 13.E） | 檔案 / heading / 位置 | 說明（雙方數值或內容） |
|---|---|---|
| 無 | 無 | 無 |

**UNDETERMINABLE findings**（check 無法可靠跑完——preview 失敗、CLI 輸出
缺資料或形狀不符、配對不可靠；未跑完本身不是違規，也不得記成違規）：

| 依據（13.B / 13.E） | 對象 | 說明 |
|---|---|---|
| 無 | 無 | 無 |

若無 finding，兩張表都填「無」——不得省略整個表格。

> 13.F 新鮮度：本結果描述的是 main specs 與本 change delta 檔在 HEAD `ba68235` 時的狀態；之後任一被編輯，本結果即過期、必須重跑（agent 執行，沒有機制偵測）。

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

---

## 實作者筆記重跑（tasks 6.2–6.4 的紀錄落點）

plan 的 6.2–6.4 要求「記錄」，紀錄落在這裡。實作者筆記（session scratchpad 的 `verification-notes.md`）視為**待驗的宣稱**；下面是本 agent 自己重跑看到的結果。

### 6.1 結構驗證

與筆記一致：dogfood 副本 `diff -rq` 無差異、`schema validate` ✓、`schemas` 列得出、change valid、全新 scratch 專案 ✓（見 §1）。筆記提到副本是以覆寫複製同步（`rm` 被拒）；覆寫複製在來源刪檔時會留下舊檔，但 `diff -rq` 沒有任何 `Only in`，所以本次沒有殘留舊檔。

### 6.2 殘留搜尋

**搜尋範圍**：`git grep`（只搜 tracked 檔），排除 `openspec/changes/archive`、`文檔`（handoff）、`docs/superpowers`（poc / research / retrospectives / specs 等紀錄與設計文件）、本 change 目錄、`*.jsonl`；v4 類另排除 `backlog.md`。`openspec/schemas/` 副本為 gitignore、不在 `git grep` 範圍。實作者筆記另用了 `--untracked`（含 repo 根三份未追蹤的討論檔，並排除之），本 agent **沒有**搜未追蹤檔——這是兩者範圍的差異。

**REQ-3 已取代的說法**：

| 樣式 | 現行文件命中 | 判定 |
|---|---|---|
| `no reviewer per task` | `openspec/specs/tdd-claim-accuracy/spec.md:102` | 留——現行 living spec 的情境文字，archive 時被 delta 取代 |
| `by the author` | `superpowers-bridge/README.md:682`（log 新段表格）；`openspec/specs/tdd-evidence-contract/spec.md:34`（無關語意） | 留——事實本該在 log；另一筆與 executing-plans 無關 |
| `作者自己` | `superpowers-bridge/README.zh-TW.md:682`（log 新段） | 留 |
| `dispatches no independent reviewer` / `no independent reviewer` | living spec `:70`、`:99`（禁令與情境本身）；`README.md:660` S13 帶日期列 | 留——禁令文字與紀錄列 |
| `whenever subagent` / `一律導向` | living spec `:101`；README en/zh `:661` S14 帶日期列 | 留——禁令與紀錄列 |
| `bring TDD` | living spec `:85`（情境文字） | 留 |
| `上游建議` | `CLAUDE.md:258`（「不寫『上游建議用哪個』」） | 留——禁令本身 |
| `upstream recommend` | living spec `:69`、`:101` | 留——禁令 |
| `v6.4.1–v6.4.2`、`沒有每個 task 的審查`、`作者自審`、`不派任何獨立審查者`、`brings TDD`、`之後要改寫`、`claudemd-governance-rewrite`、`manual fallback path described`、`no prevention possible` | 0 筆 | — |

`schema.yaml` 內 `executing-plans` 只剩 5 行（description 第 12、14 行與 apply 第 1829、1837、1840 行），皆為能力語言與指向 log，無版本號或機制描述；`schema.yaml`、`templates/*.md` 無任何 `v6.x` / `v5.1.0`。

**v4 類樣式**（`v4` 58 筆、`version: 4` 8 筆、`4.x.y` 8 筆、`4.0.0` 28 筆）：逐筆讀過，全部屬下列之一，判定「留」：v3 → v4 歷史與 rollback（CLAUDE.md:203、README 中英 516–556、703）、v4 → v5 新段本身（README 中英 526–540、701）、版本列舉（README 118、491、495、598）、v4 Compatibility 列與其說明（593、600、602，依 design 保留）、帶日期的 follow-up 紀錄（667）、`pending` 說明（697，已含 v5）、`4.0.0` 起實施 tag 的規則（CLAUDE.md:199/201、README 489/493、release-versioning REQ-1/REQ-2）、roadmap 的 v4 段、`openspec/specs/release-versioning/spec.md` REQ-3 對 v4 列的歷史宣告（仍成立）。**唯一需要改的一筆**是 `openspec/specs/release-versioning/spec.md:52` 的 REQ-3-S2「reads the v4 row」——已由本 change 的 `release-versioning` delta 處理，archive 時生效（§3、§9）。

**與筆記比對**：結論一致，未發現筆記漏判的命中。行號以本 agent 看到的為準（筆記的 README `:682`、`:660`、`:661`、`:593` 等與現檔一致）。

### 6.3 三個語意未被改變

| 語意 | 出處（現檔） | 本 agent 的確認方式 |
|---|---|---|
| 1. 沒有 subagent 能力 → Step 0 STOP | `superpowers-bridge/schema.yaml` apply Step 0「If any required skill is missing, STOP and inform the user」（第 1761 行）；必要 skill 清單（第 1751–1759 行）；第三種情境清單第一項（第 1850 行） | `git diff b40e059 2551ea0 -U0 -- schema.yaml` 的 hunk 只有 `-2`、`-9,4`、`-1667,0`、`-1732,3`、`-1796,6`、`-1807,0`；Step 0 只動到 `-1732,3`（task 1.5 那句），STOP 句與 skill 清單不在任何 hunk 內 |
| 2. 有 SDD → 第 2 步正式路徑 | apply 第 2 步「Use the Skill tool to invoke **superpowers:subagent-driven-development**」（第 1782–1786 行）；第三種情境清單第二項（第 1851 行） | 該段不在任何 hunk 內 |
| 3. 刻意略過的紀錄不被讀成保障已滿足 | `schema.yaml` retrospective Skipped-skill rules「Such a record discloses a deviation. Do not present it as satisfying an assurance…」（第 1693 行）；apply 第三種情境「a record does not make a missing assurance present」（第 1863 行）；`templates/retrospective.md` 第 101 行「這段紀錄只揭露偏離…」 | 讀現檔文字 |

與筆記一致（筆記所列行號 1761、1784–1785、1850、1851、1693、1863、模板 101 與現檔相符）。

### 6.4 每週版本檢查讀的列 = 發布中的 schema major

- `superpowers-bridge/schema.yaml` 第 2 行：`version: 5`；`VERSION`：`5.0.0`。
- `.github/workflows/version-check.yml` 第 44 行（`Read pinned versions from README` step）：`line=$(grep -E '^\| v5 \| `' superpowers-bridge/README.md | head -1)`。
- Compatibility 表有 `| v5 | `1.14.0` | `v5.1.0` | pending |`（README.md 與 README.zh-TW.md 的 backtick 欄位相同），位於 v4 列之上。
- 把該 step 第 44–53 行原樣取出（只去掉 YAML 縮排）、設 `GITHUB_OUTPUT` 指向 scratch 檔實跑：exit 0，印出 `Pinned in README: OpenSpec=1.14.0, Superpowers=v5.1.0`，`GITHUB_OUTPUT` 得到 `openspec=1.14.0`、`superpowers=v5.1.0`。與筆記一致。
- **筆記沒寫、本 agent 多做的變異測試**：把列鍵改成 `v4` 再跑——**輸出完全相同**（`1.14.0` / `v5.1.0`，exit 0），因為 v4 與 v5 兩列的版本值相同；改成不存在的 `v6`——`::error::Could not find Compatibility table row…`，exit 1。所以**這次實跑只證明「step 能跑、讀得到一列、欄位形狀沒壞」，分辨不出它讀的是 v5 還是 v4 列**；列鍵是 `v5` 這件事是靠讀第 44 行的字面確認的。這不推翻 6.4 的結論（6.4 的驗收本來就包含讀檔），但「實跑讀到 v5 列」這個說法本身沒有分辨力，往後 v5 列的值與 v4 列分開時才有。
- 本紀錄**不**宣稱該檢查會自己找出最新那一列：它讀的是寫死的列鍵，升版時手動改（與 `release-versioning` 修改後的 REQ-3-S2 一致）。

### 筆記中無法重現的項目

- 無結論層面的不一致。範圍差異一項：筆記 6.2 用了 `--untracked`，本 agent 只搜 tracked 檔（未追蹤的 repo 根討論檔不在本 agent 的搜尋範圍內，也不屬現行文件）。
- 筆記 6.2 提到「CLAUDE.md:199/201『自 4.0.0 起』」等行號，本 agent 看到的相同。

---

## Overall Decision

- [ ] ✅ PASS — 可進入 finishing-a-development-branch 與 archive
- [x] ⚠️ PASS WITH WARNINGS — 可進入後續步驟但需注意：check 1–13 無 BLOCK、review judgement 無阻塞 finding、check 13 PASS；但有下列警告（皆非阻塞）
- [ ] ❌ FAIL — 返回失敗的 artifact 修正後重跑 verify

**警告清單**：

1. **執行方式偏離（經核可的例外，非等效）**：apply 未跑 `subagent-driven-development`（brainstorm Q4 具名例外、只限本 change）。沒取得執行過程中的逐 task 獨立審查；fallback reviewer（Fable）的多輪事後審查與本 verify 不等同 SDD。retrospective 必須依 REQ-4 記錄，並寫出這是第三例（8/31、10/06）、列 §6 Promote candidate。
2. **Precommit 未執行任何檢查**：`## Overall: ⚠️ NO CHECKS RUN`，不是 PASS；替代驗證與剩餘限制見 §5。
3. **驗證者獨立性有限**：本 verify 由同一 session 派出、與實作者同模型家族；第一個 verify 載體（Fable）用量上限中途失敗，本 agent 為備援載體。
4. **未推送**：`main` 領先 `origin/main` 4 個 commit；push 需使用者授權；push 後 `version-check.yml` 的 `workflow_dispatch` 實跑尚未發生；`v5.0.0` tag 尚未存在（屬 archive 後的發版流程）。
5. **6.4 實跑沒有分辨力**：v4 與 v5 兩列值相同，step 用 `v4` 或 `v5` 列鍵輸出一樣；列鍵正確性靠讀檔確認。
6. **Design 漂移（§4）**：apply 三種情境與 Step 0 修正沒有 spec requirement 承載；zh-TW log 新段少一個「設計觸點 #4」連結。
7. **Delta spec 尚未 sync（§3）**：archive 前的正常狀態；archive 前 main spec `release-versioning` REQ-3-S2 與 CI 現況矛盾。

**下一步**：

1. 由使用者決定：警告 6 的「apply 三種情境沒有 spec 承載」要不要在 archive 前補一條 requirement（補了要重跑本 verify 的 check 13 與 §3、§4），或接受現狀、記入 retrospective。
2. 寫 retrospective（`/opsx:continue` → retrospective），依本 change 自己的 REQ-4 記錄 SDD 略過：失去的保障、Q4 裁定出處、替代審查、`one-off — schema boundary case`、裁定只限本 change、前例兩次（8/31、10/06）與位置、列 §6 Promote candidate；不得寫成等同 SDD。
3. archive（Windows 依 repo CLAUDE.md 用 `cp -r` + `diff -r` + 使用者手動刪原目錄）。若 archive 前 `tasks.md` / `plan.md` / specs 有任何修改，對應檢查過期、須重跑。
4. 最終驗證與連動文件後，在 release commit 打 annotated tag `v5.0.0`，經使用者當次授權 push，確認遠端 `refs/tags/v5.0.0^{}` 等於 release commit；push 後以 `workflow_dispatch` 跑一次 `version-check.yml`；再以文件 commit 把 roadmap v5 段標 Released／已釋出。

---

## 實作者補充（Round 1 之後；**不是** verify agent 的結論）

> 以上全文是備援 verify agent 在 `2026-10-12 12:07` 的原始結果，原樣保留、不改寫。本節由**實作者**（主 session）在使用者 2026-10-12 對 W5、W6、W3 的裁定之後補上。它記錄補做的測試與修正，但不改變上面的判定。W3 的裁定是：備援 verify agent 的結果保留，不推翻；W6 修正與文件審查完成後，由 Fable 對最終實作、規格與本檔做獨立複審。修正後的最終判定，會由那位驗證者寫成 Round 2，接在本節之後。

### W5：能分辨對錯的變異測試（實作者補測）

**要證明的事**：`version-check.yml` 的 `Read pinned versions from README` step 讀的是 v5 列，不是 v4 列。

**為什麼原本的實跑證明不了**：v4、v5 兩列的值相同，讀哪一列都得到 `1.14.0`／`v5.1.0`（Round 1 §6.4 已指出）。

**做法**：

- 在 session scratchpad 放一份 `superpowers-bridge/README.md` 的副本，只把 v5 列改成 `| v5 | `9.9.9-V5ROW` | `v9.9.9-V5ROW` | pending |`。用 `diff` 確認除了 v5 列以外與 repo 現檔完全相同。
- 從 `.github/workflows/version-check.yml` 原樣取出第 44–53 行，只去掉 YAML 縮排與 CR，存成腳本。另做一份變異版：列鍵改成 `v4`，其餘相同，兩份的 `diff` 只差第 1 行。
- 兩份腳本分別在副本與 repo 現檔上跑，並設 `GITHUB_OUTPUT` 指向暫存檔。

**更正**：實作者第一次做這個測試（`2026-10-12` 上午）用的腳本**不是**逐字照抄。前 7 行相同，但把寫 `GITHUB_OUTPUT` 的三行換成了一行 `echo`，當時卻描述成「原樣取出」。下表是 `2026-10-12 14:13`（+0800）用真正原樣取出的第 44–53 行重跑的結果：

| 腳本 | 跑在 | exit | `GITHUB_OUTPUT` |
|---|---|---|---|
| 原樣（列鍵 `v5`） | 副本（v5 列為標記值） | 0 | `openspec=9.9.9-V5ROW` `superpowers=v9.9.9-V5ROW` |
| 原樣（列鍵 `v5`） | repo 現檔 | 0 | `openspec=1.14.0` `superpowers=v5.1.0` |
| 變異（列鍵 `v4`） | 副本 | 0 | `openspec=1.14.0` `superpowers=v5.1.0` |
| 變異（列鍵 `v4`） | repo 現檔 | 0 | `openspec=1.14.0` `superpowers=v5.1.0` |

**結論**：在副本上，原樣 step 讀到的是只有 v5 列才有的標記值，列鍵改成 `v4` 就讀到 v4 列的值。所以這個 step 讀的確實是 v5 列。

**限制**：這是在本機 bash 跑，不是在 GitHub Actions 上跑。push 後以 `workflow_dispatch` 實跑的那一次仍未發生（Round 1 W4）。

### W6：補上規格（使用者 2026-10-12 裁定甲）

- `specs/tdd-claim-accuracy/spec.md` 新增 `## ADDED Requirements` → **REQ-6 Apply keeps its three execution situations apart**，附情境 S1–S4。編號依據：living spec 與 archive 內所有 `tdd-claim-accuracy` 最大是 REQ-5。
- REQ-6 依 `schema.yaml` 現行文字寫成：Step 0 必要 skill 清單與 STOP 句、1.5 改寫的「no internal manual fallback」那幾句、apply 第 2 步的三種情境。條文同時寫出一個例外：Step 0 的 CLI 工具檢查缺工具時只發警告、不停止（S4）。`schema.yaml` 不需要為此再改。
- proposal（What Changes、版本判定第 1 類、Capabilities、Impact）、design（目標、D3「規格保護」、D7「ADDED REQ-6」）、tasks（1.2、1.5、6.3 加註 REQ-6）、plan（Pointers、Global constraints 加四條逐字引文、1.2／1.5／6.3 的驗收）同步更新。
- 不新增 fallback、執行器、機械檢查或欄位，也不再升版（本來就是 schema major 5）。

### 6.3 補記：REQ-6 情境對照 `schema.yaml`（實作者紀錄，待 Round 2 核對）

| REQ-6 情境 | `superpowers-bridge/schema.yaml` 出處（apply 指令，約略行號） |
|---|---|
| S1 缺必要 skill 就停止，沒有內部 fallback | Step 0「If any required skill is missing, STOP and inform the user … This schema has no internal manual fallback for apply … Do not switch schemas or execution paths on your own initiative.」（約第 1761–1768 行） |
| S2 刻意略過是經裁定的例外，不是執行模式 | 第 2 步三種情境的第三項「this is an exception to this schema's process, NOT a supported execution mode … a ruling made for an earlier change does not carry over … Do not describe the path taken as equivalent…」（約第 1853–1861 行） |
| S3 缺少的保障要停止，不能靠紀錄放行 | 同一項「If the change requires an assurance the substitute cannot provide, STOP and report — a record does not make a missing assurance present.」（約第 1861–1863 行） |
| S4 CLI 工具缺少只發警告 | Step 0「If a tool is missing, surface as WARNING (not STOP)」（約第 1770–1776 行） |

第二種情境（有 SDD 時照契約執行）對應三種情境清單第二項（約第 1851–1852 行）與第 2 步開頭的 invoke 段。

### zh-TW README 連結

`superpowers-bridge/README.zh-TW.md` 的 log 新段「executing-plans 審查結構」裡，「設計觸點 #4」補上連結 `#4-opinionated只支援-subagent-平台沒有手動-fallback`。

- 錨點用 GitHub 式 slug 規則在本機計算：轉小寫、去掉標點、空白換成 `-`。用同一規則檢查全檔所有 `](#…)`，0 個解析不到。
- 限制：沒有在 GitHub 的實際渲染頁上點過。

### 因此變成過期的 Round 1 結果

依 Round 1 §8 的 Freshness 段與 13.F：

- `tasks.md` 有修改 → §2、§7、§8 的 check 8–12 過期。
- `plan.md` 有修改 → check 12 過期。
- delta spec 有修改 → check 13 與 §3 過期。
- `design.md`／`proposal.md` 有修改 → §4 的對照過期。

這些都要在 Round 2 重跑。

---

## Round 2 — 最終驗證（獨立驗證者，model Fable）

**驗證時間**：`2026-10-12 14:32`（+0800）
**HEAD**：`ba68235`（`main`，領先 `origin/main` 4 個 commit）
**驗證對象**：**目前的工作樹**，不是 HEAD。工作樹相對 HEAD 有 6 個已修改檔（`design.md`、`plan.md`、`proposal.md`、`specs/tdd-claim-accuracy/spec.md`、`tasks.md`、`superpowers-bridge/README.zh-TW.md`）與 1 個未追蹤檔（本檔）。實作面（`schema.yaml`、`templates/`、`VERSION`、en README、`version-check.yml`、`CLAUDE.md`、頂層 README、roadmap）自 `2551ea0` 之後**沒有再動**（`git diff --stat 2551ea0 -- <那些路徑>` 無輸出）。
**Verifier**：獨立 verify subagent（model Fable 5.1），由主 session 以 Round 2 名義派出。

**本輪讀到的輸入（sha256 前 12 碼，供 §8 Freshness 與 13.F 比對）**：`tasks.md` `264501078517`、`plan.md` `77dc34ba9c48`、delta `tdd-claim-accuracy` `ef1201c99ac7`、delta `release-versioning` `d136e75a1537`、`design.md` `625ba8dc0e11`、`proposal.md` `e60fe0bf40df`、main `tdd-claim-accuracy` `ae7558ca9a03`、main `release-versioning` `67362f02d06a`、`schema.yaml` `e8928761fcc8`、en README `6eb49a00ea8c`、zh-TW README `cab53539e40b`、`version-check.yml` `c6095c8d2b07`。

### 獨立性與其限制（照實說）

- 本 agent **沒有**實作本 change，**沒有**寫 Round 1，也**沒有**寫實作者補充。每一項結果都由本 agent 重跑或重讀取得；Round 1 與實作者補充的數字只拿來**事後比對**，不拿來當輸入。Round 1 留在 scratchpad 的中間檔沒有沿用。
- **跨模型**：Round 1 是 Opus 5.5，實作者與 Round 1 同模型家族；本輪是 Fable。這是本 change 第一次由不同模型家族跑完整 verify。
- **限制一**：本 agent 仍由**同一個主 session** 派出，派工 prompt 由實作者那方撰寫（含「W5 做了什麼」「W6 補了什麼」的背景）。這不是外部審查，也不是另一個人；派工 prompt 裡的事實我全部當成待驗宣稱重跑過，但「要查什麼」的框架是派工方給的，框架外的東西我只靠自己的六軸自檢。
- **限制二**：Round 1 提到的 fallback reviewer 文件審查也是 Fable。本 agent **沒有**讀那些審查報告，但不能宣稱與它們「模型無關」。
- **限制三**：沒有任何 lint／連結檢查器／GitHub Actions 實跑參與；精確範圍見文末「沒跑的與替代做法」。

### PRECHECK — implementation evidence

| 指令 | 結果 |
|---|---|
| `git log --oneline $(git merge-base HEAD origin/main)..HEAD \| wc -l` | **4**（merge-base `b40e059`）→ > 0，通過 |
| `grep -c '^- \[x\]' openspec/changes/executor-governance-wording/tasks.md` | **20** → > 0，通過 |

commit 範圍的組成與 Round 1 相同（`213a6fb` 開 change、`80fd84b` handoff、**`2551ea0` 唯一實作 commit**、`ba68235` backlog）。W5／W6 的修正**尚未 commit**（見 check 5）。

### 執行方式偏離（沿用 Round 1 的記錄，本輪重讀確認仍成立）

apply 沒有跑 `superpowers:subagent-driven-development`（brainstorm Q4 具名例外、只限本 change）。本輪沒有新事實改變這一點；retrospective 必須依本 change 的 REQ-4 記錄，不得寫成等同 SDD。

### 總表：PRECHECK 與 check 1–13

| 檢查 | 本輪結果 | 與 Round 1 比較 | 備註 |
|---|---|---|---|
| PRECHECK | ✓ 4 / 20 | 同 | — |
| 1 Structural validation | ✓ 7/7 valid | 同 | `openspec validate --all --json` exit 0，items 7 / passed 7 / failed 0（change 1/1、spec 6/6，僅 INFO 級「text very long」）；`openspec validate executor-governance-wording` → valid；`diff -rq superpowers-bridge openspec/schemas/superpowers-bridge` 無輸出；dogfood `openspec schema validate` ✓；**全新 scratch 專案**（scratchpad `fresh-*/openspec/schemas/`）`schema validate` ✓ exit 0、`openspec schemas` 列出 `superpowers-bridge (project)` 且 description 是改寫後的新文字 |
| 2 Task completion | ✓ 20/20 `[x]` | 同（tasks.md 已改，重跑） | `grep -nE '^\s*- \[( \|~)\]'` 0 筆：無 `[ ]`、無 `[~]` |
| 3 Delta spec sync | ✗ Needs sync × 2 capability | **多一項 ADDED** | `tdd-claim-accuracy`：REQ-3 區塊不等（delta S1–S4，main S1–S3）、REQ-4 不等（delta S1–S3，main S1）、**REQ-6 main 不存在（ADDED）**；`release-versioning`：REQ-3 區塊不等（S2 文字改）。皆為 archive 前正常狀態 |
| 4 Design / specs coherence | ✓，無阻塞漂移 | **Round 1 漂移 1 已解** | 見下方「§4 重做」 |
| 5 Implementation signal | **✗ 工作樹有未 commit 的修改** | **退步**（Round 1 時工作樹乾淨） | 6 個已修改檔 + 本檔未追蹤；`main...origin/main [ahead 4]` 未推送；precommit runner `## Overall: ⚠️ NO CHECKS RUN`（不是 PASS） |
| 6 Front-door leak | WARNING 照列，非阻塞 | 同 | `docs/superpowers/specs/` 5 個檔，`git diff --name-only b40e059..HEAD -- docs/superpowers/specs` 無輸出，皆非本 change 產物 |
| 7 Deferred dogfood | ✓ 空白即 PASS | 同（重跑） | tasks.md 存在、20 條 task 行、0 條 `- [~]` |
| 8 TDD annotation | ✓ 20/20 | 同（重跑） | 每條恰好一條 `- TDD: n/a — <reason>`，分隔符皆 em dash，reason 非空（15–108 字元） |
| 9 Records / fields / subject | N/A（無 applicable） | 同 | RED／GREEN 皆 0 |
| 10 Outcome markers | N/A | 同 | — |
| 11 Subject pairing | N/A | 同 | — |
| 12 tasks ↔ plan 1:1 | ✓ 兩階段皆過 | 同（兩檔皆改，重跑） | 見下表 |
| 13 Identity integrity | ✓ PASS | **多驗一條 ADDED** | preview 成功；13.C／13.D 無 finding；13.E 全部一致（含候選 `tdd-claim-accuracy` 6 req） |
| R1–R4 | 無 finding | 同 | R1／R2 無 applicable 任務不適用；R3 20 條 n/a 理由成立（本輪逐條重讀）；R4 無 n/a 任務帶紀錄 |

### §4 重做：design / proposal / plan / specs 內部一致性（REQ-6 修改後）

| 抽樣項 | design / proposal / plan 描述 | specs 對應 | 差距 |
|---|---|---|---|
| D3「規格保護」 | 三種情境與 1.5 修正後的 Step 0 要有規格；REQ-6 依現行文字寫成、schema 不需再改 | `tdd-claim-accuracy` ADDED REQ-6 全文 | 一致；`schema.yaml` 自 `2551ea0` 未變，與「不需再改」相符 |
| D7「ADDED REQ-6」 | 三種情境各自的條文；S4 例外（CLI 工具只警告）；編號 REQ-6 因 living spec 與 archive 最大為 REQ-5 | REQ-6 正文三個 bullet + 收尾段 + S1–S4 | 一致；編號依據本輪實查：`openspec/specs/tdd-claim-accuracy` 與 `openspec/changes/archive/*/specs/tdd-claim-accuracy/` 的 requirement ID 最大為 REQ-5，全 history 無 REQ-6 |
| proposal「版本判定」第 1 類 | REQ-6 是既有契約寫明、不讓既有 artifact 變不合法 | REQ-6 收尾段「adds no fallback, no executor, no mechanical check and no recorded field」 | 一致 |
| proposal「版本判定」首段改句 | PRECHECK 形狀不變：必要 skill 清單與 STOP 不動，1.5 只改指向不存在段落那句 | REQ-6 S1、S4 | 一致；`git diff b40e059 2551ea0 -U0 -- schema.yaml` 的 Step 0 hunk 只有一處（Round 1 已列，本輪重讀現檔第 1751–1768 行確認） |
| plan Global constraints 新增 4 句 | 標為「verbatim from the specs」 | REQ-6 第 1 句、情境 1 前兩句、情境 3 第 2 句、收尾段前兩句 | 逐字相同（唯一差異：第 1 句 spec 以冒號收尾、plan 以句號收尾） |
| plan 1.2／1.5／6.3 驗收 | 1.2 涵蓋情境 2、3（S2、S3）；1.5 涵蓋情境 1（S1）與 S4；6.3 要逐條對照 S1–S4 | REQ-6 S1–S4 | S1–S4 被 1.2 + 1.5 完整分攤；6.3 的對照紀錄落在本檔「實作者補充」表與下方本輪的三軸表 |
| D8 ↔ `release-versioning` S2 | 列鍵 `v5`、不宣稱自動找最新列 | REQ-3-S2 修改版 | 一致 |

**內部矛盾搜尋結果**：沒有找到阻塞級矛盾。一項**措辭層**觀察（非阻塞，不是違反 REQ-6）：

- REQ-6 情境 1 的觸發條件是「Step 0 列為必要的**任一** skill 缺少」（三個：`using-git-worktrees`、`subagent-driven-development`、`finishing-a-development-branch`）；但 `schema.yaml` 第 1850 行三種情境清單的第一項標籤寫「**No subagent capability** — Step 0 STOPs, as above」，design D3 第一項與 proposal 第一項也都寫「沒有 subagent 能力」。標籤比條文窄，但三處都把行為交回 Step 0（「as above」），而 Step 0 第 1761 行確實對**任一**必要 skill 缺少就 STOP，所以實際行為符合 REQ-6。這是「標籤名了子集合、行為涵蓋全集」，不是實作比規格鬆；要不要把標籤改成「缺任一必要 skill」屬使用者判斷，改了只動 schema 文字（不影響 schema major）。

**漂移警告**（非阻塞）：

1. 上面那條標籤觀察。
2. Round 1 的漂移 1（三種情境無 spec 承載）**已由 REQ-6 解決**；漂移 2（zh-TW log 新段少一個連結）**已解**（見下方「Round 1 警告狀態」）。

### Check 5 細節（本輪唯一退步的項目）

- [ ] Worktree 內無未 staged 的檔案 — **不成立**：`git status --short` 列出 6 個 ` M` 與 1 個 `??`（本檔）。這些是 W5／W6 裁定後的修正，尚未 commit。
- [ ] 所有相關 commit 已推送 — **不成立**：`[ahead 4]`。
- **Commit 範圍**：`b40e059..ba68235`（4 個 commit，實作只在 `2551ea0`）+ **工作樹未 commit 的 6 檔**。
- **Precommit**：本輪重跑 `node .claude/scripts/precommit-runner.js` → `## Overall: ⚠️ NO CHECKS RUN (no runnable scripts …)`，exit 0。**這不是 PASS**，runner 沒有執行任何檢查。
- **後果**：本輪的 check 1–13 都是對工作樹內容做的，commit 本身不會改內容，所以只要 commit 進去的檔案 sha256 與上面列的相同，本輪結果仍描述它們；但 check 5 的「已 commit」要在 commit 後才成立，archive 前要有那個 commit。

### Check 8–12 細節

判讀方式：以本 agent 自寫的腳本（scratchpad `round2/checks8to12.py`，依 instruction 的 TASK LINE／BELONGS TO／空行透明／INDENT RULE 逐行實作）讀 tasks.md 與 plan.md；plan.md 的 fence 與 entry 規則依 check 12 原文（column-0 backtick fence 切換、`## Task <n>` 與 `## <n>` 兩種形式、token 須以空白或行尾收尾）。

**Per-task results**：20 條 task 行（1.1–1.5、2.1、3.1–3.4、4.1–4.4、5.1–5.2、6.1–6.4）每條都是 ✓ `TDD: n/a — <reason>`（em dash，reason 非空）、RED 0、GREEN 0 → check 9–11 N/A。R3 逐條重讀：全部是 prose／configuration／查驗類改動，理由成立；4.2 的「本機實跑確認」在 W5 之後**已有分辨力**（見 W5 判斷），Round 1 對 4.2 的附註不再適用。

**Check 12, stage one — duplicate keys per side**：

| Side | Repeated keys (name each) | Verdict |
|---|---|---|
| `tasks.md` task numbers | — | ✓ |
| `plan.md` entry keys | — | ✓ |

**Check 12, stage two — set equality in both directions**：

| `tasks.md` task numbers | `plan.md` entry keys | Only in tasks (no entry) | Only in plan (no task) | Verdict |
|---|---|---|---|---|
| `{1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 6.1, 6.2, 6.3, 6.4}` | 同左 20 個（全為 canonical `## Task <n> — …`；plan.md 無 column-0 fence、無非條目 `##` 標題） | — | — | ✓ |

**Blocking findings（check 8–12 與 R1–R4）**：無。

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

### Check 13 細節 — Identity integrity

13. **Identity integrity** (deterministic in what it decides, agent-executed like checks 8-12; BLOCKs are of two kinds)

**Verdict（Round 2）**：✓ PASS — preview 成功，13.C／13.D 沒有任何 finding，13.E 每一項比對都完成且一致。

**13.B archive preview**：把 repo 的 `openspec/` 整個複製到 scratchpad 下全新目錄 `round2/preview13-*/`（repo 外），在那裡跑 `openspec archive executor-governance-wording -y`（無其他旗標）。三個條件皆成立：exit `0`；`openspec/changes/executor-governance-wording/` 已不存在；`openspec/changes/archive/2026-10-12-executor-governance-wording/` 存在。輸出：`release-versioning: ~ 1 modified`、`tdd-claim-accuracy: + 1 added, ~ 2 modified`、`Totals: + 1, ~ 3, - 0, → 0`（與 Round 1 的差別就是那個 `+ 1`：REQ-6）。repo 自己的 `openspec/` 未被修改（`git status` 前後相同）。check 3 兩個 capability 都是 Needs sync，無 SYNCED CAPABILITY 不可判定情形。

**13.C candidate state**（preview 產出的全部 6 個 main spec，以 13.A 字面規則逐行計數）：每個 requirement heading 都符合 `REQ-[A-Z0-9]+ <description>`，每個 scenario heading 都符合 `<REQ-ID>-S<m>` 且 REQ-ID 等於所屬區塊；同檔無重複 requirement ID、同區塊無重複 scenario ID。候選 `tdd-claim-accuracy` 的 ID 序列為 REQ-1…REQ-6。

**13.D current state**：delta `tdd-claim-accuracy` 有 `## MODIFIED Requirements`（REQ-3、REQ-4）與 `## ADDED Requirements`（REQ-6）；delta `release-versioning` 只有 MODIFIED（REQ-3）。
- 13.D.1：三個 MODIFIED 條目依 (b) 以 ID 解析到 main spec 同 ID requirement。ADDED REQ-6：main spec **不**持有 REQ-6（無碰撞）；delta 內只有一個 ADDED 條目（無同檔重複）。
- 13.D.2：無 RENAMED，不適用。
- 13.D.3：新 requirement REQ-6 為 NUMERIC，6 > main spec 現有最大數字 ID 5 ✓；其 S1–S4 為新 requirement 下的新 scenario，現有集合為空，任意正整數皆可 ✓。MODIFIED 內的新 scenario：REQ-3-S4（現有最大 S3）、REQ-4-S2／S3（現有最大 S1）皆大於現有最大 ✓；`release-versioning` REQ-3 的 S1、S2 為既有 ID。無違反。

**13.E 與 CLI 交叉比對**（只讀 stdout，`2>/dev/null`）：

| 比對 | 文字計數 | CLI | 結果 |
|---|---|---|---|
| 候選 `contract-identity` requirementCount / 各 req scenario 數 | 8 / [5,4,6,6,2,4,3,5] | 8 / [5,4,6,6,2,4,3,5] | 一致 |
| 候選 `plan-contract` | 4 / [7,2,2,10] | 4 / [7,2,2,10] | 一致 |
| 候選 `release-versioning` | 4 / [3,1,2,2] | 4 / [3,1,2,2] | 一致 |
| 候選 `repo-guidance` | 1 / [2] | 1 / [2] | 一致 |
| 候選 `tdd-claim-accuracy` | **6** / [3,2,4,3,4,**4**] | 6 / [3,2,4,3,4,4] | 一致 |
| 候選 `tdd-evidence-contract` | 3 / [2,12,4] | 3 / [2,12,4] | 一致 |
| change `release-versioning` MODIFIED 條目數 / #1 scenario 數 | 1 / 2 | 1 / 2 | 一致 |
| change `tdd-claim-accuracy` MODIFIED 條目數 / #1、#2 scenario 數 | 2 / 4, 3 | 2 / 4, 3 | 一致 |
| change `tdd-claim-accuracy` **ADDED** 條目數 / #1 scenario 數 | 1 / 4 | 1 / 4 | 一致 |

CLI `deltas` 共 4 筆（release-versioning MODIFIED；tdd-claim-accuracy ADDED、MODIFIED、MODIFIED），與文字端的 4 個條目一一對上。

**VIOLATION findings**：

| 依據（13.C / 13.D / 13.E） | 檔案 / heading / 位置 | 說明（雙方數值或內容） |
|---|---|---|
| 無 | 無 | 無 |

**UNDETERMINABLE findings**：

| 依據（13.B / 13.E） | 對象 | 說明 |
|---|---|---|
| 無 | 無 | 無 |

> 13.F 新鮮度：本結果描述 main specs 與本 change delta 檔在上面列的 sha256 時的狀態；之後任一被編輯，本結果即過期、必須重跑（agent 執行，沒有機制偵測）。

**宣稱邊界摘要**（僅摘要；完整定義見 openspec-schemas repository 的 `openspec/specs/contract-identity/spec.md` REQ-8，<https://github.com/azuma520/openspec-schemas/blob/main/openspec/specs/contract-identity/spec.md>——該 spec 不隨 `superpowers-bridge/` bundle 內含）：check 13 是一組決定論、機器可判的規則，由 verify agent 依 instruction 執行；它不是 harness 層強制、不可繞過的 archive-time gate——verify agent 沒跑它時，本 schema 沒有機制攔截這個疏漏。它只確立 candidate state 與本 change 在 13.C 到 13.E 範圍內的結論，**不**確立「退役的 ID 不會被重新配用」、「一個 scenario ID 不會透過 MODIFIED 全文替換或 archive 悄悄消失」、「同一個 ID 底下的語意沒有被弱化」，或「capability 改名後 ID 存活」。

### REQ-6 三軸對照（規格 → 實作 → 測試／證據）

實作軸的行號是本輪讀 `superpowers-bridge/schema.yaml` 現檔（sha256 `e8928761fcc8…`）取得。測試軸：REQ-6 約束的是 instruction 文字，沒有可執行測試；證據是「讀出該段文字」這個動作本身，由 tasks 6.3（`[x]`）承載、實作者補充的表記錄、本輪獨立重讀。

| REQ-6 條文（規格軸） | `schema.yaml`（實作軸） | 測試／證據軸 | 判定 |
|---|---|---|---|
| 「SHALL keep three situations apart and SHALL NOT merge any two」 | 第 1848 行「Three situations, kept apart:」，三個 bullet 第 1850、1851、1853 行 | tasks 1.2；本輪重讀 | 符合 |
| 情境 1：任一必要 skill 缺少 → Step 0 STOP 並告知使用者 | 第 1751–1759 行必要 skill 清單；第 1761 行「If any required skill is missing, STOP and inform the user」 | tasks 1.5、6.3(1)；本輪重讀；Round 1 以 `git diff -U0` 證明此句不在任何 hunk | 符合 |
| 情境 1：「state that the bridge has no internal manual fallback for apply and SHALL NOT point to one」 | 第 1763–1764 行「This schema has no internal manual fallback for apply」；apply 指令（1742–1910 行）內 `fallback` 僅出現 3 次：1763（此句）、1775（CLI 工具「user may have a fallback」）、1829（「does NOT support executing-plans as a fallback」），**沒有任何一處指向 fallback 段落** | tasks 1.5；本輪 `grep` | 符合 |
| 情境 1：點名使用者的兩個選項（安裝 skill／明確改用 `spec-driven`，「a different workflow rather than a degraded path」） | 第 1764–1767 行 | tasks 1.5 | 符合 |
| 情境 1：禁止 agent 自行切換 schema 或執行路徑 | 第 1767–1768 行「Do not switch schemas or execution paths on your own initiative」 | tasks 1.5 | 符合 |
| 情境 2：有 SDD → 依 step-2 契約執行 | 第 1782–1786 行（invoke SDD）；第 1851–1852 行 bullet | tasks 1.2、6.3(2) | 符合 |
| 情境 3：「exception … not a supported execution mode」 | 第 1854–1856 行 | tasks 1.2、6.3(3) | 符合 |
| 情境 3：「only the user's explicit ruling for this change makes the exception」、「SHALL NOT decide it on its own initiative」、「earlier change does not carry over」 | 第 1856–1859 行 | tasks 1.2 | 符合 |
| 情境 3：「SHALL NOT describe the path taken as equivalent to SDD or as satisfying the independent review it provides」 | 第 1859–1861 行 | tasks 1.2、6.3(3) | 符合 |
| 情境 3：缺必要保障 → STOP and report | 第 1861–1863 行「STOP and report — a record does not make a missing assurance present」 | tasks 1.2、6.3(3) | 符合 |
| 情境 3：「deviation is recorded per REQ-4」 | 第 1863–1865 行「Record the deviation in the retrospective per its skipped-skill rules」；該規則在第 1670–1697 行，即 REQ-4 管轄的 schema 面 | tasks 1.2、1.3 | 符合（措辭不同、指涉相同） |
| 收尾段：「adds no fallback, no executor, no mechanical check and no recorded field」 | `2551ea0` 對 `schema.yaml` 的 diff 無新 artifact、無新 `requires:`、無新檢查、無新欄位（Round 1 hunk 清單；本輪確認 schema 自該 commit 未再變） | check 1、Round 1 §6.3 | 符合 |
| 收尾段：「the third situation is not an execution path the agent may select」 | 第 1856 行「Do not decide it on your own initiative」 | — | 符合 |
| 收尾段／S4：STOP 只管必要 skill；CLI 工具缺少 → WARNING 不 STOP | 第 1770–1776 行「surface as WARNING (not STOP)」 | tasks 1.5（REQ-6-S4）；Round 1 證明該段不在任何 hunk | 符合 |
| S1 | 全部由上面情境 1 的五列承載 | — | 符合 |
| S2 | 情境 3 前三列 | — | 符合 |
| S3 | 情境 3「STOP and report」列 | — | 符合 |
| S4 | 最後一列 | — | 符合 |

**比實作嚴或鬆的地方**：

- **沒有一條 REQ-6 條文比實作嚴到實作不滿足**；每一條都在 `schema.yaml` 找得到對應文字。
- **規格比實作的「標籤」廣一處**：情境 1 條文涵蓋任一必要 skill，第 1850 行 bullet 標籤只寫「No subagent capability」（見 §4 觀察）。行為上實作透過「as above」引用 Step 0，Step 0 涵蓋全集，所以不是實作違反規格；是標籤可以更準。
- **規格沒有比實作鬆**：schema 第 1863 行「a record does not make a missing assurance present」在 REQ-6 以 S3「does not let a record of the deviation stand in for the missing assurance」承載；第 1766–1767 行「a different workflow, not a degraded path」在情境 1 條文有對應。沒有發現 schema 有、而 REQ-6 漏寫的規範性句子（REQ-3 管的能力理由段 1829–1846 行不在 REQ-6 範圍，由 REQ-3 承載）。

### W5 判斷：變異測試能不能分辨對錯

**本輪自己重做**（scratchpad `round2/w5/`，不沿用實作者的檔）：

1. 從 `.github/workflows/version-check.yml` 取第 44–53 行，只去掉 10 格 YAML 縮排與 CR，存為 `step-v5.sh`；把它與再次取出的原文 `diff` → IDENTICAL，確認逐字。
2. 變異版 `step-v4.sh`：以 Python 字串替換只把 `'^\| v5 \| `'` 改成 `'^\| v4 \| `'`；兩檔 `diff` 只差第 1 行。
3. README 副本：只把第 592 行 v5 列改成 `| v5 | `9.9.9-V5ROW` | `v9.9.9-V5ROW` | pending |`；`diff` 確認只差這一行。
4. 四種組合各跑一次，`GITHUB_OUTPUT` 指向暫存檔：

| 腳本 | 跑在 | exit | `GITHUB_OUTPUT` |
|---|---|---|---|
| 原樣（`v5`） | 副本 | 0 | `openspec=9.9.9-V5ROW`、`superpowers=v9.9.9-V5ROW` |
| 原樣（`v5`） | repo 現檔 | 0 | `openspec=1.14.0`、`superpowers=v5.1.0` |
| 變異（`v4`） | 副本 | 0 | `openspec=1.14.0`、`superpowers=v5.1.0` |
| 變異（`v4`） | repo 現檔 | 0 | `openspec=1.14.0`、`superpowers=v5.1.0` |

與實作者補充的表**完全相同**。

5. 本輪多做兩個變異：列鍵改成不存在的 `v6` → `::error::Could not find Compatibility table row…`，exit 1（抓不到列會 fail，與 CLAUDE.md 耦合表說法一致）；在副本裡把 v4 列搬到 v5 列**之上**、用 `v5` 列鍵跑 → 仍讀到標記值（選列靠列鍵，不靠列的順序或 `head -1`）。

**判斷**：這個設計**分得出對錯**。oracle 是「只有 v5 列才有的標記值」，在同一份輸入上，正確列鍵讀到標記值、錯誤列鍵讀到另一列的值，兩者輸出不同；而且錯誤列鍵的輸出剛好等於 repo 現檔上兩種列鍵的共同輸出，解釋了為什麼 Round 1 的原始實跑沒有分辨力。因此「該 step 讀的是 v5 列」這個宣稱**成立**，Round 1 的警告 5 解除。

**它沒有證明的事**（照實列）：

- **不是在 GitHub Actions 上跑的**。本機 Git Bash 與 `ubuntu-latest` 的 `run:` 預設 shell 都是 bash，`grep -E`／`awk -F` 都是 POSIX 用法，但沒有實跑過；push 後的 `workflow_dispatch` 仍未發生。
- **不證明 v5 列的值是對的**（`1.14.0`／`v5.1.0` 是比照 v4 列沿用的歷史宣告，README 表下已說明不是相容保證）；測試只證明「讀哪一列」。
- **不涵蓋 zh-TW README**：workflow 只讀 `superpowers-bridge/README.md`；zh-TW 的 v5 列與 en 相同（本輪 `grep` 兩檔第 592 行相同）是靠讀檔確認，不是靠這個 step。
- **若未來出現兩列都以 `| v5 | `` 開頭**，`head -1` 會默默取第一列——測試沒有、也不需要證明這種輸入下的行為，但 CLAUDE.md 耦合表有講。
- 實作者補充提到「第一次做的腳本不是逐字照抄、後來更正」：本輪只能驗證**更正後**的方法與結果，無法驗證那段歷史。

### Round 1 警告狀態

| Round 1 警告 | 狀態 | 本輪依據 |
|---|---|---|
| 1 執行方式偏離（經核可例外，非等效） | **仍在**（本質如此，retrospective 要記） | 無新事實 |
| 2 Precommit 未執行任何檢查 | **仍在** | 本輪重跑仍 `⚠️ NO CHECKS RUN` |
| 3 驗證者獨立性有限 | **部分解決** | 本輪是跨模型家族的獨立重跑；仍由同一 session 派出（見上方限制） |
| 4 未推送、tag 未打 | **仍在** | `[ahead 4]`；本機與 origin 只有 `v4.0.0`（剝開 `d2a350c`） |
| 5 6.4 實跑沒有分辨力 | **已解決** | W5 變異測試本輪重現 |
| 6-1 三種情境無 spec 承載 | **已解決** | ADDED REQ-6，三軸對照全部符合 |
| 6-2 zh-TW log 新段少「設計觸點 #4」連結 | **已解決** | zh-TW 第 675 行已有 `](#4-opinionated只支援-subagent-平台沒有手動-fallback)`；以 GitHub slug 規則算全檔 23 個 `](#…)` 連結，0 個解析不到（en 亦 23／0；標題各 58 個）。限制：沒在 GitHub 實際渲染頁點過 |
| 7 Delta spec 尚未 sync | **仍在**（正常），且現在多一條 ADDED | check 3 |

**本輪新增的警告／觀察**：

- **N1（警告）**：W5／W6 的修正**尚未 commit**（check 5）。archive 與發版前要 commit；commit 後本輪結果仍適用，條件是檔案內容不變（以上面 sha256 比對）。
- **N2（觀察，非阻塞）**：三種情境第一項標籤「No subagent capability」比 REQ-6 情境 1 窄（見 §4）。
- **N3（觀察，給下一階段）**：retrospective 的 PRECHECK（`schema.yaml` 第 1546–1549 行）用 `grep -cE '^- \[x\] (✅ PASS|⚠️ PASS WITH WARNINGS|❌ FAIL)'` 要求本檔**恰好一個**勾選框。本檔採「保留 Round 1、附加 Round 2」的寫法，Round 1 的 `- [x] ⚠️ PASS WITH WARNINGS` 是唯一會被那條 grep 讀到的勾選框；因此本輪的決定**刻意不寫成 column-0 的 `- [x]` 勾選框**（寫了會變成 2 個，retrospective 會以「ambiguous verdict」STOP）。本輪決定與 Round 1 相同，所以那個勾選框仍然是真的；若 Round 2 的決定與 Round 1 不同，這個寫法就會讓機械檢查讀到過時的結論——那是這種附加式 verify.md 與 schema「每次覆寫」假設之間的落差，記下來供 retrospective 判斷。

### openspec-verify-change skill 三維度

| Dimension | Status |
|---|---|
| Completeness | 20/20 tasks；delta requirement 4 條（REQ-3、REQ-4、REQ-6；release-versioning REQ-3）皆有實作證據 |
| Correctness | 4/4 reqs covered；REQ-6 S1–S4 逐條對到 `schema.yaml`；REQ-3 四個 scenario 本輪抽讀 en README 第 313、465、675、685、739 行、`schema.yaml` description 與 apply 段、CLAUDE.md 第 258 行：皆只寫能力＋限制＋引用 log，機制與版本只在 log 段（675–685 行）；REQ-4：模板第 89 行選項字面為 `one-off — schema boundary case`、第 96–101 行說明與 schema 第 1670–1697 行同義，`no prevention possible` 現行文件 0 筆；release-versioning REQ-3-S2：W5 |
| Coherence | design D1–D8 與 specs 一致（§4 重做表）；無 CRITICAL；WARNING 0；SUGGESTION 1（N2 標籤措辭） |

### 沒跑的與替代做法（照實揭露）

| 沒跑／跑不到 | 原因 | 替代 |
|---|---|---|
| `/precommit` 的 lint／build／test | runner 回 `NO CHECKS RUN`（repo 無 package.json／lint 設定） | `openspec validate --all --json`、兩處 `schema validate` + `schemas`、`diff -rq` 副本、自寫腳本跑 check 8–13、W5 實跑 |
| GitHub Actions 上的 `version-check.yml` | 未推送 | 本機逐字取出 step 實跑 + 變異測試 |
| GitHub 實際渲染頁的錨點點擊 | 無瀏覽器步驟 | 以 GitHub slug 規則本機解析（兩檔 0 個解析不到） |
| Markdown／YAML lint、`check-doc-links.js` | 未被 runner 接上，本輪也未另跑 | 人讀 + 上述錨點解析 |
| 外部（非同一 session）的審查 | 本 agent 由同一 session 派出 | 跨模型家族重跑；限制已寫在「獨立性」段 |
| Round 1 提到的 fallback reviewer 審查報告 | 本輪沒有讀 | 不依賴它們；所有結論自行取得 |

### Overall Decision（Round 2 的決定）

**Round 2 決定：⚠️ PASS WITH WARNINGS** —— check 1–4、6–13 無 BLOCK，check 13 PASS，review judgement 無阻塞 finding，REQ-6 三軸對照全部符合，W5 宣稱成立；check 5 的「已 commit」與「已推送」兩項不成立，加上 Round 1 仍在的警告 1、2、4、7。
（三個勾選框只保留 Round 1 那一個，理由見 N3；本輪的決定以本行為準。）

**警告清單（本輪）**：N1 未 commit；Round 1 的 1、2、4、7 仍在；N2 為非阻塞觀察。

**下一步**：

1. 把 W5／W6 的 6 個修改檔 commit（本檔一併進 commit）。commit 後比對檔案 sha256 與本輪所列相同即可，不必重跑 check 1–13；若在那之前又改了 `tasks.md`／`plan.md`／delta spec／main spec，依 §8 Freshness 與 13.F 重跑對應檢查。
2. 使用者判斷要不要把第 1850 行的標籤改成「缺任一必要 skill」（N2）；改了只動 schema 文字，之後要重同步 dogfood 副本、重跑 check 1 與本輪三軸表第 1 列。
3. 寫 retrospective：依 REQ-4 記錄 SDD 略過（失去的保障、Q4 裁定出處、替代審查、`one-off — schema boundary case`、裁定只限本 change、前例兩次 8/31 與 10/06、§6 Promote candidate）；順帶記 N3。
4. archive（Windows 依 repo CLAUDE.md 用 `cp -r` + `diff -r` + 使用者手動刪原目錄），再依 `release-versioning` REQ-1 打 `v5.0.0`、經授權 push、確認 `refs/tags/v5.0.0^{}`，push 後 `workflow_dispatch` 跑一次 `version-check.yml`，最後以文件 commit 把 roadmap v5 段標 Released／已釋出。

---

## 實作者附記（Round 2 之後，2026-10-12；**不是**驗證者的結論）

Round 2 寫成之後，`CLAUDE.md` 有一次未 commit 的修改，不在 Round 2 雜湊過的檔案清單裡。這次修改屬於 retrospective §6 處置表的「直接修」，依處置表要在本 change 之外單獨提交。`git diff -U0 CLAUDE.md` 的四個 hunk 是：

- 第 157 行：「重新同步副本」的觸發條件，從「改完 schema」放寬為「改了 `superpowers-bridge/` 底下任何檔案」。
- 第 190 行：跨檔耦合表新增「升 schema major」一列。
- 第 202、204 行：來源路徑改指 archive 後的位置。

四處都不在「修 schema 時的紅旗」清單內。這份 diff 中 `紅旗` 與 `❌` 的命中數為 0。REQ-3 點名的 CLAUDE.md 紅旗面因此未變，Round 2 對 REQ-3 的結論不受影響。
