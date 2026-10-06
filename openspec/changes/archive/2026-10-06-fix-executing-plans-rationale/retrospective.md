# Retrospective: fix-executing-plans-rationale

> Written: 2026-10-06 (after verify passed)
> Commit range: `a136720..9ef62c2`（實作）；verify 之後的 README 修正與 verify / retrospective 隨歸檔 commit 一起提交
> Worktree: main（inline，未開 worktree；見 §4）

---

## 0. Evidence

- **Commit range**: `a136720..9ef62c2`（1 commit，實作與 change 文件）
- **Diff size**: `9ef62c2` 為 +413 / −15，共 11 檔（`git show --shortstat`）；其中 bridge 表面 4 檔 +17 / −15，其餘為 change 文件。verify 後另有兩份 README 各 +4 / −2（未併入此數字，見 §3）
- **Tasks done**: 7/7（`grep -cE '^\s*- \[x\]' tasks.md` → 7）
- **Active hours**: 約 1.5–2 小時。本 session 約 14:05 開工、討論範圍後於 15:20 建立 change（`.openspec.yaml` mtime），15:44 實作 commit，其後 verify、README 修正與複盤
- **Subagent dispatches**: 1（獨立 verify 執行者，opus）。另有 Codex 外部審查 3 次：文件審 r1、r2（同一 thread `01a1101b-7316-…`），程式碼審 r1（thread `01a1101b-732b-…`）
- **New external dependencies**: none
- **Bugs encountered post-merge**: n/a — 直接在 main 上 commit，無 merge
- **OpenSpec validate state at archive**: 歸檔前 `openspec validate fix-executing-plans-rationale` pass；verify.md check 1 記 `openspec validate --all --json` 6/6 valid
- **Test coverage signal**: n/a — 7 個 task 全為 `TDD: n/a`（prose / configuration）。本 repo 唯一的測試 `openspec schema validate superpowers-bridge` 與 `openspec schemas` 在乾淨專案中通過

Commit chain (時序):

```
a136720 chore(handoff): mark post-session cleanup done in the 2026-10-06 12:06 session
9ef62c2 fix(bridge): correct executing-plans exclusion rationale for Superpowers v6.4.1
<archive commit：verify、retrospective、README 後續修正、歸檔>
```

---

## 1. Wins

- [evidence: brainstorm.md §1.3、§1.4] **讀上游原文而不是讀摘要。** 直接讀本機安裝的 executing-plans `SKILL.md`（6.3.0、6.4.1、6.4.2），才發現舊說法在 fallback 情境（沒有 subagent）其實一半仍成立——沒有 subagent 時最後那次審查是作者自審。新理由因此能對準 fallback 情境，而不是只把「不派審查者」改成「會派審查者」。
- [evidence: brainstorm.md Q2、design.md D1] **找到錯誤說法的源頭是正式規格 REQ-3。** REQ-3 用 SHALL 規定理由必須是那兩句；若只改文件，下次照規格檢查會把正確文字判為不合規。
- [evidence: design.md D2] **新理由不依賴「上游建議用哪個」。** 上一次失效正是因為上游建議改了；新理由只陳述 executing-plans 自己的審查結構。
- [evidence: 文件審 r1 報告、`README.md` § 2. Schema-level vs prompt-level integration] **外部審查抓到實作者看不到的矛盾。** Codex 文件審 r1 指出 README「上游升版 skill 行為時 schema 不用改」與本 change 本身矛盾；修正後依「一個缺陷＝一類缺陷」全 repo 搜同類說法，只有中英各一處。
- [evidence: verify.md check 13] **獨立 verify 執行者在暫存副本試做歸檔**，三個條件與 5 份 spec 的標題計數全數對上；它也獨立核對了全部上游說法。
- [evidence: md5 `b0376b13…`] **固定版本連結前先證明版本相同。** 上游 `v6.4.1` 標籤上的 `executing-plans/SKILL.md` 與本機 6.4.1 安裝檔 md5 相同，才把 README 連結從 `main` 改指 `v6.4.1`。

## 2. Misses

- 🟡 [painful | evidence: 文件審 r1 🔴、tasks.md 2.3] **初始範圍只搜了「executing-plans」這個詞。** README § 2 那句「上游行為改了 schema 不用改」沒有提到 executing-plans，所以不在掃描結果裡，但它正是被本 change 推翻的宣稱。修的是「上游改版讓宣稱失效」時，「怎麼處理上游改版」這類後設說法也該一起搜。花了一輪文件審。
- 🟡 [painful | evidence: brainstorm.md 第 19、111 行修正前後] **憑記憶寫工作地圖編號，兩個都寫錯**（`task-20261002-rewrite-executing-plans-rationale`、`task-20260901`）。寫完自查時對照 `work-map.jsonl` 才改正，未進審查。
- 🟡 [painful | evidence: design.md D2 修正、`CLAUDE.md` 第 252 行修正、README § 2 修正] **修正句連續三次又寫成說過頭的句子**：「每個任務都審」（SDD 會合批）、「v6.4.1 之前的版本都沒有」（實際只查過 v5.1.0、v6.3.0）、「改名或移除會被 PRECHECK 擋下」（只對必要 skill 成立）。三次都在送審前自己抓到，但同一個病一天內出現三次——全域守則記的「修正動作本身是高發場景」再次成立。
- 🟡 [painful | evidence: `文檔/handoff/session-handoff-20261005.md` 第 93–95 行、brainstorm.md 第 111、128 行] **重問已裁定的問題，並把已撤銷的依賴當成現行事實。** 10/05 已裁定「只修 executing-plans 理由、不重評 fallback」，且「紅旗改寫不可先行、須隨 apply schema change」的依賴已撤銷（非正式設計要求；工作地圖該段文字是刻意留到重新登記時才改的舊文字）。本 session 只讀 10/06 handoff、沒有回查 10/05，誤把工作地圖殘留文字當成有效約束，並重問了已裁定的 B-i。最終決定與 10/05 裁定一致，所以實作不受影響；但 brainstorm.md 第 111、128 行把「不可先行」寫成現況，第 128 行並用它當保留禁令的理由之一（design.md 的 Risks 段指回 brainstorm §三）——**以本條為準，brainstorm 原文保留不改**。由歸檔後的文件審查發現。
- 📌 [nit | evidence: verify.md 建議項] tasks、plan、design 把 `schema.yaml` 第 8–12 行稱為「檔頭註解」，實際上是 YAML `description:` 的值，CLI 會讀。使用者裁定只記錄、不修。
- 📌 [nit | evidence: 本 session 工具紀錄] 同步 dogfood 副本時 `rm -rf` 被權限擋下，改用 `cp` 覆蓋加 `diff -rq` 驗證相同。

## 3. Plan deviations

| Plan task | What changed | Why |
|-----------|--------------|-----|
| 2.3（新增） | 文件審 r1 後新增：改寫兩份 README § 2 的維護說明 | r1 🔴：該節宣稱上游行為改版時 schema 不必修改，與本 change 矛盾 |
| 3.2 | Acceptance 從「命中只剩歷史紀錄」改為允許四類命中 | 文件審 r1 🟡：歸檔前 living spec 仍是舊文、change 文件會引用舊說法，原條件照字面不可能成立 |
| （新增，verify 之後） | 兩份 README：S13/S14 紀錄段後補一行「後續狀態（2026-10-06）」；四個 executing-plans 連結由 `main` 改指 `v6.4.1` 標籤 | verify 建議項；使用者裁定修這兩項（不回頭改 10/02 紀錄、證據來源要固定版本）。這兩處改動在 verify 之後，由歸檔前的文件審把關 |
| （新增，歸檔後） | 兩份 README § Fallback strategy 的 `apply` 列補上「沒有每個 task 的審查」「無 subagent 時最後審查由作者自做」 | 歸檔後文件審查 🟡：REQ-3-S3 要求每個理由段落都陳述這兩件事，該列原本只寫「完全沒有獨立審查」，規格比實作嚴；使用者裁定現在修 |
| precommit | precommit-runner 回報 `⚠️ NO CHECKS RUN`，改跑本 repo CLAUDE.md 明定的唯一測試並記 pass | 本 repo 沒有 lint / build / test 腳本；已在對話中留 `[DEVIATION]` 紀錄 |

## 4. Skill / workflow compliance

| Skill                                            | Used |
|--------------------------------------------------|------|
| superpowers:brainstorming                        | ✓（分類為 bounded；決策在對話中逐段取得使用者同意，產出原樣寫入 brainstorm.md） |
| superpowers:using-git-worktrees                  | ✗（見下） |
| superpowers:subagent-driven-development          | ✗（見下） |
| superpowers:test-driven-development (✓ only if the skill was explicitly invoked; write `N/A — annotation-driven` when TDD discipline came from the `TDD:` annotations in `tasks.md` and their RED/GREEN evidence instead) | N/A — annotation-driven（7 個 task 全為 `TDD: n/a`，理由經 verify R3 判定成立） |
| (structural via SDD) superpowers:requesting-code-review | ✗ 未經 SDD；審查改由 Codex 外部審查承擔（文件審 2 輪、程式碼審 1 輪）＋獨立 verify 執行者 |
| superpowers:finishing-a-development-branch       | ✗（見下） |

> 本表只列兩類項目:(1) schema 明確要求呼叫的 Superpowers skill——
> `brainstorming`(由 `brainstorm` artifact 要求)與 apply pre-flight 要求的
> `using-git-worktrees`、`subagent-driven-development`、`finishing-a-development-branch`;
> (2) schema 要求落實、retrospective 必須記錄其執行情況,但 schema 本身不直接呼叫的
> Superpowers 紀律——`test-driven-development`(由 `tasks.md` 的 `TDD:` 標註與
> RED/GREEN 證據承載)與 `requesting-code-review`(透過 subagent-driven-development
> 結構性達成)。

### Deliberately Skipped Skills

- **`superpowers:using-git-worktrees` + `superpowers:subagent-driven-development` + `superpowers:requesting-code-review`（結構性）**
  - **What was skipped**: 整個 worktree 隔離與 SDD 執行器，因此也沒有 SDD 內建的每任務審查；改為主 session inline 執行，品質由外部審查多輪把關。
  - **Why this cycle**: design.md D5 事前決定並經使用者同意（brainstorm Q6）。判準：全是文字更正（7 個 task 全 `TDD: n/a`）、變更面在 design 凍結為 5 個表面、dogfood 副本在 worktree 內會與主 tree 的 opsx 指令互踩。
  - **How to prevent recurrence**: `scope-judgment rule` — 「純措辭的更正型 change：外部審查多輪＋獨立 verify 可取代 SDD 的審查結構」。**這是第二次**（先例 `openspec/changes/archive/2026-08-31-fix-tdd-transitive-claim/retrospective.md` 第 69–72 行，同一個 How to prevent），依本節規則升到 §6。
- **`superpowers:finishing-a-development-branch`**
  - **What was skipped**: 整個 skill。
  - **Why this cycle**: 沒有開分支、沒有 worktree，實作直接在 main 上 commit（`9ef62c2`，經使用者逐次授權），沒有分支可以收尾。
  - **How to prevent recurrence**: `scope-judgment rule` — 跟著上一條：不開 worktree 時本 skill 沒有作用對象；若上一條升級為 schema 規則，本列應一併納入。

## 5. Surprises

- **錯誤說法是正式規格強制的。** 原以為只是文件寫錯，實際上 REQ-3 用 SHALL 規定了舊理由。
- **8/31 沒有查錯。** v6.3.0 原文（`executing-plans/SKILL.md:14`）就是「有 subagent 就改用 SDD」，是上游 v6.4.1 改版後才失效。
- **舊說法在 fallback 情境一半仍然成立。** v6.4.1 在沒有 subagent 時由作者自審，所以「不派獨立審查者」對 fallback 情境是對的，只對有 subagent 的情境錯。
- **`schema.yaml` 第 8–12 行不是註解。** 是 YAML `description:` 的值，CLI 會讀（verify 發現）。

## 6. Promote candidates → long-term learning

- [ ] 🟡 **純措辭更正型 change 的執行路徑應明文化（第二次同樣跳過 worktree / SDD）** → **Promote to** schema（apply instruction）——併入 `task-20260901-claudemd-governance-rewrite` 一起處理
  > **Why**: 8/31 `fix-tdd-transitive-claim` 與本 change 都以「外部審查多輪＋獨立 verify」取代 SDD，How to prevent 答案相同；照 §4 規則這是 schema 層的訊號。正式設計 §5「execution-path agnostic, contract-governed」也要求任何執行路徑只要具備所需能力或依規降級並留紀錄即可。
  > **How to apply**: 處理 governance-rewrite 時，把「沒有 SDD 時以何種審查與紀錄滿足 Independent Review」寫成能力與證據要求，而不是點名禁止或允許某個執行器。
- [ ] 🟡 **修「上游改版讓宣稱失效」時，一併搜「怎麼處理上游改版」的後設說法** → **Promote to** memory（type: feedback）——Hypothesis，目前 1 例
  > **Why**: 本 change 只搜了 executing-plans 這個詞，漏掉 README § 2「上游行為改了 schema 不用改」，被文件審 r1 抓到。
  > **How to apply**: 處理 drift issue 或任何「上游改版導致說法錯誤」的修正時，除了搜被推翻的具體說法，也搜 compatibility / upgrade / 「不用改」類的維護說明。
- [ ] 📌 **引用上游原文作為查證依據時，連結指向固定版本標籤，並先驗證該標籤內容與實際查證的檔案相同** → **Promote to** bridge README 撰寫慣例（或 CLAUDE.md「雙語策略」附近）——待使用者決定
  > **Why**: verify 發現 README 寫「v6.4.1–v6.4.2 查證」卻連到 `main`；上游再改時，連結內容會跟文字對不上。
  > **How to apply**: 在 README、spec、報告中寫「依上游 X 版原文」並附連結時。
