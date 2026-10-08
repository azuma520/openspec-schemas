# Superpowers 6.x 相容基準重新定錨・第一步：能力契約缺口盤點（2026-10-08）

> ⚠️ **Working research document（分析參考），不是規範、不是裁定。** 本文盤點 bridge 對 Superpowers 的依賴在 6.x 下還差什麼，作為「6.x 相容基準重新定錨」的第一步輸入。凡涉及「bridge 該承諾什麼」的地方都列成【決策點】，由維護者拍板；拍板前不改 `superpowers-bridge/`、schema、README、specs、CLAUDE.md 與工作地圖。
>
> **定位**：工作地圖 `task-20261007-superpowers-6x-rebaseline`（第一步：能力契約缺口盤點；第三步才是整體相容性驗證）。S4／S5 已有既存工作 `task-20260826-fix-brainstorming-drift`，本文沿用、不另立。⚠️ `task-20260901-guarantee-spikes` 的 S1–S6 是**另一套編號**（capability spikes），與本文沿用的 issue #2 spike 編號 S1–S18 無關。
>
> **原則（維護者 2026-10-07 定調）**：不為追上游而升級；先問新版**原生已提供什麼**、bridge 的能力契約**實際需要什麼**、用合理成本怎麼接上。先例：`task-prefixed-plan-headings`（2026-10-08 archive）用調整 Plan Contract 讓上游原生 `task-brief` 能用，而不是做 adapter，關掉了 S11 的「辨識」那一半。
>
> **標記**：【未查證】＝沒查到來源；【推論】＝從讀到的原文推出、未實測；其餘每一條都附檔案與位置。bridge 端位置用「檔案 § 語意錨點（約第 N 行）」，行號只是提示。

---

## 0. 方法與證據來源

| 項目 | 內容 | 來源 |
|---|---|---|
| 上游版本確認 | 本機快取 `claude-plugins-official/superpowers/6.4.1/skills/` 與 `superpowers-marketplace/superpowers/6.4.2/skills/`，各自與上游 git tag `v6.4.1`、`v6.4.2` 用 `git archive` 取出的 `skills/` 做 `diff -rq`：**兩者皆逐檔相同**（2026-10-08，本 session scratchpad clone）。因此下文的上游連結用固定標籤 `https://github.com/obra/superpowers/blob/v6.4.1/...` | 本 session 實測 |
| 6.4.1 vs 6.4.2 差異 | `skills/` 之間只差 `writing-plans`（`SKILL.md` 不同、6.4.2 移除 `plan-document-reviewer-prompt.md`）。本文涉及的 brainstorming / using-git-worktrees / subagent-driven-development / finishing / executing-plans 在兩版**完全相同**，所以下文對 6.4.1 的引用同樣適用 6.4.2；兩個 marketplace 快取的 6.4.1 也逐檔相同 | 本 session `diff -rq` |
| v5.1.0 對照 | 從同一個 clone `git show v5.1.0:skills/...` 讀 brainstorming、using-git-worktrees、finishing、SDD 四份 SKILL.md 的相關段落 | 本 session |
| 上游最新 release | `gh api repos/obra/superpowers/releases/latest` → `v6.4.2`（2026-09-25）；`v6.4.1` 為 2026-09-19 | 本 session |
| 官方 marketplace 釘的版本 | 本機 `marketplaces/claude-plugins-official/.claude-plugin/marketplace.json` 與上游 `anthropics/claude-plugins-official` HEAD `b78ac49`（2026-10-07）都把 superpowers 釘在 sha `5bf4e78…`；`git describe` → **`v6.4.1`** | 本 session（補上 spike 留下的 S17【未查證】） |
| bridge 端 | `superpowers-bridge/schema.yaml`（brainstorm / design / plan instruction、apply instruction）、`README.md`（Seven touchpoints、Apply walkthrough、Six design touches、Compatibility、Re-verification log）、`templates/brainstorm.md`、`templates/plan.md`、`templates/adopters/*`、repo `CLAUDE.md` 紅旗段、`openspec/specs/tdd-claim-accuracy/spec.md` | 本 session 全文或段落讀過（見各項「沒查的」） |
| dogfood 紀錄 | `openspec/changes/archive/*/brainstorm.md` 與 `retrospective.md`（三個 change 明寫在 6.4.1 下呼叫過 brainstorming） | 本 session grep + 讀段落 |
| 起點 | `docs/superpowers/poc/2026-10-02-issue2-compat-spike/report.md` §1b、§2b、§3、§5 與 `raw/SUMMARY.md`。spike 的判定只當線索，下文每項上游行為都重新讀原文 | — |

**沒有做的**：沒有實際跑任何 Superpowers skill 或 `/opsx:*` 流程（全部是讀原文＋讀既有 dogfood 紀錄）；沒有讀 `README.zh-TW.md` 全文（只對照了本文引用的對應行）。

---

## 1. 總表

| 項 | spike 判定（10/02） | 本文分類 | 一句話 |
|---|---|---|---|
| S4 | 不成立 | **(b)** 採上游原生能力＋小幅契約調整 | 五步驟只剩 architectural 路徑；上游新增的「意圖確認＋寫回理解」與 HARD-GATE 正是 bridge 要的，改寫成「依上游分類、產出一律落 brainstorm.md」 |
| S5 | 不成立 | **(b)**（【決策點 D1】可能升為 (c)） | 上游終點是 writing-plans（architectural）或直接實作（bounded）；bridge 需要「brainstorm 到 brainstorm.md 為止」。上游 HARD-GATE 的「spec → 實作計畫 → 選執行方式」可以對到 bridge 的 brainstorm → plan → apply |
| S6 | 未查證 | **(a)** 文件更正（但文字在 schema.yaml，要搭 change） | 上游任何版本都沒說產出是 decision log；那是本 repo dogfood 的觀察 |
| S7 | 有變化 | **(a)** 文件更正（【決策點 D3】若要改 apply step 1 的承諾則搭 change） | README 的 `.worktrees/<change-name>/` 描述在 v5.1.0 就不精確；上游會先偵測、問同意、優先用原生工具、可能就地工作 |
| S11 | 不成立 → 已處理 | **(d)** 確認現況 | v4（`4.0.0`）已解決「辨識」；擷取範圍正確性仍不保證 |
| S12 | 不成立 | **(a)** 文件更正 | bridge 不依賴 discard 或 cleanup；只要改 README 描述 |
| S13 | 不成立 → 已處理 | **(d)** 確認現況 | `fix-executing-plans-rationale` 已改好；剩餘的理由／證據分離屬 `task-20260901-claudemd-governance-rewrite` |
| S14 | 不成立 | **(a)**，限 README 一句（其餘 (d)） | 宣稱句已在 10/06 移除且有 living spec 防回歸；但 README 一句後來寫的總結仍說「S14 未對齊」 |
| S17 | 有變化 | **(a)**＋【決策點 D4】 | README 安裝指令實際拿到 6.4.1（官方 marketplace 仍釘 6.4.1）；drift 檢查比的是 v6.4.2 |
| S18 | 有變化（影響小） | **(d)** | 該列是 v6.3.0 的帶日期紀錄，行號對 v6.3.0 正確；而且 6.4.1／6.4.2 同段落行號相同，spike 說的「移動」是區段取法不同 |
| （新）S19 | —（spike 未列） | **(b)** 候選【決策點 D5】 | SDD 自己的終點是呼叫 finishing（v5.1.0 起就如此），bridge 卻要求 verify → retro → archive 之後才 finishing，apply step 2 沒交代 |

分類定義（照本任務的四類）：(a) 只需更正文件；(b) 採用上游原生能力＋小幅契約調整（S11 式）；(c) 需要正式設計變更（改 bridge 保證或破壞性 schema 變更）；(d) 不需動作／資訊性。

---

## 2. 逐項

### S4 — brainstorming 走五個步驟

1. **Bridge 契約**：`schema.yaml` brainstorm instruction 末段「The brainstorming skill will: 1. Explore project context … 5. Output the validated design」（約第 57–62 行）。這是**描述上游會做什麼**，不是 bridge 自己的檢查；bridge 真正依賴的是：有一段經使用者逐步同意的設計探索，其產出完整寫進 `brainstorm.md`，足以讓 design instruction 重組成 Context / Goals / Decisions / Risks / Migration（design instruction，約第 94–118 行）。README 的 Re-verification log「Open drift」段（約第 601 行）記錄這個漂移。
2. **6.x 實際行為**（[v6.4.1 brainstorming/SKILL.md](https://github.com/obra/superpowers/blob/v6.4.1/skills/brainstorming/SKILL.md)，6.4.2 相同）：
   - 開頭新增 **Establish Shared Understanding**（第 14–36 行）：先問目的、把理解寫回給使用者確認、「Carry intent into the design … the written spec for architectural work, or the in-chat design/probe for bounded work and spikes」（第 29–32 行）。這段 6.3.0 沒有（6.3.0 → 6.4.1 `diff`）。
   - **HARD-GATE**（第 38–56 行）：spike／bounded／architectural 各自的前置核可；architectural 要「reviews and approves the written spec, then reviews the written implementation plan and selects its execution method」。
   - **Three Paths**（第 58–88 行）：先分類並說出口、使用者可推翻；「When in doubt between two paths, take the heavier one」「Nothing downgrades mid-task」。
   - **Checklist**（第 110–138 行）：五步驟（探索、一次一題、2–3 方案、分段報設計、寫出）只完整出現在 Architectural 第 1、3、4、5、6 項；Bounded 是「探索 → 問 → 聊天內短設計 → 核可 → 實作」；Spike 是「探索 → 問題＋探測計畫 → 點頭 → 調查 → 報告」。
   - 對照 v5.1.0（`git show v5.1.0:skills/brainstorming/SKILL.md`）：只有一條路徑，Checklist 第 24–32 行就是 bridge 描述的步驟；HARD-GATE 一句話（第 13–15 行）。所以 bridge 那段描述在 v5.1.0 成立、6.3.0 起不成立。
3. **bridge 的要求還需要嗎？** 「五步驟」這段**描述**不需要——它不是 bridge 要保證的東西。bridge 真正要的「探索有經使用者核可、產出可供 design 重組」，6.4.1 原生提供得比 v5.1.0 更多：意圖確認與寫回理解（第 19–28 行）、每條路徑都有核可閘（第 38–56 行）、「拿不準就走重的」（第 86 行）。缺的只有一件：bounded／spike 路徑的產出預設**不寫檔**（第 80 行「No spec file」、第 68 行「No design doc」），而 bridge 要 `brainstorm.md`。
4. **分類：(b)**。理由：不需要 adapter，也不需要改 artifact 或 PRECHECK；只要把 instruction 的五步描述換成「依上游分類執行，選定路徑的設計產物（含寫回的理解）一律原樣寫進 brainstorm.md」。上游自己就允許改輸出位置：架構路徑的「Write the validated design (spec) to `docs/superpowers/specs/…` — (User preferences for spec location override this default)」（第 241–242 行；v5.1.0 第 111–112 行同句）。bounded 路徑「不寫檔」被 bridge 覆寫成「寫進 brainstorm.md」，這一點**沒有**上游原文背書，是 bridge 的注入。
   - 實證（dogfood，非受控實驗）：6.4.1 下呼叫 brainstorming 的三個 change——`2026-10-01-requirement-scenario-identity`（architectural，`brainstorm.md` 第 3–4 行）、`2026-10-02-retro-skill-inventory`（bounded，第 3–4 行；第 98 行記「bounded 路徑原本只在對話中給短設計、不寫檔，schema 卻要求寫入 brainstorm.md」）、`2026-10-06-fix-executing-plans-rationale`（bounded，第 3 行）——都照 bridge 把產出寫進 `brainstorm.md`，之後接 proposal。n=3、同一位維護者、同一份 CLAUDE.md，不能推廣到一般採用者。
5. **建議與成本**：改寫 brainstorm instruction 的五步段落，與 S5、S6 併成一個 opsx change（就是既有工作 `task-20260826-fix-brainstorming-drift`）。【決策點 D1】見 S5。動到 `schema.yaml` 的 instruction 文字；依 README § Versioning 的 schema major 判準（約第 485 行：原本合法的 artifact 變不合法、artifact 增刪、`requires:` 改、PRECHECK 形狀改），**只改 instruction 散文不觸發 major bump**【推論：條文如此，但要看最後改法——若同時新增 verify 檢查（例如要求 brainstorm.md 記錄路徑分類），原本合法的 brainstorm.md 會變不合法，就是 major】。估計：一個 change、改動集中在 brainstorm instruction＋README Open drift 段＋adopter fragment（中英）【估計】。驗證：第三步整體驗證中，至少一次 architectural、一次 bounded 分類各跑一輪，檢查 brainstorm.md 有寫出、內容含寫回的理解與核可過的設計、design.md 能從中重組。
6. **沒查的**：沒跑 skill；沒驗「agent 讀到 bridge 注入的 instruction 後會不會照做」（只有上述 n=3 的 dogfood）；沒讀 `visual-companion.md`（6.3.0→6.4.1 有改，與本項推斷無關但沒確認）；spike 路徑在 bridge change 裡會不會真的出現【未查證】。

### S5 — brainstorming 結束後可接 proposal → design → specs → tasks

1. **Bridge 契約**：bridge 把 brainstorm 當第一個 artifact，之後依 DAG 走 proposal／design → specs → tasks → plan → apply（README § Artifact DAG，約第 198–204 行）；README Open drift 段（約第 601 行）寫「Separately, the v6.x skill states that after the architectural path the only skill to invoke next is `writing-plans`」。adopter fragment 的 Entry routing（`templates/adopters/CLAUDE.md.fragment.md` 約第 13 行，zh-TW 同）讓口頭 brainstorming 先跑、收斂後再升級成 `/opsx:propose`。
2. **6.x 實際行為**（v6.4.1 brainstorming/SKILL.md）：
   - 「**Terminal states are path-bound.** Architectural: the ONLY skill you invoke after brainstorming is writing-plans … Bounded: after approval, implementation proceeds directly through the normal development workflow; no plan document. Spike: … a reported recommendation」（第 184–189 行）；Process Flow 圖裡 bounded 的終點是「Implement via normal workflow (no plan doc)」（第 150、169 行）；Checklist Bounded 第 5 項「Implement … no plan document」（第 127 行）；After the Design「Do NOT invoke any other skill. writing-plans is the next step.」（第 263–266 行）。
   - HARD-GATE 限制的是**實作動作**（invoking an implementation skill、writing product code、scaffolding、安裝相依、建外部專案，第 39–41 行），不是寫文件。
   - **新發現（更正 README 的說法）**：「architectural 之後只能接 writing-plans」**不是 v6.x 才有**。v5.1.0 第 66 行：「The terminal state is invoking writing-plans … The ONLY skill you invoke after brainstorming is writing-plans.」，第 135–136 行同義。也就是 bridge 宣告的基準 v5.1.0 本來就與 bridge 的 DAG 有這個張力；6.x 新增的是 bounded「直接實作」（6.3.0 起，spike 報告 S5 列已引 6.3.0 SKILL.md:92）與 6.4.1 的分段核可 HARD-GATE。
3. **bridge 的要求還需要嗎？** 需要：bridge 要 brainstorming 停在「brainstorm.md 寫好、經核可」，不呼叫 writing-plans、不開始實作。但上游有一塊**可以直接借用**：6.4.1 HARD-GATE 的 architectural 前置條件「核可書面 spec → 審書面實作計畫 → 選執行方式」（第 46–49 行），與 bridge 的「brainstorm.md（書面 spec）→ … → plan.md（書面實作計畫）→ `/opsx:apply`（選定執行方式：SDD）」可以一一對上【推論】。也就是 bridge 不必對抗上游的閘門，只需宣告「在本 schema 裡，writing-plans 那一步由 change 自己的 artifacts 擔任」。現有的層層防護：OpenSpec 產生的 `openspec-continue-change` skill「STOP after creating ONE artifact」（本 repo `.claude/skills/openspec-continue-change/SKILL.md` 約第 72、110 行）讓逐步流程在 brainstorm 之後自然停下；dogfood 三例的 retrospective 都沒有呼叫 writing-plans 的紀錄（例：`2026-10-01-requirement-scenario-identity/retrospective.md` 第 114 行 `N/A`）。`/opsx:ff` 一次跑完所有規劃 artifact，沒有這個逐步停頓【推論：風險較高的入口】。
4. **分類：(b)**，前提是【決策點 D1】選 A 或 B；選 C 則為 (c)。理由：(b) 只改 instruction 散文、不動 artifact／`requires:`／PRECHECK。

   **【決策點 D1】bridge change 裡的 brainstorming 要怎麼對待上游的三條路徑？**
   - **為什麼現在要決定**：這是 S4／S5／S6 共用 change 的設計主軸，決定了改法與要不要 bump major。
   | 選項 | 好處（優勢／機會） | 代價（劣勢／風險） |
   |---|---|---|
   | A：一律走 architectural（instruction 宣告「本 schema 視為使用者已選 architectural」） | 與 README Entry gates 一致——小改動本來就該 direct PR、不進 change（README § When NOT to enter the schema，約第 150–166 行）；上游允許往重的方向調（第 86 行）、允許使用者推翻分類（第 60–63 行） | 本 repo 6.4.1 dogfood 三例有兩例被分成 bounded 且運作良好（見 S4），強制 architectural 會多一輪「書面 spec 審查」儀式；違反上游「說出分類讓使用者推翻」的精神不大，但會讓 bounded 規模的 change 變重 |
   | B：接受上游分類；不論路徑，核可後的設計（含寫回的理解）一律寫進 brainstorm.md，之後停下；不呼叫 writing-plans、不實作，plan.md＋apply 擔任上游的「實作計畫＋選執行方式」；spike 分類時提示「這不該是一個 change」 | 最貼近上游原生行為、成本最低；與 dogfood 實際做法一致 | bounded 的產出較薄，可能讓 design.md 重組時素材不足（README Open drift 段原本擔心的「starves the design artifact」）【未查證實際影響：dogfood 兩例 bounded 的 design.md 未評估】 |
   | C：不再依賴 brainstorming skill（brainstorm.md 由 agent 直接寫，skill 降為選用輔助，比照 v2 對 writing-plans 的處理） | 徹底脫離上游路徑設計的變動 | 移除 brainstorm 的 skill PRECHECK＝PRECHECK 形狀改變＝schema major bump；失去上游意圖確認／核可閘這些現成能力，違反「先用上游原生能力」原則 |
   - **建議 B**：理由是它用的全是上游已有的機制（分類、核可閘、可改輸出位置），bridge 只補「寫檔＋停下」兩件事；A 可以當 B 的加嚴選項（例如 instruction 寫「拿不準時走 architectural」，那本來就是上游規則）。**我沒查的**：bounded 產出的 brainstorm.md 對 design.md 品質的實際影響、`/opsx:ff` 入口下 agent 會不會在 brainstorm 後直接實作。
5. **建議與成本**：與 S4、S6 同一個 change。範圍：brainstorm instruction（加「terminal state in this schema」段）、README Open drift 段（以 append 新紀錄的方式更正「v6.x 才有 writing-plans 終點」——v5.1.0 就有）、adopter fragment 中英兩份的口頭 brainstorming 路由（口頭 brainstorming 在 bounded 路徑核可後上游會直接實作，與「收斂後升級 `/opsx:propose`」衝突【推論】）、README § Entry & exit gates 對應段。依 repo CLAUDE.md「跨檔耦合」表，routing 規則改動要連 fragment 一起改。驗證：第三步跑 `/opsx:new` 與 `/opsx:ff` 兩種入口各一輪，確認 brainstorm 後沒有呼叫 writing-plans、沒有產生程式碼 commit，直到 apply。
6. **沒查的**：`/opsx:ff`、`/opsx:propose` 入口下的實際行為；adopter 環境（沒有本 repo 這份強勢 CLAUDE.md）下 agent 是否照 bridge 注入停下；上游 `writing-plans` 若被 agent 誤叫，會不會把 plan 寫到 `docs/superpowers/plans/`（6.4.1 writing-plans 第 177 行預設路徑）而觸發新的外漏。

### S6 — brainstorming 的產出通常是 decision log

1. **Bridge 契約**：brainstorm instruction「The skill's natural output is typically a decision log (background → decision chain Q1-Qn → design trade-offs), but the format varies by conversation」（`schema.yaml` 約第 46–51 行）；design instruction「a raw capture of the brainstorming skill's output (typically a decision log with Q1-Qn decisions …)」與「Decisions (Q1-Qn from brainstorm) → design.md §Decisions」（約第 97–103 行）；`templates/brainstorm.md` 第 4–6 行。
2. **6.x 實際行為**：v6.4.1 brainstorming 全文沒有「decision log」或「Q1」字樣（`grep -i decision` 只命中 Visual Companion 的「Per-question decision」，第 277、280 行）；v6.3.0、v5.1.0 同樣沒有。上游說的產物是：architectural 的書面 spec（設計涵蓋 architecture, components, data flow, error handling, testing，第 221 行）、bounded 的聊天內短設計（第 125 行「approach, files touched, testing」）、以及 6.4.1 起的「寫回理解」短筆記（第 25–28 行）。
3. **還需要嗎？** 「通常是 decision log」是**本 repo dogfood 的觀察**，不是上游行為：`openspec/changes/archive/` 下 7 份 brainstorm.md 多數是「背景 → 決策鏈 Q1–Qn」形狀，其中 4 份開頭自稱「決策日誌」或「決策紀錄」（loosen-plan、requirement-scenario-identity、retro-skill-inventory 第 3 行；fix-executing-plans-rationale 第 3 行）；但其中 `2026-09-14-fix-v2-blocking-defects` 明寫手寫、未跑 skill（第 4 行），其餘反映的可能是維護者的對話習慣而非 skill 產出【推論】。design instruction 已用「typically」「format varies」留了彈性，不會因此出錯；問題是它把「Q1–Qn」寫成主要映射，讀者會以為上游產出有這個結構。
4. **分類：(a)** 文件更正。但文字位在 `schema.yaml` 的 brainstorm／design instruction 與 `templates/brainstorm.md`，依三軌制（repo CLAUDE.md「三軌制路由」：schema → opsx）要搭 change，不能直接 commit。
5. **建議與成本**：在 S4/S5 的 change 裡順手改成「產出形狀依上游選定路徑而定（architectural：書面 spec；bounded：短設計；兩者都含寫回的理解）；若對話是決策鏈形式，Decisions 對應到 design.md §Decisions」。估計增量很小【估計】。驗證：第三步 architectural 那輪的 brainstorm.md 能被 design instruction 無歧義地重組。
6. **沒查的**：沒實際跑 skill 看 architectural spec 的真實形狀（spike 的 S6 未查證仍成立）；7 份 brainstorm.md 中哪幾份真的經過 skill、哪幾份是對話後手整理，只看了開頭自述。

### S7 — using-git-worktrees 建 `.worktrees/<change-name>/`、開 branch、跑 setup、確認測試基線

1. **Bridge 契約**：README § Apply phase walkthrough「1. Workspace」：「Creates `.worktrees/<change-name>/`, switches to a new branch, runs setup, confirms a clean test baseline.」（約第 380 行；zh-TW 第 380 行同義）。`schema.yaml` apply step 1「invoke superpowers:using-git-worktrees to create an isolated git worktree for this change」（約第 1744–1746 行）。README 第 376 行另說「handling untracked change directories is the worktree skill's responsibility」。
2. **6.x 實際行為**（[v6.4.1 using-git-worktrees/SKILL.md](https://github.com/obra/superpowers/blob/v6.4.1/skills/using-git-worktrees/SKILL.md)）：Step 0 先偵測是否已在 linked worktree，是就不建（第 16–37 行）；在一般 checkout 時若使用者沒預先表態，**先問同意**，拒絕就就地工作（第 41–45 行）；優先用 harness 原生工具（如 `EnterWorktree`，第 51–57 行），沒有才 `git worktree add "$LOCATION/$BRANCH_NAME" -b "$BRANCH_NAME"`（第 92–97 行），路徑以 **branch 名**命名、目錄依「指示 → 既有 `.worktrees`／`worktrees` → 預設 `.worktrees/`」（第 65–76 行）；sandbox 擋下時就地工作（第 100 行）；setup 與基線測試仍在（第 102–132 行）。全文沒有處理「未追蹤的 change 目錄」的段落。
   - 對照 v5.1.0：同樣有 Step 0、問同意、原生工具優先（`git show v5.1.0:…` 第 41、45、51–57 行）；差別只有 v5.1.0 還有全域目錄 `~/.config/superpowers/worktrees/`（第 79、97、106 行），6.x 拿掉。所以 README 第 380 行的描述**在 v5.1.0 就不精確**。
3. **還需要嗎？** bridge 需要的是「apply 在隔離環境進行」；上游已原生提供（且比 bridge 描述的更周到：偵測、同意、原生工具）。但上游**不保證**一定隔離（使用者拒絕、sandbox 失敗都就地工作），而 apply step 1 的措辭「to create an isolated git worktree」比上游保證強。另一個相關已知事實：worktree 拿不到 gitignore 掉的 `openspec/schemas/` 副本，曾導致 opsx 靜默改用 `spec-driven`（`docs/superpowers/retrospectives/2026-09-03-loosen-plan-execution.md` 第 149 行 E1，當時定性為 dogfood 環境問題、未宣稱產品層）；同理，未 commit 的 change 目錄在新 worktree 裡也不存在【推論】，而 README 把它推給 worktree skill，上游原文沒有承擔這件事。
4. **分類：(a)** 文件更正（README 中英）。若【決策點 D3】選擇讓 apply step 1 的承諾與上游對齊，則該句改寫屬 schema instruction，搭 S4/S5 change 或下一個 apply 側 change。

   **【決策點 D3】apply step 1 要不要把「一定建 worktree」降為「建立或確認隔離工作區；使用者可拒絕」？** 好處：與上游原生行為一致，不宣告上游不保證的事；代價：明文承認可能就地工作，等於降低 bridge 對隔離的描述強度（目前也沒有任何檢查在保證它）。**建議**：改，且一併把 README 第 376 行「untracked change directories 由 worktree skill 負責」改成事實（上游沒寫；bridge 要嘛提醒 apply 前 commit change artifacts，要嘛明寫不處理）——但「提醒 commit」碰到紅旗「instruction 不得主動 git add / commit」，只能寫成提示使用者，不能寫成 agent 動作。**我沒查的**：原生 `EnterWorktree` 建出的路徑與 branch 命名規則、它對未追蹤檔的處理。
5. **建議與成本**：README 中英第 380 行改寫成「偵測既有隔離 → 徵得同意 → 優先原生工具，否則 `.worktrees/<branch>` → setup → 基線測試；使用者拒絕或 sandbox 阻擋時就地工作」。純文件、可直接 commit（三軌制「文件 → 直接 commit」）；需過 `/codex-review-doc`（`.claude/CLAUDE.md` Required Checks）。成本：數行【估計】。驗證：第三步實跑時記下走的是原生工具還是 fallback、路徑長什麼樣，與新描述比對。
6. **沒查的**：沒實跑；Codex／其他平台的原生工具；`finishing` 對原生工具建出的 worktree 走「host 擁有、不清理」分支（finishing 第 200–201 行）是否就是 Claude Code 的情況【未查證】。

### S11 — SDD 能吃 bridge 的 plan.md（確認現況，不重新分析）

- **現況**：`task-prefixed-plan-headings` 已於 2026-10-08 archive（`openspec/changes/archive/2026-10-08-task-prefixed-plan-headings/`；verify.md 第 379 行 `⚠️ PASS WITH WARNINGS`），`superpowers-bridge/VERSION` = `4.0.0`，tag `v4.0.0` 在 remote 存在（`git ls-remote --tags origin v4.0.0`），工作地圖 `task-20261002-task-brief-heading-compat` = DONE。plan instruction 接受 canonical `## Task 1.1 — …`（`schema.yaml` plan instruction 第 2 點，約第 386–434 行）。verify.md 第 344 行：用 6.4.1 `task-brief` 實跑 entry 2.2、4.2，擷取內容與 plan entry 逐行相同。
- **上游**：[v6.4.1 `scripts/task-brief`](https://github.com/obra/superpowers/blob/v6.4.1/skills/subagent-driven-development/scripts/task-brief) 的 awk 以 `^#+[ \t]+Task[ \t]+[0-9]+` 分段、`Task N([^0-9]|$)` 選段（第 29–35 行），6.4.2 相同。
- **仍開著的（已在 README 記錄，不是新缺口）**：只保證「辨識」，不保證擷取範圍正確（README Re-verification log「Follow-up status (schema v4)」，約第 643 行）；legacy `## 1.1 —` 仍不被辨識；verify.md 第 350 行 R15（check 12 的上游說明句沒標版本）deferred。
- **分類：(d)**。第三步要涵蓋：一份全 canonical 的 plan 在 SDD 下每個 entry 都被 `task-brief` 抽出，並抽查最後一個 entry 有沒有吞到尾端非 entry 文字（verify.md 第 344 行說本 repo 那份 plan 沒觸發這情境）。

### S12 — finishing：先確認綠燈、給 merge / PR / keep / discard、清理 worktree

1. **Bridge 契約**：README § Apply phase walkthrough「6. Completion」：「Confirms tests are green, presents merge / PR / keep-branch / discard options, cleans up the worktree. **PR is the last step**」（約第 423 行；zh-TW 第 423 行同義）。`schema.yaml` apply step 6（約第 1838–1848 行）只要求在 retro＋archive 之後呼叫 finishing、PR diff 要含完整 archive 後的 cycle——**沒有**依賴選單內容或清理行為。`templates/verify.md` 第 269 行只說 PASS 後「可進入 finishing-a-development-branch 與 archive」。
2. **6.x 實際行為**（[v6.4.1 finishing-a-development-branch/SKILL.md](https://github.com/obra/superpowers/blob/v6.4.1/skills/finishing-a-development-branch/SKILL.md)）：先跑全套測試、失敗就停（第 14–26 行）；一般 repo／具名 branch worktree 給**三個**選項 merge／PR／keep（第 55–65 行），detached HEAD 給兩個（第 67–76 行）；discard 只在使用者明確要求時、且要打字 `discard` 確認（第 78–82、132–157 行）；PR 與 keep **保留** worktree（第 126、161–162 行）；只有 merge 與確認過的 discard 才清理，而且只清 `.worktrees/` 或 `worktrees/` 下的，其他「host 擁有、不動」（第 159–201 行）。
   - 對照 v5.1.0：四個選項含 discard（`git show v5.1.0:…` 第 68–78 行），但 Quick Reference 已是「PR → Keep Worktree: yes」（第 196–201 行）。所以「cleans up the worktree」在 v5.1.0 對 PR 路徑就不成立；6.x 真正改的只有 discard 從選單移除（spike 引 RN v6.2.0）。
3. **還需要嗎？** bridge 不需要 discard、也不需要 finishing 清理 worktree；它需要的只是「最後一步交給 finishing 讓使用者選整合方式」，上游原生完全提供，而且多了「整合前重跑測試」「確認 base branch」（第 46–51 行）。
4. **分類：(a)** 文件更正。
5. **建議與成本**：README 中英第 423 行改為「重跑測試 → 給 merge／PR／keep 選項（discard 只在明確要求時）→ merge，或經明確要求並打字確認的 discard，才依 worktree 位置清理（只清 `.worktrees/`／`worktrees/` 下的，其他由 host 擁有、不動）；PR／keep 保留」。可與 S7 同一個直接 commit。另注意：使用者在 finishing 選「merge locally」時不會有 PR，而 bridge 寫「PR is the LAST step」「The branch's PR diff MUST contain …」——是否要把「PR」改寫成「整合（merge 或 PR）」屬措辭精確度問題，順手處理即可【建議，非必要】。驗證：第三步跑到 finishing 時記下實際選單。
6. **沒查的**：detached HEAD（原生 worktree 工具可能產生）下 bridge 流程的實際表現【未查證】。

### S13 — executing-plans 不派獨立審查、不提 TDD（確認現況，不重新分析）

- **現況**：`fix-executing-plans-rationale` 已於 2026-10-06 archive（verify.md 第 418 行 `⚠️ PASS WITH WARNINGS`；工作地圖 `task-20261002-executing-plans-rationale` = DONE）。現行文字都已改成「沒有每個 task 的審查；最後一次全分支審查在沒有 subagent 工具時由作者自審」：`schema.yaml` description（約第 8–13 行）與 apply step 2 末段（約第 1795–1806 行）、README § Seven touchpoints 的「No `executing-plans` fallback」框（約第 312 行）、§ Six design touches #4（約第 462 行）、§ Fallback strategy（約第 697 行）、repo `CLAUDE.md` 紅旗段 executing-plans 那條。README 兩處連結已指向固定標籤 `v6.4.1`。living spec `openspec/specs/tdd-claim-accuracy/spec.md`（約第 100–101 行）明文禁止舊說法回來。
- **上游原文仍支持**：[v6.4.1 executing-plans/SKILL.md](https://github.com/obra/superpowers/blob/v6.4.1/skills/executing-plans/SKILL.md) 第 8–10 行「no reviewer per task. One fresh-context review of the whole branch at the end」、第 149 行要求載入 TDD、第 253–255 行「Without a subagent tool: … perform that review yourself」。6.4.2 相同。
- **剩下的**：2026-08-26 紀錄列「✅ Still true — 0 matches」（README 約第 595 行）是帶日期的歷史紀錄，已由 S13 列註明 supersede，不改。「設計說明只寫理由、版本事實寫進 Re-verification log」的分離，以及紅旗改寫成能力／證據／降級語言，屬 `task-20260901-claudemd-governance-rewrite`（TODO）。
- **分類：(d)**。

### S14 — 上游在有 subagent 時一律導向 SDD

1. **Bridge 契約**：原本在 `schema.yaml` 與 README 拿「上游自己也這樣建議」當拒用 executing-plans 的理由之一。**現況**：該說法已被 `fix-executing-plans-rationale` 移除——它的 plan.md 驗收條件明列「不含 upstream directs users to SDD whenever subagents are available 或等義句」（archive `plan.md` 第 30、36 行），living spec `tdd-claim-accuracy` 約第 100–101 行禁止「states that upstream directs users to subagent-driven-development whenever subagents exist」。全 repo grep `whenever subagent|directs users|一律導向` 在 `superpowers-bridge/` 只剩 README 中英第 637 行的 2026-10-02 紀錄列（歷史紀錄）。
2. **6.x 實際行為**：[v6.4.1 writing-plans/SKILL.md](https://github.com/obra/superpowers/blob/v6.4.1/skills/writing-plans/SKILL.md) Execution Handoff 讓使用者在 Subagent-driven 與 Native 之間選，並由 agent 推薦其一（第 167–191 行；6.4.2 該段相同，兩版 diff 不涉及此段）；SDD 的 When to Use 圖「Partner chose inline, or no subagent tool?」→ executing-plans（SDD SKILL.md 第 35–50 行）；executing-plans 第 60–64 行「Prefer superpowers:subagent-driven-development when … wants a review gate on every task」。
3. **還需要嗎？** 不需要——bridge 現在的拒用理由只靠「沒有每個 task 的審查＋無 subagent 時自審」這件事實（見 S13），不靠上游的建議。注意一個殘留的**互動**（不是宣稱問題）：apply step 2 直接呼叫 SDD，而 SDD 自己的 When to Use 圖在「使用者選了 inline」時會導向 executing-plans【推論：bridge 已明文不支援 executing-plans，apply 由 bridge 指定執行器，衝突風險低】。
4. **分類：(a)，只限 README 一句；其餘 (d)。** README § Re-verification log 的「Why the baseline stays at `v5.1.0`」段（中英約第 639 行）最後一句「S4, S5, S12 and S14 are still not aligned」是 v4 change 才補上的，寫的時候 S14 的宣稱句已在 10/06 移除——**這句對 S14 已不成立**（對 S12 也只剩 README 第 423 行的描述）。依該段既有慣例（「不回頭改 10/02 紀錄」，見 `fix-executing-plans-rationale/retrospective.md` 第 55 行），建議以**新增一行後續狀態**的方式更正，而不是改舊句。
5. **建議與成本**：與 S7、S12 同一個 README 直接 commit（中英兩份）。數行【估計】。驗證：grep README 確認新後續狀態列與舊列不矛盾。
6. **沒查的**：`task-20260901-claudemd-governance-rewrite` 若把紅旗改成「沒有 subagent 時允許自審但留降級紀錄」，executing-plans 就可能變成可接受的降級路徑——那是正式設計 §5 層級的產品決定，本文不評估。

### S17 — 安裝指令 `claude plugin install superpowers@claude-plugins-official`

1. **Bridge 契約**：README § Install Method 1 第 8 步（約第 32–33 行）；Compatibility 表 v4 列 Superpowers 欄 `v5.1.0`、`Baseline as of` = `pending`（約第 571–573 行），表下說明「The environment known to have been exercised by the PoC for this change is Superpowers `v6.4.1`」（約第 580 行）。
2. **實際**：官方 marketplace 仍把 superpowers 釘在 sha `5bf4e78…` = `v6.4.1`——本機快取與上游 `anthropics/claude-plugins-official` HEAD `b78ac49`（2026-10-07）一致（本 session 實查，補上 spike 的【未查證】）。上游最新 release 是 `v6.4.2`。`.github/workflows/version-check.yml` 的「Get latest Superpowers release」步驟取 `releases/latest` 的 `tag_name`（約第 33–39 行），與 README v4 列字串**完全相等**才算沒漂移（約第 111 行 `superpowersPinned !== superpowersLatest`）。obra 自己的 `superpowers-marketplace` 本機 clone 標示 `version: 6.3.0`、沒有 sha 釘選【未查證上游現況；本機 clone 可能過舊】。
3. **還需要嗎？** 安裝指令本身沒問題（指令能用、拿到的版本在 6.x）；問題在於「照 README 裝到的」（6.4.1）、「drift 檢查比的」（6.4.2）、「Compatibility 表宣告的」（5.1.0）三者不一致。
4. **分類：(a)**（README 加一句「此指令安裝的是官方 marketplace 釘住的版本，可能落後最新 release」）＋【決策點 D4】（見 §3.3）。
5. **建議與成本**：文件一句、可與 S7/S12/S14 同一 commit。版本選擇見 §3.3。
6. **沒查的**：官方 marketplace 之後何時跟進 6.4.2【未查證，屬外部事實】；`claude plugin install` 對已安裝舊版的升級行為。

### S18 — Re-verification log 引用的 v6.3.0 行號（SDD SKILL.md:223-229、415-419）

- README Re-verification log 2026-08-26 表第 4 列（約第 598 行）。實查 v6.3.0 SDD SKILL.md 第 223–229 行是「Batch small same-shape work」段、第 415–418 行是 park 的兩個條目——**引用對 v6.3.0 正確**。v6.4.1、v6.4.2 同一段落仍在第 223 行起與第 411（breaker 起始）／415 行起，**行號沒有移動**；spike 說「從 415-419 移到 411-420」是兩次取的區段起點不同，不是上游變動。
- **分類：(d)**。這是帶日期的 v6.3.0 紀錄，不需要改。README 第 387 行「upstream lets the controller park … after round 5 (see the re-verification table below)」在 6.4.1 仍成立（SDD 第 411–420 行）。

### （新）S19 — SDD 自己的終點是呼叫 finishing，與 bridge 的 verify → retro → archive → finishing 順序衝突

spike 的 18 項沒有列這條；依「看到就講」補上，請維護者決定要不要納入。

1. **Bridge 契約**：apply step 3–6 規定 SDD 執行完後依序 verify → retrospective → archive → finishing，且「This is the canonical opening sequence for the PR — do NOT reorder」（`schema.yaml` apply 約第 1808–1848 行）。apply step 2 告訴 executor 讀 plan.md、更新 tasks.md、在 worktree 內工作（約第 1754–1759 行），**沒有**說 SDD 收尾時不要呼叫 finishing。step 6 有部分保護：「If it doesn't (e.g., because retrospective or archive was skipped), STOP and complete those first」。
2. **上游**：v6.4.1 SDD 流程圖最後一格「Use superpowers:finishing-a-development-branch」（SDD SKILL.md 第 91、120 行）、§ Finish「Use superpowers:finishing-a-development-branch.」（第 487 行）、範例第 567 行。v5.1.0 也一樣（`git show v5.1.0:…` 第 66、85 行），**不是 6.x 新增**。另外 SDD 的 Setup 自己也會呼叫 using-git-worktrees（第 126–127 行），與 apply step 1 重複，但 worktree skill 的 Step 0 偵測會跳過重建，無害【推論】。
3. **還需要嗎？** 需要：finishing 若在 verify／retro／archive 前就跑，使用者可能直接選 merge 或開 PR，PR 內容就缺 bridge 要的完整 cycle。目前只靠 step 6 的事後 STOP。
4. **分類：(b)**——上游 SDD 原生已有完整收尾（最終全分支審查、Rulings 清單），bridge 只要在 apply step 2 加一句「SDD 到 Finish 時把 Rulings 清單交出、回到本 instruction 的 step 3，不在此時呼叫 finishing」。屬 instruction 散文，不觸發 major【推論，依 README § Versioning 判準】。
5. **【決策點 D5】要不要把這句併進 S4/S5 的 change？** 好處：同一次 schema 改動、同一次驗證；代價：那個 change 的範圍從 brainstorm 擴到 apply，審查面變大。另一選項是等第三步實跑看有沒有真的發生再決定（證據先於修正）。**建議**：先不修、列進第三步驗證必看項；實跑中若 SDD 在 verify 前叫了 finishing，再開小 change。
6. **沒查的**：歷次 dogfood（`loosen-plan` 等）有沒有實際發生「SDD 收尾直接進 finishing」——`2026-09-03-loosen-plan-execution.md` 第 145 行只說在那之前 worktree／finishing 從未被執行過，沒查之後的 ledger【未查證】。

---

## 3. 綜合

### 3.1 建議分組（2 個工作單位＋1 個驗證）

| 順序 | 工作單位 | 項目 | 三軌制路由 | 動 `schema.yaml`？ | 估計 |
|---|---|---|---|---|---|
| 1 | **直接 commit：README 上游行為描述更正**（中英兩份） | S7（第 380 行）、S12（第 423 行）、S14（第 639 行以 append 後續狀態更正）、S17（安裝指令一句說明）；可順帶 S5 的「writing-plans 終點 v5.1.0 就有」更正（append 到 Open drift 之後） | 文件 → 直接 commit；需過 `/codex-review-doc` | 否 | 小；與其他項獨立，可隨時做【估計】 |
| 2 | **opsx change：brainstorming 路徑對齊**（沿用 `task-20260826-fix-brainstorming-drift`） | S4、S5、S6；視 D3 帶上 apply step 1 措辭；視 D5 帶上 S19 | schema instruction → opsx change | 是（brainstorm／design instruction、`templates/brainstorm.md`；連動 README Open drift／Entry gates、adopter fragment 中英） | 中；不觸發 major 的前提是只改散文、不新增檢查【推論】 |
| 3 | **第三步：整體相容性驗證**（見 3.2） | 全部 | 驗證紀錄（PoC／dogfood 報告），結果再以文件更新 Compatibility 表 | 否 | 一個完整 cycle 以上【估計】 |

順序理由：1 與 2 互不依賴；2 必須在 3 之前（否則第三步驗到的是已知不成立的 brainstorm 描述）。S11、S13、S18 不需要工作；S13 的理由／證據分離留在 `task-20260901-claudemd-governance-rewrite`。

**工作地圖對照**：`task-20261007-superpowers-6x-rebaseline` 要求「S12、S14 開工第一步先查是否已有工作」——查得的結果：**S14** 的宣稱句已由 `task-20261002-executing-plans-rationale`（DONE）移除，只剩 README 一句總結過時；**S12** 沒有既存工作項（篩工作地圖含 `S12` 或 `finishing` 的紀錄，除本工作 `task-20261007-superpowers-6x-rebaseline` 自己外，只命中已完成的 `task-20260903-loosen-plan-close`，與 S12 無關）。登記與否由維護者決定。

### 3.2 第三步「整體相容性驗證」必須涵蓋什麼

v4 列的 `Baseline as of` 依 README 約第 580、657 行的定義，只有在「以該列版本重跑完整 cycle 並確認沒退化」後才能填日期；所以第三步至少要：

1. **環境紀錄**：`claude plugin list`（實際載入的 Superpowers 版本）、`openspec --version`（1.14.0）、平台。
2. **brainstorm**：一輪被分類為 architectural、一輪 bounded（S4／S5 路徑依賴，只跑一種不夠）；各自確認分類有說出口、產出寫進 `brainstorm.md`、`docs/superpowers/specs/` 無新檔（verify check 6）、brainstorm 後沒有呼叫 writing-plans、apply 前沒有實作 commit。入口至少含 `/opsx:new`＋逐步 `/opsx:continue`，以及 `/opsx:ff` 一次（ff 沒有逐 artifact 停頓）。
3. **design**：從上述 brainstorm.md 重組得出 Context／Goals／Decisions／Risks／Migration（S6）。
4. **apply step 1**：記錄 using-git-worktrees 走原生工具或 fallback、路徑與 branch 名、是否先問同意；確認 worktree 內有 bridge schema 副本與 change artifacts（2026-09-03 E1 的已知坑）。
5. **apply step 2**：plan 全用 canonical `## Task N.M —`；每個 entry `task-brief` 抽得到、最後一個 entry 範圍正確（S11 殘留）；每 task review／batch／最終全分支 review 有發生；TDD 標註與 RED/GREEN 證據照 tasks.md 契約；**SDD 收尾沒有在 verify 前呼叫 finishing**（S19）。
6. **verify／retrospective／archive**：checks 1–13 跑完；retrospective §4 skill 表如實；Windows 上 archive 走 repo CLAUDE.md 的 cp＋diff＋委派 rm。
7. **finishing**：實際選單（三選項）、選 PR 或 merge 時 worktree 的處置與 README 新描述一致（S7／S12）。
8. **負向一項（建議）**：PRECHECK 遇缺 skill 會 STOP（Layer 1）——成本低，可在拋棄式環境移除 skill 驗。

### 3.3 【決策點 D4】Compatibility 表 v4 列要釘哪個 Superpowers 版本

**為什麼現在要決定**：第三步要在哪個版本上跑，取決於最後要釘哪個字串；跑完再換版本等於白跑。

| 選項 | 好處 | 代價 |
|---|---|---|
| D4-1：釘 `v6.4.1`，第三步就在本機官方 marketplace 的 6.4.1 上跑 | 與 README 安裝指令實際裝到的一致（本 session 實查官方 marketplace 仍釘 6.4.1）；本 repo 歷次 dogfood 都在 6.4.1；符合「只對實際跑過的版本下宣告」 | `version-check.yml` 以字串相等比對 `releases/latest`（目前 `v6.4.2`），drift issue 會繼續開著，直到官方 marketplace 跟進且 bridge 再驗一次；README 已定義「drift 是常態、不是失敗」，可接受 |
| D4-2：改裝 6.4.2（`superpowers-marketplace` 或手動），第三步在 6.4.2 上跑，釘 `v6.4.2` | 與 drift 檢查一致，issue 可關；6.4.1→6.4.2 只差 writing-plans，而 bridge 不要求 writing-plans | 採用者照 README 指令裝到的是 6.4.1，宣告版本與實際安裝不同，需在 README 補說明或改安裝指令；obra marketplace 的實際版本行為【未查證】 |
| D4-3：在 6.4.1 跑、宣告 `v6.4.2`（理由：差異只在非必要 skill） | 一次驗證、issue 可關 | 宣告了沒跑過的版本，違反 README Re-verification log「Superpowers baseline is bumped only after a full cycle is re-run」（約第 588 行）；**不建議** |

**建議 D4-1**：理由是「宣告＝實際跑過＝使用者實際會裝到」三者一致，這正是 v4 列下方說明要守的東西；drift issue 開著是已知、已文件化的常態。等官方 marketplace 跟進後，再以 6.4.1→新版的 diff 決定要不要重跑。**我沒查的**：官方 marketplace 的更新節奏；`version-check.yml` 是否值得改成「比對官方 marketplace 釘選版」（那是 CI 設計題，不在本盤點範圍）。

### 3.4 決策點一覽

| 編號 | 問題 | 建議 |
|---|---|---|
| D1 | bridge change 裡怎麼對待上游三條路徑（強制 architectural／接受分類／不再依賴 skill） | B：接受分類、一律寫 brainstorm.md 後停下 |
| D2 | S4/S5 change 只改 instruction 散文（bundle 4.x，不 bump major），還是同時加 verify 檢查（major 5） | 只改散文；檢查等第三步證據不足時再議 |
| D3 | apply step 1 是否改成「建立或確認隔離工作區，使用者可拒絕」，並更正「untracked change 目錄由 worktree skill 負責」 | 改；commit 提醒只能寫成提示使用者 |
| D4 | v4 列釘哪個 Superpowers 版本 | `v6.4.1` |
| D5 | S19（SDD 收尾直叫 finishing）現在修，還是先列入第三步觀察 | 先觀察 |

### 3.5 整體沒查的

- 沒跑任何 skill、沒跑 `/opsx:*`；所有「agent 會不會照做」都只有本 repo n=3 的 dogfood 紀錄。
- 沒讀 6.4.1 SDD 的 `implementer-prompt.md`、`task-reviewer-prompt.md`、`re-review-prompt.md`、`scripts/review-package`、`scripts/sdd-workspace`（S8–S10 不在本文範圍；SDD workspace 預設寫在 `<repo-root>/.superpowers/sdd/…`（`task-brief` 第 6–7 行註解），與 verify check 5「worktree 無未 staged 檔」的互動【未查證】）。
- 沒逐行核對 `README.zh-TW.md`，只對照了本文引用的行。
- brainstorming 架構路徑「Commit the design document to git」（第 244 行）在 bridge 重導到 brainstorm.md 後是否會讓 agent 自行 commit change 目錄，與紅旗「instruction 不得主動 git commit」的關係【未查證】——這是上游行為，不是 bridge instruction，但第三步值得順便觀察。
- 上游 release notes 沒有重讀（spike 已讀 v6.0.0–v6.4.2）；本文改以 SKILL.md 原文與 v5.1.0／6.3.0 直接比對。

---

## 4. 維護者裁定（2026-10-08）

本節記錄 §3.4 決策點的裁定；§1–§3 保留為裁定前的分析，不改寫。裁定只決定方向，**本輪不改 `schema.yaml`**；需要動 schema 的部分在後續 S4／S5／S6／S19 change 正式實作。

| 編號 | 裁定 | 條件與理由 |
|---|---|---|
| D1 | **B**：接受上游三種分類；不論路徑，設計寫進 brainstorm.md 後停下 | 有條件：接受分類**不等於**接受各分類帶來的保障降低。第三步要確認 bounded 路徑仍保留 bridge 需要的決策紀錄、核可停頓點與交接資訊（Codex 文件審 🟡：上游 architectural 的「書面 spec 核可」「實作計畫審閱」兩個停頓點，bridge 目前沒有明文對應） |
| D2 | 只改 instruction 散文，不新增 verify 檢查、不升 schema major | 目前沒有證據需要為此新增檢查 |
| D3 | **有條件允許降級** | 依既有原則「降低強度的決定權在使用者；agent 可加嚴、可提出放寬建議，但不能自行降低最低要求」（`2026-10-06-verification-strategy-after-c1.md` 第 39 行：*cost-aware policy, not cost-decided-by-worker*）。落地為三種情形：① 正常情況優先使用隔離工作區；② 無法隔離時，agent 說明原因與風險、交使用者決定；③ 使用者同意原地進行時，明確記錄「本次沒有工作區隔離保障」。另立原則：若日後某類操作被契約要求強制隔離，不能只因使用者拒絕 worktree 就放行，須走允許的例外或停止——正式設計尚未把隔離列為 required assurance（§5 基線第 197 行只談能力不足時可退回較簡單的執行模式、並顯式標示失去的保證）；現行 schema 則仍有隔離指示（apply 開頭「set up an isolated workspace」、step 1「create an isolated git worktree」，約第 1712、1745 行；見本文 S7），與上游的原地 fallback 存在張力。D3 決定的是後續如何把允許條件明文化，尚未改變現行 schema。不新增隔離驗證系統，只寫清決策權限、允許條件與證據要求 |
| D4 | 以 `v6.4.1` 為第三步的驗證目標與 v4 列的宣告版本 | 宣告＝實際跑過＝使用者照 README 指令會裝到的版本；不為追最新版而追最新版。drift issue 因比對 `v6.4.2` 會持續開著，屬 README 已定義的常態 |
| D5 | **A：本輪就補明交接指示**（同日先裁 B「先觀察」，經討論改為 A） | 改判理由：兩套流程在同一交接點給 agent 不同的下一步——上游 SDD 指示整體審查後呼叫 finishing（6.4.1 SDD SKILL.md 流程圖末格與 § Finish），bridge 要求 SDD 結束後依序 verify → retrospective → archive → finishing（apply step 3–6）。今天 C′ 的執行選擇了 bridge 的順序，證明歧義存在，不證明 agent 常會跳步；但修正成本低（一段說明文字）、範圍明確，不需要等到發生「未驗收就 merge」才修。定位：**既有生命週期契約的控制權交接澄清**，不新增完成標準、不建 Completion Gate、不加狀態或驗證欄位；仍屬 instruction 層，不得宣稱已能防止所有提前 finishing |

### 4.1 S19 交接契約要點（供後續 change 實作）

1. SDD 必須完成所有實作、逐項審查、整體審查與 Rulings 交付——不得為了避開 finishing 而跳過 SDD 自己的整體審查。
2. SDD 完成後把控制權交還 bridge apply step 3，不在此時呼叫 `finishing-a-development-branch`。
3. 在 bridge verify 完成、且必要證據已妥善持久化之前，不得清理 SDD 工作區（`<repo-root>/.superpowers/sdd/<plan>/`）；若 retrospective 或 archive 仍需原始資料，延後到不再需要為止。「verify 完成」不是無條件刪除的訊號。
4. 需要保留的驗證證據，依既有證據契約存入可追溯、適合進版控的檔案（正式設計 §3.4：長證據須是 repo 內已 commit 的檔案；scratchpad、git-ignored、未追蹤檔不得作證據落點）。

併入 S4／S5／S6 的 change 時，S19 要在 proposal／tasks 中**明列為獨立的小範圍相容性修正**，讓審查者知道要看 apply 的交接指示，而不是夾帶在 brainstorming 修正裡。

### 4.2 第三步驗證的追加要求

在 §3.2 清單之外，第三步必須另外記錄：

- **D1**：使用者實際審閱／核可了寫出的 brainstorm.md 與 plan.md，之後才開始 apply（architectural 與 bounded 各一輪）。
- **D5**：SDD 結束時 agent 把控制權交還 bridge、未提前呼叫 finishing，且 SDD 工作區在 verify 完成、證據持久化之前未被清理。一輪成功只算一個樣本，不證明不會跳步。
- **D3**：apply step 1 走的是哪一種情形（隔離／無法隔離交使用者決定／使用者同意原地），以及對應紀錄是否留下。
