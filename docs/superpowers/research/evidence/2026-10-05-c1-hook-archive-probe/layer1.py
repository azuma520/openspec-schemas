import json, subprocess, os, sys
S = os.path.dirname(os.path.abspath(__file__))
cases = [
 ("plain -y", "openspec archive probe-x -y", "block"),
 ("--yes", "openspec archive probe-x --yes", "block"),
 ("flags before name", "openspec archive -y --skip-specs probe-x", "block"),
 ("npx", "npx @fission-ai/openspec archive probe-x -y", "block"),
 ("cd &&", "cd /some/dir && openspec archive -y probe-x", "block"),
 ("bash -c", "bash -c \"openspec archive probe-x -y\"", "block"),
 ("script file", "./a.sh", "block"),
 ("env var indirection", "C=archive; openspec $C probe-x -y", "block"),
 ("variable for binary", "O=openspec; $O archive probe-x -y", "block"),
 ("quoted subcommand", "openspec 'archive' probe-x -y", "block"),
 ("char split", "openspec arch''ive probe-x -y", "block"),
 ("node direct", "node \"$(npm root -g)/@fission-ai/openspec/bin/openspec.js\" archive probe-x -y", "block"),
 ("manual mv", "mv openspec/changes/probe-x openspec/changes/archive/2026-10-05-probe-x", "block"),
 ("newline separated", "true\nopenspec archive probe-x -y", "block"),
 ("benign: openspec list", "openspec list", "allow"),
 ("benign: echo string", "echo \"openspec archive\"", "allow"),
 ("benign: git log grep", "git log --grep archive", "allow"),
 ("benign: openspec --help archive mention", "openspec list --json | grep archive", "allow"),
]
os.environ["C1_LAYER"]="1"
rows=[]
for name, cmd, want in cases:
    payload={"session_id":"layer1","hook_event_name":"PreToolUse","tool_name":"Bash","permission_mode":"layer1","tool_input":{"command":cmd},"cwd":S}
    r=subprocess.run([sys.executable, os.path.join(S,"hook.py")], input=json.dumps(payload), capture_output=True, text=True)
    got = "deny" if '"deny"' in r.stdout else "allow"
    ok = (got=="deny")==(want=="block")
    rows.append((name, cmd, want, got, "OK" if ok else ("MISS(slip)" if want=="block" else "FALSE-POSITIVE")))
for r in rows: print(" | ".join([r[0], json.dumps(r[1]), r[2], r[3], r[4]]))
