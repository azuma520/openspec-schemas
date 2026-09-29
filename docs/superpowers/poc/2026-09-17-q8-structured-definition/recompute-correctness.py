"""依凍結規則重新機械計算 Correctness 的可評集與分母（2026-09-21）。

為什麼存在
----------
原報告寫 Correctness = 15/15，分母是 (I1..I5) × 3 個 Arm。2026-09-21 的文件審指出
該分母撐不住：`inputs-six-cases.md`（凍結）對 I1 明文寫「只答 BLOCK 不算判對」，
要求的是一組 finding；而派工指令只收 VERDICT 一行與 BASIS 一句
（見 `evidence/pairs/*.md` 結尾，以及 `evidence/README.md`）。

本腳本不替報告挑分母，它做的是把判準從凍結檔本文抽出來、逐格套用、印出過程。
執行：
    PYTHONUTF8=1 python recompute-correctness.py
"""

import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# 凍結的事前期望 verdict，逐字出自 inputs-six-cases.md 的「期望判定」欄。
# I6 為「未定」，且 pre-registration.md 明定其 Correctness 不計入。
EXPECTED = {"I1": "BLOCK", "I2": "BLOCK", "I3": "PASS",
            "I4": "BLOCK", "I5": "BLOCK", "I6": None}

# 凍結檔裡「verdict 之外還要答對什麼」的標記句。這些字串逐字出自該檔，
# 不是本腳本的判斷；改動前請先確認凍結檔本文。
EXTRA_MARKERS = ["只答 BLOCK 不算判對", "必答點", "要分兩個量記"]


def load_frozen_sections():
    raw = io.open(os.path.join(HERE, "inputs-six-cases.md"), encoding="utf-8").read()
    parts = re.split(r"(?m)^## (I\d) ", raw)[1:]
    return {parts[i]: parts[i + 1] for i in range(0, len(parts), 2)}


def main():
    sections = load_frozen_sections()
    cells = json.load(io.open(os.path.join(HERE, "evidence", "results.json"),
                              encoding="utf-8"))["cells"]
    arms = ["A1", "A2", "A3"]

    print("步驟 1 — 從凍結檔抽出每個案例的額外要求（字串比對，非判斷）")
    extra = {}
    for cid in EXPECTED:
        hits = [m for m in EXTRA_MARKERS if m in sections[cid]]
        extra[cid] = hits
        print(f"  {cid}: {hits if hits else '無'}")

    print("\n步驟 2 — 逐格比對 verdict 與凍結 expected")
    for cid in EXPECTED:
        row = []
        for a in arms:
            c = cells.get(f"{a}_{cid}")
            v = c["verdict"] if c else "—"
            mark = "" if EXPECTED[cid] is None else ("✓" if v == EXPECTED[cid] else "✗")
            row.append(f"{a}={v}{mark}")
        print(f"  {cid} exp={EXPECTED[cid]}  " + "  ".join(row))

    print("\n步驟 3 — 逐格檢查 BASIS/route 能否承載該案例的額外要求")
    # I1 的凍結要求：恰好兩條 finding（check 9 + check 11），且兩條刻意不報。
    # I4 的凍結要求：兩段式讀法（是 task line／不是 task number）。
    for a in arms:
        r = cells[f"{a}_I1"]["route"]
        has9 = re.search(r"(check\s*9|F9|R6)", r, re.I) is not None
        has11 = re.search(r"(check\s*11|F11)", r, re.I) is not None
        print(f"  I1/{a}: route={r!r}\n        兩條 finding 皆現身? {has9 and has11}"
              f"（check9={has9}, check11={has11}）；兩條『刻意不報』可查證? False（BASIS 只有一句）")
    for a in arms:
        r = cells[f"{a}_I4"]["route"]
        ok = re.search(r"(no task ?num|no TASKNUM|no_number)", r, re.I) is not None
        print(f"  I4/{a}: route={r!r} → 兩段式讀法可查證? {ok}")

    print("\n步驟 4 — 分類")
    evaluable, not_evaluable, excluded = [], [], []
    for cid in ["I1", "I2", "I3", "I4", "I5"]:
        if not extra[cid]:
            evaluable.append(cid)
        elif cid == "I4" and all(
            re.search(r"(no task ?num|no TASKNUM|no_number)", cells[f"{a}_I4"]["route"], re.I)
            for a in arms
        ):
            evaluable.append(cid)  # 額外要求存在，但收到的 route 足以查證它
        else:
            not_evaluable.append(cid)
    excluded.append("I6")

    print(f"  可評   : {evaluable} → {len(evaluable) * 3} 格")
    print(f"  不可評 : {not_evaluable} → {len(not_evaluable) * 3} 格"
          f"（凍結規則要求的證據，派工設計上未收集）")
    print(f"  事前登記排除 : {excluded} → {len(excluded) * 3} 格")

    hit = sum(1 for cid in evaluable for a in arms
              if cells[f"{a}_{cid}"]["verdict"] == EXPECTED[cid])
    print(f"\n結論 — Correctness = {hit}/{len(evaluable) * 3}"
          f"（原報告寫 15/15，分母含 I1 三格）")
    print("⚠️ 這個數字只涵蓋 A1/A2/A3。A0 六格不在 results.json 內，"
          "無同期紀錄，見 evidence/README.md。")


if __name__ == "__main__":
    main()
