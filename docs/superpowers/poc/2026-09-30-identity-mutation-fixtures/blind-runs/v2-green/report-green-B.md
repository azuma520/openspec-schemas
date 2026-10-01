## case-01

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history（git log），案例目錄無有意義 git 狀態
1: PASS — openspec validate --all --json 對 session-policy/token-auth/update-token-auth 三項皆回報 valid:true
2: PASS — tasks.md 唯一任務 1.1 為 - [x]，無殘留 - [ ]
3: PASS — 記錄為 需sync 狀態（delta 尚未併入 main spec，change 尚未 archive），屬非阻斷性記錄
4: PASS — design.md 內容（refresh token 換發）與 specs 一致，無需記警告
5: NOT_APPLICABLE — 判定依賴 working-tree 是否有未提交變更（git 狀態）
6: PASS — 案例目錄下不存在 docs/superpowers/specs/*.md
7: PASS — tasks.md 無任何 [~] deferred 任務，第7項無需列出項目
8: PASS — 任務 1.1 帶 TDD: n/a — prose/doc-only，格式合法、reason 非空
9: PASS — 任務標記 n/a，不需 RED/GREEN 記錄，tasks.md 內亦未附加任何記錄
10: PASS — 無 RED/GREEN 記錄可讀，無 outcome 需檢查（vacuous）
11: PASS — 無 RED/GREEN 記錄，無 subject 需配對（vacuous）
12: PASS — tasks.md 任務鍵 1.1 與 plan.md 唯一 entry ## 1.1 一一對應
13: BLOCK — Archive preview 成功；candidate 狀態下 token-auth main spec 出現兩個 requirement block 共用同一 local ID REQ-2（既有的「REQ-2 Token expiry」與「REQ-2 Token lifetime」），13.C 判定為重複 ID 違規；13.E 文字計數（5）與 CLI requirementCount（5）一致，各 scenario 位置計數（2,2,1,4,2）與 CLI 完全吻合，未見計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-02

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history，案例目錄無有意義 git 狀態
1: PASS — openspec validate --all --json 三項皆 valid:true
2: PASS — tasks.md 唯一任務為 - [x]
3: PASS — 記錄為需sync 狀態，非阻斷性
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — 判定依賴 working-tree 狀態
6: PASS — 無 docs/superpowers/specs/*.md
7: PASS — 無 deferred 任務
8: PASS — 任務 1.1 TDD 標記合法
9: PASS — n/a 任務無需 RED/GREEN，且未附加
10: PASS — 無記錄可檢（vacuous）
11: PASS — 無記錄可檢（vacuous）
12: PASS — tasks.md 1.1 與 plan.md ## 1.1 一一對應
13: BLOCK — Archive preview 成功；main spec 現有 REQ-2 區塊內嵌一段 fenced code block，其中含一行格式合法的 Scenario: REQ-2-S9 example quoted heading。依 13.A 規則，這種標題形狀的行即使在 fenced code block 內也要被算入，但 openspec CLI 不會把它算進 JSON。文字計數下 REQ-2 底下有 3 個 scenario 標題（S9、S1、S2），而 CLI requirements[1].scenarios.length 只回報 2，requirement 總數本身雙方一致（4=4），故此為 13.E 定義下「requirement 數一致、但某位置 scenario 數不一致」的情形，直接記為 VIOLATION（非 undeterminable），並具名該位置與兩邊數值

FINAL: BLOCK | categories=VIOLATION

## case-03

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 的 ADDED 項標題寫成 Requirement: REQ-6，冒號後只有 ID、沒有任何 description。依 heading grammar，ID 後必須有一個以上空白再接非空 description，「ID 後面什麼都沒有」屬於 carries NO ID 的情形，13.C 與 13.D.3 都會把它判為違規（同一標題兩條規則都命中，只記一次）；13.E 的 requirement 數（4=4）與各位置 scenario 數（2,2,4,2）雙邊一致，未見計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-04

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md（title-only change）與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 為 RENAMED，FROM Requirement: REQ-2 Token expiry（ID=REQ-2）TO Requirement: REQ-7 Token expiry（ID=REQ-7）。13.D.2 規定 FROM 帶 ID 時 TO 的 ID 必須與 FROM 相同，這裡 REQ-2 到 REQ-7 是把舊 ID 退役、開新 ID，不算合法 rename，記為 VIOLATION。另外，candidate 狀態下該（改名後的）REQ-7 區塊底下的 scenario 標題仍寫成 Scenario: REQ-2-S1 與 REQ-2-S2，其 REQ-ID 前綴仍是舊的 REQ-2、與所屬 requirement block 的 ID（REQ-7）不一致，13.C 對此另記一筆違規；13.E 的 requirement 數（3=3）與各位置 scenario 數（2,4,2）雙邊一致，無計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-05

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 的 ADDED REQ-6 Token refresh 底下兩個 scenario 標題都寫成 REQ-6-S1（valid refresh token 與 expired refresh token 兩者同用 S1，沒有 S2）。13.C 規定同一 requirement block 內兩個 scenario 標題不可共用同一 local ID，記為 VIOLATION（重複的 scenario ID）；13.E 的 requirement 數（4=4）與各位置 scenario 數（2,2,4,2）雙邊一致（CLI 只計數量、不驗證 ID 是否重複），無計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-06

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md（固定 15 分鐘時效）與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 的 ADDED 項標題為 Requirement: REQ-2 Token lifetime，但 main spec 已經有一個 ID 為 REQ-2 的既有 requirement（Token expiry）。13.D.1 規定 ADDED 項若帶有 main spec 已持有的 ID 記為 VIOLATION（新契約冒用既有身分）；candidate 狀態下同一檔案出現兩個共用 local ID REQ-2 的 requirement block，13.C 亦另記一筆重複 ID 違規（同一底層事實，兩條規則各自命中，一併記錄為 VIOLATION）；13.E 的 requirement 數（4=4）與各位置 scenario 數（2,2,4,1）雙邊一致，無計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-07

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: PASS — Archive preview 成功；delta 的 MODIFIED REQ-2（沿用既有 ID、僅改寫描述並新增 scenario REQ-2-S3，其編號大於既有最大值 S2，符合分配規則）與 ADDED REQ-6（數值 ID，大於目前最大既有數值 ID REQ-5，符合分配規則）皆合法，candidate 狀態下所有標題語法正確、ID 唯一、scenario 前綴與所屬 requirement 一致；13.E 的 requirement 數（4=4）與各位置 scenario 數（2,3,4,2）雙邊一致，13.C 與 13.D 均未發現任何問題，preview 成功、無 undeterminable 項

FINAL: PASS

## case-08

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 的 ADDED 標題為 Requirement: REQ-FOO Token refresh，ID REQ-FOO 雖符合 REQ-[A-Z0-9]+ 的一般 heading grammar，但 13.D.3 明文規定新配發的 requirement ID 必須是數值形式 REQ-n，REQ-FOO 不是數值，記為 VIOLATION（即使該標題本身語法合法）；13.E 的 requirement 數（4=4）與各位置 scenario 數（2,2,4,2）雙邊一致，無計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-09

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 記錄為需sync 狀態（session-policy、token-auth 兩個 delta 皆未同步），非阻斷
4: PASS — design.md（每個 requirement 被改名並賦予 ID，同時以 numbered scenario 全文改寫）與 specs 內容一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: PASS — Archive preview 成功；token-auth 與 session-policy 的 main spec 目前皆為未編號標題（Requirement: Token issuance 等，scenario 亦無 ID）。delta 對 token-auth 做兩組 RENAMED（FROM 無 ID 到 TO REQ-1/REQ-2，屬 13.D.2 明文允許的遷移例外）、並隨附 MODIFIED 把內容改寫為帶編號版本；因目前 main spec 無任何數值 ID、也無任何有 ID 的 scenario，current 集合為空，新配發的 REQ-1、REQ-2 與其 scenario S1/S2 依規則current 集合為空時任何正整數都合法全部滿足。session-policy 的 MODIFIED（REQ-PB，同 ID 沿用，新 scenario S1/S2 亦落在空集合規則內）亦合法。Candidate 狀態下兩個 capability 的所有標題語法正確、ID 唯一、scenario 前綴與所屬 requirement 一致；13.E 兩個 capability 的 requirement 數與各位置 scenario 數雙邊皆一致（token-auth 2=2、[2,2]；session-policy 1=1、[2]），13.C/13.D 均未發現問題，無 undeterminable 項

FINAL: PASS

## case-10

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md（到期臨界瞬間算過期）與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 的 MODIFIED REQ-2 內文本身內嵌一段 fenced code block，裡面有一行合法形狀的 Scenario: REQ-2-S9 example quoted heading。依 13.A，這種行即便在 fence 內也要被算入文字計數，但 CLI 不算。結果：change-level 半段——文字數出該 MODIFIED 項下有 4 個 scenario 標題（S9,S1,S2,S3），而 openspec show change --json --deltas-only 回報該項 requirement.scenarios.length 為 3；requirement 項目數本身一致（1=1），故此為單純的 scenario 數不一致，記為 VIOLATION。candidate-state 半段——同樣的內容併入 main spec 後，文字計數 REQ-2 底下仍是 4 個 scenario 標題，CLI 的 requirements[1].scenarios.length 仍是 3，requirement 總數雙邊一致（3=3），scenario 數在該位置不一致，另一筆 VIOLATION。兩處皆屬數量一致、位置計數不一致情形，依規則直接記 VIOLATION，不產生 undeterminable

FINAL: BLOCK | categories=VIOLATION

## case-11

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 的 ADDED 標題為 Requirement: REQ-FOO Token refresh，與 case-08 相同情形：ID 符合一般 heading grammar，但 13.D.3 要求新配發 ID 必須是數值形式，REQ-FOO 非數值，記為 VIOLATION；13.E 的 requirement 數（4=4）與各位置 scenario 數（2,2,4,2）雙邊一致，無計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-12

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md（缺 scope 回 403）與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — 在暫存複本上執行 openspec archive update-token-auth -y 時，CLI 輸出 token-auth MODIFIED failed for header Requirement: REQ-7 Token scope - not found 並印出 Aborted. No files were changed.；複本內 openspec/changes/update-token-auth/ 仍存在、openspec/changes/archive/2026-09-30-update-token-auth/ 未產生，三個成功條件不全部成立，Archive preview 判定為 FAILED（exit code 本身為 0，但 0 並不代表成功，對應規則書明文提示的已知情形）。依 13.B PREVIEW FAILED 規則，13.C 與 13.E 的 candidate-state 半段記為 UNDETERMINABLE、不視為通過；13.D 就目前狀態評估：該 MODIFIED 項的 ID REQ-7 在目前 main spec 中不存在，依 13.D.1 的解析順序它不解析到任何 main-spec requirement，規則明文此情形不算本規則的一個 finding（正是 13.B 所指、造成 preview 失敗的原因）；change-level 半段的 13.E（比對 openspec show change --json --deltas-only）：文字數出的 1 個 MODIFIED 項、1 個 scenario，與 CLI 回報的 1 個 MODIFIED delta、requirement.scenarios.length 為1 一致，無不一致。因此本檢查僅記錄一筆 UNDETERMINABLE（preview 失敗本身），未產生 VIOLATION

FINAL: BLOCK | categories=UNDETERMINABLE

## case-13

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態（session-policy、token-auth 皆未同步），非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；token-auth 的 main spec 同 case-09，現況為未編號標題。delta 做兩組 RENAMED（FROM 無 ID，屬遷移例外）：第一組 TO REQ-1（數值，current 集合為空，合法）；第二組 TO REQ-FOO（非數值）。13.D.2 的遷移例外只豁免 FROM/TO 是否要同一 ID 的要求，新配發的 TO ID 仍要受 13.D.3 新 ID 必須是數值 REQ-n 規範，REQ-FOO 不符，記為 VIOLATION。session-policy 的 MODIFIED（REQ-PB，同 case-09 的空集合分配情形）合法，無問題。Candidate 狀態下其餘標題語法正確、ID 唯一；13.E 兩個 capability 的 requirement 數（token-auth 2=2、session-policy 1=1）與各位置 scenario 數（[2,2]、[2]）雙邊一致，無計數不一致，無 undeterminable 項

FINAL: BLOCK | categories=VIOLATION

## case-14

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；本案例的 main spec 在 delta 完全未觸及的位置，既有一個未編號的 requirement Token audience（其下 scenario wrong audience 亦未編號），此區塊原樣進入 candidate 狀態。13.C 規定 candidate 狀態下每一個 requirement／scenario 標題都要檢查合法性，不論是否被本次變更觸及；Token audience（無 ID）與其 scenario wrong audience（無 ID）皆不符合 heading grammar，記為兩筆 VIOLATION（一個 requirement、一個 scenario，標題本身皆缺 ID）。delta 本身新增的 ADDED REQ-6 部分語法合法、ID 數值遞增合規，無額外問題。13.E 的 requirement 數（5=5）與各位置 scenario 數（2,2,1,4,2）雙邊一致，無計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-15

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 在同一個 delta 檔案的 ADDED 區段裡出現兩個各自獨立的 requirement block，標題分別是 Requirement: REQ-6 Token refresh 與 Requirement: REQ-6 Token introspection，兩者共用同一 local ID REQ-6。13.D.1 明文規定同一個 delta 檔案內兩個 ADDED 項共用同一 ID 記為 VIOLATION；13.C 對 candidate 狀態下同檔案出現兩個共用 local ID 的 requirement block 亦另記一筆重複 ID 違規（同一底層事實，一併記為 VIOLATION）。13.E 的 requirement 數（5=5）與各位置 scenario 數（2,2,4,1,1）雙邊一致，無計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-16

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 的 MODIFIED REQ-2 底下新增第三個 scenario，標題寫成 Scenario: token at the expiry instant，完全沒有 REQ-ID-Sm 形式的 ID。這是一個新增（相對於 main spec 目前 REQ-2 底下只有 S1、S2）且不帶合法 ID 的 scenario 標題，13.C（scenario 標題不符 grammar）與 13.D.3（新 scenario 標題必須帶編號、這裡完全沒有）都命中，記為同一筆 VIOLATION（引用兩條規則）。13.E 的 requirement 數（3=3）與各位置 scenario 數（2,3,4）雙邊一致（CLI 仍把它算成一個 scenario 條目，只是不驗證其 ID 格式），無計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-17

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 記錄為需sync 狀態（僅 session-policy 有 delta），非阻斷
4: PASS — design.md（絕對 timeout 與 idle timeout 互補）與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: PASS — Archive preview 成功；本案例只對 session-policy 提出 delta（ADDED REQ-4 Session absolute timeout，scenario REQ-4-S1），token-auth 完全未被觸及。session-policy 目前 main spec 唯一既有 ID 是 REQ-PB（非數值形式，不計入目前數值 ID 最大值），因此目前數值 ID 集合為空，新配發的 REQ-4（數值）在此規則下任何正整數皆合法，scenario S1 亦然。標題語法正確、ID 唯一，candidate 狀態下 session-policy（REQ-PB + REQ-4）與未觸及的 token-auth（乾淨 baseline）均未發現問題。13.E 兩個 capability 的 requirement 數（session-policy 2=2、token-auth 3=3）與各位置 scenario 數皆雙邊一致，無 undeterminable 項

FINAL: PASS

## case-18

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 的 ADDED REQ-6 Token refresh 底下第二個 scenario 標題寫成 Scenario: REQ-5-S5 expired refresh token，其 REQ-ID 前綴是 REQ-5，但它實際所屬的 requirement block 是 REQ-6。13.C 規定 scenario 標題的 REQ-ID 必須恰好等於其所屬 requirement block 的 ID，即便 REQ-5 這個 ID 確實存在於這個 capability 的別處，仍算違規，記為 VIOLATION。13.E 的 requirement 數（4=4）與各位置 scenario 數（2,2,4,2）雙邊一致（CLI 僅計數量，不驗證前綴是否對應），無計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-19

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；main spec 現有 REQ-5 區塊內嵌一段 fenced code block，裡面有一行合法形狀的 Requirement: REQ-9 Example quoted heading。依 13.A，此行即便在 fence 內也要被算入文字計數（且因語法完整、ID 唯一，13.C 本身不會單獨挑出它作為違規）。文字計數下 candidate 狀態的 requirement 標題總數為 5（REQ-1、REQ-2、REQ-5、fenced 的 REQ-9、delta 新增的 REQ-10），而 CLI requirementCount 回報 4（不計 fenced 行）。Requirement 數本身就不一致，13.E 記一筆 VIOLATION（具名雙邊數值：文字 5、CLI 4）；因為這個數量不一致，依規則仰賴此計數的比對全部改記 UNDETERMINABLE——本案例中即是每個 requirement 的 scenario 數逐位比對，因文字順序（含 fenced 的 REQ-9）與 CLI 陣列順序在 REQ-5 之後即無法可靠對齊，故該檔案的位置配對整體記為 UNDETERMINABLE，不得臆測配對。change-level 半段（deltas-only，delta 本身只有乾淨的 ADDED REQ-10，無 fence）文字與 CLI 一致，無額外問題。13.D.3 對新配發的 REQ-10：因 fenced 的 REQ-9 依 13.A 定義也算入目前 main spec 內的數值 ID，目前最大值視為 9，REQ-10 大於 9 依此規則本身合規，不算違規

FINAL: BLOCK | categories=VIOLATION,UNDETERMINABLE

## case-20

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: BLOCK — Archive preview 成功；delta 的 ADDED 標題為 Requirement: REQ-3 Token refresh，main spec 目前最大既有數值 ID 為 REQ-5。13.D.3 規定新配發的數值 ID 必須大於目前該 capability main spec 中每一個既有數值 ID，REQ-3 並未大於 REQ-5（即使目前不存在 REQ-3 本身，規則書明文以 REQ-9 為現有最大值時 ADDED REQ-4 仍算違規為例，情形完全類推），記為 VIOLATION。13.E 的 requirement 數（4=4）與各位置 scenario 數（2,2,4,2）雙邊一致，無計數不一致

FINAL: BLOCK | categories=VIOLATION

## case-21

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: PASS — Archive preview 成功；delta 為單純的 ADDED REQ-6 Token refresh（scenario REQ-6-S1、REQ-6-S2，前綴與所屬 requirement 一致），main spec 為乾淨 baseline（REQ-1、REQ-2、REQ-5，無重複、無缺 ID、無 fenced 干擾行）。REQ-6 為數值 ID，大於目前最大既有數值 ID REQ-5，符合 13.D.3 分配規則；新 scenario S1、S2 屬於全新 requirement 之下，current 集合為空，任何正整數皆合法。Candidate 狀態下所有標題語法正確、ID 唯一，13.C/13.D 皆未發現問題。13.E 的 requirement 數（4=4）與各位置 scenario 數（2,2,4,2）雙邊一致，無 undeterminable 項

FINAL: PASS

## case-22

PRECHECK: NOT_APPLICABLE — 判定依賴 git commit history
1: PASS — 三項 valid:true
2: PASS — 任務 1.1 為 - [x]
3: PASS — 需sync 狀態，非阻斷
4: PASS — design.md 與 specs 一致
5: NOT_APPLICABLE — working-tree 狀態
6: PASS — 無 leak 目錄
7: PASS — 無 deferred 任務
8: PASS — TDD 標記合法
9: PASS — n/a 任務無需記錄
10: PASS — vacuous
11: PASS — vacuous
12: PASS — 1.1 對應一致
13: PASS — Archive preview 成功；delta 為 RENAMED，FROM Requirement: REQ-2 Token expiry（ID=REQ-2）TO Requirement: REQ-2 Access token expiry（ID=REQ-2，僅描述文字改變、ID 不變）。13.D.2 規定的規則本身即以 REQ-3 Token expiry 到 REQ-3 Access token expiry 為合法範例，本案例完全對應，屬合法 rename；其下 scenario 標題（REQ-2-S1、REQ-2-S2）維持不變、前綴與所屬 requirement 的 ID 一致，不受影響。Candidate 狀態下所有標題語法正確、ID 唯一；13.E 的 requirement 數（3=3）與各位置 scenario 數（2,4,2）雙邊一致，13.C/13.D 皆未發現問題，無 undeterminable 項

FINAL: PASS
