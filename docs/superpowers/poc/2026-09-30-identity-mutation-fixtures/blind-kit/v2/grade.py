#!/usr/bin/env python3
"""Deterministic grader for blind-kit v2 reports.

Usage:
    python grade.py <report_file> <mapping_file> <readme_answer_key>
    python grade.py --selftest

Standard library only. Parses exactly the two FINAL forms defined in
v2/prompt.md:

    FINAL: PASS
    FINAL: BLOCK | categories=<list>

<list> is a comma-separated, no-space subset of {VIOLATION, UNDETERMINABLE},
each token at most once, non-empty. Any other FINAL form, a missing or
duplicate FINAL line, or an unknown token makes that case NONCONFORMING_OUTPUT
-- never guessed at.

Compares each case's parsed verdict against the answer key's 預期判定 /
預期 BLOCK 類別 for the fixture that case's neutral code maps to (mapping
file), via 違規->VIOLATION, 無法判定->UNDETERMINABLE, 通過->PASS.

Prints one line per fixture: MATCH / DIFF / NONCONFORMING_OUTPUT, and totals.

Fix round 1 (2026-09-30): prompt.md v2 gained a fifth per-check token,
NO_VERDICT, for a non-blocking outcome the check's own rule text does not
make a BLOCK. NO_VERDICT never appears in the FINAL line and never
contributes a category -- this grader reads only the FINAL line and never
inspects per-check tokens, so its FINAL-line grammar (above) is unchanged
by that addition. Confirmed by the "case containing a NO_VERDICT per-check
line" scenario in run_selftest() below.
"""

import re
import sys
from pathlib import Path

ALLOWED_CATEGORY_TOKENS = ("VIOLATION", "UNDETERMINABLE")

CN_TO_EN_CATEGORY = {
    "違規": "VIOLATION",
    "无法判定": "UNDETERMINABLE",  # defensive: simplified variant seen in the wild
    "無法判定": "UNDETERMINABLE",
}

CN_TO_EN_VERDICT = {
    "通過": "PASS",
    "BLOCK": "BLOCK",
}


class NonconformingOutput(Exception):
    """Raised internally when a FINAL line fails strict parsing."""


# --- report parsing -----------------------------------------------------

CASE_HEADER_RE = re.compile(r"^##\s+(\S+)\s*$", re.MULTILINE)

# Strict FINAL forms. Anything not matching one of these two exactly (as a
# whole line, after stripping only the trailing newline) is nonconforming.
FINAL_PASS_RE = re.compile(r"^FINAL: PASS$")
FINAL_BLOCK_RE = re.compile(r"^FINAL: BLOCK \| categories=([^\s]+)$")


def split_report_into_cases(report_text):
    """Return {case_code: block_text} for each '## <case>' section."""
    matches = list(CASE_HEADER_RE.finditer(report_text))
    cases = {}
    for i, m in enumerate(matches):
        code = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(report_text)
        cases[code] = report_text[start:end]
    return cases


def parse_final_line(block_text):
    """Parse the FINAL line(s) of one case block.

    Returns ('PASS', frozenset()) or ('BLOCK', frozenset({...})).
    Raises NonconformingOutput with a reason string on any deviation.
    """
    lines = block_text.splitlines()
    final_lines = [ln for ln in lines if ln.startswith("FINAL:")]

    if len(final_lines) == 0:
        raise NonconformingOutput("missing FINAL line")
    if len(final_lines) > 1:
        raise NonconformingOutput(f"duplicate FINAL line ({len(final_lines)} found)")

    line = final_lines[0]

    if FINAL_PASS_RE.match(line):
        return "PASS", frozenset()

    m = FINAL_BLOCK_RE.match(line)
    if not m:
        raise NonconformingOutput(f"unrecognized FINAL form: {line!r}")

    raw_list = m.group(1)
    if raw_list == "":
        raise NonconformingOutput("empty categories list")

    tokens = raw_list.split(",")
    seen = []
    for tok in tokens:
        if tok not in ALLOWED_CATEGORY_TOKENS:
            raise NonconformingOutput(f"unknown category token: {tok!r}")
        if tok in seen:
            raise NonconformingOutput(f"duplicate category token: {tok!r}")
        seen.append(tok)

    return "BLOCK", frozenset(seen)


# --- mapping file parsing ------------------------------------------------

TABLE_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$")


def parse_mapping(mapping_text):
    """Parse '| 代號 | 原始 fixture |' rows into {case_code: fixture_name}."""
    mapping = {}
    for line in mapping_text.splitlines():
        m = TABLE_ROW_RE.match(line.strip())
        if not m:
            continue
        left, right = m.group(1).strip(), m.group(2).strip()
        if left in ("代號", "") or set(left) == {"-"} or set(right) == {"-"}:
            continue
        if not re.match(r"^case-\S+$", left):
            continue
        mapping[left] = right
    return mapping


# --- README answer-key parsing -------------------------------------------

ANSWER_ROW_RE = re.compile(r"^\|(.+)\|\s*$")


def parse_answer_key(readme_text):
    """Parse the 預期答案表 into {fixture_name: (verdict, categories_frozenset)}.

    verdict is 'PASS' or 'BLOCK'. categories_frozenset uses the English
    tokens (VIOLATION / UNDETERMINABLE), translated from the Chinese labels.
    """
    answers = {}
    lines = readme_text.splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("| fixture") and "預期判定" in line:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("could not locate 預期答案表 header row in README")

    for line in lines[header_idx + 2 :]:  # skip header + '|---|---|' separator
        stripped = line.strip()
        if not stripped.startswith("|"):
            break  # table ended
        m = ANSWER_ROW_RE.match(stripped)
        if not m:
            break
        cells = [c.strip() for c in m.group(1).split("|")]
        if len(cells) < 6:
            continue
        fixture = cells[0]
        verdict_cn = cells[4]
        categories_cn = cells[5]

        if verdict_cn not in CN_TO_EN_VERDICT:
            raise ValueError(f"unrecognized 預期判定 for {fixture!r}: {verdict_cn!r}")
        verdict = CN_TO_EN_VERDICT[verdict_cn]

        cat_body = categories_cn.strip()
        if cat_body.startswith("{") and cat_body.endswith("}"):
            cat_body = cat_body[1:-1].strip()
        categories = set()
        if cat_body:
            for part in cat_body.split(","):
                part = part.strip()
                if not part:
                    continue
                if part not in CN_TO_EN_CATEGORY:
                    raise ValueError(
                        f"unrecognized 預期 BLOCK 類別 token for {fixture!r}: {part!r}"
                    )
                categories.add(CN_TO_EN_CATEGORY[part])

        answers[fixture] = (verdict, frozenset(categories))

    return answers


# --- grading --------------------------------------------------------------


def grade(report_text, mapping_text, readme_text):
    """Return (results, totals) where results is a list of
    (fixture_name, status, detail) sorted by fixture_name, and totals is a
    dict of status -> count."""
    cases = split_report_into_cases(report_text)
    mapping = parse_mapping(mapping_text)
    answers = parse_answer_key(readme_text)

    results = []
    for case_code, fixture in sorted(mapping.items(), key=lambda kv: kv[1]):
        if case_code not in cases:
            results.append(
                (fixture, "NONCONFORMING_OUTPUT", f"case {case_code} missing from report")
            )
            continue

        block_text = cases[case_code]
        try:
            verdict, categories = parse_final_line(block_text)
        except NonconformingOutput as exc:
            results.append((fixture, "NONCONFORMING_OUTPUT", str(exc)))
            continue

        if fixture not in answers:
            results.append(
                (fixture, "NONCONFORMING_OUTPUT", f"no answer-key entry for {fixture!r}")
            )
            continue

        expected_verdict, expected_categories = answers[fixture]
        if verdict == expected_verdict and categories == expected_categories:
            results.append((fixture, "MATCH", ""))
        else:
            results.append(
                (
                    fixture,
                    "DIFF",
                    f"got {verdict} {sorted(categories)} expected {expected_verdict} "
                    f"{sorted(expected_categories)}",
                )
            )

    totals = {"MATCH": 0, "DIFF": 0, "NONCONFORMING_OUTPUT": 0}
    for _, status, _ in results:
        totals[status] += 1
    return results, totals


def print_report(results, totals):
    for fixture, status, detail in results:
        if detail:
            print(f"{fixture}: {status} — {detail}")
        else:
            print(f"{fixture}: {status}")
    print()
    print(
        f"totals: MATCH={totals['MATCH']} DIFF={totals['DIFF']} "
        f"NONCONFORMING_OUTPUT={totals['NONCONFORMING_OUTPUT']} "
        f"(n={sum(totals.values())})"
    )


# --- self-test -------------------------------------------------------------


def run_selftest():
    """Exercise the FINAL-line parser against every case the grader must
    handle: PASS, BLOCK with each category set, a PASS case whose per-check
    lines contain the (per-check-only) NO_VERDICT token, and each
    nonconforming form. Prints each case's classification; asserts
    nonconforming cases are flagged as such and conforming ones are not."""

    cases = [
        ("valid PASS", "FINAL: PASS", ("PASS", frozenset())),
        (
            "valid BLOCK single VIOLATION",
            "FINAL: BLOCK | categories=VIOLATION",
            ("BLOCK", frozenset({"VIOLATION"})),
        ),
        (
            "valid BLOCK single UNDETERMINABLE",
            "FINAL: BLOCK | categories=UNDETERMINABLE",
            ("BLOCK", frozenset({"UNDETERMINABLE"})),
        ),
        (
            "valid BLOCK both categories",
            "FINAL: BLOCK | categories=VIOLATION,UNDETERMINABLE",
            ("BLOCK", frozenset({"VIOLATION", "UNDETERMINABLE"})),
        ),
        (
            "PASS case whose per-check lines include a NO_VERDICT token "
            "(fix round 1: confirms NO_VERDICT is invisible to the FINAL-line "
            "grammar -- it never appears in, or affects parsing of, FINAL)",
            "PRECHECK: NOT_APPLICABLE — git state, not meaningful here\n"
            "5: NO_VERDICT — could not reach a conclusion; rule text does not "
            "block on that basis\n"
            "13: PASS — clean\n\nFINAL: PASS",
            ("PASS", frozenset()),
        ),
        ("missing FINAL line", "13: PASS — ok", None),
        (
            "duplicate FINAL line",
            "FINAL: PASS\nFINAL: BLOCK | categories=VIOLATION",
            None,
        ),
        (
            "unknown token",
            "FINAL: BLOCK | categories=OTHER",
            None,
        ),
        (
            "translated / non-ASCII token",
            "FINAL: BLOCK | categories=違規",
            None,
        ),
        ("empty categories list", "FINAL: BLOCK | categories=", None),
        (
            "space inside categories list",
            "FINAL: BLOCK | categories=VIOLATION, UNDETERMINABLE",
            None,
        ),
        (
            "duplicate token inside list",
            "FINAL: BLOCK | categories=VIOLATION,VIOLATION",
            None,
        ),
        ("placeholder none", "FINAL: BLOCK | categories=(none)", None),
        (
            "old v1 brace form",
            "FINAL: BLOCK categories={違規}",
            None,
        ),
        ("PASS with trailing categories (malformed)", "FINAL: PASS | categories=VIOLATION", None),
    ]

    print("=== grade.py self-test ===")
    failures = []
    for name, block_text, expected in cases:
        try:
            got = parse_final_line(block_text)
            status = "PARSED"
        except NonconformingOutput as exc:
            got = str(exc)
            status = "NONCONFORMING"

        if expected is None:
            ok = status == "NONCONFORMING"
        else:
            ok = status == "PARSED" and got == expected

        marker = "ok" if ok else "FAIL"
        print(f"[{marker}] {name}: {status} -> {got}")
        if not ok:
            failures.append(name)

    print()
    if failures:
        print(f"SELFTEST FAILED: {len(failures)} case(s) did not classify as expected:")
        for name in failures:
            print(f"  - {name}")
        return 1

    print("SELFTEST PASSED: all conforming forms parsed, all nonconforming forms flagged.")
    return 0


# --- entry point -----------------------------------------------------------


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return run_selftest()

    if len(argv) != 4:
        print(__doc__)
        return 2

    report_path, mapping_path, readme_path = argv[1], argv[2], argv[3]
    report_text = Path(report_path).read_text(encoding="utf-8")
    mapping_text = Path(mapping_path).read_text(encoding="utf-8")
    readme_text = Path(readme_path).read_text(encoding="utf-8")

    results, totals = grade(report_text, mapping_text, readme_text)
    print_report(results, totals)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
