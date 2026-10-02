# auth Specification

## Purpose
Authentication behaviour for the demo project used in the issue #2 compatibility spike.

## Requirements
### Requirement: REQ-1 Login
The system SHALL authenticate users with email and password.

#### Scenario: REQ-1-S1 Valid login
- **WHEN** valid credentials are given
- **THEN** a session is created

### Requirement: REQ-2 Token expiry
The system SHALL expire access tokens after one hour.

#### Scenario: REQ-2-S1 Expired token is rejected
- **WHEN** a token older than one hour is presented
- **THEN** the request is rejected

### Requirement: REQ-3 Legacy logout
The system SHALL support the legacy logout endpoint.

#### Scenario: REQ-3-S1 Legacy logout ends session
- **WHEN** the user calls the legacy logout endpoint
- **THEN** the session ends
