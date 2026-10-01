## RENAMED Requirements

- FROM: `### Requirement: Token issuance`
- TO: `### Requirement: REQ-1 Token issuance`

- FROM: `### Requirement: Token expiry`
- TO: `### Requirement: REQ-FOO Token expiry`

## MODIFIED Requirements

### Requirement: REQ-1 Token issuance

The service SHALL issue a signed access token to a client that authenticates with valid credentials.

#### Scenario: REQ-1-S1 valid credentials

- **WHEN** a client presents valid credentials
- **THEN** the service issues a signed access token

#### Scenario: REQ-1-S2 invalid credentials

- **WHEN** a client presents invalid credentials
- **THEN** the service issues no token and answers 401

### Requirement: REQ-FOO Token expiry

The service SHALL reject an access token whose expiry time has passed.

#### Scenario: REQ-FOO-S1 expired token

- **WHEN** a client presents a token past its expiry time
- **THEN** the service rejects the request with 401

#### Scenario: REQ-FOO-S2 unexpired token

- **WHEN** a client presents a token before its expiry time
- **THEN** the service accepts the token
