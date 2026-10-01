## ADDED Requirements

### Requirement: REQ-3 Concurrent session limit

The service SHALL allow at most five concurrent sessions per user.

#### Scenario: REQ-3-S1 sixth session

- **WHEN** a user opens a sixth concurrent session
- **THEN** the service ends the oldest session
