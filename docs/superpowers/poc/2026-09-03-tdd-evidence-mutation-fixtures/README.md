# TDD 證據契約——變異 fixtures（2026-09-03）

> 由 change `loosen-plan`（已 archive：[`openspec/changes/archive/2026-09-04-loosen-plan/`](../../../../openspec/changes/archive/2026-09-04-loosen-plan/)）的變異測試產出。
> 該 change 的 `verify.md` §8.2 記錄了這批 fixture 的判定結果，並以「Fixture contents, verbatim」一節複述內容——但那個標題名不副實。把該節每個 code block 的字元數對上本目錄 `tasks.md` 的實際字元數，**七個裡只有 f1 是真正逐字完整的**：
>
> | Fixture | §8.2 複述 | 實際 `tasks.md` | 比例 |
> |---|---|---|---|
> | f1 | 336 | 336 | **100%** |
> | f7 | 278 | 373 | 75% |
> | f2 | 188 | 281 | 67% |
> | f6 | 151 | 378 | 40% |
> | f3 | 139 | 366 | 38% |
> | f4 | 130 | 368 | 35% |
> | **f5** | **無 code block** | 209 | **0%** |
>
> 上表只量 code block 內容，這是「逐字」這個宣稱該用的基準；各 block 前後的**敘述文字另外攜帶了百分比不涵蓋的資訊**（最明顯的是 f2 的「(task 1 has RED only; task 2 annotated `n/a — prose/doc-only`)」，那句話用文字講出了它那 67% 漏掉的東西）。所以 35% 不等於「§8.2 只告訴你 f4 的三分之一」。
>
> 另外**沒有任何 fixture 的 `plan.md` 被以檔案形式複述**（整節只有兩行提到它：`:232` 的 f1 與 `:278` 的 f5）——而 f5 的違規**正是** `plan.md` 的 entry key，也就是它唯一的受測物剛好是該節完全沒有複製的那一個。本目錄保存的是**可直接重跑的檔案本體**。
>
> **保存理由。** fixtures 原本只存在於 git-ignored 的 SDD 工作區（`.superpowers/`），該工作區在 branch 收尾時刪除。上表就是理由本身：那份複述**大多不完整、且對 f5 等於沒有**，就算完整也還是報告裡的 markdown 而非可餵給重跑者的檔案。**它們是唯一能證明「檢查 8–12 真的抓得到違規」的資產**：宣稱一條檢查守住 X，就要能當場把 X 破壞掉跑一次。
> 保留範圍由使用者裁定（2026-09-04）：只留可重跑的最小必要資產，session reports / scratch / 中間產物不留。
>
> **姊妹目錄**（[`../2026-09-03-plan-contract-producer-smoke/`](../2026-09-03-plan-contract-producer-smoke/)）：
>
> | 資產 | 驗的是 |
> |---|---|
> | 本目錄 | 檢查器**會不會判對**（消費端） |
> | producer smoke | Plan Contract 產出器**會不會產對**（產出端） |

## 這批 fixture 在測什麼

`superpowers-bridge` schema v2 的 verify 指令帶有五條決定性檢查（deterministic checks 8–12），對 `tasks.md` 的 TDD 標註與 RED/GREEN 證據、以及 `tasks.md` ↔ `plan.md` 的任務編號集合做結構檢查。每個 fixture 是一組自足的 `tasks.md` + `plan.md`，**只破壞一件事**。

| Fixture | 破壞的東西 | 應得判定 |
|---|---|---|
| `f1-missing-annotation` | 任務 2 沒有 `TDD:` 標註 | check 8 BLOCK |
| `f2-missing-green` | 任務 1 是 applicable、有 RED 沒 GREEN | check 9 BLOCK（連帶 check 11 stage two：RED 側有該 subject、GREEN 側集合為空，兩側集合不相等）——`f2` 是這批裡刻意的例外,**同時**觸發兩條檢查，不是單一檢查的獨立樣本 |
| `f3-pass-marker-on-red` | RED 的 `outcome` 寫成 `PASS` | check 10 BLOCK |
| `f4-subject-mismatch` | RED 指 `auth.test.js`、GREEN 指 `signup.test.js` | check 11 BLOCK |
| `f5-key-set-mismatch` | tasks `{1,2,3}` 對 plan `{1,2,9}`（**數量相同、集合不同**） | check 12 BLOCK |
| `f6-syntaxerror-red` | RED 的 outcome 是 `ERROR`（SyntaxError），不是行為失敗 | **決定性檢查不 BLOCK**——check 10 形式上通過（`ERROR` 是合法的非 `PASS` 標記），只有 review judgement R1 抓得到 |
| `f7-blank-spaced-record` | **沒有破壞任何東西**——欄位之間夾空行的合規紀錄 | 不 BLOCK（正向對照） |
| `f8-duplicate-task-number` | `tasks.md` 裡任務編號 `1.1` 出現兩次（兩個不同任務共用同一個編號） | check 12 BLOCK，具名重複鍵 `1.1` |
| `f9-duplicate-plan-key` | `plan.md` 裡 `## 2.3` 這個 entry key 出現兩次 | check 12 BLOCK，具名重複鍵 `2.3` |
| `f10-subject-without-separator` | RED/GREEN 的 `subject:` 只有測試名、沒有 `::` 分隔符與檔案路徑 | check 9（`subject:` 語法）BLOCK |
| `f11-duplicate-subject-one-side` | 同一任務下兩筆 RED 記錄的 `subject:` 值逐字相同（GREEN 只有一筆） | check 11（per-subject 唯一性／cardinality）BLOCK |
| `f12-two-subjects-paired` | **沒有破壞任何東西**——同一任務下兩個不同 `subject:`，各自完整配對一組 RED＋GREEN | 不 BLOCK（正向對照） |
| `f13-deferred-task-in-tasks` | `tasks.md` 有一個 `[~]` deferred 任務、`plan.md` 為一個沒有任務列的合規 v2 entry | 兩種讀法皆不 BLOCK,BLOCK/不 BLOCK 無法區分——改記有鑑別力的結果:現行 check 7(讀 `tasks.md`)找到**1 筆** deferred 任務、需列入 §7;舊 check 7(讀 `plan.md` 找 `[~]` 列)找到 **0 筆**、合法留空 §7(舊測 BLOCK 條件「§7 空且 `plan.md` 有 `[~]` 列」不成立;新測條件「§7 空且 `tasks.md` 有 deferred 任務」因 §7 非空也不成立)。這個 fixture 驗的是讀哪個檔、找到幾筆,不是 BLOCK 與否。**check 2 的預期判定（2026-09-14 追加）**:修訂後的 check 2 接受 `- [x]` 或 `- [~]`,所以本 fixture 的 `[~]` 任務**不使 check 2 失敗**;修訂前的 check 2 要求每個 checkbox 皆為 `- [x]`,同一份輸入會失敗——這是本 fixture 對 check 2 修訂的鑑別力所在。⚠️ 此列為**作者推導**、尚未經獨立執行者複驗:2026-09-08 的獨立再推導只實作 checks 8–12,不涵蓋 check 2 |
| `f14-fenced-heading-not-entry` | `plan.md` 在行首 ``` 區塊內有 `## 9.9`，區塊外是 `## 1.1`、`## 1.2`；tasks `{1.1, 1.2}`（舊式編號標題，不用 Task 寫法） | **v3**：BLOCK，check 12 第二階段（plan 多 `9.9`，因為 v3 條文收每個 `##` 標題）；**v4**：PASS（區塊內標題不收，plan 鍵 `1.1, 1.2`）。性質：RED→GREEN |
| `f15-task-form-entry` | `plan.md` 的條目寫成 `## Task 1.1 — …`、`## Task 1.2 — …`（沒有程式碼區塊）；tasks `{1.1, 1.2}` | **v3**：BLOCK，check 12 第二階段（`Task` 不是數字，plan 收不到任何鍵，tasks 的 `1.1`、`1.2` 都缺條目）；**v4**：PASS（鍵 `1.1, 1.2`）。性質：RED→GREEN |
| `f16-task-and-legacy-same-key` | `plan.md` 同時有 `## Task 1.1 — …` 與 `## 1.1 — …`；tasks `{1.1}` | **v3**：PASS（只有 legacy 那行有鍵，鍵 `1.1` 出現一次——這個 PASS 是錯的）；**v4**：BLOCK，check 12 第一階段（`1.1` occurs more than once in plan.md；第二階段兩邊集合相等，無差異）。性質：RED→GREEN |
| `f17-task-number-nonentry-reinterpreted` | `plan.md` 有 `## 1.1 — …` 與原本是非條目段落的 `## Task 3 notes`；tasks `{1.1}` | **v3**：PASS（`Task 3 notes` 不以數字開頭，不是條目）；**v4**：BLOCK，check 12 第二階段（`Task 3` 被讀成條目，鍵 `3` 沒有對應任務）。性質：breaking change（把相容性破壞具體化，非 TDD 證據） |
| `f18-no-space-after-hashes` | `plan.md` 唯一可能的條目是 `##1.1 — …`（`##` 後沒有空白）；tasks `{1.1}` | **v3**：PASS（v3 從 `##` 之後第一個非空白字元讀鍵，收到 `1.1`）；**v4**：BLOCK，check 12 第二階段（`##` 後沒有空白，不是條目，任務 `1.1` 沒有條目）。性質：breaking change |
| `f19-indented-heading` | `plan.md` 唯一可能的條目是 ` ## 1.1 — …`（行首有一個空白）；tasks `{1.1}` | **v3**：PASS（v3 條文沒限定 `##` 在行首，收到 `1.1`）；**v4**：BLOCK，check 12 第二階段（不在行首，不是條目，任務 `1.1` 沒有條目）。性質：breaking change |
| `f20-lowercase-task-heading` | `plan.md` 唯一可能的條目是 `## task 1.1 — …`（小寫 `task`）；tasks `{1.1}` | **v3**：BLOCK，check 12 第二階段（`task` 不是數字，plan 收不到鍵，缺 `1.1`）；**v4**：BLOCK，同階段同訊息（`Task` 大小寫精確，小寫不算，`1.1` 沒有條目）。性質：regression（v3 已判對，不是 RED） |
| `f21-h3-task-heading` | `plan.md` 唯一可能的條目是 `### Task 1.1 — …`（三個 `#`）；tasks `{1.1}` | **v3**：BLOCK，check 12 第二階段（`###` 不是條目，缺 `1.1`）；**v4**：BLOCK，同階段同訊息（`###` 以下仍是條目內的子標題）。性質：regression |
| `f22-task-suffixed-number-heading` | `plan.md` 唯一可能的條目是 `## Task 1.1a — …`（編號後面緊接字母）；tasks `{1.1}` | **v3**：BLOCK，check 12 第二階段（`Task` 不是數字，缺 `1.1`）；**v4**：BLOCK，同階段同訊息（編號後必須是空白或行尾，`1.1a` 不是編號）。性質：regression |
| `f23-task-form-with-fenced-task-heading` | `plan.md` 的 `## Task 1.1`、`## Task 1.2` 之間夾一個行首 ``` 區塊，區塊內是 `## Task 9.9`；tasks `{1.1, 1.2}` | **v3**：不凍結（只要求 v4 判定；照 v3 條文會因 `Task` 不是數字而收不到鍵，BLOCK，但那個失敗原因不是「沒排除區塊」，所以不當作 v3 預期）；**v4**：PASS，plan 鍵只有 `1.1, 1.2`（`9.9` 不收）。性質：positive control（綜合） |

**f14–f23 的設計決定（change `task-prefixed-plan-headings`，D7）。** 每個 fixture 只破壞一件事：`f14` 用舊式編號標題、`f15` 沒有區塊，才能讓 v3 紅的原因只有一個；`f23` 是唯一同時用 Task 寫法與區塊的綜合樣本，只要求 v4 判定正確。
- **「不再是條目」拆成 `f18`、`f19` 兩份**：兩種寫法的 v3 判定都是 PASS、v4 都是 BLOCK；合成一份的話，`1.1` 在 v3 會被收兩次而 BLOCK（第一階段重複），那不是要凍結的 v3 行為。
- **「寫錯格式」拆成 `f20`、`f21`、`f22` 三份，各一種形式**：合成一份的話，若 v4 錯收其中兩種，兩個條目會以重複鍵的 BLOCK 呈現，看起來和預期的 BLOCK（缺 `1.1`）一樣，分辨不出誤收。拆開後每份只有一種形式，錯收就會變 PASS 或訊息不同。
- **`f16` 的 v3 PASS 是「錯的」判定**：RED 的意思沿用 `fix-v2-blocking-defects`——照改前原文判定是錯的。`f14`、`f15`、`f16` 是 RED→GREEN；`f17`–`f19` 是破壞相容的具體化；`f20`–`f22` 是 v3 已判對的回歸；`f23` 是正向對照。
- ⚠️ **`f14`–`f23` 尚未盲測**：預期判定是作者依 `task-prefixed-plan-headings` 的 REQ-4 與 v3 現行條文手推的，還沒有對本 change 無脈絡的執行者在不看答案的情況下跑過。

`f6` 與 `f7` 是這批裡最重要的兩個，理由相反：`f6` 證明「檢查通過 ≠ 判斷通過」，`f7` 證明檢查**不會誤擋合規品**。六個證明「違規會被擋」的 fixture，對「合規不會被誤擋」一句話都沒說——沒有 `f7`，這組防呆就是單向的。`f12` 是 `f7` 之後的第二個正向對照，理由同構：`f10`、`f11` 證明「subject 語法／cardinality 違規會被擋」，但單靠它們無法排除「檢查會不會連合法的雙 subject 配對都一併誤擋」——沒有 `f12`，這條防呆一樣是單向的。

⚠️ **`f8`–`f13` 這六個是目標 change `fix-v2-blocking-defects`（修正措辭後）的行為，且從未進過任何盲測**——見下一節。

## 證據來源：哪幾個是盲測的，哪一個不是

⚠️ **這一節與 archived change 的紀錄有出入，以本節為準。** `f7` 從未進過盲測，但該紀錄有**三處**把它算了進去：`verify.md:202` 的表格（七列全在「Blind agent's verdict」欄下）、`verify.md:197` 的散文（盲測主詞涵蓋那個正向對照）、以及 **`retrospective.md:39`「a seven-fixture mutation exercise run by a blind third party」——在另一個 artifact 裡、而且把數字寫死**。三處都已在 archived change 內以 append-only 更正正式記錄：[`errata.md` E1](../../../../openspec/changes/archive/2026-09-04-loosen-plan/errata.md)（原文不改、只追加）。

⚠️ **本節的依據皆已不可複驗。** 下面兩張表所根據的 `blind/` 目錄、`progress.md` 與 `task-4.1-4.2-report.md`，都在 git-ignored 的 `.superpowers/` 工作區裡，該工作區已於 2026-09-04 依裁定刪除。**表中內容是刪除前當場比對取得的，repo 內沒有留下可回頭核對的副本**——與 `errata.md` 對同一批證據的標記一致。

| Fixture | 判定者 | 依據 |
|---|---|---|
| `f1`–`f6` | **盲測 agent**（對本 change 無脈絡） | 六個 fixture 以中性名稱 `case-A`..`case-F` 打亂後交付（原名如 `f1-missing-annotation` 含答案，照原名跑等於沒跑）。結果 6/6 正確、零歧義 |
| `f7` | **作者判定 + 一次針對性複審** | `f7` 是實作者在修正第 2 輪**未經要求自行補上**的，時間晚於盲測。針對性複審被指派回答「它是真的正向對照，還是因為不相干的理由才通過」，結論為**真的**：在修正前的空行讀法下它會被假 BLOCK |

盲測時的名稱對照（歷史紀錄；**重跑時請自己重新打亂命名**，沿用下表等於洩答案）：

| 盲測名 | 實際 fixture |
|---|---|
| `case-A` | `f5-key-set-mismatch` |
| `case-B` | `f2-missing-green` |
| `case-C` | `f6-syntaxerror-red` |
| `case-D` | `f1-missing-annotation` |
| `case-E` | `f4-subject-mismatch` |
| `case-F` | `f3-pass-marker-on-red` |

盲測目錄本身不保存——刪除前以 SHA256 比對確認它與 `f1`–`f6` 逐位元組相同，留著只是同一份東西的第二份拷貝（**該比對同樣不可複驗**，理由見本節開頭）。有價值的是上面的對照表，不是拷貝。

**另一項範圍限制：** 盲測驗的是 R25 / R26 兩項修正**之前**的檢查措辭。之後 check 12 的表述與空行處理有變動，而**變動後沒有再跑第二次盲測**。`f7` 正是會測到新行為的那個 fixture。

**`f8`–`f13` 沒有盲測判定，句點。** 這六個是 change `fix-v2-blocking-defects` 修正五個 P1 缺陷後才新增的 fixture，鎖定的是修正**後**的檢查措辭；上面兩張表（判定者、盲測名稱對照）只涵蓋 `f1`–`f7`，`f8`–`f13` 不在其中，也不該被讀成隱含通過了某種盲測。它們**沒有**盲測判定這件事不變；但「尚未經任何獨立執行者驗證」已不再成立——2026-09-08 的第 3 輪 code re-review（fallback reviewer）對 13 個 fixture 做過一次**獨立再推導**，13/13 與預期判定一致，報告保存在 `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/code-rereview-fallback-3.md` § Regression。兩者的差別要留著：再推導是知道預期答案後重新導一次，盲測是不知道預期答案的執行者跑一次；**只有後者能反駁預期判定本身**，而 `f8`–`f13` 仍然沒有後者。

## 怎麼重跑

決定性檢查是 **agent 執行**的（instruction-mediated），不是腳本——所以「重跑」是把指令與受測物交給一個沒有脈絡的執行者，不是跑一支程式。

1. 取得**當前**的 verify 指令（別用舊的 render；schema 會變）。來源是 `superpowers-bridge/schema.yaml` 裡 `verify` artifact 的 `instruction:` 區塊；要拿 CLI 算出的完整版就跑：
   ```bash
   openspec instructions verify --change <某個 active change> --schema superpowers-bridge
   ```
   ⚠️ 這條指令**需要一個 active change 存在**，兩種失敗訊息不同（皆為實測，測時 repo 內 0 個 change）：完全沒有 change → `✖ Error: No changes found. Create one with: openspec new change <name>`；`--change` 指到不存在的名字 → `✖ Error: Change '<名字>' not found. No changes exist. …`（後半句是「repo 內 0 個 change」這個狀態造成的，換個狀態會不同）。**兩者都不是壞了。** 單純要讀條文時直接看 `schema.yaml` 即可。
2. 把 `fixtures/` 複製一份，**用中性名稱重新打亂**（`case-A`、`case-B`…），順序自己重排。**整批打亂的範圍是 `f1`–`f13`（共十三個 fixture），這十三個全部一起打亂**——不要只打亂 `f1`–`f7` 或只打亂 `f8`–`f13`，兩批分開重跑量不到「新舊檢查混在一起會不會互相干擾」。**`f14`–`f23` 不進這個整批重跑**：它們不放進打亂後的目錄、也不和 `f1`–`f13` 用同一份措辭比對第一張表，只走下面「`f14`–`f23` 的單份交付」（v3、v4 措辭各跑一次）。下面第 3、4 步的「打亂後的目錄」同樣只指 `f1`–`f13`。
3. 把指令與打亂後的目錄交給一個對本 change 無脈絡的執行者,請它對每個 case 回報「哪一條 check BLOCK、或不 BLOCK」。**額外針對 check 7**:BLOCK/不 BLOCK 兩種讀法在 `f13` 上答案相同、這題不能拿來鑑別新舊行為,所以再請執行者回報 check 7 找到的 deferred 任務**數量與識別(哪一筆)**——這才是能區分「讀 `tasks.md`」與「讀 `plan.md`」兩種讀法的結果。其餘每個 fixture 仍只需回答 BLOCK/不 BLOCK。
4. 用本檔第一張表比對。⚠️ 若把 `f7` 或 `f12` 併進去，**它們的正確答案都是「不 BLOCK」**——把正向對照判成 BLOCK 才是失敗。

fixtures 是純 markdown，沒有任何工具依賴；`f1`–`f7` 的 `plan.md` 除 `f5` 外全部相同（`f5` 蓄意改了 entry key）；`f8`–`f13` 各自的 `plan.md` 依其破壞的東西各不相同，見第一張表逐項對照。

### `f14`–`f23` 的單份交付（v3 / v4 措辭各跑一次）

`f14`–`f23` 的預期答案同時出現在上面的表格裡，而且 v3 與 v4 的判定常常不同（有的 v3 PASS、v4 BLOCK），所以：

1. **一次只交付一個 fixture，只交它的 `plan.md` 與 `tasks.md`**。複製到本 README 不在其中的位置（不是 `fixtures/` 的上一層，也不是含有本檔的任何目錄），目錄名用中性名稱（`case-A` 之類），不要沿用 `f14-…` 這種帶答案的原名。不要把整個 `fixtures/` 目錄交出去。
2. **執行者不可看到本 README**，也不可看到 `design.md` D7、`specs/plan-contract/spec.md` 或任何寫著預期判定的檔案。執行者只拿到：要測的 check 12 措辭（v3 或 v4，一次一種）與那一個 fixture。
3. 同一個 fixture 用 v3 措辭跑一次、用 v4 措辭跑一次，各自回報中間值（plan 收到的鍵、tasks 收到的鍵、重複、集合差）與判定；之後由另一層拿結果對照本檔表格。`f23` 的 v3 欄不凍結，只比對 v4。
4. 這十個 fixture 目前**尚未盲測**，表格裡的 v3、v4 判定是手推值。
