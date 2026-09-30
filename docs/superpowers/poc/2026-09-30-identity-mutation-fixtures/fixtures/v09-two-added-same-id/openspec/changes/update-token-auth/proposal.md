## Why

Clients must re-authenticate every time an access token expires, which interrupts long-running jobs; a refresh path lets them continue without asking the user for credentials again. Resource servers also need to check whether a token is active.

## What Changes

- Add token refresh.
- Add token introspection.

## Capabilities

### New Capabilities

### Modified Capabilities

- `token-auth`: adds refresh and introspection

## Impact

Spec-only change.
