# Errata — fix-v2-blocking-defects

> **這是 append-only 更正，不是改寫。** 本 change 的既有 artifact（`retrospective.md`、`tasks.md` 等）一律**維持原文不動**——它們記錄的是當時的狀態，改掉就沒有任何一份是「當時真的寫了什麼」。
> 本檔只追加**後來查證出來的更正**，供之後只讀 archive 的人對照。
>
> 建立於 2026-09-14，teardown 前的證據保存。慣例沿用 `../2026-09-04-loosen-plan/errata.md`。

---

## E1 — 本 change 引用的六份 SDD 工作區報告已改存永久路徑（**relocation，非內容更正**）

**本則不更正任何當時的敘述或判定。** `retrospective.md` 與 `tasks.md` 維持原文;本則只說明它們引用的檔案**現在在哪**。

本 change 的 artifact 引用下列檔案時,寫的是它們當時的位置 `.superpowers/sdd/plan/`——一個 git-ignored 的 SDD 工作區。
該工作區於 2026-09-14 teardown 時移除。移除前已把所有「被永久文件引用」的檔案保存為**逐位元組相同**的副本（SHA-256 逐檔比對）:

| 當時的路徑 | 現在的路徑 | 本 change 哪裡引用 |
|---|---|---|
| `.superpowers/sdd/plan/progress.md` | `docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/progress.md` | `retrospective.md:67` |
| `.superpowers/sdd/plan/code-review-fallback.md` | `docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/code-review-fallback.md` | `retrospective.md` |
| `.superpowers/sdd/plan/final-review.md` | `docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/final-review.md` | `retrospective.md:225` |
| `.superpowers/sdd/plan/task-1.1-brief.md` | `docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/task-1.1-brief.md` | `retrospective.md:21` |
| `.superpowers/sdd/plan/task-2.2-red-walk.md` | `docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/task-2.2-red-walk.md` | `retrospective.md` |
| `.superpowers/sdd/plan/task-2.3-red-walk.md` | `docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/task-2.3-red-walk.md` | `tasks.md:110` |

另有兩份（`code-rereview-fallback-3.md`、`codegate-fixes-report.md`）早於 2026-09-10 即已保存於
`docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/`,位置不變。

行號引用（例 `progress.md:53`）仍然有效——副本與原檔逐位元組相同。保存範圍與判準見
`docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/README.md`。

⚠️ **附帶的一件事,一併記在這裡而不改原文**:上表六個引用點裡,**有兩個**——`retrospective.md:21` 與 `:67`——
原文接著寫「git-ignored 工作區,teardown 後不可複驗」;另外兩處（`retrospective.md:225`、`tasks.md:110`）沒有這句。

對那兩處,保存副本讓該句**部分**不再成立,而不是全部:

- **不再成立的部分**:檔案本身與其內容、行號引用。副本在版控裡,與原檔逐位元組相同（SHA-256 逐檔比對）,
  `progress.md:53` 這類行號引用仍然指得到同一行。
- **仍然成立的部分**:凡是靠**檔案時間**成立的宣稱。`:21` 說 `task-1.1-brief.md` 是「first artifact」並據以算
  active hours,那是時間宣稱;副本的 mtime 是複製當下的時間,而且 **git 不儲存 mtime**,新 clone 一律重設,
  所以這一半保存救不回來。

原文維持不動（append-only）,以本則為準。其餘沒有被保存的工作區檔案,該句整句仍然成立。

---

## E2 — `retrospective.md:35` 的「byte-identical copy」宣稱強於現可驗證的範圍（**限制說明，非內容更正**）

**原文怎麼寫的**：`retrospective.md:35` 稱 `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/code-rereview-fallback-3.md`
為「byte-identical copy of the SDD workspace report」。

**實際情況**（2026-09-15 量測）：那兩份報告在 `bfc8660` 進版控時 `.gitattributes` 的 `-text` 規則尚未加入（`45b6858` 才加），
`core.autocrlf=true` 在 `git add` 時做了 CRLF→LF 正規化；`git ls-files -s` 的 blob hash 與 `git hash-object --no-filters <工作區檔>` 不相等。
原檔已隨 2026-09-14 teardown 刪除，因此「blob 等於當時原檔」**現在不可驗**——不是已證明不相等，是無法再證明相等。
2026-09-10 複製進工作區當下與原檔逐位元組相同這件事，仍以當時的紀錄為準。

**不受影響的部分**：該句引用的實質內容（§ Regression 的 13 個 fixture 獨立再推導）與行號引用不受換行符正規化影響。

**原文維持不動（append-only），以本則為準。** 該目錄 `README.md` 已同步補記。

*記於 2026-09-15。*
