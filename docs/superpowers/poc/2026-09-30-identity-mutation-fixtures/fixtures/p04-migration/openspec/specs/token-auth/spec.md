# token-auth Specification

## Purpose

Issue, expire and revoke access tokens for API clients.

## Requirements

### Requirement: Token issuance

The service SHALL issue a signed access token to a client that authenticates with valid credentials.

#### Scenario: valid credentials

- **WHEN** a client presents valid credentials
- **THEN** the service issues a signed access token

#### Scenario: invalid credentials

- **WHEN** a client presents invalid credentials
- **THEN** the service issues no token and answers 401

### Requirement: Token expiry

The service SHALL reject an access token whose expiry time has passed.

#### Scenario: expired token

- **WHEN** a client presents a token past its expiry time
- **THEN** the service rejects the request with 401

#### Scenario: unexpired token

- **WHEN** a client presents a token before its expiry time
- **THEN** the service accepts the token
