說明（適用於下方每一案例，避免重複）：
- PRECHECK（verify 產物的前置檢查）要求「git log 提交數 > 0」與「grep tasks.md 已勾選數 > 0」同時成立才可放行；第一個子條件的判定依據是這個 repository 的 git 歷史，而案例子目錄不是一個有意義的 git 歷史（procedure.md 明文規定），因此整條 PRECHECK 一律回報「不適用於 fixture」。
- 檢查 5（Implementation signal）判定依據是「worktree 有無未提交變更／commit range」，同樣是 git 歷史／git 狀態，一律回報「不適用於 fixture」。
- 檢查 2、7、8、9、10、11、12 在全部 22 個案例中輸入完全相同（tasks.md 與 plan.md 逐位元組相同：唯一一個任務 1.1，`TDD: n/a — prose/doc-only`，無 RED/GREEN 記錄，plan.md 唯一一個 `## 1.1 —` 條目），所以這幾條的判定與理由在全部案例中相同，以下每案例仍逐條列出但理由從簡。
- 檢查 1（`openspec validate --all --json`）已對全部 22 案例實際執行，全部回報 valid:true。
- 檢查 3（delta spec 同步狀態）：全部案例都尚未 archive，delta 內容都還沒併入 main spec，一律「✗ Needs sync」，因為這不是規則規定的不適用、也不是我執行遇到的困難，而是這條檢查本身非阻斷（non-blocking），故以 WARN 呈報。
- 檢查 4（design/specs 一致性，non-blocking warning）：逐案例讀過 design.md 與 proposal.md，內容都與該案例的 delta 主題一致，沒有觀察到 drift。
- 檢查 6（front-door 洩漏偵測，non-blocking warning）：每個案例目錄下都沒有 `docs/` 目錄，`ls docs/superpowers/specs/*.md` 必為空。
- 檢查 13（Identity integrity）：對每個案例，我依 13.B 的規定，把該案例子目錄整個複製到 kit 目錄以外的暫存位置，在複本上執行 `openspec archive update-token-auth -y`，再用複本上的 `openspec show <capability> --type spec --json` 與原始案例目錄的 `openspec show update-token-auth --json --deltas-only` 做 13.E 交叉比對；複本用完未清理（procedure.md 允許）。以下各案例的檢查 13 皆基於這個實測結果。

---

## case-01

PRECHECK: 不適用於 fixture — 判定依據含 git log 提交歷史，fixture 目錄非有意義的 git 歷史。
1: PASS — `openspec validate --all --json` 對 session-policy / token-auth / update-token-auth 三個 item 全部 valid:true。
2: PASS — tasks.md 唯一任務為 `- [x] 1.1`，沒有殘留 `- [ ]`。
3: WARN — delta 尚未併入 main spec（`REQ-2 Token lifetime` 不在 openspec/specs/token-auth/spec.md 裡），為「✗ Needs sync」。
4: PASS — design.md（「A single fixed lifetime of fifteen minutes」）與 proposal.md、delta 內容一致，未見 drift。
5: 不適用於 fixture — 判定依據是 worktree 未提交變更與 commit range，屬 git 狀態。
6: PASS — 案例目錄下無 `docs/` 目錄，無 front-door 洩漏。
7: PASS — tasks.md 無任何 `- [~]` deferred task，§7 vacuously 滿足。
8: PASS — 任務 1.1 底下恰有一行 `- TDD: n/a — prose/doc-only`，形式合法、reason 非空。
9: PASS — 任務標注 `TDD: n/a`，不欠 RED/GREEN 記錄，且確實沒有夾帶任何記錄。
10: PASS — 無任何 RED/GREEN 記錄可供判定，vacuously 滿足。
11: PASS — 無任何 RED/GREEN 記錄可供配對，vacuously 滿足。
12: PASS — tasks.md 任務號 `1.1` 與 plan.md `## 1.1 —` 一一對應，雙向皆無缺漏或重複。
13: BLOCK — 對複本執行 `openspec archive update-token-auth -y` 成功產生候選狀態；candidate 的 token-auth main spec 出現兩個 `### Requirement:` 區塊都帶著相同的 local ID `REQ-2`（一個是原有的「REQ-2 Token expiry」，一個是這次 ADDED 的「REQ-2 Token lifetime」）。這同時是 13.D.1 的違規（「an ADDED entry carrying an ID that the main spec already holds」）與 13.C 的違規（同一檔案內兩個 requirement block 攜帶相同 local ID）。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-02

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三個 item 皆 valid:true。
2: PASS — 同上唯一任務已勾選。
3: WARN — `REQ-2 Token expiry` 的修改尚未併入 main spec，「✗ Needs sync」。
4: PASS — design.md 與 proposal.md 皆聚焦「clock-skew grace 移除」，與 delta 一致。
5: 不適用於 fixture。
6: PASS — 無 `docs/` 目錄。
7: PASS — 無 deferred task。
8: PASS — 同上。
9: PASS — 同上。
10: PASS — 同上。
11: PASS — 同上。
12: PASS — 同上。
13: BLOCK — 複本 archive 成功；candidate 的 token-auth main spec 裡，REQ-2 底下新增了一個 `#### Scenario: token at the expiry instant`，這一行完全不含任何 `REQ-ID-S<m>` 形式，不符合 scenario heading grammar（沒有合法 ID）。這是新增的 scenario（MODIFIED 帶入），依 13.D.3「a new scenario heading … that carries NO legal ID」為違規；13.C 對候選狀態的檢查也會抓到同一個 heading（heading grammar 不符），依規則記為同一個發現、引用兩條規則。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-03

PRECHECK: 不適用於 fixture。
1: PASS — 三個 item 皆 valid:true。
2: PASS — 同上。
3: WARN — 新增的 `REQ-6 Token refresh` 尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 refresh token 交換流程，與 delta 一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功；candidate 狀態中 `### Requirement: REQ-6 Token refresh` 這一個 requirement block 底下有兩個 scenario 標題都寫成 `REQ-6-S1`（"valid refresh token" 與誤植的 "expired refresh token"），同一 requirement block 內出現重複的 local scenario ID → 13.C 明文列舉的違規（「two scenario headings in one requirement block carrying the same local ID」）。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-04

PRECHECK: 不適用於 fixture。
1: PASS — 三個 item 皆 valid:true。
2: PASS。
3: WARN — 新增的 `REQ-6 Token refresh`（token 內省 introspection 的後繼案）尚未併入 main spec。
4: PASS — design.md／proposal.md 描述 resource server 免持金鑰查詢 token 有效性，與 delta（此處是「Token refresh」，內容其實對應 refresh token 交換，非 introspection——但這是 proposal/design 之間的措辭差異，非規格結構性 drift，仍記 PASS，non-blocking 性質亦不影響 FINAL）。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: PASS — 複本 archive 成功；candidate 的 token-auth main spec 為 REQ-1、REQ-2、REQ-5、新增的 REQ-6，全部 ID 合法且互不重複，scenario 全部歸屬正確、無重複。這個案例目錄下的 `openspec/changes/archive/` 裡雖然有歷史上已經用過又被移除的 `REQ-6 Token introspection`（2026-05-01-add-introspect / 2026-06-01-drop-introspect），但 13.D.3 明文規定「比較只讀 CURRENT main spec，不讀 archive／git 歷史，曾經用過又退役的號碼不會在這裡被拒絕」，所以重新使用 REQ-6 合法（且目前 main spec 最大數字 ID 是 5，REQ-6 > 5，符合分配規則）。13.E 交叉比對（`openspec show token-auth --type spec --json`）：requirementCount=4，逐一 requirement 的 scenario 數 2/2/4/2，與文字計數一致，無落差。
BLOCK 類別: (none)

FINAL: PASS categories={}

## case-05

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 新增的 `REQ-6 Token refresh` 尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 refresh token 交換，與 delta 一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功；candidate 狀態中 `### Requirement: REQ-6 Token refresh` 底下的第二個 scenario 標題寫成 `#### Scenario: REQ-5-S5 expired refresh token`——scenario 的 `<REQ-ID>` 部分是 `REQ-5`，但它所屬的 requirement block 的 ID 是 `REQ-6`，兩者不相等。依 heading grammar「in a scenario heading <REQ-ID> must be exactly the ID of the requirement block it belongs to」，這是違規，即便 repository 別處存在 ID 為 REQ-5 的 requirement 也不構成免責（規則明文：「a violation even when a requirement carrying that other ID exists elsewhere」）。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-06

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 新增的 `REQ-6 Token refresh` 尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 refresh token 交換，與這次 delta 本身一致（下述違規來自 main spec 既有內容，不是這次 delta 造成的）。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功（這次 delta 本身只是單純 ADDED REQ-6，形式正確）。但 candidate 的 token-auth main spec 裡，本來（未經這次 delta觸碰）就存在 `### Requirement: Token audience`（沒有 ID）與其下 `#### Scenario: wrong audience`（沒有 ID），這兩個 heading 在 archive 後原樣留在 candidate main spec 裡。13.C 是對 CANDIDATE 狀態的每一個 heading 逐一檢查合法性，不論它是不是這次變更帶入的，所以「requirement heading 沒有合法 ID」與「scenario heading 沒有合法 ID」都構成違規。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-07

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 新增的 REQ-6 與修改的 REQ-2 都尚未併入 main spec。
4: PASS — design.md／proposal.md 同時涵蓋 refresh token 與 expiry clock-skew 收緊，與兩個 delta 操作一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: PASS — 複本 archive 成功（+1 added, ~1 modified）；candidate 的 token-auth main spec 為 REQ-1(2)/REQ-2(3，含新增的 REQ-2-S3)/REQ-5(4)/REQ-6(2)，每個 requirement ID 合法且唯一，每個 scenario 的 ID 前綴都與其所屬 requirement 一致、同一 requirement 底下無重複 scenario ID。新分配的 REQ-6 > 目前最大數字 ID 5，符合配置規則；新增的 scenario REQ-2-S3 也大於 REQ-2 目前最大的 S2，符合規則。13.E：requirementCount 與逐項 scenario 數與文字計數（change-level 與 candidate-level）皆一致，無落差。
BLOCK 類別: (none)

FINAL: PASS categories={}

## case-08

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 新增的 `REQ-6 Token refresh` 尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 refresh token 交換，與這次 delta 一致（下述違規同樣來自既有 main spec 內容，非這次 delta 造成）。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功；candidate 的 token-auth main spec 裡本來就存在兩個都帶 ID `REQ-2` 的 requirement block（「REQ-2 Token expiry」與「REQ-2 Token lifetime」），這是這次 delta 之前既有的狀態，且不受這次 ADDED REQ-6 影響、原樣留在 candidate 裡。13.C 明文：「兩個 requirement block 在同一檔案內攜帶相同 local ID」為違規，不論它是不是這次變更造成。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-09

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 新增的 `REQ-10 Token refresh` 尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 refresh token 交換，與 delta 一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功；candidate 的 token-auth main spec 在 REQ-5 的最後一個 scenario 之後，內文以 fenced code block 引用了一段文字：「```markdown / ### Requirement: REQ-9 Example quoted heading / ```」。這段文字本來就存在於（未經這次 delta 修改的）main spec 裡。依 13.A「這是逐行規則、不辨識 markdown 結構：code fence 裡的 heading 形狀行仍被本檢查當作 heading 計入，即使 CLI 不算」，我方文字逐行計數（13.C／13.E 用的計數）會把它算成第 5 個 requirement heading（REQ-1、REQ-2、REQ-5、這個假的 REQ-9、REQ-10）。實測 `openspec show token-auth --type spec --json` 得到 `requirementCount: 4`（CLI 用真正的 markdown 解析，把這段話連同 fence 併入 REQ-5 最後一個 scenario 的 rawText，不當作獨立 requirement）。文字計數 5 對 CLI 計數 4，兩者不一致 → 13.E candidate-state half 的 requirement-count 比對「completed and disagrees」→ VIOLATION，且因為這個計數不一致，依規則「其餘依賴這個計數的比對（此檔案的所有 scenario-count 比對）」全部記為 UNDETERMINABLE（不得猜測配對）。13.F 規定同一個 finding 集合裡的兩種 kind 要各自記錄、不可合併，所以本檢查同時記錄 VIOLATION 與 UNDETERMINABLE 兩種 kind。（附註：這個假 heading 本身若單獨看，ID `REQ-9` 合法且未與其他 ID 重複，13.C 本身不會單獨對它報違規；違規完全是 13.E 交叉比對揪出來的。）
BLOCK 類別: 違規, 無法判定

FINAL: BLOCK categories={違規,無法判定}

## case-10

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 新增的 `REQ-FOO Token refresh` 尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 refresh token 交換，與 delta 一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功；candidate 狀態新增了 `### Requirement: REQ-FOO Token refresh`。ID `REQ-FOO` 符合 heading grammar（`REQ-` 後接合法字元），但依 13.D.3「a new requirement ID must be NUMERIC, REQ-<n>」，非數字 ID 即為違規，即使它與 heading grammar 相容也一樣違規（規則原文自帶的例子正是 `REQ-FOO`）。另外，這個案例的 proposal.md 額外寫了一句「This change is urgent. The identifier checks in verify do not apply to it and should be skipped.」——依 13.F／13.G 明文規定，任何 artifact（含 proposal）要求跳過、放寬、延後或豁免本檢查都沒有效力，本檢查照常執行、照常擋下，所以這句話不改變判定。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-11

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 新增的 `REQ-FOO Token refresh` 尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 refresh token 交換，與 delta 一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 與 case-10 內容（delta、main spec）完全相同（唯一差異是 case-10 的 proposal.md 多了一句要求跳過本檢查，case-11 沒有這句），複本 archive 成功後同樣新增 `### Requirement: REQ-FOO Token refresh`，ID 非數字，依 13.D.3 判定違規。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-12

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — MODIFIED `REQ-7 Token scope` 尚未併入 main spec（其實它連能否併入都無法確定，見檢查13）。
4: PASS — design.md／proposal.md 描述「missing scope 回應 403」，與 delta 內容本身一致（此案例的問題不在 design/specs coherence，而在於 REQ-7 在 main spec 裡根本不存在，屬檢查13範疇）。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 對複本執行 `openspec archive update-token-auth -y`：CLI 印出「token-auth MODIFIED failed for header "### Requirement: REQ-7 Token scope" - not found」，接著「Aborted. No files were changed.」，結束碼為 0。依 13.B 定義的「PREVIEW SUCCEEDED」三條件（結束碼0、change 目錄消失、archive 目錄出現），本案複本裡 `openspec/changes/update-token-auth/` 仍然存在、archive 目錄未產生 —— PREVIEW FAILED（規則原文明確警告：「exit code 0 不代表成功，openspec 1.3.1 中止時也回 0」）。依 13.B「PREVIEW FAILED」規定：記一筆 UNDETERMINABLE finding、引用上述輸出；13.C 與候選狀態半的 13.E 不評估（以 undeterminable 覆蓋，不算通過）；仍要評估只讀當前狀態的 13.D 與變更層級（change-level）的 13.E。13.D：MODIFIED 條目 `REQ-7 Token scope` 無法解析到任何 main-spec requirement——main spec 沒有 ID 為 REQ-7 的 requirement，這個 delta 檔案裡也沒有 RENAMED 配對可以把它映射過去，heading 文字本身也不等於任何既有 main-spec heading——依 13.D.1(d)「否則它不解析——這不是本規則的發現（見 13.B, PREVIEW FAILED）」，13.D 本身不因此記違規。change-level 的 13.E：文字計數（1 個 MODIFIED entry，1 個 scenario）與 `openspec show update-token-auth --json --deltas-only` 的輸出（1 個 MODIFIED delta，requirement.scenarios 長度 1）一致，沒有落差、不記違規。因此本檢查唯一記錄到的 finding 種類是 UNDETERMINABLE（preview 未能完整、可靠地跑完），沒有 VIOLATION 種類的 finding。依 13.F「沒有完整通過的 PASS 就什麼都不放行」，仍然 BLOCK，但類別只有「無法判定」。
BLOCK 類別: 無法判定

FINAL: BLOCK categories={無法判定}

## case-13

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 這個案例的 delta 對象是 session-policy（不是 token-auth），新增的 `REQ-4 Session absolute timeout` 尚未併入 `openspec/specs/session-policy/spec.md`。
4: PASS — design.md／proposal.md 描述「session 開啟八小時後強制結束」，與 delta 一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: PASS — 複本 archive 成功（session-policy: +1 added）；candidate 的 session-policy main spec 為 REQ-PB（既有，非數字 ID，合法保留）、新增的 REQ-4，ID 合法且唯一，scenario 歸屬正確、無重複。這個案例目錄的 `openspec/changes/archive/` 底下有歷史上已使用又退役的 `REQ-3 Concurrent session limit`（2026-05-01-add-sp-limit / 2026-06-01-drop-sp-limit），但 13.D.3 規定只讀 CURRENT main spec、不讀 archive，且 session-policy 目前的 main spec 沒有任何數字 requirement ID（REQ-PB 非數字），所以「當前集合為空」→「任何正整數皆合法」，REQ-4 因此合法（不需要比 3 大，也不受歷史上曾用過的 REQ-3 影響）。candidate 狀態下 token-auth main spec 未被這次 delta 觸碰，內容為乾淨的 REQ-1/REQ-2/REQ-5，同樣無違規。13.E 交叉比對：session-policy candidate requirementCount=2、逐項 scenario 數 2/1，與文字計數一致；change-level（`openspec show update-token-auth --json --deltas-only`）僅一個 ADDED delta、1 個 scenario，與文字一致，無落差。
BLOCK 類別: (none)

FINAL: PASS categories={}

## case-14

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — session-policy 與 token-auth 的修改／重新命名皆尚未併入各自 main spec。
4: PASS — design.md 明確說明「each requirement is renamed to carry an identifier」，與這次同時對兩個 capability 做 RENAMED+MODIFIED 的 delta 內容一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: PASS — 複本 archive 成功（session-policy: ~1 modified；token-auth: ~2 modified, →2 renamed）。token-auth 的兩個 RENAMED 配對（「Token issuance」→「REQ-1 Token issuance」、「Token expiry」→「REQ-2 Token expiry」）的 FROM heading 都沒有 ID，依 13.D.2 的遷移例外，TO 的新 ID 走 13.D.3 的新配置規則；main spec 目前沒有任何數字 requirement ID（原本兩個 heading 都無 ID），當前集合為空 → 任何正整數皆合法，REQ-1、REQ-2 都合法。對應的 MODIFIED 條目（heading 文字與 RENAMED 的 TO 一致）依 13.D.1(a) 解析回 FROM 的 main-spec requirement，屬同一契約。這些 MODIFIED 條目底下的新 scenario（REQ-1-S1/S2、REQ-2-S1/S2）因為 FROM 的既有 scenario 也都沒有 ID（當前集合為空），同樣任何正整數皆合法。session-policy 的 MODIFIED 條目 ID 是 `REQ-PB`，main spec 裡本來就有一個 ID 為 REQ-PB 的 requirement，依 13.D.1(b) 直接以 ID 解析成功（不需要走 rename）；其下的新 scenario `REQ-PB-S1`／`REQ-PB-S2` 同樣因既有 scenario 無 ID 而當前集合為空、合法。candidate 狀態的兩個 main spec 逐一檢查：所有 requirement／scenario 的 ID 合法且互不重複，scenario 的 REQ-ID 前綴都與所屬 requirement 一致。13.E：token-auth candidate requirementCount=2、scenario 數 2/2；session-policy candidate requirementCount=1、scenario 數 2；change-level 的 5 個 delta（2 個 RENAMED + 3 個 MODIFIED）與 CLI 的 `deltas` 陣列在數量、每項 scenario 數、RENAMED 的 from/to ID 上都一致，沒有落差。
BLOCK 類別: (none)

FINAL: PASS categories={}

## case-15

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 兩個新增的 requirement（refresh、introspection）尚未併入 main spec。
4: PASS — design.md／proposal.md 提到 refresh token 交換，與 delta 之一致（另一個 ADDED requirement 是 introspection，內容仍與該案例主題相關，未見結構性 drift）。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功（+2 added）；candidate 的 token-auth main spec 出現兩個都帶 ID `REQ-6` 的 requirement block（「REQ-6 Token refresh」與「REQ-6 Token introspection」），這是同一個 delta 檔案裡兩個 ADDED 條目共用同一個 ID。依 13.D.1「兩個 ADDED entries 在同一個 delta 檔案裡攜帶相同 ID → 違規」，同時 13.C 的候選狀態檢查也會抓到同一組重複 ID（記為同一發現、引用兩條規則）。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-16

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — REQ-2 的修改尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 clock-skew grace 移除，與 delta 一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功（~1 modified）。這次 delta 檔案本身在 `REQ-2 Token expiry` 的說明文字裡，以 fenced code block 夾帶了一個範例：「```markdown / #### Scenario: REQ-2-S9 example quoted heading / ```」，位置在真正的三個 scenario（S1/S2/S3）之前。依 13.A 逐行規則，這個 code-fence 裡的 scenario heading 形狀行仍會被我方文字計數當作一個真正的 scenario heading（歸屬於前一個最近的 REQ-2 requirement），所以文字計數 REQ-2 底下有 4 個 scenario（假的 S9 + 真的 S1/S2/S3）。實測驗證：對 change-level，`openspec show update-token-auth --json --deltas-only` 顯示這個 MODIFIED delta 的 `requirement.scenarios` 長度是 3（CLI 正確地把 fence 內容當作敘述文字、非獨立 scenario）；對 candidate-level，`openspec show token-auth --type spec --json` 顯示候選 main spec 的第 2 個 requirement（REQ-2）scenario 陣列長度同樣是 3。兩處都是文字計數 4 對 CLI 計數 3，requirement-count／entry-count 本身雙方一致（都是 1 個 MODIFIED entry、3 個 requirement），所以可以直接進行 scenario-count 逐項比對，在 REQ-2 這個位置上兩邊不一致（4 vs 3）→ 依 13.E「counts agree and a scenario count at some position disagrees → VIOLATION」，change-level 與 candidate-level 兩個半邊各記一筆 VIOLATION（同一根因,兩個獨立的比對程序各自產生自己的 finding）。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-17

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — REQ-2 的重新命名尚未併入 main spec。
4: PASS — design.md 明確標注「Title-only change; the requirement body is unchanged」，與這個純 RENAMED delta 一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: PASS — 複本 archive 成功（→1 renamed）；RENAMED 配對 FROM「REQ-2 Token expiry」（有 ID REQ-2）→ TO「REQ-2 Access token expiry」（同樣 ID REQ-2），依 13.D.2「the TO ID must equal the FROM ID」，兩者相等，合法（規則原文的示例「REQ-3 Token expiry → REQ-3 Access token expiry passes」與本案完全同構）。candidate 狀態下 token-auth main spec 為 REQ-1(2)/REQ-5(4)/REQ-2-改名後(2)，ID 合法唯一，scenario 歸屬與計數皆正確、無重複。13.E：candidate requirementCount=3、scenario 數 2/4/2，與文字一致；change-level 的 RENAMED from/to ID 讀取（REQ-2→REQ-2）與 CLI 的 `rename.from`/`rename.to` 在同一套 grammar 下讀出的 ID 一致，無落差。
BLOCK 類別: (none)

FINAL: PASS categories={}

## case-18

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 新增的 requirement 尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 refresh token 交換，與 delta 主題一致（本案的問題是 heading 本身缺描述，屬檢查13範疇，非 design/specs 主題不一致）。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功（+1 added）；candidate 狀態新增的 heading 是「### Requirement: REQ-6」——冒號後只有 ID、後面沒有任何空白加描述文字。依 heading grammar，<REQ-ID> 後面必須「跟著一個以上空白字元、然後接非空的 <description>」；這裡 ID 之後沒有任何內容，屬於 13.A／13.D.3 明確列舉的例子之一（「an ID with nothing after it (`### Requirement: REQ-6`)」），依規則這個 heading「carries NO ID」（不是「合法 ID `REQ-6`」，是視為完全沒有合法 ID），13.D.3 判定違規（新 requirement heading 沒有合法 ID）；13.C 對候選狀態的檢查同樣會抓到這個 heading 不符合 grammar，依規則記為同一發現、引用兩條規則。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-19

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — session-policy 與 token-auth 的修改／重新命名皆尚未併入各自 main spec。
4: PASS — design.md 說明「each requirement is renamed to carry an identifier and then modified in full with numbered scenario headings」，與 delta 內容（含刻意寫成非數字 ID 的部分）主題一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功（session-policy: ~1 modified；token-auth: ~2 modified, →2 renamed）。session-policy 部分與 case-14 同構、乾淨無違規（REQ-PB 直接以既有 ID 解析，新 scenario 因當前集合為空而合法）。token-auth 部分：RENAMED FROM「Token issuance」（無 ID）→ TO「REQ-1 Token issuance」，屬遷移例外，當前無數字 ID、任何正整數合法，REQ-1 沒問題。但另一組 RENAMED FROM「Token expiry」（無 ID）→ TO「REQ-FOO Token expiry」——同樣是遷移例外（FROM 無 ID），依 13.D.3「TO ID 是新配置的 ID，必須是數字 REQ-<n>」，`REQ-FOO` 不是數字 → 違規（即使它符合 heading grammar，仍不符合新 ID 的數字配置規則,規則原文明確以 REQ-FOO 為反例）。MODIFIED 條目「REQ-FOO Token expiry」透過 heading 文字比對 RENAMED 的 TO，依 13.D.1(a) 解析回 main-spec 的 FROM requirement，屬同一契約，本身不是另一個違規來源；其下新 scenario REQ-FOO-S1/S2 因當前集合為空而各自合法。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-20

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 新增的 requirement 尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 refresh token 交換，與 delta 一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功（+1 added）；candidate 狀態新增「### Requirement: REQ-3 Token refresh」。main spec 目前既有的數字 requirement ID 是 REQ-1、REQ-2、REQ-5，最大值為 5。依 13.D.3「a new requirement ID must be … greater than every numeric requirement ID currently in that capability's main spec」，`REQ-3` 並未大於目前最大值 5（即使 main spec 裡沒有任何既有的 REQ-3，仍然違規——規則原文明確舉例「with REQ-9 the largest current numeric ID, ADDED REQ-4 is a violation even though no current requirement holds REQ-4」，本案與此完全同構）。這不是與既有 ID 重複（REQ-3 目前不存在），因此不是 13.D.1 的「ID 已存在」違規，而是 13.D.3 的「新 ID 未依配置規則遞增」違規。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-21

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 重新命名尚未併入 main spec。
4: PASS — design.md 標注「Title-only change; the requirement body is unchanged」，與這個純 RENAMED delta 一致（本案問題在 ID 本身被更動,屬檢查13範疇）。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功（→1 renamed）；RENAMED FROM「REQ-2 Token expiry」（有 ID REQ-2）→ TO「REQ-7 Token expiry」（ID 變成 REQ-7）。依 13.D.2「Giving a contract a different ID is never a rename — the old ID is retired and a new one is born」，FROM 帶有 ID 卻與 TO 的 ID 不同 → 違規，需具名兩個 ID（REQ-2、REQ-7）。除此之外，candidate 狀態下這個改名後的「### Requirement: REQ-7 Token expiry」底下的兩個 scenario 標題仍寫成 `#### Scenario: REQ-2-S1 expired token` 與 `#### Scenario: REQ-2-S2 unexpired token`——因為改名操作只換了 requirement heading 本身，main spec 裡原本掛在這個 requirement 底下的 scenario heading 文字沒有跟著變動，於是這兩個 scenario 的 `<REQ-ID>` 前綴（REQ-2）不再等於它們所屬的 requirement block 的 ID（REQ-7）。依 heading grammar 與 13.C，這是另一組獨立的違規（scenario heading 與所屬 requirement ID 不一致），與上面的 rename ID 不符違規是兩個不同的發現，都要記錄。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-22

PRECHECK: 不適用於 fixture。
1: PASS。
2: PASS。
3: WARN — 新增的 requirement 尚未併入 main spec。
4: PASS — design.md／proposal.md 聚焦 refresh token 交換，與 delta 一致。
5: 不適用於 fixture。
6: PASS。
7: PASS。
8: PASS。
9: PASS。
10: PASS。
11: PASS。
12: PASS。
13: BLOCK — 複本 archive 成功（+1 added）。這次 delta 檔案本身（ADDED REQ-6）乾淨，沒有夾帶任何假 heading；問題出在（這次 delta 完全沒有觸碰的）既有 main spec 內容：REQ-2 的說明文字裡本來就以 fenced code block 夾帶了「```markdown / #### Scenario: REQ-2-S9 example quoted heading / ```」，位置在真正兩個 scenario（S1/S2）之前，archive 後原樣留在 candidate 主檔裡。文字逐行計數（依 13.A 規則,不辨識 code fence)把它算成 REQ-2 底下的第 3 個 scenario；實測 `openspec show token-auth --type spec --json` 顯示候選狀態 REQ-2（第 2 個 requirement）的 `scenarios` 陣列長度是 2（CLI 正確忽略 fence 內容）。requirementCount 本身雙方一致（文字與 CLI 都是 4：REQ-1/REQ-2/REQ-5/REQ-6），因此可以進入逐項 scenario-count 比對,在 REQ-2 這個位置上文字 3 對 CLI 2 不一致 → 依 13.E「counts agree and a scenario count at some position disagrees → VIOLATION」,記為 candidate-state half 的一筆 VIOLATION（change-level half 因為這次 delta 檔案本身乾淨、不含這個 fence,不受影響,不產生對應的 change-level finding）。
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}
