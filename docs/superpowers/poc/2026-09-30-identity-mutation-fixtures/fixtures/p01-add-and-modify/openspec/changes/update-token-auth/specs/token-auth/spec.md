## ADDED Requirements

### Requirement: REQ-6 Token refresh

The service SHALL issue a new access token in exchange for a valid refresh token.

#### Scenario: REQ-6-S1 valid refresh token

- **WHEN** a client presents a valid refresh token
- **THEN** the service issues a new access token

#### Scenario: REQ-6-S2 expired refresh token

- **WHEN** a client presents an expired refresh token
- **THEN** the service issues no token and answers 401

## MODIFIED Requirements

### Requirement: REQ-2 Token expiry

The service SHALL reject an access token whose expiry time has passed, allowing no clock-skew grace.

#### Scenario: REQ-2-S1 expired token

- **WHEN** a client presents a token past its expiry time
- **THEN** the service rejects the request with 401

#### Scenario: REQ-2-S2 unexpired token

- **WHEN** a client presents a token before its expiry time
- **THEN** the service accepts the token

#### Scenario: REQ-2-S3 token at the expiry instant

- **WHEN** a client presents a token exactly at its expiry time
- **THEN** the service rejects the request with 401
