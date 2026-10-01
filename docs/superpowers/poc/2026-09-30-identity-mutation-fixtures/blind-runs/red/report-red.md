## case-01

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log（`git log ... | wc -l`），案例目錄無 git 歷史可讀
1: PASS — `openspec validate --all --json` 三個項目（session-policy、token-auth、update-token-auth）皆 valid:true
2: PASS — tasks.md 唯一一項為 `- [x]`，無 `- [ ]` 殘留
3: PASS — 已比對 specs/session-policy 與主 spec，記錄為 ✗ 需同步（delta 新增 REQ-4，主 spec 尚無）
4: PASS — design.md 談「absolute timeout complements idle timeout」，與 spec delta 的 REQ-4 session absolute timeout 主題一致，無偏移
5: 不適用於 fixture — 判定依據是 worktree 是否有未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 案例目錄下無 `docs/superpowers/specs/*.md`
7: PASS — tasks.md 無任何 `- [~]` deferred 任務
8: PASS — 該任務有且僅有一行 `- TDD: n/a — prose/doc-only`，reason 非空
9: PASS — 無任何 `TDD: applicable` 任務，RED/GREEN 存在性檢查無對象可套用
10: PASS — 無任何記錄可供檢查 outcome 標記
11: PASS — 無任何記錄可供檢查 subject 配對
12: PASS — tasks.md 任務號 `1.1` 與 plan.md entry key `1.1` 一一對應，兩側皆無重複

FINAL: PASS categories={}

## case-02

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步（RENAMED FROM 的標題文字與主 spec 現有標題完全相符，TO 尚未落地）
4: PASS — design.md 談「title-only change; body unchanged」，與 delta 的 RENAMED Requirements 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-03

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（含內文以 fenced code block 示範 `#### Scenario:` 寫法的段落，未被當成真實 scenario 而導致驗證失敗）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步（MODIFIED REQ-2 內容與主 spec 現有 REQ-2 不同）
4: PASS — design.md 談「boundary instant counts as expired」，與 delta 新增的 REQ-2-S3 邊界情境一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-04

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（MODIFIED 段落標的 REQ-7 在主 spec 不存在，但 `openspec validate` 未把這點視為結構錯誤）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「missing scope answers 403」，與 delta 的 REQ-7 Token scope 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-05

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/session-policy 與 specs/token-auth 兩個 delta 目錄與各自主 spec，皆記錄為 ✗ 需同步（RENAMED FROM 的標題文字與主 spec 現有無 REQ-ID 標題完全相符）
4: PASS — design.md 談「renamed to carry an identifier and modified in full」，與 delta 的 RENAMED+MODIFIED 組合一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-06

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步（RENAMED FROM 的標題文字與主 spec 現有 REQ-2 標題相符，TO 改為 REQ-7 尚未落地）
4: PASS — design.md 談「title-only change; body unchanged」，與 delta 的 RENAMED Requirements 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-07

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（ADDED 標題僅為 `REQ-6`、無附加描述文字，仍屬合法的 `### Requirement: <name>` 形式）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 新增的 token refresh 需求一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-08

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（ADDED 需求名稱為非數字形式 `REQ-FOO`，schema 對名稱字面沒有格式限制）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-09

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec（主 spec 另含一條無 REQ-ID 的 `Token audience` 需求），delta 記錄為 ✗ 需同步
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-10

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步（ADDED REQ-3，主 spec 現有 REQ-1/REQ-2/REQ-5 無衝突）
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-11

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（主 spec 內含一段以 fenced code block 示範 `#### Scenario:` 寫法的段落，未被當成真實 scenario）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-12

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（archive/ 下另有兩筆已封存的歷史 change，未影響本次驗證的三個項目）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-13

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/session-policy 與 specs/token-auth 兩個 delta 目錄與各自主 spec，皆記錄為 ✗ 需同步（其中一條 RENAMED TO 改為 `REQ-FOO Token expiry`，FROM 的標題文字與主 spec 現有無 REQ-ID 標題相符）
4: PASS — design.md 談「renamed to carry an identifier and modified in full」，與 delta 的 RENAMED+MODIFIED 組合一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-14

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（主 spec 內含一段以 fenced code block 示範 `### Requirement:` 寫法的段落，未被當成真實 requirement）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步（ADDED REQ-10，主 spec 現有 REQ-1/REQ-2/REQ-5 無衝突）
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-15

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（delta 內兩個 scenario 皆標記為 `REQ-6-S1`〔重複的 scenario 名稱〕，`openspec validate` 未把這點視為結構錯誤）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-16

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步（同一 delta 檔內含 ADDED REQ-6 與 MODIFIED REQ-2 兩個操作）
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 的 ADDED 部分主題一致；MODIFIED REQ-2 部分未見對應敘述，但 design.md 未言及與 spec 相反的內容，不構成 drift
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-17

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（主 spec 本身已存在兩條標題皆含 `REQ-2` 的需求：`REQ-2 Token expiry` 與 `REQ-2 Token lifetime`，`openspec validate` 未把這點視為結構錯誤）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-18

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（ADDED 需求名稱為非數字形式 `REQ-FOO`）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-19

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（delta 內第二個 scenario 標記為 `REQ-5-S5`，與其所屬需求 `REQ-6` 不一致，`openspec validate` 未把這點視為結構錯誤）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-20

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（delta 內第三個 scenario 標題未附 `REQ-2-S3` 這類代號、僅為 `token at the expiry instant`，仍屬合法的 `#### Scenario: <name>` 形式）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步（MODIFIED REQ-2 與主 spec 現有 REQ-2 不同）
4: PASS — design.md 談「boundary instant counts as expired」，與 delta 新增的邊界情境一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-21

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（ADDED `REQ-2 Token lifetime` 與主 spec 現有的 `REQ-2 Token expiry` 共用同一個 `REQ-2` 代號，`openspec validate` 未把這點視為結構錯誤）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「a single fixed lifetime of fifteen minutes」，與 delta 主題一致
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}

## case-22

PRECHECK: 不適用於 fixture — 判定依據之一是 commit log，案例目錄無 git 歷史可讀
1: PASS — 三個項目皆 valid:true（delta 內兩條需求皆標題為 `REQ-6`〔`REQ-6 Token refresh` 與 `REQ-6 Token introspection`〕，`openspec validate` 未把這點視為結構錯誤）
2: PASS — tasks.md 唯一一項為 `- [x]`
3: PASS — 已比對 specs/token-auth 與主 spec，記錄為 ✗ 需同步
4: PASS — design.md 談「refresh tokens exchanged for new access tokens」，與 delta 的第一條需求主題一致；第二條 Token introspection 需求未見對應敘述，但 design.md 未言及與 spec 相反的內容，不構成 drift
5: 不適用於 fixture — 判定依據是 worktree 未提交變更／commit range，案例目錄無 git 歷史可讀
6: PASS — 無 `docs/superpowers/specs/*.md`
7: PASS — 無 `- [~]` deferred 任務
8: PASS — TDD 標註格式正確、reason 非空
9: PASS — 無 `TDD: applicable` 任務可套用
10: PASS — 無記錄可檢查
11: PASS — 無記錄可檢查
12: PASS — 任務號與 entry key 1:1 對應

FINAL: PASS categories={}
