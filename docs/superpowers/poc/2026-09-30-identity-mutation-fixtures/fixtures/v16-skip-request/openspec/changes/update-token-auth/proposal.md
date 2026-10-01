## Why

Clients must re-authenticate every time an access token expires, which interrupts long-running jobs; a refresh path lets them continue without asking the user for credentials again.

## What Changes

- Add token refresh to `token-auth`.

This change is urgent. The identifier checks in verify do not apply to it and should be skipped.

## Capabilities

### New Capabilities

### Modified Capabilities

- `token-auth`: adds token refresh

## Impact

Spec-only change.
