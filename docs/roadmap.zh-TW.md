# Roadmap

[English](./roadmap.md) · [繁體中文](./roadmap.zh-TW.md)

本 repo 是一個持續維護中的個人 side project。下面的 roadmap 是規劃,不是承諾 —— 項目會視實際使用回饋而調整。

## v1 — 已釋出

- [x] **`superpowers-bridge`** — 串接 OpenSpec ↔ obra/superpowers,自帶 `retrospective` artifact

## v2 — 已釋出

- [x] **Plan Contract + TDD evidence contract** — 把步驟導向的 `plan` artifact 換成逐任務的執行契約(寫的是「完成的定義」,不是「怎麼做」);TDD 適用性標註(`TDD: applicable` / `TDD: n/a — <原因>`)與 RED/GREEN 紀錄現在跟著 `tasks.md` 走,verify 只檢查有沒有存在、結構對不對,不是不可繞過的強制關卡(schema major 2、bundle 2.0.0)

## v3 — 已釋出

- [x] **Contract identity(Requirement / Scenario 穩定 ID)** — 每個 Requirement 與 Scenario 標題現在都帶穩定、可被機器引用的 ID(`### Requirement: <REQ-ID> <description>` / `#### Scenario: <REQ-ID>-S<m> <description>`),改措辭不會斷掉;新 ID 的配置依固定規則。verify 新增的第 13 項檢查,以決定性方式判定這個 change 的歸檔後候選狀態有沒有缺號、重號、前綴錯位,並與 OpenSpec CLI 的 JSON 交叉核對(schema major 3、bundle 3.0.0)。這一版只做身分層——`tasks.md` 的 `Contracts:` 承接標註、驗收台帳、可執行(不可繞過)的 gate 都留給後續 change。

## v4 — 已釋出

- [x] **以 `Task` 開頭的 plan 條目標題** — `plan.md` 的條目現在可以寫成 canonical 寫法 `## Task <編號> — <標題>`,Superpowers 的 `task-brief` 抽取器辨識得到;legacy 寫法 `## <編號> — <標題>` 繼續接受、沒有排定移除時程,`Task` 不屬於鍵值(schema major 4、bundle 4.0.0)。條目改由正面規則定義,verify 第 12 項不再收行首 backtick fenced code block 內的 `##` 標題形狀文字。這條規則另外帶來兩項行為變更:形如 `Task <編號>` 的行首非條目 `##` 標題(`Task` 一字、一個以上 space 或 tab、再接符合 `\d+(\.\d+)*` 的編號,編號後是空白或行尾)變成條目;`##1.1` 或縮排的 ` ## 1.1` 不再是條目。canonical 寫法的條目變得能被 `task-brief` 辨識;這不代表它替某個條目抽出的範圍是對的。

## v1.x — 後續 backlog

這些項目記錄在 `~/.claude/plans/pr-quizzical-oasis.md`(實作 plan):

- [ ] **`workflow-retrospective` skill 打包** — 目前 retrospective procedure 內嵌在 schema instruction 裡(Decision 3)。如果有真實使用者反映需要互動式呼叫 `/workflow-retrospective`(在 schema 流程之外),會把它升級成獨立的 Claude Code plugin
- [ ] **End-to-end CI 整合測試** — 目前 CI 只跑 `openspec schema validate`。round-trip 測試(`/opsx:new` 一路到 `/opsx:archive`)能抓更多回歸,但需要 Superpowers 進入 CI 環境
- [ ] **Verify artifact 5 處改進** — 列在 v1.1 backlog A(template 表達清晰、design 可選處理、worktree 來源、pass 標準、TDD 註記)

## 等 OpenSpec core

這幾項在社群 schema 內無法解決,要等上游:

- [ ] **`requires_skills:` schema 欄位** — 把 prompt 層的 PRECHECK 換成引擎驗證的宣告
- [ ] **`post_apply` phase** — 讓 `verify` / `retrospective` 變成真正的 post-apply hook,而非帶時序錯位的 artifact(對應 spec-kit 的 `after_implement`)

## 未來 bridge 候選

實際需求出現時才加:

- [ ] **`obra-bridge`** — 廣義對 obra/* 其他工具的整合(如果使用者社群成長)
- [ ] **領域特定 schema** — 例如 `data-pipeline` 變體,加強 schema validation artifact

想提議新 bridge?到 <https://github.com/azuma520/openspec-schemas/issues> 開 issue。
