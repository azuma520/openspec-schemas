# issue #2 上游相容性 spike：OpenSpec 1.3.1 → 1.14.0、Superpowers v5.1.0 → v6.4.2

- 日期：2026-10-02
- 性質：研究 / 取事實（spike），不是實作；spike 階段沒有修改 `superpowers-bridge/`、README、`.github/`、`openspec/` 或任何既有檔案
- 精簡註記：本報告於 2026-10-02 依使用者裁定精簡 `raw/`（大部分原始輸出已移除，每一步在兩版的 exit code 與相同 / 不同判定記在 `raw/SUMMARY.md`），**結論沒有改變**
- 觸發：GitHub issue #2（weekly drift 檢查，[run 36840373547](https://github.com/azuma520/openspec-schemas/actions/runs/36840373547)）
- 範圍（使用者 2026-10-02 裁定）：兩邊一起看，但各自只驗 superpowers-bridge 真正依賴的部分；baseline 要不要提高由使用者決定
- 原始輸出：`raw/`（實驗腳本 `raw/run.sh`、`raw/extra-cases.sh`、fixture，以及機械摘要 `raw/SUMMARY.md`；重跑方式見 SUMMARY 的「版本與重現方式」）

---

## 摘要（先講結論）

| 上游 | 依賴項數 | 成立 | 有變化需評估 | 不成立 | 未查證 |
|---|---|---|---|---|---|
| OpenSpec CLI 1.14.0 | 24 | 16 | 8 | 0 | 0 |
| Superpowers v6.4.2 | 18 | 8 | 3 | 6 | 1 |

（各項的判定依據見第 2 節。O15 在 1.14.0 有實測，1.3.1 那邊沒對照到，判定時已計入「有變化需評估」。）

**OpenSpec：bridge 用到的 CLI 指令在 1.14.0 全部能跑，沒有任何一條壞掉。** schema validate、`openspec schemas`、new change、status、instructions、validate、show、archive 用同一份 fixture 在兩個版本各跑一次。四個 artifact 的 `instruction` 字串在兩版都是逐字原樣搬運（byte 相等），JSON 欄位只有新增、沒有刪除，archive 合併出來的 spec 只差空白行。

24 項的查證方法是混合的，不是 24 項都做了對稱的雙版實測：20 項（O1–O10、O13、O14、O17–O24）在兩版各實測一次對照；O15 只在 1.14.0 實測到（1.3.1 沒走到那項檢查）；O11、O12、O16 是讀原文查證（CHANGELOG、`init` 產生的 SKILL.md、原始碼註解）。instruction 的逐字比對只涵蓋 brainstorm、plan、verify、retrospective 四個 artifact；`apply.instruction` 只在 1.14.0 的 `state: ready` 確認逐字相同，1.3.1 對同一個 fixture 回的是 `all_done` 提示（見 O7、O9）。

需要評估的變化有三類：

1. **`- [~]`（延後任務）現在被 CLI 當成「未完成」**（1.13.1，#1773）。bridge 的 check 2 / check 7 把它定義成「不算未完成」，所以兩邊在同一個任務上的說法對不上：`openspec list` 顯示 2/3、`instructions apply` 把它畫成 `- [ ]`、archive 印出 incomplete 警告，而 1.14.0 的 `openspec-verify-change` skill 會把它列為 CRITICAL「Must fix before archive」。只有用到 `[~]` 的 change 才會遇到，本 repo 的 5 個 archived change 都沒用過。
2. **schema.yaml 裡幾句描述 1.3.1 行為的文字在 1.14.0 已經過時**：archive abort 時的 exit code、stderr 警告、「CLI 不提供 heading 文字」、同步過的 capability 的觀察例。check 13 的判準本身仍能正確下結論。
3. **只做到 plan 時，`openspec status` 會把下一步指向 `instructions verify`，不是 apply。** 這是 README 設計觸點 #6 那個已知時序限制，現在變得更顯眼，靠 verify 的 PRECHECK 擋住。

**Superpowers：有 6 條 bridge 的宣稱在 v6.4.2 不成立，其中 2 條是新出現的。**

- **新出現**：`executing-plans` 在 v6.4.1 重寫了，現在收尾會派一次全分支的獨立 review，也要求載入 TDD skill。bridge 在 schema.yaml、README（en + zh-TW）、repo CLAUDE.md 寫的「它不派任何獨立 reviewer、內文不提 TDD 和 code review」**已經不成立**。同時「上游在有 subagent 時一律導向 SDD」也不再是事實：現在 SDD 和 executing-plans 是在 plan 交接時讓使用者選。
- **已知但 README 沒記**：SDD 從 v6.0.0 起靠 `scripts/task-brief` 抽每個任務的內容，它只認 `## Task N` 這種標題，bridge 的 Plan Contract 用 `## 1.1 — 標題`，實測 exit 3。dogfood 時已經遇過、當時用 ruling 繞過，但 bridge README 沒寫。
- **已知、而且更嚴重了**：brainstorming 的 drift。v6.4.1 加了 HARD-GATE，bounded 路徑的終點是「直接實作、不寫 plan 文件」。
- **文件不準（影響小）**：finishing 的選單已經沒有 discard；worktree 的路徑描述也不精確。

**建議（細節見第 4 節，最後由你決定）：**
- OpenSpec 的 baseline 可以提到 1.14.0，定位是「CLI 層級的確認」，同時把 `[~]` 的差異寫進記錄。
- Superpowers 的 baseline 維持 v5.1.0。
- 「Known breaking changes」那一節不要動，上游的變化寫進 re-verification log。
- executing-plans 那條不成立的宣稱，要另開 opsx change 修正（它寫在 schema.yaml 裡）。

---

## 0. 方法與環境

| 項目 | 值 | 來源 |
|---|---|---|
| OpenSpec 基準 | 1.3.1（本機全域，`openspec --version`） | `raw/out-v1.3.1/00-version.out` |
| OpenSpec 新版 | 1.14.0（`npx -y @fission-ai/openspec@1.14.0`，沒有動全域安裝） | `raw/out-v1.14.0/00-version.out` |
| OpenSpec changelog | `CHANGELOG.md` @ tag `v1.14.0`（從 `git clone https://github.com/Fission-AI/OpenSpec` 取出），1.4.0–1.14.0 每一條都讀過 | 原文：<https://github.com/Fission-AI/OpenSpec/blob/v1.14.0/CHANGELOG.md> |
| Superpowers 基準 / 新版 | tag `v5.1.0` / `v6.4.2`（從 `git clone https://github.com/obra/superpowers` 用 `git archive` 取出 `skills/`） | 原文：`https://github.com/obra/superpowers/blob/v6.4.2/skills/...` |
| Superpowers 本機 | 啟用中的是 `superpowers@claude-plugins-official` **6.4.1**；`superpowers@superpowers-marketplace` 6.4.2 已下載但停用（`claude plugin list`）。本機快取的 6.4.2 與 git tag `v6.4.2` 抽查 4 個 SKILL.md 逐 byte 相同 | — |
| Superpowers release notes | `RELEASE-NOTES.md` @ `v6.4.2`，讀過 v6.0.0–v6.4.2 的每一節 | <https://github.com/obra/superpowers/blob/v6.4.2/RELEASE-NOTES.md> |
| v6.4.1 與 v6.4.2 的差別 | bridge 點名的 8 個 skill 中只有 `writing-plans` 有改（`git diff --stat v6.4.1 v6.4.2 -- skills`）。所以除了 S15，本報告對 6.4.2 的結論同樣適用於本機實際在用的 6.4.1 | — |

**OpenSpec 實驗做法**：在 scratch 目錄造一個測試專案，`openspec/schemas/` 放 bridge 的副本，`openspec/specs/auth/spec.md` 放一份帶 ID 的 main spec（3 條 requirement），再開一個 change `demo`，它的 delta 涵蓋 ADDED / MODIFIED / RENAMED / REMOVED 四種，`tasks.md` 含 `[x]`、`[~]` 和 TDD 紀錄，8 個 artifact 都有。同一支 `raw/run.sh` 分別用 1.3.1 和 1.14.0 跑（重跑步驟見 `raw/SUMMARY.md`；2026-10-02 修審查意見時已把腳本改成可攜式，並在新的 scratch 目錄重跑確認），每條指令的 stdout、stderr、exit code 分開存檔再比對。另外加跑幾個情境：archive 衝突導致 abort、ADDED 已經事先同步過、level-3 的 scenario、只做到 plan 的狀態、`openspec init --tools claude` 產生的 skill、拿本 repo 的 `openspec/` 複本跑 validate、`validate --archived`（這幾個情境的指令重建在 `raw/extra-cases.sh`）。實驗前先備份全域設定 `%APPDATA%\openspec\config.json`，跑完用 `cmp` 確認**沒有被改動**。

**Superpowers 驗證做法**：只讀原文（SKILL.md、scripts、release notes），沒有實際跑任何 skill。唯一的例外是 S11：直接執行 SDD 的 `scripts/task-brief`，餵它 fixture 的 `plan.md`。

**怎麼確保依賴清單沒有漏（窮盡方法）**：
1. 全文讀過：`schema.yaml`（1749 行）、`README.md`（en，637 行）、`templates/plan.md`、`brainstorm.md`、`tasks.md`、`adopters/CLAUDE.md.fragment.md`（en），以及 `templates/verify.md` 的第 1–30 行和第 245–275 行。
2. 對整個 `superpowers-bridge/` 目錄（含 zh-TW 與所有 templates）用以下字串 grep，逐筆歸類：`superpowers:[a-z-]+`、八個 skill 的不帶前綴名稱與 `code-reviewer|implementer`、`openspec [a-z]+`、`/opsx:[a-z]+`、`openspec-[a-z-]+`、`docs/superpowers`。`templates/spec.md` 另外用 `Requirement|Scenario|ADDED|MODIFIED|REMOVED|RENAMED|FROM|TO:` grep；`retrospective.md` 用 `git |validate|archive` grep。
3. 已知沒有全文讀的部分：`README.zh-TW.md`（grep 顯示指令所在行號和 en 版相同，但沒有逐行核對譯文）、`templates/proposal.md` / `design.md` / `spec.md` / `retrospective.md`（只用 grep），以及 `templates/verify.md` 第 31–244 行。見第 5 節。

---

## 1. 依賴面清單

行號以 `superpowers-bridge/` 為根目錄（README 指 en 版）。zh-TW 版對應段落沒有逐行列出。

### 1a. OpenSpec 端

| ID | bridge 依賴的東西 | 出處 |
|---|---|---|
| O1 | schema 檔的欄位要被 CLI 接受：`name` / `version` / `description` / `artifacts[].{id,generates,description,template,instruction,requires}` / `apply.{requires,tracks,instruction}` | schema.yaml:1-3, 27-33, 62, 1610-1613 |
| O2 | 專案層的 schema 搜尋：把 bundle 複製到 `openspec/schemas/superpowers-bridge/`，`openspec schemas` 要列得出來 | README:27-29, 136 |
| O3 | `openspec schema validate superpowers-bridge` | README:28, 49, 70, 96 |
| O4 | `openspec new change <name> --schema superpowers-bridge`（以及它寫出的 `.openspec.yaml`） | README:156, 339, 432 |
| O5 | `openspec status --change <name> --json` | README:440 |
| O6 | `openspec instructions <artifact>` 把 schema 的 `instruction` **原樣**交給 agent（整個整合都建在這上面） | README:12, 452-454 |
| O7 | apply 的閘門 `apply.requires: [plan]`，以及 `instructions apply` 交付 `apply.instruction` | schema.yaml:1610-1613；README:212 |
| O8 | `tracks: tasks.md` 的 checkbox 進度計算，`- [ ]` / `- [x]` 的語意 | schema.yaml:189-191, 1612；README:615 |
| O9 | `- [~]` = 延後任務，不算未完成（check 2、check 7） | schema.yaml:490-497, 535-585 |
| O10 | `openspec init --tools claude` 產生 `/opsx:*` 指令與 `openspec-*` skill（new / continue / ff / propose / apply / verify / archive） | README:330-349, 429-438；fragment:14-16 |
| O11 | continue / ff / propose 以 schema 的 `instruction` 為準；instruction 指定要呼叫某個 skill 時就去呼叫 | README:142, 454 |
| O12 | verify artifact 呼叫 `openspec-verify-change` skill，然後跑 13 項 check、寫 verify.md | schema.yaml:473-474, 1432-1434, 1709-1712；templates/verify.md:3 |
| O13 | `openspec validate --all --json` 的每個 item 有 `"valid": true` | schema.yaml:485-488；templates/verify.md:13-15；README:395, 442 |
| O14 | delta spec 格式：四種 `## … Requirements` 區段、`### Requirement:`、`#### Scenario:`、RENAMED 用 `- FROM:` / `- TO:` 加反引號；帶 ID 的 heading 要能被解析 | schema.yaml:132-176, 970-984；templates/spec.md:5-23, 27-91 |
| O15 | 宣稱「scenario 用 level-3 或 bullet 會 silent fail（不報錯直接失效）」 | schema.yaml:175；templates/spec.md:12 |
| O16 | 宣稱「archive 套用順序是 RENAMED → REMOVED → MODIFIED → ADDED」 | templates/spec.md:87 |
| O17 | `openspec archive <change> -y`：把 delta 同步進 main spec，並把 change 搬到 `archive/YYYY-MM-DD-<name>/` | schema.yaml:1726-1737；README:417-419 |
| O18 | check 13.B 的 archive preview：成功要同時滿足三個條件，並宣稱「1.3.1 abort 時仍回 exit 0」 | schema.yaml:1001-1019 |
| O19 | check 13.B 對「已同步過的 capability」舉的觀察例（已套用的 ADDED / RENAMED 會讓 preview abort） | schema.yaml:1078-1082 |
| O20 | `openspec show <cap> --type spec --json` 的 `requirementCount` 與 `requirements[].scenarios`；宣稱「CLI 不給 heading 文字，只能照位置配對」 | schema.yaml:1225-1236, 1292-1296 |
| O21 | `openspec show <change> --json --deltas-only` 的 `deltas[].spec/operation/requirement.scenarios/rename.from/rename.to`；1.3.1 會在 stderr 印警告 | schema.yaml:1215-1221, 1241-1263 |
| O22 | `openspec list`、`openspec schemas`（給使用者自查用） | README:439-441, 598 |
| O23 | `openspec init` | README:25 |
| O24 | artifact 圖的時序：verify / retrospective 在圖上 `requires` plan / verify，實際上要等 apply 之後才產出（設計觸點 #6） | schema.yaml:476-480, 1472-1476；README:291-294, 473-475 |

### 1b. Superpowers 端

| ID | bridge 依賴的東西 | 出處 |
|---|---|---|
| S1 | 被點名的 8 個 skill 存在：brainstorming、writing-plans、using-git-worktrees、subagent-driven-development、finishing-a-development-branch、test-driven-development、requesting-code-review、executing-plans | schema.yaml:5-7, 40, 359, 1622-1630, 1697；README:296-310；templates/retrospective.md:55-61 |
| S2 | Layer-1 PRECHECK：`superpowers:<name>` 會出現在 agent 的可用 skill 清單（plugin 名稱是 `superpowers`） | schema.yaml:33-38, 1616-1636；README:450 |
| S3 | brainstorming 預設寫到 `docs/superpowers/specs/`（這是重導的對象，也是 check 6 偵測外漏的依據） | schema.yaml:42-44, 515-533；README:125, 170, 189, 316-318；fragment:13, 29, 41 |
| S4 | brainstorming 走五個步驟（探索 → 一次問一題 → 2-3 個方案 → 分段報設計 → 輸出） | schema.yaml:56-61 |
| S5 | brainstorming 結束後可以接 bridge 的 proposal → design → specs → tasks | README:570（已知 drift） |
| S6 | brainstorming 的產出通常是 decision log | schema.yaml:45-50；templates/brainstorm.md:2-6 |
| S7 | using-git-worktrees 會建 `.worktrees/<change-name>/`、開新 branch、跑 setup、確認測試基線 | README:380 |
| S8 | SDD 每個任務派一個新 subagent、讀 plan.md，小而同型的任務可以批次 | schema.yaml:1650-1661, 1691-1695；README:384-389 |
| S9 | SDD 的 code review 是結構性的：「dispatches superpowers:requesting-code-review」，round 5 之後可以 park | schema.yaml:1624, 1691-1695；README:305, 371, 387 |
| S10 | SDD 的 TDD 是條件式的（implementer prompt 寫 "if task says to"，有 TDD Evidence 欄位） | README:572 |
| S11 | SDD 能吃 bridge 的 plan.md（entry 的 key 用 `## 1.1 — 標題`） | schema.yaml:377-392, 1650-1661；templates/plan.md:3, 28-49 |
| S12 | finishing：先確認測試綠燈、給 merge / PR / keep / discard 四個選項、清理 worktree | README:423；templates/verify.md:269 |
| S13 | executing-plans 不派獨立 reviewer、內文不提 TDD 和 code review | schema.yaml:8-11, 1697-1700；README:312, 462, 563-564, 626；repo CLAUDE.md 紅旗段 |
| S14 | 上游在有 subagent 時一律導向 SDD | schema.yaml:1700-1702；README:312, 462 |
| S15 | writing-plans 只是可選的私人拆解輔助，它的產出是 micro-step | schema.yaml:356-361；README:301；fragment:42 |
| S16 | test-driven-development 存在，implementer 可以自己觸發 | README:304, 371 |
| S17 | 安裝指令 `claude plugin install superpowers@claude-plugins-official` | README:32-33, 50 |
| S18 | re-verification log 引用的 v6.3.0 行號（SDD SKILL.md:223-229、415-419） | README:567 |

---

## 2. 逐項比對

判定標記：`成立` / `不成立` / `有變化需評估` / `未查證`。「實測 `NN-…`」指 `raw/run.sh` 或 `raw/extra-cases.sh` 裡的步驟名稱，每一步在兩版的 exit code 和 stdout 比對都在 `raw/SUMMARY.md`。原始輸出已精簡：只有 SUMMARY 末表列出的檔案（`00-version`、`09b`、`14b`、`15-archive-preview`、`18-conflict`、`20-status-planonly`，以及 `raw/sdd-task-brief-probe.txt`）還保留原檔；其他步驟的原始輸出沒有保留（raw output not retained），結論以 SUMMARY 和本表為準，需要原檔可照 SUMMARY 重跑；「CL」指 OpenSpec CHANGELOG @ v1.14.0；「RN」指 Superpowers RELEASE-NOTES @ v6.4.2。

### 2a. OpenSpec 1.14.0

| ID | 判定 | 證據 |
|---|---|---|
| O1 | 成立 | 實測 `01-schema-validate`：兩版 exit 0，stdout 都是 `✓ Schema 'superpowers-bridge' is valid`。CL 1.13.1 #1868 新增「`apply.tracks` 跟任何 `generates` 不完全相同時給警告」，bridge 的 `tracks: tasks.md` 和 `generates: tasks.md` 相同，實測沒有警告 |
| O2 | 成立 | 實測 `02-schemas`：兩版都列出 `superpowers-bridge (project)`，artifact 順序一樣。（CL 1.7.0 #1475 開始解析 symlink 的 schema 目錄，這和 repo CLAUDE.md「junction 掃不到」的記錄有關，見第 5 節） |
| O3 | 成立 | 同 O1 |
| O4 | 成立（輸出格式有改） | 實測 `04-new-change`：兩版 exit 0，`.openspec.yaml` 內容相同（`schema: superpowers-bridge`）。1.14.0 把成功訊息改到 stdout，並多印一行 `Next: openspec status --change demo` |
| O5 | 成立 | 實測 `05/08-status`：JSON 欄位只有新增（`isPlanningComplete`、`nextSteps`、`artifacts[].requires`、`artifactPaths`、`actionContext`、`root` 等），沒有移除 |
| O6 | 成立 | 實測 `06/10/10b/10c`：brainstorm、plan、verify、retrospective 四個 artifact 的 `instruction` 欄位在兩版都和 schema.yaml 的原文逐字相同（Python 字串相等比對，verify 那份 51,876 字元） |
| O7 | 成立 | 實測 `07`：plan 不存在時兩版都回 `state: blocked`、`missingArtifacts: ["plan"]`，1.14.0 多給 `missingPrerequisites`。實測 `09`：1.14.0 的 `instruction` 欄位和 `apply.instruction` 原文完全相同（前後沒有附加文字） |
| O8 | 成立 | `[x]` 在兩版都算完成。1.14.0 每個 task 多了 `sourcePath` / `line`（CL 1.14.0 #2018） |
| O9 | **有變化需評估** | CL 1.13.1 #1773：「every other marker now reads as unfinished, across progress, the apply task list, archive's gate and validate's task-numbering check. The archive, bulk-archive and verify workflows now tell agents the same rule」。實測：`14b-list`（1.3.1 顯示 `✓ Complete`，1.14.0 顯示 `2/3 tasks`）；`09-instr-apply-json`（1.3.1 直接丟掉 `[~]` 那行，`state: all_done`；1.14.0 列出 `1.2 … done:false`，`state: ready`）；`09b`（1.14.0 把 `[~]` 畫成 `- [ ] 1.2`）；`15-archive-preview`（1.14.0 印出 `Warning: 1 incomplete task(s) found. Continuing due to --yes flag.`）。另見 O12 |
| O10 | 成立 | 實測 `20-init`：兩版 `init --tools claude` 都 exit 0，產生同一組 11 個 `.claude/skills/openspec-*` 與 `.claude/commands/opsx/*.md`（用本機全域 profile 的 11 個 workflow）。全域 config 前後 `cmp` 相同 |
| O11 | 成立（上游明文化了） | CL 1.7.0 #1405：「The templates now state that the `instruction` field is the authoritative guidance, and … invoke a skill when the instruction delegates artifact creation to one」。1.14.0 產生的 `openspec-continue-change/SKILL.md:86, 115-117` 有這段原文 |
| O12 | **有變化需評估** | 1.14.0 的 `openspec-verify-change/SKILL.md`（6.6 KB → 18 KB）改用 CLI 的 `progress`：「If `progress.remaining` is greater than 0: Add CRITICAL issue for each listed incomplete task」（:89-91），並列為「CRITICAL (Must fix before archive)」（:180-181）。1.3.1 版是直接解析 `- [ ]` / `- [x]`（1.3.1 SKILL.md:57），`[~]` 兩邊都不算。結果：用到 `[~]` 時，skill 報 CRITICAL，bridge 的 check 2 卻說不阻擋。另外，兩版這個 skill 都**不會**寫出 verify.md；verify.md 的格式完全由 bridge 的 instruction 決定（`templates/verify.md:3` 說「此檔案由 openspec-verify-change skill 產生」不精確，這點兩版都一樣） |
| O13 | 成立 | 實測 `11-validate-all`：兩版的 items、`valid`、summary 形狀相同，1.14.0 多一個 `root` |
| O14 | 成立（驗證變嚴，方向相容） | 實測 `12/13/15`：兩版解析出的 delta 數量、每條 requirement 的 scenario 數都相同；RENAMED 的 `from/to` 也相同。CL 裡變嚴的幾條：1.13.1 #1806（FROM/TO 配不成對 → ERROR）、#1858（只有標題沒有內文的 scenario → 拒絕）、#1864（只差大小寫或空白的同名 requirement → 拒絕）、1.8.0 #1482（MODIFIED 漏掉 scenario → validate 就擋）。這些都和 bridge 的寫法規則一致 |
| O15 | **有變化需評估** | 實測 `19-h3-scenario`（1.14.0）：ADDED requirement 底下用 `### Scenario:` → INFO「is not a "### Requirement:" header and is ignored」，加上 ERROR「must include at least one scenario」，exit 1。也就是**不是 silent**（CL 1.6.0 #1281、1.7.0 #1521）。1.3.1 沒對照到：同一個測試在 1.3.1 回 `Unknown item 'h3'`（1.3.1 要求 change 有 proposal.md 才查得到，CL 1.7.0 #1433），所以 1.3.1 下的行為**未查證** |
| O16 | 成立 | 原始碼註解：`src/core/specs-apply.ts:244`（v1.3.1）與 `:439`（v1.14.0）都寫「Apply operations in order: RENAMED → REMOVED → MODIFIED → ADDED」 |
| O17 | 成立 | 實測 `15/15b/15c`：兩版都 exit 0，都搬到 `archive/2026-10-02-demo`，`+1 ~1 -1 →1` 相同。合併出的 spec 只差三行空白（CL 1.9.0 #1640 / #1528 調整空行），requirement 順序相同 |
| O18 | **有變化需評估**（判準仍正確） | CL 1.6.0 #1311：human mode 下 archive 被擋時改回 `process.exitCode = 1`。實測 `18-conflict`：同樣是「ADDED failed … already exists / Aborted. No files were changed.」，1.3.1 exit 0，1.14.0 exit 1。另外 1.14.0 在 abort 時會留下空的 `openspec/changes/archive/`（實測 `16b`、`18`），但三條件判準的第 3 條要的是 `archive/<date>-<change>/`，所以仍判定失敗。schema.yaml:1016-1019「exit 0」那句是 1.3.1 才對的描述 |
| O19 | **有變化需評估**（判準不受影響） | CL 1.7.0 #1376 / #1386：已同步過、內容相同的 ADDED，或已改名過的 RENAMED，改成「什麼都不做」。實測 `18-synced`：事先把 ADDED 原文貼進 main spec 後，1.3.1 abort（`already exists`，exit 0），1.14.0 **archive 成功**（`+ 0, ~ 1, - 1, → 1`）。schema.yaml:1078-1082 自己就說那只是「Observed examples only, never a rule」，而 SYNCED CAPABILITY 判成 UNDETERMINABLE 的規則不看 preview 結果，所以判準不受影響，只是例子在 1.14.0 已經不對 |
| O20 | 欄位成立；「不給 heading 文字」那句**有變化需評估** | 實測 `13/15d/17c`：`requirementCount` 和每條的 scenario 數兩版相同（含本 repo `contract-identity` 的 8 條 / [5,4,6,6,2,4,3,5]）。1.14.0 在 requirement 和 scenario 上多了 `name`（例：`REQ-2 Access token expiry`、`REQ-1-S2 Lockout after five failures`）。來源：CL 1.14.0 #1972。schema.yaml:1235-1236、1292-1296 的「CLI emits no heading text」在 1.14.0 已經不成立。這是個機會：可以改成按名稱配對 |
| O21 | 欄位成立；stderr 那句**有變化需評估** | 實測 `12-show-deltas`：`deltas[].spec/operation/requirement.scenarios/rename.from/to` 兩版都有，1.14.0 多了 `name`。1.3.1 的 stderr 有 `Warning: Ignoring flags not applicable to change: scenarios`，1.14.0 的 stderr 是空的（CL 1.7.0 #1437）。CL 1.13.1 #1856 把這個指令改成用和 archive 同一套解析器；fixture 上兩版輸出的數量一致。schema 要求「只讀 stdout」，在 1.14.0 仍然安全 |
| O22 | 成立 | 實測 `14/14b`（list 對 `[~]` 的顯示見 O9）、`02/03` |
| O23 | 成立 | 實測 `20-init` exit 0 |
| O24 | **有變化需評估**（已知限制變得更顯眼） | 實測 `20-status-planonly`：只做到 plan、verify / retrospective 還沒寫時，1.14.0 的 `status` 結尾印 `Next: openspec instructions verify --change "demo" --json`，`nextSteps` 是同一句，`isPlanningComplete: false`；1.3.1 沒有這行建議。來源：CL 1.13.1 #1786（Next 行）、1.8.0（`isPlanningComplete`）。照著 CLI 建議走的 agent 會被引去先寫 verify.md，目前靠 verify 的 PRECHECK（commit 數 > 0、`[x]` 數 > 0）擋住，這正是 README 設計觸點 #6 的緩解方式 |

另外，拿本 repo 的 `openspec/` 複本跑 `17-repo-validate-all`：兩版都 5/5 通過，只有 INFO 訊息（「>500 字元」）的措辭變了。1.14.0 的 `validate --archived`：5 個 archived change 全過（本 repo 沒有用過 `[~]`）。

### 2b. Superpowers v6.4.2

| ID | 判定 | 證據 |
|---|---|---|
| S1 | 成立 | `git ls-tree v6.4.2 skills/`：8 個都在，另外新增了 `diagnosing-superpowers` |
| S2 | 成立 | v6.4.2 的 `.claude-plugin/plugin.json` 裡 `"name": "superpowers"`。本 session（6.4.1）的可用 skill 清單裡看得到 `superpowers:brainstorming` 等名稱 |
| S3 | 成立 | v6.4.2 `brainstorming/SKILL.md:135`、`:241`：「save to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` and commit」，和 v5.1.0 的 :29 / :111 相同 |
| S4 | **不成立**（已知 drift，變得更深） | RN v6.3.0「Requests are classified as spike, bounded, or architectural」；RN v6.4.1「finds out why you want the thing before proposing features … ties your approval to the actual design and planning stages」。v6.4.2 SKILL.md:110-138：只有 Architectural 路徑有那五步；開頭還多了意圖確認（:14-35）和 HARD-GATE（:38-56） |
| S5 | **不成立** | v6.4.2 SKILL.md:184-188：「Architectural: the ONLY skill you invoke after brainstorming is writing-plans … Bounded: after approval, implementation proceeds directly … no plan document」。HARD-GATE :46-49：「Architectural: … reviews and approves the written spec, then reviews the written implementation plan and selects its execution method」。bounded 直接實作這條，v6.3.0 已經有（v6.3.0 SKILL.md:92）；README:570 只寫了「short in-chat answer and stops」，沒寫到「bounded 的終點是直接實作」 |
| S6 | 未查證 | 產出長什麼樣要實際跑才看得到，本 spike 沒跑 |
| S7 | **有變化需評估** | v6.4.2 `using-git-worktrees/SKILL.md`：優先用 harness 自己的 worktree 工具（:55、:164，例如 `EnterWorktree`）；路徑是 `path="$LOCATION/$BRANCH_NAME"`（:94），不一定是 change 名稱；已經在 linked worktree 裡就跳過不建（:33）；setup 和基線測試仍在（:102-132）。v6.0.0 起拿掉了全域目錄 `~/.config/superpowers/worktrees/`（RN v6.0.0；v5.1.0 SKILL.md:79、:106 還有） |
| S8 | 成立 | v6.4.2 SDD SKILL.md:223-229「Batch small same-shape work … send the whole batch to a single subagent」；每個任務的 implementer dispatch 在 :246-275 |
| S9 | 成立（措辭可以更精確） | 每個任務的 review 用 SDD 自己的 `task-reviewer-prompt.md`（RN v6.0.0「The two per-task reviewer prompts became one」）；最後的全分支 review 用 requesting-code-review 的 `code-reviewer.md`（SKILL.md:88、:448-454）。round 5 之後 park 在 :411-420。「dispatches superpowers:requesting-code-review」這句字面上只對最後那次 review 成立；v5.1.0 也是把它當 reviewer 範本（v5.1.0 SKILL.md:272） |
| S10 | 成立 | v6.4.2 `implementer-prompt.md:36`「Write tests (following TDD if task says to)」、`:113`、`:133-135`「TDD Evidence (if TDD was required for this task)」 |
| S11 | **不成立**（相容缺口，v6.0.0 就有） | SDD SKILL.md:251-252 要求「run this skill's `bash scripts/task-brief PLAN_FILE N`」；`scripts/task-brief:30-36` 只認 `^#+[ \t]+Task[ \t]+N`。實測 `raw/sdd-task-brief-probe.txt`：拿 fixture plan.md（`## 1.1 — …`）跑，結果 `task 1 not found … (no heading matching 'Task 1')`，exit=3。v5.1.0 沒有 scripts 目錄（RN v6.0.0 才加）。dogfood 時已經遇過：`docs/superpowers/retrospectives/2026-09-03-loosen-plan-execution.md:158`，以及 `…-sdd-reports/progress.md:59`（Ruling：改用等效的抽取方式）。bridge 的 README 和 schema 都沒記這件事 |
| S12 | **不成立**（文件不準） | v6.4.2 `finishing-a-development-branch/SKILL.md:55-62`：只給 3 個選項（merge / PR / keep）；discard 只有在使用者明確要求時才做（:78-81、:132-143；RN v6.2.0）。PR 那個選項會保留 worktree（:126）。v5.1.0 :73-76 當時是 4 個選項 |
| S13 | **不成立**（新出現） | RN v6.4.1「`executing-plans` is rebuilt as Native execution … then dispatches one fresh whole-branch review on the most capable model」。v6.4.2 SKILL.md:8-10「One fresh-context review of the whole branch at the end」；:149「REQUIRED SUB-SKILL: load superpowers:test-driven-development」；:240-243 用 requesting-code-review 的 code-reviewer.md 派 reviewer。`grep -c`：test-driven-development / code-review 的出現次數 v5.1.0 = 0/0、v6.3.0 = 0/0、v6.4.1 = 2/4、v6.4.2 = 2/4。（另外仍然成立的一點：它**沒有每個任務的 reviewer**，:8-9「no reviewer per task」） |
| S14 | **不成立**（新出現） | v6.4.2 SDD SKILL.md:39-49 的決策圖：「Partner chose inline, or no subagent tool?」→ yes 就走 executing-plans。executing-plans :60-64：「Prefer superpowers:subagent-driven-development when your human partner wants a review gate on every task, or when the plan is long」。RN v6.4.1：「The plan handoff offers two approaches, Subagent-driven and Native … recommends one」 |
| S15 | 成立 | 這個 skill 還在。RN v6.4.2 把 plan 改成「records decisions, not a transcript of the code」，step 是「one action with a checkable result」，仍然是逐步的計畫。bridge 不依賴它的產出 |
| S16 | 成立 | `skills/test-driven-development/SKILL.md` 存在 |
| S17 | **有變化需評估** | 本機 `marketplaces/claude-plugins-official/.claude-plugin/marketplace.json` 對 superpowers 釘的 `sha 5bf4e78…`，`git describe` 對應到 `v6.4.1`。也就是照 README 的指令安裝，在本機拿到的是 6.4.1，不是 drift 檢查拿來比的 v6.4.2。官方 marketplace 上游現在釘哪一版：**未查證**（本機的 marketplace clone 可能是舊的） |
| S18 | 有變化（影響小） | v6.4.2 的 batch 段仍在 SKILL.md:223-229；park 段從 415-419 移到 411-420 |

---

## 3. 破壞性變更與風險清單

依我判斷的影響排序。「影響處」指 bridge 裡要跟著評估的位置。

| # | 變更 | 上游版本 | 影響處 | 嚴重度與理由 |
|---|---|---|---|---|
| R1 | brainstorming 分三條路徑 + HARD-GATE；bounded 的終點是直接實作、不寫 plan 文件；architectural 的終點只能是 writing-plans（S4、S5） | Superpowers ≥ v6.3.0，v6.4.1 加深 | schema.yaml:40-61（brainstorm instruction）；README:565-576（已知 drift）；README:296-300 | **高**。這是 bridge 的入口 artifact。agent 可能在寫 brainstorm artifact 的途中就開始實作（bounded），或被要求去跑 writing-plans 並選執行方式（architectural）。目前在 README 記為 open drift，但「bounded 直接實作」和 v6.4.1 的 HARD-GATE 沒記到 |
| R2 | executing-plans 重寫，收尾會派獨立 review，也要求 TDD（S13、S14） | Superpowers ≥ v6.4.1 | schema.yaml:8-11、1697-1707；README:310-312、391、460-462、563-564（log 裡「✅ Still true — 0 matches」那列）、626；README.zh-TW 對應段；repo CLAUDE.md「修 schema 時的紅旗」的 executing-plans 那條 | **中高**。這是 bridge 排除 executing-plans 的理由，而理由本身已經不成立。結論（不接受它當 fallback）可能還站得住，因為它仍然沒有每個任務的 reviewer，但理由要重寫。理由一旦在 schema.yaml 裡改字，就屬於 schema 改動，要走 opsx change |
| R3 | SDD 的 `task-brief` 認不得 Plan Contract 的標題（S11） | Superpowers ≥ v6.0.0 | schema.yaml:377-392（entry 的標題格式）、1650-1661（apply step 2）；templates/plan.md:3、28-49 | **中**。不會讓整個流程失敗（dogfood 時 controller 用 ruling 自己繞過去），但要靠 controller 臨場應變，而且 bridge 的文件沒寫，換一個 agent 不一定會繞 |
| R4 | `[~]` 被 CLI 當成未完成（O9、O12） | OpenSpec ≥ 1.13.1 | schema.yaml:490-497（check 2）、535-585（check 7）、473-474（呼叫 verify skill）、1726-1729（archive -y） | **中**，只有用到 `[~]` 的 change 會遇到。agent 會同時看到「CRITICAL：先修再 archive」（OpenSpec 的 skill）和「不阻擋」（bridge 的 check 2）兩種說法；`openspec list` 和 apply 的任務清單都把延後任務當成還沒做，apply 時 agent 可能去實作被延後的任務。`archive -y` 仍會繼續，不加 `-y` 在非互動環境下會怎樣：**未實測** |
| R5 | 只做到 plan 時，`status` 的 Next 指向 verify（O24） | OpenSpec ≥ 1.13.1 | README:291-294、473-475（設計觸點 #6）；schema.yaml:459-471（verify PRECHECK） | **低到中**。已知的時序錯位，現在 CLI 會主動建議錯的順序。PRECHECK 仍然擋得住 |
| R6 | check 13 裡描述 1.3.1 行為的句子過時（O18–O21） | OpenSpec ≥ 1.6.0 / 1.7.0 / 1.14.0 | schema.yaml:1016-1019、1078-1082、1215-1221、1235-1236、1292-1296 | **低**。判準仍正確（實測確認）；只是文字描述的版本行為不對，且有機會改成按 `name` 配對 |
| R7 | 幾處文件不準（S7、S9、S12、O15、O12 的 verify.md 註記） | 多個版本 | README:380（worktree 路徑）、423（finishing 選項）、305 / 371（dispatch 的措辭）；schema.yaml:175 與 templates/spec.md:12（silent fail）；templates/verify.md:3 | **低**。不影響執行，只影響讀者對上游行為的理解 |
| R8 | 安裝指令拿到的版本和 drift 檢查比的版本不同（S17） | — | README:32-33、50 | **低**，資訊性。drift 檢查比的是 GitHub 最新 release，使用者照 README 裝到的是官方 marketplace 釘住的版本 |

**沒有發現**：OpenSpec 端任何讓 bridge 原本能跑的指令改成會失敗的變更（24 項沒有一項不成立），也沒有任何一條 instruction 搬運被改寫。

---

## 4. 給使用者的決策點

以下三個決定都屬於你：要不要把「這個版本可以用」寫成公開宣告，以及要不要另外投入一個 change。我附上事實和建議，不替你決定，也沒有動 README。

### 決策 A：README 釘的 OpenSpec baseline 要不要從 1.3.1 提到 1.14.0

**為什麼現在要決定**：drift issue #2 的 OpenSpec 那半邊只等這個決定；CI 每週都已經用 1.14.0 跑過 validate。

| 選項 | 好處 | 代價 |
|---|---|---|
| A1：提到 1.14.0，定位成「CLI 層級的確認」（比照 v2 / v3 那兩列的寫法），同時在 re-verification log 加一筆，寫明 O9 / O12（`[~]`）、O18–O21、O24 的差異 | 釘住的版本和使用者實際裝到的版本一致（`npm i -g` 會拿到最新版）；這次的實測支持「CLI 指令面沒有壞」；issue 的 OpenSpec 那半邊可以關 | `[~]` 的衝突沒有解決，只是記錄下來；「baseline」要寫清楚只代表 CLI 層級確認，不代表跑過完整 prompt 流程 |
| A2：先開一個 opsx change 處理 `[~]` 的語意（例如 check 2 / 7 承認 CLI 把它算成未完成，或改用別的延後標記），也一起修 check 13 的過時描述，做完再提 baseline | baseline 的宣告不帶已知衝突 | 要多一輪 change 的工作量；在那之前 baseline 停在 1.3.1，和實際安裝版本脫節 |
| A3：維持 1.3.1，只在 re-verification log 記錄這次檢查（比照目前 Superpowers v6.3.0 的做法） | 不做任何新宣告 | issue 的 OpenSpec 半邊會繼續被每週 drift 檢查標成漂移；新使用者裝到的是 1.14.0，README 卻寫 1.3.1 |

**建議 A1。** 理由：本 spike 用同一份 fixture 跑過 bridge 用到的全部 CLI 指令，沒有一條不成立；`[~]` 是選用寫法（本 repo 5 個 archived change 都沒用過），風險侷限在用到它的 change，而且 A1 會把它寫成「已知行為差異」，不會藏起來。`[~]` 要不要調整 schema，可以之後另開 change 再決定（那就是 A2 的內容，和 A1 不衝突）。

### 決策 B：README 釘的 Superpowers baseline 要不要從 v5.1.0 往上提

**為什麼現在要決定**：drift issue #2 的另一半；而且這次發現了一條新的「不成立」（R2）。

| 選項 | 好處 | 代價 |
|---|---|---|
| B1：維持 v5.1.0，在 re-verification log 加一筆「v6.4.2 局部複查」，列出 S4、S5、S11、S12、S13、S14 | 和 README:576 的既定立場一致（「brainstorming drift 修好之前不提 baseline」）；不宣告沒驗過的東西 | issue 的 Superpowers 半邊會一直開著；README 的幾處文字（R2、R7）在修正之前仍然是錯的 |
| B2：提到 v6.4.1（本機官方 marketplace 實際裝到的版本，也是 requirement-scenario-identity 那個 change 的 apply 階段實際跑過的版本） | 和使用者實際裝到的版本一致 | R1 / R2 / R3 都還在，提了等於替已知不成立的宣稱背書 |
| B3：提到 v6.4.2 | 和 drift 檢查比的版本一致 | 同 B2，而且這個版本沒有在任何 bridge 流程裡實際跑過 |

**建議 B1**，並把 R2（executing-plans 理由錯了）和 R3（task-brief 缺口）登記成後續工作。理由：S4 / S5 / S13 / S14 都在 bridge 的規範文字裡，提 baseline 等於重新宣告它們成立；這幾條要修，都需要動 schema.yaml 的 instruction 文字，照 repo 的規矩要走 opsx change。

**連帶的子決定**（屬於「值不值得做」，留給你）：
- B-i：R2 是不是只修理由的文字（「它沒有每個任務的 reviewer」），還是要重新評估「是否接受 executing-plans 當 fallback」這個設計決定本身？後者是設計變更，不只是修錯。
- B-ii：R3 要把這件事寫進文件（README 加一條已知摩擦），還是改 Plan Contract 的標題格式去配合 `task-brief`（例如 `## Task 1.1 — …`）？後者會改到 check 12 的 key 讀法，很可能要 bump schema major。我沒有實測 `task-brief` 能不能處理 `1.1` 這種有小數點的編號：它的 regex 是 `Task[ \t]+N([^0-9]|$)`，N 帶 `.` 時會被 awk 當成 regex 的萬用字元，**沒有實測**。

### 決策 C：README 的 Compatibility 表和「Known breaking changes」要怎麼動

**事實**：README:590-596 對「Known breaking changes」的定義是 bridge **自己的 schema major 變動**（v1→v2、v2→v3），而且 :596 說之後的 schema major bump 都會記在這裡；這次沒有任何 bridge schema 的改動。issue #2 的 checklist 寫的是「If breaking, add an entry under Known breaking changes」。

| 選項 | 好處 | 代價 |
|---|---|---|
| C1：「Known breaking changes」不動；上游的行為變化寫進 re-verification log；Compatibility 表依決策 A / B 的結果改對應的欄位和日期 | 和那一節自己的定義一致，不會把上游的變化和 bridge 的 migration guide 混在一起 | issue checklist 那一格要另外註明「上游變化記在 re-verification log」 |
| C2：在「Known breaking changes」加一筆上游造成的變化（例如「OpenSpec ≥ 1.13.1：`[~]` 算未完成」） | 讀者在同一處就能看到 | 和 :596 的定義衝突；那一節原本代表「要做 migration」，混進去會讓讀者誤以為要遷移 |

**建議 C1。** 補充兩點（照 repo CLAUDE.md 的「跨檔耦合」表）：
1. Compatibility 表的形狀要維持「第一欄 `v3`、兩個版本各自包在單一 backtick 裡」，否則 `version-check.yml` 的 grep 會讓 CI 直接失敗。
2. 動到 README 的 Compatibility 段時，`README.zh-TW.md` 要一起改。

---

## 5. 沒查的是什麼

- **沒跑完整的 prompt 流程**：沒有讓 agent 用 1.14.0 或 Superpowers v6.4.x 從 `/opsx:new` 一路走到 archive。prompt 層的項目（S4–S7、S12–S14、O11、O12）都是讀原文判斷的；O6 只證明 instruction 字串有原樣交到 agent 手上，沒證明 agent 會照著做。
- **`/opsx:*` 指令只看了產生出來的檔案**，沒有實際被 agent 執行。
- **OpenSpec**：讀的是 tag `v1.14.0` 的 `CHANGELOG.md`，沒有另外讀 GitHub Releases 頁面，也沒有 diff 原始碼（只有 O16 用 `git grep` 看了一處原始碼註解）。沒測 `archive` 不加 `-y` 在非互動環境碰到未完成任務時的行為（CL 1.8.0 #1483 說會報錯並提示要加的旗標）。沒測 `--store` 相關路徑。只在 Windows（Git Bash + Node）上跑，沒測 macOS / Linux。O15 在 1.3.1 下的行為沒對照到。沒測 1.14.0 對 symlink / junction 安裝的 schema 的行為（repo CLAUDE.md 的「junction 掃不到」是 1.3.1 的結論；CL 1.7.0 #1475 說現在會解析 symlink 的 schema 目錄）。
- **CL 裡和 Windows archive 鎖有關的修正**（1.13.2 #1926 的 EPERM 搬移、#1769 的 `.openspec-archive.lock` 殘留）可能和 repo CLAUDE.md「archive 在 Windows 必定撞目錄鎖」有關（那條講的是 agent 自己 `mv` 撞鎖，不是 CLI），**沒有實測**。
- **Superpowers**：沒有實際跑任何 skill。SDD 的 SKILL.md 只讀了相關段落（決策圖、:220-275（其中 dispatch 段從 :246 起）、:405-425、:448-454）和兩支 script，沒有從頭讀完；brainstorming 讀了 :14-60、:110-192；using-git-worktrees / finishing 只用 grep 定位後讀相關行；executing-plans 全文讀過。`task-reviewer-prompt.md`、`re-review-prompt.md`、`review-package` 沒讀。S6（brainstorming 的產出長什麼樣）未查證。官方 marketplace 上游現在釘的版本未查證（S17）。v6.0.0 之前的 release notes（v5.1.0 本身那節以前）沒讀。
- **bridge 自己沒全文讀的部分**：`README.zh-TW.md`、`templates/proposal.md` / `design.md` / `retrospective.md` / `spec.md`（只用 grep 掃）、`templates/verify.md` 第 31–244 行、`templates/adopters/CLAUDE.md.fragment.zh-TW.md`（只用 grep）。如果這些地方有 grep 字串掃不到的上游依賴（例如沒提 skill 名稱、只描述上游行為的句子），本清單會漏掉。
- **CI 的 `version-check.yml` 怎麼判定 issue 可以關**（例如是不是要兩邊都和最新版相同）沒讀，所以決策 A / B 對 issue 狀態的影響是推論，**未查證**。
- **scratch 目錄沒清**（有兩個 upstream repo clone 和多個實驗目錄）：它們在 session scratchpad 裡，不在 repo 內。報告用到的原始輸出當初複製到了 `raw/`，2026-10-02 精簡後只保留 `raw/SUMMARY.md` 末表列出的檔案。
