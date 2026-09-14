## 1. Fixture group

- [x] 1.1 Add email validation
  - TDD: applicable
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS
- [x] 1.1 Update the README install section
  - TDD: n/a — prose/doc-only
