# Final whole-branch review — `fix-v2-blocking-defects`

Range reviewed: `6c4605e..HEAD` (`22c15cf`, `cffe99a`, `787b14c`) plus the uncommitted
working tree, read with `--ignore-cr-at-eol`. Read-only: no file, index, HEAD or branch
state was modified.

## Overall verdict

**⛔ Needs revision** — no Critical findings, five Important ones. The change does close
all five P1 defects, passes its own checks 8–12, and does not break CI. What it does not
do is finish the sweep it set out to do: the same overclaim it exists to repair survives
in a seventh surface nobody audited (`templates/plan.md`), the single-pair cardinality
survives in both bridge READMEs' apply section, one fixture silently stopped isolating,
the change's own task list misreports four completed tasks as open, and the permanent
archive record (E3) misdescribes the defect it records. Each is a one-or-two-line fix;
none requires re-opening a design decision.

---

## 1. Cross-surface coherence — claim by claim, surface by surface

Six surfaces were named in the brief. I checked seven — `templates/plan.md` is a
bridge-owned normative surface that states the check-12 contract and was in nobody's
task list.

| Load-bearing claim | schema checks | schema `plan`/`tasks` instr. | templates/verify.md | templates/tasks.md | templates/plan.md | README.md | README.zh-TW.md |
|---|---|---|---|---|---|---|---|
| check 12 = two stages, dupes then sets | ✅ `:694-771` | ✅ `:322-337` | ✅ `:152,176-193` | ✅ `:3-7` | ⛔ **only set equality** `:21` | ✅ `:397` | ✅ `:397` |
| stage one does **not** short-circuit | ✅ `:665-675`, `:732-741` | — | ✅ `:157-160,188-190` | — | — | ✅ `:397` | ✅ `:397` |
| `::` grammar (exactly one, both sides non-empty, nothing further) | ✅ `:585-600` | ✅ `:207-217` | ✅ `:152` (title) | ✅ `:31-33` | — | ✅ `:397` | ✅ `:397` |
| per-subject uniqueness + one RED/one GREEN per subject | ✅ `:625-681` | ✅ `:219-230` | ✅ `:152,156-162` | ✅ `:25-30` | — | ✅ `:397` | ✅ `:397` |
| a task MAY carry several subjects | ✅ `:562-566`, `:581-583` | ✅ `:219-230`, SHAPE `:252-274` | ✅ `:151` | ✅ `:26-30` + 2-pair example | — | ⛔ **`:386` singular pair** | ⛔ **`:386` singular pair** |
| check 7 carrier = `tasks.md`, `- [~]` task lines only | ✅ `:464-514` | — | ✅ `:104-127` | — | — | ✅ `:395` | ✅ `:395` |
| RED outcome = single uppercase token ≠ `PASS` | ✅ `:611-623` | ✅ `:245-249` | ✅ `:153` | ✅ `:35-37` | — | ✅ `:397` | ✅ `:397` |
| checker-truth boundary (structure/format/cardinality only) | ✅ `:682-692` | — | ✅ `:199-200` | — | — | ✅ `:402` | ✅ `:402` |
| freshness map: `tasks.md`→2,7,8–12; `plan.md`→12 | ✅ `:820-825` | — | ✅ `:205-213` | — | — | — | — |

Two drifts, both real:

- **`superpowers-bridge/templates/plan.md:21`** — "key 對應 tasks.md 的任務編號，**1 對 1**，
  兩邊集合必須完全相同（tasks.md 少一個或 plan.md 多一個都會擋在 verify）". This is the
  *exact* shape of P1-1: the name says 1:1, the text describes only set equality, and the
  two failure modes it enumerates are precisely the two that a set comparison can see. Its
  sibling `templates/tasks.md:3-7` was rewritten to two stages; this one was not, because
  task 3.1's delivered set named `templates/tasks.md` and `templates/verify.md` only.
- **`README.md:386` / `README.zh-TW.md:386`** — "Every task annotated `TDD: applicable`
  owes **a RED record and a GREEN record**" / 「附上**一筆** RED 紀錄與**一筆** GREEN 紀錄」.
  Under D2 the cardinality is one pair *per subject*, and a task may carry several. Task 3.2
  scoped itself to the checks 8–12 explanation (`:395-403`), so the apply-phase bullet 9
  paragraphs above it was never read against the new contract. This is the one phrasing
  task 2.4's residual-wording grep hunted inside `schema.yaml` — it just was not run over
  the READMEs.

Everything else matches, in both languages, character for character where it matters. The
zh-TW version is a faithful translation of the English, not a lagging one — I read both
`:395-403` blocks side by side and found no claim present in one and absent from the other.

## 2. Are the five defects actually closed?

I read the fixed text against the pre-edit text (`git show 22c15cf:superpowers-bridge/schema.yaml`)
rather than judging the diff by its shape.

| P1 | Defect | Closed? | Why I believe it |
|---|---|---|---|
| 1 | check 12 named 1:1, asserted set equality | **Yes** | `:720-749` collects both sides as **lists**, examines each side independently, names every repeated key with a message the text explicitly distinguishes from missing/extra, and `:766-771` states the equivalence honestly — "unique on each side plus equal as sets is exactly a bijection". Walked against f8 and f9: both BLOCK, on the right side, for the right reason. Walked against f7 and the change's own artifacts: no finding. |
| 2 | checks 9–11 constrained nothing but non-emptiness | **Yes** | `:585-600` gives a decidable grammar with the overlap rule spelled out (`a:::b` holds one), `:602-609` makes a grammar failure an unsatisfied field so check 9 owns it, `:625-681` pairs by value with uniqueness first. Two agents reading this on f10/f11/f12 cannot diverge — I re-derived each verdict independently and got the fixtures README's answers. |
| 3 | check 7 scanned `plan.md`, a carrier v2 forbids | **Yes** | Every reference moved: opening condition `:477`, the "tasks + test files" aside `:490-491`, the blocking condition `:512-514`, and the freshness map `:820-825`. `grep -n 'plan.md'` inside check 7's body returns zero. The `[~]` definition at `:466-475` is now positive (first non-space chars are `- [~]`), which also closes the "`[~]` in a title" false positive. |
| 4 | canonical spec named two carriers | **Yes** | `openspec/specs/tdd-claim-accuracy/spec.md:22-27` and `:59-68` both now name the tasks.md annotation + RED/GREEN evidence, and `:62` adds the explicit prohibition on plan.md task content. I re-read all 87 lines; there is no third statement. |
| 5 | CLAUDE.md coupling row named the `v1` grep | **Yes** | Row now quotes ``grep -E '^\| v2 \| `'`` **and** records `head -1` as load-bearing — which it now is, since the `v2` row precedes the retained `v1` row. Verified against `.github/workflows/version-check.yml:44`. |

One thing worth saying plainly: the fix for P1-2 does not merely add rules, it removes an
*undecidable* branch. The pre-edit check 11 body is four lines using the definite singular
("the RED record's `subject:` value and the GREEN record's"), which designates nothing when
a task holds two of each. f12's RED records that honestly as `INDETERMINATE` rather than
inventing a failure. That is the right call and it is rare.

## 3. The evidence chain

Checked as a set, against the three boundaries the tasks.md header sets.

- **Is each RED a pre-edit verdict?** Materially, yes — every RED cites
  `git show 22c15cf:superpowers-bridge/schema.yaml` with a line range, and **I re-ran every
  citation**: `:523-556` is pre-edit check 12, `:483-521` is pre-edit checks 9–11, and the
  check-7 block runs from `:421`. All four resolve to exactly the text claimed. Because the
  baseline is a committed blob, a later reader can reproduce every walk without trusting
  the author. Procedurally there is one asymmetry: 2.2 and 2.3 wrote their walk to
  `task-2.2-red-walk.md` / `task-2.3-red-walk.md` **before** editing; 2.1 has no such file,
  so its RED is attested only by the citation. Minor — the citation is the stronger evidence
  of the two, but the pattern should be uniform.
- **Do RED and GREEN bind the same subject character for character?** Yes — verified
  mechanically across all six pairs. 2.1 {f8, f9}, 2.2 {f10, f11, f12}, 2.3 {f13}; RED set
  equals GREEN set in every task, no repeat on either side.
- **Does each `failure:` state EXPECTED vs ACTUAL?** Yes, all six, in that order, with the
  *mechanism* named — not just "it passed" but which pre-edit clause was satisfied and why.
  f11's RED is the best of them: it notices that pre-edit check 9's "one `- RED:` line" is
  itself ambiguous and shows the RED holds **under either reading**. That is the kind of
  robustness a RED normally lacks.
- **Does every `TDD: n/a` reason name a control that could actually have failed?** Yes —
  all twelve. 1.1–1.3 defer to 2.1–2.3's RED/GREEN; 1.4 is a two-directional
  directory↔table listing; 2.4 a residual-wording grep; 3.1 a mechanical title diff; 3.2 a
  sentence-by-sentence match plus the Compatibility-row re-run; 4.1 a grep whose backticks
  are called out because the bare-word form silently returned 0 before; 4.2 a side-by-side
  read of the workflow line; 5.1 a falsifiability check run in **both** directions (new-only
  strings 0× pre-fix and ≥1× in the render, old titles 1× pre-fix and 0× in the render);
  5.2 an additions-only numstat. None is "I looked and it seemed fine."

The chain is reproducible. The one caveat is that 2.4's grep was scoped to `schema.yaml`,
which is why the identical phrasing survived in the two READMEs (Issue I2).

## 4. The thirteen fixtures under the new checks

I re-derived every fixture's verdict under the **new** wording, not the old.

| Fixture | Verdict under new checks | Still isolates? |
|---|---|---|
| f1 | check 8 (task 2 unannotated); task 1's records conform | ✅ |
| f2 | check 9 (no GREEN) **and check 11 stage two** (RED subject unpaired) | ⛔ **no** — see I4 |
| f3 | check 10 (RED `outcome: PASS`); sets equal, grammar OK | ✅ |
| f4 | check 11 stage two, both directions | ✅ |
| f5 | check 12 stage two, both directions; no dupes | ✅ |
| f6 | no deterministic BLOCK (`ERROR` conforms); R1 only | ✅ |
| f7 | no BLOCK — positive control, blank lines transparent | ✅ |
| f8 | check 12 stage one, tasks side, names `1.1` | ✅ |
| f9 | check 12 stage one, plan side, names `2.3` | ✅ |
| f10 | check 9 grammar, both records; check 11 finds nothing | ✅ |
| f11 | check 11 stage one, RED side; check 9 clean | ✅ |
| f12 | no BLOCK — positive control | ✅ |
| f13 | check 7 finds one deferred task | ✅ |

Twelve of thirteen still isolate. Crucially, **the grammar did not retroactively break
f1–f7**: every one of their subjects is `test/…::…`, so none of them newly trips check 9.
That was the biggest risk in this change and it came out clean. f2 is the exception, and
it is a consequence of check 11 becoming *decidable*: with no GREEN, stage two now
definitively reports the RED subject as unpaired, where the old singular text arguably had
nothing to compare. The fixture is still a good fixture; the README's answer key is now
incomplete.

## 5. Self-application: does the change pass its own checks 8–12?

I ran all five by hand and then mechanically over
`openspec/changes/fix-v2-blocking-defects/{tasks.md,plan.md}`.

- **check 8** — 15 task lines, each with exactly one conforming `- TDD:` line. Pass.
- **check 9** — three applicable tasks (2.1, 2.2, 2.3); every RED carries
  `subject`/`outcome`/`failure`, every GREEN `subject`/`outcome`, none empty after trim.
  All six subjects hold exactly one `::` with non-empty sides — including the ones whose
  right-hand side contains a literal `` `subject:` `` , which is not a `::` sequence. Pass.
- **check 10** — RED outcomes `FAIL`×5 and `INDETERMINATE`; all single uppercase tokens,
  none `PASS`. GREEN outcomes all exactly `PASS`. Pass.
- **check 11** — RED and GREEN subject lists unique per side and equal as sets in all three
  tasks. Pass.
- **check 12** — task numbers and entry keys are both
  `{1.1,1.2,1.3,1.4,2.1,2.2,2.3,2.4,3.1,3.2,4.1,4.2,5.1,5.2,5.3}`, no duplicate on either
  side, `## Self-review` correctly not collected as an entry. Pass.
- **check 7** — no `- [~]` line anywhere in tasks.md, so "no deferred tasks"; §7 may be
  blank. Pass.

**The change does not block itself.** But check 2 (task completion) will have something to
say: tasks 1.1–1.4 are still `- [ ]` although group 1 landed in `22c15cf` — all six fixture
directories exist and the README carries their six rows. Check 2 is non-blocking *provided
a reason is documented*, and the only truthful reason here is "it is done". See I3. Task
5.3's `- [ ]` is correct — it is genuinely pending by design.

## 6. The `version-check.yml` dependency

Intact. I re-ran the workflow's own two commands against the current file:

- `grep -E '^\| v2 \| \`' superpowers-bridge/README.md | head -1` → `| v2 | \`1.3.1\` | \`v5.1.0\` | 2026-09-01 |` (line 520)
- `awk -F'\`' '{print $2}'` → `1.3.1`; `'{print $4}'` → `v5.1.0`

The `v1` row survives at 521, which is why `head -1` matters and why CLAUDE.md's coupling
row now records it. `git diff --ignore-cr-at-eol -- superpowers-bridge/README.md | grep '^[+-]| v2 |'` is empty —
the row was never touched. **CI is not at risk.**

Additional facts checked outside the diff, each for a named risk: `superpowers-bridge/VERSION`
is `2.0.0` and `schema.yaml: version: 2` (D5 non-goal holds); `git tag -l` is empty and the
branch is 24 commits ahead of `origin/main` (D5's precondition still true, which is what 5.3
must re-confirm); `diff -r superpowers-bridge openspec/schemas/superpowers-bridge` is empty
(the dogfood copy really is the fixed checker).

## Deferred items, triaged

| Item | Ruling |
|---|---|
| No fixture carries both a duplicate key and a set difference | **May ship.** The non-short-circuit clause governs *reporting completeness*, not the verdict — both inputs BLOCK either way, so nothing ships unguarded. Each stage has its own fixture (f8/f9 vs f5). Building the combined case would require a fixture whose key sets are unequal, hence a new task in tasks.md *and* a matching plan entry, and the ruling that this is out of scope is right. Record it as a retrospective Miss with a follow-up, not as a merge blocker. |
| `templates/verify.md:54` §4 heading drift and "Design / Specs Coherence Spot Check" vs "Design/specs coherence" | **May ship.** Pre-existing, check 4 untouched by this change, and the template's own §1–§7 headings are consistently Title Case. House style, correctly reported and not fixed. |
| `templates/verify.md:148` task-line enumeration narrower than the schema's definition | **May ship**, but it is an *underclaim*, not cosmetic: the schema counts `- [` + any one char + `]`, the template enumerates only three markers, so a `- [?]` task would be silently omitted from the per-task table. Pre-existing and outside the delivered set. Fix at the next touch: "one row per task line (`- [` + any single character + `]`)". |
| `CLAUDE.md:187` 「需從 2 bump」 | **May ship.** It is correct today, and any concrete number goes stale at the next bump; 「需從當前 schema major bump」 would be durable, but this is a cosmetic follow-up, not a merge concern. |
| `CLAUDE.md:87` 「這個 repo 正在從 v1 往下一代改」 | **May ship.** Stale framing, fenced to a separately registered governance task, and the table immediately below it now reads `v2` correctly, so a reader is not misled about the current state. |
| check 11's collection step silent on a record carrying no `subject:` | **May ship — premise verified, not assumed.** I tested it rather than accepting it: check 9 (`:578-579`, `:602-609`) requires `subject:` on **every** RED and **every** GREEN, examines every record ("a defect in a task's second RED record is reported exactly as one in its first"), and BLOCKs naming the record. Its scope is identical to check 11's — both are quantified over tasks annotated `TDD: applicable` — so no input can reach check 11 with a subject-less record while check 9 stays silent. The gate verdict is therefore never wrong. What remains is narrower than the earlier ruling implied and worth one sentence some day: check 11's *own reported findings* on such an input are undefined, so two agents could file different check-11 text under an identical (and identically blocking) overall verdict. Listed as Minor, not a blocker. |
| Dogfood re-sync done as an in-place `cp -R` | **May ship.** I verified the end state independently rather than trusting the reasoning: `diff -r` between source and copy is empty. The stated caveat — that the equivalence does not generalise to a change that deletes a file from the bundle — is exactly right and worth keeping in the retrospective. |

## Strengths

Worth recording, because they are the reason this review found so little:

1. **The change holds itself to its own standard.** Check 12's closing paragraph
   (`:766-771`) states the *equivalence* — "unique on each side plus equal as sets is
   exactly a bijection" — and then immediately bounds it: "This check reads keys only".
   That is a name, a proof, and a disclaimer in four lines. The same discipline appears in
   check 9's `a:::b` overlap rule and check 11's "a malformed value still takes part here".
2. **The f12 RED is intellectually honest.** Recording `INDETERMINATE` where a lesser
   record would have claimed `FAIL` is the single best thing in the evidence chain, and
   f11's "this RED holds under either reading of the ambiguous pre-edit sentence" is a
   close second.
3. **Positive controls are treated as first-class.** f7 and f12 both exist, both are
   flagged as positive controls in the README table, and step 4 of the re-run instructions
   warns the re-runner that BLOCKing them is the failure. Most guard sets ship
   one-directional.
4. **The tasks.md header pre-commits to three falsifiable boundaries** before any evidence
   is written, including "a BLOCK is not automatically GREEN — the direction is per fixture
   and must be written out". That is why the six records are readable.
5. **Task 5.1's falsifiability check runs in both directions** — new-only strings absent
   from the pre-fix schema *and* old titles absent from the render. A one-directional
   version would pass on a stale copy.
6. **Check 7's absent-`tasks.md` paragraph** (`:494-508`) is not in the delivered set at
   all; it was added because the author noticed that checks 2 and 8–11 are all vacuously
   satisfied on an empty task list. That is the six-axis "what did I skip" habit working.

## Issues

### Critical

None.

### Important

**I1 — `superpowers-bridge/templates/plan.md:21`: the exact defect under repair, in an
un-audited surface.**
The comment says "1 對 1，兩邊集合必須完全相同（tasks.md 少一個或 plan.md 多一個都會擋在
verify）" — it claims 1:1 and then describes only set equality, naming only the two failure
modes a set comparison can detect. Its sibling `templates/tasks.md:3-7` was rewritten to two
stages; this file was outside task 3.1's delivered set and outside the six surfaces the
review brief named. Why it matters: an author who writes a plan from this template is told
duplicate keys are fine, and will be blocked by a check the template never mentioned.
**Fix:** mirror `templates/tasks.md:3-7` — "1 對 1 是兩個條件：先確認任一邊都沒有重複的 key
（同一個編號出現兩次就是 BLOCK，訊息與「少一個 / 多一個」不同），再把兩邊化為集合、雙向比對".

**I2 — `superpowers-bridge/README.md:386` and `README.zh-TW.md:386`: single-pair cardinality
survives in both languages.**
"Every task annotated `TDD: applicable` owes a RED record and a GREEN record" /
「都必須在同一個 checkbox 底下附上一筆 RED 紀錄與一筆 GREEN 紀錄」. Under D2 a task may carry
several subjects and owes one pair *per subject*; this sentence reads as exactly one pair
per task. Task 2.4's residual-wording grep was scoped to `schema.yaml`, and task 3.2 was
scoped to the checks 8–12 paragraphs, so nothing looked here.
**Fix:** "owes at least one RED record and one GREEN record — one pair per `subject:`, since
a task may carry several" / 「至少一筆 RED 與一筆 GREEN——每個 `subject:` 各一組，一個任務可帶多個 subject」.

**I3 — `openspec/changes/fix-v2-blocking-defects/tasks.md:44,46,48,50`: four completed tasks
still marked `- [ ]`.**
Tasks 1.1–1.4 all landed in `22c15cf` — the six fixture directories exist and the README
carries their six rows and the shuffle-all-thirteen note. Leaving them open forces verify's
check 2 to "document the reason" for four tasks whose only honest reason is "done", and
tasks.md is the schema's declared single source of truth for completion state.
**Fix:** change the four `- [ ]` to `- [x]` (5.3 correctly stays `- [ ]`).

**I4 — fixtures README:37: f2's answer key is now incomplete, so the blind re-run is
mis-scored.**
The row says `f2-missing-green` → "check 9 BLOCK". Under the new check 11 stage two, f2 also
blocks: RED carries `test/auth.test.js::rejects empty email` and the GREEN set is empty, so
the set comparison reports an unpaired subject. A blind re-runner who correctly names both
checks is marked as having over-reported against the key, and f2 no longer isolates one
thing — which is the property the whole fixture set is built on.
**Fix:** amend the row to "check 9 BLOCK（連帶 check 11 stage two：RED 有、GREEN 無）" and say
in the same row that f2 is deliberately the one fixture that trips two checks.

**I5 — `openspec/changes/archive/2026-09-04-loosen-plan/errata.md` E3: the archive record
misdescribes the defect it records.**
E3's table says checks 9–11 「以**位置（序數）**配對而非以 `subject:` 值配對」. That is not what
the pre-edit text did. `git show 22c15cf:superpowers-bridge/schema.yaml` check 11 reads in
full: "within one task, the RED record's `subject:` value and the GREEN record's `subject:`
value must be identical character for character… Any difference → BLOCK" — a definite
singular that designates *nothing* when a task holds two of each. It was **indeterminate,
not ordinal**. Ordinal pairing is what the new spec *prohibits* going forward, not what the
old check did. This contradicts the change's own f12 RED record (which correctly records
`INDETERMINATE`) and design D2. Since E3 is append-only and is the pointer a future reader
of the archive is told to trust, the wrong description is the one that survives.
**Fix:** 「配對規則對多筆紀錄**未定義**——條文用單數指稱「那筆 RED」與「那筆 GREEN」，一個任務帶
兩組以上時無從決定誰配誰；`subject:` 文法亦未受約束」. Append a correction rather than editing E3
if the file's own append-only rule forbids the edit.

### Minor

- **`superpowers-bridge/templates/verify.md:148`** — "one row per `- [ ]` / `- [x]` / `- [~]`
  task line" is narrower than the schema's `- [` + any char + `]`. Underclaims; pre-existing.
- **`superpowers-bridge/schema.yaml:634-637`** — check 11's collection step does not say what
  to collect from a record with no `subject:` field. Gate-safe (check 9 blocks first, same
  scope), but the *findings text* is undefined. One clause would close it: "a record with no
  `subject:` field contributes nothing to either list; its absence is check 9's finding".
- **`CLAUDE.md:187`** — 「schema major 需從 2 bump」 hard-codes today's major.
- **`openspec/changes/fix-v2-blocking-defects/tasks.md:61`** — task 2.1's RED has no pre-edit
  walk file, while 2.2 and 2.3 each wrote one before editing. The `22c15cf` citation is the
  stronger evidence, but the pattern should be uniform across the three.
- **`superpowers-bridge/templates/verify.md:54`** — §4 heading/title drift vs the schema's
  "Design/specs coherence". Pre-existing house style, already reported by task 3.1.

## Assessment

This is careful work on a hard target, and the hardest part — making five agent-executed
prose checks decidable without over-specifying them — came out right. The `::` grammar is
minimal in exactly the way D3 argued for, the two-stage structure is stated identically in
both two-stage checks, and the boundary sentences say what the checks *cannot* decide as
clearly as what they can. The evidence chain is the strongest I have seen in this repo:
every RED cites a committed blob with a line range, and every citation I re-ran resolved.

The five Important findings share one shape, which is worth naming because it is the same
shape as the original five P1s: **a scoped grep or a scoped task list was mistaken for a
complete sweep.** Task 2.4's residual-wording grep covered `schema.yaml` and stopped, so I2
survived in two READMEs. Task 3.1's delivered set named two templates, so I1 survived in the
third. The fixture answer key was written against the fixture's *intent* rather than re-derived
under the *new* checks, so I4 survived. In each case the check that would have caught it was
one command wider than the one that ran. The fix for all five is small; the lesson is that a
coherence change needs one final grep across *every* bridge-owned surface, not per-task ones.

Fix I1–I5 and this is ready. None of them touches a design decision, a spec, or the schema's
check logic; four are single sentences and one is four checkboxes.

⛔ Needs revision
