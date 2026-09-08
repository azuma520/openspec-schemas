# CLAUDE.md

> 給 Claude Code 在這個 repo 工作時的脈絡指引。維持繁體中文書寫。
>
> 關於這個 repo「是什麼、為什麼存在、有哪些 bridges」 → 看 [README.md](./README.md)(英文)或 [README.zh-TW.md](./README.zh-TW.md)(繁中)。
> 本檔聚焦 Claude 在這個 repo 工作時需要知道的**慣例與紅旗**。

---

## 結構約定

```
openspec-schemas/                     ← 本 repo
├── README.md                         ← 英文,GitHub 預設 render
├── README.zh-TW.md                   ← 繁中,有切換連結
├── CLAUDE.md                         ← 你正在讀的(繁中,給 Claude 看)
├── LICENSE                           ← MIT
├── .gitignore
├── .github/workflows/
│   ├── validate-schemas.yml          ← CI 對每個 bridge 跑 openspec schema validate
│   └── version-check.yml             ← 每週驗證 upstream OpenSpec / Superpowers,落後就開 issue
├── docs/
│   ├── roadmap.md / .zh-TW.md        ← 公開 roadmap
│   └── superpowers/                  ← 維護者開發本 repo 時的 superpowers 產出(本 repo 無 openspec/,不跑自己的 bridge 流程)
│       ├── specs/                    ← 設計 spec(brainstorming 產出)
│       ├── plans/                    ← 實作 plan(writing-plans 產出)
│       ├── poc/                      ← PoC / capability spike 報告(實測取事實)
│       ├── research/                 ← 成熟來源拆解分析(讀 skill 全文後的比較;有目錄索引 README)
│       └── retrospectives/           ← 結案複盤
└── superpowers-bridge/                ← 第一個 bridge,自包式 schema bundle
    ├── README.md / .zh-TW.md         ← 完整 bridge 文件(含 install/upgrade + integration runbook)
    ├── VERSION                       ← bundle SemVer(2.0.0),與 schema.yaml 的 version: 2 是兩回事
    ├── schema.yaml                   ← 唯一的行為來源:artifacts DAG + instruction prompts + apply 編排
    └── templates/                    ← artifact 模板(8 個 artifact 各一份)
        ├── brainstorm.md / proposal.md / design.md / spec.md
        ├── tasks.md / plan.md / verify.md / retrospective.md
        └── adopters/                 ← 給採用者貼進自己 CLAUDE.md 的 routing fragment(en + zh-TW)
```

未來新增 bridge:在 repo 根加一個 `<new-bridge>/` 子目錄,內含與 `superpowers-bridge/` 相同結構。CI matrix 在 `.github/workflows/validate-schemas.yml` 的 `matrix.bridge` 加一行即可。

## 命名約定

- **Repo / 目錄 / schema name**:lowercase + hyphen + 對的單複數
  - repo:`openspec-schemas`(複數,可長多個 bridge)
  - bridge dir / schema name:`superpowers-bridge`(單數)
  - 不用 PascalCase(雖然 OpenSpec 自身 repo 用 `OpenSpec`,但他們的 CLI / npm package 都是 lowercase,我們對齊功能性命名)
- **Locale 編碼**:用 `zh-TW`(繁中)、`zh-CN`(簡中);避免裸寫 `zh`

## 雙語策略

| 檔案類型 | 語言 |
|---------|------|
| 入口 `README.md` | 英文 canonical + `README.zh-TW.md` 翻譯 + 頂端切換連結 |
| `CLAUDE.md`(這份) | 繁中(給維護者 + Claude;國際讀者從 README 入口進來) |
| `docs/roadmap.md` | 英文 canonical + `.zh-TW.md` 翻譯 + 切換連結 |
| `superpowers-bridge/README.md` | 英文 canonical + `.zh-TW.md` 翻譯 + 切換連結 |
| `schema.yaml` | 英文(機器讀 + 國際讀者) |
| `templates/*.md` | 模板正文英文;`<!-- -->` 內的填寫指引可用繁中(現況即如此,勿一律翻成英文) |
| `templates/adopters/*.fragment*.md` | en canonical + `.zh-TW` 版,兩份都要改 |
| Commit message | 英文(國際慣例) |
| Code comment | 英文 |

**翻譯同步原則**:英文 canonical,翻譯版可能滯後。修改英文版時若 schema / 工作流發生實質變動,要同步更新繁中版。小改動允許先英文後繁中。

## 沒有 build / test / lint

這個 repo **沒有原始碼、沒有 package.json、沒有測試框架**。它是一包 YAML + Markdown。
唯一的「測試」就是 OpenSpec CLI 的 schema 驗證 —— CI(`validate-schemas.yml`)跑的也只有這兩條指令。

```bash
# 本地跑「單一測試」= 驗一個 bridge(等同 CI 的全部內容)
rm -rf /tmp/test-project && mkdir -p /tmp/test-project/openspec/schemas
cp -R superpowers-bridge /tmp/test-project/openspec/schemas/
cd /tmp/test-project
openspec schema validate superpowers-bridge   # 結構驗證
openspec schemas                              # smoke test:列得出來才算裝好
```

- `openspec` CLI 已裝在本機(`openspec --version` → 1.3.1);沒有的話 `npm i -g @fission-ai/openspec` 或 `npx @fission-ai/openspec`。
- 這個驗證**只驗結構**(artifact 欄位、`requires:` 邊、YAML 形狀)。`instruction:` 裡的 prompt 文字改壞了 CI 一樣是綠的 —— prompt 層的正確性只能靠人讀,這點 bridge README 的 Compatibility 段已明講。
- 必須複製到 `openspec/schemas/` 底下才驗得動;直接在 repo 根跑 `openspec schema validate` 會找不到。
- Windows:上面用 bash 語法(Bash tool / `!` 前綴都走 bash),不要改寫成 PowerShell。

## 目前的工作方向(2026-08-26 起,動 schema 前必讀)

這個 repo 正在從 v1 往下一代改。**動 `schema.yaml` 任何一行之前,先確認你的改動符合下面的方向。**

### 動工門檻:事件閘門,不是時間階段(2026-08-28 重表述)

Orca 已經確定是 bridge 未來的正式 execution runtime,相關架構方向以 [Bridge Guarantee 方向文件](./docs/superpowers/specs/2026-08-27-bridge-guarantee-architecture-direction.md)為準;但在**概念 PoC 通過、正式設計完成並核可之前,不修改 `schema.yaml`,也不新增正式 artifact type**(方向文件護欄 10)。

這句的邏輯是:**方向可以先決定 ≠ 現在就可以實作**。守門從舊的時間階段(「階段二還沒開始」——已不是事實)改成兩個可回答的事件:

| 閘門事件 | 目前答案 |
|---|---|
| 概念 PoC 通過了嗎? | **YES**(2026-08-28,concept supported,見 `docs/superpowers/poc/2026-08-28-traceability-gate/poc-report.md`) |
| 正式設計核可了嗎? | **YES**(2026-09-01,正式設計核可,見 `docs/superpowers/specs/2026-09-01-bridge-guarantee-formal-design.md`) |

**雙 YES 已成立(2026-09-01):schema 實作已解鎖,但解鎖 ≠ 可以直接改。** 正式實作仍**逐塊走各自的 opsx change**,並依正式設計 §9 治理——先 spike 取事實、再選型、再由使用者拍板 implement / simplify / defer / reject,不自動視為必做、不因解鎖直接動 `schema.yaml`。兩件事分開看:

```text
有沒有解鎖實作? → YES
解鎖後能不能繞過 change 流程與 §9 治理? → NO
```

第一個落地的 schema change 是 `loosen-plan`(已 archive,見 `openspec/changes/archive/2026-09-04-loosen-plan/`,Plan Contract + TDD 證據契約,schema major → 2)。

**歷史紀錄(已失效):** 雙 YES 前的守門是「兩個事件全 YES 之前不做正式 schema 實作;單一 YES 不解鎖」(2026-08-28 曾有「PoC 過了就能動 schema.yaml」的放寬解讀,已被使用者否決)。當時唯一的例外是 **corrective fix(修錯例外,2026-08-28 拍板)**——只允許刪除或修正已被證偽的既有宣稱(唯一適用案 `fix-tdd-transitive-claim`,已 archive)。**雙 YES 成立後該例外已失效**(2026-09-01 拍板:例外唯一適用案已 archive、雙 YES 後無存在必要);其「修錯走完整 opsx change 流程與審查鏈」的要求,現由一般 change 流程涵蓋。

Orca 方向的討論素材在 repo 根的 `Orca Worktree 模型分析.md`(43k 行 ChatGPT 匯出)、`2026-08-25-brainstorm-派工模式判準.md`、`2026-08-26-監督式協調-攜出討論包.md`。三份都未進版控。

### 核心設計原則:規定證據,不規定步驟

這是現階段 bridge 調整工作的主軸,也是使用者親自定調的:

> **模型擁有路徑,harness 擁有證據和不可逾越的邊界。**

判準(用來篩 plan / tasks 裡的每一句):

> **如果兩個優秀的 agent 可以用不同做法、最後都符合規格,那計畫就不該提前替它們選一個。**

- 留:`必須 MIT 授權`、`schema 必須 validate 通過`、`不得修改 OpenSpec CLI`、`必須做 TDD 並附 RED/GREEN 輸出`
- 刪:`用 Write 工具建檔`、`跑這串 /tmp 指令驗`、`分成 9 個 commit`、`LICENSE 大約 21 行`

### 硬約束:TDD 不可丟

使用者用這整套的理由就是 SDD + TDD。**任何放寬 plan 的改動,都必須同時確保 TDD 還在**——而且是用「要求證據」的方式,不是用「寫死步驟」的方式。

`plan` artifact **不刪除**,改的是寫法。使用者質疑的是 plan 的細度,不是 spec 或 TDD 的價值。

### Evidence Matrix 三軸(證據規格的既有版本)

使用者早已形式化過這套紀律,見 memory `feedback_evidence_matrix_archive_gate`(在 `~/.claude/projects/D--------1150511googleWorkspace/memory/`)。change archive 前三軸必須對齊:

| 軸 | 內容 |
|---|---|
| 規格 | spec.md 的該需求段落(FR-N / Req-N) |
| 實作 | commit hash 或檔案路徑 |
| 測試 | 對應 test case,或真站 smoke 紀錄(business-level evidence) |

**三軸全部強制、不允許 N/A**。想寫 N/A = spec 沒寫清楚驗證方式,退回補 spec。使用者的原話:「規格及測試規劃沒有的就是我們的邊界。」

配套兩條:
- `feedback_green_semantics_test_vs_business` — 報「綠」要分**程式綠**(test pass)與**業務綠**(真站可用),禁用「全綠」這種含糊詞。
- `feedback_verify_no_write_invariants_by_real_run` — 「唯讀 / 不寫檔」類承諾要真跑 + 前後 snapshot 斷言,mock 只驗 argv 形狀會遮蔽真實副作用。

> ⚠️ 這三份 memory 內文提到的「CLAUDE.md Guardrail #11 / #12」是**舊指標**,現行全域 CLAUDE.md 已改寫、沒有編號 Guardrail;等價紀律現在寫在「複審紀律」節的「先讀『實際驗到什麼』再讀『名字說驗什麼』」。

## 本 repo 自己吃自己的 schema(dogfooding)

這個 repo 已 `openspec init`,並把 `superpowers-bridge` 裝進 `openspec/schemas/`,用它管理本 repo 後續的 schema 優化工作。

- **唯一來源是根目錄的 `superpowers-bridge/`**。`openspec/schemas/superpowers-bridge/` 是實體副本、已 gitignore。
  改完 schema **必須重新同步**,否則跑 opsx 時吃到的是舊副本:
  ```bash
  rm -rf openspec/schemas/superpowers-bridge && cp -R superpowers-bridge openspec/schemas/
  ```
- **不能用 symlink / junction 取代複製**:實測 junction 過得了 `openspec schema validate`,但 `openspec schemas` 掃不到,schema 等於沒裝。
- `.claude/commands/opsx/` 與 `.claude/skills/openspec-*/` 是 CLI 產生物,已 gitignore;新 clone 跑 `openspec init --tools claude` 重建。
- 起手用 CLI 指定 schema:`openspec new change <name> --schema superpowers-bridge`(`--schema` 是 `openspec new change` 的參數)。
- ⚠️ **archive 在 Windows 必定撞目錄鎖**(3/3 複現,穩定模式非偶發)。`mv` 進 `archive/` 一定回 `Permission denied`——git / 編輯器持有目錄 handle。正確做法:
  1. `cp -r openspec/changes/X openspec/changes/archive/X`(複製,不搬)
  2. `diff -r` 驗來源/目標 IDENTICAL
  3. **委派使用者**跑 `rm -rf openspec/changes/X`(AI 的 rm 會被 deny)
  
  見 memory `feedback_opsx_archive_windows_dir_lock`。**別先試 `mv` 撞牆再想起來。**
- **三軌制路由**(memory `feedback_no_opsx_for_evaluation`):opsx change 是**交付容器,不是評估容器**。對外合約 / **schema** / 跨系統介接 / 合規邊界 → 走 opsx;研究 / 評估 / 可逆探索 → 直接 commit + 觀察節點;typo / 文件 / config 微調 → 純直接 commit。每個 change 都要有「ship 了」的明確判準——**是 code 動作、是事件,不是時間軸**。
- **全域 profile 依賴**:bridge 需要 `verify` / `continue` / `new` / `ff` workflow。OpenSpec 預設的 `core` profile 只給 propose / explore / apply / archive,缺 `openspec-verify-change` skill 與 `/opsx:verify`。
  本機已把全域設定(`%APPDATA%\openspec\config.json`)的 `workflows` 開到 11 個全集。**別的機器上要重做這步**,否則 verify artifact 只能走 schema 內建的手動 fallback。
  注意 `openspec config set workflows` 不吃陣列(會報 `expected array, received string`),要直接編 config.json,改完跑 `openspec update` 重生指令。

## Schema 修改流程

1. 編輯 `<bridge>/schema.yaml` 或 `<bridge>/templates/*.md`
2. 跑上面那段本地驗證
3. 依「跨檔耦合」表把該連動的檔案一起改完(同一個 commit)
4. Commit message 用英文,符合 conventional commits(`feat:`、`fix:`、`refactor:`、`chore:`、`docs:`、`ci:`)
5. push 觸發 CI

## 跨檔耦合(改一處必連動,CI 抓不到)

| 你改了什麼 | 必須同步改什麼 | 不改的後果 |
|---|---|---|
| `superpowers-bridge/README.md` 的 Compatibility 表格格式 | `version-check.yml` 的 `Read pinned versions` step | **CI 直接 fail**。它用 ``grep -E '^\| v2 \| `'`` 抓那一行(取第一筆),再用 ``awk -F'`'`` 取第 2、4 個 backtick 欄位 —— 表格必須維持「第一欄 `v2`、OpenSpec 版本與 Superpowers 版本各自包在單一 backtick 裡」的形狀 |
| `schema.yaml` 的 verify / retrospective 時序或 PRECHECK | README「六個值得記住的設計觸點」#5 #6 + 繁中版 | 已知限制的文件化失效(這是 PR #970 顧慮 #2 的唯一應對) |
| `schema.yaml` 的 artifact 增刪 / `requires:` 邊 | bridge README 的 Artifact DAG + Lifecycle 段、`templates/` 對應模板、`docs/roadmap.md` | schema major 需從 2 bump,且 README 要新增 migration guide(見 Versioning 段) |
| 新增 bridge 目錄 | `validate-schemas.yml` 的 `matrix.bridge` + 頂層 `README.md` 的 bridges 表(en + zh-TW) | 新 bridge 完全不進 CI,沒人驗 |
| bridge README 的 routing / 前門規則 | `templates/adopters/CLAUDE.md.fragment.md` + `.zh-TW.md` | 採用者貼進自己 CLAUDE.md 的規則與 README 說法不一致 |
| CLI 指令、slash command 名稱 | bridge README 的「CLI cheat sheet」 | 使用者照抄跑不動 |

## 兩個版本號別搞混

| 識別碼 | 位置 | 什麼時候動 |
|---|---|---|
| schema major | `schema.yaml: version: 2` | 只有 schema graph 契約破壞(artifact 增刪、`requires:` 改、PRECHECK 形狀改)才 bump |
| bundle release | `superpowers-bridge/VERSION` + git tag(`v2.x.y`,發版時打) | 這包的 SemVer 發版,包含純文字修訂;`2.x.y` 都屬 schema major 2 |

Compatibility 表的列鍵用的是 **schema major(`v2`)**,不是 bundle 版本 —— 改 VERSION 不要順手去動那張表的第一欄(會打爆上面的 CI grep)。

## CI / 自動化的既有約定

- `version-check.yml` 每週一 14:00 UTC 跑:比對 npm 上的 `@fission-ai/openspec` 與 obra/superpowers 最新 release,與 README 釘住的 baseline 有差就開/更新一張帶 `upstream-version-check` label 的 issue。**漂移不算失敗**(workflow 保持綠);只有「用最新版驗 schema 失敗」才 fail run。
- `upstream-version-check` label 由 workflow 每次執行時保證存在(README 的 Upstream Drift badge 靠它解析),不要手動刪。
- bridge README 的 badge URL 硬寫了 `JiangWay/openspec-schemas`;repo 若改名 / 換 owner,badge 與 issue 連結要一起改。
- 兩支 workflow 都固定 Node 24 + `actions/checkout@v6` / `setup-node@v6` / `github-script@v9`。

## 三個 alfred-openspec 顧慮的應對(內化記憶)

PR #970 review 提出三個顧慮,本 schema 在 v1 已具體應對。Claude 在這個 repo 修任何 schema 行為前都要記住:

| 顧慮 | 應對 |
|------|------|
| #3 主動 commit 使用者 git | **完全移除**。Step 0 改為 skill PRECHECK,只驗 skill 不動 git |
| #1 與 Superpowers 強耦合無 capability detection | **Layer 1**:每個 invoke skill 的 instruction 開頭跑 PRECHECK,缺失就 STOP。**Layer 2**:對 verify / retrospective 加 evidence-based PRECHECK(`git log`、`grep` 檢查可觀察狀態) |
| #2 verify 時序錯位(以及 retrospective 同型) | 已知限制,在 bridge README 的「設計觸點 #6」文件化。完整修法等 OpenSpec 引擎引入 `post_apply` phase。Layer 2 evidence-based PRECHECK 是當前緩解 |

**修 schema 時的紅旗** —— 以下行為**不要做**(會反 PR #970 的應對):

- ❌ 在 instruction 寫「主動 git add / git commit」
- ❌ 拿掉某個 PRECHECK 但沒換更強的替代品
- ❌ 把 verify / retrospective 從 artifact 拉掉但沒在 README「設計觸點」段同步更新限制
- ❌ 改 schema name 但沒同步改 bridge 內所有文件 + 頂層 README 的 bridge 索引
- ❌ 在 apply instruction 加 `superpowers:executing-plans` 當 fallback(它不派任何獨立審查者——單 agent 自跑自查,上游在有 subagent 時也明示改用 subagent-driven-development;TDD 不是差異點——TDD 由 tasks.md 的 applicability 標註 + 證據契約承載(`loosen-plan` 起),與哪個執行器無關。本 schema 刻意只支援有 subagent 的平台,缺就叫使用者改用內建 `spec-driven`)
- ❌ 把 PRECHECK 失敗改成「靜默降級」(整套設計就是 fail loud;缺 skill 一律 STOP)

## 相關連結

- 設計 spec:[`docs/superpowers/specs/2026-05-02-openspec-schemas-monorepo-design.md`](./docs/superpowers/specs/2026-05-02-openspec-schemas-monorepo-design.md)
- 實作 plan:[`docs/superpowers/plans/2026-05-02-phase-1-implementation.md`](./docs/superpowers/plans/2026-05-02-phase-1-implementation.md)
- 結案複盤:[`docs/superpowers/retrospectives/2026-05-03-pr970-endgame.md`](./docs/superpowers/retrospectives/2026-05-03-pr970-endgame.md)
- 成熟來源拆解分析索引:[`docs/superpowers/research/README.md`](./docs/superpowers/research/README.md)(plan 結構比較、TDD evidence 分析)
- roadmap(v1.x backlog 與「等 OpenSpec core」項目):[`docs/roadmap.md`](./docs/roadmap.md)
- PR #970 review:<https://github.com/Fission-AI/OpenSpec/pull/970>
- 既有 spec-kit superpowers bridges 參考:
  - [RbBtSn0w/spec-kit-extensions/superpowers-bridge](https://github.com/RbBtSn0w/spec-kit-extensions/tree/main/superpowers-bridge)
  - [WangX0111/superspec](https://github.com/WangX0111/superspec)
<!-- workflow-harness:start -->
<!-- 由 workflow-harness plugin 自動加入。本區由 plugin 管理，**請勿手改**。升級用 /init-harness、卸載用 /uninstall-harness（v1.x 後期加）。 -->

## Workflow Harness 規則（plugin 注入）

> 健檢：`/doctor-harness`

### 6 條核心 Guardrails

1. **驗收節點必進 `驗收節點.md` sentinel 區段**（E2）— 時間觸發 + 明確驗收標準走 A 路徑、不可散 backlog / 散別處
2. **多步驟工作（≥3 步 / 跨 tool call）必跑 TaskCreate**（A4）— 開工後新增的子任務用 `TaskUpdate` append、不另開新 list
3. **Handoff 六欄 append-only**（A6）— 同日多 session 寫同檔；前 session 內容不可改；第四欄含【紀律接力】+【當日洞見】sub-segments
4. **Session 開工三步驟順序不可跳**（A3）— 不可在沒讀 handoff 前直接動工；① 跑 `/work-status` 看現況 + 讀最新 handoff、② 讀最新區塊了解進度、③ 綜合現況 + 成熟 backlog 提優先建議；月首 / 週首先 backlog triage、動工前確認本 session 主題
5. **新事件必走 Decision Tree 5 問**（F1）— 不可直接寫進任意 markdown 檔
6. **Session 收工必透過 `/end-session` 寫 handoff**（A5+A6+L9）— 不可只手寫繞過 schema 檢查

### 工作完整性（交接點結清 handoff）

一個工作單位 = 程式改動 + next actor 需要的接力 context（diff 看不出的決策 / 否決的選項 / 風險）。
本地 WIP commit 可不綁 handoff；但**撞到交接點前、未清的 handoff debt 必須結清**：

> 切換 task ・ 停手或 session 結束 ・ push ・ PR ・ shared branch ・ review ・ 改方向 ・ 交另一 session

「交付才算做完」——紀錄是工作的最後一步、不是 commit 尾巴。Plugin 提醒、不擋。

**完成同步**：完成一個工作單位（change 歸檔 / backlog 標完成）時、順手清掉 `next-actions` 與專案 README「Next Actions」裡對應的、已做完的過時條目——這也是完成工作的一部分、在該工作單位的交接點一起收、不事後補。

### 主動 surface 優先建議（感測器、不是判官）

agent 在兩個場景主動提 1-3 條優先建議：

- **開工**：跑完開工步驟、等使用者輸入前
- **被問**：使用者問「先做哪個 / 接下來做什麼 / 排個順序」

effort / impact 當場白話評（「這條一下午能做完」「這條影響最大」）、不寫進條目、不替使用者拍板。

### 「task」這個詞怎麼理解（進出兩個方向）

<!-- 本段是這個詞的辨義規矩本身，指名它才講得清楚；禁用詞掃描 MUST 排除本段。 -->

| 方向 | 規矩 |
|---|---|
| **agent 輸出**（對話、範本、命令說明、hook 訊息） | 一律中文。工作地圖的單位稱「**任務**」；OpenSpec `tasks.md` 內的項目稱「**步驟**」；Claude Code 內建的同名工具 MUST NOT 出現在對外文字中 |
| **使用者輸入**（口語） | **句中同時出現登記動詞時**（清單見登記流程 `work-status-registration`、本處不重抄），該詞指涉之事即為**登記對象**，agent 走登記流程、**不套下方預設**。**句中無登記動詞時**，agent **預設理解為「步驟／逐項執行」**、**MUST NOT** 逕自視為登記請求 |
| 無法判別時 | agent 問一句確認，MUST NOT 猜著做 |

**預設值偏向「不做」**，理由是錯誤成本不對稱：猜成「步驟」而錯 → 少登記一條、使用者補一句即可；猜成「任務」而錯 → agent 擅自寫進使用者的工作地圖，需回頭清理。

**登記動詞優先於預設值**：句中出現登記動詞時意圖已由使用者明示，成本方向反轉——此時不登記才是那個要使用者回頭補的錯。

### 5 問 Decision Tree

新事件來了 → 依序問五題，**遇到 Yes 立刻定位**：

```
Q1: 是「今天做的事」或「session 內進度」？
    → handoff 二、完成事項 / TaskCreate

Q2: 有明確時間觸發（X 月 Y 日要做 / 看）+ 明確驗收標準？
    → 驗收節點.md sentinel 區段（observation-checkpoint V1-V3）；用 `/pending-verify`（別名 `/observe`）建 4 欄 SMART schema

Q3: 是某個 active 專案的事？（≥3 步 / 跨 ≥2 session 才算專案、開資料夾；1-2 步 / 1 session 內結束 → 不開、走 next-actions）
    → 該專案 README.md「Next Actions」或 tasks.md（D4）

Q4: 是規則改動 / SOP 候選 / 累積觀察 / 技術債 / 構想 / bug？
    → backlog.md `## 待辦` heading + 對應主分類 tag（`[SOP 候選]` / `[優化建議]` / `[bug]` / `[構想]`）

Q5: 「想累積樣本評估規則是否有效」（沒明確 deadline、沒明確驗收）？
    → backlog.md `[優化建議]` tag（B 路徑、N=5 surface）

以上都不是 → 問用戶（不可自主裁量）
```

### Slash Commands

- `/init-harness` — 安裝 / 升級 plugin 骨架（含撞檔 matrix）
- `/new-project <name>` — 建專案資料夾（D1 schema）
- `/end-session` — 半自動寫 handoff（對應 Guardrail #6）
- `/doctor-harness` — 自我健檢（hook / template / config）

### Subagent / Tool 慣例

- **動工前先診斷問題**（G4）：repro → root cause → scope → 動手方式

### 優先級

若本區規矩與本檔上方「個人化區段」衝突，**以使用者個人化區段為準**（spec §Risks R4）。
若本區規矩與其他 plugin 衝突（superpowers / sd0x-dev-flow），**以使用者明示優先級為準**（spec §Risks R6）。

<!-- workflow-harness:end -->
