#!/usr/bin/env bash
# Extra cases run after run.sh (2026-10-02 spike). Reconstructed from the
# commands executed in the spike session; outputs listed in SUMMARY.md.
# Prerequisite: run.sh has already been run for both labels, so that
# "$S/run-<label>/openspec" holds the fixture project with change `demo`.
# usage: S=<same scratch dir as run.sh> extra-cases.sh <label> <openspec command...>
#   e.g. S=/c/scratch/spike bash extra-cases.sh v131 openspec
#        S=/c/scratch/spike bash extra-cases.sh v1140 npx -y @fission-ai/openspec@1.14.0
# Needs git (20-init runs `git init`) and python (18-synced).
set -u
LABEL=$1; shift
OS=("$@")
S="${S:?set S to the scratch directory used by run.sh}"
OUT="$S/out-$LABEL"
export OPENSPEC_TELEMETRY=0 OPENSPEC_NO_UPDATE_CHECK=1 NO_COLOR=1 OPENSPEC_NO_ANIMATION=1

# 18-conflict: main spec already holds REQ-4 with DIFFERENT text -> archive must abort (O18)
# 18-synced:   main spec already holds the ADDED block verbatim (early sync)          (O19)
for c in conflict synced; do
  T="$S/x18-$LABEL-$c"; mkdir -p "$T"; cp -R "$S/run-$LABEL/openspec" "$T/"; cd "$T"
  if [ "$c" = conflict ]; then
    printf '\n### Requirement: REQ-4 Password reset\nThe system SHALL do something different.\n\n#### Scenario: REQ-4-S1 Other\n- **WHEN** x\n- **THEN** y\n' >> openspec/specs/auth/spec.md
  else
    PYTHONUTF8=1 python -c "
import io
d=io.open('openspec/changes/demo/specs/auth/spec.md',encoding='utf-8').read()
blk=d.split('## ADDED Requirements\n',1)[1].split('\n## ',1)[0]
io.open('openspec/specs/auth/spec.md','a',encoding='utf-8').write('\n'+blk.strip()+'\n')"
  fi
  "${OS[@]}" archive demo -y > "$OUT/18-$c.out" 2>&1; echo $? > "$OUT/18-$c.exit"
done

# 19-h3-scenario: an ADDED requirement whose scenario is written at level 3 (O15)
T="$S/x19-$LABEL"; mkdir -p "$T"; cp -R "$S/run-$LABEL/openspec" "$T/"; cd "$T"
mkdir -p openspec/changes/h3/specs/auth
printf 'schema: superpowers-bridge\n' > openspec/changes/h3/.openspec.yaml
printf '## ADDED Requirements\n### Requirement: REQ-5 Audit log\nThe system SHALL write an audit log entry on login.\n\n### Scenario: REQ-5-S1 Entry written\n- **WHEN** a user logs in\n- **THEN** an entry is written\n' > openspec/changes/h3/specs/auth/spec.md
"${OS[@]}" validate h3 --json > "$OUT/19-h3-scenario.out" 2> "$OUT/19-h3-scenario.err"; echo $? > "$OUT/19-h3-scenario.exit"

# 20-status-planonly: artifacts up to plan exist, verify/retrospective not yet (O24)
T="$S/x20-$LABEL"; mkdir -p "$T"; cp -R "$S/run-$LABEL/openspec" "$T/"; cd "$T"
mv openspec/changes/demo/verify.md "$S/x20-$LABEL-verify.bak"
mv openspec/changes/demo/retrospective.md "$S/x20-$LABEL-retro.bak"
"${OS[@]}" status --change demo > "$OUT/20-status-planonly.out" 2>&1; echo $? > "$OUT/20-status-planonly.exit"
"${OS[@]}" status --change demo --json > "$OUT/20b-status-planonly.json" 2>/dev/null
"${OS[@]}" instructions apply --change demo --json > "$OUT/20c-apply-planonly.json" 2>/dev/null

# 20-init: generated /opsx commands and openspec-* skills (O10)
D="$S/init-$LABEL"; mkdir -p "$D"; cd "$D"; git init -q .
"${OS[@]}" init --tools claude > "$OUT/20-init.out" 2>&1 < /dev/null; echo $? > "$OUT/20-init.exit"

# 1.14.0 only (run in the repo-copy prepared by run.sh as tmp-<label>-repo):
#   openspec validate --archived  > 19-repo-validate-archived.out
#   openspec list --archived      > 19b-list-archived.out
echo done "$LABEL"
