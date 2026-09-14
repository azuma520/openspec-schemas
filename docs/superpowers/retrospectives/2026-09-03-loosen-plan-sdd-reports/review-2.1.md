# Review — task 2.1 (check 12 two-stage 1:1)

Reviewer: task-scoped gate. Base 22c15cf, working-tree diff over
`superpowers-bridge/schema.yaml` and `openspec/changes/fix-v2-blocking-defects/tasks.md`.
Read-only review; nothing in the working tree, index, HEAD or branch state was mutated.

### Spec Compliance

✅ **Spec compliant**, with one Important defect in the new text (an undecided branch, below) that is a wording gap rather than a missed requirement.

Verified point by point, against the fixtures and the schema text rather than the report:

- **Pre-existing branches present, unaltered, in order** — `superpowers-bridge/schema.yaml:534-554`: non-numeric-first-token defect (`:536-539`), entry-key collection (`:540-548`), absent plan.md (`:550-554`), then STAGE ONE (`:556-575`), then STAGE TWO with the no-collectable-entry-key clause still inside it (`:577-586`). Every one of those lines is context (unmarked) in the diff — no removal touches them.
- **Placement per design Open Question 1** — duplicate detection sits after the absent-plan.md branch and before the set comparison. ✅
- **f8** (`fixtures/f8-duplicate-task-number/`): tasks.md carries `- [x] 1.1 Add email validation` and `- [x] 1.1 Update the README install section`; plan.md carries one `## 1.1 —`. Walking `:556-563` yields a task number carried by two task lines → BLOCK, reported by name and side. Report's claimed verdict is the verdict the text yields. ✅
- **f9**: plan.md carries `## 2.3 — email validation (backend)` and `## 2.3 — email validation (frontend)`; tasks.md one `2.3`. `:564-566` ("Two entries keyed alike are duplicates whether or not their titles differ") decides this explicitly → BLOCK naming `2.3` in plan.md. ✅
- **f7** (`[1, 2]` vs `## 1`, `## 2`): no repeat, sets equal, plan present, every task line numbered → no finding from check 12. ✅
- **f5** (`[1,2,3]` vs `## 1`, `## 2`, `## 9`): stage one silent; stage two's message text is character-for-character the pre-edit message apart from the `STAGE TWO — SET EQUALITY. Now reduce both collections to sets.` lead-in and one re-wrap. ✅
- **Messages distinguishable by a reader** — `:562-563` gives literal templates ("`1.1` occurs twice in tasks.md"); `:578-579` says "a task number with no entry key" / "an entry key matching no task number". A reader cannot confuse them. ✅
- **`1:1` survives nowhere the logic does not deliver** — `grep -n "1:1"` returns 7 hits: `:285`, `:298` (the ruled-in `plan` instruction) and `:531, 539, 573, 582, 588`, all inside check 12 and all now backed by the two stages. ✅
- **Ruling edit confined to the one item** — the first hunk's added and removed lines all fall inside `plan` structure item 2; the Delivers / Acceptance / Blocked by / Interfaces bullets below are context. The new wording is one-to-one with the two stages: "no key repeats on either side" ↔ STAGE ONE, "the set of entry keys and the set of task numbers are identical in both directions" ↔ STAGE TWO, and "in both of its stages" is accurate — stage one collects entry keys by the same leading-key heading rule. ✅
- **tasks.md 2.1** — ticked `[x]`; two RED/GREEN pairs; both pairs' `subject:` values identical character for character between RED and GREEN (verified with `cat -A`); indentation matches the normative SHAPE at `schema.yaml:226-238` (two-space `- RED:`, four-space fields, literal keys); each `subject:` is `<fixture dir>::<expected verdict>` with exactly one `::` and non-empty sides; both `failure:` fields state expected verdict then actual verdict. ✅
- **No extra files, no P2, schema major untouched** — the diff is the two files; `version: 2` and VERSION are outside it.

⚠️ **Cannot verify from the diff alone:**

1. **That the RED walk happened before the edit.** What I can confirm is that the reasoning is sound *against the actual pre-edit wording*: the diff's removed lines are exactly the three sentences the report quotes, that enumeration contains no duplicate condition, and `{1.1,1.1}` vs `{1.1}` and `{2.3}` vs `{2.3,2.3}` both collapse to no difference — so PASS is the correct pre-edit verdict and the RED is reproducible by anyone from the removed lines. The ordering claim itself rests on the report.
2. **A provenance mismatch worth a sentence**: the report cites the pre-edit text as `git show HEAD:superpowers-bridge/schema.yaml` "as of HEAD (`5aa19bf`)", but this review's base is `22c15cf` — and the f8/f9 fixtures themselves landed in task 1.1, i.e. after `5aa19bf`. The quoted sentences match `22c15cf`'s removed lines, so the walk is against the right text; the commit id in the record is stale. Minor, but a record that names the wrong baseline is a record a later reader cannot re-run.
3. That no file outside the two was written (I did not re-run git per instruction).

### Strengths

- The closing paragraph at `:588-594` is the part that actually answers the standard this change is held to: it states that unique-per-side plus set-equality *is* the bijection, and then bounds the claim ("that an entry's contract text actually describes its task is review judgement, never this check"). That is the title-vs-steps discipline applied to itself, not just asserted.
- `:571-575` explains *why* stage one must precede stage two ("a set comparison cannot see a duplicate at all — the set absorbs it"). An executor who understands that will not reorder the stages when paraphrasing.
- The f9 case was pre-empted in the text (`:564-566`), not left to the reader — that is design Open Question 2 settled in the instruction rather than in a design doc nobody executing the check will read.
- The `plan`-instruction fix genuinely repaired an overclaim rather than restating one: "the entry-key **set** is readable" → "the **keys** are readable" removes the set reduction from the *reason for the rule*, which is where the conflation was actually load-bearing.

### Issues

#### Critical (Must Fix)

None.

#### Important (Should Fix)

**1. `schema.yaml:556-586` — the text does not decide whether a stage-one BLOCK terminates the check, and the evidence relies on the reading it does not state.**

Two readings are equally available to an executor:

- *Short-circuit*: `:562` says "and BLOCK", so the check ends there.
- *Both stages run*: `:583-586` folds the duplicate into stage two's terminal enumeration — "A repeated key on either side, either difference non-empty, a task line carrying no task number, no collectable entry key, or no plan.md → BLOCK" — which reads as a union of conditions collected across the whole check, i.e. stage two still evaluates and reports.

For a fixture with a duplicate **and** a set difference (tasks `[1.1, 1.1, 2]` against plan `## 1.1`), one executor reports one finding and another reports two. Neither is wrong under the text, which is exactly the property a deterministic check must not have.

Why it matters beyond the abstract case: the GREEN record in `openspec/changes/fix-v2-blocking-defects/tasks.md` asserts the short-circuit as observed behaviour — "BLOCKs **before stage two reduces anything to a set**" — and the report's §3 states "f8/f9 block through stage one and never reach stage two". That is a claim about behaviour the instruction never specifies. It does not change the f8/f9 verdicts (both fixtures have equal *sets*, so stage two would find nothing either way), which is why this is Important and not Critical.

Fix: one clause. Either at the end of `:562-563` — "and BLOCK; a stage-one failure ends this check, so stage two is not evaluated" — or, if both stages are meant to report, say so there and drop the ambiguity from `:583`. Then align the GREEN `invocation:` wording with whichever is chosen.

#### Minor (Nice to Have)

**2. `schema.yaml:562-563` — the literal message template does not cover a key repeated three or more times.** "Report EVERY repeated key by name and by the side it repeats on — "`1.1` occurs twice in tasks.md"". The *verdict* is decided by `:558-561` ("carried by more than one task line"), so nothing is undecided about blocking; only the message string breaks, since "occurs twice" would be false for a triple. Fix: "…by the side it repeats on, with the number of occurrences — "`1.1` occurs 3 times in tasks.md"".

**3. Message-specification asymmetry between the stages.** Stage one gives quoted literal templates; stage two gives only a description of what to report. Pre-existing on stage two's side and not a regression, but the acceptance criterion "the two failures get distinct messages" is now carried by one literal and one paraphrase. Worth a literal example on stage two when 3.1/3.2 mirror this text.

**4. The repair distinction is now stated twice, in `plan` item 2 (`:290-292`) and in check 12 (`:568-571`).** Both spellings are near-identical prose. This is defensible — one is the author-facing surface, the other the checker — and the binding spec sentence arguably requires both, but it is two copies to keep in sync, and 3.1/3.2 will add more. Flagging so the duplication is deliberate rather than accidental.

**5. `schema.yaml:578` is 72 columns where the surrounding block holds at ≤70.** A consequence of the re-wrap; cosmetic.

On growth: check 12 went from ~34 to ~64 lines for one new stage. Roughly half the new text is rationale rather than steps, which matches the register of the rest of this instruction (the `tasks` EVIDENCE segment and the FRESHNESS block are written the same way), so I do not read it as disproportionate.

### Assessment

**Task quality:** Needs fixes

**Reasoning:** Every acceptance bullet is satisfied and all four fixture verdicts are the ones the new text actually yields — but a deterministic check must not leave an executor two readings, and `:562` vs `:583` does exactly that for the duplicate-plus-difference case, with the GREEN record asserting the unstated reading as fact. One clause closes it; the rest is Minor.
