# Retrospective: fix-tdd-transitive-claim

> Written: 2026-08-31 (after verify passed)
> Commit range: `af10e67..280b987`
> Worktree: main(inline;docs-only corrective fix,單 session)

---

## 0. Evidence

- **Commit range**: `af10e67..280b987` (4 commits)
- **Diff size**: +654 / -89 lines across 13 files(修正面 +105/-89 across 8;artifacts +549 across 5)
- **Tasks done**: 12/12 (`grep -cE '^\s*- \[x\]' tasks.md` → 12)
- **Active hours**: ~1.5(單 session,2026-08-31 上午)
- **Subagent dispatches**: 2(fallback code reviewer 首審 + 複驗,同一 general-purpose agent 複用)
- **New external dependencies**: none
- **Bugs encountered post-merge**: none(尚未 push)
- **OpenSpec validate state at archive**: pass(--all 2/2;schema validate + schemas smoke 皆綠)
- **Test coverage signal**: n/a(無測試框架 repo;等效驗證 = validate + smoke + 雙面審查鏈)

Commit chain (時序):

```
7bfd3c8 fix(schema): replace false TDD-enforcement claim with honest conditional statement
8b9f48c docs(bridge): correct TDD claims and executing-plans rationale in both READMEs
529afd0 docs: correct remaining TDD false-premise surfaces and bump bundle to 1.0.1
280b987 docs(openspec): add fix-tdd-transitive-claim change artifacts
```

---

## 1. Wins

- [evidence: 7bfd3c8 + grep NO RESIDUE] 假保證本體(`internally enforces` / `do NOT need to invoke` / `TDD-via-subagents`)在全部 current-authority 面清零,替代句全為條件式、負向以 **guarantees** 圈定。
- [evidence: 審查鏈 code 4+2 輪、doc 4 輪] 每輪修正都交回審查者複驗,共抓出 **13 個 blocking finding**——其中至少 3 個是「修 A 時寫出的新絕對句」(brainstorm §五 同型病的第 10、11 次實例),證明外部複驗在這類 change 是必要層不是儀式。
- [evidence: 8b9f48c] en/zh README 逐段對稱落地,同 commit 收(跨檔耦合表要求)。
- [evidence: Codex round 1 finding #5 → 529afd0/7bfd3c8] 審查抓到凍結清單外的第 6 個 schema 段(schema 內建 retrospective 指令的同型誘導)——凍結清單「不得當窮舉證明」的預言成真,補償控制(外部審查)如設計運作。
- [evidence: `[REVIEWER_FALLBACK]` 記錄 + fallback ✅ Ready×NONE] Codex 額度第 5 次中斷,fallback 鏈零停等接手並收案。

## 2. Misses

- 🟡 [painful | evidence: round-2 code finding #1] 修「invoked per task」時寫出鏡像絕對句「nothing invokes that skill separately」——與 brainstorm §五 #8 完全同型,在明知這個病的 change 裡再犯。外部審查攔下。
- 🟡 [painful | evidence: doc rounds 2-4] plan.md 內嵌的措辭 snippet 隨每輪審查漂移,追平成本吃掉兩輪 doc review;plan 把交付句字面寫死的做法對「措辭會被審查迭代」的 change 是負資產。
- 📌 [nit | evidence: 0-byte /tmp msg file] smart-commit 的 alloc(Git Bash /tmp)與 Write 工具的 /tmp 是不同目錄,首次寫入落空——被「消費端 runtime 驗非空」擋下,全域規則 N=5 的同型第 6 例。

## 3. Plan deviations

| Plan task | What changed | Why |
|-----------|--------------|-----|
| Task 2 Step 1(:304/:368/:383)| 措辭經 doc review 三輪收斂為「TDD discipline via plan content;skill 不被 precheck/invoke」 | 審查指出「followed by the implementer」仍可讀成 skill 使用宣稱 |
| Task 3 | 新增 Step 0:schema 內建 retrospective 指令的誘導段(凍結清單外第 6 段) | code review round 1 finding #5 |
| tasks.md 2.1「keep rows 500/501 unchanged」 | 改為過去式指涉 | 刪本體後該兩列懸空、自身變不實;[DEVIATION] 已當輪聲明 |
| 3 commits 計畫 | 實際 4 commits(artifacts 另一筆) | change artifacts 與修正面分開更乾淨 |

## 4. Skill / workflow compliance

| Skill                                            | Used |
|--------------------------------------------------|------|
| superpowers:brainstorming                        | ✓(8/27 既有 brainstorm.md,本 cycle 承接) |
| superpowers:writing-plans                        | ✓ |
| superpowers:using-git-worktrees                  | ✗(見下) |
| superpowers:subagent-driven-development          | ✗(見下) |
| superpowers:test-driven-development (✓ only if the skill was explicitly invoked; write `N/A — plan-step TDD only` when TDD discipline came from plan steps alone) | N/A — 純 prose change,plan 未帶 TDD 步驟(上游明訂 prose 不需測試);等效驗證為 validate + smoke + 雙面審查鏈 |
| (structural via SDD) superpowers:requesting-code-review | N/A — 未走 SDD;審查由 Codex/fallback 審查鏈承擔(4+2 輪 code、4 輪 doc,嚴格度不低於單次 reviewer dispatch) |
| superpowers:finishing-a-development-branch       | ✗(見下) |

### Deliberately Skipped Skills

- **`superpowers:using-git-worktrees` + `superpowers:subagent-driven-development`**
  - **What was skipped**: 整個 worktree 隔離 + SDD 執行器,改為 maintainer inline 執行(plan 表頭有明載)。
  - **Why this cycle**: docs-only corrective fix、單 session、變更面已凍結且全在文字層;dogfood 同步(`openspec/schemas/` 副本)在 worktree 內會與主 tree 的 opsx 指令互相踩;實際觸發點 = plan.md 表頭「In this repo the maintainer executes inline」+ 使用者核准的 4-commit 計畫直接落在 main。
  - **How to prevent recurrence**: `scope-judgment rule` — docs-are-the-product repo 的純措辭 corrective fix,審查鏈(外部 reviewer 多輪複驗)即等效於 SDD 的 reviewer 結構;下個含可執行行為的 change 仍應走 worktree + SDD,判準是「有無可執行行為」不是「檔案多寡」。
- **`superpowers:finishing-a-development-branch`**
  - **What was skipped**: 整個 skill。
  - **Why this cycle**: 無 feature branch——工作直接在 main(上一條的下游結果);無「合回」動作可做,push 另走 /push-ci 核准。
  - **How to prevent recurrence**: 同上一條 scope-judgment rule 的附帶結果;恢復 worktree 流程時自然恢復。

## 5. Surprises

- schema.yaml 自己的 retrospective 指令段藏著與模板同型的誘導(「Default expectation: 全部 ✓」)——凍結清單三條掃描路徑全沒抓到,因為它一個 TDD 關鍵字都沒有;與 brainstorm §4.1a 的預言完全一致:「宣稱自動發生」不可用精確搜尋窮舉。
- OpenSpec spec validator 只檢查 requirement 首行有無 SHALL/MUST——「MUST NOT」在第二行就報錯,措辭得遷就 parser。

## 6. Promote candidates → long-term learning

- [ ] 🟡 **修絕對句時寫出的替代句要當場再過一次例外檢查——即使(尤其)在修這個病的 change 裡** → **One-off**(全域 CLAUDE.md「證據先於斷言」已有此條;本 cycle 是它的第 10/11 個實證,不新增規則,樣本記在 handoff)
  > **Why**: round-2 的「nothing invokes that skill separately」與 brainstorm §五 #8 完全同型,發生在對此病最有戒心的 change 裡。
  > **How to apply**: 既有全域條文;本例作為 N+1 樣本支持其不可放寬。
- [ ] 📌 **plan.md 不要把「會被審查迭代的交付句」字面寫死,寫「終稿以 spec 條文與審查收斂為準」+ 指向 spec** → **One-off**(先觀察;若下個 change 再發生 plan 追平成本,升為 schema plan.instruction 的一句話)
  > **Why**: 本 cycle plan snippet 漂移吃掉兩輪 doc review。
  > **How to apply**: 寫 plan 時,凡是「將寫進交付物的措辭」引用 spec requirement 而非內嵌全文。
- [ ] 📌 **smart-commit alloc 的 /tmp 訊息檔在 Windows 要先 cygpath 再 Write** → **Promote to memory** (type: feedback,本專案 memory)
  > **Why**: Write 工具的 /tmp 與 Git Bash /tmp 不同目錄,首寫落空 0 bytes;「消費端驗非空」攔下。
  > **How to apply**: 本 repo 任何 /smart-commit --execute 的 Write 步驟,一律 `cygpath -w` 解出 Windows 路徑後再寫,commit 前 `wc -c` 驗非空。
