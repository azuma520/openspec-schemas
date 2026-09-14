# Task 2.3 — PRE-EDIT RED walk (written BEFORE any edit to schema.yaml)

Baseline text walked: commit `22c15cf`, `superpowers-bridge/schema.yaml`, check 7.
Verified byte-identical to the working tree at the time of this walk:

    diff <(git show 22c15cf:superpowers-bridge/schema.yaml | awk '/7\. \*\*Deferred dogfood/,/CHECKS 8-12/') \
         <(awk '/7\. \*\*Deferred dogfood/,/CHECKS 8-12/' superpowers-bridge/schema.yaml)
    -> no output (identical)

Fixture: `docs/superpowers/poc/2026-09-03-tdd-evidence-mutation-fixtures/fixtures/f13-deferred-task-in-tasks`

    plan.md:
      # Fixture plan
      ## 1 — checkout flow staging smoke test

    tasks.md:
      ## 1. Fixture group
      - [~] 1 Verify checkout flow against staging
        - TDD: n/a — manual smoke test, deferred this cycle

## The sentence applied (verbatim from 22c15cf)

    If plan.md has any tasks marked `[~]` deferred (manual smoke /
    dogfood / live-environment checks that weren't run in this
    cycle), enumerate each in verify.md §7 and identify the
    equivalent automated test that covers the same assertions.

and the blocking condition:

    Blocks only if §7 is empty AND plan.md has `[~]` rows (means
    the gap analysis was skipped, not that gaps don't exist).

## Walking it against f13

1. The condition names `plan.md` as the file to search for tasks marked `[~]`.
2. f13's `plan.md` is a conforming v2 plan: a header and one `##` contract entry.
   It contains no `[~]` anywhere, and under the v2 Plan Contract it carries no task
   rows at all, so no conforming v2 plan can ever satisfy this condition.
3. The condition is therefore FALSE. Check 7 enumerates nothing; verify.md §7 may be
   left blank.
4. The blocking condition needs "§7 is empty AND plan.md has `[~]` rows". The second
   conjunct is false, so check 7 does not block either.

ACTUAL verdict under the pre-edit text: **no deferred tasks; §7 may be blank; PASS.**

## Why that is wrong

f13's `tasks.md` holds exactly one genuinely deferred task —
`- [~] 1 Verify checkout flow against staging`, a manual staging smoke test not run
this cycle. That is precisely the situation check 7 is named for. The deferral marker
lives in `tasks.md` because the Plan Contract makes `tasks.md` the carrier of task-level
state; check 7 searches `plan.md`, which by contract can never hold one. The check
reports "no deferred tasks" while a deferred task sits in the change, and the gap
analysis it exists to force is silently skipped.

EXPECTED verdict: check 7 finds ONE deferred task, enumerates it in verify.md §7, and
proceeds to the equivalent-automated-test identification step.
ACTUAL verdict: no deferred tasks found; §7 may be blank; the equivalence step is
never reached.

subject: f13-deferred-task-in-tasks::check 7 finds one deferred task and requires §7 enumeration
