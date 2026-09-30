## case-01

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對(git merge-base/origin),案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 對本案例所有 item 回傳 valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync),檢查本身可完整判定
4: PASS — design.md 的 Context/Decisions 與本案例 spec delta 主題一致,未見明顯偏離
5: 不適用於 fixture — 判定依據為 worktree 是否有未提交變更與 commit range,案例目錄無有意義的 git 狀態
6: PASS — docs/superpowers/specs/*.md 不存在,無 front-door routing leak
7: PASS — tasks.md 沒有任何 [~] deferred task
8: PASS — task 1.1 恰有一行 TDD: n/a - prose/doc-only,格式合法、reason 非空
9: PASS — 唯一任務標註 TDD: n/a,不需亦未夾帶 RED/GREEN 記錄
10: PASS — 沒有任何 RED/GREEN record,outcome 規則無適用對象(vacuously satisfied)
11: PASS — 沒有 TDD: applicable 任務,無需配對 subject(vacuously satisfied)
12: PASS — tasks.md 任務號 {1.1} 與 plan.md entry key {1.1} 一一對應,雙邊皆無重複
13: BLOCK — 13.D.1:ADDED 的 REQ-2 Token lifetime 沿用 main spec 已有的 REQ-2(Token expiry)識別碼,是新契約冒用既有身分;13.C:archive 後 candidate 檔案裡出現兩個 REQ-2 requirement block(本地 ID 重複)
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-02

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例主題(token refresh)一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD: n/a - prose/doc-only 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶 RED/GREEN 記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — 13.D.1:同一 delta 檔案內兩個 ADDED entries(Token refresh / Token introspection)都叫 REQ-6,兩個 ADDED entries 同 ID 直接違規;13.C:archive 後 candidate 檔案裡出現兩個 REQ-6 requirement block
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-03

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: PASS — ADDED REQ-6(6 大於目前最大數字 ID 5)合法且唯一,scenario REQ-6-S1/S2 對應父 ID 正確,archive preview 成功,13.E 各項計數全部一致

FINAL: PASS categories={}

## case-04

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容(expiry 邊界時刻)與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — MODIFIED REQ-2 新增的第三個 scenario「token at the expiry instant」不帶任何 ID:此 scenario 是新配置,違反 13.D.3(新 scenario 必須帶合法編號);同一標題在 candidate state 掃描下亦不符 13.C 的 grammar,依規則對同一標題只記一次但引用兩條規則
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-05

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — session-policy 與 token-auth 的 delta 均尚未併入 main spec(Needs sync)
4: PASS — design.md 說明(rename 並補上編號 scenario,文字不變)與本案例 delta 一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — 兩個 RENAMED 都是 FROM 無 ID 的 migration:第一個配到數字 ID REQ-1(合法);第二個把「Token expiry」配到新 ID REQ-FOO,不是 REQ-<n> 數字形式,違反 13.D.3 的新 ID 配置規則(即使該 ID 本身符合 heading grammar)
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-06

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: PASS — ADDED REQ-6(6>5)合法唯一;MODIFIED REQ-2 新增的 REQ-2-S3(3>目前該 requirement 下最大 2)亦合法;archive preview 成功,13.E 各項計數一致,無重複或不合法 ID

FINAL: PASS categories={}

## case-07

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致(此 spot-check 不涉及與 delta 無關的既有 audience 需求)
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — 13.C 對 candidate state 進行全檔案掃描時,main spec 裡與本次 delta 無關、既有的「Requirement: Token audience」不帶任何 ID,不符合 heading grammar;13.C 的規則不論該標題是否被本次 delta 觸碰,一律列入掃描
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-08

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — ADDED REQ-6 下第二個 scenario 標題寫成「REQ-5-S5」,其 REQ-ID(REQ-5)與所屬 requirement 的 ID(REQ-6)不一致;即使 REQ-5 在別處確實存在,13.C 明文指出這仍是違規
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-09

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — ADDED 的新 requirement 使用非數字 ID REQ-FOO,違反 13.D.3(新配置的 requirement ID 必須是 REQ-<n> 數字形式),即使該 ID 的 grammar 本身合法且不與任何既有 ID 衝突
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-10

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容(僅標題改變、內文不變)與本案例 delta 一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — RENAMED 把帶 ID 的 REQ-2 改成 REQ-7,違反 13.D.2(rename 必須保留原 ID,FROM 帶 ID 時不可換號);archive 後 candidate 內遺留的 scenario 標題仍寫 REQ-2-S1/REQ-2-S2,與所屬 requirement 的新 ID REQ-7 不一致,亦違反 13.C 的 scenario grammar
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-11

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — 本案例 delta 內容與 case-09 逐位元組相同:ADDED 的新 requirement 使用非數字 ID REQ-FOO,違反 13.D.3
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-12

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — session-policy 的 delta 尚未併入 main spec(Needs sync);本案例未觸碰 token-auth
4: PASS — design.md 內容(absolute timeout 補充 idle timeout)與本案例 delta 一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: PASS — 本案例的 delta 是 session-policy(非 token-auth);ADDED REQ-4 在 session-policy 主 spec 目前沒有任何數字 ID 的情況下(當前集合為空)允許任意正整數,合法;archive preview 成功;candidate state 對 session-policy 與未受影響的 token-auth 逐一掃描均無重複或不合法 ID

FINAL: PASS categories={}

## case-13

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — ADDED REQ-6 下兩個 scenario 標題都寫成「REQ-6-S1」,同一 requirement block 內本地 ID 重複,違反 13.C(兩個 scenario 標題共用同一 local ID)
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-14

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — main spec 的 REQ-2 body 內,一段 fenced code block 示範用的「Scenario: REQ-2-S9 example quoted heading」依 13.A 的逐行規則仍被算作真實 scenario heading(不識別 markdown 結構),導致本檢查對 REQ-2 的 scenario 計數(3)與 openspec show --json 的計數(2,CLI 正確忽略了 fence 內容)不一致;13.E 在計數不一致的情況下判定為 VIOLATION
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-15

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — session-policy 與 token-auth 的 delta 均尚未併入 main spec(Needs sync)
4: PASS — design.md 說明(rename 並補上編號 scenario,文字不變)與本案例 delta 一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: PASS — 兩個 RENAMED 都是 FROM 無 ID 的 migration,依 13.D.2 例外配置新 ID(REQ-1、REQ-2),兩者皆為數字形式且互不重複,符合 13.D.3;新配置的 scenario ID 亦全部合法;archive preview 成功,13.E 各項計數一致

FINAL: PASS categories={}

## case-16

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — main spec 內一段 fenced code block 示範文字「Requirement: REQ-9 Example quoted heading」依 13.A 逐行規則仍被算成真實 requirement heading,使本檢查對 candidate 檔案的 requirement 計數(5)與 CLI JSON 的計數(4)不一致,13.E 判定為 VIOLATION;計數不一致後,同一檔案的 scenario 逐項比對已無法可靠配對,依規則記為 UNDETERMINABLE(該 fenced 標題本身因符合 heading grammar 且唯一,13.C 未單獨判它違規)
BLOCK 類別: 違規, 無法判定

FINAL: BLOCK categories={違規, 無法判定}

## case-17

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true(CLI 的結構驗證不檢查 MODIFIED 標頭是否能在 main spec 中解析到)
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync);此判定不依賴 archive preview 是否成功
4: PASS — design.md 內容(missing scope 回應 403)與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — archive preview 失敗(token-auth MODIFIED failed for header "Requirement: REQ-7 Token scope" - not found / Aborted. No files were changed.,退出碼 0 但變更目錄未移動、archive 目錄未建立,依 13.B 判定為 PREVIEW FAILED);13.C 與 candidate 半邊的 13.E 因此未被評估,記為 UNDETERMINABLE;13.D 對這個無法解析的 MODIFIED entry 明文規定不是本規則的違規(它正是 preview 失敗的成因本身);change-level 13.E 的 entry/scenario 計數比對一致,未發現其他違規
BLOCK 類別: 無法判定

FINAL: BLOCK categories={無法判定}

## case-18

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta(僅描述文字改變)一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: PASS — RENAMED 保留原 ID(REQ-2 到 REQ-2,僅描述文字從 Token expiry 改成 Access token expiry),符合 13.D.2;candidate 內遺留的 scenario 標題(REQ-2-S1/S2)與所屬 requirement 的 ID 一致;archive preview 成功,13.E 各項計數全部一致

FINAL: PASS categories={}

## case-19

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — delta 檔案的 MODIFIED REQ-2 body 內,一段 fenced code block 示範用的「Scenario: REQ-2-S9 example quoted heading」依 13.A 逐行規則仍被算作真實 scenario heading,使 change-level(openspec show --deltas-only)與 candidate-level(openspec show --json)的 scenario 計數(本檢查算出 4)都與 CLI 的計數(3,正確忽略 fence 內容)不一致,兩處都被 13.E 判定為 VIOLATION
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-20

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — ADDED 的 requirement 標題只寫「Requirement: REQ-6」,ID 後面沒有任何描述文字,不符合 heading grammar(視為沒有合法 ID);此標題同時違反 13.C(grammar 檢查)與 13.D.3(新 requirement 必須帶合法 ID),依規則對同一標題只記一次但引用兩條規則
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-21

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — ADDED 的新 requirement 使用數字 ID REQ-3,但目前 main spec 已有的最大數字 ID 是 5,REQ-3 不大於目前最大值,違反 13.D.3 的新配置規則(即使 REQ-3 本身未與任何既有 ID 衝突)
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}

## case-22

PRECHECK: 不適用於 fixture — 判定依據為 git commit log 與 branch 比對,案例目錄的 git 歷史不具意義
1: PASS — openspec validate --all --json 全部 item valid:true
2: PASS — tasks.md 僅任務 1.1,checkbox 為 - [x]
3: PASS — token-auth 的 delta 尚未併入 main spec(Needs sync)
4: PASS — design.md 內容與本案例 delta 主題一致
5: 不適用於 fixture — 判定依據為 worktree 未提交變更與 commit range
6: PASS — 無 front-door routing leak
7: PASS — 無 [~] deferred task
8: PASS — task 1.1 的 TDD annotation 格式合法
9: PASS — 唯一任務為 TDD: n/a,未夾帶記錄
10: PASS — 無記錄可判定(vacuously satisfied)
11: PASS — 無 TDD: applicable 任務(vacuously satisfied)
12: PASS — tasks.md {1.1} 與 plan.md {1.1} 一一對應
13: BLOCK — main spec 本身已存在兩個 requirement block 共用本地 ID REQ-2(Token expiry / Token lifetime),這是既有缺陷,與本次 delta(乾淨地新增 REQ-6,未觸碰 REQ-2)無關,但 13.C 對 candidate state 的全檔案掃描仍會抓出這個重複
BLOCK 類別: 違規

FINAL: BLOCK categories={違規}
