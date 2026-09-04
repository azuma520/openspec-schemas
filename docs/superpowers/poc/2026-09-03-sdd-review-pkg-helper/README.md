# `review-pkg.sh` —— snapshot-based review package（2026-09-03）

> **定位：可複用的 POC helper，不是正式 workflow infrastructure**（使用者裁定，2026-09-04）。
> 它目前仍綁在 `snapshots/<task-id>/` 這套特定工作方式上，還沒證明值得成為 repo 的通用工具。
> **升格條件**：再有 1–2 個真實 change 重複使用並證明穩定，才考慮移進正式 `scripts/` / tooling 位置。
>
> 出處：change `loosen-plan`（已 archive：[`openspec/changes/archive/2026-09-04-loosen-plan/`](../../../../openspec/changes/archive/2026-09-04-loosen-plan/)）的 SDD 工作區。原檔逐位元組保存，未做任何修改。

## 它解決什麼約束

上游 SDD 自己的 `scripts/review-package` 是從 `BASE..HEAD` 的 **commit range** 建 diff 給複審者。

**這個 repo 用不了那條路**：`.claude/rules/discretion.md` 的 **Anchor Register #4** 禁止 Claude 執行 `git add` / `commit`（除三個列舉的核可流程外），所以實作者不 commit，**根本沒有 per-task 的 commit range 可以 diff**。

這支腳本改走另一條：**派工前**由控制者把該任務會碰到的檔案 snapshot 到 `snapshots/<task-id>/`，**事後**用這支腳本把 snapshot 與工作樹比對，產出複審包。

```
派工前：snapshot 檔案 ──► snapshots/<task-id>/
派工後：review-pkg.sh <task-id> ──► review-<task-id>.diff
```

下一個在本 repo 走 SDD 的 change 會撞上**同一個**約束（Anchor #4 沒有要放寬），所以這是「還會再用到」而不是「曾經用過」。

## 用法與預期輸入結構

```bash
review-pkg.sh <task-id>        # 例：review-pkg.sh 1.1
```

腳本假設自己**待在工作區目錄裡**，且該目錄底下有：

```
<workspace>/
├── review-pkg.sh
└── snapshots/
    └── <task-id>/                    ← 派工前的檔案快照
        └── <保留原本的路徑結構>        例：superpowers-bridge/schema.yaml
                                            docs/roadmap.md
```

snapshot 的內部路徑**保留斜線結構**（不是壓平），腳本靠這個把每個檔案對回工作樹的同名路徑。

輸出 `review-<task-id>.diff` 依序包含四段：scope 檔案清單 / 每檔 `+N -M` 統計 / **工作樹的完整 `git status` 短格式**（標題寫「Untracked additions」但實際不只未追蹤檔，見已知限制 2）/ snapshot → 工作樹的 10 行 context diff。

## 已知限制

**1. ⚠️ 移到本目錄之後，路徑推導是壞的——而且它 exit 0、靜默產出一份看起來完全正常的錯報告。**

腳本用相對位置往上數三層推出 repo root：

```bash
WS="$(cd "$(dirname "$0")" && pwd -P)"
ROOT="$(cd "$WS/../../.." && pwd -P)"
```

原本待在 `.superpowers/sdd/plan/` 時，往上三層剛好是 repo root，正確。**放在 `docs/superpowers/poc/2026-09-03-sdd-review-pkg-helper/` 時，往上三層是 `<repo>/docs/`——錯的**（被剝掉的三段依序是 `2026-09-03-sdd-review-pkg-helper`、`poc`、`superpowers`；實測 `cd ../../.. && pwd -P` 回 `…/loosen-plan/docs`）。

**錯了之後不會有人喊。** 實測（在 repo 外構造一個同樣深度錯誤的工作區，建好 `snapshots/1.1/` 再跑）：腳本 **exit 0**，產出一份格式完整的複審包，其中**每一個 in-scope 檔都被報成 `DELETED`**，diff 段把它們的原始內容整份印成純刪除。複審者拿到的是一份看起來很正常、實質完全錯誤的報告。

**第三段的表現取決於算錯的 `ROOT` 落在哪裡，而預設的那種落點反而最不容易看出來。** `git status` 找的是**最近的那個外圍 repo**：

| 算錯的 `ROOT` 落在 | 第三段 |
|---|---|
| **仍在同一個 repo 內**（本目錄的實際情形——上面說的 `<repo>/docs`） | **完全正常**，報的就是這個 repo。`git status --porcelain` 印的是 repo-root 相對路徑，所以這一段與從 repo 根跑出來的**逐位元組相同**，沒有任何異常可看 |
| **落進另一個 repo 內** | 列出**那個** repo 的完整狀態。⚠️ 實測一次 `ROOT` 落進使用者家目錄那個 repo，產出的複審包**含個人檔案清單、大小約 179 MB**（**此數字不可複驗**：測試工作區未保存，repo 內沒有東西能回頭核對大小或清單） |
| **真的不在任何 repo 裡** | `git status` 失敗，而 `:62` 把 stderr 消音 → **第三段整段是空的**，同樣不會有錯誤訊息 |

⚠️ **所以不要拿「第三段有沒有異常」當判斷依據。** 本目錄這個落點屬於第一列——第三段長得完全正常，**這讓它比第二列更難被發現**，而不是更容易。唯一可靠的症狀是統計段：**每個 in-scope 檔都是 `DELETED`**。第二列那種跨 repo 外洩是另一種落點才會發生的事，記在這裡是因為它是同一個根因（`ROOT` 靠算術推導、沒有任何斷言）能造成的最壞後果。

**今天之所以看起來「會出錯」，是個意外。** 本目錄沒有 `snapshots/` 目錄，所以腳本在 `:22` 就 `exit 1` 了——那是目前唯一的 fail-loud 守門。但本檔 §用法 正是叫讀者**在這個目錄底下建 `snapshots/<task-id>/`**；那一刻起，這道守門消失，失效模式立刻翻轉成上面那個靜默錯報。

這裡**刻意不修腳本**：本目錄保存的是「已實測有效」的那一支原檔，改過就不再是被驗過的那個東西了。要用的人**把它複製回一個位於 repo root 底下三層的工作區**（例如 `.superpowers/sdd/plan/`），或自行把 `ROOT` 改成 `git rev-parse --show-toplevel`。真要升格成正式工具時，這是第一個該改的地方——而且該加的不只是正確的 `ROOT`，還要有一個「算出來的 ROOT 真的是預期 repo」的斷言。

**2. 只比對 snapshot 裡有的檔案。** 派工前沒 snapshot 到的檔案，統計段與 diff 段都完全看不到——**看不見的是內容 diff 與 `+N -M` 統計，不是檔名**：第三段跑的是無過濾的 `git status --porcelain --untracked-files=all`，所以漏掉的既有檔仍會以 ` M` / ` D` 出現在那段裡。**漏 snapshot 一個既有檔＝複審者知道它被動過、卻看不到動了什麼，而且不會有任何錯誤訊息。**

⚠️ 腳本自己在 `:60` 把該段標題寫成 “Untracked additions in the worktree (new files this task may have created)”——**這個標題名不副實**，它實際上印的是完整的 `git status` 短格式。讀輸出時以實際內容為準。

**3. 沒有 git 依賴，除了第三段那次 `git status --porcelain` 呼叫**（即上面限制 2 講的那段，它印的是完整短格式、不只未追蹤檔）。這是刻意的——整套設計的前提就是「沒有 commit 可用」。

**4. 檔案刪除在兩段裡表現不同**：統計段只印 `DELETED`（不給 `+N -M` 數字），diff 段則對 `/dev/null` 比對、會完整印出被刪掉的內容。看統計段會低估刪除的規模，實際內容在下面。

**5. ⚠️ 一旦 `snapshots/<task-id>/` 存在（也就是照 §用法 做完之後），這支腳本就沒有任何一段會 fail loud——這是限制 1 之所以那麼危險的根本原因。** 唯一的例外是限制 1 講的 `:22`（snapshot 目錄不存在就 `exit 1`），而那道守門在你照文件建好目錄的那一刻就消失了；它也**與這個 bug 無關**——`SNAP` 是從 `WS` 推的、不是從 `ROOT` 推的，所以它從頭到尾沒在檢查 `ROOT` 對不對。 `:14` 只有 `set -u`，**沒有 `set -e`、沒有 `pipefail`**；而每一個可能失敗的動作都被消音（`:52`、`:53`、`:72` 的 `diff` 與 `:62` 的 `git status` 全帶 `2>/dev/null`）。後果是：讀不到（權限）、`diff` 本身出錯，一律降級成 `+0 -0` 或一段空 diff，**不會是錯誤**。設計上「不報錯」與「沒有差異」在輸出裡長得一模一樣。（**唯一的例外是「工作樹裡沒有這個檔」**——`:43` 的 `[ -e "$b" ]` 會攔下來印 `DELETED`，即上面限制 4 講的那條路；限制 1 的每檔 `DELETED` 就是這條路被大量觸發的樣子。）腳本刻意凍結不改，所以這裡只能用文件承載。

**6. 升格前該補的檢查（目前都不成立，非 bug、是邊界）**：① snapshot 裡若有二進位檔，`diff` 只回一行 `Binary files … differ`，被 `NR>2` 濾掉 → 統計印 `+0 -0`，與空行漏算是同一類靜默低估（本 repo 全是 YAML／Markdown，暫時碰不到）；② `:34` 的 `find . -type f` **排除 symlink**，符號連結檔在統計段與 diff 段都是隱形的；③ `$TASK` 未經驗證就串進 `$SNAP` / `$OUT`。要**逃出工作區**得用 `review-pkg.sh ../../x`；`../x` 只會讓 `SNAP` 退到 `<workspace>/x`（仍在工作區內），但它同時把 `OUT` 變成 `<workspace>/review-../x.diff`——那個父層 `review-..` 目錄不存在，**於是每一次寫入都失敗、整份複審包不會產生，而腳本照樣 exit 0**。這一項本身就是限制 5 的縮影。三項對本地 helper 都可接受，列出來是為了升格時有清單可照。

## 為什麼空行統計不能用 `grep -c` 做

腳本裡數增刪行數用的是 `awk`，不是直覺的 `grep -c '^+[^+]'`。這是**實測踩出來的**，註解裡也寫著：

```bash
add=$(diff -U10 "$a" "$b" 2>/dev/null | awk 'NR>2 && /^\+/ {n++} END {print n+0}')
```

`'^+[^+]'` 這個 pattern **要求 `+` 後面還有第二個字元**，所以它會**靜默漏掉每一個新增的空行**（空行在 diff 裡就是單獨一個 `+`）。

task 1.1 的複審者抓到的實例：stat 印出 `+61 -18`，git 對同一份改動報的是 `+70 -22`——差的正好是 **9 個新增空行、4 個刪除空行**。

危險的地方在於**它不會報錯**：複審者拿到一個看起來完全正常的統計，只是數字偏小，於是**低估了 diff 的規模**。這與本 change 的主題同型——形式成立、無人抗議、只有事後交叉比對才看得出來。

（`NR>2` 是為了跳過 `--- a/…` / `+++ b/…` 那兩行檔頭，否則檔頭的 `+++` 會被算成新增行。）
