## 1. Fixture group

- [x] 1 Add email validation
  - TDD: applicable
  - RED:
    - subject: rejects empty email
    - outcome: FAIL
    - failure: expected 'Email required', got undefined
  - GREEN:
    - subject: rejects empty email
    - outcome: PASS
