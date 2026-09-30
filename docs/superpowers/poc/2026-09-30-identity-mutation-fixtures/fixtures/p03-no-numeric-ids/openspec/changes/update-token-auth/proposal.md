## Why

Idle timeout alone lets a continuously active session live forever; an absolute limit bounds how long a stolen session stays useful.

## What Changes

- Add an absolute session timeout to `session-policy`.

## Capabilities

### New Capabilities

### Modified Capabilities

- `session-policy`: adds absolute timeout

## Impact

Spec-only change.
