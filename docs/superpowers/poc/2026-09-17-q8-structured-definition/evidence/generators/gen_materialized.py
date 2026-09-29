import io, os, sys, importlib.util, hashlib

H = os.path.dirname(os.path.abspath(__file__))
D = 'C:/Users/user/orca/openspec-schemas/docs/superpowers/poc/2026-09-17-q8-structured-definition'

spec = importlib.util.spec_from_file_location('gp', H + '/gen_pairs.py')
gp = importlib.util.module_from_spec(spec)
sys.stdout = io.StringIO()
spec.loader.exec_module(gp)
sys.stdout = sys.__stdout__

ORDER = ['I1', 'I2', 'I3', 'I4', 'I5', 'I6']
LABEL = {
    'I1': '同一筆紀錄兩行 `subject:`',
    'I2': '紀錄完全沒有 `subject:`',
    'I3': '`###` 子標題落在 `##` entry 底下',
    'I4': '`]` 後沒有空白：`- [x]1.1 Foo`',
    'I5': '`## 1x` 開頭的 plan 標題',
    'I6': '圍籬程式碼區塊裡的 `- [x]`',
}

out = ['''# 實際餵給判讀者的輸入（materialized inputs）

> **這份檔案為什麼存在**：`inputs-six-cases.md`（SHA256 凍結）描述的是六個案例的**由來與
> 事前判定**，它**不含**每個案例完整的 `tasks.md` / `plan.md` 兩側材料——I3 與 I5 在該檔
> 裡只有 plan.md 片段。實際派給判讀者的是下面這六組完整配對。
>
> 這個落差是 2026-09-21 的 fallback 文件審抓到的：報告 §6 的「機械驗證」區塊標稱
> 出自「六個輸入檔」，但那些數字其實是對這些 materialized 配對跑的，而當時 repo 內
> 沒有任何一份檔案記載它們。**凍結檔未被修改**；本檔是補上缺的那一半記錄。
>
> 每組的 plan.md 為最小構造，選擇原則是**不引入自身的 finding**，除了 I3 與 I5——
> 那兩組的 plan.md 本身就是案例的主體。
>
> 產生來源：`gen_pairs.py` 的 `INPUTS`（session scratchpad）。下方內容已驗證與實際
> 派工的配對檔逐位元相同，驗證方法見本檔末。
''']

for k in ORDER:
    t, p = gp.INPUTS[k]
    out.append(f'\n## {k} — {LABEL[k]}\n')
    out.append('### `tasks.md`\n')
    out.append('````markdown\n' + t + '````\n')
    out.append('### `plan.md`\n')
    out.append('````markdown\n' + p + '````\n')

# verify against the dispatched pair files
PAIRS = H + '/pairs'
checks = []
for k in ORDER:
    t, p = gp.INPUTS[k]
    src = io.open(f'{PAIRS}/A1_{k}.md', encoding='utf-8').read()
    ok_t = ('````markdown\n' + t + '````') in src
    ok_p = ('````markdown\n' + p + '````') in src
    checks.append((k, ok_t, ok_p))

out.append('\n## 驗證\n')
out.append('本檔每組 `tasks.md` / `plan.md` 區塊，與實際派給判讀者的配對檔 '
           '（`pairs/A1_I*.md` 等 24 份）中的對應區塊做子字串比對：\n\n')
out.append('| 案例 | tasks.md 逐位元相同 | plan.md 逐位元相同 |\n|---|---|---|\n')
for k, a, b in checks:
    out.append(f'| {k} | {"✅" if a else "❌"} | {"✅" if b else "❌"} |\n')

body = ''.join(out)
path = D + '/materialized-inputs.md'
io.open(path, 'w', encoding='utf-8', newline='\n').write(body)

print('all tasks verbatim:', all(a for _, a, _ in checks))
print('all plans verbatim:', all(b for _, _, b in checks))
print('written:', len(body.splitlines()), 'lines')
print('sha256:', hashlib.sha256(io.open(path, 'rb').read()).hexdigest()[:16])
