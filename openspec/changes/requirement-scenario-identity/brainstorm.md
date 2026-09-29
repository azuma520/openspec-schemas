# Brainstorm — requirement-scenario-identity（2026-09-29）

> Raw capture：決策日誌。分類：**architectural**（改變採用者必須遵守的 spec 格式、跨 schema major）。
> 已呼叫 `superpowers:brainstorming`（6.4.1）；依 schema `brainstorm` instruction 的輸出重導，寫入本檔、不寫 `docs/superpowers/specs/`。
> 探索、選項與裁定均在 2026-09-29 同一場對話完成，本檔保存決策鏈，作為 proposal / design / specs 的來源。

## 背景

- 主線排序（2026-09-29 使用者選方案一）：需求追蹤正式實作拆成 **Identity → Task→Requirement（`Contracts:`）→ 驗收台帳 → Gate/freshness → 歸檔身分檢查**。本 change 是第一塊，work-map `task-20260929-requirement-scenario-identity`。
- 範圍上限：只做正式設計（`docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`，2026-09-24 核可版 `8002fa0`）§3.1 的 stable ID 身分層。**不加 `Contracts:`、不做 `verification-results.json`、不做 executable Gate。**
- 載體已由 Spike S1 拍板：標題載體（`docs/superpowers/poc/2026-09-01-capability-spikes/spike-report.md` § S1）。

## 實測事實（2026-09-29，openspec 1.3.1，scratchpad 複本，未動 repo）

| 測什麼 | 結果 |
|---|---|
| `### Requirement: REQ-1 …`／`#### Scenario: REQ-1-S1 …` 搭配 ADDED / MODIFIED / RENAMED | `openspec validate --all --json` 全 valid；`openspec archive -y` 成功，合併後 ID 全在 |
| 補號遷移（RENAMED 舊標題 → `REQ-n 舊標題`，同 change 以新標題 MODIFIED 全文、情境標題補 `REQ-n-Sm`） | 本 repo 實際 specs 複本：3 capability、10 條 requirement、37 個 scenario 一次完成；`validate --strict` valid；archive 後與預期逐行比對一致（忽略空行） |
| 同一 capability 兩條 requirement 都叫 `REQ-1`、兩個 scenario 都叫 `REQ-1-S1` | **CLI 完全不擋**，validate valid、archive 照合併 ⇒ 重號檢查必須由 bridge 自己做 |
| `MAX_DELTAS_PER_CHANGE = 10`（`core/validation/constants.js`，套在 `change.schema.js` 的 `deltas` 陣列） | 補號 change 含 10 MODIFIED + 10 RENAMED 仍 `--strict` valid ⇒ ~~此上限不是 spec delta 筆數~~（推論理由錯誤，見 Q12：計數對象就是 spec delta，只是 validate 路徑碰不到、archive 路徑只警告不擋） |

現況盤點：schema 中身分相關只在 `specs` instruction（`### Requirement: <name>` 格式段）與 `templates/spec.md`；verify 現有 checks 1–12，無任何 ID 檢查。本 repo 主 spec 中 `REQ-PB`（`repo-guidance`）是唯一既有 stable ID，其兩個 scenario 無 ID。

## 決策鏈

### Q1 版本號

**裁定：升 schema major 3。**依據 bridge README「Why v1 → v2 is a schema-major bump」自己的定義——原本合法的 artifact 變不合法即為 breaking；無編號 spec 在本 change 後過不了 verify。

**使用者修正**：v3 描述的是**相容性邊界**，不是 roadmap 階段。不預先宣告後續 `Contracts:`／驗收台帳／Gate 都屬 v3；每個後續 change 依它本身是否再讓「既有合法 v3 artifact 變不合法」各自判斷是否需要 v4。

否決：每塊各跳一次（先驗承諾多次遷移）；不跳版本、只查新寫的需求（等於為了不跳版本改寫 breaking 定義，README 已明文否決此路）。

### Q2 既有 spec

**裁定：一次補完，不留 legacy 例外。**本 repo 3 capability、10 條 requirement、37 個 scenario 在本 change 內補號；check 13 的範圍涵蓋所有主 spec。理由（使用者）：成本已實測可控；Identity 本身在解決「東西是誰」，第一版就留兩套身分制度違背目的。

`REQ-PB` 保留（正式設計 §3.1 grandfathered）；其兩個 scenario 補為 `REQ-PB-S1`、`REQ-PB-S2`——保留既有 ID 是保護既存 identity，不等於底下永遠不建立 scenario identity。

### Q3 檢查形式

**裁定：verify 新增 check 13，與 checks 8–12 同層級**——判準 deterministic、machine-evaluable，執行者仍是 verify agent。真正不可繞過的 executable Gate 留給後續 Gate change。

**Claim boundary（必須照此措辭，不得寫強）**：「verify 已有判準固定的 identity integrity check，由 verify agent 依規則執行；真正不可繞過的 executable Gate 尚未實作。」**不得**寫成「Harness 已機械保證 ID 不會出錯」。（→「必須照此措辭」已由 Q9 修訂：spec 為 owner，其他 artifact 摘要或引用。）

否決：本版就寫可執行腳本（仿 PoC `gate_check.py`）——Gate 排在後面那塊，此處提前做會讓本 change 長成半套 traceability system。

### Q4 本 change 與「歸檔身分檢查」的切面

**本 change 做（當前 change／current spec 即可判斷的 identity integrity）**：缺 ID、同一 capability 內同一 local ID 指向不同契約、scenario ID 不屬於所在 requirement、RENAMED 換 ID。

**留給歸檔身分檢查（需要歷史或歸檔前後比較）**：退休 ID 不得重新指派；MODIFIED／archive 過程不得無聲弄丟 scenario ID（MODIFIED 為全文替換，情境在此被刪時本 change 抓不到）；scenario retirement 紀錄格式。

### Q5 ID 語法與新號配置

分成兩個問題：**「這個 ID 合不合法存在」**與**「新 ID 可以怎麼發」**。

- **Requirement ID 合法語法**：`REQ-` + 大寫英數（`[A-Z0-9]+`），故 `REQ-PB` 合法。標題形狀 `### Requirement: <ID> <描述>`，描述不得為空。
- **Scenario ID 語法**：`<所屬 requirement 的完整 local ID>-S<正整數>`，例 `REQ-3-S1`、`REQ-PB-S2`。`S` 後只能是數字。
- **新 requirement（出現在 ADDED）**：ID MUST 為數字型 `REQ-<正整數>`，且 MUST 大於該 capability **目前主 spec** 中所有數字型 requirement ID。新建 `REQ-FOO` 被擋——不是因為解析不了，而是違反新號配置規則。不建立 legacy registry。
- **新 scenario**（ADDED requirement 下的全部 scenario，或 MODIFIED requirement 中主 spec 該 requirement 沒有的 scenario ID）：序號 MUST 大於**同一 requirement** 目前主 spec 中已有 scenario 的最大序號；不跨 requirement 合算。

**否決的原案「必須等於目前最大值 + 1」**（使用者先提、後撤回）：反例——歷史上 `REQ-10` 已退休，目前主 spec 最大只剩 `REQ-9`，強制 `max(current)+1` 會把退休的 `REQ-10` 指定成唯一合法新號，直接違反「退休 ID 不得重用」（正式設計 §3.1）。故拆兩層：

| 層 | 內容 | 誰執行 |
|---|---|---|
| check 13 檢查 | 新 ID 為數字且**大於目前主 spec 最大值**——保證不倒退、不撞 current identity | verify agent 依規則 |
| 發號規則（MUST，寫在 specs instruction） | 取號基準是**歷史上用過的最大號**：連同已歸檔 change 的 delta spec 一起看，往上取 | 寫 spec 的 agent |
| 未撞到 retired identity | 延後 | 歸檔身分檢查那塊 |

**空集合**：沒有任何既有數字型 requirement ID 時，check 13 的下限是 `REQ-1`（任何正整數都大於空集合）；某 requirement 沒有既有 scenario 時，下限是 `S1`。發號時仍須先查歷史——空的主 spec 不代表沒用過號碼（例：該 capability 的 requirement 曾全部退休），此時從歷史最大號往上取，不是固定從 1 開始。

### Q6 「同一契約」的機械定義（取代「字串出現兩次＝重號」）

沿用 9/24 正式設計修訂的精確語意：**同一 capability 內，同一 local ID 不得指向兩個不同的 contract identity**；同一契約在多處出現不是錯。「是不是同一契約」由 artifact 結構與 OpenSpec 操作角色導出，不由 agent 讀文字判斷：

| 情形 | 判定 |
|---|---|
| 主 spec 的 `REQ-3` ＋ delta `MODIFIED` 的 `REQ-3` | 同一 identity，合法 |
| `RENAMED` 的 FROM 與 TO | **FROM 與 TO 的 local ID 必須相同**；不同 → BLOCK |
| `ADDED` 的 `REQ-3` ＋ 主 spec 已有 `REQ-3` | 新契約搶既有 identity → BLOCK |
| 同一檔案（同一載體）內兩個不同 block 都宣告 `REQ-3` | BLOCK |
| 兩個 `ADDED` block 都宣告 `REQ-3` | BLOCK |

Scenario 同理，在所屬 requirement 內判定。

### Q7 check 13 的內容（草案，待 specs / design 落定措辭）

範圍：所有主 spec ＋ 本 change 的 delta spec。（→ 已由 Q9 細化：驗收對象是預演歸檔後的主 spec，歸檔前狀態只作判斷基準。）

1. 每個 requirement／scenario 標題都有合法 ID（Q5 語法）→ 否則 BLOCK
2. 同一 local ID 指向不同契約（Q6 表）→ BLOCK
3. scenario ID 前綴不等於所屬 requirement ID → BLOCK
4. RENAMED FROM／TO 的 local ID 不同 → BLOCK
5. 新 ID 不符 Q5 配置規則（非數字，或不大於目前最大值）→ BLOCK
6. 交叉核對（正式設計 §3.3）：從文字抽出的 requirement 數與 CLI JSON 的 requirement 數不一致 → BLOCK；語意是兩種方法互相抓錯，不預設哪邊對。scenario 層的交叉核對做法（CLI 對 scenario 只吐 `rawText`、不吐標題）在 design 階段確認

### Q8 證據命名

- 以故意做錯的小範例（mutation fixtures）驗 check 13：缺號、重號（Q6 各列）、前綴不符、RENAMED 換 ID、新號違規、數量不一致，外加一組全部正確的 happy path。
- **這些 fixtures 稱為 mutation / acceptance evidence，不稱 TDD evidence。**本版 check 13 是 agent 依 deterministic instruction 執行的規則，沒有可執行的 checker，無法形成有意義的 RED→GREEN。
- （→ 本條與上一條：Q10 曾改為 `TDD: applicable`；Q11 再改回 `n/a`、理由換成正式設計 §4.3 的範圍；**最終由 Q14 定為 `TDD: applicable`（行為判準）**，原句「無 executable checker 故無法形成有意義的 RED→GREEN」不再使用。）TDD applicability **逐 task 判定**，不寫成整個 change 一律 n/a。對應 task 標 `TDD: n/a — 本版 identity check 為由 verify agent 依 deterministic instruction 執行的規則，尚無 executable checker，無法形成有意義的 RED→GREEN。`；若某 task 實際新增可執行程式或其他可 TDD 的行為，該 task 重新判定。
- **fixtures 證明的範圍（寫進 README／design 的 claim boundary）**：第 13 條文字規則具有足夠的可執行明確度，agent 依規則能對已知反例做出預期判定。**不證明**：Harness 已自動強制這些 identity invariants。
- 後續 Gate change 寫出真正的 checker 時，同一組 fixtures 可作為那時的 RED/GREEN 素材。

### Q9 後續補充裁定（寫 proposal / design 期間，2026-09-29）

- **proposal 格式**：模板四段之外新增 `## Out of Scope`、`## Assurance Boundary` 兩段（OpenSpec parser 只要求 `## Why`、`## What Changes`，未知段落略過）。本 change 當 dogfood，不改 `templates/proposal.md`；retrospective 再評估。Modified Capabilities 改寫為「需求標題（身分）變更、行為不變」。
- **宣稱邊界的 owner（修訂 Q3 的「必須照此措辭」）**：`contract-identity` spec 是 normative owner；proposal 只做摘要並指向 spec，design 只說理由，README 摘要並連結。審查比對語意一致、不要求逐字一致。原提議「四處逐字抄、逐字比對」撤回——那是主動製造同步副本。Q3 的措辭仍是 spec 撰寫的起點，但不再是其他 artifact 必須逐字複製的文字。
- **D5 兩個角色**：歸檔前狀態＝判斷基準（context），預演歸檔後狀態＝要驗收的候選狀態（candidate state）；預演歸檔失敗即 BLOCK。
- **交叉核對**：scenario 按順序配對是 openspec 1.3.1 的已知依賴假設；無法可靠配對 → BLOCK。**不設降級出口**——身分完整性是 Core Integrity Invariant I1（正式設計 §2.1），不可關閉、不進 override 模型。

### Q10 文件審 r1 後的裁定（2026-09-29，Codex thread `01a0ec4a`）

- （→ 本點先由 Q11 推翻（改回 n/a），再由 Q14 定為 applicable，但 RED 內容改為真實的錯誤判定、不是 `INDETERMINATE`。）**推翻 Q8 的 `TDD: n/a`**：現行 `tdd-evidence-contract`（2026-09-14 fix-v2 納入）已明定「以閱讀執行的規則」可形成 TDD、RED 可記 `INDETERMINATE`；Q8 的前提「無 executable checker 故做不出有意義的 RED→GREEN」與之衝突（Codex r1 🔴）。使用者選**甲：新增 check 13 規則文字的 task 標 `TDD: applicable`**，每個 fixture 為一個 subject，RED `INDETERMINATE`（加規則前）→ GREEN（加規則後），前例 fix-v2 的 f12。
  - **證據力要克制**：對尚不存在的規則，RED 幾乎必然成立，只證明舊規則集判不出此案例，不是強的 test-first 證據；承重的是 GREEN。RED 合乎 contract，但證據力弱。
  - 改叫 TDD evidence 不提高任何 assurance 宣稱：仍只證明 agent 執行的規則可被驗證，不證明 Harness 有不可繞過的 enforcement。
  - 否決：維持 n/a 換理由（找不到不衝突的理由）；修改 tdd-evidence-contract 排除此類規則（推翻 9/14 已定規則、超出範圍）。
- **兩種 BLOCK 的邊界補齊**（Codex r1 🟡，使用者裁定本輪一併補）：交叉核對已可靠配對並完成、但數量不一致＝**違規**（查完了、不符合）；只有比對本身無法可靠完成（CLI 缺資料、輸出結構變了、順序無法配對、預演歸檔失敗）才是**無法判定**（查不完、不能證明符合）。兩者都 BLOCK。
- **交叉核對擴及 delta 的 scenario 數量**（Codex r1 🟡）：原本 delta 只核對 requirement 數；Requirement 與 Scenario 都要有 stable identity，核對也要兩層都做。
- **遷移指南改為單一 change 補完所有 capability**（Codex r1 🔴）：按 capability 分批的 change 會被 check 13 對全部主 spec 的判定擋下，與 Q2「全部檢查、不留 legacy 例外」不相容。

### Q11 TDD 改回 n/a（2026-09-29，推翻 Q10 第一點；本題已由 Q14 推翻）

- **事實更正**：Q10 時 AI 稱「維持 n/a 找不到不與契約衝突的理由」，這是錯的，漏看兩處：①正式設計 §4.3 把 TDD 限定在 executable-behavior code task，並明寫「改文件、純資料調整等不 applicable 的 task 不硬造 RED/GREEN」；②schema tasks instruction 的 n/a 理由種子詞包含 prose/doc-only。
- **分清兩個問題**：`INDETERMINATE` 條款回答「若決定對以閱讀執行的規則做 TDD，RED 可以長什麼樣」（允許、不要求）；§4.3 回答「哪些 task 必須進 TDD policy」。第 13 條是規則文字，可以做 TDD，但不屬必須納入的範圍。Codex r1 🔴 抓到的是 Q8 那句理由（「無 executable checker 故做不出 RED→GREEN」）與條款衝突，不是 n/a 本身。
- **使用者選乙**：相關 task 標 `TDD: n/a — schema instruction / prose rule，不屬於正式設計 §4.3 所定義的 executable-behavior code task`。mutation fixtures、正反案例、archive 預演、數量交叉核對全部照做，角色是 **conformance / acceptance evidence**，也是主要證據，不包裝成 RED→GREEN。
- **學習候選（Identity 結束後另立研究題）**：兩份契約分別回答不同問題，使用時被混在一起——§4.3 與 `tdd-evidence-contract` 之間的邊界落差。研究題：驗證方法是否應依 artifact 類型／宣稱類型路由，而不是先問 TDD applicable / n/a。
- **Fable 代審**：Codex 額度用完（r3 `codex_fail`）。本輪修完後改以 Fable 跑 `contract-neutral-reviewer`（thorough），記 `[REVIEWER_FALLBACK]`——它記的是這輪由誰審（provenance），不是審查品質比較差。Codex 恢復後是否補審，看 Fable 的 finding 性質再判：若 Fable 抓到正式設計矛盾或跨 artifact contract drift 這類高承重問題，修完後傾向等 Codex 補一次。

### Q12 Fable 代審後的修正（2026-09-29，使用者選甲：現在修、再請 Fable 複審）

Fable 代審 ✅ Mergeable（0 個 🔴），但提出 4 🟡 ＋ 1 ⚪，使用者裁定全部現在修，範圍只限這 5 條，不重整其他措辭、不開新設計題：

1. **MODIFIED 經 RENAMED 對應回 FROM**（REQ-3 新增 S6、REQ-4、design D4 表）：補號遷移時 MODIFIED 用的是 TO 標題，主 spec 還沒有它；規則補上「標題等於同檔 RENAMED 的 TO 者，經該對應回到 FROM 那條，是同一契約」，其 scenario 是否為新對照 FROM 那條。原本照字面讀會找不到對象。
2. **RENAMED 的計數單位**（REQ-6、design D6）：一組 FROM / TO 算一筆 rename。
3. **proposal 摘要落後 owner**（D10 的第一個實例）：proposal 原寫「對所有主 spec 檢查缺 ID」，owner（spec REQ-5）已是「驗收預演歸檔後的候選狀態」；改摘要對齊語意。
4. **`MAX_DELTAS_PER_CHANGE` 的理由更正**：原推論「此上限不是 spec delta 筆數」理由錯。讀 openspec 1.3.1 原始碼：計數對象就是 spec delta；`validate` 走 `validateChangeDeltaSpecs` 碰不到；`archive` 雖呼叫 `validateChange`，但程式註明 proposal 驗證 informative only、不擋歸檔（主 session 覆核時補查到這點）。結論「不受影響」不變，理由換成真的。
5. **佔位符統一**：proposal 的 `<ID>-S<n>` 改為 `<REQ-ID>-S<m>`，與 design、spec 一致。

複審通過即進 tasks，不需為這批 finding 等 Codex 補審——這些屬規格精確度、摘要落差、實證理由，不是正式設計矛盾或跨 artifact contract drift。

### Q13 Fable 複審後再修一小輪（2026-09-29）

Fable 複審 ✅ Mergeable（0 🔴），提出 3 🟡 ＋ 3 ⚪。使用者裁定**先不進 tasks**：其中一條會讓 task 驗錯狀態，不能留給 task 去補設計。

- **原則**：`Mergeable` ≠「所有 finding 都應延後」——它只表示沒有必須阻止 merge 的問題。在 design → tasks 的邊界上，會影響 task 推導的 finding 即使是 🟡 也現在修。tasks 應該承接設計，不應該替設計補洞。
- **現在修**：①proposal 的 Modified Capabilities 導言把 RENAMED 一般化到四個 capability，但 `repo-guidance` 只有 MODIFIED——已改寫（摘要落差，D10 的第二個實例）；②**REQ-6 與 design D6 補上「CLI 要對它所判定的狀態跑」**：候選狀態的主 spec 核對在暫存複本、預演歸檔後執行，change 層核對對歸檔前狀態執行——否則會成功執行卻比錯對象；③design 對 `rename.from` / `rename.to` 的描述改精確（是 `### Requirement:` 之後的標題名稱、不含前綴）；⑤spec 內兩處連續空行清掉。
- **留給 tasks 當實作驗收細節（不升為 normative contract）**：④`openspec show <change> --json --deltas-only` 在 1.3.1 會往 stderr 印 `Warning: Ignoring flags not applicable to change: scenarios`，第 13 條規則要叫 agent 只讀 stdout，否則 JSON 解析失敗、被誤判為無法判定；⑥change JSON 中 ADDED / MODIFIED 條目的情境陣列欄位是 `requirement.scenarios`（同條目另有 `requirements` 陣列），規則文字寫明確切欄位。
- 修完在同一個 Fable 審查脈絡續審；通過即凍結 brainstorm / proposal / design / specs，開始 tasks.md。

### Q14 TDD 改為 applicable，採行為判準（2026-09-29，推翻 Q11）

- **為什麼推翻**：寫 tasks 前讀上一個同類 change（fix-v2）的 tasks.md，查到 **2026-09-07 使用者裁定**：「applicability does not turn on whether a conventional test framework runs the case; it turns on whether the same re-runnable case shows the old behaviour violating the contract before the edit and the corrected verdict after it.」Q11 做決定時漏查了這條已決。原因不是 `INDETERMINATE` 條款強迫文字規則做 TDD。
- **更正錯誤推論**：Q10／Q11 都以為加規則前的 RED 只會是 `INDETERMINATE`（判不出來）。實際上舊 verify（checks 1–12）對缺 ID 的 fixture 預期會**明確放行**——這是真實的錯誤判定，證明現行系統有一個可重現的契約缺口。⚠️ 此點目前仍是推論，由 RED task 在改 schema 前實跑確認。
- **使用者選甲**：本 change 採 9/07 的行為判準，第 13 條相關 task 標 `TDD: applicable`。`schema.yaml` 雖是文字，但它改變 verify agent 面對固定案例時可觀察的判定行為。
- **條件**：
  - RED 必須在修改 `schema.yaml` 之前實際跑出並保存，不得事後推論「以前應該會 PASS」。
  - RED / GREEN 同一 fixture、同一受測對象、同一執行方式，唯一變數是第 13 條規則。
  - 只有舊判定與新契約不一致的 fixture 是 TDD subject（`<fixture 目錄>::<預期判定>`，沿用 fix-v2）；正向範例與已被早先檢查擋下者只作 conformance evidence，不硬湊 RED（AI 補充、使用者同意方向）。
- **兩件事分開**：TDD evidence 可以成立（有真實的 RED→GREEN 行為轉變）；assurance 仍只是 agent 執行的固定判準，不是不可繞過的 executable Gate。
- **不解決的張力**：此裁定不自動解決正式設計 §4.3（artifact 類型判準）與 9/07 裁定（可觀察行為判準）之間的範圍落差，留待 Identity 完成後的獨立研究：**TDD applicability 應由 artifact 類型決定，還是由可觀察行為／可重跑案例決定？**
- 改動改到 applicability 與證據策略，先前的文件審 pass 不沿用，修完重審再進 tasks。

## 連動範圍（依 repo CLAUDE.md「跨檔耦合」表）

- `superpowers-bridge/schema.yaml`：`specs` instruction（語法、配置規則、RENAMED 保 ID）、`verify` check 13；`version: 2` → `3`
- `templates/spec.md`、`templates/verify.md`
- bridge `README.md` ＋ `.zh-TW.md`：格式說明、verify 檢查清單、Versioning（v3 為相容性邊界的說法）、v2 → v3 遷移指南、Compatibility 表新列、Known breaking changes
- `.github/workflows/version-check.yml`：抓 `^\| v2 \| ` 的那行（未同步則 CI 直接 fail）
- `superpowers-bridge/VERSION`、repo `CLAUDE.md`「兩個版本號別搞混」與跨檔耦合表中寫死 `v2` 之處
- `docs/roadmap.md` ＋ `.zh-TW.md`
- 本 repo `openspec/specs/` 補號（Q2），及本 change 自身的新 capability spec
- mutation fixtures（Q8），落點比照 `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/`

## 未查證

- ~~`MAX_DELTAS_PER_CHANGE` 實際計數對象（推測為 proposal 的變更清單，未追）~~ 已查明，見 Q12。
- scenario 層與 CLI JSON 的交叉核對做法（Q7 第 6 點）。
- 有沒有外部採用者釘在 v2。
