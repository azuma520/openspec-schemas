## MODIFIED Requirements

### Requirement: REQ-PB Session idle timeout

The service SHALL end a session after thirty minutes without activity.

#### Scenario: REQ-PB-S1 idle session

- **WHEN** a session has had no activity for thirty minutes
- **THEN** the service ends the session

#### Scenario: REQ-PB-S2 active session

- **WHEN** a session has activity within thirty minutes
- **THEN** the session stays open
