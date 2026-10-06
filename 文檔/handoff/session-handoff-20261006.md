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
- [#接力] 審查暫存檔待手動刪（AI 的 rm 被擋）：scratchpad 下 `rv/`、`rv2/`、`c1r3/`；本機另有三個巢狀測試 session 的逐字紀錄在 `~/.claude/projects/` 以測試專案路徑命名的目錄。
- [#接力] 照舊：`v3.0.0` tag 未打；`.claude/worktrees/requirement-scenario-identity` 空目錄待刪。
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
3. 不急：`v3.0.0` tag；task-brief 上游回報草稿（已標 NEXT）；手動刪 scratchpad 審查暫存。
