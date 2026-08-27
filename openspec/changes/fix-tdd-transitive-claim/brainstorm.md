<!--
Raw capture of superpowers:brainstorming output — 2026-08-27 session。
本檔原樣捕捉討論過程，不強制結構。design.md 從本檔萃取重組，兩者互補不重疊。
-->

# Brainstorm — fix-tdd-transitive-claim

> 2026-08-27，使用 `superpowers:brainstorming`（架構路徑）。
> 路徑分類：程式面工作屬 bounded（動的是既有檔案），但本 repo 規矩要求 schema 改動走 opsx，
> 而 `superpowers-bridge` 的 DAG 本就要求完整 artifact 鏈。**衝突時取重**，故走架構路徑。

---

## 一、背景：問題是什麼

`superpowers-bridge/schema.yaml` 的 apply 第 2 步對執行的 agent 說：

> IMPORTANT — transitive skill activation:
> subagent-driven-development internally enforces the following skills,
> **so you do NOT need to invoke them manually:**
> - superpowers:test-driven-development — every task follows RED-GREEN-REFACTOR

這句話有兩個問題，第二個比第一個嚴重：

1. **它是假的**
2. **它的語氣是解除性的**——不只描述錯誤，還主動叫 agent 停止做某件事

---

## 二、查證事實（每條附出處）

### 2.1 上游從未強制過 TDD——這不是漂移，是一開始就讀錯

| 版本 | `subagent-driven-development/SKILL.md` 內 TDD 字樣 | 實際寫什麼 |
|---|---|---|
| 5.1.0 | 2 處 | `Subagents follow TDD **naturally**`（L207，在 "Advantages" 段）<br>`**Subagents should use**: test-driven-development`（L276，在 Integration 段）|
| 6.2.0 | **0 處** | — |
| 6.3.0 | **0 處** | — |

出處：`~/.claude/plugins/cache/superpowers-marketplace/superpowers/5.1.0/skills/subagent-driven-development/SKILL.md:204-213, 273-279`；6.2.0 / 6.3.0 同路徑，grep 命中數 0。查證日期 2026-08-27。

6.3.0 中所有 TDD 字樣都在 `implementer-prompt.md`，且**三處全是條件句**：

- `:36` — `Write tests (following TDD **if task says to**)`
- `:113` — `Did I follow TDD **if required**?`
- `:133` — `**TDD Evidence (if TDD was required for this task)**`

反向證據：`task-reviewer-prompt.md:75` **假設** TDD evidence 存在——上游自身的契約裂縫。

**結論**：`internally enforces` 這個詞在上游任何一版都找不到來源。我方讀到的是「建議清單」（`should use`）與「宣傳語」（`naturally`），寫下來變成「保證」。

### 2.2 同一宣稱散在 10 處，且 README 自相矛盾

全 repo 掃描（`grep -rniE "transitiv|do NOT need to invoke|brings TDD|internally enforces"`，排除 `openspec/`、`docs/superpowers/`、討論素材與 handoff）：

| 檔案 | 位置 |
|---|---|
| `schema.yaml` | L10-11、L19-20（**schema description**，會被 `openspec schemas` 直接印給使用者）、L474、L507-513 |
| `README.md` | L213、L247（mermaid 圖）、L282、L304-305、L368、L381、L443-445 |
| `README.zh-TW.md` | L445 等對應處 |
| `templates/retrospective.md` | L59-60 |

**矛盾**：README L500 的 Compatibility 表已於 commit `c134f1c`（8/26）正確標為 `❌ False in v6.3.0`，但同一份文件其餘七處仍當作成立的事實敘述。

**8/26 那次修正本身就是半修**——修了一列，沒往外掃同類。

### 2.3 `verification-before-completion` 已存在，但 bridge 完全沒用到

`schema.yaml` 引用的 superpowers skill：`brainstorming`、`writing-plans`、`using-git-worktrees`、`subagent-driven-development`、`finishing-a-development-branch`、`test-driven-development`、`requesting-code-review`、`executing-plans`（否定引用）。

`grep -rn "verification-before-completion" superpowers-bridge/` → **0 命中**。

該 skill 自述：`requires running verification commands and confirming output before making any success claims; evidence before assertions always`。

出處：`~/.claude/plugins/cache/claude-plugins-official/superpowers/6.3.0/skills/verification-before-completion/SKILL.md` frontmatter，2026-08-27。

### 2.4 已存在一份成熟的 skill：`review-fix-propagation`

位置：`D:/workflow-harness/.claude/skills/review-fix-propagation/`

來歷與本次同型：5/20-5/21 連續 7 個「修完 anchor 沒擴散、下輪 review 又抓到同類殘留」案例（`references/dogfood-history.md`）。

9 個檢查維度中，三個直接對應本次缺陷：

| 維度 | 內容 | 對應 |
|---|---|---|
| 7 | 新寫的規範句自我代入——「這句話**本身**語意錯，傳播越完整錯得越一致，前六維度全綠」 | 把「建議」寫成「保證」 |
| 8 | 會被照著做的規範句配**正向**斷言——「把它原封退回去，有沒有測試會紅？」<br>**明文：反向斷言（驗「沒有什麼」）不算數，擋得住漂移、擋不住整句消失** | 那句解除性的話被刪掉後無人守 |
| 9 | 同類出口並排比對——「照規格，還有誰該講同樣的話？」 | 10 處散落 |

**維度 7、8、9 MUST 由外部檢查者跑、MUST NOT 由撰稿方自審**——記錄為「全數由外部 reviewer 抓到，無一由自審發現」。

**分層警告**（memory `feedback_use_propagation_check_after_review_fix`）：該 skill 是 **dev workflow tool**，不是 plugin 對使用者承諾的機制。

### 2.5 兩個換腦審查者今日皆可用

| 工具 | 版本 / 模型 | 驗證方式 |
|---|---|---|
| Codex | `codex-cli 0.149.1` | `codex exec` 實際打通，回應正常 |
| agy | `1.1.16`，`gemini-3.7-flash-high` | `agy -p --model gemini-3.7-flash-high` 實際打通 |

⚠️ `agy` 的 `--effort` **不換模型**，必須用 `--model`，指定錯不會報錯。

### 2.6 `strict-reviewer` 與 `doc-review` 的實際能力（讀定義，非讀名字）

- **`strict-reviewer`**：sd0x 子代理，`model: opus`、`effort: high`，工具 Bash/Read/Grep/Glob。四維度＝正確性/安全/效能/可維護性。證據規矩明文「**不准推測，只回報在程式碼裡可以驗證的東西**」。
  - ⇒ 結構上抓不到本次缺陷（四維度不沾，且真相在別的 repo 的 markdown 裡）。
  - ⇒ 但它有 Grep + 要求 `file:line`，**適合本 repo 內部一致性與同類殘留掃描**。
- **`doc-review`**：`allowed-tools` 含 `mcp__codex__codex`——**它走的就是 Codex**，不是文案審查。流程：確定性連結檢查 → 所有改動的 `.md` 當**一個計畫**一起審 → 五維度評分 + 閘門。
  - 內含與本次同型的紀律：「絕不把多檔改動縮成單檔審……**計畫漏掉的檔案，就是沒有任何人審過的檔案**」。

---

## 三、決策鏈

### Q1：假保證刪掉後放什麼？→ **B（真話修正 + 補正向要求）**

- A＝純真話修正（只是不再說謊，不新增要求）
- **B＝真話修正 + apply dispatch 契約要求會改變行為的任務附 TDD**

理由：A 之後 schema 處在「知道 TDD 可能不發生，但什麼也不做」的狀態，而 TDD 是使用者用這整套的理由。且 Change 3（放寬 plan）正要拿掉目前唯一的 TDD 到達管道。

### Q2：沒有測試框架的任務怎麼辦？→ **(iii) 放寬「測試」定義，不放寬「要有證據」**

本 repo 明文「沒有原始碼、沒有 package.json、沒有測試框架」，唯一的測試是 `openspec schema validate`。

- (i) 二分宣告——「不改變行為」會變成好按的逃生鈕
- (ii) 有測試框架才要求——即靜默降級，且判斷權在被要求的一方
- **(iii) 凡可判定的檢查都算**（單元測試、`schema validate`、grep 斷言、`diff -r`），要求不變：**先跑看到失敗（RED）→ 改 → 再跑看到通過（GREEN）**

對齊使用者既有裁定 `feedback_evidence_matrix_archive_gate`（三軸全部強制、不允許 N/A）與原話「規格及測試規劃沒有的就是我們的邊界」。

### Q3：閘門放哪？→ **分層，各司其職，不互相冒充**

使用者提出「交第三方審查就有閘門」。查證後修正為**緩解不是保證**，因為上游 SDD 有三個已查證的合法繞道：

| 繞道 | 出處 |
|---|---|
| reviewer 被明令不准重跑 implementer 已跑的測試 | `task-reviewer-prompt.md:64-89` |
| controller 可在第 5 輪後 park 掉它自己認定為真實的 finding | `SKILL.md:415-419` |
| 同形小任務會被合併成一次 dispatch、diff 當一個單位審 | `SKILL.md:223-229` |

⚠️ **若寫成「經第三方審查即可確保正確」，就是用同一類缺陷去修同一類缺陷。**

分層結論：

| 層 | 誰 | 管什麼 | 擋得住嗎 |
|---|---|---|---|
| 說明書 | schema 要求 | 告訴人要做什麼 | ❌ |
| 判斷 | 外部 AI 審查者 | 範圍夠不夠 | ⚠️ 判得出、可能被跳過 |
| 換腦 | Codex / agy | 框架外的東西 | ⚠️ 同上 |
| 硬擋 | CI 自動檢查 | **有沒有交證據** | ✅ |
| 完成定義 | 沒有 Propagation Check Report 就不算修完 | 把「記得做」變成「沒做不算完」 | ✅ |

依據：`openspec archive -y` 對未完成任務連問都不問就歸檔（8/26 查證），**prompt 層擋不住任何東西**。

### Q4：這個問題有解嗎？→ **不能根除，但可分兩種，一種可機械化**

- **完全解決＝不可能**：判斷「檢查夠不夠寬」需先知道真正範圍；而若已知真正範圍，一開始就不會寫窄。且檢查者的檢查也有範圍，無限回歸。
- **宣稱關於「文字」的**（例：這包不該再出現某句話）→ **可窮舉**，把判斷題變成搜尋題。關鍵規矩：**搜的對象是「整包」，不是「我改的那幾行」**。
- **宣稱關於「行為」的**（例：後面那個人會做測試）→ 搜不到，只能去讀對方的東西。降級做法：**每句對外宣稱綁出處**（檔案 + 行號 + 讀取日期），使其可回頭重讀、可被漂移偵測。

本 repo 的優勢是**規模小到窮舉負擔得起**（個位數檔案、對外宣稱數得完）。這是實質優勢，不是精神喊話。

已知失效條件：①這包長大 ②宣稱變成搜不到的東西 ③換腦那層垮掉 ④使用者不再看。

### Q5：範圍——合併還是分開？→ **合併**

原建議分開（照 8/26 已決：修 TDD 漂移 vs 建可追溯性拆兩個 change）。使用者將「機制」定為重點後改為合併。

理由：只把話改對而機制留到下一件，中間會出現「說明書要求了但沒東西接住」的狀態——**那正是我們現在要修的病的鏡像版**。

⚠️ 後果：本 change 實質吸收了原 Change 2「TDD 證據契約」的題目。8/26 該題有**六個設計已被第三方審查推翻**，見 `.handoff/2026-08-26-tdd-evidence-contract-redesign.md`，設計時逐條避開。

### Q6：用現成的還是新寫？→ **兩層都做（C）**

- **第一層（dev tool，自己用）**：本 repo 也裝 `review-fix-propagation`，做這個 change 時真跑一次，觀察 9 維度裡哪幾條在本 repo 有用。
- **第二層（對採用者承諾，寫進 bridge）**：借該 skill 用 7 案例 + 3 次復發換來的**判準**，不搬 skill 本體。

使用者定調：「skill 是 dev workflow tool、不是工具本身」的意思是**鷹架不是房子**——警告的是別把鷹架當房子交給客戶，不是說鷹架學到的東西不能用在房子上。

**自我要求**：寫進 bridge 的每一句都要能回答「出處是什麼？整段被刪掉會不會有東西紅？」，答不出來只准寫成建議、不准寫成保證。

### Q7：審查怎麼派？→ **依能力分工，不依強弱排名**

使用者立場：審查只信 Codex 與 Fable；agy 頂多做第三方意見、文案、受眾模擬；技術/規格相關都算程式碼審查的一部分。

**同意其歸類（決定誰審），但提出一條反駁（決定審什麼）**：

> 「歸類為程式碼審查」是對的，但若因此**只用程式碼的尺去量**，本次這種缺陷會再漏一次。

證據：`strict-reviewer` 四維度＋「只報程式碼裡可驗證的東西」，結構上報不出本次缺陷。Codex 的程式碼審查流程是同一組尺。

本次缺陷不是「寫錯了」，是「**說了一件沒有出處的事**」。抓它需要一個程式碼審查表都不會問的題目：

> **這句話的出處是什麼？出處說的，跟這裡寫的一樣嗎？**

⇒ **路由決定「誰審」，題目決定「審什麼」**；兩者都要，缺後者是本次事故的直接成因。

最終分工（使用者修正版——`strict-reviewer` 不是拿掉，是放對位置）：

| 審什麼 | 誰 | 為什麼是他 |
|---|---|---|
| 本 repo 內部一致性、同類殘留、交叉引用 | `strict-reviewer` | 有 Grep、釘 Opus 高推理、證據要求 `file:line` |
| 對外合約、規格、宣稱 vs 出處 | **Codex**（`doc-review` / `review-spec`），不可用 → **Fable** | 換一個腦，才看得到框架外 |
| 「這句話像不像在保證」 | agy | 語感題，當**輸入**不當閘門 |
| 同類殘留掃描 | 不派人，用搜尋 | 確定性優於判斷 |

### Q8：審查路由要不要做成機制？→ **便宜版現用，貴版另立**

- **便宜版（本次採用）**：一張對照表決定用哪個審查，不做機制。
- **貴版（獨立工作）**：做成會自動判斷的東西。它有與本次同型的毛病——**路由選錯不會有人抗議，症狀又是「一切正常」**。值得認真做，不該塞進本 change 順手做掉。

---

## 四、設計結論

### 4.1 兩類缺陷、兩種修法

| 類別 | 這句話做了什麼 | 處數 | 修法 |
|---|---|---|---|
| **解除型** | 寫在會被執行的指令裡，**叫 agent 不用做** | 2（`schema.yaml` L507-513、L474）| **不能只刪**——刪掉會留下洞。要換上真的接得住的交代 |
| **描述型** | 寫在說明文件裡，**只是講錯**，未叫人停手 | 8 | 改成準確即可 |

### 4.2 要寫進 bridge 的五條

| # | 內容 | 出處 |
|---|---|---|
| 1 | 修掉 10 處假宣稱（2 處解除型換成真交代，8 處描述型改準確） | 本次全域搜尋 |
| 2 | schema 引用 `verification-before-completion` | 架上現成、bridge 0 命中（§2.3）|
| 3 | 要求**正向**斷言，不是反向 | propagation skill 維度 8 |
| 4 | 動手前先宣告「這次會動到哪些地方」（Affected Surface）| `references/參考意見.md` 第七層 |
| 5 | 維度 7/8/9 必須外部審、不可自審 | propagation skill 明文＋「無一由自審發現」的紀錄 |

### 4.3 步驟對應的既有 skill

| 步驟 | 用什麼 | 狀態 |
|---|---|---|
| 設計探索 | `superpowers:brainstorming` | 本檔即產出 |
| 寫計畫 | `superpowers:writing-plans` | 現成 |
| 隔離工作區 | `superpowers:using-git-worktrees` | 現成 |
| 執行 | `superpowers:subagent-driven-development` | 現成 |
| 先寫檢查再改 | `superpowers:test-driven-development` | 現成 |
| 沒證據不准說完成 | `superpowers:verification-before-completion` | 🆕 bridge 未用 |
| 修完掃同類殘留 | `review-fix-propagation` | 🆕 本 repo 未裝 |
| 內部審查 | `superpowers:requesting-code-review` | 現成 |
| 收審查意見（不准敷衍點頭） | `superpowers:receiving-code-review` | 現成 |
| 換腦審查 | `sd0x:doc-review`（走 Codex）/ `review-spec` | 🆕 |
| change 完整性 | `/opsx:verify` | 現成 |

### 4.4 fallback 鏈

使用者定調：**審查只信 Codex 與 Fable**。故：

> Codex → （不可用時）Fable

⚠️ 這**修改了** CLAUDE.md「複審紀律」現行條文（原為 Codex → strict-reviewer / 確定性驗證 → 確有必要才升 Fable）。使用者知情下更動，理由是 agy 屬 Flash 級、不足以承擔規格審查；strict-reviewer 與撰稿方同腦。**該條文需同步更新，否則規矩與實作不一致。**

每輪審查結果即時落檔，不因單點故障把審查掛起來等。

---

## 五、明確不做

- ❌ 不寫「經第三方審查即可確保正確」——那是新的假保證
- ❌ 不做自動化殘留檢查腳本——`dogfood-history.md` 記載使用者 5/21 拍板「先讓 skill dogfood 3-5 次評估性價比」
- ❌ 不把 `review-fix-propagation` 本體搬進 bridge——鷹架不是房子
- ❌ 不重蹈 8/26 被推翻的六個設計（升 schema 版本號隔離、`evidence` 列為 artifact、標題當識別碼、commit SHA 當 RED 證據等）
- ❌ 不動階段二（Orca 對接）

---

## 六、未決 / 待確認

1. **審查路由貴版**需登記為獨立工作（Q8）
2. **CLAUDE.md 複審紀律條文**需依 §4.4 同步更新
3. **工作登記需對齊**：work-map 現有 Change 1 與 Change 2 兩筆分開，本 change 已合併兩者
4. **bridge 當初對照的 Superpowers 版本**未查（README Compatibility 表有釘版本，尚未讀該格）——不影響結論（5.1.0 與 6.x 皆不成立），但影響「當初是誤讀」這個說法能講多滿

---

## 七、本次未讀完的材料

- `review-fix-propagation/references/propagation-checklist.md`（7.7KB，詳細 grep 指令範例）
- `review-fix-propagation/evals/evals.json`（6.6KB）
- `2026-08-26-TDD證據契約-設計結論-待第三方審.md` 全文（僅讀交接摘要）
- 階段二素材兩份（刻意不讀）
