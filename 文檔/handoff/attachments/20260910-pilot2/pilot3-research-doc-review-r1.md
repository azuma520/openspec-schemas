<!-- Pilot 3: research doc 2026-09-10-contract-drift-archaeology.md, Codex gpt-5.6-sol high, threadId 01a08aa4-79e2-74f3-8c4f-96071d3ca86e, dispatched ~09:27Z 2026-09-10, Task Context five fields present -->
Context mismatch: 1 (factual, on author's side) — "62 條 finding" overclaim: 0907 five P2 missing, rows merge findings.
🔴 ×8 (all verified true by author against sources before fixing): scope/atomicity; H1 cffe99a vs 787b14c; H5 misread of plan-structure-comparison row 3 vs row 4; H11 repeated a claim provenance analysis had already corrected; H12 "全 Nit" wrong; tasks.md:146 mis-edited to :147 + :1177 stale; internal count contradictions; README row.
🟡 ×1: 影響面 had 2 hits (README.zh-TW:175, fragment:32) — true, different sense.
Sealed list (5 items) vs report: #1 (#62 weak row) MISS; #2 (rows 11–18 from ledger) — not raised; #3 (估計 counts) — partly HIT via count-consistency 🔴; #4 (表列 3 wording) HIT (as part of H5 🔴); #5 (README "…") HIT (README 🔴).
Reviewer self-verification: git history (cffe99a/787b14c), line-number resolution in worktree, rg for 影響面, cross-file consistency with 0909 provenance doc and pilot2 record.
Anchoring on Task Context: none observed; reviewer contradicted the Context's "全部 62 條" directly.

## r2 (codex-reply, same thread) — ⛔ 6 🔴, 0 🟡
All six verified true by author: coupling-table surfaces overstated (CLAUDE.md / canonical spec not on the table) + Q5 stale "commit 級"; H2 bare :1177; G secondary count 8→12 (author counted main column only); B "全部 tokenizer" vs Q8 10/12; H11 "四條全在作者面" vs #53/#54 intra; Q5 "Nit 全漏" vs H12. All fixed; G recount by script.
## r3 dispatch: Codex quota exhausted at ~09:50Z (resets 19:40 local). Per user ruling (2026-09-10) no fallback dispatched; gate stays ⛔ (doc_review fail r2 noted). Resume with codex-reply on the same thread after 19:40, or fresh dispatch if the thread rotates (2 replies so far, R-a threshold 3).
[THREAD_ROTATED] plane=doc_review from=01a08aa4-79e2-74f3-8c4f-96071d3ca86e reason=session-not-found(overnight MCP restart) | 2026-09-11T00:11:20Z

## new thread 01a08dce r1 (2026-09-11 00:19Z, fresh first dispatch, Task Context five fields) — ⛔ 5 🔴 + 2 🟡
Context mismatch: 1 (path-resolution rule too narrow — factual, author's side).
All five 🔴 verified true and fixed: resolution basis enumerated; report copies described as untracked; H1 → coupling table zero hits (retrospective attribution flagged); SSOT search result lists artifact-level owner declarations (templates/design.md:20, loosen-plan/design.md:42, CLAUDE.md dogfooding); B recoded into 5 subtypes (lexical 3 / record grammar 5 / set logic 1 / control flow 1 / message 2) and dependents regenerated.
🟡 ×2 deferred ([NIT_DEFERRED] as logged by reviewer).
Observation: a fresh reviewer on a rotated thread found 5 new 🔴 the previous thread's two rounds had not raised (all real) — rotation cost = new eyes, not just lost context.
r2 dispatch attempted 00:23Z → Codex quota exhausted (resets 13:12 local). No fallback per user ruling. doc_review fail noted (rounds=3).

## new thread 01a08dce r2 (2026-09-11 05:1xZ) — ⛔ 2 🔴 + 1 🟡
First dispatch attempt returned EMPTY content (no report). Re-sent once asking for the Gate section FIRST so the verdict survives truncation — second attempt delivered a full report. Same failure family as the reviewer-verdict-delivery item (work-map task-20260904-reviewer-verdict-delivery); putting the gate first worked as a workaround.
Both 🔴 verified true against primary sources before fixing:
- H1 :35 attributed the dogfood-sync rule to the coupling table; verified against worktree CLAUDE.md — coupling table is :185-190 (six rows, no orig↔copy), sync rule is the dogfooding section :155. Fixed; now consistent with :139.
- Stale "tokenizer" labels after the r1 B recoding. Verified: fallback r1's three findings are #28 (record grammar), #31 (lexical), #32 (message) per the §2 rows.
🟡 ×1 (path-family enumeration not exhaustive) — reviewer logged it [NIT_DEFERRED] itself.
**Reviewer sub-claim NOT upheld**: report said line 250's five recurring units include "three record-grammar cases". Traced §1 H8's five claims → four lexical + one record grammar (#28). Rewrote the line to state that breakdown and put the discrepancy back to the reviewer in r3.

### A1 four-step sweep — FIRST REAL SAMPLE (2026-09-11)
- Step 1 (pre-`rg`): `tokenizer` → 8 hits; 耦合表誤歸因 → 1 hit; experiment-scope terms → 3 hits.
- Step 2 (fix): 4 edits, then 1 more from the sweep.
- Step 3 (post-`rg`): `tokenizer` 8 → 6, all six verified legitimate uses (taxonomy definition, contrast usage, correctly-qualified references).
- Step 4 (`diff -r --strip-trailing-cr`): bundle vs dogfood copy IDENTICAL; no bridge file touched this round (`git status -- superpowers-bridge` = 0), so the check confirms the invariant rather than a change.
- **Three numbers**: sweeps done = 1 / surfaces hit per sweep = 8 for the main term, of which 2 were stale / **reviewer named 2 defects, the sweep found a 3rd surface (§4 :264) the reviewer did not name**.
- Value observed: the sweep's marginal find (:264) was the same stale label in a different section — exactly the "同一字串的其他出現處" class the habit targets.

## new thread 01a08dce r3 (2026-09-11 05:23Z) — ✅ Mergeable, 0 🔴
All previous blocking items confirmed addressed. Reviewer also adjudicated my pushback: my four-lexical/one-record-grammar derivation is supported; the apparent "three" arose because #31 bundles two claims into one classification unit. `doc_review pass` noted (digest sha256:efad5e34…, rounds reset to 0).
Rounds used on this thread: 3 (r1 first dispatch + 2 replies). fast-tier cap 6 — under cap. R-a rotation threshold (3 replies) not reached.
