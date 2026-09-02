# Session Handoff — 2026-09-02

## Session 07:59

### 一、本 session 主題

loosen-plan change 開工(2026-09-01 晚間起、跨午夜):Q1–Q5 brainstorming 全數拍板,artifacts 4/8(brainstorm / proposal / design / specs 落檔、validate 過),research 分析文檔 ×2 落檔並建索引。

### 二、完成事項

- 開工三步驟:跑 /work-status、讀 9/1 handoff 四個 session 區塊、接力棒 3 條逐條交代、提優先建議 3 條;doctor 唯一警告為 work-map 未知 key `evidence`(前向相容保留、使用者裁示放著)。
- 前置閱讀:正式設計全文、spike 報告全文、現行 schema.yaml + plan/tasks 模板、work-map record。
- 開 change:`openspec/changes/loosen-plan/`(--schema superpowers-bridge),dogfood 副本確認同步。
- **Q1 拍板**:TDD 證據契約與 plan 放寬綁同一 change(同一治理轉換的左右兩半);scope 封閉集四項、其餘 Bridge Guarantee 能力不帶。
- **Q2 拍板**:先定 Plan Contract 再選 producer;writing-plans(172 行)與 /to-tickets(107 行)全文閱讀後做逐元素「保留/修改/移除/新增」比較;(a) Interfaces 條件式必填、(b) fail-closed 雙落點。
- **Q3 拍板**(兩輪修正收斂):TDD Evidence 最小契約——tasks.md 為 applicability SSOT;RED claim 定稿為「同一 subject 曾被執行、因目標行為尚未成立而正確失敗;支持 RED→GREEN 轉變、不支持完整 TDD history」;5 required 欄 + invocation supporting;假 state ref 移除;suite-green 留 change-level;九項明確不做清單。
- **Q4 拍板**:producer = agent direct generation;residual risk 明寫(機械檢查只托底結構完整性、語意品質靠 producer + Review);C(Harness-native skill)留觸發條件明確的升級路徑;writing-plans 移除 normative dependency 不禁止;/to-tickets 吸收不 invoke。
- **Q5 拍板**:schema major 升 2、bundle 2.0.0——主理由 backward compatibility(v1 合法 tasks.md 升級後會被新 verify 擋)、副理由 PRECHECK shape 命中 policy;`version: 2` CLI 全鏈路實測正常(validate/schemas/new/status/instructions)。
- artifacts 落檔:brainstorm.md(Q1–Q5 決策日誌)、proposal.md(經使用者三點收口修訂:fail-closed 宣稱限定、PRECHECK 理由改寫、versioning 拍板)、design.md(D1–D7)、specs ×3(plan-contract ADDED、tdd-evidence-contract ADDED、tdd-claim-accuracy MODIFIED);`openspec validate` 通過。
- research 文檔落檔 + 索引:`docs/superpowers/research/`(plan-structure-comparison + tdd-evidence-analysis + README 索引);CLAUDE.md 結構樹補 poc/ + research/、相關連結加索引行。

### 三、未完事項 / 接力棒

- [#接力] **design.md(D1–D7)+ specs ×3 待使用者核可**——上次呈現重點:SSOT 分工表(不產生第二個 SSOT 的落法)、三 capability 邊界互不侵犯。核可後進 tasks artifact(展開跨檔耦合清單:schema description / 兩 README / adopters fragments / version-check.yml grep / VERSION 2.0.0 / migration guide)。
- [#接力] **doc gate 批清**:本 session 約 10 個 .md 新增/修改未過 /codex-review-doc(見四【紀律接力】)。
- [#接力] 下次 push 順驗 GitHub Actions 是否自動觸發(沿 9/1 session 接力、fork 啟用後首次 push 為最終實測)。
- [#不重議] Q1–Q5 均已拍板、記錄於 change 的 brainstorm.md——後續 artifact 遇同題引用出處照辦,不重提。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] 動工前查已決兩次兌現:「更適合的 skill 參考」靠 grep handoff + 方向文件找回 /to-tickets 綁定表,沒憑印象猜;版本題被使用者攔下「graph 沒變 → non-breaking 推論跳太快」後,查 policy 原文 + 實測 `version: 2` 全鏈路才端決策。
- [#債] **doc gate 未清**:本 session 新增/修改約 10 個 .md(research×3、CLAUDE.md、change artifacts×6),/codex-review-doc 未跑——change artifacts 仍在使用者審閱中、收斂後一批審,**下 session 必清**。

**【當日洞見】**

- [#決策] loosen-plan Q1–Q5 全數拍板(詳 change 的 brainstorm.md):TDD 證據契約與 plan 放寬綁同一 change(同一治理轉換的左右兩半);Plan Contract 先於 producer 選型;TDD 最小證據契約(5 required + invocation supporting);producer = agent direct generation + 觸發式升級路徑;schema major → 2(主理由 backward compatibility、副理由 PRECHECK policy 命中)。
- [#洞見] writing-plans 與 /to-tickets 不是競爭者——防不同的失敗(執行者太笨 vs 計畫太快過期);Plan Contract = 留協調資訊、換控制機制。
- [#洞見] 舊 TDD 保險絲大半是想像的:規定了步驟、驗證了零(apply instruction 自己承認);新制放寬的只有路徑自由度,Harness 可驗證 assurance 是淨升級(宣稱範圍限定至此)。
- [#洞見] spec 釘措辭的反向效應:tdd-claim-accuracy 把「schema 不驗證 TDD」釘成規格——實作升級後不改 spec,規格反而強迫繼續宣稱「沒驗證」。假合規的鏡像案例(spec 比實作弱也會製造 drift)。

**【學習候選】**

沒有——版本題「先查完再分析」是既有全域「能碰就碰／證據先於斷言」的又一例,已有 always-on 載體,不硬造新規則。

### 五、檔案異動

本 session 無新 commit;改動全在 working tree(收工 commit 收入):

| 異動 | 內容 |
|---|---|
| 新增 | `openspec/changes/loosen-plan/`(brainstorm / proposal / design / specs×3) |
| 新增 | `docs/superpowers/research/`(README 索引 + plan-structure-comparison + tdd-evidence-analysis) |
| 修改 | `CLAUDE.md`(結構樹補 poc/ + research/、相關連結加 research 索引行) |
| 修改 | `workflow-harness/work-map.jsonl`(loosen-plan 標 DOING,收工結算) |
| 未進版控 | `2026-08-27-brainstorm-產品承諾.md`(沿慣例) |

錨來源:本 session 開工 commit(fa3ad02、開工於 2026-09-01T15:33:10)——列 fa3ad02..HEAD(無新 commit)

### 六、下一步建議

1. **核可 design + specs → 進 tasks artifact**:tasks 會把跨檔耦合展開成工作項(schema.yaml 各段 / 模板×2 / 兩 README + migration guide / adopters fragments / version-check.yml / VERSION);Q1–Q5 已全拍板、tasks 之後 plan artifact 將是新 Plan Contract 的第一次 dogfood。
2. **doc gate 批清**(research ×3 + CLAUDE.md + change artifacts,一個 /codex-review-doc dispatch)。
3. 下次 push 順驗 Actions 自動觸發(fork 啟用後最終實測)。
