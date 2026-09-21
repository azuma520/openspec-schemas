# Session Handoff — 2026-09-21

<!--
本檔每個 session 結束時 append 一個 ## Session HH:MM 區塊。
六欄 heading 順序固定，缺漏會被 Stop hook block。
四欄內 sub-segment marker（**【紀律接力】** / **【當日洞見】**）缺漏會 Stop hook ⚠️ Warn（不 block）。
-->

## Session 08:01

### 一、本 session 主題

**Q8 / B 小實驗（散文 vs 結構化規則的可判性 pilot）＋ 9/21 外部審補課。**

本區塊 08:01 先以進行中形式寫入（日期由 09-17 跨到 09-21 觸發 Stop hook），
其後在**同一區塊**持續補完，不另開區塊——與 `session-handoff-20260917.md` 同型。

本 session 由使用者拍板開 B 小實驗，並把主線 `superpowers-bridge 下一代改造` 的
下一步指向它（不從四個可升子項先拍一條）。08:06 Codex 週級額度恢復後，
接著補跑積欠四天的外部審。

### 二、完成事項

- **work-map 更新**：`task-20260915-b-structured-definition-experiment` 改為 `DOING`、
  `parent` 掛到 `task-20260826-superpowers-bridge-next-gen`。已跑引擎驗證主線的
  「下一步」現算結果確實變成 B（非宣稱）。四條 TODO 子項未動。
  ⚠️ 機制事實：`/work-status` 的「下一步」**沒有手寫欄位**，由子項現算。
- **B 小實驗跑完 24 格**（A0/A1/A2/A3 × 六輸入，每格一位盲判 fresh reader、模型固定
  sonnet）。產物七檔在 `docs/superpowers/poc/2026-09-17-q8-structured-definition/`。
- **結果**：A1/A2/A3 三個 Arm **合計 18 格全滿**（Determinacy 18/18、Correctness 15/15、
  Agreement 未量測）；**A0（修正前散文）6 格中 3 格分歧**——I1 UNDETERMINED、
  I4 與 I5 自信判 PASS（修正後為 BLOCK）。
- **三輪外部審已派兩輪、成功兩輪**：
  - workflow-harness `0b5cdb6` **程式面** → **⛔ Blocked**（2×P1、2×P2、1×Nit；
    依 Anchor Register #3 升 `thorough`，故 4 條擋門）
  - openspec-schemas **Q8 文件面** → **⛔ Needs revision**（6 條 blocking）
  - 已記 `[REVIEW_STATE] doc_review fail, rounds 1`
- **依 Codex doc review findings 修正報告（使用者裁定走「乙」）**：逐案 commit
  provenance、四個 experiment design defect 明列、重跑準則改標真實來源、複驗指令改為
  可跑、handoff 補成現況。**未修改 Arm 2/3、未重跑、實驗刺激材料保持原狀。**
- **第二輪 Q8 文件審（fallback，Codex 額度耗盡）→ ⛔ Needs revision，2 條 blocking**，
  兩條都打在同一處：§6 的「機械驗證」區塊**標錯了證據出處**。那些數字是對 scratchpad
  生成的配對檔跑的，不是對凍結的 `inputs-six-cases.md`——而該凍結檔 I3 沒有 tasks.md
  那一側、I5 沒有 TDD 標註，且只記載 I1/I2 補了 plan.md（實際六組皆補）。
  **即凍結的 pre-registration 產物不足以決定實際用了什麼刺激材料。**
- **已修**：新增 `materialized-inputs.md` 記錄實際餵給判讀者的六組完整 `tasks.md` /
  `plan.md`（已驗證與 24 份派工檔逐位元相同），§6 改為指名該檔並**實跑複現**過；
  另修 7 處 🟡/⚪（D5 表述差異補列、缺口格數 5→7、圍籬掃描補做確認為 0、
  Arm 0 逐位元比對寫明方法、行數欄位口徑說明、handoff「各 18 格」措辭）。
  **凍結檔仍未被修改。**

- **workflow-harness `0b5cdb6` 程式面：P1-2（fail loud）與 P2-1（例外契約）已修完**，
  改在 worktree `.worktrees/fix-issue-4-worktree-canonical-root`，**尚未 commit**。
  - **P1-2**：`find_project_state_root` 由兩種結果改為**三種**——認證通過的 worktree →
    主樹；**可證明不是 worktree**（`.git` 為目錄或不存在、pointer 但無 `commondir`）→
    `harness_root`；**無法安全解析**（指標是 link/junction、格式不成立、認證不過、
    讀取出錯）→ **`None`**。新增 `_dotgit_kind()` 做這個分流。
    Stop 在解析任何 base **之前**先擋（`_emit_block`），順序刻意——其下的
    ultra-degraded 出口是 `exit 0`（跳過閘門），先跑它就正好是 Issue #4 要消滅的
    靜默退讓。`paths_runtime.resolve_for_hook_read` 在 `None` 時回 `None`（縱深防禦）。
  - **P2-1**：三處 except 補接 `RuntimeError`。
  - 清掉死碼 `_is_plain_regular_file`（邏輯併入 `_dotgit_kind` 後零呼叫）。
  - **行為改動使 18 條既有測試轉紅**——全是編碼舊 fallback 行為的那些，已照新契約
    改寫並更名（`_returns_itself` / `_falls_back` → `_is_unresolved`，舊名字陳述的是
    已被移除的行為）。新增一條反向控制（`.git` 為目錄的主樹仍須 ALLOW）。
  - **全套測試：`7 failed, 3183 passed, 4 xfailed`。** 7 條為 `red-evidence.md` 記錄的
    既有 baseline（與本次無關）；passed 由 3182 → 3183，差額剛好是新增的反向控制。

- **P2-2 / 文件面 3 條 / P1-1 落地，全部完成**（2026-09-21 續做）：
  - **P2-2**：`test_separate_git_dir_main_tree_without_commondir_returns_itself` 改用
    **真 git** `init --separate-git-dir` 建版面（舊版是「worktree 版面扣掉 commondir」，
    名字說 A、建的是 B），並把原手寫格拆成獨立一條保留其判定意義；
    `test_10_main_cwd_l2_text_unchanged` 改為 `..._both_l2_hints_byte_identical`，
    **兩個** Layer-2 提示各自逐字比對全文（舊版只跑一個、只比一個子字串）。
    補四種缺的版面：母 repo 被搬動、一般 submodule、submodule 背後的 worktree、
    **根路徑本身含中文字元**。
  - **文件面**：測試數字全部**重新量測**（`--collect-only`）——
    `test_project_state_root.py` **38**、`test_session_start_worktree.py` **11**、
    `TestStopHookLinkedWorktree` **11**、`test_paths_runtime_hook_read.py` **6**；
    `brainstorm.md` E5 那列的可重跑指令同步改正（原寫 27、跑出來 38）。
    `design.md:3`「3 份 live spec」改為「兩份」並點名（與 `brainstorm.md` E2 一致）。
    `proposal.md` 補上 `handoff-guard` 的**第二條 MODIFIED**、把「刻意不動」收窄到
    真正沒變的部分（原寫「SessionStart→Stop 的 read-target」整項不動，與交付的 delta 不符）。
  - **連帶修正（同一類，文字沒跟上實作）**：文件多處寫 bare / separate-git-dir /
    symlink 指標「會 fallback」——該行為今天已移除，全部改為 unresolved；
    `design.md` 新增 **D9** 記錄 fail-loud 的三結果契約與理由。
  - **spec 同步**：`specs/project-state-root/spec.md` 由兩結果改寫為**三結果**契約
    （簽章改 `-> Path | None`、逐步驟標明何者回 `harness_root`、何者回 `None`、
    例外集合加 `RuntimeError`），新增四個 Scenario（submodule 自身／submodule worktree
    unresolved／母 repo 搬動 unresolved／`RuntimeError` 被接住）與一條新 Requirement
    「An unresolvable project-wide state root MUST stop the Stop hook」。
    ⚠️ 這條是必要的：改前 spec 比實作**寬**，後人會把 fail-loud 當 bug 修掉。
  - **P1-1 落地**：`proposal.md` 新增 §殘餘風險——讀取端／寫入端兩半的分工表、
    本 change 只保證讀取端、**不宣稱**已關閉資料遺失生命週期；與
    `task-20260904-worktree-handoff-lifecycle` **兩邊互指**（work-map 那筆也加了
    反向 cross-reference）。明文記下**該線不是 Issue #4 的關閉前置**。
  - 另收四條 🟡：`stop._same_path` 在 merge-base 並不存在（design/tasks 兩處措辭更正）、
    `plan.md` 的 PR 前置補上 4.4a 外部補審閘門、`handoff-guard` spec 補上 Layer-2
    位置後綴的 byte budget 例外（該例外原只記在會被 archive 的 design.md）。
  - **驗證**：全套 `7 failed, 3189 passed, 4 xfailed`（7 條為既有 baseline，逐條相同）；
    `openspec validate fix-worktree-canonical-root --strict` 通過；
    `test_change_delta_integrity.py -k fix-worktree-canonical-root` 4 條全過。

- **第二條線（文件同步／解耦研究）第一輪完成**，產物
  `docs/superpowers/research/2026-09-21-issue4-information-item-inventory.md`（421 行）：
  - 以 **Issue #4 本次真實變更**當第一組 ground truth，單位是**資訊項**（規則／主張／
    數值），檔案只當 carrier。共 **17 項**，每項記四欄：角色／關係／同步粒度／
    這次實際怎麼發現漂掉。
  - **分布**：必須同步 13、相關但解耦 1、歷史保留 2、**未決（混合角色）1**。
    必須同步的 13 項中，語意 8、字面或數值 5。
  - ⚠️ **偵測手段的分布是本輪最強訊號**：**沒有任何一項是被自動化機制發現的**——
    外部審讀／比對 9、外部審實際執行指令 1、我自己主動掃 2、順帶注意到 1、
    使用者裁定 1、不適用 3。
  - 新增 **§分析**（8 個 semantic-sync 項的共同結構，**暫定**）與 **§研究邊界**。
    重點：不變量多為**集合關係**而非文字相等（8 項中 6 項為包含或互斥）；
    source/derived 方向**不統一**（code→prose / delta→prose / prose→prose 三種並存）；
    source 側多半可機械抽取，**derived 散文側是唯一難點**；
    **I16 是唯一 derived 端可機讀、也是唯一已有機械檢查的案例**。
  - 依指示**不升類**：「已移除行為仍被描述」記為 failure mode；「同義但不同寫法」記為
    semantic sync 候選性質（本輪 17 項**無任何實例**）。
    surface lifetime（1/8）與 finding 上下游（1 例）**證據不足，不升為通則**——
    先前「文件面應掃相鄰而非掃同類」的說法證據不足，已收回為觀察。
  - **不導出任何機制、不做設計決策。**

### 三、未完事項 / 接力棒

- [#接力] ⚠️ **workflow-harness `0b5cdb6` 的文件面審：已降級派 fallback、結果未回**。
  使用者 2026-09-21 裁定兩件都降級。已記
  `[REVIEWER_FALLBACK] plane=doc_review scope=workflow-harness/fix-worktree-canonical-root
  from=codex to=contract-neutral-reviewer reason=quota`。
  ⚠️ **即使回 `✅ Mergeable` 也不使該 change 結案**：①程式面仍 `⛔ Blocked`；
  ②屬資料遺失類高風險，依專案 CLAUDE.md 2026-09-01 條件降級須補 Codex 那一輪
  （額度 13:07 恢復）。fallback 這輪拿到的是 findings，不是通行證。
- ~~[#接力] 程式面剩 P2-2 未修~~ **已完成**（見二欄）。原文保留以下細節供追溯：
  P2-2 = 三條比名字弱的既有測試（`test_separate_git_dir_main_tree_without_commondir_
  returns_itself` 沒真的建出 separate-git-dir 主樹；`test_10_main_cwd_l2_text_unchanged`
  宣稱文字不變卻只檢查一個子字串）＋ 四種缺的版面（母 repo 被搬動 / 一般 submodule /
  submodule 背後的 worktree / **根路徑本身含中文字元**——現有 CJK 測試只把 `文檔/`
  放在 ASCII 命名的根底下）。
- ~~[#接力] 文件面 3 條 blocking 未修~~ **已完成**（見二欄）。⚠️ 原記的
  「必須重新量測」已照辦，實測值為 38／11／11／6。原文保留：①所有測試數字過期
  （`test_project_state_root.py` 實 32、文件四處說 27；`TestStopHookLinkedWorktree`
  實 10 說 7；`test_session_start_worktree.py` 實 11、`plan.md:11` 用現在式說 9），
  且 `brainstorm.md:43` 把「27 collected」放進「可重跑的查證」欄、跑出來是 32——
  **那一列自己違反自己的契約**。⚠️ 我改完程式後這些數字**又變了**，必須重新量測、
  不可沿用上列數字。②`design.md:3`「3 份 live spec」與 `brainstorm.md:40`「兩份＋
  第三份是已更正的錯誤」互相矛盾，後者為真（grep 回 0）。③`proposal.md:56` 說
  「各一條 MODIFIED」但 `handoff-guard` 實有兩條，且 `proposal.md:31` 把
  「SessionStart→Stop 的 read-target」列為刻意不動，而第二條 requirement 正是改它。
- ~~[#接力] P1-1 文件落地未做~~ **已完成**（見二欄）。
- [#接力] ⚠️ **仍欠三輪審查，全部未記 pass**：
  ① **程式面重審**——本次改的是安全行為，且 18 條既有測試換了契約、另加 6 條新測試。
  ② **文件面重審**——change 的 11 份文件與 spec 本輪大幅改動（含一條新 Requirement）。
  ③ **workflow-harness 文件面補 Codex**——fallback 那輪的條件降級義務，額度 13:07 恢復。
  ~~spec 仍寫舊的兩結果契約~~ **已同步為三結果**（見二欄）。
- [#接力] **Q8 報告仍欠一輪 doc review**（openspec-schemas 側，`doc_review` 記在 `fail`）。
- [#接力] ⭐ **下一輪的分水嶺：「規範權威」vs「事實來源」**（使用者 2026-09-21 指定）。
  §分析 C 段觀察到**權威多半不在 spec**——事實來源多半是實作或已交付的 delta，
  spec 是被推導的一端。但那究竟是「應然如此」還是「本樣本的偶然」，本輪沒有答案。
  ⚠️ **先討論這一題，再決定研究方向**；不要順勢往下設計。
- [#不重議] 文件同步研究**不建立新 mechanism、不把分類改成正式規格、不宣告任何 final
  pass**（使用者 2026-09-21 明示）。樣本數 n=1，B/C/D 三段分布在第二個 change 上
  完全可能不同。
- [#不重議] **P1-1 已裁定（2026-09-21）：維持 scope、只修正宣稱。**
  同一事故有兩半——**讀取端**（hooks 在 worktree 讀錯 root）與**寫入端**
  （`/end-session` 仍可能把 handoff 寫在 worktree）。Issue #4 從一開始鎖的就是讀取端。
  - **不**把 `/end-session` 寫入端納入本 change（會把 bounded fix 擴成生命週期設計問題）。
  - ⚠️ **也不**把 lifecycle 修復設為 Issue #4 的關閉前置——否則 issue identity 會混掉：
    Issue #4 定義成 root resolution bug，該 bug 修好、review、dogfood 通過**即可關**。
    （agent 原先提的 ② 在這點上講太鬆，已由使用者更正。）
  - 但**接受 reviewer 指出的風險事實**：本 change 不得宣稱已完整解決 worktree handoff
    的資料遺失生命週期。要做的是：把文件宣稱收窄為「修復 hooks 的 project-wide state
    讀取 root」，並與 `task-20260904-worktree-handoff-lifecycle` 互相 cross-reference、
    保持該線 open。
  - 📌 **已唯讀掃描過**：`design.md:21,23,66,67` 與 `proposal.md:16,31` **已經**把寫入端與
    lifecycle 明列為刻意不動。所以待辦偏向「補 cross-reference ＋ 補一句殘餘風險」，
    而非「刪除過度宣稱」。⚠️ 尚未逐句讀完問題陳述與完成條件段，**還不能宣告「完全沒有
    過度宣稱」**。
- [#接力] **Q8 報告第二輪修正已完成，需再送一輪 doc review**（Fixing ≠ Verifying）。
  目前 `doc_review` 仍記在 `fail`，**未記 pass**。
- [#不重議] Arm 0 → Arm 1 的差異 **MUST NOT** 歸因給「結構化」——兩者規則內容本身就不同。
- [#不重議] 不修 Arm 2/3、不重跑 pilot。修了等於事後更動實驗刺激材料，原 18 格結果
  就不能再說是對「這份 Arm」跑的。使用者 2026-09-21 明示。
- [#不重議] 不補跑第一輪 18 格第二輪。Agreement 留作 experiment limitation。
- [#待裁] work-map 未知欄位 `evidence` 暫不處理（格式債非阻塞）。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] ⚠️ **「空輸出沒追」當日復發——這條 09-16 才剛接力過來。**
  我把四個 `git log -S` 查詢排成一張 `printf` 表一起跑。第一個字串在原檔**跨兩行**、
  回 0 命中，而並排格式讓下一列的標籤接在同一行後面，**我把「沒有命中」讀成了
  `e38e817`**，並據此寫下「六案都由同一 commit 修掉」這個已查證宣稱。是外部審抓到的。
  attribute：`session-handoff-20260916.md` 【紀律接力】「空輸出沒追」；
  全域 CLAUDE.md「宣告沒有／不存在前先列舉所有可能存放處逐一查完」。
  propose action：**多條查詢 MUST NOT 並排成表**——一條一行、且 0 命中要明確印出
  （`[ -z "$r" ] && echo "<<< 0 命中 >>>"`）。已寫進報告 §4 的複驗指令當示範。
  ⚠️ 使用者裁示：**本題只記 finding，不現在開新機制。**
  這已經不是「不知道」，而是**知道但工作當下沒有形成可靠的操作掛點**。
- [#反] **我的資訊量對等自查放行了四個真實偏離（D1–D4）。** 我確實做了自查、也補回
  四處漏搬，然後宣稱 Arm 2/3 與 Arm 1 等價——但 `outcome` 的 trim、畸形 TDD 標註、
  checks 9-11 的適用閘、plan 缺席時的重複掃描，四處都沒看出來。
  attribute：複審紀律「先讀實際驗到什麼、再讀名字說驗什麼」。
  propose action：**自查宣稱「等價」時，要逐條對照可觀察的判定差異，不是通讀一遍
  覺得都有寫到。**
- [#反] ⭐ **變異檢查本身也可能是假的。** 驗 `test_10_main_cwd_both_l2_hints_byte_identical` 時，
  我把 debug 後綴的字面換掉、測試沒轉紅，一度以為那條測試又是弱的。實際原因是
  **我的 replace 帶了 `,1`，只換了 2 處出現中的 1 處**——測試走的是另一處。
  換全部之後立刻轉紅。
  attribute：同「一個缺陷＝一類缺陷」——我在做同類掃描時只掃了一個實例。
  propose action（**維持 learning，使用者 2026-09-21 明示不開新機制**）：**做變異時先數 `count()` 再決定換幾處，並把數字印出來**；
  「改了但沒轉紅」的第一個假設應該是**變異沒生效**，不是測試沒守住。
  ⚠️ 這條與上一條方向相反但同樣重要：上一條是測試假綠，這條是**檢測手段**假陰性。
  兩者疊加時最危險——弱測試 ＋ 不完整的變異檢查 = 看起來驗過了。
- [#反] **本 session 我自己抓到的 blocking 缺陷：0。** 程式面 4 條、文件面 6 條，
  全部由外部審抓到。這與 09-16 記的「五個 P1 全由外部審抓到」同型，**累積 2 例**。
- [#反] ⭐ **我自己新寫的測試是假綠燈，靠 mutation check 才抓出來。**
  為 P2-1 補的 symlink-loop 測試跑起來是綠的，但把三處 `RuntimeError` 拿掉後
  **33 條照樣全過**——它根本沒守住它名字宣稱的東西。原因：**本機是 Python 3.13.5，
  `resolve()` 對 symlink loop 已不再拋 `RuntimeError`**（直接回傳路徑），
  審查者說的是 3.9–3.12。改成注入條件（monkeypatch `Path.resolve` 拋 RuntimeError）
  直接測處理器後，變異檢查轉紅（1 failed，RuntimeError 穿出），還原後 33 全綠。
  attribute：複審紀律動作版「宣稱這條測試守住 X 時 SHALL 當場把 X 破壞掉跑一次、
  看轉紅數——不是看測試名、不是用讀的推論」。
  ⚠️ **這是「測試存在 ≠ 測試真的守住契約」的一個完整真實案例**：綠燈、名字正確、
  邏輯看起來也對，唯一能發現的方法是破壞它。而我當時正在修的 P2-2 就是同一類缺陷——
  **我一邊修別人的假測試，一邊寫了一條自己的。**
  propose action：**環境相關的失敗條件（直譯器版本、OS、檔案系統）不可用「製造真實
  觸發條件」來測**——本機不觸發時測試會假綠。改用注入，測的是處理器不是觸發器。
- [#觀察] **「判定一致」不等於「理解一致」**，累積 1 例（I5：三個 Arm 走三條不同條款、
  判定全同）。指標只收 verdict 時完全不可見。
- [#觀察] **缺規則不一定產生不確定，有時產生非常確定但沒人拍板過的答案**，累積 3 例
  （I6 圍籬四個 Arm 全判 BLOCK、A0_I4、A0_I5）。
  推論：`UNDETERMINED` **不是完整的規則缺口偵測器**。

**【當日洞見】**

- **實驗結果本身可以沒錯，實驗解釋仍然可以錯。** 這次 24 格數據沒有因為兩個重大錯誤
  而消失；壞掉的是「我以為為什麼會得到這些結果」（假的單一 commit 歸因）與
  「我以為三個 Arm 控制了哪些變因」（假的等價）。**修正方式是降低可宣稱範圍，
  不是重做實驗。**
- **逐案 provenance 的真相**：I1/I3/I4 → `e38e817`（09-08）；I2 → `932a044`（09-02，
  v1→v2）；I5 → `4626e96`（09-14）；I6 從未被修。天花板效應的**方向**成立，
  但機制是「三次不同修正各蓋一部分」，不是一次。
- **A0_I1 回 UNDETERMINED，理由正是 FIELD CARDINALITY 當初要解決的事**
  （「規則沒說一筆紀錄帶兩個 `subject:` 時該讀哪一個」）。24 格裡唯一的 UNDETERMINED。
- **那條「9/21 08:06」門檻本身就是 Codex 週級額度的恢復時間**（09-16 handoff 三處寫明）。
  而**額度在兩次派工後就再度耗盡**（13:07 才恢復）。⚠️ 這代表「等 Codex 恢復再補審」
  的策略比預期脆弱：一個恢復窗口能支撐的派工次數，比一個 change 需要的審查輪數還少。
- **我在派工前自己抓到一個會污染 I6 的錯**：Arm 2/3 初版開頭寫了「對圍籬與 HTML 註解
  未作任何規定」。Arm 1 是沉默的、Arm 2/3 卻明說自己沉默，會把讀者推向 UNDETERMINED。
  已刪除並複掃無洩漏。
- **`Shared definitions, used by checks 8-11` 射程錯誤在 `e38e817^` 就已存在**，
  不是修正時引入的。
- **13 個既有 fixture 對六個輸入的覆蓋是 0/6**（四項全集命中 0，比 09-08 報告自己記的
  「三條無 fixture」多一條）。

### 五、檔案異動

- `workflow-harness/work-map.jsonl` — B 小實驗那筆改 `DOING` + 掛主線（僅 1 行；
  換行結尾與 HEAD 一致：23 LF / 0 CRLF）。
- `docs/superpowers/poc/2026-09-17-q8-structured-definition/` — 新增**八檔**
  （arm0 / arm1 / arm2 / arm3 / inputs / **materialized-inputs** / pre-registration /
  results）；`results-and-next-step.md` 依兩輪 doc review findings 改寫過兩次。
- `文檔/handoff/session-handoff-20260921.md` — 本檔。
- **workflow-harness worktree `.worktrees/fix-issue-4-worktree-canonical-root`**
  （**未 commit**）：`hooks/lib/project_state_root.py`（三結果契約 + `_dotgit_kind`
  + 刪死碼 + 接 RuntimeError）、`hooks/lib/paths_runtime.py`（`None` 不代換）、
  `hooks/stop.py`（fail-loud 訊息常數、`_state_root()` 改 raise、main() 前置擋門）、
  `hooks/lib/test_project_state_root.py`（13 條改寫更名 + 5 條新增 + 1 條重建 + 模組註記）、
  `hooks/test_stop.py`（⑥ 改為 BLOCK + ⑥b 反向控制 + ⑩ 改為兩提示逐字比對）、
  `openspec/changes/fix-worktree-canonical-root/` 全部 11 份文件
  （proposal / brainstorm / design +D9 / plan / tasks / 四份 spec）。
- `workflow-harness/work-map.jsonl`（本 repo）— lifecycle 那筆加反向 cross-reference。
- `docs/superpowers/research/2026-09-21-issue4-information-item-inventory.md` — 新增
  （17 項盤點 + §分析 + §研究邊界，421 行）。

**尚未 commit。** 未追蹤檔另有 `2026-08-27-brainstorm-產品承諾.md`（長期刻意排除）。
**無專案資料夾** → Changelog skip。**驗收節點無可回填** → skip。

### 六、下一步建議

> **本 session 停在 decision checkpoint（使用者 2026-09-21 指示）**：fail-loud 這個
> 設計問題已決並實作完成、有變異檢查證據，刻意**不**順勢把剩餘項做完，
> 以免把「Issue #4 收尾」與「Q8 下一步」兩條討論線黏在一起。
> **未記任何 pass、未宣告 Issue #4 完成。**

> **狀態定位（使用者 2026-09-21 用語）：Implementation complete / Verification pending**——不是「完成」。
> 範圍內的實作與文件修正已全部收乾淨（P1-2、P2-1、P2-2、文件面 3 條、P1-1 落地、
> spec 同步、4 條 🟡），但**尚未取得最後審查**。未記任何 pass、未宣告 Issue #4 完成——
> 測試綠不等於通過審查。

1. **13:07 後補 Codex 三輪**：① workflow-harness 程式面重審 ② 同 change 文件面
   （條件降級的義務，fallback 那輪不能代替）③ openspec-schemas 的 Q8 報告 doc review。
2. 三輪都過之後才談：commit（走 `/smart-commit --execute`）→ PR（需 4.4a 通過）→
   merge → 更新 plugin cache → 真實 linked worktree dogfood → 才把 work-map
   `task-20260915-stop-hook-worktree-root` 標完成。
3. **Q8 的 §9 三條路**（甲改量測／乙找新案例／丙收掉）待使用者拍板——
   使用者表示要另起一條 Q8 設計討論，本 session 不碰。
4. `task-20260904-worktree-handoff-lifecycle` 維持 open，與本 change 互指；
   ⚠️ **不是** Issue #4 的關閉前置。
4. 主線 `superpowers-bridge 下一代改造` 的下一步目前指向 B 小實驗；pilot 已收束，
   §9 的三條路（甲改量測／乙找新案例／丙收掉）待使用者拍板。
   ⚠️ 相對初版，**甲的成本已上修**——D1–D4 使任何後續表示形式比較都必須先修 Arm
   並重跑，不能沿用本輪材料。
