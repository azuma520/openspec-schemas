## Why

Requirements and scenarios have no stable identifiers, so nothing can cite them reliably; this change assigns identifiers to every existing requirement and scenario without changing their text.

## What Changes

- Assign `REQ-<n>` to every requirement and `<REQ-ID>-S<m>` to every scenario; keep `REQ-PB`.

## Capabilities

### New Capabilities

### Modified Capabilities

- `token-auth`: assigns identifiers
- `session-policy`: assigns scenario identifiers

## Impact

Spec-only change.
