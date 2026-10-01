## case-01

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's Context/Decisions ("boundary instant counts as expired") align with the proposal/delta topic, no drift to warn about
5: NOT_APPLICABLE — depends on working-tree/commit state ("no unstaged files"), no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks, so no gap-analysis is owed
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; it carries no RED/GREEN records, none owed
10: PASS — no records present, nothing to violate the outcome-marker rule
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md task number `1.1` and plan.md entry key `## 1.1 —` correspond 1:1, each unique
13: BLOCK — the delta's MODIFIED REQ-2 entry adds a new scenario heading "#### Scenario: token at the expiry instant" with no `<REQ-ID>-S<m>` form at all; a new scenario heading carrying no legal ID is a violation under 13.C (grammar) and 13.D.3 (new-ID allocation), reported once citing both. The archive preview succeeded and the CLI's requirement/scenario counts agreed with the text-based counts, so this is a completed, reliable VIOLATION.

FINAL: BLOCK | categories=VIOLATION

## case-02

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's Context ("fixed lifetime of fifteen minutes") aligns with the delta topic, no drift
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the delta ADDs a requirement titled "REQ-2 Token lifetime", reusing the ID REQ-2 that the main spec's existing "Token expiry" requirement already holds — a 13.D.1 violation ("an ADDED entry carrying an ID that the main spec already holds"). The archive preview succeeded and the resulting candidate spec literally contains two requirement blocks both carrying local ID "REQ-2", a second, independent 13.C duplicate-ID violation. Counts (requirementCount 4=4, per-position scenario counts) all agreed with the CLI, so both findings are completed, reliable VIOLATIONs.

FINAL: BLOCK | categories=VIOLATION

## case-03

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's Context ("Refresh tokens are exchanged for new access tokens") aligns with the delta topic
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the delta ADDs a new requirement "REQ-FOO Token refresh". "REQ-FOO" matches the heading grammar (`REQ-` + `[A-Z0-9]+`) but is non-numeric; 13.D.3 requires a newly-allocated requirement ID to be numeric ("REQ-FOO under ADDED is a violation although it matches the heading grammar"). Archive preview succeeded; counts (requirementCount 4=4, scenario counts per position) all agreed, so this is a completed, reliable VIOLATION.

FINAL: BLOCK | categories=VIOLATION

## case-04

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's Context (refresh-token topic) aligns with the delta's ADDED requirement, no drift
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the CURRENT main spec's last scenario (REQ-5-S4) is followed by prose containing a fenced code block whose single line is "### Requirement: REQ-9 Example quoted heading". Per 13.A this is a line-by-line, fence-blind rule: that line still counts as a literal requirement heading in the text-based scan, even though the OpenSpec CLI's real markdown parser ignores it. The delta cleanly ADDs REQ-10 (numeric, above the current max of 5 — no violation there). But in the candidate (post-archive) file this pre-existing quoted line survives unchanged, so the text-based requirement-heading count is 5 (REQ-1, 2, 5, the quoted REQ-9, and REQ-10) while the CLI's `requirementCount` is 4 — a 13.E top-level count disagreement, itself a VIOLATION. Because that count disagrees, every dependent scenario-count comparison for this file can no longer be paired reliably by position and is recorded as UNDETERMINABLE (not a pass) rather than guessed.

FINAL: BLOCK | categories=VIOLATION,UNDETERMINABLE

## case-05

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec (session-policy) correctly not yet synced into the main spec; non-blocking record
4: PASS — design.md's Context ("Absolute timeout complements the idle timeout") aligns with the delta topic
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: PASS — the delta ADDs "REQ-4 Session absolute timeout" to session-policy. The capability's only current numeric requirement set is empty (its one existing requirement, REQ-PB, is non-numeric), so under 13.D.3 "any positive integer satisfies the rule" — REQ-4 passes even though `openspec/changes/archive/` shows a REQ-3 was once added and later removed from this same capability (that historical maximum is explicitly out of this check's scope; it reads only the current main spec). Archive preview against a fresh temp copy succeeded (exit 0, change dir removed, dated archive dir created), and the CLI's `requirementCount`/scenario counts agreed exactly with the text-based counts in both halves of 13.E. No 13.C or 13.D finding.

FINAL: PASS

## case-06

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's refresh-token Context aligns with the delta topic (both ADDED requirements concern token refresh/introspection)
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the delta's ADDED section contains two separate requirement headings both titled "REQ-6" ("Token refresh" and "Token introspection"). Two ADDED entries in one delta file sharing an ID is a direct 13.D.1 violation. Archive preview succeeded, and the resulting candidate spec literally carries two requirement blocks both with local ID "REQ-6" — a second, independent 13.C duplicate-ID violation. Counts (requirementCount 5=5, per-position scenario counts) all agreed with the CLI.

FINAL: BLOCK | categories=VIOLATION

## case-07

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's Context ("Title-only change; the requirement body is unchanged") matches a pure RENAMED delta
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the delta RENAMEs "REQ-2 Token expiry" to "REQ-7 Token expiry". The FROM heading already carries an ID (REQ-2), so under 13.D.2 the TO ID must equal it; REQ-7 ≠ REQ-2 is exactly the schema's own counter-example ("giving a contract a different ID is never a rename — the old ID is retired and a new one is born") — a direct VIOLATION. Archive preview succeeded (the CLI performed the textual rename as requested) and the change-level ID-pair comparison in 13.E agreed with the text (both read REQ-2→REQ-7), so this is a completed, reliable finding, not an UNDETERMINABLE one.

FINAL: BLOCK | categories=VIOLATION

## case-08

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's refresh-token Context aligns with the delta's ADDED requirement
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the delta ADDs requirement "REQ-6 Token refresh" (numeric, legal, no collision — fine on its own), but its second scenario is written "#### Scenario: REQ-5-S5 expired refresh token" — its `<REQ-ID>` (REQ-5) does not equal the ID of the requirement block it sits under (REQ-6). This is a 13.C violation ("a violation even when a requirement carrying that other ID exists elsewhere in the capability" — REQ-5 Token revocation does exist, but that doesn't excuse the mismatch). Archive preview succeeded and counts (requirementCount 4=4, 2=2 scenarios under REQ-6) agreed with the CLI, so this is a completed, reliable VIOLATION.

FINAL: BLOCK | categories=VIOLATION

## case-09

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's refresh-token Context aligns with the delta topic
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — identical defect to case-03: the delta ADDs a new requirement "REQ-FOO Token refresh" whose ID matches the heading grammar but is non-numeric, violating 13.D.3's numeric-allocation rule for newly-allocated requirement IDs. Counts agreed throughout, so this is a completed, reliable VIOLATION.

FINAL: BLOCK | categories=VIOLATION

## case-10

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's refresh-token Context aligns with the delta's ADDED requirement
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the delta ADDs "REQ-6 Token refresh" with two scenarios, but both scenario headings carry the same local ID "REQ-6-S1" ("valid refresh token" and, mistakenly, "expired refresh token" too). Two scenario headings in one requirement block sharing a local ID is a direct 13.C violation. Archive preview succeeded; requirementCount (4=4) and the per-position scenario count under REQ-6 (2=2) agreed with the CLI — the duplicate is a content/identity defect, not a count defect, so this is a completed, reliable VIOLATION.

FINAL: BLOCK | categories=VIOLATION

## case-11

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's Context matches a pure RENAMED delta
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: PASS — the delta RENAMEs "REQ-2 Token expiry" to "REQ-2 Access token expiry": the FROM heading's ID (REQ-2) equals the TO heading's ID (REQ-2), only the description text changes, which conforms exactly to 13.D.2 ("`REQ-3 Token expiry` → `REQ-3 Access token expiry` passes"). Archive preview against a fresh temp copy succeeded, and all 13.E comparisons (entry count, FROM/TO ID pair) agreed between the text and the CLI's `rename.from`/`rename.to`. No 13.C or 13.D finding.

FINAL: PASS

## case-12

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's expiry-instant Context aligns with the MODIFIED REQ-2 delta
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the delta's MODIFIED REQ-2 body contains, before its real scenarios, a fenced example block whose single line is "#### Scenario: REQ-2-S9 example quoted heading". Per 13.A this literal line still counts as a scenario heading in the text-based scan even though it sits inside a code fence. Verified directly: the OpenSpec CLI's `show --deltas-only` JSON lists only 3 scenarios for this entry (the real S1/S2/S3) while the delta text contains 4 scenario headings (S9 quoted + S1/S2/S3) — a 13.E change-level VIOLATION (entry count agreed at 1=1, so this is a direct, reliably-paired mismatch, not dependent-UNDETERMINABLE). The same fenced line survives into the archived candidate spec unchanged, so the candidate-state half of 13.E independently disagrees too (text 4 vs CLI `requirements[1].scenarios.length` 3) — a second VIOLATION (requirementCount agreed at 3=3 first).

FINAL: BLOCK | categories=VIOLATION

## case-13

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's refresh-token Context aligns with the delta's ADDED requirement
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: PASS — the delta ADDs "REQ-6 Token refresh". This repository's `openspec/changes/archive/` shows a *different* requirement, "REQ-6 Token introspection", was previously added and later removed from this same capability — so the ID REQ-6 is being reused. Per 13.D.3 and 13.G, this check reads only the CURRENT main spec's numeric maximum (5, from REQ-1/2/5) and explicitly does NOT read `openspec/changes/archive/` or git history; since 6 > 5, the structural allocation rule is satisfied. The reused-retired-ID risk is the `specs` artifact author's unverified obligation, stated by the schema to be out of this check's scope. Archive preview succeeded and all counts agreed (no duplicate exists in the candidate state, since the historical REQ-6 was already removed before this change). No 13.C or 13.D finding.

FINAL: PASS

## case-14

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's refresh-token Context aligns with the delta's ADDED requirement
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the CURRENT main spec's REQ-2 body already contains a fenced example block whose single line is "#### Scenario: REQ-2-S9 example quoted heading" (untouched by this ADDED-only delta). Per 13.A this literal line is counted as a real scenario heading. In the candidate (post-archive) spec this quoted line survives unchanged, so the text-based scan counts 3 scenario headings under REQ-2 (S1, S2, and the quoted S9) while the CLI's `requirements[1].scenarios.length` is 2 (only the real S1/S2 — the fence is invisible to its markdown parser). requirementCount agreed first (4=4), so this is a direct, reliably-paired 13.E position-level VIOLATION, not a dependent UNDETERMINABLE one.

FINAL: BLOCK | categories=VIOLATION

## case-15

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's Context aligns with the delta's ADDED+MODIFIED pair
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: PASS — the delta ADDs "REQ-6 Token refresh" (numeric, above current max 5, scenarios S1/S2 numbered from an empty set — all legal) and MODIFIEs REQ-2 to add a correctly-formed new scenario "REQ-2-S3 token at the expiry instant" (numeric, above REQ-2's current max of 2 — legal, no fenced-code trap this time). Archive preview against a fresh temp copy succeeded, and every 13.E comparison (requirementCount 4=4, every per-position scenario count) agreed between text and CLI. No 13.C or 13.D finding.

FINAL: PASS

## case-16

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's refresh-token Context aligns with the delta's ADDED requirement
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the delta ADDs requirement "REQ-3 Token refresh". REQ-3 does not collide with any existing requirement ID (no current REQ-3 exists, so no 13.C duplicate and no 13.D.1 collision), but the capability's current largest numeric requirement ID is REQ-5 (from REQ-1/2/5), and 3 is not greater than 5. This is exactly the schema's own counter-example ("with REQ-9 the largest current numeric ID, ADDED REQ-4 is a violation even though no current requirement holds REQ-4") — a 13.D.3 allocation-rule VIOLATION. Archive preview succeeded and all counts agreed, so this is a completed, reliable finding.

FINAL: BLOCK | categories=VIOLATION

## case-17

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — both delta specs (token-auth, session-policy) correctly not yet synced into their main specs; non-blocking record
4: PASS — design.md's Context ("Each requirement is renamed to carry an identifier...the text is unchanged") matches the migration delta exactly
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: PASS — the token-auth main spec currently has fully unnumbered requirements and scenarios. The delta RENAMEs each ("Token issuance"→"REQ-1 Token issuance", "Token expiry"→"REQ-2 Token expiry") with FROM headings carrying no ID — exactly 13.D.2's sanctioned migration exception, so the new numeric TO IDs are judged under 13.D.3: the current numeric-ID set is empty, so any positive integer is legal, and REQ-1/REQ-2 are both legal and distinct. The paired MODIFIED entries resolve through those RENAMED pairs to the (ID-less) FROM requirements, whose unnumbered scenarios leave the current scenario set empty, so the newly-numbered scenarios (REQ-1-S1/S2, REQ-2-S1/S2) are likewise all legal new allocations. The session-policy delta similarly assigns scenario IDs (REQ-PB-S1/S2) under the already-numbered REQ-PB, also from an empty current scenario set — legal. Archive preview against a fresh temp copy succeeded for both specs, and every 13.E comparison agreed. No 13.C or 13.D finding.

FINAL: PASS

## case-18

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's refresh-token Context aligns with the delta's ADDED requirement
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the delta's ADDED requirement heading is literally "### Requirement: REQ-6" with nothing after the ID (confirmed in the archived candidate text). This is the schema's own illegal example ("an ID with nothing after it (`### Requirement: REQ-6`)") — it carries no legal ID at all, a 13.C/13.D.3 violation (reported once, citing both). Its two scenario headings ("REQ-6-S1"/"REQ-6-S2") each claim parent ID "REQ-6", but since the parent block itself carries no local ID under the grammar, their `<REQ-ID>` cannot equal "the ID of the requirement block it belongs to" — two further 13.C violations. requirementCount and per-position scenario counts otherwise agreed with the CLI (4=4, 2=2), so these are completed, reliable findings.

FINAL: BLOCK | categories=VIOLATION

## case-19

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's refresh-token Context aligns with the delta's ADDED requirement
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the CURRENT main spec already has two separate requirement blocks both carrying local ID "REQ-2" ("Token expiry" and "Token lifetime"), untouched by this ADDED-only delta (which cleanly adds REQ-6). 13.C is a pure scan of the candidate (post-archive) file regardless of origin, so this pre-existing duplicate carries straight into the candidate state and is flagged directly ("two requirement blocks in one file carrying the same local ID"). Archive preview succeeded and requirementCount (5=5) plus every per-position scenario count agreed with the CLI, so this is a completed, reliable VIOLATION.

FINAL: BLOCK | categories=VIOLATION

## case-20

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — both delta specs (token-auth, session-policy) correctly not yet synced into their main specs; non-blocking record
4: PASS — design.md's migration Context aligns with the delta (rename + modify pairs)
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — like case-17, this delta migrates two unnumbered token-auth requirements via RENAMED pairs with ID-less FROM headings (the sanctioned 13.D.2 exception), so each TO ID is judged as a new ID under 13.D.3. "Token issuance"→"REQ-1 Token issuance" is fine (numeric), but "Token expiry"→"REQ-FOO Token expiry" assigns a non-numeric new ID, which 13.D.3 requires to be numeric regardless of grammar conformance ("REQ-FOO under ADDED is a violation although it matches the heading grammar" — the same rule applies to a migration TO ID). The session-policy delta (REQ-PB scenario numbering) is clean, same as case-17. Archive preview succeeded and all 13.E comparisons agreed, so this is a completed, reliable VIOLATION isolated to the REQ-FOO rename.

FINAL: BLOCK | categories=VIOLATION

## case-21

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's refresh-token Context aligns with the delta's ADDED requirement
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the CURRENT main spec already has an unnumbered requirement ("### Requirement: Token audience", no ID) with an unnumbered scenario ("#### Scenario: wrong audience", no ID), untouched by this ADDED-only delta (which cleanly adds REQ-6). Both carry unchanged into the candidate state, where 13.C flags each independently as a requirement/scenario heading that does not match the grammar (no legal ID). Archive preview succeeded and requirementCount (5=5) plus every per-position scenario count agreed with the CLI, so these are completed, reliable VIOLATIONs.

FINAL: BLOCK | categories=VIOLATION

## case-22

PRECHECK: NOT_APPLICABLE — depends on commit history (`git log`), which has no meaningful state in this fixture
1: PASS — `openspec validate --all --json` reports valid:true for all 3 items (0 failed)
2: PASS — the single task 1.1 is checked `- [x]`
3: PASS — delta spec correctly not yet synced into the main spec (pre-archive state); non-blocking record
4: PASS — design.md's Context ("Missing scope answers 403") aligns with the MODIFIED REQ-7 delta
5: NOT_APPLICABLE — depends on working-tree/commit state, no meaningful git state in this fixture
6: PASS — no `docs/superpowers/specs/*.md` present
7: PASS — tasks.md has no `[~]` deferred tasks
8: PASS — the task carries exactly one well-formed `- TDD: n/a — prose/doc-only` annotation
9: PASS — task is `TDD: n/a`; no RED/GREEN records, none owed
10: PASS — no records present
11: PASS — no records present, pairing vacuously satisfied
12: PASS — tasks.md `1.1` and plan.md `## 1.1 —` correspond 1:1
13: BLOCK — the delta's MODIFIED entry targets "### Requirement: REQ-7 Token scope", but no such requirement exists in the current main spec (which only has REQ-1/2/5) and no RENAMED pair in this delta supplies a TO heading matching it — none of 13.D.1's three resolution rules apply, so the entry does not resolve. Verified directly: the archive preview against a fresh temp copy exited 0 but printed `token-auth MODIFIED failed for header "### Requirement: REQ-7 Token scope" - not found` / `Aborted. No files were changed.`, and the change directory was NOT removed and no dated archive directory was created — a FAILED preview under 13.B's three-part test (exit code alone is not sufficient; openspec 1.3.1 exits 0 even when it aborts). Per 13.B, this records an UNDETERMINABLE finding quoting the archive output; 13.C and the candidate-state half of 13.E are not evaluated (covered by the undeterminable finding, never passed). The current-state-only parts still ran: 13.D records no rule-violation for an entry that fails to resolve ("not a finding of this rule"), and the change-level half of 13.E (entry count 1=1, scenario count 1=1 for the one MODIFIED entry) agreed with the CLI's `--deltas-only` JSON, so it contributes no VIOLATION.

FINAL: BLOCK | categories=UNDETERMINABLE
