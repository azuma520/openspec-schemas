## ADDED Requirements

### Requirement: REQ-6 Token introspection

The service SHALL report whether a presented access token is active.

#### Scenario: REQ-6-S1 active token

- **WHEN** a resource server introspects an active token
- **THEN** the service reports it active
