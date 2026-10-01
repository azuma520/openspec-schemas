## Why

Clients must re-authenticate every time an access token expires, which interrupts long-running jobs; a refresh path lets them continue without asking the user for credentials again.

## What Changes

- Add token refresh to `token-auth`.
- Add an absolute session lifetime to `session-policy`.

## Capabilities

### New Capabilities

### Modified Capabilities

- `token-auth`: adds token refresh
- `session-policy`: adds an absolute session lifetime

## Impact

Spec-only change.
