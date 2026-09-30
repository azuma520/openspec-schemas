## case-01

PRECHECK: 不適用於 fixture — 判定依据之一(commit evidence)須比对 HEAD 与 origin/main 的 git commit log,属这个 repository 的 git 历史,案例目录不是有意义的 git 历史。
1: PASS — `openspec validate --all --json` 三个 item(session-policy、token-auth、update-token-auth)全部 `valid: true`。
2: PASS — tasks.md 唯一任务 1.1 已标记 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」(delta 尚未合并进 main spec,属正常记录,不阻断)。
4: PASS — design.md(「一个固定十五分钟的存续期」)与 delta 新增的 REQ-2 Token lifetime 一致,未见 drift。
5: 無法判定 — 案例目录没有 `.git`,无法用 `git status`/worktree 状态判断是否有 unstaged files;这不是「取决于 git 历史」而是当下工作树状态,依 procedure 仍须尝试,但输入本身不具备可判定的基础。
6: PASS — `docs/superpowers/specs/*.md` 不存在,无 front-door 泄漏文件。
7: PASS — tasks.md 无 `- [~]` 被延后的任务,§7 无需列举。
8: PASS — 任务 1.1 底下恰有一行 `- TDD: n/a — prose/doc-only`,分隔符与非空理由皆合规。
9: PASS — 无标记 `TDD: applicable` 的任务,不要求 RED/GREEN 记录(vacuous)。
10: PASS — 同上,无记录可判定 outcome(vacuous)。
11: PASS — 同上,无记录可配对(vacuous)。
12: PASS — tasks.md 任务编号集合 `{1.1}` 与 plan.md 的 `## 1.1 — …` entry key 集合 `{1.1}` 双向相等,且各自无重复。
13: BLOCK — 用暂存复本实际执行 `openspec archive update-token-auth -y` 预览:成功产生候选态(`openspec/specs/token-auth/spec.md` 出现两个 `### Requirement: REQ-2` 区块——既有的「REQ-2 Token expiry」与新增的「REQ-2 Token lifetime」)。ADDED 条目使用了 main spec 已经持有的 ID REQ-2(13.D.1 违规),同一份候选态文件出现两个相同 local ID 的需求区块(13.C 违规)。经 `openspec show token-auth --type spec --json` 核对,requirementCount 与逐需求 scenario 数与文本计数一致,故非 13.E 发现。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-02

PRECHECK: 不適用於 fixture — 同上,commit evidence 子项依据 git 历史。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务 1.1 已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 描述与 delta(新增 refresh/introspection 两个需求)一致。
5: 無法判定 — 无 `.git`,worktree 状态不可判定。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记格式合规。
9: PASS — 无 applicable 任务(vacuous)。
10: PASS — 同上(vacuous)。
11: PASS — 同上(vacuous)。
12: PASS — 任务编号与 plan entry key 一一对应。
13: BLOCK — 归档预览成功。delta 的 `## ADDED Requirements` 区段内两个需求区块(「Token refresh」与「Token introspection」)都写成 `### Requirement: REQ-6`,同一 delta 文件内两个 ADDED 条目使用相同 ID,直接违反 13.D.1(「两个 ADDED 条目携带相同 ID → VIOLATION」)。候选态文件也因此出现两个 REQ-6 区块,13.C 同时命中。用 `openspec show update-token-auth --json --deltas-only` 核对:两个 ADDED entry 的 scenario 数(各 1)与文本一致,非 13.E 发现。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-03

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 与新增的 REQ-6 Token refresh 一致。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: PASS — 归档预览成功(`openspec/changes/archive/2026-05-01-add-introspect/`、`2026-06-01-drop-introspect/` 两个既存归档目录不影响本次预览,13.D.3 的编号上限判定明文只读当前 main spec、不读 archive)。候选态 token-auth 新增 REQ-6(数字,大于既有最大 REQ-5)、两个 scenario REQ-6-S1/REQ-6-S2 均带合法且互异的编号。`openspec show token-auth --type spec --json` 的 requirementCount(4)与逐需求 scenario 数与文本计数完全一致,`openspec show update-token-auth --json --deltas-only` 的 ADDED entry/scenario 数亦与文本一致。13.C/13.D/13.E 均无发现。

FINAL: PASS categories={}

## case-04

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md(「到期瞬间算作已过期」)与 delta 的第三个 scenario 一致。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。MODIFIED REQ-2 全文替换后新增第三个 scenario 标题为「token at the expiry instant」,不带任何 `REQ-2-Sm` 前缀,不符合 heading grammar——这是「新 scenario」(其本地 ID 不在 REQ-2 当前的 {S1,S2} 中),按 13.D.3「新 scenario 标题不带合法 ID → VIOLATION」命中,13.C 对候选态同一标题也重复命中(依规则记一次、引用两条规则)。`openspec show token-auth --type spec --json` 显示该需求 scenario 数为 3,与文本计数一致(CLI 不检查 ID 语法,只认标题结构),故本发现非 13.E 议题。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-05

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: session-policy, token-auth」。
4: PASS — design.md(「每个需求先改名取得 ID,再整篇 MODIFIED,文字不变」)准确描述了 delta 的 RENAMED+MODIFIED 组合。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。两点违规:(a) delta 的 RENAMED 将「Token expiry」(FROM 无 ID)改名为「REQ-FOO Token expiry」——FROM 无 ID 属于「迁移」情形,TO ID 依 13.D.3 须是新分配的数字 ID,但 REQ-FOO 不是数字形式,违反 13.D.3;(b) 本次 delta 完全未触及 session-policy,候选态沿用未变的 main spec,其 REQ-PB 需求下两个 scenario 标题(「idle session」「active session」)在候选态里仍不带合法 ID,13.C 违规(候选态检查覆盖所有 capability,不限于本次改动的)。核对 `openspec show update-token-auth --json --deltas-only`:RENAMED 的 from/to 文本、MODIFIED 的 scenario 数均与文本一致,`openspec show session-policy --type spec --json` 的 scenario 数(2)与文本计数一致——以上两处违规都不是 13.E 的计数不一致,而是 13.D.3/13.C 本身的语法判定。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-06

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 与 delta(新增 REQ-6 + 修改 REQ-2 增加第三个已编号 scenario)一致。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: PASS — 归档预览成功。候选态:REQ-6(数字、大于既有最大 REQ-5)新增且带合法编号;REQ-2 新增的第三个 scenario REQ-2-S3 编号大于既有最大 S2 且合法。`openspec show token-auth --type spec --json` 的 requirementCount(4)与逐需求 scenario 数(2,3,4,2)与文本计数完全一致,change-level 的 deltas JSON 亦一致。13.C/13.D/13.E 均无发现。

FINAL: PASS categories={}

## case-07

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 与新增的 REQ-6 一致(design.md 未提及既存的「Token audience」需求,但那与本次改动无关,不构成 drift)。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。main spec 本身已存在一个不带 ID 的既有需求「### Requirement: Token audience」,本次 delta 只 ADD REQ-6、未触及它,候选态原样保留此需求——13.C「需求标题不符合 grammar(无 ID)→ VIOLATION」命中。`openspec show token-auth --type spec --json` 的 requirementCount(5)与该需求的 scenario 数(1)均与文本计数一致,故这不是 13.E 的计数分歧,是 13.C 本身的语法判定。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-08

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md(「refresh token 换发新 access token」)与 delta 主旨一致(design.md 未提到 scenario 标题的 ID 笔误,但该笔误不构成设计层面的 drift)。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。ADDED 需求 REQ-6 底下第二个 scenario 标题写成「REQ-5-S5 expired refresh token」,其 `<REQ-ID>` 前缀(REQ-5)不等于所属需求区块的 ID(REQ-6)——13.C 明文「scenario 的 REQ-ID 必须恰好等于其所属需求区块的 ID……即使另有一个需求确实持有那个 ID,也是违规」,即使 REQ-5 本身在别处确实存在也一样违规。`openspec show token-auth --type spec --json` 该需求 scenario 数(2)与文本一致(CLI 不检查 ID 是否匹配父需求,只认结构),故这不是 13.E 议题。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-09

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 与新增的 refresh 需求一致。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。ADDED 新需求的 ID 写成 `REQ-FOO`——虽符合 heading grammar(`REQ-` 后接 `[A-Z0-9]+`),但 13.D.3 明文「新需求 ID 必须是数字形式 `REQ-<n>`,`REQ-FOO` 即使符合标题 grammar 也违规」。`openspec show token-auth --type spec --json` 的 requirementCount 与 scenario 数与文本一致,非 13.E 议题。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-10

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 未特别提及此改名,但也未与 delta 内容矛盾,未见明显 drift。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。两点违规:(a) delta 唯一的 RENAMED 条目 FROM=「REQ-2 Token expiry」TO=「REQ-7 Token expiry」,FROM 本身带 ID(REQ-2),按 13.D.2「改名必须保留原 ID,否则旧 ID 退役、新 ID 视为新生」,TO ID(REQ-7)≠ FROM ID(REQ-2)→ 违规;(b) 候选态里原来挂在 REQ-2 下的两个 scenario(REQ-2-S1、REQ-2-S2)文字未随改名更新,如今挂在新标题 REQ-7 底下,其 `<REQ-ID>` 前缀(REQ-2)不等于所属需求的 ID(REQ-7)→ 13.C 违规。核对 `openspec show update-token-auth --json --deltas-only` 的 rename.from/rename.to 与 `openspec show token-auth --type spec --json` 的 requirementCount/scenario 数,均与文本计数一致,以上两点都是语法/规则判定,非 13.E 计数分歧。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-11

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 与新增的 refresh 需求一致。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。与 case-09 相同模式:ADDED 新需求 ID 写成 `REQ-FOO`,非数字形式,违反 13.D.3。计数比对(requirementCount、scenario 数)与文本一致,非 13.E 议题。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-12

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: session-policy」(token-auth 本次未被此 delta 触及,N/A)。
4: PASS — design.md 与新增的 session-policy REQ-4 一致。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: PASS — 归档预览成功(`openspec/changes/archive/2026-05-01-add-sp-limit/`、`2026-06-01-drop-sp-limit/` 两个既存归档目录不影响,13.D.3 明文只读当前 main spec、不读 archive)。候选态 session-policy 新增 REQ-4(数字;当前 main spec 无任何数字 ID,空集合下任何正整数合法),scenario REQ-4-S1 同理合法。`openspec show session-policy --type spec --json` 的 requirementCount(2)、scenario 数(2,1)与文本计数一致;token-auth 未被触及,候选态维持原本干净的 REQ-1/REQ-2/REQ-5 结构,`openspec show token-auth --type spec --json` 的 requirementCount(3)与 scenario 数(2,2,4)亦与文本一致。13.C/13.D/13.E 均无发现。

FINAL: PASS categories={}

## case-13

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 与新增 refresh 需求一致。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。ADDED 需求 REQ-6 底下两个 scenario 标题都写成「REQ-6-S1」(第二个应是「expired refresh token」却仍标 S1),同一需求区块内本地 ID 重复,13.C「两个 scenario 标题在同一需求区块内携带相同本地 ID → VIOLATION」命中。`openspec show token-auth --type spec --json` 该需求的 scenario 数(2)与文本一致(CLI 只认结构、不检查重名),非 13.E 议题。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-14

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 与新增 REQ-6 一致(main spec 里既有的、给整合者示范的 fenced 范例与本次改动无关,不构成 drift)。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。main spec 的 REQ-2 需求区块内含一段给整合者看的 fenced code block,里面写了一行「#### Scenario: REQ-2-S9 example quoted heading」;本次 delta 未触及 REQ-2,候选态原样保留这段文字。按 13.A「逐行规则不识别 markdown 结构,fenced code block 内的标题形状的行仍被算作标题,即使 CLI 不算」,文本计数下 REQ-2 有 3 个 scenario(S9+S1+S2)。实测 `openspec show token-auth --type spec --json` 该需求(index 1)的 scenarios 长度为 2(CLI 正确忽略了 fence 内的行)。requirementCount 双方一致(4=4),故进入逐 scenario 数比对,该位置 3≠2 不一致 → 13.E 候选态比对 VIOLATION。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-15

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: session-policy, token-auth」。
4: PASS — design.md 与 delta(RENAMED+MODIFIED 两个 capability)一致。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: PASS — 归档预览成功。token-auth 的两个 RENAMED 都是「FROM 无 ID → 迁移分配新数字 ID」(REQ-1、REQ-2),当前 main spec 数字 ID 集合为空,任何正整数合法且互不相同;其下 scenario(REQ-1-S1/S2、REQ-2-S1/S2)同理属新分配、合法。session-policy 的 MODIFIED 完整替换 REQ-PB,新写入的 scenario(REQ-PB-S1/S2)也补上了合法编号,弥补了该 capability 原本未编号的问题。`openspec show token-auth --type spec --json`(requirementCount 2、scenario 数 2,2)与 `openspec show session-policy --type spec --json`(requirementCount 1、scenario 数 2)均与文本计数一致,change-level deltas JSON 亦一致。13.C/13.D/13.E 均无发现。

FINAL: PASS categories={}

## case-16

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 与新增 REQ-10 一致(main spec 里给整合者示范的 fenced 范例与本次改动无关)。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。main spec 的 REQ-5 需求区块下方有一段给整合者看的示例,fenced code block 内写了一整行「### Requirement: REQ-9 Example quoted heading」(是需求标题、不是 scenario);delta 未触及此处,候选态原样保留。按 13.A 逐行规则,这行仍被算作一个真实的需求标题,文本计数下候选态共有 5 个需求标题(REQ-1、REQ-2、REQ-5、fenced 的 REQ-9、REQ-10)。实测 `openspec show token-auth --type spec --json` 的 requirementCount 为 4(CLI 正确忽略 fence 内的行)。requirement 数量本身不一致 → 13.E 候选态比对在需求计数这一步就 VIOLATION;因两侧需求数不一致,该文件后续所有依赖对齐位置的 scenario 数比对按规则记为「无法可靠配对」的 UNDETERMINABLE(不是另一层单独判定为 PASS)。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-17

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`(CLI 的结构校验不检查 MODIFIED 条目是否能在 main spec 找到对应标题)。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」(delta 存在但显然未同步——main spec 里根本没有 REQ-7)。
4: PASS — design.md 未与此 MODIFIED 矛盾,未见明显 drift。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 用暂存复本执行 `openspec archive update-token-auth -y`:实测输出「token-auth MODIFIED failed for header "### Requirement: REQ-7 Token scope" - not found」、「Aborted. No files were changed.」,退出码 0 但三个成功条件不全部成立(change 目录仍存在、archive 目录未产生)——按 13.B「PREVIEW FAILED」,候选态不存在。因为 main spec 完全没有 REQ-7,delta 的 MODIFIED 条目无法解析(13.D.1 的 (a)(b)(c) 均不成立),这本身「不是 13.D 的发现,而是 preview 失败的后果」,记为 UNDETERMINABLE,并注明是引用文本。13.C 与 13.E 的候选态一半因此记为「未评估」(由这条 UNDETERMINABLE 涵盖),不当作 PASS。change-level 一半(不依赖 preview)另行核对:`openspec show update-token-auth --json --deltas-only` 该 MODIFIED entry 的 scenario 数为 1,与文本(REQ-7-S1 一个)一致,未见分歧。13.D 在「current state 单独可判定」的部分也未发现独立违规。
BLOCK 类别: 无法判定

FINAL: BLOCK categories={无法判定}

## case-18

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 未与此改名矛盾。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: PASS — 归档预览成功。delta 唯一的 RENAMED 条目 FROM=「REQ-2 Token expiry」TO=「REQ-2 Access token expiry」,ID 前后一致(仅描述文字改变),符合 13.D.2「改名必须保留原 ID」的允许情形。候选态里该需求下的 scenario(REQ-2-S1、REQ-2-S2)仍正确挂在 REQ-2 下,前缀一致,无 13.C 发现。`openspec show token-auth --type spec --json` 的 requirementCount(3)与 scenario 数(2,4,2)与文本一致,`openspec show update-token-auth --json --deltas-only` 的 rename.from/to 亦与文本一致。13.C/13.D/13.E 均无发现。

FINAL: PASS categories={}

## case-19

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 未与此 MODIFIED 矛盾。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。delta 本身的 MODIFIED REQ-2 全文替换里,就内嵌了一段给整合者看的 fenced code block,内含一行「#### Scenario: REQ-2-S9 example quoted heading」。按 13.A 逐行规则,这行仍被算作一个真实 scenario 标题,delta 文本对该 MODIFIED 条目的 scenario 计数为 4(S9+S1+S2+S3)。实测 `openspec show update-token-auth --json --deltas-only` 该 entry 的 `requirement.scenarios` 长度为 3(CLI 正确忽略 fence 内的行)——change-level 半边 4≠3,13.E VIOLATION。归档后候选态同一区块文字原样保留,`openspec show token-auth --type spec --json` 该需求(index 1)的 scenarios 长度亦为 3,候选态文本计数仍为 4——candidate-state 半边同样 4≠3,13.E 再记一笔 VIOLATION。requirementCount 双方均一致(change-level entry 数 1=1;candidate-state 需求数 3=3),故两处都是「计数一致后,scenario 数不一致」的直接 VIOLATION,不是 UNDETERMINABLE。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-20

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 未与此 ADDED 矛盾。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。ADDED 需求标题写成「### Requirement: REQ-6」,ID 后面没有任何描述文字。按 heading grammar「ID 后须有一个以上空白再接非空描述」,「ID 后面没有东西」明文视为「不带合法 ID」(与「### Requirement: REQ-6」范例完全对应),既是 13.D.3(新需求必须带合法 ID)的违规,也是 13.C(候选态标题不符合 grammar)的违规,依规则记一次、引用两条。`openspec show token-auth --type spec --json` 的 requirementCount(4)与该需求 scenario 数(2)与文本一致(CLI 只要标题结构存在就计入,不检查描述是否为空),非 13.E 议题。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-21

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 未与此 ADDED 矛盾。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。main spec 当前最大的数字需求 ID 是 REQ-5,delta 的 ADDED 新需求却编号为 REQ-3——按 13.D.3「新需求编号必须大于该 capability main spec 里目前每一个数字需求 ID」,REQ-3 < REQ-5,即使目前没有需求真的叫 REQ-3 也一样违规(规则原文举的正是这个反例模式)。`openspec show token-auth --type spec --json` 的 requirementCount(4)与 scenario 数(2,2,4,2)与文本一致,非 13.E 议题。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}

## case-22

PRECHECK: 不適用於 fixture — 同上。
1: PASS — 三个 item 全部 `valid: true`。
2: PASS — 任务已 `- [x]`。
3: PASS — 记录为「✗ Needs sync: token-auth」。
4: PASS — design.md 与新增 REQ-6 一致(main spec 里既有的 REQ-2 重复问题与本次 delta 无关,不构成 drift)。
5: 無法判定 — 无 `.git`。
6: PASS — 无泄漏文件。
7: PASS — 无 `[~]` 延后任务。
8: PASS — TDD 注记合规。
9: PASS — vacuous。
10: PASS — vacuous。
11: PASS — vacuous。
12: PASS — 编号一一对应。
13: BLOCK — 归档预览成功。main spec 本身已经存在两个使用相同本地 ID REQ-2 的需求区块(「REQ-2 Token expiry」与「REQ-2 Token lifetime」),这是既存于 main spec 的重复,本次 delta 只 ADD 了 REQ-6、完全没有触及 REQ-2,候选态原样保留这个重复——13.C「同一文件内两个需求区块携带相同本地 ID → VIOLATION」命中(candidate state 检查覆盖整份候选态文件,不只是本次改动触及的部分)。`openspec show token-auth --type spec --json` 的 requirementCount(5)与逐需求 scenario 数(2,2,1,4,2)与文本计数完全一致(REQ-2 的两个区块各自的 scenario 数在其自身位置上都对得上),故此发现是 13.C 本身的重复 ID 判定,不是 13.E 计数分歧。
BLOCK 类别: 违规

FINAL: BLOCK categories={违规}
