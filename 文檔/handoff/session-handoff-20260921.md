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


---

## Session 18:33

### 一、本 session 主題

補齊 09-21 早場接力棒第 1 條指名的**三輪外部審**，並收完其中兩輪回報的 blocking
findings。三輪為：① workflow-harness `fix-worktree-canonical-root` 程式面重審
② 同 change 文件面（條件降級的補審義務）③ openspec-schemas 的 Q8 報告 doc review。

**①③ 取得結果、皆為 Blocked；② 未取得**（Codex 額度當日第二次耗盡，22:13 恢復）。
使用者裁定：先修完 ①③ 已確認的問題，22:13 後再對①②③的**最終狀態**重審——
不浪費第②輪去審一份馬上會過期的狀態。

本 session **未記任何 pass、未 commit**。

### 二、完成事項

- **三輪審查派工**（tier 一律 `thorough`，依 Anchor Register #3 資料完整性升級）：
  - ① 程式面：範圍取**整條 branch**（commit `0b5cdb6` ＋ 未 commit 的修正，21 檔 +2756），
    不只取未 commit 的 delta——契約本身被改了。額外要求 **Test Strength Audit**
    必交付欄位。→ **⛔ Blocked**，1×P0、2×P1、3×P2。
  - ③ Q8 文件面：8 檔一 batch、86KB、未超預算；link check `failures: []` / `unresolved: 0`；
    profile 全數 `full-design`。額外要求 **Verification Log** 必交付欄位。
    → **⛔ Needs revision**，7 條 blocking。
  - ② 文件面：11 檔 / 128KB 備料完成（link check 亦乾淨），派工時 **Codex 額度耗盡失敗**。
  - 三輪 prompt 皆依 `codex-invocation.md`：只給 metadata、強制自行讀／跑／查，
    未餵 diff、未餵結論。

- **①的 6 條 finding 我逐條讀碼核實，全部成立**。其中兩條的性質比報告寫的更重：
  - **P0**：`project_state_root.py` 把「缺 `commondir`」當成 main tree 的正面證據，
    但 `<gitdir>` 坐在 `worktrees/` 底下時那是**損壞**；且 `Path.is_file()` 會把
    `PermissionError` 吞成 `False`，所以不只「被刪」一種觸發。
    ⚠️ 而 `test_hand_built_pointer_without_commondir_returns_itself` **把這個不安全
    結果寫成測試固定下來**，docstring 還明寫它在 pin resolver 的決定。
  - **P1（`artifact_paths.py` 漏接 `RuntimeError`）是同一天稍早 P2-1 的同類漏網**——
    當時只補了 `project_state_root.py` 三處就收手。

- **決定一（證據保存，選甲）落地**：`docs/superpowers/poc/2026-09-17-q8-structured-definition/evidence/`
  29 檔 400KB——24 份派工材料、4 支產生器、`results.json`、README。
  - 起因：Codex 判「證據鏈不存在、無法獨立稽核」。**依 repo 現況那個判定是對的**；
    追查後發現材料還活在會被回收的 session scratchpad。
  - 內容掃過：無金鑰／token／email。三支產生器有硬寫絕對路徑，**刻意不改**——
    改產生器就是改證據。
  - ⚠️ **mtime 揭穿一件事**：`pairs/A1_*`、`A2_*`、`A3_*` 那 18 份的 mtime 是
    **09-21 08:45 而非 09-17**——當天跑 `gen_materialized.py` 時它 exec 了
    `gen_pairs.py`、**把原始派工檔覆寫了**。那 18 份是重新產生的，**09-17 原件無副本**。
    A0 的 6 份則是同期（A0 本就 09-21 才跑）。README 為此立了逐檔「證明力分級」表。
  - 用救回的檔案把 Codex 標「could not check」的 byte-identity 宣稱**驗成 holds**：
    六組材料逐位元出現在 `A1_I*.md`，0 例外。

- **決定二（Q8 報告）落地，7 條 blocking 全收**：
  - **Correctness 分母 15 → 12**，機械算出、非挑選。判準從凍結檔本文字串抽取
    （I1「只答 BLOCK 不算判對」、I4「兩段式必答點」、I6 事前登記排除），
    再逐格檢查 `results.json` 的 route 能否承載各自要求：I4 三格皆逐字記下正確讀法
    → 可評；I1 要的是恰兩條 finding ＋ 兩條刻意不報，一句 `BASIS` 撐不起、且
    `A1_I1` 實際只記一條 → 不可評。寫成可重跑腳本 `recompute-correctness.py`。
    ⚠️ **報告中明寫 I4 留在可評集是一個解讀**、若採嚴格讀法分母為 9（數值同 100%）。
  - 從派工檔挖到機械事實：指令只要求 `VERDICT:` 一行 ＋ `BASIS:` 一句，
    **從頭到尾沒要求列 finding**——finding set **不是事後遺失、是派工設計上就沒收**。
  - **D6（第五個 decision-affecting 偏離）**：A1 數前導**空白格數**
    （`arm1-prose-baseline.md:20-21` 逐字 `its number of leading spaces`），
    A2/A3 數前導**空白字元數**（`arm2/arm3:13` 的 `L1`）。已機械驗六組材料
    前導 tab 命中 **0**、未被觸發。編號跳過 D5（D5 已用於不影響判定的表述差異）。
  - I3 的 task number 由「無 task line」更正為 `1.1`（結論不變、**寫出來的證據是錯的**）。
  - §1「六個輸入皆取自已修好的 finding」與 I6「從未被規定」矛盾 → 射程收窄為 I1–I5。
  - 新增 **§6.1 experiment specification defect**：S1 = I2 的 provenance 不實
    （f7 原檔 20 行，刪 RED `subject:` 應剩 19，凍結檔只有 8——標題／空行／第二筆任務
    也被刪）；S2 = I1 凍結要求與事前登記 metric 互相矛盾。**凍結檔未修改。**
  - 事前登記時序**降級為未經佐證的作者宣稱**；SHA256 能證明與不能證明的分別寫清楚。
  - §8 已知限制新增三列：證據鏈當時不在版控、事前登記無法佐證、24 格皆無原始回覆。

- **決定三＋程式面 6 條全修完**，`7 failed / 3193 passed / 4 xfailed`——
  failed 與 `red-evidence.md` 的 baseline **逐條相同**，passed 由 3189 增 4，
  差額剛好是新增的 4 條。
  - **兩次變異檢查（動作版，非讀碼推論）**：拿掉 `worktrees/` 判別 → **2 條轉紅**；
    注入同名原地改寫 → `test_does_not_mutate_disk` **轉紅**（修改前只比檔名、會放行）。
  - submodule 兩條改用**真 git** 建（`protocol.file.allow=always`），手寫版保留但
    改名說實話「pin 的是決定、不是 git 實際寫出的版面」。
  - P1 雙重解析：`resolve_for_hook_read` 新增 `state_root` 參數，Stop 解析一次傳下去。
  - spec 收窄到與實作一致（**spec 比實作寬正是這次 P0 能活下來的機制**），
    `openspec validate --strict` 通過、delta integrity 4 條過。
  - 文件測試數字重新量測：`test_project_state_root.py` **38 → 42**，
    其餘（`test_session_start_worktree.py` 11 / `TestStopHookLinkedWorktree` 11 /
    `test_paths_runtime_hook_read.py` 6）未變。

- **同類全掃並留紀錄**（使用者明示要求，不得只修被點名位置）：
  新檔 `openspec/changes/fix-worktree-canonical-root/resolve-exception-sweep.md`。
  AST 掃全 repo：56 個 `.resolve()`、37 個納入判定、**25 個未被 `RuntimeError`
  或廣義 handler 覆蓋**。修 3 個 in-scope，其餘 22 處 / 8 檔記
  `[OUT_OF_SCOPE_DEFERRED]` 附完整負面證據——全修會超過 scope-discipline 斷路器
  門檻（>5 個 baseline 外檔案）。掃描紀錄自述兩個限制：只掃 `.resolve()` 一種載體、
  AST 只看語法上包住的 `try`、不追跨函式呼叫鏈。

- **週一 backlog 週檢**（第 3 次 shadow 掃描）：0 筆可自動刪、1 筆待拍板
  （`[優化建議] [mature: 2026-09-07]` 讀了名字沒讀它實際說什麼）。
  ⚠️ **射程不完整**：8 條裡只有 1 條有穩定 `#NNN`，7 條沒編號因而未進比對；
  W37/W38/W39 三輪皆因 coverage 不完整**永遠不計入**四輪時間盒，
  **已完成判讀的輪次為 0 / 4**——時間盒實際在空轉。
- 上述 mature 條目 **case-count 由 5 累加至 6**（本 session 四條比名字弱的測試）。

### 三、未完事項 / 接力棒

- [#接力] ⚠️ **第②輪（workflow-harness 文件面補 Codex）仍未取得**。
  這正是 09-21 早場記的「條件降級補審義務」——早場已走過一次 fallback
  （`contract-neutral-reviewer`），義務指名要補的就是 **Codex 那一輪**，
  **再派一次 fallback 不清償它**。備料已完成（11 檔 / 128KB、一 batch、link check 乾淨）。
- [#接力] ⚠️ **三輪都要對最終狀態重跑，且重審對象比第一輪更大、不是更小**：
  本 session 動了程式 5 檔、spec、5 份 change 文件、Q8 報告大改、兩個新目錄。
  **目前沒有任何一個 plane 記了 pass。Fixing ≠ Verifying。**
- [#接力] `workflow-harness` 未裝 sd0x 的 `review-state.js`，它那兩輪的 verdict
  **沒有 state slot 可記**；依 hook-lightweighting，durable record 即本 handoff 與對話。
  openspec-schemas 的 slot **不可**拿來記它的 verdict（digest 綁的是另一棵樹）。
- [#接力] **本 session 全部未 commit**。兩個 repo 都是 dirty：openspec-schemas
  （Q8 報告 + evidence/ 29 檔 + recompute 腳本 + backlog + work-map）、
  workflow-harness worktree（程式 5 檔 + change 文件 + 掃描紀錄）。
  依早場裁定「三輪都過之後才談 commit」，**刻意不提前**。
- [#接力] 新登記 `task-20260921-path-resolve-runtimeerror-sweep`（`.resolve()`
  全庫例外保護對齊，22 處 / 8 檔 out-of-scope deferred）。
- [#待裁] backlog 那條 mature `[優化建議]` 仍待使用者決定保留／升級／移除。
  我的建議是**保留但改問法**：規矩已在全域 CLAUDE.md，再升級一條同義規範沒有掛點；
  真正的問題是「有規矩卻擋不住」，該收的樣本應換成「哪一層本來該喊卻沒喊」。
- [#待裁] backlog 射程問題（7 條無編號未進比對、四輪時間盒 0/4 空轉三週）未修。
- [#不重議] 決定一的範圍：**只保最小證據集**，且**保存不回溯提升歷史證明力**
  （使用者 2026-09-21 明示）。A0 缺原始回覆的缺口照實保留，不補歷史。
- [#不重議] 不重跑、不修 Arm 2/3（沿用先前裁定）。D6 直接補進報告並明寫為設計缺陷。
- [#不重議] Correctness 分母 **MUST NOT 靠直覺換**——必須從凍結規則與現有證據重新算
  （使用者 2026-09-21 明示，理由是這幾天一路踩到的就是這個）。

### 四、洞見 / 反省

**【紀律接力】**

- **「一個缺陷＝一類缺陷」在同一天內被實證違反一次。** P2-1 修 `RuntimeError`
  只補了 `project_state_root.py` 三處，第二輪審就在 `artifact_paths.py` 抓到同型。
  這次的做法改成：**先掃完同類、把掃描範圍與結果落檔、再決定修哪些**——
  而掃完才發現母體是 25 處、不是 2 處，且其中 22 處依 scope-discipline 不該在本
  change 修。**先掃再修不只是紀律，它改變了「該修多少」這個問題的答案。**
- **比「測試比名字弱」更深一層的形狀：測試把缺陷祝福了。**
  `test_hand_built_pointer_without_commondir_returns_itself` 的名字、斷言、實作
  三者完全一致，錯的是**被固定下來的那個行為本身**，而 docstring 還明寫它在 pin
  resolver 的決定。這一類**測試全綠、名字正確、邏輯自洽**，沒有任何一層會喊——
  只有外部審去問「這個被 pin 的決定對嗎」才抓得到。
  ⚠️ 它是**修復動作本身**產生的：上個 session 修 P2-2 時發現舊測試形狀錯，
  修法是另建真 git 版本、**卻把形狀錯的那個案例保留下來並祝福它的結果**。
- **證據只活在會消失的位置，是一個會重複發生的事故形狀。** 這次是 scratchpad 的
  24 份派工檔，09-04 是 worktree 裡的未追蹤 handoff。兩次都是「當事人知道它在哪，
  但那個位置不在任何人的保存範圍內」。**Reviewer 依 repo 判「不存在」每次都會是對的。**
- **保存證據 ≠ 提升歷史證明力。** 事後把材料補進版控，能讓未來可重驗，
  **不能**讓「當時已完整凍結／可重現」變成真。這次差點就在 README 裡寫成後者——
  擋下它的是去看 mtime，不是任何規則。
- **spec 比實作寬是缺陷能存活的機制，不是保守。** P0 的那個過寬 carve-out
  同時寫在程式註解、模組 docstring、spec 三處，彼此一致，所以三處互相佐證了一個錯的東西。

**【當日洞見】**

- Codex 的 read-only sandbox **沒有可寫的暫存目錄**，因此它**跑不了測試**。
  那份 70 條的 Test Strength Audit 是**用讀的推論**出來的——判「adequate」的那些
  尚未取得執行證據。它自己有誠實講，但若不看那句話會直接把它當成驗過。
- Codex 額度**一天內第二次耗盡**（早場一次、17:2x 一次）。它已不是偶發事件，
  而是需要納入排程假設的常態條件。
- **檔案 mtime 是這次唯一揭穿「這批就是當時派出去的檔案」的東西。** 內容看起來
  完全正確、hash 也算得出來，只有時間戳說出它是重新產生的。

**【學習候選】**

1. **Case** — 修 P2-1（`RuntimeError` 例外契約）時點對點修了 3 處就收手；
   同一天第二輪外部審在 `artifact_paths.py` 抓到同型漏網。這次改為先做 AST 全掃，
   掃出母體 25 處，其中只有 3 處依 scope-discipline 屬本 change 射程。
2. **Candidate Pattern** — 「一個缺陷＝一類缺陷」的既有規則只說了「要掃同類」，
   沒說**掃描要先於修復、且掃描結果要落檔**。先修後掃時，修改範圍已經先被
   「被點名的位置」決定了；先掃後修才有機會發現母體與射程不一致。
   **適用邊界**：缺陷有可機械列舉的同類載體時（例外 handler、API 呼叫點、字串模式）。
   不適用於語意性缺陷（無法機械列舉母體）。
3. **Evidence** — N=1 完整實例（本次）＋ 1 個反例（P2-1 先修後停）。
   因果尚未確立為通則，標 **Hypothesis**。
4. **Minimum Sufficient Intervention** — **不新增規則**。既有的「一個缺陷＝一類缺陷」
   已在全域 CLAUDE.md，本次的差異不在規則有無、在**執行順序**。
   建議改既有條文的動詞而非新增一條：把「立刻全範圍掃同類實例一次修完」
   改為「**先**全範圍掃同類、把掃描範圍與結果落檔、**再**依射程決定修哪些」。
   ⚠️ **enforcement 掛點**：外部審查（本次就是它抓到的）＋ 掃描紀錄檔本身
   （落檔後可被複審讀到，沒落檔則複審看不到範圍）。
   ⚠️ 但**掛點強度僅止於「有外部審時才會被發現」**——沒有任何機械檢查會在
   「只修被點名位置」時喊。若使用者認為這不夠，本項應降級為 Observe。
5. **Promotion** — 建議停在 **Refine Existing Strategy**（改既有條文的動詞，不新增規則）。
   正式升級由使用者決定。

### 五、檔案異動

**本 session 無 commit**（錨點 `commit_range`，開工 commit `ff3e806`、開工於
2026-09-21T17:09:07，`ff3e806..HEAD` 為空）。以下皆為 working tree 改動。

**openspec-schemas**（`C:/Users/user/orca/openspec-schemas`）：

- `docs/superpowers/poc/2026-09-17-q8-structured-definition/results-and-next-step.md` — 依
  第三輪 doc review 的 7 條 blocking 大幅修正（分母、D6、I3、I6 矛盾、§6.1、provenance 降級、§8）
- `docs/superpowers/poc/2026-09-17-q8-structured-definition/evidence/` — **新增 29 檔**
  （`README.md` ＋ `pairs/` 24 ＋ `generators/` 4 ＋ `results.json`）
- `docs/superpowers/poc/2026-09-17-q8-structured-definition/recompute-correctness.py` — 新增
- `backlog.md` — mature 條目 case-count 5 → 6
- `backlog-crosscheck-shadow.json` — 週一 shadow-plan 第 3 次掃描記帳
- `workflow-harness/work-map.jsonl` — 新增 `task-20260921-path-resolve-runtimeerror-sweep`
- `文檔/handoff/session-handoff-20260921.md` — 本區塊
- 未追蹤且長期刻意排除：`2026-08-27-brainstorm-產品承諾.md`

**workflow-harness worktree**（`D:/workflow-harness/.worktrees/fix-issue-4-worktree-canonical-root`，**未 commit**）：

- `hooks/lib/project_state_root.py` — P0 `worktrees/` 判別式、`gitdir` 只解析一次、
  `same_path` 接 `RuntimeError`、模組契約敘述收窄
- `hooks/lib/artifact_paths.py` — `_resolve_one` 與 `resolve_bases` 兩處補接 `RuntimeError`
- `hooks/lib/paths_runtime.py` — `resolve_for_hook_read` 新增 `state_root` 參數
- `hooks/stop.py` — 解析一次並傳下去，消除雙重解析
- `hooks/lib/test_project_state_root.py` — 42 collected（+4）：worktree 缺 commondir、
  commondir 不可讀、separate-git-dir 反向控制、真 git submodule ×2；
  `does_not_mutate_disk` 改為 bytes+sha 快照
- `hooks/lib/test_paths_runtime_hook_read.py` — 兩處改為完整四 base 等式斷言
- `openspec/changes/fix-worktree-canonical-root/specs/project-state-root/spec.md` — 步驟 3
  加判別式、新增兩個 Scenario
- 同 change 的 `brainstorm.md` / `design.md` / `plan.md` / `proposal.md` — 測試數字與行為敘述同步
- `openspec/changes/fix-worktree-canonical-root/resolve-exception-sweep.md` — **新增**（掃描紀錄）
- `hooks/test_stop.py` / `specs/handoff-guard/spec.md` / `tasks.md` — 早場改動，本場未動

**本 session 外的暫存**：`C:/Users/user/orca/q8-evidence-rescue-20260921/`
（救援中繼副本，內容已進版控，可刪）。

### 六、下一步建議

> **狀態定位：Fixes complete / Verification not started。**
> ①③ 回報的 blocking 已全數處理並附證據（含兩次變異檢查），但**修正本身尚未被
> 任何人審過**，且重審對象比第一輪更大。**未記任何 pass、未 commit。**

1. **22:13 後跑三輪重審**（順序不拘、可並行但注意額度）：
   ① workflow-harness 程式面（branch 範圍、tier `thorough`）
   ② workflow-harness 文件面（11 檔一 batch，**這是條件降級的補審義務、fallback 不算**）
   ③ openspec-schemas Q8 報告 doc review（含新增的 `evidence/` 與 `recompute-correctness.py`）
   ⚠️ 派工前重新抓 metadata——本 session 之後檔案集已變。
2. 三輪都過之後才談：commit（走 `/smart-commit --execute`，**不由 `/end-session`
   自跑**，2026-09-07 裁定的 B 路徑）→ PR（需 `plan.md` 4.4a 通過）→ merge →
   更新 plugin cache → 真實 linked worktree dogfood → 才把
   `task-20260915-stop-hook-worktree-root` 標完成。
3. **Q8 的 §9 三條路**（甲改量測／乙找新案例／丙收掉）＋ 那條 ⭐ 分水嶺題
   （「規範權威」vs「事實來源」）仍待使用者拍板。⚠️ 甲的成本因 D6 再度上修——
   現在是**五處**偏離都要先修才能重跑。
4. **backlog 兩件待裁**：mature `[優化建議]` 的保留／升級／移除；以及射程問題
   （7 條無編號、四輪時間盒 0/4 空轉三週，不修則該機制永遠評估不出結果）。
5. `task-20260904-worktree-handoff-lifecycle` 維持 open、與本 change 互指；
   ⚠️ **不是** Issue #4 的關閉前置（沿用早場裁定）。


---

### 追記（同一 session，22:13–23:05）—— 三輪重審的實際結果

> 本段是 `## Session 18:33` 區塊的續寫，不是新 session。18:33 當下的內容未改動。

**額度窗只夠一輪。** 22:13 恢復後派出①③，**①成功、③失敗**（額度第三次耗盡，
下次恢復 **2026-09-22 03:16**）；②從未派出。今日累計派工 5 次、成功 3 次、
額度失敗 2 次。**額度已是這條工作線的瓶頸**，不是時間也不是產出速率。

#### 第①輪重審：⛔ Blocked，2×P1 + 5×P2

⚠️ **最重的一條是我自己修出來的。** P0 的判別式我用了目錄名
`gitdir.parent.name == "worktrees"`，而 `worktrees` 是使用者可自選的普通目錄名。
以真 git 實測確認兩種合法版面被判成 `None`：

| 版面 | `gitdir` 父層名 | 判別式結果 | 正解 |
|---|---|---|---|
| `--separate-git-dir` 指向 `<x>/worktrees/repo.git` | `worktrees` | `None` ❌ | 回 root |
| submodule 掛在路徑 `worktrees/sub`（git dir 落在 `.git/modules/worktrees/sub`） | `worktrees` | `None` ❌ | 回 root |
| 真 linked worktree、`commondir` 被刪（對照） | `worktrees` | `None` ✅ | `None` |

**後果是 Stop 會對合法 repo 直接 BLOCK。** 改用結構性訊號 `<gitdir>/gitdir`
（`git worktree add` 必寫的回指檔）：實測 A 無 / B 無 / C 有，完全可分，
且它是 git 自己寫的結構，無法靠命名偽造。

#### 本輪修正（全部已收，含證據）

| 項目 | 證據 |
|---|---|
| 判別式改結構訊號 | 變異檢查：換回名字比對 → **2 條新反向控制轉紅**（真 git 建） |
| `test_does_not_mutate_disk` 再補強 | 加 `st_mtime_ns` / `st_mode` / `st_size`——原版同位元組覆寫、改 mtime 都抓不到 |
| 三條 P1 缺的回歸測試 | 變異檢查：三個修正逐一拿掉，**各抓到一條** |
| `hooks/artifact_paths.py:294` | 第二輪審指出實為 in-scope（`run()` 於 `:322` 一跳呼叫已改動的 `resolve_bases`），初版台帳誤 defer |
| spec 三處 | 補 `state_root` 參數與信任邊界（含「Stop MUST 傳、SessionStart MUST NOT」）、消除「不可讀 `commondir`」與第 64 行的自相矛盾、判別式改結構描述並**明文禁止用目錄名** |
| 掃描台帳計數更正 | 原寫 56（grep 行命中）與 22（混用檔案位置與呼叫運算式）**單位都錯**。正確：全 repo **314** 個呼叫運算式 → 納入判定 **37** → 已修 **5** → **deferred 20 個運算式 / 7 檔** |

**驗證**：`7 failed, 3199 passed, 4 xfailed`——failed 與 `red-evidence.md` baseline
逐條相同，passed 由 3193 增 **6**，差額剛好是新增的 6 條。
`openspec validate --strict` 通過。測試數重新量測：
`test_project_state_root.py` **42 → 45**、`test_paths_runtime_hook_read.py` **6 → 8**，
`test_session_start_worktree.py` 11 與 `TestStopHookLinkedWorktree` 11 未變；
四處文件引用已同步。

#### ⚠️ 本輪我做錯的事（與早場【紀律接力】同一形狀）

**我今天做過兩次變異檢查，兩次都只驗 P0 那一條。** 三個 P1 修正
（`state_root=` 傳參、兩個 `RuntimeError` handler、`same_path`）一條都沒驗——
拿掉它們測試全綠。是審查者點出來我才補的。

這與早場記的「一個缺陷＝一類缺陷」是**同一個形狀的第二個實例**：
紀律本身有做，但只套在**被點名的那一項**上，沒套在同一類的其他項。
早場那次是「修了三處就停」，這次是「驗了一條就停」。
⚠️ 兩次都不是忘記做，是**做了但沒做完**——而「做了」的感覺正好掩蓋了「沒做完」。

#### 使用者裁示（2026-09-21 23:05）

**03:16 的額度窗給第①輪（選項乙）。** 理由：①剛被大改過，且我已在它身上
留下一次實證的誤判紀錄（名字判別式）——它是最可能還藏著東西的那一份；
③的 blocking 多屬文件表述，風險不對稱。

②與③的補審順延。⚠️ **②仍是唯一不能用 fallback 清償的那一輪**
（09-01 定的條件降級補審義務指名 Codex）。
若該義務的原意是「高風險項要有獨立外部審」而非「必須是這個供應商」，
fallback 的定位可以重談——**但那是規則解釋，歸使用者**，本 session 未決。

#### 追記後的狀態

- **仍未記任何 pass、仍未 commit。** 兩個 repo 依舊 dirty。
- ①的第 3 輪、②的首輪、③的第 2 輪，三者全欠。
- 本輪新增檔案異動（在原「五、檔案異動」之上）：
  `hooks/artifact_paths.py`（`run()` 補 `RuntimeError`）、
  `hooks/test_stop.py`（新增 `TestStopPassesPreResolvedStateRoot` 結構守門）、
  以及 `project_state_root.py` / `test_project_state_root.py` /
  `test_paths_runtime_hook_read.py` / `specs/project-state-root/spec.md` /
  `resolve-exception-sweep.md` / `brainstorm.md` / `design.md` / `plan.md` /
  `proposal.md` 的再次修改。
