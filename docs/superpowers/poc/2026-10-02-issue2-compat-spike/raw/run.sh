#!/usr/bin/env bash
# usage: S=<scratch dir> run.sh <label> <openspec command...>
#   e.g. S=/c/scratch/spike bash run.sh v131 openspec
#        S=/c/scratch/spike bash run.sh v1140 npx -y @fission-ai/openspec@1.14.0
# S must be a scratch directory outside the repo; outputs go to $S/out-<label>.
# The fixture is read from this script's directory; the bridge bundle is copied
# from the repo that contains it (override with REPO=<repo root>).
set -u
LABEL=$1; shift
OS=("$@")
S="${S:?set S to a scratch directory outside the repo}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIX="$HERE/fixture"
REPO="${REPO:-$(git -C "$HERE" rev-parse --show-toplevel)}"
export OPENSPEC_TELEMETRY=0 OPENSPEC_NO_UPDATE_CHECK=1 NO_COLOR=1
OUT="$S/out-$LABEL"; rm -rf "$OUT" "$S/run-$LABEL" "$S/tmp-$LABEL"*; mkdir -p "$OUT"
P="$S/run-$LABEL"; cp -R "$FIX" "$P"; rm -rf "$P/delta"
# git does not keep empty directories; the fixture project needs these two
mkdir -p "$P/openspec/schemas" "$P/openspec/changes"
cp -R "$REPO/superpowers-bridge" "$P/openspec/schemas/"
cd "$P"
r() { # r <name> <args...>  -> stdout/stderr/exit captured separately
  local n=$1; shift
  "${OS[@]}" "$@" >"$OUT/$n.out" 2>"$OUT/$n.err"; echo $? >"$OUT/$n.exit"
}
r 00-version --version
r 01-schema-validate schema validate superpowers-bridge
r 02-schemas schemas
r 03-schemas-json schemas --json
r 04-new-change new change demo --schema superpowers-bridge
ls -A openspec/changes/demo >"$OUT/04b-change-dir.txt" 2>&1; cat openspec/changes/demo/.openspec.yaml >"$OUT/04c-openspec-yaml.txt" 2>&1
r 05-status-empty status --change demo --json
r 06-instr-brainstorm-json instructions brainstorm --change demo --json
r 06b-instr-brainstorm-text instructions brainstorm --change demo
r 07-instr-apply-blocked instructions apply --change demo --json
cp -R "$FIX/delta/." openspec/changes/demo/
r 08-status-full status --change demo --json
r 08b-status-text status --change demo
r 09-instr-apply-json instructions apply --change demo --json
r 09b-instr-apply-text instructions apply --change demo
r 10-instr-verify-json instructions verify --change demo --json
r 10b-instr-retro-json instructions retrospective --change demo --json
r 10c-instr-plan-json instructions plan --change demo --json
r 11-validate-all validate --all --json
r 11b-validate-change-strict validate demo --strict --json
r 12-show-deltas show demo --json --deltas-only
r 13-show-spec show auth --type spec --json
r 14-list-json list --json
r 14b-list list
# archive preview (13.B procedure)
T="$S/tmp-$LABEL-preview"; mkdir -p "$T"; cp -R openspec "$T/"; cd "$T"
r 15-archive-preview archive demo -y
ls -A openspec/changes openspec/changes/archive >"$OUT/15b-after-archive-ls.txt" 2>&1
cp openspec/specs/auth/spec.md "$OUT/15c-candidate-auth-spec.md"
r 15d-show-candidate show auth --type spec --json
# abort case: ADDED collides with existing requirement
T2="$S/tmp-$LABEL-abort"; mkdir -p "$T2"; cp -R "$P/openspec" "$T2/"; cd "$T2"
sed -i 's/### Requirement: REQ-4 Password reset/### Requirement: REQ-1 Login/' openspec/changes/demo/specs/auth/spec.md
r 16-archive-abort archive demo -y
ls -A openspec/changes >"$OUT/16b-after-abort-ls.txt" 2>&1
# real repo openspec tree (dogfood)
T3="$S/tmp-$LABEL-repo"; mkdir -p "$T3"; cp -R "$REPO/openspec" "$T3/"; mkdir -p "$T3/openspec/schemas"; cp -R "$REPO/superpowers-bridge" "$T3/openspec/schemas/"; printf 'schema: superpowers-bridge\n' > "$T3/openspec/config.yaml"; cd "$T3"
r 17-repo-validate-all validate --all --json
r 17b-repo-list-specs list --specs --json
r 17c-repo-show-contract-identity show contract-identity --type spec --json
echo done "$LABEL"
