## case-01

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — ADDED 的 REQ-2 Token lifetime 與主 spec 既有 REQ-2 Token expiry 同名 ID：屬「ADDED 使用既有 ID」(13.D.1)，候選檔案中亦形成兩個同 local ID 的 requirement block(13.C)，兩條規則命中同一缺陷。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-02

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — MODIFIED 新增的 scenario「token at the expiry instant」沒有合法 ID，不符合 heading grammar；同時是 13.C(不合語法的 scenario heading)與 13.D.3(新 scenario 缺合法 ID)命中的同一發現，一併引用兩條規則。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-03

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — 同一個 REQ-6 requirement block 下兩個 scenario 都寫成 local ID `REQ-6-S1`，違反 13.C「同一 requirement block 內 scenario local ID 不得重複」。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-04

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: PASS — ADDED REQ-6(數值 6 大於主 spec 現有最大數值 REQ-5)、scenario S1/S2 各自合法且不重複；候選狀態與 CLI 的 requirement/scenario 計數一致，未見任何 13.C/13.D/13.E 發現。

FINAL: PASS categories={}

## case-05

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — REQ-6 requirement block 下第二個 scenario 寫成 `REQ-5-S5`，其 <REQ-ID> 與所屬 requirement 的 ID(REQ-6)不符，違反 13.C 的「scenario 的 REQ-ID 須與所屬 requirement 完全一致」規則。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-06

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — 候選 main spec 內既有、此 delta 未觸及的「Token audience」requirement 標題沒有合法 ID；13.C 對候選整份檔案逐條檢查，不因未被此變更觸及而略過，因此命中。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-07

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: PASS — ADDED REQ-6(6>5)與 MODIFIED REQ-2 新增 scenario REQ-2-S3(大於現有最大 S2)皆合乎配置規則；候選/CLI 計數一致，未見發現。

FINAL: PASS categories={}

## case-08

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — 候選檔案中主 spec 既有(此 delta 未觸及)的兩個 requirement block「REQ-2 Token expiry」與「REQ-2 Token lifetime」共用同一 local ID REQ-2，13.C 判定為重複；此為既存缺陷，經候選合併後仍需依全檔規則檢查而命中。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-09

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — 候選檔案中以 fenced code block 引用的「### Requirement: REQ-9 Example quoted heading」在本檢查逐行文字計數下仍算一個 requirement heading，使候選 requirement 計數(文字 5)與 CLI `requirementCount`(4)不一致 → 依 13.E 判定為 VIOLATION；計數不一致後，該檔案所有依賴此計數配對的 scenario 數比對依規則一律記為 UNDETERMINABLE，不得猜測配對。
BLOCK 類別: 違规, 無法判定

FINAL: BLOCK categories={違规, 無法判定}

## case-10

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — ADDED 的新 requirement ID `REQ-FOO` 不是數值形式(REQ-<n>)，違反 13.D.3「新配發 ID 必須為數值」；proposal.md 內「識別碼檢查可略過」的說明依 13.F 對本檢查沒有任何效力，已忽略並照常完整執行本檢查。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-11

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — 與 case-10 相同的 ADDED `REQ-FOO`(非數值形式)違反 13.D.3「新配發 ID 必須為數值」。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-12

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — MODIFIED 指向主 spec 中不存在的「REQ-7 Token scope」；依 13.B 規定以 ARCHIVE PREVIEW 實測(於暫存複本執行 `openspec archive update-token-auth -y`)，結果為 exit 0 但輸出「not found」、變更資料夾未被移除、archive/ 未產生對應新目錄 → PREVIEW FAILED，記為 UNDETERMINABLE；13.D 對此「不解析」的 MODIFIED 條目本身不構成該規則的發現，change-level 13.E 的文字/CLI 計數比對一致、未見不符。
BLOCK 類別: 無法判定

FINAL: BLOCK categories={無法判定}

## case-13

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：session-policy 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: PASS — 本案例僅觸及 session-policy：ADDED REQ-4 為新 ID，主 spec 目前數值 ID 集合為空(REQ-PB 非數值)，依規則空集合下任何正整數皆合格；候選與 CLI 計數一致，未見發現(archive/ 中曾出現又被移除的舊識別碼不影響本檢查，規則明訂本檢查不讀 archive 歷史)。

FINAL: PASS categories={}

## case-14

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：session-policy 與 token-auth 皆記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: PASS — 兩個 RENAMED pair 的 FROM 標題皆無 ID(屬遷移)，TO ID 為 REQ-1/REQ-2；主 spec 當前(該能力)數值 ID 集合為空，任何正整數皆合格；對應的 MODIFIED 條目透過與 TO 標題完全比對解析回 FROM 需求，合乎 13.D.1(a)；候選與 CLI 計數一致，未見發現。

FINAL: PASS categories={}

## case-15

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — 同一 delta 檔案內兩個 ADDED requirement 都使用 local ID `REQ-6`，違反 13.D.1「兩個 ADDED entry 同 ID」，候選檔案中亦形成兩個同 local ID 的 requirement block，同時違反 13.C。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-16

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — delta 與候選檔案中，REQ-2 底下以 fenced code block 引用的「#### Scenario: REQ-2-S9 example quoted heading」在本檢查逐行文字計數下仍算一個 scenario heading，造成 change-level(文字 4 vs CLI MODIFIED scenarios=3)與候選狀態(同一位置文字 4 vs CLI 3)兩處計數不一致，依 13.E 判定為 VIOLATION(分別記錄)。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-17

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: PASS — RENAMED 的 FROM/TO 皆帶 ID REQ-2(僅改描述文字為「Access token expiry」)，ID 未變，合乎 13.D.2 允許的重新命名；候選中對應 scenario 仍標記 REQ-2-S1/S2，與所屬 requirement ID 一致；計數與 CLI 一致，未見發現。

FINAL: PASS categories={}

## case-18

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — ADDED 的「### Requirement: REQ-6」標題後方沒有描述文字，不符合 heading grammar(視為「ID 後無內容」，等同無合法 ID)，同時違反 13.C(候選中不合語法的 requirement heading)與 13.D.3(新 requirement 須帶合法 ID)。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-19

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：session-policy 與 token-auth 皆記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — 第二個 RENAMED pair 的 FROM 標題無 ID(屬遷移)，但其 TO ID 被配發為 `REQ-FOO`，不是數值形式，違反 13.D.3 的新配發 ID 規則。
BLOCK 類別: 違规

FINAL: PASS categories={}

## case-20

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — ADDED 的 REQ-3 是數值形式，但小於主 spec 目前(該能力)最大數值 ID(REQ-5)，違反 13.D.3「新 ID 必須大於當前最大數值 ID」。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-21

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — RENAMED 把 FROM 的 ID(REQ-2)改成 TO 的 ID(REQ-7)，違反 13.D.2「重新命名不得更換 ID」；候選檔案中該 requirement 底下兩個 scenario 仍標記 REQ-2-S1/REQ-2-S2，與新的 parent ID(REQ-7)不符，另各自違反 13.C 的「scenario 的 REQ-ID 須與所屬 requirement 一致」規則(兩筆各記一次)。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

## case-22

PRECHECK: 不適用於 fixture — 判定依據為 `git log`/`git merge-base` 所反映的 repository 歷史(commit 範圍)，案例目錄的 git 狀態不代表其所測試的狀態。
1: PASS — 於此案例目錄執行 `openspec validate --all --json`，所有項目(session-policy、token-auth、update-token-auth)皆回報 valid:true。
2: PASS — tasks.md 中唯一的任務 1.1 標記為 `- [x]`。
3: PASS — 已比對 delta 與主 spec：token-auth 記錄為「✗ Needs sync」(主 spec 尚未套用此 delta 的內容)。
4: PASS — design.md 的 Context/Decisions 與此變更的 spec delta 內容相符，未見明顯偏離(spot check)。
5: 不適用於 fixture — 此檢查的判定依據是 repository 目前的 git 工作樹/commit 狀態(是否有 unstaged 檔案)，案例目錄沒有可反映該狀態的 git 歷史。
6: PASS — 案例目錄下不存在 `docs/superpowers/specs/*.md`，無 front-door 洩漏。
7: PASS — tasks.md 沒有任何 `- [~]` deferred 任務，§7 留空合乎規則(沒有 deferred 任務即無需列項)。
8: PASS — 任務 1.1 唯一一行 TDD 標註為 `- TDD: n/a — prose/doc-only`，格式合乎規則(分隔符與非空 reason 皆具備)。
9: PASS — 該任務標註為 `TDD: n/a`，不欠任何 RED/GREEN 記錄，也未見多餘記錄，vacuously 通過。
10: PASS — 沒有任何 RED/GREEN 記錄可供檢查，vacuously 通過。
11: PASS — 沒有 RED/GREEN 記錄需要配對，vacuously 通過。
12: PASS — tasks.md 任務編號集合 {1.1} 與 plan.md entry key 集合 {1.1} 皆各自唯一且雙向相等。
13: BLOCK — 候選檔案中主 spec 既有、此 delta 未觸及的 REQ-2 底下以 fenced code block 引用的「#### Scenario: REQ-2-S9 example quoted heading」在逐行文字計數下仍算一個 scenario heading，使該 requirement 位置的候選文字計數(3)與 CLI(2)不一致，依 13.E 判定為 VIOLATION；此為既存缺陷，經候選合併後仍依全檔規則檢查而命中。
BLOCK 類別: 違规

FINAL: BLOCK categories={違规}

