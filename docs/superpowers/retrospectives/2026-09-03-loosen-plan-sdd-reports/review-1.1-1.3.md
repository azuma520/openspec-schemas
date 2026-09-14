# Review — tasks 1.1, 1.2, 1.3 (six new mutation fixtures)

## Spec Compliance

✅ Spec compliant, with one isolation defect (see Important #1).

All six directories exist with both files; nothing outside them was created:

- `fixtures/f8-duplicate-task-number/{tasks.md,plan.md}`
- `fixtures/f9-duplicate-plan-key/{tasks.md,plan.md}`
- `fixtures/f10-subject-without-separator/{tasks.md,plan.md}`
- `fixtures/f11-duplicate-subject-one-side/{tasks.md,plan.md}`
- `fixtures/f12-two-subjects-paired/{tasks.md,plan.md}`
- `fixtures/f13-deferred-task-in-tasks/{tasks.md,plan.md}`

Per-brief walk against `superpowers-bridge/schema.yaml` (checks 7–12 at lines 419–556), done independently of the report:

| Fixture | Brief demands | Verified |
|---|---|---|
| f8 | one task number twice, sets otherwise equal, PASS under pre-edit 12 | ✅ `f8/tasks.md:3,12` both `1.1`; `f8/plan.md:3` single `## 1.1`. Check 12 (`schema.yaml:548` "Compare the two **sets** in BOTH directions") collapses `{1.1,1.1}`→`{1.1}`, equal → PASS. Claim correct. |
| f9 | one plan key twice, sets otherwise equal, PASS under pre-edit 12 | ✅ `f9/plan.md:3,5` both `## 2.3`; `f9/tasks.md:3` single `2.3`. Same set collapse → PASS. Claim correct. |
| f10 | only defect is missing `::`; GREEN carries the same malformed value | ✅ `f10/tasks.md:6,10` both `subject: rejects empty email`, identical, so check 11 (`schema.yaml:517-521`, RED subject ≡ GREEN subject) has nothing to say; check 9 (`schema.yaml:498-504`) constrains presence/non-emptiness only, no format. Claim correct. |
| f11 | only defect is two REDs with identical subjects + one GREEN | ⚠️ structurally correct (`f11/tasks.md:5-12` two REDs, same subject; `:13` one GREEN) but carries a second candidate finding — Important #1. |
| f12 | zero non-conformances under the corrected contract; two paired subjects | ✅ `f12/tasks.md:6/10` and `:13/17` — two distinct subjects, each exactly one RED + one GREEN, both grammar-valid, outcomes valid (`schema.yaml:506-515`), check 12 `{1}`={1}. Zero non-conformances. Does not block. |
| f13 | exactly one `[~]`; plan.md conforming v2 with no task rows | ✅ `f13/tasks.md:3` single `[~]`; `f13/plan.md` header + one `## 1` heading, zero checkbox lines. Check 7 (`schema.yaml:421,438` — "If **plan.md** has any tasks marked `[~]`… Blocks only if §7 is empty AND plan.md has `[~]` rows") finds nothing → cannot fire. Claim correct. |

All five of the report's verdict-walk claims cite sentences that do say what the report says they say; I re-derived each from the schema text rather than accepting the walk.

⚠️ Cannot verify from the package: check 9's phrase "must include **one** `- RED:` line and one `- GREEN:` line" (`schema.yaml:490-491`) is genuinely ambiguous between *at least one* and *exactly one*. Under the strict reading f11 trips check 9 for an unrelated reason and stops isolating, and f12 (the positive control) would trip it too. The pre-edit text does not settle it; 2.1/2.2 must. The implementer flagged this — correctly, though it mis-names which fixtures depend on it (Minor #2).

## Strengths

- Every fixture reuses f1–f7's exact shape: `## 1. Fixture group`, two-space nesting, `- RED:`/`- GREEN:` with four-space fields, `# Fixture plan` + bare `## N — <title>` entries, em-dash `n/a` separators. Byte-level check (`cat -A`) shows real em dashes and no CRLF, matching f1–f7.
- Domain content is realistic and continuous with the existing set (auth/email/password, README, checkout smoke) — no `foo`/`bar`/`123`.
- f8's plan entry title "email validation and README install section" (`f8/plan.md:3`) is a thoughtful touch: one entry honestly covering the two duplicate-numbered tasks, so the fixture isn't self-contradictory.
- f12 genuinely interleaves RED/GREEN/RED/GREEN rather than grouping — that is the arrangement that makes ordinal pairing visibly wrong, which is exactly what the positive control needs to exercise.
- The report does not overclaim: it reports f12's pre-edit verdict as *indeterminate* instead of forcing a PASS/BLOCK, and it names its own check-9 reading as a reading call rather than a fact.

## Issues

### Critical (Must Fix)

None.

### Important (Should Fix)

**1. `f11-duplicate-subject-one-side/tasks.md:11-12` — the second RED is a candidate R1 violation, giving the fixture a possible second finding.**

```
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: ERROR
    - failure: TypeError: cannot read property 'value' of undefined
```

Review judgement R1 (`schema.yaml:563-568`) asks whether each RED's `failure:` is a *behavioural* failure "rather than a SyntaxError, import error, missing dependency or other test-harness error", and says a violation is "a blocking finding of the review". An `ERROR` outcome whose excerpt is a bare `TypeError: cannot read property …` is precisely the shape `f6-syntaxerror-red` exists to represent. A reviewer running verify against f11 could therefore raise two blocking findings — the duplicate subject *and* R1 — at which point f11 no longer isolates which rule fired, which is the one property the brief pins on it ("f11's only non-conformance is the duplicated RED subject").

I cannot prove the R1 reading (a TypeError thrown by unimplemented code is arguably behavioural), so this is contingent — but the ambiguity is free to remove and expensive to leave, because 2.2's RED record for f11 has to name one expected verdict.

Fix — one line, matching the first RED's register:

```
    - outcome: FAIL
    - failure: expected 'Email required', got undefined (second run, after refactor)
```

Keeping `outcome: ERROR` is also fine if the excerpt is made behavioural; what should go is the harness-error *shape*.

### Minor (Nice to Have)

**2. `.superpowers/sdd/plan/task-1.1-1.3-report.md:228-241` — the Concerns section names the wrong fixture as depending on the check-9 cardinality reading.**

It says "f11 and f9's cardinality vs. check 9's wording". f9 (`f9/tasks.md:5,9`) has exactly one RED and exactly one GREEN — its duplicate is a *plan key*, which check 9 never reads, so f9 is unaffected under either reading. The fixtures that actually hinge on it are f11 and **f12** (two RED + two GREEN under one task). The report's own f12 walk gets this right; only the summary paragraph is wrong. Worth correcting before 2.1/2.2 read it as a scoping note, since it points them at the wrong pair.

**3. `f13-deferred-task-in-tasks/tasks.md` is 4 lines against f1–f7's 8–20 — sufficient, but one ordinary task would make it stronger.**

The brevity is *not* padding-worthy in itself: check 7's blindness is demonstrated by the presence of a `[~]` in tasks.md and its absence from plan.md, and one task shows that. But every other fixture in the set carries a second, conforming task, and a file containing nothing except the deferred task leaves open the reading "the check found nothing because there was nothing else to find". Adding a second, ordinary `- [x] 2 …` task with `TDD: n/a — prose/doc-only` plus a matching `## 2 — …` plan entry would keep the single defect, match the set's convention, and make check 12 non-trivial for this fixture too. Judgment call — currently exactly sufficient, not thin.

## Assessment

**Task quality:** Needs fixes

**Reasoning:** All six fixtures exist, follow the f1–f7 convention, and five of them provably isolate exactly the property their brief names — and every verdict walk the report claims holds up against the pre-edit schema text I re-read. The one blocker is f11's second RED, whose harness-error-shaped `failure:` excerpt puts a second, independent finding (R1) on a fixture the brief requires to carry exactly one; it is a one-line fix.
