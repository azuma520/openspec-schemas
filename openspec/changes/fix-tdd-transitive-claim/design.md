# Design — fix-tdd-transitive-claim

> Reorganized from `brainstorm.md` (2026-08-27 rewrite, survived 3 external review rounds).
> One-line scope: **delete the false claim that upstream automatically enforces TDD, replace it
> with an honest statement. No evidence mechanism is built in this change.**

## Context

- `superpowers-bridge/schema.yaml` (and both READMEs) claim upstream
  `subagent-driven-development` "internally enforces" TDD so agents "do NOT need to invoke
  [it] manually". Verified false: in all three checked upstream versions (5.1.0 / 6.2.0 /
  6.3.0) TDD is **conditional on the task saying so** (3 conditional clauses + 1 unconditional
  assumption in `task-reviewer-prompt.md:75`, which is upstream's own contract crack, not a
  guarantee). Full evidence: brainstorm §一–§二.
- How TDD actually arrives: `writing-plans` writes RED→GREEN micro-steps into each task
  (**plan content, not executor feature**). The bridge's plan artifact does invoke
  `writing-plans` (schema.yaml:178), but that is a convention, not a guarantee — and the
  manual-fallback path (`templates/plan.md`, a 17-line shell) carries no TDD structure at all.
- Why it matters here: this repo has no source code — `schema.yaml` **is** the behavior.
  A false claim in it removes the layer that would otherwise be responsible for noticing
  a missing TDD requirement (harm chain: brainstorm §1.2).
- Governance: this change runs under the **corrective-fix exception** (CLAUDE.md event gate,
  2026-08-28): only deletion/correction of already-falsified claims is allowed. No Completion
  Gate, no Contract Verification, no Orca integration, no new formal design capability.
- Same-shaped disease recurred 4 times in 24h (brainstorm §1.3, §五: 9 false guarantees,
  8 self-authored). Every wording this change ships must itself pass the
  "convention must not be written as guarantee" test.

## Goals / Non-Goals

**Goals:**

1. Delete/correct every claim (in the frozen Affected Surface, brainstorm §四: 35 segments /
   21 logical positions) that says or implies TDD happens automatically downstream.
2. Add the honest replacement statement (draft wording frozen in brainstorm §三 Q3; it says
   "no layer **guarantees** to add TDD", not "no layer will").
3. Rewrite the `executing-plans` fallback rationale (README/schema) — the old "it lacks
   TDD+code-review transitivity, we have it" comparison collapsed on the TDD half (§D3).
4. Correct the top-level README `TDD-via-subagents` phrase (both languages) — it is a
   compressed form of the false premise, not a skill name (§D4).
5. Defuse the inducement block in `templates/retrospective.md` (:55–84 by meaning, not by
   line range) that pressures agents to check "all ✓" (§D5).

**Non-Goals** (brainstorm §六, all explicit):

- ❌ No evidence mechanism / no real gate (Change 2's scope; current carriers would be
  refuted — D4-style hand-copied evidence proves "green now", not "red-then-green").
- ❌ No residue-check script / CI blacklist (blacklists already failed in user's own record;
  the checkpoint cannot catch the failure that actually happened — nobody knew the sentence
  was wrong).
- ❌ No schema major bump (no artifact graph / `requires:` change).
- ❌ No rewriting of record-class files (handoffs, discussion material, archives).
- ❌ Codex / agy never enter the outward contract (local dev premise only).
- ❌ No fixing of `templates/plan.md`'s 17-line shell (§D6 — out of corrective-fix scope).

## Decisions

### D1: Delete + one honest sentence; no gate in this change

- **Choice**: The fix is deletion of the false guarantee plus the honest replacement
  (brainstorm §三 Q3 wording). Evidence mechanism deferred to Change 2.
- **Why**: The gate one could build now (grep blacklist / propagation report policy) is
  refuted by the user's own records (blacklist bypassed by rewording, green while failing);
  a policy is not a gate. Building a known-refutable gate inside a change that fixes false
  guarantees would mint a new false guarantee.
- **Alternative considered**: bundle with traceability/evidence work — rejected 2026-08-26
  (review §5: "Change 1 unaffected, proceed as planned"; Codex #2: do not share necessity
  arguments). The 8/27 morning merge decision was revoked.

### D2: The honest statement is itself a claim and must stay conditional

- **Choice**: Ship the frozen wording: TDD depends on the task list; `writing-plans`'
  standard format **contains** TDD micro-steps but whether each task carries them depends on
  its judgment of task type; this schema itself neither enforces nor verifies; if the task
  list lacks TDD, **no layer guarantees** to add it.
- **Why**: earlier drafts wrote the mirror-image absolute ("no layer **will** add it") —
  falsified by upstream TDD skill's own trigger (`any feature or bugfix` — a subagent may
  self-trigger) and by retrospective's weak after-the-fact detection. Absolute negation is
  the same disease in the opposite direction (brainstorm §五 #5/#7/#8 — committed three
  times while writing the brainstorm itself).

### D3: New `executing-plans` fallback rationale — review structure, not TDD

- **Choice**: Keep the conclusion (bridge does not support `executing-plans` as apply
  fallback) but replace the reason with two verified facts:
  1. `executing-plans` (v6.3.0, 64 lines, re-read 2026-08-31) dispatches **no independent
     reviewer at all** — single agent executes steps and self-checks; SDD structurally
     dispatches per-task review (weakened — README:501 already honestly marks "not one per
     task" — but present).
  2. Upstream itself directs users to SDD whenever subagents exist (`executing-plans`
     SKILL.md:14); the bridge deliberately targets subagent platforms.
- **Why**: the old comparison "it doesn't transitively bring TDD, we do" is false — when a
  task requires TDD, both executors receive that requirement through plan content, and
  neither guarantees it otherwise (symmetric, cannot differentiate). The code-review half
  only weakened, did not collapse; it becomes the load-bearing half.
- **Alternative considered**: delete the whole rationale paragraph — rejected: the
  conclusion still holds and the red-flag list in CLAUDE.md depends on it being stated;
  only the reasoning is corrected.

### D4: Top-level README `TDD-via-subagents` → honest phrase

- **Choice**: Replace `TDD-via-subagents` in both top-level READMEs (line 11, en + zh-TW)
  with a description that names what actually happens, e.g. plan-driven TDD micro-steps +
  subagent execution (exact wording finalized at implementation, subject to D2's test).
- **Why**: it is not any skill's name; it is the false premise compressed into a
  pseudo-identifier. Brainstorm §4.2a explicitly rejected filing it as "neutral".

### D5: `retrospective.md` inducement block — defuse, keep the table

- **Choice**: Rework the block around the skill-compliance table (meaning-wise :55–84; the
  55–78 range cuts mid-list — follow the semantic block, line numbers only for relocation):
  remove "Default expectation: all ✓ / blank section (all green) is the expected state /
  must-not-write '不需要'" inducements; keep the table itself, with its row labels corrected
  so the TDD row records explicit skill invocation only (plan-step TDD alone is recorded as
  `N/A — plan-step TDD only`, not as the skill being used) and the code-review row is
  labeled structural ("structural via SDD").
- **Why**: the block does not state the false claim, it **acts** on it — it pressures the
  agent to attest compliance it cannot know happened. Inducement-type, a third category
  beyond claim/description (brainstorm §4.4).

### D6: `templates/plan.md` 17-line shell — NOT fixed here

- **Choice**: Leave the manual-fallback plan template's missing TDD structure untouched;
  it belongs to the "plan 放寬" work line (existing record).
- **Why**: adding TDD structure is **adding capability**, which the corrective-fix
  exception explicitly forbids ("不得藉此加入…任何新正式設計能力"). The honest statement
  (D2) already discloses that the fallback path carries no TDD structure, so the gap is no
  longer silent.

### D7: Frozen Affected Surface is the work list; not an exhaustiveness proof

- **Choice**: Work from brainstorm §四's frozen list (35 segments / 21 logical positions;
  three convergent scan paths). No re-running of discovery scans after edits begin. Each
  segment is re-confirmed by reading at edit time; segments are identified by **what they
  say**, not by the 2026-08-27 line numbers.
- **Why**: re-scanning a dirty tree absorbs edited files (scope-discipline's exact failure
  mode); but the list's own history (5 missed segments, 3 arithmetic errors — brainstorm
  §4.1a) proves exhaustiveness by keyword search is impossible for "is this sentence
  claiming something happens automatically". The external review chain (§Migration) is the
  compensating control.

## Risks / Trade-offs

- [Risk] The replacement wording itself mints a new false guarantee (happened 8×; twice on
  delivery sentences) → Mitigation: every new/changed sentence passes the D2 test
  (absolute claims need a counter-example hunt first — global CLAUDE.md rule); full review
  chain, no self-review-only close; reviewer explicitly asked to hunt guarantee-shaped wording.
- [Risk] A false-claim segment outside the frozen list survives (translation, case,
  paraphrase escape precise search) → Mitigation: accepted for this change — D7's
  re-confirm-at-edit + external review; the honest statement reduces the harm of any
  stragglers (the master claim they lean on is gone). Residual risk documented, not denied.
- [Risk] zh-TW README drifts from en during the edit (14+14 symmetric segments) →
  Mitigation: edit both languages in the same commit per segment pair; the cross-file
  coupling table in CLAUDE.md already mandates this.
- [Trade-off] Deleting the guarantee without a gate leaves TDD conventional, not enforced →
  Accepted: an honest "not guaranteed" is strictly safer than a false "automatic"; the gate
  is Change 2 with its own necessity argument.
- [Trade-off] `schema.yaml` edits are code-class (review via `/codex-review-fast`, not doc
  review) while the rest is doc-class → Accepted: both planes run; `deeper()` semantics
  mean templates may be reviewed deeper than requested, which is harmless.

## Migration Plan

No deployment. Rollout is:

1. Edit per frozen surface (schema.yaml + both bridge READMEs + retrospective template +
   CLAUDE.md:207 red-flag entry + top-level READMEs line 11).
2. Sync the dogfood copy: `rm -rf openspec/schemas/superpowers-bridge && cp -R
   superpowers-bridge openspec/schemas/`.
3. Local validation: `openspec schema validate superpowers-bridge` + `openspec schemas`
   smoke (per CLAUDE.md's /tmp procedure).
4. Full review chain (no corrective-fix discount): code plane `/codex-review-fast` →
   precommit-equivalent (validate + smoke); doc plane `/codex-review-doc`; Codex probe
   first, fallback chain per auto-loop rules if unavailable; note review-state verdicts.
5. Bundle release: bump `superpowers-bridge/VERSION` patch (1.0.x — wording fix, no schema
   major change); Compatibility table row key `v1` untouched.
6. Rollback: single revert commit (all edits are text; no state).

## Open Questions

None blocking. The three carried in brainstorm §七 are resolved by this design:
executing-plans rationale → D3 (re-verified 2026-08-31); `TDD-via-subagents` → D4;
`templates/plan.md` shell → D6 (explicitly out, corrective-fix scope).

Non-blocking, tracked elsewhere: opening `review-fix-propagation` (user-approved, own
record, no dependency on this change).
