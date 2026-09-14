# Review — task 2.2 (checks 9–11 decide evidence per subject)

Scope reviewed: `superpowers-bridge/schema.yaml` checks 9, 10, 11 and their titles
(new lines 490–623; old lines 483–525), plus the task-2.2 RED/GREEN records in
`openspec/changes/fix-v2-blocking-defects/tasks.md` (lines 74–102).
Hunks at old lines 285, 548, 554 (plan instruction + check 12) are task 2.1's and were
not reviewed. Base `22c15cf`; nothing committed.

Every verdict below was reached by walking the fixture text against the schema text
myself, not by reading the report's walk.

## Spec Compliance

✅ **Spec compliant.** Verified point by point:

| Requirement | Where satisfied | Verified how |
|---|---|---|
| Pair by `subject:`, not ordinally | `schema.yaml:559-563` states the rule and the reason verbatim in substance | read |
| Exactly one RED + one GREEN per subject | stage one (`:576-587`) gives ≤1 per side, stage two (`:589-596`) gives set equality; together exactly one each — the title's claim is the conjunction of the two stages, no more | derived both stages by hand |
| Uniqueness per task **per side** | `:577-582` "more than once in the RED list, or more than once in the GREEN list" | read |
| Grammar: exactly one `::`, non-empty trimmed sides, nothing else | `:516-531`, closing with "NOTHING FURTHER is constrained — not path syntax, not file extension, not the characters of the test name" | read |
| Boundary sentence (structure/format/cardinality only, never evidence truth) | `:613-623`, and it splits the four never-decided things correctly between R1/R2 and the ENFORCEMENT BOUNDARY paragraph rather than attributing all four to R1/R2 | cross-checked against `:703-742` — R1, R2 and R4 all exist and say what they are cited as saying |
| No sentence in 9–11 presumes a single RED or GREEN | check 9 "AT LEAST ONE" + "EVERY record belonging to the task is examined" (`:494-495`, `:513-515`); check 10 "applied to EVERY record … Each GREEN record's … Each RED record's" (`:544-552`); check 11 works on lists and sets throughout | independent grep of lines 490–623 for `the RED record`, `the GREEN record`, `a RED record and a GREEN record`, `identical to RED`, "one `- RED:` line and one" — **zero hits** |
| `tests/api_test.go::TestRejectsEmptyEmail/subcase-2` accepted | walked: one `::` (after `.go`), left `tests/api_test.go`, right `TestRejectsEmptyEmail/subcase-2`, both non-empty ⇒ conforms; and the text cites this exact identifier as a worked example, so no later reader can re-derive a path rule from silence | walked |
| Non-goals | only 2 files changed (`git status`); `version: 2` and `VERSION` = `2.0.0` unchanged; no archived loosen-plan artifact touched; the `tasks` artifact instruction (old 190–245) is **byte-identical** to `22c15cf` | `diff` against `22c15cf` |

**Fixture walk — I applied the new text myself to all six named fixtures:**

| Fixture | My verdict from the new text | Claimed | Match |
|---|---|---|---|
| f10 | check 9 BLOCK: trimmed `rejects empty email` holds zero `::` where exactly one is required ⇒ `subject:` is not a satisfied field, reported for both records. Check 11 silent (one value each side, sets equal) | check 9 BLOCK | ✅ |
| f11 | check 9 silent (both values conform); check 10 silent; check 11 stage one finds `test/auth.test.js::rejects empty email` twice in the RED list ⇒ BLOCK naming value and side; stage two still runs and adds nothing | check 11 stage one BLOCK | ✅ |
| **f12 (positive control)** | check 9: two `- RED:` and two `- GREEN:` lines satisfy AT LEAST ONE of each; all fields present; both values hold exactly one `::` with non-empty sides. check 10: `FAIL`, `FAIL`, `PASS`, `PASS` all conform. check 11: RED list `[…empty email, …empty password]` no repeat, GREEN list identical, sets equal both directions. **No finding from any of 9–11.** | no finding | ✅ — the control survives, and it survives *because* the presence/cardinality split was chosen; under an "exactly one record" reading of check 9 it would have been falsely rejected |
| f2 | check 9 BLOCK (zero `- GREEN:` lines). Task 2 is `TDD: n/a` with no records, correctly out of 9–11 | check 9 BLOCK, unchanged | ✅ (check 11 stage two now additionally reports the RED subject with no GREEN — a second finding on the same defect, verdict unchanged) |
| f3 | check 9 silent, check 10 BLOCK (RED `outcome: PASS`), check 11 silent | check 10 BLOCK, unchanged | ✅ |
| f4 | check 11 stage one clean, stage two `{auth…}` vs `{signup…}` non-empty both directions ⇒ BLOCK naming both | check 11 BLOCK, unchanged | ✅ |

**Records (tasks.md 2.2):** ticked `[x]`; three RED/GREEN pairs for f10, f11, f12. I extracted the
`subject:` values programmatically: all six carry **exactly one** `::`, RED and GREEN are
byte-identical within each pair, the three values are distinct, and each appears once per side —
so this change's own tasks.md passes the checks it is writing (dogfooding holds). Outcomes
`FAIL`, `FAIL`, `INDETERMINATE` / three × `PASS`: `INDETERMINATE` is 13 uppercase letters, no
whitespace, ≠ `PASS`, so **check 10 accepts it** — the deliberate non-`FAIL` token is legal, not a
loophole. Record shape matches the normative SHAPE block at `schema.yaml:226-237` (records at the
`TDD:` indent, fields one level deeper, literal keys). Convention `<fixture dir>::<expected verdict>`
followed in all three.

**RED authenticity.** The pre-edit text I recovered myself (`git show 22c15cf:…` lines 483–521)
contains no mention of `::`, no value-format rule, and no uniqueness or cardinality sentence at
all — so f10's and f11's REDs are real pre-edit failures, not retrospective assertions. f12's
`INDETERMINATE` is honest: pre-edit check 11's whole body is one sentence using the definite
singular "**the** RED record" / "**the** GREEN record" over a task holding two of each, which
designates nothing; pairing 1↔1 / 2↔2 gives no difference and 1↔2 gives BLOCK, and no rule
chooses. Recording that as neither PASS nor BLOCK is the accurate call, and calling it FAIL would
have been the overclaim. `.superpowers/sdd/plan/task-2.2-red-walk.md` has mtime 17:04:42,
`schema.yaml` 17:07:47 — consistent with the walk preceding the edit.

⚠️ **Cannot verify from the diff alone:** that the RED walk was performed rather than
reconstructed. The mtime ordering and the fact that the pre-edit text independently yields the
recorded verdicts are corroboration, not proof.

## Strengths

- **The positive control was actually protected, and the reasoning is visible.** The
  presence-vs-exactly-one ambiguity was settled the only way that keeps f11 and f12 isolable:
  check 9 decides presence, check 11 decides cardinality per subject. Under "exactly one" f11
  would have blocked on record count without ever naming the duplicate, and f12 would have
  blocked outright. The chosen reading is stated in the text (`:495-498`) rather than left to be
  inferred.
- **Decidability was added where the spec was silent, without adding a constraint.** "Exactly one
  `::`" is undecidable for `a:::b` under overlapping matches; the non-overlapping-scan clause
  (`:521-525`) settles it and says so with a worked example. That is the right shape: make it
  decidable, do not tighten it.
- **Every check now states its own multiplicity of reporting** — "Every such finding is reported,
  not just the first" (9), "every offending record is reported" (10), "every one that holds is
  reported" (11). This is the question the brief asked and all three answer it explicitly.
- **The boundary paragraph splits attribution correctly.** R1/R2 carry two of the four
  never-decided things; the ENFORCEMENT BOUNDARY carries the other two. Attributing all four to
  R1/R2 would have been this change's own defect class committed inside its own fix.
- **Register matches check 12.** Same two-stage shape, same explicit no-short-circuit paragraph,
  same distinct-messages / distinct-repairs rationale, same "a set comparison cannot see a
  duplicate — the set absorbs it" justification for the ordering. A reader moving between 11 and
  12 meets one voice.
- **Isolation is clean.** Check 7, check 12 and the `tasks` artifact instruction are untouched
  (the last verified byte-for-byte against `22c15cf`), and no file outside the two in scope moved.

## Issues

### Critical (Must Fix)

None.

### Important (Should Fix)

**1. The fixtures README now states the wrong check for f10, and this task is what made it wrong.**
`docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md:45` reads
`f10-subject-without-separator | … | check 11（subject: 語法）BLOCK`. Under the new text the
grammar lives in check 9, so f10 BLOCKs at **check 9**. That README is the answer key for the
blind re-run protocol (its line 93 instructs a re-runner to compare against that very table), so a
re-runner who gets the *correct* answer is graded wrong. The f11 and f12 rows are still accurate.
*Fix:* change the f10 row to check 9. An owner exists — task **1.4** ("Extend the fixtures README")
is still `[ ]` unticked in tasks.md, so this belongs there rather than inside 2.2's fence, but it
must not be allowed to close silently. Worth adding to that row that f2 now additionally trips
check 11 stage two alongside its check 9 BLOCK (verdict unchanged, but a re-runner reporting both
is not wrong). The implementer flagged this in report §9.1; recorded here so it has a
reviewer-side owner.

**2. `schema.yaml:714-716` (review judgement R2) now says something false about check 9, and no
task owns fixing it.** R2 reads "Checks 9-11 read the subject as an opaque string and compare it
to itself." Check 9 now validates the subject's *format*, so it does not read it as opaque; and no
subject is compared "to itself" any more — check 11 compares values across records. R2's actual
point (no check judges whether the subject tests the right behaviour) survives, so this
under-claims rather than over-claims — but it is a bridge-owned sentence that this task falsified.
Task 2.4's grep list is "a RED record and a GREEN record", "identical to RED's", "the RED record's
`subject:`" — none of which matches R2's wording, so 2.4 as written will not catch it. *Fix:*
either amend R2 to "Checks 9-11 decide the subject's form and its pairing, never whether the named
test exercises the behaviour the task claims", or add the phrase `compare it to itself` to 2.4's
grep list. One sentence either way.

**3. `tasks.md:89` — f11's RED `failure:` states "actual PASS" on a pre-edit sentence the same
work elsewhere documents as ambiguous.** The field asserts "Pre-edit check 9 is satisfied (a RED
line and a GREEN line are present…)", which picks the "at least one" reading of the pre-edit
"must include one `- RED:` line and one `- GREEN:` line" and records it as the fact of what
happened. The implementer's own report §3 and red-walk both note the other reading exists — and
for f12 an equally undecidable pre-edit sentence was correctly recorded as `INDETERMINATE`. The
same treatment was not applied here. The RED's *conclusion* survives either reading (under
"exactly one" the pre-edit text blocks at check 9 on record count without ever naming the
duplicated subject — the wrong verdict for a different reason), so this is a precision defect in
the durable record, not a false RED. It matters because the record is what survives the change and
the report is not, and because "stating one reading of an ambiguous sentence as the verdict" is
the exact class this change exists to close. *Fix:* one clause appended to the `failure:` field —
"…so no difference is found. Under a strict 'exactly one record' reading of the pre-edit check 9
the verdict is instead a BLOCK on record count that never names the duplicated subject — wrong for
a different reason, so the RED holds either way."

### Minor (Nice to Have)

**4. `schema.yaml:490` — the retitle lost a branch the check still decides.** The new title is
"RED and GREEN records present, required fields **non-empty**, and every `subject:` value
well-formed", but the check also BLOCKs on a *missing* required field (`:534-536`), which
"non-empty" does not name. The old title's "with required fields" covered it. Underclaim, not
overclaim. *Fix:* "required fields present and non-empty".

**5. `schema.yaml:516` — "a required field is satisfied when it is present AND its value conforms"
is stated generally, but only `subject:` has a grammar here.** A literal reader can ask whether
`outcome:` "conforms" and try to answer it inside check 9, which is check 10's question (check 10
opens "this check reads the MARKER ONLY"). No grammar for `outcome:` exists in check 9, so nothing
can actually be decided wrongly — but on f3 a strict reader might attach a spurious second finding
to check 9. *Fix:* scope the clause — "a `subject:` field is satisfied when it is present AND its
value conforms to the grammar below".

**6. `schema.yaml:564-570` — check 11's collection step does not say what to collect from a record
that has no `subject:` field at all.** "collect the trimmed `subject:` value of every `- RED:`
record" has no value to collect there; the text says neither "skip it" nor "treat it as empty",
and the two choices produce different stage-one findings (two subject-less REDs collide as empty
strings under one reading, vanish under the other). The task's *verdict* is unaffected — check 9
already BLOCKs on the missing field — so only the finding list diverges. The pre-edit text had the
same silence, so this is inherited rather than introduced, but the new text enumerates the
collection explicitly and is the natural place to close it. *Fix:* one clause — "a record carrying
no `subject:` field contributes nothing to either list; its missing field is check 9's finding."
This mirrors the malformed-value clause at `:569-573`, which handles the analogous case well.

**7. `schema.yaml:537` — "naming the offending value and the record it belongs to" has no way to
name a record.** When a task carries two `- RED:` records the phrase does not resolve to an
identifier. Reporting precision only. *Fix:* "…and which record (by side and order of appearance)
it belongs to", matching stage one's "by name and by the side it repeats on".

### Not findings — branches I walked and found decided

| Branch | Decided by |
|---|---|
| A subject appearing three times | `:577-579` "more than once", which covers 3 as well as 2 |
| Two REDs and no GREEN for one subject | stage one (`:577`) **and** stage two (`:591-593`), both reported — `:598-600` says stage one does not short-circuit |
| `TDD: n/a` task carrying records | `:532-535` routes it to review judgement R4, and R4 (`:718-724`) exists and says exactly that |
| A `subject:` that trims to empty | `:534-537` on two independent grounds (empty after trimming; zero `::` fails the grammar) — the grounds agree rather than conflict |
| A value containing `::` twice | `:527-531` "EXACTLY ONE such sequence", with `a::b::c` as the worked counter-example |
| `a:::b` | `:521-525`, the non-overlapping scan clause — undecidable without it |
| A GREEN whose subject matches no RED | stage two, `:592-593`, explicitly the second direction |
| Malformed subject that also duplicates | `:569-573` — both checks report, neither suppresses the other |
| Multiple failures in one task | stated explicitly in all three checks |

**File growth:** checks 9–11 went from ~43 to ~134 lines (+91). Proportionate: check 12 under task
2.1 grew to a comparable ~78 lines for the same two-stage shape, and `schema.yaml` is an
instruction surface executed by hand, exempt from the prose line budget. The one duplication worth
naming is check 11's no-short-circuit paragraph, which restates check 12's near-verbatim — in a
document read check-by-check that repetition is load-bearing, not bloat.

## Assessment

**Task quality:** Approved with fixes

**Reasoning:** The delivered text does what its titles claim — I walked all six fixtures and the
spec's conforming identifier against it myself and every verdict came out as claimed, including
the positive control, which survives precisely because presence and cardinality were separated
rather than collapsed. The three Important items are each a one-sentence repair and none of them
changes a verdict: one stale README row (owner: open task 1.4), one falsified review-judgement
sentence with no current owner, and one RED `failure:` field that states an ambiguous pre-edit
reading as settled.
