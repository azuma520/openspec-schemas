# 需求追溯（Identity + Reference）現況盤點與缺口分析（2026-09-23）

> **定位：current-state / gap analysis，不是設計、不是提案。**
> **不取代** 2026-09-01 已核可的[正式設計](../specs/2026-09-01-bridge-guarantee-formal-design.md)；
> 本文只回答「一份外部討論交接提出的『Identity + Artifact Structure + Reference + Verification』構想，
> 與 repo 現況差多少」。第 7 節的設計決定留待使用者逐題裁定。
>
> **方法**：repo 內檔案實讀；上游 OpenSpec 讀本機已安裝 1.3.1 的 `dist/` 原始碼（關鍵句本人抽查過）；
> Spec Kit 讀 `github/spec-kit` `main` 分支 `67ab049`（2026-09-23 下載）的 templates；Issue #4 缺陷清單由
> 一個唯讀 subagent 逐份讀取後分類，本人抽查其中三項事實（見 §8）。**推論一律標【推論】**，未標者為讀到的事實。

---

## 0. 結論摘要

交接描述的方向**大部分已在正式設計 §3 拍板**，S1 spike 也已選定載體；缺的是**實作**——
Core Integrity Invariants 的 I1–I3（正式設計 §2.1）在 `schema.yaml` 裡零行，工作地圖上也沒有任何一條
承接它的實作工作。

同時，盤點抓到三處**正式設計與後來實作演化之間的衝突**（§3 ①②③），在任何實作之前需要先裁。

---

## 1. 現況地圖

| 能力 | 設計狀態 | 實作狀態 | 證據位置 |
|---|---|---|---|
| Requirement stable ID | 已決（正式設計 §3.1：heading 載體、immutable、fail-closed、不建 registry） | 只有 1 條 requirement 用了 `REQ-PB`；其餘 10 條正式 requirement 都沒有 ID | `openspec/specs/repo-guidance/spec.md:11`；`openspec/specs/{plan-contract,tdd-claim-accuracy,tdd-evidence-contract}/spec.md` 標題 |
| Scenario ID | 已決（`REQ-12-S1`；S1 拍板 A：標題載體） | 無任何真實使用；PoC fixture 用名稱指向（`REQ-A/happy path`） | `docs/superpowers/poc/2026-09-01-capability-spikes/spike-report.md` S1；`poc/2026-08-28-traceability-gate/fixture/.../tasks.md` |
| Task → Requirement | 已決（`- Contracts:`，縮排嚴格深於 checkbox；Requirement→Task 必須全覆蓋、Task→Contract 不強制） | 僅 PoC 與 `claude-md-phase-boundary` specimen；schema 未寫 | 正式設計 §3.2；`poc-report.md` |
| **Task → Design Decision** | 無設計 | **實務上一直在用**：已歸檔 change 的 tasks 寫「per D1」「per D2/D3」；2 個 change 以 Decision 引用為主，`loosen-plan` 相反（見 §3 ①） | `fix-tdd-transitive-claim`、`loosen-plan`、`fix-v2-blocking-defects` 的 `tasks.md` |
| **Task → 測試證據** | 正式設計 §4.3 原設想經驗證結果（`method = automated-test`）承載 | **已實作且會擋**：每個 `TDD: applicable` task 底下 RED/GREEN 紀錄、`subject: <檔>::<測試名>`，checks 8–11 | `superpowers-bridge/schema.yaml` checks 8–11（`loosen-plan` 起） |
| Task ↔ plan | — | 已實作：task 編號 1:1，check 12（兩階段） | `schema.yaml` check 12 |
| Decision → Requirement | 無設計 | verify check 4 每次動態重建成表（非阻塞）。實例：fix-v2 的 D1–D4 各自對到 requirement，D5 / D6 **無對應 requirement** | `schema.yaml` check 4；`openspec/changes/archive/2026-09-14-fix-v2-blocking-defects/verify.md:104-117` |
| Verification → Scenario | 已決（Result 的 `contract` 欄須能指認 Scenario；S5 拍板 change 目錄內 `verification-results.json`） | 未實作；verify.md 無任何逐條 requirement / scenario 覆蓋檢查。既有樣本只有 requirement 粒度、都無 Scenario 指認：真實 change 唯一一份是 PoC specimen（`contract: REQ-PB`），另有 PoC fixture（`REQ-A`…`REQ-F`，`docs/superpowers/poc/2026-08-28-traceability-gate/fixture/openspec/changes/poc-traceability/verification-results.json`） | 正式設計 §3.4；`schema.yaml` checks 1–12；`openspec/changes/archive/2026-08-31-claude-md-phase-boundary/verification-results.json` |
| Completion Gate | 已決（§7） | 只有 PoC throwaway `gate_check.py` | `poc/2026-08-28-traceability-gate/` |
| Code 為 reference 載體 | 正式設計未列入 | 無 | — |

### 上游事實

**OpenSpec 1.3.1**（安裝於 `~/.bun/install/global/node_modules/@fission-ai/openspec/`，路徑以其 `dist/core/` 為基準）：

- Requirement 身分 = 標題文字 trim 後的結果，大小寫敏感（`parsers/requirement-blocks.js`：`normalizeRequirementName(name) { return name.trim(); }`）。
- 歸檔合併以名稱對應，順序 RENAMED → REMOVED → MODIFIED → ADDED；**MODIFIED 整塊替換**（`specs-apply.js`：`nameToBlock.set(key, mod)`）。RENAMED 語法 `- FROM:` / `- TO:`。
- Scenario 在 CLI 無身分：`ScenarioSchema` 只有 `rawText`，標題名不存。
- **兩條合併路徑不一致**：`templates/workflows/sync-specs.js` 教 agent「Unlike programmatic merging, you can apply **partial updates** … To add a scenario, just include that scenario under MODIFIED - don't copy existing scenarios」；CLI archive 對同一份 MODIFIED 會整塊替換。
- `validate`：MUST/SHALL 關鍵字、至少一個 `####`（任何四級標題都算）、各類重複 / 跨區段衝突；`**ID**:` 這類 metadata 行被跳過、內容不使用。**無 ID 格式、無 traceability**（整個已安裝套件不分大小寫搜 `traceab`、`REQ-[0-9]`：0 筆命中；上述跳過 `**ID**` 的是 `validation/validator.js` 的一行註解，與此搜尋無關）。
- verify workflow（`templates/workflows/verify-change.js`）每次重新以關鍵字搜程式碼（「Search codebase for keywords related to the requirement」），結果只出現在對話報告，不存檔。
- schema artifact 欄位：`id` / `generates` / `description` / `template`（必填）、`instruction`、`requires`；`apply` 有 `requires` / `tracks` / `instruction`。【推論】zod 預設會丟棄未知鍵、不報錯。

**Spec Kit**（`67ab049`）：

- `FR-001` 為 requirement key；`SC-001` 是 **Success Criteria**（可量測指標），**不是** Scenario；acceptance scenarios 為無 ID 的編號清單，`converge` 以位置引用（`US1/AC2`）。
- Task 格式 `T012 [P] [US1] …`，**只掛 story、不掛 FR**；例外是 `converge` 追加的 task 寫 `per FR-003`。
- `analyze` 唯讀、每次重算覆蓋表（`| Requirement Key | Has Task? | Task IDs |`），只要求重跑結果一致；不存 requirement → code 對應。

---

## 2. 缺口表

| 構想 | repo 現況 | 已有？ | 缺口 | 最小補法 | 需要新機制？ | 證據位置 |
|---|---|---|---|---|---|---|
| Requirement ID | 設計已定、1 條在用 | 設計有、實作無 | schema 指令與模板未寫；**ID 的唯一範圍（全 repo / 每 capability）與 REMOVED 後可否重用**未定義 | spec 指令與模板加寫法 + 一條 verify 檢查 | 否 | 正式設計 §3.1；`repo-guidance/spec.md:11` |
| Scenario ID | 設計已定 | 設計有 | CLI 整塊替換 + 上游 sync skill 的 partial update 指示 → Scenario（連同 ID）可能被無聲丟掉 | Gate 比對歸檔前後 Scenario ID 集合 | 否，但需處理此風險 | spike S1；上游 `sync-specs.js` / `specs-apply.js`。bridge 已有部分緩解：spec 指令要求 MODIFIED「MUST include full updated content」（`schema.yaml:134`），與上游 sync skill 的 partial update 指示相反；殘餘風險是 agent 改照上游 sync skill 走 |
| Task → Requirement | 設計已定、PoC 證過 | 部分 | schema 未寫 | `Contracts:` + 存在 / 覆蓋檢查（沿用 PoC 邏輯） | 否 | 正式設計 §3.2；`poc-report.md` |
| Decision → Requirement | check 4 動態重建 | **已有、未利用** | 不存、不擋 | 維持動態；至多 Decision 可選填 `Serves: REQ-x` | 否 | check 4；fix-v2 `verify.md:104-117` |
| Decision 自身 ID | 模板建議 `### D1`，實務普遍使用並被引用 | **已有** | 只在單一 change 內有效 | 不用做，只需正式承認 | 否 | `templates/design.md`；已歸檔 change 的 tasks / plan / verify |
| Verification → Scenario | 設計已定 | 無 | 與已實作的 Task 層 RED/GREEN 形成**雙證據載體**（§3 ②） | 待裁 | 待定 | 正式設計 §3.4、§4.3；`schema.yaml` checks 8–11 |
| Code 不為正式載體 | 正式設計本來就沒列 | 一致 | — | — | 否 | — |
| 不加 relation type | 正式設計本來就沒有 | 一致 | — | — | 否 | 正式設計 §3 |
| Proposal → Requirement | proposal 只列 capability 名稱（capability 粒度） | 無 | requirement 粒度的漏列抓不到（§4.1 #8，即 09-21 盤點的資訊項 I5——非正式設計的 invariant I5） | proposal 列出 requirement ID，與 delta 做集合比對 | 否 | `templates/proposal.md`；§4.1 #8 |

> **2026-09-24 註（後續裁定已推翻本表最後一列的「最小補法」）**：2026-09-23 裁定撤回「Proposal → Requirement ID」——Proposal 的責任是 change 立案/意圖/範圍，維持 capability 粒度，不維護 requirement ID 清單（見 `文檔/handoff/session-handoff-20260923.md` 的 Session 16：40 裁定快照）。依據是其後定為上位原則的「先定 Artifact 責任、結構化副本仍是副本」（2026-09-24 核可版正式設計（`docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`，commit `8002fa0`） §1）。核可版正式設計本身沒有 Proposal 粒度的條文；本列保留作為當時的分析。

---

## 3. 反例：交接構想中不成立或與現況衝突之處

**① 「Design Decision 一開始不需要 ID」與現況相反。** Decision 早就有 ID，而且是實務上被引用最多的單位：4 個已歸檔 change 中 3 個各有 6–7 條 `### D<n>`，且每一個都被 tasks / plan / verify（部分含 retrospective、errata）引用。**多數情況下 Task 實際掛的是 Decision，不是 Requirement**——以行數計（`grep -ciE 'requirement|REQ-|scenario'` 對 `grep -cE '\bD[0-9]+\b'`），`fix-tdd-transitive-claim` 為 1 對 7、`fix-v2-blocking-defects` 為 1 對 6；**`loosen-plan` 相反**，為 3 對 1（`tasks.md:62,74,83` 以名稱或序號引用 requirement / Scenario）。另 fix-v2 的 D5（版本號）、D6（雙語 README 同步）屬流程決策，本來就無對應 requirement ⇒ Decision → Requirement 只能選填。

**② 驗證落點與已實作的載體衝突。** 目前唯一會擋的證據載體（RED/GREEN）綁在 **Task** 上，不是 Scenario。若再依正式設計 §3.4 新增以 Scenario 為單位的 `verification-results.json`，同一個測試證據會有兩個記錄處。`loosen-plan` 把 TDD 證據放進 `tasks.md`，【推論】實質上已偏離正式設計 §4.3 當初的承載設想，而這個偏離未被寫回正式設計。

**③ 「wording change → ID 不變」只有一半成立。** ID 放在標題 ⇒ 標題描述文字一改，OpenSpec 就視為另一個身分，必須走 RENAMED FROM/TO。RENAMED 本身可以保留同一個 ID，但需要一條檢查「RENAMED 前後 ID 相同」；否則 ID 可以隨 RENAMED 被無聲換掉。內文措辭改動（標題不變）則走 MODIFIED，ID 不受影響。

**④ Verification 不一定適合落到 Scenario。** Issue #4 的主要驗證對象是 `decision-matrix.md` 的列（L1–L15、M1–M17：輸入狀態 → 判定），不是 Scenario；且 56 個測試函式只有 3 處帶列號（L9、M7、M7），而該矩陣宣稱「每列都有測試、列↔測試對照在測試模組 docstring」——docstring 內並無該表。
Task 不屬於任何 requirement 的情形合理，正式設計 §3.2 已允許（鷹架、雜項）。

**⑤ active 與 archived 的 reference 會混淆，除非補一條規則。** 已歸檔 change 的 `Contracts:` 會指向之後被 MODIFIED / REMOVED 的 requirement。只要 ID 不可變**且刪除後不重用**，舊 reference 就只是歷史紀錄、不會誤指；目前只有「不可變」，**沒有「不重用」**。

**⑥ 已有機制不應另造**：rename 已有 OpenSpec RENAMED；Decision → Requirement 對應已有 check 4；requirement → code 的動態重建已有上游 verify workflow。

---

## 4. 真實案例檢驗

### 4.1 Issue #4（workflow-harness `fix-worktree-canonical-root`）18 項實際缺陷

判定：**1** = IDs + reference + 機械存在 / 覆蓋檢查能抓到；**2** = 讓審查者較易找到；**3** = 無幫助。

| # | 缺陷 | 類型 | 判定 | 理由 |
|---|---|---|---|---|
| 1 | 初版 D2 把所有非標準 git 佈局都 fallback 到 harness root，bare / `--separate-git-dir` 解析錯 | 例外分支 vs 規格例外 | 3 | 佈局清單本身不完整，reference 指不到沒人列出的佈局 |
| 2 | `.git` 用 `Path.is_file()` 判斷，會跟隨 symlink | 其他 | 3 | 函式庫行為，靠對抗式審查發現 |
| 3 | junction 測試根本沒走到新 guard，「變異會轉紅」已公開貼在 Issue #4 | 測試名 > 斷言 | 3 | 只有「點名哪條轉紅」的變異檢查能抓 |
| 4 | 給 agent 的路徑相對主樹，worktree 內會讀到過期副本；測試只斷言檔名 | proposal 漏 + 測試弱 | 3 | 當時該 requirement 還不存在（事後才新增），覆蓋檢查抓不到沒寫的需求 |
| 5 | 「修一整類」掃描加了相對 state root 的 Read 比對，把讀過期副本當合法 | 理解不一致 | 3 | 前提錯；reference 反而會把錯的改動「連」到 scenario |
| 6 | 兩個 Layer-2 擋下分支沒給檔案位置 | proposal 漏 | 3 | 程式分支不是 reference 載體 |
| 7 | design 寫「3 份 live spec」，證據 E2 引用的 spec 其實沒提 marker | 其他 | 2 | 引用單條 requirement ID 比引用整份 spec 更易看出不符，但存在檢查會過 |
| 8 | proposal 漏列 handoff-guard 第二條 MODIFIED requirement，「刻意不動」與 delta 矛盾 | proposal 漏 / 舊說法殘留 | 1（漏列）、2（矛盾） | proposal 清單 vs delta MODIFIED 集合是純集合比對 |
| 9 | 測試數量反覆過期（27/7/9 vs 38/11/11，再到 42、45、48…） | 舊說法殘留 | 3 | 衍生數字，不是 reference |
| 10 | root 解析不出時靜默 fallback 到 worktree，且 spec 允許 | 理解不一致 / 例外分支 | 3 | 契約本身不安全，屬判斷 |
| 11 | proposal 暗示資料遺失的生命週期已關閉，但寫入端不在範圍內 | 其他 | 2 | 目標 → REQ 對照會顯示沒有 requirement 涵蓋寫入端；比對散文主張不是機械的 |
| 12 | 沒接 `RuntimeError`；修了三處，下一輪在 `artifact_paths.py` 再現；掃描台帳計數也錯 | 例外分支 | 3 | 需要 AST 掃描（動態發現） |
| 13 | 名為真 `--separate-git-dir` 主樹的測試實際建的是缺 `commondir` 的 worktree；L2 測試只比一個提示 | 測試名 > 斷言 | 3 | 斷言強度，不是連結 |
| 14 | **P0**：缺 `commondir` 被當成主樹；測試、docstring、程式註解、spec **一致地錯** | 全部一致但全錯 | 3，且更糟 | reference 會顯示完全對齊，給出錯誤安心 |
| 15 | 後續兩次修正同型錯誤（看目錄名 `worktrees`；把缺反向指標檔當主樹證據） | 其他 | 3 | 只有真 git 佈局實測抓得到 |
| 16 | 三條自寫測試假綠（Python 3.13 symlink loop 不拋、argv `--root` 被忽略、家目錄本身是 repo）；S3 `¬repo_evidence` 分支零測試 | 測試名 > 斷言 | 3 | 全由變異檢查發現 |
| 17 | 09-23 各輪：子目錄 root 把「沒有 `.git`」當證據、`config` 只 stat 未 open、懸空 symlink、`lstat` 錯誤被吸收、兩 marker 只驗一邊、Stop 訊息誤稱有 `.git`、no-spawn 守門名實不符 | 例外分支 / 測試弱 | 3 | 對稱對與列舉缺口 |
| 18 | 舊模型措辭殘留（design D9 表、「矩陣是唯一來源」、spec 的 `worktrees` 判別） | 舊說法殘留 | 2（部分 1） | D2 若有 superseded-by 連結，指向它的地方會被標出；決策內部的過期散文仍會通過存在檢查 |

**分布**（依上表逐列計數）：**3 = 14 項**（#1–6、#9、#10、#12–17）；**2 = 3 項**（#7、#11、#18）；**1 = 1 項**（#8 的漏列部分）。另有部分判定：#8 的矛盾部分判 2、#18 部分判 1。⇒ 18 項中**有任何幫助的是 4 項**（#7、#8、#11、#18），其中可機械抓到 1 項（加部分則 2 項）；**無幫助 14 項**。**最嚴重的兩件（#14 P0、#10）無幫助**；#14、#5【推論】reference 會增加錯誤信心而不增加正確性。
來源：workflow-harness worktree `openspec/changes/fix-worktree-canonical-root/`（proposal、design、tasks、plan、decision-matrix、brainstorm、self-review-degraded、red-evidence、resolve-exception-sweep、spec 標題）、`文檔/handoff/session-handoff-20260915.md`～`20260923.md`。

### 4.2 交叉對照

- **fix-v2 的規則 × 表面缺口**：9 條規則在指令 / check / 模板三個表面之一缺席（`docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/codegate-fixes-report.md` §matrix）。判定 1——前提是每條規則有 ID、每個表面宣告它必須承載哪些規則；那份手工矩陣本身就是一張追溯矩陣。
- **舊措辭存活是因為掃描搜的是新詞**（`docs/superpowers/retrospectives/2026-09-14-fix-v2-round-learnings.md` §1.2 樣本 2b）：判定 2——搜 ID 能找到任何措辭的重述，前提是重述有標 ID。
- **已經在抓東西的機械檢查**：workflow-harness `hooks/lib/change_delta_integrity.py` 的 `check_promise_coverage` 以反引號識別字比對 spec 與 `tasks.md`，曾正確擋下 `repo_evidence` 等 spec 引入但無 task 承接的概念（handoff 0922 追記二）。
- **09-21 資訊項盤點**：17 項中無一由自動化機制發現；8 項 semantic sync 中 7 項的比對對象是散文（[`2026-09-21-issue4-information-item-inventory.md`](./2026-09-21-issue4-information-item-inventory.md)）。

**ID 真正發揮的地方是「兩個集合互相比對」**：proposal vs delta、規則 × 表面、矩陣列 vs 測試、spec 概念 vs task。這些對應**多半不在交接列的三個載體（Decision / Task / Verification）上**。

---

## 5. 技術意見

- **方向自然**：與 OpenSpec「每次重新發現 code 對應」、Spec Kit「穩定 key + 每次重算」一致，且已被正式設計核可。
- **值得保留**：Requirement ID、`Contracts:`、code 對應動態重建、不加 relation type。
- **需要先裁的衝突**：§3 ①（Decision ID）、②（雙證據載體）、③（RENAMED 保 ID）。
- **預期效益應校正**：以 Issue #4 為樣本（n=1），reference 在 18 項中有 4 項（約 22%：#7、#8、#11、#18）可抓到或協助找到，其中可機械抓到 1 項（部分 2 項），且不是最痛的那幾類；§4.2 的 fix-v2 規則 × 表面缺口與 `check_promise_coverage` 是另外的正面樣本，不計入這 18 項；最痛的仍靠變異檢查、真 git 佈局實測、獨立審查。它的價值是**替審查者列出該看的地方，並讓集合比對比名稱比對更穩**，不是正確性保證。

## 6. 最小可驗證方向（只描述形狀）

1. **不動 schema 的回溯實驗**：取 Issue #4 與 fix-v2 各一份複本，手動補 ID、`Contracts:` 與 proposal → requirement 清單，用 PoC 現成的 `gate_check.py` 跑，數它實際能抓到幾個已知缺陷。
2. 結果若值得，再開一個 opsx change，只做 I1 + I2（requirement ID + task 覆蓋）與一條 verify 檢查；Scenario 層與 Result JSON 延後。⚠️ 這一步**與正式設計 §9.3 衝突**：該節明定「Scenario identity + Scenario-level Verification coverage 是 v1 必做（I3 依賴它，不可延後）」。所以「先做 I1 + I2、延後 Scenario」不能在實作 change 裡順手決定，要先經 §7 第 7 題裁定。

## 7. 需要使用者裁定的事

1. 是否排入 I1–I3 實作；與進行中的 Q8 實驗、workflow-harness Issue #4 審查的先後。
2. 驗證證據的錨點：Task（現況）、Scenario（正式設計），或由 Task → Scenario 推導。
3. 是否正式承認 Decision ID（`D<n>`）為引用載體。
4. ID 唯一範圍（全 repo / 每 capability）、REMOVED 後可否重用、現有 10 條無 ID 正式 requirement 是否補 ID。
5. proposal 是否列出 requirement ID（唯一能機械抓到 §4.1 #8 類缺陷的做法）。
   > **2026-09-24 註**：已裁定——不列（Proposal 維持 capability 粒度），見 §2 表後的註。
6. 外部討論交接與正式設計 §3 的關係：補充或修訂（本文立場：不取代）。
7. 若要分段實作，Scenario 層可否延後——需要修訂正式設計 §9.3「v1 必做、不可延後」（§6 第 2 點）。
   > **2026-09-24 註**：已裁定——Scenario 層 **v1 仍必做**，不延後；Scenario → Evidence 由 Verification Result 建立。見 `文檔/handoff/session-handoff-20260923.md` 的 Session 16：40 裁定快照，以及 2026-09-24 核可版正式設計（`docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`，commit `8002fa0`） §4.2、§9.3（§9.3「v1 必做」未修改）。§6 第 2 點「延後 Scenario 層」的構想因此不成立。

---

## 8. 未查證項目與推論限制

- **上游 sync skill 的 partial update 是否會在本 repo 實際造成 Scenario 被刪**：只從讀程式碼推得（§2 Scenario ID 列、§3 ③ 周邊），**未實測**。bridge 的 spec 指令已要求 MODIFIED 貼完整內容（`schema.yaml:134`），殘餘風險是 agent 改照上游 sync skill 的指示走。
- **Spec 內文只讀了標題**：本 repo 的 spec 與 Issue #4 的 spec 都只讀 `### Requirement` / `#### Scenario` 標題，未逐段讀內文。
- **Spec Kit 以 `main` `67ab049`（2026-09-23）為準**；其他版本可能不同。
- 【推論】OpenSpec RENAMED 後的 requirement 會被移到 Requirements 區段末尾（讀 `specs-apply.js` 的重建迴圈推得，未實跑）。
  > **2026-09-24 註（此推論已被實測推翻）**：2026-09-23 在 scratchpad 實跑——單一 capability 11 個 RENAMED，`openspec validate --strict` 通過、`openspec archive -y` 成功，**需求順序保留**，並未移到末尾（見 `文檔/handoff/session-handoff-20260923.md` 的 Session 16：40 裁定快照 的「實測」段）。跨多個 capability 的情形未測。
- 【推論】zod 預設丟棄未知鍵：讀 `artifact-graph/types.js` 使用一般 `safeParse` 推得。S3 spike 已實測「自訂頂層區塊不會導致 validate 失敗」，但「被丟棄」本身未實測。
- 【推論】`loosen-plan` 偏離正式設計 §4.3 的承載設想：以兩份文件內容比對推得，未查 `loosen-plan` 是否有明文記錄此偏離。
- **Issue #4 的 18 項判定由 subagent 產出**；本人抽查三項事實：`check_promise_coverage` 存在（`change_delta_integrity.py:664`）、測試模組 56 個 `test_` 函式、列號標記只出現 3 處（L9、M7、M7）。其餘 15 項的來源與分類未逐一覆核。⚠️ 該 subagent 的**摘要**寫「4 可抓 / 5 助找 / 9 無助」，與它自己的逐列表格不符；初稿照抄了摘要，經 fallback 文件審指出後，已改為依表格逐列重數（§4.1）。subagent 自述未讀：spec 全文（只讀標題）、`2026-09-03-loosen-plan-execution.md`、`code-rereview-fallback-3.md`、loosen-plan SDD 報告、handoff 0921 三/五/六欄。
- **樣本數**：Issue #4 是 n=1 的單一 change；§4.1 分布不代表一般情況。
- **Decision ID 的引用統計**（§3 ①）只涵蓋本 repo 4 個已歸檔 change 的 `tasks.md` / `plan.md` / `verify.md` / `retrospective.md` / `errata.md` / `brainstorm.md`，未涵蓋 handoff 與其他 repo。
