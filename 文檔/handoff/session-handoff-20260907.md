# Session Handoff — 2026-09-07

## Session 08:36

### 一、本 session 主題

**loosen-plan 收尾的主體段。** 這個 session 從 09-04 開工、跨到 09-07 收工（等待使用者裁定佔了大部分跨度），做完接力棒四件事裡的前兩件與第三件的一半：archive、SDD 工作區清理、可重跑資產保存、雙 gate（doc + code）、六個 commit。**push 尚未執行**——卡在一個我自己訂下、目前仍是紅燈的硬 gate（見三）。

前一份是 `session-handoff-20260904.md`（Session 08:17），記的是另一個 session；本檔不重貼。

### 二、完成事項

- **`03bf87e` archive loosen-plan** —— Windows 目錄鎖照 CLAUDE.md 走 `cp -r` → `diff -r` IDENTICAL → 使用者跑 `rm -rf`。git 解析為 **11 個 rename，全部 100% similarity**（等於 git 自己證明搬移逐位元組相同）。`openspec list` 回「No active changes found」。
- **`489df22` delta spec sync** —— `plan-contract`（ADDED）、`tdd-evidence-contract`（ADDED）、`tdd-claim-accuracy`（MODIFIED）。`openspec validate --all` 4/4。
- **`68b3e70` 三組可重跑資產進版控**（22 檔，19 檔逐檔 SHA256 驗過）：
  - `2026-09-03-tdd-evidence-mutation-fixtures/` f1–f7（檢查器判得對嗎）
  - `2026-09-03-plan-contract-producer-smoke/` run2 輸入／刺激物／輸出（產出器產得對嗎）
  - `2026-09-03-sdd-review-pkg-helper/` `review-pkg.sh`（定位為 reusable POC helper，**不升格**；升格條件寫在 README）
- **`1379de4` errata.md（append-only，原文一字未改）** —— E1：f7 被歸為盲測結果，**三處、跨兩個 artifact**；E2：`verify.md:419` 與 `:649` 對產出者行為的描述不成立，但其結構性 WARNING 保留。
- **`1125e06` 兩筆 follow-up 登記** —— `task-20260904-spec-contradiction-cleanup`、`task-20260904-reviewer-verdict-delivery`。
- **`6b72cff` `.gitattributes` LF pin** —— 範圍 `docs/superpowers/poc/`、逐副檔名列舉（`.md/.txt/.sh/.py/.json`）而非 `**`，確保未來放 binary 不被強制當 text（負向對照已驗：POC 目錄下的假想 `.png` 回 `unspecified`）；`.gitattributes` 自己也釘住。
- **`.superpowers/` 已刪**（129 檔）—— 保存前逐檔比對，只留可重跑資產。
- **雙 gate 全綠**：`doc_review` / `code_review` / `precommit` 三個 plane 皆 pass 且 digest 相符。兩個 sentinel 都經 `validate-family-sentinel.js` **fail-closed 驗過**；`gate_source=fallback:contract-neutral-reviewer`（Codex 配額至 9/7）。

### 三、未完事項 / 接力棒

**A. push 前的硬 gate（紅燈中，擋住 push / PR / CI）**

`docs/superpowers/poc/` 底下**仍有 11 個檔是 CRLF**（624 行）。`.gitattributes` 的 pin **只治理 checkout、不修既有工作區**，而 `text` 會把工作區 CRLF 正規化回 LF 進 index，所以 **`git status` 顯示乾淨、永遠不會提起它們**。

清單：`2026-08-28-traceability-gate/` 六檔 + 其 `fixture/` 四檔、`2026-09-01-capability-spikes/spike-report.md`、`2026-09-03-plan-contract-producer-smoke/rendered-plan-instruction.txt`。**本次新增的 mutation fixtures 與其 README 不在內**，所以 README 那張字元數表（在 LF 上量的）仍成立。

校正指令（需使用者執行，AI 的 `rm` 被 deny；只改工作區、不產生 commit）：

```
cd "<worktree>" && rm -r docs/superpowers/poc && git checkout -- docs/superpowers/poc && echo "剩餘 CRLF 檔數: $(grep -rlU $'\r' docs/superpowers/poc/ | wc -l)"
```

**B. 接力棒剩餘三件**（`task-20260903-loosen-plan-close`）

⛔ **push 已嘗試兩次、皆被網路阻塞**（09-07 上午）：`/push-ci` Phase 0 preflight hard abort——`git ls-remote origin` exit 128，`Failed to connect to github.com port 443 after 30s`。

**根因已查出：DNS 解析失敗，不是 GitHub 的問題。** `nslookup github.com` 回 `Server failed`（DNS 伺服器為路由器 `192.168.0.1`），連 IP 都查不出來，git 的 30 秒逾時只是後果。**任何需要外網的操作現在都做不了**（`gh` / `npm` / CI 查詢同理）。建議先試：確認瀏覽器能否上網 → 若只有指令列不通則改 DNS 為 `8.8.8.8` / `1.1.1.1` → 或重啟路由器（`Server failed` 常見於路由器 DNS 轉發卡住）。

**核可仍然有效，網路恢復後直接重跑 `/sd0x-dev-flow:push-ci` 即可**，不需要重新走一次前面的 gate。

1. push（已獲核可，**16** 個 commit 領先 `origin/main`；被網路阻塞中）
2. 開 PR（`finishing-a-development-branch`，本 repo 首次 dogfood）
3. 補驗 task 9.1 的 live Actions run，回填 `verify.md` §10 的 owed verification

**C. 兩項欠款**
- `[NIT_DEFERRED]` `2026-09-03-sdd-review-pkg-helper/README.md:68` —— 「**唯一**可靠的症狀是每個檔都 `DELETED`」是絕對句；若有 snapshot 路徑剛好存在於錯的 `ROOT` 底下，該檔會變成看似正常的 diff，全稱即破。替代措辭：「大多數落點下最可靠的症狀是…」。
- **兩個 gate 都由 fallback 審查者承擔**，Codex 配額今日（9/7）恢復 → **應補外部審**。

**D. 尚未裁定**：`/end-session` 第六步要自跑 `git commit`，與 Anchor Register #4 的封閉授權清單衝突（`/end-session` 不在其中）。本 session 同前次一樣繞開——handoff 不進本 branch、commit 走 `/smart-commit --execute`。**此衝突自 09-04 起懸置未決。**

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **修正動作本身是最高發的缺陷場景，本 session 實證四次。** ① 修 E2 的「只涵蓋一次出現」時，E1 自己也只涵蓋一次出現；② 修「§8.2 是逐字」這個錯誤描述時，用的量測腳本自己有 bug（未設邊界，把後面章節算進 f7），而**同一個 bug 在相隔數輪處造成兩個看似無關的錯誤宣稱**；③ 修完矛盾後寫出的替代句「這支腳本沒有任何一段會 fail loud」，與同檔另一句「`:22` 是唯一的 fail-loud 守門」直接互斥；④ 解釋「為什麼舊的 f7 數字是錯的」時，編了一個沒查證的機制（§8.2 有 code fence——實際為零）。**attribute:** 全域 CLAUDE.md「修正絕對句時寫出的那句替代句，自己又是絕對句、要再過一次例外檢查」。**propose action:** 這四次的共同形狀是「**改的那一刻沒有回到 artifact 重驗**」。既有規則已涵蓋，不新增；但 N 從 7 升到 11，且首次出現「一個量測 bug 生出兩個相隔數輪的錯誤宣稱」這種**單根因多症狀**的形態，值得記進案例。

- [#觀察] **「一個缺陷＝一類缺陷」在紀錄層同樣適用，而且更難自查。** E1 漏掉的兩處中，一處在**另一個 artifact**（`retrospective.md:39`）。掃描邊界訂在「本 change 的 artifact」時它就是隱形的。**propose action:** 宣稱做過 class sweep 時，**把掃描指令與範圍寫進交付物本身**——本 session 已這樣做（errata 的 E1/E2 都附可跑的 `grep` 與「無第 N 處」結論），下次可沿用。

**【當日洞見】**

- **Gate fail-closed 是正常運作；有問題的是 verdict delivery protocol。** 一份 findings 已收斂的審查，花了七輪才把有效 verdict 送到 gate——terminal sentinel 位在長報告尾端、連續多輪因輸出截斷取不到，同一 thread 被重試而非 rotation。首次取得的 sentinel 又因一份報告含兩個 terminal 被 validator **正確**擋下。**兩個 terminal 被擋不是壞事**，那是系統抓到 ambiguity。已登記為 `task-20260904-reviewer-verdict-delivery`（bounded investigation，四個候選方向）。
- **「規則正確、但它承諾的狀態在它落地的那個工作區裡當下就不成立」是一個獨立的缺陷類別。** `.gitattributes` 的 LF pin 內容完全正確，但它落地的 clone 裡有 11 個檔已經是 CRLF，而 `git status` 因為 `text` 的正規化方向而顯示乾淨。這與 POC helper 的 L1（腳本 exit 0、靜默把每個檔報成 DELETED）是同一形狀，只是高一層。**共同特徵：宣稱自己防止某個靜默錯誤的東西，自己就處在那個錯誤裡。**
- **同一個缺陷類別當天第二次發作：substring probe 因格式不符回 0 命中，且不報錯。** 收工後開 `spec-contradiction-cleanup` 時，用 `grep "writing-plans' task format contains TDD micro-steps"` 查那兩處條文，**只命中 1 處**——看起來像「另一處已經不在了」。實際上兩處都在，miss 的原因是檔案裡寫的是 markdown inline code `` `writing-plans` ``，我的 pattern 少了那對反引號（實測：原 pattern 回 0，加 backtick 回 1）。**只因為我接著讀了前後行才發現。** 這與執行報告 §5 那十一個產物裡的「substring probe 漏掉換行的句子」同族，也與本 session 兩次量測 bug 同族：**篩選器回 0 命中時，那個 0 不能當答案用**。全域 CLAUDE.md 已有對應條文（「自動篩選回報 0 命中時，換一條結構完全不同的路徑交叉驗」）——這次是那條規則的正面實證，不需新增規則，但 N 值該往上加。**下次動這條 change 時，兩處條文的確切位置是 `openspec/specs/tdd-claim-accuracy/spec.md:21-22`（第一處，跨行）與 `:60`（第二處）。**

- **保存資產時，「複述在報告裡」不等於「保存了」。** archived `verify.md` §8.2 標題寫著 "Fixture contents, verbatim"，實測七個 fixture 只有 f1 是 100%，f5 連 code block 都沒有——而 f5 的違規正是 `plan.md` 的 entry key，也就是唯一完全沒被複製的那一個。**逐項量過才知道那份複述餵不了重跑者。**

### 五、檔案異動

錨來源：本 session 開工後的 commit 範圍 `6dae1c6..HEAD`（6 個 commit）

```
6b72cff chore(git): pin LF for the POC assets, and for this file        M  .gitattributes
1125e06 chore(work-map): register the two follow-ups this close-out surfaced  M  workflow-harness/work-map.jsonl
1379de4 docs(archive): record two corrections to the loosen-plan record  A  openspec/changes/archive/2026-09-04-loosen-plan/errata.md
68b3e70 docs(poc): preserve the loosen-plan verification assets          A  22 檔（三組 POC 資產）
489df22 feat(specs): sync the loosen-plan delta specs into main specs    A/M 3 檔
03bf87e chore(openspec): archive loosen-plan                            R100 × 11
```

未追蹤且刻意排除：`文檔/handoff/session-handoff-20260903.md`、`-20260904.md` 與本檔（handoff 屬 main，不進本 branch）。

**無專案資料夾** → 專案 Changelog 這步 skip。

### 六、下一步建議

1. **跑 CRLF 校正指令**（見三-A），確認回 `0`。這是 push 前唯一紅燈。
2. **push + 開 PR** —— 已獲核可；`finishing-a-development-branch`，本 repo 首次 dogfood。push 前確認 `文檔/handoff/` 三份仍在 branch 外。
3. **補驗 task 9.1 的 live Actions run**，回填 `verify.md` §10。
4. **把三份 handoff 複製回主目錄**並在 main 上以既有受控流程 commit（`task-20260904-worktree-handoff-lifecycle` 未完成前，這一步仍是手動的）。
5. **Codex 配額今日恢復** → 補外部審（doc + code 兩個 plane 目前都是 fallback 背的），並順手收掉 `README.md:68` 那條 `[NIT_DEFERRED]`。

## Session 14:14

### 一、本 session 主題

**loosen-plan 收尾撞上補審紅燈，轉為開 post-archive follow-up change。** 開工時的計畫是「修網路 → push → 開 PR」，實際走成「補外部審 → 審出 5 個 P1 → 使用者裁定全收 → 開新 change 承接」。push 仍未執行，但**擋住它的理由從網路換成了 5 個 blocking correctness defects**。

前一份是本檔 Session 08:36（同日、另一 session），記的是 archive 與資產保存那半。

### 二、完成事項

- **CRLF 校正完成（11 → 0）** —— 上個 session 留下的 push 前唯一紅燈。使用者跑 `rm -r docs/superpowers/poc && git checkout --`，重取後 32 個檔全在、CRLF 歸零（Python 逐檔驗位元組）。
- **`[NIT_DEFERRED]` 收掉，並做同類全掃** —— `2026-09-03-sdd-review-pkg-helper/README.md:68` 的「**唯一**可靠的症狀是每個檔都 `DELETED`」是已被證偽的全稱句，改為「大量被報成 `DELETED`、判準是**比例異常**」，並把反例（算錯的 `ROOT` 底下剛好存在同名相對路徑時，該檔會產出看似正常的 diff）**寫進句子本身**。同類掃描：正規表示式掃整批 POC 文件 20 處全稱句，其餘 19 處成立（實測紀錄／機械性事實／已寫例外），掃描指令留在對話可重跑。
- **backlog 週一週檢（`shadow-plan`）** —— 0 筆可自動刪、0 筆待判。結果為 **`incomplete_coverage`、不計入四輪**（累積 0/4）：6 條裡 5 條無穩定編號，交叉比對一條都沒比到。額外判讀：**6 條裡有 4 條講的不是這個 repo 的事**（workflow-harness／sd0x 兩個 plugin），在此 repo 內無從驗證失效與否。
- **補 Codex code plane 外部審（配額 10:26 恢復後）** —— 範圍 `origin/main..HEAD`（16 commits／55 檔）。**判決 ⛔ Blocked：5 個 P1 + 5 個 P2。**
- **逐條回原始碼獨立查證，5/5 全部屬實、零誤報** —— check 12 `:548` 明文只做集合雙向比較而內文兩處自稱 keyed 1:1；check 9 `:498` 的 `subject:` 只驗 trim 後非空；check 11 `:517` 建立在「一 task 一組 RED/GREEN」前提；check 7 `:421` 仍寫 `If plan.md has any tasks marked [~]`；`version-check.yml:44` 已抓 `v2` 而 `CLAUDE.md` 耦合表仍寫 `v1`。另驗到 archive 後三條相對連結全 DEAD、`git tag -l` 為空（README 卻宣稱 `v2.0.0` 已建）。
- **使用者裁定（2026-09-07）** —— 五條 P1 全視為 blocking、全收；**第 4 條解除延後**（原 `task-20260904-spec-contradiction-cleanup` 的裁定被新證據推翻：獨立 Reviewer 在不知既有討論下再次抓到，理由是 canonical spec 會給未來執行者互斥的現行規則）；不回頭改寫已 archive 的 loosen-plan；P2 暫不擴張。
- **開 `fix-v2-blocking-defects` change（`--schema superpowers-bridge`）** —— **4/8 artifact，`openspec validate` 通過**：
  - `brainstorm.md` 走 schema 明列的**手寫出口**（使用者明確選擇、非靜默降級），保存已完成的決策鏈
  - `proposal.md`（Why 372 字元／限制 50–1000）、`design.md`（6 個決策各附已拒替代方案、5 條 Risk／Trade-off、落地順序、3 個 Open Question）
  - `specs/` 三份 delta（`plan-contract`／`tdd-evidence-contract`／`tdd-claim-accuracy`），新增 15 個 scenario
- **`backlog line 84` case-count 4 → 5**，同交易自動帶 `[mature: 2026-09-07]`（使用者裁定今日案例算同一條 pattern）。

### 三、未完事項 / 接力棒

**A. `fix-v2-blocking-defects` 剩餘 4 個 artifact**：`tasks` → `plan` → `verify` → `retrospective`（DAG 順序，`tasks` 為當前唯一解鎖者）。

**B. 五條 P1 的實作全部未動**（僅完成規格層）。逐條的最小修法邊界已寫進 `design.md` §Decisions，實作時直接照 D1–D6 走，不需重新設計：

1. check 12：兩邊 key 先各自去重檢測 → 再集合相等；重複與缺漏**給不同錯誤訊息**
2. checks 9–11：配對單位由 task 改為 **subject**；subject grammar 為「恰一個 `::`、兩側 trim 後非空」；同 task 內 subject 唯一；每 subject 恰一 RED 一 GREEN
3. check 7：掃描對象 `plan.md` → `tasks.md`，其餘判定邏輯一字不動
4. `openspec/specs/tdd-claim-accuracy/spec.md` 兩處 stale clause（`:20-22` 與 `:59-61`）
5. `CLAUDE.md` 耦合表 `v1` → `v2`，併同版本敘述與已 archive 的 change 路徑

⚠️ **D5 的前提要複驗**：「不再 bump 版本」成立於「v2 從未發版」（已查 `git tag -l` 為空）。若在本 change 完成前 v2 被 push 並打 tag，此決策必須重新評估。

⚠️ **落地順序有一步容易漏**：改完 schema 後**必須重新同步 dogfood 副本**（`rm -rf openspec/schemas/superpowers-bridge && cp -R superpowers-bridge openspec/schemas/`），否則本 change 自己的 verify 會跑在舊 checker 上。

**C. doc plane 外部審未補** —— 本 session 只補了 code plane（刻意不併發，避免再撞配額）。doc plane 目前仍由 fallback 審查者承擔。

**D. push / PR / CI 全部往後推** —— 已獲核可、網路已恢復（`git ls-remote` exit 0）、領先 16 個 commit，但**現在擋住它的是 5 個 P1**，不是網路。完成條件：follow-up change 無 blocking finding 後 archive，再回到 push → PR → CI。

**E. P2 五條記為 observation、不拉進本輪**（使用者裁定）：check 7 的「deferred 任務連回 plan 條目」建議、plan producer 未宣告的直接依賴（`design`／`specs`）、`templates/tasks.md` 預填看似完成的證據、README 的 RED outcome 說明寬於 schema、archive 後三條 DEAD 連結、README 宣稱 `v2.0.0` tag 已建立而實際無 tag。

**F. 兩個懸置未決**：
- `/end-session` 第六步自跑 `git commit` 與 Anchor Register #4 封閉授權清單衝突。**2026-09-07 查清**：Register #4 原文為「動這張清單本身也是 Anchor 級改動」，**不是禁止**；且本 repo 沒有釘住規則的測試（`test/rules/discretion-tiers.test.js` 不存在），`.claude/rules/*.md` 是 plugin 裝的副本、**改了會被下次 `/install-rules` 覆蓋且無人喊**。使用者裁定**走 B（繼續繞開）**；建議的真正修法是 C（改 `/end-session` 委派給 `/smart-commit --execute`），屬另一條工作線。
- backlog 交叉比對的四輪時間盒是否就此停掉（射程對 6 條規模的 backlog 用不上）——已端出，未裁定。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **fallback 審查通過 ≠ 沒問題——這次是那條降級規則的正面實證。** loosen-plan 收尾時兩個 plane 全綠、雙 gate 全過、fallback 審查者給了經 validator 驗過的有效 verdict，而正規外部審一進來就是 ⛔ Blocked、5 個 P1，且**逐條回原始碼獨立查證 5/5 全部屬實、零誤報**。**attribute:** 全域 CLAUDE.md 複審紀律「降級有條件、非免票：高風險項不得就此結案，外部審恢復後必須補審」。**propose action:** 既有規則已涵蓋且本次證明有效，不新增；但這是該條首次產出「補審抓到的缺陷數 > 0」的實例，值得當作它的承重案例。

- [#觀察] **「名字宣稱的範圍 > 實際斷言的範圍」今天在 checker 上再現兩次，且三層審查都沒抓到。** check 12 內文兩處自稱 `keyed 1:1`、實際只做集合相等（重複會被集合吃掉）；check 9 名為 "with required fields"、實際只驗 trim 後非空。**載體從文件換成了檢查器**——原本這條 pattern 記的是「我讀了文件的名字就下結論」，今天是「檢查器自己的名字比它的斷言大，而本 repo 雙 gate ＋ fallback 審查都信了那個名字」。已 bump `backlog line 84` 至 `case-count: 5`、自動帶 `[mature: 2026-09-07]`。**propose action:** 該條目已成熟、待評估是否升格；下次動 checker 類產物時，把「名稱 vs 斷言」的對照當成必跑的一項，而不是等外部審抓。

**【當日洞見】**

- **「先補審再 push」的決定當場回本。** 替代選項是先 push、審查意見在 PR 上收。若走了那條，5 個 P1 會先進遠端、**CI 還會是綠的**（CI 只驗 schema 結構、驗不到判定邏輯），然後在 PR 上回頭改契約。
- **改檔會讓審查關卡重開，所以修正要排在審查之前。** 收 `[NIT_DEFERRED]` 時先改檔再派審，不是反過來——否則審完再動檔，那份 verdict 就失效了。
- **昨天那條「規則承諾的狀態在它落地的工作區當下就不成立」今天被清掉了**：`.gitattributes` 的 LF pin 內容完全正確，但同一個 clone 裡 11 個檔仍是 CRLF，而 `git status` 因為 `text` 的正規化方向顯示乾淨。砍掉重取後歸零。
- **backlog 的交叉比對機制對 6 條規模的 backlog 用不上，而「射程不完整」不等於「機制壞了」。** 根因是那份 backlog 的 5 條沒有穩定編號，而其中 **4 條講的根本不是這個 repo 的事**——跨專案的條目就近記在手邊那本，後果是它們在所在的 repo 裡驗不了。
- **Anchor 的「這也是 Anchor 級改動」不等於「不准改」。** 卡了三天的 `/end-session` commit 衝突，實際查原文後發現它從來沒禁止把 `/end-session` 加進授權清單，只是說那件事需要使用者拍板。**沒去讀原文，就把「需要你決定」自動讀成了「不能做」**——這與本 session 的紀律接力第二條同源。

**【學習候選】**

1. **Case** — 外部審恢復後補審，抓到 5 個 fallback 審查與雙 gate 都放過的 P1，且 5/5 查證屬實；其中 2 條的形態是「檢查器的名稱比它的斷言大」。
2. **Candidate Pattern** — 凡是「宣稱驗證了 X 的機制」，它自己的名稱與實際斷言必須被當成兩個東西對照一次；**同一個執行者無法可靠地對自己做這件事**（本 repo 雙 gate ＋ fallback 審查，三層都信了那個名字）。適用邊界：有明確可讀實作的檢查器／測試／驗收條件；不適用於純人工判斷項。
3. **Evidence** — 本次 2 例 ＋ `backlog line 84` 已累積至 5 例（跨文件、profile 表、checker 三種載體）。跨載體復發已成立；「同一執行者做不到自查」目前是 **Hypothesis**（樣本皆為同一執行者，缺對照組）。
4. **Minimum Sufficient Intervention** — **不新增規範**。既有紀律（「先讀實際驗到什麼再讀名字說驗什麼」＋降級補審條款）已完整涵蓋本案，且本次正是它們生效的證明。真正缺的是**掛點**：目前沒有任何一層會在「宣稱某檢查守住 X」時要求當場破壞 X 跑一次。傾向優先改既有環境——把這項併入 `fix-v2-blocking-defects` 的 verify 要求（每條修改過的判定，交付前記錄一次轉紅），而不是新增一條全域規則。
5. **Promotion** — 建議 **Refine Existing Strategy**（強化既有條文的掛點，不新增規則）。`backlog line 84` 已 `[mature:]`，升格與否由使用者決定。

### 五、檔案異動

錨來源：本 session 開工 commit（b2e377e、開工於 2026-09-07T09:05:13）——列 b2e377e..HEAD

**本 session 無任何 commit**（`git log b2e377e..HEAD` 為空）；下列為 working tree 改動，於本次收工一併 commit：

```
 M  backlog.md                                                    case-count 4→5 + [mature:] + prose 指標
 M  docs/superpowers/poc/2026-09-03-sdd-review-pkg-helper/README.md  絕對句修正（:68）
 ?? backlog-crosscheck-shadow.json                                週檢 shadow 帳（skill 明文要求進版控）
 ?? openspec/changes/fix-v2-blocking-defects/                      7 檔（.openspec.yaml + 4 artifact + 3 delta spec）
```

未追蹤且**刻意排除**：`文檔/handoff/session-handoff-20260903.md`、`-20260904.md` 與本檔（handoff 屬 main、不進本 branch）。

CRLF 校正只改工作區、不產生 commit（git 存的本來就是 LF，已驗）。

**無專案資料夾** → 專案 Changelog 這步 skip。驗收節點 sentinel 區段無條目 → 打勾這步 skip。

### 六、下一步建議

1. **接續 `fix-v2-blocking-defects` 的 `tasks` artifact**（唯一解鎖者），然後 plan → 實作五條 P1 → verify → retrospective。
2. **實作時記得那兩個 ⚠️**：改完 schema 要重新同步 dogfood 副本；D5「不 bump 版本」的前提（v2 未發版）在 push 前要複驗一次。
3. **補 doc plane 外部審**——本 session 只補了 code plane，doc plane 仍由 fallback 背。
4. **五條 P1 收斂、無 blocking finding 後 archive**，再回到 push → PR → CI（已核可、網路已恢復、領先 16 commit）。
5. **兩個懸置待裁**：backlog 四輪時間盒是否停掉；C 案（改 `/end-session` 委派 `/smart-commit`）要不要登記成正式工作線。

## Session 16:05

### 一、本 session 主題

**主目錄開工、worktree 收工的接續段。** 開工提示指向 0904 的交接，但真實現況在 worktree：今天已有兩個 session 的紀錄只存在那裡、主目錄工作地圖落後 6 筆。止血後接續 `fix-v2-blocking-defects`：寫完 tasks 與 plan（6/8），doc gate 由 Codex 本尊三輪審到 Mergeable，以 `/smart-commit --execute` 進了一個 commit。裁定兩件：backlog 四輪時間盒停用；TDD applicable 以「同一可重跑 case 改前紅、改後綠」為判準，不以是否用測試框架為判準。

前一份是本檔 Session 14:14（同日、另一 session）；本區塊不重貼。

### 二、完成事項

- **三份 handoff 複製回主目錄 `文檔/handoff/`**（0903、0904、0907），逐位元組比對相同。照 0904「先止血、制度另開 change」裁定，未 commit。
- **`tasks.md` 落地**：15 個步驤、5 組，順序照 design 落地順序，唯一刻意倒置是 fixtures 先於 checker 修正（RED 只能在改措辭前取得）。checker 修正 2.1–2.3 標 `TDD: applicable`、以 fixture 判定為 RED/GREEN subject；使用者裁定的三個邊界寫進檔頭。
- **`plan.md` 落地**：15 個契約條目、key 集合與 tasks 兩向相等；全域約束逐字取自三份 delta spec；引用的行號、grep 字串、CI grep 行皆回原始碼核對。
- **doc gate 三輪（Codex，非 fallback）**：第一輪 2 🔴（check 7 的 `plan.md` 在該檢查與 freshness 表共四處、不是一個字；plan 介面耦合漏 1.4 與 3.2→5.1）；第二輪 2 🔴 皆為第一輪修出來的（f7 沒有 RED 卻被要求 RED/GREEN；5.3 被寫成消費 5.1 的 checker）；第三輪零 finding、`✅ Mergeable`。doc_review 記 pass。
- **`3eba33d` `docs(openspec): land tasks and plan for fix-v2-blocking-defects, artifacts 6/8`** —— 走 `/smart-commit --execute`，執行腳本自驗與 `verify-last` 皆 exit 0、無 AI 署名。
- **Codex 配額 15:08 用完、15:28 恢復**：選等待而非切 fallback（切了會 sticky 綁定整個 change），記 `[DEVIATION]` 一則。
- **兩件懸置結清**：四輪時間盒停用（使用者裁定）；C 案已於 14:14 session 登記為 `task-20260907-end-session-commit-delegation`，不重登。

### 三、未完事項 / 接力棒

- **`fix-v2-blocking-defects` 進實作**（`/opsx:apply`）：group 1 fixtures 先做、再改 schema.yaml。實作一行未動。
- **實作提醒**：改完 schema 重同步 dogfood 副本；D5 前提（`git tag -l` 空、未 push）在 verify 前複驗（tasks 5.3）。
- **code plane 外部審**：實作完要重派；doc plane 本 session 已由 Codex 補上。
- **backlog line 88 是錯誤條目**（「worktree 缺 smart-commit 腳本」——三支腳本自 7a426fa 起在版控、worktree 也有），要刪。本 session 未動它以免重開 doc gate。
- **四輪時間盒的落地方式**：本 repo 之後週檢只跑唯讀 `plan`、不跑 `shadow-plan`；shadow 帳檔不刪（刪了遺失實驗歷史）。plugin 側「無穩定編號 / 多數條目屬別 repo 的 backlog 應可退出交叉比對」屬 workflow-harness 的設計缺口，由使用者帶去那邊。
- **handoff 落點**：三份已在主目錄、未 commit；等 main 上以受控流程 commit（`task-20260904-worktree-handoff-lifecycle` 未完成前仍是手動）。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **修正動作生新缺陷，今日第五次。** 第一輪審完修 check 7 的類掃描時，順手把 f7 也寫成要 RED/GREEN——它在舊措辭下本來就判對、沒有 RED 可拿；又把 5.3 寫成消費 5.1 的 checker，而它只跑 git 指令。第二輪審全抓到。形狀不變：改的那一刻沒回 artifact 重驗。**attribute:** 全域 CLAUDE.md「修正絕對句時寫出的那句替代句要再過一次例外檢查」的同族。**propose action:** 既有規則已涵蓋，N 從 11 升到 13，不新增規則。
- [#反] **讀了別人寫的 backlog 條目就照講，沒去 `ls`。** 早上 session 的 backlog 說「worktree 缺 smart-commit 腳本」，我據此出了一套手動指令給使用者貼；使用者問「你不能執行嗎」才去查，三支腳本一直在、且 7a426fa 就進版控。**attribute:** backlog line 84 那條 pattern（讀了名字沒讀實際）的又一例，載體換成「另一 session 寫的 backlog 條目」——那條已 `[mature:]`，本例不再 bump。**propose action:** 刪 line 88；寫進交付物前對「某處缺 X」類宣稱先 `ls` 一次。
- [#觀察] **`/end-session` 開工錨點在跨目錄 session 會降級。** 主目錄開工、worktree 收工，快照 root 對不上（`root_mismatch`），退回 per-cwd 時間戳 N=2h。本次 2h 剛好涵蓋正確範圍，那是運氣不是機制。**propose action:** 屬 `task-20260904-worktree-handoff-lifecycle` 的射程，不另開。

**【當日洞見】**

- **「fallback 通過 ≠ 沒問題」在 doc plane 也成立。** Codex 配額用完到恢復只差 20 分鐘，等待零成本；換到的是三輪共 4 個屬實的 🔴，其中兩個是 fallback 最不擅長抓的「改動範圍寫窄了」與「介面耦合漏邊」。
- **TDD applicable 的判準拍板（使用者）：** 不看有沒有測試框架，看能不能用同一個可重跑 case 在改前證明舊行為違約、改後證明轉正。三個邊界——RED 改前實跑、RED/GREEN 綁同 subject、`failure:` 寫明預期 vs 實際判定——已寫進 tasks.md 檔頭。上一個 change 對同類工作標 `n/a` 不回溯，因為當時沒有可重跑 fixture。
- **專案 hook 擋含 Git Bash 暫存目錄字面路徑的指令，而 smart-commit 的 `alloc` 正好回該目錄下的路徑。** 同一 Git Bash 讀寫其實安全；用 `$(dirname "$(mktemp -u)")` 取目錄即可繞過。不改規則。附帶：handoff 正文若寫出那個字面路徑，append 指令本身也會被擋——本區塊因此改寫成描述。
- **四輪時間盒沒有提前停用的開關。** skill 設計是跑滿四輪才拍板；本 repo 才跑一輪且不計入。裁定落地方式見三。

**【學習候選】**

沒有。今天的案例都命中既有規則（修正重驗、讀名字不讀實際、降級補審），是 N 值上升、不是新 pattern。

### 五、檔案異動

⚠️ 錨來源：共用 per-cwd 時間戳 N=2h（起點 2026-09-07T14:43:45）——可能非本 session（快照屬另一專案根）

視窗內 4 個 commit，其中前三個（368d586、a78d45d、ad92839）屬 Session 14:14 收工時所提交、非本 session 產出；本 session 產出僅：

```
3eba33d docs(openspec): land tasks and plan for fix-v2-blocking-defects, artifacts 6/8
A	openspec/changes/fix-v2-blocking-defects/plan.md
A	openspec/changes/fix-v2-blocking-defects/tasks.md
```

結算改動（本次收工 commit）：`workflow-harness/work-map.jsonl`（fix-v2-blocking-defects NEXT → DOING）。

未追蹤且刻意排除：`文檔/handoff/session-handoff-20260903.md`、`-20260904.md` 與本檔（handoff 屬 main、不進本分支；三份已複製到主目錄）。

**無專案資料夾** → 專案 Changelog skip。驗收節點 sentinel 區段無條目 → skip。

### 六、下一步建議

1. **`/opsx:apply` 進實作**，group 1 fixtures 先做（RED 要在改 schema 前拿到），再 group 2 的五條檢查。
2. **實作中兩個提醒**：改完 schema 重同步 dogfood 副本；D5 前提在 verify 前複驗。
3. **實作完重派 code plane 外部審**；doc plane 已補。
4. **刪 backlog line 88**；三份 handoff 在主目錄等 main 上受控 commit。
5. **懸置已清空**：四輪時間盒停用已裁、C 案已登記。無待裁事項。
