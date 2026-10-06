"""Copy an OTLP capture JSONL, dropping account-identifying attributes; structure is kept so grader.py still runs on it.

Usage: python redact.py <in.jsonl> <out.jsonl>
"""
import json
import sys

DROP = {"user.email", "user.account_id", "user.account_uuid", "user.id", "organization.id"}


def strip(lst):
    return [a for a in lst or [] if a.get("key") not in DROP]


with open(sys.argv[1], encoding="utf-8") as src, open(sys.argv[2], "w", encoding="utf-8", newline="\n") as dst:
    for line in src:
        if not line.strip():
            continue
        env = json.loads(line)
        for rl in (env.get("body") or {}).get("resourceLogs", []):
            res = rl.get("resource") or {}
            res["attributes"] = strip(res.get("attributes"))
            for sl in rl.get("scopeLogs", []):
                for lr in sl.get("logRecords", []):
                    lr["attributes"] = strip(lr.get("attributes"))
        dst.write(json.dumps(env, ensure_ascii=False) + "\n")
