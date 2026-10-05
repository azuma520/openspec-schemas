#!/bin/bash
P="C:/Users/user/AppData/Local/Temp/claude/C--Users-user-orca-openspec-schemas/88aae4de-4371-4663-80b8-dfe9fac6fb11/scratchpad/c1-hook-probe/proj"
if [ -d "$P/openspec/changes/probe-x" ]; then a1=present; else a1=MISSING; fi
n=$(ls -A "$P/openspec/changes/archive" 2>/dev/null | wc -l)
echo "probe-x=$a1 archive_entries=$n $(ls "$P/openspec/changes/archive" 2>/dev/null | tr '\n' ' ')"
echo "hooklog_lines=$(wc -l < "C:/Users/user/AppData/Local/Temp/claude/C--Users-user-orca-openspec-schemas/88aae4de-4371-4663-80b8-dfe9fac6fb11/scratchpad/c1-hook-probe/hook.log" 2>/dev/null || echo 0)"
