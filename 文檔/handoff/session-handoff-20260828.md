# Session Handoff — 2026-08-28

## Session 08:07

### 一、本 session 主題

架構討論「這包 bridge 到底保證什麼」（8/27 接力棒指定主題）：使用者分四輪給出 Product Promise → 依賴鏈上修 → 十條護欄 → v0 綁定表，AI 逐項查證後收斂成正式技術方向文件、過審、commit。零 schema 改動（照方向文件護欄，PoC 前不動 schema.yaml）。

### 二、完成事項

- **Bridge Guarantee 定案**：Product Promise 合併版（語意留初版閘門式、語感借改版）＋三條 mechanism-independent 保證（Contract Preservation / Verifiable Completion / Explicit Degradation）。
- **TDD 位置定案**：不進承諾本身，活在 Contract Verification 層（「目前版本對程式變更要求的驗證機制，證據 RED/GREEN」）——硬約束沒削弱、換了住址。
- **依賴鏈上修一層**：真根不是 Evidence Contract、是 Bridge Guarantee；四條卡住工作全部重新掛載。
- **v0 綁定表逐 skill 查證**：全部存在；`/to-tickets` 讀全文（107 行）確認四性質屬實＋撈到三個適配事實（`disable-model-invocation`、模板無 Contracts 欄、自帶第二套清單載體＝SSOT 待定）。
- **探索層定案**：不綁定、不建 router；預設 brainstorming → grilling、explore 為前置；harness 只規定出口條件（進 Task Decomposition 前要有被接受的 spec）。
- **正式文件落地**：`docs/superpowers/specs/2026-08-27-bridge-guarantee-architecture-direction.md`（定位＝技術方向與設計邊界、非 implementation spec；含七項未決顯式清單）。
- **審查**：Codex 額度耗盡 → 照 4.3.1 降級矩陣記 `[REVIEWER_FALLBACK]`、派 `contract-neutral-reviewer` 兩輪：第一輪 ✅ Mergeable（2 sub-threshold 當場修）、第二輪複驗零新缺陷 ✅ Mergeable；`review-state note doc_review pass` 已記。
- **Commit**：`b1abd82`（使用者親口核可；照 repo 慣例英文 conventional commits、無 AI 署名）。
- **登記**：`task-20260828-concept-poc`（概念 PoC，掛下一代改造底下）。

### 三、未完事項 / 接力棒

- [#接力] **下一步＝概念 PoC**（方向文件 §7）：證明最小鏈 `Requirement/Scenario → Task → Verification Method → Verification Result → Gate PASS/BLOCK`。PoC 前不動 schema.yaml、不建新 artifact。PoC 自己作為一個 change 走 brainstorm → spec → 核可。
- [#接力] **七項未決在文件 §6**，其中要使用者拍板的：#1 G1 要不要雙向（不偷加；AI 建議納入）、#2 CLAUDE.md 階段界線重表述（v0 已把 Orca 定為唯一 runtime）。
- [#接力] `fix-tdd-transitive-claim` **仍暫停**；文件 §6#7 明寫其第一題定案（丙）應保住，推翻要明說。
- [#不重議] 探索層不建 router 機制、`verify.md` 不重構、Evidence 不當主系統——均已定案寫進文件。
- [#環境] Codex 額度 8/27 22:30 已恢復；本 session 備援鏈（contract-neutral-reviewer via general-purpose agent）實測可用。

### 四、洞見 / 反省

**【紀律接力】**

- [#正] **「修完外送、不自查」這次照做了**：文件兩處 sub-threshold 修正後，交第二個獨立審查者專門盯「修 A 造 B」，複驗確認零新缺陷——8/27 學習候選（修改動作本身是缺陷產生源）的直接應用。
- [#反] **Codex 額度三天內第二次在審查中途耗盡**。這次 fallback 鏈走通（照 4.3.1 降級矩陣派 `contract-neutral-reviewer`、記 `[REVIEWER_FALLBACK]`、驗 sentinel），沒把審查掛起來等。attribute: 全域 CLAUDE.md 複審紀律「複審開跑前先定 fallback 鏈」。propose action: 無需新規——本次即為該條的正常執行，記錄以供下次直接照走。

**【當日洞見】**

- [#洞見] **表面瓶頸與真瓶頸差一層**：AI 診斷「四條卡在證據契約」，使用者上修「證據契約自己卡在 Bridge Guarantee」。錯誤的形狀是把中間層當根——中間層看起來像根，因為所有下游確實都指向它。
- [#洞見] **探索層綁單一 skill 是對自家原則的自違反**——「規定證據不規定步驟」的 repo，自己的綁定表把保證範圍上游的探索層釘死成一個 skill，與 plan 放寬要刪的句子同型。
- [#洞見] **`/to-tickets` 三個適配事實全部只有讀全文才撈得到**——「讀了名字沒讀實際說什麼」的正面對照組：這次先讀完才進綁定表。
- [#決策] **v0 把 Orca 定為唯一 runtime＝階段界線正式跨過**；CLAUDE.md 兩階段表在方向落地時要重表述（文件 §6#2）。

**【學習候選】**

> Gate 第 3 次手動試跑（累計 3 / 目標 5，見 `驗收節點.md` 2026-09-10 節點）。同樣標註：我知道閘門在驗什麼，成績受污染。

- **Case**：AI 診斷四條工作的共同卡點是 Evidence Contract；使用者把診斷再上修一層到 Bridge Guarantee，四條工作隨即自然重新掛載。
- **Candidate Pattern**：多條工作卡在同一個中間層時，SHALL 先問「這個中間層自己是從哪裡推導出來的」——共同卡點常常還有上游。邊界：卡點若是外部依賴（額度、他人）不適用。
- **Evidence**：1 次，標 **Hypothesis**。
- **Minimum Sufficient Intervention**：不新增規則——「動工前三問」已含背景層提問；缺的是把「發現共同卡點」當成再上溯一層的觸發訊號。無 enforcement 掛點 ⇒ 依規則停在 Observe。
- **Promotion**：History only（傾向），由使用者決定。

### 五、檔案異動

| 異動 | 內容 |
|---|---|
| `b1abd82` | `docs/superpowers/specs/2026-08-27-bridge-guarantee-architecture-direction.md` 新增（246 行） |
| 未進版控 | `2026-08-27-brainstorm-產品承諾.md`（討論工作紀錄，repo 根，照 8/25、8/26 慣例不 commit） |
| （本次收工） | `workflow-harness/work-map.jsonl`（+1 筆 `task-20260828-concept-poc`）、本 handoff |

錨來源：本 session 開工 commit（fb9be44、開工於 2026-08-27T18:10:06）——列 fb9be44..HEAD

### 六、下一步建議

1. **拍板未決 #1（G1 要不要雙向）**——一句話能定，定了 PoC 的 verify 對照就知道要不要看反方向。
2. **概念 PoC 立 change**：走 brainstorm → spec → 核可（照探索層定案，brainstorming 起手、要打就 grilling）。
3. **CLAUDE.md 階段界線與兩階段表重表述**——可與 PoC change 一起或先行小 change。
4. **`fix-tdd-transitive-claim` 依新方向決定**：恢復（照丙案只刪假宣稱）或併入 PoC 後續。
