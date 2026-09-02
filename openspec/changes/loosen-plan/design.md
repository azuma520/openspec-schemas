# Design — loosen-plan

## Context

The bridge's plan artifact prescribes steps: `superpowers:writing-plans` decomposes tasks into 2-5 minute micro-steps with exact file paths, code snippets, and commit points. Those micro-steps are also the only carrier of TDD — the apply instruction states "this schema itself neither enforces nor verifies TDD", and `openspec/specs/tdd-claim-accuracy/spec.md` pins that wording as the honest claim. The repo's governing principle ("the model owns the path; the harness owns evidence and hard boundaries", root CLAUDE.md) and the bridge-guarantee formal design (§4.3 TDD evidence contract; spike ruling S4) both point the same way: replace step prescription with an evidence contract.

Constraints inherited, not re-decided: event gate double YES holds (PoC 2026-08-28, formal design 2026-09-01) but implementation still goes block-by-block through opsx changes; `tasks.md` is the authoritative task list (SSOT, ruled 2026-08-28); the plan artifact is not deleted (root CLAUDE.md — the user questioned plan's granularity, not its existence); formal-design guardrail 8 leaves `verify.md` unrestructured.

Source analyses (read-in-full dissections of `writing-plans`, `/to-tickets`, and both mature TDD skills) live in `docs/superpowers/research/` — this design records outcomes and reasoning, not the raw comparisons.

## Goals / Non-Goals

**Goals**

1. plan.md becomes a per-task execution contract (what done means, boundaries, interfaces) instead of a micro-step script.
2. TDD moves from "steps prescribed, nothing verified" to "evidence required, presence and structure mechanically checked" — in the same change, so the fuse is never absent (Q1).
3. Every bridge-owned claim stays truthful after the switch, including the pinned `tdd-claim-accuracy` carrier statement.
4. Honest v1→v2 versioning with a minimal migration path.

**Non-Goals** (closed set, Q1): Scenario traceability; Gate lifecycle / gate-pass records; reviewer provenance / executor identity; digest/freshness; evidence JSON schema or any new file format; harness runtime capture of commands/exit codes; full TDD history provenance; per-task regression-suite evidence; test-quality scoring; any migration framework beyond the guide in this change; `/to-tickets` adaptation (independent work line, formal design §9.3).

## Decisions

### D1 — Bundle plan loosening and TDD evidence in one change

They are the two halves of one governance switch: micro-steps are removed and the evidence contract is installed in the same edit, so no state exists where TDD has no carrier. Alternative (two sequential changes) rejected: either an assurance gap (loosen first) or the same instruction text edited twice (evidence first). (Q1)

### D2 — Plan Contract shape

plan.md carries a header (goal, pointers to this change's specs/ and design.md, global constraints copied verbatim) and one contract entry per tasks.md task, keyed by task number (1:1, mechanically cross-checkable). Each entry: **what it delivers** (end-to-end behaviour, not layer-by-layer), **acceptance criteria** (concrete and verifiable — vague language like "works correctly" is non-conforming), **blocked by** (explicit dependency edges), **interfaces** (conditionally required — only where a task couples with a neighbour; unconditional requirement would force fabricated interfaces, same failure mode the formal design §3.2 rejects for reverse Task→Contract annotation). Right-sizing rule retained from writing-plans: a task is the smallest unit carrying its own test cycle and worth a fresh reviewer's gate, sized to a single fresh context window. Exact file paths, code snippets and commit points are **not required**; a decision-rich snippet (state machine, schema, type shape) may be included where it encodes a decision more precisely than prose (rationale imported from `/to-tickets`: implementation detail goes stale fastest). Architecture and tech-stack prose stays in design.md, referenced not repeated. (Q2; element-by-element derivation in research/2026-09-01-plan-structure-comparison.md)

### D3 — Producer: agent direct generation

The plan instruction defines the contract; the agent fills it from tasks.md + design.md + specs. No skill invocation is required to produce plan.md. v1 hypothesis (stated so it can fail): the Plan Contract is explicit enough that filling it is a transcription-and-structuring job, not a planning-procedure job. **Residual risk, stated honestly**: mechanical checks cover contract completeness only (fields present, IDs match, evidence attached); semantic quality — whether acceptance criteria are actually verifiable, boundaries actually right — rests on producer quality plus review. "Acceptance: feature works" passes every mechanical check and is still a bad plan; review is what catches it.

- `writing-plans`: normative dependency and PRECHECK removed; **not banned** — an executor may use it as an optional decomposition aid, but its micro-steps do not define plan.md's normative format.
- `/to-tickets`: design reference only (its contract qualities are absorbed into D2); not invoked — `disable-model-invocation: true`, setup dependency, foreign output carrier, and it would add an adopter plugin dependency.
- Harness-native contract-planning skill: **trigger-defined upgrade path**, not built now. Triggers (recorded so failure of D3 is detectable, not vibes): recurring unverifiable acceptance criteria, recurring boundary/interface/dependency omissions, reviewers repeatedly rewriting plans wholesale, or high variance across producers. Any of these recurring → bounded spike comparing direct generation vs a dedicated skill (§9 governance), then a user decision. (Q4)

### D4 — TDD evidence contract

- **tasks.md is the SSOT for applicability**: every task carries `TDD: applicable` or `TDD: n/a — <reason>` (indented under the checkbox, following the mechanically-parseable annotation pattern the PoC validated for `Contracts:`). plan.md entries may echo but never redefine it.
- **Applicable tasks attach RED/GREEN evidence.** Required fields — RED: subject (v1 carrier: `test-file::test-name`), outcome (non-pass, and a behavioural failure rather than a SyntaxError / import / dependency / harness error), failure output excerpt sufficient to show the target behaviour was not yet satisfied. GREEN: subject (identical to RED — mechanical equality is the load-bearing join), outcome (pass). Supporting, not required: invocation (command) — it serves reproducibility and review depth, and no completion-claim check takes it as input; useful does not auto-promote to required.
- **RED's claim, exactly**: the subject was executed and failed correctly because the target behaviour was not yet satisfied; this supports the RED→GREEN transition, not a full test-first history. No artifact-state wording — this change has no state identity.
- **The annotation is a semantic assertion** (S4): review judges whether `n/a` reasons hold and whether the subject actually tests the claimed behaviour; the mechanical layer verifies presence, format, and the subject join only. The upstream skill's exception list (throwaway prototypes, generated code, configuration) seeds the `n/a` reason vocabulary.
- Suite-level regression and refactor-stays-green remain change-level concerns (verify/CI), deliberately not per-task evidence. (Q3; full derivation in research/2026-09-01-tdd-evidence-analysis.md)

### D5 — Fail-closed placement and its honest claim

Two layers, one guarantee: plan/tasks self-review instructions catch problems at generation time (prompt layer — earlier feedback, best effort, and CI cannot see prompt-text rot); the **verify artifact's new numbered mechanical checks are the guarantee** — annotation presence/format on every task, RED+GREEN presence for applicable tasks, subject equality, fail/pass markers, and plan↔tasks entry-count cross-check. **v1 guarantees mechanical blocking before archive/acceptance; it does not guarantee interception at generation time.** Adding numbered checks to verify's existing list leaves its structure untouched — read as compatible with formal-design guardrail 8 ("no verify.md restructuring"); this reading is stated here precisely so reviewers can challenge it.

### D6 — Versioning: schema major 2, bundle 2.0.0

**Primary breaking fact**: v2's normative Plan/TDD contract makes some previously-valid v1 changes (tasks.md without annotations) fail the new verification until migrated — previously-legal artifacts becoming illegal is what breaking means, independent of any PRECHECK argument. **Secondary**: removing the plan PRECHECK also hits the README Versioning policy's "PRECHECK shape" criterion. Keeping v1 and rewording the policy was rejected: it would redefine "breaking" to fit the change and silently break the v1.x compatibility promise. CLI behaviour under `version: 2` verified normal end-to-end (validate / schemas / new / status / instructions; openspec 1.3.1, isolated test project, 2026-09-01). (Q5)

### D7 — PRECHECK removal is a consequence, not a substitution

The plan PRECHECK answered "is `superpowers:writing-plans` present?". With the normative dependency removed, that question has no object — the PRECHECK is removed because its subject is, not because contract text "replaces" it. Assurance is not silently dropped: the Plan Contract plus D5's verify checks establish the **replacement control objective** (a conforming plan, mechanically checked before archive) — a different control for a different question, not a one-to-one substitute. This is the argued exception to the CLAUDE.md red flag "removed a PRECHECK without a stronger replacement": the red flag targets dropping a control while keeping the dependency; here the dependency itself is gone and a new control covers the new objective. All other PRECHECKs (brainstorm, verify, retrospective, apply pre-flight) are untouched.

## Risks / Trade-offs

- [Semantic quality of agent-direct plans] → D3 triggers make failure observable; review carries semantic judgment; upgrade path pre-defined.
- [Prompt-layer rot invisible to CI] → known repo-wide limitation (README Compatibility caveat); the mechanical teeth live in verify's checks, which operate on artifact text, not prompt text.
- [Weakest scenario: self-review + fabricated evidence passes v1] → stated, not solved — evidence authenticity is review-layer assurance and degrades with it (formal design §8#5); reviewer provenance is S6/Gate work, out of scope here.
- [plan↔tasks drift (two files, hand-maintained)] → 1:1 task-number keying + verify count cross-check (near-zero cost, pattern already proven in PoC).
- [Upstream `writing-plans` evolution] → no longer load-bearing: the contract no longer references its output shape.

## Migration Plan (v1 → v2)

For adopters upgrading an in-flight change (goes into the bridge README as the migration guide; kept minimal by design):

1. tasks.md — add `TDD: applicable` / `TDD: n/a — <reason>` under every task.
2. Applicable tasks — provide RED/GREEN evidence per the contract before verify.
3. plan.md — migrate micro-step plans to the Plan Contract shape (or regenerate from tasks.md + design.md).
4. `superpowers:writing-plans` — no longer a required dependency; remove from install expectations.

Repo-side coupling (same change): README Versioning/Compatibility sections gain the v2 row; `version-check.yml`'s pinned-version grep keys on the compatibility row — update together (cross-file coupling table row 1); adopter fragments and design-touchpoint sections updated en + zh-TW. Rollback: adopters can pin bundle 1.0.1 (v1 stays a published cut).

## Open Questions

None blocking. Deferred by design: D3 upgrade triggers are observed during dogfood, not scheduled; S2's "Orca UI gate-resolve signature" stays attached to future Gate work, not this change.
