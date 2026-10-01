<!--
任務編號即 plan.md 的 entry key（check 12：兩邊各自不重複，再比集合相等）。

【順序：RED 是硬前置】
群組 2 的 RED 盲測必須在群組 3 任何一處修改 superpowers-bridge/schema.yaml 之前完成，
plan.md 要把它寫成阻斷依賴（3.1 被 2.1 阻斷），不能只是說明文字。
理由要寫對：舊規則文字事後用 git show 仍拿得回來，所以不是「技術上補不回」；
而是 RED 記錄的是「修改前實際跑過、當時判錯」這個歷史事實——改完再拿舊文字重跑，
就不再是修改前取得的 RED（tdd-evidence-contract 與 design D9）。

【TDD applicability 的依據】
採 2026-09-07 使用者對 fix-v2 的裁定（行為判準）與本 change design D9：
新增 check 13 規則文字的 task 標 applicable；只有「舊 verify（checks 1–12）判定與新契約不一致」
的 fixture 才是 TDD subject，subject 寫法沿用 fix-v2：`<fixture 目錄>::<預期判定>`。
舊判定已與新契約一致者（正向對照、或已被 checks 1–12 以其他理由擋下者）只作 conformance evidence，
不記 RED。⚠️ 這點刻意與 fix-v2 的 f12 前例不同（f12 的 RED 記 INDETERMINATE）——D9 已定，此處再提醒一次。
「舊 verify 會放行缺 ID fixture」目前仍是推論，由 2.1 實跑確認；若實跑推翻這個前提，停下回報使用者，
不自行改寫 applicability。

【盲測執行裁定（2026-09-30 使用者拍板：決定一 B、決定二 C）】
- 寫 fixture 的人只負責建案例、保存預期答案、做打亂命名與對照表；判定一律交給對本 change
  無設計脈絡、看不到預期答案的 subagent。
- RED：1 位盲測執行者，對修改前規則跑一次，取得真實 baseline。
- GREEN／conformance：2 位互相獨立的盲測執行者各跑一次。實驗條件相同——同一模型（派工時明確指定、
  寫入結果表，不靠預設值）、同一份 blind prompt、同一份 fixture 副本、同一規則來源、同一操作程序；
  差別只在各自獨立的 context。
- 執行者只拿到：fixture 副本＋凍結的規則文字＋固定操作指示。不得告知「此 fixture 在 RED 判錯」
  或任何預期判定；RED 同樣如此。
- 兩位 GREEN 判定不一致：不投票、不取多數、不找第三人。記為「判定不穩定／rule ambiguity detected」，
  該 fixture 不算 GREEN、該步驟 BLOCK，回頭查規則歧義、讀錯狀態、操作程序不夠固定，
  或這類判斷已不適合留在文字規則層。
- 兩位一致但與預期不符：同樣不算 GREEN，依同一清單查因。
- 不做統計實驗（不跑 5 次、10 次、不算一致率）；本次只問「第二個獨立判定者會不會暴露第一個看不出的不穩定」。
- 執行者逐條回報 checks；PRECHECK 與 check 5 讀 repo 的 git 紀錄，fixture 天生無法滿足，
  標「不適用於 fixture」。RED 要回答的是「checks 1–12 有沒有任何一條抓到這個身分缺陷」，
  不是整份 verify 過不過。

【不在本檔】
- archive 後 `openspec/specs/contract-identity/spec.md` 的 `## Purpose` 會是 CLI 產生的 TBD，
  要另補正式說明（loosen-plan 前例）——archive 之後的 follow-up，不是本 change 的 task。
- 證據名稱照實寫：fixture-based behavioural verification, agent-executed，不寫成測試框架執行；
  TDD evidence 成立不提高 assurance（contract-identity REQ-8）。
-->

## 1. 身分 mutation fixtures 與盲測器材

- [x] 1.1 在 `docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/fixtures/` 建立 fixtures（不併入舊的 f1–f13）。每個 fixture 是一個自足的迷你 repo：`openspec/specs/` 主 spec ＋ `openspec/changes/<name>/` 一個 change（delta spec 與使 checks 1–12 可判讀所需的其餘 artifact，全部合規）。正向對照 fixture 不含身分缺陷；違規與無法判定 fixture 只引入一個身分相關的 mutation source（一個 mutation 必然連帶觸發多條規則時可以接受，見 plan.md 1.1）。涵蓋規則：`contract-identity` spec 中每個 THEN 是 identity check 判定的 scenario，至少對應一個 fixture——違規類 REQ-1-S2、REQ-1-S3、REQ-1-S4、REQ-2-S3、REQ-2-S4、REQ-3-S2、REQ-3-S3、REQ-3-S4、REQ-3-S5、REQ-4-S2、REQ-4-S3、REQ-6-S2、REQ-6-S3、REQ-6-S4、REQ-7-S2、REQ-7-S3（完成的比對不一致記為違規）；無法判定類 REQ-5-S2（預演歸檔失敗）、REQ-7-S1（無法判定不記為違規）；正向對照 REQ-1-S1、REQ-1-S5、REQ-2-S1、REQ-2-S2、REQ-3-S1、REQ-3-S6、REQ-4-S1、REQ-4-S4、REQ-4-S5、REQ-5-S1（補號遷移 change）、REQ-6-S1，以及宣稱邊界對照 REQ-4-S6、REQ-8-S2（check 不讀歷史，重用退休號不被擋）。REQ-7-S1／S3 判的是 BLOCK 的類別，可由判同一情形的違規／無法判定 fixture 兼任，不必另建；REQ-8-S1、S3–S5 判的是文件表面與證據紀錄、不是 check 判定，不需要 fixture。一個 fixture 可涵蓋多個正向 scenario；違規 fixture 一次只引入一個 mutation source。某個 scenario 若在 openspec 1.3.1 下造不出來（例如造不出「文字數得到、CLI 看不到」的標題行），記下實測過程與結論作為覆蓋缺口，不硬湊
  - TDD: n/a — fixtures 是 3.1 的受測素材，不是受測對象；其正確性由 2.1／3.1 的盲測判定與預期答案比對呈現
- [x] 1.2 寫 fixtures README：①預期答案表（fixture／破壞了什麼／預期判定：通過，或 BLOCK 並註明「違規」或「無法判定」；一個 fixture 同時觸發兩種時兩種都寫）②`contract-identity` scenario → fixture 覆蓋對照表，含 1.1 記下的覆蓋缺口 ③結果表，欄位至少：fixture、預期判定、RED 實際、GREEN 執行者 A、GREEN 執行者 B、A/B 是否一致、不一致或失敗的類型 ④怎麼重跑（比照 `2026-09-03-tdd-evidence-mutation-fixtures/README.md`「怎麼重跑」）
  - TDD: n/a — prose/doc-only；以「每個 fixture 目錄都有一列、每一列都有目錄」與「覆蓋表的每個 scenario ID 都存在於 contract-identity spec」兩項對讀驗證
- [x] 1.3 準備盲測器材並在 2.1 開跑前凍結：打亂命名的 fixture 副本（中性名稱，放在 repo 之外的暫存目錄；RED 與 GREEN 各自重新打亂，GREEN 兩位執行者拿同一份）、打亂名 ↔ 原名對照表（不交給執行者）、固定的 blind prompt（只描述輸入與回報格式：逐 fixture、逐 check 回報判定與理由，BLOCK 時分「違規」與「無法判定」；PRECHECK 與 check 5 回報「不適用於 fixture」）、固定操作程序、規則來源的取得方式（RED＝修改前 commit 的 verify instruction，以 `git show <base commit>:superpowers-bridge/schema.yaml` 取得並記下 commit；GREEN＝3.1 寫入 check 13 後的 verify instruction）。prompt 與程序在 RED、GREEN 之間只有規則來源這一個變數
  - TDD: n/a — 實驗器材準備；控制方式是器材凍結後的內容雜湊或全文存檔，事後可比對 RED／GREEN 用的是同一份 prompt 與程序
  - 驗收紀錄：approved deviation — 「RED 與 GREEN 之間只有規則來源一個變數」未逐字成立：RED（2.1）用 prompt v1，GREEN（3.1）用 prompt v2（器材修正，只改回報格式）；使用者裁定 RED provenance 採混合，另以 replay（prompt v2＋修改前規則）取得同器材對照，22/22 與 original RED 一致。plan 1.3 原文保留不改。見 `docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/README.md` §3b、`sdd-ledger.md` 第 81、86 行

## 2. RED：修改 schema 前的盲測 baseline

- [x] 2.1 以 1 位盲測執行者（明確指定模型並記錄；RED 與 3.1 的兩位 GREEN 執行者用同一個模型）、修改前的 verify 規則（checks 1–12）跑全部 fixtures，把每個 fixture 的實際判定寫進結果表「RED 實際」欄。據此決定 TDD subject：舊判定與預期判定不一致者列為 3.1 的 subject；一致者（正向對照、或已被 checks 1–12 以其他理由擋下者）只作 conformance evidence。若結果推翻「舊 verify 會放行缺 ID fixture」這個前提，停下回報使用者。本 task 完成前，不得修改 `superpowers-bridge/schema.yaml`
  - TDD: n/a — 取得 RED 的盲測執行步驟；RED 紀錄寫在 3.1 底下，本 task 產出的是結果表與 subject 清單
  - 盲測紀錄：RED 執行者模型 sonnet（claude-sonnet-5），2026-09-30；原始回報與對照表見 docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/blind-runs/red/

## 3. schema.yaml：check 13、specs 作者規則、schema major 3

- [x] 3.1 在 verify instruction 新增 check 13（identity integrity），並以雙人盲測取得 GREEN。規則內容對應 `contract-identity` REQ-1 至 REQ-8 與 design D2–D6：語法、改名保 ID、同一契約依操作角色判定、新號檢查層、候選狀態＝暫存複本實跑 `openspec archive <change> -y`（不加 `--skip-specs`）、CLI 交叉核對（候選狀態在暫存複本、預演歸檔後跑；change 層對歸檔前狀態跑）、BLOCK 分「違規」與「無法判定」且皆不得降級、宣稱邊界。規則文字要寫明兩個 openspec 1.3.1 實作細節：`openspec show <change> --json --deltas-only` 只讀 stdout（stderr 會有 `Warning: Ignoring flags not applicable to change: scenarios`，混讀會解析失敗而被誤判為無法判定）；change JSON 中 ADDED／MODIFIED 條目的 scenario 陣列欄位是 `requirement.scenarios`。規則寫入後做 GREEN／conformance 盲測：2 位互相獨立的執行者（與 2.1 同一模型並記錄、同一 blind prompt、同一 fixture 副本、同一操作程序），以寫入 check 13 後的 verify 規則各跑一次全部 fixtures，填結果表「GREEN 執行者 A／B」「是否一致」欄。兩位一致且符合預期的 subject，在本 task 底下各寫一筆 GREEN（每個 subject 只寫一筆，`invocation:` 註明兩次執行）；不一致或不符預期者不寫 GREEN，記錄類型（規則不清、讀錯狀態、CLI 資料不足、操作對應不清、忽略規則、重跑不一致）後修規則，修完兩位執行者都以新的打亂副本重跑。非 subject 的 fixture 結果只作 conformance evidence。2.1 列出的每個 subject 都取得一致且符合預期的判定、寫完 GREEN，才勾選本 task
  - TDD: applicable
  - RED:
    - subject: u01-modified-no-match::BLOCK {無法判定}
    - outcome: FAIL
    - failure: expected BLOCK {無法判定}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: u01-modified-no-match::BLOCK {無法判定}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {無法判定}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v01-req-no-id::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v01-req-no-id::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v02-scenario-no-id::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v02-scenario-no-id::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v03-id-no-description::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v03-id-no-description::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v04-prefix-mismatch::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v04-prefix-mismatch::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v05-rename-changes-id::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v05-rename-changes-id::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v06-migration-non-numeric::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v06-migration-non-numeric::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v07-added-existing-id::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v07-added-existing-id::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v08-main-two-blocks::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v08-main-two-blocks::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v09-two-added-same-id::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v09-two-added-same-id::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v10-dup-scenario-id::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v10-dup-scenario-id::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v11-added-non-numeric::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v11-added-non-numeric::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v12-added-below-max::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v12-added-below-max::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v13-main-req-in-fence::BLOCK {違規, 無法判定}
    - outcome: FAIL
    - failure: expected BLOCK {違規, 無法判定}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v13-main-req-in-fence::BLOCK {違規, 無法判定}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規, 無法判定}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v14-main-sc-in-fence::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v14-main-sc-in-fence::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v15-delta-sc-in-fence::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v15-delta-sc-in-fence::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - RED:
    - subject: v16-skip-request::BLOCK {違規}
    - outcome: FAIL
    - failure: expected BLOCK {違規}, actual PASS {} under checks 1–12 (original RED, blind executor sonnet, prompt v1, before the schema edit; blind-runs/red/)
    - invocation: blind executor per blind-kit/prompt.md (v1), rule git show 42c3d24:superpowers-bridge/schema.yaml
  - GREEN:
    - subject: v16-skip-request::BLOCK {違規}
    - outcome: PASS
    - invocation: two independent blind executors (sonnet A, B) per blind-kit/v2/prompt.md, rule schema.yaml sha256 a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504 (final check 13, rerun 2026-10-01); both reached BLOCK {違規}; graded by blind-kit/v2/grade.py fix round 2 (blind-runs/v3-green/)
  - 驗收紀錄：approved deviation — 上方 RED 的 invocation 為 prompt v1、GREEN 為 prompt v2，與 plan 1.3「只有規則來源一個變數」不逐字相符；處理與證據同 1.3 的驗收紀錄（replay 22/22 與 original RED 一致）。
  - GREEN 後修改紀錄（2026-10-01，歷史敘述）：① 全分支總審 r1 後，verify instruction 在 check 13 本體以外改了兩處（FRESHNESS 段加入 check 13 例外句、check 13 前加區塊標題 `CHECK 13 — CONTRACT IDENTITY.`）；當時 check 13 本體（從 `13. **Identity integrity**` 那行到 `REVIEW JUDGEMENTS` 前一行，含該空白行；LF 換行、每行含尾端換行）的 sha256 仍是 `b5d970761e166fbd281e96db116a9ea97307da06cc90f5658d96190ff7380c90`，與原 GREEN 規則檔 `blind-runs/green-r2/schema-green-r2.yaml`（f2eea915…）相同。② 其後 Codex code review r1 發現 check 13 本體內 I3（已 sync capability）分支的互斥句（13.B SYNCED CAPABILITY 清單與 13.E 開頭把 13.E 比對列為無法判定，INTERACTION 段卻說 preview 成功時照常比對），使用者裁定修正以對齊 I3 裁定（只有依賴 pre-sync 基準的判斷記無法判定；13.E 兩半都不讀 pre-sync 主 spec），check 13 本體因此改變（span sha256 `026648370fbcf15e0ee27f9afd4cf87433d38a3d4f13f3420dc75e4660cfe5d4`）。**最終 ship 的 check 13 已不同於原 GREEN 盲測文字**；原 GREEN（`blind-runs/v2-green/`）保留為 provenance，不再作為最終文字的直接證據。③ 使用者裁定對最終文字重跑 GREEN（不是重試到過：被測物改變了）：規則檔 `schema.yaml` sha256 `a78e207c4fe5f7482424577d31b35e654866d7bbaaeee71d1f32f0788d012504`（副本 `blind-runs/v3-green/schema-green-v3.yaml`），器材 v2 prompt／procedure 不變、grader 為 fix round 2，兩位全新 sonnet 執行者 A、B，重新打亂（seed 87309），A、B 皆 MATCH 22／DIFF 0／NONCONFORMING 0、FINAL 逐案相同，跑完 kit 雜湊未變（`blind-runs/v3-green/`）。上方 17 筆 GREEN 紀錄指向這次重跑。
  - 證據限制：I3 分支（已 sync 的 capability）**不在**凍結的 22 個 fixture 涵蓋範圍內——沒有任何 fixture 讓 check 3 記為 ✓ Already synced。因此這次重跑的 22/22 只證明「修正後的 check 13 沒有破壞既有 22 個案例」，**不證明** I3 分支本身經過盲測驗證。
  - I3 定點驗收（2026-10-01，使用者裁定；凍結 22 案例盲測組**之外**的 post-fix I3 focused acceptance — 2 paired cases，不是第 23、24 題）：為補上一條限制而另做兩個成對案例（`docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/focused-i3/`）——`i3-mixed-synced-and-violation`（A 已 sync 使歸檔預演中止，B 只依賴歸檔前狀態的違規仍保留，預期 BLOCK {違規, 無法判定}）與 `i3-synced-only`（A 已 sync 進 main 的 `REQ-1` 不得被判成衝突，預期 BLOCK {無法判定}）。單一案例時「A 被誤判成衝突」不改變 FINAL，因此拆成兩題；派工前先以假報告證明評分器分得出兩條錯誤路徑。規則檔同上（`a78e207c…`），器材 v2 prompt／procedure 與 fix round 2 grader 不變，一位全新 sonnet、一次跑完、不重試：MATCH 2／DIFF 0／NONCONFORMING 0，跑完 kit 雜湊未變（報告 `focused-i3/report.md`）。證明範圍：最終 check 13 在這兩個 I3 狀態下能被一位執行者執行出已裁定的語意（依 capability、依證據依賴局部退化；已 sync 的 ID 不成為違規）；評分只讀 FINAL 行，單一執行者、單次樣本。**不**擴大凍結盲測組的範圍，也不涵蓋其他 I3 形狀（例如預演成功的已 sync MODIFIED delta）。
- [x] 3.2 更新 `specs` instruction：標題語法（`### Requirement: <REQ-ID> <description>`、`#### Scenario: <REQ-ID>-S<m> <description>`）、改名保 ID（RENAMED 的 FROM／TO local ID 必須相同，唯一例外是補號遷移）、新號配置兩層（檢查層由 check 13 驗；發號層要求作者連同 `openspec/changes/archive/` 的 delta spec 查歷史最大號、往上取，check 13 不驗這一層）。並將 `version:` 改為 3
  - TDD: n/a — 作者表面的規則文字，本 change 沒有可重跑案例驗證作者行為；以逐句對讀 contract-identity REQ-1、REQ-2、REQ-4 驗證，並以 1.1 的 fixtures 不需改寫、照樣成立作旁證

## 4. 連動表面（依 repo CLAUDE.md 跨檔耦合表）

- [x] 4.1 更新 `superpowers-bridge/templates/spec.md`（標題範例帶 ID、RENAMED 範例示範保 ID）與 `templates/verify.md`（新增 check 13 段落：兩種 BLOCK 分開記錄、宣稱邊界摘要並指向 spec）
  - TDD: n/a — template prose；以機械比對 schema 與 template 中 check 13 的標題（同編號、同標題；checks 1–12 不在本 task 改動範圍，既有標題差異不列入）驗證，並在一次性專案複本中分別跑 `openspec instructions specs --change <change>` 與 `openspec instructions verify --change <change>`，兩者 render 成功且含新文字
- [x] 4.2 同步更新 `superpowers-bridge/README.md` 與 `README.zh-TW.md`：標題格式說明；列舉 verify checks 之處補 check 13 與宣稱邊界摘要（連到 contract-identity spec，不另寫一份完整規範）；Versioning 表改 `version: 3`／`3.0.0`，Meaning 欄與既有「原本合法的 artifact 變不合法即 breaking」判準一致；新增「Why v2 → v3」與「Migrating v2 → v3」（依 design Migration Plan：一個補號 change 涵蓋所有 capability、不可按 capability 分批）；Compatibility 表在 v2 列之上新增 v3 列（OpenSpec／Superpowers 版本填實際驗過的版本並附驗證紀錄，不照抄 v2 列），v2、v1 列保留；Known breaking changes 新增 v2 → v3；其餘描述「現行」schema major 或 bundle release 的句子（例如 Current bundle release `2.0.0` 那句）一律改為 v3／`3.0.0`，描述歷史的 v1 → v2 紀錄保留不改
  - TDD: n/a — prose/doc-only；以逐句對讀 schema 與 contract-identity spec 驗證，並重跑 `version-check.yml` 的 grep／awk 指令確認取得 v3 列的兩個版本；兩份 README 的 `v2`／`2.0.0` 殘留逐筆判讀為「歷史紀錄」或已更新
- [x] 4.3 更新其餘寫死 v2 之處：`superpowers-bridge/VERSION` → `3.0.0`；`.github/workflows/version-check.yml` 的列鍵 grep 由 `v2` 改 `v3`；repo `CLAUDE.md` 的結構樹 VERSION 行、跨檔耦合表 Compatibility 列、「兩個版本號別搞混」兩列與列鍵說明句，以及 schema major 的 bump 判準句與 README 判準一致；`docs/roadmap.md` 與 `.zh-TW.md` 新增 v3（Identity）條目；根目錄 `README.md` 與 `README.zh-TW.md` bridges 表中 `superpowers-bridge` 的版本欄 `v2` → `v3`
  - TDD: n/a — configuration / prose；以重跑 workflow 的 grep／awk 指令取得版本、並對 `v2`／`2.0.0` 殘留逐筆判讀（歷史紀錄保留、現行描述更新）驗證

## 5. 收尾：用新規則判本 change 自己

- [x] 5.1 同步 dogfood 副本（`openspec/schemas/superpowers-bridge/` 與 `superpowers-bridge/` 內容一致），`openspec schema validate superpowers-bridge` 與 `openspec schemas` 成功，`openspec instructions verify --change requirement-scenario-identity` render 出的內容含 check 13
  - TDD: n/a — configuration / copy step；以 `diff -r` 為空作控制（只抽查標題看不到規則內文的差異）
  - 驗收紀錄：見 `docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/migration-acceptance.md`
- [x] 5.2 補號遷移驗收（design D7）：在暫存複本對本 change 實跑 `openspec archive requirement-scenario-identity -y`，預演歸檔後的主 spec 中 `plan-contract`、`tdd-claim-accuracy`、`tdd-evidence-contract` 共 10 條 requirement、37 個 scenario 全部帶 ID，`repo-guidance` 為 `REQ-PB`＋`REQ-PB-S1`／`REQ-PB-S2`，`contract-identity` 為 `REQ-1`–`REQ-8`；這四個既有 capability 的內文除標題外與歸檔前逐行一致；CLI 數量交叉核對一致
  - TDD: n/a — 遷移驗收的一次性實跑；記錄的指令輸出即證據
  - 驗收紀錄：approved deviation — repo-guidance 有 3 行純空白差異，非空白內容確認一致，見 `docs/superpowers/poc/2026-09-30-identity-mutation-fixtures/migration-acceptance.md`
- [x] 5.3 Verification Strategy 試行紀錄：結果表完整（無空欄），另附簡短觀察——regression（RED→GREEN）顯示了什麼、兩位 conformance 執行者多抓到什麼、哪些規則出現不一致、哪些判斷值得日後升為 executable Gate。只記觀察，不修改正式設計或既有契約
  - TDD: n/a — prose/doc-only record；以結果表每列對應一個 fixture 目錄驗證
