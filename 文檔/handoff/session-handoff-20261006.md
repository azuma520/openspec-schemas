# Session Handoff — 2026-10-06

## Session 08:40

### 一、本 session 主題

開工流程（work-status、10-05 17:30 交接、接力棒 3 條）＋查 Superpowers 是否已是最新版。純查證 session，未改 repo 內任何檔案（本 handoff 除外）。

### 二、完成事項

- **開工三步驟**：work-status 正常；接力棒 3 條逐條交代。backlog 週檢 10-05 已跑（W41），今天是週二、不重跑。
- **接力棒 1：fork 每週排程已跑**：`gh run list --workflow version-check.yml` → run `37374999719`（schedule，2026-10-05T21:18:01Z，success，比排定 14:00 UTC 晚約 7 小時）。issue #2 新增留言：OpenSpec `1.14.0` 無漂移；Superpowers 仍釘 `v5.1.0`、最新 `v6.4.2`；schema 對 `1.14.0` 驗證通過。此條收。
- **Superpowers 版本查證**：
  - 本機啟用 `superpowers@claude-plugins-official` **6.4.1**（全域＋本 repo 專案層）；`superpowers@superpowers-marketplace` 6.4.2 已裝但停用（`installed_plugins.json`、`settings.json`）。
  - v6.4.2 release notes（`gh release view v6.4.2 -R obra/superpowers`）：只改 `writing-plans`（計畫記決定不抄程式碼、長度自檢、步驟改「一個動作＋可檢查結果」、刪 `plan-document-reviewer-prompt.md`）＋刪上游自己的 `CLAUDE.md`。對 bridge 無影響：`schema.yaml:356-361` 只把 `writing-plans` 當私下輔助，與 10-02 spike S15「成立」一致。
  - **官方商店目前提供的就是 6.4.1**：GitHub `anthropics/claude-plugins-official` 的 `.claude-plugin/marketplace.json` 釘 `5bf4e78…`；`obra/superpowers` 的 `v6.4.1` = `5bf4e78…`、`v6.4.2` = `8ca22db…`。10-02 spike 標「未查證」的 S17 今日查證：照 README 安裝拿到的是 6.4.1。
  - **使用者裁定丙**：本機維持 6.4.1，等官方商店跟上；不切到另一個商店的 6.4.2。
- 封裝候選檢查：backlog 無 open `[SOP 候選]`，無命中。

### 三、未完事項 / 接力棒

- [#接力] **C1 維持 DOING、下一個子題等使用者定題**（本 session 提了甲 E2 載體／乙其他 E1 載體／丙直接進產品決策，建議甲；使用者未選）。
- [#不重議] Superpowers 本機維持 6.4.1、不切 superpowers-marketplace（2026-10-06 使用者裁定丙）。repo 宣稱基準維持 `v5.1.0`（10-02 B1）。
- [#接力] 官方商店何時上 6.4.2 沒有通知機制；要看時重跑同一條查法（讀 GitHub 上官方 `marketplace.json` 的 superpowers `sha`、對 `obra/superpowers` tag）。
- [#待確認] 開工 hook 在週二注入「今天週一」的 backlog 週檢提醒，原因未查（可能是週一未跑的延後提醒、也可能是星期判斷錯）；要不要記給 workflow-harness 由使用者決定。
- [#接力] 照舊：`v3.0.0` tag 未打；`.claude/worktrees/requirement-scenario-identity` 空目錄仍在（git 已不認），重開機後刪。

### 四、洞見 / 反省

**【紀律接力】**

- **沒有來源的事實宣稱（10-05 hash 編造之後，今日再 1 次）**：照 hook 注入文字向使用者說「今天週一」，沒查日期；查 `date` 才知是週二、當場更正。做法：hook／注入文字裡的事實（日期、星期、計數）也是待驗證的宣稱，轉述前先查一次。
- **驗證比對錯了對象（10-05 兩次之後，今日再 1 次）**：對非 git 目錄的商店快取跑 `git -C <dir> log`，git 往上層找到家目錄的另一個 repo，讀到「6/5 之後沒更新」的假訊號；改看檔案時間戳（今日 07:00）＋讀 GitHub 原檔才對上。做法：`git -C` 前先確認目標本身就是 repo（`remote -v` 對不對得上預期來源），否則讀到的是別人的歷史。

**【當日洞見】**

- **Superpowers 的「最新版」有兩層答案**：上游 release（6.4.2）≠ 官方商店實際發的版本（6.4.1）。drift 檢查比的是前者，使用者照 README 裝到的是後者——兩者不同步時，issue #2 的「落後」有一部分是商店層落後、不是 bridge 落後。
- **6.4.2 改版原因點名 Opus 5.5 寫計畫時會越界直接實作**；本 repo bridge 的 plan 不走 `writing-plans`，不受影響，但使用者在其他專案用 superpowers 寫計畫時相關。

**【學習候選】**

- 沒有。

### 五、檔案異動

錨來源：本 session 開工 commit（8f6a0b3、開工於 2026-10-05T17:55:22）——列 8f6a0b3..HEAD

- 無 commit。本機商店清單快取由 `claude plugin marketplace update claude-plugins-official` 更新（repo 外）。
- 本次收工：本 handoff（新檔）

### 六、下一步建議

1. C1 下一個子題：請使用者定題（甲 E2 載體／乙其他 E1 載體／丙進「補機制 vs 收窄承諾」產品決策；建議甲），定了再登記、再做。
2. 重寫 executing-plans 拒用理由（走 opsx change，連動 schema、README en+zh-TW、CLAUDE.md 紅旗）——約一下午。
3. 不急：`v3.0.0` tag（對外、需使用者點頭）；證據包「保存每案 prompt 原文」NIT；C2 維持延後。

## Session 12:06

### 一、本 session 主題

同一個 session 接 08:40 區塊之後的工作（08:40 區塊是開工查證後應使用者要求先寫的交接，之後 session 繼續）：C1 第三輪「由系統保存的執行紀錄能否證明驗證真的有跑」從定題、讀文件、實測到寫入研究文件；C1 結案；把結案討論整理成上層 Verification Strategy 的新備忘；決策 A 裁定、決策 B 與 G2 加註登記。

### 二、完成事項

- **C1 第三輪**（`32f4bee` 研究文件 §3.5＋證據包、`ac45a40` 工作地圖）：
  - 判準先定（runtime 寫入／對得回哪次執行／看得出沒做／agent 改不到），分類開跑前凍結（可行／部分可行／不足）。
  - 文件層：Orca `worker-read` 讀的是 provider 自己的對話紀錄、沒有另起紀錄；本機對話紀錄同帳號可改 → 兩者皆弱證據。
  - 實測（Claude Code 2.1.290 OTel logs 外送本機收集端）：正向讀三檔 `READ_ALL`；反向二「沒讀卻宣稱 PASS」`NOT_READ`。T1 實測成立、T2 只有文件支持 → **部分可行**。
  - 證據包 22 檔（帳號屬性已刪）；提交後以 `git cat-file` 驗 PROVENANCE 21 個雜湊全對上 HEAD blob。
  - 審查：Codex 2 輪 ✅、Fable 1 輪 ✅（使用者要求加審）。
- **C1 結案**（`a338227`）＋**上層備忘** `docs/superpowers/research/2026-10-06-verification-strategy-after-c1.md`（`b455006`）：能力邊界、成本與階段先用正式設計 §2.3、延後驗證須有觸發條件、機械執行≠oracle 對準、「證據裁決／審查收斂／責任人決策」三分；每條標注對 10/02 起點備忘是支持或新。Codex 額度用完（13:18 恢復），改由備援審查者（contract-neutral-reviewer）負責，七輪皆 ✅ Mergeable，每輪報告經 `validate-family-sentinel.js doc` 驗過。
- **決策 A**：維持 10/02「下次修訂時加註、不改 G2」裁定（`task-20261006-vs-g2-commitment-wording`，DONE）。
- **登記**：決策 B `task-20261006-vs-execution-record-capability`（TODO）；G2 加註延後工作 `task-20261006-g2-annotation-on-next-revision`（TODO）。
- **收工結算**：task-brief 底下唯一可升子項 `task-20261005-superpowers-task-brief-upstream-report` 標 NEXT。
- 新記憶：`feedback_subthreshold_red_risk_discuss`（審查小項若有 🔴 風險，端給使用者決定要不要現在修）。
- 封裝候選檢查：backlog 無 open `[SOP 候選]`，無命中。

### 三、未完事項 / 接力棒

- [#接力] **Verification Strategy 下一步要使用者挑**：底下有 4 件還沒開始（C2、verify/sync lifecycle、決策 B、G2 加註），≥2 件，收工未自動標下一步。
- [#不重議] 決策 A 已決：維持 10/02 裁定；G2 加註只是執行舊裁定，不重開 G2 決策。
- [#不重議] C1 結案、不再追加實驗；C1 §5 未查證項（第 3、4、9、10 條）凍結，決策 B 推進前先重開第 9、10 條。
- [#不重議] Superpowers 本機維持 6.4.1（08:40 區塊）。
- ~~審查暫存檔待手動刪~~ 已於收工後由使用者清除（scratchpad `rv/`、`rv2/`、`c1r3/`、`orca-orch.md`；`~/.claude/projects/` 下 c1r3 與 10/05 c1-hook-probe 兩個巢狀測試 session 目錄；9/29 遺留的兩個空 `smart-commit-msg.*`），已逐項查證不存在。
- [#接力] 照舊：`v3.0.0` tag 未打。（`.claude/worktrees/requirement-scenario-identity` 空目錄已於收工後由使用者刪除，查證 `.claude/worktrees/` 為空。）
- [#待確認] 08:40 區塊提到的「開工 hook 週二講成週一」仍未處理。

### 四、洞見 / 反省

**【紀律接力】**

- **轉述二手來源當事實（今日 3 次）**：① 照 hook 文字說「今天週一」；② 只讀 WebFetch 摘要就宣稱「官方文件寫錯欄位」（Codex 抓到，下載原文第 799、1574 行才定案）；③ 改正時又寫出「從推論變成有實證」「唯一的實驗」兩句說過頭的話（備援審查抓到）。做法：引用文件內容時讀原文（curl 下來 grep），不讀摘要；改正句寫完再過一次「這句的來源是哪一行」。⚠️ 修正動作本身是高發場景（全域規則已寫，今天仍復發）。
- **審查迴圈不自然收斂**：無記憶的備援審查者每輪都找出新小項。照使用者新規則分三類（真 🔴 必修／有 🔴 風險端給使用者／純小項只記錄）才停得下來。

**【當日洞見】**

- **E2 的通用判準**：重點不是有沒有紀錄，而是紀錄有沒有離開受觀察 agent 寫得到的範圍。
- **自己做的假樣本會和判斷者共用同一個錯誤假設**：v1 判讀腳本的 6 組假事件自檢全過，因為假事件也照錯欄位做；讓錯誤浮現的是一筆已知為正的真實樣本。「先用假報告證明分得出對錯」要補「還要一筆已知為正的真實樣本」。
- **「判斷正確」改為「證據裁決／審查收斂／責任人決策」**：正式設計 §8 第 4 條本就不保證判斷正確；收斂要靠審查者夠不同＋能對照現實處就對照。
- 遙測事件中使用者 prompt 與回覆是 `<REDACTED>`，只呈現動作——「做了什麼」與「說了什麼」天然分開。

**【學習候選】**

- **Case**：判讀腳本看錯欄位，6 組自製假事件全過；真實正向樣本才揭露。
- **Candidate Pattern**：驗證判斷者時，負向對照用自製假樣本即可，但至少要有一筆**真實、已知為正**的樣本；自製樣本與判斷者出自同一份理解，會一起錯。不適用：判斷者輸入格式由規格完全釘死且有官方範例的情形。
- **Evidence**：本次 1 例；與 memory `feedback_claim_first_discriminating_oracle`（先用假報告證明 grader 分得出）同族，是它的補充條件。Hypothesis。
- **Minimum Sufficient Intervention**：不新增規則；把這句補進既有 memory `feedback_claim_first_discriminating_oracle`（掛點＝該 memory 本身會在 oracle 設計時被 recall）。
- **Promotion**：Refine Existing Strategy（待使用者同意後補進該 memory）。

### 五、檔案異動

錨來源：本 session 開工 commit（8f6a0b3、開工於 2026-10-05T17:55:22）——本區塊列 f03b44e..HEAD（f03b44e 為 08:40 區塊的提交）

- `32f4bee`：`docs/superpowers/research/2026-10-05-verification-c1-enforcement-surface.md`、`docs/superpowers/research/README.md`、`docs/superpowers/research/evidence/2026-10-06-c1-telemetry-execution-probe/`（新，22 檔）
- `ac45a40`：`workflow-harness/work-map.jsonl`（C1 第三輪登記並結案）
- `b455006`：`docs/superpowers/research/2026-10-06-verification-strategy-after-c1.md`（新）、`docs/superpowers/research/README.md`、C1 研究文件開頭結案註記
- `a338227`：`workflow-harness/work-map.jsonl`（C1 結案）
- 本次收工：備忘 §5 A 改【已決】、B 加編號；索引列同步；work-map 新增 A、B、G2 加註三筆並標 task-brief 子項 NEXT；本 handoff

### 六、下一步建議

1. Verification Strategy 挑下一件：決策 B（§2.2 執行紀錄能力，需先重開 C1 §5 第 9、10 條）或 C2（判讀正確性），由使用者定。
2. 重寫 executing-plans 拒用理由（走 opsx change）——仍是最接近「一下午做完」的一件。
3. 不急：`v3.0.0` tag；task-brief 上游回報草稿（已標 NEXT）。

## Session 17:13

### 一、本 session 主題

開工核實「上次沒收工」為誤報（12:06 收工後 session 未關、13:15 自動壓縮與 /clear 更新了對話檔時間，機轉同 9/10 外掛自查）；討論審查路由（每任務審 vs 最後審）與 SDD 過程紀錄保存的取捨；完成 `fix-executing-plans-rationale` 從開案到歸檔整個流程。

### 二、完成事項

- **`fix-executing-plans-rationale`**（`9ef62c2` 實作、`0749aa2` 歸檔）：
  - 依 Superpowers v6.4.1 原文更正 bridge 拒用 executing-plans 的理由（結論不變）：沒有每個 task 的審查、只在最後審一次；無 subagent 時那次由作者自審。不再引用「上游建議用哪個」。
  - 源頭是正式規格 `tdd-claim-accuracy` REQ-3（用 SHALL 規定了舊理由），一併修改並新增 REQ-3-S3。
  - 表面：`schema.yaml` 兩處、README 中英文（touchpoints 段、設計觸點 #4、§ 2 維護說明、降級策略 apply 列、10/02 紀錄後補「後續狀態」一行、四個連結固定指向 `v6.4.1` 標籤）、`CLAUDE.md` 紅旗（含「依正式設計 §5 之後改寫」預告句）。
  - 審查：程式碼 Codex r1 ✅＋歸檔後備援 strict-reviewer ✅；文件 Codex r1 ⛔（README § 2 宣稱「上游行為改了 schema 不用改」與本 change 矛盾）→ r2 ✅；Codex 額度用完（20:17 恢復）後改由 contract-neutral-reviewer，[REVIEWER_FALLBACK] 已記，三輪皆 ✅、每份原始報告經 `validate-family-sentinel.js` 驗過；precommit 以 repo 唯一測試（schema validate）代替並留 [DEVIATION]；verify 由獨立執行者完成（⚠️ PASS WITH WARNINGS）。
  - 執行：主 session inline、不開 worktree／SDD（沿用 8/31 先例，複盤 §4 記錄）。
- **否決登記**：「SDD 過程紀錄不隨歸檔保存」使用者裁定不登記（對一般採用者不需要；研究需要時當次保存）。10/02 retro-skill-inventory 複盤第 123 行那個未勾的「升到證據生命週期子題」以此結論視為已處理（不改已歸檔複盤）。
- **結算**：`task-20261002-executing-plans-rationale` 標 DONE。
- 封裝候選檢查：backlog 無 open `[SOP 候選]`，無命中。

### 三、未完事項 / 接力棒

- [#接力] **複盤 §6 三條長期規則候選待使用者決定是否升級**（`openspec/changes/archive/2026-10-06-fix-executing-plans-rationale/retrospective.md` §6）：①純措辭更正的執行路徑明文化（第二次跳過 worktree/SDD），建議併入 `task-20260901-claudemd-governance-rewrite` ②修「上游改版讓說法失效」時一併搜「怎麼處理上游改版」的維護說明（memory，Hypothesis）③引用上游原文時連結指向固定版本標籤。
- [#接力] 最後一輪審查留下的 sub-threshold 小項（只記錄、使用者裁定不再開循環）：retrospective §0 README diff 寫 +4/−2、實際 +5/−3；retrospective 引用 10/05 handoff 第 93–95 行、B-i 實在第 96 行；README 第 610 行「依目前的上游行為」未寫版本、也未說 S4/S5 仍擋 baseline。
- [#不重議] executing-plans：只修理由、不重評 fallback（10/05 裁定，本 session 結論一致）；要不要放寬交給 `task-20260901-claudemd-governance-rewrite`，該件「不可先行」依賴已於 10/05 撤銷（工作地圖文字仍是舊的、等重登記時改）。
- [#不重議] SDD 過程紀錄不登記。
- [#接力] 照舊：commit 未 push（main 比 origin 多 21 筆）；`v3.0.0` tag 未打。
- 審查暫存檔已由使用者清除（scratchpad 整個資料夾，已查證不存在）。

### 四、洞見 / 反省

**【紀律接力】**

- **修正句說過頭（今天又 4 次，連同 08:40／12:06 區塊累計 7 次）**：「每個任務都審」（SDD 會合批）、「6.4.1 以前都沒有最後審查」（只查過 5.1.0、6.3.0）、「改名就會被 PRECHECK 擋下」（只對必要 skill）、「design.md 也寫了不可先行」（查證沒有）。全是**寫替代句時**發生。做法：每寫一句替代句，先答「這句的證據是哪一行、射程是不是全部」再往下寫。全域規則已寫仍復發＝規則擋不住。
- **開工只讀最新 handoff、沒回查前一天的 [#不重議]**：10/05 已裁定「只修理由、不重評」、紅旗改寫依賴已撤，我重問了使用者並把工作地圖舊文字當事實。做法：動某件工作前，先搜近幾天 handoff 裡提到它的 `[#不重議]`，不只信工作地圖 description。
- **驗證工具一律餵原始報告**：今天差點拿刪減版報告去跑 `validate-family-sentinel.js`（等於偽造驗證）；工具在等 stdin 卡住才沒產生結果。做法：報告整份原文照存，不摘要。

**【當日洞見】**

- **上游改版造成的失效 ≠ 當初查錯**：8/31 的說法在 6.3.0 成立；修正紀錄要分清楚，免得後人以為當時查證有問題。
- **錯誤說法的源頭可能是正式規格**：只改文件不改規格，下次照規格驗收會把正確文字判成不合規。
- **新規格也可能比實作嚴**：REQ-3-S3 寫「每一段」，README 降級策略那列沒跟上，是歸檔後文件審查才抓到。
- **SDD 過程紀錄不隨歸檔保存是上游刻意設計**（`sdd-workspace` 第 81 行自動 gitignore、SKILL.md 第 482–483 行總審後刪除），前提是每個任務都 commit；本 repo 禁止 AI commit，前提不成立。使用者裁定不登記。
- **審查路由的判準**：要不要每個任務都審，重點不在風險高低，而在「後面的任務會不會建立在測試驗不出來的理解上」；建議寫計畫時就在 tasks.md 標審查切點。實測依據：6 個已歸檔 change 已混用每任務審／合批審／不走 SDD 三種，皆當下判斷、事後寫進複盤。未登記。

**【學習候選】**

- **Case**：修正「上游改版讓說法失效」時，只搜了 `executing-plans` 這個詞，漏掉 README「上游行為改了 schema 不用改」的後設說法，被 Codex 文件審 r1 抓到。
- **Candidate Pattern**：修正因外部改版而失效的宣稱時，除了搜被推翻的具體說法，也搜「怎麼處理外部改版」的維護說明——外部改版本身常是那些說明的反例。不適用：宣稱失效不是因外部改版。
- **Evidence**：1 例。Hypothesis。
- **Minimum Sufficient Intervention**：不新增規則；待使用者決定是否把複盤 §6 第 2 條升為 memory（觸發點：處理 drift issue 時）。
- **Promotion**：Case Memory（待使用者決定）。

### 五、檔案異動

錨來源：本 session 開工 commit（a136720、開工於 2026-10-06T14:02:31）——列 a136720..HEAD

- `9ef62c2`：`superpowers-bridge/schema.yaml`、`superpowers-bridge/README.md`、`superpowers-bridge/README.zh-TW.md`、`CLAUDE.md`、`openspec/changes/fix-executing-plans-rationale/`（新，7 檔）
- `0749aa2`：change 搬到 `openspec/changes/archive/2026-10-06-fix-executing-plans-rationale/`（含新增 `verify.md`、`retrospective.md`）、`openspec/specs/tdd-claim-accuracy/spec.md`（REQ-3 修改）、兩份 README（後續狀態行、固定版本連結、降級策略 apply 列）
- 本次收工：work-map（`task-20261002-executing-plans-rationale` 標 DONE）、本 handoff

### 六、下一步建議

1. 決定複盤 §6 三條長期規則候選要不要升級、升到哪裡。
2. Verification Strategy 挑下一件：C2 或決策 B（沿用 12:06 接力）。
3. 不急：push 21 筆 commit；`v3.0.0` tag；task-brief 上游回報草稿（已標 NEXT）。


## Session 18:11

### 一、本 session 主題

開工後依上次接力棒第 1 條，白話討論 `fix-executing-plans-rationale` 複盤 §6 三條長期規則候選並逐條裁定；把 (c) 寫進 CLAUDE.md、(a) 併進紅旗改寫工作；收尾時檢討「要使用者反問才發現不需要」的模式並改進記憶。

### 二、完成事項

- **複盤 §6 三條候選裁定**（使用者 2026-10-06）：
  - (a) 純措辭更正型 change 的執行路徑明文化 → **併入 `task-20260901-claudemd-governance-rewrite`**。工作地圖該條 name 已改寫：刪除已撤銷的「須隨 apply schema change、不可先行」；併入 (a)；另併入「bridge README 中英文談 executing-plans 的兩段（touchpoints 提示框、設計觸點 #4）理由與證據分開——設計說明只寫理由、上游哪版做到／沒做到寫在 Re-verification log」（本 session 討論「README 的功能是什麼」時得出）。
  - (b) 修上游改版失效時一併搜維護說明 → **不存記憶**，留在複盤當案例（1 例 Hypothesis；本益比低、現有文件審已接得住）。
  - (c) 引用上游原文時連結指向固定版本 → **寫進 `CLAUDE.md`「雙語策略」節**（翻譯同步原則之後一段）：適用範圍、理由、排除（指路用連結）、來源。
- **文件審（CLAUDE.md）**：Codex r1 額度用完（`ERROR: You've hit your usage limit`，20:17 恢復，無報告）→ `[REVIEWER_FALLBACK] plane=doc_review from=codex to=contract-neutral-reviewer reason=quota | 2026-10-06T09:58:33Z`（`review-dispatch.js` 決定）→ ✅ Mergeable，原始報告整份存檔經 `validate-family-sentinel.js doc` → `[SENTINEL_VALID]`，已 note pass。暫存檔由使用者刪除、已查證資料夾為空。
- **sub-threshold 三項**：🟡 位置放在雙語策略下不好找（不處理）；⚪「確認標籤內容」沒寫方法（使用者反問後判定不需要：實測本機 Superpowers 副本 6.4.1／6.4.2 的 executing-plans/SKILL.md 與 GitHub 同名標籤 sha256 相同，僅 1 檔 1 次樣本）；⚪ 複盤 §6 未勾選（歸檔複盤不改，以本 handoff 為處理紀錄）。
- **記憶改進**：`feedback_subthreshold_red_risk_discuss.md` 加 Refinement＋MEMORY.md 索引行（端出前先用事實答「不做會怎樣、發生過嗎」，答不出標推測不升級；被反問先查再改口）。
- 封裝候選檢查：backlog 無 open `[SOP 候選]`，無命中。
- **結算**：`task-20261006-vs-execution-record-capability`（決策 B）標 NEXT（序 5、4 個可升子項，經使用者確認）。

### 三、未完事項 / 接力棒

- [#接力] **本 session 改動未 commit**（`CLAUDE.md`、`workflow-harness/work-map.jsonl`、本 handoff）——收工時待使用者確認。
- [#接力] 審查提醒把 `work-map.jsonl` 算成 code（`code_review`／`precommit` 為 stale）；未跑，未查以前改工作地圖是否跑過，已告知使用者。
- [#接力] Verification Strategy 下一步已選**決策 B**（使用者依建議裁定，`task-20261006-vs-execution-record-capability` 標 NEXT）。理由：接在今天決策 A 之後、同一條線；C2 登記為延後、G2 加註是事件觸發不可主動開工、Verify/Sync 無急迫性。⚠️ B 不能直接拍板：研究文件 §5 寫明須先重開 C1 §5 第 9 條（T2 信任邊界未實測）與第 10 條（第二個 runtime），兩項實測規模【未查】。備選：紅旗改寫可交付實際改動，若要先出成果可換它。
- [#不重議] 複盤 §6：(a) 併入紅旗改寫、(b) 不存記憶、(c) 已寫 CLAUDE.md、第 2 點「確認方法」不補。
- [#接力] 照舊：commit 未 push（main 比 origin 多 21 筆）；`v3.0.0` tag 未打。

### 四、洞見 / 反省

**【紀律接力】**

- **修正句說過頭（今天第 8 次）**：收回建議時寫「本機副本都放在帶版本號資料夾」，沒查就寫；下一輪才實查（剛好成立）。做法照舊：寫替代句前先答「證據是哪一行、射程是不是全部」。
- **要使用者反問才發現「不需要」**：把審查的 ⚪ 套上「假合規」標籤升級端出，沒先問「不做會怎樣、發生過嗎」；使用者一問就收回，且收回也沒查證——兩個方向都是推理沒碰事實。全域 CLAUDE.md 已有對應條文（能碰就碰、六軸下游、三關必要性）仍復發，故改記憶索引行而非加 CLAUDE.md。做法：端出任何「建議要做」前，先用事實答「不做會怎樣、發生過嗎／做的代價」；被反問先查再決定維持或收回。

**【當日洞見】**

- **bridge README 一份裝三種東西**：使用手冊（採用者）、設計說明（為什麼長這樣）、查證紀錄（某天對某版查到什麼）。有日期的上游行為寫進「設計說明」，上游一改說明就過期；寫進「查證紀錄」再連過去，改版時只動紀錄。固定版本連結只是讓過期可辨識，分開放才減少過期。
- **使用者的反問是在測必要性**：「有需要寫這麼詳細嗎」「為什麼要指向固定版本」兩問都讓結論變得更扎實或被收回——代表我端出前少做了一步必要性自問。

**【學習候選】**

- **Case**：CLAUDE.md 文件審的 ⚪「確認標籤內容沒寫方法」，我升級為高風險端給使用者；使用者反問後收回，收回句又未查證。使用者問「為什麼有些事情要我反問你之後，你才能夠發現不需要」。
- **Candidate Pattern**：把審查小項或自己的建議端給使用者前，先用事實回答「不做會怎樣、發生過嗎」與「做的代價」；答不出事實就標推測、不升級。被反問時先查再改口。不適用：使用者明確要求列出所有可能項時。
- **Evidence**：本 session 1 例（同 session 稍早 (c) 也是使用者問「README 的功能是什麼」才引出更根本的分法，性質相近但不完全同型）。Hypothesis。
- **Minimum Sufficient Intervention**：已改既有記憶 `feedback_subthreshold_red_risk_discuss` 與 MEMORY.md 索引行（常駐載入）；不新增 CLAUDE.md 規則（已有對應條文仍復發，且說不出 enforcement 掛點）。觀察：下次再因使用者反問才發現「不需要」即記第 2 例。
- **Promotion**：Refine Existing Strategy（已做）；是否進一步升級由使用者決定。

### 五、檔案異動

錨來源：本 session 開工 commit（f877960、開工於 2026-10-06T17:39:11）——列 f877960..HEAD（區間內無新 commit）

- 未 commit：`CLAUDE.md`（雙語策略節新增「引用上游原文當查證依據」一段）、`workflow-harness/work-map.jsonl`（`task-20260901-claudemd-governance-rewrite` name 改寫）、本 handoff
- repo 外：`~/.claude/projects/C--Users-user-orca-openspec-schemas/memory/feedback_subthreshold_red_risk_discuss.md`、`MEMORY.md`

### 六、下一步建議

1. 決策 B：先查 C1 §5 第 9、10 條要補的實測有多大，再開工。
2. 紅旗改寫（`task-20260901-claudemd-governance-rewrite`）範圍已擴大、依賴已撤，可排進主線考慮。
3. 不急：push 未推送的 commit；`v3.0.0` tag；task-brief 上游回報草稿（已標 NEXT）。
