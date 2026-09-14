# 執行報告：loosen-plan —— schema v1 → v2，以及這個 repo 第一次真的走完自己的 apply 流程

> 寫於 2026-09-03。語言用繁中，理由與 `CLAUDE.md` 同一條：讀者是維護者與 Claude。
> Commit 範圍：`5aa19bf..84df208`（4 個 commit，18 檔，+1614 / −184），branch `worktree-loosen-plan`。
> 逐輪原始紀錄是 SDD ledger（`docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/progress.md`(原 `.superpowers/sdd/plan/progress.md`)，經 repo 的 `.git/info/exclude` 第 9 行排除 —— 見 §6 E4，**不是** `.gitignore`；注意在 worktree 裡 `.git` 是檔案不是目錄，該路徑要從主 checkout 讀；branch 收尾時刪除）；
> 本檔是它的可讀化萃取，**寫出來就是為了在那份 ledger 消失後仍然存在**。

## 0. 這份跟 `openspec/changes/loosen-plan/retrospective.md` 差在哪

兩份都不是對方的摘要，範圍不同：

| | change 的 `retrospective.md` | 本檔 |
|---|---|---|
| 對象 | 這個 change 的交付內容 | 這次**執行過程**本身 |
| 壽命 | 隨 change 進 `archive/` | 常駐 `docs/` |
| 回答 | 「v2 交了什麼、證據在哪」 | 「這套流程在這個 repo 實跑起來是什麼樣、哪些假設被打破」 |

會需要翻本檔的場合有三個：重新檢討 Anchor #4（§7）、決定 apply 的 worktree/PR 兩步要保留還是簡化（§6）、以及下一次要設計任何「用來證明某件事」的機制之前（§5）。

---

## 1. 做了什麼（事實）

**目標**：`superpowers-bridge` schema major 1 → 2。兩件耦合的事：

1. `plan` artifact 從「規定步驟」改成 **Plan Contract** —— 每個 task 一則條目，講清楚「做完長什麼樣」，不講「怎麼做」。
2. TDD 的載體從那些 micro-step 換成 **`tasks.md` 的 per-task 標註**（`TDD: applicable` / `TDD: n/a — <理由>`）＋ RED/GREEN 證據，由 verify 的五條確定性檢查驗其**存在與結構**。

**執行方式**：照 schema 自己的 apply 指令走完整流程 —— push main 對齊 origin → 建 worktree + branch → subagent-driven-development 逐 task 派工 → 每 task 獨立審查 → 群組邊界 commit → verify → retrospective → archive → PR。

**規模**（皆可查證）：

| 項目 | 數字 |
|---|---|
| tasks | 27（群 1–11；原 25，群 11 於 verify 階段補開） |
| commit | 4，落在 4 個 checkpoint 邊界 |
| `schema.yaml` | 583 → **916** 行 |
| bridge README（雙語） | 各 564 → **607** 行，30/30 **改寫段落**互相對映（全檔共 43 個 section，這不是全檔對映） |
| `verify.md` / `retrospective.md` | 653 / 237 行於 commit `84df208`；doc gate 兩輪後增至 694+ / 246+（會隨後續修正再動，以最終 commit 為準） |
| 累積裁定 | R0–R32（33 條裁定）＋ **11 條** controller 自身缺陷：9 條記在 ledger（其中 **6 條**有 `defect #N` 編號：#1、#2、#3、#7、#8、#9；另 3 條有記錄但未編號），2 條由 doc gate 補上（見 §5）。兩個序列獨立，**那 11 條不是 33 條的子集** |

**commit 粒度是使用者裁定的**：review 維持 task-level，commit 收在 group-level。理由原話：**「不要把『有 commit』當成『review 已完成』的證據。」** task 的審查與證據由 ledger、diff、review result 承載，不由 commit 邊界承載。

---

## 2. 為什麼選了比較麻煩的路（使用者裁定，逐條記錄以免日後失真）

- **選 (a) 走 worktree + PR**：「理由不是這 25 步本身需要高度隔離，而是這次正在修改 schema 自身；目前已確認 apply 的 worktree / finishing 流程在本 repo 從未真正 dogfood 過。」
- **前置條件：先確認 local main 領先的 3 個 commit 該不該進 main，是就先 push 對齊再開 branch。** 這條比預期更必要 —— `EnterWorktree` 預設從 `origin/<default-branch>` 開分支；沒先推的話，當時的 25 步（後來 reopen 為 27）會建在一棵**缺少 `tasks.md` / `plan.md`** 的樹上。
- **環境層發現一律定性為 dev / dogfood 問題，不泛化成產品層**，除非另做 bounded spike。
- **retrospective 不得寫成「Agent 本來就不應該 commit」**，要寫成日後重新檢討 Anchor #4 的事實基礎（§7）。
- **checkpoint 3/4 被擋下一次**（2026-09-03）：D1／D3 known-open 時，讓 `tasks.md` 以 25/25 進 checkpoint，語意上等於「已知仍有必要修正，但已宣稱所有任務完成」。改為補開群 11 → 25/27 → 做完 → 27/27。**一個不能倒退的完成度數字，會停止表達任何意思。**

---

## 3. Plan Contract 能不能替代 micro-step —— Q4-A 的實測

使用者定的三分法：能自主完成 / 因缺 micro-step 卡住 / 自主性變成 scope expansion。

**執行面：全程零次因缺步驟卡住，零次 scope expansion。** 三個具體樣本：

1. **task 1.1**：契約沒給步驟，它自行重建 dogfood 副本以便跑 validate，並**自創「PRECHECK 行號前後比對」當邊界證據** —— brief 只說要守住邊界，沒說怎麼證。
2. **task 3.1 fix round**：被要求移除一段錯誤複述後，它分辨了「定義形式」與「指涉對象」的差別（前者移除、後者保留），這個區分既不在 brief 也不在 finding 裡，然後**標記出來讓 controller 裁**而非自作主張。
3. **task 4.1 fix round 2**：未經要求自行加了 **F7 正向對照** —— 一份有空行、應該通過的紀錄，並驗證它在修正前會被假 BLOCK。那正是本 repo always-on 規則對防呆的要求（擋東西的規則要附上「應該通過」的那一半）。

**但這些都不是 Q4-A 的判定證據** —— 本 change 的 `plan.md` 是在 v1 下手寫的。真正的樣本是 task 10.4 的 fresh-context 生成，而它跑了兩次：

**Run 1 因儀器缺陷作廢（R31），且該裁定寫在 run 2 存在之前。** 這一點是審查者要求的：*「你要說 run 1 是因儀器缺陷、不是因結果而作廢 —— 這個區分只有在你看到 run 2 之前說出口才成立。」* 事後說則不可證偽。三個儀器缺陷都是我造的：（a）給的是我從 `schema.yaml` 抽出的指令，**比採用者實際收到的少一個 `<template>` 區塊** —— 逐字但比現實薄；（b）fixture 裡「不耦合」那個 task 是一份**描述其他 task 的文件**，而消費別人的形狀與名稱正是 Interfaces 的定義，所以那格是「fixture 沒有裁決的擲硬幣」；（c）四條契約條文完全沒被評分。

**Run 2（修正後儀器，三處修正皆為 pre-run、皆非 coaching，由另一位不知道 run 1 存在的評分者評）：3 yes / 2 no。**

| 評分項 | 結果 | 說明 |
|---|---|---|
| entry-key 集合相等 | ✅ | 雙向一致 |
| 無模糊驗收語言 | ❌ | 1.1 寫「**例如** client IP」而 design.md 已釘死該預設值，條目選擇不釘 |
| Interfaces 條件性正確 | ❌ | 一處**該寫而未寫**；而該不該省略的那半 **這次終於測到，且通過** |
| 無步驟規定 | ✅ | 兩處 borderline 判為允許並附理由 |
| 無第二份證據副本（v2 專有） | ✅ | plan 未帶任何紀錄、形狀或文法 |

**最有價值的發現是結構性的，不是品質抱怨。** 兩個 no 都落在條目 1.1，評分者被明說「N=1 時答『巧合』是可接受的」之後仍分開處理：驗收語言那項判為巧合；**Interfaces 那項不是** —— 該欄位的措辭是**消費者視角**（「它消費或產出的名稱與形狀」），所以**一個寫在其消費者存在之前的條目，沒有東西可以消費**。1.2 與 2.2 正確指名 1.1，只因為輪到它們時另一端已經在紙上了。原句：

> **「要求每個條目自陳它的邊，會讓『只有上游』的那個條目，成為唯一一處真實的邊從你站的位置看不見。」**

而群 10 的審查者**從另一面描述了同一件事**：這個遺漏會**通過審查**，因為「除非審查者自己建出耦合圖，否則看不出來，而單一條目的審查不會逼他這麼做」。生產端與審查端是同一個性質的兩面：**per-entry 的欄位無法浮現一條從該條目看不見的邊。** 兩層都不是不用心，問題在欄位的粒度。

**另外，契約本身有一個由實作而非由論證找到的洞，且被兩位評分者在兩次不同的 run、不同儀器設定下各自獨立提出**：指令說 global constraints「逐字抄自 specs」，卻**沒有給 change 沒有 `specs/` 時的 fallback**。這一條不依賴任一次 run 的儀器是否健全。

**這次能得出的結論，與不能得出的**：Interfaces 上這兩次 run 支持的是「生產者**供給不足**」，run 2 額外證明了「條件性那半會被尊重」。四個 D3 觸發條件裡有兩個是關於**再現性與變異度**，單一樣本按定義無法顯示 —— 評分者是這麼說的，而不是把一次觀察拉成趨勢。

---

## 4. 五條確定性檢查的證據強度

**盲測（R21）**：一位從未見過本 change 的 agent，只拿到 rendered verify 指令與六個**中性化改名、順序打亂**的 fixture：**6/6，零歧義**，並主動聲明未讀 fixture / report / ledger 任何一個。它同時找到一個作者測不出的洞：check 9 的豁免條款使得「`n/a` task 卻掛著 RED/GREEN」無人捕捉 → 補為第四條審查判斷 R4。

**正向對照（F7）**：六個 fixture 證明「違規會被擋」，F7 是第一個證明「合規不會被誤擋」的。

**對本 change 自己跑**（真正的 dogfood）：27 個 task 全為 `n/a`、0 個 applicable → 檢查 8 與 12 實質判定，**9/10/11 空跑**。這個空跑是 `design.md` § Risks **事先預測**的性質，且明文拒絕為了操練載體而捏造一個 applicable task。正負對照都跑，因為**一個什麼都沒讀的檢查器，跟一個讀完全部的檢查器，輸出一模一樣**。

**強制力邊界（寫進 schema 與模板，逐字要求照抄）**：這五條檢查在**判定什麼**上是確定性的，在**如何執行**上是 agent-executed（instruction-mediated）。它**不是** Harness 層、機械強制、不可繞過的 archive gate；verify agent 若跳過一條，本 schema 沒有任何機制攔截，verify.md 的審查是唯一後盾。它們驗證標註與紀錄的**存在與結構**，不證明證據為真、不證明 test-first 的開發歷程、不評估語意品質。

---

## 5. 最重要的一節：十一個「形式完整、實質空洞」的產物

**這次執行中，我自己製造了十一個不會報錯、但會輸出一個有說服力的錯東西的產物。** 全部列出，因為這一節的價值不在單一條目，在於它們的共同形狀。

> 這一節原本寫「九個」。第 10、11 個是這份文件送去獨立審查時抓出來的 —— **其中一個就在這一節評價的那些檢查裡，另一個就在這一節本身的隔壁段落**。編號沒有停在九，是因為一份主張「不要低報」的清單如果自己低報，它就只是修辭。

| # | 產物 | 症狀 | 誰發現 |
|---|---|---|---|
| 1 | `review-pkg.sh` 扁平快照 | 誤報整檔 DELETED，並產出一份**看起來合理的整檔 diff** | 我 |
| 2 | 統計用 `grep -c '^+[^+]'` | **漏算所有空行**，報 `+61 −18`（實為 `+70 −22`）—— 一個看起來合理的數字 | task 1.1 的 reviewer |
| 3 | fixture 目錄名 `f1-missing-annotation` | **答案印在路徑上**，盲測會 6/6 全中而什麼都沒證明 | 我（派工前 `ls` 的當下） |
| 4 | `review-pkg.sh` 的 "Untracked additions" | 印的是 repo-wide `git status`，不是該 task 的新增 | task 5.1 的 reviewer |
| 5 | 用 `/tmp` 當 Python↔bash 中介 | Git Bash 與 Windows Python 的 `/tmp` 是不同目錄，兩邊各自成功、讀到的不是同一個檔 | **hook 攔下** |
| 6 | 快照式審查包留下兩個基準 | reviewer 遇疑改用 `git diff`（＝對 HEAD），把自己二十分鐘前插入的行讀成「既有行被替換」 | 兩次，皆 reviewer 端誤報 |
| 7 | 用 Python `newline='\n'` 重寫雙語 README | CRLF→LF 全檔轉換；**git 會正規化所以它不會抗議** | 我自己的工具 |
| 8 | 10.4 的保真度修正削弱了盲測 | 真實 CLI render 的 `<output>` 帶著一條指向裝有 bundle 的 scratch project 的絕對路徑 | 我（事後） |
| 9 | 查「這句話在不在」用原始子字串 | 檔案**折行**，句子在、我的檢查說不在；**正向對照沒救到我**，因為對照字串剛好不折行 | 我（改讀實際行時） |
| 10 | **check 12 的通過紀錄本身** | 檢查在 25 tasks 時**誠實地通過**；群 11 把 tasks 加到 27 卻沒補 plan 條目，於是有一個 commit 的期間，**這個 change 違反了它自己新加的檢查**（27 vs 25）。紀錄還躺在 verify.md 上，正確地描述著一棵已經不存在的樹 | doc gate 的獨立審查（它去查本文件引的「27 個 task」，順手比對了兩個檔） |
| 11 | 本文件 §9 那句「**本檔用精確版本**」 | 在那句話裡把 **15 行**當成 **15 處**寫（實為 23 處），且列的三個章節漏了 3 行 —— 就在我拿來糾正 ledger 的那一段 | 同上 |

**第 10 個值得單獨看一眼，因為它的機制跟前九個都不同。** 前九個是「做出來的東西一開始就是錯的」；第 10 個是**做出來的東西一開始是對的，然後被檢查的對象變了**。少的不是正確性，是**新鮮度** —— 而這個 schema 裡沒有任何一層擁有新鮮度：`verify` 規定了檢查「archive 前要跑」，沒有規定「`tasks.md` 或 `plan.md` 後來被改過，先前的結果就作廢」。所有的閘門都在 reopen **之前**跑完了，沒有一個會再跑。（已補跑並雙向舉證：`verify.md` §8.1a；schema 層的缺口列入 carried-forward #6，交由 owner 裁。）

**共同形狀**：十一個裡有十個的失敗症狀是「一切正常」—— 沒有錯誤訊息、沒有紅燈、沒有人抗議。唯一在產出任何結果**之前**就被擋下的是第 5 個，而它是唯一有 enforcement 掛點的（hook 檢查 `/tmp` 字面）。這正是全域規則那句「寫不出掛點的規範要降級為 Observe」的正面實證 —— **不是又一條該新增的規則，是既有規則的一次實證**。

**還有兩件同類但不是我造的**：
- 第三方 reviewer 也犯了 #6 那一類（宣稱 guardrail 8 不成立，實為基準錯置），我用 HEAD 基準實測推翻。
- **證據裡有一個 silent zero**：class-(b) 掃描對兩個檔案回報「0 hits」，實際是 1 和 4；根因是「一次 ad hoc grep 靜默回空（工具路徑問題），而我沒有交叉驗證就採信」。**結論成立，支持結論的證據不成立。** 這觸發了本 repo 自己的 always-on 規則（自動篩選回報 0 命中時換一條結構不同的路徑交叉驗），一小時內觸發兩次：一次由 implementer，一次由我檢查自己的工作。第二次的做法值得留：Python 逐檔讀 ＋ **明確的 missing-file 回報** ＋ **正向對照**（一個必定存在的字串）—— 因為「讀完全部沒找到」與「什麼都沒讀所以沒找到」的輸出是逐位元組相同的，只有對照能分開它們。

**為什麼這節比「Plan Contract 好不好用」更值得記**：這個 change 的整個主題是**規定證據**。而在執行它的過程中，證據載體本身十一次產出形式完整、實質錯誤的結果，十一次都不會有人抗議 —— 其中兩次是在**這份記錄自己被送去獨立審查時**才浮現的。

> **規定證據不夠，證據本身也要能被驗證不是自我循環。**
> 這次唯一真正打破自我循環的動作是 R21 的盲測 —— 而它之所以有效，是因為在派工前的最後一刻拿掉了目錄名裡的答案。

**兩條由此而來的常設修正**（已在後續派工中執行）：
- 任何 guardrail 型的宣稱**必須指名基準**；快照式審查包要在最上面一行寫明基準，並明說 `git diff` 回答的是另一個問題。
- 折行檔案裡的散文要用**空白正規化**後再探；而**正向對照只控制得住它剛好與真實探針共有的那個失效模式**。

---

## 6. schema 自己的 apply step 1 / 6 首次執行 —— 環境層證據

事實：本次之前，`git branch -a` 只有 main、`git worktree list` 只有主目錄、`git log --merges` 為 0，**77 個 commit（`git rev-list --count 5aa19bf`）全部直接落在 main** —— 包含上一個走完整流程並 archive 的 change。**schema 規定的 worktree 與 finishing-a-development-branch 兩步，在它自己的 repo 裡一次都沒有被執行過。**

| 編號 | 發現 | 定性 |
|---|---|---|
| E1 | **worktree 下 opsx 靜默切換 schema 並宣告完成**：`openspec/schemas/` 被 gitignore，新 worktree 沒有 bundle；`.openspec.yaml` 寫 `superpowers-bridge`，CLI 卻回報 `spec-driven`、artifact 從 8 掉到 4、`isComplete: true`、exit 0、無警告 | dogfood + worktree 環境**已實測**。是否為產品層 silent fallback 需另做 bounded spike，本次不宣稱 |
| E2 | `.claude/worktrees/` 未被 gitignore，而 `.claude/` 有 58 個檔在版控裡。原生 `EnterWorktree` 路徑**沒有** ignore precheck，手動 `git worktree add` 路徑**有** | 兩條名義等價的建立路徑，assurance 不等價 |
| E3 | **正面**：harness 機械阻止 isolated session 對主 checkout 操作 git，也拒絕「無法靜態證明留在 worktree 內」的複合指令 | 隔離是 enforced，不靠自律 |
| E4 | `.superpowers/`（SDD 工作區）**不在版控的 `.gitignore` 裡**；它是被 `.git/info/exclude:9` 忽略的 —— 一份**本地、不進版控、任何 clone 或同事都拿不到**的檔案。skill 假設這個工作區是 ignored 的 | 在這台機器上成立，換一台就不成立；同 E2 一類（保護存在，但不是它看起來的那一層在保護） |
| E5 | `rm -rf` 被權限層拒絕，連帶使 task 10.1 的驗收字面無法由 agent 執行 | 替代為覆蓋複製 + `diff -r`；**來源檔被刪除時兩者不等價**，本 change 無刪除故成立 |

**E1 的連帶後果值得單獨記**：task 10.1「重建 dogfood 副本」在 worktree 下是**開工前置條件**，不只是收尾驗證。**execution environment 改變後，task 之間的依賴也跟著改變** —— 而 `tasks.md` 裡看不出這件事。

**SDD 與本 repo 的耦合摩擦**：
- `task-brief` 腳本寫死 `writing-plans` 的 `## Task N` 標題慣例；Plan Contract 用 `## 1.1 —` 當 key，腳本回 `no heading matching 'Task 1'`（ledger R7，`progress.md:53` 的原字串）。**schema 指定 SDD 當執行器，而 SDD 的輔助腳本綁在這個 change 正要移除的輸出格式上。**
- 架構 learning：**重用 skill ≠ 繼承 skill 的權限假設。skill 定義 procedure，repo / harness 定義 execution permission。**

---

## 7. Anchor #4 的事實基礎（本檔不裁定，只記錄）

`subagent-driven-development` 的正常流程**依賴 implementer 做 task-level local commit**；本 repo governance **全域禁止 agent `git add` / `commit`**（Anchor Register #4，其例外清單本身也是 anchor）。本次以「快照式審查包」替代 commit range —— 而 §5 的 #6 顯示那個替代方案自己製造了一類新的誤判（兩個活的基準）。

同時本次**實測**：isolated worktree 會**機械阻止** session 對主 checkout 做 git 操作（是拒絕執行，不是警告）。

因此值得日後正式檢討的問題是：**worktree 是否不只是檔案隔離，而是一個可以安全授予 worker 局部權限的 execution boundary** —— 具體形式為：isolated worktree ＋ 非保護分支上，是否允許 worker-local `git add` / `commit`，同時仍然禁止 push / 保護分支 / rebase / force。

這屬 Anchor #4 的正式治理變更，需 human approval ＋ 自己的 spec/change ＋ tests。**本檔不做這個裁定，只把事實基礎放在一處，供那時引用。**

---

## 8. Codex 保證缺口的處置（僅限本 change）

跨 session 技術債：本 change 的 Codex independent review 未取得。使用者要求先**分類再處置**，區分兩種情況；分類依原始 SHALL 的措辭做，不依事後方便：

`文檔/handoff/session-handoff-20260902.md:99` 的 SHALL 全文是「**SHALL 補獨立審，補審前不 archive**」：其受詞是「補**獨立審**」，缺陷描述是「只過 **fallback** 審」，Codex 出現在**時間條件**的位置（「額度恢復後」）。而 `auto-loop.md` § Review Dispatch 本身已使審查者身分可替換、以 gate 為所守之物。

**第二個子句「補審前不 archive」寫在這裡，是為了讓這次的解除可稽核** —— §9 把 archive 列為待執行，而正是這個裁定解除了那個前置條件。不寫出來，解除就只是隱含的。

→ 判為 **equivalent-assurance substitution（等效保證替代）**，**不是** Codex 專屬的降級豁免。逐字記錄於 `verify.md` §15 與 `retrospective.md` §7，**範圍僅限 `loosen-plan` 本次 change，明文不作為先例**。

實際承載保證的是：每個 task 的獨立 subagent 審查、一次 2009 行的 whole-branch 審查、盲測 ＋ 正向對照、以及跨路徑的交叉驗證。

---

## 9. 仍然開著的事

| 項目 | 狀態 |
|---|---|
| task 9.1 的 live Actions run 驗證 | **未做** —— push 後才驗得到，已在 `verify.md` 記為 owed verification 而非略過 |
| v1 → v2 migration guide | **從未有任何 in-flight v1 change 走過它**。這一條在 final review 之前不在任何清單上 |
| `archive` → PR | 待執行（Windows 目錄鎖：`cp -r` ＋ `diff -r` ＋ **委派使用者跑 `rm -rf`**） |
| Anchor #4 正式檢討 | 事實基礎見 §7；未排期 |
| E1 是否為產品層 silent fallback | 需 bounded spike；本次不宣稱 |
| **schema 沒有任何一層擁有「檢查新鮮度」**<br>**（2026-09-04 後記：已部分關閉，見本節末）** | 本次實證（§5 第 10 個）。`verify` 規定檢查 archive 前要跑，沒規定「`tasks.md` / `plan.md` 後來被改過，先前結果就作廢」。已補跑並雙向舉證，但**缺口在 schema、不只在這次執行**；且能否在不動用 claim boundary 明文否認的 Harness 層機制下表述，本身就是問題的一部分。列入 `verify.md` carried-forward #6，交你裁 |

> **後記（2026-09-04，不改寫上方紀錄，只標明其後續）**：使用者於次日裁定 —— 這不是「還能更好」，是**本次已實測的假放行**，必須在出貨前補到「當前架構真正能提供的保證程度」。`verify` 指令因此加入**新鮮度要求**：一筆已記錄的結果描述的是檢查當下的 artifact，之後改動 `tasks.md` 或 `plan.md` 會使**由該檔算出的每一筆結果**變成 STALE、必須在 archive 前重跑（受影響集合**由各檢查的輸入推導**：check 2 與 8–11 讀 `tasks.md`、check 7 讀 `plan.md`、check 12 兩者皆讀）。**定位僅為 agent-executed** —— 不計算也不比對任何 digest，各表面不得宣稱新鮮度已被機械保證。上方那句「沒有任何一層擁有新鮮度」在 09-03 當下為真；今日起精確的說法是「**沒有任何一層機械地擁有它**」。真正的機械版（結果綁定被驗證狀態的 digest、gate 前重算、不符即失效）另列為後續正式 change 候選，本次刻意未開始。

**一個已收斂、值得記錄其收斂方式的**：bundle 的規範指令面（`schema.yaml` ＋ `templates/`）現在有**零個** `\bv1\b`；兩份 README 各有 **15 行 / 23 處**，其中 12 行落在 migration guide、compatibility matrix 與 versioning 說明 —— **那裡指名前一個 major 正是它的用途** —— 另 3 行分別在導言（`:12`）、升級說明（`:117`）與 apply 走查（`:411`，那處是 `v1.x`，指 bundle 發版而非 schema major）。（ledger 裡記的是「bundle 零個」，那句話的實際範圍是前者。而本檔第一版在這句宣稱「用精確版本」的話裡，**把行數當成處數寫** —— 由 doc gate 的獨立審查抓出，見 §10。）

---

## 10. 這份文件哪些部分可獨立查證、哪些只有 ledger 佐證

本檔在 2026-09-03 過了一次 doc gate：獨立審查者（opus，非 Codex —— 見 §8 的等效保證替代）逐項查證，回 `⛔ Needs revision`，一個 🔴（即 §5 的第 10 個）、四個 🟡、四個 ⚪，全部已修。sentinel 驗證通過（`[SENTINEL_VALID] contract=doc`）。

**但比 findings 更該留下來的，是它主動畫出的那條線** —— 因為這份文件的用途就是在 ledger 被刪掉之後被人引用，而引用者需要知道每一句話背後站著什麼。

| 分級 | 內容 | 憑什麼 |
|---|---|---|
| **可從 repo 獨立查證** | 所有行數、commit 範圍與 diff 統計、R0–R32 的條數、27 個 `n/a` 標註、`.claude` 的 58 個追蹤檔、`.git/info/exclude:9`、CI 的 `v2` grep key、§7 對 Anchor #4 的描述、§5 #5 那支 hook 真的存在且匹配 `/tmp/` 字面 | 審查者用 `git`、`wc -l`、`grep`、`check-ignore` 各自跑過 |
| **兩份文件互相一致，但無法確認事件發生過** | 兩次 10.4 的 run 與評分結果 | 只能確認 `verify.md` §11 與本檔 §3 說的是同一件事 |
| **只有 ledger 佐證 —— 即「被摘要的來源自己的旁證」，不是獨立確認** | **§5 的前九個產物**、所有 subagent 與評分者的引言、checkpoint 裁定與 commit 粒度裁定、E1／E2 後半／E3／E5 的環境行為、`+61 −18` 當時的原始統計、§5 #5 那支 hook **在當下真的觸發** | ledger 條目，其中 6 條帶 `defect #N` 編號、3 條僅有敘述。（§5 的第 10、11 個不在此列 —— 它們由 doc gate 的獨立審查發現並可從 repo 重算） |

**所以：§5 —— 我在 §0 稱為「這份報告存在的理由」的那一節 —— 是全檔唯一無法獨立查證的一節。** 它的證據鏈終點是我自己寫的 ledger，而 ledger 也是我寫的。

這不是缺陷，審查者也沒把它列為 finding。但它是這份記錄的**可信度分佈**，而在獨立審查之前，沒有任何人寫下來過 —— 包括我。**一份講「證據要能被驗證不是自我循環」的文件，自己最重的那一節就是自我循環的**，這件事必須寫在文件裡，不能只寫在我心裡。

（可稽核性的實際做法：§5 的每一條在 ledger 裡都有對應編號的條目；ledger 隨 branch 收尾刪除，但它的內容經由本檔與 `verify.md` 保存。想要更強的等級，唯一的路是當時就把工具輸出落檔進版控 —— 這是下一次可以做、這一次沒做的事。）

---

## 11. 【學習候選】

1. **Case** — 十一個自製的「形式完整、實質空洞」產物中，十個的失敗症狀是「一切正常」；唯一在產出結果前被擋下的，是唯一有 enforcement 掛點的那一個。
   **Candidate Pattern** — 為「證明某件事」而建的機制（測試、掃描、fixture、審查包、統計），其缺陷的預設症狀是**靜默通過**，不是報錯；因此這類機制上線前必須各自帶一個**正向對照**（一個必定成立的輸入，用來區分「讀完全部沒找到」與「什麼都沒讀」）。
   **Evidence** — 本次 N=11，跨六種載體（腳本、統計、fixture 命名、路徑、字串探針、**先前通過的檢查紀錄**）；另有 silent zero 一例來自 implementer 端，同型。第 10 個把 pattern 的邊界推廣了一格：**正向對照解決不了新鮮度** —— 一個當時正確的結果，之後不會因為對象改變而自己失效。那需要的是「輸入變了就作廢先前結論」的綁定，不是更好的對照。
   **Minimum Sufficient Intervention** — **不新增規則**。既有 always-on 已有「自動篩選回報 0 命中時換結構不同路徑交叉驗」，本次證實它有效（一小時內觸發兩次）。建議的最小介入是把「正向對照」寫進**既有的**那條，而不是另立一條 —— 掛點沿用既有那條的掛點。
   **Promotion** — Refine Existing Strategy（由使用者決定）。

2. **Case** — Plan Contract 的 Interfaces 欄位以消費者視角措辭，導致「只有上游」的條目結構性地看不見自己的邊；而審查端因為單條目審查不強迫建耦合圖，同一個遺漏也看不見。
   **Candidate Pattern** — **per-entry 的自陳欄位無法浮現一條從該條目看不見的關係**；凡是要求「每個 X 自陳它的邊」的設計，都需要一個**跨 X 的推導動作**當補集，否則上游端的遺漏由建構決定其不可見。
   **Evidence** — 兩位獨立評分者在兩次不同儀器設定的 run 各自到達；群 10 審查者從審查端描述同一性質。仍為 **Hypothesis**（N=1 個契約設計）。
   **Minimum Sufficient Intervention** — 不改 schema。先在下一次 plan 審查時實測「要求審查者自行建一次耦合圖」是否抓得到，再談改欄位。
   **Promotion** — Pattern Candidate。

3. **Case** — checkpoint 3/4 被使用者擋下，理由是 25/25 會使「已知仍有必要修正」與「已宣稱全部完成」同時成立。
   **Candidate Pattern** — 完成度計數若允許在已知缺口未閉合時仍宣告滿分，該計數即停止承載資訊；正確動作是**補開 task 讓分母上升**（25/27），不是維持分子。
   **Evidence** — 單一實例，但機制清楚且可機械查驗（`openspec list` 的計數來源）。
   **Minimum Sufficient Intervention** — 無需新規則；本檔記錄該次裁定即為往後引用點。
   **Promotion** — Case Memory。
