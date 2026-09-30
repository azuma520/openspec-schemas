## Why

Clients must re-authenticate every time an access token expires, which interrupts long-running jobs; a refresh path lets them continue without asking the user for credentials again. Expiry handling is also tightened at the boundary instant.

## What Changes

- Add token refresh to `token-auth`.
- Clarify expiry at the exact expiry instant.

## Capabilities

### New Capabilities

### Modified Capabilities

- `token-auth`: adds token refresh; clarifies expiry

## Impact

Spec-only change.
