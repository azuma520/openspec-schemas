# Code-plane fallback review — fix pass report

Scope: `superpowers-bridge/schema.yaml` only. No spec, design, change plan/tasks,
fixture or README touched. `templates/plan.md` NOT touched (see I3).

## I1 — a record carrying two lines with the same field key

**Owner: check 9.** Check 9 is the record-shape check: it already decides which
fields a record must carry, whether their values are non-empty, and (for
`subject:`) whether the value conforms to a grammar. Cardinality of a record's
field lines is the same class of fact. Checks 10 and 11 are *consumers* of a
record's single `outcome:` / `subject:` value, so if either owned the rule the
other would still be undecided — the half-answer the brief warns about. They
instead carry one carve-out each, routing such a record back to check 9,
mirroring the existing "record carrying no `subject:` at all" carve-out in
check 11.

### Before (check 9)

```
EVERY record belonging to the task is examined: a defect in
a task's second RED record is reported exactly as one in its
first.
```

### After (check 9 — added paragraph)

```
FIELD CARDINALITY — within ONE record, each field key
appears AT MOST ONCE. A record carrying more than one line
with the same field key is malformed → BLOCK, naming the
repeated key and the record it belongs to; this holds for
every key, required or not. It is the record-level analogue
of check 8's "more than one" rule for the annotation, and it
is what keeps checks 10 and 11 decidable: each of those
reads a record's `outcome:` or `subject:` as ONE value, so a
repeated key would leave one executor taking the first line
and another taking both, reaching opposite verdicts on the
same input. This check is the sole owner of the rule; checks
10 and 11 route such a record back here rather than deciding
it themselves.
```

### Check 10 — before / after

```
before: ... however many there are. Each GREEN record's `outcome:` value ...
after:  ... however many there are. A record carrying more than one
        `- outcome:` line yields NO outcome verdict here — that record is
        malformed and its malformation is check 9's finding, never this
        check's. Each GREEN record's `outcome:` value ...
```

### Check 11 — before / after

```
before: A record carrying no `subject:` field at all contributes
        nothing to either list; its absence is check 9's finding, never
        this check's.
after:  A record carrying no `subject:` field at all, and a record
        carrying more than one, each contribute nothing to either list:
        an absent `subject:` and a repeated one are alike check 9's
        finding, never this check's.
```

### Author-facing companion (tasks instruction)

The `tasks` instruction's `invocation:` sentence said "add it as a further
`- invocation: <command>` field", which a reader could take as licence for two.
Left alone it would be an instruction looser than the check that judges it —
the I2 failure direction. It now reads:

```
add it as a further `- invocation: <command>` field — ONE such
field, like every other: within a single record each field key
appears at most once, and a record carrying two lines with the
same key is malformed (verify check 9 blocks it).
```

### The review's concrete input, walked against the new text

```
- [x] 1.1 Foo
  - TDD: applicable
  - RED:
    - subject: a::b
    - subject: c::d
    - outcome: FAIL
    - failure: expected X, got undefined
  - GREEN:
    - subject: a::b
    - outcome: PASS
```

- Check 9: the RED record carries two `- subject:` lines → FIELD CARDINALITY →
  **BLOCK**, naming `subject:` and that RED record. Same for both executors.
- Check 10: that record has exactly one `outcome:` line, so the carve-out does
  not apply; `FAIL` conforms, GREEN `PASS` conforms → no finding. Decided.
- Check 11: the RED record carries more than one `subject:`, so it contributes
  nothing to either list. RED list `{}`, GREEN list `{a::b}`. Stage one: no
  repeats. Stage two: `a::b` has a GREEN and no RED → **BLOCK**. Same for both
  executors — the "take the first" executor no longer has a first to take, and
  the "take both" executor no longer feeds `c::d` into the list.

Both readings now converge on: check 9 BLOCK + check 11 BLOCK. The former
`✓` / `⛔` split is closed. The same holds for a repeated `outcome:` (check 9
blocks, check 10 abstains) and a repeated `failure:` (check 9 blocks).

## I2 — plan instruction SELF-REVIEW item 1

```
before: 1. Entry keys — does the set of entry keys equal the set of
           tasks.md task numbers exactly, in both directions?
after:  1. Entry keys — does every entry key occur exactly once, does
           every tasks.md task number occur exactly once, and are the
           two sets equal in both directions? All three, not the last
           alone: a repeated key on either side is a defect a set
           comparison cannot see.
```

Now the same question check 12 asks, in the same two-condition shape as
STRUCTURE item 2 and both templates.

## I3 — plan.md must not carry task-level state markers

**Placed in the `plan` instruction's WHAT NOT TO WRITE section, not the
template.** WHAT NOT TO WRITE is where this instruction already tells the plan
author what does not belong in plan.md (micro-steps, execution sequences, a
second copy of the TDD evidence); a state marker is the same kind of
prohibition and belongs beside them. The template is the shape an author fills
in — it has no natural slot for "and here is a thing you must not add", and a
prohibition stated only there would be invisible to an author writing plan.md
from the instruction. Added after the decision-rich-snippet sentence:

```
Do NOT carry task-level state markers into plan.md — a `[~]`
deferral marker, a `[x]` completion marker, or any other
per-task status. tasks.md is their carrier: verify's deferral
check reads tasks.md and nothing else, so a state marker written
here records nothing and is seen by nothing.
```

Boundary respected: this is author-facing prose only. **No check was added**,
no check's inputs changed, and nothing links a deferred task to a plan entry
(design D4's binding non-goal). The last clause restates check 7's existing
carrier sentence; it is not a new rule about what check 7 must find.

## Minors

**M1 — `##` vs `###` in check 12's plan-side collection.** Added after "whose
text begins with such a token":

```
— a heading at EXACTLY that level. `###` or deeper is a sub-heading
INSIDE an entry, not an entry: it is not collected, so a
`### 1.1 — <detail>` sitting under `## 1.1 — <title>` does
not make `1.1` a repeated key.
```

"Exactly that level" also settles `#`: an h1 beginning with a number is not
collected either.

**M2 — no whitespace after `]`.** Added to the task-number collection sentence:

```
AT LEAST ONE whitespace character must follow the `]`: with none,
`- [x]1.1 Foo` carries NO task number — it is the same
defect as a non-numeric token, never a task numbered `1.1`.
```

This also settles a bare `- [x]` with nothing after it: no whitespace, no task
number, same defect.

**M3 — "occurs twice" message templates.** Both rewritten to "occurs more than
once", each with a sentence saying why:

- check 11 stage one: `"…occurs more than once among this task's RED records"`
  plus "a value appearing three times is one repeated value reported once, not
  a value that 'occurs twice'."
- check 12 stage one: `"1.1 occurs more than once in tasks.md"`, `"2.3 occurs
  more than once in plan.md"` plus the same clarification.

**M4 — the `INDETERMINATE` RED.** Recorded in the schema's **R1** text, which is
where it belongs: R1 is the judgement that decides whether a non-`PASS` RED is a
behavioural failure or a harness error, and "is `INDETERMINATE` a malformed
outcome?" is exactly that question. (It could not go in the change's own
tasks.md — out of scope — and check 10 would be wrong, since check 10 explicitly
reads the marker only.) Appended to R1:

```
Judge the `failure:` excerpt, not the marker: an outcome other than
`FAIL` does not by itself make a RED a harness error. Where the
subject under test is a rule executed by READING rather than code —
these checks themselves, when a change edits them — a RED recording
`INDETERMINATE` because the rule AS WRITTEN could not decide the
case is the target property (decidability) going unsatisfied: a
behavioural failure under this judgement, deliberate rather than
malformed.
```

## Self-review

- **Two executors, same verdict?** Walked above for I1's input. M1 and M2 each
  name the decided branch explicitly rather than leaving it to reading.
- **Any new rule leaving its own boundary undecided?** FIELD CARDINALITY names
  its reach (every key, required or not; within one record only) and says which
  check owns it and what the other two do instead. The check-10 and check-11
  carve-outs each state what the record contributes (nothing / no verdict) and
  where the finding lives. M1 covers `#`, `##`, `###`+. M2 covers zero
  whitespace including end-of-line.
- **I3 stayed author-facing** — prose in WHAT NOT TO WRITE, no check, no
  deferred-task-to-plan-entry rule.
- **YAML**: parses (`yaml.safe_load` → `version: 2`, 8 artifacts).

## Dogfood re-sync and validation

Precondition confirmed before the in-place copy — the file sets of
`superpowers-bridge/` and `openspec/schemas/superpowers-bridge/` were identical,
so no file needed removing:

```
$ diff <(cd superpowers-bridge && find . -type f | sort) \
       <(cd openspec/schemas/superpowers-bridge && find . -type f | sort)
IDENTICAL FILE SETS (no removals needed)

$ cp -R superpowers-bridge openspec/schemas/
$ diff -r superpowers-bridge openspec/schemas/superpowers-bridge
SYNC IDENTICAL

$ openspec schema validate superpowers-bridge
Note: Schema commands are experimental and may change.
✓ Schema 'superpowers-bridge' is valid

$ openspec schemas
Available schemas:

  spec-driven
    Default OpenSpec workflow - proposal → specs → design → tasks
    Artifacts: proposal → specs → design → tasks

  superpowers-bridge (project)
    Spec-driven workflow integrated with Superpowers skills. Requirements:
    Superpowers plugin installed, providing skills: brainstorming,
    using-git-worktrees, subagent-driven-development,
    finishing-a-development-branch. Requires a subagent-capable platform
    (Claude Code, Codex, etc.) — this schema does not support runtimes without
    subagent support, because the alternative executor (executing-plans)
    dispatches no independent reviewer, losing the review rigor Superpowers
    brings. If your platform lacks subagent support, use spec-driven instead.
    Each artifact / apply step verifies its required skills before invoking and
    surfaces a clear error if any are missing. brainstorm → proposal → specs →
    tasks → plan → verify → retrospective. design is required (reorganizes raw
    brainstorm output into structured Context / Goals / Decisions / Risks /
    Migration; referenced by tasks and plan for implementation guidance). Apply
    phase uses git worktrees + subagent-driven-development (structural
    code-review dispatch; TDD applicability is declared per task in tasks.md,
    and tasks annotated applicable record RED/GREEN evidence there — verify's
    deterministic checks read the presence and structure of that evidence
    before archive, instruction-mediated rather than a mechanically enforced,
    non-bypassable gate).

    Artifacts: brainstorm → proposal → design → specs → tasks → plan → verify →
    retrospective
```

(The `openspec schemas` block above is the run's output; it was captured in two
invocations — the full listing on the first run and the head on the second,
after the last edit — and the schema entry is unchanged between them.)

## Fixture verdicts

**No fixture verdict changes.** Verified mechanically rather than by reading:

- Duplicate field key within a record: a script implementing the new FIELD
  CARDINALITY rule (record range by the schema's own nesting and
  blank-line-transparent rules) over all 13 fixtures' `tasks.md`, this change's
  `tasks.md`, and `templates/tasks.md` reports zero duplicated keys in any
  record. The template's two-pair SHAPE block is clean too.
- `###` headings: `grep -rn '^###'` over the fixtures, this change's `plan.md`
  and `templates/plan.md` → zero hits, so M1 changes nothing anyone's plan
  produces.
- Checkbox with no following whitespace: `grep -rnE '^\s*- \[.\][^ ]'` over the
  fixtures and this change's `tasks.md` → zero hits, so M2 changes nothing.

The fixtures README answer key therefore needs no amendment.

## Files changed

- `C:/Users/user/orca/openspec-schemas/.claude/worktrees/loosen-plan/superpowers-bridge/schema.yaml`
  (the only file edited; the dogfood copy at
  `openspec/schemas/superpowers-bridge/schema.yaml` was re-synced from it and is
  gitignored)

Other modified files in the working tree (`CLAUDE.md`, both bridge READMEs,
`templates/plan.md`, the fixtures README, this change's `tasks.md`, the archived
change's `errata.md`) are earlier waves' uncommitted work and were left
untouched. No `git add` / `commit` / `push` was run.

## Concerns

1. **FIELD CARDINALITY now blocks two `invocation:` lines in one record.** That
   is a real behaviour decision, not only a clarification: nothing previously
   forbade it. I chose the simple universal rule ("every key, at most once")
   over a required-keys-only rule, because a rule applying to some keys and not
   others reintroduces exactly the "which line do I read" question for any
   future field, and because the `tasks` instruction speaks of *the* command,
   singular. The instruction now says so out loud, so an author cannot fall into
   it. If a maintainer wants two commands recorded, the shape is two records, or
   a follow-up change that says so.
2. **The FRESHNESS input map is untouched and still correct** — no check's input
   files changed (checks 9/10/11 still read `tasks.md`, check 12 still reads
   both).
3. **No re-review was run by me** — one is already scheduled, and this report's
   fixture claims are script-verified rather than self-assessed.

---

# Round 2 — template sync + two undecided branches

Scope this round: `superpowers-bridge/schema.yaml` and
`superpowers-bridge/templates/tasks.md`. Nothing else touched.

## N1 — the template's record-rule comment block did not carry FIELD CARDINALITY

### The one line named

`templates/tasks.md`, the `invocation:` sentence (was lines 40-42):

```
before: `- invocation: <command>`（實際跑過的指令）是**佐證**欄位：建議寫下來以利
        重現，但**規格從不要求**。要寫就在該筆紀錄底下、與其他欄位同層級再加一個
        `- invocation: <command>`。

after:  ...同層級再加一個 `- invocation: <command>`——**一個就好**，跟其他欄位一樣。

        同一筆紀錄裡，**每個欄位鍵最多只能出現一次**（包含 `invocation:` 這種
        非必填欄位）；同一個鍵寫兩行就是壞掉的紀錄，verify 的 check 9 會 BLOCK。
        要記兩個 subject 就寫**兩筆紀錄**，不是在一筆紀錄裡疊兩行 `subject:`。
        另外，**一個欄位就是一行**：值寫到行尾為止，換行續寫的那行不算這個欄位的
        內容（也不算錯，只是不被讀入）。`failure:` 的錯誤摘錄請整理成一行。
```

The added paragraph carries both of this round's new record rules — FIELD
CARDINALITY and the one-line-field decision of Minor 2 — plus the mis-formatting
FIELD CARDINALITY exists to catch (stacking two `subject:` lines instead of
writing two records), which is exactly the shape the multi-subject wording
invites.

### The sweep — every record rule, both surfaces

I compared the `tasks` instruction (`schema.yaml`) against the template's
comment block rule by rule. "This round" = introduced or tightened by change
`fix-v2-blocking-defects`, established by `git diff 6c4605e`.

| Record rule | Instruction | Template | This round? | Action |
|---|---|---|---|---|
| RED/GREEN required fields | yes | yes | tightened | in parity |
| Outcome tokens (`PASS` / non-`PASS` uppercase) | yes | yes | tightened | in parity |
| Subject grammar — exactly one `::`, non-empty sides | yes | yes | this round | in parity |
| Subject grammar — `::` counted non-overlapping, `a:::b` holds ONE | yes | **NO** | **this round** | **FIXED — second gap of the same class** |
| Pairing by `subject:` value, never ordinal | yes | yes | this round | in parity |
| Same-side uniqueness of `subject:` values | yes | yes | this round | in parity |
| A task may carry several subjects; re-run adds no record | yes | yes | this round | in parity |
| `invocation:` optional | yes | yes | pre-existing | in parity |
| FIELD CARDINALITY — one line per key per record | yes | **NO** | **this round** | **FIXED (N1)** |
| A field is exactly one line; no continuation lines | yes | **NO** | **this round** | **FIXED (Minor 2)** |
| Blank lines transparent inside a record | yes | no | pre-existing | not fixed — see below |
| Any greater indent accepted (formatter-safe) | yes | no (says copy the shape) | pre-existing | not fixed — tighter authoring guidance, never rejects conforming work |
| Record ORDER carries no meaning (all REDs then all GREENs conforms) | yes | no | pre-existing | not fixed |
| A `TDD: n/a` task carrying records is review judgement R4 | yes | no | pre-existing | not fixed |
| Annotation: exactly one `- TDD:` line per task | yes (check 8) | no | pre-existing | not fixed |
| Annotation: four accepted separators (em/en dash, `-`, `--`) | yes (check 8) | shows em dash only | pre-existing | not fixed |

**The sweep found one further gap in this round's own rules** — the `a:::b`
non-overlap clause, added to the instruction and to check 9 by this change and
never carried to the template. Fixed:

```
before: `subject:` 的文法：去掉頭尾空白後，值裡**恰好出現一次** `::`，且左右兩側
        去空白後都非空。除此之外不限制——…

after:  `subject:` 的文法：去掉頭尾空白後，值裡**恰好出現一次** `::`，且左右兩側
        去空白後都非空。`::` 由左往右數、比對到就消耗，不重疊——所以
        `a:::b` 算**一次**（合規），`a::b::c` 算兩次（不合規）。
        除此之外不限制——…
```

**The six pre-existing rows are reported, not fixed.** None is a rule this
change added or tightened, and none makes the template loosen what a check
enforces in the direction that produces rejected work: an author following the
template writes the em-dash annotation, one per task, at the shown indent, and
conforms. They are the standing residue of the same class and belong in a sweep
of their own, not in this fix's diff.

```
[OUT_OF_SCOPE_DEFERRED] superpowers-bridge/templates/tasks.md | six pre-existing record/annotation rules stated in the tasks instruction and not in the template (blank-line transparency, indent tolerance, record order, R4, one-annotation-per-task, the four separators) | suggested ticket: template/instruction parity sweep for pre-existing rules | 2026-09-08
```

## Minor 1 — SUBJECT GRAMMAR on a record whose `subject:` repeats

Decided by **suppression, stated in FIELD CARDINALITY** (which owns the
repeated-key case), with a back-pointer from SUBJECT GRAMMAR so a reader
arriving there does not have to reconstruct it. Added to FIELD CARDINALITY:

```
NO PER-VALUE RULE OF THIS CHECK RUNS ON A REPEATED KEY. Its
presence is satisfied and its cardinality is the finding, so
neither the non-empty requirement nor — for `subject:` — the
SUBJECT GRAMMAR below is evaluated on it: no executor has to
choose which of the two values to read, and the record yields
exactly ONE finding for that key. Only the repeated key is
exempted: a record blocked for a repeated `failure:` still
carries one `subject:`, whose grammar IS evaluated, and both
findings are reported.
```

Added to the end of SUBJECT GRAMMAR:

```
A record carrying more than one `- subject:` line is not examined
here at all — see FIELD CARDINALITY above, which is the whole of
this check's report about that record's subject.
```

Note this suppresses the **non-empty** requirement on the repeated key too, not
only the grammar. That branch was undecided for exactly the same reason (which
of the two values is the one that must be non-empty?), and leaving it open would
have reproduced the finding one clause over.

**Finding set on the review's input, now identical for every executor:** the RED
record carrying `subject: a::b` and `subject: c::d` yields exactly one check-9
finding — FIELD CARDINALITY on `subject:` — and no grammar finding, no emptiness
finding. Neither "one grammar finding", "two", nor "none by accident" is
reachable. `outcome:` and `failure:` on that same record are unaffected and are
still checked for presence, non-emptiness and cardinality.

## Minor 2 — multi-line values, decided in the FIELD definition

Placed in check 9's FIELD definition, immediately after the blank-line
transparency sentence, because that is where "what counts as a field" is settled
and FIELD CARDINALITY reads its answer:

```
A FIELD IS EXACTLY ONE LINE, and its value ends where that
line ends. A line inside the record's range that is NOT of
the form `- <key>: <value>` is not a field and is not a
continuation of the field above it: it contributes nothing
and is not itself an error — so a `failure:` excerpt whose
text is wrapped onto a second line records only what stands
on the `- failure:` line, and a second `- failure:` line
carrying the rest is a repeated key (see FIELD CARDINALITY
below), not a longer value. Record a multi-line excerpt
condensed onto the one line.
```

Boundary cases this decides, each stated rather than implied:

- A wrapped continuation line: not a field, contributes nothing, **not an
  error** — the check adds no new blocking condition here.
- A wrapped `failure:` whose first line is empty: the field's value is empty
  after trimming, which the existing non-empty rule already blocks. Decided, not
  new.
- Splitting a long excerpt across two `- failure:` lines: a repeated key → FIELD
  CARDINALITY. Deliberate, and the template now tells authors so.

## Self-review

- **Does each new sentence decide its own boundary case?** FIELD CARDINALITY's
  suppression names its own limit ("only the repeated key is exempted") and says
  what happens to the record's other keys. The one-line-field rule says what a
  non-field line is, that it is not an error, and what the two-line workaround
  becomes. Neither leaves a branch for an executor to fill in.
- **Is the template's comment block now complete?** For the rules this change
  introduced or tightened, yes — the sweep table's "this round" rows are all in
  parity. It is **not** a complete statement of every record rule: six
  pre-existing rows remain instruction-only, reported above rather than silently
  left.
- **YAML**: parses (`version: 2`, 8 artifacts).

## Dogfood re-sync and validation (round 2)

```
$ diff <(cd superpowers-bridge && find . -type f | sort) \
       <(cd openspec/schemas/superpowers-bridge && find . -type f | sort)
IDENTICAL FILE SETS (no removals needed)

$ cp -R superpowers-bridge openspec/schemas/
$ diff -r superpowers-bridge openspec/schemas/superpowers-bridge
SYNC IDENTICAL

$ openspec schema validate superpowers-bridge
Note: Schema commands are experimental and may change.
✓ Schema 'superpowers-bridge' is valid

$ openspec schemas
Available schemas:

  spec-driven
    Default OpenSpec workflow - proposal → specs → design → tasks
    Artifacts: proposal → specs → design → tasks

  superpowers-bridge (project)
    Spec-driven workflow integrated with Superpowers skills. Requirements:
    Superpowers plugin installed, providing skills: brainstorming,
    using-git-worktrees, subagent-driven-development,
    finishing-a-development-branch. Requires a subagent-capable platform
    (Claude Code, Codex, etc.) — this schema does not support runtimes without
    subagent support, because the alternative executor (executing-plans)
    dispatches no independent reviewer, losing the review rigor Superpowers
    brings. If your platform lacks subagent support, use spec-driven instead.
    Each artifact / apply step verifies its required skills before invoking and
    surfaces a clear error if any are missing. brainstorm → proposal → specs →
    tasks → plan → verify → retrospective. design is required (reorganizes raw
    brainstorm output into structured Context / Goals / Decisions / Risks /
    Migration; referenced by tasks and plan for implementation guidance). Apply
    phase uses git worktrees + subagent-driven-development (structural
    code-review dispatch; TDD applicability is declared per task in tasks.md,
    and tasks annotated applicable record RED/GREEN evidence there — verify's
    deterministic checks read the presence and structure of that evidence
    before archive, instruction-mediated rather than a mechanically enforced,
    non-bypassable gate).

    Artifacts: brainstorm → proposal → design → specs → tasks → plan → verify →
    retrospective
```

(Output above is verbatim, re-wrapped only where the terminal line exceeded this
document's width; no words changed.)

## Fixture regression, re-run after these edits

Minor 2 changes what counts as a field, so the scan was extended to look for
continuation lines as well as duplicate keys:

```
files scanned: 15 (13 fixtures + change tasks.md + template)
records with a repeated field key: 0
non-field / continuation lines inside a record: 0
=== ### in plans ===   (zero hits)
=== no-space checkbox ===   (zero hits)
```

**No fixture verdict changes.** Every field in every fixture record — and in the
template's own SHAPE block — is a single `- <key>: <value>` line with a unique
key, so neither the cardinality rule nor the one-line-field rule reaches any of
them. The fixtures README answer key needs no amendment.

## Files changed (round 2)

- `C:/Users/user/orca/openspec-schemas/.claude/worktrees/loosen-plan/superpowers-bridge/schema.yaml`
- `C:/Users/user/orca/openspec-schemas/.claude/worktrees/loosen-plan/superpowers-bridge/templates/tasks.md`

Cumulative diffstat for those two files against `6c4605e`
(`git diff --ignore-cr-at-eol --stat`): `schema.yaml` 102 changed,
`templates/tasks.md` 12 changed — 100 insertions, 14 deletions across both. No
`git add` / `commit` / `push` was run.

## Concerns (round 2)

1. **Six pre-existing instruction/template parity gaps remain**, listed in the
   sweep table and recorded above. None loosens the template below a check, but
   the recurrence pattern this round was called out for is visible in them too.
2. **The one-line-field rule makes a wrapped `failure:` silently lossy** — the
   continuation line is not an error, so a long excerpt split across lines
   records only its first line and nothing reports it. Making it an error would
   be a new blocking condition on input no fixture exercises; I chose the
   non-blocking reading and told authors, on both surfaces, to condense onto one
   line. Worth a maintainer's eye if excerpt fidelity matters more than that.
3. The round-1 concern stands: FIELD CARDINALITY blocks two `invocation:` lines
   in one record; it is now stated on both surfaces.

---

# Round 3 — the one-line-field rule reaches the instruction; bidirectional 3-surface sweep

Scope this round: `superpowers-bridge/schema.yaml` only (both fixes landed in the
`tasks` artifact instruction; the template already carried both rules).

## G1 (the reported finding) — one-line field rule stated in the `tasks` instruction

Added directly after the `- GREEN:` required-fields bullet, which is where the
instruction defines what a record's fields are:

```
A FIELD IS ONE LINE. Its value runs to the end of that line and no
further. A line that continues it by WRAPPING is not part of the
field and is not an error either — it is simply not read, so the
wrapped text stays visible in the file but is absent from the
record. Splitting the text across a second `- <same key>:` line
does not join them: that is a repeated key, which makes the record
malformed (see the cardinality rule with `invocation:` below).
What decides is the FORM, not the intent: a wrapped line that
itself happens to read `- <key>: <value>` is read as a field of
that key, never as continuation. Condense a long `failure:`
excerpt onto the one line.
```

Both halves an author needs are present: the wrap is lossy-but-legal, the second
`- <same key>:` line is a repeated key rather than a longer value.

**The boundary case I went looking for, and found.** "A continuation line is not
read" leaves open what happens when the wrapped line *itself* matches
`- <key>: <value>` — an excerpt wrapping onto `- expected: 3, got: undefined`
would silently become a field named `expected`. Check 9's text already decides
it by construction ("a line ... NOT of the form ... is not a field" ⇒ a line of
that form is one), but an author reading only the instruction would not have
known. The sentence "What decides is the FORM, not the intent" states it. No
check text changed — this is the same rule, made visible on the surface that
lacked it.

Cardinality is stated once, in the `invocation:` paragraph (round 1), and
pointed to from here rather than restated — one statement, one place to change.

## G2 — found only by the bidirectional scan: task-number uniqueness and the plan 1:1

Scanning template → instruction (the direction round 2 lacked) turned up a
second gap, and it is the more consequential of the two. `templates/tasks.md`'s
top comment block states that a task number is also the plan.md entry key and
that verify's check 12 rejects a repeat on either side. The `tasks` **instruction**
said neither: an author writing tasks.md from the instruction alone could number
two tasks `1.1` and be BLOCKed by a rule stated on no surface they read. That is
precisely the deferral-safety test failing, so it was fixed rather than
recorded:

```
before: - Each task MUST be a checkbox: `- [ ] X.Y Task description`

after:  - Each task MUST be a checkbox: `- [ ] X.Y Task description` —
          the number is separated from the `]` by whitespace, and NO task
          number repeats anywhere in this file. That number is also the
          key of the corresponding plan.md entry: verify compares the two
          collections in two stages, first rejecting a number carried by
          two task lines (or a key leading two plan entries), then
          requiring the two sets to be equal in both directions. A
          renumbering here is a renumbering there.
```

This also carries M2's whitespace rule (round 1) onto the instruction surface,
which the same scan showed was check-only there.

## The matrix — rule × surface, both directions

**I** = `tasks` artifact instruction (`schema.yaml`) · **C** = check text, checks
8–12 and R1–R4 · **T** = `templates/tasks.md` comment blocks.
`—` = absent. `(ex)` = present by worked example only, not stated as a rule.
A cell is a **gap** when a rule is absent from a surface it belongs on.

| # | Rule | I | C | T | Verdict |
|---|---|---|---|---|---|
| 1 | Annotation required on every task; the two forms | yes | yes | yes(ex) | ok |
| 2 | The four accepted separators (`—` `–` `-` `--`) | yes | yes | — | **D1 deferred** |
| 3 | Exactly ONE annotation line per task | — | yes | — | **D2 deferred** (reviewer's correction applied — see below) |
| 4 | `n/a` reason must be non-empty | yes | yes | yes(ex) | ok |
| 5 | Whether an `n/a` reason holds is review judgement (R3) | yes | yes | — | **D3 deferred** |
| 6 | Applicable task carries ≥1 RED and ≥1 GREEN | yes | yes | yes | ok |
| 7 | Required fields per record type | yes | yes | yes | ok |
| 8 | Fields nest one level under the record | yes (4 spaces) | yes (any greater) | yes(ex) | ok — I narrower than C |
| 9 | Blank lines transparent inside a record | — | yes | — | **D4 deferred** |
| 10 | Any greater indent accepted (formatter tolerance) | — | yes | — | **D5 deferred** |
| 11 | **A field is exactly one line; wrap not read, not an error** | **— → yes** | yes | yes | **G1 FIXED** |
| 12 | FIELD CARDINALITY — each key at most once per record | yes | yes | yes | ok (rounds 1–2) |
| 13 | Subject grammar: exactly one `::`, non-empty sides | yes | yes | yes | ok |
| 14 | Subject grammar: `::` counted non-overlapping (`a:::b` = one) | yes | yes | yes | ok (round 2) |
| 15 | No per-value rule runs on a repeated key (grammar + non-empty suppressed) | n/a | yes | n/a | **by design** — a finding-set rule for the check's executor; an author cannot act on it and the record blocks either way |
| 16 | Outcome tokens: GREEN `PASS`, RED any other uppercase token | yes | yes | yes | ok |
| 17 | Pairing by `subject:` value, never ordinal | yes | yes | yes | ok |
| 18 | Same-side uniqueness of `subject:` values | yes | yes | yes | ok |
| 19 | Re-running a test adds no further record | yes | yes | yes | ok |
| 20 | Several subjects per task; one RED + one GREEN each | yes | yes | yes | ok |
| 21 | Record ORDER carries no meaning | yes | yes (by construction) | — | **D6 deferred** |
| 22 | `invocation:` optional supporting evidence | yes | yes | yes | ok |
| 23 | A `TDD: n/a` task carrying records → R4, checks 9–11 do not apply | — | yes | — | **D7 deferred** |
| 24 | **Task numbers unique; they key plan.md entries 1:1 (two stages)** | **— → yes** | yes | yes | **G2 FIXED** |
| 25 | Task number follows the `]` after whitespace | **— → yes** (with #24) | yes | yes(ex) | **fixed with G2** |

**Gap count: 9** — 2 fixed (G1, G2, with #25 riding on G2), 7 deferred (D1–D7).
Row 15 is not counted as a gap: it is check-only by design, and I have said so
rather than leaving the cell blank.

### Deferral safety — the reviewer's test applied to each

*A deferral is safe only if no surface an author works from is looser than the
check that judges them.*

| | Direction | Safe? |
|---|---|---|
| D1 separators | T shows only the em dash; C accepts four | Safe — T is **narrower**; following it conforms |
| D2 one annotation per task | Absent from **both** author surfaces; C blocks "more than one" | **The one deferral that does not fully pass.** Mitigation: no surface invites a second annotation line, so reaching it takes a deliberate duplicate. Left deferred on the reviewer's explicit ruling, flagged here rather than silently |
| D3 R3 review judgement | Not a rejection rule (no check decides it) | Safe |
| D4 blank-line transparency | C is **looser** than the surfaces | Safe — it only means a hand-spaced record still conforms |
| D5 indent tolerance | C is **looser** (I says four spaces) | Safe — same direction |
| D6 record order | T silent, C order-independent | Safe — C is looser |
| D7 `n/a` carrying records → R4 | Non-blocking by design (a review judgement) | Safe |

```
[OUT_OF_SCOPE_DEFERRED] superpowers-bridge/schema.yaml + templates/tasks.md | seven pre-existing rule×surface gaps D1-D7 (separators, one-annotation-per-task, R3, blank-line transparency, indent tolerance, record order, R4-on-n/a) | suggested ticket: pre-existing surface-parity sweep; D2 needs a maintainer ruling because it is stated on neither author surface | 2026-09-08
```

### Row 3 — the classification the reviewer corrected

`schema.yaml:169-176` says the annotation "is written in exactly one of these two
**forms**", which selects a form; it does not say a task carries exactly one
annotation **line**. So the cardinality of the annotation is stated **only in
check 8** ("Zero matching lines, more than one … → BLOCK") — a **both-author-
surfaces** gap, not a template-side one. Round 2's table mis-filed it as
template-only; row 3 above carries the corrected reading so the next reader is
not misled.

## Self-review

- **Does the new instruction text decide its own boundary cases?** The wrap case,
  the second-`- <same key>:` case, and the wrapped-line-that-looks-like-a-field
  case are each stated. That third one is the instance of this family I went
  looking for inside my own fix, on the assumption that there would be one; it
  was real, and it is closed rather than reported.
- **Any cell I could not fill?** One class — row 15's I and T cells. It is not
  "unsure": a rule about which findings a check emits has no author-facing
  content, so the cell is `n/a` **by design**, stated as such rather than left
  blank.
- **Did the sweep run in both directions this time?** Yes, and the second
  direction (T → I, C → I) is what produced G2 and row 25. Round 2's I → T scan
  could not have seen either.
- **YAML**: parses (`version: 2`, 8 artifacts).

## Dogfood re-sync and validation (round 3)

```
$ diff <(cd superpowers-bridge && find . -type f | sort) \
       <(cd openspec/schemas/superpowers-bridge && find . -type f | sort)
IDENTICAL FILE SETS (no removals needed)

$ cp -R superpowers-bridge openspec/schemas/
$ diff -r superpowers-bridge openspec/schemas/superpowers-bridge
SYNC IDENTICAL

$ openspec schema validate superpowers-bridge
Note: Schema commands are experimental and may change.
✓ Schema 'superpowers-bridge' is valid

$ openspec schemas
Available schemas:

  spec-driven
    Default OpenSpec workflow - proposal → specs → design → tasks
    Artifacts: proposal → specs → design → tasks

  superpowers-bridge (project)
    Spec-driven workflow integrated with Superpowers skills. Requirements:
    Superpowers plugin installed, providing skills: brainstorming,
    using-git-worktrees, subagent-driven-development,
    finishing-a-development-branch. Requires a subagent-capable platform
    (Claude Code, Codex, etc.) — this schema does not support runtimes without
    subagent support, because the alternative executor (executing-plans)
    dispatches no independent reviewer, losing the review rigor Superpowers
    brings. If your platform lacks subagent support, use spec-driven instead.
    Each artifact / apply step verifies its required skills before invoking and
    surfaces a clear error if any are missing. brainstorm → proposal → specs →
    tasks → plan → verify → retrospective. design is required (reorganizes raw
    brainstorm output into structured Context / Goals / Decisions / Risks /
    Migration; referenced by tasks and plan for implementation guidance). Apply
    phase uses git worktrees + subagent-driven-development (structural
    code-review dispatch; TDD applicability is declared per task in tasks.md,
    and tasks annotated applicable record RED/GREEN evidence there — verify's
    deterministic checks read the presence and structure of that evidence
    before archive, instruction-mediated rather than a mechanically enforced,
    non-bypassable gate).

    Artifacts: brainstorm → proposal → design → specs → tasks → plan → verify →
    retrospective
```

(Verbatim; re-wrapped only where the terminal line exceeded this document's
width, no words changed.)

## Fixture regression, re-run (round 3)

```
files scanned: 15   (13 fixtures + change tasks.md + template)
records with a repeated field key: 0
non-field / continuation lines inside a record: 0
=== ### in plans ===         (zero hits)
=== no-space checkbox ===    (zero hits)
```

**No fixture verdict changes.** Both edits are author-facing instruction text;
no check's rule, inputs or verdict changed, and the scan confirms no fixture
contains input either new statement would newly reach. The fixtures README
answer key needs no amendment. (`f8-duplicate-task-number` still blocks on
check 12 exactly as its README row claims — G2 states that rule for authors, it
does not alter it.)

## Files changed (round 3)

- `C:/Users/user/orca/openspec-schemas/.claude/worktrees/loosen-plan/superpowers-bridge/schema.yaml`

`templates/tasks.md` was not touched this round — it already carried both rules.
Cumulative against `6c4605e` (`git diff --ignore-cr-at-eol --stat`):
`schema.yaml` 471 changed, `templates/tasks.md` 44 changed — 432 insertions,
83 deletions across the two. No `git add` / `commit` / `push` was run.

## Concerns (round 3)

1. **D2 is the deferral to watch.** "Exactly one `- TDD:` line per task" is
   stated on neither author surface while check 8 blocks on it. Deferred per the
   reviewer's ruling; it is the only one of the seven that fails the
   author-rejection test, and it wants a maintainer's yes/no rather than another
   round of mine.
2. **The instruction still says "indented four spaces" where the check accepts
   any greater indent** (row 8/D5). Harmless in direction, but it means a
   formatter-reindented file is conforming while reading as non-conforming to
   whoever compares it against the instruction.
3. Rounds 1 and 2 concerns stand: two `invocation:` lines block; a wrapped
   `failure:` is lossy by design — now stated on all three surfaces.
