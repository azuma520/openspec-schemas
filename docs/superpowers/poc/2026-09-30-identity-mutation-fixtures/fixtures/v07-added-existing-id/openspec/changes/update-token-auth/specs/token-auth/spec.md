## ADDED Requirements

### Requirement: REQ-2 Token lifetime

The service SHALL issue access tokens with a lifetime of fifteen minutes.

#### Scenario: REQ-2-S3 issued lifetime

- **WHEN** the service issues an access token
- **THEN** its expiry time is fifteen minutes after issuance
