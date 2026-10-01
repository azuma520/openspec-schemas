## Context

- 正式設計（`docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`，2026-09-24 核可版 `8002fa0`）§3.1 定義身分層：每條可追蹤 Contract 有 stable ID、heading 載體、capability 內唯一、改措辭不改 ID、退休不重用、不建 registry、fail-closed。§3.3 規定任何從文本抽取的計數都要與 CLI JSON 交叉核對。Spike S1 已拍板 Scenario 也用標題載體。
- 現況：schema 中身分相關只在 `specs` instruction 的格式段（`### Requirement: <name>`）與 `templates/spec.md`；verify checks 1–12 沒有任何 ID 檢查。本 repo 主 spec 共 4 個 capability，唯一既有 stable ID 是 `repo-guidance` 的 `REQ-PB`。
- OpenSpec 1.3.1 的實際行為（2026-09-29 實測，細節見 brainstorm.md「實測事實」）：
  - 帶 ID 的標題在 validate / archive 下完全正常；補號遷移（RENAMED ＋ 以新標題 MODIFIED 全文）在本 repo 實際 specs 複本上一次成功、合併結果逐行一致。
  - **CLI 不檢查 ID**：同一 capability 兩條需求同為 `REQ-1` 照樣 valid、照樣合併。
  - CLI JSON 不吐 Requirement / Scenario 標題：spec 層 `openspec show <spec> --type spec --json` 給 `requirementCount` 與每條 requirement 的 `scenarios` 陣列（只有 `rawText`）；change 層 `openspec show <change> --json --deltas-only` 給每筆 delta 的 operation 與 scenarios，RENAMED 則給 `rename.from` / `rename.to`，其值是 `### Requirement:` 之後的標題名稱（含 ID，不含 `### Requirement:` 前綴；例 `"to": "REQ-1 Plan is a per-task execution contract"`）。
  - 沒有 archive dry-run。
- 約束：事件閘門雙 YES 已成立，本 change 走一般 opsx 流程；不改 OpenSpec CLI；本 repo 無程式碼、無測試框架。

## Goals / Non-Goals

**Goals:**

- Requirement / Scenario 有可被機器引用、不隨措辭改變的 stable ID，寫法與新 ID 配置有固定規則。
- verify 有一條判準固定的 identity integrity check（check 13），能擋下「當前 change ＋ 當前主 spec」就判得出來的身分錯誤。
- 本 repo 既有 spec 全部補號，不留兩套身分制度。
- 以 schema major 3 誠實標示相容性破壞，附遷移指南。

**Non-Goals:**

- `Contracts:` 承接標註、`verification-results.json` 驗收台帳、executable Gate（後續 change）。
- 需要歷史或歸檔前後比較的身分檢查：退休 ID 不得重新指派、MODIFIED / archive 不得無聲弄丟 Scenario ID、Scenario 退休紀錄格式（歸檔身分檢查那一塊）。
- 判斷同一 ID 下的語意有沒有被改弱（屬 G1a 語意審查，正式設計 §8#4）。
- capability 改名時的 ID 延續（正式設計 §8#10）。

## Decisions

### D1：schema major 2 → 3，版本號表示相容性邊界

- **選擇**：本 change 將 `schema.yaml` 的 `version` 升為 3、bundle 升為 `3.0.0`。README 的 Versioning 說明 v3 的起點是「無 ID spec 變不合法」；後續 change 是否仍屬 v3，依它本身是否讓既有合法 v3 artifact 變不合法各自判斷，不預先把整條 traceability roadmap 綁成 v3。
- **理由**：bridge README「Why v1 → v2 is a schema-major bump」已定義 breaking＝原本合法的 artifact 變不合法，本 change 正是如此。
- **已考慮 alternative**：後續幾塊一律併入 v3、全部做完才發版（把版本號綁成專案階段，使用者否決）；每塊各跳一次（先驗承諾多次遷移）；不跳版本、只檢查新寫的需求（等於為了不跳版本改寫 breaking 定義，README 已明文否決這條路）。

### D2：ID 語法

- **選擇**：
  - Requirement 標題：`### Requirement: <REQ-ID> <description>`，`<REQ-ID>` 為 `REQ-` 加一段大寫英數（`[A-Z0-9]+`），其後至少一個空白與非空描述。
  - Scenario 標題：`#### Scenario: <REQ-ID>-S<m> <description>`，`<REQ-ID>` 必須等於所屬 requirement 的完整 local ID，`<m>` 為不帶前導零的正整數。
  - 散文中可用 `REQ-3` 簡稱；跨 artifact 的正式機械引用（後續 change 的 `Contracts:` 等）一律寫 `capability / local-ID`，不在本 change 範圍。
- **理由**：「合法存在」與「新號配置」是兩個問題（見 D3）。語法放寬到英數才能容納既有 `REQ-PB`，又不必建 registry；Scenario 序號沒有歷史包袱，只收數字。
- **已考慮 alternative**：語法只收數字、另設「保留舊名清單」——清單得放在採用者 repo、schema 要多定義一種設定檔，實質是一份小 registry，而全世界只有 `REQ-PB` 一例。

### D3：新 ID 配置分兩層

- **「新」的定義**（由結構導出）：出現在 delta `ADDED` 的 requirement 是新 requirement，其下所有 scenario 都是新 scenario；`RENAMED` 的 FROM 標題沒有 ID 時（補號遷移），TO 的 ID 也是新 ID，照配置規則檢查——否則補號時可以取 `REQ-FOO` 而不被擋；`MODIFIED` requirement 中，ID 不在主 spec 該 requirement 之下的 scenario 是新 scenario。
- **檢查層（check 13 會擋）**：新 requirement 的 ID MUST 為 `REQ-<正整數>`，且大於該 capability **目前主 spec** 所有數字型 requirement ID；新 scenario 的序號 MUST 大於**同一 requirement** 目前主 spec 中已有 scenario 的最大序號（不跨 requirement 合算）。空集合時任何正整數都合法。
- **發號層（寫在 `specs` instruction，MUST 照做）**：取號基準是歷史上用過的最大號——連同 `openspec/changes/archive/` 裡已歸檔 change 的 delta spec 一起看，從那個最大號往上取。只有歷史上從未出現任何號碼，才從 1 開始。
- **未撞到退休號碼**：不在本 change 檢查，留給歸檔身分檢查。
- **理由**：check 13 只看當前狀態、看不到歷史；若強制「等於目前最大值 + 1」，當最大號已退休時，會把退休號碼指定成唯一合法的新號，直接違反「退休不重用」。拆兩層後，check 13 只保證「不倒退、不撞現有身分」，這個宣稱邊界是誠實的。
- **已考慮 alternative**：check 13 強制 `max(current)+1`（使用者先提、後撤回，理由即上述反例）；只寫成建議、不擋（放任 `REQ-FOO` 這類新號出生）。

### D4：「同一契約」由操作角色導出

- **選擇**：同一 capability 內，同一 local ID 不得指向兩個不同的 contract identity；是否為同一契約由 artifact 結構與 OpenSpec 操作角色判定，不由 agent 讀文字判斷：

  | 情形 | 判定 |
  |---|---|
  | 主 spec 的 `REQ-3` ＋ delta `MODIFIED` 的 `REQ-3` | 同一 identity，合法 |
  | `RENAMED` 的 FROM 與 TO | FROM 與 TO 的 local ID 必須相同，不同即 BLOCK；唯一例外是 FROM 沒有 ID（補號遷移），此時 TO 的 ID 是新 ID（D3） |
  | `MODIFIED` 的標題等於同一 delta 檔中某筆 `RENAMED` 的 TO | 經 RENAMED 對應回 FROM 那條主 spec requirement，是同一 identity；補號遷移時主 spec 還沒有 TO 標題，也照此對應。其 scenario 是否為新，對照的是 FROM 那條的 scenario（無 ID 者不計入目前集合） |
  | `ADDED` 的 `REQ-3` ＋ 主 spec 已有 `REQ-3` | 新契約搶既有 identity，BLOCK |
  | 同一檔案內兩個不同 block 都宣告 `REQ-3` | BLOCK |
  | 兩個 `ADDED` block 都宣告 `REQ-3` | BLOCK |

  Scenario 同理，在所屬 requirement 內判定。
- **理由**：延續 9/24 正式設計修訂的精確語意——同一契約出現在多處不是錯，錯的是同一 ID 代表兩件事。以操作角色判定，才能做到判準固定。
- **已考慮 alternative**：「字串出現兩次即重號」（9/24 已修掉的舊語意，會把 MODIFIED 誤判為重號）。

### D5：check 13 的檢查對象是「歸檔前」與「預演歸檔後」兩個狀態

- **選擇**：check 13 同時讀兩個狀態，角色不同：
  - **歸檔前狀態＝判斷基準（context）**：目前的主 spec ＋ 本 change 的 delta spec。用來判定「這是既有 requirement 還是 ADDED」、D3 的「目前最大值」、RENAMED 的 FROM 是誰等 D4 操作角色。**不**拿來要求「所有 requirement 都已有 ID」——歸檔前仍可能是無編號的 v2 格式。
  - **預演歸檔後狀態＝候選狀態（candidate state，真正要驗收的對象）**：把 repo 的 `openspec/` 複製到暫存目錄，實跑 `openspec archive <change> -y`（不得加 `--skip-specs`）得到的主 spec。要回答的問題是「如果現在 archive 這個 change，得到的 spec 是否滿足身分規則」：每條 requirement / scenario 都有合法 ID、沒有同 ID 兩條、scenario 前綴正確。
  - **預演歸檔失敗**（例如 MODIFIED 的標題在主 spec 找不到）→ 候選狀態無法產生 → BLOCK，不跳過。
- **理由**：補號遷移的 change 在 verify 時，主 spec 仍是無 ID 的舊樣子；只看歸檔前狀態會把遷移 change 自己擋下。正式設計 §3.1 已規定需要預演歸檔後狀態時「在暫存複本實跑 `openspec archive`，不重寫 merge 邏輯」，本決策照辦。
- **已考慮 alternative**：只看 delta ＋ 主 spec 中未被觸及的 requirement（等於在 instruction 裡重寫一份 OpenSpec merge 邏輯，§3.1 明文否決）；對遷移 change 開例外（違背「不留兩套身分制度」）。

### D6：check 13 的檢查項與交叉核對

- **選擇**：以下任一成立即 BLOCK：
  1. 預演歸檔後的任一 requirement / scenario 標題沒有合法 ID（D2）。
  2. 同一 local ID 指向不同契約（D4）。
  3. scenario ID 前綴不等於所屬 requirement ID。
  4. RENAMED 的 FROM / TO local ID 不同。
  5. 新 ID 不符檢查層配置規則（D3）。
  6. 交叉核對不一致：
     - **CLI 要對它所判定的那個狀態跑**：候選狀態的主 spec 核對，CLI 必須在 D5 的暫存複本裡、預演歸檔之後執行——在 repo 本身跑會讀到歸檔前的主 spec，比錯對象而且不會報錯；change 層核對則對歸檔前狀態跑（該 change 在 repo 裡尚未歸檔）。
     - 每個預演歸檔後的主 spec：從文字數出的 requirement 數 ＝ `openspec show <spec> --type spec --json` 的 `requirementCount`；第 k 條 requirement 從文字數出的 scenario 數 ＝ JSON `requirements[k].scenarios` 的長度（CLI 不吐標題，故依出現順序配對）。
     - 本 change：每個 delta 檔中各 operation 從文字數出的 requirement 數（ADDED / MODIFIED / REMOVED 數 `### Requirement:` 標題；RENAMED 數 `FROM` / `TO` 組，一組算一筆）＝ `openspec show <change> --json --deltas-only` 中同 spec、同 operation 的筆數；每筆 ADDED / MODIFIED 的第 k 條 requirement，文字數出的 scenario 數 ＝ CLI 同 operation 第 k 筆的 `scenarios` 長度（Requirement 與 Scenario 兩層都核對，不只 requirement）；RENAMED 的 FROM / TO 以 CLI 的 `rename.from` / `rename.to` 為準再比一次 ID。
     - 語意是兩種方法互相抓錯，不預設哪邊對。
     - **依賴假設（openspec 1.3.1）**：CLI JSON 不提供 scenario identity，scenario 數只能依 requirement 出現順序配對。若無法可靠配對（例如 requirement 數本身就不一致），判為交叉核對無法完成 → BLOCK，不猜測配對。
  - BLOCK 分兩種原因，紀錄時必須分開寫，不可混稱「ID 驗證失敗」：
     - **違規**：檢查完成，發現第 1–5 項任一成立；或第 6 項的比對已可靠配對、完成，結果數量不一致 → identity integrity 不成立。查完了，發現不符合。
     - **無法判定**：檢查本身無法可靠完成（CLI 沒提供所需資料、輸出結構變了無法對應、順序無法可靠配對、預演歸檔失敗 D5）→ 查不完，所以不能證明符合， identity integrity 無法判定，fail-closed BLOCK。沒有形成判定不等於違規，但沒有 PASS 就不能放行。
  - 兩種都沒有**降級放行**的出口：身分完整性是正式設計 §2.1 的 Core Integrity Invariant I1，「任何 change 都不可關閉、不進 override 模型」；只有 §2.2 列為 degradable 的 assurance 才能降級。
  - check 13 與 checks 8–12 同一層級：判準固定、可機械判定，執行者是 verify agent。
- **Claim boundary 的分工**（D10）：完整的保證／不保證由 `contract-identity` spec 定義；本 design 只說明為什麼停在 agent 執行的規則。
- **理由**：OpenSpec 不做任何 ID 檢查（實測），這是 bridge 必須自己補的完整性規則。可執行的 Gate 排在後面那一塊，此時提前做會把本 change 擴成半套 traceability system；因此本版宣稱只到「判準固定」，不到「不可繞過」。
- **已考慮 alternative**：本版就寫可執行腳本（仿 PoC `gate_check.py`）——會讓 repo 首次出現需維護的程式碼，並把本 change 長成半套 traceability system。

### D7：本 repo 既有 spec 在本 change 一次補號

- **選擇**：`plan-contract`、`tdd-claim-accuracy`、`tdd-evidence-contract` 的 10 條 requirement 以 RENAMED 補上 `REQ-<n>`（依文件內順序從 1 起，因這三個 capability 歷史上從未發過號），同一 change 以新標題 MODIFIED 全文、scenario 補 `REQ-<n>-S<m>`，內容一字不改。`repo-guidance` 的 `REQ-PB` 維持原名，以 MODIFIED 全文把兩個 scenario 補為 `REQ-PB-S1`、`REQ-PB-S2`。
- **理由**：成本已實測可控；Identity 在解決「東西是誰」，第一版就留兩套身分制度違背目的。
- **已考慮 alternative**：只檢查本 change 有動到的 capability（留下有 ID / 無 ID 並存與一條永久例外）。

### D8：新 capability `contract-identity` 承載規則

- **選擇**：D2–D6 的規範性內容寫成新 capability `contract-identity` 的 spec；schema 的 `specs` instruction、`verify` check 13 與 `templates/spec.md`、`templates/verify.md` 是它的作者表面與執行表面。本 change 自己的 spec 也照 D2 / D3 寫 ID（新 capability 從 `REQ-1` 起）。
- **理由**：身分規則是一項獨立的契約能力，不屬於現有四個 capability 中任何一個。

### D9：證據命名與 TDD applicability

- **選擇**：
  - 以 mutation fixtures 驗 check 13：缺號、D4 表每一種重號、前綴不符、RENAMED 換 ID、新號違規（非數字、不大於目前最大值）、交叉核對不一致（例如破損標題行），以及一組全部正確的 happy path，另含一個「補號遷移 change」的正向範例（驗 D5 不會把遷移擋下）。落點比照 `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/` 的形狀。
  - fixtures 同時是 **conformance / acceptance evidence**：每個 fixture 有預期判定（BLOCK 並註明違規或無法判定，或通過），verify agent 依規則判出的結果須與預期一致。它們證明的是「第 13 條文字規則具有足夠的可執行明確度，agent 依規則能對已知反例做出預期判定」；**不證明** Harness 已自動強制這些 identity invariants。此宣稱範圍由 `contract-identity` spec 定義（D10）。
  - **TDD applicability 採行為判準**（2026-09-07 使用者對 fix-v2 的裁定：「applicability does not turn on whether a conventional test framework runs the case; it turns on whether the same re-runnable case shows the old behaviour violating the contract before the edit and the corrected verdict after it」）。新增 check 13 規則文字的 task 標 `TDD: applicable`。
    - **受測對象**：只有「舊 verify（checks 1–12）的判定與新契約不一致」的 fixture 才是 TDD subject，寫法沿用 fix-v2：`<fixture 目錄>::<預期判定>`。舊判定已與新契約一致的 fixture（例如預期通過的正向範例，或已被 check 1 的 `openspec validate` 擋下者）行為沒有改變、形成不了 RED，只作 conformance evidence，不硬湊 RED。
    - **RED**：在修改 `schema.yaml` 之前，實際以現行 verify 規則跑該 fixture，記下錯誤判定（預期例如缺 ID 的 fixture 被放行）。「舊版應該會通過」這種事後推論不是 RED。**「舊 verify 會放行」目前是推論，由 RED task 實跑確認**；實跑若顯示舊判定已與新契約一致，該 fixture 即不列為 subject。
    - **GREEN**：加入 check 13 後，以同一 fixture、同一執行方式重跑，得到新契約要求的判定。唯一改變的變數是第 13 條規則。
    - **證據份量**：這種 RED 證明現行系統存在一個可重現的契約缺口，不是 `INDETERMINATE`（「規則還沒寫所以判不出來」）那種空洞證據。但 TDD evidence 成立不提高 assurance：執行判定的仍是 agent，不是不可繞過的 executable Gate。
    - 若某 task 實際新增可執行程式，照樣逐 task 判定。
- **理由**：同一個可重跑的 fixture，在修改前後顯示 verify 從錯誤判定變為正確判定——這正是 9/07 裁定所定義的可 TDD 的行為改變。`schema.yaml` 雖是文字，但它改變的是 verify agent 面對固定案例時可觀察的判定行為，不是在測文字寫得好不好。
- **已考慮 alternative**：
  - `TDD: n/a — schema instruction / prose rule，不屬於正式設計 §4.3 所定義的 executable-behavior code task`（Q11 曾採，後推翻：寫 tasks 前查到 9/07 的既有裁定，並更正了「加規則前的 RED 只會是 `INDETERMINATE`」的錯誤推論——舊 verify 對缺 ID fixture 預期是明確放行，是真實的錯誤判定）。
  - `TDD: applicable`、RED 記 `INDETERMINATE`（Q10 曾採）：RED 的內容錯了，舊 verify 不是判不出來，而是會放行。
  - 原 Q8 理由「無 executable checker 故做不出有意義的 RED→GREEN」（Codex r1 🔴 指出與 `INDETERMINATE` 條款衝突）。
  - 修改 `tdd-evidence-contract` 或正式設計 §4.3（超出本 change 範圍；兩者與 9/07 裁定之間的落差另立研究題，見 Open Questions）。

### D10：宣稱邊界單一 owner，其餘 artifact 摘要或引用

- **選擇**：`contract-identity` spec 是宣稱邊界的 normative owner，完整定義本版能保證什麼、不能保證什麼。proposal 的 Assurance Boundary 只做摘要並指向 spec；design 只說明理由；README 寫到時同樣摘要並連結 spec。審查檢查三者**語意**是否一致，不要求逐字一致。
- **理由**：正式設計 §1 上位原則「結構化副本仍是副本」。各 artifact 承擔不同語意角色（contract / scope 摘要 / rationale）時提到同一件事不算重複真相；三處都寫成完整規範、再要求永遠逐字一樣，才是製造同步負擔。
- **已考慮 alternative**：四處逐字抄同一句、審查逐字比對（本 change 先提後撤回：短期防錯字，長期是主動製造四份同步副本）。
- **Retrospective 觀察**（proposal 新增 Out of Scope / Assurance Boundary 兩段的 dogfood，樣本 n=1）：①tasks、審查、verify 有沒有真的用到這兩段；②這幾個 artifact 能不能形成清楚的 owner / 摘要 / 理由分工，而不是靠逐字同步維持一致。結果正面才另開 change 考慮改 `templates/proposal.md`（含 Modified Capabilities 說明改為「行為或身分變更」）。

## Risks / Trade-offs

- [Risk] check 13 由 agent 依文字執行，agent 可能漏做或判錯 → Mitigation：規則逐條寫成固定判準；mutation fixtures 驗規則明確度；對外只宣稱「判準固定」，不宣稱「不可繞過」；executable Gate 留待後續 change。
- [Risk] 預演歸檔（D5）依賴 `openspec archive` 在暫存複本上的行為；CLI 若變更 archive 語意，預演結果會跟著變 → Mitigation：`version-check.yml` 每週用最新版 OpenSpec 驗 schema；預演只借用 CLI 的 merge，不自己重寫，CLI 行為變了反而會先在這裡被看見。
- [Risk] 交叉核對的 scenario 數量按順序配對（CLI 不吐標題），若 CLI 改變輸出順序會誤報 → Mitigation：誤報方向是 BLOCK（fail-closed），不會放過錯誤；實測目前順序與文件一致。
- [Risk] 發號層的「查歷史最大號」由寫 spec 的 agent 執行、check 13 不驗 → Mitigation：這正是 D3 刻意留給歸檔身分檢查的缺口，在 spec 的宣稱邊界與 README 明寫；已知未撞退休號的保證**尚不存在**。
- [Risk] MODIFIED 全文替換時刪掉 scenario，本 change 抓不到 → Mitigation：列為 Non-Goal，歸檔身分檢查那一塊處理。
- [Trade-off] ID 語法放寬到英數，檢查層只能靠「新 ID 必須是數字」擋掉新的非數字 ID；既有非數字 ID 只剩 `REQ-PB` 一例 → 接受理由：不建 registry（正式設計 §3.1）。
- [Trade-off] 升 v3 讓所有採用者都要遷移 → 接受理由：不跳版會違背 README 自己對 breaking 的定義；遷移步驟已在本 repo 實測可一次完成。

## Migration Plan

- **本 repo**：本 change 內完成 D7 的補號；archive 後主 spec 全部帶 ID。同步 `superpowers-bridge/` 到 `openspec/schemas/`（repo CLAUDE.md 規定的複製步驟）後，後續 change 即受 check 13 約束。
- **採用者（寫進 bridge README 的 v2 → v3 遷移指南）**：
  1. 升級 bundle 到 `3.0.0`。
  2. 開**一個**補號 change，涵蓋所有 capability：每條 requirement 用 RENAMED 補 `REQ-<n>`（已有 stable ID 者保留原 ID），並以新標題 MODIFIED 全文、scenario 補 `<REQ-ID>-S<m>`；內容不改。**不可按 capability 分批**：check 13 判定預演歸檔後的**全部**主 spec（D5、Q2 不留 legacy 例外），只補一部分的 change 會被其餘未補號的 capability 擋下。
  3. 跑 verify（含 check 13）後 archive。
  4. 進行中、尚未 archive 的 v2 change：delta spec 依 D2 / D3 補 ID 後才能通過 verify。
- **Rollback**：釘回 bundle `2.x.y`；schema major v2 維持為已發布版本，不撤回。已補的 ID 對 v2 無害（v2 不檢查 ID、帶 ID 的標題在 CLI 下照常運作）。

## Open Questions

- ~~`MAX_DELTAS_PER_CHANGE` 的計數對象~~ 已查明（2026-09-29，讀 openspec 1.3.1 `dist/` 原始碼，Fable 代審提出、主 session 覆核）：上限套在 `ChangeSchema`（`core/schemas/change.schema.js`），計數對象**就是** spec delta 筆數（`core/parsers/change-parser.js` 在 `specs/` 存在時以 delta spec 條目為準）。但它只經 `validateChange` 生效：`openspec validate` 走 `validateChangeDeltaSpecs`（`commands/validate.js`），碰不到此上限；`openspec archive` 雖呼叫 `validateChange`（`core/archive.js`），程式註明「Proposal validation is informative only (do not block archive)」，只印警告、不擋歸檔。⇒ 大型 repo 的單一補號 change 不會因此上限被 validate 或 archive 擋下；本 change 預演歸檔含 29 筆 delta 亦成功。此項不再是 open question。
- 有沒有外部採用者釘在 v2，未查。
- **（本 change 範圍外，另立研究題）** TDD applicability 目前有兩種判準並存：正式設計 §4.3 的字面近似「看 task 是不是 executable-behavior code」（artifact 類型判準）；2026-09-07 對 fix-v2 的使用者裁定是「看同一個可重跑的案例，修改前後有沒有顯示行為改變」（可觀察行為判準）。另有 `tdd-evidence-contract` 的 `INDETERMINATE` 條款，回答的是「若做，RED 可以長什麼樣」。本 change 因此在 n/a 與 applicable 之間來回三次（Q8 → Q10 → Q11 → Q14），最後採行為判準，但不以此解決兩種判準的落差。研究題：**TDD applicability 應由 artifact 類型決定，還是由可觀察行為／可重跑案例決定？** 以及驗證方法是否應依受測對象路由（程式行為 → TDD；schema 與可機械規則 → conformance 與 mutation cases；Skill 與文字規則 → behavioral eval；跨文件契約 → consistency / traceability check；migration → before/after 對帳）。
