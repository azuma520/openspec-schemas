#!/bin/bash
# Reset fixture: probe-x active, archive empty
P="C:/Users/user/AppData/Local/Temp/claude/C--Users-user-orca-openspec-schemas/88aae4de-4371-4663-80b8-dfe9fac6fb11/scratchpad/c1-hook-probe/proj"
rm -rf "$P/openspec/changes/probe-x" "$P/openspec/changes/archive"
mkdir -p "$P/openspec/changes/archive"
cp -r "C:/Users/user/AppData/Local/Temp/claude/C--Users-user-orca-openspec-schemas/88aae4de-4371-4663-80b8-dfe9fac6fb11/scratchpad/c1-hook-probe/probe-x.bare" "$P/openspec/changes/probe-x"
rm -f "$P/a.sh"
