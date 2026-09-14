# Code-plane gate — round 4 (contract-aware fallback reviewer)

Worktree: `C:/Users/user/orca/openspec-schemas/.claude/worktrees/loosen-plan`
Change: `fix-v2-blocking-defects`. Verified against the files, not against the fixer's report.
All diffs run with `--strip-trailing-cr` (this `diff` build does not accept `--ignore-cr-at-eol`; see Notes).

---

## G1 — the one-line-field rule on the `tasks` instruction

**ADDRESSED.**

`superpowers-bridge/schema.yaml:223-233` (new this round):

> A FIELD IS ONE LINE. Its value runs to the end of that line and no
> further. A line that continues it by WRAPPING is not part of the
> field and is not an error either — it is simply not read, so the
> wrapped text stays visible in the file but is absent from the
> record. Splitting the text across a second `- <same key>:` line
> does not join them: that is a repeated key, which makes the record
> malformed (see the cardinality rule with `invocation:` below).
> What decides is the FORM, not the intent: a wrapped line that
> itself happens to read `- <key>: <value>` is read as a field of
> that key, never as continuation. Condense a long `failure:`
> excerpt onto the one line.

Does it decide its own boundary case? **Yes** — the "FORM, not the intent" sentence is exactly the
case a wrap-vs-field rule leaves open, and it decides it in the direction the check reads.

Agreement with the check text, `schema.yaml:606-616` (check 9):

> A FIELD IS EXACTLY ONE LINE, and its value ends where that line ends. A line inside the record's
> range that is NOT of the form `- <key>: <value>` is not a field and is not a continuation of the
> field above it: it contributes nothing and is not itself an error — so a `failure:` excerpt whose
> text is wrapped onto a second line records only what stands on the `- failure:` line, and a second
> `- failure:` line carrying the rest is a repeated key (see FIELD CARDINALITY below), not a longer
> value.

The two are the same rule stated from the two ends (author side / reader side): a line matching
`- <key>: <value>` is a field; anything else contributes nothing and is not an error. **In substance
word for word.** Confirmed by re-derivation: my independent implementation of check 9 reads fields
by exactly this predicate and reproduces all thirteen fixture verdicts (below).

Third surface, `superpowers-bridge/templates/tasks.md:46-50`, is where G1 is *less* complete — see
**Fifth recurrence** below.

## G2 — task-number uniqueness and 1:1 keying on the `tasks` instruction

**ADDRESSED.**

`schema.yaml:161-168` (new this round):

> - Each task MUST be a checkbox: `- [ ] X.Y Task description` —
>   the number is separated from the `]` by whitespace, and NO task
>   number repeats anywhere in this file. That number is also the
>   key of the corresponding plan.md entry: verify compares the two
>   collections in two stages, first rejecting a number carried by
>   two task lines (or a key leading two plan entries), then
>   requiring the two sets to be equal in both directions. A
>   renumbering here is a renumbering there.

Boundary cases decided: the whitespace after `]` (check 12's `- [x]1.1 Foo` case, `schema.yaml:782-785`),
duplicates on *either* side, and both directions of the set comparison. Agrees with check 12
stage one (`schema.yaml:806-816`) and stage two (`:838-847`), and with `templates/tasks.md:2-7`,
which already carried the two-stage statement. The fixer also carried the same two-stage wording onto
`templates/plan.md:20-24` this round, so the plan-side author surface now says it too.

One imprecision, **nit, not a finding**: "NO task number repeats anywhere in this file" is broader
than the check, which collects numbers from task lines only. A literal reading would make the group
heading `## 1. Fixture group` collide with a task `- [x] 1` (the shape six of the fixtures actually
use). The direction is safe — the author surface is *stricter* than the check, so nobody is blocked
unexpectedly — but "on a task line" would be the accurate phrase.

---

## Matrix audit — five rows, every cell checked against the files

Columns as the fixer's matrix uses them: **I** = `tasks` artifact instruction, **C** = check text in
checks 8–12, **T** = `templates/tasks.md`. Criterion under test: *no author surface (I or T) may be
looser than the check that judges them.*

### Row 2 — the four accepted separators (D1, deferred)

| Cell | Verified at | Content |
|---|---|---|
| I | `schema.yaml:185-190` | "any one of `—` (em dash, canonical …), `–` (en dash), `-` (hyphen), or `--`. All four are accepted; nothing else is." |
| C | `schema.yaml:583-585` | "`<SEP>` is one of `—` … `–` … `-` … or `--`, and nothing else" |
| T | `templates/tasks.md:15` | `- TDD: n/a — <!-- reason … -->` — em dash only, no prose about alternatives |

**Deferral holds.** T is *narrower* than C: an author copying the template writes the canonical em
dash, which conforms. A narrower author surface never produces an unexplained block.

### Row 3 — exactly ONE annotation line per task (D2, deferred; reclassified this round)

| Cell | Verified at | Content |
|---|---|---|
| I | `schema.yaml:175-181` | "Every task MUST carry a TDD applicability annotation … written in exactly one of these **two forms**" — a form choice, not a cardinality. No sentence anywhere in the instruction says at most one such line. |
| C | `schema.yaml:576`, `:586-587` | "exactly one line belonging to it must match" … "Zero matching lines, **more than one**, any other form … → BLOCK" |
| T | `templates/tasks.md:20` | "每個任務都必須帶 TDD 適用性標註（縮排在 checkbox 底下）。" — an obligation to carry one, silent on carrying two |

**Deferral FAILS the criterion**, exactly as the fixer says. Both author surfaces are looser than the
check. The reclassification from "template-only gap" to "both-author-surfaces gap" is correct.
(Ruling taken elsewhere; not counted as a finding here — see **D2 characterisation**.)

### Row 9 — blank lines transparent inside a record (D4, deferred)

| Cell | Verified at | Content |
|---|---|---|
| I | grep of the whole `tasks` instruction | No mention. Cell `—` is accurate. |
| C | `schema.yaml:600-606` | "again blank lines are transparent: a blank line between two fields does NOT end the record. A record hand-formatted with spacing is conforming" |
| T | `templates/tasks.md` | No mention; the example block has no interior blank lines. |

**Deferral holds.** C is strictly *looser* than both author surfaces — it accepts a shape neither
surface teaches. Exercised positively by `f7-blank-spaced-record`, which my re-derivation confirms
does not block.

### Row 15 — "no per-value rule runs on a repeated key" (marked `n/a` for both author surfaces by design)

| Cell | Verified at | Content |
|---|---|---|
| I | — | Absent, and correctly so. |
| C | `schema.yaml:641-651` | "NO PER-VALUE RULE OF THIS CHECK RUNS ON A REPEATED KEY. Its presence is satisfied and its cardinality is the finding … the record yields exactly ONE finding for that key." |
| T | — | Absent. |

**`n/a` by design is correct, and stating it explicitly rather than leaving the cells blank is the
right call.** This rule governs the *check executor's finding set* — how many findings one malformed
record yields — not what an author must write. An author cannot act on it: the record blocks either
way, and the repair (write the key once) is already stated on both surfaces at
`schema.yaml:264-269` and `templates/tasks.md:46-48`. A blank cell here would have been
indistinguishable from an unexamined gap; the explicit `n/a` is what makes the row auditable.

### Row 25 — the task number follows the `]` after whitespace (fixed with G2)

| Cell | Verified at | Content |
|---|---|---|
| I | `schema.yaml:161-162` | "the number is separated from the `]` by whitespace" — new this round |
| C | `schema.yaml:782-785` | "AT LEAST ONE whitespace character must follow the `]`: with none, `- [x]1.1 Foo` carries NO task number — it is the same defect as a non-numeric token" |
| T | `templates/tasks.md:12-15`, `:53` | By example only (`- [ ] 1.1 <!-- … -->`) |

**In parity.** T-by-example is not looser: copying the template produces the whitespace. I now states
it in prose, closing the gap that existed before this round.

---

## D2 characterisation — **accurate**

All three surfaces, quoted in full:

1. **`tasks` instruction** — `superpowers-bridge/schema.yaml:175-181`:
   > TDD APPLICABILITY — tasks.md is the single source of truth.
   > Every task MUST carry a TDD applicability annotation. It is a
   > markdown list item nested under the task's own checkbox line —
   > indented two spaces from the `- [ ]` marker, so its own `- `
   > begins at column 3 — and it is written in exactly one of these
   > two forms (the leading `- ` IS part of the required form):

   "exactly one of these two forms" ranges over the **two forms**, not over the number of lines.
   The instruction's own SELF-REVIEW (`:305-313`) asks only "is any task **missing** its TDD
   annotation, and does any `TDD: n/a` lack a reason after the separator?" — the duplicate case is
   not among the two conditions it names. I grepped the whole instruction for any cardinality
   statement about the annotation: there is none.

2. **`templates/tasks.md:20`**:
   > 每個任務都必須帶 TDD 適用性標註（縮排在 checkbox 底下）。

   ("Every task must carry a TDD applicability annotation, indented under the checkbox.") An
   obligation to carry one. Nothing about a second. The template's cardinality prose at `:46-48`
   is scoped to **fields inside a record** ("同一筆紀錄裡，每個欄位鍵最多只能出現一次"), not to
   the `- TDD:` annotation line.

3. **Check 8** — `schema.yaml:576` and `:586-587`:
   > For EVERY task line in tasks.md, **exactly one** line belonging to it must match …
   > Zero matching lines, **more than one**, any other form, or an `n/a` whose reason is empty
   > after trimming → BLOCK.

Check 8 does block on more than one. Neither author surface states it. **The fixer's
characterisation is accurate in every particular**, including its own assessment that this is the
one deferral failing its test, and its mitigation ("no surface invites a second annotation line, so
reaching it takes a deliberate duplicate") is a fair statement of the residual risk rather than a
minimisation of it. Per the brief, not counted as a finding.

---

## Fifth recurrence — **FOUND (Minor, non-blocking)**

The family is real and it recurred a fifth time: **G1's boundary sentence went onto the instruction
this round and not onto the template.**

- Instruction, `schema.yaml:230-232` (new this round): "What decides is the FORM, not the intent: a
  wrapped line that itself happens to read `- <key>: <value>` is read as a field of that key, never
  as continuation."
- Template, `templates/tasks.md:49-50`: "另外，**一個欄位就是一行**：值寫到行尾為止，換行續寫的那行
  **不算這個欄位的內容（也不算錯，只是不被讀入）**。" — "the wrapped line … is not an error either,
  just not read." Stated without the qualifier, as an absolute.

The fixer's matrix row 11 marks T = "yes" for this rule. That is the *unqualified* version of the
rule; the qualifier the instruction gained this round is not on the template.

**Why it is Minor rather than a failed deferral.** The template's preceding paragraph
(`templates/tasks.md:46-48`) already covers the only case where the check actually blocks:
"同一筆紀錄裡，**每個欄位鍵最多只能出現一次** … 同一個鍵寫兩行就是壞掉的紀錄，verify 的 check 9 會
BLOCK." So a template-only author who wraps a `failure:` excerpt onto a second `- failure:` line has
been told, one paragraph earlier, that it blocks. The two sentences must be read together and in
order; the instruction supplies an explicit tiebreak that the template leaves to the reader. That is
an ambiguity, not a surface looser than its check — **no author is blocked with no surface telling
them**, which is the criterion. Recommended (not required for this gate): append the FORM-decides
clause to `templates/tasks.md:49-50`, or reorder so the cardinality sentence follows the one-line
sentence.

Two further one-surface rules I checked and cleared, listed so the sweep is auditable:

- "Do NOT carry task-level state markers into plan.md" (`schema.yaml:389-394`, new this round) is
  absent from `templates/plan.md`. **No check judges it** — check 7 reads `tasks.md` and nothing else
  — so no author surface is looser than any check. Guidance asymmetry only.
- "`###` or deeper is a sub-heading INSIDE an entry, not an entry" (`schema.yaml:794-798`) is
  check-only. The rule is *permissive* — it prevents a false BLOCK — so its absence from the author
  surfaces cannot block anyone.

---

## Regression — thirteen fixtures re-derived independently

I implemented checks 8–12 from the check text alone (field predicate, blank-line transparency,
any-greater-indent nesting, non-overlapping `::` scan, two-stage uniqueness-then-set on both check 11
and check 12, `##`-only heading collection, whitespace-after-`]`) and ran it over every fixture. The
fixtures README's first table is the answer key.

| Fixture | README expects | Re-derived | Match |
|---|---|---|---|
| f1-missing-annotation | check 8 BLOCK | check 8: task line 12 has NO TDD annotation | ✔ |
| f2-missing-green | check 9 BLOCK + check 11 stage two | check 9 no GREEN; check 11.2 RED-only `test/auth.test.js::rejects empty email` | ✔ |
| f3-pass-marker-on-red | check 10 BLOCK | check 10: RED outcome `'PASS'` | ✔ |
| f4-subject-mismatch | check 11 BLOCK | check 11.2 both directions (`auth.test.js…` RED-only, `signup.test.js…` GREEN-only) | ✔ |
| f5-key-set-mismatch | check 12 BLOCK | check 12.2: task `'3'` no entry, plan key `'9'` no task | ✔ |
| f6-syntaxerror-red | NOT blocked (R1 only) | NO BLOCK | ✔ |
| f7-blank-spaced-record | NOT blocked | NO BLOCK | ✔ |
| f8-duplicate-task-number | check 12 BLOCK naming `1.1` | check 12.1: tasks.md key `'1.1'` more than once | ✔ |
| f9-duplicate-plan-key | check 12 BLOCK naming `2.3` | check 12.1: plan.md key `'2.3'` more than once | ✔ |
| f10-subject-without-separator | check 9 BLOCK | check 9: bad subject `'rejects empty email'` on both records | ✔ |
| f11-duplicate-subject-one-side | check 11 BLOCK | check 11.1: value more than once among RED | ✔ |
| f12-two-subjects-paired | NOT blocked | NO BLOCK | ✔ |
| f13-deferred-task-in-tasks | not BLOCK-discriminating; check 7 finds **1** deferred task in `tasks.md` | NO BLOCK from 8–12; `[~] 1` is the single deferred task line in `tasks.md`, and `plan.md` carries no `[~]` line | ✔ |

**13/13 verdicts unchanged.** No blocking consequence.

Coverage observation, **deferred, not a finding**: three of the sub-rules this change tightened have
**no fixture** — I grepped for each. No fixture `plan.md` contains a `###` heading; no fixture task
line omits the whitespace after `]`; no fixture record carries a repeated field key. Those three
rules are therefore verified by reading only, while the other ten are verified by a re-runnable
asset. The fixture set is this change's own deliverable (tasks 1.1–1.4) and rounds 1–3 accepted it,
so I record this as an evidence-adequacy observation for the maintainer rather than a finding of this
round.

## Self-application — checks 8–12 against this change's own artifacts

`openspec/changes/fix-v2-blocking-defects/tasks.md` + `plan.md`, same re-derivation:

- Task numbers: `1.1 1.2 1.3 1.4 2.1 2.2 2.3 2.4 3.1 3.2 4.1 4.2 5.1 5.2 5.3` (15, no repeat).
- Plan entry keys: identical set, no repeat. The `## Self-review` heading is correctly not collected.
- 3 tasks `TDD: applicable`, 12 `TDD: n/a` with reasons; 6 RED and 6 GREEN records, every subject
  paired, all outcomes conforming.
- **NO BLOCK.**

Control: `openspec/changes/archive/2026-09-04-loosen-plan/` (27 tasks / 27 entry keys) — **NO BLOCK**,
so the tightened wording does not retroactively block the already-archived change either.

## Toolchain

- `diff -r --strip-trailing-cr superpowers-bridge openspec/schemas/superpowers-bridge` → **empty**
  (dogfood copy in sync). Note: this environment's `diff` rejects `--ignore-cr-at-eol`
  (`diff: unknown option`); `--strip-trailing-cr` is the equivalent this build provides, and I used
  it on every diff.
- `openspec schema validate superpowers-bridge` → `✓ Schema 'superpowers-bridge' is valid`
- `openspec schemas` → `superpowers-bridge (project)` listed, 8 artifacts, brainstorm → … → retrospective.

## New breakage

**None.** The round-4 edits are additive prose on the `tasks` instruction plus the "more than once"
message wording and the R1 `INDETERMINATE` clarification; nothing narrows a previously-conforming
input. Every fixture verdict and both self-applications are unchanged.

## Scope

Read-only throughout: no working-tree, index, HEAD or branch mutation; no `git add` / `commit` /
`push`. The scratch re-derivation script lives outside the repo, in the session scratchpad.

---

Findings this round: **one Minor** (fifth recurrence, template missing G1's FORM-decides qualifier),
one nit ("anywhere in this file"), one deferred coverage observation. Nothing at or above the
blocking severity for this plane.

✅ Ready
