"""反向對照：逐一裝回壞實作、跑指定測試、記錄轉紅測試名與失敗型別，最後還原。
用法：python mutants.py <group>   group ∈ task1 / task2 / task3
"""
import re
import subprocess
import sys
from pathlib import Path

WT = Path(r"D:\workflow-harness\.claude\worktrees\fix-deferred-verification-resurface")
VP = WT / "hooks" / "lib" / "verification_parser.py"
SS = WT / "hooks" / "session_start.py"

GROUPS = {
    "task1": (["lib/test_verification_parser.py"], [
        ("拿掉 checkbox 護欄", VP, "return (not self.is_checked) and self.deferral_date is not None", "return self.deferral_date is not None"),
        ("延期搜整行", VP, "_DEFERRAL_RE.finditer(mask_code_spans(self.result))", "_DEFERRAL_RE.finditer(mask_code_spans(self.raw_line))"),
        ("拿掉反引號遮罩", VP, "_DEFERRAL_RE.finditer(mask_code_spans(self.result))", "_DEFERRAL_RE.finditer(self.result)"),
        ("只憑字樣判 open", VP, "return (not self.is_checked) and self.deferral_date is not None", "return (not self.is_checked) and \"延期\" in self.result"),
        ("拿掉日期後界", VP, r'(\d{4}-\d{2}-\d{2})(?!\d)")', r'(\d{4}-\d{2}-\d{2})")'),
        ("checkbox 先判", VP, "        if self.is_unfilled:\n            return True\n        return (not self.is_checked)", "        if self.is_checked:\n            return False\n        if self.is_unfilled:\n            return True\n        return (not self.is_checked)"),
    ]),
    "task2": (["lib/test_verification_parser.py", "test_session_start_surface.py"], [
        ("到日條件退回 is_unfilled", VP, "if n.is_open and n.effective_due_date <= today", "if n.is_unfilled and n.due_date <= today"),
        ("排序鍵退回 due_date", VP, "candidates.sort(key=lambda n: (n.effective_due_date, n.line_no))", "candidates.sort(key=lambda n: (n.due_date, n.line_no))"),
        ("顯示退回 due_date", SS, "due=n.effective_due_date.isoformat()", "due=n.due_date.isoformat()"),
    ]),
    "task3": (["lib/test_backlog_triage.py", "lib/test_verification_parser.py"], [
        ("清掃退回 is_unfilled", VP, 'pairs.append((m.group("target").strip(), node.is_open))', 'pairs.append((m.group("target").strip(), node.is_unfilled))'),
    ]),
}


def run(tests):
    r = subprocess.run([sys.executable, "-m", "pytest", *tests, "-q", "-p", "no:cacheprovider", "-rf"],
                       cwd=WT / "hooks", capture_output=True, text=True, encoding="utf-8")
    out = r.stdout + r.stderr
    kinds = sorted(set(re.findall(r"^E\s+(\w+(?:Error|Exception))", out, re.M)))
    failed = [(n, "/".join(kinds)) for n in re.findall(r"FAILED \S+::(\S+)", out)]
    summary = out.strip().splitlines()[-1] if out.strip() else ""
    return failed, summary


tests, mutants = GROUPS[sys.argv[1]]
for label, path, old, new in mutants:
    orig = path.read_text(encoding="utf-8")
    assert orig.count(old) == 1, (label, orig.count(old))
    try:
        path.write_text(orig.replace(old, new), encoding="utf-8", newline="")
        failed, summary = run(tests)
    finally:
        path.write_text(orig, encoding="utf-8", newline="")
    print(f"【{label}】{summary}")
    for name, kind in failed:
        print(f"    紅：{name}  ({kind or '?'})")
failed, summary = run(tests)
print(f"還原後：{summary}")
