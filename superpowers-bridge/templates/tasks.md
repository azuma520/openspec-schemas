<!--
每個任務的編號（1.1、1.2、2.1…）也是 templates/plan.md 對應 entry 的
key——verify 的 check 12 分兩階段比對：先確認任一邊都沒有重複的 key
（同一個編號出現兩次就是 BLOCK，訊息與「少一個 / 多一個」不同），
再把兩邊化為集合、雙向比對必須完全相同。這份範例的任務編號集合
{1.1, 1.2, 2.1} 刻意對齊 templates/plan.md 範例的 entry key 集合，
不是各自獨立的示範。
-->

## 1. <!-- Task Group Name -->

- [ ] 1.1 <!-- Task description -->
  - TDD: applicable
- [ ] 1.2 <!-- Task description -->
  - TDD: n/a — <!-- reason, e.g. configuration / prose-only / generated code -->

## 2. <!-- Task Group Name -->

<!--
每個任務都必須帶 TDD 適用性標註（縮排在 checkbox 底下）。
`TDD: applicable` 的任務，完成時要在同一層級補上 RED / GREEN 紀錄——
下面這個範例區塊是規格明文規定的形狀（normative），照抄鍵名、巢狀與縮排，
只換內容值——會變的不只是值，**紀錄的組數也會變**：組數跟著該任務的
subject 數走。

紀錄以 `subject:` 的**值**配對，不看順序、不看位置（第 n 筆 RED 配第 n 筆
GREEN 是明文禁止的）。一個任務可以帶**多個 subject**：該任務底下出現的
每一個 subject 值，恰好一筆 RED 與一筆 GREEN；同一側（RED 之間、GREEN
之間）不得出現重複的 subject 值。下面刻意示範兩個 subject 讓多 subject
的形狀明確——只有一個 subject 的任務就寫一組 RED/GREEN，同樣合規；
重跑測試不會多一筆紀錄（一個 subject 永遠一 RED 一 GREEN）。

`subject:` 的文法：去掉頭尾空白後，值裡**恰好出現一次** `::`，且左右兩側
去空白後都非空。除此之外不限制——路徑寫法、副檔名、測試名稱的字元都不管
（`tests/api_test.go::TestRejectsEmptyEmail/subcase-2` 合規）。

`- RED:` 必須有 `subject:`、`outcome:`、`failure:`；`- GREEN:` 必須有
`subject:` 與 `outcome:`。GREEN 的 `outcome:` 必須是 `PASS`，RED 的必須是
`PASS` 以外的單一大寫 token（`FAIL` / `ERROR` / `FAILED`）。
`- invocation: <command>`（實際跑過的指令）是**佐證**欄位：建議寫下來以利
重現，但**規格從不要求**。要寫就在該筆紀錄底下、與其他欄位同層級再加一個
`- invocation: <command>`。
-->

- [ ] 2.1 Login error handling
  - TDD: applicable
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS
  - RED:
    - subject: test/auth.test.js::rejects malformed email
    - outcome: FAIL
    - failure: expected 'Email invalid', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects malformed email
    - outcome: PASS
