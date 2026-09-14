## Context

`loosen-plan` 把 schema 從 v1 推到 v2（Plan Contract + TDD 證據契約），並於 2026-09-04 archive。
當時雙 gate 全綠，但兩個 plane 都由 fallback 審查者承擔（Codex 配額耗盡）。

2026-09-07 補派的獨立 Codex review 回報 ⛔ Blocked，5 個 P1。逐條回原始碼查證，**五條全部成立**
（查證方式與行號見 [brainstorm.md](./brainstorm.md) §已查證依據）。

**關鍵的現況約束：v2 尚未發版。** `superpowers-bridge/VERSION` 已寫 `2.0.0`，但本機與遠端**都沒有
任何 git tag**，README 的「git tag `v2.0.0` created at release」是一句尚未兌現的敘述。
branch 領先 `origin/main` 16 個 commit、尚未 push。

這個事實決定了本設計的性質：**這批修正不是對已發布契約的破壞性變更，而是 v2 出廠前的缺陷修復。**

### 缺陷的共同形態

P1-1 與 P1-2 屬同一類：**檢查的名稱宣稱的範圍，大於它實際斷言的範圍。**

| 檢查 | 名稱宣稱 | 實際斷言 |
|---|---|---|
| check 12 | "task-number set **equals** plan entry-key set"，內文兩處自稱 keyed **1:1** | 集合雙向差集為空——重複會被集合吃掉 |
| check 9 | "RED and GREEN records present **with required fields**" | 欄位存在且 trim 後非空——不驗任何格式 |

此類缺陷的症狀是「一切正常」：驗證全過、沒有任何一層會抗議，只有事後交叉比對才發現。

## Goals / Non-Goals

**Goals:**

1. 讓 check 12 真正實現它自稱的 1:1，而非集合相等。
2. 讓 checks 9–11 對「什麼形狀的證據算合格」給出**單一決定性**答案，任何兩個 agent 讀同一份 `tasks.md`
   必得相同判定。
3. 讓 check 7 掃現行 carrier，恢復一道在 v2 底下已失效的檢查。
4. 讓 `tdd-claim-accuracy` 主 spec 對「TDD 走哪個載體」只剩一個答案。
5. 讓 `CLAUDE.md` 的跨檔耦合表與 CI 現況一致。

**Non-Goals:**

1. **不納入 P2**——除非某個 P2 直接影響這 5 個 P1 的修復正確性。
2. **不重做 Evidence system**——不引入 evidence registry、不做跨 change 的證據追蹤、不驗證 evidence truth。
3. **不重開 loosen-plan**——不改寫任何已 archive 的 artifact。
4. **不重新設計 traceability**（P1-1）、**不重新設計 deferred 規則**（P1-3）。
5. **不順手做其他治理優化。**

## Decisions

### D1：check 12 的 1:1 用「先去重檢測、再集合相等」實現

- **選擇**：分兩階段。階段一分別檢測 `tasks.md` 任務編號與 `plan.md` entry key **各自是否有重複**，
  任一側有重複即 BLOCK 並逐筆點名重複的 key；階段二才做既有的雙向集合比較。
- **理由**：這是能達成 1:1 的最小改動。無重複 + 集合相等 ⇔ 存在雙射，數學上等價於 1:1，
  不需引入計數或多重集比較的新機制。且**兩種失敗給出不同的錯誤訊息**——
  「1.1 出現兩次」與「1.1 沒有對應的計畫條目」是不同的缺陷，合併成一句會讓修的人找錯地方。
- **已考慮 alternative**：
  - *比較多重集 / 計數*——能抓到同樣的問題，但錯誤訊息會退化成「數量不符」，
    診斷資訊比逐筆點名差；且需要新的比較機制。
  - *只在 tasks 側去重*——不對稱。`plan.md` 出現兩個 `## 1.1` 同樣違反 1:1。

### D2：Evidence 的配對單位從「task」改為「subject」

- **選擇**：一個 task 底下可以有多個 subject。RED / GREEN 紀錄**以其 `subject:` 值配對**，
  每個 subject 必須恰好有一個 RED 與一個 GREEN。同一 task 內，subject 值在**每一側各自唯一**
  ——至多一筆 RED、至多一筆 GREEN 帶同一個 subject（RED 與 GREEN 本來就共用同一個 subject，
  所以唯一性不能跨側要求）。
- **理由**：現行 check 11（「RED 的 subject 必須等於 GREEN 的 subject」）隱含了「一 task 只有一組配對」
  的前提，一旦允許多個測試就無法決定要拿哪個 RED 比哪個 GREEN。**改用 subject 當配對鍵，
  多對紀錄的配對關係才是唯一確定的**——這正是「決定性」這個宣稱的要求。
  「同一側內 subject 唯一」是配對可解的前提：同一側出現兩筆同名 subject 時，
  配對又回到不確定。
- **已考慮 alternative**：
  - *維持一 task 一組配對*——最小，但把「一個任務要寫多個測試」這個常態排除在契約外，
    逼使用者把一個任務硬拆成多個。
  - *以出現順序配對（第 n 個 RED 對第 n 個 GREEN）*——不需要 subject 每側唯一，
    但順序是脆弱的隱含契約：中間插入一筆就全錯位，且錯位後仍可能通過檢查。

### D3：subject grammar 採最小可判定形式

- **選擇**：`subject:` 的值 trim 後，必須符合 `<test-file>::<test-name>`——
  **恰好一個 `::` 分隔符，且左右兩側 trim 後皆非空**。不對檔名語法（副檔名、路徑分隔、大小寫）
  再作規定。
- **理由**：schema 現有文字已經指定了 `test-file::test-name` 這個形式（`schema.yaml:205-207`），
  並明說它是「本 schema 的第一個慣例、不是架構不變量」。**把既有慣例變成可判定的規則就夠了**；
  再去規定路徑語法會把不同生態系（pytest / vitest / go test）的合法識別碼擋在外面，
  那不是 correctness 修復，是新增限制。
- **已考慮 alternative**：
  - *完整檔案路徑正規表示式*——過度規定，且無法涵蓋所有測試框架的命名。
  - *維持只驗非空*——就是本次要修的缺陷。

### D4：check 7 改讀 `tasks.md`，不追加「deferred 任務須連回 plan 條目」的新規則

- **選擇**：把 check 7 的掃描對象從 `plan.md` 改為 `tasks.md`，其餘判定邏輯
  （逐筆列舉、指認等價自動化測試、無等價者記入 retrospective Misses）**一字不動**。
- **理由**：這是 migration 漏改，不是規則設計錯誤。v2 把任務標記搬到 `tasks.md` 時漏了這一處，
  改回正確的 carrier 就恢復原本的行為。外部審另建議「把每個 deferred 任務連回它的 plan 條目」，
  **本次不採納**——那是新增規則，不在 scope 內（使用者裁定：不要重新設計規則）。
- **已考慮 alternative**：
  - *同時掃兩邊*——`plan.md` 在 v2 底下不可能有任務列，掃它是純粹的死碼。
  - *採納連回 plan 條目的建議*——超出 scope；記為 follow-up observation。

### D5：schema major 不從 2 再 bump，bundle 版本維持 `2.0.0`

- **選擇**：`schema.yaml` 的 `version:` 維持 `2`；`superpowers-bridge/VERSION` 維持 `2.0.0`。
- **理由**：兩條依據。①`CLAUDE.md` 定義 schema major 只在**圖契約破壞**時 bump
  （artifact 增刪、`requires:` 改、PRECHECK 形狀改）——本次三項皆未動。
  ②**v2 從未發版**（無 tag、未 push），所以這批修正是出廠前修缺陷，不是對已發布契約的變更；
  沒有任何採用者持有舊的 v2 行為需要遷移。
- **已考慮 alternative**：
  - *bump 到 3*——會讓 Compatibility 表出現一個從未有人使用過的 v2 列，
    且觸發 `version-check.yml` 的解析改動（該表第一欄是 CI 的抓取鍵）。代價大於收益。
  - *bump 到 2.0.1 / 2.1.0*——patch / minor 語意都不對：`2.0.0` 這個版本號還沒被發布過，
    修的是它自己尚未出廠的內容。
- ⚠️ **此決策有一個必須成立的前提**：v2 確實未曾發布。已查證——`git tag -l` 回空。
  若在本 change 完成前 v2 被 push 並打了 tag，這個決策必須重新評估。

### D6：README 的 checks 8–12 說明與 schema 同步修正，雙語一起

- **選擇**：`superpowers-bridge/README.md` 與 `README.zh-TW.md` 的對應段落隨 schema 一併修改，
  同一個 commit。
- **理由**：`CLAUDE.md` 的跨檔耦合表明列這是連動項，且外部審已抓到既有的一處不同步
  （README 說 RED outcome 可以是 "anything else"，schema 要求單一大寫 token）——
  這正是不同步的實例。

## Risks / Trade-offs

- **[Risk] 修 checker 的同時把 checker 改壞，而現有機制抓不到。**
  → Mitigation: 每一項修正都必須有 mutation fixture 的**正負案例**——不只驗「壞的會被擋」，
  也要驗「好的不會被誤擋」。既有的 `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/`
  已保存 f1–f7 可直接擴充，其 README 記載了重跑方式。

- **[Risk] 「宣稱這條檢查守住 X」而實際沒守住——本次修的就是這個病，修的過程可能復發。**
  → Mitigation: 每一條新增 / 修改的判定，交付前**當場把 X 破壞掉跑一次、記錄轉紅**。
  答不出「哪一條會紅」就是還沒守住。這是全域紀律的動作版要求，不是本 change 自訂。

- **[Risk] D2 是語意變更，`schema.yaml` 的任務指令段（`:196-212`）也建立在單組配對的前提上
  （"a RED record and a GREEN record"、"Its `subject:` value MUST be identical to RED's"）。
  只改 checks 不改指令，會讓產出端與驗證端對不上。**
  → Mitigation: 指令段與 checks 段視為同一項改動，同一個 commit 修完；
  交付前以 `grep` 掃 `schema.yaml` 全文確認無殘留的單組配對措辭。

- **[Trade-off] D3 只驗 `::` 的存在與兩側非空，不驗檔名語法。**
  → 接受理由：跨生態系的測試識別碼形式不可窮舉，過度規定會製造假不合規。
  代價是 `foo::bar` 這種無意義但形式合法的值仍會通過——那屬於 evidence truth，
  依 D2 的責任邊界歸 Reviewer 判斷，checker 明文不宣稱驗它。

- **[Trade-off] 本 change 自己的 `tasks.md` 會被修好後的 checks 驗。**
  → 接受理由：這是 dogfooding 的正常結果，而且是有價值的——若新規則讓本 change 自己過不了，
  那本身就是設計有問題的訊號。但需注意**先後順序**：schema 修好並同步到 `openspec/schemas/` 之後，
  本 change 的 verify 才會跑在修好的 checker 上。

## Migration Plan

**採用者遷移：N/A。** v2 未發版、無採用者持有 v2 行為（見 D5 前提查證）。

**本 repo 內的落地順序：**

1. 改 `superpowers-bridge/schema.yaml`（checks 2、7、9–12 ＋ 任務指令段；check 2 為 2026-09-11 追加，理由見 proposal §Impact）
2. 同步 `superpowers-bridge/templates/`（`verify.md`、`tasks.md`）與雙語 README
3. 補 mutation fixture 的正負案例
4. 修 `openspec/specs/tdd-claim-accuracy/spec.md` 的 stale clause
5. 修 `CLAUDE.md` 跨檔耦合表
6. **重新同步 dogfood 副本**：`rm -rf openspec/schemas/superpowers-bridge && cp -R superpowers-bridge openspec/schemas/`
   ——不做這步，本 change 的 verify 會跑在舊 checker 上
7. 在 archive 的 `errata.md` 追加一條 pointer（append-only）

**Rollback：** 本 change 全部落在單一 branch、尚未 push；rollback 即為捨棄該批 commit。
無資料遷移、無外部狀態。

## Open Questions

1. **check 12 的重複偵測要不要也涵蓋「任務編號不是數字」的既有分支？**
   現行 check 12 已把「任務列首個 token 不是數字」列為自身的缺陷（`schema.yaml:529-531`）。
   去重檢測應在該分支之前或之後，影響錯誤訊息的順序，但不影響判定結果。
   → 傾向維持現行順序、去重檢測插在集合比較之前，實作時確認。

2. **`plan.md` 的 entry key 去重，要不要區分「同一標題重複」與「不同標題但同編號」？**
   → 傾向不區分：兩者都違反 1:1，錯誤訊息點名編號與出現行號即可。

3. **本 change 自己的 `tasks.md` 是否會有 `TDD: n/a` 的任務？**
   修文件（P1-4、P1-5）性質上無自動化測試可寫。
   → 依既有契約標 `TDD: n/a` 並在 verify 說明理由；此為既有機制，非本 change 新增。
