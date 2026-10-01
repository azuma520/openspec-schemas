## MODIFIED Requirements

### Requirement: REQ-7 Token scope

The service SHALL reject a request whose access token lacks the scope the endpoint requires.

#### Scenario: REQ-7-S1 missing scope

- **WHEN** a client calls an endpoint without the required scope
- **THEN** the service rejects the request with 403
