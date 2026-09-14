# Code-plane fallback review — `fix-v2-blocking-defects` (`6c4605e..HEAD` + working tree)

Reviewer: contract-aware fallback (primary reviewer's quota exhausted). Primary file under
review: `superpowers-bridge/schema.yaml`, read as an algorithm.

## Summary

The change closes five defects of one shape — a check whose title claimed more than its steps
decided — in the twelve hand-executed verify checks of `superpowers-bridge/schema.yaml`.
Check 12 becomes two stages (per-side duplicate detection, then bidirectional set equality),
which is genuinely a bijection: uniqueness on each side plus set equality is exactly 1:1, and
the text is explicit that stage one does not short-circuit, so a duplicate and a set difference
in the same input yield both findings in one run. Checks 9–11 move the pairing unit from the
task to the `subject:` value: check 9 gains a subject grammar (after trimming, exactly one `::`
counted non-overlappingly, non-empty on both sides, nothing further constrained — so `a:::b`
holds one separator and conforms, `a::b::c` holds two and does not), check 10 is quantified over
every record rather than "the" record, and check 11 becomes uniqueness-per-side then a
two-direction set comparison keyed on subject. Ordinal pairing is explicitly forbidden, which is
the right call: it is the only rule under which inserting a record silently re-pairs the rest.
Check 7's carrier moves from `plan.md` (where a conforming v2 plan can never carry a `[~]` row,
so the check was dead) to `tasks.md`, with a `- [~]`-at-line-start definition that excludes
`[~]` appearing in prose, plus an absent-`tasks.md` branch that records "undetermined" rather
than "no deferred tasks". The FRESHNESS input map moves with it. I re-executed checks 8–12
mechanically against all six new fixtures (f8–f13) and against this change's own artifacts;
every fixture produces exactly the verdict its README row claims, including f12 as a positive
control that must not block. The three preserved-behaviour claims hold under word-diff against
`6c4605e`: the non-numeric-token branch and the absent-`plan.md` branch of check 12 are
byte-identical, and check 7's enumeration and gap-routing paragraphs are unchanged apart from
the carrier rename and one added "every deferred task, not merely the first" sentence. The four
RED/GREEN evidence records cite `git show 22c15cf:superpowers-bridge/schema.yaml` line ranges
483–521 and 523–556; both resolve exactly to the pre-edit checks 9–11 and check 12 blocks, so
the baselines are re-runnable. CI is safe: `superpowers-bridge/README.md:520` is
`| v2 | \`1.3.1\` | \`v5.1.0\` | 2026-09-01 |`, which satisfies `grep -E '^\| v2 \| \`'` and
yields `1.3.1` / `v5.1.0` from `awk -F'\`'` fields 2 and 4.

What I found is not in the five defects, which are closed. It is three residues: one record-level
cardinality the new multi-record shape newly exposes, and two author-facing surfaces that were
not brought along with the checks they feed.

## Findings

### Critical

None.

### Important

**I1. `superpowers-bridge/schema.yaml:568` and `:635` — a record carrying two `subject:` fields
is undecided, and two executors reach opposite verdicts.**

Check 9 defines a FIELD as "a line written `- <key>: <value>`" in the record's range and states
no cardinality; it requires the fields `subject:`, `outcome:`, `failure:` to be *present* and
non-empty. Check 11 then says "collect the trimmed `subject:` value of every `- RED:` record" —
singular, presupposing one. On this input:

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

check 9 passes (both values satisfy the grammar, every required field present and non-empty),
and check 11 gives `✓` to an executor that takes the first `subject:` and `⛔ BLOCK` to one that
takes both (`c::d` RED with no GREEN). Nothing in the text picks. The same hole exists for a
repeated `outcome:` under check 10 and a repeated `failure:` under check 9.

Why it matters here specifically: this is the same defect class the change exists to close — an
unstated cardinality that the surrounding prose silently presumes — and the change *increases*
its likelihood, because "a task may carry several subjects" invites exactly the mis-formatting
of stacking two `subject:` lines under one record instead of writing two records. Check 8
already handles the analogous case explicitly ("Zero matching lines, more than one … → BLOCK"),
so the omission reads as an oversight rather than a decision.

Fix: one sentence in check 9, alongside the required-fields sentence — *a record carrying more
than one line with the same field key is malformed → BLOCK, naming the key and the record* —
and, in check 11's collection paragraph, *a record whose `subject:` field is not unique
contributes nothing to either list; its malformation is check 9's finding.* That mirrors the
carve-out already added for a record with no `subject:` at all.

**I2. `superpowers-bridge/schema.yaml:378` — the plan instruction's own SELF-REVIEW still tells
the author to check set equality, which check 12 no longer accepts as sufficient.**

Item 1 reads "does the set of entry keys equal the set of tasks.md task numbers exactly, in both
directions?". The change updated STRUCTURE item 2 above it (`:320-338`) to the two-condition
form, and updated `templates/plan.md`'s and `templates/tasks.md`'s comments, but this checklist
was left at the pre-change framing. An author who passes it can still be blocked by stage one —
the instruction is looser than the check it feeds, in the direction that produces work the
checker rejects. The whole point of a self-review item is to be the same question the gate asks.

Fix: "does every entry key occur exactly once, does every tasks.md task number occur exactly
once, and are the two sets equal in both directions?"

**I3. `superpowers-bridge/schema.yaml:359-370` — this change's own plan-contract spec adds
"plan.md SHALL NOT carry task-level state markers (deferral and the like)", and no bridge-owned
surface tells a plan author that.**

`openspec/changes/fix-v2-blocking-defects/specs/plan-contract/spec.md` introduces that SHALL NOT
(it is not in the canonical spec), and check 7's new rationale leans on it explicitly: "a `[~]`
marker sitting in any other file — including a non-conforming plan that carries task rows the
Plan Contract forbids it to carry — is outside this check's inputs". But the `plan` artifact
instruction's WHAT NOT TO WRITE section forbids micro-steps, execution sequences and a second
copy of the evidence, and says nothing about state markers. So an author may write `[~]` rows in
plan.md, no instruction discourages it, no check fires, and the deferral is silently invisible —
which is the failure mode check 7 was just repaired to prevent, relocated one file over. A SHALL
NOT that no surface communicates and no check enforces is a claim, not a control.

Fix: one clause in WHAT NOT TO WRITE — *do not carry task-level state markers (`[~]` deferral
and the like); tasks.md is their carrier and verify's deferral check reads only tasks.md* —
which also makes check 7's cross-reference to "the Plan Contract" resolvable from within the
bundle.

### Minor

**M1. `:707-715`** — check 12 collects "each `##` heading in plan.md whose text begins with such
a token". Whether a `### 1.1 — …` sub-heading is a "`##` heading" is not stated. Under the
markdown-h2 reading it is not collected; under a literal prefix reading it is, and stage one then
BLOCKs the plan for a duplicate `1.1`. Inherited text, unchanged by this change, and no template
or fixture uses `###` inside an entry — but stage one is what makes the ambiguity
verdict-changing, so it is worth one clause ("an `##` heading, not `###` or deeper").

**M2. `:702-704`** — "the token IMMEDIATELY after the `]` of its checkbox and the whitespace
following it" presupposes whitespace exists. `- [x]1.1 Foo` is undecided: no whitespace to skip,
so either the token is `1.1` or there is no token and the line "carries no task number → BLOCK".

**M3. `:730-731` and check 11's stage-one message (`:651-653`)** — the message templates say "occurs
twice" while the rules fire on "more than one" / "appearing more than once". A key repeated three
times is reported with a count the input does not have. Wording only; the verdict is unaffected.

**M4. `openspec/changes/fix-v2-blocking-defects/tasks.md:97`** — task 2.2's third RED records
`outcome: INDETERMINATE` for the f12 positive control. It conforms to check 10 (uppercase A–Z,
not `PASS`), and the reasoning is sound (the pre-edit wording could not decide the case, so the
target property was not satisfied). Flagging only so the R1 review judgement records that an
"undecidable under the old text" RED is deliberate and not a harness-error analogue.

## Boundary-condition table

| Case | Sentence that decides it |
|---|---|
| `tasks.md` absent | `:494-508` — recorded "tasks.md absent — deferral state undetermined", never "no deferred tasks"; does not block on that basis; check 12 and the PRECHECK are named as the surfaces that do catch it. Verified: with no task numbers, check 12 blocks in every sub-case (plan with entries → extra keys; plan with none → "no collectable entry key"; plan absent → "no plan.md") |
| `plan.md` absent | `:717-721` — check fails, reported as "plan.md absent — no entry keys to compare", not as a set difference. Unchanged from `6c4605e` |
| Empty collection (zero tasks) | Decided, by derivation: checks 8–11 vacuous (`:504-506` says so explicitly), check 12 → empty task set against a non-empty plan set, or "no collectable entry key" if the plan is empty too. Blocks either way |
| Field value that trims to empty | `:602-606` — "a required field whose value is empty after trimming … → BLOCK". An empty `subject:` additionally fails the grammar, and `:607` says every finding is reported |
| Key repeated three times, not twice | `:725-729` ("carried by more than one task line") and `:648-651` ("appearing more than once"). Decided; only the example message's "twice" is imprecise (M3) |
| Duplicate on both sides at once | `:723-731` — "examine each side INDEPENDENTLY … Report EVERY repeated key by name and by the side it repeats on" |
| Record missing a required field | Check 9 blocks (`:602-606`); for check 11 specifically, `:640-643` (working-tree edit) — "A record carrying no `subject:` field at all contributes nothing to either list; its absence is check 9's finding" |
| Record with a *repeated* field key | **Undecided** — see I1 |
| Separator appearing twice (`a:::b`) | `:589-594` and `:222-227` — counted left to right and consumed, so `a:::b` holds ONE and conforms; `a::b::c` holds two and does not. Confirmed by execution |
| Stage-one failure ending the check | Explicitly decided for both two-stage checks: `:672-682` (check 11) and `:733-742` (check 12) — stage one does not short-circuit, both stages report |
| `[~]` inside a title or record field | `:466-470` — only a line whose first non-space characters are `- [~]` counts |
| `TDD: n/a` task carrying records | `:598-601` — checks 9–11 do not apply; R4 is what reports it |
| `###` heading in plan.md | **Undecided** — see M1 |
| No whitespace after `]` | **Undecided** — see M2 |

## Self-application

Checks 8–12 executed by hand (script-mediated, implementing the written steps literally) against
`openspec/changes/fix-v2-blocking-defects/tasks.md` and `plan.md`:

| Check | Verdict |
|---|---|
| 8 — annotation present and well-formed | ✓ 15/15 task lines carry exactly one conforming `- TDD:` line (4 `applicable`, 11 `n/a` with a non-empty reason after an em dash) |
| 9 — records, fields, subject grammar | ✓ tasks 2.1–2.3 carry 4 + 6 + 2 records; every RED has `subject:`/`outcome:`/`failure:`, every GREEN has `subject:`/`outcome:`; all 12 subject values hold exactly one `::` with non-empty sides |
| 10 — outcome markers | ✓ every GREEN `PASS`; REDs are `FAIL` ×3 and `INDETERMINATE` ×1, all uppercase A–Z tokens other than `PASS` |
| 11 — pairing by subject | ✓ stage one: no repeated value on either side in any task (2.1 has 2 subjects, 2.2 has 3, 2.3 has 1). Stage two: both set differences empty in every task |
| 12 — 1:1 keys | ✓ stage one: 15 task numbers, each once; 15 plan entry keys, each once (`## Self-review` correctly not collected). Stage two: both differences empty |

Also run: check 7 finds zero `- [~]` lines, so §7 may be blank and the check does not block.
Check 2 finds one unchecked task, `5.3`, which is the D5 precondition re-verification the plan
schedules for immediately before verify.md is written — expected at this point, and it must be
ticked before verify.

**The change does not block itself**, and the three findings above do not change that: I1 needs a
record with a duplicated field key (none exists here), I2 and I3 are author-facing surfaces, not
checks.

## Also confirmed

- `.github/workflows/version-check.yml:44` greps `^\| v2 \| \`` and `README.md:520` matches; the
  `awk -F'\`'` fields 2 and 4 resolve to `1.3.1` and `v5.1.0`. CI grep intact.
- The dogfood copy is in sync: `superpowers-bridge/schema.yaml` and
  `openspec/schemas/superpowers-bridge/schema.yaml` are byte-identical, including the
  working-tree-only edit at `:640-643`. `schema.yaml` parses, `version: 2`, 8 artifacts.
- No residual single-pair wording anywhere in the bundle: `a RED record and a GREEN record`,
  `identical to RED's`, `RED subject equals`, `task-number set equals` all return zero hits
  across `schema.yaml`, both READMEs and all templates.
- `README.zh-TW.md` is at parity with `README.md` on every changed passage.
- `openspec/specs/plan-contract/spec.md` and `.../tdd-evidence-contract/spec.md` are not yet
  synced with this change's deltas while `tdd-claim-accuracy` is (task 4.1 edited the canonical
  file deliberately). Expected — verify check 3 should report the first two as "needs sync" and
  archive performs it. Not a finding, noted so the asymmetry is not mistaken for one.

⛔ Blocked
