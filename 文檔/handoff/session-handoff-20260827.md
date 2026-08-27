# Session Handoff — 2026-08-27

## Session 08:01

### 一、本 session 主題

跨日界線的收工續章——8/26 那個 session（14:24 開工）的 `/end-session` 流程在今早 08:00 完成落地；**設計內容全部在 `session-handoff-20260826.md`，本檔不重抄**。

### 二、完成事項

- **建立 5 筆工作登記**（`workflow-harness/work-map.jsonl`）：父項「superpowers-bridge 下一代改造」（DOING）+ 四個 roadmap 子項；父項 `next_branch=2`（已有下一步）、`errors: []` `integrity: []` 核對通過
- **gitignore 三份討論素材 + auto-loop 狀態檔**：`Orca Worktree 模型分析.md`（784KB ChatGPT 匯出）、兩份階段二素材、`.claude_review_state.json`；結論已萃取進 CLAUDE.md 與設計文件，原始逐字稿不進版控
- **收工 commit `40214c3`**：7 檔、335 insertions（harness 骨架 + 5 筆登記 + 8/26 handoff 同一 commit，兌現「程式 + handoff 同 commit」）
- **結算 marker 寫入**（`state: settled`, commit `40214c3`）；已驗證 `.workflow-harness/` 被 gitignore 擋住、不混進 commit

### 三、未完事項 / 接力棒

- [#接力] **`修正 TDD 保證的錯誤宣稱`** 已標 `NEXT`——下次開工第一件事，同時當第一次完整走 opsx 流程的試跑
- [#接力] **Change 2（TDD 證據契約）需重新設計**——完整脈絡見 `.handoff/2026-08-26-tdd-evidence-contract-redesign.md`，內含「已查證、不必重查」的引擎與上游事實清單
- [#待確認] **Gemini 訂閱類型**——決定第二視角救不救得回來
- [#待確認] **`~/.gemini/settings.json` 的 `defaultApprovalMode: "yolo"`** 是無效值，未動
- [#不重議] **階段二（Orca）不建 record**——它還沒有可定義的完成條件，留在 CLAUDE.md 當方向

### 四、洞見 / 反省

**【紀律接力】**

- [#接力] **8/26 的兩條 `[#反]` 尚未有載體**（「先讀實際驗到什麼」誤用、「宣告不存在前沒窮舉」第 5 個載體）。兩條都寫了 propose action 但還沒落到任何 rule / memory / hook，下次若再犯就是同一條累積第 2 次，屆時應考慮升 always-on 或寫進 backlog `[SOP 候選]`。

**【當日洞見】**

- [#決策] **不把跨日界線寫成新的工作紀錄**。hook 依日期要求 8/27 的 handoff，但這個 session 的實質內容全在 8/26；本檔只記午夜後真正發生的四件事（登記、gitignore、commit、marker），其餘指回 8/26。**同一件事有兩份等重的紀錄，比只有一份更難用。**
- [#偏離] **時鐘落差**：`settled_at` 記的是 UTC（`2026-08-27T00:00:54Z`），本機是 UTC+8（08:00）。讀 marker 時間時要記得換算，否則會誤判成「半夜在工作」。

### 五、檔案異動

- `40214c3` — `.gitignore`（+討論素材/狀態檔/`.workflow-harness/`）、`CLAUDE.md`（harness section）、`.workflow-harness.yaml`、`backlog.md`、`驗收節點.md`、`workflow-harness/work-map.jsonl`（5 筆登記）、`文檔/handoff/session-handoff-20260826.md`

（8/26 的五個 commit 列在 `session-handoff-20260826.md` 五欄，不重抄。）

### 六、下一步建議

1. **開始 `修正 TDD 保證的錯誤宣稱`**（已 `NEXT`）——`schema.yaml` 507-513 行那句 `so you do NOT need to invoke them manually` 是主動叫 agent 放手，改成據實說明 TDD 在 v6.3.0 是條件性的
2. 這件事適合**順便驗證整條 opsx 流程**在本 repo 跑不跑得動（低風險題目、第一次 dogfood）
3. **Change 2 重新設計前**先決定要不要救 Gemini——Codex 這次在 Windows 可攜性那條判斷錯誤，顯示單一審查者不夠
4. 改 `superpowers-bridge/` 後**務必重新同步安裝副本**：`cp -R superpowers-bridge/. openspec/schemas/superpowers-bridge/`


---

## Session 10:31

### 一、本 session 主題

第一次完整 dogfood opsx 流程：開 change `fix-tdd-transitive-claim` → 寫 brainstorm → 交 Codex 第三方審查（**不通過**）→ 中途發現 sd0x-dev-flow 從未裝進本 repo、補裝 → 審查結果寫成討論素材，留待下 session 白話討論。

### 二、完成事項

- **查證：TDD 假保證不是漂移，是一開始就讀錯**。上游 SDD 的 `SKILL.md` 在 6.2.0 / 6.3.0 內 TDD 字樣 0 處；5.1.0 只有 `Subagents follow TDD naturally`（宣傳語）與 `Subagents should use: test-driven-development`（建議清單）。`internally enforces` 在已查的三版都找不到來源。
- **全域掃描**：同一句假宣稱散在 10 處（審查後修正為**至少 28 段**）；README 自己跟自己打架——L500 已標 ❌ False，其餘七處仍當真。
- **建 opsx change + `brainstorm.md`**（`f8a1455`），決策鏈 Q1-Q8 附出處。
- **Codex 第三方審查：不通過**（2 P0 / 7 P1 / 2 P2）。P0-1 打斷設計：我們指定要用的 TDD skill 明文 `never grep its text`，而我們機制的核心就是 grep；它也把 configuration files 列為「問人類」的例外——而 `schema.yaml` 正是 configuration。
- **抽驗 8 條 citation**：7 條逐字成立、1 條修正措辭（`evals.json` 從沒寫「涵蓋維度 1-6」，那是推論）。並發現審查者漏掉的一項：`design_notes` 自陳 fixture case 被跳過，理由是「subagents describe their plan instead of actually grepping」——**那 4 個 eval 驗的是「有沒有說出計畫」，不是「有沒有真的去搜」**。
- **審查結果 + 每條建議 + 為什麼** → `2026-08-27-TDD假保證-第三方審查與改寫建議.md`（`ace9b9e`），含 5 個待拍板問題。
- **發現 sd0x 從未安裝**——auto-loop hook 整場 session 都在印「審核義務見 rules/auto-loop.md」，而該檔在本 repo 不存在，全程零報錯。裝入 4.3.1 的 16 份規則 + 37 支腳本（`131efe9`），修 LF/manifest 一致性（`3b48843`）。
- **Gemini 第二視角結案**：不是訂閱問題，是 Google 停掉整個個人層。定案改用 `agy --model gemini-3.7-flash-high`；更新 zhengwangle memory（`--effort` 不換模型的陷阱）+ 本專案建路標 memory。

### 三、未完事項 / 接力棒

- [#接力] **`brainstorm.md` 要重寫、不是打補丁**——P0-1 與 P1-3 動到的是問題的切分方式。改寫順序寫在審查文件 §三。
- [#接力] **改寫前必讀三份材料**（審查指出會直接改變設計）：`2026-08-26-TDD證據契約-Codex審查與查證.md:174`、`propagation-checklist.md:56-58`、`evals/evals.json` 全檔。
- [#待拍板] 五題見審查文件 §四：① configuration file 例外怎麼辦（上游說「問人類」，本 repo 產物幾乎全是 configuration）② 甲(分類表) / 乙(每張任務說出驗收判準) ③ 真閘門現在做還是另立 ④ 合併(Change1+2)還要不要維持 ⑤ 全域 CLAUDE.md 複審紀律改 `Codex → Fable` 還是標本 repo 例外。
- [#待確認] `~/.gemini/settings.json` 的 `defaultApprovalMode: "yolo"` 是無效值，未動（沿自 8/27 08:01）。
- [#環境] sd0x 快取已升 4.3.1，**重啟後才生效**；本 session 載入的仍是 4.2.1（規則與腳本內容已是 4.3.1）。
- [#未裝] sd0x hooks 刻意沒裝——會改變 repo 行為，等這個 change 收掉再議。

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **「讀了名字沒讀它實際說什麼」今天是第 3 個載體**。8/26 已是第 2 次、寫了 propose action 但**沒有落到任何載體**（本檔 08:01 區塊的接力棒明寫這件事）。今天我又犯：設計證據機制一整個下午，沒讀我們指定要 agent 去用的那個 TDD skill 自己怎麼定義證據。⇒ **這次已落 backlog `[優化建議] [case-count: 2]`**，不再只留在 handoff。
- [#反] **「宣告不存在前先窮舉」第 6 個載體**：`claude plugin --help | head -30` 被截斷就宣告「沒有更新路徑」，實際有 `update` 子命令。自己把輸出切掉，然後對切掉的部分下結論。

**【當日洞見】**

- [#洞見] **假保證有三個共同形狀**：把「建議」寫成「保證」、把「政策」寫成「閘門」、把「引用」寫成「執行」。三者都預設**「寫下來就會發生」**。今天在一份修第一種的文件裡，同時犯了第二、三種。
- [#洞見] **抄別人的引用等於自己的宣稱**。審查報告裡 Codex 的引用我全部自己驗過才寫進文件——其中一條發現他講得比原文支持的更滿。
- [#反] **「機器永遠判不出來」是我說的絕對句，被東杰當場推翻**。死板的檢查程式與會讀東西的 AI 是兩種東西，不能都叫「機器」——**人類不必當那個判斷者**。這條也命中全域 CLAUDE.md「寫絕對斷言前先找一個反例」。
- [#洞見] **安裝 / 生成類工作一定要回讀雙向核對**。`.claude/CLAUDE.md` 的切片程式在第一個空行就停了，只複製到 1 個引用（該 16 個）。是雙向核對抓到的，不是「檔案建好了」抓到的。
- [#洞見] **LF/CRLF 與 manifest 雜湊的互動**會造成「未來靜默跳過升級」；症狀一樣是一切正常。

**【學習候選】**

> 東杰提出的 Learning Candidate Gate 首次手動試跑（**不動 harness**；照其設計哲學先手跑幾次再決定要不要蓋機制）。本次產出 2 個候選、判定 1 個不升級。**依東杰選擇，候選停在本檔、不入 backlog、不動載體。**

- **候選 1 — Case**：設計證據機制一下午，第三方指出我們要 agent 去用的 TDD skill 明文 `never grep its text`，而機制核心就是 grep。
  **Pattern**：設計要「叫別人的元件去做某件事」時，先讀**那個元件自己怎麼定義那件事**，再設計你的要求。｜可重複：整合 / 橋接類；能改變行動：把「讀被整合方的定義」提到設計之前；邊界：只適用於「要求別人執行」，自己實作的不適用。
  **Evidence**：**強**（今天同型 3 次，因果直接，第三方一讀就抓到）。
  **Minimum Intervention**：不新增規則——在 brainstorm 既有探索步驟加一問「這個設計要求誰去做什麼？那個『誰』自己怎麼定義？」（改既有 Strategy）。
  **Promotion**：**Pattern Candidate**。與既有「先讀實際驗到什麼」高度重疊，**可能該是細化既有規則而非新增一條**——由東杰決定。

- **候選 2 — Case**：切片程式在第一個空行停了，`.claude/CLAUDE.md` 只複製到 1 個引用（該 16 個）。
  **Pattern**：「複製 / 生成一組東西」的驗證要用**雙向核對**（該有的都在 且 在的都該有），不是抽樣或存在性檢查。｜可重複：安裝 / 遷移 / 批次生成 / 翻譯同步；邊界：需有明確對照集，探索性工作不適用。
  **Evidence**：**中偏強**（今天 1 次直接命中；同家族第 3 次。「雙向比單向有效」只有 1 個直接證據，**接近成立、非確立**）。
  **Minimum Intervention**：不新增規則也不新增 skill——**已有載體**（`review-fix-propagation` 維度 9），缺的是安裝 / 生成類工作時會想到它 ⇒ 改該 skill 的觸發描述。
  **Promotion**：**Refine Existing Strategy**。

- **判定不升級**：「抄別人的引用等於自己的宣稱」＝既有「證據先於斷言」的直接應用，沒有新增判斷力。⇒ **History only**。

- [#實驗設計] ⚠️ **本次結果不算數的部分**：東杰在提問時已說明他要驗「agent 會不會什麼都想記、會不會硬升 Rule、Minimum Intervention 是否真比加規則簡單」。我知道被考什麼，兩個候選的 Minimum Intervention 都落在「改既有載體」——**成績受污染**。下次要真驗，指令只給五欄格式、不說要驗什麼。

### 五、檔案異動

| commit | 內容 |
|---|---|
| `131efe9` | sd0x-dev-flow 4.3.1 裝入：`.claude/rules/` 16 份、`.claude/scripts/` 22 core + 11 lib + 4 config、`.claude/CLAUDE.md`、`.sd0x/install-state.json` |
| `3b48843` | `.gitattributes` 釘 LF；51 檔正規化；manifest 依 LF 重算 |
| `f8a1455` | `openspec/changes/fix-tdd-transitive-claim/{.openspec.yaml, brainstorm.md}` |
| `ace9b9e` | `2026-08-27-TDD假保證-第三方審查與改寫建議.md` |
| （本次收工） | `backlog.md`（+2 條）、`workflow-harness/work-map.jsonl`（1 筆轉 DOING）、本 handoff |

### 六、下一步建議

1. **開工先讀** `2026-08-27-TDD假保證-第三方審查與改寫建議.md`——審查結果、每條建議與理由、5 個待拍板題都在裡面。
2. **讀完三份必讀材料**（見三、接力棒），再開始改寫。
3. **白話討論 5 個拍板題**，其中 ① configuration file 例外 與 ④ 合併要不要維持 會決定這個 change 的大小。
4. **重寫 `brainstorm.md`**（不是打補丁），順序見審查文件 §三。
5. 改 `superpowers-bridge/` 後務必重新同步安裝副本——**以本 repo CLAUDE.md 那條為準**（`rm -rf` 再 `cp`，8/27 08:01 handoff 第六欄第 4 條的疊加寫法不會清掉已刪檔案），並用 `diff -r` 回讀確認 IDENTICAL。
