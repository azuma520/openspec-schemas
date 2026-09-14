## 1. Fixture group

- [x] 1 Add signup validation
  - TDD: applicable
  - RED:
    - subject: test/auth.test.js::rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty email
    - outcome: PASS
  - RED:
    - subject: test/auth.test.js::rejects empty password
    - outcome: FAIL
    - failure: expected 'Password required', got undefined
  - GREEN:
    - subject: test/auth.test.js::rejects empty password
    - outcome: PASS
