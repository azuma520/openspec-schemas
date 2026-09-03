# Verification Report — loosen-plan

> Produced after apply completed, to confirm the implementation matches specs / design / tasks.
> A failed check returns to the owning artifact for correction and verify is re-run.
>
> **Provenance of the evidence below.** Every task was implemented by a fresh subagent and reviewed
> by a separate one; six fix rounds were run. The per-task reports lived in a git-ignored SDD
> workspace that is deleted when the branch finishes, so the outputs that matter are reproduced
> **inline here** rather than cited by path. Where a number is quoted, the command that produced it
> is quoted with it.

---

## 1. Structural Validation

```
$ openspec validate loosen-plan
Change 'loosen-plan' is valid
```

Bundle validation from a **clean scratch project outside this repository** (the case that catches a
bundle which parses but is not installed):

```
$ openspec schema validate superpowers-bridge
✓ Schema 'superpowers-bridge' is valid

$ openspec schemas
  superpowers-bridge (project)
```

Both were run: `validate` answers *well-formed*, `schemas` answers *discoverable*. This repo has
previously hit the state where a bundle validated but was not listed — which means it is effectively
not installed — so the second is not redundant.

Dogfood copy in sync: `diff -r superpowers-bridge openspec/schemas/superpowers-bridge` → empty.

**Verdict: PASS.**

---

## 2. Task Completion

**27 of 27** tasks complete (`openspec list` → `loosen-plan ✓ Complete`, 0 unchecked).

**The count was 25/25 and was reopened to 25/27 by owner ruling**, because verification found two holes
that "all tasks complete" would have papered over: three bridge-owned surfaces still carrying a v1 TDD
claim no task covered (§14.1), and a fail-open PRECHECK (§14.2). Both were classified as **task-coverage
holes rather than scope expansion** — the specs already required these surfaces to be true; the task
breakdown missed them. Group 11 was added, the work done, reviewed, and only then ticked.

Checkboxes were ticked **only after a task passed independent review**, so the record distinguishes
*written* from *accepted*. Group 1–5 landed in commit `932a044`; group 6–9 in `a4c761c`; group 10 is
in this commit.

**Verdict: PASS.**

---

## 3. Delta Spec Sync State

Three delta specs are staged for sync at archive:

| Delta spec | Operation | Target |
|---|---|---|
| `specs/plan-contract/spec.md` | ADDED | `openspec/specs/plan-contract/` |
| `specs/tdd-evidence-contract/spec.md` | ADDED | `openspec/specs/tdd-evidence-contract/` |
| `specs/tdd-claim-accuracy/spec.md` | MODIFIED | `openspec/specs/tdd-claim-accuracy/` (exists) |

Not yet synced — `openspec archive` performs the sync. State is correct for this point in the cycle.

**Verdict: PASS (sync pending, as expected).**

---

## 4. Design / Specs Coherence Spot Check

| Design decision | Where it landed | Coherent? |
|---|---|---|
| D1 — plan loosening and the TDD evidence contract ship in **one** change, so no state exists where TDD has no carrier | this branch: `plan` instruction and `tasks` instruction changed in the same commit (`932a044`) | ✓ — verifiable from the commit itself, not from a claim |
| D2 — Plan Contract shape, entries keyed by task number | `schema.yaml` `plan` instruction; `templates/plan.md` | ✓ — and the entry-key **form** is now stated at the definition site (R25), because check 12 reads it |
| D3 — producer is agent direct generation, no skill invocation | `plan` instruction; `writing-plans` PRECHECK removed | ✓ |
| D4 — tasks.md is the SSOT for applicability; RED/GREEN under the checkbox | `schema.yaml` `tasks` instruction | ✓ |
| D5 — deterministic checks are the required control; enforcement is instruction-mediated | `verify` instruction checks 8–12 + boundary block | ✓ |
| D6 — schema major 2, bundle 2.0.0 | `schema.yaml: version: 2`; `VERSION` 2.0.0 | ✓ |
| D7 — the plan PRECHECK is removed because its subject is gone | `plan` instruction; every other PRECHECK untouched | ✓ — verified by diff, not asserted |

**One design claim was corrected during verification rather than after.** Design D5 and the specs use
"v1" to mean *the first generation of the instruction-mediated mechanism*. Six sentences carrying that
word shipped **inside the bundle**, which also carries `VERSION 2.0.0` and a "Migrating v1 → v2"
section teaching the reader that v1 means the previous schema major. To that reader, *"no **v1**
mechanism intercepts the omission"* reads as *v2 does intercept* — the exact inversion of the boundary
the sentence exists to state. All bundle-owned occurrences were made schema-relative
(`grep -rn "\bv1\b"` over `schema.yaml` and `templates/` → **0**). The specs' own use is on a
different axis and is not shipped; it was deliberately left as written.

**Verdict: PASS.**

---

## 5. Implementation Signal

| Surface | Signal |
|---|---|
| `superpowers-bridge/schema.yaml` | 583 → 902 lines (`wc -l`, both measured); `version: 1 → 2` |
| `superpowers-bridge/VERSION` | `1.0.1 → 2.0.0` |
| `superpowers-bridge/templates/plan.md` | micro-step shell → Plan Contract shape |
| `superpowers-bridge/templates/tasks.md` | annotation + normative record block |
| `superpowers-bridge/templates/verify.md` | new §8 reporting checks 8–12 |
| `superpowers-bridge/README.md` / `.zh-TW.md` | 564 → 607 lines each; 30 sections rewritten, mirrored 30/30 |
| `superpowers-bridge/templates/adopters/*.md` | both locales |
| top-level `README.md` / `.zh-TW.md`, `docs/roadmap*.md` | v2 row, v2 Released entry |
| `.github/workflows/version-check.yml` | drift grep repointed to the v2 row |

**Verdict: PASS.**

---

## 6. Front-Door Routing Leak Detector (warning, non-blocking)

`docs/superpowers/plans/` contains one pre-existing file (`2026-05-02-phase-1-implementation.md`) from
the repo's original build, predating this change. No new leak: this change produced no file under
`docs/superpowers/plans/`, and the `plan` artifact's output-redirection rule is unchanged.

**Verdict: PASS (no new leak).**

---

## 7. Deferred Manual Dogfood vs Automated Test Equivalence

`plan.md` contains no `[~]` rows, so this section is empty by the template's own rule.

**Verdict: PASS (not applicable).**

---

## 8. TDD Evidence Contract — Deterministic Checks 8–12

### 8.1 Results for this change

25 tasks, **all annotated `TDD: n/a`**, 0 applicable.

| Check | What it decides | Result |
|---|---|---|
| 8 | annotation present and well-formed on every task | **PASS** — 25/25; `applicable` = 0, `n/a` = 25, every `n/a` carries an accepted separator and a non-empty reason |
| 9 | every `applicable` task has RED and GREEN with required fields | **PASS (vacuous)** — no applicable task |
| 10 | RED outcome marker non-pass, GREEN marker pass | **PASS (vacuous)** |
| 11 | RED subject == GREEN subject | **PASS (vacuous)** |
| 12 | tasks.md task-number set == plan.md entry-key set, both differences empty | **PASS** — \|tasks\| = 25, \|plan\| = 25, both differences empty |

Controls run alongside, because a checker that read nothing produces the same output as one that read
everything: positive control — both files non-empty and parsed; negative control — a bogus key `99.9`
is absent from both sets.

**Three of the five checks are vacuous here, and that is a stated property of this change, not an
oversight.** design.md § Risks records it in advance: *"every task in this change's tasks.md is
honestly `TDD: n/a` … so the change verifies the `n/a` path and the deterministic checks against
synthetic fixtures, but produces no natural `applicable → RED/GREEN` record of its own."* Fabricating
an applicable task to exercise the carrier would have contradicted the contract it installs. The
carrier's end-to-end use is therefore **unproven by this change** and is owed to the first downstream
change with executable behaviour.

### 8.2 Mutation run — the evidence that the checks catch what they claim

Six fixtures, each violating exactly one check, plus one positive control. Run **blind** by an agent
with no context on this change, given only the rendered verify instruction and the fixtures under
**neutral, shuffled directory names** — the original names (`f1-missing-annotation`, …) contained the
answers, and using them would have proved nothing.

| Fixture | Violation | Blind agent's verdict | Correct? |
|---|---|---|---|
| f1 | annotation missing on task 2 | check 8 BLOCK | ✓ |
| f2 | applicable task with RED and no GREEN | check 9 BLOCK | ✓ |
| f3 | RED outcome marker is `PASS` | check 10 BLOCK | ✓ |
| f4 | RED subject ≠ GREEN subject | check 11 BLOCK | ✓ |
| f5 | tasks `{1,2,3}` vs plan `{1,2,9}` | check 12 BLOCK | ✓ |
| f6 | RED outcome is a `SyntaxError`, not a behavioural failure | **no deterministic BLOCK**; flagged under review judgement R1 | ✓ |
| f7 | conforming record with blank lines between fields | **no BLOCK** (positive control) | ✓ |

**6/6 correct, zero reported ambiguities** — the agent's own words: *"no place where the instruction's
wording left me guessing."* It volunteered that it had read none of the fixture, report or ledger files.

f6 is the sharpest case and is by design: check 10 passes formally (`ERROR` is a valid non-`PASS`
token) and only the review judgement catches the real problem. The blind agent named this itself as
*"the sharpest illustration of check passing ≠ judgement passing."*

f7 exists because six fixtures proving the checks **catch violations** say nothing about whether they
**pass conforming artifacts**. It was verified to have been a false BLOCK on check 9 under the
pre-fix reading of blank lines.

The blind run also found a gap neither the author nor the author's own fixtures could expose: check 9's
escape clause meant a **stray or fabricated RED/GREEN under an `n/a` task was caught by nothing**. That
became review judgement **R4**.

#### Fixture contents, verbatim

Reproduced in full so the mutation evidence is reproducible from this file alone, after the workspace
that held the fixtures is gone.

**f1 — missing annotation** (`plan.md`: entries `1`, `2`)

```markdown
## 1. Fixture group

- [x] 1 Add email validation
  - TDD: applicable
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS
- [x] 2 Update the README install section
```

**f2 — missing GREEN** (task 1 has RED only; task 2 annotated `n/a — prose/doc-only`)

```markdown
- [x] 1 Add email validation
  - TDD: applicable
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
```

**f3 — PASS marker on RED**

```markdown
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS
    - failure: expected 'Email required', got undefined
```

**f4 — subject mismatch**

```markdown
  - RED:
    - subject: test/auth.test.js::rejects empty email
  - GREEN:
    - subject: test/signup.test.js::rejects empty email
```

**f5 — key-set mismatch** — `tasks.md` has `1`, `2`, `3`; `plan.md` has `## 1`, `## 2`, `## 9`.
Equal counts, different sets: the case a count comparison cannot detect.

**f6 — SyntaxError RED**

```markdown
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: ERROR
    - failure: SyntaxError: Unexpected token ')' at src/auth.js:12
```

**f7 — positive control, blank-spaced conforming record**

```markdown
- [x] 1 Add email validation

  - TDD: applicable

  - RED:

    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL

    - failure: expected 'Email required', got undefined

  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS
```

### 8.3 Claim boundary — copied as written, claiming no more

These checks are deterministic in *what they decide* and agent-executed (instruction-mediated) in
*how they run*: their execution is the verify agent following the schema instruction. This schema
requires them to run before archive and to block on failure, but this is **not** a Harness-level,
mechanically enforced, non-bypassable archive-time gate — if the verify agent skips one, no mechanism
in this schema intercepts the omission, and review of this file is the only backstop. The checks
verify the **presence and structure** of the annotations and records; they do not establish that the
evidence is authentic (the evidence is agent-submitted), do not prove a test-first development
history, and do not assess semantic quality.

**Verdict: PASS.**

---

## 9. Guardrail 8 — verify instruction is append-only

The formal design's guardrail 8 forbids restructuring the verify instruction. Established
**against HEAD**, not against a mid-change snapshot: the `verify` block at the branch base is 108
lines, the working tree's is 264, and a `difflib` opcode comparison yields `['equal', 'insert']` only
— a single insert, with **108 of 108 pre-existing lines preserved in order**.

The reviewer confirmed this independently from the diff shape (`@@ -419,20 +419,158 @@`, zero `-`
lines) rather than from the author's own run.

> A note for whoever reads a future package: the snapshot-based review packages used during this
> change have **two live baselines** — the snapshot and HEAD — and a reviewer in doubt reaches for
> `git diff`, which answers the other question. This produced two false positives during the change.
> Any guardrail-style claim must name its baseline.

**Verdict: PASS.**

---

## 10. Task 9.1 — the CI drift check, and what could not be verified here

`.github/workflows/version-check.yml:44` now keys on the v2 Compatibility row:

```
line=$(grep -E '^\| v2 \| `' superpowers-bridge/README.md | head -1)
```

The `awk -F'\`'` extraction at lines 49–50 is unchanged, because the README row shape was built to
satisfy it. Extraction verified with the workflow's own commands: `1.3.1` / `v5.1.0`, both non-empty.

**Proof the repoint matters:** the pre-change key `^\| v1 \| \`` applied to the edited README still
selects the **v1** row — so without this task, the weekly drift check would keep validating against
the retired major.

**Stated honestly: the consequence is currently latent.** Both rows carry identical version values
today, so reading the wrong row has no visible effect yet. This is a correctly-pointed check, not a
repaired outage.

**DEFERRED — the one acceptance criterion this cycle cannot close.** Task 9.1's acceptance also asks
that *"the next scheduled or dispatched run is green"*. That cannot be verified from a worktree; it
needs a live GitHub Actions run after the branch is pushed. It is recorded here as an owed
verification rather than dropped, and it is the only acceptance criterion in this change that is not
closed by evidence in this file.

**Verdict: PASS, with one deferred item named above.**

---

## 11. Task 10.4 — the Plan Contract producer smoke test (Q4-A's first evidence)

### 11.1 What was run, and what was discarded

**Run 1 was discarded for instrument defects, and that was recorded before run 2 existed.** Its scores
are on the record and were not re-rolled for a better number: entry-key equality yes; no-vague-acceptance
**no**; interfaces-conditional **no**; no-step-prescription yes. A review of the *experiment design*
then found three defects in the setup:

1. **No unambiguously uncoupled task**, so the *conditional* half of the Interfaces rule went untested —
   the fixture's docs task consumed a shape and a set of names from its siblings, which is what
   Interfaces is defined as. The reviewer's verdict: *"a coin flip the fixture did not settle."*
2. **`templates/plan.md` was withheld.** The CLI wraps an instruction with a `<template>` block, so a
   real adopter receives the template — which demonstrates, at its own entry 1.2, the very
   Interfaces-omission rule two of the scores judged. The test was **harder than reality**.
3. **Four contract clauses went unmeasured**, notably the v2-only rule that plan.md must not hold a
   second copy of the RED/GREEN evidence.

Three pre-run corrections were made — none of them coaching: the producer received the **full
CLI-rendered artifact block** including `<template>`; the docs task was replaced with a genuinely
standalone one (a CI job checking that files under `config/` parse as YAML, worded to know nothing
about what any file contains); and the no-duplicate-evidence clause was added as a fifth criterion.
Subject, task count and the no-coaching rule were unchanged.

### 11.2 Run 2 result — scored by an agent not told run 1 existed

| # | Criterion | Result |
|---|---|---|
| 1 | entry-key set equality | **yes** — `{1.1,1.2,2.1,2.2,3.1,3.2}` both directions |
| 2 | no vague acceptance language | **no** — entry 1.1: *"a default resolution behaviour (e.g. client IP) is defined"* names no observable and leaves the default unfixed, while design.md D2 fixes it |
| 3 | Interfaces present where coupled, omitted where not | **no**, one wrong omission — see below |
| 4 | no step prescription | **yes** — two borderlines ruled permitted: paths lifted verbatim from tasks.md, and a function signature as the decision-rich shape the contract allows |
| 5 | no second copy of the evidence | **yes** — no record, no shape, no grammar; it did not even use the permitted echo |

**What the corrected instrument bought, and it is the reason the second run was worth its cost:**

- **The conditional half was finally tested and passed.** The genuinely standalone task exchanges
  nothing, and its Interfaces omission is **correct**.
- **The 1.1 omission reproduced with the template present**, so it is not an artifact of the withheld
  template.
- **No invented couplings** in either run.

### 11.3 The structural finding

Both scorers, independently and on different instruments, reached the same conclusion about the
contract text: **"Global constraints copied verbatim from the specs" is unconditional and gives no
fallback when a change has no `specs/` directory.** The producer had to both choose a source and
silently relax *verbatim* to *drawn from*. This does not depend on either run's instrument being
sound, and it is a defect in the contract, not in the producer.

On the Interfaces omission, the scorer was asked whether both failures landing on entry 1.1 was
coincidence, and told plainly that "coincidence at N=1" was an acceptable answer. It separated them:

> Not coincidence in the Interfaces case, and the mechanism is visible in the instruction rather than
> constructed: the field is worded **consumer-first**, and an entry written before its consumers exist
> has nothing to consume — the later entries name 1.1 correctly *because by then the other end was on
> the page*. **Asking each entry for its own edges makes an upstream-only entry the one place where a
> real edge is invisible from where you stand.**

The acceptance-criterion failure it read as **coincidence at N=1**.

This matches the group-10 reviewer's independent conclusion from the other side: the Interfaces
omission would **survive review**, because *"the omission is only visible if the reviewer builds the
coupling graph themselves, which review of a single entry does not force."* Producer-side blindness
and reviewer-side blindness are two faces of one property — a per-entry field cannot surface an edge
that is invisible from the entry.

### 11.4 D3 triggers — consulted, and answered at the strength one sample supports

| Trigger | Verdict |
|---|---|
| recurring unverifiable acceptance criteria | **cannot tell from one sample** — one instance observed |
| recurring boundary / interface / dependency omissions | **cannot tell from one sample** — one instance observed, and it is the one the contract's own self-review asks about |
| reviewers repeatedly rewriting plans wholesale | **not observed** — no reviewer pass exists in this sample |
| high variance across producers | **cannot tell** — one producer |

Two of the four triggers are about *recurrence* and *variance*, which a single run cannot show by
definition. This is stated as one sample, not a verdict.

### 11.5 Stated limitation of run 2

The rendered artifact block's `<output>` line carries an absolute path into a scratch project that
also contains the installed bundle, and nothing enforced inputs-only reading. The scorer bounded what
that permits concluding: the bundle holds **no worked conforming plan**, and the entry skeleton was
already in the `<template>` the producer legitimately received, so the marginal information available
was restatements of the same contract, not an exemplar to copy. It permits concluding the produced
shape is reachable from the contract as rendered; it forbids calling this a clean fresh-context run.

**Q4-A recommendation is not made here.** The decision belongs to the project owner; this file reports
what one corrected run shows.

**Verdict: PASS as a completed exercise. The Q4-A judgement is deferred to the owner.**

---

## 12. Superseded-claim sweep (task 10.2)

**Class (a) — exact superseded sentences, expect 0.** Across `schema.yaml`, `templates/` (including
`adopters/`), both bridge READMEs, both top-level READMEs and root `CLAUDE.md`:

| Sentence | Hits |
|---|---|
| `neither enforces nor verifies TDD` | 0 |
| `TDD micro-steps` | 0 |
| `TDD arrives via plan.md task content` | 0 |
| `writing-plans' standard task format` | 0 |
| `plan-step TDD` | 0 |
| `TDD discipline came from plan steps` | 0 |
| `did not require TDD` | 0 |
| `任務單沒要求 TDD` | 0 |
| `計畫步驟的 TDD` | 0 |

**The last five phrases were added by task 11.1, and the reason is the point.** The original four matched
**none** of the three surviving v1 claims found at verification (§14.1) — so this sweep reported clean
while three normative surfaces still carried them. Extending the list is the half of that fix that stops
the next instance depending on a reader noticing. Each of the three was checked against its **pre-fix**
text (`git show a4c761c:…`) to confirm the new phrases would actually have caught it: a phrase list that
only matches the repaired wording would be worthless.

`計畫步驟的 TDD` matches nothing in the repo and is a speculative entry — recorded here rather than
removed, so the "five added" count is not read as five evidenced ones.

Cross-verified through a **structurally different path** (a Python reader rather than `grep`), with a
missing-file report and a positive control, after a silent zero was found elsewhere in this sweep
(below). 16 surfaces scanned, no missing files, total 0, control present.

**Class (b) — boundary vocabulary, where 0 is explicitly not the criterion.** `mechanical`,
`guarantee`, `bypass`, `gate`, `fail-closed`: 39 raw hit-lines across 9 surfaces, grouped into 25
dispositioned rows under a stated grouping rule. Every hit is a negation, an in-boundary claim, or
out of scope. **0 findings.** A reviewer independently spot-checked the four most positive-sounding
dispositions and found none wrong.

> **An honest note about this sweep's first version.** Its original table recorded "0 hits" for
> top-level `README.md` and root `CLAUDE.md`. Those were wrong — actually 1 and 4. The cause was an
> ad hoc grep that silently returned nothing and was trusted without cross-checking. The five missed
> hits were later read individually and every one is a negation or out of scope, so **the conclusion
> held** — but the evidence behind it had not. It is recorded because a zero from a reader that read
> nothing is byte-identical to a zero from a reader that read everything.

**R18 pointer check.** The apply instruction now points at the `tasks` artifact for the annotation
grammar and record shape rather than restating them. Both cross-references were followed to the
pointed-at text and confirmed to contain what they claim.

**Verdict: PASS.**

---

## 13. Task 10.3 — v2 render check

In a clean scratch project, `openspec new change <name> --schema superpowers-bridge` succeeded, and:

- `openspec instructions plan` — **no `writing-plans` PRECHECK**; the Plan Contract text renders in full
- `openspec instructions tasks` — the `TDD:` annotation rule renders in full
- `openspec status` — the change was accepted and its **8-artifact DAG matches v2**

**One qualification, stated rather than glossed:** `openspec status` does not literally print
`version: 2` — there is no such field in its output. The substitute evidence is that validation passes
against a bundle whose `schema.yaml` declares `version: 2` and that the artifact DAG matches. Reported
at that strength.

**CJK anchors** added by the zh-TW mirror (`#從-v1-遷移到-v2`,
`#0-pre-flight--驗證必要的-superpowers-skill`): the target headings exist verbatim and follow the
convention the file's pre-existing, working anchors already use. GitHub's renderer was **not**
executed and no claim is made about it.

**Verdict: PASS.**

---

## 14. Group 11 — the two holes found at verification

Both were reopened by owner ruling after this report's first draft, and both are now closed and reviewed.

### 14.1 Three v1 TDD claims on surfaces no task covered

`templates/retrospective.md` §4's row label and its zh-TW note, and the `retrospective` instruction's
Skipped-skill rules in `schema.yaml`, all still described TDD as arriving from **plan steps** — a category
that does not exist under v2, where every task carries an applicability annotation. `tdd-claim-accuracy`
Scenario 2 forbids this on **any** bridge-owned normative surface, so the specs already required these to
be true; the task breakdown simply missed them. Rewritten to the v2 categories (`TDD: n/a` is the
declaration, and it is not a skip) with each passage's original purpose intact — the reviewer confirmed
both halves survive, including "a blank subsection is not proof of compliance".

Class swept before editing: ten hit-groups dispositioned, **no fourth instance**. One judgement call ruled
by the owner's standing convention: `README.md:544` / `README.zh-TW.md:544` restate the v1 carrier inside
a dated 2026-08-26 upstream-drift record, bracketed by "**Resolved in v2**" before and "the deeper fix
landed in schema v2" after. **Kept as a record** — it never states the v1 carrier as current, and the
repo's own convention exempts records ("text in it going out of date is the record working").

### 14.2 The retrospective PRECHECK was fail-open

It ran `! grep -q '^- \[x\] ❌ FAIL' verify.md` — which passes when verify.md records **no verdict at
all**, because the grep finds no FAIL line and absence is read as permission. **Not theoretical: this
report's own first draft had zero decision checkboxes and passed it.**

Rewritten fail-closed — proceeding now requires positive evidence of an acceptable verdict:

| State | Result |
|---|---|
| exactly one checkbox set, and it is `✅ PASS` or `⚠️ PASS WITH WARNINGS` | proceed |
| none set | **BLOCK** — no verdict recorded |
| more than one set | **BLOCK** — ambiguous |
| `❌ FAIL` set | **BLOCK** |

**Exercised four ways, three of them by breaking it on purpose** — a guard that has not been broken is
not known to work: this change's real verify.md (one box, `⚠️ PASS WITH WARNINGS`) → PROCEED; all boxes
removed → count 0 → BLOCK; two boxes set → BLOCK; FAIL only → BLOCK. **And the old command was run
against the no-boxes fixture and returned exit 0** — the hole demonstrated rather than described.

The reviewer confirmed by reading the commands that absence BLOCKs *because absence is measured*
(`grep -c` yields a literal `0`; its exit 1 does not suppress the count), not by accident. A "why this
must not be simplified away" clause is present, because a future editor who does not know will simplify
it back.

Coupling caught by the implementer and not named in the dispatch: design touch #5 in **both** bridge
READMEs documented the old one-command PRECHECK and would have gone false; both updated.

---

## 15. Assurance decision — the Codex independent-review debt

A prior session recorded: *"Codex independent review 未補 … 只過 fallback 審 … schema 契約屬高風險——Codex
額度恢復後 SHALL 補獨立審，補審前不 archive。"*

**Classified from the original wording, not from convenience.** The SHALL's object is 「補**獨立審**」 —
supply *independent review*. The stated deficiency is 「只過 **fallback** 審」. Codex appears as the
**timing condition** (「額度恢復後」), i.e. the vehicle designated at the time. The repo's own
`rules/auto-loop.md` § Review Dispatch already treats reviewer identity as substitutable — "Codex
unavailable → a contract-aware fallback reviewer carries the gate" — with the gate, not the reviewer,
being what must hold.

**This is therefore an equivalent-assurance substitution, not a Codex-specific waiver.** The requirement
was independent review beyond a single fallback pass; what this change actually received:

- 11 independent subagent reviews and re-reviews, each on a fresh context
- 1 blind mutation exercise by an agent with no knowledge of the change
- 1 blind plan-generation sample plus an independent scorer, on a corrected instrument
- 1 whole-branch review on the full 2009-line diff
- 6 fix rounds, which caught defects that would otherwise have shipped — including a check that both
  wrongly blocked conforming work and wrongly passed the defect it existed for, and a front-page
  description that under-claimed what verify does

**Recorded verbatim as the owner directed:** *Original Codex-specific review debt is explicitly
dispositioned for this change using the completed multi-layer independent review chain. This is an
explicit assurance decision, not a silent skip, and does not establish a general precedent for future
changes.*

Scope of this decision: **`loosen-plan` only.** It does not retire the debt for any other change, and it
does not amend `rules/auto-loop.md`'s fallback discipline, under which a high-risk item would ordinarily
be re-reviewed when external review recovers.

---

## Overall Decision

| Dimension | Status |
|---|---|
| Completeness | 25/25 tasks; 3 delta specs staged for sync |
| Correctness | 5/5 deterministic checks pass; mutation run 6/6 + 1 positive control |
| Coherence | 7/7 design decisions landed; one shipped wording defect found and fixed during verification |

- [ ] ✅ PASS — 可進入 finishing-a-development-branch 與 archive
- [x] ⚠️ PASS WITH WARNINGS — 可進入後續步驟但需注意：一個出貨文字缺口（見下方 WARNING）與四項接力
- [ ] ❌ FAIL — 返回失敗的 artifact 修正後重跑 verify

**下一步**：retrospective → checkpoint commit → archive → PR。

**No CRITICAL issues. One WARNING. Four items carried forward.**

### WARNING — a gap in shipped contract text, found by §11.3 and not closed by this change

The `plan` instruction requires global constraints "copied **verbatim** from the specs"
(`schema.yaml:293-295`, `specs/plan-contract/spec.md:5`) and **states no fallback for a change that has
no `specs/` directory**. Two independent scorers, on two runs and two instrument configurations, each
hit it unprompted: the producer had to both choose a source and silently relax *verbatim* to *drawn
from*. It is a defect in the contract text rather than in any producer, and it does not depend on
either run's instrument being sound.

It is left open deliberately — closing it means amending a spec this change is landing, which is a
decision for the owner, not a verification fix. Recorded here so the Overall Decision does not read
cleaner than the file it summarises.

### Carried forward

1. **Task 9.1's live CI run** — cannot be verified from a worktree; owed after the branch is pushed.
   The only acceptance criterion in this change not closed by evidence in this file.
2. **The evidence carrier is installed but not exercised end-to-end** — all 25 tasks are honestly
   `TDD: n/a`, so checks 9–11 are vacuous here. Predicted in design.md § Risks; the first downstream
   change with executable behaviour is the real dogfood.
3. **The v1 → v2 migration guide has never been walked** — no in-flight v1 change has been migrated
   through its four steps. The guide is stated and reviewed, not exercised.
4. **`tasks.md` task 4.2 carries a false premise on the record** — it describes updating
   `templates/verify.md` "§4 TDD rows" that never existed (`git show 5aa19bf:…/templates/verify.md |
   grep -i tdd` → 0 hits). The delivered §8 is the right outcome; the task text is left unedited as the
   historical record of what was planned.
5. **Class-(a) detection is exact-phrase, so a differently-worded fourth instance would still slip.**
   Narrowed rather than closed: the class-(b) boundary-vocabulary sweep is the hand-reviewed net such an
   instance would most likely fall into. Widening class (a) to patterns is a separate change.

**Two items that were on this list in the first draft are now closed rather than carried**: the three v1
TDD survivors (§14.1) and the fail-open PRECHECK (§14.2). They were reopened as tasks, fixed, reviewed and
ticked — not deferred.

**Result: PASS. Ready for retrospective and archive**, with the warning and the four items above
recorded for the retrospective rather than resolved here.

### Provenance of this section

This Overall Decision was itself corrected during the final whole-branch review. Its first version read
"No CRITICAL issues. No WARNING issues." while §11.3 already recorded the contract gap above — a summary
that let a reader take away **less** than the file established. Two counts in this file were also wrong
and are corrected: `schema.yaml`'s line count (`583 → ~860`, actually 902) and "7/7 design decisions"
against a table that listed six. Recorded rather than silently amended, because a verification report
that quietly fixes its own numbers is exactly the artefact this change exists to make harder.
