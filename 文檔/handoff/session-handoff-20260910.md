# Session Handoff — 2026-09-10

<!--
本檔每個 session 結束時 append 一個 ## Session HH:MM 區塊。
六欄 heading 順序固定，缺漏會被 Stop hook block。
四欄內 sub-segment marker（**【紀律接力】** / **【當日洞見】**）缺漏會 Stop hook ⚠️ Warn（不 block）。
-->

## Session 08:36

### 一、本 session 主題

**補兩道 review gate + 兩輪唯讀分析「既有 review 能力是否被繞過」+ 把結論寫進 research 文件。** 本 session 自 2026-09-09 08:46 開工、跨日。⚠️ 本區塊在 session **進行中**寫入（跨日觸發 Stop hook），非收工紀錄；收工時以 `/end-session` 補完。三件主線：①補 0909 欠的 doc gate 與 code plane Codex 補審；②使用者發起的兩輪分析（既有 skill / rule 盤點 vs 實戰 pattern；Task Context 是否值得補）；③把分析結論寫成 research 文件 §5、走 doc gate 至今 7 輪未過。`fix-v2-blocking-defects` 全程維持凍結。

### 二、完成事項

- **code plane Codex 補審完成**（09-09 01:23Z 派、沿用 09-08 04:48 派工單、拿掉錯誤 CRLF 前提、加「先命名被換掉的假設、列依賴表面」段）：⛔ Blocked，2 Important——`schema.yaml:1177` apply 指令殘留單一對措辭（1177/1178 行間換行，fallback 當初的單行 grep 掃不到）、`:175/:567` 作者指令固定縮排 vs 檢查接受任意深縮排。另報 `templates/tasks.md` 與 `verify.md` 兩檔 CRLF→LF 翻轉（0908 只記 verify.md，未核）。凍結中未修、未記 review-state。
- **doc gate 第一段**（research 文件 §0–§4 + README 索引列）：Codex 3 輪 → ✅ Mergeable、已記 `doc_review pass`。抓到並修正：「五 P1 一個形狀」的載體誤植（實為 04:48 派工單與 fallback 報告，版控三處只套 P1-1/1-2）、A–E 圖例缺失。
- **分析一（既有 review 機制盤點 / 0907 繞過查證 / 九項 pattern A–D 對照）**完成並寫入 research 文件 §5。核心事實：0907 與 0908 兩次外部審都繞過 `/codex-review-branch` 直呼 MCP（N=2）；主 Agent 自建任務明寫「走 /codex-review-branch」仍未 invoke；`FOCUS` 槽只在 fast/full 模板、branch 模板無，且 fast/full baseline 為 `git diff HEAD` 審不到已 commit 分支。
- **分析二（Task Context）**完成、僅口頭回報未落檔：task nature / change intent 在 SDD 路徑已有、Codex 路徑無；artifact role 在 doc review 有 `> **Doc role**:` 宣告機制但本次未用（research 文件因無宣告被判成 Current authority）；downstream use / required assurance 全路徑皆無。七輪 12 條 🔴 中 10 條為引用可追溯類、2 條為本 session 修改時製造。
- 封裝候選檢查：backlog 無未結案 `[SOP 候選]`；本次完成事項無 Tier 1 命中，痛點記入四【當日洞見】。

### 三、未完事項 / 接力棒

- [#接力] **research 文件 doc gate 第二段（§5 寫入後）仍 ⛔**：Codex 3 輪 + fallback 4 輪，第 6 輪達 fast tier cap、已做一次 cap 診斷（`UNVERIFIED_CLAIM`）與有界調整，第 7 輪仍 1 🔴（已修但未再審）。依規則 ⚠️ Need Human。三選一待拍板：A 授權第 8 輪 fallback／B 用 Codex 跑第 8 輪／C 記欠債。使用者傾向把第 8 輪當 Task Context 試驗一（見六）。review-state 已記 `doc_review fail`。
- [#接力] **code plane 兩個 Important + CRLF 兩檔差異**凍結中未動，等 D1–D5 複盤一起決定。
- [#待確認] **change-level 外部審裝 repo 題目的路徑**：A 改 branch 模板加 `${FOCUS}`（動 skill、plugin cache 會被覆蓋）／B 走 `/codex-review-branch` 流程、模板後附 Task Context 段。使用者 09-10 表態走「派工習慣、不改 skill」= B 型。
- [#接力] 0909 接力棒其餘未動：D1–D5 複盤、D5-2 錯誤前提更正形式、worktree 分支 backlog line 88 待刪 / line 84 bump、`.gitattributes` 補 bridge 目錄、work-map `evidence` 未知欄位。
- [#不重議] archive 前不宣告完成；D2 不併入本 change；凍結期間不 teardown / 不刪 `.superpowers/sdd/plan/` / 不 archive / 不 push（承 0908）。
- [#不重議] **先不造新 review 系統**（使用者 2026-09-09 裁定）：優先修 invocation、其次用派工單補背景、skill 不改、先在 2–3 個真實 review 試。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **我抄了 reviewer 的斷言當事實寫進文件，兩次。** 第 2 輪自加的圖例與原表打架；第 6 輪把 fallback 說的「該節 byte-identical」直接寫成「逐字相同」，第 7 輪對照兩份 prompt 發現只有標題行相同。**attribute:** 全域 CLAUDE.md「證據先於斷言」+「先讀實際驗到什麼」；也正是 research 文件自己描述的「reviewer 報告被當前提」機制。**propose action:** 既有規則涵蓋、不新增；記為承重案例。修 review finding 時，finding 裡的事實宣稱與文件原句同等地位、都要回源。
- [#觀察] **「事後一句話成為前提」累積數 3**（0908 「十一席當散文讀」、「五 P1 一個形狀」載體誤植、本 session 「byte-identical」）。0909 使用者說再出現就升 backlog 條目；本 session 未動 backlog（凍結 + 由使用者決定）。
- [#觀察] **doc gate 七輪的 🔴 全是同一類（引用與來源對不上）但沒有 stall**：每輪全關、下輪換行再冒。cap 診斷分類 `UNVERIFIED_CLAIM`。根因是原文憑壓縮記憶寫成 + 各 reviewer 抽樣不同子集，到第 6–7 輪才有人做全量解析（約 60 條）。這類文件的 required assurance 若第一輪就說清，輪數可能少一半——hypothesis，證據只有「同 prompt 下 fallback 自己推出了樹基準問題、Codex 沒有」。
- [#接力] **Task Context 派工習慣（使用者 09-10 提出、我同意）**：派 reviewer 前加五格（Task / Artifact / Change / Downstream use / Required assurance），只放可指來源的任務事實、不放分析、不指問題點；reviewer 若發現 Context 與來源衝突以來源為準並回報 Context mismatch。掛點：handoff 四記「派幾次 / 附幾次 / 幾次 mismatch」。反指標：Context 自己被證偽的次數。第 8 輪為 pilot（三變數同動、非因果證據），正式 A/B 留給下一個新 change。

**【當日洞見】**

- **同一份 prompt、兩個 reviewer 家族抓的是不同半邊。** Codex 三輪抓「引用內容說錯」；fallback（Opus）四輪抓「引用在目標樹上解不到」與「工單指向不存在的段落」，後者要真的到 main 與 worktree 各解一次才會發現。對 D4 是資料點非結論。
- **「先命名被換掉的假設、列依賴表面」那一段，第一次用就命中一個殘留**（`schema.yaml:1177`）。單次證據。
- **fallback 的 grep 零命中宣稱被 Codex 推翻**：那句在 YAML 換行處斷開，單行 grep 掃不到。0908 自記的「範圍化 grep 被當完整掃描」再發一次，載體換成量測工具的換行盲點。
- **doc review 的 profile 解析器把 research 記錄判成 Current authority**：`doc-metadata.js` 只認 `requests/`、`review-log-`、`adr-`、`0-3-*` 路徑或文件內 `> **Doc role**:` 宣告，其餘 fail-closed 成權威。誠實宣告成 record 又會落到 `record-diff`、免除引用驗證。四分類對「以可追溯性為信度核心的 research 文件」沒有合適的格。
- **Stop hook 與使用者「不改檔」指示衝突時的處理**：本 session 使用者已解除不改檔，故照 Guardrail #6 寫本區塊。

### 五、檔案異動

錨來源：本 session 開工 commit（5aa19bf、開工於 2026-09-09T08:46:54）——列 5aa19bf..HEAD

`5aa19bf..HEAD` 為空（main 無新 commit）。working tree 改動：

- `docs/superpowers/research/2026-09-09-review-provenance-analysis.md`（未追蹤，52 → 107 行）——§0 來源更正、A–E 圖例、路徑解析基準、§2 版本錨、新增 §5（既有 review 能力對照與裁定）、多處引用行號更正
- `docs/superpowers/research/README.md`（修改）——目錄定位補「審查行為實證考古」、索引列補 §5
- 未追蹤且刻意排除：`文檔/handoff/session-handoff-{20260903,20260904,20260907,20260908,20260909}.md`、`2026-08-27-brainstorm-產品承諾.md`、`.claude/worktrees/`
- scratchpad（不進版控）：`doc-review-fallback-r1..r4.md` 四份 fallback 報告

**無專案資料夾** → 專案 Changelog skip。**驗收節點 sentinel 區段無條目** → skip。
**work-map 無需變更**：`task-20260907-fix-v2-blocking-defects` 維持 DOING；本 session 零 record 狀態變化。
**未 commit**：doc gate 尚未通過，依 terminal completion invariant 不收 commit。

### 六、下一步建議

1. **第 8 輪 doc review 當 Task Context pilot（試跑，非因果驗證）**：使用者 09-10 拍板——同時換了 reviewer、文件 snapshot、加 Context 三個變數，只能回答「reviewer 能否理解五格、有無 mismatch、有無 anchoring、五格寫起來是否笨重」，不能拿來說命中率提高。做法：doc-review 原版模板（拿掉前七輪加的「逐條驗引用」程序指令）+ 五格範例一字不改 + Context mismatch 輸出行；載體 Codex。**真正的 A/B 留給下一個新 change**：同 snapshot（釘 commit hash）、同 reviewer 家族、同模板、並行兩隻、只差 Task Context 一段。試行期紀錄只做三個數（派幾次 / 附幾次 / mismatch 幾次），不進規則。
2. **decide change-level 外部審路徑（B 型）後，補 code plane 兩個 Important 的處置**，與 D1–D5 複盤合併；複盤前提用 research 文件 §0 修正後版本（I2 在範圍內仍漏、範圍差只解釋 I3）。
3. **收工前**：把「事後一句話成為前提」N=3 是否升 backlog 條目端給使用者；handoff 本區塊補完為正式收工紀錄。


## Session 09:03

### 一、本 session 主題

**正式收工紀錄**（同日 08:36 區塊為跨日觸發的進行中寫入，事實細節以該區塊為準、此處不重抄）。本 session 09-09 08:46 開工、09-10 收工。主題：補 doc gate 與 code plane 補審、兩輪唯讀分析（既有 review 能力 vs 實戰 pattern；Task Context）、把結論寫入 research 文件 §5 並走 doc gate（7 輪未過、Need Human）。使用者於本 session 末拍板「先不造新 review 系統、先修 invocation、Task Context 當派工習慣試行、第 8 輪只算 pilot」，並決定收工、下個 session 做派工單實測觀察。

### 二、完成事項

- code plane Codex 補審：⛔ Blocked、2 Important（`schema.yaml:1177` 殘留、`:175/:567` 縮排口徑）+ CRLF 兩檔翻轉待核。凍結中未修。
- doc gate 第一段（§0–§4）Codex 3 輪 ✅；第二段（§5 寫入後）Codex 3 輪 + fallback 4 輪仍 ⛔，cap 診斷 `UNVERIFIED_CLAIM` 已用、第 7 輪 1 🔴 已修未再審。
- research 文件 §5 落檔：既有 review 機制盤點、0907 繞過 skill 查證（N=2）、九項 pattern A–D 對照、使用者裁定。README 索引列同步。
- Task Context 分析口頭回報完成（未落檔）：SDD 路徑已有 task/intent；doc review 有 `Doc role` 宣告未用；downstream use / required assurance 全路徑缺。
- 第 8 輪派工單已組好（原版模板 + 五格 + Context mismatch 行、拿掉程序指令），**未送出**（使用者決定留到下個 session）。

### 三、未完事項 / 接力棒

- [#接力] **下個 session 主題：派工單實測觀察任務**。①第 8 輪 doc review 當 **pilot**（三變數同動、非因果證據）：派工單原文在本 session transcript（`133797d7`）最後一次 `mcp__codex__codex` 呼叫、被使用者攔下未送；照原樣送即可，載體 Codex。②之後 2–3 個新 change 試行 Task Context 派工習慣，至少一個做同 snapshot / 同 reviewer 家族 / 同模板 / 並行兩隻 / 只差 Context 的 A/B。③試行期只記三個數（派幾次 / 附幾次 / mismatch 幾次），寫 handoff 與 research 文件觀察節，不進規則。
- [#接力] doc gate 仍 ⛔（`doc_review fail` 已記）：第 8 輪 pilot 同時負責收 gate。
- [#接力] code plane 兩個 Important + CRLF 差異、D1–D5 複盤、D5-2 更正形式、worktree backlog line 88/84、`.gitattributes`、work-map `evidence` 欄位——全部承前未動。
- [#待確認] 「事後一句話成為前提」累積數 3，是否升 backlog 條目由使用者決定（本 session 未動 backlog）。
- [#待確認] 下個 session 要不要把「派工單實測觀察」登記進 work-map（建議 id `task-20260910-task-context-pilot`、parent `none`）；本 session 未寫。
- [#不重議] 先不造新 review 系統；優先修 invocation（change-level 走 `/codex-review-branch`）；skill 不改、先試 2–3 次；第 8 輪不算效果證據（使用者 2026-09-10）。
- [#不重議] archive 前不宣告完成；D2 不併入；凍結期間不 teardown / 不刪 `.superpowers/sdd/plan/` / 不 archive / 不 push。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **我自己立的「一次只變一個變數」，下一段就拿三變數的第 8 輪當試驗一，使用者抓到。** 同一 session 內第二次「規則寫完立刻自己不遵守」（第一次：寫「零 Skill 呼叫」時把「零 review skill」寫寬）。**attribute:** 全域 CLAUDE.md「動工前三問」的衝動警報 + 「修正絕對句時寫出的替代句要再過一次檢查」同族——提出規則的那一刻就是最高發的違規時刻。**propose action:** 既有規則涵蓋、不新增；記為承重案例。
- [#反] **使用者說「可以」我就派工，沒等他看派工單全文**，被攔下。**attribute:** 全域 CLAUDE.md「屬用戶那半的決定 SHALL 端出來」——派工單內容（五格怎麼寫、拿掉什麼）是他要看的東西。**propose action:** 不新增規則；派 reviewer 前若派工單有新形狀，先貼全文再送。
- [#接力] Task Context 派工習慣的四條邊界（使用者 09-10 拍板）：只放可指來源的任務事實；Required assurance 寫「要可靠到什麼程度」不寫「你要怎麼查」；reviewer 與來源衝突以來源為準並回報 Context mismatch；試行期只做可回查紀錄、不做永久治理掛點。
- 其餘紀律接力見同日 08:36 區塊（reviewer 斷言當事實 ×2、事後一句話成為前提 N=3、七輪同類 🔴 無 stall）。

**【當日洞見】**

- 見同日 08:36 區塊五條（兩個 reviewer 家族抓不同半邊、「命名被換假設」首用命中、grep 換行盲點、profile 解析器把 record 判成權威、Stop hook 與不改檔衝突的處理）。
- **Task Context 與 Focus 的切線可以講得很短**：「這東西要可靠到什麼程度」是背景，「請逐條檢查 X」是程序。前七輪我在派工單裡寫的「逐條驗 §5 引用、指錯即 🔴」屬後者——第 8 輪把它拿掉，正是 pilot 要看的東西。

**【學習候選】**

1. **Case**：提出規則的同一段話裡立刻違反該規則，本 session 兩次（單變數 / 零 Skill 呼叫寫寬）。
2. **Candidate Pattern**：寫下一條新判準後、在同一則回覆內對自己接下來的建議跑一次該判準。適用：提出新規則或新判準的當下；不適用：套既有規則的一般回覆。
3. **Evidence**：N=2 本 session；0908 「一個永遠回同一答案的檢查」亦同形（Hypothesis：提出者對新規則的例外敏感度最低）。
4. **Minimum Sufficient Intervention**：不新增規則。既有「修正絕對句時替代句要再檢查」已是同族，把本例掛為其承重案例即可；掛點＝該條已在 always-on。
5. **Promotion**：Case Memory。

### 五、檔案異動

錨來源：本 session 開工 commit（5aa19bf、開工於 2026-09-09T08:46:54）——列 5aa19bf..HEAD

`5aa19bf..HEAD` 為空。working tree 與 08:36 區塊相同，另加：本檔 08:36 區塊六第 1 條措辭由「試驗一」改「pilot」（同 session 自己的區塊）。**未 commit**：doc gate 未過。handoff 依慣例留 main 未追蹤。

**無專案資料夾** → Changelog skip。**驗收節點無條目** → skip。**work-map 零變更**（`task-20260907-fix-v2-blocking-defects` 維持 DOING）。

### 六、下一步建議

1. **開工先送第 8 輪 pilot**：派工單原文取自本 session transcript 最後一次 `mcp__codex__codex` 呼叫（被攔未送），先貼全文給使用者看一眼再送。回來記三個數、看 Context mismatch、看有無 anchoring；同時收 doc gate。
2. **決定要不要登記** `task-20260910-task-context-pilot`（parent none）追蹤 2–3 次試行與一次 A/B。
3. **D1–D5 複盤**照舊排在 pilot 之後，前提用 research 文件修正後版本。

## Session 12:25

### 一、本 session 主題

**Task Context 派工習慣兩筆 pilot + 觀察期裁定收斂 + fix-v2-blocking-defects 修 r1/r2 finding。** 本 session 09:07 開工、12:25 收工。Pilot 1（research 文件 doc review、Codex）第 8–10 輪收掉 doc gate 並 commit；使用者拍板三條裁定（Task Context 為派工習慣 / evidence-first 只管證據宣稱 / 觀察期不改 skill），登記 `task-20260910-task-context-pilot`；Pilot 2（fix-v2 code plane、`/codex-review-branch` 形狀）Codex 額度用盡改 fallback，兩輪 ⛔ 全部修完並 freeze 最終快照，等 Codex 額度（13:56）做正式 branch review。下午追加四條裁定（H3 改配置問題 / 已核實附方法 / 記 miss / 耦合型錯誤先觀察既有機制）。整合紀錄頁：artifact「Task Context Pilot 觀察帳」（https://claude.ai/code/artifact/7e20f772-ed0a-4b13-a332-7a7ea71570a6）；memory `feedback_review_observation_protocol`。

### 二、完成事項

- **Pilot 1 / doc gate 收掉**：第 8 輪派工單照原樣送 Codex（Task Context 五格、無程序指令）→ ⛔ 2 🔴 1 🟡（branch tip 錯認、「全部 blocking 來自 change-level」過度概括、裁定缺時間座標）→ 修 → 第 9 輪 ⛔ 2 🔴 全在我修正句上（`HEAD ->` 字串在 `[30]` 非開頭、層別描述過度概括）→ round-10 checkpoint 診斷 `ATTENTION_DIFFUSION`、每句先回源再送 → 第 10 輪 ✅ Mergeable。`doc_review pass` 已記。
- **research 文件 + README 索引 commit**：`fc8f552`（走 smart-commit --execute、使用者純文字核准）。
- **work-map 登記** `task-20260910-task-context-pilot`（DOING、parent none、bounded observation）。
- **Pilot 2 r1（fallback Opus）**：⛔ 1 P2（work-map 條目引用只在本機 `.superpowers/` 的兩份報告卻稱證據已備妥）+ 4 Nit；miss：`schema.yaml:1177` 每 task 單一對殘留。修：兩份報告逐位元組存 `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/` + README、retrospective 三處引用改指副本或標不可複驗、1177 改每 subject、`.gitattributes` 加 bridge 規則。
- **Pilot 2 r2（fallback Opus、修後快照）**：⛔ 1 P1 + 4 P2 + 3 Nit。P1 dogfood 副本未同步（我修 1177 時造成）→ 重新同步、5.1 控制改寫為 `diff -r` 不變量、verify.md 補記；P2 check 10 補「缺 outcome 欄」句；P2 R1 `INDETERMINATE` 放寬補宣告（proposal §What Changes + Modified Capabilities、`tdd-evidence-contract` delta 兩句 SHALL、retrospective §3 一列；前提查證：R1 為 review judgement、INDETERMINATE 只在 RED 側、不等於 PASS、不替代 GREEN）；P2 `.gitattributes` 改逐副檔名列舉 + 註解點名三個 CRLF blob；Nit verify.md 四點→五點。使用者跑 `git add --renormalize superpowers-bridge/`，14 個 blob 全 `i/lf`、三個模板 staged diff 純 EOL。`openspec schema validate` ✓、dogfood `diff -r` 回空。
- **最終快照 freeze**：HEAD `b07d571` + 13 個改動檔 blob hash，見 `文檔/handoff/attachments/20260910-pilot2/pilot2-snapshot.md`（同目錄有 fallback r1/r2 報告全文）。review-state `code_review fail` r2 已記。
- 封裝候選檢查：backlog 無未結案 `[SOP 候選]`；Tier 1 不開（使用者明示不新增機制），痛點記入【當日洞見】。

### 三、未完事項 / 接力棒

- [#接力] **開工第一件事：Codex 正式 branch review（額度 13:56 後）**。派工單 = 本日 Pilot 2 r2 那份（Task 格為「已納入 scope、來源見 proposal §Why」、base `368d586`、cwd 為 worktree、審 HEAD + 未 commit 修正；Scope Baseline 凍結 36+4，另註修正新增檔依 branch 引入歸類）；載體 `gpt-5.6-sol` high read-only。**報告明記審的是修後快照**（attachments 的 blob 清單）。回來後：`validate-family-sentinel.js code` 驗 gate、逐條回源核實、與 fallback r1/r2 做描述性對照（不稱 A/B）、記七項（含 miss）、第一輪 findings 與 miss 交使用者判是否服務實際風險。**Codex 通過後不再做任何改 digest 的正規化**，直接 smart-commit（worktree 內 7 個改動檔 + 1 新目錄，含 renormalize 的三個模板）。
- [#接力] **fix-v2 剩餘流程**：Codex 過 → commit → verify 重跑（tasks.md 已動、§2/§7/§8 依 freshness 規則要重算）→ retrospective 補 → archive（Windows 目錄鎖：cp + diff -r + 委派使用者 rm）→ 併回 main → push。凍結解除以 Codex ✅ 為事件。
- [#接力] **已知但本輪未修**：上次 Codex 補審的「`:175/:567` 縮排口徑」Important（判為刻意差異，fallback 兩輪未報）；D1–D5 複盤；worktree backlog line 88/84；work-map `evidence` 未知欄位；「事後一句話成為前提」N=3 是否升 backlog。
- [#待確認] fallback r2 三條 Nit 未修：`schema.yaml:1180` 84 字元行、`:532` check 7 說 grep 回 0 實為 exit 2（STOP 仍成立）、check 10 缺 outcome 欄無 fixture。
- [#不重議] 觀察期不改 Skill、不加 reviewer 層、不加 gate、不改 routing；不建模型排行榜、不為比較加 review；Task Context 不放 known defect / 前次 finding / 懷疑位置；R1 放寬保留並已宣告。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **「已核實」標籤自己翻車一次**：CRLF 翻轉宣稱我用沒校過的方法量到 0、就宣布上次判斷不成立；改用 `tr -cd '\r' | wc -c` 才確認宣稱一直是對的（0908、0909、0910 第三次出現）。**attribute:** 全域「先讀實際驗到什麼」對自己的量測同樣適用。**propose action:** 不新增規則；標「已核實」時附「來源 → 方法 → 結果」（使用者 09-10 拍板）。
- [#反] **修 review finding 時製造 3 個新缺陷，全是「改 A 忘了 B」**：改 schema 沒同步 dogfood 副本（CLAUDE.md 耦合表明寫）、`.gitattributes` 萬用字元違反同檔 POC 段理由、註解宣稱與 index 狀態不符。**attribute:** 耦合表在，但修 finding 當下沒有任何東西把它端到眼前。**propose action:** 不新增機制，先觀察既有耦合機制為何沒幫上忙（使用者拍板）。
- [#反] **grep 命中就寫、沒定位是哪次呼叫**（Pilot 1 r9 的兩個 🔴 都是修 r8 時引入）。r10 每句先回源再送，一次過。**attribute:** evidence-first 的證據宣稱型。
- [#接力] **使用者 09-10 三條裁定 + 下午追加四條**：①Task Context 為派工習慣，不是 skill 欄位／gate；五格不強制、不重複 skill 已知；只放可回源的任務事實、不放 known defect / 前次 finding / 懷疑位置 / 作者結論；Required assurance 寫可靠程度不寫程序；衝突以來源為準並回報 Context mismatch。②evidence-first 只管證據宣稱（session 行為、tool call、commit、版本、檔案內容、prompt 原文、時間座標），分析與假設分開標。③觀察期 2–3 個真實 review，不改 Skill / reviewer 層 / gate / routing。④H3 改寫為配置問題（Codex/Claude 各有能力邊界，找任務、Context、工具、機械保證的最佳配置；不排行榜、不為比較加 review、條件不同不歸因模型）。⑤已核實附方法。⑥記 miss：送審前封一份不送 reviewer 的已知缺陷清單、審後對答案，只測已知缺陷的 miss。⑦耦合型修正錯誤不算 evidence-first 失效，先觀察既有機制。memory `feedback_review_observation_protocol`。
- [#接力] **每次 review 記七項**：reviewer/model/effort、base + snapshot digest、Context 異同、第一輪 finding 按類型、reviewer 自主驗證行為、已知但漏掉的 defect、mismatch/anchoring。第一輪 findings 與 miss 交使用者判「是否服務實際風險」，AI 不自評。

**【當日洞見】**

- **Pilot 1**（Codex、doc review）：r8 兩 🔴 都是作者推論被原始紀錄證偽；reviewer 自己追 rollout metadata / git blob / worktree task review / transcript 時間戳，但模板本來就要求獨立研究，不歸功 Context。mismatch 0。
- **Pilot 2**（fallback Opus、branch review）：r1 唯一 P2 直接扣著 Downstream use 格（teardown 後證據消失），目前唯一能歸給 Context 的一筆；r1 漏 1177 殘留（已知缺陷、記 miss——能記下來純因派工前碰巧看過那三行）；r2 抓到我修正製造的 P1 + 2 P2、check 10 缺一角、R1 放寬未宣告。兩輪 mismatch 0（r2 正確指出凍結基準未含修正新增檔，歸類做法正確）。兩輪驗證行為相同：實跑 checks 8–12 對 fixture、`diff -r`、`ls-files --eol`、對照 proposal 與 spec。
- **同一 CRLF 宣稱三次出現、前兩次被判錯**：我們自己的「已核實」出錯比 reviewer 漏一條更會靜默累積。
- **Task Context 與 Focus 的切線**：「要可靠到什麼程度」是背景、「請逐條查 X」是程序；拿掉後 reviewer 去了前七輪沒去的 §2 / §3。
- **五指標**：Pilot 1 — Context 1 / mismatch 0 / 輪數 3（r8–r10）/ 修正新增 2（證據宣稱型）；Pilot 2 — Context 1 / mismatch 0 / 輪數 2+（fallback）/ 修正新增 3（耦合同步型）；「第一輪 finding 是否服務任務風險」由使用者複盤判。
- **兩條外部審載體同時耗盡**（Codex 額度 13:56、Claude subagent 12:00）：等待期用作者自查（明標不算 gate）與快照 freeze，沒有派第三載體。

**【學習候選】**

1. **Case**：標「已核實」的宣稱，量測方法本身錯（CRLF 三次）。
2. **Candidate Pattern**：需要工具或算法得出結果的宣稱，「已核實」必附方法；適用 research / audit / decision record，不適用一般分析文字。
3. **Evidence**：N=1 本 session 親手翻車，加 0908 / 0909 兩次同宣稱被判錯（Hypothesis：判錯者都沒寫量測方法，事後無從對照）。
4. **Minimum Sufficient Intervention**：不新增規則。觀察期在文件裡留「來源 → 方法 → 結果」；掛點＝reviewer 下一輪與使用者複盤都看得到方法欄。
5. **Promotion**：Case Memory（已寫 memory `feedback_review_observation_protocol`）。

### 五、檔案異動

錨來源：本 session 開工 commit（5aa19bf、開工於 2026-09-10T09:07:01）——列 5aa19bf..HEAD

`5aa19bf..HEAD`（main）：

- `fc8f552` docs(research): land review provenance analysis — A `docs/superpowers/research/2026-09-09-review-provenance-analysis.md`、M `docs/superpowers/research/README.md`

main working tree：`workflow-harness/work-map.jsonl`（M，登記 pilot 條目，本次收工 commit）；未追蹤且刻意排除：`文檔/handoff/*`、`文檔/handoff/attachments/20260910-pilot2/`（快照 + fallback r1/r2 報告）、`2026-08-27-brainstorm-產品承諾.md`、`.claude/worktrees/`。

worktree `.claude/worktrees/loosen-plan`（HEAD `b07d571`，**未 commit、凍結等 Codex**）：M `.gitattributes`、`openspec/changes/fix-v2-blocking-defects/{proposal,retrospective,tasks,verify}.md`、`specs/tdd-evidence-contract/spec.md`、`superpowers-bridge/schema.yaml`；staged（renormalize）`superpowers-bridge/templates/{design,plan,spec}.md`；新目錄 `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/`（3 檔）。dogfood 副本已同步（gitignored）。

**無專案資料夾** → Changelog skip。**驗收節點無實條目**（兩行為模板佔位）→ skip。**work-map**：新增 `task-20260910-task-context-pilot`（DOING）；結算無 mark_done / leftover（Codex 補審屬 fix-v2 change 既有 record）。

### 六、下一步建議

1. **13:56 後先送 Codex 正式 branch review**（派工單、快照、驗證步驟見三第 1 條）。這是 Pilot 2 的第三筆資料點（同 Context、同 base、修後快照、換載體），只做描述性對照。
2. **Codex ✅ 後**：smart-commit worktree（訊息點名 r1/r2 修正與 R1 宣告）、重跑 verify、補 retrospective、archive、併 main、push；每步依既有裁定，凍結以 Codex ✅ 解除。
3. **複盤時**由使用者對 Pilot 1/2 的第一輪 findings 與 miss 判「是否服務實際風險」；D1–D5 複盤前提用 research 文件修正後版本，並把「CRLF 宣稱三次」納入 D 複盤。


## Session 08:31（2026-09-11 補記 0910 12:25 之後的正式收工紀錄）

### 一、本 session 主題

**0910 下午：Codex 正式 branch review r1 → 採甲修五條 → verify 主 session 重跑 → contract drift 三方對照研究 → 使用者收斂。** 0910 沒有跑 `/end-session`（使用者下班、session 保持開啟），本區塊由 0911 08:xx 的收工補記；細節以 0911 handoff 08:15 區塊與本區塊為準。

### 二、完成事項

- Codex 正式 branch review r1（`gpt-5.6-sol` high、修後快照 r3）：⛔ 4 P1 + 5 P2 + 3 Context mismatch（全屬實、mismatch 全在作者側）；sentinel 合法；已知缺陷清單 5/5 未報（severity 混合）。七項紀錄、dispositions、sealed list 存 `文檔/handoff/attachments/20260910-pilot2/`。
- 使用者採甲：四條對既有裁定記 `[USER_SKIPPED]`（D2 / G1 第五次復發 / 潛在歧義 3 / deferred observation），修五條：spec delta :7「unique within each side」+ plan.md:17；check 12 plan-key 分隔符（schema + plan 指令、dogfood 同步）；canonical delta 補 record field form + 兩 scenario；verify.md 復原指令並整份重跑（17:03，PASS WITH WARNINGS）；retrospective no-fixture 列改四條。
- verify subagent 撞 session 額度上限 → 主 session 自跑；CRLF 量測改用 `tr -cd`（`grep -c $''` 在本機每行命中）。
- research 文件 `docs/superpowers/research/2026-09-10-contract-drift-archaeology.md` + README 索引列落檔；doc gate r1 8 🔴、r2 6 🔴 全修，r3 撞 Codex 額度。
- 使用者收斂裁定（已寫 memory `feedback_review_observation_protocol`）：Q10 四步 sweep 為觀察期習慣；A/B 平行、B 另開小實驗；不擴研究；work-map 採手改 + tooling observation。

### 三、未完事項 / 接力棒

- 見 0911 handoff。

### 四、洞見 / 反省

**【紀律接力】**

- 見 0911 handoff 收工區塊（本區塊為補記，不重抄）。

**【當日洞見】**

- 見 0911 handoff 收工區塊。

### 五、檔案異動

錨來源：0910 09:07 開工 commit（5aa19bf）——列 5aa19bf..HEAD：`fc8f552`、`98cc5e2`。其餘為 working tree（main：research 文件 + README 索引 + attachments；worktree：11 個改動檔 + 3 個未追蹤報告），未 commit（doc gate ⛔、code gate ⛔ 等 Codex）。

### 六、下一步建議

1. 見 0911 handoff 六。
