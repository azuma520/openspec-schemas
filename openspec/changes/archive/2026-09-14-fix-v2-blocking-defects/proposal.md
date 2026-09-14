## Why

`loosen-plan`（schema major 1 → 2）archive 時，兩個審查 plane 都由 fallback 審查者承擔——Codex 配額當時已耗盡。全域紀律規定該降級有條件：高風險項目不得就此結案，外部審恢復後必須補審。

2026-09-07 補派的獨立 Codex review 回報 ⛔ Blocked，指出 5 個 P1 correctness 缺陷；逐條回原始碼查證後**五條全部成立、無誤報**。其中兩條屬同一形態：check 12 自稱驗 "1:1" 實際只驗集合相等、check 9 自稱驗必要欄位實際只驗非空——症狀是「一切正常」，驗證全過而無人抗議。

現在處理的理由是這批缺陷正擋在 push / PR 之前：一旦 v2 發版，採用者會依這些檢查判定自己的證據合格，而檢查其實放行了不合格的形狀。

## What Changes

**check 12 — tasks.md ↔ plan.md 對應**
- From: 收集兩邊 key 後直接做集合雙向比較
- To: 兩邊 key 先各自保證無重複，再做集合相等；`duplicate → BLOCK`、`unique + same set → PASS`
- Reason: 集合會吃掉重複——`tasks.md` 兩個 `1.1` 對上 `plan.md` 一個 `1.1` 會通過，但實際有任務沒有自己的契約條目
- Impact: 破壞性（原本會過的重複編號輸入將 BLOCK），影響所有採用者

**checks 9–11 — Evidence 決定性語意**
- From: `subject:` 只驗 trim 後非空；每 task 假定僅一組 RED/GREEN；未拒絕重複紀錄與重複欄位
- To: 一 task 可有多個 subject；subject 須合 `file::test` grammar；同 task 內 subject **每一側各自唯一**；每個 subject 恰好一個 RED 與一個 GREEN；多次執行歷史不納入 completion evidence
- Reason: 現況下結構無效或互相衝突的證據可通過，且不同 agent 可得出不同判定——而這組 check 自稱決定性
- Impact: 破壞性；check 11 由「單組配對」重寫為 per-subject 配對

**check 7 — deferred 標記載體**
- From: 掃 `plan.md` 尋找 `[~]` 任務列
- To: 掃現行 carrier `tasks.md`
- Reason: v2 已把任務標記移出 `plan.md`，該檢查在 v2 底下永遠不會觸發（migration 漏改）
- Impact: 非破壞性修復；恢復一道原本失效的檢查

**R1 審查判準 — 以閱讀執行的規則之 RED**
- From: R1 只問「RED 的 `failure:` 是行為失敗、還是 SyntaxError / import / 缺依賴等 harness error」
- To: 加一句：當受測對象是**以閱讀執行的規則**（例如這些 check 本身，在某個 change 修改它們時），RED 記 `INDETERMINATE`、理由是「規則照字面無法裁定此案」，在 R1 下算行為失敗（目標性質＝可裁定性未被滿足），屬刻意而非 malformed
- Reason: 本 change 的 f12 正向對照組 RED 正是這種形狀（`tasks.md` 2.2 的紀錄）。原 R1 只列 code 類 harness error，對「規則讀不出答案」沒有裁定，會讓不同 reviewer 對同一筆 RED 給出不同判定
- Impact: 非破壞性；只影響 review judgement R1（非決定性 check）。`INDETERMINATE` 仍受 check 10 約束：只能出現在 RED 側、永遠不等於 `PASS`、不能替代完成宣稱所需的 GREEN，也不會讓任何 blocking check 通過。此項於 2026-09-10 branch review（r2）指出未宣告後補記；實作已在 e38e817 落地

**canonical spec 自我矛盾**
- From: `tdd-claim-accuracy` 同一份 spec 內，一處說 TDD 走 `tasks.md`、另兩處說走 `plan.md`
- To: 只保留 v2 的單一答案
- Reason: 規範性文件內部互斥會指示未來維護者把 v2 刻意移除的載體裝回去
- Impact: 非破壞性；consistency repair

**CLAUDE.md 跨檔耦合表**
- From: 表中記載 CI 解析 Compatibility 表的 `v1` 列
- To: 更新為現況 `v2`，併同 bundle / schema 版本敘述與已 archive 的 change 路徑
- Reason: CI 已改抓 `v2`，而這張表正是用來防止「改一處漏一處」的機制，它自己漏改了
- Impact: 非破壞性；文件同步（本身可當 regression case）

## Capabilities

### New Capabilities

（無——本 change 不引入新能力，只修既有契約的 correctness 缺陷。）

### Modified Capabilities

- `plan-contract`: check 12 的對應關係由「集合相等」收緊為「無重複 + 集合相等」；並明確 plan.md 不承載任務標記，故檢查不得於其中尋找任務列（check 7 漏改的根因）
- `tdd-evidence-contract`: RED/GREEN 證據由「每 task 一組」改為「每 subject 一組」，並加上 subject grammar、同 task 內**每側**唯一性、cardinality 三項結構要求；同時明文界定 checker 只驗結構／格式／cardinality，不宣稱驗證 evidence truth；並在 R1 判準下承認「以閱讀執行的規則」之 `INDETERMINATE` RED 為行為失敗（不等於 PASS、不能替代 GREEN）
  - 措辭修訂（2026-09-11，Codex branch review）：上面兩處原寫「同 task 內 subject 唯一」，與「RED 與 GREEN 共用同一個 subject」字面衝突。依 `specs/tdd-evidence-contract/spec.md:7` 的現行條文收斂為「每一側各自唯一」。
- `tdd-claim-accuracy`: 修掉兩處仍宣稱 TDD 經由 `plan.md` 傳遞的 stale clause

## Impact

- `superpowers-bridge/schema.yaml`——checks 2、7、9、10、11、12 的判定文字（schema major 已是 2，本次為契約收緊，需評估是否再 bump）
  - check 2 為 2026-09-11 追加的 bounded scope extension（Codex branch review r1 的 P1）：原文要求每個 checkbox 必須是 `- [x]`，與 check 7「一個已完整交代的 `- [~]` 延後任務不阻擋、Overall Decision 維持 PASS」直接衝突，同一行 task 兩個執行者會得到相反判定。改為接受 `- [x]` 或 `- [~]`，並明寫 `- [~]` 屬 check 7 定義的 DEFERRED TASK、其交代是否充分由 check 7 判。納入本 change 的理由：verifier 自我矛盾直接傷害「可重現驗證」這個本 change 的核心宣稱；其餘同族的作者表面缺口維持延後、不隨之吸收。
- `superpowers-bridge/templates/verify.md`、`templates/tasks.md`——與上述檢查連動的模板段落
- `superpowers-bridge/README.md` 與 `README.zh-TW.md`——checks 8–12 的說明段落（雙語同步）
- `openspec/specs/tdd-claim-accuracy/spec.md`——stale clause 修復
- `CLAUDE.md`——跨檔耦合表與版本敘述
- `openspec/changes/archive/2026-09-04-loosen-plan/errata.md`——僅追加一條 pointer，原 verify / retrospective 一字不改
- mutation fixtures——需補 duplicate-task、duplicate-entry、invalid-subject、duplicate-record 等正負案例
- 採用者：check 12 與 checks 9–11 的收緊屬破壞性，需在 README 說明遷移方式
