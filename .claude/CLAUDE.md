# openspec-schemas

> 由 `/install-rules` Phase 4.6 建立（2026-08-27，sd0x-dev-flow 4.3.1）。
> 這份只承載 sd0x 規則引用；本 repo 的工作慣例仍以根目錄 `CLAUDE.md` 為準。

## Required Checks (Stop Hook reminded)

This table constrains the **end state**, not your choreography. How you batch edits, how deep you review, and when you run each gate are yours to choose; what is fixed is that every gate a change class requires has passed *after the last edit in that class*.

| Change Type | Must Run | Can Skip |
|-------------|----------|----------|
| code files | `/codex-review-fast` -> `/precommit` | - |
| `.md` docs | `/codex-review-doc` | `/codex-review-fast` |

Comment-only edits get no free pass: comments can carry compiler/lint/build directives, so edits to code files are conservatively classified as code even when only comments changed.

> **What the Stop Hook actually does** (hook-lightweighting, 2026-08-13): it is a **reminder, not a gate** — it prints which gates the reminder state still shows as owed and always exits 0. Verdicts are recorded via `node scripts/review-state.js note <plane> <pass|fail>` (installed projects: `.claude/scripts/review-state.js`), bound to the tree digest, so an edit re-opens its plane's reminder. What binds is the behaviour layer — the terminal completion invariant in @rules/auto-loop.md. One caveat carried over from the enforcement era still holds: a recorded precommit pass proves the command ran, not which stages existed to run — `/precommit` resolves lint / build / test from whatever your manifest actually defines, and it prints the resolved stages; read them rather than assuming.

Before PR: `/pr-review`

## Workflow

Reference shapes, not scripts — deviate when the change calls for it:

```
Feature: develop -> write tests -> /verify -> /codex-review-fast + /codex-test-review -> /precommit -> /pr-review
Bug fix: /issue-analyze -> /bug-fix -> investigate -> fix -> regression test -> /verify -> /codex-review-fast -> /precommit
```

### Auto-Loop

| After editing... | Review | Then on pass |
|------------------|--------|--------------|
| code files | `/codex-review-fast` | `/precommit` |
| `.md` docs | `/codex-review-doc` | (done) |

The terminal completion invariant, tiers, sub-threshold handling, and sentinels live in @rules/auto-loop.md (highest priority). One reviewer — Codex — by default; when Codex is unavailable, a contract-aware fallback reviewer carries the gate under the same mechanism, fail-closed per family contract (@rules/auto-loop.md § Review Dispatch); `--dual` is `/codex-review-branch` opt-in only.

**What is yours to decide**: the effective tier (escalate above the configured baseline when the change warrants it -- never below), when to batch and when to review, how deep to review, and when 80 is a passing grade rather than another round. **What is not**: the four Anchor corollaries -- Declaring != Executing, Summary != Completion, Fixing != Verifying, and an edit re-opening its own plane's gate. Naming a gate is not running it, and no context or session pressure outranks an open one. Sub-threshold findings are **logged and passed**, not weighed: @rules/auto-loop.md § Sub-Threshold Findings allows exactly two on-the-spot fixes (a one-line fix in a file already open, and a finding whose severity was mis-assigned to something that is really a security or data-integrity defect) -- anything else is a `[DEVIATION]`, not a judgment call.


## Rules

- @rules/discretion.md -- **Read this first**: Anchor / Default / Guidance, the Anchor Register, and how to deviate
- @rules/auto-loop.md -- Auto review loop (highest priority)
- @rules/auto-loop-project.md -- Project-specific auto-loop overrides (user-owned)
- @rules/codex-invocation.md -- Codex must independently research (critical)
- @rules/fix-all-issues.md -- Zero tolerance for blocking findings; sub-threshold ones are logged, not fixed
- @rules/scope-discipline.md -- Scope axis orthogonal to severity; out-of-scope pre-existing defects get a recorded exit, not a repo-wide sweep
- @rules/testing.md -- Test pyramid, conventions, evidence model, adequacy gate
- @rules/testing-project.md -- Project-specific testing overrides (user-owned)
- @rules/framework.md
- @rules/security.md
- @rules/docs-writing.md
- @rules/docs-numbering.md
- @rules/git-workflow.md
- @rules/logging.md
- @rules/self-improvement.md -- Corrected → record → prevent recurrence
- @rules/context-management.md -- Data-driven context monitoring (measure before deciding)
