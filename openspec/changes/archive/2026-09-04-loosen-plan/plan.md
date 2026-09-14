# loosen-plan — Plan Contract

> First plan written to the Plan Contract (design.md D2) instead of the v1 micro-step format. Producer: agent direct generation from tasks.md + design.md + specs (D3). Executor: `superpowers:subagent-driven-development`, one fresh subagent per task; each entry says what done means, not how to get there.
>
> **Claim boundary of this dogfood:** this plan was hand-produced against the v1-installed schema (the CLI still served the writing-plans instruction, which was not invoked), by an agent that had just authored the contract. It exercises the contract's *shape*; it does **not** verify the direct-producer path (a fresh-context agent reading only the v2 `plan` instruction). That is task 10.4, after apply + sync; Q4-A is judged on that result, not on this file.

**Goal:** Replace the bridge's step-prescribing plan artifact with a per-task execution contract, and replace "TDD prescribed as micro-steps, nothing verified" with a TDD evidence contract whose presence and structure verify checks deterministically — in one change, shipping as schema major 2 / bundle 2.0.0 with every bridge-owned claim held to v1's real capability.

**Pointers:** `specs/plan-contract/spec.md`, `specs/tdd-evidence-contract/spec.md`, `specs/tdd-claim-accuracy/spec.md`, `design.md` (D1–D7, Risks, Migration Plan). Source analyses: `docs/superpowers/research/2026-09-01-plan-structure-comparison.md`, `docs/superpowers/research/2026-09-01-tdd-evidence-analysis.md`.

**Global constraints (verbatim from the specs; every entry below is bound by them):**

- "The plan artifact instruction SHALL NOT require micro-step decomposition, exact file paths, code snippets, commit points, or any fixed execution sequence."
- "Every task in tasks.md SHALL carry a TDD applicability annotation, indented under the task checkbox: `TDD: applicable` or `TDD: n/a — <reason>`. tasks.md is the single source of truth for applicability; plan.md entries MAY echo but SHALL NOT redefine it."
- "The RED and GREEN records SHALL be written in tasks.md, indented under the task's checkbox beside its `TDD:` annotation; plan.md SHALL NOT hold a second copy."
- "They SHALL distinguish a *deterministic (machine-evaluable) check* from a *mechanically enforced gate* … surfaces SHALL NOT claim a Harness-level mechanically enforced, non-bypassable archive-time gate."
- "The instruction SHALL NOT claim TDD executes automatically or unconditionally, SHALL NOT claim the schema verifies more than presence and structure, SHALL NOT claim a non-bypassable mechanical gate, and SHALL NOT retain the superseded statements that the schema 'neither enforces nor verifies TDD' or that TDD arrives via `writing-plans`' micro-step task content."

**Repo constraints (root CLAUDE.md, apply to every entry):** no `git add` / `git commit` in any instruction text; no PRECHECK removed other than the plan PRECHECK (D7); no `superpowers:executing-plans` fallback; PRECHECK failure stays fail-loud; every edit to `superpowers-bridge/` must pass `openspec schema validate superpowers-bridge` from a project copy; English canonical + zh-TW mirror for READMEs and adopter fragments; commit messages in English, conventional commits.

**Right-sizing:** each entry is one task from tasks.md (1:1, keyed by task number); a task is the smallest unit that carries its own verification and is worth a fresh reviewer's gate.

---

## 1.1 — plan artifact instruction: Plan Contract replaces writing-plans

- **Delivers:** An agent reading `openspec instructions plan` on the v2 schema is told to produce plan.md as header + one entry per tasks.md task, and is told nothing about invoking a skill or decomposing into steps.
- **Acceptance:** (a) the instruction contains no `writing-plans` PRECHECK and no `Skill` invocation; (b) it names all six contract elements — header (goal / pointers / global constraints), delivers, acceptance criteria, blocked by, interfaces marked conditional, right-sizing rule; (c) it states that exact paths, snippets and commit points are not required and that a decision-rich snippet is allowed; (d) it carries a generation-time self-review list (entry keys = task numbers, no vague acceptance language, interfaces present where coupled) and says self-review is earlier feedback, not the required control; (e) `openspec schema validate` passes; (f) `openspec instructions plan` renders the new text.
- **Blocked by:** none.
- **Interfaces:** *produces* the Plan Contract entry shape and the "keyed by task number" rule — consumed by 3.2 (executor reads entries), 4.1 check (e) (entry-key set), 6.1 (template mirrors the shape).

## 1.2 — plan artifact description line

- **Delivers:** The `plan` artifact's one-line `description:` names the contract, not writing-plans.
- **Acceptance:** `openspec status` / `openspec instructions plan` show the new description; no "micro-task" or "writing-plans" wording remains in it.
- **Blocked by:** 1.1 (same artifact block; wording must match).
- **Interfaces:** none.

## 2.1 — tasks artifact instruction: annotation SSOT + evidence carrier

- **Delivers:** An agent producing tasks.md on v2 is told every task must carry `TDD: applicable` or `TDD: n/a — <reason>` under its checkbox, is given the `n/a` reason vocabulary, and is told the RED/GREEN record shape that applicable tasks write under the same checkbox at completion, with tasks.md named as the v1 carrier rather than an invariant.
- **Acceptance:** (a) the instruction states the annotation grammar exactly as the spec does; (b) it lists the seed vocabulary (throwaway prototype, generated code, configuration, prose/doc-only) and says the reason is review-judged; (c) it states the RED record fields (subject `test-file::test-name`, outcome, failure excerpt) and GREEN fields (same subject, pass), invocation optional; (d) it says plan.md never duplicates evidence; (e) it says "first carrier, not an architecture invariant"; (f) validate passes.
- **Blocked by:** none.
- **Interfaces:** *produces* the annotation grammar and the RED/GREEN record shape — consumed by 3.1 (apply tells implementers what to write), 4.1 checks (a)–(d), 6.2 (template sample).

## 2.2 — tasks self-review line

- **Delivers:** The tasks instruction ends with a self-check an agent can run before declaring tasks.md done.
- **Acceptance:** the self-check names both conditions — no task without an annotation, no `n/a` without a reason — and is labelled earlier feedback (the required control is verify).
- **Blocked by:** 2.1.
- **Interfaces:** none.

## 3.1 — apply step-2 TDD passage rewritten

- **Delivers:** The apply instruction tells the executor where TDD comes from under v2 and claims exactly the tdd-claim-accuracy boundary.
- **Acceptance:** (a) passage says applicability is annotation-driven from tasks.md, applicable tasks owe RED/GREEN records under the task, verify's deterministic checks are agent-executed / instruction-mediated, semantics and authenticity rest on review; (b) `grep -n "neither enforces nor verifies TDD" superpowers-bridge/schema.yaml` and `grep -n "standard task format contains TDD" superpowers-bridge/schema.yaml` both return 0 hits; (c) no sentence claims automatic or unconditional TDD, or a non-bypassable gate; (d) validate passes.
- **Blocked by:** 2.1 (must describe the record shape 2.1 defines).
- **Interfaces:** *consumes* annotation grammar + record shape from 2.1; *produces* the list of superseded sentences that 10.2 greps for.

## 3.2 — apply executor wording reads contract entries

- **Delivers:** The apply pre-flight and step-2 executor text refer to plan.md entries (per-task contracts), not "micro-tasks", while the subagent-driven-development dispatch, the no-`executing-plans` rule and all other PRECHECKs are byte-for-byte unchanged.
- **Acceptance:** (a) `grep -n -i "micro" superpowers-bridge/schema.yaml` returns 0 hits inside the apply block; (b) **boundary:** the brainstorm / verify / retrospective / apply-pre-flight PRECHECK blocks, the subagent-driven-development dispatch and the no-`executing-plans` rule read identically before and after — only the sentences describing plan.md's shape and the TDD passage (3.1) may differ; (c) the CLAUDE.md red-flag table was re-read and none of its rows is triggered.
- **Blocked by:** 1.1 (entry shape), 3.1 (same block).
- **Interfaces:** *consumes* Plan Contract entry shape from 1.1.

## 4.1 — verify instruction: numbered deterministic checks + review judgements

- **Delivers:** verify's existing numbered list gains checks (a)–(e) and a separate short list of review judgements, and states its own enforcement boundary.
- **Acceptance:** (a) the five deterministic checks appear as additional numbered items — annotation present and well-formed on every task; RED and GREEN records present with required fields on every `applicable` task; RED outcome marker non-pass and GREEN marker pass; RED subject == GREEN subject; tasks.md task-number set == plan.md entry-key set with both differences empty — each ending in "→ BLOCK"; (b) a separate list names the review judgements (behavioural-vs-error RED, subject tests the claimed behaviour, `n/a` reason holds); (c) the instruction says the checks are agent-executed and that skipping one is not intercepted by v1; (d) **boundary:** every pre-existing verify instruction line is still present in its original order (guardrail 8: additions only, no restructuring); (e) mutation run: on a fixture change, each of the five violations (missing annotation / missing GREEN / PASS marker on RED / subject mismatch / plan `{1,2,9}` vs tasks `{1,2,3}`) produces BLOCK when the instruction is followed, and one SyntaxError-RED fixture surfaces as a review finding — results recorded in this change's verify.md.
- **Blocked by:** 1.1 (entry-key rule), 2.1 (annotation + record shape).
- **Interfaces:** *consumes* entry-key rule (1.1), annotation grammar + record shape (2.1); *produces* the check numbering that 4.2's template rows refer to.

## 4.2 — templates/verify.md §4 TDD rows

- **Delivers:** verify.md's §4 reports per-task TDD outcomes instead of "did the task list require TDD".
- **Acceptance:** §4 has a place to list, per task, its annotation and whether its records passed the deterministic checks plus the review judgement; the old "task list did not require TDD" wording is gone; the rest of the template is unchanged.
- **Blocked by:** 4.1.
- **Interfaces:** *consumes* check numbering from 4.1.

## 5.1 — top-level description: skill list + TDD sentence

- **Delivers:** The schema's top-level `description:` lists the four remaining required skills and states the TDD carrier at v2 capability.
- **Acceptance:** (a) `writing-plans` absent from the list; the other four (`brainstorming`, `using-git-worktrees`, `subagent-driven-development`, `finishing-a-development-branch`) present and unchanged — this is the description's required list, not the README's seven-row touchpoints table; (b) "TDD arrives via plan.md task content" replaced by an annotation + evidence-contract sentence that stays inside the tdd-evidence-contract "Claim boundaries" requirement; (c) validate passes.
- **Blocked by:** none.
- **Interfaces:** *produces* the required-skill list — consumed by 7.1 / 7.4 (README touchpoints, install expectations), 8.1 (adopter fragments).

## 5.2 — version literals

- **Delivers:** `schema.yaml: version: 2`; `superpowers-bridge/VERSION: 2.0.0`.
- **Acceptance:** from a clean test project copy, `openspec schema validate superpowers-bridge` passes and `openspec schemas` lists the bridge; **boundary:** nothing other than those two literals changes in this task.
- **Blocked by:** 1.1, 2.1, 3.1, 3.2, 4.1, 5.1 (the bump must land on the finished v2 content, not before).
- **Interfaces:** *produces* the version pair — consumed by 7.2 (Compatibility row), 8.2 (bridges table), 9.1 (CI grep key).

## 6.1 — templates/plan.md rewritten to the contract shape

- **Delivers:** The plan template scaffolds exactly the shape 1.1 prescribes, so an agent filling it produces a conforming plan without reading the instruction twice.
- **Acceptance:** the template has the header block (goal, pointers, global constraints), one example entry keyed by task number with delivers / acceptance / blocked by / interfaces (interfaces marked conditional in the `<!-- -->` guidance); no `Step N` checkboxes remain; zh-TW fill-in guidance allowed per repo convention.
- **Blocked by:** 1.1.
- **Interfaces:** *consumes* Plan Contract entry shape from 1.1.

## 6.2 — templates/tasks.md shows annotation + record shape

- **Delivers:** The tasks template shows a sample task with its `TDD:` annotation and a RED/GREEN record beneath it.
- **Acceptance:** the sample uses the exact grammar from 2.1; the `- [ ] X.Y` checkbox form the apply parser tracks is preserved.
- **Blocked by:** 2.1.
- **Interfaces:** *consumes* annotation grammar + record shape from 2.1.

## 7.1 — bridge README (en) claim updates

- **Delivers:** Every place the English bridge README describes plan.md, writing-plans or how TDD arrives now describes v2 truthfully.
- **Acceptance:** (a) exact superseded phrases return 0 hits in `superpowers-bridge/README.md`: "TDD micro-steps", "TDD per task content", "TDD arrives via plan.md", "writing-plans" as a required/PRECHECKed skill; (b) the touchpoints table row for writing-plans says it is no longer invoked and the TDD row describes the annotation + evidence contract; (c) the "Open drift — TDD is conditional upstream" paragraph marks the deeper fix as landed in v2 and leaves the brainstorming drift open; (d) every remaining "mechanical" / "guarantee" / "gate" hit is a negation or sits inside the Claim-boundaries requirement (checked hit by hit, not by count); (e) the Mermaid DAG and the comparison table no longer show writing-plans / micro-steps.
- **Blocked by:** 5.1 (skill list), 3.1 (the boundary wording it must mirror).
- **Interfaces:** *consumes* required-skill list from 5.1 and the claim boundary from 3.1; *produces* the section structure that 7.3 mirrors.

## 7.2 — Compatibility v2 row + migration guide

- **Delivers:** Adopters can see which OpenSpec / Superpowers versions v2 is verified against and how to move an in-flight v1 change.
- **Acceptance:** (a) a `| v2 | \`<openspec>\` | \`<superpowers>\` | <date> |` row is added and the v1 row is kept intact; (b) the two version cells are each a single backtick span (the shape 9.1's awk depends on); (c) a "Migrating v1 → v2" section lists the four steps from design.md § Migration Plan and the rollback (pin bundle 1.0.1); (d) Versioning prose says why this is a schema-major bump (previously-valid tasks.md failing v2 verify; PRECHECK shape).
- **Blocked by:** 5.2.
- **Interfaces:** *consumes* version pair from 5.2; *produces* the Compatibility row shape consumed by 9.1.

## 7.3 — bridge README (zh-TW) mirror

- **Delivers:** The zh-TW bridge README says the same things as 7.1 + 7.2.
- **Acceptance:** section-by-section parity with the English file for every section 7.1 / 7.2 touched (same tables, same rows, same claim wording in Taiwanese Mandarin); language-switch links intact.
- **Blocked by:** 7.1, 7.2.
- **Interfaces:** *consumes* section structure from 7.1.

## 7.4 — CLI cheat sheet / install expectations

- **Delivers:** Nothing in the cheat sheet or install steps tells a user they need `writing-plans`.
- **Acceptance:** `grep -n "writing-plans" superpowers-bridge/README.md` hits only the "optional aid, not required" mention (or none); two different kinds of README list are handled differently: (i) lists of skills the schema *requires or prechecks* (the description's required list; the apply pre-flight list) no longer include `writing-plans`; (ii) the version-check row "skills this schema names" (README:497) is a *names* list — it deliberately includes `executing-plans`, which the schema names only to forbid — so it is updated to whatever v2 still names (if `writing-plans` remains named as an optional aid, it stays in that row), and its "Layer 1 PRECHECK intact" verdict cell is re-checked against the removed plan PRECHECK. Counts follow from the lists, not the other way round.
- **Blocked by:** 5.1.
- **Interfaces:** *consumes* required-skill list from 5.1.

## 8.1 — adopter fragments (en + zh-TW)

- **Delivers:** Adopters pasting the fragment into their CLAUDE.md get v2 rules: the `TDD:` annotation expectation, and no red-flag row that presumes writing-plans is invoked.
- **Acceptance:** both locale files edited in the same commit; the "letting writing-plans write to docs/superpowers/plans/" row is removed or reworded for the optional-aid case; a line states tasks.md tasks carry `TDD:` annotations; both files remain consistent with the bridge README routing rules (cross-file coupling table row 5).
- **Blocked by:** 5.1, 7.1.
- **Interfaces:** *consumes* required-skill list from 5.1.

## 8.2 — top-level README bridges table (en + zh-TW)

- **Delivers:** The repo entry page shows the bridge at schema major v2 with a description that no longer mentions writing-plans micro-steps.
- **Acceptance:** the bridges table's version column reads `v2` in both locales; description cell reworded; both files in the same commit.
- **Blocked by:** 5.2.
- **Interfaces:** *consumes* version pair from 5.2.

## 8.3 — roadmap (en + zh-TW)

- **Delivers:** The roadmap records the plan-loosening / TDD-evidence item as landed in v2 and leaves everything else as it was.
- **Acceptance:** exactly one item changes state and it names v2 / 2.0.0; unrelated backlog items (verify polish points, brainstorming drift, "wait for OpenSpec core" items) are untouched; both locales.
- **Blocked by:** 5.2.
- **Interfaces:** *consumes* version pair from 5.2 (same coupling as 8.2).

## 8.4 — root CLAUDE.md: stale TDD clauses only

- **Delivers:** The repo's own CLAUDE.md — a bridge-owned normative surface per `openspec/specs/tdd-claim-accuracy` requirement 3 — no longer says TDD arrives through plan.md / writing-plans micro-steps or "when the task list requires it".
- **Acceptance:** (a) the executing-plans red-flag row's TDD clause reads the v2 carrier (tasks.md applicability annotation + evidence contract, executor-independent); (b) no other CLAUDE.md sentence describes TDD as arriving via plan.md content or writing-plans; (c) **boundary:** the rest of that red-flag row and every other red flag read identically before and after — the full §5 capability / evidence / degradation rewrite is *not* done here (it stays with the registered work-map item); (d) CLAUDE.md is inside 10.2's sweep scope and its hits are dispositioned there.
- **Blocked by:** 3.1 (the carrier wording it mirrors).
- **Interfaces:** *consumes* the claim boundary from 3.1.

## 9.1 — version-check.yml grep key

- **Delivers:** The weekly upstream-drift workflow reads its pinned baselines from the v2 Compatibility row.
- **Acceptance:** (a) the `Read pinned versions` step's grep matches the v2 row (either by literal `v2` or by "newest row" logic); (b) the step's extraction, applied to the edited README, yields a non-empty OpenSpec version and a non-empty Superpowers version, and they are the v2 row's values; (c) *verification procedure (recorded in verify.md, not a build step):* the pre-change `^\| v1 \|` key applied to the edited README still selects the v1 row — evidence that without this task CI would silently keep validating against the v1 baseline; (d) the awk backtick-column extraction is unchanged; (e) the next scheduled or dispatched run is green.
- **Blocked by:** 7.2.
- **Interfaces:** *consumes* Compatibility row shape from 7.2.

## 10.1 — dogfood re-sync + validate

- **Delivers:** The repo's own `openspec/schemas/superpowers-bridge/` is the v2 copy, and the bundle validates from a clean project.
- **Acceptance:** `diff -r superpowers-bridge openspec/schemas/superpowers-bridge` is empty; from a fresh test project, `openspec schema validate superpowers-bridge` passes and `openspec schemas` lists it; outputs pasted into this change's verify.md.
- **Blocked by:** every task in groups 1–6.
- **Interfaces:** none.

## 10.2 — superseded-claim sweep (two classes)

- **Delivers:** Evidence that no bridge-owned surface still carries a v1 claim or over-claims v2.
- **Acceptance:** (a) exact superseded sentences ("neither enforces nor verifies TDD", "TDD micro-steps", "TDD arrives via plan.md task content", "writing-plans' standard task format") return 0 hits across schema.yaml, templates/, both bridge READMEs, adopter fragments, top-level READMEs, and root CLAUDE.md (spec-named surface — a sweep that omits it can report clean while a normative surface still carries a v1 claim); (b) boundary vocabulary ("mechanical", "guarantee", "bypass", "gate", "fail-closed") is grepped and every hit is dispositioned in verify.md as negation / within Claim-boundaries / finding — a finding here blocks; 0 hits is not the criterion for class (b).
- **Blocked by:** groups 1–9 (8.4 included).
- **Interfaces:** *consumes* the superseded-sentence list from 3.1.

## 10.3 — v2 instruction render check

- **Delivers:** Proof that a new change on v2 gets the new plan and tasks instructions.
- **Acceptance:** in the test project, `openspec new change <x> --schema superpowers-bridge` succeeds; `openspec instructions plan` shows no writing-plans PRECHECK and the Plan Contract text; `openspec instructions tasks` shows the `TDD:` annotation rule; `openspec status` shows `version: 2` accepted; outputs recorded in verify.md.
- **Blocked by:** 10.1.
- **Interfaces:** none.

## 10.4 — bounded fresh-context v2 plan-generation smoke test

- **Delivers:** First evidence on Q4-A (agent direct generation): a plan.md produced by an agent that has *only* the v2 `plan` instruction, a tasks.md and a design.md — no prior exposure to this change's discussion — judged against the Plan Contract.
- **Acceptance:** (a) bounded: one fixture change (≥ 5 tasks, at least two coupled), one fresh-context subagent, one generation, no coaching; (b) the result is scored against the contract: entry-key set equality with tasks.md, no vague acceptance language, interfaces present on the coupled tasks, no step prescription — each a yes/no recorded in verify.md with the offending text quoted where "no"; (c) the D3 trigger list is consulted and each trigger marked observed / not observed on this sample; (d) the outcome is stated as one sample, not a verdict — Q4-A stands or a spike is proposed per D3, and that recommendation is left for the user to rule on.
- **Blocked by:** 10.1, 10.3.
- **Interfaces:** none.


## 11.1 — remove the superseded v1 TDD framing, and extend the detector that missed it

- **Delivers:** Three retrospective surfaces stop describing TDD as arriving from plan steps or from "a task list that did not require TDD" — categories v2 does not have, since every task carries an applicability annotation — plus the change to task 10.2's class (a) that makes this class catchable by the sweep rather than by a reader.
- **Acceptance:** `templates/retrospective.md`'s §4 TDD row label and its zh-TW note, and the `retrospective` instruction in `schema.yaml`, each state the v2 category (`TDD: n/a` in tasks.md is the declaration; its reason is judged by review) and no longer name plan steps or a task list that did or did not require TDD; task 10.2's class-(a) phrase list is extended so that each of the three sites **would have matched before it was repaired** — verified against the pre-fix text rather than the repaired text; the class is swept across all bridge-owned surfaces and any further instance is either fixed or ruled a record with the reason stated; the extended sweep returns 0 and the result is recorded in verify.md.
- **Blocked by:** 10.2 — the class-(a) phrase list this task extends must exist first.
- **Interfaces:** consumes the `TDD:` annotation vocabulary defined at 2.1 (`applicable` / `n/a — <reason>`) — the replacement wording must name that vocabulary and no other; produces the extended class-(a) phrase list that task 10.2's sweep runs.

## 11.2 — make the retrospective PRECHECK fail-closed

- **Delivers:** The `retrospective` PRECHECK stops treating "no failure evidence" as permission to proceed, and requires positive evidence of an acceptable verdict instead.
- **Acceptance:** the PRECHECK requires **exactly one** of verify.md's three Overall Decision boxes to be checked **and** that one not to be FAIL; zero checked, more than one checked, and FAIL each STOP; the instruction states why the count check cannot be simplified away, in terms of the fail-open it closes; the behaviour is demonstrated by running the amended check against a verdict-less fixture, a two-box fixture and a real verify.md, and by showing that the **previous** single command passes the verdict-less one; both bridge READMEs' design-touch description of this PRECHECK is updated in the same change, since it documents the command being replaced.
- **Blocked by:** none.
- **Interfaces:** consumes verify.md's Overall Decision checkbox shape as fixed by the `verify` template (the three literals `✅ PASS`, `⚠️ PASS WITH WARNINGS`, `❌ FAIL`) — a change to those literals breaks this check; produces the PRECHECK wording that both bridge READMEs' design-touch #5 must mirror.

---

## Self-review (generation-time, per D5 — earlier feedback, not the required control)

- Entry keys: 1.1 1.2 2.1 2.2 3.1 3.2 4.1 4.2 5.1 5.2 6.1 6.2 7.1 7.2 7.3 7.4 8.1 8.2 8.3 8.4 9.1 10.1 10.2 10.3 10.4 11.1 11.2 — 27 entries; tasks.md has 27 checkboxes with the same numbers; both differences empty.
  - **11.1 and 11.2 were added after group 11 reopened the task list**, and the gap between the two is the reason this line is worth reading twice. The reopen added the tasks and not the entries, so for one commit the change violated its own check 12 (27 task numbers, 25 entry keys) — caught by an independent review of the execution record, not by any gate, because every gate had run *before* the reopen and none re-ran after it. Recorded here rather than only in verify.md because this file is where the key sets are asserted.
- No acceptance criterion reads "works correctly" / "handles properly"; each names an observable (grep result, diff shape, CLI output, table cell, fixture outcome).
- Interfaces stated on every entry that produces or consumes a shared shape (annotation grammar, record shape, entry-key rule, skill list, version pair, Compatibility row); the five entries with no cross-task coupling (1.2, 2.2, 10.1, 10.3, 10.4) state `**Interfaces:** none.` explicitly rather than dropping the field — the spec's wording is "MAY be omitted", so an explicit `none` is conforming and distinguishes "no coupling" from "field forgotten". Both group-11 entries state Interfaces: 11.1 consumes 2.1's annotation vocabulary and produces 10.2's phrase list; 11.2 consumes the verify template's three checkbox literals and produces the wording both READMEs mirror. Set check re-run after the group-11 entries landed: 27 tasks.md keys, 27 plan.md keys, both differences empty.
- No entry prescribes an edit sequence, tool, or commit point; where a path appears it identifies *what must be true*, not *how to get there*.
- TDD applicability is not restated here — tasks.md is the SSOT; evidence, when any task is applicable, lives there.
