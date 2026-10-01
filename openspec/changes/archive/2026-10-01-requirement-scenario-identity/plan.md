# requirement-scenario-identity — Plan Contract

> **For agentic workers:** Use superpowers:subagent-driven-development
> to implement this plan task-by-task. Each entry states what "done"
> means for one task, not how to get there — two executors may satisfy
> the same entry by different paths and both conform.

**Goal:** 讓 Requirement／Scenario 有不隨措辭改變的 stable ID，verify 新增判準固定的 identity integrity check（check 13），本 repo 既有 spec 一次補號，並以 schema major 3 標示這個相容性破壞。同時以 regression（RED→GREEN）與雙人盲測 conformance 兩條證據線，試行 Verification Strategy。

**Pointers:** [`specs/contract-identity/spec.md`](./specs/contract-identity/spec.md)（身分規則與宣稱邊界的 normative owner）；[`specs/plan-contract/spec.md`](./specs/plan-contract/spec.md)、[`specs/tdd-claim-accuracy/spec.md`](./specs/tdd-claim-accuracy/spec.md)、[`specs/tdd-evidence-contract/spec.md`](./specs/tdd-evidence-contract/spec.md)、[`specs/repo-guidance/spec.md`](./specs/repo-guidance/spec.md)（補號 delta）；[`design.md`](./design.md) D1–D10 與 Migration Plan；[`tasks.md`](./tasks.md) 檔頭註解承載 2026-09-30 的盲測執行裁定與 RED 順序理由，本檔不另抄一份。

**Global constraints (verbatim from the specs; every entry below is bound by them):**

- "A contract's ID SHALL NOT change once the contract exists."
- "Whether two occurrences denote the same contract SHALL be decided from artifact structure and the OpenSpec operation role, never from reading the text"
- "The check SHALL NOT re-implement OpenSpec's merge."
- "Counts the identity check extracts from text SHALL be compared with the OpenSpec CLI's JSON, and any disagreement SHALL block without presuming which side is right. Each comparison SHALL read the CLI against the state it judges."
- "When the pairing cannot be made reliably — for instance the requirement counts already disagree — the cross-check is undeterminable and SHALL block; the check SHALL NOT guess a pairing."
- "An undeterminable outcome SHALL NOT be recorded as an identity violation. Neither kind SHALL have a degraded pass: identity integrity is a Core Integrity Invariant, which no change may switch off or override."
- "The identity check is a set of deterministic, machine-evaluable rules executed by the verify agent as part of verify; it is not a non-bypassable executable gate, and no surface SHALL describe it as one."
- "No surface SHALL present the fixtures as establishing more than this requirement states."
- "Where a subject was run more than once, the records submitted as completion evidence SHALL be the single RED and the single GREEN that make the claim; additional runs SHALL NOT be recorded as further RED or GREEN records under that subject."

Binding non-goals carried from design.md（不是 spec 原文，但每個 entry 都受其約束）：不加 `Contracts:`、不做 `verification-results.json`、不做 executable Gate、不新增任何需維護的程式碼；不做需要歷史或歸檔前後比較的身分檢查；補號 delta 的 requirement／scenario 正文一字不改；不修改正式設計、`tdd-evidence-contract` 或已凍結的本 change design artifacts。

---

## 1.1 — 身分 mutation fixtures

- **Delivers:** 新目錄 `docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/fixtures/` 下的一組 fixtures。每個 fixture 是一個自足的迷你 repo（主 spec＋一個 change）。正向對照 fixture 全部合規；違規與無法判定 fixture 只有一個作者引入的 mutation source，其餘都合規；合起來涵蓋 `contract-identity` 所有以 identity check 判定為 THEN 的 scenario（清單見 tasks.md 1.1）。
- **Acceptance:** tasks.md 1.1 列出的每個 scenario ID 至少被一個 fixture 涵蓋，或在 1.2 的覆蓋表中記為覆蓋缺口，並附當時的實測指令與輸出。每個違規或無法判定的 fixture 只有一個作者主動引入的 mutation source：拿 `contract-identity` REQ-1 至 REQ-6 逐條檢查，找不到第二個獨立引入的缺陷。一個 mutation 必然同時觸發多條規則時（例如 ADDED 重用現有 ID，同時觸犯 REQ-3 與 REQ-4），這些連帶命中是合法的，不算第二個缺陷；1.2 的預期答案表逐一列出主要違規與連帶命中，並說明為什麼避不開。主要違規與連帶命中的區分只供作者分析，不作為盲測的評分標準。盲測評分模型（2026-09-30 使用者裁定，2.1 與 3.1 皆適用）：每個 fixture 有一個預期最終判定（通過或 BLOCK），以及零或多個必須出現的 BLOCK 類別（違規、無法判定）；執行者的判定正確，當且僅當最終判定相同、且回報的 BLOCK 類別集合與預期集合相同。一個 fixture 同時觸發兩類時（例如 requirement 數量比對已完成且不一致記為違規，其後 scenario 無法可靠配對記為無法判定），兩類都要回報。不要求理由逐字一致，不要求執行者指出作者定義的主要違規；執行者另外列出可由同一 mutation 推導出的違規細節，不算判錯。每個 fixture 在自己的目錄內跑 `openspec validate --all` 的結果都有記錄；預期會被 check 1 擋下的（若有）在預期答案表註明。不動舊 f1–f13 目錄的任何檔案（`git status` 在該目錄下無變動）。
- **Blocked by:** none
- **Interfaces:** 產出 fixture 目錄名稱與「破壞了什麼」，供 1.2（預期答案表與覆蓋表）、1.3（打亂副本）、2.1、3.1 使用。

## 1.2 — fixtures README：預期答案、覆蓋表、結果表

- **Delivers:** fixtures 目錄的 README，承載預期答案表、`contract-identity` scenario → fixture 覆蓋表、結果表（欄位至少包含 tasks.md 1.2 列的七欄），以及重跑說明。
- **Acceptance:** 列出 `fixtures/` 下的目錄，與預期答案表逐列比對，兩個方向都沒有缺漏。預期答案表每列都寫明預期判定：寫「通過」，或寫「BLOCK」並註明「違規」「無法判定」或兩者都有。覆蓋表的每個 scenario ID 在 `specs/contract-identity/spec.md` 都查得到（grep 命中）。結果表在本 task 完成時已建好欄位，列數等於 fixture 數；RED、GREEN 欄可以先空著。重跑說明寫明：要用中性名稱重新打亂；預期答案表不交給執行者。
- **Blocked by:** 1.1
- **Interfaces:** 消費 1.1 的 fixture 清單。產出預期答案表，2.1、3.1 拿它比對判定；產出結果表，2.1、3.1 填入判定，5.3 讀取。

## 1.3 — 盲測器材凍結

- **Delivers:** 一套固定的盲測器材：打亂命名的 fixture 副本、打亂名與原名的對照表、blind prompt、操作程序，以及 RED／GREEN 各自的規則來源取得方式。RED 與 GREEN 之間的 fixture 內容、prompt、操作程序都相同，打亂後的名稱每次重新產生（防止答案沿用），影響判定的變數只有「規則文字」。
- **Acceptance:** 開跑 RED 前，prompt 與操作程序已存成全文或記下內容雜湊。3.1 的 GREEN 盲測使用的 prompt 與程序與此逐字相同；兩者差異只在規則來源那一段，可用 diff 看出。交給執行者的副本不含任何預期判定，目錄名、檔名、註解都不會洩漏答案（逐檔 grep 預期答案表的關鍵字無命中）。副本放在 repo 之外。prompt 要求逐 fixture、逐 check 回報，BLOCK 時分「違規」與「無法判定」，PRECHECK 與 check 5 回報「不適用於 fixture」。RED 的規則來源註明是哪個 commit 的 `schema.yaml`。
- **Blocked by:** 1.1
- **Interfaces:** 產出盲測器材，供 2.1（RED 規則來源）與 3.1（GREEN 規則來源、同一份 prompt 與程序）使用；GREEN 用的打亂副本與 RED 用的那份要各自重新打亂。

## 2.1 — RED 盲測 baseline

- **Delivers:** 1 位盲測執行者依修改前的 checks 1–12 判過全部 fixtures 的紀錄，以及據此導出的 TDD subject 清單。
- **Acceptance:** 結果表「RED 實際」欄每列都有值，執行者使用的模型已記錄。以執行者的原始回報為準；結果表與原始回報對讀，每一列都一致。每個 fixture 依規則二選一：舊判定與預期判定不一致的，列為 3.1 的 subject，寫成 `<fixture 目錄>::<預期判定>`；一致的標為 conformance only。本 task 完成時，`git diff` 顯示 `superpowers-bridge/schema.yaml` 沒有被修改。若沒有任何缺 ID 的 fixture 被舊規則放行，停下回報使用者，3.1 不開工。
- **Blocked by:** 1.2, 1.3
- **Interfaces:** 消費 1.1 的 fixtures（經 1.3 打亂）、1.2 的預期答案表與結果表、1.3 的器材。產出 subject 清單與每個 subject 的 RED 內容（預期判定與實際判定），3.1 據此寫 RED 紀錄。

## 3.1 — verify check 13（identity integrity）與 GREEN 雙人盲測

- **Delivers:** `schema.yaml` 的 verify instruction 新增 check 13，完整承載 `contract-identity` REQ-1 至 REQ-8，並寫明兩個 openspec 1.3.1 的讀取細節；接著由 2 位互相獨立的盲測執行者依新規則各判一次全部 fixtures，提供本 task 的 GREEN 與全部 fixture 的 conformance evidence。規則寫入與 GREEN 取得在同一個 task 內完成，TDD 證據因此留在加規則的這個 task 底下（`contract-identity` REQ-8）。
- **Acceptance:** `contract-identity` 的每個 REQ 都能在 check 13 內文找到對應的判定句，找不到的就是缺漏。內文寫明以下各點：
  - 預演歸檔在暫存複本上跑，而且不加 `--skip-specs`。
  - 候選狀態的 CLI 核對在暫存複本上執行，change 層的核對對歸檔前的狀態執行。
  - `--deltas-only` 的輸出只讀 stdout。
  - scenario 陣列的欄位是 `requirement.scenarios`。
  - 從文字計數的方法（2026-09-30 使用者裁定）：逐行比對，行首精確等於 `### Requirement:` 算一條 requirement、精確等於 `#### Scenario:` 算一個 scenario，大小寫與空白照字面，不辨識 code block 等 markdown 結構。這是已知的保守限制：code block 內形似標題的行會使計數與 CLI 不一致而 BLOCK。
  - 預演歸檔成功的判準：結束碼 0 且暫存複本中的 change 已移入 `openspec/changes/archive/`；只看結束碼不夠（openspec 1.3.1 中止歸檔時結束碼仍是 0，見 1.1 的 `author-run.md`）。
  - 「違規」與「無法判定」分開記錄，而且都沒有降級出口。
  - 宣稱邊界：check 13 不被描述成 executable Gate。

  盲測部分：結果表的「GREEN 執行者 A」「GREEN 執行者 B」「是否一致」三欄每列都有值。兩位與 2.1 用同一個模型，已記錄。兩位用同一份 prompt、同一份打亂副本、同一套操作程序，可從 1.3 的存檔比對。
  - 不一致或不符預期的列：寫明類型（規則不清、讀錯狀態、CLI 資料不足、操作對應不清、忽略規則、重跑不一致），不算 GREEN。
  - 修改 check 13 之後：兩位執行者都要以新打亂的副本重跑，舊結果保留在紀錄中、不覆蓋。

  2.1 的每個 subject 都有恰好一筆 RED、一筆 GREEN，各自寫在 tasks.md 3.1 底下。RED 的 `failure:` 寫出預期判定與實際判定。GREEN 只在兩位執行者判定一致、且符合預期時才寫。有 subject 做不到時，停下回報使用者，不得宣告完成。`openspec schema validate` 在一次性專案複本中通過。
- **Blocked by:** 1.3, 2.1（2.1 是硬性前置：2.1 完成前不得修改 `schema.yaml`）
- **Interfaces:** 消費 1.1 的 fixtures（經 1.3 打亂）、1.2 的預期答案表與結果表、1.3 的器材、2.1 的 subject 清單與 RED 內容。產出 check 13 文字，4.1、4.2 要與它一致；產出結果表的 GREEN 內容，5.3 使用。

## 3.2 — specs 作者規則與 schema major 3

- **Delivers:** `schema.yaml` 的 `specs` instruction 寫入 ID 標題語法、改名保 ID、新號配置兩層（檢查層與發號層），並把 `version:` 改為 3。
- **Acceptance:** 逐句對讀 `contract-identity` REQ-1、REQ-2、REQ-4：語法、RENAMED 保 ID 與其補號例外、檢查層兩條大小規則、發號層「查含 archive 在內的歷史最大號」都有對應句子。`specs` instruction 明寫發號層不在 check 13 驗證範圍內。`schema.yaml` 第 2 行是 `version: 3`。`openspec schema validate` 在一次性專案複本中通過。1.1 的 fixtures 不需要因此修改。
- **Blocked by:** 2.1（`schema.yaml` 任何修改都在 RED 之後）
- **Interfaces:** 產出作者規則文字，4.1 的 `templates/spec.md` 與 4.2 的 README 格式說明要與它一致。產出 `version: 3`，4.2、4.3 的版本描述以它為準。

## 4.1 — templates 對齊

- **Delivers:** `templates/spec.md` 的範例標題帶 ID，RENAMED 範例示範保留 ID；`templates/verify.md` 新增 check 13 段落。
- **Acceptance:** `templates/spec.md` 的 ADDED、MODIFIED、REMOVED、RENAMED 範例標題都符合 REQ-1 語法，RENAMED 的 FROM／TO 使用同一個 ID。`templates/verify.md` 的 check 13 標題與 `schema.yaml` 逐字相同。段落要求把「違規」與「無法判定」分開記錄，宣稱邊界只做摘要，並連到 spec。在一次性專案複本中分別跑 `openspec instructions specs --change <change>` 與 `openspec instructions verify --change <change>`，兩者結束碼都是 0，輸出也都含新文字。
- **Blocked by:** 3.1, 3.2
- **Interfaces:** 消費 3.1 的 check 13 標題與內容、3.2 的標題語法。

## 4.2 — bridge README（en＋zh-TW）

- **Delivers:** 兩份 bridge README 同步說明以下各項：ID 格式、check 13 與宣稱邊界、v3 的 Versioning、「Why v2 → v3」、「Migrating v2 → v3」、Compatibility v3 列、Known breaking changes；原本描述現行版本的句子一律更新。
- **Acceptance:** 兩份 README 的段落一一對應，語意一致。遷移指南明寫「一個補號 change 涵蓋所有 capability、不可按 capability 分批」。Compatibility 表的第一個資料列是 v3，版本欄填實際驗過的版本，並附驗證紀錄；v2、v1 列保留。重跑 `version-check.yml` 的 grep 與 awk 指令，取得的是 v3 列的兩個版本。兩份 README 的 `v2`／`2.0.0` 殘留逐筆判讀，每筆要嘛是歷史紀錄，要嘛已經更新。check 13 的說明沒有任何一句宣稱它不可繞過，也沒有宣稱由 Harness 強制。
- **Blocked by:** 3.1, 3.2
- **Interfaces:** 消費 3.1 的 check 13 內容與 3.2 的 `version: 3`。Compatibility 表的列形狀要與 4.3 修改後的 `version-check.yml` grep 一致，兩個 task 互為對方的另一端。

## 4.3 — 其餘寫死版本之處

- **Delivers:** 以下各處全部對齊 v3／`3.0.0`：`VERSION`、`version-check.yml` 的列鍵、repo `CLAUDE.md` 的版本與耦合描述、roadmap（en＋zh-TW）、根目錄兩份 README 的 bridges 表。
- **Acceptance:** `superpowers-bridge/VERSION` 內容是 `3.0.0`。`version-check.yml` 以 `v3` 為列鍵，對 4.2 修改後的 README 實跑其 grep 與 awk，取得兩個版本。`CLAUDE.md` 的 schema major bump 判準句與 bridge README 的 breaking 判準一致。roadmap 兩份都有 v3 條目。根目錄兩份 README 的 `superpowers-bridge` 版本欄是 `v3`。以上檔案的 `v2`／`2.0.0` 殘留逐筆判讀，每筆要嘛是歷史紀錄，要嘛已經更新。
- **Blocked by:** 3.2
- **Interfaces:** 消費 3.2 的 `version: 3`。`version-check.yml` 的 grep 要與 4.2 的 Compatibility 表列形狀相符，另一端是 4.2。

## 5.1 — dogfood 副本同步

- **Delivers:** `openspec/schemas/superpowers-bridge/` 與 `superpowers-bridge/` 內容一致，之後的 opsx 流程吃到的是新規則。
- **Acceptance:** `diff -r` 兩個目錄沒有輸出。`openspec schema validate superpowers-bridge` 通過，`openspec schemas` 列得出它。`openspec instructions verify --change requirement-scenario-identity` 的輸出含 check 13 標題。
- **Blocked by:** 3.1, 3.2, 4.1, 4.2, 4.3
- **Interfaces:** 產出已同步的 schema 副本，本 change 的 verify artifact 依它執行 check 13。

## 5.2 — 補號遷移驗收

- **Delivers:** 本 change 以預演歸檔實證 design D7：歸檔後，本 repo 主 spec 全部帶 ID，正文不變。
- **Acceptance:** 在暫存複本跑 `openspec archive requirement-scenario-identity -y`，結束碼是 0，而且預期的歸檔狀態轉換確實發生：暫存複本中原本的 change 路徑已不存在，`openspec/changes/archive/` 下出現對應的已歸檔 change。只看結束碼不夠——openspec 1.3.1 在歸檔中止（輸出 `Aborted. No files were changed.`）時結束碼仍是 0（實測見 `docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/author-run.md`）。預演後的主 spec 必須符合：
  - `plan-contract`、`tdd-claim-accuracy`、`tdd-evidence-contract` 共 10 條 requirement、37 個 scenario 全部帶合法 ID。
  - `repo-guidance` 為 `REQ-PB` 加 `REQ-PB-S1`／`REQ-PB-S2`。
  - `contract-identity` 為 `REQ-1`–`REQ-8`。
  - 四個既有 capability 除了標題之外，與歸檔前逐行 diff 一致。
  - 在暫存複本上跑的 CLI JSON 數量，與從文字數出的數量一致。

  記錄以上各項的指令輸出。
- **Blocked by:** 5.1
- **Interfaces:** none

## 5.3 — Verification Strategy 試行紀錄

- **Delivers:** fixtures README 的結果表完整填好，並附一段試行觀察，作為後續研究題 `task-20260929-verification-strategy-research` 的第一份真實資料。
- **Acceptance:** 結果表每一列都對應一個 fixture 目錄，每一欄都沒有空值。觀察段逐題回答四個問題：regression 顯示了什麼、第二位執行者多抓到什麼、哪些規則出現不一致、哪些判斷值得升為 executable Gate；沒有資料可回答的題目寫「無」並說明原因。這個 task 的 diff 只動 fixtures README，沒有動正式設計或任何 spec。
- **Blocked by:** 3.1
- **Interfaces:** 消費 1.2 建好的結果表，以及 2.1、3.1 填入的判定。
