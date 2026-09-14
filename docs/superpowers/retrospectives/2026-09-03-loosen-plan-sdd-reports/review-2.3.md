# Review — task 2.3 (check 7's carrier: plan.md → tasks.md, D4)

Scope reviewed: check 7 (`superpowers-bridge/schema.yaml:426-470`), the FRESHNESS
map (`superpowers-bridge/schema.yaml:774-779`), and the 2.3 RED/GREEN records in
`openspec/changes/fix-v2-blocking-defects/tasks.md`. Hunks for check 12, the
`plan` instruction item 2, checks 9–11 and R2 were confirmed out of scope
(diff hunks `@@ -282`, `@@ -480`, `@@ -545`, `@@ -567`) and are not reviewed here.

Base: `22c15cf`. Nothing committed. Working tree not mutated by this review.

## Spec Compliance

❌ Issues found — one Important (`superpowers-bridge/schema.yaml:460-462`).
Everything the brief enumerates as *required* is present and correct; the defect
is an inaccurate justification clause inside the new absent-`tasks.md` paragraph.

Verified point by point:

| Brief requirement | Verdict | Evidence |
|---|---|---|
| Opening condition reads `tasks.md` | ✅ | `schema.yaml:439` — "If tasks.md has any tasks marked `[~]` deferred" |
| "plan + test files" aside → "tasks + test files" | ✅ | `schema.yaml:454` |
| Blocking condition reads `tasks.md` | ✅ | `schema.yaml:469-470` |
| FRESHNESS affected sets moved | ✅ | `schema.yaml:774-779`: "check 2, check 7 and checks 8-11 read `tasks.md`; check 12 reads BOTH … an edit to `tasks.md` reaches check 2, 7, 8, 9, 10, 11 and 12, and an edit to `plan.md` reaches check 12 only" — exactly the brief's wording |
| No surviving `plan.md` carrier reference in check 7's body | ✅ | `awk '/7\. \*\*Deferred dogfood/,/CHECKS 8-12/'` piped to `grep -n plan` returns only "non-conforming **plan** that carries task rows" and "follow-up **plan**". Zero occurrences of the string `plan.md` |
| Freshness block's only `plan.md` mentions describe check 12 / the general staleness rule | ✅ | grep over the freshness range returns 2 hits: the "`tasks.md` or `plan.md` is modified" staleness sentence (unchanged from 22c15cf, attributes `plan.md` to no check) and "an edit to `plan.md` reaches check 12 only" |
| Fifth carrier reference | ✅ none exists | `grep -n -i "deferred\|\[~\]" schema.yaml` hits only check 7 and the CHECKS 8-12 shared TASK LINE definition (out of scope, untouched) |
| Enumeration / equivalent-test identification / retrospective-Misses routing unchanged char-for-char | ✅ | `git diff 22c15cf` hunks `@@ -418,10 +425,23` and `@@ -430,12 +450,21`: those three paragraphs appear as **context lines only** |
| `tasks.md` 2.3 ticked, RED/GREEN for f13 only | ✅ | `tasks.md` diff: `- [x] 2.3`, one RED + one GREEN, subject `f13-deferred-task-in-tasks::…` |
| D4 non-goal: no deferred-task→plan-entry rule | ✅ | The only clause mentioning the plan says the check does **not** read it (`schema.yaml:432-438`) |
| No archived loosen-plan artifact rewritten; schema major `2`; bundle `2.0.0` | ✅ | `git status --short` shows only `README.md` (group-1 work), `tasks.md`, `schema.yaml`; `version: 2`; `VERSION` = `2.0.0` |
| No files beyond `schema.yaml` + the change's `tasks.md` | ✅ | as above; the README modification predates this task (verified below) |

⚠️ Cannot verify from diff alone:
- `openspec schema validate` was not run (needs the bundle copied under
  `openspec/schemas/`, task 5.1). A YAML parse is the only sanity evidence
  available here, and the report says so honestly.
- `superpowers-bridge/templates/verify.md:104,118,119,168` still say §7 reads
  `plan.md` and that an edit to `plan.md` reaches "§7 and check 12". That is
  task 3.1's deliverable per the brief's Interfaces line, **not** a 2.3 defect —
  recorded so it is not lost: until 3.1 lands, the template contradicts the schema.

## Ruling A — absent `tasks.md` reports but does not BLOCK

**Unsound as stated.** The premise is that checks 2 and 8–12 "all read `tasks.md`"
and would therefore block an absent one. I walked each:

| Check | Behaviour on an absent `tasks.md` |
|---|---|
| 2 (`schema.yaml:392-395`) | "Confirm every checkbox in tasks.md is `- [x]`" — zero checkboxes, **vacuous PASS** |
| 8 (`schema.yaml:501`) | "For EVERY task line in tasks.md …" — zero task lines, **vacuous PASS** |
| 9, 10, 11 | scoped to "every task annotated `TDD: applicable`" — zero such tasks, **vacuous PASS** |
| 12 (`schema.yaml:648-720`) | **BLOCKs in every branch.** plan.md absent → "plan.md absent — no entry keys to compare" → BLOCK. plan.md present with keys → stage two's "entry key matching no task number" non-empty → BLOCK. plan.md present with no collectable key → "no collectable entry key" → BLOCK |

Outside the checks, the verify PRECHECK (`schema.yaml:365-368`) requires
`grep -c '^- \[x\]' openspec/changes/<name>/tasks.md` > 0, so an absent
`tasks.md` STOPs verify before verify.md is produced at all.

So the **conclusion** survives — an absent `tasks.md` is caught loudly, and check 7
not blocking is defensible — but the **stated reason is false for five of the six
checks it names**, and that false reason is written into the shipped text
(`schema.yaml:460-462`). See finding I1.

## Ruling B — check 7 keeps a local DEFERRED TASK definition

**Sound.** I read both definitions and hunted for a line they classify differently.

- Local (`schema.yaml:428-431`): "a task line in tasks.md whose checkbox marker is
  `~` — a line whose first non-space characters are `- [~]`".
- Shared (`schema.yaml:480-483`): "any line whose first non-space characters are
  `- [`, one character, `]` — `- [ ]`, `- [x]` and `- [~]` alike".

Both key on *first non-space characters* and both require the literal `- [`, one
character, `]`. The local one fixes that character to `~`; the shared one leaves it
free and explicitly lists `- [~]` among its members. Divergence candidates tested
and rejected: `-  [~]` (two spaces after the dash) fails **both**, since neither
tolerates anything between `-` and `[`; `- [~] text` and a nested `  - [~]` are
accepted by both; trailing content is unconstrained by both. **No line exists that
one counts and the other does not** — the local definition is exactly the `~`
subset. Its two additions (a `[~]` in a title/prose/record field is not a marker;
this check reads `tasks.md` and nothing else) have no counterpart in the shared
block and contradict nothing in it. The duplication is redundancy, not drift, and
the report's concern #2 (keeping the "used by checks 8-11" header true) is correct.

## RED genuineness

Genuine, on evidence independent of the report:

- `.superpowers/sdd/plan/task-2.3-red-walk.md` mtime `2026-09-08 08:14:31.404`;
  `superpowers-bridge/schema.yaml` mtime `08:15:28.481`. The walk predates the edit.
- I re-walked the **pre-edit** text from `git show 22c15cf:…` myself: the opening
  condition names `plan.md`; f13's `plan.md` is `# Fixture plan` plus
  `## 1 — checkout flow staging smoke test`, containing no `[~]`; condition false →
  "no deferred tasks"; blocking condition's second conjunct false → no block.
  **ACTUAL = PASS / no deferred tasks**, which is the recorded RED.
- I re-walked the **post-edit** text against f13: exactly one line
  `- [~] 1 Verify checkout flow against staging` matches → one deferred task, §7
  enumeration, equivalence step reached. **GREEN correct.**
- `failure:` states EXPECTED vs ACTUAL explicitly and names the direction. RED and
  GREEN `subject:` are identical character for character:
  `f13-deferred-task-in-tasks::check 7 finds one deferred task and requires §7 enumeration`
  (one `::`, non-empty on both sides — conforms to the grammar this change
  itself introduces).

f7 control, walked independently: its `tasks.md` carries `- [x] 1` and `- [x] 2`
only; no line matches `- [~]`; the new text yields "no deferred tasks" with §7
permitted to be blank, and the blocking condition's second conjunct is false. The
pre-edit text yields the same, so f7 genuinely has **no RED to give** — correctly
used as an acceptance control and correctly not recorded as a second evidence pair.

## README coupling (named risk 2)

`docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md:48` cites
check 7 by number and describes the old wording parenthetically as old. Check 7
keeps its number (`7.`) and its title (`**Deferred dogfood vs automated-test
equivalence**`) — verified against both the old and new text. **No edit is owed**,
and none was made: `git diff 22c15cf` on that README contains no check-7 row change
(its modified state comes from group 1).

## Strengths

- All four carrier references moved, and the grep control the brief asks for
  genuinely returns clean — including the deliberate removal of an earlier draft
  that named `plan.md` inside check 7's body in order to deny it. That is the right
  call: a control a reader must clear by parsing a negation is not a control.
- The three preserved procedures survive as diff **context lines**, the strongest
  available evidence of "character for character".
- The multiplicity sentence and the `[~]`-in-prose exclusion close two branches the
  pre-edit text left to the reader, in the same register as the rewritten neighbours.
- The RED walk was written to disk before the edit and its timestamp proves it —
  exactly what the tasks.md header's boundary 1 demands.
- Scope fence held: no edit to checks 8–12, the shared definitions block, or the
  `tasks` instruction.

## Issues

### Critical (Must Fix)

None.

### Important (Should Fix)

**I1 — `superpowers-bridge/schema.yaml:460-462`: the absent-`tasks.md` branch
attributes the report to checks that do not make it.**

The text reads: "an absent required artifact is a different defect, reported by the
checks that read `tasks.md` for their own purposes". Of the six checks that read
`tasks.md`, five (2, 8, 9, 10, 11) pass **vacuously** on an absent file — their
obligations are universally quantified over task lines, and there are none. Only
check 12 reports it, and even it does so by consequence (empty task-number set →
non-empty set difference, or its own absent-plan.md branch) rather than by naming
the absence.

Why it matters: this change exists because a check claimed something it could not
do. The same standard binds a justification clause. A reader executing check 7,
finding no `tasks.md`, and trusting this sentence would expect the sibling checks to
surface the absence; four of the five they would look at report nothing. The clause
is also the sole support for the ruling that check 7 need not BLOCK.

Fix (one clause, no behaviour change): name the reporter precisely — e.g. "…an
absent required artifact is a different defect, reported by check 12, whose key-set
comparison cannot succeed against an absent tasks.md, and by this artifact's own
PRECHECK — but the undetermined result must not be recorded as a pass." Everything
else in the paragraph, including the "NEVER as 'no deferred tasks'" prohibition,
stands as written.

### Minor (Nice to Have)

**M1 — `superpowers-bridge/schema.yaml:469-470`: the blocking condition still says
"`tasks.md` has `[~]` rows" rather than "has deferred tasks".** The definition
paragraph governs and is explicit that only line-initial `- [~]` counts, so the
correct reading is available — but the blocking sentence read alone invites the
looser "any row containing `[~]`". Substituting "any DEFERRED TASK" would bind it to
the definition. Pre-existing phrasing, inherited unchanged.

**M2 — partial §7 does not block.** With two `[~]` tasks and a §7 listing one,
"§7 is empty" is false, so nothing blocks. The added sentence makes the *obligation*
non-guessable, and check 7 produces §7 rather than auditing it, so an executor
following the text cannot land here — but an auditor re-reading a stale verify.md
can. Unchanged from pre-edit and arguably outside D4's scope; noted, not owed.

**M3 — `openspec/changes/fix-v2-blocking-defects/tasks.md`, 2.3 GREEN
`invocation:`** folds the f7 control walk into the record whose `subject:` names
f13. It is accurate, and the brief permits f7 to carry no record of its own, but a
record's `invocation:` describing a *second* fixture blurs the one-subject-per-record
discipline the sibling tasks hold to. A sentence outside the record — "f7 control
walked separately; no record, no RED available" — would read cleaner.

## Assessment

**Task quality:** Needs fixes

**Reasoning:** The carrier move itself is complete and correct — all four references
moved, the three preserved procedures byte-identical, the grep control genuinely
clean, the RED provably pre-edit, and both fixtures yielding the claimed verdicts
when walked independently. The one blocking issue is I1: the new absent-`tasks.md`
paragraph justifies its non-blocking choice by attributing the report to checks that
pass vacuously — the same class of unearned claim this change exists to remove.
