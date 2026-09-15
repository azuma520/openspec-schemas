# Pilot 2 dispatch snapshot (fix-v2-blocking-defects, /codex-review-branch shape)
dispatched_codex: 2026-09-10T01:5xZ -> failed (quota; reset 13:56 local)
fallback_dispatch: contract-neutral-reviewer (Opus) ~2026-09-10T02:05Z  [REVIEWER_FALLBACK] plane=code_review from=codex to=contract-neutral-reviewer reason=quota
worktree: worktree-loosen-plan HEAD=b07d571fbb99c45856548e093e445fbeb7f64b5e
base: 368d5865ed1f43df8e75f72dd2d475a125c43263 (= a78d45d^)
commits: 9
tree: fd76acc9b64552a518a68c98f8f129169be0da84
worktree_status: 4 lines (untracked handoff 0903/0904/0907/0908 only)
baseline: 36 changed files (git diff --name-only 368d586 HEAD) + 4 untracked handoff
context_shape: Task/Artifact/Change/Downstream/Required assurance + Context mismatch line; Task wording per user edit (scope-included, source proposal §Why)

## r2 (after fixes; uncommitted working tree over HEAD b07d571)
fixed: P2 (reports preserved under docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/ + retrospective citations), schema.yaml:1177 per-subject wording, .gitattributes superpowers-bridge/** eol=lf
blob hashes of changed/new files (git hash-object):
  f409b17a659243b77eef50ade1575aa613b33c92  .gitattributes
  455451f16f1558bb890671341c4d07388763aeb3  superpowers-bridge/schema.yaml
  90ff60a640eaa05c5f2cdc656e63ca8acbbc607b  openspec/changes/fix-v2-blocking-defects/retrospective.md
  c1a2643829d2e397cffd1eda551fe80f30f22783  docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/README.md
  fd04b22c67a0dd3e38d8f1b0ab8d9a0c0882c953  docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/code-rereview-fallback-3.md
  67cc853691f04a8e3921d54c9012f0f6454a224a  docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/codegate-fixes-report.md
fallback r2 dispatch: contract-neutral-reviewer (Opus), same prompt + fixed-snapshot note

## FINAL-ish snapshot for Codex formal review (frozen 2026-09-10T04:22:01Z)
HEAD=b07d571fbb99c45856548e093e445fbeb7f64b5e  base=368d586  worktree branch=worktree-loosen-plan
renormalize: user ran 'git add --renormalize superpowers-bridge/' -> all 14 bundle blobs i/lf; staged templates design/plan/spec are EOL-only (diff --cached --ignore-cr-at-eol lists only schema.yaml)
r2 fixes applied: P1 dogfood re-sync (+5.1/verify.md notes), P2 check10 absent-outcome sentence, P2 R1 INDETERMINATE declared (proposal/delta spec/retrospective), P2 gitattributes enumerated + comment, Nit verify.md 四點->五點
worktree blob hashes (git hash-object of working-tree files):
  dbe8924b4e906832847aaea17cd191b85a807a36  .gitattributes
  a9694ae8411cc780e2216fe3fd6e19bffa2ae0b0  openspec/changes/fix-v2-blocking-defects/proposal.md
  e581ec74d397cafd83249d335c362b7a69351a90  openspec/changes/fix-v2-blocking-defects/retrospective.md
  c25a7b3095203163f1de875052d931bded45f1a9  openspec/changes/fix-v2-blocking-defects/specs/tdd-evidence-contract/spec.md
  72e23a7549af8bf7bc0bc70772fdecbbc069bf9c  openspec/changes/fix-v2-blocking-defects/tasks.md
  31496f019ce2e7d9a5a56d4e6342c33cb61da745  openspec/changes/fix-v2-blocking-defects/verify.md
  83add31943b221b89e7becde66c7c9021590e04e  superpowers-bridge/schema.yaml
  9307fb7adf4943591742be7b50e6e5afc720dc05  superpowers-bridge/templates/design.md
  06c0bf8ca5ae2f7866f0efc28293c84d046eb6a6  superpowers-bridge/templates/plan.md
  206b50b0361fb5b6dbdcf3adfcda45d0de5384f8  superpowers-bridge/templates/spec.md
  67cc853691f04a8e3921d54c9012f0f6454a224a  docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/codegate-fixes-report.md
  fd04b22c67a0dd3e38d8f1b0ab8d9a0c0882c953  docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/code-rereview-fallback-3.md
  c1a2643829d2e397cffd1eda551fe80f30f22783  docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/README.md
dogfood copy: diff -r --strip-trailing-cr rc=0

## r3 snapshot — after Codex r1 fixes (option 甲), frozen 2026-09-10T09:2xZ, HEAD still b07d571
fixed: spec delta :7 "unique within each side of a task" (+plan.md:17); check 12 plan-key delimiter (schema check 12 + plan instruction :353-359); canonical delta record-field-form clause + 2 scenarios; verify.md split command restored + FRESH RERUN (Verified at 2026-09-10 17:03, PASS WITH WARNINGS); retrospective §5 no-fixture row → four rules
USER_SKIPPED ×4: see pilot2-codex-r1-dispositions.md
work-map path reference: NOT fixed pending user decision on legal writer path (no description-edit primitive in work_status_register)
dogfood copy: diff -r --strip-trailing-cr rc=0 after schema edit; openspec schema validate ✓; openspec validate --all 5/5
worktree blob hashes (git hash-object, changed since r2):
  9071051a44c1ac1596460a770c44476b9adba6d9  openspec/changes/fix-v2-blocking-defects/retrospective.md
  2f21f7b6e54f97e2c1eb8245b8812a59ce4d3acc  openspec/changes/fix-v2-blocking-defects/specs/tdd-evidence-contract/spec.md
  5a79b64d388491ad4838776bcdd6f37681806f17  openspec/changes/fix-v2-blocking-defects/plan.md
  4f71d351a1dea09c1615d1c56b685b38275ca13f  openspec/changes/fix-v2-blocking-defects/verify.md
  1ccd8a4c90e78811b209a61b2ec22a65b277c0f0  superpowers-bridge/schema.yaml
unchanged since r2: .gitattributes, proposal.md, tasks.md, templates/{design,plan,spec}.md, review-reports dir (3)

## r4 — after user hand-edit of work-map (2026-09-11 08:2xZ), HEAD still b07d571
user ran sed on workflow-harness/work-map.jsonl: `.superpowers/sdd/plan/code-rereview-fallback-3.md` → `docs/superpowers/retrospectives/2026-09-08-fix-v2-review-reports/code-rereview-fallback-3.md` (only the `name` field of task-20260908-author-surface-gate-alignment changed; all other lines byte-identical to HEAD; verified by JSON parse + line compare)
  ddcdf58a46f8d9cdfe5b2bbfc5ac76bef6c9f501  workflow-harness/work-map.jsonl
all other blobs unchanged since r3.

## r5 — 2026-09-11 15:04 local, after the 乙-case fix round (pending Codex re-review)

Worktree `.claude/worktrees/loosen-plan`, HEAD `b07d571` + uncommitted working tree. Content hashes of the files this round touched:

```
f4440957b339f635e7d425f1db8578750c84aaf6  superpowers-bridge/schema.yaml
cf1d26c62f69f6ee45abcf7c9276d82b299fb3ab  openspec/changes/fix-v2-blocking-defects/design.md
ecc449a73e638ab06a4ae5d85540b34f21fca54e  openspec/changes/fix-v2-blocking-defects/proposal.md
3f20b8d1d8b998e03d698b92b66d8a4df1ff2134  openspec/changes/fix-v2-blocking-defects/brainstorm.md
8f8c17933ea4e567d145903b280e009a4a7c2ba7  openspec/changes/fix-v2-blocking-defects/verify.md
923846bca9ea51b0301f88f33a7266c363f442d4  docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/README.md
```

Post-fix invariants verified at this snapshot: dogfood copy `diff -r --strip-trailing-cr` empty; `openspec schema validate superpowers-bridge` ✓; `openspec validate --all --json` 5/5. `tasks.md` and `plan.md` untouched this round, so neither documented freshness trigger fired.

### r2 re-review dispatch — BLOCKED on Codex quota
Thread `01a08eed-df04-78e3-95b0-608dbd9e6df5`, dispatched 2026-09-11 ~14:5xZ local, failed: *"You've hit your usage limit … try again at 6:18 PM."* Quota resets **18:18 local**. Per the standing user ruling (2026-09-10, reaffirmed 2026-09-11) **no fallback reviewer was dispatched**. This is the 4th quota interruption in this review chain.

The r2 prompt is preserved in the conversation and should be re-sent verbatim via `codex-reply` on thread `01a08eed` after 18:18 — it carries all six `[USER_SKIPPED]` dispositions and the three-item fix summary. If that thread is also dead by then (overnight MCP restarts have killed every thread so far), rotate: record `[THREAD_ROTATED]`, open a new thread with a **first dispatch** (metadata + frozen baseline only, dispositions withheld and reconciled afterwards), exactly as this round did.

### ⚠️ Gate-state reading caution
`review-state.js check` currently reports `code_review: digest_match=true, owed=false`. **That is not a statement about the fixed tree.** The digest is computed over the main checkout, which cannot see worktree edits (the known limitation recorded at `research/2026-09-10-contract-drift-archaeology.md:200`). The true position is: the last reviewer verdict (`⛔ Blocked`, r4) predates this fix round, and **no verdict exists for the current state**. Do not read the slot as permission to proceed, and do not note a pass.
