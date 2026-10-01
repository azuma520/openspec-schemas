## ADDED Requirements

### Requirement: REQ-4 Session absolute timeout

The service SHALL end a session eight hours after it started, whatever its activity.

#### Scenario: REQ-4-S1 long session

- **WHEN** a session has been open for eight hours
- **THEN** the service ends the session
