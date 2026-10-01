## ADDED Requirements

### Requirement: REQ-10 Token refresh

The service SHALL issue a new access token in exchange for a valid refresh token.

#### Scenario: REQ-10-S1 valid refresh token

- **WHEN** a client presents a valid refresh token
- **THEN** the service issues a new access token

#### Scenario: REQ-10-S2 expired refresh token

- **WHEN** a client presents an expired refresh token
- **THEN** the service issues no token and answers 401
