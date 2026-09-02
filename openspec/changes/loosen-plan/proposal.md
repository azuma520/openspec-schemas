# Proposal — loosen-plan

## Why

The bridge's plan artifact currently prescribes **steps**: `superpowers:writing-plans` decomposes every task into 2-5 minute micro-steps with exact file paths, code snippets, and commit points. This violates the repo's governing principle ("the model owns the path; the harness owns evidence and hard boundaries") — if two good agents can implement differently and both satisfy the spec, the plan should not pre-choose for them. It is also the sole carrier of TDD: the apply instruction admits "this schema itself neither enforces nor verifies TDD" — TDD exists only as micro-step text that no layer checks. Removing the micro-steps without a replacement would cut the fuse entirely; the two moves are one governance switch (user ruling Q1, 2026-09-01): **quality control shifts from "prescribe how" to "require proof of what"**.

Unlocked by the event gate's double YES (concept PoC 2026-08-28; formal design 2026-09-01) and grounded in the formal design §4.3 (TDD evidence contract) and spike ruling S4 (explicit applicability annotation).

## What Changes

1. **Plan Contract replaces micro-step prescription.** plan.md becomes a per-task execution contract: what it delivers (end-to-end behaviour), acceptance criteria, dependency edges, interfaces (conditionally required — only where tasks couple), global constraints, right-sizing rules. Step-encoding content (2-5 min steps, mandatory exact paths, commit points, execution handoff) is removed. Structure decisions recorded in brainstorm.md Q2; full source analysis in `docs/superpowers/research/2026-09-01-plan-structure-comparison.md`.
2. **Producer: agent direct generation** (Q4). The plan PRECHECK and the normative `writing-plans` dependency are removed (not banned — an executor may still use it as an optional aid; its micro-steps no longer define plan.md's format). `/to-tickets` remains a design reference, not invoked. A Harness-native contract-planning skill is a **trigger-defined** upgrade path, not built now.
3. **TDD evidence contract.** tasks.md is the SSOT for applicability: every task carries `TDD: applicable` or `TDD: n/a — <reason>`. Applicable tasks must attach RED/GREEN evidence (five required fields; valid RED = behavioural failure, not error). **Fail-closed, stated at v1's real capability**: v1 guarantees mechanical blocking before archive/acceptance through the verify checks; generation-time self-review provides earlier feedback but is not itself the mechanical guarantee. Semantic quality stays with review (residual risk stated, not papered over). Full analysis in `docs/superpowers/research/2026-09-01-tdd-evidence-analysis.md`.
4. **Coupled surface sync.** Schema description, both bridge READMEs (design touchpoints), adopter fragments (en/zh-TW), and the plan/tasks templates are updated to the new truthful claims.

Scope is closed (Q1): no Scenario traceability, no Gate lifecycle, no reviewer provenance, no digest/freshness, no evidence JSON schema, no executor identity.

## Capabilities

- **New Capabilities**
  - `plan-contract`: what a conforming plan.md must contain (contract shape, producer rules, conditional interfaces, fail-closed points).
  - `tdd-evidence-contract`: applicability annotation SSOT, RED/GREEN evidence requirements and validity criteria, mechanical verify checks, claim boundaries.
- **Modified Capabilities**
  - `tdd-claim-accuracy`: its "Honest statement of the TDD carrier" requirement pins the current apply-instruction wording ("the schema itself neither enforces nor verifies TDD"; "writing-plans' standard task format contains TDD micro-steps"). Both become false under this change — the carrier becomes the annotation + evidence contract, and the schema *does* mechanically verify evidence presence/structure. The requirement is updated to the new truthful carrier statement while keeping its core prohibition (no unconditional-execution claims; no over-claiming evidence authenticity).

## Impact

- `superpowers-bridge/schema.yaml` — plan artifact instruction (rewritten), tasks instruction (TDD annotation), apply instruction (TDD passage rewritten; writing-plans references), verify instruction (new numbered mechanical checks), top-level description (skill list, TDD sentence). **Versioning (ruled 2026-09-01): schema major → 2, bundle → 2.0.0.** Primary breaking fact: the new normative Plan/TDD contract makes some previously-valid v1 changes (tasks.md without TDD annotations) fail the new verification until migrated — previously-legal artifacts becoming illegal is the definition of breaking, independent of the PRECHECK question. Secondary: the plan PRECHECK removal also hits the README Versioning policy's "PRECHECK shape" criterion. The alternative — keeping v1 and rewording the policy — was rejected as redefining "breaking" to fit the change. CLI risk verified absent (`version: 2` passes validate / list / new / status / instructions, openspec 1.3.1, isolated test project). Design includes a minimal v1→v2 migration path, a v2 compatibility row, and the version-check CI coupling — no broader migration framework.
- `superpowers-bridge/templates/plan.md`, `templates/tasks.md` — rewritten to the contract shape (settles the 2026-08-27 open item on plan.md's 17-line shell).
- `superpowers-bridge/README.md` + `.zh-TW.md`, `templates/adopters/*.fragment*.md` — claim updates.
- `openspec/specs/tdd-claim-accuracy/spec.md` — delta spec (MODIFIED).
- No change to: OpenSpec CLI, other artifacts' graph position, PR #970 mitigations. On the plan PRECHECK specifically: it is removed **because the normative `writing-plans` dependency it guarded is removed** — a PRECHECK answers "is this skill present?", which has no object once no skill is invoked. Assurance is not silently dropped: the Plan Contract plus the verify checks establish the replacement **control objective** (a conforming plan, mechanically checked before archive) — a different control, not a one-to-one substitute for the PRECHECK. Argued explicitly in design.md.
