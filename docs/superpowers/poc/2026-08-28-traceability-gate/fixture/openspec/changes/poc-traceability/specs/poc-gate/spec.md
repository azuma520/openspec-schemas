## ADDED Requirements

### Requirement: REQ-A expired token rejection
The system SHALL reject expired tokens with HTTP 401.

#### Scenario: happy path
- **WHEN** a request carries an expired token
- **THEN** the system responds 401

### Requirement: REQ-B audit log retention
The system SHALL retain audit logs for 90 days.

#### Scenario: retention window
- **WHEN** an audit entry is 90 days old
- **THEN** it is still queryable

### Requirement: REQ-C rate limiting
The system SHALL limit clients to 100 requests per minute.

#### Scenario: over limit
- **WHEN** a client exceeds 100 requests in a minute
- **THEN** further requests receive 429

### Requirement: REQ-D password hashing
The system SHALL hash passwords with bcrypt.

#### Scenario: storage format
- **WHEN** a password is persisted
- **THEN** only a bcrypt hash is stored

### Requirement: REQ-E input validation
The system SHALL validate request payloads against the declared schema.

#### Scenario: malformed payload
- **WHEN** a payload fails schema validation
- **THEN** the request is rejected with 400

### Requirement: REQ-F session timeout
The system SHALL expire idle sessions after 30 minutes.

#### Scenario: idle expiry
- **WHEN** a session is idle for 30 minutes
- **THEN** the next request requires re-authentication
