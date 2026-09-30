# token-auth Specification

## Purpose

Issue, expire and revoke access tokens for API clients.

## Requirements

### Requirement: REQ-1 Token issuance

The service SHALL issue a signed access token to a client that authenticates with valid credentials.

#### Scenario: REQ-1-S1 valid credentials

- **WHEN** a client presents valid credentials
- **THEN** the service issues a signed access token

#### Scenario: REQ-1-S2 invalid credentials

- **WHEN** a client presents invalid credentials
- **THEN** the service issues no token and answers 401

### Requirement: REQ-2 Token expiry

The service SHALL reject an access token whose expiry time has passed.

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

### Requirement: REQ-5 Token revocation

The service SHALL stop accepting an access token once it has been revoked.

#### Scenario: REQ-5-S1 revoked token

- **WHEN** a client presents a revoked token
- **THEN** the service rejects the request with 401

#### Scenario: REQ-5-S2 revocation by owner

- **WHEN** the token owner revokes the token
- **THEN** the token is revoked immediately

#### Scenario: REQ-5-S3 revocation by administrator

- **WHEN** an administrator revokes the token
- **THEN** the token is revoked immediately

#### Scenario: REQ-5-S4 revocation is idempotent

- **WHEN** a revoked token is revoked again
- **THEN** the service answers success and changes nothing
