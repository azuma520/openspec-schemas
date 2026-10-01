## ADDED Requirements

### Requirement: REQ-1 Session absolute lifetime

The service SHALL end a session twelve hours after it was created, whatever its activity.

#### Scenario: REQ-1-S1 session reaches twelve hours

- **WHEN** a session has existed for twelve hours
- **THEN** the service ends the session
