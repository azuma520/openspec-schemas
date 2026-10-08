## Context

**缺口**：Superpowers v6.0.0 起，`subagent-driven-development`（SDD）用 `scripts/task-brief` 從 plan 抽出單一任務的簡報。它只認 `Task <數字>` 形式的標題；bridge Plan Contract 規定的條目標題 `## 1.1 — <標題>` 交給它會 exit 3（bridge README Compatibility § S11；最早 2026-09-03 loosen-plan dogfood 撞到，2026-10-02 retro-skill-inventory apply 再撞，以等效抽取繞過）。決策紀錄與實測見 `docs/superpowers/poc/2026-10-07-task-brief-heading-compat/report.md`（以下稱 poc 報告）；本檔的決策來源是 `brainstorm.md`。

**現況**：條目標題的寫法同時出現在下列表面，都只認「標題以編號開頭」：

| 表面 | 位置（語意錨點） |
|---|---|
| Plan Contract | `schema.yaml` `plan` instruction，STRUCTURE 第 2 點「Write each entry as a `##` heading whose text BEGINS with that task number」起，到「…is not an entry (this plan's own header, a self-review section)」 |
| check 12 | `schema.yaml` `verify` instruction 第 12 項「tasks.md task numbers and plan.md entry keys correspond 1:1」的 ENTRY KEY 收集段 |
| 作者模板 | `templates/plan.md` 的 HTML 註解（「entry key 必須放在每個 `##` heading 最前面」）與三個範例標題 `## 1.1 —`、`## 1.2 —`、`## 2.1 —` |
| 文件 | bridge README（en + zh-TW）Compatibility § S11 與其下「Why the baseline stays at」「Follow-up status」兩段 |

**上游 `task-brief` 的行為**（本機 6.4.1，原文見 brainstorm §一）：以 `^#+[ \t]+Task[ \t]+[0-9]+` 判定任務邊界，範圍只在下一個 Task 標題結束；選取條件把編號直接拼進 regex；只把行首 ``` 當程式碼區塊切換。

**約束**：

- 不改上游、不發上游 PR、不做轉接層（poc 報告結論，已定案）。
- v3 的 Plan Contract 明文說「不以數字開頭的 `##` 不是條目」，所以 `## Task 3 備註` 在 v3 合法；任何認 `Task` 前綴的寫法都會重新解讀這類標題 → schema major 3 → 4（poc 報告「版本號」節，已定案）。
- check 12 與 Plan Contract 都是給 agent 讀的說明文字，沒有 parser 程式；CI 只驗結構，改壞 prompt 文字 CI 照樣綠（repo `CLAUDE.md`「沒有 build / test / lint」節）。
- 使用者確認目前沒有外部採用者（brainstorm 第三段）。

## Goals / Non-Goals

**Goals:**

- 依 bridge 寫法寫成的 plan，交給上游 SDD 的 `task-brief` 時抽得到每個條目（**辨識得到**；抽取範圍的已知限制見 D3）。
- 舊寫法 `## <編號> —` 的 plan 一般不需遷移就繼續通過 check 12。
- check 12 的判定對 `Task` 寫法、程式碼區塊有明確且與上游一致的規則。
- 版本號、文件、CI 一致反映 schema major 4。

**Non-Goals:**

- 不修上游 selector 的抽取範圍問題（編號碰撞、整數多抓、最後項吞尾段、不認 legacy 邊界、把 Task-like 非條目當邊界）；只寫 guidance。
- 不加近似格式提示（`## task 1.1`、`### Task 1.1` 等）——屬既有工作「作者表面與 Gate 規則對齊」。
- 不改 check 13；不改 tasks.md 側的程式碼區塊語意。
- 不改 Compatibility 的 Superpowers 基準值（6.x 重新定錨由 `task-20261007-superpowers-6x-rebaseline` 負責）。
- 不補打 `v3.0.0` tag；不修 v1→v2、v2→v3 遷移說明的 rollback 寫法（記為觀察）。
- 不改 adopters fragment（查證無標題格式內容）。

## Decisions

### D1：舊寫法無期限保留，`Task` 寫法是唯一 canonical（brainstorm Q1 A′）

- **選擇**：三層分開陳述——canonical：`## Task <編號> …`；legacy accepted：`## <編號> …`；上游 `task-brief` 可辨識：只有 canonical。不承諾在哪個 major 移除舊寫法。將來重議的判準（不是任何人在守的機制）：雙語法明顯增加 checker／tooling 複雜度、造成實際誤用、新能力只能建立在 Task 寫法上、維護兩種格式開始產生持續成本。
- **理由**：check 12 的職責是 Plan Contract 1:1 對應，不替某個上游 helper 執法。把「Bridge 認為合法」與「上游某工具處理得了」綁在一起，等於讓上游 parser 的寬窄決定 Bridge 的合法性。
- **已考慮 alternative**：B 下一個 major 移除舊寫法——沒有實際成本驅動，預先承諾只會製造一次注定的破壞；C 這版就只認 Task——把所有既有 plan 一次變不合法，且混淆兩種職責。

### D2：條目由正面規則定義，`Task` 前綴取上游可辨識語言的安全子集（brainstorm Q3 A）

- **選擇**：一行 `##` 標題是條目，當且僅當同時符合：
  1. 不在 D4 定義的程式碼區塊內；
  2. 行首剛好 `##` 接空白（`###` 以下仍是條目內的子標題）；
  3. 其後文字是 canonical：`Task`（大小寫精確）+ 一個以上 space/tab + 編號，或 legacy：編號；編號為 `\d+(\.\d+)*`，其後必須是空白或行尾。

  其他 `##` 一律是非條目段落。鍵值是**編號**，`Task` 只用來辨認、不進鍵值，所以 `## Task 1.1` 與 `## 1.1` 的鍵值相同。
- **理由**：凡 Bridge 合法的 `Task` 條目，上游都辨識得到（子集方向對）；Bridge 既有的編號文法不變；不反向照抄上游較寬的 parser。Plan Contract 現有理由「key must LEAD so the keys are readable without interpretation」改寫為「編號要擺在最前面，或只接在固定字 `Task` 後面，讓鍵值不需語意解讀即可辨識」，否則規則與理由自相矛盾。
- **相容性（第三項 breaking，2026-10-08 使用者裁定 A）**：v3 check 12 條文說鍵值「從 `##` 之後第一個非空白字元開始」，沒要求 `##` 後有空白、也沒限定 `##` 在行首，照字面讀會收 `##1.1` 與縮排的 ` ## 1.1`。第 2 點的「行首剛好 `##` 接空白」對兩種寫法一體適用，所以 v4 不再收這兩種，列為行為變更。不替 legacy 寫法保留 v3 的寬鬆讀法：那會讓 canonical 用結構規則、legacy 用歷史掃描規則，同一份 plan 兩套辨識。本 repo 以兩條路徑（git 追蹤清單逐檔 grep、rg 全庫）掃全部 45 個 `plan.md`，兩種寫法皆 0 筆——只支持「本 repo 遷移風險為零」，不推及外部。（此掃描早於本 change 加入的變異 fixtures；apply 後 f18、f19 刻意含這兩種寫法，「0 筆」指 fixtures 以外。）
- **已考慮 alternative**：B `task` 不分大小寫——會重現本 change 要消滅的缺口（Bridge PASS、上游找不到）；C 強制完整 `## Task <編號> — 標題`——把「建議怎麼寫」與「最低合法語法」混在一起；把「非條目」維持為反面表述（「不以數字開頭」）——加了 Task 後反面表述講不清楚哪些是條目。

### D3：「安全子集」只保證辨識，不保證抽取範圍正確

- **選擇**：文件只宣稱 **recognition**。已知會抽錯範圍的五種情況寫進 guidance 的理由，不寫成檢查：
  - 編號碰撞：要 `1.1` 會連 `## Task 101` 一起抽（regex 的 `.` 配任意字元；審查時以 6.4.1 實測）。
  - 整數編號：要 `1` 會抽到所有 `1.x`。
  - 最後一項：其後的非條目段落一起被抽入。
  - canonical 後接 legacy：上游不把 `## 1.2` 當邊界，`## Task 1.1` 的範圍延伸過整個 1.2。
  - Task-like 非條目：`## Task 1.1a 備註` 在 Bridge 是非條目、在上游卻是邊界，會截斷前一項，要 `1.1` 時又被一併抽入。
- **三句 guidance**（全部不進 validation）：
  1. plan 要交給上游 SDD `task-brief` 時，整份條目統一用 `## Task <編號> …`；混用在 Plan Contract 仍合法。
  2. 非條目 H2 不以 `Task <數字>` 開頭。
  3. 非條目段落（如 self-review）放在第一個條目之前。

  另一句建議：新寫或修改的 plan 使用 `Task` 寫法，因為它是 Bridge 定義、且上游可辨識的 canonical form。**不可寫「上游只認這種」**——上游接受的形式其實更寬。
- **理由**：Bridge 不因上游 parser 的缺陷收緊原本合法的 Plan Contract；但要走上游 SDD 的人要知道哪種寫法安全。這也是驗證必須比對抽出內容、不能看 exit code 的原因（D7）。
- **已考慮 alternative**：把這些情況寫成 check 12 的 BLOCK——等於替上游 selector 的缺陷執法，與 D1 衝突。

### D4：check 12 跳過行首未縮排的 ``` 區塊，不認 `~~~` 與縮排 fence（brainstorm Q3a）

- **選擇**：Plan Contract 以語意陳述：「在 Plan 結構辨識時，位於行首未縮排的 backtick fenced code block 內之 heading-like text 不構成 entry。」開關判定的細節放在 check 12：逐行掃，行首三個字元為 ``` 的行切換區塊狀態，該行與區塊內各行都不收。
- **理由**：上位理由是 Markdown 結構語意——程式碼裡寫著 `## Task 1.1 —` 不應改變 plan 的任務結構。上游行為剛好給了 interoperability 的理由：只認行首 ```，取兩邊能力的交集；若 Bridge 忽略 `~~~` 內的 `## Task 1.1` 而上游拿它切任務，等於修完一個 parser 差異又主動留下另一個。Plan Contract 是機器可讀契約，可以比 Markdown 更窄、更可預測，不擴成 CommonMark parser。
- **已考慮 alternative**：連 `~~~` 一起認（AI 原建議）——與上游行為不一致，使用者選了更窄的版本；不處理程式碼區塊——``` 內的 `## Task 1.1 —` 會被 check 12 收成條目、上游卻看不到，違反 D2 的子集方向。
- **相容性**：**不宣稱 backward-compatible**。v3 條文照字面讀（「每個 `##` 標題」）會收區塊內的標題，可能有舊 plan 靠此通過或被擋；v4 改為跳過，列為行為變更。本 repo 所有 `plan.md` 的區塊內查過沒有 `##` 開頭的行——只支持「本 repo 遷移風險為零」，不推及外部。（此查核早於本 change 加入的變異 fixtures；apply 後 f14、f23 刻意在區塊內放 `##` 標題，「沒有」指 fixtures 以外。）

### D5：check 12 只改「plan 裡哪些行可以產生鍵值」

- **選擇**：
  - 第一階段（重複）、第二階段（集合比對）、不提前結束、訊息格式全部不改。
  - 新舊混用合法；`## Task 1.1` 與 `## 1.1` 並存＝鍵值 `1.1` 重複，第一階段擋下。寫法不是身分的一部分。
  - 區塊沒關 → 其後條目都收不到 → 第二階段報缺鍵擋下；上游同樣抽不到，兩邊一致。這是診斷訊息好不好懂的問題，不是對錯問題，不另設「區塊沒關」錯誤。
  - 不加近似格式提示：為了更友善的錯誤訊息而建立第二套「近似 parser」（`task`？`TASK`？`### Task`？`## Tasks 1.1`？），會讓「什麼算條目」出現兩個來源。
  - **check 12 與 check 13 的區塊處理不對稱，兩處都寫理由**：check 12 跳過區塊，因為它判斷 plan 的條目結構，而在區塊處理上（只認行首 ```）與上游 task-brief 的抽取取交集（見 D4）——這個一致只限區塊處理，條目怎麼辨識、範圍怎麼切等其他部分不以 SDD 的任務抽取為準（見 D3）；check 13 不跳過，因為它要與 CLI 的表面計數比對（check 13 原文刻意不認 Markdown 結構）。此差異是刻意設計，不應被「好心統一」。check 13 的判定不改，只加一句不對稱理由。
  - tasks.md 側不改：明寫「本次只改 plan 側的條目辨識；tasks 側的解析維持現況，其程式碼區塊語意不在本次範圍」。
- **理由**：縮小改動面；check 12 的兩階段設計有自己的審查歷史（fix-v2），沒有理由連動。
- **已考慮 alternative**：統一 check 12 與 check 13 的區塊語意——兩者比對的對象不同，統一會讓其中一個比錯東西。

### D6：schema major 3 → 4，基準值不改，rollback 指向 commit SHA

- **選擇**：
  - `schema.yaml` `version: 4`；`VERSION` `4.0.0`。
  - Compatibility 表最上方新增 `v4` 列、`v3` 列保留。v4 列的 Superpowers 欄仍填 `` `v5.1.0` ``（`version-check.yml` 以 awk 讀第 4 個反引號欄位，該格必須是反引號版本號）；說明寫在**表格下方**、不寫進格子（格子多一個反引號會位移 awk 的欄位）。說明內容：沿用的歷史宣告，v2 起沒在 5.1.0 重跑，目前無採用者、不再投資重新驗證，**不構成相容保證**；已知的本次 PoC 實測環境為 Superpowers 6.4.1；dogfood 的驗證版本以實際載入的版本為準並留紀錄，完成前不得寫「已完整驗證」。
  - v4 列的「Baseline as of」填 `pending`（純文字、不加反引號；CI 只讀第 2、4 個反引號欄位，不讀日期欄）。README 定義此日期為「維護者對**該列所列版本**重跑完整流程、確認沒退化」的日期；v4 列列的是 `v5.1.0`，而 C′ dogfood 跑在實際載入的 6.x 上——所以 **C′ dogfood 成功不構成填日期的依據**，C′ 只覆蓋 S11 這一項整合，S4、S5、S12、S14 仍未對齊。日期要等 `task-20261007-superpowers-6x-rebaseline` 把該列改成實際驗證版本並跑完整流程後才填。（2026-10-07 使用者裁定；不採「填落地日、表下註明只做 CLI 層確認」——欄位定義是完整流程，填日期再用說明打折，等於機器表面與語意分裂。v2、v3 列既有的 CLI 層日期不在本 change 改。）
  - rollback 指向**第一個把 `schema.yaml` 改成 `version: 4` 的 commit 的 parent**，以完整 SHA 寫入，不引用不存在的 `3.x.y` tag。定稿時填入並實際 checkout 一次確認；歷史若被改寫要重填（本 repo 直推 fork main、不 squash，風險低，但要寫明）。
- **理由**：Compatibility 表以 schema major 為列鍵，10/02 OpenSpec 1.3.1 → 1.14.0 是直接改 v3 列、未升 major——之後轉到 6.x 改 v4 列即可，不需要再破壞一次相容。v4 列若直接填 6.4.x，等於重新宣稱 S4、S5、S12、S14 已成立，而它們未修或未查。repo 沒有任何 tag，舊兩份遷移說明的「pin bundle」照做會失敗，不能再寫第三份。
- **release tag（2026-10-07 使用者裁定）**：
  - **這是落實既有規則，不是新政策**：repo `CLAUDE.md`「兩個版本號別搞混」表早已寫「bundle release = `VERSION` + git tag（`v3.x.y`，發版時打）」，README 也寫「git tag `v3.0.0` created at release」；但 repo 至今沒有任何 tag（2026-10-07 本機 `git tag -l` 與遠端 `git ls-remote --tags origin` 皆為空），規則最晚在第一次宣告 bundle 1.0.0 時就已存在（2026-05-14 commit `f7624d6` 在 bridge README 寫入「`1.0.0` (tagged `v1.0.0`)」；`VERSION` 檔 2026-05-18 才開始追蹤），之後的 1.0.0、1.0.1、2.0.0、3.0.0 四個 bundle release（跨 schema major v1–v3）都沒有對應 tag——規則寫著卻沒被執行（2026-10-08 以 `git log` 查證；原作者 repo 的遠端 tag 也為空），缺的是執行時點與掛點，不是條文。
  - **release commit 的定義**：C′ 完成 archive、最終驗證與所有 release 連動文件更新後，準備發布到 `main` 的最終 commit。不等同 archive commit——archive 之後仍可能有 review 修正或收尾 commit；要標記的是最後完整代表 4.0.0 發布內容的 tree。
  - **release 動作**：最終 commit 就緒 → 建立 annotated tag `v4.0.0` 指向它（repo 無既有 tag 慣例；annotated 帶建立者、日期與訊息，較適合當 release 標記）→ push `main` 與 tag → 以 `git ls-remote --exit-code --tags origin 'refs/tags/v4.0.0^{}'` 取得遠端 tag **剝開後**指向的 commit，與事先記下的 release commit SHA 比對一致（annotated tag 不加 `^{}` 查到的是 tag 物件本身的 SHA，與 commit SHA 必不相等；2026-10-07 以臨時 repo 實測） → 才算完成。push tag 屬受管制的 git 操作，執行當下須取得使用者對該次 push 的明確授權。
  - **掛點**：C′ 在工作地圖上的那筆（`task-20261002-task-brief-heading-compat`）的完成條件為「遠端 tag 已確認」，未確認前維持 DOING——`/work-status` 每次開工都會顯示、交接接力棒會帶著。不放進 tasks.md：該 tag 在 archive 之後才建立，verify（check 2）與 retrospective 都在 archive 之前，放進去只會以未勾選狀態被歸檔、retrospective 也確認不到。
  - **README 陳述改成規則式**：「Current bundle release」那句不再寫「tag 已建立」這類事件，改為「每個 bundle release 以同版本 Git tag `vX.Y.Z` 標記；此 release discipline 自 bundle 4.0.0 起實際執行。」——寫在被標記的 commit 裡的句子不可能描述標記之後才發生的事，規則式在開發中與發版後都成立。現存「`v3.0.0` tag created at release」是錯誤陳述，本次改這段時一併修正，不複製成新的假陳述（en + zh-TW）。
  - `v3.0.0` 不補打（哪個 commit 才是 v3.0.0 需要證據，不反推）；v3 → v4 rollback 照上面用 SHA。
  - 每週檢查加「`VERSION` 沒有對應 tag」提醒（乙案）：另登記為延後工作，v4.0.0 發布後再評估，不在 C′ 實作。
- **已考慮 alternative**：v4 列直接填 6.4.2——沒有完整驗證就宣稱相容；在 v4 列格子寫「未驗證」——打爆 CI 的 awk 欄位；rollback 寫「pin bundle `3.x.y`」——tag 不存在。

### D7：驗證＝agent 執行的變異測試＋自己吃自己的完整 SDD 流程（brainstorm Q2 A、第四段 A）

- **選擇**：
  1. **變異測試**：fixtures 放在 `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/`，編號接續。RED 定義沿用 `fix-v2-blocking-defects`：照改前原文判定是錯的。

     | 測試資料 | 內容 | v3 判定 | v4 預期 | 性質 |
     |---|---|---|---|---|
     | 程式碼區塊排除 | `## 1.1`、``` 內 `## 9.9`、`## 1.2`；tasks `{1.1, 1.2}` | BLOCK（多 `9.9`） | PASS | RED→GREEN |
     | 新寫法辨認 | `## Task 1.1`、`## Task 1.2`；tasks `{1.1, 1.2}` | BLOCK（收不到鍵） | PASS | RED→GREEN |
     | 新舊同鍵值 | `## Task 1.1` 與 `## 1.1` 並存；tasks `{1.1}` | PASS（錯） | BLOCK：`1.1` occurs more than once in plan.md | RED→GREEN |
     | 舊非條目被重新解讀 | tasks `{1.1}`；plan `## 1.1` + `## Task 3 備註` | PASS | BLOCK（多 `3`） | 非 TDD，把破壞相容具體化 |
     | 非行首 H2 不再是條目 | tasks `{1.1}`；plan `##1.1`（或縮排的 ` ## 1.1`） | PASS | BLOCK（缺 `1.1`） | 非 TDD，把破壞相容具體化；不併入下一列——下一列的 v3 判定是 BLOCK，併入會讓這兩種的 v3 行為看不見 |
     | 寫錯格式不算條目 | `## task 1.1`、`### Task 1.1`、`## Task 1.1a`；tasks `{1.1}` | BLOCK | BLOCK（缺 `1.1`） | 回歸測試；v3 已判對，不是 RED、不冒充 TDD 證據 |
     | 綜合 | Task 寫法 + ``` 內 `## Task 9.9` | — | PASS，鍵值只有 `1.1, 1.2` | 只要求 v4 判定正確 |

     一份資料只測一個缺陷：若用一份「Task 寫法＋區塊」，v3 的失敗原因是「不認 Task」而非「沒排除區塊」，RED 紅的原因不對。
  2. **oracle**＝凍結的 fixtures＋預先寫死的預期結果。`docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md`（在 `fixtures/` 的上一層）已有「應得判定」欄（f1–f13），新 fixture 的預期也記在那裡；所以測試 Agent **不可拿到 README，也不可拿到整個 fixtures 目錄**，只拿到單一 fixture 的 plan／tasks 檔（複製到 README 不在其中的位置再交付，具體做法由 plan 決定）；被測的是執行 check 12 的 Agent。Agent 要回報中間值（plan 收到的鍵、tasks 收到的鍵、重複、集合差），且**事先看不到預期答案**——先產生判定，再由另一層與凍結的預期比對。腳本只做機械輔助（驗 fixture 未被改、記 hash、批次餵入、比對 actual 與 expected），**不實作 check 12**。證據名稱照實寫：instruction 層的行為證據，不是程式自動測試。
  3. **完整 SDD 流程**：本 change 的 `plan.md` 一開始就用 `## Task` 寫法、至少兩個條目；apply 時照 SDD 原文跑**實際載入的那版**上游 `task-brief`，記下版本與路徑。至少一個非最後一項，抽出的簡報與 plan 中該條目原文**逐行相同**——`rc=0` 不算證據（上游抽錯也是 0）。最後一項若吞入其後的非條目段落，記為上游已知限制。執行與審查子代理拿同一份簡報做事，留紀錄。`sdd-workspace` 的目錄命名由計畫檔名決定、與標題寫法無關：留執行紀錄，但不宣稱為本次驗證到的性質。
  4. **同步後跑 verify**：schema 改完、同步 `openspec/schemas/` 副本後，以新版 check 12 驗本 change 自己的 plan（只有這時拿得到新版判定）。
  5. **結構驗證**：`openspec schema validate`、`openspec schemas`、CI；模板三個標題以 grep 確認已改。**必驗**：`version-check.yml` 改抓 `v4` 後，`Read pinned versions` step 讀得到 v4 列、且讀出正確的 OpenSpec 與 Superpowers 版本號。
  6. **沿用 poc、不重跑**：整數多抓、最後項吞尾段照 poc 報告引用；`101` 撞 `1.1` 已在 brainstorm 審查時實測。
- **理由**：要驗的是「Agent 讀到 check 12 原文後會不會照規則得到正確結論」。另寫 parser 腳本全綠，只證明腳本實作了我們對 check 12 的理解，可能出現「腳本全綠、Agent 解讀錯」——驗錯對象。完整流程定位是 integration acceptance test，parser 邊角已由 poc 覆蓋，不另造第二份完整測試計畫。
- **已考慮 alternative**：寫 parser 腳本當 oracle（brainstorm 第四段 B）；另造測試計畫跑 SDD（Q2 B／C）。

### D8：連動檔案清單

| 檔案 | 改什麼 |
|---|---|
| `superpowers-bridge/schema.yaml` | `version: 4`；Plan Contract 條目定義、理由、程式碼區塊語意句、guidance；check 12 ENTRY KEY 收集段與「Headings that do not begin with a number」改正面表述、區塊開關、與 check 13 不對稱的理由、tasks 側不在範圍 |
| `superpowers-bridge/VERSION` | `4.0.0` |
| `superpowers-bridge/templates/plan.md` | 三個範例標題改 `## Task 1.1 —`、`## Task 1.2 —`、`## Task 2.1 —`；HTML 註解改為接受固定 `Task` 前綴、前綴不屬於鍵值 |
| bridge README（en + zh-TW） | 開頭 `Schema version`；「Crossing a schema major does need migration」段補 v3 → v4；Versioning 表與「A bundle release `3.x.y`…」句；新增「Why v3 → v4 is a schema-major bump」「Migrating v3 → v4」；**Known breaking changes 新增 v3 → v4 條**（含 rollback SHA）；版本歷史；Compatibility 新增 v4 列與表下說明；S11 列與「Why the baseline stays」「Follow-up status」兩段；「Current bundle release」句改為 D6 的規則式並修掉 `v3.0.0` tag 的錯誤陳述；徽章若隨之變動一併處理 |
| `.github/workflows/version-check.yml` | `grep -E '^\| v3 \|'` → `v4` |
| repo `CLAUDE.md` | 結構樹註解「bundle SemVer(3.0.0)…version: 3」、「兩個版本號別搞混」表、跨檔耦合表等寫死 v3／`3.x.y` 處；「兩個版本號別搞混」表 bundle release 列的「git tag（`v3.x.y`，發版時打）」補上 D6 的 release commit 定義與「自 4.0.0 起實際執行」；跨檔耦合表 Compatibility 那列的「CI 直接 fail」補一句：新增列而舊列保留時不會 fail，而是默默讀舊列 |
| `docs/roadmap.md`（+ zh-TW） | **design 階段核對結果：需要連動**。v2、v3 各有一段「— Released」，v4 照例新增一段（schema major 4、bundle 4.0.0；說明 Task 寫法與程式碼區塊行為變更） |
| `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/` | `fixtures/` 新增 D7 的測試資料；凍結預期記在上一層的 `README.md` |

## Risks / Trade-offs

- [Risk] 上游 selector 抽錯範圍（D3 五種），Agent 拿到被污染的簡報照做。→ Mitigation：guidance 三句；D7 第 3 點比對內容而非 exit code。殘餘風險：不照 guidance 寫的 plan 仍會被抽錯，Bridge 不攔。
- [Risk] 外部 plan 的 ``` 區塊內有 `##` 標題，v3 靠它通過、v4 變不通過（或反之）。→ Mitigation：列為 v4 行為變更並寫進遷移說明；本 repo 查過無此情況，不推及外部。
- [Risk] 舊 plan 有 `## Task <數字>` 開頭的非條目 H2，v4 把它讀成條目。→ Mitigation：遷移說明點名此例外；fixture「舊非條目被重新解讀」把破壞具體化。
- [Risk] 外部 plan 用 `##1.1` 或縮排的 ` ## 1.1` 當條目，v3 照字面收、v4 不收，變成缺鍵被擋。→ Mitigation：遷移說明點名此例外；fixture「非行首 H2 不再是條目」把破壞具體化；本 repo 掃過無此情況。
- [Risk] check 12 是說明文字、沒有程式，Agent 可能讀錯新規則。→ Mitigation：D7 第 1、2 點的 agent 執行變異測試，Agent 事先看不到答案、要回報中間值。殘餘風險：證據是 instruction 層的行為樣本，不是窮舉。
- [Risk] `version-check.yml` 改抓 v4 後讀錯欄位，每週檢查默默比錯版本。→ Mitigation：D7 第 5 點列為必驗；表下說明不寫進格子。
- [Risk] 有人「好心統一」check 12 與 check 13 的區塊處理。→ Mitigation：兩處都寫刻意不對稱的理由（D5）。
- [Risk] rollback SHA 留下 placeholder 或填錯。→ Mitigation：定稿時填入並實際 checkout 一次；verify 前必須結掉。
- [Risk] release tag 規則再次沒被執行。→ Mitigation：完成條件掛在工作地圖那筆上（D6），未確認遠端 tag 前不得結案；跨 release 的提醒（乙案）另登記評估。殘餘風險：v4.0.0 之後的 release 仍靠各自 change 記得設同樣的完成條件。
- [Trade-off] 雙語法並存，checker 規則比單一語法長。→ 接受：避免一次讓所有既有 plan 變不合法；D1 列了將來重議的判準。
- [Trade-off] 只認 ```、不認 `~~~`，比 CommonMark 窄，作者用 `~~~` 包範例時裡面的標題仍會被收。→ 接受：與上游一致比貼近 Markdown 規格重要（D4）；作者可改用 ```。
- [Trade-off] v4 列基準仍是 `v5.1.0`，每週落後檢查會持續提醒。→ 接受：符合真實狀態；轉 6.x 另有工作。

## Migration Plan

**採用者（v3 → v4）**——寫進 bridge README「Migrating v3 → v4」：

> 既有 plan 一般不需遷移，舊的 `## <編號> —` 條目標題仍有效。需要檢查的例外有三種：
> 1. 原本作為非條目使用、但標題以 `## Task <數字>` 開頭的 H2：v4 會把它解讀成條目，需要改名。
> 2. 行首 ``` 區塊內寫著 `##` 標題：check 12 現在跳過它們，原本靠區塊內標題才通過（或因此被擋）的 plan 判定會改變。
> 3. 條目標題必須從行首開始，且 `##` 後必須有空白：v3 照字面可能接受的 `##1.1` 或縮排的 ` ## 1.1`，v4 不再視為條目。
>
> 本 repo 已確認三種情況都沒有。

**本 repo 部署順序**：

1. 改 `superpowers-bridge/` 底下的 schema、模板、VERSION、README，與 `version-check.yml`、repo `CLAUDE.md`、roadmap——同一個 change 內完成，跨檔耦合表要求的連動一起進。
2. 本地 `openspec schema validate` + `openspec schemas`。
3. 同步 `openspec/schemas/superpowers-bridge/` 副本（`rm -rf` 後 `cp -R`），再跑本 change 的 verify。
4. push 後確認 `validate-schemas.yml` 綠；手動觸發 `version-check.yml`（`workflow_dispatch`），確認 `Read pinned versions` 讀到 v4 列的兩個版本號。
5. archive、最終驗證、release 連動文件都完成後，依 D6 的 release 動作建立並推送 annotated tag `v4.0.0`，確認遠端指向 release commit，再把工作地圖那筆改為完成。

**退回**：checkout D6 定義的 SHA（第一個 `version: 4` commit 的 parent）取得 v3 的 `superpowers-bridge/`，重新複製進 `openspec/schemas/`。

## Open Questions

- 「寫錯格式」那份測試資料是否拆成三份（各一種錯法）：plan 階段決定。
- `sdd-workspace` 在 Git Bash 印 `/tmp/...` 路徑、Windows 子代理的讀檔工具能否直接讀：poc 報告列為未測，dogfood 時會碰到。
- dogfood 實際載入的 Superpowers 版本：執行時確認並寫進證據。
- v3 退回用 SHA：commit 邊界確定後填入並實際 checkout 驗證；不得留 placeholder。
- 只在 Claude Code 上測，其他平台未測。
- S12、S14 是否已有工作處理：屬 `task-20261007-superpowers-6x-rebaseline` 第一步，不在本 change。
