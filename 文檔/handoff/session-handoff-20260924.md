<!--
workflow-harness — Handoff template
對應 inventory：A5 六欄 schema、A6 append-only、A7 檔名 schema
檔名：文檔/handoff/session-handoff-{DATE:YYYYMMDD}.md
規則：append-only — 同日多 session append 多個「## Session HH:MM」區塊；前段不可改
-->

# Session Handoff — 2026-09-24

## Session 08:15（跨日 session：開工 2026-09-23 16:44、錨點 08983ee；因日期換日由 Stop hook 要求建檔，session 仍在進行）

### 一、本 session 主題

兩條線交錯：①workflow-harness Issue #4 外部審（Codex 額度恢復後續審、修第 2 輪 finding、派第 3 輪）；②依 09-23 裁定製作 9/1 正式設計的**章節修訂對照表**（revision map），經兩輪文件審、使用者裁定十題。

### 二、完成事項

- **修訂對照表落檔**：`docs/superpowers/specs/2026-09-23-formal-design-revision-map.md`（未 commit）。內容：正式設計 12 節改動逐節對照（改什麼／為什麼／來源）、9/1 那 9 筆 deferred findings 的**原文首次轉錄進 repo**（F1–F9，原只存在 09-01 對話紀錄）、同批但不在正式設計本文的項目、§4 裁定紀錄、§5 未查項。
- **使用者裁定（2026-09-23～24，#不重議）**：Q1 甲（Verification executor independence 進 §2.2、`degradable`；不宣稱 verify provenance 已被 S6 證明）＋連帶 §5 補第二個明名降級項；Q2 甲（Scenario 退休只定責任、不定格式）；Q3 乙（新開 §3.5 Decision 引用）；Q4 甲′（取消人工逐字副本；reference 或 source-derived snapshot，由後續 schema change 實測選型；正式設計寫原則句）；Q5 乙（spike 報告兩筆 deferred 分開，已登記）；Q6 甲（§1 第 17 行附註更新）；A 甲（Q4 原則照寫、明示 plan-contract spec／schema／template 尚未對齊）；B 統一用 `FRESH`；C acceptance record 可偽造併入 §8 第 5 條；D 研究文件加註不改寫。
- **map 文件審兩輪**（Codex 無額度 → fallback contract-neutral-reviewer，`[REVIEWER_FALLBACK] plane=doc_review from=codex to=contract-neutral-reviewer reason=quota`）：r1 ✅ Mergeable（9 筆非阻擋，全數修入 map）；r2 ✅ Mergeable（9 筆非阻擋，**依使用者裁定不再修 map、直接帶進正式設計修訂**，清單見三）。兩輪 sentinel 皆經 `validate-family-sentinel.js doc` 驗證（⚠️ 餵的是保留標頭／終端／延後行的精簡副本，非逐字原報告）、`note doc_review pass`。
- **登記** `task-20260923-spike-report-deferred`（掛 superpowers-bridge 下一代改造）：spike 報告 :4 可重現憑據、:1 中英排版。
- **Issue #4 外部審**：r2（`01a0cc1f`、gpt-6-sol，09-23 20:11 重派）⛔ Blocked——前輪 5 條中 3 條獨立驗證已解；新 P2（no-spawn 靜態守門漏 `import os as _os` 別名，自行重現且同類 `_os.popen` 亦漏）＋Nit（`decision-matrix.md` 結語 fixture 說法殘留）。**已修（bounded，使用者指示不擴相鄰問題）**：別名追蹤＋雙向測試（負向 +2、正向參數化 3 條）；雙向變異各轉紅（拿掉別名追蹤 → 2 紅；放寬比對 → 1 紅）；全套 7 failed／3229 passed／4 xfailed、無 error，7 條與 baseline 相同；`validate --strict` 通過；tasks.md 記 3.14。**r3 已派**（同 thread 第 2 次續審）。
- 09-23 16:47 那次重派因額度中途耗盡（約 40 萬 token）無 verdict，不算輪次。

- **15:55 收工補記**：
  - **正式設計核可版 commit `8002fa0`**（正式設計＋修訂對照表＋本 handoff 的核可紀錄；三檔，其餘 dirty 檔未收）。
  - **研究文件三處加註 commit `1879bd8`**（`2026-09-23-requirement-traceability-current-state.md`，+5 行、不改寫原推導）：①§2 表後註＋§7 第 5 題註：Proposal → Requirement ID 已撤回（Proposal 維持 capability 粒度；指向 09-23 快照與正式設計 §1，並明寫正式設計本身無 Proposal 粒度條文）②§7 第 7 題註：Scenario 層 v1 仍必做（指向快照與正式設計 §4.2、§9.3）③§8 RENAMED 推論註：已被 09-23 實測推翻（順序保留，跨 capability 未測）。Codex record-diff 審 ✅ Mergeable、零 finding（thread `01a0d261`）。
  - 工作地圖結算：`task-20260923-formal-design-revision-map`、`task-20260901-design-223-convergence` 標 DONE（證據：`8002fa0`）。

### 三、未完事項 / 接力棒

- [#接力] **Issue #4 程式面外部審 ①：第 3 輪（`01a0cc1f`、gpt-6-sol）✅ Ready**（08:3x 補記）——r2 兩條經審查者獨立驗證已解（含在記憶體中拿掉別名追蹤、兩條新斷言轉紅）、無新 finding；它收集到 3240 個測試、`validate --strict` 通過；唯讀環境無暫存目錄，**全套測試結果未能獨立驗證**（本地實跑：7 failed／3229 passed／4 xfailed）。結果檔同目錄 `r3-result.md`。**①取得有效 PASS；但 tasks.md 4.4a 要求程式與文件各補一輪外部審——原計畫的 ②（Codex-specific 兩 batch）仍未派，未過前不得 commit／PR／archive。**
- [#接力] **使用者定的順序**：Issue #4 r3 → 若 PASS → 依 map 一次修訂 9/1 正式設計 → 正式設計自己送完整文件審 → 新一輪核可。
- [#接力] **map r2 的 9 筆，修訂正式設計時一併處理**（map 本身不再修、不再審）：
  1. map :15「行號一律指 9/1 版本」過絕對——其他檔的行號指本表製作時的 HEAD／工作樹。
  2. §2.2 收錄標準「Gate 判得動」要同時涵蓋 Independent Review 與新增的 Verification executor independence 兩列（後者 provenance 未實測，重演 F3 張力）。
  3. FRESH 掃描集補第 219 行（「還 fresh 嗎」）；第 204–205 行「current digest」指當下指紋、**不可**改成 FRESH。
  4. §3.2 `Contracts:` 語法是否接受 `capability / REQ-x` 限定形——map 無列交代，修訂時要補；§3.3、§9.1 需明寫不需修改的理由。
  5. map §4 殘留句「各題列的沒查的已併入 §5」指向已不存在的欄（半修殘留）。
  6. map 頭與 :29「六題」少算（實為 Q1–Q6＋A–D）。
  7. I6 列第一項缺 ① 標號。
  8. §2.3 替換文字「本輪定案（附錄 #6）」在新增第二張附錄表後會歧義 → 寫「2026-09-01 拍板（附錄 9/1 表 #6）」。
  9. map :89「2026-09-01 代審」誤標——spike 報告那次是正常 Codex 審。
- [#接力] 研究文件三處加註（D）與 plan-contract／schema／template 對齊（後續 opsx change，含 plan-contract requirement 的 MODIFIED delta）都**不在**正式設計修訂內。
- [#不重議] 上面二的全部裁定；map 不再跑第 3 輪審（使用者：「審藍圖」不要變成新的工作循環，品質門檻放在正式設計本身的文件審）。
- [#接力] **9/1 正式設計已依 map 修訂完（09:xx 補記）**：`docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md` 306→約 366 行、未 commit、**已凍結等 Codex 文件審**。map r2 的 9 筆中，與正式設計相關的 4 筆（第 2、3、4、8 筆）已修入；只關於 map 措辭的 5 筆（第 1、5、6、7、9 筆）依「map 不再修」裁定不處理。殘留掃描、連結檢查通過。
- [#不重議] **`Contracts:` 一律 capability-qualified**（`capability / REQ-x`），無「單一 capability 可省略」例外；散文簡稱不受限（使用者 09-24）；同理 **`verification-results.json` 的 `contract` 也一律限定形**（`capability / REQ-3-S1`）——凡跨 Artifact、供機器解析的正式引用皆 `capability / local-ID`；修訂前已歸檔紀錄（如 `"contract": "REQ-PB"`）不回改，規則自修訂核可後的新 change 生效。§3.5「Decision 選填服務哪條 Requirement」**維持刪除**——研究建議不升格為 normative rule。
- [#接力] **審查排程（使用者 09-24 定）**：13:07 提醒 → 先派 Issue #4 ② batch 1（`doc2-b1-prompt.md`）→ 取得有效 verdict 後再派正式設計文件審（Codex、新 thread、gpt-6-sol；prompt 已備 `fd-review-prompt.md`，同 scratchpad）。② batch 2（`doc2-b2-prompt.md`）排在哪個位置**未定**，到時問使用者。② batch 1 在 08:4x 首派時撞額度（log：try again at 1:03 PM），無 verdict。
- [#接力] 正式設計 Codex 審無 blocking 後，**由使用者另行核可 9/24 修訂本**（文件頭已寫「核可前以 9/1 原版為準」）。
- [#接力] **15:19 補記——兩條審查線結果**：
  - **Issue #4 外部審全清**：①程式面 r3 ✅ Ready；②文件面 batch 1（規格 5）首輪 ⛔ 2🔴（spec 相對路徑斷鏈——改寫為明寫位置＋archive 去處，未照審查建議用 `../../`；引用已刪 `rules/session-rules.md`——註明刪除 commit `e2e0690` 與取回方式、改引原句；同類：memory 引用與 sweep 裡兩處 plugin 規則註明出處，記 tasks 3.15）→ 同 thread r2 ✅ Mergeable；batch 2（敘事 8）✅ Mergeable。三個 sentinel 皆驗證。**收尾（4.4a 打勾、`/smart-commit --execute`、使用者 `/push-ci`、PR、merge、cache、dogfood）等使用者，agent 不自行啟動。**延後 3 筆：matrix :6、:39，brainstorm :22。
  - **9/1 正式設計修訂**：Codex 文件審（thread `01a0d1d2`）首輪 ✅ Mergeable＋2🟡 → 使用者裁定（ID 措辭＝不得重新指派給不同契約；BLOCKED 不是第三種判定、有有效 PASS／FAIL 即不參與判定且與先後無關、PASS／FAIL 皆有效才 CONFLICT、正常 BLOCKED 不走 invalidation；I6 改以每個必要 Scenario 的有效判定為單位）→ 修入並同 thread r2 **✅ Mergeable、零 finding**。檔案 370 行、未 commit、凍結。**下一步是使用者對 9/24 修訂本另行核可**；核可後再談 commit 與研究文件三處加註。
- [#不重議] **2026-09-24 Formal Design 修訂版已由使用者正式核可**（`docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`，370 行）。審查紀錄：Codex 文件審 thread `01a0d1d2` 首輪 ✅ Mergeable（2🟡）→ 依裁定修入 → 同 thread 複審 ✅ Mergeable、零 finding。**核可後本體未再修改**；此凍結版即核可定案版，不再修改其設計內容。
  - ⚠️ 已知不一致（刻意未動、待使用者決定）：文件頭仍寫「本次修訂須另經使用者核可;核可前以 9/1 原版為準」——核可後這句已過時，但使用者指示核可版不再修改，故未改；是否以一行狀態更新處理，留待下個 session 裁定。
- [#不重議] `Contracts:` 與 Result `contract` 一律限定形；BLOCKED 規則如上；§3.5 不加 Decision→Requirement 選填。
- [#接力] 本 session 設的 cron 提醒是 session-only，session 結束即消失。

### 四、洞見 / 反省

**【紀律接力】**

- **修完 review finding 後沒跑擴散檢查，下一輪又被抓到自己留的殘留。** map r1 修完後，r2 抓到兩條我自己造成的半修（「六題」少算、指向已刪欄位的句子）。`review-fix-propagation` skill 正是為此存在，這次沒呼叫。⇒ 動作版：**每次修完 finding、送下一輪審之前，跑一次舊說法搜尋**（本 session 在 Issue #4 那邊有做、map 這邊沒做——同一 session 兩種對待）。attribute：全域 CLAUDE.md「一個缺陷＝一類缺陷」＋ skill `review-fix-propagation`。
- **備份檔路徑兩邊不一致，還原失敗讓檔案停在變異狀態。** 變異檢查的備份 `cp` 用了 `$TEMP ||` scratchpad 的 fallback，第一次落在 `$TEMP`，第二次還原時只寫了 scratchpad 路徑 → 還原失敗、檔案停在被故意改壞的版本；靠事後 grep 計數發現並從 `$TEMP` 還原。attribute：全域 CLAUDE.md「跨 Python／bash 不落地暫存檔當中介；非得落地用 scratchpad 絕對路徑、兩邊同一份字面」——這次是同一條規則換成「備份／還原兩個指令」的形狀。⇒ 動作版：變異前後用**同一個變數字面**、還原後**立刻驗還原**（grep 改壞標記為 0 且正確標記為 1）再往下跑。

**【當日洞見】**

- **續審換模型是可行的**：`codex exec resume <id> -m gpt-6-sol` 會真的換成新模型（log 開頭 `model:` 可證）；memory 裡「對話綁定建立時的模型」只對「改 config 預設」成立，不對 `-m` 明寫。代價是同一對話前後由不同模型審。
- **gpt-6-sol 單輪耗量大**：r2 兩次分別約 40 萬（中途耗盡）與 61 萬 token【觀察，未比較 5.6-sol】。
- 9/1 deferred findings 原文只活在對話紀錄裡，repo 內只有交接提到兩筆名字——「deferred 清單不落 repo」會讓下一個接手的人無從得知要修什麼；這次靠翻 `.jsonl` 撈回。

**【學習候選】**

1. **Case**：map 修完第 1 輪 finding 後，第 2 輪抓到兩條自己引入的半修殘留；同 session 在 Issue #4 那側修完卻有做同類掃描。
2. **Candidate Pattern**：送下一輪審之前固定跑一次「舊說法／計數」搜尋，不論改的是程式還是文件。適用：任何修 finding 後要重審的情形；不適用：首輪審。
3. **Evidence**：本 session 1 例；全域 memory `feedback_review_observation_protocol` 的 A1 已把「先搜舊說法」回灌 review-fix-propagation skill——**Hypothesis**：缺的是觸發時機，不是方法。
4. **Minimum Sufficient Intervention**：不新增規則；既有 skill 已涵蓋，先觀察文件側是否再發。
5. **Promotion**：History only。

### 五、檔案異動

錨來源：本 session 開工 commit（08983ee、開工於 2026-09-23T16:44:42）——列 08983ee..HEAD：**本 session 零 commit**。working tree 中本 session 的改動：

- `docs/superpowers/specs/2026-09-23-formal-design-revision-map.md`（新增）
- `workflow-harness/work-map.jsonl`（新增 `task-20260923-spike-report-deferred` 一行；該檔另有本 session 前的既有改動）
- 本 handoff 檔（新建）
- **workflow-harness worktree**（`D:/workflow-harness/.worktrees/fix-issue-4-worktree-canonical-root`，未 commit）：`hooks/lib/test_project_state_root.py`（別名追蹤＋測試）、`openspec/changes/fix-worktree-canonical-root/decision-matrix.md`（結語）、`tasks.md`（3.14）

git status 中其餘 dirty 檔（`backlog-crosscheck-shadow.json`、Q8 報告與 `evidence/`、`recompute-correctness.py`、`session-handoff-20260921.md`、產品承諾 brainstorm）**早於本 session**，不記在本 session 帳上。

### 六、下一步建議

（15:55 收工改寫；前版內容已被本 session 後續進度取代——Issue #4 r3 已過、正式設計已核可並 commit。）

1. **Issue #4 收尾**（使用者另外指示才動）：程式面 ①、文件面 ② 全過；依 tasks 4.4a 打勾（記兩面 verdict）→ worktree `/smart-commit --execute` → **使用者**在 `D:\workflow-harness` 跑 `/push-ci`、確認 `origin/main == main` → PR（關聯 Issue #4）→ merge → 更新 plugin cache → 真實 linked worktree dogfood → 標 `task-20260915-stop-hook-worktree-root` 完成。延後 3 筆：matrix :6、:39，brainstorm :22。
2. **正式設計文件頭狀態句**：仍寫「須另經使用者核可;核可前以 9/1 原版為準」，核可後已過時；使用者指示核可版不再修改，是否以一行狀態更新處理待裁。
3. **下一個 traceability implementation change**：依核可版正式設計，由使用者決定何時開、範圍多大（本 session 不自行開始）。③（Q8 報告 doc review）仍未派。
