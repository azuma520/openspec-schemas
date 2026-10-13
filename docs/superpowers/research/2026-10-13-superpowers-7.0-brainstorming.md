# Superpowers 7.0.0 brainstorming 改寫：對 bridge 的影響與方向裁定

> 日期：2026-10-13
> 定位：working research，不是規範。§3 記錄維護者在討論中的裁定；正式改動走後續 opsx change（沿用 `task-20260826-fix-brainstorming-drift`），本文不改 `schema.yaml`。
> 前文：[2026-10-08-superpowers-6x-capability-gap.md](./2026-10-08-superpowers-6x-capability-gap.md)（S4–S6、S19 與 D1–D5 裁定）。

## 0. 證據來源與限制

- **讀的版本**：Superpowers `v7.0.0`，tag 指向 commit `bb92a77741419a4ab5f06e711a283343f1ada0c3`（2026-10-10，`gh api repos/obra/superpowers/commits/v7.0.0`）。
- **本機快取核對**：`~/.claude/plugins/cache/superpowers-marketplace/superpowers/7.0.0/` 的 `skills/brainstorming/SKILL.md` 與 `builder-check-prompt.md`，經 `diff` 比對，與 tag `v7.0.0` 的同名檔逐字相同。這個比對分辨得出差異：拿同一份 tag 檔去比 6.4.1 的快取，結果顯示不同。
- **讀了全文的檔案**：
  - [v7.0.0 brainstorming/SKILL.md](https://github.com/obra/superpowers/blob/v7.0.0/skills/brainstorming/SKILL.md)，225 行。
  - [builder-check-prompt.md](https://github.com/obra/superpowers/blob/v7.0.0/skills/brainstorming/builder-check-prompt.md)，23 行。
- **沒做的**：
  - 沒有實際跑過 7.0 的 brainstorming。§2、§3 都是讀原文推出來的。
  - 沒讀 7.0 的 `writing-plans`、`visual-companion.md`，也沒讀其他 skill。
  - 沒逐行比對 6.4.1 與 7.0 的全文差異，只比對了與 bridge 有關的段落。
- **官方 marketplace 現況**：仍釘在 6.4.1（commit `5bf4e78`），10/08 研究已實查。7.0.0 只能從作者自己的 marketplace（`superpowers-marketplace`）安裝。2026-10-13 的週檢 run 38326687799 回報上游最新版是 `v7.0.0`。

## 1. 7.0 與 bridge 有關的改動

| # | 6.4.1 | 7.0.0（行號指 v7.0.0 SKILL.md） | 對 bridge 的影響 |
|---|---|---|---|
| 1 | 三條路徑：spike／bounded／architectural，先分類並說出口 | 改成先問「我知道多少」（第 17–24 行），再依規模分三種：quick task／small change（設計寫在對話裡）／project（寫成設計文件），見第 129–143 行。spike 不再是一條路徑 | 10/08 D1「接受上游分類」的精神不變，只是分類的名字與內容換了 |
| 2 | 沒有跳過提問的出口 | 第一則訊息就告訴使用者可以跳過提問；使用者選跳過，skill 就此結束（第 30–34 行），HARD-GATE 也一併取消（第 186–187 行） | bridge 要的「寫進 brainstorm.md、寫完停下」可能整段被繞過 → §3 A |
| 3 | spike 是獨立路徑：調查後回報 | 討論中途可以做「用完就丟的試作」：不寫測試或只寫最少的、略過 plan／實作／review（第 104–110 行）；使用者同意後才能做，若要留下成果，算一個新請求、要重新過閘門（第 187–189 行） | 與「TDD 不可丟」、與「apply 之前不寫正式程式」之間的界線 → §3 B |
| 4 | 沒有 | 建造者檢查（第 160–177 行）：另派一個 subagent，以「要照文件規劃、但問不到作者」的身分，列出「非得猜、而且猜錯會有影響」的問題（prompt 第 14–17 行）。這些問題分三類：對話已回答的補進文件；小事由 AI 決定並標成「your call」；其餘歸使用者，一次問完。沒有 subagent 工具時，由 AI 自己用建造者的角度讀一遍 | 與 design instruction 允許推論（見 §2）直接相關 → §3 C |
| 5 | architectural 的前置條件：先核可書面 spec，再審閱實作計畫並選定執行方式 | 只剩「核可完整描述」（第 179–184 行），核可後直接接 `writing-plans`（第 191–192 行） | 10/08 D1 已記錄「實作計畫審閱」在 bridge 沒有明文對應；現在連上游都拿掉了 → §3 D |
| 6 | 設計文件寫在 `docs/superpowers/specs/`，並註明使用者偏好可以覆蓋 | 同上（第 156–158 行） | bridge 把輸出改導到 brainstorm.md，仍有上游原文支持 |
| 7 | 寫回理解 | 邊談邊複述：每懂一段就用約 200–300 字講回去；猜的部分要標成猜的（第 112–127 行） | 抓「寫錯的」，與建造者檢查抓「沒寫的」互補 |

另外，「AI 替使用者做的選擇，要寫成 AI 的決定，不得寫成使用者同意的」（第 64–65 行；Red Flags 第 200 行）這條原則在 7.0 是明文。

## 2. bridge 現況中與上述改動衝突的地方

- **brainstorm instruction 的「五步驟」描述**（`schema.yaml` brainstorm artifact，約第 59–64 行）：從 6.3 起就已經不成立（10/08 S4），7.0 下更不成立。
- **design instruction 允許推論**（約第 108–109 行）：原文是「Add Goals/Non-Goals and Migration Plan (may require inference from brainstorm.md content)」。這等於明文允許 AI 在 design 這一步補上沒有討論過的目標與範圍，正是建造者檢查想擋下的那種猜測。
- **plan 只要求自我審查**（plan instruction 約第 480 行「SELF-REVIEW before you finish」），apply instruction（約第 1739 行起）也沒有任何「使用者已看過 plan」的確認。2026-10-13 以不分大小寫的 `approv|user (has )?review|confirm with the user|ask the user` 搜尋 `schema.yaml`，只命中 brainstorm 五步驟描述裡的「Present design sections for approval」。檔內 confirm 另外出現 8 次（第 37、530、534、555、572、1748、1770、1877 行），都是 agent 自己做的檢查：skill／CLI 工具是否可用、verify 檢查項、PRECHECK，以及搬移外漏的設計檔前先確認內容已收進 change。沒有一處要求使用者審閱 plan 或確認開工。本 repo 的 plan.md 實際上會送 Codex 文件審，但這是 repo CLAUDE.md 與 sd0x 的規定，不是 bridge 自己的要求。
- **決策出處**：抽查 archive 中的 `2026-10-08-task-prefixed-plan-headings/design.md`，8 個決策裡有 4 個標了 brainstorm 出處（D1、D2、D4、D7），另外 4 個沒標。本 repo 已經部分做到溯源，但那是維護者的 CLAUDE.md 帶出來的習慣，bridge 本身沒有要求。

## 3. 維護者裁定（2026-10-13）

各題都採「只改 instruction 散文、不新增 verify 檢查、不升 schema major」，延續 10/08 D2。

| 題 | 裁定 | 要點 |
|---|---|---|
| 方向 | **甲：instruction 不綁上游版本**，附加條件 | 只寫 bridge 需要的結果：使用者核可過的內容要原樣寫進 brainstorm.md，寫完停下，不接 writing-plans、不實作。不再描述上游的步驟。**附加條件（使用者補充）：仍然必須真的呼叫 brainstorming skill，經過討論、收斂出決策，不可以由 AI 直接寫 brainstorm.md**；現有的 skill PRECHECK 保留。10/08 D4（以 6.4.1 為驗證目標）不變 |
| A：使用者要跳過討論 | **乙** | AI 不主動提出可以跳過。使用者自己要求跳過時，AI 說明兩件事：change 這條路需要討論；若真的不需要討論，這件事可能本來就不該開 change（README § When NOT to enter the schema）。使用者仍堅持時，AI 依然要先了解現況、提出實作建議，寫進 brainstorm.md 並標明「AI 判斷、未經討論」，然後停下，等使用者說繼續 |
| B：討論中途試作 | **甲：允許，附三個條件** | ① 試作程式不進該 change 的 commit，用完即丟；② 學到的東西寫進 brainstorm.md，附上實際執行的指令與輸出；③ 要正式採用的部分，到 apply 用 TDD 重寫，不可直接搬用。TDD 規範的是交付出去的程式，試作不交付，所以兩者不衝突 |
| C：未知盤點與溯源 | **採用** | ① brainstorm 收尾前做未知盤點：以下一步（proposal／design／specs／tasks／plan）的角度，找出「非得猜、而且猜錯會有影響」的地方，依建造者檢查的三類處理；使用者暫時不決定的，明列為待決問題。盤點結果（找到什麼、各自怎麼處理）寫進 brainstorm.md。bridge 規定的是這份紀錄，不規定要派 subagent：上游 7.0 已做過建造者檢查的，沿用其結果；6.4.1 由 AI 自己用建造者的角度讀一遍。② design 不得默默推論：刪掉「may require inference」；brainstorm.md 沒有的內容，要嘛標成 AI 推論，要嘛放進 §Open Questions。③ 目的是**溯源**：每個決策都能追到出處——使用者在討論中定的（指出 brainstorm 哪一段）、AI 的決定（標明）、或尚未決定 |
| D：動手前的確認 | **採用：apply 開始前停下並確認** | AI 先講清楚三件事：plan 是誰審的（獨立 AI 審查並附結論／使用者自己看過／都沒有，照實寫，不得把沒審寫成審過）；審查還有沒有未處理的問題；最後問使用者要開始，還是先自己看 plan.md。**審查者由使用者選**：維護者的習慣是「討論過，或 AI 審過，沒問題就開始」，也有使用者會想自己看。唯一不允許的是誰都沒審就開始；若要這樣做，使用者必須明說，而且要留下紀錄。審查者、結論、使用者的開工指示都記進 change 紀錄。先以 instruction 落地；若 6.x 驗證輪觀察到 AI 會跳過，再考慮改成機器檢查（那時會牽動 schema major，需重新裁定） |

### 3.1 本機切換到 7.0（同日裁定）

- 只在本 repo 切換，全域維持 6.4.1。理由是全域切換會改變其他專案的 brainstorming 行為，而那些專案沒有人在觀察。
- 做法：新增 `.claude/settings.local.json`（全域 git ignore 已排除、不進版控），關閉 `superpowers@claude-plugins-official`，開啟 `superpowers@superpowers-marketplace`（7.0.0）。追蹤中的 `.claude/settings.json` 不動。
- 目的：讓後續 brainstorming change 在 7.0 下 dogfood，取得 §3 各題的實跑證據。
- 與 D4 的關係：D4 規定「以 6.4.1 實際跑完整流程」做驗證。這一輪要在切換前跑完，或是到時候切回 6.4.1 再跑；兩條路都還開著，本次不決定。
- **未驗證**：專案層 local 設定能否覆蓋全域的 `enabledPlugins`。需要重開 session，看實際生效的版本才知道。

## 4. 待查

1. 7.0 `writing-plans` 是否自帶 plan 審查。這會影響 D 題「獨立 AI 審查」可以由誰擔任。
2. 採用者手上沒有 Codex 時，D 題的獨立審查用什麼工具做。
3. 6.4.1 的 spike 路徑是否包含動手寫程式。B 題只讀了 7.0。
4. §3.1 的專案層設定能否覆蓋全域。
5. 過去 change 的 design.md 裡，有沒有「AI 的決定被當成使用者決定」而造成問題的實例。C 題目前是預防性的，沒有事故佐證。
6. `/opsx:ff` 跑完後，AI 會不會在同一輪直接進入 apply。這延續 10/08 S5 的「沒查的」。

## 5. 後續

- 方向與 A–D 併入 brainstorming 對齊的 opsx change（`task-20260826-fix-brainstorming-drift`）；S19 依 10/08 §4.1 處理，在 proposal／tasks 裡列為獨立的小範圍修正。
- D 題會動到 apply instruction，C 題會動到 design instruction。兩者都超出原本「只改 brainstorm」的範圍，開 change 時要在 proposal 寫明。
- 6.x 驗證輪（10/08 §4.2）新增觀察項目：A 的跳過處理、C 的未知盤點紀錄、D 的開工確認，三者 AI 是否照做。
