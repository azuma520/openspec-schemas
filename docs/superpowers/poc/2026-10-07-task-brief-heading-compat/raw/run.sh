#!/usr/bin/env bash
# Re-run the 2026-10-07 task-brief heading spike.
# Usage: bash run.sh <path-to-superpowers>/skills/subagent-driven-development
# Needs: bash, git, awk. Writes only under a fresh temp dir; touches nothing in this repo.
set -uo pipefail
[ $# -eq 1 ] || { echo "usage: bash run.sh <sdd-skill-dir>" >&2; exit 2; }
sdd=$(cd "$1" && pwd) || { echo "no such SDD skill dir: $1" >&2; exit 2; }
[ -f "$sdd/scripts/task-brief" ] && [ -f "$sdd/scripts/sdd-workspace" ] \
  || { echo "not an SDD skill dir (scripts/task-brief, scripts/sdd-workspace missing): $sdd" >&2; exit 2; }
here=$(cd "$(dirname "$0")" && pwd) || exit 1
work=$(mktemp -d) || { echo "mktemp failed" >&2; exit 1; }
cd "$work" || exit 1
git init -q || exit 1
mkdir -p openspec/changes/demo openspec/changes/other
cp "$here/fixture-bridge-form.md" openspec/changes/demo/plan.md
cp "$here/fixture-task-form.md"   openspec/changes/demo/plan-task.md
printf '# Other\n\n## 1.1 — X\nDelivers: X\n' > openspec/changes/other/plan.md

echo "### 1. sdd-workspace (upstream) on two changes whose plans share the basename plan.md"
ws=$(bash "$sdd/scripts/sdd-workspace" openspec/changes/demo/plan.md); echo "demo  -> ${ws##*/.superpowers/sdd/}"
ws2=$(bash "$sdd/scripts/sdd-workspace" openspec/changes/other/plan.md); echo "other -> ${ws2##*/.superpowers/sdd/}"

echo "### 2. upstream task-brief on the current bridge form (## 1.1 — ...)"
bash "$sdd/scripts/task-brief" openspec/changes/demo/plan.md 1.1 "$work/up-bridge.md"; echo "rc=$?"

echo "### 3. upstream task-brief on the Task form (## Task 1.1 — ...)"
for n in 1.1 1.10 1.2 2.1 1 2; do
  bash "$sdd/scripts/task-brief" openspec/changes/demo/plan-task.md "$n" "$work/up-$n.md" >/dev/null; rc=$?
  echo "-- n=$n rc=$rc headings: $(grep -c '^## ' "$work/up-$n.md" 2>/dev/null) :: $(grep '^## ' "$work/up-$n.md" 2>/dev/null | tr '\n' '|')"
done

echo "### 4. prototype adapter (abandoned option B) on the bridge form"
for n in 1.1 1.10 1.2 2.1 1 1.1x; do
  bash "$here/prototype-bridge-task-brief.sh" openspec/changes/demo/plan.md "$n" "$ws/task-$n-brief.md" >/dev/null 2>&1; rc=$?
  echo "-- n=$n rc=$rc headings: $(grep '^## ' "$ws/task-$n-brief.md" 2>/dev/null | tr '\n' '|')"
done
echo "(work dir: $work)"
