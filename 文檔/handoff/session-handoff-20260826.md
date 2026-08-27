# Session Handoff — 2026-08-26

## Session 18:15

### 一、本 session 主題

發現 `superpowers-bridge` 對 Superpowers v6.3.0 的 TDD 保證已失效，設計「規定證據取代規定步驟」的替代契約，經第三方審查後確認設計需重做。

### 二、完成事項

- **CLAUDE.md 大幅補強**（`9e9ea40`）：補上 repo 沒有 build/test/lint 的事實與唯一驗證指令、跨檔耦合表（最關鍵：`version-check.yml` 用 grep+awk parse README 的 Compatibility 表格，改格式會直接 fail CI）、兩個版本號的區別、CI 既有約定、下一代工作方向
- **在本 repo 安裝 OpenSpec + superpowers-bridge**（dogfooding）：`openspec init` 建目錄、bridge 以**實體副本**裝入 `openspec/schemas/`（實測 junction 過得了 validate 但 `openspec schemas` 掃不到）、副本與產生物已 gitignore
- **修好全域 OpenSpec profile**：原本 `custom` 只開 4 個 workflow，缺 bridge 依賴的 `verify`/`continue`/`new`/`ff`。已開到 11 個全集（`config set workflows` 不吃陣列，直接編 `config.json` + `openspec update`）
- **對 v6.3.0 做局部重新查證並落檔**（`3156806`）：8 個 skill 全在、設計觸點 #4 仍成立、code-review 仍成立（有條件）、**TDD 保證已失效**。刻意**不**推進 Compatibility 基準列——依 README 自訂規則，推進日期等同宣告「跑過完整 cycle 且沒退步」，而我們兩者皆非
- **記錄兩條既有實務規則**（`84cb2d6`）：Windows archive 目錄鎖 workaround、三軌制路由
- **走完 grilling 拷問**：定出 D1-D7 七項設計決策 + 四階段 roadmap
- **寫設計文檔並送第三方審查**（`15a2f2c`）：Codex 完成、**Gemini 失敗**
- **修正自己寫錯的宣稱**（`c134f1c`）：README 的 code-review 那列從 ✅ 改 ⚠️
- **install-harness**：七個目標全綠、CLAUDE.md 純新增 90 行未損壞既有內容

### 三、未完事項 / 接力棒

- [#接力] **重新設計 Change 2（TDD 證據契約）** —— 原設計 D1/D3/D4/D5/D6/D7 六項被推翻，需重來。完整交接在 `.handoff/2026-08-26-tdd-evidence-contract-redesign.md`
- [#接力] **Change 1（修正 TDD 錯誤宣稱）可照原計畫做** —— 不受推翻影響，且適合當第一次 dogfood 試跑
- [#待確認] **Gemini 訂閱類型** —— 決定第二視角救不救得回來
- [#待確認] **change 邊界判準要不要寫進 CLAUDE.md** —— 已討論出雛形但被 Codex 推翻「最細切法」，尚未寫入
- [#不重議] **階段二（Orca / execution-readiness / Coordinator）往後放** —— 本 session 已定案先修 bridge
- [#不重議] **`plan` 不刪除、只改寫法** —— 使用者明確要求保留 TDD
- [#已試失敗] **junction / symlink 裝 schema** —— `openspec schema validate` 過得了但 `openspec schemas` 掃不到，只能實體複製
- [#已試失敗] **升級 gemini CLI 到 0.57.0 解認證** —— 伺服器仍回 `free-tier` / `UNSUPPORTED_CLIENT`，是帳號授權問題不是版本問題
- [#已試失敗] **`openspec config set workflows` 傳逗號字串或 JSON 字串** —— 都回 `expected array, received string`，只能直接編 config.json

### 四、洞見 / 反省

**【紀律接力】**

- [#反] **我犯了自己 CLAUDE.md 裡「先讀『實際驗到什麼』再讀『名字說驗什麼』」那一條。** 我把「SDD 會 transitive 強制 code-review」寫成無條件成立，但 `SKILL.md:223-229` 明寫同形小任務要合併成一次 dispatch、diff 當一個單位審；`415-419` 又允許 park 掉真實 finding。我讀了保證的名字、沒讀它實際斷言什麼。
  attribute: 全域 CLAUDE.md「複審紀律」第 2 條。
  propose action: 寫任何「X 保證 Y」之前，先在來源檔案裡找**反例或例外條款**，找不到才准寫——與既有的「絕對斷言前先找反例」同源，但那條目前只涵蓋「所有 X 都會 Y」句式，未涵蓋「A 工具保證 B 行為」句式。建議把該條的觸發句式擴充。
- [#反] **宣告「Gemini 用不了」時我沒窮舉完就收手。** 使用者當場糾正「我有訂閱阿」。我看到 `IneligibleTierError` 就下結論，沒注意到函式名是 `throwIneligibleOrProjectIdError`——「或 ProjectId」那半我完全沒查。
  attribute: 全域 CLAUDE.md「宣告『沒有 / 不存在 / 做不到』前先列舉所有可能存放處逐一查完」。
  propose action: 錯誤訊息本身就是一個「可能存放處清單」——**看到錯誤先讀拋出它的原始碼**，函式名 / 分支條件會告訴你還有哪些路徑沒試。這是該條規則的一個新載體（前四次是篩選器 / 資料庫 / CLI / git repo，這次是 error message），累積 N=5。
- [#取捨] **第三腦機制這次推翻率遠超 30-50%** —— Codex 推翻六項設計決策中的六項。但它也有盲點：它斷言 PRECHECK 的 POSIX 指令在 Windows 不可攜，那對本機不成立（`!` 前綴與 Bash 工具都走 bash，全域 CLAUDE.md 早有記載）。**單一外部審查者仍需交叉驗證**，這次 Gemini 掛掉導致缺了那一半。

**【當日洞見】**

- [#決策] **不推進 Compatibility 基準列**：原計畫是把 `v5.1.0` 改成 `v6.3.0`，但 README 第 499 行自訂規則寫明「基準日期由 maintainer 重跑完整 cycle 確認沒退步後才推進」。我們沒重跑、而且找到退步，改數字等於偽造聲明。改成新增「重新查證紀錄」段，誠實記錄查了什麼、**還有什麼沒查**。
- [#偏離] **`schema.yaml` 的 `version:` 欄位在執行期什麼都不做。** `.openspec.yaml` 只存 schema 名稱與建立日期，沒有版本欄位，change 永遠解析到該名稱的當前版本。所以「升 v2 保護既有採用者」整個推理是錯的——要隔離必須換 schema 名稱。
- [#偏離] **`openspec archive -y` 對未完成任務連問都不問就歸檔**，且完全不檢查自訂 artifact graph。任何「blocking gate」寫在 prompt 裡都只是 policy，引擎層無強制力。
- [#偏離] **`post_apply` 不是「會報錯」是「validate 通過但靜默失效」**（實測確認）。zod 沒有 `.strict()`，未知欄位被丟棄。這比報錯危險——有人會加了它以為生效。
- [#決策] **D5 的論證是假兩難，我沒看出來。** 我說「scenario 層對照會逼測試名稱跟規格措辭綁死」，但可以用 ID 對應（`SCN-xxx → tests/x.py::test_y`），測試名不必等於 scenario 文案。用一個不存在的困境否決了可行方案。
- [#建議] **`~/.gemini/settings.json` 的 `general.defaultApprovalMode: "yolo"` 是無效值**（合法值 `default`/`auto_edit`/`plan`），每次跑 gemini 都印錯誤。未動，等使用者決定。

### 五、檔案異動

- `CLAUDE.md` — repo 慣例、跨檔耦合表、兩個版本號、CI 約定、下一代工作方向、dogfooding 說明、Windows archive workaround、三軌制路由；另 init-harness append 90 行
- `.gitignore` — 忽略 `openspec/schemas/`（bridge 實體副本）與 `.claude/commands/opsx/`、`.claude/skills/openspec-*/`（CLI 產生物）
- `superpowers-bridge/README.md` / `README.zh-TW.md` — 新增「重新查證紀錄」段（v6.3.0 局部查證 + 兩個未解漂移）；修正 code-review 宣稱
- `2026-08-26-TDD證據契約-設計結論-待第三方審.md` — 新增，D1-D7 設計 + 七個自陳攻擊點
- `2026-08-26-TDD證據契約-Codex審查與查證.md` — 新增，Codex 判決 + 我方獨立查證結果（分開記錄「自己重跑過的」與「憑論證接受的」）
- `.handoff/2026-08-26-tdd-evidence-contract-redesign.md` — 新增（gitignored），下個 session 的重新設計交接
- `openspec/`、`.workflow-harness.yaml`、`backlog.md`、`驗收節點.md`、`文檔/` — 新增（init-harness + openspec init 產生，**尚未 commit**）

### 六、下一步建議

1. **先 commit init-harness 的產出**（`.workflow-harness.yaml`、`backlog.md`、`驗收節點.md`、CLAUDE.md 的 90 行 append）—— 目前未追蹤，下個 session 開工前先落地比較乾淨
2. **跑 `/doctor-harness`** 確認 harness 安裝健康（init 的三提示之一，本 session 未跑）
3. **開始 Change 1**（修正 TDD 錯誤宣稱）—— 不受第三方推翻影響，且是低風險的 dogfood 試跑題目，可以順便驗證整條 opsx 流程在這個 repo 跑不跑得動
4. **Change 2 重新設計**前，先決定要不要救 Gemini 第二視角 —— Codex 這次在 Windows 可攜性那條判斷錯誤，顯示單一審查者不夠
5. **注意 CLAUDE.md 現在有兩套規矩並存** —— 上半是 repo 專屬（schema 維護），下半是 workflow-harness 通用。目前無直接衝突，但兩者都在講工作流程，若說法打架以 repo 專屬為準
