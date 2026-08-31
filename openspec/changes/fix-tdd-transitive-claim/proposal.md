# Proposal — fix-tdd-transitive-claim

## Why

`schema.yaml` and both bridge READMEs claim upstream `subagent-driven-development`
"internally enforces" TDD (every task RED-GREEN-REFACTOR, no manual invocation needed).
Verified false in all three checked upstream versions: upstream TDD is conditional on the
task list. In this repo the schema **is** the behavior, so the false claim actively removes
the layer responsible for noticing a missing TDD requirement — and the upcoming "plan 放寬"
work would make that silent gap real. Fix now, under the corrective-fix exception, before
any formal schema work builds on the false premise.

## What Changes

**schema.yaml transitive-activation claim (apply instruction)**
- From: "subagent-driven-development internally enforces … test-driven-development — every
  task follows RED-GREEN-REFACTOR … you do NOT need to invoke them manually"
- To: honest conditional statement (frozen draft, brainstorm §三 Q3): TDD depends on the
  task list; `writing-plans`' standard format contains TDD micro-steps but per-task
  inclusion depends on its judgment; this schema neither enforces nor verifies; no layer
  **guarantees** to add TDD if the task list lacks it.
- Reason: the claim is falsified; the replacement must not mint a mirror-image absolute.
- Impact: non-breaking (prompt text only; no artifact graph change, schema major stays 1).

**`executing-plans` fallback rationale (schema.yaml + both bridge READMEs)**
- From: "not supported because it does not transitively bring TDD and code-review"
- To: same conclusion, corrected reasons — it dispatches no independent reviewer at all
  (SDD structurally does, per-task, though not one-reviewer-per-task); upstream itself
  directs to SDD when subagents exist. TDD is symmetric between the two paths and is no
  longer used as the differentiator.
- Impact: non-breaking; CLAUDE.md red-flag entry (line 207) reworded to match.

**Both bridge READMEs — every claim in the frozen Affected Surface (14 en + 14 zh-TW
segments)**: guarantee-shaped wording corrected to conditional; already-honest rows kept.

**Top-level READMEs (en + zh-TW), bridges table**
- From: `TDD-via-subagents` (a pseudo-identifier compressing the false premise)
- To: honest phrase naming plan-driven TDD micro-steps + subagent execution.

**`templates/retrospective.md` inducement block (semantic block around :55–84)**
- From: "Default expectation: all ✓ … blank section (all green) is the expected state …
  must not write '不需要'"
- To: neutral attestation — the table stays, the pressure to attest unverifiable
  compliance goes.

**Not in scope**: evidence mechanism / real gate (Change 2), residue-check automation,
`templates/plan.md` TDD structure (plan-放寬 work line), record-class files, schema major.

## Capabilities

### New Capabilities

- `tdd-claim-accuracy`: what the bridge is allowed to claim about TDD — every statement
  about TDD reaching the implementer must be conditional (task-list-dependent), name the
  actual carrier (`writing-plans` plan content, not the executor), and never state or imply
  an unconditional guarantee; the `executing-plans` exclusion rationale must rest on review
  structure, not TDD transitivity.

### Modified Capabilities

(none — `openspec/specs/` is empty; no existing capability specs to delta)

## Impact

- `superpowers-bridge/schema.yaml` (6 segments — the 5 frozen ones plus the
  retrospective-instruction inducement block found during review, the schema-side twin of
  the template's block; code-class review plane)
- `superpowers-bridge/README.md` + `README.zh-TW.md` (14 + 14 segments, edited in pairs)
- `superpowers-bridge/templates/retrospective.md` (1 semantic block)
- `CLAUDE.md:207` red-flag entry; top-level `README.md` / `README.zh-TW.md` line 11
- `openspec/schemas/superpowers-bridge/` dogfood copy re-sync after edits
- `superpowers-bridge/VERSION` patch bump (1.0.x); no CI/workflow changes
