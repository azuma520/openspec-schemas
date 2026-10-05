import sys, json, re, datetime, os
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hook.log")
raw = sys.stdin.read()
try:
    d = json.loads(raw)
except Exception as e:
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().isoformat()}\tPARSE_ERROR\t{e!r}\n")
    sys.exit(0)
cmd = (d.get("tool_input") or {}).get("command", "")
# Simple detector: token "openspec" followed (no shell separator in between) by token "archive"
hit = re.search(r"\bopenspec\b[^;&|\n]*\barchive\b", cmd) is not None
decision = "deny" if hit else "allow"
with open(LOG, "a", encoding="utf-8") as f:
    f.write(f"{datetime.datetime.now().isoformat()}\t{d.get('hook_event_name')}\t{d.get('tool_name')}\t{d.get('permission_mode')}\t{decision}\t{json.dumps(cmd)}\n")
if hit:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "C1-PROBE: openspec archive is blocked by sandbox PreToolUse hook"}}))
sys.exit(0)
