"""Grade whether required files were actually read, using only exported OTLP log events.

Usage: python grader.py <captures.jsonl> <session_id> <file1> [<file2> ...]

Verdicts (printed as one JSON line):
  READ_ALL   every required file has a successful Read tool_result event in this session
  NOT_READ   the session exported events, but at least one required file has no successful Read
  NO_EVENTS  no event at all for this session -- absence of telemetry is NOT evidence of not reading
"""
import json
import sys


def attrs(lst):
    out = {}
    for a in lst or []:
        v = a.get("value", {})
        out[a.get("key")] = next(iter(v.values()), None) if isinstance(v, dict) and v else None
    return out


def records(path):
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        env = json.loads(line)
        body = env.get("body") or {}
        for rl in body.get("resourceLogs", []):
            res = attrs((rl.get("resource") or {}).get("attributes"))
            for sl in rl.get("scopeLogs", []):
                for lr in sl.get("logRecords", []):
                    a = dict(res)
                    a.update(attrs(lr.get("attributes")))
                    b = lr.get("body") or {}
                    a["_body"] = next(iter(b.values()), None) if isinstance(b, dict) and b else None
                    yield a


def is_tool_result(a):
    name = str(a.get("event.name") or "") + " " + str(a.get("_body") or "")
    return "tool_result" in name


def main():
    path, sid, required = sys.argv[1], sys.argv[2], sys.argv[3:]
    recs = [a for a in records(path) if a.get("session.id") == sid]
    if not recs:
        print(json.dumps({"verdict": "NO_EVENTS", "session": sid}))
        return
    read_ok = set()
    reads = []
    for a in recs:
        if not is_tool_result(a) or a.get("tool_name") != "Read":
            continue
        params = str(a.get("tool_parameters") or "")
        ok = str(a.get("success")).lower() == "true"
        reads.append({"params": params[:200], "success": ok})
        if ok:
            for f in required:
                if f in params:
                    read_ok.add(f)
    missing = [f for f in required if f not in read_ok]
    print(json.dumps({"verdict": "READ_ALL" if not missing else "NOT_READ", "session": sid,
                      "events": len(recs), "read_events": reads, "missing": missing},
                     ensure_ascii=False))


main()
