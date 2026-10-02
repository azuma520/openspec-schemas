## ADDED Requirements
### Requirement: REQ-4 Password reset
The system SHALL allow a password reset by email.

#### Scenario: REQ-4-S1 Reset link sent
- **WHEN** a user requests a password reset
- **THEN** a reset link is emailed

## MODIFIED Requirements
### Requirement: REQ-1 Login
The system SHALL authenticate users with email and password and SHALL lock the account after five failures.

#### Scenario: REQ-1-S1 Valid login
- **WHEN** valid credentials are given
- **THEN** a session is created

#### Scenario: REQ-1-S2 Lockout after five failures
- **WHEN** five consecutive logins fail
- **THEN** the account is locked

## RENAMED Requirements
- FROM: `### Requirement: REQ-2 Token expiry`
- TO: `### Requirement: REQ-2 Access token expiry`

## REMOVED Requirements
### Requirement: REQ-3 Legacy logout
**Reason**: Replaced by the standard logout.
**Migration**: Call the standard logout endpoint.
