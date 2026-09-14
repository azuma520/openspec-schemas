#!/usr/bin/env bash
# Snapshot-based review package for no-commit SDD (ledger R8).
#
# SDD's own scripts/review-package builds a diff from a BASE..HEAD commit range.
# This repo's governance (Anchor Register #4) forbids implementer commits, so
# there is no per-task commit range to diff. Instead the controller snapshots the
# files a task will touch into snapshots/<task>/ before dispatching, and this
# script diffs that snapshot against the working tree afterwards.
#
# Usage:  review-pkg.sh <task-id>            e.g. review-pkg.sh 1.1
# Writes: review-<task-id>.diff   and prints its path.
#
# Snapshot layout: snapshots/<task-id>/<path/with/slashes/preserved>
set -u

WS="$(cd "$(dirname "$0")" && pwd -P)"
ROOT="$(cd "$WS/../../.." && pwd -P)"
TASK="${1:?usage: review-pkg.sh <task-id>}"
SNAP="$WS/snapshots/$TASK"
OUT="$WS/review-$TASK.diff"

[ -d "$SNAP" ] || { echo "no snapshot at $SNAP" >&2; exit 1; }

: > "$OUT"
{
  echo "# Review package — task $TASK"
  echo "# snapshot: $SNAP"
  echo "# worktree: $ROOT"
  echo
  echo "## Files in scope (snapshotted before dispatch)"
} >> "$OUT"

# List snapshotted files, relative to the snapshot root.
( cd "$SNAP" && find . -type f | sed 's|^\./||' ) | sort > "$WS/.pkg-files-$TASK"
sed 's|^|#   |' "$WS/.pkg-files-$TASK" >> "$OUT"

{
  echo
  echo "## Stat"
} >> "$OUT"
while IFS= read -r f; do
  a="$SNAP/$f"; b="$ROOT/$f"
  if [ ! -e "$b" ]; then
    echo "#   $f  DELETED" >> "$OUT"
  else
    # Count with awk, not `grep -c '^+[^+]'`: that pattern requires a second
    # character, so it silently drops every ADDED BLANK LINE. Found by the task
    # 1.1 reviewer — the stat line read +61 -18 for a change git reports as
    # +70 -22 (9 blank additions, 4 blank deletions). A reviewer trusting the
    # stat would mis-size the diff, and nothing errors.
    # NR>2 skips the `--- a/…` / `+++ b/…` header pair.
    add=$(diff -U10 "$a" "$b" 2>/dev/null | awk 'NR>2 && /^\+/ {n++} END {print n+0}')
    del=$(diff -U10 "$a" "$b" 2>/dev/null | awk 'NR>2 && /^-/  {n++} END {print n+0}')
    echo "#   $f  +$add -$del" >> "$OUT"
  fi
done < "$WS/.pkg-files-$TASK"

{
  echo
  echo "## Untracked additions in the worktree (new files this task may have created)"
} >> "$OUT"
( cd "$ROOT" && git status --porcelain --untracked-files=all 2>/dev/null | sed 's|^|#   |' ) >> "$OUT"

{
  echo
  echo "## Diff (snapshot -> working tree, 10 lines of context)"
  echo
} >> "$OUT"
while IFS= read -r f; do
  a="$SNAP/$f"; b="$ROOT/$f"
  [ -e "$b" ] || b=/dev/null
  diff -U10 -L "a/$f" -L "b/$f" "$a" "$b" >> "$OUT" 2>/dev/null
done < "$WS/.pkg-files-$TASK"

rm -f "$WS/.pkg-files-$TASK"
echo "$OUT"
