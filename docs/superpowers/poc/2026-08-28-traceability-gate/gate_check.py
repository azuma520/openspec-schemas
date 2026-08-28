#!/usr/bin/env python3
"""Throwaway PoC validator: traceability + completion gate (Phase 1).

Evidence for docs/superpowers/specs/2026-08-28-concept-poc-traceability-gate-design.md.
Read-only: modifies 0 files. Stdlib only. Not a product; kept unmaintained after the PoC.

Data sources:
- Requirements/Scenarios: `openspec show <change> --json --deltas-only` (CLI JSON is
  authoritative; per Step 0 finding #3 the JSON carries no requirement title names,
  so titles are supplemented by a one-line `### Requirement:` scan, cross-checked
  against the CLI requirement count -- not a Markdown re-parse).
- Task coverage: provisional `- Contracts: <ref>[, <ref>...]` lines in tasks.md.
- Verification results: provisional verification-results.json
  (list of {contract, status, evidence}).

Provisional conventions (PoC only, not a schema):
- Contract ID = first whitespace token of the requirement title (`REQ-A ...` -> `REQ-A`);
  duplicate IDs abort (exit 2).
- A reference may point at a scenario (`REQ-A/happy path`); coverage resolves to the
  requirement (the part before `/`).

Gate per requirement, first failing check wins (fail-closed order):
  NO_TASK -> NO_RESULT -> CONFLICT (PASS+FAIL coexist) -> RESULT_FAIL
  -> EMPTY_EVIDENCE -> PASS.

Exit codes: 0 = gate all-PASS (or, with --expected, all verdicts match);
1 = some BLOCK (or expected mismatch); 2 = integrity error (bad refs, CLI failure).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REQ_TITLE = re.compile(r"^### Requirement:\s*(.+?)\s*$")
CONTRACTS_LINE = re.compile(r"^\s*-\s*Contracts:\s*(.+?)\s*$")
TASK_CHECKBOX = re.compile(r"^\s*-\s*\[[ xX]\]\s")


def die(msg):
    print(f"INTEGRITY ERROR: {msg}")
    sys.exit(2)


def cli_requirement_count(fixture_root, change_id):
    proc = subprocess.run(
        ["openspec", "show", change_id, "--json", "--deltas-only"],
        cwd=fixture_root, capture_output=True, text=True, shell=(sys.platform == "win32"),
    )
    if proc.returncode != 0:
        die(f"openspec show failed: {proc.stderr.strip()}")
    data = json.loads(proc.stdout)
    return sum(len(d.get("requirements", [])) for d in data.get("deltas", []))


def requirement_ids(change_dir, expected_count):
    titles = []
    for spec in sorted(change_dir.glob("specs/*/spec.md")):
        for line in spec.read_text(encoding="utf-8").splitlines():
            m = REQ_TITLE.match(line)
            if m:
                titles.append(m.group(1))
    if len(titles) != expected_count:
        die(f"title scan found {len(titles)} requirements, CLI JSON reports {expected_count}")
    ids = [t.split()[0] for t in titles]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        die(f"duplicate contract IDs: {sorted(dupes)}")
    return dict(zip(ids, titles))


def covered_contracts(change_dir, known_ids):
    covered = set()
    task_indent = None  # indentation of the checkbox a Contracts line may attach to
    for line in (change_dir / "tasks.md").read_text(encoding="utf-8").splitlines():
        m = CONTRACTS_LINE.match(line)
        if m:
            indent = len(line) - len(line.lstrip())
            if task_indent is None or indent <= task_indent:
                die("tasks.md has a Contracts annotation not attached to a task checkbox "
                    "(must be indented deeper than its checkbox; orphan/sibling annotation "
                    f"would fake coverage): {line.strip()!r}")
            for ref in (r.strip() for r in m.group(1).split(",")):
                rid = ref.split("/")[0].strip()
                if rid not in known_ids:
                    die(f"tasks.md references unknown contract: {ref!r}")
                covered.add(rid)
        elif TASK_CHECKBOX.match(line):
            task_indent = len(line) - len(line.lstrip())
        else:
            # any other line (blank, heading, comment, prose) closes the task block
            task_indent = None
    return covered


def load_results(change_dir, known_ids):
    path = change_dir / "verification-results.json"
    results = {}
    if not path.exists():
        return results
    for i, entry in enumerate(json.loads(path.read_text(encoding="utf-8"))):
        if not isinstance(entry, dict):
            die(f"verification-results.json entry #{i} is not an object")
        contract, status, evidence = (entry.get(k) for k in ("contract", "status", "evidence"))
        if not isinstance(contract, str) or not isinstance(status, str):
            die(f"verification-results.json entry #{i}: contract/status must be strings")
        if evidence is None:
            evidence = ""  # absent evidence gates as EMPTY_EVIDENCE, not a crash
        if not isinstance(evidence, str):
            die(f"verification-results.json entry #{i}: evidence must be a string or null")
        rid = contract.split("/")[0].strip()
        if rid not in known_ids:
            die(f"verification-results.json references unknown contract: {contract!r}")
        if status not in ("PASS", "FAIL"):
            die(f"unknown status {status!r} for {rid}")
        results.setdefault(rid, []).append({"contract": contract, "status": status, "evidence": evidence})
    return results


def gate(rid, covered, results):
    if rid not in covered:
        return "BLOCK", "NO_TASK"
    entries = results.get(rid, [])
    if not entries:
        return "BLOCK", "NO_RESULT"
    statuses = {e["status"] for e in entries}
    if statuses == {"PASS", "FAIL"}:
        return "BLOCK", "CONFLICT"
    if "FAIL" in statuses:
        return "BLOCK", "RESULT_FAIL"
    if any(not e["evidence"].strip() for e in entries):
        return "BLOCK", "EMPTY_EVIDENCE"
    return "PASS", "OK"


def main():
    args = sys.argv[1:]
    expected_path = None
    if "--expected" in args:
        i = args.index("--expected")
        expected_path = Path(args[i + 1])
        del args[i:i + 2]
    if len(args) != 2:
        print("usage: gate_check.py <fixture-root> <change-id> [--expected expected.json]")
        sys.exit(2)
    fixture_root = Path(args[0]).resolve()
    change_id = args[1]
    change_dir = fixture_root / "openspec" / "changes" / change_id

    count = cli_requirement_count(fixture_root, change_id)
    ids = requirement_ids(change_dir, count)
    covered = covered_contracts(change_dir, ids)
    results = load_results(change_dir, ids)

    verdicts = {rid: gate(rid, covered, results) for rid in ids}
    print(f"Gate report for change {change_id!r} ({count} requirements via CLI JSON)\n")
    for rid, (verdict, reason) in verdicts.items():
        print(f"  {rid:8s} {verdict:5s} {reason:14s} ({ids[rid]})")

    if expected_path is None:
        blocked = sum(1 for v, _ in verdicts.values() if v == "BLOCK")
        print(f"\nGate: {'PASS' if blocked == 0 else f'BLOCK ({blocked} contract(s) not complete)'}")
        sys.exit(0 if blocked == 0 else 1)

    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    if set(expected) != set(verdicts):
        die("expected table and fixture requirement IDs differ")
    print()
    mismatches = 0
    for rid in ids:
        verdict, reason = verdicts[rid]
        want = expected[rid]
        ok = (verdict == want["verdict"] and reason == want["reason"])
        mismatches += (not ok)
        print(f"  {rid:8s} expected {want['verdict']}/{want['reason']:14s} got {verdict}/{reason:14s} {'MATCH' if ok else 'MISMATCH'}")
    print(f"\nCore Mechanism: {'PASS (6/6 cases correct)' if mismatches == 0 else f'FAIL ({mismatches} case(s) wrong)'}")
    sys.exit(0 if mismatches == 0 else 1)


if __name__ == "__main__":
    main()
