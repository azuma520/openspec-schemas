## ADDED Requirements

### Requirement: REQ-6 Token refresh

The service SHALL issue a new access token in exchange for a valid refresh token.

#### Scenario: REQ-6-S1 valid refresh token

- **WHEN** a client presents a valid refresh token
- **THEN** the service issues a new access token

### Requirement: REQ-6 Token introspection

The service SHALL report whether a presented access token is active.

#### Scenario: REQ-6-S2 active token

- **WHEN** a resource server introspects an active token
- **THEN** the service reports it active
