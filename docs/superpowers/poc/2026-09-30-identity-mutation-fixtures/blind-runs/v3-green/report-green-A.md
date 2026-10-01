## case-01

PRECHECK: NOT_APPLICABLE — this verify PRECHECK's "commit evidence" step depends on git commit history (`git log ... | wc -l`), which is a git-status-based judgement; per procedure this check is reported NOT_APPLICABLE regardless of the file-based half.
1: PASS — `openspec validate --all --json` returns `valid: true` for both specs and the change, 0 failures.
2: PASS — tasks.md's only task (1.1) is checked `- [x]`.
3: PASS — token-auth delta (MODIFIED REQ-2) is not yet reflected in `openspec/specs/token-auth/spec.md` → recorded as "Needs sync", the expected pre-archive state.
4: PASS — design.md's decision to tighten REQ-2 (no clock-skew grace) aligns with the delta's MODIFIED REQ-2 text; no drift found.
5: NOT_APPLICABLE — depends on working-tree/commit status ("no unstaged files").
6: PASS — `ls docs/superpowers/specs/*.md` finds nothing; no front-door routing leak.
7: PASS — tasks.md has no `- [~]` deferred tasks, so an empty section 7 does not block.
8: PASS — task 1.1 carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation.
9: PASS — task is `TDD: n/a` and carries no RED/GREEN records, which is conforming.
10: PASS — no records exist to check outcome markers on.
11: PASS — no task is `TDD: applicable`, so nothing to pair.
12: PASS — tasks.md task number `1.1` and plan.md entry key `1.1` correspond 1:1, no duplicates either side.
13: BLOCK — archive-preview succeeded (candidate state produced). The delta's MODIFIED REQ-2 adds a third scenario heading `#### Scenario: token at the expiry instant` with no `<REQ-ID>-S<m>` prefix at all — it carries no legal ID. This is a VIOLATION under 13.D.3 (a new scenario heading with no legal ID) and the identical heading also fails 13.C's candidate-state grammar check (scenario heading not matching the grammar) in the merged `openspec/specs/token-auth/spec.md` — recorded once, citing both rules. All 13.E count comparisons (change-level 3 vs 3 scenarios; candidate-state requirement count 3 vs 3, REQ-2 scenario count 3 vs 3) agree, so no additional UNDETERMINABLE finding arises from counting.

FINAL: BLOCK | categories=VIOLATION

## case-02

PRECHECK: NOT_APPLICABLE — same git-dependent commit-evidence reasoning as case-01.
1: PASS — `openspec validate --all --json` returns `valid: true` for all 3 items.
2: PASS — task 1.1 is `- [x]`.
3: PASS — delta (ADDED REQ-2 Token lifetime) not yet in main spec → "Needs sync".
4: PASS — design.md's token-lifetime decision is reflected in the delta; no drift found.
5: NOT_APPLICABLE — git working-tree dependent.
6: PASS — no `docs/superpowers/specs/*.md` files.
7: PASS — no deferred tasks.
8: PASS — well-formed `TDD: n/a — prose/doc-only`.
9: PASS — n/a task, no records, conforming.
10: PASS — vacuous, no records.
11: PASS — vacuous, no applicable tasks.
12: PASS — 1:1 task/plan key correspondence.
13: BLOCK — archive preview succeeded. The delta ADDs a new requirement under the heading `### Requirement: REQ-2 Token lifetime`, but `REQ-2` is already the ID of the existing main-spec requirement "Token expiry" — this is a VIOLATION under 13.D.1 ("an ADDED entry carrying an ID that the main spec already holds"). The resulting candidate `openspec/specs/token-auth/spec.md` literally contains two requirement blocks both carrying local ID `REQ-2` ("Token expiry" and "Token lifetime") — a second VIOLATION under 13.C ("two requirement blocks in one file carrying the same local ID"). Count-based 13.E comparisons (entry counts, scenario counts, candidate requirementCount 4 vs CLI 4) all agree, since the CLI happily merges both headings without detecting the ID collision — the collision is a content-identity defect, not a count defect.

FINAL: BLOCK | categories=VIOLATION

## case-03

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — ADDED REQ-FOO not yet in main spec → "Needs sync".
4: PASS — design.md's token-refresh rationale matches the delta; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. The delta ADDs a brand-new requirement with ID `REQ-FOO`, which matches the heading grammar (`REQ-[A-Z0-9]+`) and does not collide with any existing ID, so 13.C finds no grammar/duplicate problem. However 13.D.3 requires a newly allocated requirement ID to be NUMERIC (`REQ-<n>`); `REQ-FOO` is non-numeric → VIOLATION ("`REQ-FOO` under ADDED is a violation although it matches the heading grammar", per the rule's own worked example). Scenario IDs (`REQ-FOO-S1`, `REQ-FOO-S2`) are internally consistent and not themselves flagged. Count-based 13.E comparisons all agree.

FINAL: BLOCK | categories=VIOLATION

## case-04

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — ADDED REQ-10 not yet in main spec → "Needs sync".
4: PASS — design.md matches the delta's intent; no drift found.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. The CURRENT main spec's REQ-5 body contains a fenced example quoting a heading-shaped line, `### Requirement: REQ-9 Example quoted heading`, inside a markdown code block. Per 13.A this line IS counted as a real requirement heading by this check (literal line match, fence-blind), although the OpenSpec CLI (which respects fencing) does not count it. I verified this directly against the generated candidate file (preview `openspec/specs/token-auth/spec.md`): literal count of `### Requirement:` lines there = 5 (REQ-1, REQ-2, REQ-5, the phantom REQ-9, and the new REQ-10), but the CLI's `openspec show token-auth --type spec --json` for the same candidate state reports `requirementCount: 4`. This is a disagreement at the requirement-count level → VIOLATION (13.E, candidate-state half), and because the counts disagree, the per-position scenario-count comparisons that depend on this count can no longer be paired reliably → UNDETERMINABLE (13.E's dependent-finding rule), recorded as a separate finding alongside the VIOLATION, not absorbed by it. (Separately, the phantom REQ-9 does not retroactively make the new REQ-10 illegal: read literally by this check, it also raises the "current" numeric maximum in the main spec to 9, and REQ-10 > 9 still satisfies 13.D.3's allocation rule, so no additional violation arises there.)

FINAL: BLOCK | categories=VIOLATION,UNDETERMINABLE

## case-05

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid (session-policy, token-auth, update-token-auth).
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (ADDED REQ-4 to session-policy) not yet in main spec → "Needs sync".
4: PASS — design.md's absolute-timeout rationale matches the delta; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: PASS — archive preview succeeded (`openspec/specs/session-policy/spec.md` updated with `+1 added`). The delta ADDs REQ-4 to session-policy, whose current main spec has only the non-numeric `REQ-PB` — so the "current numeric maximum" set is empty and any positive integer satisfies 13.D.3's allocation rule; REQ-4 qualifies trivially. No ID collisions, no malformed headings, and candidate requirementCount (2) matches the CLI's reported `requirementCount: 2` with no scenario-count mismatches. This change's directory also contains two unrelated, already-archived changes (archive/2026-05-01-add-sp-limit, archive/2026-06-01-drop-sp-limit adding and then removing a REQ-3 in session-policy) — per 13.D.3 and the check's own stated scope, this check does not read openspec/changes/archive/ or git history, so that retired REQ-3 has no bearing on this check's verdict (it is only relevant to the specs artifact instruction's separate, unverified historical-maximum authoring obligation).

FINAL: PASS

## case-06

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (2x ADDED) not yet in main spec → "Needs sync".
4: PASS — design.md covers both refresh and introspection; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. The delta file contains two separate ADDED requirement entries, "Token refresh" and "Token introspection", BOTH headed `### Requirement: REQ-6 ...` — a VIOLATION under 13.D.1 ("two ADDED entries in one delta file carrying the same ID"). Verified directly in the generated candidate `openspec/specs/token-auth/spec.md`: both blocks appear verbatim with local ID `REQ-6`, a second VIOLATION under 13.C ("two requirement blocks in one file carrying the same local ID"). All count-based 13.E comparisons (2 ADDED entries, 1 scenario each, candidate requirementCount 5 vs CLI 5) agree — again the CLI silently accepts the duplicate ID, so only content-identity rules catch it.

FINAL: BLOCK | categories=VIOLATION

## case-07

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — rename not yet applied to main spec → "Needs sync".
4: PASS — design.md's rename rationale matches the delta; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded (`-> 1 renamed`). The RENAMED pair is `FROM: REQ-2 Token expiry` -> `TO: REQ-7 Token expiry`. The FROM heading carries an ID (`REQ-2`), so this is NOT the no-ID migration exception, and 13.D.2 requires the TO ID to equal the FROM ID; `REQ-7 != REQ-2` -> VIOLATION ("giving a contract a different ID is never a rename — the old ID is retired and a new one is born"). The candidate state itself is internally well-formed (REQ-1, REQ-5, REQ-7 all legal and unique, confirmed via the CLI's candidate output and the generated spec file), so 13.C raises nothing further, and the 13.E ID-pair comparison (text FROM/TO vs CLI rename.from/rename.to) agrees on what the IDs literally are — the violation is a business-rule (identity-preservation) violation, not a text/CLI disagreement.

FINAL: BLOCK | categories=VIOLATION

## case-08

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta not yet in main spec → "Needs sync".
4: PASS — design.md matches delta intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. The ADDED requirement is headed `### Requirement: REQ-6 Token refresh`, but its second scenario is headed `#### Scenario: REQ-5-S5 expired refresh token` — its `<REQ-ID>` prefix (`REQ-5`) does not match the ID of the requirement block it sits under (`REQ-6`). Per the heading grammar this scenario heading does not match the grammar at all (no legal ID), which is a VIOLATION under 13.C ("a scenario heading ... whose <REQ-ID> is not exactly the ID of the requirement block it belongs to — a violation even when a requirement carrying that other ID exists elsewhere"), and the same heading is also a VIOLATION under 13.D.3 (a new scenario heading carrying no legal ID) — recorded once, citing both rules. Verified directly in the generated candidate file. Count-based 13.E comparisons (2 scenarios text vs 2 CLI; candidate requirementCount 4 vs 4) agree, since the counting rule only counts scenario headings, not their ID correctness.

FINAL: BLOCK | categories=VIOLATION

## case-09

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta not yet in main spec → "Needs sync".
4: PASS — design.md matches delta intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. Identical pattern to case-03: the delta ADDs a new requirement with a non-numeric ID (`REQ-FOO`), which is grammar-legal and non-colliding (so 13.C raises nothing) but fails 13.D.3's requirement that a newly allocated requirement ID be NUMERIC -> VIOLATION. Count-based 13.E comparisons all agree.

FINAL: BLOCK | categories=VIOLATION

## case-10

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta not yet in main spec → "Needs sync".
4: PASS — design.md matches delta intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. The ADDED requirement `REQ-6 Token refresh` carries TWO scenario headings, both literally `#### Scenario: REQ-6-S1 ...` (identical local ID `REQ-6-S1` used twice under the same requirement block) — verified directly in the generated candidate file. This is a VIOLATION under 13.C ("two scenario headings in one requirement block carrying the same local ID"). Count-based 13.E comparisons (2 scenarios text vs 2 CLI; candidate requirementCount 4 vs 4) agree, since raw counting doesn't check ID uniqueness — only the content-identity rule catches the duplicate.

FINAL: BLOCK | categories=VIOLATION

## case-11

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — rename not yet applied to main spec → "Needs sync".
4: PASS — design.md matches the rename intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: PASS — archive preview succeeded (`-> 1 renamed`). The RENAMED pair is `FROM: REQ-2 Token expiry` -> `TO: REQ-2 Access token expiry` — the FROM ID (`REQ-2`) equals the TO ID (`REQ-2`); this is a legitimate description-only rename and satisfies 13.D.2. The candidate state (verified via the generated spec file and the CLI's candidate JSON) has REQ-1, REQ-5, REQ-2 all unique and well-formed — no 13.C violation. The 13.E ID-pair comparison (text FROM=REQ-2/TO=REQ-2 vs CLI rename.from="REQ-2 Access token expiry" read under the grammar as ID REQ-2, rename.to likewise REQ-2) agrees. No count mismatches anywhere. This is the clean, correctly-identity-preserving rename case.

FINAL: PASS

## case-12

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (MODIFIED REQ-2) not yet in main spec → "Needs sync".
4: PASS — design.md matches delta intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. The delta's MODIFIED REQ-2 body contains a fenced example, a markdown code block containing the line `#### Scenario: REQ-2-S9 example quoted heading`, which per 13.A is counted literally as a real scenario heading by this check even though it sits in a code fence (and even though the OpenSpec CLI, which is fence-aware, does not count it). I confirmed this directly: the delta file literally shows 4 scenario headings under this MODIFIED entry (the phantom S9, S1, S2, S3), while the CLI's --deltas-only JSON reports `requirement.scenarios` with only 3 entries for the same delta — a disagreement -> VIOLATION (13.E, change-level half, scenario-count mismatch at this MODIFIED entry, 4 vs 3). The same phantom carries into the generated candidate file (verified directly), producing an identical disagreement in the candidate-state half: candidate text shows 4 scenario headings under REQ-2 vs the CLI's candidate JSON `requirements[1].scenarios.length` of 3 -> a second VIOLATION (13.E, candidate-state half). The phantom heading is itself grammatically well-formed and non-duplicate (no other S9 exists), so 13.C raises nothing on its own, and the quoted scenario would in any case be a "new" scenario (9 > 2, the current max under REQ-2) and so would not fail 13.D.3's allocation rule even if it were real.

FINAL: BLOCK | categories=VIOLATION

## case-13

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (ADDED REQ-6) not yet in main spec → "Needs sync".
4: PASS — design.md matches delta intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: PASS — archive preview succeeded (`+1 added`). The delta cleanly ADDs `REQ-6 Token refresh` with two properly-IDed scenarios (`REQ-6-S1`, `REQ-6-S2`); the current main spec's numeric maximum is 5, so `REQ-6 > 5` satisfies 13.D.3's allocation rule, and the candidate state (verified via the generated spec file and candidate JSON, requirementCount 4 = 4) has no duplicate or malformed IDs. This change directory also contains two unrelated, already-archived changes (archive/2026-05-01-add-introspect ADDING, and archive/2026-06-01-drop-introspect REMOVING, a *different* REQ-6 Token introspection). Per 13.D.3 and the check's stated scope, this check never reads openspec/changes/archive/ or git history, so that retired REQ-6 usage does not make the new REQ-6 here a violation under this check — reuse-of-a-retired-ID is explicitly out of this check's reach ("a number that was once used and has since been retired is NOT rejected here"), and is only the specs artifact instruction's separate, unverified authoring obligation.

FINAL: PASS

## case-14

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (ADDED REQ-6) not yet in main spec → "Needs sync".
4: PASS — design.md matches delta intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. This time the fenced phantom scenario heading (`#### Scenario: REQ-2-S9 example quoted heading` inside a markdown code block) sits in the CURRENT main spec's REQ-2 body, not in the delta (the delta here is a clean ADDED REQ-6, untouched REQ-2). Because 13.C evaluates every heading in the full candidate state (not only the touched parts), and this delta doesn't modify REQ-2, the phantom carries through unchanged into the candidate file — confirmed directly: the generated candidate openspec/specs/token-auth/spec.md literally shows 3 scenario headings under REQ-2 (phantom S9, S1, S2), while the CLI's candidate JSON reports only 2 scenarios for that same requirement (`requirements[1].scenarios.length == 2`). This disagreement is a VIOLATION under 13.E's candidate-state half (scenario-count mismatch at the REQ-2 position); the overall candidate requirementCount (4 vs 4) agrees since the phantom is a scenario heading, not a requirement heading. The phantom is itself grammar-legal and non-duplicate, so 13.C's own rules raise nothing further.

FINAL: BLOCK | categories=VIOLATION

## case-15

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (2 operations) not yet in main spec → "Needs sync".
4: PASS — design.md matches both delta operations; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: PASS — archive preview succeeded (`+1 added, ~1 modified`). The ADDED REQ-6 Token refresh (6 > current max 5) and the MODIFIED REQ-2 Token expiry (adding a cleanly-IDed third scenario REQ-2-S3, with 3 > the current max of 2 under REQ-2) both satisfy 13.D.3's allocation rule; unlike case-01/case-12, every scenario heading here carries a proper REQ-2-Sn ID, with no missing IDs or quoted/fenced look-alikes. Verified directly against the generated candidate file: no duplicate or malformed headings. All 13.E count comparisons agree at every level (change-level: 2 scenarios for ADDED, 3 scenarios for MODIFIED, both matching CLI; candidate-state: requirementCount 4 vs 4, REQ-2 scenario count 3 vs 3).

FINAL: PASS

## case-16

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (ADDED REQ-3) not yet in main spec → "Needs sync".
4: PASS — design.md matches delta intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. The delta ADDs a new requirement with ID `REQ-3`. The current main spec's largest numeric requirement ID is `REQ-5`; 13.D.3 requires a newly allocated requirement ID to be greater than every numeric ID currently in the main spec, regardless of whether that specific number is already in use — `REQ-3 < REQ-5` -> VIOLATION, exactly matching the rule's own worked example ("ADDED REQ-4 is a violation even though no current requirement holds REQ-4"). REQ-3 does not collide with any existing ID, so 13.C's grammar/duplicate rules raise nothing. Count-based 13.E comparisons all agree.

FINAL: BLOCK | categories=VIOLATION

## case-17

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (5 operations across 2 specs) not yet in main spec → "Needs sync" for both capabilities.
4: PASS — design.md matches the ID-migration intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: PASS — archive preview succeeded (`~1 modified` session-policy; `~2 modified, ->2 renamed` token-auth). This is a legitimate migration: both main specs currently hold UNNUMBERED requirements/scenarios (`### Requirement: Token issuance` / `Token expiry` with unnumbered scenarios in token-auth; REQ-PB's scenarios are themselves unnumbered in session-policy). The two RENAMED pairs (`Token issuance`->`REQ-1 Token issuance`, `Token expiry`->`REQ-2 Token expiry`) each have a FROM heading carrying NO ID — the explicit migration exception in 13.D.2 — so their TO IDs (REQ-1, REQ-2) are new allocations, and since the current numeric-ID set in token-auth is empty, any positive integer satisfies 13.D.3; both pass. The MODIFIED entries for REQ-1/REQ-2 resolve, via 13.D.1(a), to the FROM requirements through the same-delta-file RENAMED pairs, and since the FROM requirements' scenarios are themselves unnumbered, the current scenario-ID set under each is empty, so the newly-IDed scenarios (REQ-1-S1/S2, REQ-2-S1/S2) are all new and all satisfy the (vacuous) allocation rule. The session-policy MODIFIED entry resolves directly by existing ID match (REQ-PB->REQ-PB, no rename involved there), and its new REQ-PB-S1/S2 scenario IDs are likewise new against an empty current scenario-ID set. Verified directly against the generated candidate files: no duplicate/malformed headings in either capability, and all 13.E count/ID-pair comparisons agree at both the change level and the candidate-state level (token-auth candidate requirementCount 2 vs 2; session-policy candidate requirementCount 1 vs 1; every per-position scenario count matches).

FINAL: PASS

## case-18

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta not yet in main spec → "Needs sync".
4: PASS — design.md matches delta intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. The ADDED requirement's heading is literally `### Requirement: REQ-6` with nothing after the ID — exactly the schema's own illustrative example of an illegal heading ("`### Requirement: REQ-3` (nothing after the ID) is illegal"). Verified directly in the generated candidate file: the heading reads `### Requirement: REQ-6` with no description. This is a VIOLATION under 13.D.3 (a new requirement heading carrying no legal ID — "an ID with nothing after it") and the same heading is also a VIOLATION under 13.C's candidate-state grammar check — recorded once, citing both rules. The two scenarios under it (REQ-6-S1, REQ-6-S2) claim REQ-6 as their parent ID, but since the parent heading itself carries no legal local ID under the grammar, these scenario headings cannot be said to legitimately match "the ID of the requirement block it belongs to" either; I treat this as part of the same underlying defect rather than a separate, countable violation. Count-based 13.E comparisons (2 scenarios text vs 2 CLI; candidate requirementCount 4 vs 4) agree — the count-level checks don't look at whether a heading has a legal ID.

FINAL: BLOCK | categories=VIOLATION

## case-19

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (ADDED REQ-6) not yet in main spec → "Needs sync".
4: PASS — design.md matches delta intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. The delta itself (ADDED REQ-6 Token refresh, 6 > current numeric max 5) is clean on its own. However, the CURRENT main spec openspec/specs/token-auth/spec.md already contains a pre-existing identity defect unrelated to this delta: it holds TWO requirement blocks both carrying local ID REQ-2 — "Token expiry" and "Token lifetime" (with scenario REQ-2-S3). Per 13.B, the current state is not itself graded by 13.C, but since this delta does not touch REQ-2, both blocks carry through unchanged into the candidate state, which 13.C DOES grade in full — verified directly in the generated candidate file, which still literally contains both REQ-2 blocks. This is a VIOLATION under 13.C ("two requirement blocks in one file carrying the same local ID"), surfaced only because archiving this change finally subjects the whole main spec to the full-grammar candidate check. Count-based 13.E comparisons (candidate requirementCount 5 vs CLI 5) agree, since duplicate IDs don't change the raw count.

FINAL: BLOCK | categories=VIOLATION

## case-20

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (5 operations across 2 specs) not yet in main spec → "Needs sync" for both capabilities.
4: PASS — design.md matches the migration intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. This is the same unnumbered-main-spec migration setup as case-17 (Token issuance/Token expiry with no ID in the current main spec), but the second RENAMED pair here is `FROM: Token expiry` (no ID) -> `TO: REQ-FOO Token expiry`. Since the FROM heading carries no ID, this is a legitimate migration under 13.D.2's exception, so the TO ID (REQ-FOO) is treated as a NEW allocation subject to 13.D.3 — which requires newly allocated requirement IDs to be NUMERIC. REQ-FOO is non-numeric -> VIOLATION, exactly the same defect as case-03/case-09 but reached via the RENAMED-migration path rather than ADDED. (The first RENAMED pair, Token issuance->REQ-1 Token issuance, is clean, matching case-17.) REQ-FOO's heading is otherwise grammar-legal and non-duplicate, so 13.C raises nothing, and the 13.E FROM/TO ID-pair comparison (text vs CLI rename.to="REQ-FOO Token expiry") agrees that the ID literally is REQ-FOO — the violation is purely the numeric-allocation rule, not a text/CLI disagreement. The session-policy MODIFIED REQ-PB entry and its new REQ-PB-S1/S2 scenarios are clean, as in case-17.

FINAL: BLOCK | categories=VIOLATION

## case-21

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid.
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (ADDED REQ-6) not yet in main spec → "Needs sync".
4: PASS — design.md matches delta intent; no drift.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — archive preview succeeded. The delta itself (ADDED REQ-6 Token refresh, 6 > current numeric max 5) is clean. However the CURRENT main spec already contains a pre-existing, entirely unnumbered requirement, `### Requirement: Token audience` (with an unnumbered scenario `#### Scenario: wrong audience`), sitting between REQ-2 and REQ-5 and untouched by this delta. As in case-19, 13.B exempts the current state from 13.C's grammar check, but this heading carries through unchanged into the candidate state — verified directly in the generated candidate file — where 13.C DOES apply in full: the requirement heading has no ID (VIOLATION, "a requirement heading that does not match the grammar — no ID") and its scenario heading likewise has no ID and cannot be said to match its parent's ID (a second VIOLATION, same rule family for scenario headings). Count-based 13.E comparisons agree (candidate requirementCount 5 vs CLI 5, since a heading lacking an ID is still counted as a requirement heading for raw counting purposes).

FINAL: BLOCK | categories=VIOLATION

## case-22

PRECHECK: NOT_APPLICABLE — git-dependent commit-evidence step.
1: PASS — all items valid (note: this is the pre-archive state; openspec validate does not attempt the merge that trips check 13 below).
2: PASS — task 1.1 `- [x]`.
3: PASS — delta (MODIFIED REQ-7) not yet in main spec → "Needs sync".
4: PASS — design.md's intent (tightening scope enforcement) is stated for an existing "REQ-7 Token scope" that in fact does not exist in the current main spec; non-blocking either way.
5: NOT_APPLICABLE — working-tree dependent.
6: PASS — no leak directory.
7: PASS — no deferred tasks.
8: PASS — well-formed annotation.
9: PASS — n/a, no records.
10: PASS — vacuous.
11: PASS — vacuous.
12: PASS — 1:1 correspondence.
13: BLOCK — the archive-preview ITSELF FAILED: `openspec archive update-token-auth -y` printed `token-auth MODIFIED failed for header "### Requirement: REQ-7 Token scope" - not found` followed by `Aborted. No files were changed.`, the change directory still exists under openspec/changes/update-token-auth/, and no openspec/changes/archive/<date>-update-token-auth/ directory was created. Per 13.B's three-condition success test this is a FAILED preview even though the process exited 0 (exactly the fail-open trap the schema itself warns about — "openspec 1.3.1 exits 0 when it aborts the archive"). Per 13.B, I record an UNDETERMINABLE finding quoting that output; 13.C and the candidate-state half of 13.E are not evaluated (covered by this undeterminable finding, never passed). I still evaluated 13.D and the change-level half of 13.E on the current state: the delta's single MODIFIED entry is headed REQ-7 Token scope, which does not match any existing main-spec requirement ID (current max is REQ-5), is not the TO heading of any RENAMED pair in this delta, and its heading text doesn't match any main-spec heading — so under 13.D.1(d) it simply "does not resolve," which the schema explicitly says is "not a finding of this rule" but rather the archive preview's own failure (consistent with what was observed). The change-level 13.E comparisons (1 MODIFIED entry text vs 1 CLI entry; 1 scenario text vs 1 CLI scenario) agree with each other, so no additional violation arises there. No VIOLATION is recorded for check 13 — only the one UNDETERMINABLE finding from the failed preview.

FINAL: BLOCK | categories=UNDETERMINABLE
