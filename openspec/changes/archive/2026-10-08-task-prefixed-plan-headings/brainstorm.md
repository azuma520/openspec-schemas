<!--
Raw capture of superpowers:brainstorming output.
2026-10-07 session（15:30 之後的開工 session）對話的決策紀錄。brainstorming skill（Superpowers 6.4.1，
實際載入路徑 claude-plugins-official/superpowers/6.4.1）分類為 architectural：改動別人依賴的格式
（Plan Contract 條目標題）並 bump schema major。逐題問答、逐段設計皆經使用者同意。
使用者的裁定多以「貼上整段回覆」形式給出（memory feedback_pasted_rulings_are_user_replies）。
-->

# Brainstorm — task-prefixed-plan-headings

> **本 change 的一句話**：Plan Contract 的條目標題改以 `## Task <編號> — <標題>` 為建議寫法，
> 讓上游 SDD 的 `task-brief` 能直接抽取；舊寫法 `## <編號> —` 無期限繼續接受；
> check 12 改為以正面方式認條目並跳過 ``` 區塊；schema major 3 → 4。

---

## 一、背景與起點（已定案，本 session 不重議）

- 來源工作：`task-20261002-task-brief-heading-compat`（地圖狀態 NEXT）。
- 決策紀錄與實測：`docs/superpowers/poc/2026-10-07-task-brief-heading-compat/report.md`（以下稱 poc 報告）。
- 已定案（2026-10-07 使用者裁定，依據見 poc 報告「結論」「版本號」「不新增的規則」三節）：
  - 採 C′；不做轉接層（B）、不改本機上游副本、不發上游 PR（D）。
  - schema major 3 → 4。理由：Plan Contract 原文（`schema.yaml` 第 396–398 行）明文承認「不以數字開頭的
    `##` 不是條目」，故 v3 下 `## Task 3 備註` 合法；新增 `Task` 形式必然重新解讀這類標題。
  - 上游 selector 的兩個問題（最後一項吞尾段、整數／三層編號多抓）只寫建議、不加會擋人的檢查。
- 上游 `task-brief` 原文（本機 6.4.1，`scripts/task-brief` 第 30–36 行）：
  - 以 `^#+[ \t]+Task[ \t]+[0-9]+` 判定任務邊界；任務範圍只在**下一個 Task 標題**結束，遇其他標題不停。
  - 選取條件 `^#+[ \t]+Task[ \t]+` + n + `([^0-9]|$)`，n 直接拼進 regex（`.` 可配任意字元）。
  - 只把**行首**的 ``` 視為程式碼區塊切換；不認 `~~~`、不認縮排的 ```。
- 開工時查到的事實：
  - adopters 兩份 fragment 沒有提到標題格式（poc 報告「未查」一項結案，本 change 不改它們）。
  - repo 目前沒有任何 git tag（`git tag` 空）。
  - 本 repo 所有 `plan.md` 的 ``` / `~~~` 區塊內，沒有任何 `##` 開頭的行。
  - check 13（`schema.yaml` 第 935–943 行）**刻意不認** Markdown 結構：區塊內的標題形狀行照算，
    再與 CLI 計數比對；schema 中目前沒有任何「程式碼區塊」的定義可沿用。

---

## 二、決策鏈

### Q1 舊寫法 `## 1.1 —` 接受到什麼時候？ → **A′**

選項：A 一直接受／B 下一個 major 移除／C 這版就只認 Task。

裁定：**A′**——舊格式無期限保留為 legacy-compatible syntax；v4 起 `## Task …` 是唯一 canonical /
recommended syntax；不預先承諾某個 major 移除舊格式。

- **沒有期限，但有重議判準**（只是將來重議時的理由，不是任何人在守的機制）：雙語法明顯增加
  checker／tooling 複雜度；造成實際誤用或錯誤率；其他新能力只能建立在 Task syntax 上；維護兩種格式
  開始產生持續成本。
- **三層要分開講**：accepted syntax ≠ canonical syntax ≠ interoperability level。
  - canonical：`## Task <編號> …`
  - legacy accepted：`## <編號> …`
  - upstream SDD `task-brief` 可辨識：只有 canonical form
- check 12 的職責是 Plan Contract 的 1:1 對應，**不替 `task-brief` 做相容性執法**；
  C 會把「Bridge 認為 plan 合不合法」與「上游某個 helper 能不能處理它」混在一起。
- **遷移說明定稿文字**（修正過一次：原稿「完全不用遷移」說過頭，與升版理由自相矛盾）：
  > 既有 plan 一般不需遷移，舊的 `## <編號> —` 條目標題仍有效。需要檢查的例外是：原本作為非條目
  > 使用、但標題以 `## Task <數字>` 開頭的 H2；v4 會把它解讀成條目，因此需要改名。
  > 本 repo 已確認沒有此類既有標題。
- 連動：Plan Contract 現有理由「key must LEAD so the keys are readable without interpretation」要改寫，
  否則規則與理由自相矛盾。

### Q2 完整 SDD 流程實測拿哪份計畫跑？ → **A（自己吃自己）**

選項：A 本 change 自己的 plan.md／B 另造測試計畫／C 兩者都做。

裁定：**A**。定位是 **integration acceptance test**，不是 parser unit test；parser 邊角已由 poc
（`raw/output.txt` 第 3 段）覆蓋，不另造第二份完整測試計畫。

- 本 change 的 plan.md 一開始就用 `## Task` 寫法，**至少兩個 task**。
- apply 時照 SDD 原文跑**實際載入的那版**上游 `task-brief`，並記下版本。
- **至少一個非最後一項**：抽出的簡報與 plan 中該條目原文**逐行相同**。不把 `rc=0` 當成內容正確的證據
  （上游抽錯也是 rc=0）。
- 最後一項若吞入其後的合法非條目 H2，明記為上游已知限制。
- 執行子代理與審查子代理只拿同一份簡報做事，留紀錄。
- `sdd-workspace` 工作目錄命名由**計畫檔檔名**決定，與標題寫法無因果關係：留執行紀錄，但**不宣稱**
  為本次驗證到的性質（claim–oracle 對齊）。
- 時序：apply 階段的 `task-brief` 是上游腳本、與 schema 無關，schema 改完前即可實測；新版 check 12
  對本 plan 的判定只能在 schema 改完並同步 `openspec/schemas/` 副本後的 verify 階段取得。

### Q3 check 12 怎麼認 Task 寫法？ → **A（安全子集）**

選項：A `Task` 照上游、編號照 Bridge 既有規則／B `task` 不分大小寫／C 強制完整 `## Task <編號> — 標題`。

裁定：**A**。原則：

> 對新增的 `Task` syntax，Bridge 接受的語言是上游 `task-brief` 可辨識語言的安全子集；
> Bridge 既有的 entry-number grammar 保持不變；不反向照抄上游的寬鬆 parser。

- 只認 `##`（Plan Contract 本來就是 H2 entry）；`Task` 大小寫精確一致；`Task` 後一個以上 space/tab；
  編號 `\d+(\.\d+)*`；編號後須為 whitespace 或行尾（`## Task 1.1a` 不是條目，與 `## 1.1a` 同理）。
- B 會重現本 change 要消滅的缺口（Bridge PASS、上游找不到）；C 把「推薦怎麼寫」與「最低合法語法」混淆。
- **「安全子集」的保證範圍（修正過一次）**：只保證 **recognition**——凡 Bridge 合法的 `Task` 條目標題，
  上游都辨識得到；**不保證 exact extraction**——上游 selector 不是精確的 Plan Contract parser，不能從
  「辨識得到」推導「一定只抽到該 entry」。已知會抽錯範圍的情況（2026-10-07 審查後補完）：
  - 編號碰撞：要 `1.1` 會連 `## Task 101` 一起抽（regex 的 `.` 配任意字元；審查時 Fable 實測確認）。
  - 整數編號：要 `1` 會抽到所有 `1.x`。
  - 最後一項：其後的非條目段落一起被抽入。
  - **canonical 後接 legacy**（Codex 審查發現）：上游只把 `Task <數字>` 當邊界，`## Task 1.1` 之後的
    `## 1.2` 不會終止 1.1 的抽取，整個 1.2 被一起抽入。
  - **長得像 Task 的非條目 H2**（Fable 審查、實測）：`## Task 1.1a 備註` 在 Bridge 是合法非條目，在上游
    卻是任務邊界——會截斷前一項，且要 `1.1` 時會被一併抽入（`1.1([^0-9]|$)` 配到 `a`）。

  這也是 Q2 證據必須比對內容的原因。對應的寫法建議見第一段 guidance。
- 非條目的定義改為**正面表述**：只有符合 legacy numeric entry pattern 或 canonical `Task <number>`
  entry pattern 的 H2 才是 entry；其他 H2 是 non-entry section。

### Q3a 程式碼區塊要不要納入本 change？ → **納入**

起因：上游不把 ``` 內的行當成標題（判任務邊界時略過；但在已選中的任務範圍內，區塊內容照樣被抽出），check 12 對 ``` 一字未提，``` 內的 `## Task 1.1 —` 可能被 check 12 算成
條目、上游卻看不到——違反「安全子集」。

裁定：納入本 change。上位理由是 Markdown 結構語意（程式碼裡寫著 `## Task 1.1 —` 不應改變 plan 的
任務結構），上游行為只是剛好提供了 interoperability 的理由。

- **不宣稱 backward-compatible**（修正過一次：原稿說「不影響相容性」說過頭）。v3 條文沒提到
  程式碼區塊，照字面讀（「每個 `##` 標題」）會把區塊內的標題收為鍵——可能有舊 plan 靠此剛好通過或
  被擋；v4 改為跳過，列為 v4 行為變更。（再修正一次：原稿寫「v3 未定義」，與第四段測試表中 v3 的
  確定判定矛盾，Fable 審查指出。）本 repo 查過無此情況，
  只支持「本 repo 遷移風險為零」，不推及外部。

---

## 三、分段設計（四段，逐段經使用者同意）

### 第一段 Plan Contract 的 v4 寫法（通過，附 fence 收斂）

- 條目標題 = 同時符合：①不在 Plan 所認定的程式碼區塊內 ②行首剛好 `##` 接空白 ③文字為 canonical
  `Task` + 1+ space/tab + 編號 + (whitespace|EOL)，或 legacy 編號 + (whitespace|EOL)。其他 `##` 都是非條目。
- **程式碼區塊（使用者收斂）**：v4 只把**行首、未縮排的 backtick fenced block** 視為結構掃描要忽略的
  區域；`~~~` 與縮排 fence **不在 v4 的結構排除保證內**。理由：取 Bridge 與上游能力的交集——若 Bridge
  忽略 `~~~` 內的 `## Task 1.1` 而上游拿它切 brief，等於剛修完一個 parser 差異又主動留下另一個。
  Plan Contract 是機器可讀契約，可以比 Markdown 更窄、更可預測，不擴成 CommonMark parser。
  （AI 原建議連 `~~~` 一起認，使用者選了更窄、與上游一致的版本。）
- **措辭用語意、不綁演算法**：「在 Plan 結構辨識時，位於行首未縮排的 backtick fenced code block 內之
  heading-like text 不構成 entry。」開關判定的細節放在 check 12。
- 理由改寫：「編號要擺在最前面，或只接在固定字 `Task` 後面，讓鍵值不需語意解讀即可辨識。」
- guidance（**全部不進 validation**；Bridge 不因上游 parser 的缺陷收緊原本合法的 Plan Contract，但要取得
  SDD `task-brief` interoperability 的人，要清楚知道哪種寫法才安全）：
  - 「新寫或修改的 plan 建議使用 `Task` 寫法，因為這是 Bridge 定義、且可被上游 SDD `task-brief` 辨識的
    canonical form。」（使用者修正：不可寫「上游只認這種」——上游其實接受更寬的形式，那會把上游能力說窄。）
  - 以下三句於 2026-10-07 審查後定稿（使用者裁定，對應 Q3 補完的抽取限制）：
    1. 若 plan 要交給上游 SDD `task-brief`，整份 task entry 應統一使用 canonical `## Task <編號> …`。
       新舊混用在 Plan Contract 仍合法，但上游不把 legacy `## <編號> …` 視為下一個任務邊界，可能把後續
       舊格式 task 一起抽入 brief。
    2. 非條目 H2 不應以 `Task <數字>` 開頭。`## Task 1.1a 備註` 在 Bridge 是合法非條目，但上游較寬鬆的
       selector 會把它當任務邊界，造成抽取範圍被截斷或污染。
    3. 非條目段落（如 self-review）建議放在第一個 task entry 之前，避免最後一項沒有下一個 Task 邊界時
       把尾段一起抽入。
- 模板 `templates/plan.md` 三個條目標題改為 `## Task 1.1 — …`、`## Task 1.2 — …`、`## Task 2.1 — …`；
  第 19–20 行附近的註解「entry key 必須放在每個 `##` heading 最前面…verify 讀的就是這個位置」同步改為
  接受固定 `Task` 前綴、前綴不屬於 key（Codex 審查發現：只改標題會留下互相矛盾的作者指引）。
- 刻意不做：不鎖 `x.y`、不強制 `—`、不修上游 selector 的編號碰撞／最後項問題。

### 第二段 check 12（通過，提示選 A）

- check 12 的責任不變：建立 plan entry key set，再與 tasks.md 比對；**v4 只改「plan 裡哪些行可以產生
  entry key」**。
- plan 側收集：逐行掃；行首三字元為 ``` 的行切換區塊狀態，該行與區塊內各行都不收；區塊外符合第一段
  條目定義者收集**編號**為鍵值（`Task` 前綴只用來辨認、不進鍵值）。
- 第一階段（重複）與第二階段（集合比對）、不提前結束、訊息格式**全部不改**。
- 自然結果，寫進說明：
  - 同一份 plan 可混用新舊寫法（合法；但要走上游 SDD 時不建議，見第一段 guidance 1）；`## Task 1.1` 與 `## 1.1` 並存 = 鍵值 `1.1` 重複，第一階段擋下。
    syntax 不是 identity 的一部分。
  - 區塊未關閉 → 其後條目都收不到 → 第二階段報缺鍵擋下；上游同樣抽不到，兩邊一致。
    這是 diagnostics 問題，不是 correctness 問題，不另設「fence 沒關」錯誤。
- **提示選 A：不加近似格式提示**。原則：不要為了更友善的錯誤訊息，偷偷建立第二套「近似 parser」
  （`task`？`TASK`？`### Task`？`## Tasks 1.1`？）。作者讀得懂錯在哪，屬既有工作「作者表面與 Gate
  規則對齊」的範圍。
- **check 12 與 check 13 的區塊不對稱**：本來就沒有可沿用的定義（check 13 刻意不認結構）。兩處都要寫
  rationale：check 12 忽略區塊，因為它判斷 Plan entry structure、需與 SDD task extraction 的結構語意對齊；
  check 13 不忽略，因為它要與 CLI 的表面計數比對。此差異為刻意設計，**不應被「好心統一」**。
  check 13 本身不改。
- **tasks.md 側不改**：它收任務行時本就不處理區塊（作者表面工作已記錄此潛在歧義）。寫明「本次只改
  plan-side entry recognition；tasks-side parsing 維持現況，其 fence semantics 不在本次 scope」。

### 第三段 版本與遷移（通過）

必改（照 CLAUDE.md 跨檔耦合表）：

- `schema.yaml` `version: 3` → `4`；`VERSION` `3.0.0` → `4.0.0`。
- bridge README（en + zh-TW）：開頭 `Schema version: v3`；第 117 行附近「Crossing a schema major does need
  migration」段補 v3 → v4 一句；Versioning 表 `schema.yaml: version: 3` 那列（約第 485 行）與「A bundle
  release `3.x.y` is a published cut of schema major `v3`」（約第 488 行）；Versioning 新增「Why v3 → v4 is a
  schema-major bump」「Migrating v3 → v4」、版本歷史一條；Compatibility 表最上方新增 `v4` 列（`v3` 列保留）；
  S11 列與「後續狀態」段；徽章若隨之變動一併處理。（README 第 117、485、488 行由 Fable 審查補列。）
- `.github/workflows/version-check.yml`：`grep -E '^\| v3 \|'` → `v4`（否則 CI fail）。
- repo `CLAUDE.md`：第 32 行附近結構樹註解「bundle SemVer(3.0.0)…version: 3」、「兩個版本號別搞混」表、
  跨檔耦合表等寫死 `version: 3` / `v3` / `3.x.y` 的段落。
- `docs/roadmap.md`（+ zh-TW）：連動表要求核對，**未讀**，design 階段核對。

遷移說明：Q1 定稿文字 + Q3a 的 ``` 行為變更（「check 12 現在跳過 ``` 區塊內的標題；原本靠區塊內假標題
才通過的計畫會變成不通過；本 repo 已查過無此情況」）。

**Compatibility 基準（經兩輪討論）**：

- 第一輪選「維持 v5.1.0，另寫實測環境」。使用者隨後重開：為什麼不用新版？
- AI 查證的事實（`superpowers-bridge/README.md`）：
  - 第 595–608 行：10/02 以 6.4.2 對 18 項依賴，6 項不成立。S11 由本 change 修、S13 已於 10/06 修；
    **S4、S5（brainstorming 三路徑漂移）未修**；S12、S14 未查到後續處理。README 原文：把基準提到 6.x
    等於重新宣稱這些說法成立。
  - 第 624 行：自 v1 列 2026-05-11 起沒有重跑過完整流程——v2、v3 都在 6.x 上開發，**5.1.0 對 v2 以後
    的 schema 從未驗證過**。
  - Compatibility 表以 schema major 為列鍵；10/02 OpenSpec 1.3.1 → 1.14.0 是**直接改 v3 列**、未升 major。
    所以以後轉到 6.x 不需要再破壞一次相容。
  - 上游最新 release：v6.4.2（2026-09-25，`gh release list`）。
  - 本 session 沒有在任何版本上跑過完整流程：6.4.1 只有 poc 的 `task-brief` 解析實測；6.4.2 只做了
    `task-brief` 檔案比對（與 6.4.1 相同），沒有跑。
- 使用者確認外部採用者為零 → 沒有產品理由繼續投資 5.1.0。
- **裁定**：
  - 本 change **不改基準值**。`version-check.yml` 以 awk 讀第 4 個反引號欄位，該格必須是反引號版本號，
    所以 v4 列機械欄位仍填 `v5.1.0`；**說明寫在表格下方**（如現有的 `>` 註記），不寫進該列格子——格子裡
    多一個反引號會位移 awk 讀到的第 4 個欄位（Fable 審查指出）。說明內容：沿用的歷史宣告，v2 起未在
    5.1.0 重跑，目前無採用者、不再投資重新驗證，**不構成相容保證**；目前已知的本次 PoC 實測環境為
    Superpowers 6.4.1；C′ dogfood 的實際驗證版本以執行當下實際載入的版本為準並留下紀錄，**完成前不得寫
    「已完整驗證」**（使用者審閱時收窄：原稿寫「實際開發與驗證環境為 6.4.1」，與 Q2「跑實際載入的那版
    並記下版本」不一致）；轉到 6.x 的工作另行登記，完成完整流程後直接改 v4 列。
  - 每週落後檢查會持續提醒（6.4.2 ≠ 5.1.0）——符合真實狀態。
  - 另登記 `task-20261007-superpowers-6x-rebaseline`（TODO，掛在 `task-20260826-superpowers-bridge-next-gen`
    底下）：以能力契約重新檢視 6.x，對齊 S4、S5、S12、S14（S4/S5 沿用 `task-20260826-fix-brainstorming-drift`；
    S12、S14 開工第一步先查是否已有工作），C′ 完成後納入其 S11 證據，完成整體相容性驗證後更新 v4 列基準。
  - **版本策略原則**（寫在該工作裡，不另立規範）：能力契約是目標，版本是手段；先看能力契約，再決定
    upstream 版本；優先使用「已驗證的新能力」≠ 追最新版；向下相容是成本約束，不是架構方向。

**退回方式（rollback）→ A′**：

- 事實：repo 沒有任何 tag，既有兩份遷移說明分別寫「pin bundle `2.x.y`」（v2 → v3）與「pin bundle
  `1.0.1`」（v1 → v2），照著做都會失敗。（原稿把兩份都寫成 `2.x.y`，Fable 審查更正。）
- 裁定：v3 → v4 遷移的退回說明指向**最後一個 v3 狀態的 immutable commit SHA**，不引用不存在的
  `3.x.y` tag。定義：**第一個把 `schema.yaml` 改成 `version: 4` 的 commit 的 parent**（change 會分多個
  commit，不能直接說「change commit 的 parent」）。SHA 在文件定稿時填入；歷史若被改寫要重填
  （本 repo 直推 fork main、不 squash，風險低，但說明要寫）。
- 舊兩份遷移說明的同類問題：**記為觀察，不在本 change 修**。
- `v3.0.0` tag 是否補打：release 決策，不進本 change。

### 第四段 驗證（通過，選 A：agent-mediated mutation tests）

**一、變異測試資料**（沿用 `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/`，
編號接續；RED 定義沿用 `fix-v2-blocking-defects`：照改前原文判定是錯的）

| 測試資料 | 內容 | v3 判定 | v4 預期 | 性質 |
|---|---|---|---|---|
| 程式碼區塊排除 | 舊寫法 `## 1.1`、``` 內 `## 9.9`、`## 1.2`；tasks `{1.1, 1.2}` | BLOCK（多 `9.9`） | PASS | RED→GREEN（只測區塊排除） |
| 新寫法辨認 | `## Task 1.1`、`## Task 1.2`；tasks `{1.1, 1.2}` | BLOCK（收不到鍵） | PASS | RED→GREEN（只測 Task 辨認） |
| 新舊同鍵值 | `## Task 1.1` 與 `## 1.1` 並存 | PASS（v3 不認 Task 行，錯） | BLOCK：`1.1` occurs more than once in plan.md | RED→GREEN |
| 舊非條目被重新解讀 | tasks `{1.1}`；plan `## 1.1` + `## Task 3 備註` | PASS | BLOCK（多 `3`） | 非 TDD，把破壞相容具體化（對應 Q1 遷移例外） |
| 寫錯格式不算條目 | `## task 1.1`、`### Task 1.1`、`## Task 1.1a` | BLOCK | BLOCK（缺 `1.1`） | 防規則放太寬的回歸測試；v3 已判對，**不是 RED、不冒充 TDD 證據** |
| 綜合 | Task 寫法 + ``` 內 `## Task 9.9` | — | PASS，鍵值只有 `1.1, 1.2` | 只要求 v4 判定正確 |

拆分理由：若只用一份「Task 寫法 + 區塊」資料，v3 的失敗原因是「不認 Task」而非「沒排除區塊」——RED
紅錯原因。一個 RED 只證明一個缺陷。

執行方式與證據規格（使用者補強）：

- oracle = **frozen fixtures + 預先寫死的預期結果**；Agent 是被測的 executor。
- Agent 不只回 PASS/FAIL，要回報**中間值**：plan 收到哪些 entry keys、tasks 收到哪些 keys、是否重複、
  集合差在哪——讓審查者判斷它是不是碰巧猜對。
- **測試 Agent 不預先看到預期答案**：先給 fixture + check 12 產生判定，再由另一層拿結果與 frozen oracle 比。
  （待 plan 階段確認：既有 fixtures 目錄的 README 是否寫有預期判定——若有，不可交給測試 Agent。）
- 腳本可做**機械輔助**（驗 fixture 未被改、記 hash、批次餵案例、收集輸出、actual vs expected 機械比對），
  **不實作 check 12 本身**。
- 不另寫 parser 腳本（B）的理由：要驗的是「Agent 讀到 check 12 原文後會不會照規則得到正確結論」；
  腳本全綠只證明腳本實作了我們對 check 12 的理解，可能出現「腳本全綠、Agent 解讀錯」——驗錯對象。
- 證據名稱照實：**instruction-layer 的行為證據**，非程式自動測試（check 12 本身就是 agent 執行的說明文字）。

**二、自己吃自己的完整流程實跑**：見 Q2。

**三、同步後跑 verify**：schema 改完、同步 `openspec/schemas/` 副本後，用新版 check 12 驗本 change 自己的 plan。

**四、結構驗證**：`openspec schema validate`、`openspec schemas`、CI；模板三個標題以 grep 確認已改為 Task 寫法。
**必驗**（使用者審閱時由「待確認」改列此處——它不是未知問題）：`version-check.yml` 改抓 `v4` 後，
`Read pinned versions` step 要抓得到 v4 列、並讀出正確的 OpenSpec 與 Superpowers 兩個版本號。

**五、沿用 poc、不重跑**：整數編號多抓、最後一項吞尾段——照 poc 報告引用；`101` 撞 `1.1` 原為 regex
推得、未實測，本次審查時 Fable 以上游 6.4.1 `task-brief` 實測確認。

---

## 四、範圍外（明確不做）

- 不改上游、不發上游 PR、不做轉接層。
- 不修上游 selector 的編號碰撞／整數多抓／最後項吞尾段／不認 legacy 邊界／把 Task-like 非條目當邊界；
  只在 guidance 寫明。
- 不加近似格式提示（作者表面工作的範圍）。
- 不改 check 13；不改 tasks.md 側的區塊語意。
- 不改 Superpowers 基準值；6.x 轉換另有工作 `task-20261007-superpowers-6x-rebaseline`。
- 不補打 `v3.0.0` tag（release 決策）；不修舊兩份遷移說明的 rollback 寫法（記觀察）。
- 不改 adopters fragment（查證無標題格式內容）。

## 五、未查 / 待後續階段確認

- `docs/roadmap.md` 是否需要連動：未讀，design 階段核對。
- S12、S14 是否已有工作處理：未查，屬 `task-20261007-superpowers-6x-rebaseline` 第一步。
- 既有 fixtures 目錄是否含預期判定（影響「測試 Agent 不看答案」的實作）：plan 階段確認。
- 「寫錯格式」那份測試資料是否拆成三份（各一種錯法）：plan 階段決定。
- `sdd-workspace` 在 Git Bash 印 `/tmp/...` 路徑、Windows 子代理讀檔工具能否直接讀：poc 報告列為未測，
  dogfood 時會實際碰到。
- 只在 Claude Code 上測；其他平台未測。
- **dogfood 實際載入的 Superpowers 版本**：執行時確認並固定到證據裡（避免設計寫 6.4.1、實跑卻是更新版、
  文件沿用舊版本號）。
- **v3 退回用 SHA**：commit 邊界確定後填入，並實際 `git checkout` 一次確認可用；屬實作／定稿時必須結掉的
  待辦，不得留下 placeholder 或錯 SHA。
