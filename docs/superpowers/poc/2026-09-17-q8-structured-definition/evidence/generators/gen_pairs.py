import io, os

REPO = 'C:/Users/user/orca/openspec-schemas'
D = REPO + '/docs/superpowers/poc/2026-09-17-q8-structured-definition'
OUT = os.path.dirname(os.path.abspath(__file__)) + '/pairs'
os.makedirs(OUT, exist_ok=True)

# ---- Arm texts -------------------------------------------------------------
arm1_raw = io.open(D + '/arm1-prose-baseline.md', encoding='utf-8').read()
# Arm 1 file wraps the verbatim block in a ```text fence after a meta header.
# Hand the reader ONLY the rule text, with no provenance header.
start = arm1_raw.index('```text\n') + len('```text\n')
end = arm1_raw.rindex('\n```')
ARM1 = '# tasks.md / plan.md 驗證規則\n\n```text\n' + arm1_raw[start:end] + '\n```\n'

ARM2 = io.open(D + '/arm2-structured.md', encoding='utf-8').read()
ARM3 = io.open(D + '/arm3-structured-plus-procedure.md', encoding='utf-8').read()

ARMS = {'A1': ARM1, 'A2': ARM2, 'A3': ARM3}

# ---- Six inputs, materialized as complete (tasks.md, plan.md) pairs --------
# plan.md is minimal and chosen NOT to introduce findings of its own, except
# where plan.md IS the subject of the case (I3, I5).
INPUTS = {}

INPUTS['I1'] = ('''## 1. Group

- [x] 1.1 Foo
  - TDD: applicable
  - RED:
    - subject: a::b
    - subject: c::d
    - outcome: FAIL
    - failure: expected X, got undefined
  - GREEN:
    - subject: a::b
    - outcome: PASS
''', '''## 1.1 — Foo
''')

INPUTS['I2'] = ('''## 1. Group

- [x] 1 Add email validation
  - TDD: applicable
  - RED:
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS
''', '''## 1 — Add email validation
''')

INPUTS['I3'] = ('''## 1. Group

- [x] 1.1 Add email validation
  - TDD: n/a — prose-only
''', '''## 1.1 — Add email validation

### 1.1 — Interface detail
''')

INPUTS['I4'] = ('''## 1. Group

- [x]1.1 Foo
  - TDD: n/a — prose-only
''', '''## 1.1 — Foo
''')

INPUTS['I5'] = ('''## 1. Group

- [x] 1 Add email validation
  - TDD: n/a — prose-only
''', '''## 1x — Add email validation
''')

INPUTS['I6'] = ('''## 1. Group

- [x] 1 Add email validation
  - TDD: applicable
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS

範例（僅供說明，不是真的任務）：

```
- [x] 9 這行只是範例
```
''', '''## 1 — Add email validation
''')

TASK = '''
---

# 你的工作

上面是一份驗證規則。下面是一組待驗的 `tasks.md` 與 `plan.md`。

**只依據上面那份規則**判斷這組輸入的結果，並且**只輸出下面兩行**、不要有任何其他文字：

```
VERDICT: <PASS 或 BLOCK 或 UNDETERMINED>
BASIS: <一句話說明依據>
```

- `PASS` = 依規則沒有任何一條被違反。
- `BLOCK` = 依規則至少有一條被違反。
- `UNDETERMINED` = 規則文字**無法**決定這個輸入該算哪一種。

⚠️ 不要使用任何工具、不要讀取任何檔案、不要搜尋任何程式庫。判斷所需的一切都在本檔內。
'''


def pair_doc(arm_text, tasks_md, plan_md):
    return (arm_text
            + '\n\n---\n\n# 待驗輸入\n\n## `tasks.md`\n\n````markdown\n'
            + tasks_md
            + '````\n\n## `plan.md`\n\n````markdown\n'
            + plan_md
            + '````\n'
            + TASK)


n = 0
for a in ('A1', 'A2', 'A3'):
    for i in ('I1', 'I2', 'I3', 'I4', 'I5', 'I6'):
        t, p = INPUTS[i]
        io.open(f'{OUT}/{a}_{i}.md', 'w', encoding='utf-8', newline='\n').write(
            pair_doc(ARMS[a], t, p))
        n += 1

print('wrote', n, 'pair files to', OUT)
# leak check across every generated file
import glob
bad = []
for f in glob.glob(OUT + '/*.md'):
    s = io.open(f, encoding='utf-8').read()
    for kw in ('Arm 1', 'Arm 2', 'Arm 3', 'expected', 'BLOCK（已定）', 'policy gap'):
        if kw in s:
            bad.append((os.path.basename(f), kw))
print('leak hits:', bad if bad else 'none')
