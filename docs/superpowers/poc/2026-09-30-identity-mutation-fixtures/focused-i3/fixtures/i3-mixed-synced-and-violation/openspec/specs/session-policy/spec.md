# session-policy Specification

## Purpose

Keep interactive sessions bounded in time so that an abandoned or stolen session stops being usable.

## Requirements

### Requirement: REQ-PB Session idle timeout

The service SHALL end a session after thirty minutes without activity.

#### Scenario: REQ-PB-S1 idle session

- **WHEN** a session has had no activity for thirty minutes
- **THEN** the service ends the session

#### Scenario: REQ-PB-S2 active session

- **WHEN** a session has activity within thirty minutes
- **THEN** the session stays open

### Requirement: REQ-1 Session absolute lifetime

The service SHALL end a session twelve hours after it was created, whatever its activity.

#### Scenario: REQ-1-S1 session reaches twelve hours

- **WHEN** a session has existed for twelve hours
- **THEN** the service ends the session
