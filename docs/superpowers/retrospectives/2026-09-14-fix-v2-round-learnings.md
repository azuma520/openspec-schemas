# loosen-plan / fix-v2 這一輪：我們現在知道什麼（2026-09-14 收斂）

> **性質**：證據收斂，不是新的 retrospective、不新增 Skill / Gate / 規範 / change。
> 範圍由使用者 2026-09-14 指定：五個已有證據的主題 ＋ A1 三樣本評估（定位依使用者 2026-09-14 裁定，見 §1.4）。每一條「知道」都附出處；
> 沒有出處的判斷標【推論】或【未查】。行號引用分兩種：**現行檔案**的行號以寫作當日（2026-09-14）的工作區為準；**改前位置**（標「當時的」）指的是修正前的檔案，現行檔案該行已是修正後的文字，能對到 blob 的附 commit（`git show <commit>:<path>`），對不到的（當時未提交的工作區）以 `文檔/handoff/attachments/` 的紀錄為唯一證據。
>
> 主線事實：`loosen-plan`（schema major 1→2）2026-09-04 archive（commit `03bf87e`，目錄 `openspec/changes/archive/2026-09-04-loosen-plan/`；收尾 session 於 09-07 結束）；`fix-v2-blocking-defects`（修 v2 五個 P1）
> 2026-09-14 archive、PR #1 合併、teardown、push 結案。逐日紀錄在 `文檔/handoff/` 底下的 `session-handoff-20260903.md`、`session-handoff-20260904.md`、`session-handoff-20260907.md`、`session-handoff-20260908.md`、`session-handoff-20260909.md`、`session-handoff-20260910.md`、`session-handoff-20260911.md`、`session-handoff-20260914.md`（各日一檔），
> A1 樣本紀錄在 `文檔/handoff/attachments/20260910-pilot2/`——**兩者都未進版控**（untracked、非 gitignored）。本文件引用它們，
> 等於把它們變成有永久 consumer 的檔案（§5 的判準對本文件自己同樣成立）；要不要把 `attachments/` 納入版控是使用者的決定，本文件不代做。

---

## 0. 一頁摘要

| 主題 | 一句話 | 已有證據強度 |
|---|---|---|
| A1 四步 sweep | 對既有全域 Skill `review-fix-propagation` 提供一項 refinement：改既有規則時，改前優先搜**被淘汰的舊說法／舊概念**，新說法主要用於改後驗證；只搜新字眼可能假綠。refinement 已回灌該 Skill，不另建機制 | 3 個真實樣本，其中 1 個假綠、1 個改搜舊說法後命中；支持的是搜尋方向這一項，不是整套 Skill |
| 量測工具 | `grep -c $'\r'` 在本機有兩種錯法：放在 `$( )` 命令替換裡時 `$'\r'` 變成空字串、回行數（假陽性）；不加 `-U` 回 0（假陰性）。非零命中同樣不可信 | 本文件 §2 當日重現；機制未查 |
| EOL 保證 | 「逐位元組相同」是三件不同的事（原檔 / blob / 工作區），`core.autocrlf=true` 讓每一步都可能無聲改變；能被驗證的只有 blob，且 mtime 一律救不回 | 09-10、09-14 實測 ＋ `.gitattributes` 現行註解 |
| Windows 目錄鎖 | CLAUDE.md「必定撞」的 3/3 樣本來自**另一個 repo**；本 repo 兩次 archive 一次沒試、一次成功；本 repo 撞到的只有 `git worktree remove --force` 最後那個目錄 | §4 表 5 列（第一列彙總另一 repo 的 3 次，共 7 次操作） |
| teardown 證據 | 「臨時工作區」一旦被永久文件引用，生命週期就跟著永久文件；能不能刪要掃**消費者**，不能看目錄名 | 09-04（未保存）、09-08（保存 2）、09-14（9→12）三個時點 |

---

## 1. A1 四步 sweep：三個樣本，以及它回灌到哪裡

### 1.1 習慣的定義（原始出處）

Q10 提出：修 reviewer finding 時，改前 `rg` 該規則的關鍵名詞列命中 → 改 → 改後再 `rg` → `diff -r` dogfood 副本；只記三個數（做了幾次 / 每次命中幾個表面 / reviewer 下一輪還抓到幾條多表面型）。不升 Skill / Gate。
出處：`docs/superpowers/research/2026-09-10-contract-drift-archaeology.md` §Q10（:238–:250）；使用者 09-10 裁定與 09-11 A1/A2 切分見 memory `feedback_review_observation_protocol`。
它的來歷本身是個事實：同一句裁定 09-08 已寫在 gitignored 的 SDD ledger（`progress.md:158`，現保存於 `docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/progress.md`），09-10 修 finding 時「不存在於任何我會讀到的地方」（research §Q3 :174）。

**與既有機制的關係（使用者 2026-09-14 定位）**：A1 不是新發明的 propagation 機制。全域 Skill `review-fix-propagation`（canonical：`C:/Users/user/.claude/skills/review-fix-propagation/`）原本就負責「修完 review finding 不直接進下一輪、檢查同類殘留、跨檔／跨層／規格／測試傳播、區分必修殘留 / 歷史紀錄 / intentional reference」。原版的 grep 範例實際上多數搜的是舊詞，但**沒有把「先搜舊說法」獨立說成一條原則**。本輪 A1 三個樣本提供的是這一項 refinement，並已回灌：SKILL.md 最前面新增獨立章節「最重要的一條：搜『舊說法』，不是搜『新說法』」、Step 2 改為「舊 → 新」配對表且左欄為主要 grep 對象；`references/propagation-checklist.md` 新增範例 D「規則口徑改動」（不能只搜 `[~]`，要搜舊的 `[ ]` / `[x]` 二分描述、incomplete / complete、「全部／所有」等關鍵字組合）。正確的歷史敘事是：既有 propagation Skill → 真實 dogfood 暴露搜尋方向盲點 → A1 提煉「優先搜舊說法」→ refinement 回灌既有 Skill。不是「A1 發明了新 Skill」，也不是「這條原則原版早已完整存在」。

### 1.2 三樣本對照

| 樣本 | 日期 / 對象 | reviewer 點名 | sweep 額外找到 | sweep 漏掉 | 出處 |
|---|---|---|---|---|---|
| 1 | 09-11，research 文件過期標籤 | 2 | 1（當時的 research §4 `:264`，同一過期標籤在另一節；該行已修正，現行檔案無此標籤；改前版本當時未提交、無 blob，以右欄紀錄為證） | — | `文檔/handoff/attachments/20260910-pilot2/pilot3-research-doc-review-r1.md:29–35` |
| 2a | 09-11，「subject 唯一」措辭 | 5 | 1（`git show b07d571:openspec/changes/fix-v2-blocking-defects/design.md` 第 71 行「不需要 subject 唯一」；現行封存檔已修正） | — | `文檔/handoff/attachments/20260910-pilot2/pilot2-codex-r1-record.md:58–62` |
| 2b | 09-11，check 2 改為接受 `[~]` | — | 0 | **2**（`git show b07d571:superpowers-bridge/templates/verify.md` 第 33 行「所有 `- [ ]` 已變為 `- [x]`」；change `verify.md` 的第 54 行對應當時未提交的工作區、無 blob，以右欄紀錄 `:71` 為證；兩處現已修正），由 Codex r2 抓出 | 同上檔 `:75–79`；handoff 0914 08:10 四 |
| 3 | 09-14，check 2 改動的傳播 | 2 | 2（當時的 fix-v2 change 內 `design.md:156`、`verify.md:23`——對應當時未提交的工作區、無 blob，以右欄紀錄 `:83` 為證；現已修正）＋ 1 處**正確地不改**（`openspec/changes/archive/2026-08-31-fix-tdd-transitive-claim/verify.md:36`，本日仍是舊措辭） | — | 同上檔 `:81–86` |

樣本編號說明：表有四列、樣本三個——2a 與 2b 是同一天同一輪修正裡的兩條規則，2b 那次的 sweep 假綠、由樣本 3 回頭修正，所以拆開列。

### 1.3 每個樣本各自說了什麼

- **樣本 1、2a：習慣對準的那一類確實存在。** 兩次額外命中都是「同一字串的其他出現處」——正是 research §2 A 類（32 條）的形狀。兩次都是 reviewer 沒點名、sweep 多找到。
- **樣本 2b：第二次為什麼假綠。** 改 check 2 時搜的是**新規則的字眼**（`every checkbox`、`DEFERRED TASK`、`[~]`），而兩個仍矛盾的表面用的是**舊說法**「所有 `- [ ]` 已變為 `- [x]`」，一個新字眼都不含。sweep 從結構上不可能找到它們，而我仍宣告該輪一致。同一天 `verify.md:54` 就在螢幕上、我在它下面加註記而沒認出它在重述同一條規則——搜尋詞錯**加上**讀漏，兩層都失敗（`pilot2-codex-r1-record.md:77–79`）。
- **樣本 3：修正的方向。** 改用**舊斷言的字面措辭**去搜，五處命中（四處現行文件、一處封存紀錄）：兩處 reviewer 點名的、兩處沒點名的、一處是已封存 change 的驗證紀錄——那是真的在舊規則下跑過的紀錄，改了就是竄改；Codex 獨立同意保留（handoff 0914 08:10 當日洞見第二條）。sweep 的第二個價值在這裡出現：讓「不該改的」變成有意識的決定，而不是漏掉或誤改。
- **樣本 1 與 2a 為何沒暴露這個缺口**【推論】：那兩次新舊措辭恰好共用關鍵詞，搜哪一邊都命中。詞彙不共用時失效率高，目前是 Hypothesis（handoff 0914 08:10【學習候選】3）。

### 1.4 三樣本評估與最終定位（使用者 2026-09-14 裁定）

**結論**：不新增 A1 Skill、不新增 Gate、不維持一套平行的 A1 規則。本輪真實樣本對既有 `review-fix-propagation` Skill 提供一項實務 refinement——**既有規則變更時，改前優先搜尋被淘汰的舊說法／舊概念；新說法主要用於改後驗證**。該 refinement 已吸收回既有全域 Skill（§1.1 末段），因此不另建機制。

**證據支持的邊界**（保留，不擴張）：
1. 三個樣本支持的是**搜尋方向這一項** refinement，不是證明整套 6 步／9 維 propagation Skill 都被驗證。
2. 四次搜尋裡有三次多找到 reviewer 未點名的表面（樣本 1、2a、3），其中樣本 3 另多找到一處「該保留」的歷史紀錄並正確選擇不改。2a 的紀錄寫明當時只做了第一步（改前 `rg`），後三步標為待做（`pilot2-codex-r1-record.md:61`）；那些修改最後有落地（現行檔案可證），但**是否以四步形式完成沒有紀錄**。樣本 3 的紀錄有改前搜尋、修改與 `diff -r`，沒有改後 `rg` 的紀錄；**完整四步證據只有樣本 1**。
3. 【推論】唯一的失敗（2b）是**搜尋方向**錯，不是機制錯——改搜舊說法後（樣本 3）同一類表面被找到；N=1，不足以排除其他原因。
4. 「只搜新說法會失敗」不是絕對句：樣本 1 與 2a 新舊措辭恰好共用關鍵詞，搜哪一邊都命中；真正成立的是**當舊殘留不含任何新規則字眼時，只搜新說法從結構上找不到它**。Skill 原本寫的「為什麼必然失敗」已依此改為「為什麼只搜新說法會產生系統性盲點」。

**回灌的 dogfood 證據**（只算一次，不擴張成整套 Skill 已驗證）：全域 Skill 可攜化時對自身跑過一次 propagation check——`Propagation Check Report: review-fix-propagation 可攜化（拆本 repo 指路） | 抓到 2 處並修 | 2026-09-14`（來源：使用者 2026-09-14 於對話中提供；本 repo、handoff、attachments 與 skill 目錄內**無可定位的副本**，那次 run 的細節【未查】）。

邊界（refinement 不適用、樣本仍為 0 的情形）：
- **新增規則**（無舊字串可搜）：只能用新字眼搜「應該提到卻沒提到的表面」，那是另一種掃描。
- **概念改名而非措辭改動**（例：check 7 的載體從 `plan.md` 改成 `tasks.md`，handoff 0907 16:05 二）：舊「說法」是一個檔名，四處命中；但同型的「舊概念」若散在散文裡，`rg` 只能抓字面。

未查：
- 三個樣本全部由同一個執行者做（我），沒有第二個執行者的樣本。
- 「reviewer 下一輪還抓到幾條多表面型」這個數只在 2b 有意義（2 條），其他樣本 reviewer 下一輪沒有再報同型。N 太小，不足以說趨勢。

---

## 2. 量測工具會產出看起來像確認的錯誤答案

### 2.1 這一輪發生了什麼

同一個宣稱（「這些檔是 CRLF」）在 09-08、09-09、09-10 被判錯兩次、第三次才確認一直是對的（handoff 0910 12:25 四【紀律接力】第一條）。09-14 保存證據時再犯一次：`grep -c $'\r'` 對 `progress.md` 回 216，我據此在 README 寫「12 檔全是 CRLF」，還拿這個數字反駁 reviewer 的正確指正，第五輪才用 Python 數原始位元組 ＋ `git ls-files --eol` 推翻——實際 12 檔裡 11 份 LF、1 份 CRLF（handoff 0914 10:0x 四；`2026-09-03-loosen-plan-sdd-reports/README.md:7–8`；本日 `git ls-files --eol` 複驗一致）。

### 2.2 本日重現（2026-09-14，本機 GNU grep 3.0 / bash 5.2.37 msys）

測試檔：`eol-lf.txt` 三行純 LF（CR 數 0）、`eol-crlf.txt` 兩行 CRLF（CR 數 2）。

| 指令 | LF 檔應回 0 | CRLF 檔應回 2 | 判讀 |
|---|---|---|---|
| `grep -c $'\r' f` | 0 | **0** | 假陰性：msys grep 文字模式把 CRLF 當行尾、`\r` 永遠比對不到 |
| `grep -cU $'\r' f` | 0 | 2 | 正確（`-U` 二進位模式） |
| `echo "$(grep -c $'\r' f)"` | **3** | （未測 CRLF 檔） | 假陽性：回**行數**；`-U` 也一樣回 3。原因量到了：在 `$( )` 內 `printf '%q' $'\r'` 印出 `''`——**`$'\r'` 在命令替換裡變成空字串**；`$'\x0d'` 同樣；改成先 `CR=$'\r'` 再在 `$( )` 內用 `"$CR"` 則正確回 0。`bash -c` 與獨立 script 檔重現相同結果 |
| `grep -c '' f` | 3 | — | 對照：空 pattern 匹配每一行，與上一列同值 |
| `tr -cd '\r' \| wc -c` | 0 | 2 | 正確 |
| Python `read().count(b'\r')` | 0 | 2 | 正確 |
| `git ls-files --eol` | `i/lf w/lf` | `i/crlf w/crlf`（repo 內樣本） | 正確，且同時看得到 index 與工作區兩側 |

三個歷史紀錄各自對到一列：09-08 的失敗是「包在雙引號的 `$( )` 裡」（handoff 0908 16:50 四第一條）＝第三列；09-14 的「`$'\r'` 沒進 pattern，空 pattern 匹配每一行」＝同一列；09-07 用的 `grep -rlU $'\r'`（handoff 0907 08:36 三-A）＝第二列，當時是對的。⚠️ 09-08 與 09-14 兩份紀錄裡的失敗指令**不能逐字重跑**：那兩處 `$'` 與 `'` 之間存的是真實的換行 / CR 位元組而不是 `\r` 兩個字元（本日以位元組檢視確認），當時到底打了什麼只能由紀錄的描述推回；09-07 handoff 的 `grep -rlU $'\r'` 則完整保留 `\r` 兩個字元、可逐字重跑。本表第三列重現的是**本機今天的行為**，不是 09-08 / 09-14 當時那條指令。

【未查】為什麼 `$'\r'` 在這個 bash（5.2.37 msys）的 `$( )` 裡會退化成空字串——一般 bash 的預期是命令替換內照常做 ANSI-C 展開（Codex 本日審查時以此質疑本列，但其沙盒跑不了 msys bash、無法實測）。本文件只記可重現的行為與量到的中間值，不記機制；這個「預期與實測不符」本身就是 §2.3 第三條的實例。

### 2.3 現在知道什麼

- **非零命中同樣不可信，而且更危險。** 既有全域規矩只寫「篩選回報 0 命中時換路徑交叉驗」。這一輪兩種錯法都出現過：0（假陰性）與行數（假陽性）；行數那個看起來像證據，所以被寫進文件、拿去反駁 reviewer。
- **同一個量測 bug 會生出相隔數輪的多個錯誤宣稱**（handoff 0907 08:36 四第一條②：一個未設邊界的腳本在兩處造成兩個看似無關的錯誤）。修其中一個宣稱不會修另一個。
- **可靠的判準不是「我確不確定」，是「這個方法有沒有被一個應該失敗的輸入驗過」**（handoff 0908 16:50 四：「一個永遠回同一個答案的檢查，先餵一個應該失敗的輸入」）。§2.2 那張表就是這麼做的。
- 這條與 A1 的 2b 同型：兩者都是「工具沒報錯、輸出形式正確、結論錯」。差別只在一個是搜尋詞、一個是量測指令。

---

## 3. EOL：什麼是真的保證、什麼只是工作區表象

### 3.1 三個「檔案」不是同一個東西

| 層 | 誰決定內容 | 會無聲改變的情況 |
|---|---|---|
| 原檔（例 `.superpowers/` 裡的報告） | 產出它的程式 | 被刪就沒了（§5） |
| blob（index / commit） | `git add` 時的 `.gitattributes` ＋ `core.autocrlf` | `core.autocrlf=true` 且無 `-text`：CRLF → LF 正規化（handoff 0914 10:0x 當日洞見第一條） |
| 工作區 | checkout 時的同一組設定 | `core.autocrlf=true`：LF blob → CRLF 工作區；且 `text` 屬性讓 CRLF 工作區對 LF blob 時 `git status` 顯示乾淨（`.gitattributes` POC 段註解；handoff 0907 08:36 三-A：11 檔 CRLF 而 status 乾淨） |

本機 `core.autocrlf` 實值為 `true`（本日 `git config core.autocrlf`）。

### 3.2 這一輪實際發生的四件事

1. `templates/verify.md` 在 `787b14c` 被**靜默**從 CRLF 轉成 LF，造成整檔重寫的幻影 diff（`git show --numstat 787b14c`：225 加 / 181 刪，合計 406 行）；因為我預先給了「工作區 CRLF 所以每個 diff 都膨脹」這個錯誤通則，沒有任何審查者去追這次真實翻轉（handoff 0908 16:50 四第二條）。**一個錯的通則會替真實異常提供掩護。**
2. `.gitattributes` 的 LF pin 內容正確，但它落地的 clone 裡 11 個 POC 檔已是 CRLF、`git status` 乾淨——「規則承諾的狀態在它落地的工作區當下就不成立」（handoff 0907 08:36 當日洞見第二條）。校正是砍掉重取（`rm -r` ＋ `git checkout --`），09-07 14:14 歸零。
3. bridge 三個模板的 blob 本來就是 CRLF，加 `superpowers-bridge/**/*.md text eol=lf` 後要 `git add --renormalize` 才會改 index（`.gitattributes` bridge 段註解；handoff 0910 12:25 二）。
4. 保存 SDD 報告時要的是「一個位元組都不要動」而不是「釘成 LF」，所以用 `-text`（兩個方向都不轉換），並以「staged blob 的 hash 是否等於 `git hash-object --no-filters 原檔`」實測（`2026-09-03-loosen-plan-sdd-reports/README.md:7–18`；本日 `git ls-files --eol` 對該目錄 12 份保存報告——**不含目錄自己的 `README.md`**——顯示全部 `attr/-text`、11 份 `i/lf`、`task-1.1-brief.md` 為 `i/crlf`；連 README 一起數是 13 檔）。

### 3.3 現在知道什麼

- **能被驗證的保證只有一個：blob 等於原檔的未過濾雜湊。** 工作區相同不推出 blob 相同（正規化在 `add` 時發生）；blob 相同也不推出下次 checkout 的工作區相同（轉換在 checkout 時發生）。
- **`text eol=lf` 與 `-text` 是兩個目的**：前者「統一成 LF」，後者「照原樣」。保存證據用後者，可重跑資產用前者。兩者都只治理未來的 add / checkout，不修既有 index 與工作區。
- **mtime 一律救不回。** git 不儲存 mtime，`cp -p` 也無用；靠檔案時間成立的宣稱（「哪一份是第一個產出的 artifact」、耗時統計）保存後仍不可複驗（README `:20`；errata E1「仍然成立的部分」）。
- **姊妹目錄 `2026-09-08-fix-v2-review-reports/` 的三檔，本日量到 blob 與工作區不相等。** `git ls-files --eol` 顯示 `i/lf w/crlf attr/-text`；`git ls-files -s` 的 blob hash 與 `git hash-object --no-filters` 對工作區檔算出的 hash 三檔皆不同（本日量測）。時序：三檔在 `bfc8660`（09-14）進版控，`-text` 規則在其後的 `45b6858`（09-14）才加（本日 `git log -S'-text' -- .gitattributes`）——所以 add 時走的是 `core.autocrlf=true` 的正規化，原檔若是 CRLF，blob 已被轉成 LF。handoff 0910 12:25 二寫「兩份報告逐位元組存」，那個宣稱量的是工作區副本，不是 blob；原檔已隨 teardown 刪除，**blob 是否等於原檔現在已不可驗**。這一條是本文件寫作時才量到的，記在這裡、不處理（處理方式屬使用者決定：接受、或在 README 註明這三檔的保證弱於姊妹目錄）。

---

## 4. Windows 目錄鎖：不是「必定失敗」，是不同動作有不同形態

### 4.1 實例

| 日期 | 動作 | 結果 | 出處 |
|---|---|---|---|
| 2026-06-03 / 06-05 / 06-08 | `mv openspec/changes/X archive/`（**另一個 repo**：googleWorkspace 專案） | 3/3 `Permission denied` | memory `feedback_opsx_archive_windows_dir_lock`（該專案 memory 目錄） |
| 2026-09-04（commit `03bf87e` 18:53；紀錄寫在 09-07 收工的 handoff） | archive loosen-plan | **沒有試 mv**：照 CLAUDE.md 直接走 `cp -r` → `diff -r` → 委派 `rm -rf` | handoff 0907 08:36 二第一條；`git show -s 03bf87e` |
| 2026-09-14 | `openspec archive fix-v2-blocking-defects -y`（官方路徑） | **一次成功**，11 檔 rename 100% | handoff 0914 08:18 二、四 |
| 2026-09-14 | `rm -rf .superpowers`（73 檔） | 成功 | handoff 0914 10:3x 二 |
| 2026-09-14 | `git worktree remove --force` | **半成功**：檔案全刪、中繼資料清掉、目錄本身 `Permission denied` | 同上 |

### 4.2 現在知道什麼

- **CLAUDE.md「3/3 複現，穩定模式非偶發」的三個樣本全在另一個 repo。** 本 repo 對 archive 這個動作的樣本是：一次沒試、一次成功。這是六軸裡的「對象」軸——量的不是這個環境。該句被寫成絕對句時，本 repo 的反例只是還沒出現（handoff 0914 08:18 四第一條）。
- **`03bf87e` 的 commit 訊息與上一條矛盾，本文件判為誤歸因。** 該訊息寫「`mv` into archive/ hits a Windows directory lock in this repo (3/3 reproduced)」。能定位到的三個樣本全在 googleWorkspace 專案的 memory（日期 2026-06），本 repo 自 09-01 起的 handoff 沒有任何一次 `mv` 撞牆的紀錄，而同一份 handoff 記載 09-04 那次 archive 根本沒試 `mv`。【推論】那句是把 CLAUDE.md 的絕對句抄進 commit 訊息，「in this repo」是措辭誤植；commit 訊息改不了，以本條為準。【未查】09-01 之前的本 repo 歷史沒有掃。
- **本 repo 實際撞到的只有一次：`git worktree remove --force` 刪完所有檔案後，worktree 目錄本身留下。** 同一天 `rm -rf .superpowers` 刪掉一個 73 檔的目錄樹（含子目錄）成功，`openspec archive` 搬目錄也成功。所以「刪目錄會撞、刪檔案不會」這種按動作類型的歸納**不成立**（handoff 0914 10:3x 當日洞見那句措辭本文件不採）。【推論】差別在目標目錄的狀態：worktree 根目錄可能被某個 process（編輯器、或本 session 的 cwd）持有 handle，`.superpowers/` 與 change 目錄沒有。這是假說，沒有量過哪個 process 持有。
- **一次成功不足以反推「以後都會過」。** 09-14 那次是在工作區完全乾淨、可用 git 完整還原的前提下才試的——「乾淨的工作區把一個不可逆的嘗試變成可逆的」（handoff 0914 08:18 當日洞見第一條）。這個前提是讓「試官方路徑」成為安全動作的關鍵，不是目錄鎖消失了。
- 可用的降級措辭素材（本輪依指示**不改** CLAUDE.md）：「archive 在 Windows **已知會**撞目錄鎖（另一 repo 3/3；本 repo 一次成功、一次未試）；先確認工作區乾淨、可還原，再試官方 `openspec archive`；撞到時走 `cp -r` → `diff -r` → 委派使用者 `rm -rf`。」只寫觀察到的結果，不寫動作類型的歸納。

---

## 5. teardown 證據：一旦被永久文件引用，生命週期就變了

### 5.1 三個時點

| 時點 | 發生什麼 | 後果 |
|---|---|---|
| 09-04 | loosen-plan 收尾刪 `.superpowers/`，只保留可重跑資產 | errata E1 的三項查證依據（`blind/`、`progress.md`、`task-4.1-4.2-report.md`）當時記為「已不可複驗、repo 內沒有留下可回頭核對的副本」（`openspec/changes/archive/2026-09-04-loosen-plan/errata.md` E1 ⚠️ 段）。**09-14 後的現況**：後兩檔已由 E4 保存（同檔 E4；實檔在 `docs/superpowers/retrospectives/2026-09-03-loosen-plan-sdd-reports/`），`blind/` 仍不可複驗。同一 change 的 handoff 差點也隨 worktree 消失（handoff 0904 四第二條） |
| 09-08 | fix-v2 freeze；工作區 72 檔備份到 repo 外；10 日保存 2 檔到 `2026-09-08-fix-v2-review-reports/` | 保存判準是「work-map 條目引用了它們」——只掃了一個載體 |
| 09-14 | teardown 前確認：先報 9 檔、再修正為 12 檔；6 處引用 relocation；兩個已封存 change 用 append-only errata | 「09-08 只盤點了 work-map 的引用，漏掉其他六個載體」（handoff 0914 09:2x 四第一條）；9→12 的錯因是從路徑字串那端搜（範圍含 handoff 多算一個、漏三個裸檔名引用、漏一個二階依賴）（handoff 0914 10:0x 四第二條） |

### 5.2 現在知道什麼

- **「臨時工作環境」這個詞會誤導清理決策。** 判斷一份資料能不能刪，看的是**有沒有別的東西指著它**，不是它被歸在哪個目錄——而那要實際去查，不能靠目錄名推論（handoff 0914 09:2x 當日洞見）。
- **反查要從消費者那端掃。** 正確做法是列出所有永久文件（research / retrospectives / poc / archive 的 artifact 與 errata / work-map），逐一找它們引用了工作區的哪些檔，含裸檔名與二階依賴；不是拿工作區的路徑字串去 grep（handoff 0914 10:0x 四第二條）。
- **保存的判準與邊界已寫死在 README**：只保存「已有永久 consumer」的檔案（72 = 12 + 2 + 58），明文「不是建立 Evidence 系統」（`2026-09-03-loosen-plan-sdd-reports/README.md:22–23`）。
- **保存救得回內容與行號，救不回時間**（§3.3）。errata E1 把「不可複驗」拆成兩半：檔案與行號那半不再成立，檔案時間那半仍然成立（`openspec/changes/archive/2026-09-14-fix-v2-blocking-defects/errata.md` E1 ⚠️ 段）。
- **已封存的紀錄不改寫，用 append-only errata 承載更正與 relocation**——這一輪兩個 archive 各一份 errata，慣例已成形（`openspec/changes/archive/2026-09-04-loosen-plan/errata.md` E1–E4、`openspec/changes/archive/2026-09-14-fix-v2-blocking-defects/errata.md` E1）。
- **09-04 那次沒有保存**、09-08 只掃一個載體、09-14 第一次數錯：三個時點都是「這次沒有釀成事故的唯一原因是刪除前真的做了確認」（handoff 0914 09:2x 四第一條）。沒有任何一層會自動抗議。

---

## 6. 貫穿五題的兩條線

1. **形式上完全成立的錯誤，這一輪的載體有：搜尋詞（§1）、量測指令（§2）、EOL 狀態（§3）、絕對斷言（§4）、清理判準（§5）。** 共同症狀是靜默：工具不報錯、狀態看起來乾淨、結論被寫進文件。抓到者：reviewer（1.2b、2.1 的 reviewer 指正）、刪除前確認（§5）、反例出現（§4）。自查抓到的只有把「應該失敗的輸入」餵給量測工具那一次（§2.2）。
2. **「前面錯過不代表這次也錯」。** Stop hook 09-14 誤報三次（root 解析跑進 worktree）、第四次正確；Codex doc review 我反駁過一次而錯的是我。信不信一個來源靠逐次回源核實，不靠過往命中率（handoff 0914 10:5x 當日洞見）。這條與 §2 相反方向但同一根：都是拿「上次的結果」代替「這次的量測」。

---

## 7. 本文件刻意沒做的事

- 沒有新增任何規則、Skill、Gate、routing、治理機制、backlog 條目；backlog 第 84 行依裁定保留不升級。A1 的 refinement 是回灌既有全域 Skill（§1.4），不是新機制。
- 沒有改 CLAUDE.md 的目錄鎖絕對句（§4.2 只留措辭素材）。
- memory `feedback_review_observation_protocol` 的 A1 段已依 §1.4 的裁定改寫（A1 觀察期結束、refinement 回灌既有 Skill）；B 小實驗的定位不變。
- 沒有評估 Stop hook root 解析、doc gate 文件角色分類、B 小實驗——那是使用者已定的下一步順序，不在本文件範圍。
