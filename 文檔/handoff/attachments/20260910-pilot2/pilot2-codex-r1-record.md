# Pilot 2 — Codex formal branch review r1 — 七項紀錄

1. reviewer / model / effort: Codex MCP, gpt-5.6-sol, reasoning high, sandbox read-only, threadId 01a08a0b-45fd-7c91-9dfd-bb5135b6bf8a; dispatched 2026-09-10 ~06:29Z, returned ~07:00Z.
2. base + snapshot: base 368d586; worktree HEAD b07d571 + frozen working tree (13 blob hashes re-verified identical to pilot2-snapshot.md FINAL-ish list at 06:26Z before dispatch).
3. Context 異同: same five-field Task Context as fallback r1/r2 verbatim; Branch Info merged the r2 operating note (working tree included, `git diff 368d586`, condition-3 note). No known defects / prior findings / suspected locations added.
4. 第一輪 findings 按類型 (9 total, 4 P1 + 5 P2; author verification in brackets):
   - 決定性邊界 (rule text admits two readings): P1 spec.md:7 "unique within a task" [text verified; sentence self-qualifies with "on the same side" but plan.md:17 quotes it without the qualifier]; P1 schema:497 check 7 no fence/comment exclusion [text verified; retrospective:233 already records same family for checks 8–12, user ruled 2026-09-08 not to expand]; P1 schema:789/794 plan-key delimiter [text verified; 794–801 `###` exclusion is in-diff, delimiter absence pre-existing 932a044b]
   - stale verification: P1 verify.md:8/11 [verified; the 2026-09-10 補記 was inserted mid-command, splitting `diff -r ... superpowers-bridge` / `openspec/schemas/superpowers-bridge` across lines 11–12 — introduced by my r2 fix; full re-run already planned post-Codex in handoff]
   - canonical drift: P2 spec.md:3 field cardinality / one-line parsing absent from delta [verified: only line 13 mentions "cardinality" as scope boundary]
   - coverage gap: P2 design.md:124 vs three no-fixture rules [verified; retrospective:234 records it as deferred observation]
   - author-surface vs gate (D2 family): P2 templates/tasks.md:49 [verified; retrospective:232 "fifth recurrence"]; P2 schema:175 check 8 cardinality [verified; = D2, user-ruled deferred, work-map task-20260908-author-surface-gate-alignment]
   - evidence persistence: P2 work-map.jsonl:20 still cites `.superpowers/sdd/plan/code-rereview-fallback-3.md` [verified; fallback r1's P2 fix updated retrospective citations but not work-map]
5. reviewer 自主驗證行為 (self-reported in Merge Gate): ran `openspec schema validate`, `openspec validate --all --json` (5/5), JSON/JSONL parse, bundle/dogfood byte comparison, `git diff --check`; git blame for origin on two findings.
6. 已知但漏掉 (sealed list, 5 items, none reported → 5 MISS): schema:1180 84-char line (Nit); schema:532 grep exit-2 wording (Nit); check-10 absent-outcome fixture (Missing-Items class; Codex listed other missing fixtures but not this one); schema:175/:567 indent-depth mismatch (Important per 0909 Codex; this round reported D2 at :175 instead); f8–f13 never blind-run. Note: Codex emitted no Deferred Findings section at all.
7. mismatch / anchoring: Context mismatch = 3, all factual and all on my side — baseline list (36) omitted `.gitattributes` + 2 renormalized templates (39 tracked); 3 untracked report files not in baseline; R1 INDETERMINATE beyond the five fixes (declared in proposal §Impact). No anchoring observed on Task Context wording; reviewer did not echo Required-assurance phrases as findings.

Descriptive comparison with fallback r1/r2 (not A/B; different snapshot, model, round):
- All 5 fallback-r2 blocking findings were fixed before this dispatch; Codex reported none of them (consistent with fixed).
- Overlap with fallback: work-map path (extends fallback r1's evidence-persistence P2 to a surface r1 did not name); stale verify (fallback r2 "Missing Items: verify not re-run" → Codex P1).
- New to Codex: spec.md:7 wording, check 7 fence/comment, plan-key delimiter, canonical cardinality drift. Known-deferred items re-raised as blocking: D2, template:49, three no-fixture rules.
- Gate: ⛔ Blocked, gate_reason=IN_SCOPE_BLOCKING, [SENTINEL_VALID] contract=code. review-state noted code_review fail (rounds=3, digest null — noted from main cwd, worktree tree not visible to it).
[THREAD_ROTATED] plane=code_review from=01a08a0b-45fd-7c91-9dfd-bb5135b6bf8a reason=session-not-found(overnight MCP restart) | 2026-09-11T00:16:45Z

## Pilot 4 — fix-v2 branch review, NEW thread first dispatch (2026-09-11 05:25–05:33Z)

Old thread `01a08a0b` was not reachable (overnight MCP restart, same failure as the doc plane).
`[THREAD_ROTATED] plane=code_review from=01a08a0b to=01a08eed-df04-78e3-95b0-608dbd9e6df5 reason=session-not-found | 2026-09-11T05:25Z`
Per the rotation contract the new thread got a **first dispatch**: metadata + mandated exploration only. The four `[USER_SKIPPED]` dispositions were deliberately **withheld** from the prompt and reconciled here afterwards. The 08:15 prompt was not saved to disk, so the dispatch was rebuilt from the same branch template with every fact re-measured (39 tracked files, 9 commits, 2590+/499-, base `368d586`).

### Seven items
1. **Reviewer / model / effort**: Codex, `gpt-5.6-sol`, reasoning effort high, sandbox read-only.
2. **Base + snapshot**: base `368d586`, HEAD `b07d571` + uncommitted working tree; 39 tracked + 3 untracked branch-introduced reports.
3. **Context identical?** No — this was a first dispatch on a new thread, Task Context five fields present, dispositions withheld by contract.
4. **First-round findings by type**: 0 P0 / 2 P1 / 6 P2 / 1 Nit deferred / 0 out-of-scope. Gate `⛔ Blocked`, `gate_reason=IN_SCOPE_BLOCKING`.
5. **Reviewer's own verification behaviour**: ran `openspec schema validate` and `openspec validate --all --json` (5/5), parsed JSON/JSONL, compared the gitignored dogfood copy byte-for-byte against the 14-file source bundle, checked all 13 fixture directories against the answer table, and independently agreed the `文檔/handoff/` untracked files are out of the baseline.
6. **Known defects missed**: sealed list 5/5 **MISS** again — (1) the 84-char line at schema.yaml:1180, (2) check 7's `grep -c` exit-2 claim at :532, (3) check 10's absent-`outcome:` fixture gap, (4) the fixed-indent vs any-depth asymmetry at :175/:567, (5) the f8–f13 blind-run gap. Item 5's *surface* was raised but in the opposite direction (the README now understates the verification that exists), which is a different claim, so it is scored MISS on the sealed claim.
7. **Mismatch / anchoring**: no Context mismatch raised. No anchoring observed — the dispositions were withheld and the reviewer independently re-derived four of them.

### Disposition reconciliation (done here, not in the prompt)
| Finding | Covered by | Verdict |
|---|---|---|
| P1 `schema.yaml:797` fenced code / HTML comments in the task-line scanner | disposition 3 (verbatim identity match) | covered, does not block |
| P2 `schema.yaml:175` check 8 annotation cardinality | disposition 1 | covered, does not block |
| P2 `templates/tasks.md:46` wrapped line vs FORM-decides | disposition 2 | covered, does not block |
| P2 `design.md:123` missing mutation fixtures — **the four named rules** | disposition 4 | covered for those four |
| P2 `design.md:123` — the **compound stage-one/stage-two** case | nothing | **NOT covered** |
| P1 `schema.yaml:457` check 2 "every checkbox `[x]`" vs check 7's non-blocking `[~]` | nothing | **NOT covered** |
| P2 `design.md:62` etc. "subject unique within a task" in brainstorm/proposal/design | nothing | **NOT covered** |
| P2 `schema.yaml:462` checks 3 and 5 leave their gate effect undefined | nothing | **NOT covered** |
| P2 fixture `README:80` "f8–f13 未經任何獨立驗證" contradicted by the branch-introduced report | nothing | **NOT covered** |

All four uncovered findings were verified against primary sources before being reported as real:
- `schema.yaml:457-460` says confirm every checkbox is `- [x]` and its escape clause covers only `- [ ]`; `:544-548` says a fully enumerated `[~]` deferral keeps Overall Decision PASS. Confirmed contradiction.
- `brainstorm.md:79`, `proposal.md:19,56`, `design.md:62,66` read "同一 task 內 subject 唯一"; the corrected delta `specs/tdd-evidence-contract/spec.md:7` reads "unique within each side". Confirmed — the 2026-09-10 fix reached the delta spec and `plan.md:17` only.
- `schema.yaml:462-476`: check 4 is marked "(non-blocking)" and check 6 "(warning, non-blocking)", while checks 3 and 5 carry no such qualifier. Confirmed asymmetry.
- fixture `README:80` vs saved report `README:10` + `code-rereview-fallback-3.md` § Regression (13-fixture independent re-derivation). Confirmed; the blind-run distinction is still valid, the "no independent verification" clause is not.

### A1 four-step sweep — SECOND REAL SAMPLE (2026-09-11, subject-uniqueness wording)
- Step 1 (pre-`rg`): the uniqueness wording appears in **9 files**. Correct ("each side" present): `tasks.md:75`, both READMEs `:397`, the delta spec, `plan.md:17`. Incorrect: `brainstorm.md:79`, `proposal.md:19,56`, `design.md:62,66`.
- **The sweep found a 6th incorrect-candidate the reviewer did not name**: `design.md:71` ("不需要 subject 唯一").
- Steps 2–4 not yet run: the fix is pending the user's scope decision below (some of these artifacts are records rather than current authority).
- Running total for the A1 observation period: **2 samples, both of which surfaced at least one surface the reviewer had not named** (sample 1: `:264`; sample 2: `design.md:71`).

## Pilot 4 r2 (2026-09-14) — ⛔ Blocked, 1 P1 + 2 P2, all three caused by my own r1 fix round

Thread `01a08eed` survived the three-day gap (first reply came back **empty**; a resend asking for the gate section first delivered the full report — same delivery failure and same workaround as the doc plane on 09-11, now N=2).

The reviewer listed all six `[USER_SKIPPED]` dispositions unprompted. They were **not** in this round's prompt: they entered the thread on 2026-09-11 in the re-review dispatch that then failed on quota. The message landed even though the reply did not. Worth knowing: a quota-failed dispatch still mutates thread state.

All three findings verified against sources before acting:
- **P1** `templates/verify.md:33` and `openspec/changes/fix-v2-blocking-defects/verify.md:54` both still read 「所有 `- [ ]` 已變為 `- [x]`」 after check 2 was amended to accept `- [~]`. Confirmed — and fixture `f13` is a conforming `[~]` input, so the contradiction has a real trigger.
- **P2** `f13`'s answer row scores check 7 only ("這個 fixture 驗的是讀哪個檔、找到幾筆,不是 BLOCK 與否"). Confirmed.
- **P2** `proposal.md:62` §Impact lists "checks 7、9、10、11、12" — check 2 absent. Confirmed.

### A1 four-step sweep — THIRD REAL SAMPLE, and the one that found the habit's limit

**Sample 2's sweep produced a false green.** On 09-11 I swept for the *new* rule's vocabulary (`every checkbox`, `DEFERRED TASK`, `[~]`) and the post-sweep read clean. The two surfaces that actually still contradicted the amended rule state it in the *old* vocabulary — 「所有 `- [ ]` 已變為 `- [x]`」 — which contains none of those terms. The sweep could not have found them, and I declared the round consistent anyway.

Worse, I had `verify.md:54` on screen on 09-11 and wrote a note *underneath* it instead of recognising it as a surface restating the rule. So this is a search-term failure **and** a reading failure.

Sample 3's sweep was therefore run on the **old assertion's literal wording**, and found:
- the two surfaces the reviewer named (`templates/verify.md:33`, `verify.md:54`);
- **two the reviewer did not name** — `design.md:156` and `verify.md:23`, both listing the changed checks as "checks 7、9–12" with check 2 missing;
- **one that must NOT be changed** — `openspec/changes/archive/2026-08-31-fix-tdd-transitive-claim/verify.md:36`, an archived record of a verification that really did run under the old wording. Editing it would falsify a record. The sweep's value here was making that a **conscious** decision rather than a miss in either direction.

**Refinement this sample earns** (observation only — not a rule, not a Skill, not a gate): when a rule's wording is changed, sweep for **the wording being replaced**, not only the wording replacing it. A surface that still states the old rule is exactly the surface that will not contain the new rule's terms.

### Three numbers, cumulative over the A1 observation period
| Sample | Reviewer named | Sweep additionally found | Sweep missed |
|---|---|---|---|
| 1 (research doc, 09-11) | 2 | 1 (`:264`) | — |
| 2 (subject uniqueness, 09-11) | 5 | 1 (`design.md:71`) | — |
| 2 (check 2, 09-11) | — | 0 | **2** — found by the reviewer in r2 |
| 3 (check 2 propagation, 09-14) | 2 | 2, plus 1 correctly-left-alone archived record | — |

Three samples done. The observation period's material is complete enough to evaluate, but per the standing ruling it is **not** auto-promoted to a Skill or gate; the evaluation is the user's call.

### Fixes applied this round
`templates/verify.md` §2 attestation; `verify.md` §2 attestation and §23 check list; `proposal.md` §Impact plus a rationale sub-bullet for the bounded scope extension; `design.md` §實作順序 check list; the `f13` answer row now states check 2's expected verdict and is explicitly marked author-derived and not independently re-verified (the 09-08 re-derivation implemented checks 8–12 only — no independent result was manufactured).
Post-fix invariants: dogfood `diff -r --strip-trailing-cr` empty, `openspec schema validate` ✓, `openspec validate --all --json` 5/5.
r3 re-review dispatched on thread `01a08eed`.
