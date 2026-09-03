<!--
每個任務的編號（1.1、1.2、2.1…）也是 templates/plan.md 對應 entry 的
key——verify 會比對 tasks.md 的任務編號集合與 plan.md 的 entry key 集合，
兩邊必須完全相同（1 對 1，雙向）。這份範例的任務編號集合 {1.1, 1.2, 2.1}
刻意對齊 templates/plan.md 範例的 entry key 集合，不是各自獨立的示範。
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
只換內容值：
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
