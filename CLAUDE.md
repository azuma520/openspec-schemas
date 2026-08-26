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
│       └── retrospectives/           ← 結案複盤
└── superpowers-bridge/                ← 第一個 bridge,自包式 schema bundle
    ├── README.md / .zh-TW.md         ← 完整 bridge 文件(含 install/upgrade + integration runbook)
    ├── VERSION                       ← bundle SemVer(1.0.0),與 schema.yaml 的 version: 1 是兩回事
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

### 分兩階段,不要混

| 階段 | 範圍 | 狀態 |
|---|---|---|
| **一(現在)** | 把 `superpowers-bridge` 調整成符合現行做法與需求 | 進行中 |
| **二(之後)** | 接 Orca:`execution-readiness` artifact、Coordinator agent、派工判準 | **還沒開始,不要提前把 Orca 的東西塞進 schema** |

階段二的討論素材在 repo 根的 `Orca Worktree 模型分析.md`(43k 行 ChatGPT 匯出)、`2026-08-25-brainstorm-派工模式判準.md`、`2026-08-26-監督式協調-攜出討論包.md`。三份都未進版控。

### 核心設計原則:規定證據,不規定步驟

這是階段一的主軸,也是使用者親自定調的:

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
| `superpowers-bridge/README.md` 的 Compatibility 表格格式 | `version-check.yml` 的 `Read pinned versions` step | **CI 直接 fail**。它用 ``grep -E '^\| v1 \| `'`` 抓那一行,再用 ``awk -F'`'`` 取第 2、4 個 backtick 欄位 —— 表格必須維持「第一欄 `v1`、OpenSpec 版本與 Superpowers 版本各自包在單一 backtick 裡」的形狀 |
| `schema.yaml` 的 verify / retrospective 時序或 PRECHECK | README「六個值得記住的設計觸點」#5 #6 + 繁中版 | 已知限制的文件化失效(這是 PR #970 顧慮 #2 的唯一應對) |
| `schema.yaml` 的 artifact 增刪 / `requires:` 邊 | bridge README 的 Artifact DAG + Lifecycle 段、`templates/` 對應模板、`docs/roadmap.md` | schema major 需從 1 bump,且 README 要新增 migration guide(見 Versioning 段) |
| 新增 bridge 目錄 | `validate-schemas.yml` 的 `matrix.bridge` + 頂層 `README.md` 的 bridges 表(en + zh-TW) | 新 bridge 完全不進 CI,沒人驗 |
| bridge README 的 routing / 前門規則 | `templates/adopters/CLAUDE.md.fragment.md` + `.zh-TW.md` | 採用者貼進自己 CLAUDE.md 的規則與 README 說法不一致 |
| CLI 指令、slash command 名稱 | bridge README 的「CLI cheat sheet」 | 使用者照抄跑不動 |

## 兩個版本號別搞混

| 識別碼 | 位置 | 什麼時候動 |
|---|---|---|
| schema major | `schema.yaml: version: 1` | 只有 schema graph 契約破壞(artifact 增刪、`requires:` 改、PRECHECK 形狀改)才 bump |
| bundle release | `superpowers-bridge/VERSION` + git tag `v1.0.0` | 這包的 SemVer 發版,包含純文字修訂;`1.x.y` 都屬 schema major 1 |

Compatibility 表的列鍵用的是 **schema major(`v1`)**,不是 bundle 版本 —— 改 VERSION 不要順手去動那張表的第一欄(會打爆上面的 CI grep)。

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
- ❌ 在 apply instruction 加 `superpowers:executing-plans` 當 fallback(它不會 transitive 帶起 TDD 與 code-review,等於把 Superpowers 的價值抽掉;本 schema 刻意只支援有 subagent 的平台,缺就叫使用者改用內建 `spec-driven`)
- ❌ 把 PRECHECK 失敗改成「靜默降級」(整套設計就是 fail loud;缺 skill 一律 STOP)

## 相關連結

- 設計 spec:[`docs/superpowers/specs/2026-05-02-openspec-schemas-monorepo-design.md`](./docs/superpowers/specs/2026-05-02-openspec-schemas-monorepo-design.md)
- 實作 plan:[`docs/superpowers/plans/2026-05-02-phase-1-implementation.md`](./docs/superpowers/plans/2026-05-02-phase-1-implementation.md)
- 結案複盤:[`docs/superpowers/retrospectives/2026-05-03-pr970-endgame.md`](./docs/superpowers/retrospectives/2026-05-03-pr970-endgame.md)
- roadmap(v1.x backlog 與「等 OpenSpec core」項目):[`docs/roadmap.md`](./docs/roadmap.md)
- PR #970 review:<https://github.com/Fission-AI/OpenSpec/pull/970>
- 既有 spec-kit superpowers bridges 參考:
  - [RbBtSn0w/spec-kit-extensions/superpowers-bridge](https://github.com/RbBtSn0w/spec-kit-extensions/tree/main/superpowers-bridge)
  - [WangX0111/superspec](https://github.com/WangX0111/superspec)
