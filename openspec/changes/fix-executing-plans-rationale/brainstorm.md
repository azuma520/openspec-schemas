<!--
Raw capture of superpowers:brainstorming output.
2026-10-06 session（開工 14:0x 起）對話的決策紀錄。brainstorming skill 分類為 bounded：
只改既有檔案的文字，設計於對話中逐段向使用者說明並取得同意後才開本 change。
-->

# Brainstorm — fix-executing-plans-rationale

> **本 change 的一句話**：bridge 拒用 `superpowers:executing-plans` 當 apply fallback 的**理由**
> 已因上游 v6.4.1 改版而不成立，把理由改回查證過的事實；**拒用這個結論不變**。
> 要不要放寬、怎麼放寬，是另一件工作的事（見 Q5）。

---

## 一、背景

### 1.1 來源

- 工作地圖 `task-20261002-executing-plans-rationale`（2026-10-02 使用者裁定 B1 附帶登記）。
- issue #2 相容性 spike 報告 `docs/superpowers/poc/2026-10-02-issue2-compat-spike/report.md` 的 R2、S13、S14。

### 1.2 bridge 目前的說法（三句）

出處：`superpowers-bridge/schema.yaml:10-12`、`:1707-1718`；`README.md:312`、`:462`、`:660`
與 `README.zh-TW.md` 同行號；repo `CLAUDE.md:252` 紅旗；以及**正式規格**
`openspec/specs/tdd-claim-accuracy/spec.md` REQ-3（`:61-73`）。

1. executing-plans 不派任何獨立審查者，單一 agent 自做自查。
2. 上游自己說：有 subagent 就改用 subagent-driven-development。
3. TDD 不是兩者的差異點。

### 1.3 上游原文現況（本 session 直接讀本機安裝檔，非轉述）

讀的是 `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/skills/`；
`superpowers-marketplace/superpowers/6.4.2/` 同檔 grep 結果行號一致。

| bridge 說法 | 上游 6.4.1 原文 | 判定 |
|---|---|---|
| ① 不派獨立審查者 | `executing-plans/SKILL.md:8-10`「no implementer subagent per task, no reviewer per task. One fresh-context review of the whole branch at the end.」；`:240`「With a subagent tool: dispatch the reviewer…」；`:253-257`「Without a subagent tool: read code-reviewer.md and perform that review yourself… a self-review by the author is weaker than a fresh reviewer, and your human partner decides whether that…」 | **一半錯**。有 subagent 時最後會派獨立審查；沒有 subagent 時（＝bridge 說的 fallback 情境）只能作者自審——這一半仍成立。兩種情況都**沒有每個任務的審查** |
| ② 上游有 subagent 一律導向 SDD | `executing-plans/SKILL.md:3` description「your human partner chose inline execution, or no subagent tool is available」；`:60-61`「Prefer superpowers:subagent-driven-development when your human partner wants a review gate on every task, or when the plan is long enough…」；`writing-plans/SKILL.md:179-182` 計畫完成時列出 Subagent-driven 與 Native 兩種方式並要求 agent 推薦其一 | **錯**。上游把兩條路當成由使用者挑選的平等選項 |
| ③ TDD 不是差異點 | `executing-plans/SKILL.md:149`「REQUIRED SUB-SKILL: load superpowers:test-driven-development now」；SDD 端仍是條件式（`subagent-driven-development/implementer-prompt.md:36`「following TDD if task says to」） | **結論成立**，但 REQ-3 的推理句「it does not travel through either of them」已不成立——executing-plans 現在無條件載入 TDD |

### 1.4 當時不是查錯，是上游後來改了

`superpowers/6.3.0/skills/executing-plans/SKILL.md:14`：「If subagents are available, use
superpowers:subagent-driven-development instead of this skill.」——8/31 的說法在當時版本成立。
spike 報告 S13 列 `grep -c` 計數：test-driven-development / code-review 出現次數
v5.1.0 = 0/0、v6.3.0 = 0/0、v6.4.1 = 2/4。所以本 change 修的是「上游改版、我們沒跟上」，
**不是 8/31 `fix-tdd-transitive-claim` 的查證錯誤**。

---

## 二、決策鏈

### Q1 只改理由，還是連「接不接受 executing-plans」一起重評？

- 選項 A：只改理由，結論不變。
- 選項 B：重評，有 subagent 時允許它當第二條路。
- 使用者先把問題拉高：「有沒有 skill 指導 agent 決定審查頻率」「per-task review 是否較好」
  「per-task 與 end-of-plan 能否用路由解決」「沒有 subagent 時自審能否算降級」。討論結果：
  - 「自審算降級」**已決**：正式設計 `docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`
    §2.2 把 Independent Review 列為 degradable，§5 寫「降級＝同一套 review skill＋self-review＋degradation record」。
  - 上游已有路由雛形（`writing-plans/SKILL.md:179-182` 推薦一種並附理由；
    `subagent-driven-development/SKILL.md:223-229` 同類小改動合批審一次），bridge 因
    apply 寫死 SDD 而繞過了這個路由點。
  - 查 6 個已歸檔 change：實務上已混用「每個任務審」「合批審」「不走 SDD、靠外部多輪審」三種做法，
    但都是當下判斷、事後寫進複盤，沒有事前寫進計畫。
- **裁定（使用者）**：這次只把說法改對；要不要放寬、怎麼放寬，是後面那件工作的事（見 Q5）。

### Q2 改哪些地方？

| 位置 | 動作 |
|---|---|
| 正式規格 REQ-3 | **改寫**（源頭：它用 SHALL 規定理由必須是那兩句，文件是照它寫的；只改文件不改規格，下次照規格檢查會被改回去） |
| `schema.yaml:10-12`、`:1707-1718` | 照新 REQ-3 改 |
| `README.md` / `README.zh-TW.md` `:312`、`:462`、`:660` | 照新 REQ-3 改 |
| `CLAUDE.md:252` 紅旗 | 照新 REQ-3 改，並加一句預告（見 Q4） |
| `README.md` / `README.zh-TW.md` `:563-564` 查核紀錄列 | **不改**：歷史紀錄；`:605` 已有「這筆取代上面那列」的新列 |

- **裁定（使用者）**：沒問題。

### Q3 新理由寫什麼？

只寫查證過的事實：
- executing-plans 沒有每個任務的審查，只在最後審一次。
- 沒有 subagent 的平台上（fallback 會發生的情境），最後那次只能作者自審。
- bridge 的 apply 依賴「每個任務都有獨立審查」的審查結構，所以不接受它。
- TDD 不是差異點：bridge 的 TDD 要求經 tasks.md 標註與證據契約送達執行者，與哪個執行者無關。
  （不再寫「TDD 不經過任何一個執行者」——executing-plans 現在會載入 TDD。）

- **裁定（使用者）**：同意。

### Q4 要不要加一句「這條禁令之後會改成另一種寫法」？

- 我原本建議全部位置都加。使用者問為什麼要加。
- 重新評估：風險只在**維護者面**——之後的 agent 讀到 CLAUDE.md 紅旗會把禁令當永久規定，
  在依正式設計 §5 改寫時可能拿它來反對。schema 與 README 是給採用者看的，「之後可能會改」
  對他們沒有用處；且這件事已在工作地圖追蹤。
- **裁定（使用者）**：只加在 `CLAUDE.md`。

### Q5 既然上游有新版，要不要開始允許 executing-plans？

- 注意：bridge 從來沒用過它，是「要不要開始允許」，不是「恢復」。
- 好處：省、快；新版已有 TDD 與最後的獨立審查（有 subagent 時）。
- 代價：沒有每個任務的審查。紀錄裡每個任務的審查確實抓過東西（fix-v2 複盤
  `openspec/changes/archive/2026-09-14-fix-v2-blocking-defects/retrospective.md:83`：審查者推翻了
  controller 依未查證前提做的裁定）；上游自己說計畫長時改用 SDD；使用者說過「做好做對更重要」。
- 這題的正確形狀是「依工作類型決定只審一次、檢查點審、還是每個任務都審」，
  不是二選一。
- **裁定（使用者）**：這次不動禁令；放寬與否交給工作地圖上的
  `task-20260901-claudemd-governance-rewrite`「CLAUDE.md 紅旗治理語言改寫」那件（須隨 apply 相關 schema 實作一起做）。

### Q6 怎麼執行？

- 走完整 opsx change（動到正式規格，必走）。
- 全是文字更正：**主 session 直接做，不開 worktree、不走 SDD**，品質靠外部審查多輪把關。
  先例：`openspec/changes/archive/2026-08-31-fix-tdd-transitive-claim/retrospective.md:69-72`
  記錄了同樣的判斷與理由（docs-only corrective fix、變更面凍結在文字層、dogfood 副本在 worktree 內會互踩）。
- **裁定（使用者）**：可以。

---

## 三、已知矛盾（記錄，不在本 change 處理）

正式設計 §2.2 把 Independent Review 定為 degradable：沒有 subagent 時應允許自審降級並留紀錄。
照此，bridge 在無 subagent 平台應**允許**降級而非禁止——本 change 保留禁令，與設計不一致。
保留的理由：設計 §5 末段明寫「由後續 implementation change 改寫，本設計不直接修改」，
工作地圖該件亦註明「須隨 apply 相關 schema 實作 change 一起做，不可先行」。
使用者裁定：「好，到時候做」。

## 四、版本

- 不讓任何原本合法的 artifact 變不合法、不增刪 artifact、不改 `requires:`、不改 PRECHECK 形狀
  → **schema major 不動**。
- `VERSION`（目前 3.0.0、tag 未打）是否改 3.0.1：發版時再決定，本 change 不動。

## 五、範圍外（同 session 討論過、明確不在本 change）

- 審查路由研究（依改動風險與依賴結構決定審查頻率）：未登記；若要正式研究另行登記。
- SDD 過程紀錄（`.superpowers/sdd/`）不隨 archive 保存：使用者裁定**不登記**——對一般採用者
  不需要，研究需要時當次保存即可；複盤引用則把關鍵內容直接寫入。
