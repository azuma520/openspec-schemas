## MODIFIED Requirements

### Requirement: REQ-2 Token expiry

The service SHALL reject an access token whose expiry time has passed, allowing no clock-skew grace.

Integrators writing their own scenarios follow this heading shape:

```markdown
#### Scenario: REQ-2-S9 example quoted heading
```

#### Scenario: REQ-2-S1 expired token

- **WHEN** a client presents a token past its expiry time
- **THEN** the service rejects the request with 401

#### Scenario: REQ-2-S2 unexpired token

- **WHEN** a client presents a token before its expiry time
- **THEN** the service accepts the token

#### Scenario: REQ-2-S3 token at the expiry instant

- **WHEN** a client presents a token exactly at its expiry time
- **THEN** the service rejects the request with 401
