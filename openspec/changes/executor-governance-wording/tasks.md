## 1. schema.yaml

- [x] 1.1 改寫檔頭 `description` 第 8–13 行：拒用理由改為 apply 所需能力（執行過程中的獨立審查）＋目前限制（本版只支援 SDD、缺能力時改用 `spec-driven`），executing-plans 的版本事實改為引用 bridge README 的 Re-verification log（REQ-3、design D1）
  - TDD: n/a — prose-only：YAML `description` 文字，CLI 只顯示不解讀；正確性由 REQ-3 逐句對照與文件審查判定
- [x] 1.2 改寫 apply 第 2 步的 executing-plans fallback 段（約第 1795–1806 行），依 D1 只寫能力與限制並引用 log；其後加入三種情境（無 subagent 能力 → Step 0 STOP；有 SDD → 照契約；有 SDD 但經使用者明確裁定刻意略過 → 例外偏離、非支援模式、不得稱等同 SDD、必要保障做不到就停止、依略過規則記錄）（REQ-3、design D3）
  - TDD: n/a — prose-only：instruction 文字，`openspec schema validate` 不讀 prompt 內容；Step 0 STOP 行為不變由文件審查與 verify 確認
- [x] 1.3 在 retrospective 的 Skipped-skill rules 加入「經使用者明確裁定略過 `subagent-driven-development`」時既有三題的答法：失去的保障、裁定與替代審查、`one-off — schema boundary case` 且裁定只對本 change 有效、已有前例時寫出次數與位置並列 §6 Promote candidate、不得寫成等效 SDD 或符合執行契約（REQ-4、design D4）
  - TDD: n/a — prose-only：instruction 文字，retrospective 沒有機械檢查；正確性由 REQ-4 情境 S2、S3 對照與文件審查判定
- [x] 1.4 `version: 4` 改為 `version: 5`（design D8）
  - TDD: n/a — configuration：版本識別值，由 `openspec schema validate` 與 `openspec schemas` 確認仍能載入

- [x] 1.5 修正 apply Step 0 指向不存在段落的那句（「explicitly opt into the manual fallback path described at the end of this instruction」：`75274b6` 加入時有對應段落〔2b executing-plans fallback 與結尾的 manual fallback 段〕，`045ab98` 刪除那些段落後未一併刪除這句，自此指向不存在的段落）：改為缺必要 skill 時停止，使用者可安裝所需 skill，或明確選擇改用內建 `spec-driven` schema 繼續該 change；Bridge 沒有內部 manual fallback，agent 不得自行切換 schema 或執行路徑。PRECHECK 與 STOP 行為不變（使用者 2026-10-12 裁定甲）
  - TDD: n/a — prose-only：instruction 文字，修正指向不存在路徑的說法；正確性由文件審查判定

## 2. retrospective 模板

- [x] 2.1 `templates/retrospective.md` 的 `### Deliberately Skipped Skills`：加入與 1.3 同義的經裁定略過 SDD 答法說明；`one-off` 選項字面刪除「, no prevention possible」，與 `schema.yaml` 一致；不新增欄位或選項（REQ-4、design D4）
  - TDD: n/a — prose-only：模板說明文字；正確性由 REQ-4 與文件審查判定

## 3. bridge README

- [x] 3.1 `superpowers-bridge/README.md` 的拒用理由各段依 D6 處理：No `executing-plans` fallback 提示框、§2 apply 段指向設計觸點那句（補刻意略過的定位）、設計觸點 #2 的維護說明、設計觸點 #4、Fallback strategy 的 `apply` 列；Naming is not requiring 提示框不改（REQ-3、design D1、D6）
  - TDD: n/a — prose-only：說明文件
- [x] 3.2 `superpowers-bridge/README.md` 的 Re-verification log 末端新增 documentation-only 一段，集中寫 executing-plans 的審查結構事實與查證版本（v6.4.1 固定標籤原文、v6.4.2 spike 比對），註明設計說明引用本段；既有帶日期列與 follow-up 段不改（REQ-3、design D2）
  - TDD: n/a — prose-only：查證紀錄，內容沿用既有查證，不新增上游查證
- [x] 3.3 `superpowers-bridge/README.md` 的 schema major 5 連動：開頭 Schema version、Upgrading 段跨 major 說明、Versioning 表與「published cut」句與列鍵清單、新增「Why v4 → v5」（只有「原本合法的 artifact 變不合法」成立、記下以「沒有檢查會擋」為由維持 v4 被否決）、新增「Migrating v4 → v5」（只影響往後經裁定略過 SDD 的 retrospective、封存紀錄不改、rollback 指向 tag `v4.0.0`）、Current bundle release `5.0.0`、Compatibility 新增 v5 列（`1.14.0`／`v5.1.0`／`pending`）與表下說明、`pending` 說明涵蓋 v5、Known breaking changes 新增 v4 → v5（design D8）
  - TDD: n/a — prose-only：說明文件；Compatibility 表形狀由 4.2 的 grep/awk 實跑確認
- [x] 3.4 `superpowers-bridge/README.zh-TW.md` 對應 3.1–3.3 的所有段落，語意一致
  - TDD: n/a — prose-only：說明文件翻譯

## 4. 版本連動（bridge 目錄外）

- [x] 4.1 `superpowers-bridge/VERSION` 改為 `5.0.0`（design D8）
  - TDD: n/a — configuration：版本識別值
- [x] 4.2 `.github/workflows/version-check.yml` 的 `Read pinned versions` step 列鍵 `v4` 改為 `v5`（design D8）
  - TDD: n/a — configuration；以本機實跑該 step 的 grep/awk，對改後的 README 讀到 v5 列的兩個版本號確認（push 後另以 `workflow_dispatch` 跑一次，不屬本任務完成條件）
- [x] 4.3 頂層 `README.md`、`README.zh-TW.md` 第 11 行 bridges 表 Status 欄 `v4` → `v5`（design D8）
  - TDD: n/a — prose-only：索引表的版本標示
- [x] 4.4 `docs/roadmap.md`、`docs/roadmap.zh-TW.md` 新增 v5 段，標題不標「Released／已釋出」（標記於遠端 tag 確認後另以文件 commit 補上）（design D8）
  - TDD: n/a — prose-only：公開 roadmap

## 5. CLAUDE.md

- [x] 5.1 改寫「修 schema 時的紅旗」executing-plans 那條：能力與保障導向、不准把降級／偏離紀錄當成保障已滿足、註明本版只支援 SDD、引用 Re-verification log；刪除版本沿革與「⚠️ 之後要改寫」整句（REQ-3、design D5）
  - TDD: n/a — prose-only：維護者守則
- [x] 5.2 更新 D8 點名的版本描述：結構約定的 `VERSION` 註記、跨檔耦合表的列鍵描述、「兩個版本號別搞混」表的 `version: 4` 與「需從目前的 4 bump」、「Compatibility 表的列鍵」一句（design D8）
  - TDD: n/a — prose-only：維護者守則

## 6. 驗證

- [x] 6.1 重同步 dogfood 副本，跑 `openspec schema validate superpowers-bridge`、`openspec schemas`、`openspec validate executor-governance-wording`
  - TDD: n/a — configuration / 查驗：同步與結構驗證，無新行為
- [x] 6.2 殘留搜尋：REQ-3 列為已取代的說法（設計說明內的 executing-plans 版本機制描述、「不派任何獨立審查者」、上游推薦類理由、TDD 差異論）全 repo 不再出現於現行文件；`git grep` 搜 `v4`、`version: 4`、`4.x.y`、`4.0.0`，逐筆判定改或屬紀錄不改；排除 archive、handoff、poc、retrospectives、research 等紀錄類位置
  - TDD: n/a — 查驗：搜尋與逐筆判定，無新行為
- [x] 6.3 逐處確認三個語意未被改變並記下出處：沒有 subagent 時仍在 Step 0 STOP；有 SDD 時仍走第 2 步正式路徑；刻意略過 SDD 的紀錄不會被讀成已滿足必要保障（併入文件審查與 verify，不新增機械檢查）
  - TDD: n/a — 查驗：語意對照，判準為 brainstorm「驗證」節的三點
- [x] 6.4 依 `release-versioning` REQ-3-S2（本 change 修改版）查核：`schema.yaml` 宣告的 schema major、`version-check.yml` 讀取列的列鍵、Compatibility 表裡該列三者一致，並原樣取出該 step 實跑，讀到該列的兩個版本號；記錄結果（使用者 2026-10-12 裁定）
  - TDD: n/a — 查驗：一致性比對與實跑既有 step，無新行為

<!--
不在本清單內（依 release-versioning REQ-1，完成條件掛在工作地圖紀錄，不在 tasks.md）：
archive 與最終驗證後，在 release commit 打 annotated tag `v5.0.0`，經使用者授權 push，
確認遠端 `refs/tags/v5.0.0^{}` 等於 release commit；之後以文件 commit 把 roadmap v5 段標為 Released／已釋出。
-->
