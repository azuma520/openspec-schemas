## 1. Fixture group

- [x] 1 Add email validation
  - TDD: applicable
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/signup.test.js::rejects empty email
    - outcome: PASS
- [x] 2 Update the README install section
  - TDD: n/a — prose/doc-only
