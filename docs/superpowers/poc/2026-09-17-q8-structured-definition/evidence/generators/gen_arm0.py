import io, os, importlib.util, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE + '/pairs'
os.makedirs(OUT, exist_ok=True)

# Reuse the exact INPUTS and TASK text from the round-1 generator so Arm 0
# sees byte-identical inputs and byte-identical instructions.
spec = importlib.util.spec_from_file_location('gp', HERE + '/gen_pairs.py')
gp = importlib.util.module_from_spec(spec)
sys.stdout = io.StringIO()          # suppress gen_pairs' own prints / re-writes
spec.loader.exec_module(gp)
sys.stdout = sys.__stdout__

A, B = 516, 771
src = io.open(HERE + '/schema_prefix.yaml', encoding='utf-8').read().splitlines()
body = '\n'.join(src[A - 1:B])
assert 'CHECKS 8-12' in body.splitlines()[0]
assert 'REVIEW JUDGEMENTS' not in body

ARM0 = '# tasks.md / plan.md 驗證規則\n\n```text\n' + body + '\n```\n'

# archive the arm text alongside the others, for the record
REPO = 'C:/Users/user/orca/openspec-schemas'
D = REPO + '/docs/superpowers/poc/2026-09-17-q8-structured-definition'
io.open(D + '/arm0-prose-prefix.md', 'w', encoding='utf-8', newline='\n').write(
    f'''# Arm 0 — 修正前散文（逐字全文，`e38e817^`）

> `superpowers-bridge/schema.yaml` 在 commit `e38e817` 的**父 commit** 的版本，
> 行 {A}-{B}，逐字複製、未改一字、未裁切。
> 邊界慣例與 Arm 1 相同：起於 `CHECKS 8-12` 標題，止於 `REVIEW JUDGEMENTS` 之前。
> 共 {B - A + 1} 行（修正後的 Arm 1 為 324 行）。
>
> ⚠️ **用途受限**：Arm 0 與 Arm 1 之間**規則內容本身就不同**，不只是表達形式不同。
> 因此 Arm 0 → Arm 1 的任何差異**不得**歸因給「結構化」。它只回答一件事：
> **這六個案例對歷史上真正出問題的規則版本，有沒有辨識力。**

```text
{body}
```
''')

n = 0
for i in ('I1', 'I2', 'I3', 'I4', 'I5', 'I6'):
    t, p = gp.INPUTS[i]
    io.open(f'{OUT}/A0_{i}.md', 'w', encoding='utf-8', newline='\n').write(
        gp.pair_doc(ARM0, t, p))
    n += 1

print('arm0 source lines:', B - A + 1)
print('wrote', n, 'A0 pair files')

# confirm inputs are byte-identical to the round-1 files
import re
for i in ('I1', 'I2', 'I3', 'I4', 'I5', 'I6'):
    a0 = io.open(f'{OUT}/A0_{i}.md', encoding='utf-8').read()
    a1 = io.open(f'{OUT}/A1_{i}.md', encoding='utf-8').read()
    tail0 = a0[a0.index('# 待驗輸入'):]
    tail1 = a1[a1.index('# 待驗輸入'):]
    print(f'  {i}: input+instruction identical to round 1 ->', tail0 == tail1)
