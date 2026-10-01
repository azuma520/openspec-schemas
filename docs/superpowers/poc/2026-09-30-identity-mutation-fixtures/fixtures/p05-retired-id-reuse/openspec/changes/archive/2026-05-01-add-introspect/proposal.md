## Why

Resource servers need to ask whether a token is still active without holding the signing key.

## What Changes

- Add token introspection.

## Capabilities

### New Capabilities

### Modified Capabilities

- `token-auth`: adds introspection

## Impact

Spec-only change.
