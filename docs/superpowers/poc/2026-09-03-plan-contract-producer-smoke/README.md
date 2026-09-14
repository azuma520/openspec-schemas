# Plan Contract 產出器 smoke test（2026-09-03，run 2）

> 由 change `loosen-plan`（已 archive：[`openspec/changes/archive/2026-09-04-loosen-plan/`](../../../../openspec/changes/archive/2026-09-04-loosen-plan/)）task 10.4 產出。
> 完整記錄見該 change `verify.md` §11；本目錄保存的是**可重跑的最小資產**。
>
> **與姊妹目錄的分工**（[`../2026-09-03-tdd-evidence-mutation-fixtures/`](../2026-09-03-tdd-evidence-mutation-fixtures/)）：
>
> | 資產 | 驗的是 |
> |---|---|
> | mutation fixtures | 檢查器**會不會判對**（消費端） |
> | 本目錄 | Plan Contract 產出器**會不會產對**（產出端） |
>
> 保留範圍由使用者裁定（2026-09-04）：只留實測有效、可低成本重跑的資產，不為保存歷史而全存。

## 測什麼

給一個無脈絡的產出者：v2 的 `plan` artifact 指令（含 `<template>`）＋ 一份 `design.md` ＋ 一份 6 步的 `tasks.md`，看它產出的 `plan.md` 符不符合 Plan Contract。**沒有任何提示或指導**（no coaching）。

⚠️ **`design.md` 是怎麼交付的，保存下來的刺激物沒有記錄。** `rendered-plan-instruction.txt` 的 `<dependencies>` 只宣告了 `<dependency id="tasks">` 一項並附路徑（`:12–15`）；`design.md` 只在**散文**裡出現三次（`:24`、`:38`、`:112` 的 Pointers 說明），沒有對應的 dependency 條目或路徑。產出者顯然讀到了它（產出物逐一引用 D1–D4），但**交付機制不在紀錄裡**——重跑時要自己決定怎麼給，並且知道這一點本身就是與原run 的一處差異。

## 目錄內容

| 檔案 | 角色 |
|---|---|
| `inputs/design.md`、`inputs/tasks.md` | 餵給產出者的輸入（虛構的 rate-limit 功能，6 步：1.1、1.2、2.1、2.2、3.1、3.2） |
| `rendered-plan-instruction.txt` | 產出者收到的**刺激物原樣**——CLI 算出的完整 artifact block，含 `<template>` |
| `produced-plan.md` | 產出者的**實際輸出**，未經修改 |

⚠️ `rendered-plan-instruction.txt` 第 13、19 行帶有當時 session 的**絕對路徑**（`C:\Users\user\AppData\...\scratchpad\`）。刻意保留原樣——它就是當時真正餵進去的東西，改了就不再是被測的那個刺激物。**重跑時必須重指這兩條路徑。**

## 預期行為（run 2 的五項判定，由不知道 run 1 存在的評分者給出）

| # | 判準 | 結果 |
|---|---|---|
| 1 | entry-key 集合相等 | **yes** —— `{1.1,1.2,2.1,2.2,3.1,3.2}` 雙向皆空差集 |
| 2 | 無模糊驗收語言 | **no** —— entry 1.1 寫「a default resolution behaviour (e.g. client IP) is defined」，沒指名任何可觀察的東西，而 design.md D2 其實已把那個 default 訂死 |
| 3 | 有耦合就寫 Interfaces、沒耦合就省略 | **no**，一處錯誤省略（見下） |
| 4 | 無步驟指定 | **yes** —— 兩個邊界案判為允許：逐字取自 tasks.md 的路徑、以及作為「決定性形狀」的函式簽名 |
| 5 | 證據不出現第二份拷貝 | **yes** —— 連契約允許的 echo 都沒用 |

**重跑時 2 與 3 判成 `no` 才是符合預期的**——這不是壞掉，是這份輸入已知會踩到的兩個點。判成 `yes` 反而要回頭查產出者是不是被洩題了。

### 這次真的抓到的東西（不是假想測試）

- **§11.3 的結構性發現**：契約條文說 global constraints 要「copied **verbatim** from the specs」，卻**沒有為「這個 change 沒有 `specs/` 目錄」留任何 fallback**。產出者只能自己挑一個來源。兩位評分者在兩套不同儀器上各自獨立撞到同一點，所以**與儀器是否健全無關**。這是條文缺陷、不是產出者缺陷，並以 WARNING 形式寫進了該 change 的 Overall Decision。

  ⚠️ **archived `verify.md` 對產出者行為的描述不正確，以本段為準——該句在該檔出現兩次**：`:419`（§11.3）與 `:649`（`## Overall Decision` 底下的 WARNING 區塊，只讀 archive 的人最可能讀到的那一段）。兩處都寫產出者「silently relax *verbatim* to *drawn from*」，但對照 `produced-plan.md` 三項皆不成立——`:10` 用一整段 **Pointers 明講**「This change has no `specs/` directory. The source used ... is `design.md`」（**不是 silent**）；`:12` 寫的是「Global constraints (**verbatim** from design.md…)」且逐條帶實際引號（**verbatim 保住了**）；全文 `drawn from` 出現 **0 次**。被放寬的是**來源**（specs → design.md），不是 verbatim 本身。**結構性發現不受影響**——`:10` 那行正是它的證據。
- **Interfaces 省略的機制**：欄位措辭是 **consumer-first**，而一個寫在它的消費者之前的 entry 沒有東西可以「consume」——1.1 的**實際消費者**反而都正確指名了它（1.2 於 `produced-plan.md:40`、2.2 於 `:61`），因為輪到它們時另一端已經在紙上了。（不是「後面每個 entry 都指名 1.1」——2.1 `:50` 指的是 1.2，3.1 `:71` 指的是 1.2 與 2.1，各自指向自己真正的上游。）**逐 entry 問它自己的邊，會讓「只有上游」的那個 entry 成為唯一看不見真實邊的位置。** 群 10 的複審者從另一側得到同一結論：這個省略**會通過複審**，因為只有複審者自己建出耦合圖才看得見它。

### 已知限制（重跑前先讀）

- **N=1**：一個產出者、一次執行。**change 自己的** design.md（[`archive/2026-09-04-loosen-plan/design.md:38`](../../../../openspec/changes/archive/2026-09-04-loosen-plan/design.md)，D3「Producer: agent direct generation」）列了四個升級觸發條件，其中兩個是關於「復發」與「變異」，單次執行按定義證明不了。
  ⚠️ 別跟本目錄 `inputs/design.md` 的 D3 搞混——那是 fixture 輸入裡的「Resolution happens at registration」，與觸發條件無關。本檔其他地方單寫 `design.md` 都是指 `inputs/design.md`；**只有這一條指的是 change 自己的那份**。
- **不是乾淨的 fresh-context run**：render 的 `<output>` 路徑指向一個同時裝著 bundle 的 scratch 專案，沒有任何機制強制「只讀輸入」。當時評分者已界定它容許得出什麼結論——bundle 裡**沒有任何一份寫好的合規 plan** 可抄，而 entry 骨架本來就在產出者合法收到的 `<template>` 裡，所以邊際資訊只是同一份契約的複述。它容許說「這個形狀從契約算得出來」，**不容許**說這是乾淨的 fresh-context 執行。

## 為什麼沒有 run 1（儀器缺陷那次）

run 1 因**儀器缺陷**被判定無效並記錄在案（`verify.md` §11.1 三項：沒有真正無耦合的任務、`templates/plan.md` 被抽掉、四條契約條款未被量到），其分數留在紀錄上、沒有為了好看重擲。

**它的檔案不另存**，判斷依據是實測而非推論：run 1 與 run 2 的輸入 `design.md` **逐位元組相同**，`tasks.md` **只差 task 3.2 兩行**。也就是說 run 1 唯一不可替代的內容，就是那兩行壞掉的 fixture 措辭——複製一份 43 行的 design、20 行的 tasks、76 行的過期 render 和 169 行的無效輸出來保存它，正是「蓋證據博物館」而不是留資產。那兩行連同它為什麼錯，記在下面。

⚠️ **本節與下一節「儀器陷阱」中，所有取自 run 1 的材料——數字、比對結果，以及那段 task 3.2 的逐字引文——都是刪除前當場取得的，現已不可複驗**（run 1 的檔案在 `.superpowers/` 裡，已於 2026-09-04 依裁定刪除）。這一點對**引文**尤其要緊：`grep -rn "Document the policy format" openspec/ docs/` 全 tree 只命中本檔自己，`verify.md` §11.1 只轉述那三項儀器缺陷、**從未引用原文**，所以那段引文在 repo 內沒有第二個來源可以對照。run 2 的兩個數字則隨時可驗：`inputs/design.md` 43 行、`inputs/tasks.md` 20 行，都在本目錄裡。此標記與 [`errata.md`](../../../../openspec/changes/archive/2026-09-04-loosen-plan/errata.md) 對同一批已刪證據的處理一致。

### 儀器陷阱（設計這類 fixture 時會再踩的）

run 1 的 task 3.2 原本寫的是：

```text
3.2 Document the policy format and the two headers in `docs/api/rate-limits.md`,
    including what an operator does when a policy name is wrong
```

它**看起來**是一個孤立的文件任務，被拿來測 Interfaces 規則「沒耦合就省略」的那一半。但它其實從兄弟任務**消費了一個形狀和一組名字**（policy format、那兩個 header）——而「消費形狀與名字」正是 Interfaces 的定義。當時複審者的原話：*"a coin flip the fixture did not settle."*

run 2 改成現在 `inputs/tasks.md` 裡那條——一個只檢查 `config/` 底下檔案能不能 parse 成 YAML 的 CI 任務，措辭上明確不知道任何檔案該裝什麼——才真正無耦合，**條件式的那一半這時才第一次被測到，而且通過了**。

> **教訓**：要測「條件式規則的否定側」，fixture 必須有一個**真的**滿足否定條件的案例。「看起來獨立」不算——先問它有沒有從別處拿走名字或形狀。

## 怎麼重跑

1. 取得**當前**的 `plan` artifact 指令（別用本目錄這份，schema 會變）：
   ```bash
   openspec instructions plan --change <某個 active change> --schema superpowers-bridge
   ```
   ⚠️ 這條**需要一個 active change 存在**，兩種失敗訊息不同（皆為實測，測時 repo 內 0 個 change）：完全沒有 change → `✖ Error: No changes found. Create one with: openspec new change <name>`；`--change` 指到不存在的名字 → `✖ Error: Change '<名字>' not found. No changes exist. …`（後半句是「repo 內 0 個 change」這個狀態造成的，換個狀態會不同）。**兩者都不是壞了。** 另要確保 `<template>` 有被包進去——run 1 的第二個缺陷就是它被抽掉。
2. 把 `inputs/` 的兩個檔放進一個乾淨專案，路徑重指。
3. 交給一個對本 repo 無脈絡的產出者，不給任何提示。
4. 用上面五項判準評分，並與 `produced-plan.md` 對照。**評分者不該被告知本檔的預期結果**——那是洩題。
