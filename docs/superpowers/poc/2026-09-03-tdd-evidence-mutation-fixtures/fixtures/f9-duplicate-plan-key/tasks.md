## 1. Fixture group

- [x] 2.3 Add email validation
  - TDD: applicable
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS
