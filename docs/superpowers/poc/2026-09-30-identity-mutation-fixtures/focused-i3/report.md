## case-01

PRECHECK: NOT_APPLICABLE — 此檢查其中一個必要條件（commit evidence 的 `git log ... | wc -l`）判定依據是 repository 的 commit 歷史，案例子目錄不具備有意義的 git 狀態
1: PASS — `openspec validate --all --json` 對 session-policy、token-auth 兩個 spec 與 update-token-auth 這個 change 都回傳 `"valid": true`
2: PASS — tasks.md 唯一一條任務 1.1 的 checkbox 是 `- [x]`，不是 `- [ ]`
3: PASS — 逐一比對兩個 delta 目錄與對應主 spec：session-policy 的 ADDED REQ-1 內容與主 spec 既有的 REQ-1 Session absolute lifetime（含同一條 scenario REQ-1-S1）逐字相同 → 記為「✓ Already synced」；token-auth 的 ADDED REQ-3 Token refresh 在主 spec（REQ-1/REQ-2/REQ-5）中不存在 → 記為「✗ Needs sync」；兩者皆有明確、可記錄的結論
4: PASS — design.md 的決策（維持 proposal 所述的 spec delta）與 specs/ 的內容沒有看出牴觸或漂移
5: NOT_APPLICABLE — 此檢查判定依據是 repository 的 working-tree 狀態（是否有未提交變更）
6: PASS — `ls docs/superpowers/specs/*.md` 在案例目錄下找不到任何檔案，沒有 front-door routing leak
7: PASS — tasks.md 僅有一條任務且 checkbox 是 `[x]`，沒有任何 `- [~]` deferred task，§7 不需要列任何列、也沒有「§7 空但存在 deferred task」的 BLOCK 條件成立
8: PASS — 任務 1.1 底下恰有一行 `- TDD: n/a — prose/doc-only`，分隔符是合法的 em dash，`n/a` 後面的理由非空
9: PASS — 該任務標註 `TDD: n/a`，不要求 RED/GREEN 記錄；實際上也沒有任何 RED/GREEN 記錄，檢查對它不適用、沒有缺陷
10: PASS — 沒有任何 RED/GREEN 記錄存在，outcome 標記檢查在此案例中沒有對象可檢查，沒有發現任何不合規記錄
11: PASS — 沒有任何標註 `TDD: applicable` 的任務，配對規則沒有對象可檢查，沒有發現任何不合規
12: PASS — tasks.md 的任務編號集合 {1.1} 與 plan.md 的 entry key 集合 {1.1}（`## 1.1 — Update the spec delta described in the proposal`）在兩側皆無重複、且兩個集合互相相等
13: BLOCK — 實際執行 archive preview（複本 + `openspec archive update-token-auth -y`）：指令以 exit 0 結束，但輸出 `session-policy ADDED failed for header "### Requirement: REQ-1 Session absolute lifetime" - already exists` 與 `Aborted. No files were changed.`，複本裡的 change 目錄仍存在、`archive/` 目錄未產生 → PREVIEW FAILED，13.C 與 13.E 的 candidate-state 半邊對兩個 capability 都記為 UNDETERMINABLE；session-policy 經 check 3 記為已同步，其 13.D 讀主 spec 的判斷（ADDED 是否已持有該 ID、新 ID 配置的目前最大值）記為 UNDETERMINABLE（required pre-sync state unavailable），僅從 delta 本身可判的 heading grammar 部分正常執行且沒有違規；token-auth 未同步，13.D 全面執行：主 spec 目前最大數字 ID 為 REQ-5（REQ-1、REQ-2、REQ-5），新配置的 ADDED REQ-3 並未大於 5 → 違反 13.D.3 的配置規則，記為 VIOLATION；13.E 的 change-level 半邊（`openspec show update-token-auth --json --deltas-only`）文字計數與 JSON 計數一致（兩個 capability 各 1 筆 ADDED、scenario 數 1 與 2 皆吻合），這部分沒有發現落差

FINAL: BLOCK | categories=VIOLATION,UNDETERMINABLE

## case-02

PRECHECK: NOT_APPLICABLE — 此檢查其中一個必要條件（commit evidence 的 `git log ... | wc -l`）判定依據是 repository 的 commit 歷史，案例子目錄不具備有意義的 git 狀態
1: PASS — `openspec validate --all --json` 對 session-policy、token-auth 兩個 spec 與 update-token-auth 這個 change 都回傳 `"valid": true`
2: PASS — tasks.md 唯一一條任務 1.1 的 checkbox 是 `- [x]`，不是 `- [ ]`
3: PASS — session-policy 的 ADDED REQ-1 內容與主 spec 既有的 REQ-1 Session absolute lifetime（含同一條 scenario REQ-1-S1）逐字相同 → 記為「✓ Already synced」；token-auth 的 ADDED REQ-6 Token refresh 在主 spec（REQ-1/REQ-2/REQ-5）中不存在 → 記為「✗ Needs sync」；兩者皆有明確、可記錄的結論
4: PASS — design.md 的決策與 specs/ 的內容沒有看出牴觸或漂移
5: NOT_APPLICABLE — 此檢查判定依據是 repository 的 working-tree 狀態（是否有未提交變更）
6: PASS — `ls docs/superpowers/specs/*.md` 在案例目錄下找不到任何檔案，沒有 front-door routing leak
7: PASS — tasks.md 僅有一條任務且 checkbox 是 `[x]`，沒有任何 `- [~]` deferred task，沒有「§7 空但存在 deferred task」的 BLOCK 條件成立
8: PASS — 任務 1.1 底下恰有一行 `- TDD: n/a — prose/doc-only`，分隔符是合法的 em dash，`n/a` 後面的理由非空
9: PASS — 該任務標註 `TDD: n/a`，不要求 RED/GREEN 記錄；實際上也沒有任何 RED/GREEN 記錄
10: PASS — 沒有任何 RED/GREEN 記錄存在，outcome 標記檢查在此案例中沒有對象可檢查
11: PASS — 沒有任何標註 `TDD: applicable` 的任務，配對規則沒有對象可檢查
12: PASS — tasks.md 的任務編號集合 {1.1} 與 plan.md 的 entry key 集合 {1.1} 在兩側皆無重複、且兩個集合互相相等
13: BLOCK — 實際執行 archive preview（複本 + `openspec archive update-token-auth -y`）：指令以 exit 0 結束，輸出與 case-01 相同的 `session-policy ADDED failed for header "### Requirement: REQ-1 Session absolute lifetime" - already exists` 與 `Aborted. No files were changed.`，複本裡的 change 目錄仍存在、`archive/` 目錄未產生 → PREVIEW FAILED，13.C 與 13.E 的 candidate-state 半邊對兩個 capability 都記為 UNDETERMINABLE；session-policy 經 check 3 記為已同步，其 13.D 讀主 spec 的判斷記為 UNDETERMINABLE（required pre-sync state unavailable），僅 heading grammar 部分正常執行且無違規；token-auth 未同步，13.D 全面執行：主 spec 目前最大數字 ID 為 REQ-5，新配置的 ADDED REQ-6 大於 5，符合 13.D.3 的配置規則，沒有發現違規；13.E 的 change-level 半邊文字計數與 JSON 計數一致（兩個 capability 各 1 筆 ADDED、scenario 數 1 與 2 皆吻合），這部分沒有發現落差；本案例在 13.C/13.D/13.E 中沒有任何 VIOLATION，但 preview 失敗本身與 session-policy 的已同步狀態使部分判斷無法可靠完成，故整體仍 BLOCK（check 13 只有在 preview 成功且所有比對完成一致、13.C/13.D 均無發現時才算 PASS）

FINAL: BLOCK | categories=UNDETERMINABLE
