#!/usr/bin/env bash
# PROTOTYPE: extract one Plan Contract entry (`## <task number> — title`) into OUTFILE.
# Entry = its `##` heading up to the next `#`/`##` heading outside a code fence.
set -euo pipefail
[ $# -eq 3 ] || { echo "usage: bridge-task-brief PLAN_FILE TASK_NUMBER OUTFILE" >&2; exit 2; }
plan=$1 n=$2 out=$3
[ -f "$plan" ] || { echo "no such plan file: $plan" >&2; exit 2; }
awk -v n="$n" '
  /^```/ { infence = !infence }
  !infence && /^##?[ \t]/ {
    key = ""
    if ($0 ~ /^##[ \t]+[0-9]+(\.[0-9]+)*([ \t]|$)/) { s=$0; sub(/^##[ \t]+/, "", s); split(s, a, /[ \t]/); key = a[1] }
    on = (key != "" && (key "") == (n ""))
  }
  on { print }
' "$plan" > "$out"
[ -s "$out" ] || { echo "entry ${n} not found in ${plan}" >&2; rm -f "$out"; exit 3; }
echo "wrote ${out}: $(wc -l < "$out" | tr -d ' ') lines"
