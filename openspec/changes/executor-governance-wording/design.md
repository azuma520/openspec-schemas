## Context

- **正式設計 §5**（`docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md` § 5 Degraded Mode 的治理方向「execution-path agnostic, contract-governed」）規定：執行路徑只要具備所需能力，或依 G3 合法降級並留下 degradation record，就可以使用；失去的是 required 保證時要 BLOCK，不得降級；Evidence 不能把不存在的能力變成存在。同節明寫 CLAUDE.md 的 executing-plans 紅旗要改寫成能力、證據、降級的寫法。
- **現況有三個問題：**
  1. CLAUDE.md「修 schema 時的紅旗」中 executing-plans 那條仍是工具禁令，句尾留著「⚠️ 之後要改寫」。
  2. `schema.yaml` 的 `description` 與 apply 指令、README 中英的提示框、設計觸點 #4、Fallback strategy 的 `apply` 列，都把設計理由和「Superpowers 某版本的 executing-plans 怎麼審查」寫在同一句。上游改版就得重寫理由，2026-10-06 已經發生過一次（`fix-executing-plans-rationale`，10/05 裁定、10/06 落地）。
  3. 有 subagent、經使用者裁定刻意不跑 SDD 的情境（8/31 `fix-tdd-transitive-claim`、10/06 `fix-executing-plans-rationale`）沒有規則說怎麼揭露。retrospective 雖然有 `### Deliberately Skipped Skills` 三題，但沒說這種情況怎麼回答，容易被讀成「記下來就等於符合」。
- **約束：**
  - living spec `tdd-claim-accuracy` REQ-3 用 SHALL 規定每一處說明拒用理由的地方都要陳述 executing-plans 的結構事實，並在 S1、S3 點名 CLAUDE.md 紅旗，所以只改文件會違反現行規格。
  - REQ-4 目前只管 `templates/retrospective.md`。
  - REQ-5 末段「skipped-skill rules … stay as they are」只是 REQ-5 自身不改它們的聲明，不禁止別的 requirement 調整。
- **範圍：** 依 brainstorm Q1，選 A，只對齊治理說明，不改 Step 0 STOP、不開放新的執行方式。

## Goals / Non-Goals

**Goals:**

- CLAUDE.md 紅旗改成能力與保障導向，刪除「之後要改寫」句。
- 設計說明（schema、README、CLAUDE.md）只寫 Bridge 要求的能力、保障與目前限制。上游哪個版本有或沒有這些能力，集中寫在 README 的 Re-verification log。
- apply 指令寫明三種情境，讓「刻意略過 SDD」有明確定位：例外偏離，不是支援的執行模式。
- retrospective 說明經裁定略過 SDD 時，既有三題怎麼回答，讓揭露內容包含失去的保障。
- 改寫 REQ-3、REQ-4，讓規格與新文件一致。
- 依 Versioning 判準，把 schema major 升到 5、bundle 升到 `5.0.0`，並完成所有連動與發版（D8）。

**Non-Goals:**

- 不改 Step 0 STOP，不新增 fallback、審查機制、機械檢查或降級資料結構。
- 不判斷 Bridge 是否要支援沒有 SDD 的能力等價或降級執行，這題留給 `task-20261012-non-sdd-execution-support` 依 §9 研究。
- 不重新查證上游。本 change 搬移的版本事實沿用既有查證：10/06 `fix-executing-plans-rationale` 對本機 v6.4.1 原文的查證，以及 10/02 spike 對 v6.4.2 的比對（該 spike 記錄 v6.4.1 與 v6.4.2 在本 schema 點名的 skill 中只差 `writing-plans`）。
- 不改 Re-verification log 既有的帶日期列與 follow-up 段，那些是紀錄。
- 不改正式設計文件；CI 只改 version-check 的列鍵（D8），不改其他 workflow 行為。

## Decisions

### D1：設計說明寫能力與限制，版本事實集中在 Re-verification log

- **選擇**：每一處說明拒用理由的地方只寫三件事：
  1. Bridge 的 apply 需要哪種能力：執行過程中的獨立審查，也就是每個任務、或每批同類小任務做完就審，而不是只在最後審。
  2. 目前限制：本版 apply 要求 SDD，缺能力時在 Step 0 STOP，不會自動改用 executing-plans。
  3. executing-plans 經查證不具備這項能力，細節與版本以 Re-verification log 為準（附連結或段名）。

  「沒有每個任務的審查」「無 subagent 時最後那次由作者自審」這類機制層的描述，以及對應的版本號、原文連結，只寫在 log。
- **理由**：上游改版時只需要在 log 新增一列，設計說明不必改。這也符合 §5「看能力、不看工具名」的原則。
- **已考慮 alternative**：
  - 設計說明完全不提 executing-plans。拒絕，因為讀者會不知道它已經被評估過，也不知道去哪查原因。
  - 保留現行寫法，只加 log 連結。拒絕，因為版本事實仍然寫在多個地方，下次改版又要逐處改。

### D2：Re-verification log 新增一段，集中寫 executing-plans 的審查結構事實

- **選擇**：在 log 末端（2026-10-08 follow-up 段之後）新增一段，標成 documentation only，不動 baseline。這段寫 executing-plans 的審查結構：
  - 沒有每個任務的審查。
  - 最後審一次整條分支：有 subagent 工具時派新的審查者，沒有時由作者自審。
  - 載入 `test-driven-development`。
  - 查證依據：v6.4.1 原文（固定標籤連結，沿用現有提示框那個連結）與 v6.4.2 spike 比對。

  另寫一句說明：此後設計說明引用本段，上游改版時更新本段。S13 列與 2026-08-26 列不改。
- **理由**：現有 S13 列只寫「v6.4.1 重建、最後派一次審查」，沒有無 subagent 時由作者自審這一層；提示框則寫 v6.4.1–v6.4.2。兩處的版本與內容不一致，需要一個完整、可被引用的位置。
- **已考慮 alternative**：直接改寫 S13 列。拒絕，因為那是帶日期的 spike 紀錄，改寫會讓紀錄與當時的查證脫節。

### D3：apply 指令加入三種情境

- **選擇**：在 `schema.yaml` apply 指令的 fallback 段後面加一段，內容如下：
  - **沒有 subagent 能力**：依現行 Step 0 STOP，建議改用 `spec-driven`。行為不變。
  - **有 SDD**：照第 2 步的契約執行。行為不變。
  - **有 SDD，但經使用者明確裁定刻意不用**：屬於例外偏離，不是本 schema 支援的執行模式。agent 不得自行決定略過，要由使用者明確裁定。retrospective 必須依略過規則記錄（見 D4），不得宣稱等同 SDD，也不得宣稱已滿足 SDD 提供的保障。若某項保障是這個 change 的必要條件、替代做法又提供不了，就停止並回報，不能靠紀錄放行。
- **理由**：Step 0 只處理「沒有能力」這一種情況；8/31、10/06 兩次都是「有能力但選擇不用」，目前在指令裡沒有定位（brainstorm Q3）。
- **已考慮 alternative**：只寫在 CLAUDE.md。拒絕，因為 CLAUDE.md 只給本 repo 的維護者看，採用者的 agent 讀的是 schema 指令。
- **實作中追加（使用者 2026-10-12 裁定甲，tasks 1.5）**：Step 0 原有一句「explicitly opt into the manual fallback path described at the end of this instruction」，但 apply 指令結尾沒有這條路徑。這句在 `75274b6`（2026-05-02）加入時有對應段落（2b executing-plans fallback 與結尾的 manual fallback 段）；同日稍晚的 `045ab98` 刪除那些段落，卻沒有一併刪除這句，從此指向不存在的段落，也和 README「no manual fallback within this schema」及第一種情境互相矛盾。修法是改寫成：缺必要 skill 就停止；使用者可以安裝所需 skill，或明確選擇改用內建的 `spec-driven` 繼續這個 change；Bridge 沒有內部的手動替代流程，agent 不得自行切換。PRECHECK 和 STOP 行為都不變，也不新增執行能力。

### D4：retrospective 只說明既有三題怎麼回答，不加欄位

- **選擇**：在 `schema.yaml` 的 Skipped-skill rules 和 `templates/retrospective.md` 的 `### Deliberately Skipped Skills` 說明裡，加一段「經使用者明確裁定刻意略過 `subagent-driven-development` 時」的回答方式：
  - **What was skipped**：寫出略過的子步驟，以及因此沒取得的保障，例如每個任務的獨立審查，或執行過程中的審查。
  - **Why this cycle**：寫使用者裁定（出處）、實際怎麼執行、用什麼替代的審查或驗證。
  - **How to prevent recurrence**：選既有選項 `one-off — schema boundary case`。邊界理由寫「經裁定的例外」，並寫出本次如何揭露偏離、證據保存在哪裡。這題要防的是未經授權的偏離、沒有揭露的保障缺口、不實的符合宣稱，不是要禁止經裁定的例外。
  - **選項字面對齊（使用者 2026-10-12 裁定）**：這個選項在兩處的字面原本就不一樣。`schema.yaml` 的 Skipped-skill rules 寫 `one-off — schema boundary case`，`templates/retrospective.md` 寫 `one-off — schema boundary case, no prevention possible`。模板多出的後綴意思是「無法預防」，與這一題仍要寫出防範內容相抵。這次把模板改成 schema 的字面，只刪除後綴，不新增選項，選項數量也不變。

  另加一句：這段紀錄只揭露偏離，不表示該執行方式受支援，也不能把沒達成的保障算成已達成。

  **語意界線（使用者 2026-10-12 裁定）：例外可以逐次核可，但反覆發生的例外不能永久當作偶發事件。** 因此 `one-off` 在這裡指「本次裁定只對這一個 change 有效」，不是宣稱這種情況只會發生一次：
  - 每個 change 都要使用者另行裁定，不得引用前例自動沿用。不能推論「前幾次都准了，以後純文字 change 就可以不跑 SDD」。
  - 同類略過再次出現時，第三題要寫明這是第幾次、前例在哪裡，並依既有規則（schema Skipped-skill rules 末段：「If multiple cycles skip the same skill with similar "How to prevent" answers, that pattern is a §6 Promote candidate」；模板「與 §6 Promote candidates 的關係」段）列為 §6 Promote candidate，指向正式評估替代執行方式的工作。這是沿用既有回饋機制，不新增流程。
  - 第三題的回答範例（使用者提供）：「本次是經使用者明確裁定的個案例外，並非正式支援的執行路徑。已記錄未使用 SDD 的原因、替代審查方式及失去的保障。未來每次仍須獨立裁定，不得自動沿用本次例外；若同類情況持續出現，應依既有複盤機制評估是否需要正式調整執行契約。」
- **理由**：
  - 對應 brainstorm Q5、Q6。
  - 這樣寫是把既有題目套到這種情況（「specific sub-step」本來就涵蓋失去的審查），並用既有選項回答，沒有新增欄位或選項。但指定必選的選項、禁止等效 SDD 的宣稱、要求寫出前例，這些是新增的規範性要求，會讓原本合法的寫法不合法，因此升 schema major（見 D8 與 proposal 版本判定）。
- **已考慮 alternative**：
  - 新增「Lost assurances」欄位。拒絕，因為這會改動模板的形狀；既有三題已足以承載同樣的內容。
  - 新增 `sanctioned deviation` 選項。拒絕，因為這會改掉既有的選一清單形狀，等於新增寫法；既有的 `one-off — schema boundary case` 已經要求寫明為什麼是邊界情況，足夠承載。

### D5：CLAUDE.md 紅旗改寫

- **選擇**：第 258 行改成下面的意思（措辭在實作時定）：
  > ❌ 在 apply 加入不具備 apply 所需能力（執行過程中的獨立審查）、又沒有依正式設計 §5 合法降級的執行方式；或把降級／偏離紀錄當成保障已滿足。目前限制：本版 apply 只支援 SDD，缺能力時 Step 0 STOP、引導改用 `spec-driven`。executing-plans 經查證不具備這項能力，事實與版本見 bridge README Re-verification log。

  拿掉的內容：版本沿革（v5.1.0、v6.3.0、8/31 等）、「⚠️ 之後要改寫」整句、工作編號。保留的內容：不以上游推薦為理由、TDD 不是差異點。這兩點改成能力語言，或併入 REQ-3 的保留禁令。
- **理由**：§5 要求紅旗管的是能力與保障。版本沿革屬於紀錄，已經寫在 10/06 change 與 log 裡。
- **已考慮 alternative**：保留版本沿革當作維護者提醒。拒絕，因為那正是會隨上游過時、要逐處改的內容。

### D6：README 逐處處理

| 位置（en；zh-TW 為對應段落） | 處理 |
|---|---|
| Seven Superpowers touchpoints 段下的 Naming is not requiring 提示框 | 不改。「named only to rule it out」仍然成立 |
| No `executing-plans` fallback 提示框 | 依 D1 改寫，機制描述移到 log |
| §2 Apply 段的「does NOT support … See Six design touches」 | 保留指向，另補一句三種情境中刻意略過的定位（例外偏離，記在 retrospective），與 schema 一致 |
| 設計觸點 #2 Schema-level vs prompt-level（說明「why executing-plans is excluded」需隨上游重查） | 改成：上游行為的查證集中在 Re-verification log；schema 指令只陳述能力與限制，並引用該 log |
| 設計觸點 #4 | 依 D1 改寫，保留 fail loud 與 `spec-driven` 引導 |
| Re-verification log 既有各列與 follow-up 段 | 不改（紀錄） |
| Re-verification log 新段 | 依 D2 新增 |
| Fallback strategy 的 `apply` phase 列 | 依 D1 改寫理由，指向設計觸點 #4 與 log |

### D7：規格修改的形狀（細節在 specs artifact）

- **MODIFIED REQ-3**：
  - 設計說明（schema、兩份 README 的設計段、CLAUDE.md）陳述能力、保障與執行限制，並引用 Re-verification log。
  - log 記錄上游各版本提供或缺少的能力，以及查證來源。
  - CLAUDE.md 紅旗移出「逐處陳述 executing-plans 版本事實」的範圍，但仍要依據已查證的事實。
  - 現有三條禁令保留：不以上游推薦為理由、不說它完全沒有獨立審查、不以 TDD 為區分。
  - 情境 S1、S3 依新範圍改寫。
- **MODIFIED REQ-4**：
  - 適用範圍從模板擴到 `schema.yaml` 的 retrospective 略過規則。
  - 新增：經裁定略過 SDD 的紀錄必須寫出失去的保障，且不得被模板或指令表述成等於符合 Bridge 或已滿足保障。
  - 新增：裁定只對該 change 有效、不得引用前例沿用；同類略過反覆出現時要寫明次數與前例，並列為 §6 Promote candidate。
  - 新增情境涵蓋上述兩點。

### D8：schema major 4 → 5、bundle `5.0.0`（使用者 2026-10-12 裁定）

- **選擇**：D4 與 REQ-4 新增的規範性要求，使原本合法的 retrospective 寫法變得不合法（分類見 proposal「版本判定」）。依 Versioning 段，這一條單獨就足以升 schema major。連動的地方比照 v3 → v4 的 `0b11be5`：

| 位置 | 改動 |
|---|---|
| `schema.yaml` | `version: 5` |
| `VERSION` | `5.0.0` |
| bridge README 中英：開頭的「Schema version」 | `v5`，連結改指「Migrating v4 → v5」 |
| bridge README 中英：Upgrading 段跨 major 的說明 | 補一句 v4 → v5 改了什麼（經裁定略過 SDD 的 retrospective 寫法） |
| bridge README 中英：Versioning 表的 `version: N`、「`N.x.y` is a published cut」、列鍵清單 | 加入 v5 |
| bridge README 中英：Versioning 段 | 新增「Why v4 → v5」：只有「原本合法的 artifact 變不合法」一條成立；沒有 artifact 增刪、沒有改 `requires:`、PRECHECK 不變；寫明「不合法」不限於機械檢查會擋，並記下以「沒有檢查會擋」為由維持 v4 的方案已被否決 |
| bridge README 中英：Versioning 段 | 新增「Migrating v4 → v5」：只影響往後記錄經裁定略過 SDD 的 retrospective；其他 artifact 不必遷移；in-flight change 若會略過 SDD，依新規則寫；封存的 retrospective 不回頭改。Rollback 指向已存在的 tag `v4.0.0`（2026-10-12 查證：本機與 `origin` 都有，剝開後指向 `d2a350c`） |
| bridge README 中英：Compatibility | 「Current bundle release」改為 `5.0.0`；新增 v5 列（OpenSpec `1.14.0`、Superpowers `v5.1.0`、`pending`），比照 v4 列沿用歷史宣告，並在表下說明 v5 列同樣是未重新查證的歷史宣告、不是相容保證；第 662 行附近的 `pending` 說明涵蓋 v5 列 |
| bridge README 中英：Known breaking changes | 新增 v4 → v5 一條 |
| `.github/workflows/version-check.yml` | 列鍵 `v4` → `v5`，在本機跑一次那段 grep/awk，確認讀到 v5 列的兩個版本號（CLAUDE.md 跨檔耦合表要求） |
| 頂層 `README.md` 與 `README.zh-TW.md` | 第 11 行 bridges 表的 Status 欄 `v4` → `v5`。這一欄寫的是 repo 裡這份 bridge 的 schema major，合入後就是事實，不是發版宣告 |
| `docs/roadmap.md` 與 `.zh-TW.md` | 新增 v5 段，標題先寫「v5」，不標「Released／已釋出」。等遠端 tag `v5.0.0` 確認後，再以一個文件 commit 補上標記。理由：release commit 必然早於 tag，若在其中寫「Released」，tag 推上去之前那段時間的說法就不成立（同 `release-versioning` REQ-2「before and after」的判準） |
| `CLAUDE.md` | 結構約定的 `VERSION` 註記、跨檔耦合表的列鍵描述、「兩個版本號別搞混」表的 `version: 4` 與「需從目前的 4 bump」、「Compatibility 表的列鍵」一句 |
| 發版 | archive 並完成最終驗證後，在 release commit 打 annotated tag `v5.0.0`；push 需要使用者當次授權；確認遠端 `refs/tags/v5.0.0^{}` 等於 release commit 後，工作地圖紀錄才標記完成（`release-versioning` REQ-1） |

- **理由**：
  - Versioning 段的判準是「原本合法的 artifact 變不合法」，沒有限定必須被機械檢查擋下。
  - v5 不代表要新增檢查或執行模式；這次仍然只改文字與規格。
- **已考慮 alternative**：
  - 維持 4，把「不合法」解讀為「會被 verify 擋下」。被否決：這是為了這次改動臨時縮小破壞性變更的定義。
  - 只升 schema major、`VERSION` 留在 `4.0.0`。拒絕：`4.x.y` 依定義是 v4 的發佈版本，與 `version: 5` 矛盾。
- **v5 列的 Superpowers 版本**：沿用 `v5.1.0` 歷史宣告，比照 v4 列，不在本 change 重新定錨。6.x 的重新定錨屬於 `task-20261007-superpowers-6x-rebaseline`。`release-versioning` REQ-3 正文只點名 v4 列，v5 列由 README 說明比照處理，正文不改。**更正（實作時的殘留搜尋發現，使用者 2026-10-12 裁定）**：原判斷漏看了 REQ-3 的情境 S2。它寫「每週版本檢查讀 v4 列」，4.2 把列鍵改成 `v5` 後就不成立，之後的人可能照規格把正確的列鍵改回 v4。因此本 change 加一份 `release-versioning` 規格修改，把 S2 改成「讀的列與目前發布的 schema major 一致、升版時同步更新」。條文不宣稱檢查會自動辨識最新列，因為目前做法是寫死列鍵、升版時手動更新。

## Risks / Trade-offs

- **[Risk] 第三種情境被讀成「使用者同意就可以不跑 SDD」的放行指示** → Mitigation：
  - 指令明寫「不是支援的執行模式」「不得宣稱等同 SDD」「必要保障做不到就停止」。
  - verify 與文件審查時檢查 brainstorm 列的語意 3（略過的紀錄不會被解讀成已滿足必要保障）。
- **[Risk] 設計說明拿掉機制細節後，理由變成空泛的「它不具備能力」** → Mitigation：每處都必須引用 log；REQ-3 改寫後仍要求理由建立在已查證的事實上；log 新段寫完整事實與版本。
- **[Risk] 中英文 README 不同步** → Mitigation：同一個 commit 改兩份；驗證時逐段對照。
- **[Risk] `one-off` 字面讓反覆出現的略過看起來像偶發事件** → Mitigation：D4 語意界線要求寫明次數與前例，並依既有規則列為 §6 Promote candidate；本 change 是第三例，retrospective 要照做。
- **[Risk] 升 major 的連動有遺漏（CI 抓不到）** → Mitigation：依 D8 表逐處改；`git grep` 搜 `v4`、`version: 4`、`4.x.y`、`4.0.0`，逐筆判斷改或不改；在本機跑 version-check 的 grep/awk。
- **[Risk] 把「不合法」寫成連封存紀錄都要改** → Mitigation：Migrating 段明寫封存的 retrospective 不回頭改，v5 只約束往後依新契約寫的紀錄。
- **[Trade-off] 本 change 自己的 apply 不跑 SDD（brainstorm Q4 具名例外）**，失去每個步驟的獨立審查 → 接受理由：改動集中在治理說明，以 Codex 文件審查、差異檢查與完整 bridge verify 補足。retrospective 依本 change 新寫的 D4 規則如實記錄，也正好試用一次新規則。
- **[Trade-off] 一次文字為主的修改帶出一次 major 發版**（Versioning 新段、遷移說明、Compatibility 列、CI 列鍵、roadmap、tag） → 接受理由：版本契約的可信度優先於這次的改動成本（使用者裁定）。

## Migration Plan

不涉及部署變更；本 change 是一次 schema major 發版。

- 採用者：從 `4.x.y` 升到 `5.0.0`。只有往後記錄經使用者裁定略過 SDD 的 retrospective 時，要依新規則寫（見 README「Migrating v4 → v5」）。其他 artifact 不必遷移，封存的 retrospective 不回頭改。Rollback：checkout tag `v4.0.0`，把它的 `superpowers-bridge/` 複製回 `openspec/schemas/`。
- 本 repo：改完重新同步 dogfood 副本（`rm -rf openspec/schemas/superpowers-bridge && cp -R superpowers-bridge openspec/schemas/`），跑 `openspec schema validate superpowers-bridge` 與 `openspec schemas`，並在本機跑 version-check 的 grep/awk。
- 發版：archive、最終驗證、所有連動文件都更新完後，在 release commit 打 `v5.0.0`。push 要經使用者授權，並確認遠端 tag 剝開後指向該 commit。確認之後，再以一個文件 commit 把 roadmap 的 v5 段標成「Released／已釋出」（見 D8）。

## Open Questions

（無。三個語意的確認方式已定：沒有 subagent 時仍會 STOP、有 SDD 時仍走正式路徑、略過的紀錄不會被讀成保障已滿足，併入文件審查與 verify，不新增機械檢查。）
