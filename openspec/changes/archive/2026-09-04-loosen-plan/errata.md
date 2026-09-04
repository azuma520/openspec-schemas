# Errata — loosen-plan

> **這是 append-only 更正，不是改寫。** 本 change 的既有 artifact（`verify.md` 等）一律**維持原文不動**——它們記錄的是當時的狀態，改掉就沒有任何一份是「當時真的寫了什麼」。
> 本檔只追加**後來查證出來的更正**，供之後只讀 archive 的人對照。
>
> 建立於 2026-09-04，使用者裁定。

---

## E1 — f7 被歸為盲測結果（**三處，跨兩個 artifact**）

**原文怎麼寫的**：把 f7 這個正向對照算進了盲測。掃描指令與範圍：

```bash
grep -rEn "blind|Blind|盲測" --include=*.md .    # 全 repo
```

⚠️ **`-E` 不可省。** 照 BRE 跑（`grep -rn "blind|Blind|盲測"`）那三個 `|` 是字面字元，只會命中本檔自身一行——**輸出看起來像「沒問題」，其實是這個 pattern 一個字都沒比對到**。這正是本檔在講的形態，所以把可跑的形式寫出來。

命中的行裡，**三處**把 f7 算進盲測：

| 位置 | 原文 | 性質 |
|---|---|---|
| `verify.md:202` | 表格 `\| Fixture \| Violation \| Blind agent's verdict \| Correct? \|` 有七列（f1–f7），f7 那列填 `**no BLOCK** (positive control)` | 表格 |
| `verify.md:197` | 「Six fixtures, each violating exactly one check, **plus one positive control**. Run **blind** by an agent with no context on this change…」 | 散文，在表格上方五行——**盲測的主詞涵蓋了那個正向對照** |
| **`retrospective.md:39`** | 「a **seven-fixture** mutation exercise run by a **blind** third party」 | **在另一個 artifact 裡，而且把數字明講出來**——比表格更強 |

**同一份紀錄裡另有兩處是對的**，正好構成對照：`retrospective.md:55`「[evidence: blind run, **6 fixtures + 1 control**]」把兩者分開；`verify.md:610`「1 blind mutation exercise」不帶數字。本 change 以外的執行報告（`docs/superpowers/retrospectives/2026-09-03-loosen-plan-execution.md:94`、`:185`）也是對的——寫的是「六個 fixture」與「盲測 ＋ 正向對照」。

**本更正涵蓋上表三處。** 掃描範圍為**全 repo 的 `*.md`**，未發現第四處。除本 change 的 artifact 外，這條宣稱另出現在 `docs/superpowers/retrospectives/`（正確）與 **`文檔/handoff/`（正確——`session-handoff-20260903.md:16`、`:17` 寫的是「1 次盲測」與「**六個** fixture：6/6 全中」）**。把已經寫對的地方也列出來，是為了讓「沒有第四處」這個否定結論跟正面結論一樣可稽核。

**實際情況**：

| 項目 | 事實 |
|---|---|
| **「6/6 correct」的結論** | **正確，不受影響**——它指的就是進過盲測的那六個 |
| f1–f6 | 確實是盲測結果。以中性名稱 `case-A`..`case-F` 打亂後交給無脈絡 agent |
| **f7** | **不是 blind-agent verdict**。它是實作者在修正第 2 輪**未經要求自行補上**的正向對照，時間晚於盲測，由作者判定並經**一次針對性複審**確認（該複審被指派回答「它是真的正向對照，還是因為不相干的理由才通過」，結論為真：在修正前的空行讀法下它會被假 BLOCK） |

**查證依據**（收工搬運資產時比對出來，三處互相印證）：

- 工作區 `blind/` 只有 `case-A`..`case-F` 六個目錄，以 SHA256 逐檔比對，分別對應 f5 / f2 / f6 / f1 / f4 / f3；**f7 沒有任何盲測對應物**。
- `progress.md` 記載：「Copied to `blind/case-A..F` under neutral names」——就是六個。
- `task-4.1-4.2-report.md` 自己寫著：*"if you want a second blind pass, **F7 is the fixture that would test the new behaviour**"*——即第二次盲測從未執行。

⚠️ **上列三項依據、以及「實際情況」表裡關於 f7 那次針對性複審的敘述，皆已不可複驗**：`blind/`、`progress.md`、`task-4.1-4.2-report.md`，連同記載該次複審的檔案，都在 git-ignored 的 SDD 工作區 `.superpowers/` 裡，該工作區已於 2026-09-04 依裁定刪除（只保留可重跑資產，見下）。引文與該複審結論都是刪除前當場摘錄的，**repo 內沒有留下可回頭核對的副本**——這一點寫明，是為了不讓後人以為那些檔還找得到。

**影響範圍**：三處都只影響 f7 的**證據強度歸屬**（獨立盲測 vs 作者判定＋針對性複審）。f7 是真的正向對照這件事本身不受影響，`6/6` 的數字也不受影響。**沒有任何檢查結論因此改變。**

其中 `retrospective.md:39` 的「seven-fixture … blind」值得單獨點名：它**把數字寫死**，所以是三處裡唯一會讓讀者算出「七個都經過盲測」的那一句，而且它在 verify.md 之外——只讀 retrospective 的人不會看到 §8.2 的任何脈絡。

**為什麼值得記一筆**：這正是本 change 自己的主題——一份形式完全成立、沒有任何一層會抗議的產物。表格結構正確、數字誠實、每個判定都對，**卻有三處把同一件事說錯，其中兩處根本不在那張表裡**：一處是表格上方五行的散文，一處在另一個 artifact 裡且把數字寫死。它在收工搬運資產、被迫逐檔比對時才浮出來，而不是被任何一道 gate 攔下。

**而「三處」這件事本身也是後來才補上的**：本條最初只寫了表格那一處，直到隔壁 E2 因同樣的毛病被指出、再回頭用同一把尺量本條，才發現另外兩處。**修正一個「只涵蓋一次出現」的缺陷時，修正本身又只涵蓋一次出現**——這是全域紀律「修正絕對句時寫出的替代句要再過一次檢查」在紀錄層的同型復發。

**可重跑資產與正確對照表**：見 [`docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md`](../../../../docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md)（該檔「證據來源」一節為準）。變異 fixtures f1–f7 隨本檔同一個 commit 進版控（本檔撰寫當下該目錄尚未 commit）；產出端的 smoke 資產另見 [`docs/superpowers/poc/2026-09-03-plan-contract-producer-smoke/`](../../../../docs/superpowers/poc/2026-09-03-plan-contract-producer-smoke/)。

---

## E2 — `verify.md` 對產出者行為的描述不正確（**兩處，同一句**）

**原文怎麼寫的**：稱產出者「had to both choose a source and **silently relax *verbatim* to *drawn from***」。

**這句話在 `verify.md` 裡出現兩次，本更正涵蓋兩處**（掃描指令見下，命中就這兩行，無第三處）：

```bash
grep -rn "silently relax" --include=*.md .    # 全 repo
```

⚠️ **`-r` 不可省。** `grep -n "silently relax"` 沒帶 `-r` 也沒給檔名時不會遞迴、只會等 stdin，**給不出任何全 repo 結論**。

| 位置 | 所在段落 |
|---|---|
| `verify.md:419` | §11.3 The structural finding |
| `verify.md:649` | `## Overall Decision` 底下的 `### WARNING — a gap in shipped contract text` 區塊 |

**`:649` 是比較要緊的那一處**——只讀 archive 的人最可能只讀到 Overall Decision，而那段把同一個錯誤描述又講了一遍。

**實際情況**（對照本 change 保存下來的產出物 `docs/superpowers/poc/2026-09-03-plan-contract-producer-smoke/produced-plan.md`，三項皆不成立）：

| 原文的說法 | 產出物實際上 |
|---|---|
| **silently**（悄悄） | **明示**。`:10` 用一整段 **Pointers** 寫著「This change has no `specs/` directory. The source used for the header, global constraints, and per-entry acceptance criteria below is `design.md`」 |
| **放寬 *verbatim*** | **verbatim 保住了**。`:12` 寫的是「Global constraints (**verbatim** from design.md; every entry below is bound by them)」，其下每一條都帶實際引號逐字引用 |
| **改成 *drawn from*** | 全文 `drawn from` 出現 **0 次** |

被自行替換的是**來源**（`specs/` → `design.md`），不是 verbatim 這個要求本身。

**不受影響的部分（重要）**：§11.3 的**結構性發現依然完全成立**——契約條文「Global constraints copied verbatim from the specs」是無條件的，**對「這個 change 沒有 `specs/` 目錄」沒有留任何 fallback**，所以產出者只能自己挑一個來源。`produced-plan.md:10` 那段 Pointers 正是這個缺陷的直接證據。**Overall Decision 裡那條結構性 WARNING 的實質主張原樣保留、不撤回**——它指出的契約缺陷是真的。

⚠️ 但要分清楚兩件事：**該 WARNING 區塊（`:649`）本身就含有上表所列的那句錯誤描述**。保留的是它的結論（契約對無 `specs/` 沒留 fallback），**不是**它對產出者行為的描寫。讀 `:649` 時請一併讀本節。

**為什麼值得記一筆**：與 E1 同型，但更接近本 change 的核心。§11.3 是報告裡專門講「契約文字不誠實」的那一節，而它自己對受測物的描述沒有回頭核對——**兩位評分者的結論（契約缺 fallback）是對的，敘述那個結論時附帶的行為描寫是錯的**。它在收工保存資產、被迫逐行比對產出物時才浮出來。

**更正的落點**：`docs/superpowers/poc/2026-09-03-plan-contract-producer-smoke/README.md`「這次真的抓到的東西」一節已載明本更正並註「以該段為準」。
