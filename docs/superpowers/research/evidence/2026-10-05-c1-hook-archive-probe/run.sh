#!/bin/bash
# usage: run.sh <case-name> <hook|nohook> <permission-args> <prompt>
name="$1"; mode="$2"; perm="$3"; prompt="$4"
S="C:/Users/user/AppData/Local/Temp/claude/C--Users-user-orca-openspec-schemas/88aae4de-4371-4663-80b8-dfe9fac6fb11/scratchpad/c1-hook-probe"
bash "$S/reset.sh"
cp "$S/settings.$mode.json" "$S/proj/.claude/settings.json"
before=$(wc -l < "$S/hook.log" 2>/dev/null || echo 0)
echo "### case=$name settings=$mode perm=$perm" > "$S/logs/$name.meta"
echo "before_hooklog=$before" >> "$S/logs/$name.meta"
cd "$S/proj"
claude -p "$prompt" $perm --output-format stream-json --verbose --max-turns 8 > "$S/logs/$name.jsonl" 2> "$S/logs/$name.stderr"
echo "exit=$?" >> "$S/logs/$name.meta"
bash "$S/oracle.sh" >> "$S/logs/$name.meta"
after=$(wc -l < "$S/hook.log" 2>/dev/null || echo 0)
echo "new_hooklog_lines=$((after-before))" >> "$S/logs/$name.meta"
cat "$S/logs/$name.meta"
